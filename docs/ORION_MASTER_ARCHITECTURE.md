# ORION MASTER ARCHITECTURE

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

# Purpose

This document defines the complete software architecture of Project Orion.

It is the single architectural reference for every future implementation.

Every new component, service and workspace must comply with the principles defined in this document.

GitHub remains the single source of truth.

---

# Core Philosophy

Project Orion is **not** an automated trading bot.

Project Orion is a deterministic AI-assisted decision-support platform.

Its responsibilities are:

- Scan markets
- Identify opportunities
- Evaluate risk
- Recommend actions
- Monitor open positions
- Explain deterministic decisions

It never executes broker orders.

---

# Architectural Principles

Every architectural decision follows these principles.

## 1. Deterministic First

Every BUY

Every HOLD

Every SELL

Every EXIT

Every RiskPlan

must be reproducible.

Randomness is forbidden.

---

## 2. Separation of Responsibilities

Every service owns exactly one responsibility.

Examples

TradingPipeline

↓

BUY / HOLD / SELL

AdaptiveRiskEngine

↓

RiskPlan

ExitEvaluationService

↓

EXIT

TradeLifecycleService

↓

Trade State

PortfolioStore

↓

Portfolio Persistence

Duplicate responsibilities are forbidden.

---

## 3. Explainability

Artificial Intelligence never creates decisions.

Artificial Intelligence only explains deterministic output.

AI may

✔ Explain

✔ Summarize

✔ Compare

✔ Generate natural language

AI may never

✘ BUY

✘ SELL

✘ EXIT

✘ Calculate indicators

✘ Calculate confidence

✘ Calculate RiskPlans

✘ Override deterministic output

---

## 4. UI Is Presentation Only

Qt widgets never perform business logic.

Qt widgets

✔ Render

✔ Display

✔ Trigger workflows

Qt widgets never

✘ Calculate indicators

✘ Generate decisions

✘ Save portfolio data

✘ Modify lifecycle state

---

# High-Level Architecture

Project Orion consists of five major layers.

```text
Presentation Layer

↓

Controllers

↓

Deterministic Services

↓

Domain Models

↓

Persistence
```

Every layer has a single responsibility.

Communication always flows downward.

No layer may bypass another.

---

# Current System Flow

The complete operational workflow is now

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

AdaptiveDecisionEngine

↓

AdaptiveRiskEngine

↓

RiskPlan

↓

Mission Control

↓

Trading Workspace

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
```

This represents the complete deterministic trading lifecycle currently implemented.

---

# Major Architecture Components

Current major components

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

✔ TradeLifecycleService

✔ TradeMonitorService

✔ PositionAnalysisService

✔ ExitEvaluationService

✔ PortfolioStore

✔ OpenTradeStore

✔ TradeHistoryStore

✔ AIContextBuilder

✔ AIExplainer

The architecture is modular.

Each component owns exactly one responsibility.

---

# Current Architectural Status

Backend

🟢 Stable

Desktop

🟢 Stable

Trade Lifecycle

🟢 Operational

Mission Control

🟢 Operational

Adaptive Risk Engine

🟢 Operational

Paper Trading

🟡 Planned

Broker Integration

⚪ Future

---

# Architectural Goal

The goal of Orion is no longer simply finding good stocks.

The goal is to provide a complete deterministic swing trading workstation that supports the trader throughout the entire investment lifecycle.

Opportunity Discovery

↓

Trade Decision

↓

Risk Planning

↓

Trade Lifecycle

↓

Portfolio Management

↓

Performance Evaluation

↓

Paper Trading

↓

Optional Broker Connectivity

Every future sprint must strengthen this architecture instead of replacing it.

---

# End of Part 1

---

# Backend Architecture

The backend is the deterministic core of Project Orion.

Every trading decision, risk calculation and lifecycle transition originates from backend services.

The backend remains the single source of truth.

No presentation component may duplicate backend logic.

Current backend architecture

```text
YahooProvider
        │
        ▼
IndicatorBuilder
        │
        ▼
IndicatorPack
        │
        ▼
SignalFusionEngine
        │
        ▼
MarketIntelligenceEngine
        │
        ▼
AdaptiveDecisionEngine
        │
        ▼
AdaptiveRiskEngine
        │
        ▼
TradingPipeline
        │
        ▼
Mission Control
Trading Workspace
Trade Monitor
```

---

# YahooProvider

Responsibility

Retrieve deterministic market data.

Responsibilities

- Current market price
- Historical candles
- Volume
- Market history
- Exchange-specific symbols

YahooProvider never

- Calculates indicators
- Creates BUY decisions
- Calculates risk
- Creates RiskPlans

---

# IndicatorBuilder

Responsibility

Convert raw market data into deterministic technical indicators.

Produces

IndicatorPack

Containing

- Symbol
- Current Price
- RSI
- Trend
- Momentum
- Volatility
- Volume

IndicatorBuilder never

- Generates BUY decisions
- Calculates confidence
- Calculates stop-loss
- Calculates targets

---

# IndicatorPack

IndicatorPack is the deterministic technical input shared by all higher-level services.

Current model

```text
IndicatorPack

Symbol

Price

RSI

Trend

Momentum

Volatility

Volume
```

IndicatorPack contains raw technical information only.

No decisions exist inside IndicatorPack.

---

# SignalFusionEngine

Responsibility

Combine multiple technical indicators into a unified market signal.

Outputs include

- Pressure Score
- Buy Pressure
- Sell Pressure
- Strength
- Trend
- Momentum
- RSI
- Volatility

SignalFusionEngine performs no trading decisions.

It prepares deterministic information for higher-level services.

---

# MarketIntelligenceEngine

Responsibility

Interpret market conditions.

Current outputs

- Market Regime
- Volatility State
- Risk Score

Example

```text
Bull Market

↓

Low Volatility

↓

Risk Score

↓

Adaptive Risk
```

MarketIntelligenceEngine never creates BUY decisions.

---

# AdaptiveDecisionEngine

Responsibility

Produce deterministic BUY / HOLD / SELL decisions.

Inputs

- SignalFusionEngine
- MarketIntelligenceEngine

Outputs

```text
BUY

Confidence

Reason
```

AdaptiveDecisionEngine remains the only deterministic decision engine.

No other component may generate BUY, HOLD or SELL.

---

# PositionSizer

Responsibility

Determine position size.

Inputs

- Portfolio
- Trading Capital
- Confidence
- Risk
- FX Conversion

Outputs

- Position Size
- Required Investment
- Buying Power

PositionSizer never performs risk planning.

---

# AdaptiveRiskEngine

Sprint 5.8 introduced the AdaptiveRiskEngine.

Purpose

Generate deterministic RiskPlans.

Current workflow

```text
BUY

↓

AdaptiveRiskEngine

↓

RiskPlan
```

Inputs

- Entry Price
- Confidence
- Risk Score
- Market Regime
- Volatility

Outputs

- Stop Loss
- Target 1
- Target 2
- Target 3
- Risk %
- Reward %
- Risk / Reward Ratio
- Notes

AdaptiveRiskEngine never

- Generates BUY
- Generates HOLD
- Generates SELL
- Generates EXIT

It operates only after a BUY decision exists.

---

# RiskPlan

RiskPlan is a deterministic domain model.

Current structure

```text
RiskPlan

Symbol

Entry Price

Stop Loss

Target 1

Target 2

Target 3

Risk %

Reward %

Risk / Reward

Confidence

Notes
```

RiskPlan is immutable.

It contains no business logic.

It is generated exclusively by AdaptiveRiskEngine.

---

# TradingPipeline

TradingPipeline orchestrates all deterministic backend services.

Current workflow

```text
IndicatorPack

↓

SignalFusionEngine

↓

MarketIntelligenceEngine

↓

AdaptiveDecisionEngine

↓

PositionSizer

↓

AdaptiveRiskEngine

↓

Pipeline Result
```

Current pipeline output

- Decision
- Confidence
- Pressure Score
- Buy Pressure
- Sell Pressure
- Position Size
- Expected Risk
- RiskPlan
- AI Context
- Human Explanation

TradingPipeline remains the deterministic backbone of Orion.

---

# OpportunityService

Responsibility

Transform TradingPipeline results into Mission Control opportunities.

Responsibilities

- Ranking
- Sorting
- Opportunity presentation
- Portfolio-aware investment information

OpportunityService never recalculates backend decisions.

---

# TradeLifecycleService

Responsibility

Own the lifecycle state of every trade.

Current lifecycle

```text
Open Trade

↓

OPEN

↓

Trade Monitor

↓

Close Trade

↓

CLOSED

↓

Trade History
```

TradeLifecycleService owns

- State transitions
- Persistence coordination
- Lifecycle timestamps

No UI component owns lifecycle state.

---

# Backend Status

Current backend maturity

🟢 Stable

Architecture

🟢 Modular

Responsibilities

🟢 Clearly separated

Business Logic

🟢 Backend only

Regression Tests

🟢 Passing

Current backend architecture is considered production-quality for deterministic paper trading.

---

# End of Part 2

---

# Desktop Architecture

The desktop application follows a strict presentation architecture.

Qt is responsible only for rendering deterministic backend output.

The desktop never performs business logic.

Current architecture

```text
Backend Services

↓

Controllers

↓

Presenters

↓

Workspaces

↓

Qt Widgets
```

Business logic always flows downward.

No UI component bypasses backend services.

---

# Mission Control

Mission Control is the operational center of Orion.

Responsibilities

- Scan market universe
- Display market status
- Display Top 10 opportunities
- Display buying power
- Display investment size
- Display confidence
- Display deterministic explanations

Mission Control never

- Calculates indicators
- Generates BUY decisions
- Generates RiskPlans
- Opens trades automatically

Current workflow

```text
Universe

↓

TradingPipeline

↓

OpportunityService

↓

Mission Control
```

Mission Control is optimized for rapid opportunity discovery.

---

# Trading Workspace

Purpose

Perform deterministic analysis for a single instrument.

Responsibilities

- Analyze selected symbol
- Present BUY / HOLD / SELL
- Display Confidence
- Display Pressure Score
- Display Position Size
- Display AI Explanation
- Open Trade

Current workflow

```text
User

↓

TradingController

↓

TradingPipeline

↓

AdaptiveRiskEngine

↓

RiskPlan

↓

Trading Workspace
```

The Trading Workspace never owns trading logic.

---

# Trade Monitor

Purpose

Monitor every active position.

Responsibilities

- Current Price
- Unrealized Profit/Loss
- Market Value
- Exit Intelligence
- Stop Loss
- Take Profit
- Trade Lifecycle
- Close Trade

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

Trade Monitor presents deterministic monitoring information only.

---

# Portfolio Workspace

Purpose

Manage deterministic capital information.

Responsibilities

- Trading Capital
- Available Buying Power
- Position sizing context
- Portfolio persistence

PortfolioWorkspace never calculates position sizing.

---

# History Workspace

Purpose

Display completed trades.

Responsibilities

- Closed trades
- Trade archive
- Historical performance

History is read-only.

TradeHistoryStore remains the owner of persistence.

---

# Performance Workspace

Purpose

Future portfolio analytics.

Planned capabilities

- Equity curve
- Monthly returns
- Win/Loss ratio
- Drawdown
- CAGR
- Sharpe Ratio

Current status

Framework completed.

Feature implementation planned for Sprint 6.

---

# Settings Workspace

Purpose

Configure deterministic platform behavior.

Responsibilities

- Universe selection
- Trading configuration
- Market configuration
- Platform preferences

Settings never modify deterministic trading logic.

---

# Controller Architecture

Controllers coordinate workflows.

Current controllers

✔ MissionControlController

✔ TradingController

✔ PositionMonitorController

✔ WorkspaceController

Controllers may

- Request backend services
- Coordinate workflows
- Update presenters

Controllers never

- Calculate indicators
- Generate BUY decisions
- Generate RiskPlans
- Modify persistence directly

---

# Presenter Architecture

Presenters convert deterministic models into GUI models.

Current presenters

✔ MissionControlPresenter

✔ PositionMonitorPresenter

✔ TradeMonitorPresenter

✔ HistoryPresenter

✔ SettingsPresenter

Presenters never contain business logic.

---

# Workspace Architecture

Each workspace owns one business domain.

Mission Control

↓

Market Discovery

Trading Workspace

↓

Trade Entry

Trade Monitor

↓

Trade Lifecycle

Portfolio

↓

Capital

History

↓

Completed Trades

Performance

↓

Analytics

Settings

↓

Configuration

No workspace performs another workspace's responsibility.

---

# Desktop Status

Architecture

🟢 Stable

Navigation

🟢 Stable

Presentation Layer

🟢 Stable

Controllers

🟢 Stable

Presenters

🟢 Stable

Business Logic Separation

🟢 Verified

The desktop architecture now follows a clean Model–Service–Controller–Presenter–Workspace design.

---

# End of Part 3

---

# Trade Lifecycle Architecture

The Trade Lifecycle manages every position from creation until archival.

Trading decisions and lifecycle management are intentionally separated.

Current lifecycle

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

ExitEvaluationService

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

# Trade States

Current lifecycle states

```text
NEW

↓

OPEN

↓

MONITORED

↓

CLOSED

↓

ARCHIVED
```

State transitions are owned exclusively by TradeLifecycleService.

The UI never changes lifecycle state directly.

---

# Data Flow

Current deterministic data flow

```text
YahooProvider

↓

IndicatorBuilder

↓

IndicatorPack

↓

TradingPipeline

↓

Pipeline Result

↓

Mission Control

↓

Trading Workspace

↓

TradeLifecycleService

↓

Trade Monitor
```

Every data transformation is deterministic.

Every layer consumes immutable models whenever possible.

---

# Persistence Architecture

Persistence is fully separated from business logic.

Current persistence services

PortfolioStore

↓

Portfolio.json

OpenTradeStore

↓

open_trades.json

TradeHistoryStore

↓

trade_history.json

Configuration

↓

config/

Logs

↓

logs/

No controller writes directly to disk.

Persistence is owned exclusively by Store classes.

---

# Domain Models

Current domain layer

```text
IndicatorPack

↓

Decision

↓

RiskPlan

↓

Trade

↓

Portfolio
```

Each domain model represents immutable business data.

Business logic belongs inside deterministic services.

---

# Risk Management Architecture

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

Future versions will extend RiskPlan without changing TradingPipeline.

Examples

- ATR Stop
- Trailing Stop
- Break-even Stop
- Dynamic Targets
- Partial Exit Strategy

---

# Artificial Intelligence Layer

Artificial Intelligence exists completely outside deterministic decision making.

Current architecture

```text
TradingPipeline

↓

AIContextBuilder

↓

AIExplainer

↓

Desktop
```

AI receives deterministic output.

AI never produces deterministic output.

Allowed

✔ Explain

✔ Summarize

✔ Compare

✔ Describe

Forbidden

✘ BUY

✘ SELL

✘ EXIT

✘ Position Size

✘ RiskPlan

✘ Stop Loss

✘ Take Profit

✘ Confidence

---

# Logging Architecture

Every important service logs deterministic execution.

Current logging

✔ TradingPipeline

✔ MissionControlController

✔ TradingController

✔ TradeMonitorService

✔ YahooProvider

✔ AdaptiveRiskEngine

Logs remain diagnostic only.

Logs never alter application state.

---

# Testing Strategy

Every architectural layer must be independently testable.

Current automated tests

✔ TradingPipeline

✔ AdaptiveRiskEngine

✔ PositionSizing

✔ TradeLifecycleService

✔ OpenTradeStore

✔ TradeMonitorService

✔ TradingConfig

✔ IndicatorConfig

✔ FX Rate Service

Regression

```powershell
python run_tests.py
```

Desktop validation

```powershell
python app.py
```

Manual validation remains mandatory before every Git push.

---

# Scalability

The architecture is intentionally modular.

Future deterministic services can be inserted without breaking existing layers.

Examples

```text
TradingPipeline

↓

AdaptiveRiskEngine

↓

PortfolioRiskEngine

↓

PaperBroker

↓

TradeLifecycleService
```

No existing responsibility needs to move.

Only new deterministic layers are added.

This keeps Orion maintainable as the project grows.

---

# Current Architecture Assessment

Backend

🟢 Production-quality

Desktop

🟢 Stable

Persistence

🟢 Stable

Trade Lifecycle

🟢 Operational

Risk Management

🟢 Operational

Testing

🟢 Stable

Scalability

🟢 Excellent

The architecture is now considered mature enough to support Paper Trading and future broker integrations without major restructuring.

---

# End of Part 4

---

# Development Rules

Every future implementation must comply with the architectural principles defined in this document.

Mandatory rules

✔ One responsibility per service

✔ No duplicate business logic

✔ Deterministic backend only

✔ Immutable domain models where possible

✔ UI contains presentation only

✔ Controllers orchestrate workflows only

✔ Presenters transform backend models only

✔ Stores own persistence only

✔ Artificial Intelligence explains deterministic output only

Architecture violations are never acceptable, even if they reduce implementation time.

---

# Future Architecture

The architecture has been intentionally designed to evolve through the addition of new deterministic services rather than replacing existing ones.

Current architecture

```text
Market Data

↓

Analysis

↓

Trading Decision

↓

Risk Planning

↓

Trade Lifecycle

↓

Trade Monitoring

↓

Trade History
```

Future architecture

```text
Market Data

↓

Analysis

↓

Trading Decision

↓

Adaptive Risk

↓

Portfolio Risk

↓

Paper Broker

↓

Trade Lifecycle

↓

Performance Analytics

↓

Broker Compatibility
```

Each future layer must integrate into the existing architecture without modifying existing responsibilities.

---

# Planned Architecture Evolution

## Sprint 5.9

Intelligent Risk Management

Planned

- RiskPlan visualization
- Risk / Reward presentation
- Target 2 visualization
- Target 3 visualization
- ATR-aware Stop Loss
- Dynamic Trailing Stop foundation
- Break-even foundation
- Partial profit-taking foundation

---

## Sprint 6.0

Paper Trading

Planned

- Paper Broker
- Simulated Orders
- Portfolio Performance
- Commission Model
- Slippage Model
- Equity Curve
- Daily Statistics
- Trade Journal

---

## Sprint 6.1

Portfolio Intelligence

Planned

- Portfolio Risk Engine
- Exposure Analysis
- Sector Allocation
- Correlation Analysis
- Drawdown Analysis
- Capital Allocation

---

## Sprint 6.2

Broker Compatibility

Planned

- Portfolio Import
- Portfolio Synchronization
- Assisted Order Preparation
- CSV Import / Export

Real broker execution remains outside Orion.

---

# Architectural Constraints

The following architectural constraints are permanent.

TradingPipeline

The only deterministic BUY / HOLD / SELL engine.

AdaptiveDecisionEngine

The only deterministic trading decision engine.

AdaptiveRiskEngine

The only deterministic RiskPlan generator.

ExitEvaluationService

The only deterministic EXIT engine.

TradeLifecycleService

The only owner of lifecycle state.

PortfolioStore

The only owner of portfolio persistence.

OpenTradeStore

The only owner of active trade persistence.

TradeHistoryStore

The only owner of historical trade persistence.

Any future implementation violating these ownership rules must be rejected.

---

# Definition of Done

A feature is complete only when all of the following are true.

Architecture

✔ Responsibility correctly assigned

✔ No duplicate logic

✔ No business logic inside UI

Backend

✔ Deterministic implementation

✔ Existing architecture respected

✔ Existing services reused where appropriate

Testing

✔ Regression tests pass

✔ New tests added when required

✔ Manual validation completed

Desktop

✔ Application launches successfully

✔ Navigation verified

✔ Workspace validated

Documentation

✔ AI_CONTEXT synchronized

✔ PROJECT_STATUS synchronized

✔ TODO synchronized

✔ CHANGELOG synchronized

✔ ORION_MASTER_ARCHITECTURE synchronized

✔ PROJECT_VISION synchronized

✔ TRADING_STRATEGY synchronized

Version Control

✔ Git commit

✔ Git push

---

# Current Architecture Status

Architecture Version

v2.2

Overall maturity

🟢 Stable

Backend

🟢 Stable

Desktop

🟢 Stable

Trade Lifecycle

🟢 Operational

Adaptive Risk Engine

🟢 Operational

Mission Control

🟢 Operational

Trading Workspace

🟢 Operational

Trade Monitor

🟢 Operational

Portfolio

🟢 Operational

History

🟢 Operational

Performance

🟢 Foundation Complete

Paper Trading

🟡 Planned

Broker Compatibility

⚪ Future

---

# Closing Statement

Project Orion has evolved from a market scanner into a modular deterministic trading workstation.

The architecture is intentionally designed around independent services, strict ownership of responsibilities and complete explainability.

Future development should focus on extending intelligent risk management, portfolio intelligence and paper trading without compromising the deterministic foundation.

The architecture defined in this document is considered the reference implementation for all future development.

GitHub remains the single source of truth.

---

# End of ORION_MASTER_ARCHITECTURE