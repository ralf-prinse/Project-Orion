# PROJECT ORION

# PRESENTER_ARCHITECTURE.md

**Purpose:** Desktop Presentation Architecture

**Status:** Active

**Last Updated:** July 2026

---

# 1. Purpose

This document defines the presentation architecture of Project Orion.

Its purpose is to ensure that the desktop application remains modular,
maintainable, deterministic and easy to extend.

The presentation architecture is intentionally separated from the deterministic
business architecture described in `ORION_MASTER_ARCHITECTURE.md`.

---

# 2. Core Philosophy

The GUI is a presentation layer.

It never owns business logic.

It never performs calculations.

It never makes trading decisions.

Every visual element originates from deterministic models produced by Orion's
core services.

---

# 3. Presentation Flow

Every screen follows exactly the same direction of data flow.

```text
Deterministic Service
        │
        ▼
Presenter
        │
        ▼
GuiSection
        │
        ▼
WorkspacePanel
        │
        ▼
Workspace
        │
        ▼
MainWindow
```

Data always flows downward.

No presentation component may modify deterministic models.

---

# 4. Responsibilities

## Deterministic Services

Responsible for:

- calculations
- market analysis
- signals
- decisions
- portfolio management
- risk management
- trade planning

Never responsible for:

- Qt
- widgets
- layouts
- styling
- presentation

---

## Presenters

Presenters transform deterministic models into presentation models.

Responsible for:

- GuiSection creation
- GuiMetric creation
- labels
- formatting
- descriptions
- presentation grouping

Never responsible for:

- calculations
- service orchestration
- database access
- portfolio mutation
- risk calculations

---

## GuiSection

GuiSection is the standard presentation model.

A GuiSection contains only display data.

Typical contents:

- title
- description
- metrics

GuiSection contains no business logic.

---

## WorkspacePanel

WorkspacePanel is Orion's reusable renderer.

Responsibilities:

- render GuiSections
- render titles
- render metrics
- own Qt widgets

WorkspacePanel never communicates with services.

---

## Workspaces

Every workspace owns only presentation layout.

Responsibilities:

- arrange WorkspacePanels
- manage widgets
- expose presentation APIs

Preferred public API:

```python
set_sections(sections)
```

Temporary compatibility methods may exist during migrations but should eventually
be removed.

---

## MainWindow

MainWindow is the composition root.

Responsibilities:

- dependency wiring
- workspace creation
- navigation
- orchestration

MainWindow should never contain:

- HTML generation
- presentation formatting
- business calculations

---

# 5. Standard Rendering Pipeline

The preferred rendering pipeline is:

```text
Portfolio
        │
PortfolioPresenter
        │
GuiSection
        │
WorkspacePanel.from_section()
        │
PortfolioWorkspace
```

The same pattern applies to every workspace.

---

# 6. Current Presenter Catalogue

Implemented:

- DashboardPresenter
- PortfolioPresenter
- HistoryPresenter
- SettingsPresenter
- TradeAdvicePresenter

Planned:

- PerformancePresenter
- AIExplanationPresenter
- BacktestPresenter
- PaperTradingPresenter

---

# 7. Current Workspace Catalogue

Implemented:

- DashboardWorkspace
- ScannerWorkspace
- PortfolioWorkspace
- HistoryWorkspace
- SettingsWorkspace

Future:

- PerformanceWorkspace
- AIWorkspace

---

# 8. Migration Status

## Portfolio

Status:

✅ GuiSection based

---

## History

Status:

✅ GuiSection based

---

## Settings

Status:

✅ Presenter based

---

## Dashboard

Status:

🚧 Migration in progress

---

## Scanner

Status:

🚧 Migration in progress

---

# 9. Architectural Rules

## Rule 1

Business logic never belongs inside Qt widgets.

---

## Rule 2

Presenters own presentation formatting.

---

## Rule 3

MainWindow remains a composition root.

---

## Rule 4

GuiSection is the preferred presentation model.

---

## Rule 5

WorkspacePanel is the preferred renderer.

---

## Rule 6

Data always flows downward.

```text
Service
    ↓
Presenter
    ↓
Workspace
    ↓
Qt
```

Never in reverse.

---

# 10. Long-Term Vision

The desktop application should evolve without changing the presentation
architecture.

Future additions may include:

- tables
- charts
- docking
- layout persistence
- multi-monitor support
- AI workspace
- plugins

These features should integrate into the existing presentation pipeline rather
than introducing alternative architectures.

---

# 11. Definition of Done

A presentation feature is considered complete when:

- deterministic service exists
- presenter exists
- GuiSections are produced
- Workspace renders GuiSections
- MainWindow only orchestrates
- regression tests pass
- documentation is synchronized

---

# 12. Guiding Principle

A developer should be able to understand any Orion workspace by reading:

```
Service
↓
Presenter
↓
Workspace
```

Nothing more.

If additional layers become necessary, they should be introduced only when they
provide a clear architectural benefit.

---

End of document.