# ORION_MASTER_ARCHITECTURE.md

> Documentation Version: v1.15
> Architecture Version: v2.4
> Last Updated: 2026-07-07

---

# PROJECT ORION

## Master Architecture

This document defines the complete high-level architecture of Orion.

It serves as the single source of truth for all architectural decisions.

Every subsystem must comply with this document.

---

# DESIGN PHILOSOPHY

Orion is designed as a deterministic autonomous swing trading platform.

Primary goals:

- deterministic
- modular
- explainable
- regression-testable
- broker independent
- AI assisted
- production ready

AI may assist with:

- interpretation
- summarization
- market commentary

AI may never directly generate:

- BUY decisions
- SELL decisions
- stop-loss values
- targets
- risk sizing
- broker execution

All trading decisions must remain deterministic.

---

# CORE ARCHITECTURE

Orion is divided into independent subsystems.

Each subsystem has:

- Models
- Services
- Tests

Each orchestration layer:

- accepts exactly one Context or State object
- returns exactly one immutable Result object

Pattern:

Subsystem

↓

Context / State

↓

Engine

↓

Result

This pattern is mandatory throughout the project.

---

# SYSTEM OVERVIEW

```text
                    Market Data
                         │
                         ▼
                Market Intelligence
                         │
                         ▼
                 Trading Pipeline
                         │
                         ▼
                  Risk Engine
                         │
                         ▼
               Execution Engine
                         │
                         ▼
                 Paper Broker
                         │
                         ▼
                Trading Session
                         │
                         ▼
              Position Management
                         │
                         ▼
                 Trading Cycle
                         │
                         ▼
             Paper Trading Runner
```

---

# CURRENT IMPLEMENTED SUBSYSTEMS

```
Market Analysis

Risk Engine

Execution Layer

Paper Trading

Position Management

Trading Cycle

Paper Trading Runner
```

All systems above are operational and covered by regression tests.

---

# SUBSYSTEMS

---

# 1. MARKET ANALYSIS

Purpose

Analyze raw market data and produce deterministic trading decisions.

Responsibilities

- collect indicator values
- analyze trend
- analyze volatility
- detect market structure
- detect momentum
- combine signals

Output

TradingDecision

Main Components

- MarketScanner
- AIMarketScanner
- SignalFusionEngine
- MarketIntelligenceEngine
- TradingPipeline

The Market Analysis subsystem never performs:

- risk calculations
- execution
- portfolio management
- broker communication

---

# 2. RISK ENGINE

Purpose

Convert a trading decision into a deterministic RiskPlan.

Responsibilities

- ATR stop-loss
- volatility adjustments
- market regime adjustments
- reward targets
- risk validation

Input

RiskContext

Output

RiskPlan

Main Components

- RiskContext
- AdaptiveRiskEngine
- RiskPlanValidator

The Risk subsystem never performs:

- market scanning
- order execution
- portfolio management

---

# 3. EXECUTION LAYER

Purpose

Convert deterministic trading decisions into broker-neutral orders.

Responsibilities

- validate execution
- build orders
- execute through broker abstraction
- produce execution reports

Input

ExecutionContext

Output

ExecutionEngineResult

Main Components

- ExecutionRequest
- ExecutionContext
- ExecutionValidator
- OrderFactory
- ExecutionEngine
- ExecutionReportBuilder

Broker Implementation

PaperBroker

Future

BrokerAdapter

The Execution subsystem never generates BUY or SELL decisions.

---

# 4. PAPER TRADING

Purpose

Execute trades in a deterministic simulated environment.

Responsibilities

- maintain paper portfolio
- maintain cash
- maintain equity
- simulate fills

Main Components

- PaperPortfolio
- PaperPosition
- TradingSession
- PaperTradingService
- PaperPositionUpdateService
- PaperPositionCloseService

The Paper Trading subsystem never:

- scans markets
- calculates indicators
- generates trading decisions

---

# 5. POSITION MANAGEMENT

Purpose

Manage already opened positions.

Responsibilities

- break-even
- trailing stop
- time stop
- health monitoring
- position updates

Input

PositionState

Output

PositionUpdateResult

Main Components

- PositionManager
- PositionUpdateEngine
- BreakEvenService
- TrailingStopService
- TimeStopService
- PositionHealthService
- PositionStateStore
- PositionManagementSummaryBuilder

Position Management never:

- opens trades
- closes trades directly
- generates BUY or SELL signals

---

# 6. TRADING CYCLE

Purpose

Execute one complete deterministic trading tick.

Responsibilities

- open positions
- update positions
- close positions
- return updated TradingSession

Input

MarketSnapshot

Output

TradingCycleResult

Main Components

- MarketSnapshot
- TradingCycle
- TradingCycleResult

TradingCycle is the orchestration layer connecting:

TradingPipeline

↓

Execution

↓

Paper Trading

↓

Position Management

TradingCycle does not calculate indicators itself.

---

# 7. PAPER TRADING RUNNER

Purpose

Replay deterministic trading cycles.

Responsibilities

- execute multiple TradingCycles
- preserve TradingSession
- collect history

Input

TradingSession

+

MarketSnapshots

Output

PaperTradingRunResult

Main Components

- PaperTradingRunner
- PaperTradingRunResult

Future responsibilities

- historical replay
- multi-symbol replay
- live replay

---

# ARCHITECTURAL RULES

Every subsystem must satisfy the following rules.

Rule 1

One orchestration layer.

Rule 2

One Context or State object as input.

Rule 3

One immutable Result object as output.

Rule 4

No circular dependencies.

Rule 5

No duplicated business logic.

Rule 6

Business logic belongs inside services.

Rule 7

Models remain lightweight and deterministic.

Rule 8

Regression tests are mandatory.

---

# FUTURE ARCHITECTURE

The current implementation represents the foundation of Orion.

The remaining development focuses on expanding capabilities without changing the architectural principles defined in this document.

Every future subsystem must integrate into the existing deterministic pipeline.

---

# TARGET AUTONOMOUS FLOW

The final Orion architecture is designed as a continuous deterministic trading engine.

```
                Market Data
                     │
                     ▼
             Indicator Builder
                     │
                     ▼
              Trading Pipeline
                     │
                     ▼
                Risk Engine
                     │
                     ▼
             Execution Engine
                     │
                     ▼
               Broker Adapter
                     │
                     ▼
             Trading Session
                     │
                     ▼
          Position Management
                     │
                     ▼
             Portfolio Engine
                     │
                     ▼
             Trading Cycle
                     │
                     ▼
          Continuous Runner
                     │
                     └───────────────┐
                                     │
                                     ▼
                             Next Market Tick
```

---

# DEVELOPMENT PHASES

Development is divided into capability levels.

The objective is to complete one fully operational capability before introducing the next.

---

# LEVEL 1

Deterministic Paper Trading

Status

Completed (Foundation)

Capabilities

- TradingPipeline
- Risk Engine
- Execution Engine
- Paper Broker
- Paper Portfolio
- Position Management
- Trading Cycle
- Paper Trading Runner

Current limitation

TradingPipeline is not yet automatically connected to TradingCycle.

---

# LEVEL 2

Automatic TradingPipeline Integration

Objective

Remove manually prepared pipeline output.

Future flow

Market Data

↓

Indicator Builder

↓

TradingPipeline

↓

ExecutionRequest

↓

ExecutionEngine

↓

TradingCycle

↓

PaperTradingRunner

New planned components

- IndicatorBuilder
- PipelineAdapter
- TradingPipelineRunner

---

# LEVEL 3

Historical Replay Engine

Objective

Replay historical market data through the complete trading engine.

Capabilities

- multiple candles
- multiple symbols
- deterministic replay
- portfolio evolution
- trade history

Planned components

- ReplayEngine
- CandleFeed
- HistoricalSession

---

# LEVEL 4

Portfolio Intelligence

Objective

Evaluate the portfolio as a whole instead of evaluating only individual trades.

Planned capabilities

- total exposure
- sector exposure
- position sizing
- capital allocation
- portfolio heat
- portfolio drawdown
- portfolio risk
- portfolio performance

Possible components

- PortfolioAnalytics
- PortfolioAllocator
- PortfolioRiskEngine
- PortfolioPerformanceEngine
- PortfolioReportBuilder

---

# LEVEL 5

Multi-Asset Trading

Objective

Trade multiple symbols simultaneously.

Capabilities

- concurrent open positions
- portfolio-wide exposure control
- ranking competing opportunities
- capital allocation across symbols

Possible components

- OpportunityRanker
- PortfolioAllocator
- PositionSelector

---

# LEVEL 6

Broker Abstraction

Objective

Replace PaperBroker without changing business logic.

Architecture

ExecutionEngine

↓

Broker Interface

↓

Paper Broker

Interactive Brokers

Alpaca

Trading212

Future brokers

ExecutionEngine must never contain broker-specific code.

---

# LEVEL 7

Live Trading

Objective

Execute deterministic live trades through supported broker adapters.

Requirements

- deterministic execution
- broker confirmation
- retry handling
- logging
- audit trail
- rollback protection

No trading logic may exist inside broker adapters.

---

# LEVEL 8

Autonomous Capital Management

Objective

Operate a complete investment account without manual intervention.

Capabilities

- portfolio optimization
- cash management
- exposure balancing
- daily limits
- weekly limits
- risk budgeting

Long-term objective

User configures:

- starting capital
- allowed markets
- maximum risk
- trading schedule

Orion manages the portfolio autonomously.

---

# NON-NEGOTIABLE ARCHITECTURAL PRINCIPLES

The following rules apply to every future subsystem.

1.

Every orchestration layer accepts exactly one Context or State object.

2.

Every orchestration layer returns exactly one immutable Result object.

3.

Business logic exists only inside services.

4.

Models remain lightweight.

5.

No duplicated business logic.

6.

No circular dependencies.

7.

No subsystem may bypass another subsystem.

8.

Regression tests are mandatory before every commit.

9.

Architecture changes must be reflected in this document before implementation.

10.

The TradingPipeline remains the single source of truth for trading decisions.

---

# CURRENT PROJECT STATUS

Architecture Version

v2.4

Documentation Version

v1.15

Project Health

EXCELLENT

Regression Status

ALL TESTS PASSING

Current Capability

Deterministic autonomous paper trading foundation

Next Milestone

Automatic TradingPipeline Integration

Long-Term Vision

A deterministic, explainable, fully autonomous swing trading platform capable of managing real capital through broker-independent execution.

---

END OF DOCUMENT