# PROJECT ORION

# CHANGELOG.md

All notable changes to Project Orion are documented in this file.

The format is inspired by *Keep a Changelog*.

---

# [Unreleased]

## Next Focus

### Epic 2 — Professional Desktop Experience

Planned:

* Continue GuiShell decomposition
* Professional Dashboard Workspace
* Scanner Workspace
* Portfolio Workspace
* Performance Workspace
* AI Workspace
* Settings Workspace
* Workspace layout persistence

---

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
