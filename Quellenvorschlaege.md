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

### F. Testabdeckung und Mutation Testing (Schritt 5 des Tools, `testAnalysis.qmd`)

Vorgeschlagen am 13.11.2026. Die Angaben stammen aus den Verlagsdaten bzw. dblp, die Volltexte habe ich noch nicht gelesen.

-   Gopinath, R., Alipour, A., Ahmed, I., Jensen, C. & Groce, A. (2015). *How hard does mutation analysis have to be, anyway?* 26th IEEE International Symposium on Software Reliability Engineering (ISSRE 2015), S. 216–227. https://doi.org/10.1109/ISSRE.2015.7381815
    Zeigt laut Zusammenfassung, dass eine kleine, feste Stichprobe von Mutanten unabhängig von der Programmgröße ähnliche Ergebnisse liefert wie die vollständige Analyse. Könnte die Stichprobe im Mutation Testing stützen.
-   Zhang, L., Hou, S.-S., Hu, J.-J., Xie, T. & Mei, H. (2010). *Is operator-based mutant selection superior to random mutant selection?* ICSE 2010, S. 435–444. https://doi.org/10.1145/1806799.1806863
    Vergleicht operatorbasierte mit zufälliger Auswahl von Mutanten und findet keinen Vorteil der operatorbasierten. Ebenfalls zur Begründung einer Zufallsstichprobe.
-   Papadakis, M., Kintis, M., Zhang, J., Jia, Y., Le Traon, Y. & Harman, M. (2019). *Mutation Testing Advances: An Analysis and Survey*. Advances in Computers 112, Kapitel 6, Elsevier. Postprint: https://orbilu.uni.lu/handle/10993/31612
    Überblick über Mutation Testing, Kostensenkung (u. a. Stichproben) und Kennzahlen wie den Mutation Score. Die DOI muss noch über ScienceDirect ermittelt werden.
-   Inozemtseva, L. & Holmes, R. (2014). *Coverage is not strongly correlated with test suite effectiveness*. ICSE 2014, S. 435–445. https://doi.org/10.1145/2568225.2568271
    Untersucht, wie gut Testabdeckung die Wirksamkeit einer Testsuite (gemessen mit Mutanten) vorhersagt. Begründet, warum das Tool neben der Abdeckung auch Mutation Testing misst und keine Mindestabdeckung vorgibt.

## Recherche vom 2026-11-18

### G. Bedrohungsmodellierung (Schritt 6: Bedrohungsmodell als Kontext für die Entscheidungen, `llmEvaluation.qmd`)

Anlass: Im libgdx-Lauf waren 1.512 von 2.527 Security-Entscheidungen unsicher, meist weil unklar war, welche Eingaben ein Angreifer kontrolliert. Autor, Jahr und Titel habe ich jeweils auf der Seite des Herausgebers, auf arXiv oder über Crossref geprüft. Die Volltexte habe ich nicht gelesen; die Sätze zur Relevanz beruhen auf Abstract bzw. Landingpage.

Grundlagen:

-   Braiterman, Z., Shostack, A., Marcil, J., de Vries, S., Michlin, I., Wuyts, K., Hurlbut, R., Schoenfield, B. S. E., Scott, F., Coles, M., Romeo, C., Miller, A., Tarandach, I., Douglen, A. & French, M. (o. J., laut Sekundärquellen 2020). *Threat Modeling Manifesto*. https://www.threatmodelingmanifesto.org/
    Definiert Threat Modeling als „analyzing representations of a system to highlight concerns about security and privacy characteristics“ und nennt vier Leitfragen („What are we working on?“ …); das Jahr steht nicht auf der Seite.
-   Shostack, A. (2014). *Threat Modeling: Designing for Security*. Wiley, 624 S., ISBN 978-1-118-80999-0. https://wiley-vch.de/de/fachgebiete/computer-und-informatik/threat-modeling-978-1-118-80999-0
    Standardwerk zu Methoden der Bedrohungsmodellierung (u. a. STRIDE, Datenflussdiagramme mit Vertrauensgrenzen), geeignet als Hauptquelle für den Begriff.
-   Shostack, A. (2024). *Understanding the Four-Question Framework for Threat Modeling*. Shostack + Associates White Paper #5, November 2024. https://shostack.org/files/papers/The_Four_Question_Framework.pdf
    Erklärt die vier Fragen, aus denen sich die drei Fragen des Tools ableiten lassen (die erste Frage „What are we working on?“). White Paper, kein begutachteter Text.
-   OWASP Cheat Sheet Series Team (o. J.). *Threat Modeling Cheat Sheet*. https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html
    Praxisanleitung, nach der das Systemmodell eine „clear view of trust boundaries, data flows, data stores, processes“ geben soll. Stützt die Frage nach den Vertrauensgrenzen; Stand der Seite beim Zitieren angeben.
-   Microsoft (2017, aktualisiert 2026). *Threats – Microsoft Threat Modeling Tool*. Microsoft Learn. https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats
    Primärquelle für die STRIDE-Kategorien (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege). Nur nötig, falls STRIDE in der Arbeit vorkommt.
-   Souppaya, M. & Scarfone, K. (2016). *Guide to Data-Centric System Threat Modeling*. NIST SP 800-154, Initial Public Draft. https://csrc.nist.gov/pubs/sp/800/154/ipd
    Beschreibt Threat Modeling als Form der Risikobewertung („examines the attack and defense aspects of an entity“). Achtung: bis heute nur ein Entwurf, laut NIST-Seite soll er finalisiert werden.

Überblick:

-   Xiong, W. & Lagerström, R. (2019). *Threat modeling – A systematic literature review*. Computers & Security 84, S. 53–69. https://doi.org/10.1016/j.cose.2019.03.010
    Systematisches Review zu Methoden der Bedrohungsmodellierung. Die Angaben habe ich über Crossref geprüft, die Verlagsseite war nicht abrufbar. Laut Sekundärquellen wertet das Review 54 Arbeiten aus, das ist noch zu prüfen.

LLMs und Bedrohungsmodelle (zur Frage, ob das Tool das Bedrohungsmodell erzeugen kann):

-   Elsharef, I., Zeng, Z. & Gu, Z. (2024). *Facilitating Threat Modeling by Leveraging Large Language Models*. Workshop on AI Systems with Confidential Computing (AISCC) 2024, NDSS. https://dx.doi.org/10.14722/aiscc.2024.23016
    Ein offenes LLM beantwortet Fragen der Bedrohungsmodellierung anhand von Designdokumenten; laut Abstract erfüllten über 75 % der Antworten die Erwartungen menschlicher Prüfer, mit RAG besser. Stützt den Ansatz „Entwurf aus Doku erzeugen, Mensch prüft“.
-   Munshi, S., Pathak, S., Ghatode, S., Priyadarshini, T., Chandramouleeswaran, D. & Rana, A. (2025). *ACSE-Eval: Can LLMs threat model real-world cloud infrastructure?* arXiv:2505.11565. https://arxiv.org/abs/2505.11565
    Benchmark mit 100 AWS-Szenarien zur Bewertung LLM-erzeugter Bedrohungsmodelle; zeigt laut Abstract deutliche Unterschiede zwischen Modellen. Eingereicht bei NeurIPS 2025, Status prüfen.
-   AbdulGhaffar, A. & Matrawy, A. (2025). *LLMs' Suitability for Network Security: A Case Study of STRIDE Threat Modeling*. arXiv:2505.04101 (Konferenzbeitrag, 6 S.). https://arxiv.org/abs/2505.04101
    Fünf LLMs ordnen 5G-Bedrohungen STRIDE zu; die Autoren folgern, dass LLMs vor dem Einsatz angepasst werden müssen. Spricht dafür, ein erzeugtes Bedrohungsmodell nicht ungeprüft zu übernehmen.

Kontext bei der LLM-Triage statischer Befunde (zur Frage, warum das Entscheidungsmodell mehr Kontext braucht):

-   Chen, J., Xiang, H., Zhao, Z., Li, L., Zhang, Y., Ding, B., Li, Q. & Xiong, S. (2024, rev. 2025). *Utilizing Precise and Complete Code Context to Guide LLM in Automatic False Positive Mitigation*. arXiv:2411.03079. https://arxiv.org/abs/2411.03079
    Nach dem Abstract führen zu breite und zu knappe Codeausschnitte LLMs bei der Bewertung von SAST-Warnungen in die Irre; präziser Kontext (LLM4FPM) verbessert die Ergebnisse. Passt zur Beobachtung, dass das Modell aus 5 Zeilen Code nicht entscheiden kann.

Nicht gefunden: eine Arbeit, die ausdrücklich ein Bedrohungsmodell als Kontext für die LLM-Triage statischer Befunde nutzt. Das könnte eine Lücke sein, die die Thesis benennen kann; vor einer solchen Aussage gezielter suchen.

### H. Benchmarks mit bekannten Sicherheitslücken (Evaluation, Ziel 4 im Exposé)

-   OWASP Foundation (Version 1.2, Musterlösung vom Juni 2016; Repository laufend gepflegt). *OWASP Benchmark for Java* (BenchmarkJava). https://github.com/OWASP-Benchmark/BenchmarkJava, Projektseite https://owasp.org/www-project-benchmark/
    Java-Webanwendung mit 2.740 Testfällen in 11 Kategorien mit CWE (u. a. SQL Injection, XSS, Path Traversal, Command Injection, schwache Kryptografie) und einer Musterlösung (`expectedresults-1.2.csv`): 1.415 echte Lücken, 1.325 absichtlich harmlose Fälle, die nur verwundbar aussehen. Damit lassen sich Trefferquote und Fehlalarmquote vor und nach dem LLM-Filter messen. Geprüft am 18.11.2026 über das Repository (README, Musterlösung, Lizenz GPL-2.0). Die Zahlen habe ich aus der CSV gezählt. Lokal geklont: Commit `a452b3a` vom 12.11.2026. Achtung: Er ist seit 2016 öffentlich und könnte in den Trainingsdaten der Modelle stecken (siehe `caoConcernedDataContamination2024` in `references.bib`).

## Lücken, die noch offen sind

-   **Bestehende Lösungen (Ziel 2):** Hier fehlen noch Quellen, die Fähigkeiten und Limitationen konkreter Produkte beschreiben (z. B. SonarQube, Semgrep, CodeQL, CodeRabbit, GitHub Copilot Code Review). Das sind meist Herstellerdokumentationen. Soll ich dazu gezielt suchen?
-   **Qualitätsmetriken jenseits von ISO 25010:** z. B. Clean Code, SQALE, Code Smells. Hier wäre ein Hinweis nötig, welche Richtung die Arbeit nehmen soll.
-   **Regelbasiertes Prompting/Regelwerke für LLMs:** Es wurde bisher nicht gezielt nach Arbeiten gesucht, die vordefinierte Regeln im Prompt verwenden.
-   Das Schwerpunktthema „sprach- und frameworkunabhängige Regeln“ ist noch nicht abgedeckt.
