# PROJECT ORION

# CHANGELOG

**Purpose:** Historical Development Log

---

# Sprint 8.9 — Persistent Position Lifecycle

**Status:** In Progress

### Added

- `TradingSessionRepository` abstraction.
- `JsonTradingSessionRepository` implementation.
- Complete TradingSession JSON persistence.
- Regression coverage for session roundtrip and missing-session behaviour.
- Autonomous runner support for `TradingSessionRepository`.
- Autonomous position-lifecycle integration test.

### Improved

- `AutonomousPaperTradingRunner` now loads and saves complete sessions.
- `PositionState` and `RiskPlan` survive continuous iterations and restarts.
- Portfolio revaluation preserves lifecycle dictionaries.
- Executed exits remove matching lifecycle state and risk plans.
- `PaperPositionUpdateService` is now used during autonomous price updates.
- Existing break-even and trailing-stop services now update persistent state.
- Highest price, current stop, target-hit and activation flags persist.
- Portfolio-only repository support remains available during migration.

### Validation

- Complete TradingSession save/load roundtrip validated.
- Autonomous session recovery and persistence validated.
- Break-even activation validated.
- Trailing-stop activation and update validated.
- Persistent lifecycle recovery validated.
- 69 regression tests passing.

---

# Sprint 8.8 — Dashboard GUI Foundation

**Status:** Foundation Complete; Further GUI Work Deferred

### Added

- Trading dashboard GUI presenter.
- Trading dashboard workspace.
- Trading dashboard controller.
- Desktop bootstrap foundation.
- Initial modular Live Desk package and reusable metric components.
- GUI presenter, controller and bootstrap regressions.

### Decision

Further GUI expansion was deprioritized in favour of completing the persistent trading engine lifecycle.

---

# Sprint 8.7 — Closed Trade Analytics

**Status:** Complete

### Added

- `ClosedTradeStatistics` model.
- `ClosedTradeAnalyticsService`.
- Average winner and average loser.
- Profit factor.
- Largest winner and largest loser.
- Dashboard integration and CLI presentation.

### Validation

- Empty-history and populated-history analytics validated.
- Dashboard service and CLI presenter regressions updated.

---

# Sprint 8.6 — Dashboard & Trading Analytics

**Status:** Complete

### Added

- `DashboardService` and dashboard snapshot models.
- `run_dashboard.py` live CLI dashboard.
- Trading dashboard CLI presenter.
- Cash, equity, open/closed/total P/L and return display.
- Open-position overview with unrealized return percentage.
- Recent OPEN_POSITION/CLOSE_POSITION filtering.
- Dashboard regressions.

### Improved

- Dashboard reads the official paper portfolio and JSONL trade journal.
- Rejected decision entries are excluded from the Recent Trades view.

---

# Sprint 8.5 — Autonomous Paper Trading

**Status:** Complete

### Added

- Continuous autonomous paper trading runner.
- PositionMonitor.
- ExitEngine.
- PortfolioRevaluationService.
- Runtime portfolio persistence.
- Runtime JSONL trade journal.
- CLOSE_POSITION journal entries.
- Trade journal builder and repository.

### Validation

Multi-hour autonomous runtime confirmed stable scanning, BUY/SELL execution, portfolio persistence and journal generation.

---

# Sprint 8.4 — Deterministic Trading Pipeline

**Status:** Complete

### Added

- TradingPipeline.
- Signal, decision and risk layers.
- Portfolio allocation.
- Trade planning.
- AI explanation layer.

### Improved

- Deterministic architecture.
- Strict separation between AI and business logic.

---

# Earlier Sprints

## Sprint 8.3

- Market scanner.
- Indicator engine.
- Analysis engine.
- Signal generation.

## Sprint 8.2

- Portfolio, risk and trading models.
- Persistence foundations.

## Sprint 8.1

- Initial Orion architecture.
- Project structure.
- Dependency injection.
- Core services.
- Regression framework.

---

# Documentation Policy

- Current implementation: `PROJECT_STATUS.md`
- Current priorities: `TODO.md`
- Long-term architecture: `ORION_MASTER_ARCHITECTURE.md`
- New-session context: `AI_CONTEXT.md`

---

# End of CHANGELOG
