# Orion IBKR Autonomous Paper Runbook

Laatste update: 21-07-2026

## Veiligheidsgrens

Deze runtime ondersteunt uitsluitend een IBKR Paper-account met `DU`-prefix.
Live-moneyaccounts zijn niet toegestaan. Begin na iedere code- of
universumwijziging met orders uitgeschakeld.

Actuele schaalconfiguratie:

- 100 symbolen: 50 VS, 25 Amsterdam en 25 Xetra;
- alleen open beurzen worden geanalyseerd;
- historische downloads in batches van 25;
- cache-TTL 15 minuten;
- maximaal 3 nieuwe posities per cyclus;
- maximaal 20 open posities totaal;
- standaard 1 cyclus en 900 seconden scaninterval.

Actuele exitconfiguratie:

- standaard `COST_AWARE_SMALL_PROFIT` voor deze IBKR Paper-runner;
- Amerikaanse posities: EUR 5 geschatte nettowinst, EUR 8 geschat nettoverlies;
- Europese posities: EUR 10 geschatte nettowinst, EUR 15 geschat nettoverlies;
- standaard prijsmodel `FIXED`, totdat het account aantoonbaar `TIERED` gebruikt;
- commissie, slippage, externe kosten en optionele valutaconversie worden
  conservatief geraamd;
- de bestaande dynamische stop-loss blijft altijd vóór de kleine-winstlogica
  gelden.

Actuele orderbescherming:

- iedere nieuwe BUY vereist actuele IBKR bid, ask en voldoende top-of-booksize;
- een te oude quote, te brede spread of te grote prijsafwijking blokkeert BUY;
- iedere BUY wordt als bracket met broker-native stop en profit-taker verstuurd;
- native children en software-SELL delen één trade-ID gebaseerde OCA-groep;
- native fills worden bij broker-sync met hun oorspronkelijke BUY-redenering
  aan `CompletedTradeRecord` gekoppeld;
- sessieverlies, drie opeenvolgende verliezen of drie brokerfouten blokkeren
  nieuwe BUY's, maar niet het beheer van bestaande posities;
- sector- en correlatieclustermetadata staat in
  `data/instrument_metadata.csv`.

Voor orderinzending moet het account actuele API-marktdata hebben voor de
betreffende Amerikaanse en Europese noteringen. Delayed of ontbrekende
bid/askdata is bewust niet voldoende en resulteert in een afwijzing.

## Geïsoleerde shadowmodus zonder betaald marktdata-abonnement

Gebruik deze modus om signalen, allocatie, lifecycle, kostenraming en trade
memory te observeren zonder een IBKR-quote of order aan te vragen:

```powershell
$env:ORION_IBKR_PAPER_ACCOUNT_ID="<YOUR_DU_PAPER_ACCOUNT_ID>"
$env:ORION_IBKR_EXECUTION_MODE="SHADOW"
$env:ORION_IBKR_ALLOW_ORDERS="false"
$env:ORION_IBKR_NEWS_MODE="DISABLED"
$env:ORION_IBKR_CYCLES="1"
$env:ORION_IBKR_SCAN_INTERVAL_SECONDS="300"
$env:ORION_IBKR_EXIT_STRATEGY="COST_AWARE_SMALL_PROFIT"
$env:ORION_IBKR_PRICING_PLAN="FIXED"

.\.venv\Scripts\python.exe run_autonomous_ibkr_paper.py
```

Bevestiging:

```text
START ONE ORION SHADOW CYCLE
```

`SHADOW` weigert te starten als `ORION_IBKR_ALLOW_ORDERS=true`. Broker-sync,
adoptie van IBKR-posities, live bid/ask, native orders en protective-fill-
reconciliatie zijn uitgeschakeld. De geïsoleerde resultaten staan in:

- `data/orion_shadow_trading_session.json`;
- `data/orion_shadow_paper_portfolio.json`;
- `data/orion_shadow_decision_journal.jsonl`;
- `data/orion_shadow_trade_journal.jsonl`;
- `data/orion_shadow_completed_trades.jsonl`.

Shadowfills bewaren de Yahoo-referentieprijs. De journal neemt adverse slippage
en de bestaande conservatieve IBKR round-tripkostenraming apart mee. Dit bewijst
niet dat dezelfde fill bij IBKR haalbaar zou zijn.

## Afzonderlijk MICRO_500-shadowprofiel

Gebruik dit profiel voor een realistische EUR 500-kapitaalproef. Het is
technisch beperkt tot `SHADOW` en gebruikt geen bestanden van de standaard
EUR 10.000-shadowrun:

```powershell
$env:ORION_IBKR_PAPER_ACCOUNT_ID="<YOUR_DU_PAPER_ACCOUNT_ID>"
$env:ORION_IBKR_EXECUTION_MODE="SHADOW"
$env:ORION_IBKR_ALLOW_ORDERS="false"
$env:ORION_CAPITAL_PROFILE="MICRO_500"
$env:ORION_IBKR_PRICING_PLAN="TIERED"
$env:ORION_MONTHLY_MARKET_DATA_COST_EUR="3.00"
$env:ORION_IBKR_NEWS_MODE="DISABLED"
$env:ORION_IBKR_CYCLES="1"
$env:ORION_IBKR_SCAN_INTERVAL_SECONDS="300"
$env:ORION_IBKR_EXIT_STRATEGY="COST_AWARE_SMALL_PROFIT"

.\.venv\Scripts\python.exe run_autonomous_ibkr_paper.py
```

Bevestiging:

```text
START ONE ORION MICRO 500 SHADOW CYCLE
```

Profielgrenzen:

- EUR 500 startkapitaal en EUR 350 maximale positie;
- maximaal één open positie en één nieuwe positie per cyclus;
- maximaal één entry per UTC-dag, vijf per UTC-week en 240 minuten cooldown;
- minimaal 30% cashreserve en maximaal 70% totale exposure;
- TIERED-kostenmodel, plus EUR 3 maandelijkse marktdata verdeeld over twaalf
  verwachte round-trips;
- maximaal 0,6% geschatte round-tripkosten ten opzichte van positiewaarde;
- maximaal 2,5% vereiste brutobeweging inclusief kosten, nettodoel en EUR 0,50
  onzekerheidsbuffer;
- alleen `XUSA` kan entries krijgen; Amsterdam en Xetra blijven analyseerbaar;
- VS-nettodoel EUR 4,50 en nettoverlieslimiet EUR 3,00, minimaal 1,5 reward/risk;
- 180 minuten maximale houdtijd en 0,6% dagelijkse verliescircuitbreaker;
- geen entry in de eerste vijftien minuten of laatste drie sessie-uren;
- entry vereist bullish 5m, stijgende 15m, sessie-VWAP, relatief volume en
  positieve 15-minutensterkte tegenover SPY;
- vijf handelsdagen aan 5-minutencandles met twee minuten cache;
- de lopende candle wordt nooit geanalyseerd en de nieuwste volledige candle
  mag maximaal vijftien minuten na candle completion oud zijn;
- deze marge vangt de gemeten Yahoo-publicatievertraging op; oudere data wordt
  nog steeds fail-closed geweigerd;
- bij starten om 09:00 wacht Orion fail-closed tot de eerste volledige candle
  rond 09:05 beschikbaar is.
- shadowcash is netto: de volledige conservatieve round-tripkosten worden bij
  exit afgetrokken en bij starten tegen completed trades gereconcilieerd.

Bestanden:

- `data/orion_shadow_micro_500_trading_session.json`;
- `data/orion_shadow_micro_500_paper_portfolio.json`;
- `data/orion_shadow_micro_500_decision_journal.jsonl`;
- `data/orion_shadow_micro_500_trade_journal.jsonl`;
- `data/orion_shadow_micro_500_completed_trades.jsonl`.

### Volledige Europese en Amerikaanse shadowdag

Gebruik op een normale gezamenlijke handelsdag rond 08:55 Nederlandse tijd:

```powershell
.\start_orion_micro_shadow_full_day.ps1 -PaperAccountId "DU..."
```

De starter stelt uitsluitend het gecontroleerde profiel in:

- `SHADOW`, ordertoestemming `false` en nieuws `DISABLED`;
- `MICRO_500`, `TIERED` en EUR 3 maandelijkse marktdata-overhead;
- 160 cycli met exact 300 seconden interval;
- `COST_AWARE_SMALL_PROFIT` met de actuele profielgrenzen.

Bevestig exact met:

```text
START 160 ORION MICRO 500 SHADOW CYCLES
```

Bij starten rond 08:55 loopt de sessie ongeveer tot 22:10. Amsterdam en Xetra
worden vanaf de eerste volledige candle rond 09:05 geanalyseerd, maar kunnen in
`MICRO_500` geen entry krijgen. De Verenigde Staten worden vanaf de eerste
volledige candle geanalyseerd; entries blijven tot 15 minuten na opening
geblokkeerd en stoppen drie uur voor sluiting. Gesloten markten worden
fail-closed overgeslagen. TWS is voor deze geïsoleerde shadowrun niet nodig.

Verander `ORION_MONTHLY_MARKET_DATA_COST_EUR` later naar het werkelijk betaalde
maandbedrag. Een lage of nulwaarde is geen toestemming om ontbrekende realtime
bid/askdata als betrouwbaar te behandelen.

## Eén veilige observatiecyclus

```powershell
$env:ORION_IBKR_PAPER_ACCOUNT_ID="<YOUR_DU_PAPER_ACCOUNT_ID>"
$env:ORION_IBKR_EXECUTION_MODE="BUY_AND_SELL"
$env:ORION_IBKR_ALLOW_ORDERS="false"
$env:ORION_IBKR_CYCLES="1"
$env:ORION_IBKR_SCAN_INTERVAL_SECONDS="900"
$env:ORION_IBKR_EXIT_STRATEGY="COST_AWARE_SMALL_PROFIT"
$env:ORION_IBKR_PRICING_PLAN="FIXED"
$env:ORION_IBKR_NEWS_MODE="SHADOW"

.\.venv\Scripts\python.exe run_autonomous_ibkr_paper.py
```

Bevestiging:

```text
START ONE AUTONOMOUS IBKR PAPER CYCLE
```

## Begrensde observatiesessie

Onderstaand voorbeeld draait acht cycli met vijftien minuten ertussen. Dat is
ongeveer 1 uur en 45 minuten tussen de eerste en laatste starttijd.

```powershell
$env:ORION_IBKR_ALLOW_ORDERS="false"
$env:ORION_IBKR_CYCLES="8"
$env:ORION_IBKR_SCAN_INTERVAL_SECONDS="900"

.\.venv\Scripts\python.exe run_autonomous_ibkr_paper.py
```

Bevestiging:

```text
START 8 AUTONOMOUS IBKR PAPER CYCLES
```

Stop een actieve sessie zo nodig met `Ctrl+C`. Schakel ordertoestemming pas in
nadat een veilige observatie de verwachte 100 symbolen, marktsluitingen,
afwijzingsredenen en risicometingen heeft getoond.

## Ordertoestemming

`ORION_IBKR_ALLOW_ORDERS="true"` kan echte IBKR Paper BUY- en SELL-orders
plaatsen. Gebruik dit eerst met één cyclus. De positiecap van 20 is alleen een
bovengrens; cashreserve, exposure, trade-risk, portefeuillerisico en drawdown
kunnen een veel lager aantal afdwingen.

Controleer in TWS welk prijsmodel werkelijk bij het account hoort. Alleen als
dat `Tiered` is, stel je in PowerShell het volgende in:

```powershell
$env:ORION_IBKR_PRICING_PLAN="TIERED"
```

Terugschakelen naar de oorspronkelijke swing-exits kan expliciet met:

```powershell
$env:ORION_IBKR_EXIT_STRATEGY="SWING"
```

De netto-P&L is in deze fase een kostenraming en geen definitief IBKR-
commission report. Gebruik de strategie daarom eerst met orders uitgeschakeld
en daarna uitsluitend op het `DU` Paper-account. Activeer haar niet op een
live-moneyaccount.

## Nieuws-shadowmodus

`ORION_IBKR_NEWS_MODE="SHADOW"` vraagt via een afzonderlijke read-only TWS-
client recente headlines op voor open posities en maximaal twintig van de
hoogst gerangschikte kandidaten. Beschikbaarheid vereist minstens één door de
IBKR API geretourneerde nieuwsprovider; abonnementen en dekking verschillen per
account. Controleer na een observatiecyclus:

- `data/ibkr_news_events.jsonl`: unieke genormaliseerde gebeurtenissen;
- `data/ibkr_news_assessments.jsonl`: beoordeling per symbool en cyclus;
- `data/ibkr_autonomous_trade_journal.jsonl`: nieuwscontext bij entry/exit;
- `data/ibkr_completed_trades.jsonl`: gekoppelde volledig gesloten trades.

`blocking_recommended=true` is alleen een meetwaarde. In SHADOW-modus blijft de
oorspronkelijke technische/riskbeslissing exact ongewijzigd. Een lege provider-
lijst, timeout of ontbrekend abonnement wordt als `UNAVAILABLE` gejournaliseerd
en stopt BUY/SELL niet. Uitschakelen kan expliciet met:

```powershell
$env:ORION_IBKR_NEWS_MODE="DISABLED"
```

Gebruik `CompletedTradeRecord` voorlopig uitsluitend voor rapportage en offline
onderzoek. Orion mag nog geen strategie- of risicolimieten zelfstandig wijzigen.

Offline nettowachting bekijken:

```powershell
.\.venv\Scripts\python.exe analyze_completed_trades.py
```

Earnings-blackouts gebruiken uitsluitend expliciete regels met kolommen
`symbol,earnings_date` in `data/earnings_calendar.csv`, waarbij de datum
`YYYY-MM-DD` is. Vul dit bestand alleen uit een gecontroleerde kalenderbron.
Ontbrekende data wordt als onbekend behandeld; Orion verzint geen datum uit
headlines of AI-schattingen.
