# PROJECT ORION

# TODO.md

**Status:** Active Development

---

# Development Roadmap

Project Orion is developed through Epics.

Each Epic consists of Features.

Each Feature consists of small implementation Tasks.

Architecture always takes precedence over new functionality.

---

# EPIC 1 — Deterministic Trading Platform

**Status:** ✅ Completed

Completed systems:

* Universe Layer
* Market Data Layer
* Historical Data Layer
* Indicator Engine
* Analysis Layer
* Signal Layer
* Decision Layer
* Portfolio Engine
* Risk Manager
* Trade Planner
* Backtesting
* Paper Trading
* Performance Analytics
* Explainability Framework
* AI Explanation Layer
* Dependency Injection
* Event Bus
* Scan Orchestrator
* Configuration Framework

---

# EPIC 2 — Professional Desktop Experience

**Status:** 🚧 In Progress

Goal:

Transform Orion into a professional desktop trading platform while preserving complete separation between deterministic business logic and presentation.

---

# Feature 2.1 — Workspace Framework

**Status:** 🚧 In Progress

## Completed

* [x] Introduce WorkspaceController
* [x] Introduce DashboardRouter
* [x] GuiShell Refactor — Phase 1
* [x] MainWindow navigation decoupled from direct page switching

## Remaining

* [ ] Continue GuiShell decomposition
* [ ] Introduce feature-oriented workspace pages
* [ ] Docking architecture integration
* [ ] Workspace state persistence
* [ ] Navigation improvements
* [ ] Layout persistence

---

# Feature 2.2 — Professional Dashboard

**Status:** 🟡 Planned

Tasks:

* [ ] Professional dashboard layout
* [ ] Dashboard workspace
* [ ] Dashboard cards
* [ ] Metric tiles
* [ ] Status widgets
* [ ] Market overview
* [ ] Recent activity
* [ ] Scan summary
* [ ] Portfolio snapshot

---

# Feature 2.3 — Scanner Workspace

**Status:** 🟡 Planned

Tasks:

* [ ] Dedicated Scanner Workspace
* [ ] Scan progress
* [ ] Result table
* [ ] Filtering
* [ ] Sorting
* [ ] Scan history

---

# Feature 2.4 — Portfolio Workspace

**Status:** 🟡 Planned

Tasks:

* [ ] Portfolio Workspace
* [ ] Positions
* [ ] Allocation
* [ ] Exposure
* [ ] Sector allocation
* [ ] Open risk overview

---

# Feature 2.5 — Performance Workspace

**Status:** 🟡 Planned

Tasks:

* [ ] Performance Workspace
* [ ] Equity curve
* [ ] Performance statistics
* [ ] Win rate
* [ ] Drawdown
* [ ] Monthly performance

---

# Feature 2.6 — AI Workspace

**Status:** 🟡 Planned

Tasks:

* [ ] AI Explanation Workspace
* [ ] Trade explanations
* [ ] Recommendation details
* [ ] Scan summaries
* [ ] Decision explanations

---

# Feature 2.7 — Settings Workspace

**Status:** 🟡 Planned

Tasks:

* [ ] Theme configuration
* [ ] Application configuration
* [ ] Provider configuration
* [ ] User profiles

---

# Feature 2.8 — Desktop Polish

**Status:** 🟡 Planned

Tasks:

* [ ] Docking improvements
* [ ] Icons
* [ ] Keyboard shortcuts
* [ ] Accessibility
* [ ] Responsive layouts
* [ ] Theme improvements

---

# EPIC 3 — Advanced Trading Platform

**Status:** 🔵 Future

Potential features:

* Broker integration
* Watchlists
* Alerts
* Market calendar
* Earnings calendar
* Notifications
* Multi-monitor support
* Cloud synchronization

---

# EPIC 4 — AI Assistant

**Status:** 🔵 Future

Potential features:

* Natural language queries
* AI coaching
* Portfolio explanations
* Scan summaries
* Daily reports

Artificial Intelligence remains explanation-only.

AI never replaces deterministic trading engines.

---

# Continuous Engineering Tasks

These tasks are always active.

* [ ] Keep documentation synchronized
* [ ] Keep regression tests green
* [ ] Minimize technical debt
* [ ] Preserve deterministic behaviour
* [ ] Review architecture before implementation
* [ ] Prefer small incremental changes
* [ ] Keep GUI presentation-only

---

# Definition of Done

A task is complete when:

* Architecture reviewed
* Existing implementation reviewed
* One logical change implemented
* Tests executed successfully
* Documentation synchronized
* Commit created
* Changes pushed to GitHub

---

# Immediate Next Focus

Epic 2 → Workspace Framework Phase 2

Priority order:

1. Continue GuiShell decomposition
2. Professional Dashboard Workspace
3. Scanner Workspace
4. Portfolio Workspace
5. Performance Workspace
6. AI Workspace

---

End of document.
