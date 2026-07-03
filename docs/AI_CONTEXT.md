# ORION AI CONTEXT

---

# Current Phase

## Sprint 4.3 — Unified Dashboard Workspace

Project Orion has completed its deterministic backend foundation.

The backend is considered production-stable.

Current development is focused entirely on the professional desktop experience.

No new trading logic is currently being added.

Development is focused on presentation architecture, reusable workspaces, reusable widgets, visualization and desktop UX while preserving the deterministic backend.

Sprint 4.3 builds upon the completed Dashboard Widget Library by introducing a unified dashboard presentation pipeline.

---

# Development Philosophy

Project Orion follows several non-negotiable engineering principles.

## Deterministic First

Every trading decision must be reproducible.

Identical market data must always generate identical output.

Artificial Intelligence never performs calculations.

Artificial Intelligence only explains deterministic results.

The Trading Pipeline remains the single source of truth.

---

## Layer Separation

Business logic exists only inside Services.

Presentation logic exists only inside Presenters.

Qt Widgets contain no business logic.

ApplicationController coordinates communication between UI and backend.

Widgets are responsible only for rendering presentation models.

Workspaces are responsible only for presentation composition.

No widget or workspace may contain trading logic, AI logic or portfolio calculations.

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

No sprint is considered complete until all five stages have finished.

---

# Core Trading Flow

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
AI Context
        ↓
AI Explanation
        ↓
Presenters
        ↓
Qt Desktop
```

Every architectural layer owns exactly one responsibility.

The Trading Pipeline remains the only deterministic source of trading decisions.

---

# AI Market Scanner

The AI Market Scanner uses the exact same Trading Pipeline as the Trading Workspace.

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

There is only one deterministic source of truth.

No duplicate trading logic may exist.

---

# Dashboard Evolution

Sprint 4.1

Completed Dashboard migration.

↓

Sprint 4.2

Completed reusable Dashboard Widget Library.

↓

Sprint 4.3

Introduces a unified dashboard presentation architecture based on GuiWorkspace.

The dashboard is evolving from a collection of cards into a complete presentation workspace capable of rendering cards, charts and future presentation models from one presentation object.

---

# Unified Dashboard Presentation Pipeline

Current presentation flow

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
Dashboard Widgets
```

The DashboardWorkspacePresenter owns presentation orchestration only.

GuiWorkspace becomes the canonical dashboard presentation model.

DashboardWorkspace renders presentation only.

Business logic remains prohibited throughout the presentation layer.

---

# GuiWorkspace

GuiWorkspace is the new top-level dashboard presentation model.

Current responsibilities

- dashboard title
- dashboard subtitle
- cards
- charts
- sections
- status
- presentation metadata

GuiWorkspace contains presentation data only.

No calculations.

No business logic.

No AI logic.

---

# GuiWorkspaceSection

Sprint 4.3 introduces GuiWorkspaceSection as a reusable presentation grouping model.

Responsibilities

- Group related dashboard presentation items
- Support future dashboard layouts
- Contain presentation data only
- No calculations
- No business logic

GuiWorkspaceSection prepares Orion for multi-section dashboard layouts without increasing DashboardWorkspace complexity.

---

# Dashboard Widget Library

The Widget Library introduced during Sprint 4.2 remains unchanged and is now consumed through GuiWorkspace.

Current reusable widgets

✅ MetricCard

✅ HeroMetricCard

✅ MarketHealthBanner

✅ EquityCurveWidget (foundation)

Future widgets

- Portfolio Allocation Widget
- Confidence Gauge
- Pressure Gauge
- Risk Gauge
- Additional Chart Widgets

Every widget continues to integrate exclusively through DashboardWidgetFactory.

DashboardGrid remains responsible only for layout.

---

# UI Architecture

ApplicationController coordinates communication.

DashboardData aggregates deterministic backend output.

Dashboard2Presenter transforms deterministic data into dashboard presentation cards.

DashboardWorkspacePresenter creates a complete GuiWorkspace.

GuiWorkspace becomes the canonical presentation object.

DashboardWorkspace renders GuiWorkspace.

DashboardGrid performs layout only.

DashboardWidgetFactory creates widgets.

Widgets render presentation models only.

Business logic remains prohibited throughout the UI.

Artificial Intelligence performs no calculations.

Dashboard composition is now centralized inside GuiWorkspace.

---

# Current Infrastructure

Completed

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

✅ ApplicationController

✅ DashboardData

✅ Dashboard2Presenter

✅ DashboardWorkspacePresenter

✅ GuiWorkspace

✅ GuiWorkspaceSection

✅ DashboardCardCatalog

✅ DashboardWidgetFactory

✅ DashboardWorkspace

✅ DashboardGrid

✅ Shared Widget Library

✅ Trading Workspace

✅ Scanner Workspace

---

# Logging

Centralized logging remains active.

Coverage

✅ ApplicationController

✅ YahooProvider

✅ IndicatorBuilder

✅ TradingPipeline

✅ AIMarketScanner

✅ BacktestEngine

Destination

```
logs/orion.log
```

The logging system provides a complete deterministic audit trail from user interaction to deterministic trading result.

---

# Testing

Regression testing remains centralized.

Primary validation

```powershell
python run_tests.py
```

Current result

```
Passed: 6
Failed: 0
```

Sprint 4.3 additionally introduces architecture validation for the new workspace presentation layer.

```powershell
python -m pytest test_dashboard_workspace_presenter.py
```

Current result

```
1 passed
```

Both validation suites must remain green before every Git commit.

---

# Current Priority

Sprint 4.3 continues the Dashboard evolution without changing deterministic backend behavior.

Completed during the current migration phase

✅ GuiWorkspace

✅ GuiWorkspaceSection

✅ DashboardWorkspacePresenter

✅ DashboardWorkspace migration

✅ Backward-compatible card rendering

✅ Existing Widget Library reused

✅ Existing DashboardGrid reused

✅ Existing DashboardWidgetFactory reused

No duplicate presentation pipeline was introduced.

No backend logic was modified.

No business logic entered the UI.

---

# Next Sprint Focus

Sprint 4.3 is focused on evolving the dashboard into a unified presentation workspace.

Completed

✅ GuiWorkspace introduced

✅ GuiWorkspaceSection introduced

✅ DashboardWorkspacePresenter introduced

✅ DashboardWorkspace migrated to GuiWorkspace

✅ Unified presentation pipeline established

Remaining Sprint 4.3 objectives

⬜ Introduce chart presentation models

⬜ Render charts through GuiWorkspace

⬜ Integrate EquityCurveWidget

⬜ Integrate Portfolio Allocation visualization

⬜ Introduce reusable Gauge widgets

⬜ Continue desktop UX improvements

The Widget Library introduced during Sprint 4.2 remains the presentation foundation.

All future dashboard components must integrate through GuiWorkspace.

No duplicate widget implementations may be introduced.

All presentation metadata remains centralized through DashboardCardCatalog.

All widget creation remains centralized through DashboardWidgetFactory.

---

# Current Development Rules

The following architectural rules remain mandatory.

## Business Logic

Business logic belongs exclusively inside backend services.

Presenters transform deterministic backend output into presentation models.

GuiWorkspace owns dashboard composition.

DashboardWorkspace renders presentation only.

DashboardGrid owns layout.

DashboardWidgetFactory owns widget creation.

Widgets own rendering.

Business logic inside the presentation layer is prohibited.

---

## Artificial Intelligence

Artificial Intelligence never

- calculates indicators
- generates buy/sell signals
- performs portfolio calculations
- determines position sizing

Artificial Intelligence only explains deterministic results produced by the Trading Pipeline.

---

## Dashboard

Dashboard presentation flows exclusively through

```
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

Dashboard-specific business logic is prohibited.

Duplicate presentation pipelines are prohibited.

Every future dashboard component must integrate through GuiWorkspace.

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

# Current Project Health

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

Regression Testing

🟢 Passing

Technical Debt

🟢 Low

Documentation

🟢 Current

---

# Current Version

Version

**v1.2.0-alpha**

Current Sprint

**Sprint 4.3 — Unified Dashboard Workspace**

Current Validation

```
run_tests.py

Passed: 6
Failed: 0

Dashboard Workspace Presenter

Passed: 1
Failed: 0
```

Git Status

Ready for continued Sprint 4.3 development.

---