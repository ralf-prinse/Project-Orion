# PROJECT ORION

# AI_CONTEXT.md

**Purpose:** Engineering Context
**Status:** Active Development
**Audience:** Developers, AI Assistants, Software Architects

---

# 1. Purpose

This document provides the engineering context required to continue development of Project Orion.

It is intentionally concise and focuses on the current architecture, engineering principles and development workflow.

Historical implementation details belong in `CHANGELOG.md`.

Long-term architectural decisions belong in `ORION_MASTER_ARCHITECTURE.md`.

Current progress belongs in `PROJECT_STATUS.md`.

---

# 2. Product Overview

Project Orion is a professional desktop application for deterministic swing-trading analysis of the United States stock market.

The objective is to analyse thousands of stocks through a transparent processing pipeline and identify high-quality trading opportunities.

Project Orion is **not** an automated trading bot.

It is a decision-support platform.

Artificial Intelligence is used only to explain deterministic results.

AI never:

- generates trading signals
- approves trades
- calculates risk
- sizes positions
- overrides deterministic engines

Every recommendation produced by Orion must be:

- deterministic
- reproducible
- explainable
- testable

---

# 3. Current Architecture

Project Orion follows a layered architecture.

```
Universe
    ↓
Market Data
    ↓
Historical Data
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
GUI
```

Each layer has exactly one responsibility.

Business logic never belongs in the GUI.

---

# 4. Core Infrastructure

Current shared infrastructure includes:

- AnalyzerRunner
- Registry Pattern
- ApplicationContainer
- ServiceRegistry
- Event Bus
- Scan Orchestrator
- Configuration Framework
- Explainability Framework
- WorkspaceController
- DashboardRouter
- Workspace Framework

These components form the architectural foundation of Orion.

Future functionality should reuse this infrastructure instead of introducing duplicate implementations.

---

# 5. Engineering Principles

Every contribution should follow these principles.

## Architecture First

Architecture takes priority over implementation speed.

Short-term convenience must never introduce long-term technical debt.

---

## Deterministic Behaviour

Identical input must always produce identical output.

Randomness must never influence:

- analysis
- signals
- decisions
- portfolio
- risk
- trade planning

---

## Single Responsibility

Every module performs one clearly defined responsibility.

---

## Registry-Driven Design

Expandable processing layers should use registries rather than large conditional statements.

---

## Composition over Inheritance

Shared behaviour should be implemented through composition whenever practical.

---

## Explainability

Every recommendation must be traceable.

AI explains decisions.

AI never creates decisions.

---

## Testability

All important infrastructure should be independently testable.

---

# 6. GUI Philosophy

The GUI is presentation-only.

It must never contain:

- indicator calculations
- analysis logic
- signal generation
- decision making
- portfolio calculations
- risk calculations

The GUI consumes View Models produced by deterministic services.

Presentation is completely separated from business logic.

---

# 7. Current Development Phase

Project Orion has completed the analytical foundation of the platform.

Current focus has shifted towards building a professional desktop application on top of the existing architecture.

Current priorities include:

- Professional Workspace Framework
- Dashboard architecture
- GUI Design System adoption
- Navigation architecture
- Desktop user experience

---

# 8. Development Workflow

Every task follows the same workflow.

1. Review existing implementation.
2. Review architecture.
3. Modify one file at a time.
4. Replace complete files instead of partial patches.
5. Execute regression tests.
6. Synchronize documentation.
7. Commit.
8. Push.

Small verified changes are preferred over large speculative refactors.

---

# 9. Coding Standards

General rules:

- Prefer readability over cleverness.
- Use explicit type hints.
- Keep modules small.
- Avoid hidden behaviour.
- Prefer composition.
- Keep orchestration free from business logic.
- Preserve deterministic behaviour.
- Write complete implementations rather than fragmented snippets.

---

# 10. Documentation Rules

Documentation is considered part of the software.

Responsibilities:

AI_CONTEXT.md

- engineering context
- architecture overview
- engineering philosophy
- workflow

PROJECT_STATUS.md

- current implementation status

CHANGELOG.md

- historical changes

TODO.md

- upcoming work

ORION_MASTER_ARCHITECTURE.md

- long-term architectural vision

---

# 11. Development Workflow with ChatGPT

Project Orion is developed through architecture-driven collaboration.

Preferred workflow:

1. Review the existing implementation.
2. Never assume code exists.
3. Modify one complete file at a time.
4. Provide complete file replacements rather than fragmented patches.
5. Execute regression tests.
6. Update documentation.
7. Commit.
8. Push.

Large repository-wide speculative changes are avoided.

---

# 12. Instructions for Future AI Sessions

Future AI assistants should treat Orion as a professional software product.

Always:

- prefer complete file replacements
- review the existing implementation before proposing changes
- keep GUI presentation-only
- preserve deterministic architecture
- avoid speculative refactoring
- synchronize documentation before committing

Never assume code exists unless it is present in the current repository.

Never claim patches, commits or successful test executions that have not actually been performed.

The repository is the single source of truth.

This document should provide sufficient context for any future development session.