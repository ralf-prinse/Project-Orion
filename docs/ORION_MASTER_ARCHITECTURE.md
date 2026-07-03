# ORION MASTER ARCHITECTURE

---

# Architecture Version

**Architecture Freeze v1.5**

Status

🟢 Production Foundation Stable

Current Phase

🚧 Sprint 4.4 — Production Chart Pipeline

---

# System Philosophy

Project Orion is a deterministic AI-assisted desktop trading platform.

Every architectural layer owns exactly one responsibility.

Artificial Intelligence never performs investment calculations.

Artificial Intelligence only explains deterministic results.

The deterministic Trading Pipeline remains the single source of truth.

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

Rendering remains centralized.

Workspace composition remains centralized.

---

## Explainability

Every recommendation must always be

- deterministic
- reproducible
- traceable
- explainable

---

## Production Workflow

Every sprint follows

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

# Dashboard Evolution

Sprint 4.1

Completed Dashboard migration.

↓

Sprint 4.2

Completed reusable Dashboard Widget Library.

↓

Sprint 4.3

Completed Unified Dashboard Workspace foundation.

↓

Sprint 4.4

Introduces the first production chart pipeline.

The dashboard now evolves from a card-based presentation into a complete workspace capable of rendering reusable cards, charts and future presentation components through one unified rendering pipeline.

---

# Unified Dashboard Architecture

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

The presentation pipeline is now fully separated into composition, rendering and widget creation.

Business logic remains prohibited throughout the presentation layer.

---

# Presentation Responsibilities

ApplicationController

- Coordinates desktop communication.

DashboardData

- Aggregates deterministic backend results.

Dashboard2Presenter

- Produces reusable dashboard cards.

DashboardWorkspacePresenter

- Creates one GuiWorkspace.
- Orchestrates presentation.
- Produces dashboard charts.
- Contains no business logic.

EquityCurveChartPresenter

- Produces GuiChart objects.
- Performs no calculations.
- Contains no Qt code.

GuiWorkspace

- Canonical presentation model.
- Owns cards.
- Owns charts.
- Owns sections.
- Owns metadata.

WorkspaceRenderer

- Renders complete workspaces.
- Coordinates specialized renderers.
- Contains no layout logic.

DashboardGrid

- Owns metric card layout only.

ChartRenderer

- Renders GuiChart objects.
- Delegates widget creation.

ChartWidgetFactory

- Selects chart widgets.
- Centralizes chart widget creation.

LineChartWidget

- Renders GuiChart.
- Contains no business logic.
- Contains no calculations.

---

# GuiWorkspace

GuiWorkspace is now the canonical presentation object for every dashboard.

Current structure

```
GuiWorkspace

├── cards

├── charts

├── chart_sections

├── sections

├── metadata

└── status
```

GuiWorkspace owns dashboard composition.

DashboardWorkspace owns presentation only.

Business logic remains prohibited.

---

# Chart Presentation Models

Sprint 4.4 introduces reusable chart presentation models.

Completed models

✅ GuiChart

✅ GuiChartType

✅ GuiSeries

✅ GuiAxis

✅ GuiLegend

✅ GuiChartSection

These models are presentation-only.

They perform

- no calculations
- no portfolio logic
- no AI logic
- no trading logic

They exist solely to describe chart presentation.

---

# Chart Rendering Architecture

Chart rendering is now separated from workspace composition.

```
GuiChart
        ↓
ChartRenderer
        ↓
ChartWidgetFactory
        ↓
LineChartWidget
```

Future chart widgets

- AreaChartWidget
- BarChartWidget
- PieChartWidget
- DonutChartWidget
- HeatMapWidget

No workspace modifications are required when introducing additional chart widgets.

---

# Workspace Rendering

Workspace rendering is centralized.

```
GuiWorkspace
        ↓
WorkspaceRenderer
        ├──────── DashboardGrid
        └──────── ChartRenderer
```

WorkspaceRenderer orchestrates rendering only.

Layout responsibilities remain delegated to specialized components.

Business logic remains prohibited.

---

# Widget Creation

Widget creation remains centralized.

Cards

```
GuiMetricCard
        ↓
DashboardWidgetFactory
        ↓
MetricCard

HeroMetricCard

MarketHealthBanner
```

Charts

```
GuiChart
        ↓
ChartWidgetFactory
        ↓
LineChartWidget

Future Chart Widgets
```

Factories never perform business logic.

Widgets never perform calculations.

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

### Core

✅ ApplicationController

✅ Trading Workspace

✅ Scanner Workspace

---

### Dashboard Presentation

✅ DashboardData

✅ Dashboard2Presenter

✅ DashboardWorkspacePresenter

✅ DashboardWorkspace

✅ WorkspaceRenderer

✅ DashboardGrid

✅ ChartRenderer

✅ ChartContainer

---

### Presentation Models

✅ GuiWorkspace

✅ GuiWorkspaceSection

✅ GuiChart

✅ GuiChartSection

✅ GuiMetricCard

✅ GuiChartType

✅ GuiSeries

✅ GuiAxis

✅ GuiLegend

---

### Widget Factories

✅ DashboardWidgetFactory

✅ ChartWidgetFactory

---

### Desktop Widgets

✅ MetricCard

✅ HeroMetricCard

✅ MarketHealthBanner

✅ LineChartWidget

✅ EquityCurveWidget (foundation)

---

# Regression Testing

Regression validation remains centralized.

Primary validation

```powershell
python run_tests.py
```

Expected production result

```
Passed: 6
Failed: 0
```

Additional Sprint 4.4 validation

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

Regression validation remains mandatory before every commit.

---

# Current Development Focus

The deterministic backend remains feature complete.

Current development focuses on expanding the desktop presentation layer using the completed Workspace and Chart infrastructure.

Current priorities

- Integrate real chart rendering
- Connect LineChartWidget to a charting library
- Portfolio Allocation visualization
- Gauge widgets
- Dashboard Layout 2.0
- Live Dashboard updates

No backend expansion is currently planned.

---

# Architecture Rules

Business logic belongs exclusively inside backend services.

Presenters transform deterministic backend output into presentation models.

GuiWorkspace owns dashboard composition.

WorkspaceRenderer owns rendering orchestration.

DashboardGrid owns card layout.

ChartRenderer owns chart rendering.

DashboardWidgetFactory owns dashboard widget creation.

ChartWidgetFactory owns chart widget creation.

Widgets render presentation models only.

Business logic inside widgets or renderers is prohibited.

Artificial Intelligence never performs deterministic calculations.

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

# Architecture Status

Architecture Version

**Architecture Freeze v1.5**

Current Version

**v1.2.0-alpha**

Current Sprint

**Sprint 4.4 — Production Chart Pipeline**

Sprint Status

🚧 In Progress

Backend

🟢 Production Stable

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

Regression Tests

🟢 Passing

Documentation

🟢 Current

Git

Ready for commit after documentation synchronization.

---