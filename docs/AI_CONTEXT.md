# AI_CONTEXT.md

> Documentation Version: v1.15
> Architecture Version: v2.4
> Last Updated: 2026-07-07

---

# PROJECT ORION

## Mission

Project Orion is a deterministic, modular swing trading platform.

The long-term objective is to operate fully autonomously while remaining:

- explainable
- deterministic
- testable
- broker-independent
- AI-assisted (never AI-controlled)

AI may assist with analysis, but AI is never allowed to make undocumented or non-deterministic trading decisions.

---

# ARCHITECTURE PRINCIPLES

Every subsystem follows the same philosophy.

Each orchestration layer:

- accepts one Context/State object
- returns one immutable Result object

Examples:

Risk

RiskContext

↓

AdaptiveRiskEngine

↓

RiskPlan

Execution

ExecutionContext

↓

ExecutionEngine

↓

ExecutionEngineResult

Position

PositionState

↓

PositionUpdateEngine

↓

PositionUpdateResult

Trading

TradingCycle

↓

TradingCycleResult

This pattern must remain consistent throughout Orion.

---

# CURRENT SYSTEMS

## Market Analysis

Completed.

Contains:

- Market Scanner
- AI Market Scanner
- Signal Fusion
- Market Intelligence
- TradingPipeline

Produces:

Trading decisions.

---

## Risk Engine

Completed.

Contains:

- RiskContext
- AdaptiveRiskEngine
- ATR Stop Loss
- RiskPlanValidator

Produces:

RiskPlan

---

## Execution Layer

Completed.

Contains:

- ExecutionRequest
- ExecutionContext
- ExecutionValidator
- OrderFactory
- ExecutionEngine
- PaperBroker
- ExecutionReportBuilder

Produces:

ExecutionEngineResult

---

## Paper Trading

Completed.

Contains:

- PaperPortfolio
- PaperPosition
- TradingSession
- PaperTradingService
- PaperPositionUpdateService
- PaperPositionCloseService

Supports:

- paper BUY
- paper UPDATE
- paper CLOSE

---

## Position Management

Completed.

Contains:

- PositionManager
- PositionUpdateEngine
- BreakEvenService
- TrailingStopService
- TimeStopService
- PositionHealthService
- PositionStateStore

Supports:

automatic stop management.

---

## Trading Runner

Completed.

Contains:

- MarketSnapshot
- TradingCycle
- TradingCycleResult
- PaperTradingRunner

Supports:

multi-cycle deterministic replay.

---

# CURRENT END-TO-END FLOW

The current deterministic trading flow is:

Market Snapshot

↓

TradingPipeline *(currently mocked input)*

↓

ExecutionRequestBuilder

↓

ExecutionRequest

↓

ExecutionContext

↓

ExecutionEngine

↓

PaperBroker

↓

TradingSession

↓

PositionUpdateEngine

↓

PaperPositionCloseService

↓

TradingCycle

↓

PaperTradingRunner

This flow is fully deterministic and regression-tested.

---

# NEXT MILESTONE

Sprint 6E

TradingPipeline Integration

Objective:

Remove manually supplied `pipeline_output`.

Future flow:

Market Data

↓

Indicator Builder

↓

TradingPipeline

↓

TradingCycle

↓

Execution Engine

↓

Paper Trading

---

# FUTURE ROADMAP

After TradingPipeline integration:

1. Multi-symbol trading
2. Historical replay engine
3. Portfolio intelligence
4. Portfolio allocation
5. Broker abstraction
6. Live broker adapters
7. Autonomous capital management

---

# DEVELOPMENT RULES

Never bypass existing engines.

Never duplicate logic.

Every subsystem must have:

- models
- services
- tests

Regression tests must pass before every commit.

Architecture changes must be documented before implementation.

---

# CURRENT PROJECT HEALTH

Architecture:

Stable

Regression:

All tests passing

Execution Layer:

Complete

Paper Trading Foundation:

Complete

Trading Cycle:

Operational

Next focus:

TradingPipeline Integration

---

END OF FILE