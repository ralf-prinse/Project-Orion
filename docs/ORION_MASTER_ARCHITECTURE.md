# PROJECT ORION — MASTER ARCHITECTURE

**Status:** Stable deterministic architecture  
**Updated:** 2026-07-14

---

# Mission

Project Orion is a deterministic swing-trading platform.

Artificial Intelligence may explain deterministic output but never owns trading decisions, risk, execution or position management.

---

# Core Trading Flow

```text
Market Data
    ↓
Quote Validation
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
Execution Engine
    ↓
TradingSession
    ↓
Position Management
    ↓
Exit Engine
    ↓
Trade Journal
```

Every layer has exactly one responsibility.

No layer may bypass another.

---

# Canonical Runtime Aggregate

```text
TradingSession
├── PaperPortfolio
├── dict[str, PositionState]
├── dict[str, RiskPlan]
├── session metadata
└── runtime status
```

Rules:

- TradingSession is the only lifecycle owner.
- PositionState exists only inside TradingSession.
- RiskPlan exists only inside TradingSession.
- No parallel lifecycle state is allowed.

---

# Persistence Boundary

```text
TradingSessionRepository
        ↓
TradingSession
```

Repositories only serialize.

Repositories never calculate:

- indicators;
- decisions;
- risk;
- exits;
- position management.

---

# Execution

Execution is intentionally separated.

```text
ExecutionEngine
        ↓
Broker.execute(order)
```

Current implementation:

```text
PaperBroker
```

Planned implementation:

```text
IbkrBroker
```

ExecutionEngine must remain broker-independent.

---

# Position Management

Canonical flow:

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

Lifecycle ownership includes:

- current price;
- highest price;
- stop loss;
- break-even state;
- trailing stop;
- target flags;
- deterministic exits.

---

# Runtime

Runtime orchestration:

```text
ContinuousPaperTradingRunner
        ↓
RuntimeSupervisor
        ↓
AutonomousPaperTradingRunner
        ↓
TradingSessionRepository
```

Responsibilities:

RuntimeSupervisor

- runtime health;
- runtime events;
- heartbeat;
- failures;
- graceful shutdown.

RuntimeSupervisor never owns trading state.

---

# Market Sessions

Trading only occurs while configured markets are open.

Market sessions are:

- timezone-aware;
- DST-aware;
- deterministic.

When every configured market is closed:

```text
MARKETS_IDLE
```

During idle:

- no scans;
- no orders;
- no portfolio updates;
- no failed iterations.

---

# Quote Validation

Every market price must satisfy:

- finite;
- greater than zero;
- not NaN;
- not None.

Invalid quotes are rejected before entering the trading pipeline.

Portfolio equity may never become NaN.

---

# Journals

Independent journals exist for:

Trade Journal

- OPEN_POSITION
- CLOSE_POSITION

Decision Journal

- APPROVED
- REJECTED

Runtime Events

- runtime lifecycle
- failures
- idle transitions

Journals are immutable runtime evidence.

---

# Artificial Intelligence

Allowed:

- explanations;
- summaries;
- documentation;
- historical analysis.

Forbidden:

- BUY decisions;
- SELL decisions;
- EXIT decisions;
- position sizing;
- stop calculation;
- order execution;
- configuration changes.

---

# Architectural Rules

Always:

- one owner per responsibility;
- deterministic behaviour;
- explicit dependencies;
- composition over inheritance;
- immutable models where practical;
- complete regression coverage;
- architecture review before implementation.

Never:

- duplicate trading logic;
- duplicate lifecycle state;
- bypass TradingSession;
- bypass Quote Validation;
- bypass ExecutionEngine.

---

# Current Validation Baseline

Regression:

```text
75 passed
0 failed
```

Operational validation:

- continuous runtime;
- restart recovery;
- market-session transitions;
- runtime idle;
- quote validation;
- managed exits;
- persistence.

---

# Next Architectural Milestone

Interactive Brokers Paper integration.

Only the broker implementation changes.

The deterministic trading engine remains unchanged.

```text
ExecutionEngine
        ↓
IbkrBroker
        ↓
IBKR Paper
```

This preserves every deterministic layer while replacing only the execution backend.

# End