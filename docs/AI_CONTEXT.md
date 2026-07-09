# PROJECT ORION

# AI_CONTEXT

**Purpose:** Engineering Context  
**Status:** Active Development

---

# Documentation Information

| Item | Value |
|------|-------|
| Project | Orion |
| Development Phase | Autonomous Paper Trading |
| Current Sprint | Sprint 8.6 – Dashboard & Trading Analytics |
| Architecture | Deterministic |
| Latest Validation | 64 regression tests passing |

---

# Purpose

This document provides the minimum context required to continue development of Project Orion.

Detailed implementation history belongs in `CHANGELOG.md`.

Current implementation status belongs in `PROJECT_STATUS.md`.

Long-term architectural decisions belong in `ORION_MASTER_ARCHITECTURE.md`.

---

# Current Project State

Project Orion has completed its deterministic trading foundation.

Implemented systems include:

- Deterministic Trading Pipeline
- Portfolio Engine
- Risk Engine
- Trade Planner
- Paper Trading Engine
- Continuous Autonomous Runner
- Position Monitor
- Exit Engine
- Portfolio Revaluation
- Trade Journal
- Dashboard Service

The platform is now transitioning from feature implementation towards trading analytics, optimisation and professional monitoring.

---

# Current Trading Stack

```
Market Data
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
Risk Engine
      ↓
Trade Planner
      ↓
Paper Trading
      ↓
Position Monitor
      ↓
Exit Engine
      ↓
Trade Journal
      ↓
Dashboard
```

Every layer has exactly one responsibility.

---

# Architecture Principles

The following principles are non-negotiable.

## Deterministic Backend

All trading decisions are deterministic.

Identical market data must always produce identical output.

---

## Separation of Responsibilities

Business logic exists only inside backend services.

The GUI is presentation only.

Controllers orchestrate.

Presenters transform data.

Widgets never contain business logic.

---

## Artificial Intelligence

AI may:

- explain
- summarize
- compare
- generate natural language

AI may never:

- generate BUY decisions
- generate SELL decisions
- calculate indicators
- calculate confidence
- calculate risk
- calculate position sizing
- override deterministic output

---

# Current Development Focus

Current priorities are:

1. Trading Dashboard
2. Closed Trade Analytics
3. Adaptive Exit Optimisation
4. Self-learning performance analysis

Future development should improve trading quality rather than expanding the deterministic architecture.

---

# Development Workflow

Every completed feature follows exactly the same workflow.

1. Review existing implementation.
2. Design architecture.
3. Implement one complete feature.
4. Execute regression tests.
5. Validate behaviour manually.
6. Synchronize documentation.
7. Commit.
8. Push to GitHub.

No sprint is complete until all steps have been completed.

---

# Validation

Official regression command:

```powershell
python run_tests.py
```

Current expected result:

```
64 passed
```

Regression tests must pass before documentation is updated.

---

# Documentation Responsibilities

Each document has a single responsibility.

| Document | Responsibility |
|-----------|----------------|
| ORION_MASTER_ARCHITECTURE.md | Long-term architecture |
| PROJECT_STATUS.md | Current implementation status |
| TODO.md | Upcoming work |
| CHANGELOG.md | Historical implementation log |
| AI_CONTEXT.md | Development context for new sessions |

Architectural information must never be duplicated outside the Master Architecture.

---

# Instructions for Future AI Sessions

Before writing code:

1. Read all documentation.
2. Analyse the complete source tree.
3. Determine:
   - current architecture
   - current sprint
   - completed work
   - work in progress
   - next logical implementation step

Only then may implementation begin.

Never assume functionality exists.

Prefer complete file replacements over fragmented snippets.

Preserve deterministic behaviour.

Respect the existing architecture.

Update documentation after every completed sprint.

---

# End of AI_CONTEXT