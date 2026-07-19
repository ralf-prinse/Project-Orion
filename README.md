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
