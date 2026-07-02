# ORION MASTER ARCHITECTURE

---

# Architecture Version

**Architecture Freeze v1.1**

Status:

🟢 Stable

Current Phase:

Sprint 3.13 — Stabilization

---

# System Philosophy

Project Orion is a deterministic AI-assisted desktop trading platform.

Every architectural layer has exactly one responsibility.

Artificial Intelligence never performs investment calculations.

Deterministic services remain the single source of truth.

Artificial Intelligence explains deterministic results and prepares the platform for future conversational interaction.

---

# Core Principles

## Deterministic Services

Business logic exists only inside Services.

Identical input always produces identical output.

---

## Strong Layer Separation

```
State
        ↓
Services
        ↓
Orchestration
        ↓
Presenters
        ↓
Workspaces
        ↓
Qt Widgets
```

Business logic never exists inside the UI.

---

## Explainability

Every trading recommendation must be:

- deterministic
- reproducible
- traceable
- explainable

---

## Strong Data Contracts

Services communicate exclusively through explicit models.

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

```
Yahoo Finance
        ↓
IndicatorBuilder
        ↓
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
```

This deterministic pipeline represents the single source of truth.

---

# Multi-Asset Architecture

```
Trading Pipeline
        ↓
AIMarketScanner
        ↓
Opportunity Ranking
        ↓
AIScannerPresenter
        ↓
Scanner Workspace
```

Trading Workspace and Scanner Workspace now share the exact same Trading Pipeline.

No duplicate decision logic exists.

---

# Desktop Architecture

```
MainWindow
        ↓
ApplicationController
        ↓
Trading
Scanner
Dashboard
Portfolio
History
Settings
        ↓
Presenters
        ↓
Qt Workspaces
```

ApplicationController is the central UI orchestrator.

MainWindow contains no business logic.

---

# Configuration Architecture

```
TradingConfig
        ↓
IndicatorBuilder
ApplicationController
Backtest
Scanner
```

Configuration is centralized.

Hardcoded trading parameters should not exist elsewhere.

---

# Trading Intelligence Layer

Completed:

- Signal Fusion Engine
- Market Intelligence Engine
- Adaptive Decision Engine
- Position Sizing Engine

These services are deterministic and stateless.

---

# Artificial Intelligence Layer

Completed:

- AI Context Builder
- AI Explanation Engine

AI provides explanations only.

AI never influences deterministic calculations.

---

# Orchestration Layer

Completed:

- Trading Pipeline
- AIMarketScanner
- Backtest Engine
- Backtest Simulator
- Backtest Visualizer

Orchestration coordinates services.

It performs no calculations itself.

---

# Desktop Components

Completed:

- Trading Workspace
- Trading Workspace Presenter
- Dashboard Workspace
- Scanner Workspace
- AIScannerPresenter
- ApplicationController

Desktop responsibilities are fully separated from business logic.

---

# Current Status

Completed:

✅ Live Yahoo Finance

✅ IndicatorBuilder

✅ Trading Pipeline

✅ AI Market Scanner

✅ Trading Workspace

✅ Scanner Workspace

✅ ApplicationController

✅ TradingConfig

✅ Backtesting

Architecture Quality:

🟢 Stable

Technical Debt:

🟢 Low

---

# Sprint 4.0 Vision

The backend architecture is considered complete.

Future development focuses on:

- central logging
- automated testing
- dashboard enhancements
- watchlists
- equity visualization
- live monitoring
- broker abstraction

The architecture will be extended rather than redesigned.