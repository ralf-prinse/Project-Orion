# PROJECT ORION — MASTER ARCHITECTURE

**Status:** Stable engine architecture  
**Updated:** 2026-07-11

## Mission

Project Orion is a deterministic AI-assisted trading platform.

AI explains deterministic output. It never creates or overrides trading decisions, confidence, risk plans, position size or exits.

## Core Flow

```text
Market Data
    ↓
Indicators
    ↓
Analysis
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
    ↓
Position Management
    ↓
Exit Evaluation
    ↓
ExitEngine
    ↓
Trade Journal / Decision Journal
    ↓
Dashboard and Analytics
```

## Canonical Runtime Aggregate

```text
TradingSession
├── PaperPortfolio
├── dict[str, PositionState]
├── dict[str, RiskPlan]
├── name
└── status
```

Rules:

- `TradingSession` is the only lifecycle-state owner.
- `PaperPortfolio` owns cash and positions inside the aggregate.
- `PositionState` owns current managed-position state.
- `RiskPlan` owns deterministic entry risk and targets.
- no parallel in-memory state store is permitted.

## Persistence Boundary

```text
TradingSessionRepository
        ↓
TradingSession
```

Repositories only serialize and retrieve state. They never calculate decisions, stops, targets or P/L.

`JsonPaperPortfolioRepository` may exist only as an explicit compatibility mirror. It is not authoritative lifecycle state.

## Position Management

Canonical chain:

```text
PaperPositionUpdateService
        ↓
PositionUpdateEngine
        ↓
BreakEvenService
TrailingStopService
TimeStopService
        ↓
PositionMonitor
        ↓
ExitEngine
```

Responsibilities:

- update current and highest prices;
- maintain dynamic stop state;
- record targets and activation flags;
- evaluate deterministic exits;
- close positions;
- remove matching state and risk plans.

## Runtime Orchestration

```text
ContinuousPaperTradingRunner
        ↓
AutonomousPaperTradingRunner
        ↓
TradingSessionRepository
```

Runners orchestrate only. They do not duplicate lifecycle calculations.

## Journaling

```text
Trade Journal
- OPEN_POSITION
- CLOSE_POSITION

Decision Journal
- APPROVED
- REJECTED
```

Both journals may share a model and repository implementation, but their files and semantics remain separate.

## Layer Rules

- Market providers supply raw data.
- Indicators calculate values.
- Analysis interprets indicators.
- Signals describe conditions.
- Decision logic produces BUY/HOLD/SELL.
- Risk validates and plans.
- Execution mutates paper state.
- Position management owns open-position lifecycle.
- Repositories persist.
- Presenters format.
- GUI displays only.

No layer may bypass or duplicate another owner's responsibility.

## Design Principles

- deterministic behaviour;
- one owner per responsibility;
- explicit dependencies;
- composition over inheritance;
- immutable models where practical;
- no hidden global state;
- complete regression coverage for architectural changes;
- architecture analysis before implementation.

## Artificial Intelligence

Allowed:

- explanation;
- summarization;
- comparison;
- documentation;
- analysis of deterministic historical outcomes.

Forbidden:

- BUY/SELL/EXIT decisions;
- confidence calculation;
- position sizing;
- risk approval;
- stop or target calculation;
- direct execution;
- silent configuration changes.

## Validation Policy

Before merge or release:

```powershell
python run_tests.py
```

Expected current baseline:

```text
69 passed
```

Runtime-sensitive changes also require isolated smoke or duration validation.

## Future Expansion

New platform features must build on this engine without changing ownership:

- dashboard;
- analytics;
- alerts;
- broker compatibility;
- strategy comparison;
- multi-market support.

# End
