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

This deterministic Trading Pipeline remains the only source of trading decisions.

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

# Dashboard 2.0 Architecture

Dashboard has become an independent presentation layer.

Current architecture:

```
ApplicationController
        ↓
DashboardData
        ↓
Dashboard2Presenter
        ↓
DashboardWorkspace
        ↓
DashboardGrid
```

Dashboard owns presentation only.

Trading calculations remain inside the backend.

---

# IMPORTANT ARCHITECTURAL DECISION

During Sprint 4.1 an existing reusable presentation framework was discovered.

Already available:

- GuiMetricCard
- MetricCard
- GuiWorkspace
- GuiChart

Temporary Dashboard-specific components were introduced during the first Dashboard implementation:

- DashboardCard
- DashboardCardModel

These temporary components have now been removed from the project.

Future Dashboard development MUST use the existing presentation framework.

Target architecture:

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

This becomes the official Dashboard architecture.

Duplicate widget hierarchies are not permitted.

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

🟢 Active Development

Logging

🟢 Complete

Regression Tests

🟢 Passing

Technical Debt

🟢 Low

Documentation

🟢 Current

---

# Sprint 4.1 Remaining Work

Highest priority:

- Migrate Dashboard to MetricCard
- Standardize on GuiMetricCard
- Remove remaining temporary presentation code
- Introduce reusable dashboard widget library
- Add professional dashboard widgets
- Equity chart
- Allocation chart
- Gauge widgets
- Hero KPI cards

Backend expansion is NOT planned.

Future work is focused on desktop presentation while preserving the deterministic backend.

---

# Long-Term Vision

Project Orion will evolve into a professional deterministic AI-assisted trading platform featuring:

- Professional Desktop Dashboard
- Portfolio Intelligence
- Live Market Analysis
- Explainable AI
- Historical Backtesting
- Watchlists
- Paper Trading
- Broker Integration

while maintaining deterministic calculations as the only source of trading decisions.