# ============================================================
# PROJECT ORION
# PROJECT STATUS
# ============================================================

Version: 3.0
Status: ACTIVE DEVELOPMENT
Last Updated: 26 June 2026

Current Sprint:
Sprint 6.5 COMPLETE ✅

Next Sprint:
Sprint 6.6 – Historical Data Layer

Project State:
READY TO CONTINUE

# ============================================================
# ⚠️ VOOR CHATGPT - LEES DIT EERST
# ============================================================

Voordat je antwoord geeft, lees je eerst dit volledige document.

Dit document is de actuele bron van waarheid voor Project Orion.

Respecteer de bestaande architectuur.

Begin NIET opnieuw met ontwerpen.

Begin NIET opnieuw met plannen.

Werk altijd verder vanaf de laatst afgeronde sprint.

Lever altijd volledige bestanden aan.

Gebruik nooit losse codefragmenten tenzij daar expliciet om gevraagd wordt.

Werk altijd één sprint tegelijk af.

Na iedere afgeronde sprint moet PROJECT_STATUS.md opnieuw worden bijgewerkt.

# ============================================================
# PROJECT DOEL
# ============================================================

Project Orion is een professionele AI Swing Trading Assistant.

Het uiteindelijke doel is een desktopapplicatie die zelfstandig de Amerikaanse aandelenmarkt analyseert en uitsluitend duidelijke handelsadviezen teruggeeft.

De gebruiker hoeft zelf geen technische analyse uit te voeren.

Orion doet alle analyses.

De gebruiker krijgt uiteindelijk alleen:

• BUY
• SELL
• HOLD
• GEEN ACTIE

De focus ligt volledig op swing trading.

Gemiddelde houdduur:

- enkele uren
- één handelsdag
- twee tot vijf dagen

Orion is nadrukkelijk geen:

- daytrading scanner
- scalping systeem
- lange termijn beleggingssoftware
- crypto platform
- optiesoftware

# ============================================================
# ONTWIKKELFILOSOFIE
# ============================================================

Tijdens de ontwikkeling gelden altijd de volgende regels.

1. Architectuur vóór functionaliteit.
2. Iedere module heeft één duidelijke verantwoordelijkheid.
3. We werken uitsluitend met volledige bestanden.
4. Orion moet modulair uitbreidbaar blijven.
5. De GUI blijft eenvoudig.
6. De gebruiker ziet geen technische indicatoren.
7. Orion vertaalt technische analyse naar begrijpelijke taal.
8. Orion mag liever géén trade adviseren dan een slechte trade.
9. Schaalbaarheid staat altijd centraal.
10. Orion moet uiteindelijk minimaal 10.000 aandelen per scan kunnen verwerken.

# ============================================================
# HUIDIGE PROJECTSTATUS
# ============================================================

Sprint 5 is volledig afgerond.

Sprint 6.1 t/m Sprint 6.5 zijn eveneens volledig afgerond.

De nieuwe modulaire scannerarchitectuur is operationeel.

De scanner verwerkt momenteel het volledige Amerikaanse aandelenuniversum.

Huidige universum:

Nasdaq:
3538 aandelen

US Other:
2666 aandelen

Totaal:

6204 Amerikaanse aandelen

De scanner levert momenteel automatisch de Top 3 koopkansen op.

# ============================================================
# HUIDIGE ARCHITECTUUR
# ============================================================

UniverseLoader

↓

QuoteService

↓

MarketDataProvider

↓

YahooMarketDataProvider

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

Top 3 Opportunities

Deze architectuur is leidend.

Nieuwe functionaliteit wordt uitsluitend toegevoegd door nieuwe modules toe te voegen.

Bestaande verantwoordelijkheden worden niet vermengd.

# ============================================================
# HOOFDMODULES
# ============================================================

## Universe

✅ UniverseManager 2.0

✅ UniverseDownloader

✅ UniverseLoader

---

## Scanner

✅ ScanPipeline

✅ QuoteService

✅ PriceFilter

✅ VolumeFilter

✅ LiquidityFilter

✅ RelativeStrengthFilter

✅ MomentumFilter

✅ TechnicalScanner

✅ RankingEngine

---

## Portfolio

✅ Portfolio

✅ TradeManager

✅ TradeHistoryStore

✅ MarketFilter

---

## GUI

✅ Modulaire GUI

De GUI toont uitsluitend informatie die relevant is voor de gebruiker.

Technische scannerinformatie blijft verborgen.

---

## Market Data Layer

Nieuw gebouwd tijdens Sprint 6.

Bestaat momenteel uit:

✅ MarketDataProvider

✅ YahooMarketDataProvider

✅ Provider Statistics

✅ Quote Cache

✅ Negative Cache

QuoteService is niet langer direct afhankelijk van yfinance.

Nieuwe providers kunnen later zonder wijzigingen aan de scanner worden toegevoegd.

# ============================================================
# UNIVERSE
# ============================================================

Het aandelenuniversum wordt volledig automatisch beheerd.

UniverseManager is verantwoordelijk voor:

- opbouwen van het universum
- samenvoegen van verschillende markten
- verwijderen van duplicaten
- opslaan van het definitieve universum

UniverseDownloader downloadt de actuele Amerikaanse beursnoteringen.

UniverseLoader wordt gebruikt door de ScanPipeline.

UniverseLoader ondersteunt:

- volledige scan
- beperkte testscans
- automatische normalisatie
- verwijderen van dubbele symbolen

Huidige universum:

Nasdaq:
3538

US Other:
2666

Totaal:

6204 Amerikaanse aandelen

Dit universum vormt de basis van iedere scan.

# ============================================================
# SCANPIPELINE
# ============================================================

De oude ScannerService is uitgefaseerd.

Alle nieuwe ontwikkeling vindt plaats binnen ScanPipeline.

ScanPipeline bevat zelf geen analyse-logica.

De pipeline is uitsluitend verantwoordelijk voor het aanroepen van de verschillende modules in de juiste volgorde.

Pipeline:

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

Top 3 Opportunities

Iedere stap heeft precies één verantwoordelijkheid.

Nieuwe modules worden als losse pipeline-stap toegevoegd.

# ============================================================
# QUOTESERVICE
# ============================================================

QuoteService is uitsluitend verantwoordelijk voor:

- ophalen van quote-data
- beheren van quote cache
- beheren van negative cache
- communiceren met MarketDataProvider
- teruggeven van uniforme Quote-objecten

QuoteService doet nadrukkelijk GEEN:

- technische analyse
- ranking
- portfoliobeheer
- koopadviezen

QuoteService is een orchestrator.

# ============================================================
# MARKET DATA LAYER
# ============================================================

Tijdens Sprint 6 is de volledige Market Data Layer gebouwd.

Structuur:

services/

market_data/

- __init__.py
- base_provider.py
- yahoo_provider.py

MarketDataProvider vormt de abstracte interface.

Iedere toekomstige databron hoeft uitsluitend deze interface te implementeren.

Hierdoor blijft de rest van Orion volledig ongewijzigd.

Toekomstige providers:

- Polygon
- Alpaca
- Finnhub
- TwelveData
- Interactive Brokers

De scanner weet niet welke provider actief is.

Alle communicatie verloopt via MarketDataProvider.

# ============================================================
# QUOTE CACHE
# ============================================================

Quote cache:

data/cache/quotes.json

Cache TTL:

15 minuten

De cache bevat:

- actuele prijs
- volume
- vorige slotkoers
- procentuele verandering
- timestamp

Bij een cache-hit wordt geen nieuwe API-call uitgevoerd.

Hierdoor worden herhaalde scans extreem snel.

# ============================================================
# NEGATIVE CACHE
# ============================================================

Sprint 6.5 introduceerde een Negative Cache.

Wanneer een aandeel tijdelijk niet beschikbaar is via de provider, wordt dit tijdelijk opgeslagen.

Resultaat:

- geen onnodige API-calls
- minder belasting van Yahoo
- veel snellere herhaalde scans

Tijdens de laatste test:

Negative cache hits:

19

Provider requests:

0

Hierdoor werd de provider helemaal niet meer aangeroepen voor ontbrekende symbolen.

# ============================================================
# TECHNICAL SCANNER
# ============================================================

TechnicalScanner analyseert uitsluitend aandelen die de eerdere filters hebben overleefd.

Momenteel ondersteunt de scanner:

- SMA20
- SMA50
- RSI14
- 20-daags momentum

De scanner bepaalt vervolgens:

- BUY
- HOLD
- IGNORE

De TechnicalScanner downloadt momenteel nog zelf historische candles.

Dit verandert in Sprint 6.6.

Na Sprint 6.6 gebruikt de scanner uitsluitend HistoricalDataProvider.

# ============================================================
# RANKING ENGINE
# ============================================================

RankingEngine ontvangt alle technische resultaten.

Taken:

- verwijderen van IGNORE-resultaten
- sorteren op confidence
- teruggeven van uitsluitend de Top 3 koopkansen

RankingEngine haalt zelf geen marktdata op.

RankingEngine voert geen technische analyse uit.

# ============================================================
# PERFORMANCE
# ============================================================

Laatste succesvolle test:

Universe:

1000 aandelen

Quotes:

981

Quotes uit cache:

981

Nieuwe downloads:

0

Negative cache hits:

19

Technische kandidaten:

100

Technische resultaten:

99

Koopkansen:

3

Pipeline Performance:

QuoteService:

0.02 seconden

TechnicalScanner:

ongeveer 1.9 seconden

Totale pipeline:

ongeveer 2 seconden

Hieruit blijkt dat de scanner zelf inmiddels zeer snel is.

De grootste vertraging ontstaat uitsluitend wanneer nieuwe marktdata moet worden opgehaald.

Door de Market Data Layer kan deze bottleneck later eenvoudig worden opgelost zonder wijzigingen aan de ScanPipeline.

# ============================================================
# AFGERONDE SPRINTS
# ============================================================

Sprint 1
✅ Afgerond

Opgeleverd:

- Eerste projectstructuur
- Basis GUI
- Eerste scanner
- Eerste portfolio-opzet

---

Sprint 2
✅ Afgerond

Opgeleverd:

- Portfolio Engine
- Decision Engine (eerste versie)
- Database-opslag
- Basis analyseflow

---

Sprint 3
✅ Afgerond

Opgeleverd:

- Modulaire GUI
- Analyse-opslag
- Verbeterde projectstructuur

---

Sprint 4
✅ Afgerond

Opgeleverd:

- UniverseManager 2.0
- UniverseDownloader
- UniverseLoader
- Amerikaans aandelenuniversum
- 6204 aandelen

---

Sprint 5
✅ Afgerond

Opgeleverd:

- Volledige ScanPipeline
- QuoteService
- PriceFilter
- VolumeFilter
- LiquidityFilter
- RelativeStrengthFilter
- MomentumFilter
- TechnicalScanner
- RankingEngine
- Performance logging
- Top 3 koopkansen

De oude ScannerService is vervangen door een modulaire architectuur.

---

Sprint 6.1
✅ Afgerond

Opgeleverd:

- MarketDataProvider
- YahooMarketDataProvider

QuoteService is niet langer direct afhankelijk van yfinance.

---

Sprint 6.2
✅ Afgerond

Opgeleverd:

- Los provider-testscript
- Provider onafhankelijk testbaar

---

Sprint 6.3
✅ Afgerond

Opgeleverd:

- Provider Statistics

Iedere provider rapporteert nu:

- providernaam
- gevraagde symbolen
- ontvangen quotes
- ontbrekende quotes
- duur

---

Sprint 6.4
✅ Afgerond

Opgeleverd:

Providerinformatie zichtbaar in ScanPipeline.

Tijdens iedere scan wordt nu geregistreerd:

- gebruikte provider
- provider prestaties
- provider statistieken

---

Sprint 6.5
✅ Afgerond

Opgeleverd:

- Negative Cache

Niet gevonden aandelen worden tijdelijk onthouden.

Resultaat:

- minder API-calls
- snellere herhaalde scans
- lagere belasting van Yahoo

Tijdens de laatste test:

Provider requests:

0

Negative cache hits:

19

QuoteService:

0.02 seconden

Pipeline:

ongeveer 2 seconden

# ============================================================
# OPENSTAANDE VERBETERPUNTEN
# ============================================================

De huidige architectuur is stabiel.

Er zijn geen bekende architectuurproblemen.

Openstaande verbeteringen:

- Historical Data Layer
- Historical Cache
- DecisionEngine 2.0
- Risk Manager
- Position Sizing
- AI Trade Reasoning
- Paper Trading
- Broker Integratie
- GUI koppelen aan nieuwe ScanPipeline

# ============================================================
# EERSTVOLGENDE SPRINT
# ============================================================

Sprint 6.6

Historical Data Layer

Doel:

TechnicalScanner mag geen historische candles meer downloaden.

Daarvoor wordt een nieuwe abstractielaag gebouwd.

Nieuwe map:

services/

market_data/

Nieuwe bestanden:

historical_provider.py

historical_cache.py

Later uitbreidbaar met:

- Yahoo Historical Provider
- Polygon Historical Provider
- Alpaca Historical Provider

Na Sprint 6.6 haalt uitsluitend HistoricalDataProvider historische candles op.

TechnicalScanner gebruikt daarna alleen deze provider.

Hierdoor wordt ook historische data volledig provider-onafhankelijk.

# ============================================================
# BELANGRIJKE ONTWIKKELREGELS
# ============================================================

Tijdens alle volgende sprints gelden de volgende regels.

1.

Altijd volledige bestanden.

Nooit losse codefragmenten.

2.

Eerst architectuur.

Daarna implementeren.

3.

Nieuwe functionaliteit wordt altijd modulair toegevoegd.

4.

Bestaande verantwoordelijkheden worden niet vermengd.

5.

GUI blijft eenvoudig.

6.

De gebruiker ziet geen technische indicatoren.

7.

Debuginformatie blijft uitsluitend voor ontwikkelaars.

8.

Na iedere sprint wordt PROJECT_STATUS.md bijgewerkt.

# ============================================================
# INSTRUCTIE VOOR EEN NIEUWE CHATGPT
# ============================================================

Wanneer dit document wordt geüpload in een nieuwe chat gelden de volgende instructies.

Lees eerst het volledige document.

Gebruik dit document als enige bron van waarheid.

Begin NIET opnieuw met ontwerpen.

Begin NIET opnieuw met plannen.

Respecteer de bestaande architectuur.

Werk altijd één sprint tegelijk uit.

Lever altijd volledige bestanden aan.

Ga direct verder met de sprint die onder "Eerstvolgende Sprint" staat.

De huidige status van Project Orion is:

Sprint 6.5 volledig afgerond.

De volgende sprint is:

Sprint 6.6

Historical Data Layer.

# ============================================================
# CURRENT STATUS
# ============================================================

Project:

Project Orion

Status:

ACTIVE DEVELOPMENT

Laatste afgeronde sprint:

Sprint 6.5

Volgende sprint:

Sprint 6.6

Projectstatus:

READY TO CONTINUE

Laatste update:

26 juni 2026

Dit document is vanaf nu de enige actuele bron van waarheid voor de ontwikkelstatus van Project Orion.