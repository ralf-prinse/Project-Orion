# PROJECT ORION

# ORION_MASTER_ARCHITECTURE

**Purpose:** Long-Term System Architecture

This document defines the permanent architectural principles of Project Orion.

Unlike PROJECT_STATUS or TODO, this document changes infrequently and should remain stable over time.

---

# Vision

Project Orion is a deterministic AI-assisted trading platform.

Its primary goal is to autonomously analyse financial markets, evaluate opportunities, manage portfolio risk and execute trading decisions through a modular, deterministic architecture.

Artificial Intelligence supports the system by explaining deterministic decisions, but never replaces deterministic calculations.

The architecture is designed to support future expansion while maintaining predictable behaviour.

---

# Long-Term Objectives

The long-term vision consists of four major phases.

## Phase 1

Deterministic Trading Platform

Objectives:

- deterministic calculations
- modular services
- regression tested
- reproducible results

Status:

```text
COMPLETE
```

---

## Phase 2

Autonomous Paper Trading

Objectives:

- autonomous market scanning
- automatic BUY execution
- portfolio persistence
- position monitoring
- automatic SELL execution
- trade journaling

Status:

```text
COMPLETE
```

---

## Phase 3

Professional Trading Platform

Objectives:

- dashboard
- analytics
- adaptive exits
- performance optimisation
- historical trade analysis

Status:

```text
IN PROGRESS
```

---

## Phase 4

Intelligent Trading Platform

Objectives:

- strategy optimisation
- self-learning analytics
- broker integration
- live trading

Status:

```text
PLANNED
```

---

# Core Principles

Every future implementation must preserve these principles.

---

## Deterministic Decision Making

Every trading decision must be deterministic.

The same market data must always produce identical output.

Randomness is prohibited.

---

## Single Responsibility

Every service has exactly one responsibility.

Examples:

IndicatorService

calculates indicators.

RiskEngine

validates risk.

PortfolioAllocator

allocates capital.

ExitEngine

executes exits.

DashboardService

provides dashboard data.

No service may perform responsibilities belonging to another service.

---

## Loose Coupling

Services communicate through models.

Services never depend directly on GUI components.

The GUI consumes services but never owns business logic.

---

## Testability

Every business service should be regression testable.

Large architectural changes require regression validation before merge.

---

# High-Level Architecture

```text
                   Market Data
                        │
                        ▼
              Market Data Providers
                        │
                        ▼
              Indicator Calculation
                        │
                        ▼
                 Analysis Layer
                        │
                        ▼
                  Signal Layer
                        │
                        ▼
                 Decision Layer
                        │
                        ▼
                   Risk Engine
                        │
                        ▼
              Portfolio Allocation
                        │
                        ▼
                 Trade Execution
                        │
                        ▼
              Portfolio Management
                        │
                        ▼
               Position Monitoring
                        │
                        ▼
                  Exit Engine
                        │
                        ▼
                 Trade Journal
                        │
                        ▼
                 Dashboard Layer
```

---

# Core Architecture

Project Orion consists of independent architectural layers.

Each layer owns exactly one responsibility and communicates through models.

No layer may bypass another layer.

The architecture intentionally favours clarity, maintainability and deterministic behaviour over implementation shortcuts.


# Architectural Layers

## 1. Market Layer

### Responsibility

Acquire market data from supported providers.

Current responsibilities:

- price retrieval
- historical candles
- volume
- metadata

The Market Layer never performs calculations.

Its responsibility ends after delivering raw market data.

---

## 2. Indicator Layer

### Responsibility

Transform raw market data into technical indicators.

Examples include:

- RSI
- EMA
- SMA
- ATR
- MACD
- Bollinger Bands
- Volume indicators

Rules:

- Indicators are deterministic.
- Indicators never generate trading decisions.
- Indicators never access portfolio information.

Output consists only of calculated indicator values.

---

## 3. Analysis Layer

### Responsibility

Interpret indicator values.

Examples:

- trend analysis
- momentum analysis
- volatility analysis
- support/resistance
- pressure analysis

The Analysis Layer produces market observations.

It never produces BUY or SELL decisions.

---

## 4. Signal Layer

### Responsibility

Convert analysis into standardized signals.

Examples:

```text
Bullish Trend

Bearish Trend

Momentum Increasing

Momentum Weakening

High Volatility

Low Volatility

Strong Buy Pressure

Strong Sell Pressure
```

Signals describe market conditions.

Signals never execute trades.

---

## 5. Decision Layer

### Responsibility

Generate deterministic trading decisions.

Possible outputs:

```text
BUY

HOLD

SELL
```

The Decision Layer combines:

- signals
- confidence
- scoring
- deterministic rules

Output is passed to the Risk Engine.

---

## 6. Risk Layer

### Responsibility

Validate every trading decision.

Checks include:

- available cash
- maximum position size
- maximum portfolio exposure
- duplicate positions
- confidence threshold
- configured risk limits

The Risk Layer may reject any trade.

It never modifies deterministic market analysis.

---

## 7. Portfolio Layer

### Responsibility

Maintain the current portfolio state.

Responsibilities:

- cash management
- open positions
- portfolio valuation
- realized P/L
- unrealized P/L
- exposure tracking

Portfolio state is the single source of truth for all positions.

---

## 8. Execution Layer

### Responsibility

Execute validated paper trades.

Components include:

- TradingCycle
- Paper Trading Engine
- Continuous Runner

Responsibilities:

- BUY execution
- SELL execution
- portfolio updates
- persistence

Execution never performs market analysis.

---

## 9. Position Management Layer

### Responsibility

Manage existing positions after execution.

Components:

- PortfolioRevaluationService
- PositionMonitor
- ExitEngine

Responsibilities:

- refresh prices
- evaluate exits
- execute exits
- update portfolio

This layer owns the complete lifecycle of open positions.

---

## 10. Journal Layer

### Responsibility

Record trading activity.

Current responsibilities:

- BUY events
- SELL events
- rejected decisions
- runtime history

Future versions may separate:

```text
Trade Journal

Decision Log
```

to improve analytics.

---

## 11. Dashboard Layer

### Responsibility

Present trading information.

Responsibilities:

- portfolio overview
- equity
- cash
- P/L
- winrate
- recent trades
- analytics

Dashboard components never modify portfolio state.

They consume information only.

---

# Artificial Intelligence

Artificial Intelligence is an assisting layer.

It never replaces deterministic trading logic.

AI may:

- summarize trades
- explain decisions
- generate human-readable reports
- describe portfolio status
- assist documentation

AI may never:

- calculate indicators
- generate confidence
- override BUY decisions
- override SELL decisions
- calculate risk
- size positions
- modify deterministic outputs

Deterministic calculations always remain authoritative.

---

# Data Flow

The permanent Orion execution flow is:

```text
Market Data
        │
        ▼
Indicators
        │
        ▼
Analysis
        │
        ▼
Signals
        │
        ▼
Decision
        │
        ▼
Risk Validation
        │
        ▼
Portfolio Allocation
        │
        ▼
Trade Execution
        │
        ▼
Portfolio Update
        │
        ▼
Position Monitor
        │
        ▼
Exit Engine
        │
        ▼
Trade Journal
        │
        ▼
Dashboard
```

No architectural layer may bypass another layer.

Every component has exactly one owner and one responsibility.

# Design Rules

The following design rules apply to every future implementation.

---

## Single Responsibility Principle

Every class should have exactly one reason to change.

Large classes should be decomposed into smaller services.

---

## Composition over Inheritance

Business functionality should be composed from services.

Inheritance should only be used where it provides a clear architectural benefit.

---

## Explicit Dependencies

Dependencies must be injected explicitly.

Hidden global state is prohibited.

---

## Immutable Models

Data models should be immutable whenever practical.

Business logic belongs in services, not models.

---

## Clear Ownership

Every feature must have exactly one owner.

Examples:

Portfolio valuation

Owner:

PortfolioRevaluationService

Exit execution

Owner:

ExitEngine

Dashboard data

Owner:

DashboardService

Duplicate ownership is prohibited.

---

# Dependency Rules

Architectural dependencies flow in one direction only.

```text
GUI
        │
        ▼
Controllers
        │
        ▼
Services
        │
        ▼
Repositories
        │
        ▼
Storage
```

The following dependencies are prohibited:

Repository → GUI

GUI → Repository

GUI → Database

Widgets → Business Logic

Repositories → Controllers

Business services must remain reusable outside the GUI.

---

# Testing Philosophy

Regression testing is mandatory.

Every completed feature should include automated validation.

Testing priorities:

1.

Unit Tests

↓

2.

Service Tests

↓

3.

Integration Tests

↓

4.

Long-running Runtime Validation

↓

5.

Documentation Update

---

## Regression Policy

Regression tests must remain green before:

- merging
- documentation updates
- release preparation

Current validation command:

```powershell
python run_tests.py
```

Regression failures must be resolved before continuing development.

---

# Documentation Policy

Project documentation follows strict ownership.

| Document | Responsibility |
|-----------|----------------|
| AI_CONTEXT.md | Development context |
| PROJECT_STATUS.md | Current implementation |
| TODO.md | Active backlog |
| CHANGELOG.md | Historical changes |
| ORION_MASTER_ARCHITECTURE.md | Permanent architecture |

Information should appear only once.

Cross-reference documents instead of duplicating content.

---

# Architectural Decision Records

Major architectural changes should follow the same process.

1.

Identify the problem.

↓

2.

Evaluate alternatives.

↓

3.

Choose one solution.

↓

4.

Implement.

↓

5.

Validate.

↓

6.

Document.

Architectural decisions should remain stable over time.

---

# Future Expansion Principles

Future functionality should extend existing architecture rather than replacing it.

Expected future additions include:

- dashboard GUI
- adaptive exits
- trade analytics
- self-learning optimisation
- broker integration
- live trading
- multi-market support
- strategy optimisation

New features should integrate into existing architectural layers whenever possible.

Creation of unnecessary architectural layers should be avoided.

---

# Architecture Stability

The architectural foundation of Orion is now considered stable.

Future development should primarily focus on:

- improving trading quality;
- improving analytics;
- improving performance;
- improving maintainability;
- improving observability.

Large architectural redesigns are discouraged unless a clear long-term benefit exists.

---

# Final Statement

Project Orion is designed around deterministic behaviour, modular services and long-term maintainability.

Artificial Intelligence complements deterministic trading logic by improving explainability, documentation and analytical capabilities.

Trading decisions remain deterministic.

The architecture prioritises:

- correctness;
- reproducibility;
- maintainability;
- scalability;
- testability.

These principles take precedence over implementation convenience.

---

# End of ORION_MASTER_ARCHITECTURE