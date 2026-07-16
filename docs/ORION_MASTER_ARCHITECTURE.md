# PROJECT ORION — MASTER ARCHITECTURE

**Architecture Version:** Sprint 11 Baseline

**Status:** Active

**Regression Baseline:** 88 / 88 Passed

**Last Updated:** 2026-07-16

---

# Philosophy

Project Orion is a deterministic autonomous trading platform.

Artificial Intelligence assists the system by generating market intelligence and confidence scores.

Artificial Intelligence never bypasses deterministic trading rules.

Every trade must remain reproducible.

---

# Core Architecture

Market Data

↓

Scanner

↓

Trading Pipeline

↓

Portfolio Allocator

↓

Execution Engine

↓

Broker

↓

Broker Truth Synchronization

↓

Trading Session

↓

Persistence

↓

Analytics

↓

Learning

No component may skip a layer.

---

# Runtime Ownership

The TradingSession is the single runtime authority.

TradingSession owns:

- PaperPortfolio
- PositionState
- RiskPlan
- Runtime metadata

No duplicated portfolio state may exist outside TradingSession.

Repositories are persistence only.

---

# Trading Pipeline

Responsibilities:

- market analysis
- indicator generation
- market intelligence
- signal fusion
- confidence calculation
- position sizing recommendation

Output:

TradingDecision

The pipeline never communicates directly with the broker.

---

# Portfolio Allocator

Responsibilities:

- capital allocation
- exposure limits
- duplicate position prevention
- portfolio constraints

Output:

Approved trading decisions.

No broker interaction.

---

# Execution Engine

Responsibilities:

- validate execution request
- build execution context
- select broker
- execute order

ExecutionEngine contains no broker-specific implementation.

---

# Broker Layer

Current implementation:

- PaperBroker
- IbkrBroker

Both implement the same execution interface.

Responsibilities:

- translate execution requests
- submit orders
- return deterministic execution results

---

# Interactive Brokers Layer

Components:

IbkrAccountService

↓

IbkrPortfolioService

↓

IbkrExecutionService

↓

IbkrBroker

↓

IbkrOrderTransport

Responsibilities:

- account access
- portfolio access
- order transport
- execution
- reconciliation

Broker state is always considered authoritative.

---

# Broker Truth Synchronization

TradingSession never assumes a broker order succeeded.

After execution:

Broker

↓

TradingSessionSyncService

↓

TradingSession

↓

Persistence

Local portfolio state is always replaced by broker truth.

This prevents:

- stale positions
- duplicate positions
- incorrect quantities
- incorrect average prices

---

# Persistence

Repositories persist state only.

Repositories never contain business logic.

Current repositories include:

- TradingSessionRepository
- PortfolioRepository
- TradeJournalRepository
- RuntimeEventRepository

---

# Runtime

ContinuousPaperTradingRunner

↓

AutonomousPaperTradingRunner

↓

TradingCycle

↓

Execution

↓

Synchronization

↓

Persistence

↓

Next iteration

The runtime must be restart-safe.

---

# Current Functional Status

Completed:

✓ Scanner

✓ Trading Pipeline

✓ Portfolio Allocation

✓ Execution Engine

✓ Paper Broker

✓ Interactive Brokers BUY execution

✓ Broker synchronization

✓ Continuous runtime

✓ Restart recovery

✓ Session persistence

Validated using Interactive Brokers Paper.

---

# Current Limitations

SELL execution is not yet implemented.

Current validation therefore uses:

- BUY only
- Paper account only
- controlled portfolio size

This limitation is intentional during validation.

---

# Sprint 11

Autonomous Position Lifecycle

Responsibilities:

Position Monitor

↓

Exit Engine

↓

SELL Execution

↓

Broker Synchronization

↓

Portfolio Update

↓

Trade Journal

↓

Performance Analysis

↓

Learning

---

# Learning Layer

Learning occurs only after completed trades.

Workflow:

Closed Trade

↓

Performance Analysis

↓

Hypothesis Evaluation

↓

Confidence Calibration

↓

Strategy Ranking

↓

Future Trade Selection

Learning never changes deterministic trading rules directly.

---

# Architectural Principles

Always preserve:

Single Responsibility

Deterministic Behaviour

Broker Truth

Regression Safety

Test Driven Development

Persistence Separation

No Business Logic in Repositories

No Manual Portfolio Updates

---

# Definition of Complete Platform

The platform is considered complete when it can autonomously:

Scan

↓

Analyse

↓

BUY

↓

Manage Position

↓

SELL

↓

Synchronize Broker

↓

Persist Runtime

↓

Analyse Performance

↓

Learn

↓

Repeat

without manual intervention while remaining fully deterministic and regression safe.