# PROJECT_STATUS.md

# Project Orion - Status

Laatste update: 19-07-2026

---

# Algemene status

Project Orion beschikt over een volledig werkende autonome IBKR Paper Trading infrastructuur.

De complete end-to-end handelsketen is operationeel:

- Universe selectie
- Marktdata (Yahoo)
- Indicator berekening
- Trading Pipeline
- AI besluitvorming
- Position Allocation
- Order creatie
- IBKR Order Transport
- Broker fills
- Broker synchronisatie
- Portfolio synchronisatie

De autonome runner voltooit een volledige cyclus zonder fouten.

De eerste schaalfase voor autonoom Paper-traden is operationeel:

- 100 gecureerde EU/VS-symbolen;
- batchgewijze historische marktdata met cache;
- configureerbare begrensde cycli met 15-minuteninterval;
- maximaal drie nieuwe posities per cyclus;
- Xetra BUY-, suffix- en broker-syncsupport.

Nieuwe observatie-infrastructuur:

- eigen Qt-GUI verwijderd; TWS plus CLI-output vormen de interface;
- IBKR-headlines beschikbaar in fail-open `SHADOW`-modus;
- nieuws beïnvloedt nog geen handelsbesluit of order;
- gesloten trades koppelen entry- en exitredenen via `trade_id`;
- learning/AI-services mogen runtimeparameters nog niet aanpassen.

Architectuuropschoning:

- één canonieke actieve decisionnamespace: `services/trading_decision`;
- oude directe decisionengine en dubbele `engines`/scannerketen verwijderd;
- research/explainability blijft geïsoleerd in `services/decisions`;
- lege placeholders en tests zonder assertions verwijderd;
- volledige testsuite: 555 geslaagd, 0 mislukt.

---

# Werkende onderdelen

## Data

✅ Yahoo Provider

✅ Indicator Builder

✅ Trading Pipeline

✅ Signal Fusion

---

## Trading

✅ BUY pipeline

✅ Position Allocator

✅ Execution Engine

✅ Paper Trading Service

✅ Autonomous Runner

---

## IBKR

✅ Account Service

✅ Broker

✅ Order Transport

✅ Broker Synchronisatie

✅ Portfolio Synchronisatie

---

## Portfolio

✅ Cash synchronisatie

✅ Positie synchronisatie

✅ Equity berekening

---

# Laatst opgeloste problemen

## Broker exits

Runner probeert geen exits meer uit te voeren voor broker-posities die niet door Orion worden beheerd.

Resultaat:

Geen crashes meer tijdens broker synchronisatie.

---

## Yahoo ticker

ASM International:

Oud:

ASMI.AS

Nieuw:

ASM.AS

---

## Position sizing

Position Allocator werkte correct, maar configuratie stond te laag voor dure aandelen.

Configuratie aangepast.

---

## Post-fill synchronisatie

Synchronisatie normaliseert nu Yahoo-symbolen en IBKR-symbolen.

Voorbeeld:

ASM.AS

↓

ASM

Hierdoor verdween de laatste IBKR synchronisatie-fout.

---

# Huidige beperkingen

Wanneer het maximum aantal open posities is bereikt worden nieuwe BUY-signalen correct afgewezen.

Dit is verwacht gedrag.

Yahoo blijft in deze fase de analysebron. Voor handel met echt geld moet actuele
IBKR-marktdata voor posities en topkandidaten nog de execution-grade bron worden.
De runtime accepteert bewust uitsluitend IBKR Paper-accounts met `DU`-prefix.

IBKR-nieuwsdekking hangt af van API-beschikbare providers en account-
abonnementen. `UNAVAILABLE` is daarom een geldige observatiestatus. De eerste
classifier is deterministisch en conservatief; hij is nog geen execution-grade
nieuws-gate.

---

# Eerste Repository Audit

Er is een eerste architectuur-audit uitgevoerd.

Belangrijkste conclusie:

Veel functionaliteit blijkt al aanwezig te zijn.

Onder andere:

- Trailing Stop
- Break Even
- Time Stop
- Exit Engine
- RiskPlan
- Position Monitoring
- Performance Analyse
- CLI-dashboardservice (desktop-GUI verwijderd)
- Trade Journal
- Portfolio Management

De verwachting is dat een aanzienlijk deel alleen nog gekoppeld hoeft te worden.

---

# Volgende fase

Prioriteit heeft nu géén nieuwe ontwikkeling.

De volgende ontwikkelfase bestaat uit een volledige functionele audit van de bestaande codebase.

Doel:

- bestaande modules analyseren
- vaststellen welke functionaliteit volledig af is
- identificeren welke onderdelen nog niet door de Autonomous Runner worden gebruikt
- bestaande componenten activeren voordat nieuwe code wordt geschreven

---

# Algemene projectstatus

Architectuur: stabiel

IBKR infrastructuur: operationeel

Autonomous Runner: operationeel

Trading Pipeline: operationeel

Productiestatus:

**Codebase is stabiel genoeg om de focus te verleggen van infrastructuur naar functionele integratie van bestaande modules.**
