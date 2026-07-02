# ORION AI CONTEXT

## 🧠 Current Focus

Orion is no longer an analytics dashboard.

It has evolved into a modular AI-assisted trading decision platform built on a deterministic service architecture.

The current focus is to stabilize the AI trading core before integrating live market data and the Qt user interface.

---

# Current Architecture

The trading system is organized into independent layers.

Indicator Data
        ↓
Signal Fusion Engine
        ↓
Market Intelligence Engine
        ↓
Adaptive Decision Engine
        ↓
Position Sizing Engine
        ↓
AI Context Builder
        ↓
AI Explanation Engine
        ↓
Trading Pipeline
        ↓
Market Scanner
        ↓
Backtest Engine
        ↓
Backtest Visualizer

Each layer has a single responsibility.

---

# Core Architecture Rules

Services
- Pure deterministic logic
- No UI
- No rendering
- No state mutation

Presenters
- UI mapping only

Workspaces
- UI composition only

Renderers
- Drawing only

Data Flow

State
→ Services
→ Presenters
→ Workspaces
→ Renderers

The UI never performs calculations.

---

# Trading Intelligence

## Signal Fusion Engine

Responsible for combining normalized indicators into one market pressure model.

Outputs:

- pressure_score
- buy_pressure
- sell_pressure
- strength

This is now the primary trading signal.

---

## Market Intelligence

Provides contextual market information.

Outputs include:

- regime
- volatility state
- risk score

It no longer owns the primary trading score.

---

## Adaptive Decision Engine

Consumes MarketSignal.

Produces:

- BUY
- SELL
- HOLD

with confidence and reasoning.

The decision engine no longer performs position sizing.

---

## Position Sizing

Consumes:

DecisionInput

Uses:

- available cash
- normalized signal score
- volatility

Outputs:

- position size

Only sizing.
No trading decisions.

---

## AI Context Builder

Produces a complete AI reasoning object.

AIContext contains:

- signal information
- market regime
- volatility
- risk
- decision
- confidence
- explanation inputs
- execution information

This object is intended for future LLM reasoning.

---

## AI Explanation Engine

Produces human-readable reasoning.

Example:

- Strong BUY signal
- Bullish regime
- Low volatility
- Buy pressure dominates
- High confidence

The explanation layer never influences decisions.

---

# Multi-Asset System

MarketScanner executes the full trading pipeline for multiple assets.

Responsibilities:

- execute pipeline
- collect results
- rank opportunities
- identify actionable trades

---

# Backtesting

Current backtesting stack:

Backtest Engine

↓

Backtest Simulator

↓

Backtest Visualizer

Current capabilities:

- deterministic simulation
- fees
- slippage
- equity curve
- trade log
- performance summary

---

# Stabilization Status

Architecture Freeze v1.0 completed.

Major improvements:

- Removed temporary runtime objects
- Introduced explicit data models
- DecisionInput introduced
- MarketSignal standardized
- PositionContext standardized
- TradingPipeline simplified
- Scanner stabilized
- Backtest stack stabilized

---

# Current Project Status

The backend trading architecture is considered stable.

Implemented:

✅ Signal Fusion

✅ Market Intelligence

✅ Adaptive Decision Engine

✅ Position Sizing

✅ AI Context

✅ AI Explanation

✅ Trading Pipeline

✅ Market Scanner

✅ Backtest Engine

✅ Backtest Simulator

✅ Backtest Visualizer

---

# Immediate Next Phase

The next development phase is UI integration.

Goals:

- Trading Workspace
- Live pipeline execution
- Decision visualization
- AI explanation panel
- Equity curve visualization
- Scanner dashboard

No additional AI features should be added before the UI is connected to the stabilized backend.

---

# Long-Term Vision

Orion becomes an AI-native trading platform capable of transforming:

Market Data

+

Portfolio State

+

Future News & Sentiment

+

Risk Models

↓

Explainable AI Trading Decisions

with a clean, deterministic and production-ready architecture.