# CHANGELOG

# Sprint 3.13 — AI Desktop Integration & Stabilization (COMPLETED)

---

## Added

### Live Market Integration

- Added `IndicatorBuilder`
- Live Yahoo Finance integration
- Deterministic indicator generation from historical market data

IndicatorBuilder now converts historical OHLCV data into standardized `IndicatorPack` models.

---

### Trading Configuration

Added centralized configuration.

New module:

- `TradingConfig`

Current configurable settings:

- RSI period
- Momentum period
- Trend period
- Volatility period
- Yahoo history period
- Yahoo interval
- Default scanner universe
- Scanner limits
- Backtest fee model
- Backtest slippage model

Hardcoded trading parameters have been removed from multiple services.

---

### AI Market Scanner

Added:

- AIMarketScanner

Capabilities:

- execute Trading Pipeline for multiple assets
- rank opportunities
- determine best trade
- produce deterministic portfolio-wide scan results

Trading and Scanner now share the exact same deterministic pipeline.

---

### Desktop Integration

Added:

- Trading Workspace
- Trading Workspace Presenter
- AI Scanner Presenter
- ApplicationController

ApplicationController is now responsible for orchestrating:

- Trading
- Dashboard
- Scanner

The desktop UI now uses a centralized orchestration layer.

---

## Changed

### Trading Workspace

Trading Workspace now performs:

Yahoo Finance

↓

IndicatorBuilder

↓

Trading Pipeline

↓

AI Context

↓

AI Explanation

↓

Desktop Presentation

No demo indicator data remains.

---

### Scanner

Legacy scanning flow has been replaced by the AI Market Scanner.

Current flow:

Yahoo Finance

↓

IndicatorBuilder

↓

Trading Pipeline

↓

AIMarketScanner

↓

AIScannerPresenter

↓

Scanner Workspace

Trading and Scanner now share one deterministic source of truth.

---

### Configuration

IndicatorBuilder now consumes TradingConfig.

ApplicationController now consumes TradingConfig.

Default scan symbols are configurable.

Historical market settings are configurable.

---

## Architecture

ApplicationController introduced as the central desktop orchestrator.

Current desktop flow:

```text
MainWindow
        ↓
ApplicationController
        ↓
Trading

or

Scanner

or

Dashboard
        ↓
Presenters
        ↓
Qt Workspaces
```

Business logic has been removed from the UI layer.

---

## Validation

Validated components:

- Trading Workspace
- Trading Pipeline
- AIMarketScanner
- AI Scanner Presenter
- IndicatorBuilder
- TradingConfig
- ApplicationController
- Dashboard integration
- Scanner integration

All manual integration tests passed.

---

## Current Status

Architecture

🟢 Stable

Backend

🟢 Stable

Desktop Integration

🟢 Stable

Technical Debt

🟢 Low

Documentation

🟢 Updated

---

## Next Sprint

Sprint 4.0

Objectives:

- Central logging
- Unified test runner
- Dashboard polish
- Equity visualization
- Watchlists
- Live refresh

# Sprint 3.10.5 — Architecture Stabilization (COMPLETED)

## Added

### Trading Intelligence

- Signal Fusion Engine
- Market Intelligence Engine
- Adaptive Decision Engine
- Position Sizing Engine

---

### Artificial Intelligence

- AI Context Builder
- AI Explanation Engine

Added explainable AI layer capable of generating deterministic reasoning for every trading decision.

---

### Trading Pipeline

Added a fully orchestrated trading pipeline connecting:

IndicatorPack

↓

Signal Fusion

↓

Market Intelligence

↓

Decision Engine

↓

Position Sizer

↓

AI Context

↓

AI Explanation

---

### Market Scanner

Added multi-asset scanning.

Capabilities:

- scan multiple assets
- rank opportunities
- identify actionable trades
- deterministic ranking model

---

### Backtesting

Added

- Backtest Engine
- Backtest Simulator
- Backtest Visualizer

Capabilities:

- deterministic trade simulation
- transaction fee model
- slippage model
- equity curve generation
- trade log generation
- performance summaries

---

## Changed

### Decision Models

Introduced standardized models:

- MarketSignal
- PositionContext
- DecisionInput
- TradeDecision
- SizedTradeDecision

These models now define service contracts across the trading architecture.

---

### Trading Pipeline

Refactored to remove temporary runtime objects.

Removed:

- dynamic `type(...)` objects
- implicit contracts

Pipeline now operates exclusively on explicit data models.

---

### Market Scanner

Refactored to use standardized pipeline outputs.

Improved:

- ranking
- orchestration
- architecture consistency

---

### Backtesting

Refactored:

- Backtest Engine
- Backtest Simulator
- Backtest Visualizer

Improved:

- deterministic PnL calculation
- fee handling
- slippage handling
- trade summaries
- equity reporting

---

## Architecture

Architecture Freeze v1.0 established.

Current execution flow:

```text
IndicatorPack
        ↓
Signal Fusion
        ↓
Market Intelligence
        ↓
Adaptive Decision
        ↓
Position Sizing
        ↓
AI Context
        ↓
AI Explanation
        ↓
Trading Pipeline
        ↓
Market Scanner
        ↓
Backtest Engine
        ↓
Backtest Visualizer
```

---

## Current Status

Backend trading architecture

🟢 Stable

Architecture consistency

🟢 High

Technical debt

🟢 Low

Documentation

🟢 Updated

---

## Next Sprint

### Sprint 3.11 — Desktop Trading Workspace

Objectives

- Trading Workspace
- Trading Presenter
- AI Decision Panel
- Scanner Workspace
- Backtest Workspace
- Equity Curve integration
- Qt Desktop integration