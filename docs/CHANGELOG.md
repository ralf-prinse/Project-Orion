# PROJECT ORION

# CHANGELOG.md

All notable changes to Project Orion are documented in this file.

The format is inspired by *Keep a Changelog*.

---

# [Unreleased]

# [v1.0.16-alpha] — Workspace Composition Foundation

## Added

### Workspace Composition

- Introduced `GuiWorkspace` as the standard workspace presentation model.
- Introduced `WorkspaceCoordinator`.
- Introduced `PortfolioWorkspacePresenter`.

### Portfolio Analytics

- Added `PortfolioAnalyticsResult`.
- Added `PortfolioAnalyticsService`.
- Added `PortfolioStateAdapter`.

### Professional Desktop Components

- Introduced `GuiMetricCard`.
- Introduced reusable `MetricCard`.
- Introduced `PortfolioMetricCardPresenter`.

### Documentation

Fully synchronized:

- AI_CONTEXT.md
- CURRENT_STATE.md
- PROJECT_STATUS.md
- PRESENTER_ARCHITECTURE.md
- ORION_MASTER_ARCHITECTURE.md
- TODO.md
- CHANGELOG.md

---

## Changed

### Desktop Presentation Architecture

The desktop architecture evolved from a Presenter Architecture into a
Workspace Composition Architecture.

Official presentation pipeline:

```text
Deterministic Service
        │
        ▼
WorkspaceCoordinator
        │
        ▼
WorkspacePresenter
        │
        ▼
GuiWorkspace
├── GuiMetricCard
└── GuiSection
        │
        ▼
Workspace
        │
        ▼
Reusable Qt Widgets
        │
        ▼
MainWindow
```

### Portfolio

Portfolio presentation now supports:

- workspace composition
- KPI presentation models
- analytics composition
- reusable presentation components

### Architecture

Epic 3 foundation has been completed.

Future development now focuses primarily on professional desktop features rather
than architectural redesign.

---

## Validation

Regression validation completed successfully.

```text
343 tests passed
```

---

## Notes

This release establishes the Workspace Composition Architecture as the official
desktop architecture for Project Orion.

Future desktop functionality—including charts, AI workspaces, broker
integration, reporting and advanced dashboards—will extend this architecture
rather than replacing it.

## Next Focus

### Epic 3 — Professional Desktop Features

Planned:

- Desktop UX polish
- Portfolio Analytics
- Professional Charts
- AI Workspace
- Docking & Layout Persistence
- Multi-monitor Support
- Broker Integration
- Advanced Reporting

---

# [v1.0.15-alpha] — Desktop Architecture Completion

## Added

### Presentation Architecture

- Introduced `PRESENTER_ARCHITECTURE.md`.
- Introduced `TradeAdvicePresenter`.
- Standardized `GuiSection` as Orion's primary presentation model.
- Introduced `WorkspacePanel.from_section()`.

### Workspaces

Completed migration of:

- DashboardWorkspace
- ScannerWorkspace
- PortfolioWorkspace
- HistoryWorkspace

to the standardized GuiSection presentation workflow.

### Documentation

Updated:

- AI_CONTEXT.md
- CURRENT_STATE.md
- PROJECT_STATUS.md
- TODO.md
- PRESENTER_ARCHITECTURE.md

---

## Changed

### MainWindow

MainWindow now primarily acts as Orion's composition root.

Responsibilities:

- dependency wiring
- workspace orchestration
- presenter coordination
- navigation

Presentation formatting responsibilities were removed.

### Presentation Layer

Presentation rendering is now standardized.

Pipeline:

```text
Service
    ↓
Presenter
    ↓
GuiSection
    ↓
WorkspacePanel
    ↓
Workspace
    ↓
MainWindow
```

### Desktop Architecture

Completed migration from legacy presentation rendering to presenter-driven rendering.

Epic 2 is now considered architecturally complete.

---

## Removed

- GuiSectionRenderer
- Legacy trade advice rendering
- Legacy HTML generation inside MainWindow
- Legacy action-card formatting

---

## Validation

Regression validation completed successfully.

```text
334 tests passed
```

---

## Architecture

Desktop presentation architecture is now considered stable.

Future development will primarily focus on Epic 3:

- Professional Desktop UX
- Portfolio Analytics
- AI Workspace
- Professional Charts
- Broker Integration

# [v1.0.14-alpha] — Workspace Framework Phase 1

## Added

### Workspace Architecture

* Introduced deterministic `WorkspaceController`
* Introduced deterministic `DashboardRouter`
* Added toolkit-independent workspace navigation layer
* Added centralized dashboard routing for presentation models

### GUI Foundation

* Connected `MainWindow` to `WorkspaceController`
* Reduced `GuiShell` responsibilities by delegating dashboard composition
* Preserved public `GuiShell` API during refactoring
* Improved separation between navigation and dashboard composition

### Architecture

* Continued migration toward a presentation-only GUI
* Further decoupled Qt implementation from deterministic application state
* Improved Workspace Framework foundation for future professional desktop features

### Validation

Regression validation completed successfully.

```text
334 tests passed
```

### Documentation

Updated:

* CURRENT_STATE.md
* PROJECT_STATUS.md
* TODO.md
* CHANGELOG.md
* AI_CONTEXT.md

---

# [v1.0 Alpha]

## Added

### Core Architecture

* Layered deterministic architecture
* Registry-driven processing pipelines
* AnalyzerRunner infrastructure
* ApplicationContainer
* ServiceRegistry
* Configuration Framework
* Event Bus
* Scan Orchestrator
* Explainability Framework

---

### Market Data

Added:

* Universe management
* Quote providers
* Quote caching
* Historical data caching
* Provider abstraction

---

### Analysis

Added:

* Indicator Library
* Indicator Engine
* Trend Analysis
* Momentum Analysis
* Volatility Analysis
* Structure Analysis
* Volume Analysis
* Relative Strength Analysis
* Market Regime Analysis
* Candlestick Pattern Analysis

---

### Signal Processing

Added:

* Signal Engine
* Signal Registry
* Signal analyzers
* Deterministic signal generation

---

### Decision Layer

Added:

* Decision Engine
* Decision Registry
* Decision analyzers
* Explainable decision pipeline

---

### Portfolio

Added:

* Portfolio Engine
* Portfolio validation
* Exposure management

---

### Risk

Added:

* Risk Manager
* Drawdown analysis
* Capital protection
* Position exposure validation

---

### Trade Planning

Added:

* Trade Planner
* Risk/Reward calculations
* Trade plan generation

---

### Simulation

Added:

* Backtesting Engine
* Paper Trading Engine
* Performance Analytics

---

### Artificial Intelligence

Added:

* AI Explanation Layer

AI remains explanation-only.

---

### GUI

Added:

* GUI Foundation
* Design System
* Navigation Framework
* Dashboard Foundation
* Workspace Foundation

---

## Changed

* Development workflow moved from sprint-based to Epic-based planning.
* Documentation reorganised into dedicated engineering documents.
* Architecture-first development process adopted.
* Repository-driven workflow introduced.

---

## Documentation

Updated:

* AI_CONTEXT.md
* PROJECT_STATUS.md
* TODO.md
* CHANGELOG.md

Documentation responsibilities were clearly separated to avoid duplication.

---

# Future

Future development continues under the Epic roadmap defined in `TODO.md`.
