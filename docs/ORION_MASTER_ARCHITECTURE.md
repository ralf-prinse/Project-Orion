# ORION MASTER ARCHITECTURE

---

# Architecture Version

**Architecture Freeze v1.4**

Status

🟢 Production Foundation Stable

Current Phase

🚧 Sprint 4.3 — Unified Dashboard Workspace

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

Presentation metadata remains centralized.

Widget creation remains centralized.

Workspace composition remains centralized.

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

# Dashboard Evolution

Sprint 4.1

Completed Dashboard migration.

↓

Sprint 4.2

Introduced reusable Dashboard Widget Library.

↓

Sprint 4.3

Introduces the Unified Dashboard Workspace architecture.

The dashboard is evolving from a collection of cards into a complete presentation workspace capable of rendering cards, charts and future presentation components from one presentation model.

---

# Unified Dashboard Architecture

Current production presentation flow:

```
ApplicationController
        ↓
DashboardData
        ↓
Dashboard2Presenter
        ↓
DashboardWorkspacePresenter
        ↓
GuiWorkspace
        ↓
DashboardWorkspace
        ↓
DashboardGrid
        ↓
DashboardWidgetFactory
        ↓
Widgets
```

Responsibilities

ApplicationController

- Coordinates desktop communication.

DashboardData

- Aggregates deterministic backend results.

Dashboard2Presenter

- Produces dashboard presentation cards.

DashboardWorkspacePresenter

- Creates one GuiWorkspace.
- Owns presentation orchestration.
- Contains no business logic.

GuiWorkspace

- Canonical dashboard presentation model.
- Contains cards.
- Contains charts.
- Contains sections.
- Contains presentation metadata only.

DashboardWorkspace

- Renders GuiWorkspace.
- Contains no trading logic.
- Contains no calculations.

DashboardGrid

- Responsible only for layout.

DashboardWidgetFactory

- Responsible only for widget creation.

Widgets

- Render presentation models only.

---

# GuiWorkspace

GuiWorkspace becomes the canonical presentation object for every dashboard.

Current structure:

```
GuiWorkspace

├── cards

├── charts

├── sections

├── metadata

└── status
```

Future dashboard components will integrate through GuiWorkspace rather than extending DashboardWorkspace directly.

Business logic remains prohibited.

Presentation orchestration remains centralized.

---

# GuiWorkspaceSection

GuiWorkspaceSection provides reusable grouping of presentation objects.

Responsibilities:

- Group related dashboard items
- Presentation only
- No calculations
- No business logic

This enables future dashboard layouts containing multiple logical dashboard sections without changing DashboardWorkspace itself.

---

# Widget Library

The Widget Library introduced during Sprint 4.2 remains the foundation of the desktop presentation layer.

Completed reusable widgets

✅ MetricCard

✅ HeroMetricCard

✅ MarketHealthBanner

✅ EquityCurveWidget (foundation)

Future widgets

- Portfolio Allocation Widget
- Confidence Gauge
- Pressure Gauge
- Risk Gauge
- Future Charts

Every widget integrates exclusively through DashboardWidgetFactory.

DashboardGrid should never require architectural changes when introducing new widgets.

---

# Dashboard Presentation Rules

Dashboard remains a presentation layer only.

Dashboard components must never:

- calculate indicators
- calculate portfolio values
- determine signals
- calculate exposure
- calculate risk
- determine position sizing

All deterministic calculations originate exclusively from the Trading Pipeline.

Dashboard presenters transform deterministic output into presentation models.

Qt widgets render presentation models only.

---

# Dashboard Presentation Models

Current presentation hierarchy

```
GuiWorkspace
        │
        ├──────── GuiWorkspaceSection
        │
        ├──────── GuiMetricCard
        │
        └──────── Future Chart Models
```

GuiWorkspace owns the dashboard.

Cards become one possible presentation element rather than the dashboard itself.

This architecture enables future expansion without modifying DashboardWorkspace.

---

# Widget Creation

Widget creation remains centralized.

```
GuiMetricCard
        ↓
DashboardWidgetFactory
        ↓
MetricCard

HeroMetricCard

MarketHealthBanner

Future Widgets
```

DashboardGrid owns layout only.

DashboardWidgetFactory owns widget creation only.

Widgets own rendering only.

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

Backtesting continues to reuse production trading logic.

No duplicate calculation pipeline exists.

---

# Configuration Architecture

```
TradingConfig
        ↓
YahooProvider
        ↓
IndicatorBuilder
        ↓
TradingPipeline
        ↓
ApplicationController
        ↓
Desktop
```

Configuration remains centralized.

Hardcoded production values remain prohibited.

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

Logging provides a deterministic audit trail.

---

# Regression Testing

Regression validation remains centralized.

Official production command

```powershell
python run_tests.py
```

Expected production result

```
Passed: 6
Failed: 0
```

Sprint 4.3 additionally introduces dedicated architecture validation for the Unified Dashboard Workspace.

Current result

```
run_tests.py
Passed: 6
Failed: 0

Dashboard Workspace Presenter
Passed: 1
Failed: 0
```

Regression validation remains mandatory before every commit.

---

# Current Production Components

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

✅ Scanner Workspace

✅ DashboardData

✅ Dashboard2Presenter

✅ DashboardWorkspacePresenter

✅ DashboardWorkspace

✅ DashboardGrid

✅ DashboardCardCatalog

✅ DashboardWidgetFactory

✅ GuiWorkspace

✅ GuiWorkspaceSection

✅ GuiMetricCard

✅ MetricCard

✅ HeroMetricCard

✅ MarketHealthBanner

✅ EquityCurveWidget (foundation)

---

# Project Health

Architecture

🟢 Stable

Backend

🟢 Production Ready

Desktop

🟢 Active Development

Dashboard

🟢 Unified Workspace Migration Started

Widget Library

🟢 Stable

Workspace Architecture

🟢 Active

Logging

🟢 Complete

Regression Tests

🟢 Passing

Technical Debt

🟢 Low

Documentation

🟢 Current

---

# Sprint 4.3 Foundation Completed

Completed during the initial Sprint 4.3 migration:

- GuiWorkspace introduced
- GuiWorkspaceSection introduced
- DashboardWorkspacePresenter introduced
- DashboardWorkspace migrated to GuiWorkspace
- Backward-compatible card rendering retained
- Existing Widget Library reused
- Existing DashboardGrid reused
- Existing DashboardWidgetFactory reused
- Existing GuiMetricCard models reused
- Unified presentation pipeline established
- Dedicated Dashboard Workspace Presenter regression test added

Current validation:

```
run_tests.py

Passed: 6
Failed: 0

Dashboard Workspace Presenter

Passed: 1
Failed: 0
```

The migration introduced no backend changes.

No business logic moved into the UI.

No duplicate presentation pipeline was introduced.

The migration preserves complete backward compatibility while preparing the desktop for future dashboard visualization.

---

# Current Development Focus

The deterministic backend is considered feature complete.

Current development focuses exclusively on desktop presentation architecture.

Highest priorities

- Expand GuiWorkspace
- Introduce chart presentation models
- Integrate EquityCurveWidget
- Integrate Portfolio Allocation visualization
- Introduce reusable Gauge widgets
- Continue desktop UX improvements

Backend expansion is intentionally paused during this architectural phase.

The Trading Pipeline remains the only deterministic source of trading decisions.

---

# Sprint 4.3 Roadmap

Current sprint objectives

✅ Introduce GuiWorkspace

✅ Introduce GuiWorkspaceSection

✅ Introduce DashboardWorkspacePresenter

✅ Migrate DashboardWorkspace

⬜ Introduce chart presentation models

⬜ Render charts through GuiWorkspace

⬜ Integrate EquityCurveWidget

⬜ Integrate Portfolio Allocation visualization

⬜ Introduce reusable Gauge widgets

⬜ Continue desktop UX improvements

Sprint 4.3 is intentionally divided into small production-safe migration steps.

Every completed step must preserve complete backward compatibility.

---

# Architecture Rules

The following architectural rules are mandatory.

## Business Logic

Business logic belongs exclusively inside backend services.

Qt widgets never perform calculations.

Presenters transform deterministic backend output into presentation models.

GuiWorkspace owns dashboard composition.

DashboardGrid owns layout.

DashboardWidgetFactory owns widget creation.

Widgets own rendering.

Business logic inside widgets is prohibited.

---

## Artificial Intelligence

Artificial Intelligence never:

- calculates indicators
- generates buy/sell signals
- performs portfolio calculations
- determines position sizing

Artificial Intelligence only explains deterministic results generated by the Trading Pipeline.

---

## Dashboard

Dashboard is a presentation layer only.

Dashboard presentation flows exclusively through:

DashboardData

↓

Dashboard2Presenter

↓

DashboardWorkspacePresenter

↓

GuiWorkspace

↓

DashboardWorkspace

↓

DashboardGrid

↓

DashboardWidgetFactory

↓

Widgets

Duplicate presentation pipelines are prohibited.

Dashboard-specific business logic is prohibited.

---

## Regression Testing

Every architectural change concludes with

```powershell
python run_tests.py
```

Expected production result

```
Passed: 6
Failed: 0
```

Additional Sprint 4.3 validation

```powershell
python -m pytest test_dashboard_workspace_presenter.py
```

Expected result

```
1 passed
```

Regression validation is mandatory before every Git commit.

---

## Production Workflow

Every sprint follows exactly the same workflow.

Feature

↓

Testing

↓

Documentation

↓

Git Commit

↓

GitHub Push

No sprint is considered complete until every stage succeeds.

---

# Long-Term Vision

Project Orion will evolve into a professional deterministic AI-assisted desktop trading platform featuring

- Professional Desktop Dashboard
- Unified Dashboard Workspace
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

**Architecture Freeze v1.4**

Current Version

**v1.2.0-alpha**

Current Sprint

**Sprint 4.3 — Unified Dashboard Workspace**

Sprint Status

🚧 In Progress

Backend

🟢 Production Stable

Desktop

🟢 Active Development

Dashboard

🟢 Unified Workspace Migration Started

Widget Library

🟢 Stable

Workspace Architecture

🟢 Active

AI

🟢 Explainability Only

Regression Tests

```
run_tests.py
Passed: 6
Failed: 0

Dashboard Workspace Presenter
Passed: 1
Failed: 0
```

Documentation

🟢 Current

Git

Ready for commit after remaining Sprint 4.3 documentation updates.

---