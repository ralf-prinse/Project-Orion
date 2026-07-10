# PROJECT ORION

# PROJECT_STATUS

**Purpose:** Current Implementation Status  
**Status:** Active Development  
**Current Sprint:** Sprint 8.9 – Persistent Position Lifecycle

---

# Executive Summary

Project Orion is a deterministic autonomous paper-trading platform.

The complete active lifecycle now persists not only the portfolio, but also the risk and management state required to continue open positions correctly across runner iterations and application restarts.

```text
Market Scan
    ↓
Trading Pipeline
    ↓
Adaptive RiskPlan
    ↓
Portfolio Allocation
    ↓
Paper BUY
    ↓
TradingSession Persistence
    ↓
Portfolio and Position Lifecycle Update
    ↓
Break-even and Trailing Stop
    ↓
Position Monitor
    ↓
Exit Engine and Paper SELL
    ↓
Trade Journal
    ↓
Dashboard and Closed-Trade Analytics
```

The primary remaining lifecycle gap is that exit evaluation still uses the simple fixed-percentage `PositionMonitor` rather than the complete persisted `PositionState` and `RiskPlan`.

---

# Current Status

| Area | Status |
|------|--------|
| Market data and scanning | ✅ Complete |
| Deterministic Trading Pipeline | ✅ Complete |
| Adaptive Risk Engine | ✅ Complete |
| Portfolio allocation | ✅ Complete |
| Paper execution | ✅ Complete |
| Continuous autonomous runner | ✅ Complete |
| Paper portfolio persistence | ✅ Complete |
| Complete TradingSession persistence | ✅ Complete |
| PositionState persistence | ✅ Complete |
| RiskPlan persistence | ✅ Complete |
| Portfolio revaluation | ✅ Complete |
| Break-even lifecycle update | ✅ Integrated |
| Trailing-stop lifecycle update | ✅ Integrated |
| Fixed-rule PositionMonitor | ✅ Operational |
| Lifecycle-aware exit evaluation | 🚧 Next |
| Exit Engine | ✅ Complete |
| Trade Journal | ✅ Complete |
| Dashboard Service | ✅ Complete |
| CLI Dashboard | ✅ Complete |
| Closed Trade Analytics | ✅ Complete |
| Dashboard GUI foundation | ✅ Foundation only |
| Broker integration | ❌ Not started |
| Real-money execution | ❌ Not started |

---

# Active Runtime State

## TradingSession

The complete runtime state consists of:

```text
TradingSession
    ├── PaperPortfolio
    ├── dict[str, PositionState]
    ├── dict[str, RiskPlan]
    ├── name
    └── status
```

It is persisted through:

```text
TradingSessionRepository
└── JsonTradingSessionRepository
```

Default storage target:

```text
data/trading_session.json
```

The runner still supports `PaperPortfolioRepository` during migration for backward compatibility.

---

# Completed Systems

## Trading Core

Implemented:

- market universes and market-data providers;
- deterministic indicators and analysis;
- signal generation;
- deterministic BUY/HOLD/SELL decisions;
- confidence and scoring;
- adaptive risk planning;
- portfolio validation and allocation;
- trade planning;
- AI explanation of deterministic output.

AI does not own trading calculations or decisions.

## Paper Execution

Implemented:

- execution validation;
- order creation;
- paper broker execution;
- portfolio mutation through `PortfolioManager`;
- execution reporting;
- paper BUY and SELL lifecycle;
- autonomous and continuous runners.

## Persistent Position Lifecycle

Implemented and validated:

- full `TradingSession` JSON roundtrip;
- recovery of portfolio, position state and risk plans;
- preservation of lifecycle state during portfolio price updates;
- use of `PaperPositionUpdateService` inside the autonomous runner;
- highest-price tracking;
- break-even activation;
- trailing-stop activation and updates;
- target-hit state persistence;
- removal of lifecycle state after a position is closed;
- legacy fallback revaluation for positions without lifecycle state.

## Journal and Analytics

Implemented:

- JSONL trade-journal repository;
- BUY, rejected decision and CLOSE_POSITION entries;
- realized and unrealized P/L summaries;
- winrate;
- average winner and loser;
- profit factor;
- largest winner and loser;
- recent real trade filtering.

## Dashboard

Implemented:

- `DashboardService` and snapshot models;
- `run_dashboard.py`;
- cash, equity, open/closed/total P/L;
- return percentage and winrate;
- open positions with unrealized return;
- recent OPEN_POSITION/CLOSE_POSITION events;
- closed-trade analytics;
- CLI presenter;
- GUI presenter, workspace, controller and desktop-bootstrap foundation.

The GUI foundation is not the current development priority. The engine remains authoritative.

---

# Validation Status

Official command:

```powershell
python run_tests.py
```

Current expected result:

```text
69 passed
```

Latest validated additions:

| Component | Status |
|-----------|--------|
| JSON TradingSession Repository | ✅ Passing |
| Complete session roundtrip | ✅ Passing |
| Autonomous session recovery | ✅ Passing |
| Autonomous session persistence | ✅ Passing |
| Position lifecycle update | ✅ Passing |
| Break-even update | ✅ Passing |
| Trailing-stop update | ✅ Passing |
| Persistent lifecycle recovery | ✅ Passing |
| Backward-compatible portfolio persistence | ✅ Passing |

Manual validation also confirmed the CLI dashboard against live paper runtime files.

---

# Current Sprint

## Sprint 8.9 – Persistent Position Lifecycle

Status:

```text
IN PROGRESS
```

Completed:

1. repository contract for complete TradingSession persistence;
2. JSON implementation;
3. save/load regression coverage;
4. autonomous runner integration;
5. state preservation across revaluation;
6. position update engine integration;
7. break-even and trailing-stop persistence;
8. regression suite expanded to 69 passing tests.

Next implementation step:

```text
Integrate lifecycle-aware exit evaluation using PositionState and RiskPlan.
```

The fixed-percentage `PositionMonitor` remains operational as a compatibility fallback until the new exit path is fully validated.

---

# Known Limitations

- Exit evaluation still primarily uses fixed percentages from `LivePaperTradingConfig`.
- Maximum holding-time evaluation is not yet fully connected to persisted lifecycle timestamps.
- Decision events and true trade events still share one JSONL journal.
- The legacy desktop flow still uses separate `portfolio.json`, `open_trades.json` and `trade_history.json` storage.
- The new GUI foundation is not yet the primary application entrypoint.
- No broker integration or real-money execution exists.
- Historical runtime files are not automatically migrated into `TradingSession`.

---

# Project Direction

The immediate objective is not to add new engines. It is to finish and consolidate the existing deterministic lifecycle.

Priority order:

1. lifecycle-aware exit evaluation;
2. time-stop persistence and evaluation;
3. long-running restart validation with `trading_session.json`;
4. decision-log separation;
5. engine consolidation and legacy mapping;
6. performance and expectancy analytics;
7. only then broader GUI and self-learning work.

---

# End of PROJECT_STATUS
