# AI_CONTEXT

---

# Documentation Information

Documentation Version

v1.13

Architecture Version

v2.2

Status

🟢 Active Development

Current Sprint

🚧 Sprint 5.8 — Adaptive Risk Engine

Last Updated

2026-07-06

---

# Project Summary

Project Orion is a deterministic AI-assisted desktop swing trading platform.

Its objective is to scan a predefined investment universe, identify high-quality trading opportunities, calculate position sizing and risk, and guide the complete trade lifecycle from opportunity discovery through trade closure.

Artificial Intelligence is used exclusively as an explainability layer.

All BUY, HOLD, SELL and EXIT decisions remain fully deterministic.

---

# Current Development State

Current project maturity

🟢 Stable desktop application

Completed major milestones

✔ Mission Control

✔ Trading Workspace

✔ Portfolio Workspace

✔ Trade Monitor

✔ Trade History

✔ Position Sizing

✔ Live FX Conversion

✔ Trading Configuration

✔ Market Scanner

✔ Opportunity Ranking

✔ Open Trade Workflow

✔ Close Trade Workflow

✔ Live Trade Monitoring

✔ Dynamic Position Refresh

✔ Personal Universe V1

✔ Adaptive Risk Engine

Current application launches successfully.

Regression tests pass.

Architecture remains clean.

Business logic remains outside the UI.

---

# Current Workspace Architecture

Mission Control

Purpose

Daily operational dashboard.

Responsibilities

- Scan complete market universe
- Present market information
- Present top opportunities
- Display buying power
- Display investment size
- Display confidence
- Display deterministic explanations

Mission Control never performs analysis.

Mission Control only presents TradingPipeline output.

---

Trading Workspace

Purpose

Single-symbol deterministic analysis.

Responsibilities

- Analyze one symbol
- Display BUY / HOLD / SELL
- Display confidence
- Display pressure score
- Display AI explanation
- Allow opening a trade

Trading Workspace never calculates indicators.

TradingPipeline remains the single deterministic decision engine.

---

Trade Monitor

Purpose

Monitor active positions.

Responsibilities

- Live current price
- Live unrealized P/L
- Dynamic exit evaluation
- Stop-loss
- Take-profit
- Close Trade workflow
- Trade lifecycle management

Trade Monitor never creates BUY decisions.

Trade Monitor only evaluates existing positions.

---

Portfolio Workspace

Responsibilities

- Trading capital
- Currency
- Position sizing context
- Buying power

Portfolio is the single source of truth for available trading capital.

---

History Workspace

Responsibilities

- Closed trades
- Historical performance
- Trade archive

---

Settings Workspace

Responsibilities

- Universe selection
- Trading configuration
- Platform settings

---

# Current Backend Architecture

Current deterministic flow

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

Trade Monitor

↓

TradeHistoryStore

The architecture follows strict separation of responsibilities.

Every layer owns exactly one responsibility.

Duplicate business logic is forbidden.

---

# Adaptive Risk Engine (Sprint 5.8)

Sprint 5.8 introduced the first adaptive risk management layer.

Previous implementation

Entry

↓

Fixed Stop Loss (-5%)

↓

Fixed Take Profit (+10%)

Current implementation

Entry

↓

AdaptiveRiskEngine

↓

RiskPlan

↓

Dynamic Stop Loss

↓

Dynamic Target 1

↓

Dynamic Target 2

↓

Dynamic Target 3

Risk calculations now depend on

- Confidence
- Risk Score
- Volatility
- Market Regime
- Entry Price

The architecture supports future expansion toward

- ATR-based stop-loss
- Trailing stop
- Break-even stop
- Partial profit taking
- Dynamic target updates
- Portfolio risk balancing

The AdaptiveRiskEngine never generates BUY or SELL decisions.

Its responsibility begins only after a BUY decision has already been produced.

---

# Current Backend State

The backend is considered stable.

Completed deterministic services

✔ YahooProvider

✔ IndicatorBuilder

✔ AnalysisEngine

✔ TechnicalScanner

✔ MarketScanner

✔ TradingPipeline

✔ SignalFusionEngine

✔ MarketIntelligenceEngine

✔ AdaptiveDecisionEngine

✔ PositionSizer

✔ AdaptiveRiskEngine

✔ OpportunityService

✔ TradeLifecycleService

✔ TradeMonitorService

✔ PositionMonitorService

✔ PositionAnalysisService

✔ ExitEvaluationService

✔ PortfolioStore

✔ OpenTradeStore

✔ TradeHistoryStore

✔ AIContextBuilder

✔ AIExplainer

The backend remains the single source of truth.

No business logic exists inside Qt widgets.

---

# Current Desktop State

The desktop application is fully operational.

Current workspaces

✔ Mission Control

✔ Trading Workspace

✔ Trade Monitor

✔ Portfolio

✔ Performance

✔ History

✔ Settings

Navigation is stable.

Workspace rendering is stable.

Application startup is stable.

No architectural blockers currently exist.

---

# Mission Control

Mission Control currently displays

✔ Scanner Status

✔ Scan Duration

✔ Market Status

✔ Universe Coverage

✔ Top 10 Opportunities

✔ Current Price

✔ BUY / HOLD / SELL

✔ Confidence

✔ Position Size

✔ Required Investment

✔ Remaining Capital

✔ Buying Power

✔ Market Refresh

✔ Scan Market button

Mission Control now acts as the operational heart of Orion.

Scanner results are fully deterministic.

Opportunity ranking is deterministic.

---

# Trading Workspace

Trading Workspace currently supports

✔ Symbol analysis

✔ TradingPipeline execution

✔ BUY / HOLD / SELL

✔ Confidence

✔ Pressure

✔ Risk

✔ Position Size

✔ AI Explanation

✔ Open Trade

✔ Pipeline result caching

TradingController stores the latest deterministic pipeline result.

Open Trade uses the latest deterministic analysis.

---

# Trade Monitor

Trade Monitor currently supports

✔ Open Trades

✔ Live Current Price

✔ Live Unrealized Profit/Loss

✔ Live Position Value

✔ Entry Price

✔ Stop Loss

✔ Take Profit

✔ Exit Advice

✔ Exit Score

✔ Trend Status

✔ Momentum Status

✔ Risk Status

✔ Exit Reasons

✔ Close Trade

✔ Automatic refresh

✔ Trade lifecycle synchronization

Trade Monitor now represents the operational center of the trade lifecycle.

---

# Portfolio

Portfolio currently supports

✔ Trading Capital

✔ Persistent storage

✔ Position sizing context

✔ Save workflow

✔ Restart persistence

PortfolioStore remains the single persistence owner.

---

# Trade Lifecycle

Current lifecycle

Trading Workspace

↓

BUY

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

Trade lifecycle state is owned exclusively by backend services.

---

# Adaptive Risk Engine

Current implementation

IndicatorBuilder

↓

IndicatorPack

↓

TradingPipeline

↓

AdaptiveRiskEngine

↓

RiskPlan

↓

Open Trade

RiskPlan currently contains

✔ Entry Price

✔ Stop Loss

✔ Target 1

✔ Target 2

✔ Target 3

✔ Risk %

✔ Reward %

✔ Risk / Reward

✔ Confidence

✔ Notes

Current adaptive inputs

✔ Confidence

✔ Risk Score

✔ Volatility

✔ Market Regime

✔ Current Price

Fixed stop-loss percentages have been replaced by adaptive calculations.

Fixed take-profit percentages have been replaced by adaptive calculations.

The architecture now supports future intelligent risk management without modifying the TradingPipeline.

---

# Validation Status

Latest validation

✔ python run_tests.py

✔ Regression tests passed

✔ AdaptiveRiskEngine tests passed

✔ Desktop launches successfully

✔ Mission Control operational

✔ Trading Workspace operational

✔ Trade Monitor operational

✔ Portfolio operational

✔ History operational

✔ Settings operational

✔ Open Trade validated

✔ Close Trade validated

✔ Live P/L validated

✔ Adaptive Risk Plan validated

✔ Manual GUI validation completed

---

# Current GUI State

Mission Control

✔ Operational

Trading Workspace

✔ Operational

Trade Monitor

✔ Operational

Portfolio

✔ Operational

History

✔ Operational

Settings

✔ Operational

The desktop now resembles a professional trading workstation with deterministic trade lifecycle support.

---

# Development Rules

Every Orion implementation must follow these rules.

## Backend

TradingPipeline remains the only deterministic BUY / HOLD / SELL decision engine.

AdaptiveDecisionEngine determines deterministic trade decisions.

AdaptiveRiskEngine determines deterministic trade risk plans.

ExitEvaluationService remains the only deterministic EXIT decision engine.

TradeLifecycleService owns lifecycle transitions.

TradeMonitorService coordinates open-trade monitoring.

PositionAnalysisService retrieves technical analysis.

PortfolioStore owns portfolio persistence.

OpenTradeStore owns active trade persistence.

TradeHistoryStore owns closed-trade persistence.

Controllers orchestrate workflows only.

No deterministic calculations may exist inside controllers.

---

## Presentation

Widgets render only.

Workspaces render only.

Presenters transform deterministic output into readable UI.

Qt widgets never calculate indicators.

Qt widgets never calculate BUY, SELL or EXIT decisions.

Qt widgets never mutate lifecycle state.

Business logic belongs exclusively in backend services.

---

## Artificial Intelligence

Artificial Intelligence may

- Explain
- Summarize
- Compare
- Generate natural language

Artificial Intelligence may never

- Generate BUY decisions
- Generate SELL decisions
- Generate EXIT decisions
- Calculate indicators
- Calculate confidence
- Calculate position sizing
- Calculate stop-loss
- Calculate take-profit
- Override deterministic output
- Override TradingPipeline
- Override AdaptiveRiskEngine
- Open trades
- Close trades

Artificial Intelligence remains an explainability layer only.

---

# Current Architecture Direction

Mission Control remains the operational center of Orion.

Trade Monitor remains the operational center of the Trade Lifecycle.

The next architectural evolution is Intelligent Risk Management.

Current deterministic workflow

Market Data

↓

Technical Analysis

↓

TradingPipeline

↓

AdaptiveDecisionEngine

↓

AdaptiveRiskEngine

↓

RiskPlan

↓

Open Trade

↓

TradeLifecycleService

↓

Trade Monitor

↓

TradeHistoryStore

The deterministic backend remains the single source of truth.

---

# Current Known Limitations

The current implementation is stable.

Remaining limitations are functional rather than architectural.

Current limitations

- RiskPlan is not yet fully visualized inside Trade Monitor.
- Target 2 and Target 3 are calculated but not yet displayed.
- Risk/Reward ratio is not yet displayed.
- Trailing Stop is not implemented.
- Break-even logic is not implemented.
- Partial profit taking is not implemented.
- ATR-based stop-loss is not implemented.
- Portfolio-wide risk management is not implemented.
- Paper Trading is not implemented.
- Broker connectivity is not implemented.

No known architectural blockers exist.

---

# Immediate Next Sprint

Sprint 5.9 — Intelligent Risk Management

Objectives

- Display complete RiskPlan inside Trade Monitor.
- Display Target 1 / 2 / 3.
- Display Risk/Reward ratio.
- Improve Trade card presentation.
- Introduce ATR-aware stop-loss calculations.
- Introduce dynamic trailing stop foundation.
- Prepare partial profit-taking architecture.

---

# Sprint 6 Roadmap

Planned evolution

Sprint 6.0

- Intelligent Risk Manager V2
- ATR-based stop-loss
- Dynamic trailing stop
- Break-even stop
- Partial exits
- Portfolio risk allocation
- Dynamic exposure management

Sprint 6.1

- Paper Trading
- Portfolio performance
- Daily statistics
- Trade journal
- Equity curve

Sprint 6.2

- Broker compatibility layer
- Portfolio synchronization
- Order preparation
- Optional broker integration

---

# Git Workflow

GitHub remains the primary source of truth.

Every completed milestone must end with

- Regression tests
- Desktop validation
- Manual GUI validation
- Documentation synchronization
- Git commit
- Git push

Documentation must never lag behind implementation.

---

# Current Project Status

Current architecture

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

Overall project maturity

The deterministic architecture is now considered mature.

Current development is focused on expanding intelligent risk management and preparing Orion for a complete paper-trading environment.

---

# End of AI_CONTEXT