# Quellenvorschläge

Diese Vorschläge sind **ungeprüft**. Sie stammen aus einer Websuche, und die Angaben zu Autoren, Jahr und Inhalt beruhen nur auf Titel und Abstract bzw. der Landingpage. Verwendet werden darf nur, was der Nutzer gelesen und über Zotero zu `references.bib` hinzugefügt hat.

Bereits in `references.bib`: `kumarBiggerIsntAlways2026`, `pereiraCRBenchEvaluatingRealWorld2026`.

## Recherche vom 2026-10-09

### A. Überblick und Literaturreviews (Fragen 1 und 4 im Exposé: Eignung von KI-Assistenten, geeignete Modelle)

-   Kaniewski, S., Schmidt, F., Enzweiler, M., Menth, M. & Heer, T. (2025). *A Systematic Literature Review on Detecting Software Vulnerabilities with Large Language Models*. arXiv:2507.22659. https://arxiv.org/abs/2507.22659
    Aktuellstes Review (263 Studien, 01/2020–11/2025) mit Taxonomie der Ansätze und Hinweis auf die schlechte Vergleichbarkeit der Studien.
-   Zhou, X., Cao, S., Sun, X. & Lo, D. (2024). *Large Language Model for Vulnerability Detection and Repair: Literature Review and the Road Ahead*. https://arxiv.org/abs/2404.02525 (ACM-Version: https://dl.acm.org/doi/10.1145/3708522, Venue-Angabe dort prüfen)
    Review über 58 Studien zu Erkennung und Behebung von Sicherheitslücken mit LLMs, geeignet für die Einordnung der Ansätze (Prompting, Fine-Tuning).
-   Ding, Y. et al. (2025, arXiv 2024). *Vulnerability Detection with Code Language Models: How Far Are We?* (PrimeVul, ICSE 2025). https://arxiv.org/abs/2403.18624
    Zeigt, dass bestehende Benchmarks die Leistung stark überschätzen (F1 68,26 % auf BigVul vs. 3,09 % auf PrimeVul) und ist damit zentral für eine kritische Einordnung der Zuverlässigkeit.

### B. LLMs für Code-Review und Qualitätsmängel (Frage 1, Qualität)

-   Cihan, U., İçöz, A., Haratian, V. & Tüzün, E. (2025). *Evaluating Large Language Models for Code Review*. arXiv:2505.20206. https://arxiv.org/abs/2505.20206
    Vergleicht GPT-4o und Gemini 2.0 Flash bei der Erkennung fehlerhaften Codes (ca. 64–69 % Genauigkeit mit Kontext) und liefert Vergleichswerte für die eigenen KPIs.
-   Cihan, U., Haratian, V., İçöz, A. et al. (2025, arXiv 2024). *Automated Code Review In Practice* (ICSE 2025, SEIP). https://arxiv.org/abs/2412.18531
    Industriestudie mit 4.335 Pull Requests, in der 73,8 % der LLM-Kommentare umgesetzt wurden, aber auch fehlerhafte und irrelevante Kommentare auftraten, also gut für Fähigkeiten und Limitationen in der Praxis.
-   Zeng, Z. et al. (2025). *SWR-Bench: Assessing LLM Performance in Real-World Code Review Comment Generation*. arXiv:2509.01494. https://arxiv.org/abs/2509.01494
    Benchmark mit 1.000 geprüften Pull Requests, laut Abstract schneiden bestehende automatische Review-Systeme darauf schwach ab.
-   *An evaluation study of large language models for addressing code quality issues* (Empirical Software Engineering, 2026). https://link.springer.com/article/10.1007/s10664-026-10858-8
    Untersucht, wie LLMs von SonarQube gemeldete Qualitätsmängel beheben, nützlich als Verbindung zwischen klassischer Analyse und LLMs. **Autoren und Details nicht geprüft** (Springer-Seite war nicht abrufbar).

### C. LLM kombiniert mit statischer Analyse und Fehlalarme (Frage 1, Effizienz, KPI „max. 10 % Fehlalarme“, Abgrenzung zu bestehenden Lösungen)

-   Li, Z., Dutta, S. & Naik, M. (2024/2025). *IRIS: LLM-Assisted Static Analysis for Detecting Security Vulnerabilities*. arXiv:2405.17238. https://arxiv.org/abs/2405.17238
    Hybridansatz, der mit GPT-4 55 von 120 Java-Schwachstellen findet (CodeQL: 27) und damit den Vergleich mit klassischen Tools abdeckt.
-   Du, X. et al. (2026). *Reducing False Positives in Static Bug Detection with LLMs: An Empirical Study in Industry*. arXiv:2601.18844. https://arxiv.org/abs/2601.18844
    Industriestudie (Tencent), nach der LLMs 94–98 % der Fehlalarme statischer Analyse eliminieren, und liefert Zahlen zu Aufwand und Kosten pro Meldung.
-   Keltek, M., Hu, R., Fani Sani, M. & Li, Z. (2024). *Boosting Cybersecurity Vulnerability Scanning based on LLM-supported Static Application Security Testing*. arXiv:2409.15735. https://arxiv.org/abs/2409.15735
    Beschreibt LSAST mit lokal betreibbarem LLM und Wissensabruf, also ein verwandter Ansatz zur lokalen Bereitstellung (Anforderung im Exposé). Laut Abstract „under review“, Status prüfen.

### D. Lokale vs. Cloud-Modelle (Anforderung: LLM austauschbar, lokal deploybar)

-   Park, S., Ko, G. & Cho, H. (2025). *On the Effectiveness of Instruction-Tuning Local LLMs for Identifying Software Vulnerabilities* (MobiSec 2025). https://arxiv.org/abs/2512.20062
    Vergleicht lokale instruction-getunte Modelle mit API-Modellen bei der CWE-Klassifikation und stützt die Begründung für lokal betriebene LLMs.

### E. Standards und Klassifikationen (Fragen „Qualitätsstandards“ und „Einstufung von Sicherheitslücken“)

Primärquellen (Normen und Spezifikationen), Zitierweise in Zotero noch festlegen:

-   ISO/IEC (2023). *ISO/IEC 25010:2023 Systems and software engineering – Systems and software Quality Requirements and Evaluation (SQuaRE) – Product quality model*. https://www.iso.org/standard/78176.html
    Produktqualitätsmodell mit neun Merkmalen (u. a. Security, Maintainability, Reliability) als Grundlage für das Regelwerk. Die Norm ist kostenpflichtig, Zugriff über die Hochschule klären.
-   MITRE. *Common Weakness Enumeration (CWE)*. https://cwe.mitre.org/
    Standardklassifikation für Schwächentypen in Software, passend für die Zuordnung der Befunde des Tools.
-   FIRST. *Common Vulnerability Scoring System (CVSS)*. https://www.first.org/cvss/
    Standard zur Schweregradbewertung (Low bis Critical) und damit Grundlage für „als kritisch eingestufte Sicherheitslücken“ in den KPIs. Version (3.1 oder 4.0) festlegen.
-   OWASP. *OWASP Top 10*. https://owasp.org/www-project-top-ten/
    Etablierte Kategorisierung der häufigsten Risiken für Webanwendungen. Die aktuelle Ausgabe ist zu prüfen.

## Lücken, die noch offen sind

-   **Bestehende Lösungen (Ziel 2):** Hier fehlen noch Quellen, die Fähigkeiten und Limitationen konkreter Produkte beschreiben (z. B. SonarQube, Semgrep, CodeQL, CodeRabbit, GitHub Copilot Code Review). Das sind meist Herstellerdokumentationen. Soll ich dazu gezielt suchen?
-   **Qualitätsmetriken jenseits von ISO 25010:** z. B. Clean Code, SQALE, Code Smells. Hier wäre ein Hinweis nötig, welche Richtung die Arbeit nehmen soll.
-   **Regelbasiertes Prompting/Regelwerke für LLMs:** Es wurde bisher nicht gezielt nach Arbeiten gesucht, die vordefinierte Regeln im Prompt verwenden.
-   Das Schwerpunktthema „sprach- und frameworkunabhängige Regeln“ ist noch nicht abgedeckt.
