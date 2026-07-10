# PROJECT ORION

# AI_CONTEXT

**Purpose:** Engineering Context  
**Status:** Active Development

---

# Documentation Information

| Item | Value |
|------|-------|
| Project | Orion |
| Development Phase | Persistent Autonomous Paper Trading |
| Current Sprint | Sprint 8.9 – Persistent Position Lifecycle |
| Architecture | Deterministic, service-oriented |
| Latest Validation | 69 regression tests passing |
| Active Branch | `feature/trading-dashboard` |

---

# Purpose

This document provides the minimum context required to continue development of Project Orion.

- Implementation history belongs in `CHANGELOG.md`.
- Current implementation status belongs in `PROJECT_STATUS.md`.
- Upcoming work belongs in `TODO.md`.
- Permanent architectural rules belong in `ORION_MASTER_ARCHITECTURE.md`.

---

# Current Project State

Project Orion has a complete deterministic autonomous paper-trading lifecycle with persistent portfolio, risk-plan and position-management state.

Implemented and validated systems include:

- deterministic Trading Pipeline;
- adaptive Risk Engine and RiskPlan generation;
- portfolio allocation;
- paper BUY and SELL execution;
- continuous autonomous runner;
- complete TradingSession persistence;
- portfolio revaluation;
- persistent PositionState and RiskPlan recovery;
- break-even and trailing-stop lifecycle updates;
- position monitoring and exit execution;
- JSONL trade journal;
- dashboard service;
- CLI trading dashboard;
- closed-trade analytics;
- dashboard GUI foundation.

The current priority is to complete lifecycle-aware exit evaluation and consolidate the active runtime around the persisted TradingSession.

---

# Active Runtime Flow

```text
Market Data
      ↓
Indicators and Analysis
      ↓
Signals
      ↓
Deterministic Decision
      ↓
Adaptive RiskPlan
      ↓
Portfolio Allocation
      ↓
Paper Execution
      ↓
TradingSession
      ├── PaperPortfolio
      ├── PositionState
      └── RiskPlan
      ↓
Persistent Session Repository
      ↓
Position Lifecycle Update
      ├── Break-even
      └── Trailing stop
      ↓
Exit Evaluation
      ↓
Exit Engine
      ↓
Trade Journal
      ↓
Dashboard and Analytics
```

---

# Sources of Truth

The active autonomous lifecycle uses:

```text
data/trading_session.json
data/trade_journal.jsonl
```

During migration, `data/paper_portfolio.json` remains supported for backward compatibility.

Older desktop runtime files such as `data/open_trades.json`, `data/trade_history.json` and `data/portfolio.json` belong to a legacy GUI flow and must not become dependencies of new autonomous functionality.

Runtime data files are local artifacts and are normally not committed.

---

# Architecture Principles

## Deterministic Backend

All trading decisions and lifecycle updates are deterministic.

Identical inputs must produce identical outputs. Randomness is prohibited in trading logic.

## Separation of Responsibilities

- Services own business logic.
- Runners and controllers orchestrate.
- Repositories load and persist state.
- Presenters format data.
- Widgets display prepared information only.
- GUI code never owns trading logic.

## Artificial Intelligence

AI may explain, summarize, compare and assist documentation.

AI may never generate or override BUY/SELL decisions, confidence, risk, position sizing, exit thresholds or deterministic calculations.

## Existing Architecture First

Before implementing a feature:

1. inspect the complete relevant runtime chain;
2. locate existing services and models;
3. avoid parallel implementations;
4. extend the existing owner of the responsibility;
5. add regression coverage before integration.

---

# Current Development Focus

Sprint 8.9 focuses on the persistent position lifecycle.

Completed in this sprint:

- `TradingSessionRepository` contract;
- `JsonTradingSessionRepository`;
- complete session save/load roundtrip;
- autonomous runner support for complete session persistence;
- preservation of `PositionState` and `RiskPlan` across iterations and restarts;
- integration of `PaperPositionUpdateService` into the autonomous runner;
- persistent break-even and trailing-stop updates;
- backward compatibility with portfolio-only persistence;
- regressions expanded to 69 passing tests.

Next logical step:

```text
Make exit evaluation consume the persisted PositionState and RiskPlan,
then reduce the fixed-percentage PositionMonitor to a legacy fallback.
```

---

# Validation

Official regression command:

```powershell
python run_tests.py
```

Current expected result:

```text
69 passed
```

Key targeted validations:

```powershell
python test_json_trading_session_repository.py
python test_autonomous_paper_trading_runner_persistence.py
python test_autonomous_position_lifecycle.py
python run_dashboard.py
```

---

# Instructions for Future AI Sessions

Before writing code:

1. read all five official project documents;
2. inspect the complete relevant source and test chain;
3. identify the active runtime and any legacy alternatives;
4. determine the single owner of the requested responsibility;
5. propose one stable implementation plan;
6. prefer complete-file replacements;
7. add or update regression tests;
8. run `python run_tests.py`;
9. update documentation only after the sprint is actually complete.

Never assume a class is the active implementation merely because it exists.

Preserve deterministic behaviour and backward compatibility unless a deliberate migration removes it.

---

# End of AI_CONTEXT
