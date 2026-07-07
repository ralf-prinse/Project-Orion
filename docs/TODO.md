# TODO.md

> Documentation Version: v1.15
> Architecture Version: v2.4
> Last Updated: 2026-07-07

---

# PROJECT ORION TODO

Current Sprint:

Sprint 6 — Paper Trading Engine

Status:

IN PROGRESS

Regression Status:

ALL TESTS PASSING

---

# COMPLETED

## Sprint 5.9 — Advanced Position Management

- [x] MarketStructure
- [x] RiskContext
- [x] AdaptiveRiskEngine V2
- [x] ATR Stop Loss
- [x] Risk Distance Targets
- [x] RiskPlanValidator
- [x] PositionState
- [x] PositionStateFactory
- [x] PositionUpdateEngine
- [x] PositionManager
- [x] BreakEvenService
- [x] TrailingStopService
- [x] TimeStopService
- [x] PositionHealthService
- [x] PositionStateStore
- [x] PositionManagementSummary
- [x] PositionManagementSummaryBuilder

---

## Sprint 6 — Paper Trading Foundation

- [x] ExecutionRequest
- [x] ExecutionContext
- [x] Order
- [x] ExecutionResult
- [x] ExecutionValidator
- [x] OrderFactory
- [x] ExecutionEngine
- [x] PaperBroker
- [x] PaperPortfolio
- [x] PaperPosition
- [x] PortfolioManager
- [x] ExecutionReportBuilder
- [x] TradingSession
- [x] PaperTradingService
- [x] PaperPositionUpdateService
- [x] PaperPositionCloseService
- [x] TradingCycle
- [x] PaperTradingRunner

---

# CURRENT WORK

## Sprint 6E — TradingPipeline Paper Integration

Priority:

VERY HIGH

Goal:

Automatically connect TradingPipeline output to the paper trading cycle.

Current flow:

MarketSnapshot

↓

Prepared pipeline_output

↓

TradingCycle

↓

PaperTradingRunner

Target flow:

MarketSnapshot

↓

IndicatorBuilder / IndicatorPack

↓

TradingPipeline

↓

ExecutionRequestBuilder

↓

ExecutionEngine

↓

PaperBroker

↓

TradingSession

---

# Sprint 6E Tasks

- [ ] Define PaperTradingPipelineAdapter
- [ ] Convert market data into IndicatorPack
- [ ] Run TradingPipeline automatically
- [ ] Pass pipeline output into TradingCycle
- [ ] Prevent duplicate open positions
- [ ] Add integration test for one symbol
- [ ] Add multi-symbol replay test
- [ ] Validate portfolio cash/equity after replay

---

# NEXT

## Sprint 6F — Close Logic Integration

Goal:

Close paper positions automatically based on deterministic rules.

Triggers:

- Stop-loss hit
- Target reached
- Time stop
- Manual close

---

## Sprint 6G — Paper Trading Loop

Goal:

Run autonomous paper trading over historical data.

Includes:

- multiple candles
- multiple symbols
- repeated scans
- portfolio updates
- position updates
- close events

---

## Sprint 6H — Portfolio Intelligence

Goal:

Add portfolio-level intelligence.

Planned:

- exposure
- allocation
- risk per position
- total portfolio risk
- cash utilization
- drawdown
- performance metrics

---

# FUTURE

## Broker Compatibility

Planned after Paper Trading is stable.

Possible broker targets:

- Interactive Brokers
- Alpaca
- Saxo
- Trading212 research

Broker adapters may only execute deterministic orders.

They may never calculate BUY, SELL, Stop Loss, Targets or Position Size.

---

END OF FILE