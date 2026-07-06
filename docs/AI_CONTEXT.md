# ORION AI CONTEXT

---

# Documentation Information

Documentation Version

v1.12

Architecture Version

v2.1

Current Sprint

🚧 Sprint 5.5 — Trade Lifecycle / Trade Monitor

Last Updated

2026-07-05

---

# Purpose

This document provides the minimum context required for every new Orion development session.

It complements:

- ORION_MASTER_ARCHITECTURE.md
- PROJECT_STATUS.md
- TRADING_STRATEGY.md

Architectural specifications intentionally exist primarily inside ORION_MASTER_ARCHITECTURE.md.

This document contains only project state, development workflow and current implementation context.

---

# Current Project State

Project Orion has completed its deterministic trading foundation and has entered the Trade Lifecycle phase.

The deterministic backend is stable.

Mission Control is the operational center of Orion.

Trading Workspace provides deterministic BUY / HOLD / SELL analysis with explainability.

Trade Monitor is evolving from the former Position Monitor into the visible Trade Lifecycle area.

The project has moved beyond only finding opportunities.

Orion now supports the first working foundation of the full trade lifecycle:

Market Scan

↓

Opportunity

↓

Trading Decision

↓

Position Sizing

↓

Open Trade

↓

OpenTradeStore

↓

Trade Monitor

↓

Exit Intelligence

↓

Future Trade History

Current development focuses on making this lifecycle visible, persistent and usable inside the desktop application.

Every completed sprint must result in a visible improvement inside the desktop application.

---

# Current Sprint Status

## ✅ Sprint 5.1 — Portfolio & Position Sizing Foundation

Completed

✔ Portfolio Workspace redesigned

✔ Portfolio reduced to Trading Capital configuration

✔ PortfolioStore persistence connected

✔ Trading capital survives application restart

✔ Market Data panel displays market data age

✔ Opportunity cards display current market price

✔ OpportunityService introduced

✔ PositionSizingService introduced

✔ Mission Control prepared for position sizing

---

## ✅ Sprint 5.2 — Position Sizing Presentation

Completed

✔ Mission Control displays recommended share quantity

✔ Mission Control displays required investment

✔ Mission Control displays remaining available capital

✔ Mission Control displays available trading capital

✔ Mission Control displays budget status

✔ Trading Workspace explainability improved

✔ Risk, pressure score, confidence and position size now have human-readable explanations

✔ No TradingPipeline logic was changed

✔ AI remained explainability-only

---

## ✅ Sprint 5.3 — Position Monitor Foundation

Completed

✔ Trade lifecycle domain model introduced

✔ Trade model added as central domain object

✔ PositionMonitorResult introduced

✔ PositionMonitorService added

✔ PositionMonitorPresenter added

✔ PositionMonitorController added

✔ PositionMonitorWorkspace added

✔ Position Monitor integrated into main desktop navigation

✔ Manual position input available

✔ Position Monitor evaluates:

- symbol
- quantity
- entry price
- current price
- stop-loss
- take-profit

✔ Position Monitor displays:

- HOLD / SELL advice
- unrealized profit/loss
- market value
- distance to stop-loss
- distance to take-profit
- deterministic reason

✔ GUI layout stabilized with scrollable workspaces

✔ Mission Control opportunity cards fixed with wrapping card renderer

---

## ✅ Sprint 5.4 — Exit Intelligence Foundation

Completed

✔ ExitEvaluationService introduced

✔ PositionMonitorService now delegates exit decisions to ExitEvaluationService

✔ PositionMonitorResult expanded with:

- exit_score
- exit_reasons
- trend_status
- momentum_status
- risk_status

✔ PositionAnalysisService introduced

✔ Position Monitor now uses the existing AnalysisEngine

✔ Exit Intelligence now uses the same technical analysis infrastructure as the buying side

✔ ExitEvaluationService supports:

- stop-loss exit
- take-profit exit
- profit protection signal
- loss warning
- weak trend warning
- weak momentum warning
- weak structure warning
- volatility / structure risk warning

✔ Position Monitor GUI now displays:

- Exit Score
- Exit Score explanation
- Trend status
- Momentum status
- Risk status
- Exit reasons

✔ First version of deterministic exit intelligence is working in the GUI

✔ No AI decision logic added

✔ No duplicate indicator logic added

---

# Current Sprint

## 🚧 Sprint 5.5 — Trade Lifecycle / Trade Monitor

Primary goal

Transform Orion from an analysis workstation into a trade lifecycle workstation.

Implemented during Sprint 5.5 so far:

✔ Position Monitor conceptually renamed toward Trade Monitor in the desktop navigation

✔ Trade Monitor workspace title and copy updated

✔ FxRateService introduced

✔ Live EUR/USD conversion added through frankfurter.app

✔ PositionSizingService made FX-aware

✔ Mission Control now displays EUR account capital and USD market buying power

✔ TradingConfig introduced

✔ DEGIRO configured as the current broker context

✔ Account currency centralized as EUR

✔ Default market currency centralized as USD

✔ Supported markets configured:

- United States / NASDAQ / NYSE / USD
- Euronext Amsterdam / EUR
- Xetra / EUR

✔ IndicatorConfig preserved inside TradingConfig

✔ OpenTradeStore introduced

✔ Open trades persisted in data/open_trades.json

✔ TradeLifecycleService introduced

✔ TradeMonitorService introduced

✔ TradeMonitorService connected to ExitEvaluationService

✔ TradeMonitorPresenter introduced

✔ Trade Monitor GUI now displays an Open Trades panel

✔ Trading Workspace now contains an Open Trade button

✔ TradingController remembers the latest deterministic pipeline result

✔ Open Trade workflow is being connected from Trading Workspace toward OpenTradeStore

Current active objective

Complete the end-to-end visible lifecycle:

Trading Decision

↓

BUY

↓

Open Trade

↓

OpenTradeStore

↓

Trade Monitor

↓

ExitEvaluationService

↓

Trade History

No broker order execution exists.

No automatic real trading exists.

No DEGIRO API integration exists.

Orion is a deterministic trading assistant, not an execution bot.

---

# Current Working Components

## Backend

✔ TradingPipeline

✔ TechnicalScanner

✔ MarketScanner

✔ AnalysisEngine

✔ RiskEngine

✔ PositionSizingEngine

✔ IndicatorBuilder

✔ YahooProvider

✔ LiveScannerService

✔ OpportunityService

✔ PositionSizingService

✔ FxRateService

✔ TradingConfig

✔ IndicatorConfig

✔ PortfolioStore

✔ Trade model

✔ OpenTradeStore

✔ TradeHistoryStore

✔ TradeLifecycleService

✔ TradeMonitorService

✔ PositionMonitorService

✔ ExitEvaluationService

✔ PositionAnalysisService

✔ AI Context Builder

✔ AI Explanation Engine

The deterministic backend remains the single source of truth.

TradingPipeline remains the only source of BUY / HOLD / SELL trading decisions.

ExitEvaluationService remains the deterministic source for open-trade exit advice.

TradeLifecycleService manages trade lifecycle state.

OpenTradeStore owns open-trade persistence.

TradeMonitorService coordinates open-trade monitoring.

AI remains explainability-only.

---

## Desktop

✔ Workspace architecture

✔ Presenter architecture

✔ WorkspaceRenderer

✔ GuiWorkspace

✔ GuiWorkspacePanel

✔ BaseWorkspace with scrollable layout

✔ MissionControlWorkspace

✔ MissionControlController

✔ TradingWorkspace

✔ TradingController

✔ PortfolioWorkspace

✔ PositionMonitorWorkspace / Trade Monitor

✔ PositionMonitorController

✔ TradeMonitorPresenter

✔ ChartCanvas Framework

✔ Auto Refresh

Mission Control remains the primary workspace.

Trade Monitor is now the first visible implementation of the Trade Lifecycle area.

---

# Current Validation

Latest validation

```powershell
python run_tests.py

Expected result

✔ Regression tests pass

Additional targeted tests added during Sprint 5.5 include:

python test_fx_rate_service.py
python test_trading_config.py
python test_open_trade_store.py
python test_trade_lifecycle_service.py
python test_trade_monitor_service.py
python test_trade_monitor_presenter.py

Desktop validation

python app.py

Validated

✔ Application starts

✔ Navigation works

✔ Mission Control loads

✔ Trading Workspace loads

✔ Portfolio Workspace loads

✔ Trade Monitor loads

✔ Scan Market works

✔ Opportunity cards render correctly

✔ Workspaces support scrolling

✔ Trading Capital persistence works

✔ Mission Control displays live FX-aware position sizing

✔ Trading Workspace displays Open Trade button

✔ Open Trade button is disabled before a BUY analysis

✔ Trade Monitor displays Open Trades panel

✔ Manual trade monitoring still works

✔ Exit Intelligence displays analysis-based status

✔ Manual GUI validation completed

Current GUI State

Mission Control currently contains

✔ Scanner Status

✔ Scan Duration

✔ Market Data

✔ Universe Coverage

✔ Market Status

✔ Top Opportunities

✔ Opportunity Price

✔ FX-aware position sizing information

✔ Share quantity

✔ Required EUR investment

✔ USD market buying power

✔ Remaining capital

✔ Budget status

✔ Scan Market button

✔ Scroll-stable opportunity cards

Portfolio currently contains

✔ Trading Capital configuration

✔ Persistent capital storage

✔ Save button

Trading currently contains

✔ TradingPipeline analysis

✔ BUY / HOLD / SELL

✔ Confidence

✔ Pressure

✔ Risk

✔ Position Size

✔ Human-readable metric explanations

✔ AI Explanation

✔ Open Trade button

Trade Monitor currently contains

✔ Manual trade input

✔ Open Trades panel

✔ Exit Advies

✔ Exit Intelligence

✔ Exit Score

✔ Trend status

✔ Momentum status

✔ Risk status

✔ Exit reasons

✔ Winst / Verlies

✔ Risico & Winstdoel

✔ Status panel

The desktop now resembles a professional trading workstation rather than a simple dashboard.

Development Rules

Every Orion implementation must follow these rules.

Backend
Trading logic exists only inside backend services.
TradingPipeline remains the only source of BUY / HOLD / SELL decisions.
ExitEvaluationService remains the deterministic source of open-trade exit advice.
TradeLifecycleService owns trade lifecycle state transitions.
OpenTradeStore owns open-trade persistence.
TradeMonitorService coordinates open-trade monitoring.
LiveScannerService performs orchestration only.
OpportunityService builds presentation-ready opportunities.
PositionSizingService calculates deterministic position sizing only.
FxRateService owns live FX rate retrieval.
PositionMonitorService calculates manual trade monitoring result data and delegates exit advice.
PositionAnalysisService retrieves technical analysis for existing trades.
PortfolioStore owns persistence of trading capital.
Controllers coordinate services but never perform calculations.
Presentation
Widgets contain presentation only.
Panels contain presentation only.
Workspaces render and forward user actions only.
Presenters transform deterministic output into readable UI text only.
WorkspaceRenderer owns Mission Control rendering only.
ChartCanvas owns painting only.
No business logic may exist inside Qt widgets.
No technical analysis may be calculated inside the UI.
No exit decision may be calculated inside the UI.
No trade lifecycle state may be mutated inside UI widgets.
Artificial Intelligence

AI may

explain
summarize
compare
generate natural language

AI may never

generate BUY signals
generate SELL signals
generate EXIT signals
calculate indicators
calculate confidence
calculate position size
override deterministic output
override TradingPipeline
override ExitEvaluationService
open trades
close trades

Artificial Intelligence remains explainability only.

Current Architecture Direction

Mission Control continues to evolve into the operational heart of Orion.

The application is now moving from opportunity detection toward full trade lifecycle support.

Current deterministic opportunity flow

Market Data

↓

LiveScannerService

↓

TechnicalScanner / TradingPipeline

↓

OpportunityService

↓

MissionControlPresenter

↓

Mission Control

Current deterministic trading analysis flow

Symbol

↓

YahooProvider

↓

IndicatorBuilder

↓

TradingPipeline

↓

TradingWorkspacePresenter

↓

Trading Workspace

Current open trade lifecycle flow

Trading Workspace

↓

Open Trade action

↓

TradingController latest pipeline result

↓

TradeLifecycleService

↓

OpenTradeStore

↓

Trade Monitor

Current deterministic position / exit flow

Trade

↓

PositionAnalysisService

↓

YahooProvider

↓

AnalysisEngine

↓

AnalysisResult

↓

PositionMonitorService / TradeMonitorService

↓

ExitEvaluationService

↓

PositionMonitorPresenter / TradeMonitorPresenter

↓

Trade Monitor Workspace

The same AnalysisEngine supports both opportunity evaluation and exit intelligence.

Current Known Limitations
Open Trade workflow is still being completed.
Open Trade currently uses early defaults for quantity, stop-loss and take-profit.
Trade Monitor still contains legacy manual input.
Open Trades list is basic text presentation.
No selectable trade detail view yet.
No Close Trade GUI action yet.
No automatic Trade History transfer from GUI yet.
No broker execution.
No DEGIRO API integration.
No automated trading.
No paper broker yet.
No commission/slippage model yet.

These are expected Sprint 5.5 / Sprint 6 limitations, not architectural blockers.

Immediate Next Steps
Finish Open Trade workflow from Trading Workspace.
Ensure a BUY analysis can create a persisted open trade.
Refresh Trade Monitor immediately after trade creation.
Improve Open Trades presentation.
Add trade selection / detail view.
Add Close Trade workflow.
Move closed trades to TradeHistoryStore.
Update docs after every visible milestone.
Git / Workflow Rules
GitHub is the primary source of truth.
After every stable milestone:
run tests
launch desktop
manually validate GUI
commit
push
update documentation
Do not continue large implementation work when docs are outdated after a completed sprint milestone.
Prefer small, safe commits.
End of AI_CONTEXT