# ORION MASTER ARCHITECTURE

---

# Architecture Version

**Architecture Freeze v1.2**

Status

🟢 Production Foundation Stable

Current Phase

🚧 Sprint 4.1 — Dashboard 2.0

---

# System Philosophy

Project Orion is a deterministic AI-assisted desktop trading platform.

Every architectural layer owns exactly one responsibility.

Artificial Intelligence never performs investment calculations.

Artificial Intelligence only explains deterministic results.

The deterministic Trading Pipeline is the single source of truth.

No business logic may exist inside the UI.

---

# Engineering Principles

## Deterministic First

Identical market data must always produce identical trading decisions.

No randomness is permitted.

No AI-generated trading decisions are permitted.

---

## Separation of Responsibilities

Business Logic

↓

Orchestration

↓

Presentation

↓

Qt UI

Every layer communicates through explicit presentation models.

---

## Explainability

Every recommendation must always be:

- deterministic
- reproducible
- traceable
- explainable

---

## Production Workflow

Every sprint follows:

Feature

↓

Testing

↓

Documentation

↓

Git Commit

↓

GitHub Push

No sprint is complete before all five stages finish successfully.

---

# Production Trading Architecture

```
User
        ↓
ApplicationController
        ↓
YahooProvider
        ↓
IndicatorBuilder
        ↓
IndicatorPack
        ↓
TradingPipeline
        ↓
Signal Fusion
        ↓
Market Intelligence
        ↓
Adaptive Decision
        ↓
Position Sizing
        ↓
AI Context Builder
        ↓
AI Explanation Engine
        ↓
Presenters
        ↓
Qt Desktop
```

The deterministic Trading Pipeline remains the only source of trading decisions.

---

# AI Market Scanner

```
ApplicationController
        ↓
YahooProvider
        ↓
IndicatorBuilder
        ↓
TradingPipeline
        ↓
AIMarketScanner
        ↓
AIScannerPresenter
        ↓
Scanner Workspace
```

Trading Workspace and AI Scanner always consume the exact same Trading Pipeline.

No duplicate business logic may exist.

---

# Dashboard Architecture

Sprint 4.1 completed the migration to Orion's shared presentation architecture.

Production architecture:

```
ApplicationController
        ↓
DashboardData
        ↓
Dashboard2Presenter
        ↓
GuiMetricCard
        ↓
MetricCard
        ↓
DashboardGrid
        ↓
DashboardWorkspace
```

Dashboard owns presentation only.

Trading calculations remain inside the deterministic backend.

Dashboard now fully reuses Orion's shared presentation framework.

Duplicate presentation components are prohibited.

---

# Dashboard Presentation Architecture

Sprint 4.1 finalized the Dashboard migration to the shared Orion presentation framework.

Completed presentation flow:

```
ApplicationController
        ↓
DashboardData
        ↓
Dashboard2Presenter
        ↓
GuiMetricCard
        ↓
MetricCard
        ↓
DashboardGrid
        ↓
DashboardWorkspace
```

Responsibilities:

ApplicationController

- Coordinates desktop communication.

DashboardData

- Contains deterministic dashboard presentation data.

Dashboard2Presenter

- Converts deterministic backend output into GuiMetricCard presentation models.

GuiMetricCard

- Standard presentation model for reusable dashboard widgets.

MetricCard

- Shared reusable dashboard widget.

DashboardGrid

- Responsible only for dashboard layout.

DashboardWorkspace

- Coordinates dashboard presentation.
- Contains no business logic.

The previous DashboardCard and DashboardCardModel implementation has been fully removed.

Dashboard-specific presentation components are no longer permitted.

---

# Backtesting Architecture

```
Historical Dataset
        ↓
MarketScanner
        ↓
BacktestEngine
        ↓
BacktestSimulator
        ↓
Trade Log
        ↓
Equity Curve
        ↓
BacktestVisualizer
```

Backtesting always reuses deterministic production logic.

---

# Configuration Architecture

```
TradingConfig
        ↓
YahooProvider

IndicatorBuilder

TradingPipeline

ApplicationController

AIMarketScanner

Backtesting
```

Configuration remains centralized.

Hardcoded values are prohibited.

---

# Logging Architecture

```
ApplicationController
        ↓
YahooProvider
        ↓
IndicatorBuilder
        ↓
TradingPipeline
        ↓
AIMarketScanner
        ↓
BacktestEngine
```

All production services use LoggingService.

Destination

```
logs/orion.log
```

Logging provides a complete deterministic audit trail.

---

# Regression Testing

Regression validation remains centralized.

Official command

```powershell
python run_tests.py
```

Current suite

- Trading Pipeline
- Decision Smoke
- Intelligence Layer
- AI Market Scanner
- AI Scanner Presenter
- Backtest Visualizer

Current status

```
Passed: 6
Failed: 0
```

Regression testing is mandatory before every Git commit.

---

# Current Production Components

Completed

## Backend

✅ TradingConfig

✅ LoggingService

✅ YahooProvider

✅ IndicatorBuilder

✅ TradingPipeline

✅ Signal Fusion Engine

✅ Market Intelligence Engine

✅ Adaptive Decision Engine

✅ Position Sizing Engine

✅ AI Context Builder

✅ AI Explanation Engine

✅ AIMarketScanner

✅ BacktestEngine

✅ BacktestSimulator

✅ BacktestVisualizer

---

## Desktop

✅ ApplicationController

✅ Trading Workspace

✅ Dashboard 2.0 Foundation

✅ DashboardData

✅ Dashboard2Presenter

✅ DashboardWorkspace

✅ DashboardGrid

✅ GuiMetricCard Integration

✅ MetricCard Integration

✅ Scanner Workspace

✅ Trading Workspace Presenter

✅ AI Scanner Presenter

---

# Project Health

Architecture

🟢 Stable

Backend

🟢 Production Ready

Desktop

🟢 Active Development

Dashboard

🟢 Shared Presentation Architecture Complete

Logging

🟢 Complete

Regression Tests

🟢 Passing

Technical Debt

🟢 Low

Documentation

🟢 Current

---

# Sprint 4.1 Completed Work

Completed:

- Dashboard migration to GuiMetricCard
- Dashboard migration to MetricCard
- DashboardGrid refactor
- DashboardWorkspace refactor
- Dashboard2Presenter refactor
- Removal of temporary Dashboard presentation components
- Dashboard presentation standardization
- Regression validation

Current regression result:

```
Passed: 6
Failed: 0
```

Sprint 4.1 architecture objectives have been completed successfully.

---

# Current Development Focus

The deterministic backend is considered feature complete.

Current development focuses on desktop presentation and user experience.

Highest priority:

- Dashboard Widget Library
- Professional KPI Cards
- Dashboard Hero Components
- Market Health Banner
- Professional Status Bar
- Dashboard Theme Improvements
- Equity Curve Visualization
- Portfolio Allocation Visualization
- Professional Gauge Widgets

Backend expansion is not planned during this phase.

The Trading Pipeline remains the only deterministic source of trading decisions.

---

# Sprint 4.2 Roadmap

Following completion of the Dashboard architecture migration, development moves toward expanding desktop functionality while preserving the deterministic backend.

Primary objectives:

- Dashboard Widget Library
- Hero KPI Cards
- Market Health Banner
- Professional Status Bar
- Equity Curve Chart
- Portfolio Allocation Chart
- Professional Gauge Widgets
- Workspace polish
- Desktop UX improvements

All new desktop components must reuse the existing Orion presentation framework.

No duplicate presentation widgets may be introduced.

---

# Architecture Rules

The following architectural rules are mandatory.

## Business Logic

Business logic belongs exclusively inside backend services.

Qt widgets must never perform calculations.

Presenters may only transform deterministic output into presentation models.

---

## Artificial Intelligence

Artificial Intelligence never:

- calculates indicators
- generates buy/sell signals
- performs portfolio calculations
- determines position sizing

Artificial Intelligence only explains deterministic results produced by the Trading Pipeline.

---

## Dashboard

Dashboard is a presentation layer only.

Dashboard components must always reuse:

- DashboardData
- Dashboard2Presenter
- GuiMetricCard
- MetricCard
- DashboardGrid
- DashboardWorkspace

Dashboard-specific presentation components are prohibited.

The shared MetricCard infrastructure is the only approved dashboard card implementation.

---

## Regression Testing

Every architectural change must end with:

```powershell
python run_tests.py
```

Expected production result:

```
Passed: 6
Failed: 0
```

No code may be committed while regression tests fail.

---

## Production Workflow

Every sprint follows the same workflow.

Feature

↓

Testing

↓

Documentation

↓

Git Commit

↓

GitHub Push

No sprint is considered complete until all five stages have finished successfully.

---

# Long-Term Vision

Project Orion will evolve into a professional deterministic AI-assisted desktop trading platform featuring:

- Professional Desktop Dashboard
- Portfolio Intelligence
- Live Market Analysis
- Explainable AI
- Historical Backtesting
- Watchlists
- Paper Trading
- Broker Integration

while preserving deterministic calculations as the only source of trading decisions.

---

# Architecture Status

Architecture Version

**Architecture Freeze v1.2**

Current Version

**v1.2.0-alpha**

Backend

🟢 Production Stable

Desktop

🟢 Active Development

Dashboard

🟢 Shared Presentation Architecture Complete

AI

🟢 Explainability Only

Regression Tests

```
Passed: 6
Failed: 0
```

Documentation

🟢 Current

Git

Ready for commit after documentation update.