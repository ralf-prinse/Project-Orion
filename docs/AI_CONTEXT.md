# AI_CONTEXT.md

> Documentation Version: v1.14
> Architecture Version: v2.3
> Last Updated: 2026-07-07

---

# PROJECT

Project Orion

Deterministic AI-Assisted Swing Trading Platform

---

# PROJECT VISION

Orion is a deterministic desktop trading platform designed to discover,
evaluate, execute and eventually manage stock trades autonomously.

Artificial Intelligence is used exclusively as an explainability layer.

Every trading decision remains completely deterministic.

The long-term objective is to evolve Orion into a fully autonomous
capital management platform capable of managing a user-defined account
according to deterministic trading rules.

Example:

> "Orion, here is €500.
> Grow this account autonomously while respecting the configured risk limits."

AI will never replace deterministic calculations.

Instead AI explains:

- why a trade exists
- why risk changed
- why a trade was closed
- why a position is healthy or unhealthy

AI never decides.

---

# CORE PRINCIPLES

Orion follows several strict engineering principles.

## Deterministic First

Every BUY

Every HOLD

Every SELL

Every EXIT

Every Stop Loss

Every Take Profit

Every RiskPlan

must always produce identical output for identical market input.

No randomness.

No LLM influence.

No hidden calculations.

---

## Artificial Intelligence

AI may:

- explain
- summarize
- educate
- generate reports

AI may NEVER:

- generate BUY
- generate SELL
- generate EXIT
- generate Stop Loss
- generate Take Profit
- generate Position Size
- overwrite deterministic output

---

# CURRENT ARCHITECTURE

Orion is now organized into five major layers.

Market Analysis

↓

Trading Decision

↓

Risk Planning

↓

Position Management

↓

Execution (future)

The architecture is intentionally modular.

Each layer owns a single responsibility.

Dependencies always flow downward.

Business logic never exists inside Qt Widgets.

Controllers coordinate workflows.

Presenters only format data.

Services perform deterministic calculations.

Models contain state only.


---

# CORE ARCHITECTURE

The deterministic trading engine is now organized as follows.

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

Portfolio

↓

Broker (Future)

---

# MARKET ANALYSIS LAYER

Responsible for transforming historical market data into deterministic indicators.

Main components

- IndicatorBuilder
- IndicatorPack
- MarketStructure

MarketStructure now contains deterministic market context including:

- ATR
- Average Daily Range
- Swing High
- Swing Low
- Support
- Resistance

MarketStructure is immutable.

It never contains business logic.

---

# DECISION LAYER

Responsible for producing deterministic BUY / HOLD / SELL decisions.

Main components

- Signal Fusion
- Market Intelligence
- AdaptiveDecisionEngine

AdaptiveDecisionEngine remains the single owner of:

- BUY
- HOLD
- SELL

No other component may generate trading decisions.

---

# RISK PLANNING LAYER

Responsible for building deterministic RiskPlans.

Main components

- RiskContextBuilder
- RiskContext
- AdaptiveRiskEngine
- RiskPlanValidator

RiskContext is now the single deterministic input for the
AdaptiveRiskEngine.

RiskContext currently contains:

- Symbol
- Entry Price
- Confidence
- Risk Score
- Market Regime
- Volatility State
- MarketStructure

AdaptiveRiskEngine now produces:

- Stop Loss
- Target 1
- Target 2
- Target 3
- Risk %
- Reward %
- Risk / Reward Ratio
- Adaptive Risk Notes

RiskPlanValidator validates every RiskPlan before it is allowed to
continue through the TradingPipeline.

Validation includes:

- Entry validation
- Stop Loss validation
- Target ordering
- Risk %
- Reward %
- Risk / Reward ratio
- Metadata validation

Invalid RiskPlans immediately stop the pipeline.

---

# POSITION MANAGEMENT LAYER

Sprint 5.9 introduced deterministic position management.

New architecture:

RiskPlan

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

PositionState contains the runtime state of every open position.

Current fields include:

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

PositionState is mutable runtime state.

RiskPlan remains immutable.

This separation is considered a permanent architectural decision.

---

# POSITION UPDATE ENGINE

PositionUpdateEngine is responsible for updating an open position.

Responsibilities

- receive market updates
- coordinate PositionManager
- update PositionState

It never:

- executes trades
- makes BUY decisions
- makes SELL decisions
- persists data

---

# POSITION MANAGER

PositionManager is now the central coordinator for open position management.

Current managed services:

- BreakEvenService
- TrailingStopService

Future managed services:

- TimeStopService
- PositionHealthService
- ExitEvaluationService

PositionManager does not execute trades.

It only produces deterministic management results.

---

# DEVELOPMENT PRINCIPLES

Project Orion follows strict software engineering principles.

## Single Responsibility Principle

Every service owns exactly one responsibility.

Examples

TradingPipeline

- orchestrates trading

AdaptiveDecisionEngine

- BUY / HOLD / SELL

AdaptiveRiskEngine

- RiskPlan generation

RiskPlanValidator

- RiskPlan validation

PositionUpdateEngine

- position update orchestration

PositionManager

- position management orchestration

BreakEvenService

- break-even calculations

TrailingStopService

- trailing stop calculations

Qt Widgets

- presentation only

---

# PERMANENT ARCHITECTURE RULES

These rules may never be violated.

TradingPipeline

→ sole trading orchestration engine.

AdaptiveDecisionEngine

→ sole BUY / HOLD / SELL engine.

AdaptiveRiskEngine

→ sole RiskPlan generator.

RiskPlanValidator

→ sole RiskPlan validation service.

PositionUpdateEngine

→ sole runtime position update engine.

PositionManager

→ sole coordinator of position-management services.

BreakEvenService

→ sole owner of break-even logic.

TrailingStopService

→ sole owner of trailing stop logic.

TradeLifecycleService

→ sole owner of trade lifecycle.

PortfolioStore

→ sole owner of portfolio persistence.

OpenTradeStore

→ sole owner of open trade persistence.

TradeHistoryStore

→ sole owner of closed trade persistence.

Controllers coordinate workflows.

Presenters format deterministic output.

Qt Widgets never contain business logic.

---

# CURRENT PROJECT STATUS

Completed

✓ Mission Control

✓ Trading Workspace

✓ Trade Monitor

✓ Portfolio

✓ History

✓ Settings

✓ TradingPipeline

✓ AdaptiveDecisionEngine

✓ AdaptiveRiskEngine V2

✓ RiskContext

✓ MarketStructure

✓ RiskPlanValidator

✓ PositionState

✓ PositionStateFactory

✓ PositionUpdateEngine

✓ PositionManager

✓ BreakEvenService

✓ TrailingStopService

✓ TradeLifecycleService

✓ PortfolioStore

✓ OpenTradeStore

✓ TradeHistoryStore

✓ ExitEvaluationService

✓ PositionAnalysisService

✓ Live Position Monitoring

✓ Dynamic RiskPlan Generation

✓ Top Opportunities

All regression tests currently pass.

Project health:

EXCELLENT

---

# CURRENT SPRINT

Sprint 5.9

Status:

Near Completion

Completed work

✓ RiskContext architecture

✓ MarketStructure integration

✓ ATR-based stop-loss

✓ Risk-distance targets

✓ RiskPlan validation

✓ PositionState runtime model

✓ PositionUpdateEngine

✓ PositionManager

✓ Break-even management

✓ Trailing stop management

Remaining before Sprint 6

- TimeStopService

- PositionHealthService

- PositionManager integration into TradeLifecycleService

- PositionState persistence

---

# NEXT MAJOR MILESTONE

Sprint 6

Paper Trading

Objectives

- Simulated portfolio

- Deterministic order execution

- Daily portfolio valuation

- Automatic position updates

- PositionManager integration

- Historical performance tracking

No broker integration before Paper Trading is fully validated.

---

# LONG TERM ROADMAP

Phase 1

Deterministic Trading Engine

Status

Completed

Phase 2

Advanced Position Management

Status

In Progress

Phase 3

Paper Trading

Status

Planned

Phase 4

Portfolio Intelligence

Status

Planned

Phase 5

Broker Compatibility Layer

Status

Planned

Phase 6

Autonomous Capital Management

Ultimate Vision

The user specifies:

- Initial capital

- Risk profile

- Allowed exchanges

- Allowed markets

Orion autonomously:

- scans markets

- opens trades

- manages positions

- protects capital

- compounds returns

using deterministic trading rules while AI remains strictly an explainability layer.

---

END OF FILE