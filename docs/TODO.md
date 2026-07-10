# PROJECT ORION

# TODO

**Purpose:** Active Development Backlog  
**Status:** Sprint 8.9

---

# Current Sprint

## Sprint 8.9 – Persistent Position Lifecycle

Status:

```text
IN PROGRESS
```

Objective:

Ensure that every open position retains and uses its deterministic RiskPlan and PositionState throughout continuous execution and application restarts.

---

# Completed in Sprint 8.9

- [x] Add `TradingSessionRepository` contract.
- [x] Add `JsonTradingSessionRepository`.
- [x] Persist `PaperPortfolio`, `PositionState` and `RiskPlan` together.
- [x] Add missing-file and save/load regression coverage.
- [x] Load complete sessions in `AutonomousPaperTradingRunner`.
- [x] Save complete sessions after successful cycles.
- [x] Preserve state through revaluation.
- [x] Remove state and risk plan after executed exits.
- [x] Integrate `PaperPositionUpdateService` into autonomous iterations.
- [x] Persist highest price, break-even and trailing-stop changes.
- [x] Keep portfolio-only persistence as a migration fallback.
- [x] Expand the official suite to 69 passing tests.

---

# Highest Priority

## 1. Lifecycle-aware Exit Evaluation

Status:

```text
NEXT
```

Replace the primary fixed-percentage exit evaluation for fully managed positions with evaluation based on:

- persisted `PositionState.current_stop_loss`;
- persisted `RiskPlan.target_1`;
- persisted `RiskPlan.target_2`;
- persisted `RiskPlan.target_3`;
- target-hit state;
- break-even state;
- trailing-stop state;
- deterministic exit reasons.

Requirements:

- reuse existing exit and position-management services;
- no duplicate optimizer;
- no AI decisions;
- fixed `PositionMonitor` retained only as a legacy fallback during migration;
- remove `PositionState` and `RiskPlan` only after successful close;
- add regressions for target exit and dynamic stop exit.

## 2. Persistent Time Stop

Connect existing time-stop logic to persisted position lifecycle data.

Requirements:

- deterministic holding-time calculation;
- restart-safe opening timestamp or equivalent persisted state;
- maximum holding-time exit reason;
- regression across save/load.

## 3. Runtime Migration and Validation

- configure continuous runner to use `data/trading_session.json` by default;
- define safe migration from existing `data/paper_portfolio.json`;
- run multi-iteration validation;
- restart runner and verify restored stop/high/target states;
- verify CLOSE_POSITION entries and realized P/L.

---

# Medium Priority

## Decision Log Separation

Separate actual trade events from rejected decisions.

```text
trade_journal.jsonl
    OPEN_POSITION
    CLOSE_POSITION

decision_log.jsonl
    REJECTED
    insufficient cash
    duplicate position
    confidence failure
    validation failure
```

## Engine Consolidation

Document and classify parallel implementations.

Focus areas:

- active autonomous runtime;
- analyzer/registry engines;
- older `engines/` modules;
- legacy manual GUI stores;
- duplicate decision and portfolio services.

Do not delete components solely because similarly named alternatives exist. Confirm entrypoint usage and regression ownership first.

## Performance Analytics Expansion

Add:

- expectancy;
- average holding time;
- exit-reason distribution;
- target-hit rates;
- stop-loss versus trailing-stop outcomes;
- equity curve from actual journal events.

---

# GUI Backlog

The GUI is intentionally lower priority than the engine.

Existing foundation:

- dashboard GUI presenter;
- dashboard workspace;
- dashboard controller;
- desktop bootstrap;
- early Live Desk components.

Future direction:

- one read-only live desk;
- minimal navigation;
- current portfolio and lifecycle state;
- recent trades and alerts;
- no GUI business logic.

Do not expand the GUI until the persistent exit lifecycle is stable.

---

# Long-Term Roadmap

## Self-learning Analytics

Analyse historical deterministic outcomes and propose configuration changes.

Allowed:

- compare strategies;
- score hypotheses;
- propose configuration variants;
- explain performance.

Not allowed:

- direct AI BUY/SELL decisions;
- nondeterministic trade execution;
- silent configuration mutation.

## Broker Integration

Only after:

- stable persistent lifecycle;
- validated exits;
- reliable trade-event journal;
- positive long-running paper results;
- complete risk controls.

## Live Trading

Real-money execution remains out of scope until paper trading has passed extensive operational validation.

---

# Development Rules

Every completed feature must include:

1. complete relevant-runtime analysis;
2. ownership and architecture review;
3. regression test first where practical;
4. implementation using existing owners;
5. targeted tests;
6. full `python run_tests.py` validation;
7. manual runtime validation where applicable;
8. documentation synchronization;
9. commit and push.

Prefer complete-file replacements over fragmented edits.

---

# End of TODO
