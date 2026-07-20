# TODO.md

# Project Orion - TODO

Laatste update: 20-07-2026

---

# Huidige prioriteit

Verzamel eerst voldoende geïsoleerde shadowresultaten voordat IBKR-orderrechten
of betaalde realtime marktdata worden overwogen. Kalibreer de nieuwe
selectiviteitsgrenzen uitsluitend offline en nooit automatisch vanuit learning.

---

# PRIORITEIT 1

## Volledige Functionele Audit

Voer een volledige analyse uit van de complete Project Orion codebase.

Voor iedere service vastleggen:

- bestaat de service?
- volledig geïmplementeerd?
- getest?
- gebruikt door Autonomous Runner?
- niet aangesloten?
- vervangen door nieuwere implementatie?
- kan direct geactiveerd worden?

---

# PRIORITEIT 2

## Risk Management

Controleer de bestaande implementaties van:

- RiskPlan
- Trailing Stop
- Break Even
- Time Stop
- Stop Loss
- Take Profit
- Position sizing

Doel:

Bepalen welke onderdelen al productierijp zijn.

---

# PRIORITEIT 3

## Exit Management

Analyseer de volledige exit-flow.

Controleer onder andere:

- Exit Engine
- Exit Evaluation
- Position Exit Execution
- Managed exits
- Broker exits

Doel:

Volledig automatisch beheer van open posities.

---

# PRIORITEIT 4

## Portfolio

Controleer:

- Portfolio synchronisatie
- Position Monitoring
- Cash Management
- Equity updates
- Portfolio allocatie

---

# PRIORITEIT 5

## Analyse & Monitoring

Inventariseer bestaande modules voor:

- CLI-dashboard en headless rapportage
- Performance
- Trade Journal
- Logging
- Metrics
- Reporting

Bepaal welke direct gebruikt kunnen worden.

---

# Pas NA de audit

Alleen wanneer duidelijk is dat functionaliteit ontbreekt:

- nieuwe modules ontwerpen
- nieuwe services ontwikkelen
- nieuwe tests schrijven

Voorkom dubbele implementaties.

---

# Afgerond

✅ End-to-end IBKR Paper Trading

✅ Broker synchronisatie

✅ Portfolio synchronisatie

✅ BUY Pipeline

✅ Position Allocator

✅ Order Execution

✅ Post-fill Synchronisatie

✅ Autonomous Runner stabiel

✅ Eerste universumopschaling naar 100 EU/VS-aandelen

✅ Historische Yahoo-batches van 25 met 15-minutencache

✅ Begrensde multi-cycle runner met configureerbaar interval

✅ Maximaal drie nieuwe posities per cyclus

✅ Xetra-contract- en suffixsupport

✅ Qt-GUI verwijderd; CLI-presentatie behouden

✅ Provider-onafhankelijke IBKR-nieuwslaag in SHADOW-modus

✅ Nieuwsnormalisatie, deduplicatie en JSONL-audittrail

✅ Gesloten trade-records met BUY/SELL-redenen en geraamde netto-P&L

✅ Canonieke actieve decisionlaag afgescheiden van researchcode

✅ Legacy `engines`/`ScannerService` en lege placeholders verwijderd

✅ Volledige testsuite uitgebreid naar 581 geslaagd en 0 mislukt

✅ IBKR live bid/ask-, spread-, freshness- en top-size execution gate

✅ Broker-native Paper brackets met OCA-veilige software-exits

✅ Native protective-fillreconciliatie naar trade memory

✅ Sessieverlies-, loss-streak- en brokerfout-circuitbreaker

✅ Markt-, sector- en correlatieclusterconcentratie voor 100 symbolen

✅ Earnings-blackoutinterface zonder verzonnen kalenderdata

✅ Offline cost-aware expectancyanalyse zonder runtimeconfiguraties te wijzigen

✅ Getekende trendnormalisatie en geannualiseerde volatiliteitsschaal

✅ Onafhankelijke thesis-/ranking-/factorselectiviteitsgate

✅ Geïsoleerde SHADOW-modus met aparte portefeuille en trade memory

---

# Volgende schaalstappen

- Paper-observatie met 100 symbolen en orders uitgeschakeld;
- minimaal meerdere weken shadowtrades verzamelen en nettoresultaten per markt,
  regime en afwijzingsreden beoordelen;
- false positives/negatives van de selectiviteitsgate handmatig auditen voordat
  grenzen worden aangepast;
- ontbrekende/ambigue Yahoo- en IBKR-contracten uit het universum filteren;
- execution-qualitymetingen tijdens Paper-cycli verzamelen en limieten op
  werkelijke spread/fill/slippage kalibreren;
- officiële earningskalender periodiek vullen en bron/auditdatum vastleggen;
- pas na stabiele meetresultaten opschalen naar 250 symbolen;
- TWS execution-historyretentie en herstel na meerdaagse uitval valideren;
- nieuwsproviderdekking en latency meten tijdens orderloze Paper-cycli;
- classifier valideren op EU/VS-headlines en false positives;
- pas daarna beslissen over een fail-closed nieuws-gate;
- offline learning uitsluitend op `CompletedTradeRecord` ontwerpen, met
  menselijke goedkeuring en versiebeheer van parameterwijzigingen.
- na Paper-validatie beoordelen of de geïsoleerde `services/decisions`-
  researchlaag nog waarde toevoegt of verder kan worden geconsolideerd;
- performance-research pas migreren naar `CompletedTradeRecord` nadat voldoende
  volledig gesloten trades beschikbaar zijn.

---

# Doel volgende ontwikkelfase

Maximaal hergebruik van bestaande Orion-functionaliteit voordat nieuwe code wordt toegevoegd.
