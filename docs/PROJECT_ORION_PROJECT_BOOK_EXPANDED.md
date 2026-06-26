# PROJECT ORION — MASTER PROJECT BOOK

Version: 2.0
Status: Active
Last Updated: 2026-06-26
Current Phase: End of Sprint 5 / Start of Sprint 6

---

# 1. Project Vision

Project Orion is een professionele AI Swing Trading Assistant.

Het doel van Orion is dat het systeem zelfstandig duizenden aandelen analyseert en de gebruiker alleen concrete handelsadviezen geeft.

De gebruiker hoeft geen indicatoren, grafieken, RSI, MACD, SMA, volumeprofielen of technische signalen te interpreteren.

Orion doet de analyse.

De gebruiker krijgt alleen duidelijke adviezen zoals:

* Koop
* Verkoop
* Houd
* Geen actie

Het einddoel is dat Orion aanvoelt als een persoonlijke professionele swingtrader die toevallig software is.

Orion moet niet voelen als een technisch analysepakket.

Orion moet voelen als een slimme assistent die zelfstandig de markt bekijkt, kansen filtert, risico inschat en alleen de beste acties teruggeeft.

---

# 2. Mission

Orion moet uiteindelijk iedere handelsdag zelfstandig:

1. Het volledige aandelenuniversum laden.
2. Marktdata ophalen.
3. Oninteressante aandelen wegfilteren.
4. Sterke kandidaten selecteren.
5. Technische analyse uitvoeren.
6. Open posities bewaken.
7. Koop-, verkoop- of houdadviezen geven.
8. Slechts enkele hoogwaardige kansen tonen.
9. Slechte of middelmatige kansen negeren.

De belangrijkste handelsregel blijft:

> Liever geen trade dan een slechte trade.

Geen actie is dus een geldig resultaat.

Orion hoeft niet iedere dag een trade te vinden.

Orion moet alleen handelen wanneer de setup sterk genoeg is.

---

# 3. Trading Philosophy

Orion richt zich op swing trading.

Gemiddelde houdduur:

* enkele uren
* 1 dag
* 2 dagen
* maximaal enkele dagen

Orion is niet bedoeld voor:

* long-term investing
* scalping
* secondenhandel
* crypto
* opties
* penny-stock gokken
* extreem illiquide aandelen

Orion zoekt aandelen met:

* voldoende liquiditeit
* voldoende volume
* duidelijke prijsbeweging
* momentum
* trendstructuur
* redelijke verhandelbaarheid

Het systeem moet conservatief genoeg zijn om slechte setups te vermijden, maar actief genoeg om sterke swing-kansen te herkennen.

---

# 4. User Experience Philosophy

De GUI moet eenvoudig blijven.

De gebruiker mag niet worden overladen met technische informatie.

Orion moet technische analyse vertalen naar gewone taal.

De gebruiker ziet niet:

* RSI
* MACD
* SMA20
* SMA50
* ruwe volumes
* ruwe scores
* API-fouten
* debugdata
* technische pipeline-informatie

De gebruiker ziet alleen:

* welk aandeel interessant is
* welke actie Orion adviseert
* hoeveel vertrouwen Orion heeft
* eventueel hoeveel aandelen gekocht kunnen worden
* een korte begrijpelijke reden

Voorbeeld van gewenste output:

Goedemorgen Ralf.

Ik heb vandaag 6204 aandelen geanalyseerd.

Er zijn 3 sterke kansen gevonden.

1. FCEL
   Koop
   Vertrouwen: 100%
   Reden: sterke trend en gezond momentum.

2. CNVS
   Koop
   Vertrouwen: 100%
   Reden: sterke technische setup.

3. APPS
   Koop
   Vertrouwen: 100%
   Reden: positief momentum en voldoende liquiditeit.

Als er geen goede kansen zijn, zegt Orion:

Geen actie vandaag.

Dat is geen fout.

Dat is discipline.

---

# 5. Development Principles

Tijdens de ontwikkeling gelden de volgende afspraken:

1. We werken altijd met volledige bestanden.
2. We gebruiken geen losse codefragmenten.
3. Eerst architectuur.
4. Daarna functionaliteit.
5. Daarna AI.
6. Daarna optimalisatie.
7. Iedere module krijgt één duidelijke verantwoordelijkheid.
8. De GUI blijft simpel.
9. De gebruiker ziet geen technische scannerdata.
10. Debuginformatie blijft voor ontwikkeling.
11. Orion adviseert.
12. De gebruiker analyseert niet.
13. Slechte kansen worden niet getoond.
14. Het systeem moet schaalbaar worden voor 10.000+ aandelen.
15. Code moet begrijpelijk en onderhoudbaar blijven.

Belangrijke ontwerpregel:

> Een module mag niet verantwoordelijk zijn voor twee totaal verschillende dingen.

Voorbeeld:

QuoteService haalt marktdata op.

QuoteService doet geen technische analyse.

TechnicalScanner analyseert technische data.

TechnicalScanner beheert geen portfolio.

RankingEngine rangschikt kansen.

RankingEngine haalt geen marktdata op.

---

# 6. Current Project Status

Sprint 5 is succesvol afgerond.

De oude monolithische ScannerService is functioneel vervangen door een modulaire ScanPipeline.

Huidige werkende onderdelen:

* Modulaire GUI
* UniverseManager 2.0
* UniverseDownloader
* UniverseLoader
* Portfolio
* TradeManager
* TradeHistoryStore
* MarketFilter
* QuoteService
* Quote cache
* PriceFilter
* VolumeFilter
* LiquidityFilter
* RelativeStrengthFilter
* MomentumFilter
* TechnicalScanner
* RankingEngine
* ScanPipeline
* Performance logging

Het huidige Amerikaanse aandelenuniversum bevat:

* Nasdaq: 3538 aandelen
* US Other: 2666 aandelen
* Totaal: 6204 aandelen

De volledige 6204-scan is getest en werkt end-to-end.

Belangrijkste huidige beperking:

> yfinance / QuoteService is de bottleneck bij volledige scans.

Daarom start Sprint 6 met een professionele Market Data Layer.

# TABLE OF CONTENTS

---

# PART I — PROJECT FOUNDATION

1. Project Vision
2. Mission
3. Trading Philosophy
4. User Experience Philosophy
5. Development Principles
6. Current Project Status

---

# PART II — SYSTEM ARCHITECTURE

7. Overall Architecture
8. Folder Structure
9. Core Modules
10. Dependency Rules
11. Data Flow
12. Configuration
13. Logging
14. Error Handling

---

# PART III — MARKET UNIVERSE

15. UniverseManager
16. UniverseDownloader
17. UniverseLoader
18. Universe Maintenance

---

# PART IV — MARKET DATA

19. Market Data Layer
20. QuoteService
21. Quote Cache
22. Historical Data
23. Future Providers

---

# PART V — SCANNER

24. ScanPipeline
25. PriceFilter
26. VolumeFilter
27. LiquidityFilter
28. RelativeStrengthFilter
29. MomentumFilter
30. TechnicalScanner
31. RankingEngine

---

# PART VI — DECISION MAKING

32. DecisionEngine
33. Portfolio
34. TradeManager
35. TradeHistoryStore
36. Risk Management
37. Position Sizing

---

# PART VII — USER INTERFACE

38. GUI Philosophy
39. Dashboard
40. Scan Screen
41. Portfolio Screen
42. Future Mobile Version

---

# PART VIII — AI

43. Orion Thinking Model
44. AI Reasoning
45. Explainable Decisions
46. Future AI Learning

---

# PART IX — PERFORMANCE

47. Performance Monitoring
48. Quote Cache
49. Future Historical Cache
50. Parallel Processing

---

# PART X — DEVELOPMENT

51. Coding Standards
52. Naming Conventions
53. Testing
54. Architectural Decision Records

---

# PART XI — PROJECT HISTORY

55. Sprint 1
56. Sprint 2
57. Sprint 3
58. Sprint 4
59. Sprint 5

---

# PART XII — ROADMAP

60. Sprint 6
61. Sprint 7
62. Sprint 8
63. Sprint 9
64. Sprint 10
65. Sprint 11
66. Sprint 12
67. Long-Term Vision

---

# PART XIII — APPENDICES

68. Glossary
69. Known Limitations
70. Future Ideas
71. Open Questions
72. Change Log


# 13. Roadmap

Sprint 5

ScanPipeline

QuoteService

Price Filter

Volume Filter

Liquidity Filter

Ranking Engine

Top 3

Sprint 6

Performance

Caching

Parallelisering

Sprint 7

Nieuws

Sentiment

Earnings

Sector Strength

Sprint 8

Paper Trading

Broker API

Sprint 9

AI Trade Reasoning

Zelflerende ranking

------------------------------------------------------------------------

# 14. Einddoel

Iedere ochtend opent de gebruiker Orion.

Orion scant automatisch duizenden aandelen.

Na filtering blijven slechts enkele hoogwaardige kansen over.

De gebruiker krijgt uitsluitend concrete koop-, verkoop- of
houdadviezen.

Alle open posities worden automatisch bewaakt.

Orion adviseert zelfstandig wanneer winst genomen of verlies beperkt
moet worden.

Dit document is de centrale bron van waarheid voor Project Orion.
