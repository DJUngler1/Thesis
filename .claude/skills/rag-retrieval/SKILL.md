---
name: rag-retrieval
description: Durchsucht die Quellen aus references.bib (Dateien direkt aus dem Zotero-Speicher) semantisch nach relevanten Textstellen zu einer gegebenen Frage / These / einem Thema. Verwendet ein lokales Embedding-basiertes RAG-System (ChromaDB + sentence-transformers) und gibt die k relevantesten Chunks mit Metadaten zurück.
argument-hint: <Frage, These oder Thema> [optional: Quelle, Anzahl Treffer]
---

# RAG-Retrieval über die geprüften Quellen

Eingabe: `$ARGUMENTS`, also eine Frage, eine These, die belegt werden soll, oder ein Thema, zu dem Material gesucht
wird. Optional kann eine Quelle (BibTeX-Key oder dessen Anfang, z. B. `pereira`) oder die Anzahl der Treffer
angegeben sein.

Pfade sind relativ zum Repo-Root. Skript, venv und Index liegen in `.claude/skills/rag-retrieval/`.

**Einordnung im Ablauf:** Dieser Skill *findet* Textstellen. Er belegt nichts und schreibt keinen Thesis-Text (siehe
`CLAUDE.md`). Der Weg zu einem Zitat in der Thesis ist immer:

1. `rag-retrieval`: Kandidaten finden
2. Fundstelle im Original lesen (Read-Tool mit `pages`) und dem Nutzer mit Seitenangabe vorlegen
3. Der Nutzer liest die Stelle selbst und formuliert den Beleg im eigenen Text (Zitat per Quarto: `@bibtexkey`)

**Quellenbasis:** Es gibt keinen Quellenordner im Projekt. Die Quelldateien liegen im Zotero-Speicher
(`~/Zotero/storage/…`) und werden von dort gelesen. Welche Datei zu welchem BibTeX-Key gehört, steht im Feld `file` der
Einträge in `references.bib` (Better-BibTeX-Export aus Zotero). Indexiert werden also genau die Einträge aus
`references.bib`, nicht die ganze Zotero-Bibliothek. Pro Eintrag wird eine Datei verwendet: bevorzugt das PDF, sonst
der HTML-Schnappschuss. `rag.py status` zeigt für jeden Eintrag, ob eine Datei gefunden wurde.

## Harte Regeln

1. **Treffer sind Hinweise, keine Belege.** Ein Chunk ist maschinell extrahierter Text. Silbentrennung, Spaltensatz,
   Tabellen und Fußnoten können darin verstümmelt sein. Nie direkt aus einem Chunk zitieren und keine Zahl aus einem
   Chunk übernehmen, ohne die Seite im Original gelesen zu haben (Read-Tool mit `pages`).
2. **Nur Einträge aus `references.bib`.** Der Index enthält ausschließlich die vom Nutzer geprüften und über Zotero
   exportierten Quellen. Findet sich nichts, wird
   **nicht** im Web nach Ersatz gesucht und nichts aus dem Gedächtnis ergänzt. Stattdessen die Lücke benennen und
   ggf. einen Quellenvorschlag zur Prüfung machen (in `Quellenvorschlaege.md`).
3. **Kein Treffer ist ein Ergebnis.** Wenn die Quellen eine Aussage nicht stützen, das so berichten. Die Aussage
   nicht so lange umformulieren, bis irgendein Chunk passt. Stellen, die der Aussage widersprechen oder sie
   einschränken, werden genauso berichtet wie stützende.
4. **Seitenzahlen nie raten.** Die Ausgabe nennt PDF-Seite und, falls bekannt, die gedruckte Seite. Steht dort `?`,
   die gedruckte Seite im PDF nachsehen (Kopf- oder Fußzeile). Bei `—` hat die Quelle keine Seitenzahlen, dann wird
   mit Abschnitt zitiert.
5. **Keine Edits** an `Thesis.qmd`, `Exposé.qmd`, `references.bib` und nichts im Zotero-Speicher (nur lesen). Erlaubt sind nur ein neuer Eintrag
   in `seitenzahlen.json`, nachdem die Seitenzählung einer Quelle am PDF geprüft wurde (siehe unten), und Vorschläge
   in `Quellenvorschlaege.md`.

## Einrichtung (einmalig)

```bash
python3 -m venv .claude/skills/rag-retrieval/.venv
.claude/skills/rag-retrieval/.venv/bin/pip install -r .claude/skills/rag-retrieval/requirements.txt
.claude/skills/rag-retrieval/.venv/bin/python .claude/skills/rag-retrieval/rag.py index
```

Voraussetzung: `references.bib` ist aktuell. Dafür in Zotero (Better BibTeX) den Export nach `references.bib` auf
„Keep updated“ stellen, sonst kennt der Skill neue Quellen nicht.

Beim ersten Lauf wird das Embedding-Modell `BAAI/bge-m3` (ca. 2,3 GB) heruntergeladen. Das erste Indexieren aller
Quellen dauert einige Minuten. Danach läuft alles lokal, es werden keine Quelltexte an externe Dienste geschickt.
`.venv/` und `.index/` sind per `.gitignore` vom Repo ausgenommen.

## Ablauf

### 1. Suchanfragen formulieren

Das Modell vergleicht Bedeutungen, nicht Stichworte. **Ganze Aussagesätze treffen deutlich besser als Stichworte.**
„LLMs erzeugen bei der Code-Analyse viele Fehlalarme“ findet passende Stellen eher als „Fehlalarme LLM“.

Pro Aussage zwei bis vier Anfragen stellen:

- die Aussage als deutscher Satz,
- dieselbe Aussage auf Englisch in der Fachsprache der Quellen (z. B. *false positives*, *code review*,
  *vulnerability detection*, *maintainability*, *static analysis*), weil die meisten Quellen englisch sind,
- bei Thesen zusätzlich die **Gegenthese**, um widersprechende Befunde zu finden,
- bei Zahlen die Größe, nach der gesucht wird („Anteil erkannter Sicherheitslücken“), nicht die erwartete Zahl.

### 2. Suche ausführen

```bash
.claude/skills/rag-retrieval/.venv/bin/python .claude/skills/rag-retrieval/rag.py query "<Anfrage>" -k 8 2>/dev/null
```

Vor jeder Suche werden neue Einträge in `references.bib` sowie geänderte oder entfernte Dateien automatisch nachgezogen. `2>/dev/null`
blendet Lade- und Fortschrittsmeldungen aus.

| Option                  | Wirkung                                                                                   |
|-------------------------|-------------------------------------------------------------------------------------------|
| `-k 8`                  | Anzahl der Treffer (Standard 8)                                                           |
| `--quelle pereira`      | nur in dieser Quelle suchen (Präfix des BibTeX-Keys, mehrfach angebbar)                   |
| `--max-pro-quelle 3`    | höchstens so viele Treffer je Quelle (Standard 3). Mit `--quelle` auf z. B. 10 erhöhen    |
| `--stichwort "51.5"`    | nur Chunks, die diesen Text wörtlich enthalten (Groß-/Kleinschreibung zählt)              |
| `--mit-literaturliste`  | auch Literaturverzeichnisse der Quellen durchsuchen, z. B. um zu sehen, wer eine Studie zitiert |
| `--min-score 0.5`       | schwache Treffer verwerfen                                                                |
| `--json`                | maschinenlesbare Ausgabe                                                                  |

Weitere Befehle: `rag.py status` zeigt, welche Dateien indexiert sind und für welche die Seitenzählung bekannt ist.
`rag.py index --neu` baut den Index komplett neu auf und ist nur nötig, wenn das Skript oder das Modell geändert wurde.

### 3. Treffer bewerten

- **Scores sind relativ.** Bei bge-m3 liegen gute Treffer meist zwischen 0,55 und 0,75. Aussagekräftiger als der
  absolute Wert ist der Abstand: Fällt der Score nach den ersten Treffern deutlich ab, sind die übrigen meist nur
  thematisch verwandt.
- Für jeden brauchbaren Treffer die **Seite im Original lesen**. Der Chunk ist oft mitten im Satz abgeschnitten, und
  der Zusammenhang (Stichprobe, Teilgruppe, Einschränkung) steht häufig auf derselben Seite davor oder danach.
- Prüfen, **worauf sich eine Zahl bezieht**. Übersichtsarbeiten berichten oft Ergebnisse *anderer*
  Studien. Dann muss im Text stehen, dass es sich um eine von ihnen ausgewertete Studie handelt.
- Studientyp mitdenken: Preprint (viele Quellen sind arXiv-Preprints), Benchmark, Befragung, Übersichtsarbeit usw.
  Bei Benchmarks außerdem: welche Modelle, welche Sprachen, welche Datensätze.

### 4. Ergebnis im Chat ausgeben

Pro gesuchter Aussage eine kurze Tabelle:

| Quelle | Fundstelle | Bezug zur Aussage | Kernaussage (eigene Worte) | Im Original geprüft |
|--------|------------|-------------------|----------------------------|---------------------|
| Pereira et al. 2026 | S. 4 (PDF 4) | stützt | … | ja / noch nicht |

`Bezug` ist *stützt*, *widerspricht*, *schränkt ein* oder *nur verwandt*. Die Kernaussage wird in eigenen Worten
wiedergegeben, nicht als kopierter Chunk. Darunter kurz festhalten:

- welche Anfragen gestellt wurden,
- ob die Aussage insgesamt **belegt**, **teilweise belegt** oder **nicht belegt** ist,
- welcher Treffer dem Nutzer zum Lesen im Original empfohlen wird (mit Quelle und Seite).

## Seitenzählung neuer Quellen (`seitenzahlen.json`)

Kommt eine neue Quelle in `references.bib`, kennt das Skript ihre gedruckte Seitenzählung nicht und gibt `?` aus. Nach der
Prüfung im PDF (gedruckte Zahl auf zwei, drei Seiten mit der PDF-Seite vergleichen) einen Eintrag ergänzen.
Schlüssel ist der BibTeX-Key:

| Fall | Eintrag |
|------|---------|
| gedruckt = PDF-Seite | `{"offset": 0}` |
| Tagungsband, PDF-S. 1 = S. 754 | `{"offset": 753}` |
| Titelei ohne arabische Zählung, gedruckt S. 1 = PDF-S. 9 | `{"offset": -8, "ab_pdf_seite": 9}` |
| römisch, PDF-S. 1 = S. xiii | `{"roemisch_ab": 13}` |
| keine Seitenzahlen | `{"ohne_seitenzahlen": true}` |

## Gotchas

- **HTML-Quellen** (z. B. arXiv-Snapshots, Webseiten) haben keine Seiten. Die Fundstelle ist die Abschnittsüberschrift, die in der
  Ausgabe steht. Im Beleg wird die Abschnittsnummer aus der Seite verwendet (z. B. „Abschnitt 3.2“).
- **Kopf- und Fußzeilen** (Lizenzvermerke, Normvermerke, Seitenzahlen) werden beim Indexieren
  entfernt. Deshalb kann ein Chunk nicht belegen, auf welcher Seite er steht, die Seite kommt aus den Metadaten.
- **Tabellen und Abbildungen** werden schlecht extrahiert. Zahlen aus Tabellen immer im PDF ablesen und mit Tabellen-
  bzw. Abbildungsnummer belegen.
- **Zweispaltige PDFs** (IEEE, ACM, arXiv) können Absätze in falscher Reihenfolge liefern. Das ist für die Suche meist
  unkritisch, beim Lesen des Chunks aber irritierend.
- **Gescannte PDFs** ohne Textebene meldet `index` mit `WARNUNG`. Sie sind nicht durchsuchbar, bis eine OCR-Fassung
  abgelegt wird. Das dem Nutzer melden.
- `--stichwort` ist ein exakter Textfilter. Englische Quellen schreiben Dezimalzahlen mit Punkt (`51.5`), deutsche
  mit Komma.
- Wird ein BibTeX-Key in Zotero geändert, wird die Quelle beim nächsten Lauf unter dem neuen Key neu indexiert und der
  alte entfernt. Der Eintrag in `seitenzahlen.json` muss dann von Hand angepasst werden.
- **Einträge ohne Datei** (kein Anhang in Zotero, Datei noch nicht synchronisiert) meldet `status` mit „NEIN“. Sie sind
  nicht durchsuchbar. Das dem Nutzer melden.
- Hat ein Eintrag mehrere PDFs (z. B. Zusatzmaterial), wird das erste aus dem Feld `file` verwendet.
