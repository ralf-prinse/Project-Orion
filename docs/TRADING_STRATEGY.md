# TRADING STRATEGY

---

# Documentation Information

Documentation Version

v1.13

Architecture Version

v2.2

Status

🟢 Active Development

Current Sprint

🚧 Sprint 5.9 — Intelligent Risk Management

Last Updated

2026-07-06

---

# Mission

Project Orion is a deterministic AI-assisted decision-support platform for swing trading.

Its purpose is not to predict future prices.

Its purpose is to continuously evaluate predefined markets, identify high-quality opportunities, generate deterministic trading decisions and calculate adaptive risk before a position is opened.

Artificial Intelligence never generates trading decisions.

Artificial Intelligence only explains deterministic output.

---

# Primary Objectives

For every monitored instrument Orion continuously answers the following questions.

1. Is this instrument worth monitoring?

2. Is this an appropriate moment to enter?

3. How large should the position be?

4. Should a trade be opened?

5. What is the appropriate deterministic RiskPlan?

6. Should an existing trade remain open?

7. Is it time to exit?

Mission Control presents these answers as quickly and clearly as possible.

---

# Trading Philosophy

Project Orion follows several non-negotiable principles.

- Capital preservation comes first.
- Missing a profitable trade is acceptable.
- Large losses are unacceptable.
- Every trade requires a predefined exit strategy.
- Every trade has a known maximum risk.
- Every recommendation must remain deterministic.
- Every recommendation must remain explainable.
- Architecture has priority over implementation speed.
- Duplicate business logic is forbidden.

---

# Market Scope

Current broker context

DEGIRO

Account currency

EUR

Supported exchanges

- NASDAQ
- NYSE
- Euronext Amsterdam
- Xetra

Supported currencies

- EUR
- USD

Supported asset classes

- Large-cap equities
- Highly liquid ETFs

Excluded

- Penny stocks
- Leveraged ETFs
- Options
- Futures
- Crypto (initially)

---

# Deterministic Trading Flow

Project Orion currently contains four deterministic workflows.

Every workflow owns exactly one responsibility.

Artificial Intelligence never participates in deterministic decisions.

---

## 1. Opportunity Discovery

```text
Universe

↓

YahooProvider

↓

TechnicalScanner

↓

AnalysisEngine

↓

TradingPipeline

↓

OpportunityService

↓

Mission Control
```

Mission Control presents deterministic opportunities only.

TradingPipeline remains the only deterministic BUY / HOLD / SELL engine.

---

## 2. Entry Workflow

```text
Symbol

↓

YahooProvider

↓

IndicatorBuilder

↓

TradingPipeline

↓

BUY / HOLD / SELL

↓

AdaptiveRiskEngine

↓

RiskPlan

↓

Trading Workspace
```

Only BUY decisions continue toward the Trade Lifecycle.

The Trading Workspace presents deterministic output only.

---

## 3. Risk Planning

Sprint 5.8 introduced deterministic adaptive risk planning.

Workflow

```text
BUY

↓

AdaptiveRiskEngine

↓

RiskPlan
```

RiskPlan currently contains

- Entry Price
- Stop Loss
- Target 1
- Target 2
- Target 3
- Risk %
- Reward %
- Risk / Reward
- Confidence
- Notes

AdaptiveRiskEngine never creates BUY, SELL or EXIT decisions.

It only generates deterministic risk management after a BUY decision already exists.

---

## 4. Trade Lifecycle

The Trade Lifecycle manages every deterministic position from creation until archival.

Current workflow

```text
Trading Workspace

↓

BUY

↓

AdaptiveRiskEngine

↓

RiskPlan

↓

Open Trade

↓

TradeLifecycleService

↓

OpenTradeStore

↓

Trade Monitor

↓

Close Trade

↓

TradeHistoryStore

↓

History Workspace
```

Responsibilities

TradingPipeline

↓

Generate BUY / HOLD / SELL

AdaptiveRiskEngine

↓

Generate RiskPlan

TradeLifecycleService

↓

Manage lifecycle state

ExitEvaluationService

↓

Generate deterministic EXIT advice

TradeHistoryStore

↓

Archive completed trades

Each responsibility exists exactly once.

---

## TradeLifecycleService

TradeLifecycleService owns the lifecycle state of every position.

Responsibilities

- Open trades
- Maintain lifecycle state
- Coordinate lifecycle transitions
- Synchronize persistence
- Archive completed trades

TradeLifecycleService never

- Calculates indicators
- Generates BUY decisions
- Generates EXIT decisions
- Calculates RiskPlans

---

## OpenTradeStore

OpenTradeStore owns persistence of active positions.

Responsibilities

- Save active trades
- Load active trades
- Remove closed trades

OpenTradeStore performs no calculations.

---

## Trade Monitor

Trade Monitor is the operational workspace for active positions.

Its purpose is to answer

- Is this trade healthy?
- Has risk increased?
- Should this trade remain open?
- Is action required?

Current workflow

```text
Open Trades

↓

TradeMonitorService

↓

PositionAnalysisService

↓

ExitEvaluationService

↓

Trade Monitor
```

Trade Monitor presents deterministic information only.

No business logic exists inside the GUI.

---

## PositionAnalysisService

PositionAnalysisService retrieves all information required to evaluate existing positions.

Responsibilities

- Retrieve latest market price
- Retrieve historical candles
- Build deterministic analysis input
- Reuse AnalysisEngine

PositionAnalysisService performs no trading decisions.

---

## ExitEvaluationService

ExitEvaluationService remains the only deterministic EXIT decision engine.

Possible outputs

- HOLD_POSITION
- TAKE_PROFIT
- STOP_LOSS
- EXIT_DUE_TO_WEAKNESS
- TRAILING_STOP (future)
- EXIT_DUE_TO_TIME_LIMIT (future)

No other service may generate EXIT advice.

---

# Risk Management

Risk management is integrated into every deterministic trade.

Current deterministic workflow

```text
TradingPipeline

↓

BUY

↓

AdaptiveRiskEngine

↓

RiskPlan

↓

TradeLifecycleService
```

Current RiskPlan

- Entry Price
- Stop Loss
- Target 1
- Target 2
- Target 3
- Risk %
- Reward %
- Risk / Reward Ratio
- Confidence
- Notes

Current AdaptiveRiskEngine inputs

- Current Price
- Confidence
- Risk Score
- Market Regime
- Volatility

Current outputs

- Dynamic Stop Loss
- Dynamic Profit Targets
- Deterministic Risk Plan

The previous fixed ±5% / ±10% model has been replaced by adaptive calculations.

---

# Current Monitoring

Every active trade is continuously monitored.

Current monitoring includes

- Entry Price
- Current Price
- Unrealized Profit/Loss
- Market Value
- Stop Loss
- Take Profit
- Exit Score
- Trend Status
- Momentum Status
- Risk Status
- Exit Reasons

Future monitoring will include

- Target 2
- Target 3
- Risk / Reward
- Trailing Stop
- Break-even
- Partial profit taking
- Portfolio exposure

Monitoring remains fully deterministic.

---

# Artificial Intelligence

Artificial Intelligence is an explainability layer.

AI may

- Explain deterministic analysis
- Summarize opportunities
- Compare opportunities
- Produce natural-language reports

AI may never

- Generate BUY signals
- Generate SELL signals
- Generate EXIT signals
- Calculate indicators
- Calculate confidence
- Calculate RiskPlans
- Override TradingPipeline
- Override AdaptiveRiskEngine
- Open trades
- Close trades

The deterministic backend always remains the single source of truth.

---

# Current Implementation Status

Completed

✔ YahooProvider

✔ IndicatorBuilder

✔ AnalysisEngine

✔ TechnicalScanner

✔ MarketScanner

✔ TradingPipeline

✔ SignalFusionEngine

✔ MarketIntelligenceEngine

✔ AdaptiveDecisionEngine

✔ AdaptiveRiskEngine

✔ PositionSizer

✔ OpportunityService

✔ Mission Control

✔ Trading Workspace

✔ Portfolio

✔ Trade Monitor

✔ TradeLifecycleService

✔ OpenTradeStore

✔ TradeHistoryStore

✔ PositionAnalysisService

✔ ExitEvaluationService

✔ AIContextBuilder

✔ AIExplainer

✔ Dynamic RiskPlan generation

✔ Live Position Monitoring

✔ Automatic Trade Refresh

✔ Top 10 Opportunity Ranking

✔ Personal Universe V1

Current Sprint

🚧 Sprint 5.9 — Intelligent Risk Management

---

# Sprint Roadmap

## Sprint 5.9

Current objectives

- Display complete RiskPlan
- Display Target 1
- Display Target 2
- Display Target 3
- Display Risk %
- Display Reward %
- Display Risk / Reward ratio
- Improve Trade Monitor presentation
- ATR-aware Stop Loss
- Dynamic Trailing Stop foundation
- Break-even foundation
- Partial profit-taking foundation

---

## Sprint 6.0

Paper Trading

Objectives

- Paper Broker
- Simulated Order Execution
- Portfolio Performance
- Trade Journal
- Commission Model
- Slippage Model
- Equity Curve
- Daily Statistics

---

## Sprint 6.1

Portfolio Intelligence

Objectives

- Portfolio Risk Engine
- Portfolio Exposure
- Sector Allocation
- Correlation Analysis
- Drawdown Analysis
- Allocation Optimizer

---

## Sprint 6.2

Broker Compatibility

Objectives

- Portfolio Import
- Portfolio Synchronization
- CSV Import / Export
- Assisted Order Preparation

Real broker execution remains outside Orion.

---

# Strategy Evolution

The strategic evolution of Orion now follows four deterministic stages.

Stage 1

Market Discovery

↓

Mission Control

---

Stage 2

Trading Decision

↓

TradingPipeline

↓

AdaptiveDecisionEngine

---

Stage 3

Risk Planning

↓

AdaptiveRiskEngine

↓

RiskPlan

---

Stage 4

Trade Lifecycle

↓

TradeLifecycleService

↓

Trade Monitor

↓

Trade History

Future stages

↓

Portfolio Intelligence

↓

Paper Trading

↓

Optional Broker Compatibility

---

# Success Criteria

A successful Orion strategy

✔ Produces deterministic decisions

✔ Produces deterministic RiskPlans

✔ Remains fully explainable

✔ Protects trading capital

✔ Minimizes unnecessary trades

✔ Keeps architecture modular

✔ Keeps business logic outside the UI

✔ Supports the complete Trade Lifecycle

✔ Supports deterministic risk management

✔ Remains reproducible

✔ Remains independently testable

---

# Current Project Assessment

Architecture

🟢 Stable

Backend

🟢 Stable

Desktop

🟢 Stable

Trade Lifecycle

🟢 Operational

Mission Control

🟢 Operational

Trading Workspace

🟢 Operational

Trade Monitor

🟢 Operational

Adaptive Risk Engine

🟢 Operational

Portfolio

🟢 Operational

History

🟢 Operational

Current development focus

The current focus is no longer building the trading workflow.

The trading workflow is considered complete.

Development now focuses on expanding deterministic intelligent risk management and preparing Orion for a complete paper trading environment.

---

# Guiding Principle

Every future feature must strengthen the deterministic architecture before expanding automation.

Trading decisions remain deterministic.

Risk planning remains deterministic.

Lifecycle management remains deterministic.

Artificial Intelligence remains an explainability layer.

The deterministic backend remains the single source of truth.

---

# End of TRADING_STRATEGY