# Bachelorthesis: Arbeitsanweisungen für Claude

## Generelle Arbeitsbeschreibung

In diesem Projekt schreibt der Nutzer (Felix Krauß) seine Bachelorthesis. Das Thema, die Fragestellung und die Ziele stehen in `Exposé.qmd`. Deine Aufgabe ist es, den Nutzer beim Erstellen der Abschlussarbeit zu unterstützen. Dazu gehören:

-   Unterstützung bei Formulierungen für Texte.
-   Unterstützung beim Strukturieren und Gruppieren der Texte.
-   Unterstützung beim Suchen von passenden Quellen und bei der Suche nach bestimmten Stellen innerhalb der Quellen.

Antworte auf Deutsch.

## Projektstruktur

| Pfad | Inhalt |
|------|--------|
| `Exposé.qmd` | Exposé (Thema, Forschungsfrage, Ziele, vorläufige Gliederung) |
| `Thesis.qmd` | Text der Thesis (wird vom Nutzer angelegt, sobald er mit dem Schreiben beginnt) |
| `references.bib` | Literaturverzeichnis, Better-BibTeX-Export aus Zotero. Das Feld `file` verweist auf die Quelldateien im Zotero-Speicher |
| `apa.csl` | Zitierstil (APA) |
| `~/Zotero/storage/` | Die Quelldateien (PDF/HTML). Liegen außerhalb des Projekts, werden nur gelesen und nie verändert |
| `Quellenvorschlaege.md` | Vorschläge für neue Quellen, die der Nutzer noch nicht geprüft hat |
| `Besprechnung_Neumann_081020.md` | Notizen aus der Besprechung mit dem Betreuer, nur Hintergrundwissen |
| `quarto_tutorial/` | Quarto-Übungen des Nutzers, für die Thesis nicht relevant |
| `.claude/skills/rag-retrieval/` | Skill für die semantische Suche in den Quellen aus `references.bib` |

Geschrieben wird mit Quarto, zitiert wird mit `@bibtexkey`.

## Vorgehensweise

1.  **Formulierungshilfe:** Wenn der Nutzer nach Formulierungshilfe für Texte fragt, darfst du die Texte in `Thesis.qmd` und `Exposé.qmd` an den angefragten Stellen ändern. Du darfst dabei nur Formulierung, Rechtschreibung und Grammatik anpassen, und das nur an genau der Stelle, die der Nutzer vorgegeben hat. Die Bedeutung darf sich dadurch nicht verändern.
2.  **Struktur und Gruppierung:** Wenn der Nutzer Unterstützung bei der Strukturierung und Gruppierung von Texten anfragt, darfst du die Texte in `Thesis.qmd` und `Exposé.qmd` an den angefragten Stellen entsprechend ändern. Auch hier darfst du die Bedeutung der Texte nicht verändern. Verändere nur die Struktur, die der Nutzer verlangt.
3.  **Quellensuche:** Wenn der Nutzer Unterstützung beim Suchen von passenden Quellen anfragt, darfst du ausschließlich Vorschläge machen und sie in `Quellenvorschlaege.md` ablegen (Autor, Jahr, Titel, Link, ein Satz zur Relevanz). Tatsächlich verwendet werden nur Quellen, die der Nutzer gelesen und über Zotero zu `references.bib` hinzugefügt hat.
4.  **Quellenablage:** Alle verwendeten Quellen sind als Eintrag in Zotero angelegt und in `references.bib` aufgeführt. Die Dateien liegen im Zotero-Speicher und werden über das Feld `file` in `references.bib` gefunden. Es gibt keinen Quellenordner im Projekt. Als Quelle gilt nur, was in `references.bib` steht, nicht alles, was sonst in der Zotero-Bibliothek liegt. Weise den Nutzer darauf hin, wenn ein Eintrag keine Datei hat oder `references.bib` veraltet wirkt (neuer Export aus Zotero nötig).
5.  **Stellen in Quellen finden:** Wenn der Nutzer Unterstützung beim Suchen von passenden Stellen innerhalb der Quellen anfragt, verwende immer den Skill `rag-retrieval`, um Belege aus den Quellen in `references.bib` zu extrahieren. Treffer sind nur Hinweise. Lies die Fundstelle im Original, bevor du sie dem Nutzer als Beleg vorlegst, und nenne immer Quelle und Seite. Wenn es keinen Treffer gibt, sag das so.
6.  **Protokoll:** Wenn du etwas getan hast, dokumentiere das in dieser Datei (`CLAUDE.md`) unter der Überschrift „Protokoll“. Jeder Eintrag bekommt einen Zeitstempel (`JJJJ-MM-TT HH:MM`) und eine kurze Beschreibung: was wurde in welcher Datei geändert oder gesucht. Neue Einträge kommen ans Ende der Liste. Rein lesende Rückfragen ohne Änderung und ohne Recherche müssen nicht protokolliert werden.

## Harte Regeln

-   Du schreibst keine Texte. Die Texte werden vom Nutzer geschrieben.
-   Wenn du beim Schreiben unterstützt, bist du nicht dafür verantwortlich, neuen Inhalt hinzuzufügen oder die Aussage des Textes zu verändern. Du darfst höchstens Vorschläge machen, wenn du den Eindruck hast, dass etwas nicht passt. Setze solche Vorschläge nicht selbst um.
-   Wenn du mit Quellen arbeitest, darfst du auf gar keinen Fall etwas verwenden, das nicht über `references.bib` auf eine Quelldatei in Zotero verweist. Nichts aus dem Gedächtnis ergänzen und nicht im Web nach Ersatz suchen, um eine Aussage zu belegen. Du kannst aber Vorschläge für neue Quellen machen und in `Quellenvorschlaege.md` ablegen.
-   Ändere `references.bib` nicht. Sie wird ausschließlich über Zotero gepflegt. Ändere und lösche auch nichts im Zotero-Speicher (`~/Zotero`), dort wird nur gelesen.

## Protokoll

-   2026-10-09 16:10: `CLAUDE.md` und Skill `rag-retrieval` an dieses Projekt angepasst. `CLAUDE.md`: Tippfehler und Widersprüche bereinigt, Projektstruktur und Abschnitt „Protokoll“ ergänzt. Skill: Index und `seitenzahlen.json` mit den Quellen eines anderen Projekts geleert, Verweis auf den nicht vorhandenen Skill `quelle-zitieren` entfernt, Beispiele auf das Thema dieser Thesis umgestellt. `rag.py`: Quellennamen im BibTeX-Key-Format werden erkannt, `status` prüft den Abgleich mit `references.bib`. Ordner `Quellen/` angelegt (leer).
-   2026-10-09 16:35: Quellen werden jetzt direkt aus Zotero gelesen statt aus `Quellen/`. `rag.py`: ordnet BibTeX-Keys über das Feld `file` in `references.bib` den Dateien im Zotero-Speicher zu (PDF bevorzugt, sonst HTML), `status` zeigt Einträge ohne Datei. `SKILL.md` und `CLAUDE.md` entsprechend angepasst, leeren Ordner `Quellen/` wieder entfernt. Index neu aufgebaut: `kumarBiggerIsntAlways2026` (28 Chunks), `pereiraCRBenchEvaluatingRealWorld2026` (71 Chunks). Seitenzählung in `seitenzahlen.json` für beide noch nicht geprüft.
