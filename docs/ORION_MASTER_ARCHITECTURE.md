# ORION MASTER ARCHITECTURE

---

# Architecture Version

**Architecture Freeze v1.0**

Status:

🟢 Stable

Current Phase:

Desktop Integration

---

# System Philosophy

Project Orion is a deterministic AI-assisted trading platform.

Every architectural layer has exactly one responsibility.

Artificial Intelligence never performs investment calculations.

Deterministic services always remain the source of truth.

Artificial Intelligence explains deterministic results and provides future user interaction capabilities.

---

# Core Principles

## Deterministic Services

Business logic exists only inside deterministic services.

Identical input always produces identical output.

---

## Strong Layer Separation

Application State

↓

Services

↓

Presenters

↓

Workspaces

↓

Renderers

↓

Qt Widgets

No business calculations may exist outside the Services layer.

---

## Explainability

Every trading decision must be:

- reproducible
- traceable
- explainable

Every recommendation must contain deterministic reasoning.

---

## Strong Data Contracts

Services communicate through explicit models.

Examples:

- IndicatorPack
- MarketSignal
- DecisionInput
- PositionContext
- TradeDecision
- AIContext

Temporary runtime objects are prohibited.

---

# Current Trading Architecture

```text
IndicatorPack
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
Backtest Simulator
        ↓
Backtest Visualizer
```

Every layer performs exactly one responsibility.

---

# Trading Intelligence Layer

## Signal Fusion Engine

Responsibilities

- normalize indicators
- calculate market pressure
- produce:

  - pressure_score
  - buy_pressure
  - sell_pressure
  - strength

The Signal Fusion Engine is the primary market scoring engine.

---

## Market Intelligence Engine

Responsibilities

- detect market regime
- classify volatility
- estimate market risk

Outputs

- regime
- volatility state
- risk score

This layer provides context only.

---

## Adaptive Decision Engine

Consumes:

MarketSignal

Produces:

- BUY
- SELL
- HOLD

with deterministic confidence and reasoning.

No position sizing is performed here.

---

## Position Sizing Engine

Consumes:

DecisionInput

Produces:

Recommended position size.

Uses:

- cash
- signal quality
- volatility

No trading decisions are made here.

---

# Artificial Intelligence Layer

## AI Context Builder

Builds a structured reasoning object.

Contains:

- trading signal
- market context
- confidence
- execution data
- risk
- features

Designed for future LLM integration.

---

## AI Explanation Engine

Transforms deterministic output into human-readable explanations.

Examples:

- Strong BUY signal
- Bullish market regime
- Low volatility
- High confidence

The explanation engine never changes decisions.

---

# Orchestration Layer

## Trading Pipeline

Coordinates all deterministic services.

Responsibilities

- execute pipeline
- build AI context
- generate explanation

No calculations occur inside orchestration.

---

## Market Scanner

Responsibilities

- execute Trading Pipeline for multiple assets
- rank opportunities
- expose actionable trades

Supports deterministic portfolio-wide scanning.

---

## Backtesting

Current components

- Backtest Engine
- Backtest Simulator
- Backtest Visualizer

Current capabilities

- deterministic simulation
- fee model
- slippage model
- equity curve
- trade log
- performance summaries

---

# Desktop Architecture

Current desktop architecture

```text
Application
        ↓
Workspace Coordinator
        ↓
Workspace Controller
        ↓
Presenter Layer
        ↓
Workspace
        ↓
Renderer
        ↓
Qt Widgets
```

Responsibilities

Services

- calculations

Presenters

- mapping

Workspaces

- composition

Renderers

- visualization

Qt

- interaction

---

# Current Status

Completed

✅ Signal Fusion

✅ Market Intelligence

✅ Adaptive Decision

✅ Position Sizing

✅ AI Context

✅ AI Explanation

✅ Trading Pipeline

✅ Market Scanner

✅ Backtest Engine

✅ Backtest Simulator

✅ Backtest Visualizer

Architecture quality:

🟢 Stable

Technical debt:

🟢 Low

---

# Next Evolution

Sprint 3.11

Desktop Trading Workspace

Planned

- Trading Workspace
- Trading Presenter
- Scanner Workspace
- Backtest Workspace
- Equity Curve UI
- AI Decision Panel
- Market Pressure Dashboard

The backend architecture should remain unchanged.

Future work extends the architecture rather than redesigning it.

---

# Long-Term Vision

Project Orion evolves into a professional AI-assisted desktop trading platform.

Future capabilities include:

- live market data
- portfolio optimization
- broker integration
- paper trading
- news ingestion
- sentiment analysis
- macro event analysis
- explainable AI
- portfolio intelligence

while preserving deterministic decision making as the foundation of the system.