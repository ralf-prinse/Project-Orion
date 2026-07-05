# ORION AI CONTEXT

---

# Documentation Information

Documentation Version

v1.10

Architecture Version

v1.9

Current Sprint

🚧 Sprint 5.1 — Portfolio & Position Sizing Foundation

Last Updated

2026-07-05

---

# Purpose

This document provides the minimum context required for every new Orion development session.

It complements:

- ORION_MASTER_ARCHITECTURE.md
- PROJECT_STATUS.md
- TRADING_STRATEGY.md

Architectural specifications intentionally exist only inside
ORION_MASTER_ARCHITECTURE.md.

This document contains only project state, development workflow and current implementation context.

---

# Current Project State

Project Orion has completed its architectural foundation.

The deterministic backend is considered stable.

Mission Control is now the operational center of Orion.

Current development no longer focuses on creating architecture.

Current development focuses on expanding visible desktop functionality while preserving the deterministic architecture.

Every completed sprint must result in a visible improvement inside the desktop application.

---

# Current Sprint

## 🚧 Sprint 5.1 — Portfolio & Position Sizing Foundation

Completed during this sprint

✔ Portfolio Workspace redesigned

✔ Portfolio reduced to Trading Capital configuration

✔ PortfolioStore persistence connected

✔ Trading capital survives application restart

✔ Market Data panel displays market data age

✔ Opportunity cards display current market price

✔ OpportunityService introduced

✔ PositionSizingService introduced

✔ Mission Control prepared for position sizing

Current implementation status

Position sizing backend is available.

Mission Control currently displays:

- symbol
- signal
- score
- trend
- reason
- latest price

The next sprint expands this with:

- shares to buy
- required investment
- remaining capital

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

✔ AI Context Builder

✔ AI Explanation Engine

The deterministic backend remains the single source of truth.

---

## Desktop

✔ Workspace architecture

✔ Presenter architecture

✔ WorkspaceRenderer

✔ GuiWorkspace

✔ GuiWorkspacePanel

✔ MissionControlWorkspace

✔ MissionControlController

✔ TradingWorkspace

✔ TradingController

✔ PortfolioWorkspace

✔ ChartCanvas Framework

✔ Auto Refresh

Mission Control remains the primary workspace.

---

# Current Validation

Latest validation

```powershell
python run_tests.py
```

Expected result

✔ 6 passed

Desktop validation

```powershell
python app.py
```

Validated

✔ Application starts

✔ Navigation works

✔ Mission Control loads

✔ Trading Workspace loads

✔ Portfolio Workspace loads

✔ Scan Market works

✔ Auto Refresh works

✔ Trading Capital persistence works

✔ Manual GUI validation completed

---

# Current GUI State

Mission Control currently contains

✔ Scanner Status

✔ Scan Duration

✔ Market Data

✔ Universe Coverage

✔ Market Status

✔ Top Opportunities

✔ Opportunity Price

✔ Scan Market button

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

✔ AI Explanation

The desktop now resembles a professional trading workstation rather than a dashboard.

---

# Development Rules

Every Orion implementation must follow these rules.

## Backend

- Trading logic exists only inside backend services.
- TradingPipeline remains the only decision engine.
- LiveScannerService performs orchestration only.
- OpportunityService builds presentation-ready opportunities.
- PositionSizingService calculates deterministic position sizing only.
- PortfolioStore owns persistence of trading capital.
- Controllers coordinate services but never perform calculations.

---

## Presentation

- Widgets contain presentation only.
- Panels contain presentation only.
- Presenters transform deterministic output only.
- WorkspaceRenderer owns rendering only.
- ChartCanvas owns painting only.
- No business logic may exist inside Qt widgets.

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

Artificial Intelligence remains explainability only.

---

# Current Architecture Direction

Mission Control continues to evolve into the operational heart of Orion.

Current architecture introduces a dedicated Opportunity model.

Current deterministic flow

Market Data

↓

LiveScannerService

↓

TradingPipeline

↓

OpportunityService

↓

MissionControlPresenter

↓

Mission Control

Position sizing is prepared for integration through PositionSizingService.

Mission Control itself performs no calculations.

---

# Development Workflow

Every Orion sprint follows exactly the same workflow.

## 1.

Implement one complete feature.

↓

## 2.

Run regression tests.

```powershell
python run_tests.py
```

Expected result

✔ 6 passed

↓

## 3.

Launch Orion.

```powershell
python app.py
```

↓

## 4.

Perform manual GUI validation.

Review

- layout
- usability
- information hierarchy
- visual quality

↓

## 5.

Synchronize documentation.

↓

## 6.

Commit changes.

↓

## 7.

Push to GitHub.

A sprint is only considered complete after the documentation has been synchronized and the repository has been updated.

---

# Current Development Focus

Highest priorities

1. Position sizing presentation
2. Mission Control GUI improvements
3. Opportunity presentation
4. Market Health
5. Trading Workspace improvements
6. Position Monitor
7. Paper Trading

---

# Upcoming Sprint

## Sprint 5.2 — Position Sizing Presentation

Objectives

- Show recommended share quantity.
- Show required investment.
- Show remaining available capital.
- Show insufficient budget warnings.
- Keep TradingPipeline as the only decision engine.
- Continue expanding Mission Control.

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

Architectural information belongs exclusively inside ORION_MASTER_ARCHITECTURE.md.

---

# New Chat Workflow

Every Orion development session starts with the same process.

1.

Upload the complete Project Orion ZIP.

2.

Upload all synchronized documentation.

3.

Read every documentation file completely.

4.

Analyse the complete source tree.

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

---

# Orion Development Philosophy

Project Orion is developed according to one central principle:

**Architecture before implementation.**

Every new feature must:

- extend the existing architecture;
- preserve deterministic behaviour;
- remain independently testable;
- produce a visible improvement inside the desktop application.

Mission Control continues to evolve into a professional trading workstation.

---

# End of AI_CONTEXT