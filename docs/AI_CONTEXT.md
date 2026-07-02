# ORION AI CONTEXT

---

# Current Phase

## Sprint 4.0.1 — Production Foundation

Project Orion has evolved into a deterministic AI-assisted desktop trading platform.

The architectural foundation is considered stable.

Development has transitioned from feature construction to production hardening.

Current priorities are:

- production stability
- centralized configuration
- centralized logging
- regression testing
- documentation
- professional desktop experience

Future development extends the architecture rather than redesigning it.

---

# Development Philosophy

Project Orion follows several non-negotiable engineering principles.

## Deterministic First

Every trading decision must be reproducible.

Identical market data must always generate identical output.

Artificial Intelligence never performs calculations.

---

## Layer Separation

Business logic exists only inside Services.

Presentation logic exists only inside Presenters.

Qt Widgets contain no business logic.

ApplicationController coordinates communication between UI and backend.

---

## Production Workflow

Every sprint follows the same workflow.

Feature

↓

Testing

↓

Documentation

↓

Git Commit

↓

GitHub Push

No sprint is considered complete until all five steps have finished.

---

# Core Trading Flow

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

AI Context

↓

AI Explanation

↓

Presenter

↓

Qt Desktop
```

Every layer has exactly one responsibility.

---

# AI Market Scanner

The AI Market Scanner uses the exact same Trading Pipeline as the Trading Workspace.

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

There is only one deterministic source of truth.

---

# Backtesting Flow

Historical Dataset

↓

MarketScanner

↓

BacktestEngine

↓

BacktestSimulator

↓

Equity Curve

↓

Trade Log

↓

Backtest Visualizer

---

# Current Infrastructure

Completed

✅ TradingConfig

✅ LoggingService

✅ YahooProvider

✅ IndicatorBuilder

✅ TradingPipeline

✅ AIMarketScanner

✅ BacktestEngine

✅ ApplicationController

✅ Trading Workspace

✅ Dashboard

✅ Scanner

---

# Logging Architecture

Every important backend component now logs to the centralized logging system.

Current coverage

✅ ApplicationController

✅ YahooProvider

✅ IndicatorBuilder

✅ TradingPipeline

✅ AIMarketScanner

✅ BacktestEngine

Log destination

```
logs/

orion.log
```

The logging system now provides a complete audit trail from user action to AI explanation.

---

# Testing

Regression testing is centralized.

Official command

```powershell
python run_tests.py
```

Current health

✅ All regression tests passing.

Regression tests are mandatory before every Git commit.

---

# Current Priority

Sprint 4.1

Objectives

- Dashboard 2.0
- Portfolio visualization
- Equity charts
- Watchlists
- Live refresh
- Portfolio analytics

No backend redesign is planned.

The current architecture is considered production-ready for continued expansion.

---

# Long-Term Vision

Project Orion will evolve into a professional AI-assisted desktop trading platform capable of:

- deterministic market analysis
- explainable AI
- historical backtesting
- portfolio intelligence
- watchlists
- paper trading
- broker integration

while preserving deterministic decision making as the single source of truth.