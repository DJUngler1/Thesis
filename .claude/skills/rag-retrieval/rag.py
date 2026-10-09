#!/usr/bin/env python3
"""Semantische Suche über die geprüften Quellen aus references.bib.

Die Quelldateien (PDF/HTML) werden direkt aus dem Zotero-Speicher gelesen. Welche Datei zu welchem BibTeX-Key gehört,
steht im Feld `file` der Einträge in references.bib. Der Zotero-Speicher wird nur gelesen, nie verändert.

Unterbefehle:
  index   Quellen einlesen und den Index inkrementell aktualisieren (neue/geänderte Dateien, entfernte Einträge löschen)
  query   Die k relevantesten Textstellen zu einer Frage, These oder einem Thema ausgeben
  status  Anzeigen, welche Einträge aus references.bib eine Datei haben und im Index liegen

Aufruf immer über die venv des Skills, z. B.:
  .claude/skills/rag-retrieval/.venv/bin/python .claude/skills/rag-retrieval/rag.py query "..." -k 8
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
REPO_ROOT = SKILL_DIR.parents[2]
BIB_DATEI = REPO_ROOT / "references.bib"
INDEX_DIR = SKILL_DIR / ".index"
SEITEN_DATEI = SKILL_DIR / "seitenzahlen.json"

COLLECTION = "quellen"
# Mehrsprachiges Modell: Fragen auf Deutsch sollen auch englische Quellen finden. bge-m3 hat im Test deutlich
# bessere sprachübergreifende Treffer geliefert als multilingual-e5-base.
MODELL = os.environ.get("RAG_MODELL", "BAAI/bge-m3")
CHUNK_ZEICHEN = 1200
UEBERLAPPUNG = 200
MIN_CHUNK = 300
UNTERSTUETZT = {".pdf", ".txt", ".md", ".html", ".htm"}


# --------------------------------------------------------------------------- Einlesen

def datei_hash(pfad: Path) -> str:
    h = hashlib.sha256()
    with open(pfad, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def autor_jahr(qid: str) -> str:
    """Dateiname = BibTeX-Key aus references.bib (Zotero/Better BibTeX), z. B. 'pereiraCRBenchEvaluatingRealWorld2026'
    -> 'Pereira 2026'. Ältere Namensform 'Autor_Jahr_Titel' wird weiter erkannt."""
    m = re.match(r"([^_]+)_(\d{4})", qid) or re.match(r"([a-z]+)[A-Za-z]*?(\d{4})$", qid)
    return f"{m.group(1).capitalize()} {m.group(2)}" if m else qid


def _bib_feld(block: str, name: str) -> str | None:
    """Inhalt von `name = {...}` aus einem BibTeX-Eintrag (verschachtelte Klammern werden berücksichtigt)."""
    m = re.search(rf"^\s*{name}\s*=\s*\{{", block, re.IGNORECASE | re.MULTILINE)
    if not m:
        return None
    tiefe, i = 1, m.end()
    while i < len(block) and tiefe:
        tiefe += {"{": 1, "}": -1}.get(block[i], 0)
        i += 1
    return block[m.end(): i - 1]


def lese_bib() -> dict[str, list[Path]]:
    """BibTeX-Key -> Dateianhänge laut Feld `file` in references.bib (Zotero/Better BibTeX). Nur Quellen mit Eintrag
    dort sind zitierbar. Pfade stehen als '/pfad/a.pdf;/pfad/b.html' oder als 'Label:/pfad/a.pdf:application/pdf'."""
    if not BIB_DATEI.exists():
        sys.exit(f"{BIB_DATEI.name} nicht gefunden – bitte aus Zotero (Better BibTeX) exportieren.")
    eintraege: dict[str, list[Path]] = {}
    for block in re.split(r"(?m)^(?=@)", BIB_DATEI.read_text(encoding="utf-8", errors="ignore")):
        m = re.match(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", block)
        if not m or m.group(1).lower() in {"comment", "string", "preamble"}:
            continue
        pfade = []
        for teil in re.split(r";(?=\s*(?:/|[^/;:]+:/))", _bib_feld(block, "file") or ""):
            teil = re.sub(r"\\(.)", r"\1", teil.strip())
            pm = re.match(r"^(?:[^/]*:)?(/.*?)(?::[\w.+-]+/[\w.+-]+)?$", teil)
            if pm and Path(pm.group(1)).suffix.lower() in UNTERSTUETZT:
                pfade.append(Path(pm.group(1)))
        eintraege[m.group(2)] = pfade
    return eintraege


def waehle_datei(pfade: list[Path]) -> Path | None:
    """Pro Eintrag eine Datei indexieren, sonst gäbe es doppelte Treffer: bevorzugt PDF, dann HTML-Schnappschuss, dann Text."""
    for gruppe in ((".pdf",), (".html", ".htm"), (".txt", ".md")):
        for pfad in pfade:
            if pfad.suffix.lower() in gruppe and pfad.is_file():
                return pfad
    return None


def lade_quellen() -> dict[str, Path]:
    """BibTeX-Key -> zu indexierende Datei im Zotero-Speicher (nur Einträge, für die eine Datei existiert)."""
    return {k: d for k, p in lese_bib().items() if (d := waehle_datei(p))}


def bereinige(text: str) -> str:
    text = text.replace("­", "")                      # weiche Trennstriche
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)            # Silbentrennung am Zeilenende
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text.strip()


def lies_pdf(pfad: Path) -> list[tuple[dict, str]]:
    """Liefert (Metadaten, Text) je PDF-Seite. PyMuPDF bevorzugt, da pypdf bei manchen Satzsystemen Leerzeichen verliert."""
    seiten = []
    try:
        import pymupdf
        with pymupdf.open(pfad) as doc:
            for i, seite in enumerate(doc, 1):
                seiten.append(({"pdf_seite": i}, seite.get_text("text")))
    except ImportError:
        from pypdf import PdfReader
        for i, seite in enumerate(PdfReader(str(pfad)).pages, 1):
            seiten.append(({"pdf_seite": i}, seite.extract_text() or ""))
    return seiten


def lies_html(pfad: Path) -> list[tuple[dict, str]]:
    """HTML ohne Seitenzahlen: in Abschnitte entlang der Überschriften zerlegen, Abschnittstitel als Fundstelle."""
    t = pfad.read_text(encoding="utf-8", errors="ignore")
    t = re.sub(r"(?s)<(script|style|svg|noscript)[^>]*>.*?</\1>", " ", t)
    t = re.sub(r"(?i)<h[1-6][^>]*>", "\n\u0001", t)
    t = re.sub(r"(?i)<br\s*/?>|</(p|div|li|tr|h[1-6])>", "\n", t)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    abschnitte = []
    for teil in t.split("\u0001"):
        zeilen = [z.strip() for z in teil.splitlines() if z.strip()]
        # Wiederkehrende Bedienelemente der Stack-Overflow-Seite sind für die Suche nur Rauschen.
        zeilen = [z for z in zeilen if not re.match(
            r"^(Download( chart)?|Share|Twitter/X Facebook LinkedIn|I acknowledge that the downloaded file.*)$", z)]
        if not zeilen:
            continue
        titel = zeilen[0][:120]
        abschnitte.append(({"abschnitt": titel}, "\n".join(zeilen)))
    return abschnitte


def lies_text(pfad: Path) -> list[tuple[dict, str]]:
    """.txt/.md: Seitenumbrüche als Formfeed (\\f), wie bei der Plagiatsprüfung."""
    t = pfad.read_text(encoding="utf-8", errors="ignore")
    teile = t.split("\f")
    if len(teile) == 1:
        return [({}, t)]
    return [({"pdf_seite": i}, s) for i, s in enumerate(teile, 1)]


def entferne_kopf_fuss(seiten: list[tuple[dict, str]]) -> list[tuple[dict, str]]:
    """Kopf- und Fußzeilen (Zeilen, die auf vielen Seiten gleich wiederkehren, z. B. Lizenz- oder Ausdruckvermerke)
    und reine Seitenzahlen entfernen. Sie tragen nichts zur Suche bei und erzeugen sonst Schein-Treffer."""
    if len(seiten) < 4:
        return seiten
    def norm(z: str) -> str:
        return re.sub(r"\d+", "#", z.strip())
    haeufigkeit: dict[str, int] = {}
    for _, text in seiten:
        for z in {norm(z) for z in text.splitlines() if z.strip()}:
            haeufigkeit[z] = haeufigkeit.get(z, 0) + 1
    grenze = max(3, int(len(seiten) * 0.4))
    wiederkehrend = {z for z, n in haeufigkeit.items() if n >= grenze and len(z) < 200}
    bereinigt = []
    for meta, text in seiten:
        zeilen = [z for z in text.splitlines()
                  if norm(z) not in wiederkehrend and not re.fullmatch(r"\s*[\divxlc:]{1,8}\s*", z)]
        bereinigt.append((meta, "\n".join(zeilen)))
    return bereinigt


LITERATUR_KOPF = re.compile(r"^\s*(\d+\.?\s*)?(references|bibliography|literatur(verzeichnis)?|quellen(verzeichnis)?)\s*$",
                            re.IGNORECASE)


def markiere_literaturliste(seiten: list[tuple[dict, str]]) -> list[tuple[dict, str]]:
    """Ab der Überschrift 'References'/'Literaturverzeichnis' wird Text als teil='literatur' markiert. Literaturlisten
    ähneln jeder Suchanfrage oberflächlich und verdrängen sonst echte Fundstellen; sie sind standardmäßig ausgeblendet."""
    out, in_liste = [], False
    for meta, text in seiten:
        if in_liste:
            out.append(({**meta, "teil": "literatur"}, text))
            continue
        zeilen = text.splitlines()
        for i, z in enumerate(zeilen):
            if LITERATUR_KOPF.match(z):
                in_liste = True
                out.append(({**meta, "teil": "text"}, "\n".join(zeilen[:i])))
                out.append(({**meta, "teil": "literatur"}, "\n".join(zeilen[i:])))
                break
        else:
            out.append(({**meta, "teil": "text"}, text))
    return out


def lies(pfad: Path) -> list[tuple[dict, str]]:
    endung = pfad.suffix.lower()
    if endung == ".pdf":
        return markiere_literaturliste(entferne_kopf_fuss(lies_pdf(pfad)))
    if endung in (".html", ".htm"):
        return lies_html(pfad)
    return lies_text(pfad)


def zerlege(text: str) -> list[str]:
    """Chunks von ca. CHUNK_ZEICHEN Zeichen mit Überlappung, bevorzugt an Satz- oder Absatzgrenzen geschnitten.
    Chunks überschreiten nie eine Seitengrenze, damit die Seitenangabe eindeutig bleibt."""
    text = bereinige(text)
    if len(text) <= CHUNK_ZEICHEN:
        return [text] if len(text) >= 80 else []
    grenzen: list[tuple[int, int]] = []
    start = 0
    while start < len(text):
        ende = min(start + CHUNK_ZEICHEN, len(text))
        if ende < len(text):
            fenster = text[start + CHUNK_ZEICHEN // 2 : ende]
            schnitt = max(fenster.rfind("\n\n"), fenster.rfind(". "), fenster.rfind(".\n"))
            if schnitt > 0:
                ende = start + CHUNK_ZEICHEN // 2 + schnitt + 1
        # Ein kurzer Rest am Seitenende wird an den vorigen Chunk gehängt statt allein zu stehen.
        if grenzen and ende >= len(text) and ende - start < MIN_CHUNK:
            grenzen[-1] = (grenzen[-1][0], ende)
        else:
            grenzen.append((start, ende))
        if ende >= len(text):
            break
        start = max(ende - UEBERLAPPUNG, start + 1)
    return [s for s in (text[a:b].strip() for a, b in grenzen) if len(s) >= 80]


# --------------------------------------------------------------------------- Seitenzahlen

def lade_seitenzahlen() -> dict:
    if SEITEN_DATEI.exists():
        return {k: v for k, v in json.loads(SEITEN_DATEI.read_text(encoding="utf-8")).items() if not k.startswith("_")}
    return {}


def roemisch(n: int) -> str:
    werte = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"), (90, "xc"),
             (50, "l"), (40, "xl"), (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
    out = ""
    for w, z in werte:
        while n >= w:
            out, n = out + z, n - w
    return out


def gedruckte_seite(qid: str, pdf_seite: int | None, regeln: dict) -> str:
    """Gedruckte Seitenzahl aus seitenzahlen.json. Unbekannt -> '?' (dann im PDF nachsehen, nie raten)."""
    if pdf_seite is None:
        return ""
    r = regeln.get(qid)
    if r is None:
        return "?"
    if r.get("ohne_seitenzahlen"):
        return "—"
    if "roemisch_ab" in r:
        return roemisch(r["roemisch_ab"] + pdf_seite - 1)
    if pdf_seite < r.get("ab_pdf_seite", 1):
        return "?"
    return str(pdf_seite + r.get("offset", 0))


# --------------------------------------------------------------------------- Index

def oeffne_collection():
    import chromadb
    from chromadb.config import Settings
    client = chromadb.PersistentClient(path=str(INDEX_DIR), settings=Settings(anonymized_telemetry=False))
    return client.get_or_create_collection(COLLECTION, metadata={"hnsw:space": "cosine", "modell": MODELL})


_modell = None


def embedde(texte: list[str], art: str) -> list[list[float]]:
    """E5-Modelle erwarten die Präfixe 'query: ' bzw. 'passage: '."""
    global _modell
    if _modell is None:
        from sentence_transformers import SentenceTransformer
        _modell = SentenceTransformer(MODELL)
    if "e5" in MODELL.lower():
        texte = [f"{art}: {t}" for t in texte]
    return _modell.encode(texte, batch_size=16, normalize_embeddings=True, show_progress_bar=False).tolist()


def indexiere(neu_aufbauen: bool = False, leise: bool = False) -> None:
    quellen = lade_quellen()
    col = oeffne_collection()
    if col.metadata.get("modell") != MODELL or neu_aufbauen:
        import chromadb
        from chromadb.config import Settings
        client = chromadb.PersistentClient(path=str(INDEX_DIR), settings=Settings(anonymized_telemetry=False))
        client.delete_collection(COLLECTION)
        col = oeffne_collection()
        print(f"Index neu aufgebaut (Modell: {MODELL}).")

    vorhanden = {}
    alle = col.get(include=["metadatas"])
    for meta in alle["metadatas"]:
        vorhanden[meta["datei"]] = meta["hash"]

    # Indexname = BibTeX-Key + Endung der Zotero-Datei (Zotero vergibt zufällige Ordnernamen).
    dateien = {f"{k}{p.suffix.lower()}": (k, p) for k, p in sorted(quellen.items())}
    namen = set(dateien)

    for datei in set(vorhanden) - namen:
        col.delete(where={"datei": datei})
        print(f"entfernt:     {datei}", file=sys.stderr if leise else sys.stdout)

    for name, (qid, pfad) in dateien.items():
        h = datei_hash(pfad)
        if vorhanden.get(name) == h:
            continue
        if name in vorhanden:
            col.delete(where={"datei": name})
        ids, docs, metas = [], [], []
        for meta_seite, text in lies(pfad):
            for n, chunk in enumerate(zerlege(text)):
                stelle = meta_seite.get("pdf_seite", meta_seite.get("abschnitt", "x"))
                ids.append(f"{name}::{stelle}::{meta_seite.get('teil', 'text')}::{n}")
                docs.append(chunk)
                metas.append({"datei": name, "quelle": qid, "hash": h, "teil": "text", **meta_seite})
        if not docs:
            print(f"WARNUNG:      {name} enthält keinen extrahierbaren Text (Scan? dann OCR nötig)")
            continue
        for i in range(0, len(docs), 64):
            col.add(ids=ids[i:i + 64], documents=docs[i:i + 64], metadatas=metas[i:i + 64],
                    embeddings=embedde(docs[i:i + 64], "passage"))
        print(f"indexiert:    {name} ({len(docs)} Chunks)", file=sys.stderr if leise else sys.stdout)
    if leise:
        return
    print(f"Index aktuell: {len({m['datei'] for m in col.get(include=['metadatas'])['metadatas']})} Quellen, "
          f"{col.count()} Chunks.")


def status() -> None:
    col = oeffne_collection()
    zaehler: dict[str, int] = {}
    for meta in col.get(include=["metadatas"])["metadatas"]:
        zaehler[meta["quelle"]] = zaehler.get(meta["quelle"], 0) + 1
    regeln = lade_seitenzahlen()
    eintraege = lese_bib()
    print(f"Modell: {MODELL}\n")
    print("| BibTeX-Key | Datei im Zotero-Speicher | Chunks | Seitenzählung bekannt |\n|---|---|---|---|")
    offen = 0
    for key, pfade in sorted(eintraege.items()):
        datei = waehle_datei(pfade)
        if datei is None:
            grund = "Datei nicht gefunden" if pfade else "kein Anhang in der Bib"
            print(f"| {key} | NEIN ({grund}) | – | – |")
            continue
        bekannt = "ja" if key in regeln else ("n/a (HTML)" if datei.suffix.lower() in (".html", ".htm") else "nein")
        chunks = zaehler.get(key, "nicht indexiert")
        offen += key not in zaehler
        print(f"| {key} | {datei.suffix.lower()[1:]} | {chunks} | {bekannt} |")
    if not eintraege:
        print("| (references.bib enthält keine Einträge) | | | |")
    if offen:
        print(f"\n{offen} Datei(en) nicht indexiert – `index` ausführen.")


# --------------------------------------------------------------------------- Suche

def suche(frage: str, k: int, quellen: list[str] | None, stichwort: str | None,
          max_pro_quelle: int, min_score: float, als_json: bool, mit_literatur: bool) -> None:
    indexiere(leise=True)  # neue oder geänderte Quellen vor jeder Suche aufnehmen
    col = oeffne_collection()
    if col.count() == 0:
        sys.exit("Index ist leer – zu keinem Eintrag in references.bib wurde eine lesbare Datei im Zotero-Speicher gefunden.")
    where = None
    if quellen:
        passende = sorted({m["quelle"] for m in col.get(include=["metadatas"])["metadatas"]
                           if any(m["quelle"].lower().startswith(q.lower()) for q in quellen)})
        if not passende:
            sys.exit(f"Keine Quelle im Index passt zu: {', '.join(quellen)}")
        where = {"quelle": passende[0]} if len(passende) == 1 else {"quelle": {"$in": passende}}
    if not mit_literatur:
        filt = {"teil": "text"}
        where = filt if where is None else {"$and": [where, filt]}
    where_doc = {"$contains": stichwort} if stichwort else None

    res = col.query(query_embeddings=embedde([frage], "query"), n_results=min(k * 5, col.count()),
                    where=where, where_document=where_doc, include=["documents", "metadatas", "distances"])
    regeln = lade_seitenzahlen()
    treffer, pro_quelle = [], {}
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        score = 1 - dist
        if score < min_score:
            continue
        if pro_quelle.get(meta["quelle"], 0) >= max_pro_quelle:
            continue
        pro_quelle[meta["quelle"]] = pro_quelle.get(meta["quelle"], 0) + 1
        pdf = meta.get("pdf_seite")
        treffer.append({
            "rang": len(treffer) + 1,
            "score": round(score, 3),
            "quelle": meta["quelle"],
            "autor_jahr": autor_jahr(meta["quelle"]),
            "datei": meta["datei"],
            "pdf_seite": pdf,
            "gedruckte_seite": gedruckte_seite(meta["quelle"], pdf, regeln),
            "abschnitt": meta.get("abschnitt"),
            "text": doc,
        })
        if len(treffer) == k:
            break

    if als_json:
        print(json.dumps({"frage": frage, "modell": MODELL, "treffer": treffer}, ensure_ascii=False, indent=2))
        return
    print(f"## Treffer für: {frage}\n")
    if not treffer:
        print(f"Keine Textstelle über der Schwelle (min-score {min_score}). Das ist ein Ergebnis: "
              "In den geprüften Quellen findet sich dazu offenbar nichts Passendes.")
        return
    for t in treffer:
        if t["abschnitt"]:
            fund = f"Abschnitt „{t['abschnitt']}“"
        elif t["pdf_seite"] is None:
            fund = "keine Seitenangabe (Textdatei)"
        else:
            fund = f"PDF-S. {t['pdf_seite']} → gedruckt S. {t['gedruckte_seite']}"
        print(f"### {t['rang']}. {t['autor_jahr']} · {fund} · Score {t['score']}")
        print(f"Datei: `{t['datei']}`\n")
        print("> " + t["text"].replace("\n", "\n> ") + "\n")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="befehl", required=True)
    p_idx = sub.add_parser("index", help="Index inkrementell aktualisieren")
    p_idx.add_argument("--neu", action="store_true", help="Index komplett neu aufbauen")
    sub.add_parser("status", help="Indexierte Quellen anzeigen")
    p_q = sub.add_parser("query", help="Relevante Textstellen suchen")
    p_q.add_argument("frage", help="Frage, These oder Thema (Deutsch oder Englisch)")
    p_q.add_argument("-k", type=int, default=8, help="Anzahl Treffer (Standard 8)")
    p_q.add_argument("--quelle", action="append",
                     help="Nur in dieser Quelle suchen (Präfix, z. B. Pearce_2022); mehrfach möglich")
    p_q.add_argument("--stichwort", help="Nur Chunks, die diesen Text wörtlich enthalten (Groß-/Kleinschreibung zählt)")
    p_q.add_argument("--max-pro-quelle", type=int, default=3, help="Höchstens so viele Treffer je Quelle (Standard 3)")
    p_q.add_argument("--min-score", type=float, default=0.0, help="Treffer unterhalb dieser Ähnlichkeit verwerfen")
    p_q.add_argument("--json", action="store_true", help="Ausgabe als JSON")
    p_q.add_argument("--mit-literaturliste", action="store_true",
                     help="Auch Literaturverzeichnisse der Quellen durchsuchen (standardmäßig ausgeblendet)")
    a = ap.parse_args()

    if a.befehl == "index":
        indexiere(a.neu)
    elif a.befehl == "status":
        status()
    else:
        suche(a.frage, a.k, a.quelle, a.stichwort, a.max_pro_quelle, a.min_score, a.json, a.mit_literaturliste)


if __name__ == "__main__":
    main()
