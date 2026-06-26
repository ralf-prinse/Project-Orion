# ============================================================
# VOOR CHATGPT - LEES DIT EERST
# ============================================================

BELANGRIJK

Voordat je antwoord geeft, lees je eerst dit volledige document.

Dit document is de actuele bron van waarheid voor Project Orion.

Project Orion is een professioneel AI-softwareproject dat stap voor stap wordt ontwikkeld.

Werk altijd verder vanaf de huidige projectstatus.

Maak geen nieuwe architectuur als deze al bestaat.

Respecteer de bestaande codebase.

BELANGRIJKE ONTWIKKELAFSPRAKEN

- Werk altijd met volledige bestanden.
- Lever nooit losse codefragmenten.
- Denk eerst na over de architectuur.
- Houd de bestaande architectuur modulair en schaalbaar.
- Iedere module heeft één verantwoordelijkheid.
- Houd de GUI eenvoudig.
- Orion doet de analyse.
- De gebruiker krijgt alleen duidelijke handelsadviezen.
- Werk altijd één sprint tegelijk af.

Wanneer je dit document volledig hebt gelezen, ga je direct verder met de sprint die onder:

"Eerstvolgende Sprint"

staat beschreven.

Ga dus NIET opnieuw analyseren wat de volgende stap is.

De volgende sprint is al bepaald.

Volg deze.

# ============================================================


# PROJECT ORION - PROJECT STATUS

**Versie:** 2.0
**Laatst bijgewerkt:** 26 juni 2026
**Projectfase:** Einde Sprint 5 – Start Sprint 6

---

# 1. Projectdoel

Project Orion is een professionele AI Swing Trading Assistant.

Het uiteindelijke doel is een systeem dat volledig zelfstandig de Amerikaanse aandelenmarkt analyseert en de gebruiker alleen duidelijke handelsadviezen geeft.

De gebruiker hoeft geen technische analyse uit te voeren.

Orion doet de analyse.

De gebruiker krijgt alleen:

* BUY
* SELL
* HOLD
* GEEN ACTIE

De focus ligt op swing trades met een gemiddelde looptijd van enkele uren tot enkele dagen.

---

# 2. Ontwikkelfilosofie

Tijdens de ontwikkeling gelden altijd de volgende afspraken:

* We werken altijd met volledige bestanden.
* Nooit losse codefragmenten.
* Eerst architectuur, daarna code.
* Iedere module heeft één duidelijke verantwoordelijkheid.
* De GUI blijft eenvoudig.
* De gebruiker ziet geen technische indicatoren.
* Orion analyseert; de gebruiker neemt geen technische beslissingen.
* Het systeem moet uiteindelijk minimaal 10.000 aandelen per dag kunnen analyseren.

---

# 3. Huidige Architectuur

De scanner is volledig modulair opgebouwd.

```text
UniverseLoader
        ↓
QuoteService
        ↓
PriceFilter
        ↓
VolumeFilter
        ↓
LiquidityFilter
        ↓
RelativeStrengthFilter
        ↓
MomentumFilter
        ↓
TechnicalScanner
        ↓
RankingEngine
        ↓
Top 3 Koopkansen
```

De oude `ScannerService` wordt niet verder ontwikkeld en zal uiteindelijk volledig verdwijnen.

---

# 4. Werkende Modules

## Universe

* UniverseManager 2.0
* UniverseDownloader
* UniverseLoader

## Scanner

* QuoteService
* PriceFilter
* VolumeFilter
* LiquidityFilter
* RelativeStrengthFilter
* MomentumFilter
* TechnicalScanner
* RankingEngine
* ScanPipeline

## Portfolio

* Portfolio
* TradeManager
* TradeHistoryStore
* MarketFilter

## GUI

* Modulaire GUI werkt.

---

# 5. Universe

Huidige aandelenuniversum:

```text
Nasdaq:      3538
US Other:    2666
-------------------
Totaal:      6204 aandelen
```

UniverseLoader ondersteunt:

* limieten voor testen
* normalisatie
* verwijderen van duplicaten

---

# 6. ScanPipeline

De ScanPipeline vervangt de oude ScannerService.

Pipeline:

```text
Universe
↓
QuoteService
↓
PriceFilter
↓
VolumeFilter
↓
LiquidityFilter
↓
RelativeStrengthFilter
↓
MomentumFilter
↓
TechnicalScanner
↓
RankingEngine
↓
Top 3 koopkansen
```

Iedere stap heeft slechts één verantwoordelijkheid.

---

# 7. QuoteService

QuoteService haalt actuele marktdata op.

Eigenschappen:

* batch downloads
* batch size configureerbaar
* fouttolerantie
* yfinance-output onderdrukt
* quote cache
* cache statistieken

Cache:

```text
data/cache/quotes.json
```

TTL:

```text
15 minuten
```

QuoteService houdt bij:

* Quotes uit cache
* Nieuwe quotes
* Niet gevonden quotes

---

# 8. TechnicalScanner

Ondersteunt momenteel:

* SMA20
* SMA50
* RSI14
* 20-daags momentum

Scoring:

```text
Koers boven SMA20
Koers boven SMA50
SMA20 > SMA50
RSI gezond
20-daags momentum positief
```

Resultaat:

```text
BUY
HOLD
IGNORE
```

---

# 9. RankingEngine

RankingEngine:

* verwijdert IGNORE
* sorteert op confidence
* toont uitsluitend Top 3 koopkansen

---

# 10. Laatste Testresultaten

## Volledige universe scan

Universe:

```text
6204 aandelen
```

Resultaat:

```text
Quotes:                     6053
Quotes uit cache:            981
Quotes nieuw opgehaald:     5072
Quotes niet gevonden:        151

Na prijsfilter:             5096
Na volumefilter:            1045
Na liquiditeitsfilter:       850
Na Relative Strength:        849
Na Momentum:                 500

Technische kandidaten:       100
Technische resultaten:        97

Koopkansen:                   3
```

Performance:

```text
QuoteService:          140.58 sec
TechnicalScanner:        5.28 sec
Pipeline totaal:       145.86 sec
```

Laatste Top 3:

```text
FCEL
CNVS
APPS
```

---

# 11. Belangrijkste Conclusies

De ScanPipeline werkt volledig.

De modulaire architectuur is stabiel.

De filters functioneren correct.

De TechnicalScanner is snel genoeg.

De grootste bottleneck bevindt zich in QuoteService.

Deze bottleneck wordt veroorzaakt door de huidige marktdata-provider (`yfinance`) en niet door de architectuur van de pipeline.

---

# 12. Openstaande Verbeterpunten

* Market Data Layer introduceren.
* QuoteService loskoppelen van yfinance.
* Historische data cachen.
* DecisionEngine uitbreiden.
* Risk Management toevoegen.
* GUI koppelen aan de nieuwe ScanPipeline.
* Paper Trading implementeren.
* Broker-integratie voorbereiden.

---

# 13. Eerstvolgende Sprint

## Sprint 6 — Market Data Layer

Doel:

QuoteService wordt een orchestrator.

Nieuwe map:

```text
services/
    market_data/
```

Geplande bestanden:

```text
base_provider.py
yahoo_provider.py
finnhub_provider.py
polygon_provider.py
alpaca_provider.py
```

Voordelen:

* eenvoudig wisselen van databron
* betere schaalbaarheid
* retries
* rate limiting
* provider-specifieke caching
* voorbereiding op professionele marktdata

---

# 14. Belangrijke Ontwikkelregels

Bij iedere volgende sprint:

* Altijd volledige bestanden leveren.
* Eerst architectuur bespreken.
* Daarna implementeren.
* Daarna testen.
* Daarna PROJECT_STATUS.md bijwerken.

---

# 15. Bericht voor een Nieuwe Chat

Wanneer een nieuwe ChatGPT-chat wordt gestart, gebruik dan de volgende instructie:

"Lees eerst PROJECT_STATUS.md volledig door. Dit document is de actuele bron van waarheid voor Project Orion.

Werk verder vanaf het einde van Sprint 5.

De ScanPipeline is afgerond en functioneert.

De hoogste prioriteit is Sprint 6: het bouwen van een professionele Market Data Layer zodat QuoteService niet langer direct afhankelijk is van yfinance.

Werk steeds één sprint tegelijk uit, lever volledige bestanden aan en bewaak de bestaande architectuur. Houd de GUI eenvoudig en laat Orion alle technische analyse uitvoeren. De gebruiker krijgt uitsluitend duidelijke BUY-, SELL- of HOLD-adviezen."

---

# Eindstatus

**Sprint 5: Afgerond** ✅

De scanner is succesvol omgebouwd naar een modulaire, schaalbare ScanPipeline.

De volgende ontwikkelfase is Sprint 6: **Market Data Layer**.
