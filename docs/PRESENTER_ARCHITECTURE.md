# PROJECT ORION

# PRESENTER_ARCHITECTURE.md

**Purpose:** Desktop Presentation & Workspace Composition Architecture

**Status:** Active

**Last Updated:** July 2026

---

# 1. Purpose

This document defines the official desktop presentation architecture of
Project Orion.

Its purpose is to ensure that every desktop feature follows the same layered
presentation model while keeping deterministic business logic completely
separated from the graphical user interface.

The desktop architecture is intentionally independent from the deterministic
engine architecture described in ORION_MASTER_ARCHITECTURE.md.

---

# 2. Architectural Philosophy

Project Orion follows a Workspace Composition Architecture.

Business logic remains completely deterministic.

Presentation is built through reusable presentation models.

Qt widgets perform rendering only.

Every layer owns exactly one responsibility.

The architecture favors:

- Composition
- Small classes
- Stable public APIs
- Reusable presentation models
- Thin GUI

---

# 3. Official Presentation Pipeline

The official desktop pipeline is now:

Deterministic Service

↓

WorkspaceCoordinator

↓

WorkspacePresenter

↓

GuiWorkspace

├── GuiMetricCard

└── GuiSection

↓

Workspace

↓

Reusable Qt Widgets

↓

MainWindow

Data always flows downward.

No presentation layer may modify deterministic business models.

---

# 4. Layer Responsibilities

## Deterministic Services

Responsible for:

- calculations
- market analysis
- signals
- decisions
- portfolio validation
- risk management
- analytics

Never responsible for:

- Qt
- widgets
- formatting
- layouts
- presentation

---

## WorkspaceCoordinator

WorkspaceCoordinator is responsible for workspace orchestration.

Responsibilities:

- coordinate workspace presenters
- build GuiWorkspace objects
- keep MainWindow small

WorkspaceCoordinator never performs calculations.

---

## WorkspacePresenter

Workspace presenters coordinate presentation.

Responsibilities:

- compose multiple presenters
- coordinate presentation services
- return one GuiWorkspace

Workspace presenters never perform business calculations.

---

## Presenters

Presenters convert deterministic models into presentation models.

Responsibilities:

- create GuiSection
- create GuiMetricCard
- format labels
- format values
- group presentation data

Presenters never perform:

- calculations
- service orchestration
- database access
- portfolio mutation

---

## GuiWorkspace

GuiWorkspace is the standard presentation model returned by every workspace
presenter.

It groups all presentation components required by one workspace while exposing
a single stable public API.

Current presentation components:

- GuiMetricCard
- GuiSection

Future presentation components may include:

- GuiChart
- GuiTable
- GuiTimeline
- GuiAlert
- GuiDockLayout

GuiWorkspace intentionally contains presentation data only.

It never contains business logic.

---

## GuiMetricCard

GuiMetricCard represents one highlighted KPI.

Typical examples:

- Portfolio Value
- Cash
- Exposure
- Open Positions

GuiMetricCard contains only display information.

Typical properties:

- title
- value
- subtitle
- trend

GuiMetricCard is rendered by MetricCard.

---

## GuiSection

GuiSection represents grouped presentation data.

Typical examples:

- Portfolio Analytics
- Position Analytics
- Trade Advice
- Scanner Results
- History

A GuiSection contains:

- title
- description
- metrics

GuiSection remains Orion's standard detailed presentation model.

---

## Workspace

Each workspace owns only layout.

Responsibilities:

- arrange presentation widgets
- render GuiWorkspace
- manage widget lifetime

Workspaces never:

- calculate
- query services
- build presentation models

Preferred public API:

```python
set_workspace(workspace: GuiWorkspace)
```

Compatibility methods such as:

```python
set_sections(...)
```

may temporarily exist during migration but should eventually disappear.

---

## MetricCard

MetricCard is Orion's reusable KPI renderer.

Responsibilities:

- render GuiMetricCard
- own Qt widgets
- display highlighted metrics

MetricCard never communicates with deterministic services.

---

## WorkspacePanel

WorkspacePanel is Orion's reusable section renderer.

Responsibilities:

- render GuiSection
- render GuiMetric objects
- own Qt widgets

WorkspacePanel never performs calculations.

---

## MainWindow

MainWindow remains the application's composition root.

Responsibilities:

- dependency wiring
- application startup
- navigation
- workspace switching

MainWindow should never:

- format presentation
- build GuiWorkspace
- compose presentation models
- perform business calculations

Presentation composition belongs to WorkspaceCoordinator.

---

# 5. Current Presentation Components

Implemented:

- GuiWorkspace
- GuiMetricCard
- GuiSection
- GuiMetric

Rendering widgets:

- MetricCard
- WorkspacePanel

Current workspaces:

- DashboardWorkspace
- ScannerWorkspace
- PortfolioWorkspace
- HistoryWorkspace
- SettingsWorkspace

Future workspaces:

- AIWorkspace
- PerformanceWorkspace
- BrokerWorkspace
- BacktestingWorkspace

Every new workspace should consume a GuiWorkspace.

---

# 6. Current Presenter Catalogue

Implemented:

- DashboardPresenter
- PortfolioPresenter
- PortfolioAnalyticsPresenter
- PortfolioMetricCardPresenter
- PortfolioWorkspacePresenter
- HistoryPresenter
- SettingsPresenter
- TradeAdvicePresenter

Future presenters:

- AIWorkspacePresenter
- PerformanceWorkspacePresenter
- BrokerWorkspacePresenter

Workspace presenters should remain small and compose specialized presenters
rather than accumulating responsibilities.

---

# 7. Migration Status

The migration from the original Presenter Architecture to the Workspace
Composition Architecture is complete.

## Dashboard

Status:

✅ Complete

Uses standardized presentation models.

---

## Scanner

Status:

✅ Complete

Uses standardized presentation models.

---

## Portfolio

Status:

✅ Complete

Uses:

- PortfolioWorkspacePresenter
- PortfolioMetricCardPresenter
- PortfolioAnalyticsPresenter
- GuiWorkspace

---

## History

Status:

✅ Complete

Uses standardized presentation models.

---

## Settings

Status:

✅ Complete

Fully migrated to GuiSection-based presentation.

---

# 8. Architectural Rules

## Rule 1

Business logic never belongs inside Qt widgets.

---

## Rule 2

Deterministic services never create presentation models.

---

## Rule 3

WorkspaceCoordinator owns workspace composition.

---

## Rule 4

WorkspacePresenters own presentation composition.

---

## Rule 5

Specialized presenters own formatting.

Examples:

- PortfolioPresenter
- PortfolioAnalyticsPresenter
- PortfolioMetricCardPresenter

---

## Rule 6

GuiWorkspace is the standard presentation model for complete workspaces.

---

## Rule 7

GuiSection remains the standard detailed presentation model.

---

## Rule 8

GuiMetricCard remains the standard KPI presentation model.

---

## Rule 9

Reusable widgets perform rendering only.

Examples:

- MetricCard
- WorkspacePanel

---

## Rule 10

Data always flows downward.

Deterministic Service

↓

WorkspaceCoordinator

↓

WorkspacePresenter

↓

GuiWorkspace

↓

Workspace

↓

Qt Widgets

Never in reverse.

---

# 9. Long-Term Vision

The presentation architecture should remain stable while desktop functionality
continues to expand.

Future presentation components may include:

- Professional Charts
- Data Tables
- Timeline Views
- Docking Layouts
- AI Panels
- Broker Widgets
- Reporting Views
- Multi-monitor Dashboards

These features should extend the Workspace Composition Architecture rather than
introducing alternative presentation patterns.

---

# 10. Definition of Done

A presentation feature is considered complete when:

✓ Deterministic service exists

✓ Presentation models exist

✓ Specialized presenters exist

✓ Workspace presenter composes the presentation

✓ GuiWorkspace is produced

✓ Workspace renders GuiWorkspace

✓ MainWindow only orchestrates

✓ Regression tests pass

✓ Documentation is synchronized

---

# 11. Guiding Principle

A developer should be able to understand any Orion workspace by following the
same layered structure:

Deterministic Service

↓

WorkspaceCoordinator

↓

WorkspacePresenter

↓

GuiWorkspace

↓

Workspace

↓

Reusable Qt Widgets

↓

MainWindow

Every new feature should integrate naturally into this architecture.

If additional abstraction is considered, it should only be introduced when it
clearly reduces long-term complexity and supports concrete functionality.

---

End of document.