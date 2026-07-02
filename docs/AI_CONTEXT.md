# PROJECT ORION

# AI_CONTEXT.md

**Purpose:** Engineering Context
**Status:** Active Development
**Audience:** Developers, AI Assistants, Software Architects

---

# 1. Purpose

This document provides the engineering context required to continue development of Project Orion.

It intentionally contains only the current engineering context.

Historical implementation details belong in `CHANGELOG.md`.

Current implementation progress belongs in `CURRENT_STATE.md` and `PROJECT_STATUS.md`.

Long-term architectural decisions belong in `ORION_MASTER_ARCHITECTURE.md`.

---

# 2. Product Overview

Project Orion is a professional desktop application for deterministic swing-trading analysis of the United States stock market.

Its objective is to analyse thousands of stocks through a transparent processing pipeline and identify high-quality trading opportunities.

Project Orion is **not** an automated trading bot.

It is a deterministic decision-support platform.

Artificial Intelligence is used exclusively to explain deterministic outputs.

AI never:

- generates trading signals
- approves trades
- calculates indicators
- validates portfolio risk
- sizes positions
- overrides deterministic engines

Every recommendation produced by Orion must remain:

- deterministic
- reproducible
- explainable
- testable
- transparent

---

# 3. High-Level Architecture

Project Orion follows a layered deterministic architecture.

```
Universe Layer
        ↓
Market Data Layer
        ↓
Historical Data Layer
        ↓
Indicator Engine
        ↓
Analysis Layer
        ↓
Signal Layer
        ↓
Decision Layer
        ↓
Portfolio Engine
        ↓
Risk Manager
        ↓
Trade Planner
        ↓
AI Explanation Layer
        ↓
Desktop GUI
```

Each processing layer owns exactly one responsibility.

Business logic never belongs inside the GUI.

---

# 4. Desktop GUI Architecture

The desktop application follows a presentation-only architecture.

```
Deterministic Services
        ↓
Presenters
        ↓
GuiSection Models
        ↓
Workspace Panels
        ↓
Workspace Pages
        ↓
MainWindow (Composition Root)
```

Responsibilities:

**Services**

- deterministic calculations
- business rules
- orchestration

**Presenters**

- convert deterministic models into GUI models
- never perform calculations

**Workspace Pages**

- display presentation models
- own Qt widgets only

**MainWindow**

- composition root
- dependency wiring
- navigation
- workspace orchestration

---

# 5. Shared GUI Infrastructure

Current reusable GUI infrastructure includes:

- WorkspaceController
- DashboardRouter
- BaseWorkspace
- WorkspacePanel
- DashboardWorkspace
- ScannerWorkspace
- PortfolioWorkspace
- HistoryWorkspace
- SettingsWorkspace
- DashboardPresenter
- PortfolioPresenter
- HistoryPresenter
- SettingsPresenter

Future GUI functionality should extend this infrastructure rather than introducing duplicate implementations.

---

# 6. Engineering Principles

Project Orion follows several non-negotiable principles.

## Architecture First

Architecture always takes precedence over implementation speed.

---

## Deterministic Behaviour

Equal input always produces equal output.

No randomness may influence:

- analysis
- signals
- decisions
- portfolio
- risk
- trade planning

---

## Single Responsibility

Every module owns one clearly defined responsibility.

---

## Composition over Inheritance

Shared behaviour should be implemented through composition whenever practical.

---

## Presentation Only GUI

The GUI never performs:

- analysis
- signal generation
- decision making
- portfolio calculations
- risk calculations
- trade planning

---

## Explainability

AI explains deterministic outputs.

AI never generates deterministic outputs.

---

## Testability

Every reusable component should be independently testable.

Regression tests remain mandatory after every logical change.

---

# 7. Current Development Phase

Project Orion has completed its deterministic trading foundation.

Current focus is **Epic 2 – Professional Desktop Experience**.

Completed highlights:

- Workspace Framework
- WorkspaceController
- DashboardRouter
- BaseWorkspace
- WorkspacePanel
- Workspace migration
- Presenter migration (Phase 1)
- MainWindow simplification
- Composition-root architecture

Current work:

- GuiSection migration
- Presenter expansion
- Professional desktop UX

---

# 8. Development Workflow

Every implementation follows the same workflow.

1. Review the existing implementation.
2. Review the architecture.
3. Modify one logical responsibility.
4. Prefer complete file replacements.
5. Execute regression tests.
6. Synchronize documentation.
7. Commit.
8. Push.

Small verified improvements are preferred over speculative rewrites.

---

# 9. Coding Standards

General rules:

- Prefer readability over cleverness.
- Use explicit type hints.
- Keep responsibilities small.
- Avoid hidden behaviour.
- Preserve deterministic behaviour.
- Prefer composition.
- Keep orchestration free from business logic.
- Keep GUI presentation-only.

---

# 10. Documentation Rules

Documentation is part of the software.

Responsibilities:

**AI_CONTEXT.md**

- engineering context
- architecture overview
- engineering philosophy
- workflow

**CURRENT_STATE.md**

- current implementation snapshot

**PROJECT_STATUS.md**

- detailed implementation status

**CHANGELOG.md**

- historical changes

**TODO.md**

- upcoming work

**ORION_MASTER_ARCHITECTURE.md**

- long-term architecture

---

# 11. ChatGPT Development Workflow

Preferred collaboration:

1. Review existing code.
2. Never assume implementation exists.
3. Prefer complete file replacements.
4. One logical change at a time.
5. Execute regression tests.
6. Synchronize documentation.
7. Commit.
8. Push.

Large speculative repository-wide rewrites should be avoided.

---

# 12. Instructions for Future AI Sessions

Future AI assistants should treat Orion as a professional software product.

Always:

- review the repository first
- preserve deterministic architecture
- keep the GUI presentation-only
- prefer composition
- preserve existing engineering principles
- keep documentation synchronized
- provide complete file replacements whenever practical

Never:

- assume code exists
- invent architecture
- introduce business logic into the GUI
- claim tests passed without execution
- claim commits or pushes that have not occurred

The repository remains the single source of truth.

End of document.