# ORION MASTER ARCHITECTURE

---

# Architecture Version

**Architecture Freeze v1.2**

Status

🟢 Production Foundation Complete

Current Phase

Sprint 4.1 — Dashboard Evolution

---

# System Philosophy

Project Orion is a deterministic AI-assisted desktop trading platform.

Every architectural layer has exactly one responsibility.

Artificial Intelligence never performs investment calculations.

Artificial Intelligence explains deterministic results.

The deterministic pipeline remains the single source of truth.

---

# Engineering Principles

## Deterministic First

Identical market data must always produce identical trading decisions.

No randomness is permitted.

---

## Separation of Responsibilities

Business Logic

↓

Orchestration

↓

Presentation

↓

Qt UI

Every layer communicates through explicit models.

---

## Explainability

Every recommendation must be:

- deterministic
- reproducible
- traceable
- explainable

---

## Production Workflow

Every sprint follows:

Feature

↓

Testing

↓

Documentation

↓

Git Commit

↓

GitHub Push

A sprint is not finished before all five stages have completed.

---

# Production Architecture

```
User
        ↓
ApplicationController
        ↓
YahooProvider
        ↓
IndicatorBuilder
        ↓
IndicatorPack
        ↓
TradingPipeline
        ↓
Signal Fusion
        ↓
Market Intelligence
        ↓
Adaptive Decision
        ↓
Position Sizing
        ↓
AI Context Builder
        ↓
AI Explanation Engine
        ↓
Presenters
        ↓
Qt Desktop
```

This deterministic pipeline is the only source of trading decisions.

---

# AI Market Scanner

```
ApplicationController
        ↓
YahooProvider
        ↓
IndicatorBuilder
        ↓
TradingPipeline
        ↓
AIMarketScanner
        ↓
AIScannerPresenter
        ↓
Scanner Workspace
```

Trading Workspace and AI Scanner always share the exact same Trading Pipeline.

No duplicate business logic exists.

---

# Backtesting Architecture

```
Historical Dataset
        ↓
MarketScanner
        ↓
BacktestEngine
        ↓
BacktestSimulator
        ↓
Trade Log
        ↓
Equity Curve
        ↓
BacktestVisualizer
```

Backtesting reuses deterministic production logic.

---

# Configuration Architecture

```
TradingConfig
        ↓
YahooProvider

IndicatorBuilder

TradingPipeline

ApplicationController

AIMarketScanner

Backtesting
```

Configuration is centralized.

Hardcoded values should not exist elsewhere.

---

# Logging Architecture

```
ApplicationController
        ↓
YahooProvider
        ↓
IndicatorBuilder
        ↓
TradingPipeline
        ↓
AIMarketScanner
        ↓
BacktestEngine
```

All important backend components use LoggingService.

Output:

```
logs/orion.log
```

Logging provides a complete audit trail.

---

# Regression Testing

Regression validation is centralized.

Official command

```powershell
python run_tests.py
```

Current suite

- Trading Pipeline
- Decision Smoke
- Intelligence Layer
- AI Market Scanner
- AI Scanner Presenter
- Backtest Visualizer

Regression testing is mandatory before releases.

---

# Current Production Components

Completed

✅ TradingConfig

✅ LoggingService

✅ YahooProvider

✅ IndicatorBuilder

✅ TradingPipeline

✅ Signal Fusion Engine

✅ Market Intelligence Engine

✅ Adaptive Decision Engine

✅ Position Sizing Engine

✅ AI Context Builder

✅ AI Explanation Engine

✅ AIMarketScanner

✅ BacktestEngine

✅ BacktestSimulator

✅ BacktestVisualizer

✅ Trading Workspace

✅ Dashboard

✅ Scanner

✅ ApplicationController

---

# Project Health

Architecture

🟢 Stable

Backend

🟢 Stable

Desktop

🟢 Stable

Logging

🟢 Complete

Regression Tests

🟢 Passing

Technical Debt

🟢 Low

Documentation

🟢 Current

---

# Sprint 4.1 Vision

Development now shifts from backend infrastructure to user experience.

Primary objectives:

- Dashboard 2.0
- Portfolio Overview
- Equity Visualization
- Confidence Gauges
- Watchlists
- Live Refresh

No architectural redesign is expected.

Future development extends the existing production architecture.