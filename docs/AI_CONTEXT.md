# ORION AI CONTEXT

---

# Current Phase

## Sprint 4.4 — Production Chart Pipeline

Project Orion has completed its deterministic backend foundation.

The backend is considered production-stable.

Current development is focused entirely on the professional desktop experience.

No new trading logic is currently being added.

Development is focused on presentation architecture, reusable workspaces, reusable renderers, reusable widgets, visualization and desktop UX while preserving the deterministic backend.

Sprint 4.4 builds upon the completed Unified Dashboard Workspace by introducing Orion's first production chart pipeline.

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

Rendering logic exists only inside Renderers.

Qt Widgets contain no business logic.

ApplicationController coordinates communication between UI and backend.

Widgets render presentation models only.

Renderers orchestrate visualization only.

Workspaces compose presentation only.

No widget, renderer or workspace may contain trading logic, AI logic or portfolio calculations.

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

# Dashboard Evolution

Sprint 4.1

Completed Dashboard migration.

↓

Sprint 4.2

Completed reusable Dashboard Widget Library.

↓

Sprint 4.3

Completed Unified Dashboard Workspace.

↓

Sprint 4.4

Introduces the Production Chart Pipeline.

The dashboard is evolving into a complete presentation workspace capable of rendering cards, charts and future presentation models through one deterministic presentation pipeline.

---

# Unified Dashboard Presentation Pipeline

Current production presentation flow

```
ApplicationController
        ↓
DashboardData
        ↓
Dashboard2Presenter
        ↓
DashboardWorkspacePresenter
        │
        ├──────── GuiMetricCard
        │
        └──────── EquityCurveChartPresenter
                    ↓
                 GuiChart
        ↓
GuiWorkspace
        ↓
WorkspaceRenderer
        ├──────── DashboardGrid
        └──────── ChartRenderer
                    ↓
            ChartWidgetFactory
                    ↓
             LineChartWidget
```

Presentation orchestration is now fully centralized.

Business logic remains prohibited throughout the presentation layer.

---

# GuiWorkspace

GuiWorkspace is the canonical dashboard presentation model.

Current responsibilities

- dashboard title
- dashboard subtitle
- cards
- charts
- chart sections
- workspace sections
- status
- presentation metadata

GuiWorkspace contains presentation data only.

No calculations.

No business logic.

No AI logic.

---

# Chart Presentation Models

Sprint 4.4 introduces reusable chart presentation models.

Completed

✅ GuiChart

✅ GuiChartType

✅ GuiSeries

✅ GuiAxis

✅ GuiLegend

✅ GuiChartSection

These models describe chart presentation only.

They never calculate values.

They never access backend services.

---

# Rendering Architecture

Rendering is now separated from presentation composition.

WorkspaceRenderer

- orchestrates complete workspace rendering

DashboardGrid

- renders metric cards only

ChartRenderer

- renders chart presentation models

ChartWidgetFactory

- creates chart widgets

LineChartWidget

- renders GuiChart

Every rendering layer owns exactly one responsibility.

---

# Dashboard Widget Library

The Widget Library introduced during Sprint 4.2 remains unchanged.

Dashboard widgets

✅ MetricCard

✅ HeroMetricCard

✅ MarketHealthBanner

Chart widgets

✅ LineChartWidget

Future chart widgets

- AreaChartWidget
- PieChartWidget
- DonutChartWidget
- HeatMapWidget
- PortfolioAllocationWidget

DashboardWidgetFactory and ChartWidgetFactory remain completely separated.

---

# UI Architecture

ApplicationController coordinates communication.

DashboardData aggregates deterministic backend output.

Dashboard2Presenter transforms deterministic results into dashboard cards.

DashboardWorkspacePresenter creates a complete GuiWorkspace.

EquityCurveChartPresenter creates reusable GuiChart models.

GuiWorkspace owns dashboard composition.

WorkspaceRenderer owns rendering orchestration.

DashboardGrid owns card layout.

ChartRenderer owns chart rendering.

Widgets render presentation models only.

Business logic remains prohibited throughout the UI.

Artificial Intelligence performs no calculations.

Presentation composition and rendering are now fully separated.

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

✅ EquityCurveChartPresenter

✅ GuiWorkspace

✅ GuiWorkspaceSection

✅ GuiChart

✅ GuiChartSection

✅ WorkspaceRenderer

✅ DashboardGrid

✅ ChartRenderer

✅ ChartContainer

✅ DashboardWidgetFactory

✅ ChartWidgetFactory

✅ LineChartWidget

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

Additional presentation validation

```powershell
python -m pytest test_dashboard_workspace_presenter.py
python -m pytest test_dashboard_workspace_charts.py
python -m pytest test_equity_curve_chart_presenter.py
python -m pytest test_workspace_renderer.py
python -m pytest test_chart_renderer.py
python -m pytest test_chart_widget_factory.py
python -m pytest test_chart_models.py
python -m pytest test_gui_chart.py
python -m pytest test_chart_container.py
python -m pytest test_line_chart_widget.py
```

All validation suites currently pass.

Regression validation remains mandatory before every Git commit.

---

# Current Development Focus

The deterministic backend remains feature complete.

Current development focuses entirely on desktop presentation architecture.

Completed

✅ Unified Dashboard Workspace

✅ Chart Presentation Models

✅ WorkspaceRenderer

✅ ChartRenderer

✅ ChartContainer

✅ ChartWidgetFactory

✅ LineChartWidget

✅ Production Chart Pipeline

Current priorities

⬜ Replace placeholder LineChartWidget rendering with a production chart library

⬜ Portfolio Allocation visualization

⬜ Gauge widgets

⬜ Dashboard Layout 2.0

⬜ Live Dashboard updates

No backend expansion is currently planned.

---

# Current Development Rules

Business logic belongs exclusively inside backend services.

Presenters transform deterministic backend output into presentation models.

GuiWorkspace owns presentation composition.

WorkspaceRenderer owns rendering orchestration.

DashboardGrid owns metric card layout.

ChartRenderer owns chart rendering.

DashboardWidgetFactory owns dashboard widget creation.

ChartWidgetFactory owns chart widget creation.

Widgets render presentation models only.

Business logic inside widgets or renderers is prohibited.

---

# Artificial Intelligence

Artificial Intelligence never

- calculates indicators
- generates buy/sell signals
- performs portfolio calculations
- determines position sizing

Artificial Intelligence only explains deterministic results produced by the Trading Pipeline.

---

# Long-Term Vision

Project Orion will evolve into a professional deterministic AI-assisted desktop trading platform featuring

- Professional Desktop Dashboard
- Unified Dashboard Workspace
- Production Chart Pipeline
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

Workspace Foundation

🟢 Completed

Chart Foundation

🟢 Completed

Production Chart Pipeline

🟢 Completed

Visible Chart Integration

🟢 In Progress

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

Architecture Freeze

**v1.5**

Current Sprint

**Sprint 4.4 — Production Chart Pipeline**

Current Validation

```
run_tests.py

Passed: 6
Failed: 0
```

Additional Presentation Validation

```
10 dedicated presentation tests
All Passing
```

Git Status

Ready for documentation synchronization and Sprint 4.4 completion.

---