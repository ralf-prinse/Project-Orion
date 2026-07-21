# Project Orion

Project Orion is een headless, deterministisch handelsplatform dat momenteel
uitsluitend autonoom handelt via een IBKR Paper-account met `DU`-prefix. TWS is
de operationele GUI; Orion zelf levert CLI-output en persistente auditdata.

## Canonieke autonome keten

```text
EU/US universe en beurskalender
  -> Yahoo historische data en indicatoren
  -> services.orchestration.TradingPipeline
  -> services.trading_decision
  -> canonieke RiskPlan en PortfolioAllocator/RiskManager
  -> session-, earnings- en concentration gates
  -> actuele IBKR bid/ask execution-quality gate
  -> ExecutionEngine en IbkrBroker
  -> IBKR Paper bracket/OCA fill en broker-truth synchronisatie
  -> managed exits, journals en CompletedTradeRecord
```

Nieuws draait uitsluitend in `SHADOW`-modus. Het wordt opgehaald, genormaliseerd
en gejournaliseerd, maar kan geen BUY, SELL, quantity, riskplan of order
wijzigen. Learning- en recommendationservices zijn eveneens niet met de
autonome runtime verbonden.

Execution mode `SHADOW` is een afzonderlijke veiligheidsgrens voor fictieve
trades zonder betaald IBKR-marktdata-abonnement. De modus gebruikt een lokale
shadowbroker, aparte persistentie en Yahoo-referentieprijzen; IBKR-quotes,
orders, broker-sync en positieadoptie zijn niet bereikbaar.

## Belangrijkste entrypoints

- `run_autonomous_ibkr_paper.py`: begrensde autonome IBKR Paper-cycli;
- `test_ibkr_account_reader.py`: read-only account- en positiediagnose;
- `run_dashboard.py`: optionele tekstuele rapportage zonder desktop-GUI.
- `analyze_completed_trades.py`: offline netto-expectancy na geraamde kosten.

## Veilige observatiecyclus

```powershell
$env:ORION_IBKR_PAPER_ACCOUNT_ID="<DU_PAPER_ACCOUNT>"
$env:ORION_IBKR_EXECUTION_MODE="BUY_AND_SELL"
$env:ORION_IBKR_ALLOW_ORDERS="false"
$env:ORION_IBKR_NEWS_MODE="SHADOW"
$env:ORION_IBKR_CYCLES="1"

.\.venv\Scripts\python.exe run_autonomous_ibkr_paper.py
```

Ordertoestemming moet expliciet worden aangezet en blijft beperkt tot Paper
Trading. Activeer dit project niet op een live-moneyaccount.

## Geïsoleerde shadowcyclus zonder IBKR-marktdata

```powershell
$env:ORION_IBKR_PAPER_ACCOUNT_ID="<DU_PAPER_ACCOUNT>"
$env:ORION_IBKR_EXECUTION_MODE="SHADOW"
$env:ORION_IBKR_ALLOW_ORDERS="false"
$env:ORION_IBKR_NEWS_MODE="DISABLED"
$env:ORION_IBKR_CYCLES="1"

.\.venv\Scripts\python.exe run_autonomous_ibkr_paper.py
```

Bevestig met `START ONE ORION SHADOW CYCLE`. Resultaten worden uitsluitend
geschreven naar bestanden met prefix `data/orion_shadow`; deze portefeuille
wordt nooit gemengd met de echte IBKR Paper-portefeuille.

## Realistische €500-shadowcyclus

Gebruik `MICRO_500` om strategiegedrag met het beoogde startkapitaal te meten
zonder de bestaande €10.000-shadowportefeuille te wijzigen:

```powershell
$env:ORION_IBKR_PAPER_ACCOUNT_ID="<DU_PAPER_ACCOUNT>"
$env:ORION_IBKR_EXECUTION_MODE="SHADOW"
$env:ORION_IBKR_ALLOW_ORDERS="false"
$env:ORION_CAPITAL_PROFILE="MICRO_500"
$env:ORION_IBKR_PRICING_PLAN="TIERED"
$env:ORION_MONTHLY_MARKET_DATA_COST_EUR="3.00"
$env:ORION_IBKR_NEWS_MODE="DISABLED"
$env:ORION_IBKR_CYCLES="1"

.\.venv\Scripts\python.exe run_autonomous_ibkr_paper.py
```

Bevestig met `START ONE ORION MICRO 500 SHADOW CYCLE`. Dit profiel start met
€500, houdt minimaal 30% cash aan, staat maximaal twee posities en twee nieuwe
entries per dag toe, gebruikt een 60-minuten herinstappauze en een 90-minuten
tijdstop. Entries gebruiken vijf handelsdagen aan uitsluitend afgeronde
5-minutencandles. Een nog lopende candle wordt verwijderd en data ouder dan tien
minuten wordt fail-closed geweigerd. Een economische gate weigert een entry wanneer geraamde retourkosten
meer dan 2% van de positie vragen of kosten plus nettodoel en buffer een
brutobeweging boven 1,6% vereisen. Het netto microdoel is EUR 0,50; hoge
Europese minimumcommissies blijven daardoor via de economische gate
fail-closed. De eigen state gebruikt prefix
`data/orion_shadow_micro_500`.

## Architectuurgrenzen

- `services/trading_decision`: enige decisionimplementatie van de actieve
  `TradingPipeline`;
- `services/decisions`: geïsoleerde research-/explainabilitylaag, niet actief
  in de autonome runtime;
- `services/news`: provider-onafhankelijke observatielaag;
- `services/ibkr`: account-, nieuws-, order- en synchronisatieadapters;
- `services/learning_pipeline.py`: offline research, zonder schrijfpad naar
  handelsconfiguratie of orders.

Zie [IBKR runbook](docs/IBKR_AUTONOMOUS_RUNBOOK.md),
[trading strategy](docs/TRADING_STRATEGY.md) en
[master architecture](docs/ORION_MASTER_ARCHITECTURE.md) voor de operationele
grenzen en veiligheidsregels.
