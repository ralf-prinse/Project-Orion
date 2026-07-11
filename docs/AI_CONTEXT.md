# PROJECT ORION — AI CONTEXT

**Status:** Engine consolidation complete  
**Active branch:** `sprint-8.13-position-state-store-removal`  
**Validation:** `69 passed`  
**Updated:** 2026-07-11

## Purpose

This is the first document to read in a new development chat. It provides the minimum context needed to continue safely.

Use together with:

- `ORION_MASTER_ARCHITECTURE.md`
- `PROJECT_STATUS.md`
- `TODO.md`
- `CHANGELOG.md`

## Current State

Project Orion has a deterministic, restart-safe autonomous paper-trading engine.

Completed and validated:

- deterministic market scan and Trading Pipeline;
- adaptive `RiskPlan`;
- portfolio allocation and paper execution;
- complete `TradingSession` persistence;
- managed `PositionState` lifecycle;
- break-even, trailing-stop and lifecycle-aware exits;
- restart exit recovery;
- crash recovery;
- session-integrity validation;
- continuous runner heartbeat and graceful shutdown;
- separate trade and decision journals;
- 100-iteration operational validation;
- removal of the legacy `PositionStateStore`.

## Runtime Source of Truth

```text
TradingSession
├── PaperPortfolio
├── dict[str, PositionState]
└── dict[str, RiskPlan]
```

`TradingSessionRepository` is the canonical persistence boundary.

No service may introduce a second runtime-state owner.

## Active Runtime

```text
ContinuousPaperTradingRunner
        ↓
AutonomousPaperTradingRunner
        ↓
TradingSessionRepository
        ↓
TradingSession
        ↓
PaperPositionUpdateService
        ↓
PositionUpdateEngine
        ↓
BreakEvenService / TrailingStopService / TimeStopService
        ↓
PositionMonitor
        ↓
ExitEngine
```

## Journals

```text
trade_journal.jsonl
- OPEN_POSITION
- CLOSE_POSITION

decision_journal.jsonl
- APPROVED
- REJECTED
```

Both use the existing `TradeJournalEntry` model and JSONL repository.

## Non-Negotiable Rules

1. Analyse the complete relevant runtime chain before changing code.
2. Do not create duplicate models, engines or services.
3. `TradingSession` remains the only lifecycle-state owner.
4. Trading logic stays deterministic.
5. AI may explain but never decide, size, approve or exit trades.
6. GUI code remains presentation-only.
7. Prefer complete-file replacements.
8. Run targeted tests and then `python run_tests.py`.
9. Commit and push only after all tests pass.

## Current Branch Work

Sprint 8.13 removed `PositionStateStore` and consolidated lifecycle ownership in `TradingSession`.

Before starting new functionality:

```powershell
git status
python run_tests.py
```

Expected:

```text
nothing to commit, working tree clean
69 passed
```

## Recommended Next Step

Perform the Engine 1.0 review and freeze:

- verify no remaining duplicate runtime ownership;
- review remaining compatibility repositories;
- confirm documentation and test runner alignment;
- tag the stable engine baseline;
- then begin Sprint 9.0 platform/dashboard work.

## New Chat Opening Instruction

A future chat must first:

1. inspect this branch;
2. read every file in `docs/`;
3. confirm the runtime chain;
4. confirm `69 passed`;
5. propose the next step before writing code.

# End
