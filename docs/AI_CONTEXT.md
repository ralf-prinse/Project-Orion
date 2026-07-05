# ORION AI CONTEXT

---

# Documentation Information

Documentation Version

v1.11

Architecture Version

v2.0

Current Sprint

✅ Sprint 5.4 — Exit Intelligence Foundation Completed

Next Sprint

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

Architectural specifications intentionally exist primarily inside
ORION_MASTER_ARCHITECTURE.md.

This document contains only project state, development workflow and current implementation context.

---

# Current Project State

Project Orion has completed its deterministic trading foundation and has now entered the Trade Lifecycle phase.

The deterministic backend is stable.

Mission Control is the operational center of Orion.

Trading Workspace provides deterministic BUY / HOLD / SELL analysis with explainability.

Position Monitor now performs deterministic exit intelligence for open trades.

The project has moved beyond only finding opportunities.

Orion now supports the first version of the full trade lifecycle:

Market Scan

↓

Opportunity

↓

Trading Decision

↓

Position Sizing

↓

Trade

↓

Position Monitor

↓

Exit Intelligence

↓

Future Trade History

Current development focuses on expanding visible desktop functionality while preserving deterministic architecture.

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

✔ FX warning added for current EUR/USD limitation

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

# Next Sprint

## 🚧 Sprint 5.5 — Trade Lifecycle / Trade Monitor

Primary goal

Transform Position Monitor into a clearer Trade Lifecycle / Trade Monitor experience.

Expected objectives

- Rename Position Monitor conceptually toward Trade Monitor.
- Improve trade lifecycle information hierarchy.
- Show the full trade state more clearly:
  - entry
  - current status
  - technical health
  - exit score
  - exit advice
  - risk state
  - profit/loss
- Prepare the flow for opening trades from Trading Workspace / Mission Control.
- Prepare future trade persistence.
- Prepare future trade history integration.
- Keep SELL / HOLD exit decisions deterministic.
- Keep AI explainability-only.

No broker integration yet.

No real order execution yet.

No automated trading yet.

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

✔ PortfolioStore

✔ Trade model

✔ PositionMonitorService

✔ ExitEvaluationService

✔ PositionAnalysisService

✔ AI Context Builder

✔ AI Explanation Engine

The deterministic backend remains the single source of truth.

TradingPipeline remains the only source of BUY / HOLD / SELL trading decisions.

ExitEvaluationService is now the deterministic source for open-trade exit advice.

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

✔ PositionMonitorWorkspace

✔ PositionMonitorController

✔ ChartCanvas Framework

✔ Auto Refresh

Mission Control remains the primary workspace.

Position Monitor is currently the first implementation of the Trade Lifecycle area.

---

# Current Validation

Latest validation

```powershell
python run_tests.py

Expected result

✔ 6 passed

Desktop validation

python app.py

Validated

✔ Application starts

✔ Navigation works

✔ Mission Control loads

✔ Trading Workspace loads

✔ Portfolio Workspace loads

✔ Position Monitor loads

✔ Scan Market works

✔ Opportunity cards render correctly

✔ Opportunity cards no longer overflow horizontally

✔ Workspaces support scrolling

✔ Trading Capital persistence works

✔ Position Monitor can evaluate a manually entered trade

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

✔ Position sizing information

✔ Share quantity

✔ Required investment

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

Position Monitor currently contains

✔ Manual trade input

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

---

# Development Rules

Every Orion implementation must follow these rules.

## Backend

- Trading logic exists only inside backend services.
- TradingPipeline remains the only source of BUY / HOLD / SELL decisions.
- ExitEvaluationService is the deterministic source of open-trade exit advice.
- LiveScannerService performs orchestration only.
- OpportunityService builds presentation-ready opportunities.
- PositionSizingService calculates deterministic position sizing only.
- PositionMonitorService calculates trade monitoring result data and delegates exit advice.
- PositionAnalysisService retrieves technical analysis for existing trades.
- PortfolioStore owns persistence of trading capital.
- Controllers coordinate services but never perform calculations.

---

## Presentation

- Widgets contain presentation only.
- Panels contain presentation only.
- Workspaces render and forward user actions only.
- Presenters transform deterministic output into readable UI text only.
- WorkspaceRenderer owns Mission Control rendering only.
- ChartCanvas owns painting only.
- No business logic may exist inside Qt widgets.
- No technical analysis may be calculated inside the UI.
- No exit decision may be calculated inside the UI.

---

## Artificial Intelligence

AI may

- explain
- summarize
- compare
- generate natural language

AI may never

- generate BUY signals
- generate SELL signals
- calculate indicators
- calculate confidence
- calculate position size
- override deterministic output
- override TradingPipeline
- override ExitEvaluationService

Artificial Intelligence remains explainability only.

---

# Current Architecture Direction

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

PositionMonitorService

↓

ExitEvaluationService

↓

PositionMonitorPresenter

↓

Position Monitor Workspace

The same AnalysisEngine now supports both opportunity evaluation and exit intelligence.

Mission Control, Trading Workspace and Position Monitor perform no calculations themselves.

---

# Important Architectural Facts

## TradingPipeline

TradingPipeline remains the only source for BUY / HOLD / SELL trading decisions.

No UI component may produce trading decisions.

No AI component may produce trading decisions.

## ExitEvaluationService

ExitEvaluationService is the deterministic source for open-trade exit advice.

It may produce:

- HOLD_POSITION
- TAKE_PROFIT
- STOP_LOSS
- TRAILING_STOP
- EXIT_DUE_TO_WEAKNESS
- EXIT_DUE_TO_TIME_LIMIT

Current implementation actively supports:

- HOLD_POSITION
- TAKE_PROFIT
- STOP_LOSS
- EXIT_DUE_TO_WEAKNESS

Future implementation will expand:

- TRAILING_STOP
- EXIT_DUE_TO_TIME_LIMIT

## Trade Model

The Trade model is now the central domain model for the lifecycle of a trade.

It represents:

- symbol
- quantity
- entry price
- entry datetime
- entry reason
- confidence
- current price
- highest price
- lowest price
- stop-loss
- take-profit
- trailing stop
- status
- exit signal
- exit reason
- exit price
- exit datetime
- realized profit/loss
- unrealized profit/loss
- notes

The Trade model contains no business logic.

## Position Monitor

Position Monitor is the first user-facing implementation of the Trade Lifecycle area.

It currently accepts manual trade input.

It does not yet persist open trades.

It does not yet open trades automatically from Trading Workspace.

It does not yet connect to broker APIs.

It does not yet execute orders.

---

# Current Development Focus

Highest priorities

1. Trade Lifecycle / Trade Monitor
2. Connect Trading decisions to trade creation
3. Persist open trades
4. Trade history integration
5. Improve Exit Intelligence presentation
6. Add trailing stop logic
7. Add time-based exit logic
8. Mission Control trade overview
9. Paper Trading
10. Broker integration later

---

# Upcoming Sprint

## Sprint 5.5 — Trade Lifecycle / Trade Monitor

Objectives

- Rename Position Monitor conceptually toward Trade Monitor.
- Improve screen structure and wording.
- Make the lifecycle visible:
  - opportunity
  - decision
  - open trade
  - monitoring
  - exit advice
  - closed trade later
- Prepare open trade persistence.
- Prepare future trade creation from Trading Workspace.
- Keep TradingPipeline as the only source of BUY / HOLD / SELL.
- Keep ExitEvaluationService as the only source of exit advice.
- Keep AI explainability-only.
- Avoid broker integration for now.

Expected first implementation step

- Update UI terminology and architecture references from Position Monitor toward Trade Monitor / Trade Lifecycle.
- Keep existing working PositionMonitor classes unless a rename is explicitly part of the sprint.
- Avoid breaking the current working GUI.
- Preserve manual trade input until trade persistence exists.

---

# Documentation

The official Orion documentation consists of

- PROJECT_VISION.md
- ORION_MASTER_ARCHITECTURE.md
- TRADING_STRATEGY.md
- PROJECT_STATUS.md
- TODO.md
- CHANGELOG.md
- AI_CONTEXT.md

Architectural information belongs primarily inside ORION_MASTER_ARCHITECTURE.md.

AI_CONTEXT.md exists to give a new chat enough operational context to continue safely.

---

# New Chat Workflow

Every Orion development session starts with the same process.

1.

Use GitHub repository as primary source of truth.

Repository:

https://github.com/ralf-prinse/Project-Orion

2.

Read all synchronized documentation.

3.

Read the current source tree from GitHub.

4.

Analyse the complete architecture before implementation.

5.

Determine

- Architecture Version
- Documentation Version
- Current Sprint
- Completed work
- Active work
- Next logical implementation step

6.

Only after the complete analysis may implementation begin.

No assumptions are allowed before analysis has been completed.

ZIP files are no longer the preferred workflow.

GitHub is the primary source of truth.

---

# Orion Development Philosophy

Project Orion is developed according to one central principle:

**Architecture before implementation.**

Every new feature must:

- extend the existing architecture;
- preserve deterministic behaviour;
- remain independently testable;
- produce a visible improvement inside the desktop application.

Current architectural direction:

**Opportunity detection → Trading decision → Position sizing → Trade lifecycle → Exit intelligence → Trade history → Paper trading → Broker integration**

Mission Control continues to evolve into a professional trading workstation.

Trade Monitor / Trade Lifecycle is the next major functional area.

---

# End of AI_CONTEXT