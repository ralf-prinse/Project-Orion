# PROJECT ORION

# TODO.md

**Status:** Active Development

---

# Development Roadmap

Project Orion is developed through Epics.

Every Epic consists of Features.

Every Feature consists of small deterministic implementation tasks.

Architecture always takes precedence over implementation speed.

---

# EPIC 1 — Deterministic Trading Platform

**Status:** ✅ Completed

Completed:

- Universe Layer
- Market Data Layer
- Historical Data Layer
- Indicator Engine
- Analysis Layer
- Signal Layer
- Decision Layer
- Portfolio Engine
- Risk Manager
- Trade Planner
- Backtesting
- Paper Trading
- Performance Analytics
- Explainability Framework
- AI Explanation Layer
- Dependency Injection
- Event Bus
- Scan Orchestrator
- Configuration Framework

---

# EPIC 2 — Professional Desktop Experience

**Status:** 🚧 In Progress

Goal:

Transform Orion into a professional desktop trading platform while preserving complete separation between deterministic business logic and presentation.

---

# Feature 2.1 — Workspace Framework

**Status:** ✅ Completed

Completed:

- WorkspaceController
- DashboardRouter
- BaseWorkspace
- WorkspacePanel
- DashboardWorkspace
- ScannerWorkspace
- PortfolioWorkspace
- HistoryWorkspace
- SettingsWorkspace
- Workspace navigation
- MainWindow composition-root migration

---

# Feature 2.2 — Presenter Architecture

**Status:** 🚧 In Progress

Completed:

- DashboardPresenter
- PortfolioPresenter
- HistoryPresenter
- SettingsPresenter

Remaining:

- Complete presenter migration
- Remove remaining HTML presentation
- Standardize GuiSection rendering

---

# Feature 2.3 — GuiSection Migration

**Status:** 🚧 In Progress

Tasks:

- Simplify WorkspacePanel rendering
- Migrate remaining workspaces to WorkspacePanel.from_section()
- Migrate DashboardWorkspace
- Migrate HistoryWorkspace
- Migrate ScannerWorkspace
- Eliminate remaining HTML rendering

---

# Feature 2.4 — Professional Desktop UX

**Status:** 🟡 Planned

Tasks:

- Professional dashboard layout
- Docking architecture
- Layout persistence
- Keyboard shortcuts
- Toolbar
- Status bar
- Theme improvements
- Responsive layouts

---

# Feature 2.5 — Portfolio Experience

**Status:** 🟡 Planned

Tasks:

- Position cards
- Exposure overview
- Allocation overview
- Portfolio metrics
- Performance integration

---

# Feature 2.6 — AI Workspace

**Status:** 🟡 Planned

Tasks:

- AI explanations
- Trade summaries
- Recommendation explanations
- Daily overview

---

# EPIC 3 — Advanced Trading Platform

**Status:** 🔵 Future

Potential features:

- Broker integration
- Watchlists
- Alerts
- Market calendar
- Earnings calendar
- Multi-monitor support
- Cloud synchronization

---

# EPIC 4 — AI Assistant

**Status:** 🔵 Future

Potential features:

- Natural language interaction
- Portfolio coaching
- Scan summaries
- Daily reports
- Workflow assistance

AI remains explanation-only.

---

# Continuous Engineering Tasks

Always active:

- Keep documentation synchronized
- Keep regression tests green
- Preserve deterministic behaviour
- Review architecture before implementation
- Minimize technical debt
- Prefer complete file replacements
- Keep GUI presentation-only

---

# Definition of Done

A task is complete when:

- Architecture reviewed
- Existing implementation reviewed
- One logical responsibility implemented
- Regression tests passed
- Documentation synchronized
- Commit created
- Changes pushed

---

# Immediate Next Focus

Priority order:

1. Simplify WorkspacePanel rendering
2. Migrate remaining workspaces to GuiSection-based panels
3. Complete GuiSection migration
4. Complete presenter migration
5. Remove remaining HTML rendering
6. Professional desktop UX

---

End of document.