# ORION_MASTER_ARCHITECTURE.md

> Architecture Version: v2.3
> Documentation Version: v1.14
> Last Updated: 2026-07-07

---

# PROJECT ORION

## Master Architecture

Deterministic AI-Assisted Swing Trading Platform

---

# ARCHITECTURAL PHILOSOPHY

Orion is built around one fundamental principle:

**Every trading decision must be deterministic.**

Artificial Intelligence exists solely to explain deterministic output.

AI is never allowed to influence the outcome of:

- BUY decisions
- HOLD decisions
- SELL decisions
- EXIT decisions
- Stop Loss calculations
- Take Profit calculations
- Position sizing
- Risk calculations

Deterministic engines always own business logic.

AI owns explanation only.

---

# SYSTEM LAYERS

Orion is divided into five architectural layers.

```
Market Analysis

↓

Trading Decision

↓

Risk Planning

↓

Position Management

↓

Execution (Future)
```

Every layer owns exactly one responsibility.

Dependencies always flow downward.

Higher layers may orchestrate lower layers.

Lower layers never know about higher layers.

---

# CORE DESIGN PRINCIPLES

## Single Responsibility

Every service owns one responsibility.

Examples

TradingPipeline

→ Trading orchestration

AdaptiveDecisionEngine

→ BUY / HOLD / SELL

AdaptiveRiskEngine

→ RiskPlan generation

RiskPlanValidator

→ Risk validation

PositionUpdateEngine

→ Position update orchestration

PositionManager

→ Position management orchestration

BreakEvenService

→ Break-even calculations

TrailingStopService

→ Trailing stop calculations

---

## Deterministic First

All deterministic calculations must produce identical output for identical market input.

No randomness.

No hidden state.

No AI influence.

---

## Immutable Planning

Planning objects never change.

Examples

- IndicatorPack
- MarketStructure
- RiskContext
- RiskPlan

These objects describe how Orion intends to trade.

---

## Mutable Runtime State

Runtime state changes continuously.

Examples

- PositionState

PositionState describes how Orion manages an already opened trade.

This separation between planning and runtime state is considered permanent architecture.

---

# ARCHITECTURE OVERVIEW

The complete deterministic pipeline now consists of:

```
Market Data

↓

IndicatorBuilder

↓

IndicatorPack

↓

MarketStructure

↓

Signal Fusion

↓

Market Intelligence

↓

AdaptiveDecisionEngine

↓

Trading Decision

↓

RiskContextBuilder

↓

RiskContext

↓

AdaptiveRiskEngine

↓

RiskPlan

↓

RiskPlanValidator

↓

PositionStateFactory

↓

PositionState

↓

PositionUpdateEngine

↓

PositionManager

↓

BreakEvenService

↓

TrailingStopService

↓

TradeLifecycleService

↓

Execution Layer (Future)
```

---

# LAYER 1 — MARKET ANALYSIS

## Purpose

Transform raw market data into deterministic market intelligence.

This layer never produces trading decisions.

It only prepares deterministic information.

### Components

Market Scanner

IndicatorBuilder

IndicatorPack

MarketStructure

Signal Fusion

Market Intelligence

### Responsibilities

- Download market data
- Calculate indicators
- Build deterministic MarketStructure
- Measure volatility
- Detect support
- Detect resistance
- Calculate ATR
- Detect swing highs
- Detect swing lows
- Calculate signal pressure

### Output

IndicatorPack

↓

MarketStructure

↓

Market Intelligence

---

# LAYER 2 — TRADING DECISION

## Purpose

Produce deterministic BUY / HOLD / SELL decisions.

### Components

AdaptiveDecisionEngine

TradingPipeline

### Responsibilities

- Evaluate market intelligence
- Generate BUY
- Generate HOLD
- Generate SELL

### Permanent Rule

BUY / HOLD / SELL may ONLY be produced by:

AdaptiveDecisionEngine

No exceptions.

TradingPipeline orchestrates the process but never owns trading logic.

---

# LAYER 3 — RISK PLANNING

## Purpose

Transform a deterministic trading decision into a deterministic RiskPlan.

### Components

RiskContextBuilder

RiskContext

AdaptiveRiskEngine

RiskPlan

RiskPlanValidator

### Responsibilities

Build RiskContext

↓

Generate RiskPlan

↓

Validate RiskPlan

### RiskContext

RiskContext contains every deterministic input required by the
AdaptiveRiskEngine.

Current fields

- Symbol
- Entry Price
- Confidence
- Risk Score
- Market Regime
- Volatility State
- MarketStructure

### MarketStructure

MarketStructure currently contains

- ATR
- Average Daily Range
- Swing High
- Swing Low
- Support
- Resistance

### AdaptiveRiskEngine

AdaptiveRiskEngine is solely responsible for:

- Stop Loss
- Target 1
- Target 2
- Target 3
- Risk %
- Reward %
- Risk / Reward Ratio

Current implementation

- ATR based Stop Loss
- Risk Distance based Targets

Future versions

- ATR based Trailing Stop
- Time Horizon
- Support / Resistance constrained targets
- Dynamic volatility scaling

### RiskPlanValidator

Every RiskPlan is validated before leaving the Risk Planning Layer.

Validation includes

- Entry validation
- Stop validation
- Target ordering
- Risk %
- Reward %
- Risk / Reward Ratio
- Metadata validation

Invalid RiskPlans terminate pipeline execution immediately.

---

# LAYER 4 — POSITION MANAGEMENT

## Purpose

Manage already opened positions.

No BUY decisions.

No SELL decisions.

Only runtime management.

### Components

PositionStateFactory

PositionState

PositionUpdateEngine

PositionManager

BreakEvenService

TrailingStopService

### PositionState

PositionState represents mutable runtime information.

Current runtime fields

- Symbol
- Entry Price
- Current Price
- Highest Price
- Current Stop Loss
- Break-even Active
- Trailing Stop Active
- Target 1 Hit
- Target 2 Hit
- Target 3 Hit

Unlike RiskPlan,

PositionState changes continuously while a trade remains open.

### PositionUpdateEngine

Coordinates runtime updates.

Responsibilities

- receive market updates
- coordinate PositionManager
- update PositionState

No business logic beyond orchestration.

### PositionManager

Coordinates deterministic management services.

Current managed services

- BreakEvenService
- TrailingStopService

Future managed services

- TimeStopService
- PositionHealthService
- ExitEvaluationService

### BreakEvenService

Responsibilities

- activate break-even
- never lower Stop Loss
- preserve capital

### TrailingStopService

Responsibilities

- monitor Highest Price
- raise Stop Loss
- never reduce protection

Current implementation

Fixed percentage trailing.

Future implementation

ATR based trailing.

---

# LAYER 5 — EXECUTION

Status

Future

Responsibilities

- Paper Trading
- Simulated Orders
- Broker Adapter
- Portfolio Synchronization
- Order Execution

No implementation exists yet.

The architecture has already been prepared for this layer.


---

# ARCHITECTURAL OWNERSHIP

Every major responsibility inside Orion has exactly one owner.

This rule may never be violated.

---

## Trading Decisions

Owner

AdaptiveDecisionEngine

Responsible for

- BUY
- HOLD
- SELL

No other component may generate trading decisions.

---

## Risk Planning

Owner

AdaptiveRiskEngine

Responsible for

- Stop Loss
- Target 1
- Target 2
- Target 3
- Risk %
- Reward %
- Risk / Reward Ratio

No other component may generate RiskPlans.

---

## Risk Validation

Owner

RiskPlanValidator

Responsible for

- RiskPlan consistency
- RiskPlan validation
- Pipeline safety

Invalid RiskPlans terminate execution.

---

## Position Updates

Owner

PositionUpdateEngine

Responsible for

- Runtime position updates
- Updating PositionState
- Coordinating PositionManager

PositionUpdateEngine never contains business logic.

---

## Position Management

Owner

PositionManager

Responsible for coordinating deterministic position-management services.

Current services

- BreakEvenService
- TrailingStopService

Future services

- TimeStopService
- PositionHealthService
- ExitEvaluationService

PositionManager itself contains orchestration only.

---

## Break-even

Owner

BreakEvenService

Responsibilities

- Activate break-even
- Protect capital
- Never lower Stop Loss

---

## Trailing Stop

Owner

TrailingStopService

Responsibilities

- Track Highest Price
- Raise Stop Loss
- Never decrease Stop Loss

---

## Trade Lifecycle

Owner

TradeLifecycleService

Responsible for

- Trade state transitions
- Open
- Active
- Closed

TradeLifecycleService never calculates trading decisions.

---

## Persistence

Portfolio

PortfolioStore

Open Positions

OpenTradeStore

Closed Positions

TradeHistoryStore

Each persistence service owns exactly one storage domain.

---

# DEPENDENCY RULES

Dependencies always flow downward.

```
TradingPipeline

↓

AdaptiveDecisionEngine

↓

AdaptiveRiskEngine

↓

RiskPlanValidator

↓

PositionUpdateEngine

↓

PositionManager

↓

BreakEvenService

↓

TrailingStopService
```

Reverse dependencies are forbidden.

Services may never depend on Qt Widgets.

Qt Widgets may depend on Presenters.

Presenters may depend on Models.

Controllers orchestrate workflows only.

---

# IMMUTABILITY RULES

Immutable models

- IndicatorPack
- MarketStructure
- RiskContext
- RiskPlan

Mutable runtime models

- PositionState

RiskPlan is never modified after creation.

PositionState is continuously updated while a position remains open.

---

# EXTENSION STRATEGY

Future functionality must extend the architecture without modifying existing ownership.

Examples

TimeStopService

↓

PositionManager

↓

PositionUpdateEngine

PositionHealthService

↓

PositionManager

↓

PositionUpdateEngine

Broker Adapter

↓

Execution Layer

↓

TradeLifecycleService

No new functionality may bypass the established ownership rules.

---

# ARCHITECTURAL GOALS

The architecture has been designed to support:

✓ deterministic trading

✓ deterministic risk management

✓ deterministic position management

✓ paper trading

✓ broker compatibility

✓ autonomous portfolio management

without requiring structural redesign.


---

# CURRENT MATURITY

The Orion architecture has evolved from a market analysis application
into a deterministic trading engine.

Current maturity by subsystem

Market Analysis

████████████████████ 100%

Trading Decision

████████████████████ 100%

Risk Planning

███████████████████░ 95%

Position Management

██████████████████░░ 90%

Execution Layer

░░░░░░░░░░░░░░░░░░░░ 0%

Broker Integration

░░░░░░░░░░░░░░░░░░░░ 0%

---

# CURRENT PRIORITIES

The architecture is now considered stable.

No further architectural restructuring is planned before
Sprint 6.

Development effort should now focus on extending the existing
architecture instead of redesigning it.

Remaining Position Management work

• TimeStopService

• PositionHealthService

• PositionStateStore

• TradeLifecycle integration

After these components are complete,
the Position Management Layer is considered feature complete.

---

# SPRINT 6

Primary Objective

Paper Trading

Planned architecture

```
TradingPipeline

↓

AdaptiveRiskEngine

↓

RiskPlan

↓

PositionState

↓

PositionUpdateEngine

↓

Paper Broker

↓

Paper Portfolio

↓

Performance Analytics
```

Paper Trading must reuse the deterministic engine.

No duplicate business logic is allowed.

---

# BROKER COMPATIBILITY

Broker support will only be implemented after
Paper Trading has been fully validated.

The future Broker Layer will only translate deterministic
orders into broker-specific API calls.

Broker adapters will never calculate:

- BUY
- SELL
- Stop Loss
- Targets
- Position Size

Those values remain exclusively owned by the deterministic engine.

---

# AUTONOMOUS CAPITAL MANAGEMENT

Ultimate project vision

The user specifies:

• Initial Capital

• Maximum Risk

• Trading Universe

• Broker

• Trading Rules

Orion autonomously performs:

• Market Scanning

• Trade Selection

• Risk Planning

• Position Management

• Portfolio Monitoring

• Capital Protection

• Performance Tracking

while remaining completely deterministic.

Artificial Intelligence continues to function solely
as an explainability layer.

---

# VERSION HISTORY

Architecture v2.0

Introduced deterministic trading architecture.

Architecture v2.1

Introduced AdaptiveDecisionEngine.

Architecture v2.2

Introduced AdaptiveRiskEngine.

Architecture v2.3

Introduced the complete Position Management Layer.

Major additions

✓ MarketStructure

✓ RiskContext

✓ RiskPlanValidator

✓ PositionState

✓ PositionStateFactory

✓ PositionUpdateEngine

✓ PositionManager

✓ BreakEvenService

✓ TrailingStopService

This architecture establishes the foundation required for:

- Advanced Position Management
- Paper Trading
- Portfolio Intelligence
- Broker Compatibility
- Autonomous Capital Management

without requiring fundamental architectural redesign.

---

# ARCHITECTURE STATUS

Architecture Version

v2.3

Status

STABLE

Regression Status

ALL TESTS PASS

Project Health

🟢 EXCELLENT

Next Target

Sprint 6 — Paper Trading

---

END OF FILE