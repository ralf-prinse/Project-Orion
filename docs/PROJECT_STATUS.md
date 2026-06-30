# PROJECT ORION

# PROJECT STATUS

Project Version: v0.8.3.3-alpha

**Document Version:** 2.0

**Last Updated:** June 2026

---

Current Milestone

✅ Sprint 8.3.3 – Explainability Framework completed
---

# 1. Executive Summary

Project Orion is a professional deterministic swing-trading platform for the United States stock market.

Unlike conventional stock scanners, Orion is designed as a layered decision-support platform in which every recommendation originates from transparent and reproducible calculations.

Artificial Intelligence is intentionally **not** responsible for investment decisions.

Instead, Orion combines deterministic technical analysis, modular processing pipelines and explainable scoring models to generate professional trading signals.

Every processing layer has a single responsibility and communicates only through clearly defined data models.

This architecture enables Orion to grow from a technical scanner into a complete investment platform without requiring architectural redesign.

Current implementation status:

- ✅ Universe Layer
- ✅ Market Data Layer
- ✅ Historical Data Layer
- ✅ Indicator Library
- ✅ Indicator Engine
- ✅ Analysis Layer
- ✅ Signal Layer
- ✅ Decision Layer Foundation
- ✅ Explainability Framework
- ⏳ Portfolio Layer
- ⏳ Risk Layer
- ⏳ Trade Planning
- ⏳ Artificial Intelligence Layer
- ⏳ Professional GUI
---
# 2. Current Architecture

Project Orion follows a deterministic layered architecture.

```text
Universe Layer
        ↓
Market Data Layer
        ↓
Historical Data Layer
        ↓
Indicator Engine
        ↓
Analysis Layer
        ↓
Signal Layer
        ↓
Decision Layer
        ↓
Portfolio Layer
        ↓
Risk Manager
        ↓
Trade Planner
        ↓
Artificial Intelligence Layer
        ↓
Graphical User Interface


# 3. Current Development Status

## Development Phase

**Alpha Development**

Project Orion has successfully completed its analytical foundation and has entered the signal generation phase.

The platform now contains a fully deterministic pipeline from historical market data to deterministic investment decisions.
Current implementation flow:

```text
Historical Data

↓

Indicator Engine

↓

Analysis Layer

↓

Signal Layer

↓

Decision Layer
```

The next major milestone is the implementation of Position Sizing and the Portfolio Engine.
---

## Completed Infrastructure

The following infrastructure is considered production-ready within the current alpha phase.

### Universe Layer

Status: ✅ Completed

Capabilities:

- Download US stock universes
- Merge multiple exchanges
- Remove duplicates
- Store locally
- Fast local loading

Current universe:

Approximately **6,200+ US listed stocks**

---

### Market Data Layer

Status: ✅ Completed

Capabilities:

- Yahoo Finance integration
- Batch quote downloads
- Quote caching
- Retry handling
- Error handling

---

### Historical Data Layer

Status: ✅ Completed

Capabilities:

- Historical OHLCV downloads
- Daily timeframe
- Local caching
- Automatic cache reuse
- Incremental updates

---

### Indicator Library

Status: ✅ Completed

Currently implemented indicators:

- SMA20
- SMA50
- EMA20
- EMA50
- RSI14
- MACD
- ATR14
- Bollinger Bands
- ADX14

All indicators are fully reusable and isolated from business logic.

---

### Indicator Engine

Status: ✅ Completed

Responsibilities:

- Calculate technical indicators
- Calculate benchmark-aware metrics
- Produce unified IndicatorResult objects

The Indicator Engine never performs technical interpretation.

---

### Analysis Layer

Status: ✅ Completed

Components:

- AnalyzerRegistry
- AnalysisEngine
- BaseAnalyzer
- TrendAnalyzer
- MomentumAnalyzer
- VolatilityAnalyzer
- StructureAnalyzer
- VolumeAnalyzer
- MarketRegimeAnalyzer
- RelativeStrengthAnalyzer
- CandlestickPatternAnalyzer

Current capabilities:

- Technical scoring
- Market context
- Relative strength analysis
- Raw candlestick analysis
- Configurable score weighting
- Deterministic overall scoring

The Analysis Layer represents the analytical foundation of Project Orion.

---

### Signal Layer

Status: ✅ Completed

Components:

- SignalEngine
- SignalRegistry
- BaseSignalAnalyzer
- EntrySignalAnalyzer
- SignalResult
- Signal configuration

Current capabilities:

- Deterministic BUY signals
- Deterministic WATCH signals
- Deterministic SELL signals
- Deterministic IGNORE signals
- Configurable signal thresholds
- Registry-driven orchestration

The Signal Layer converts technical analysis into deterministic trading signals while remaining fully modular.

---

### Decision Layer

Status: ✅ Foundation Completed

Components:

- DecisionEngine
- DecisionRegistry
- DecisionContext
- DecisionState
- DecisionResult
- BaseDecisionAnalyzer
- SignalValidationAnalyzer
- PortfolioValidationAnalyzer
- RiskValidationAnalyzer
- DecisionAssemblerAnalyzer

Current capabilities:

- Deterministic decision pipeline
- Portfolio validation
- Risk validation
- Decision orchestration
- Structured decision state

The Decision Layer converts deterministic trading signals into deterministic investment decisions while remaining fully modular.
# 3. Development Philosophy

Project Orion is developed according to several fundamental engineering principles.

## Deterministic Analysis

Every recommendation must be reproducible.

No investment recommendation may depend on randomness or opaque AI reasoning.

---

## Modular Architecture

Every subsystem performs a single responsibility.

Modules communicate through well-defined interfaces while remaining independent from each other.

---

## Explainability

Every recommendation should be explainable.

Every score should be traceable.

Every calculation should be reproducible.

---

## Incremental Development

The project is developed through small, fully functional sprints.

Every sprint must result in:

* Working software
* Passing tests
* Updated documentation
* Git commit
* GitHub push

A sprint is only considered complete after all five requirements have been satisfied.

---

## Long-Term Objective

The long-term objective is to transform Orion from a stock scanner into a complete AI-assisted trading platform capable of supporting the entire investment workflow, from market analysis to portfolio management and trade execution planning.

This objective is achieved through continuous incremental development rather than large architectural rewrites.


# 4. Roadmap

Project Orion follows a strictly incremental development strategy.

Each sprint introduces one clearly defined capability while preserving the existing architecture.

---

## Completed

### Infrastructure

- ✅ Universe Layer
- ✅ Market Data Layer
- ✅ Historical Data Layer
- ✅ Quote Cache
- ✅ Historical Cache

### Analysis

- ✅ Indicator Library
- ✅ Indicator Engine
- ✅ Analyzer Framework
- ✅ AnalyzerRegistry
- ✅ AnalyzerRunner
- ✅ Analysis Layer

### Technical Analysis

- ✅ Trend Analysis
- ✅ Momentum Analysis
- ✅ Volatility Analysis
- ✅ Structure Analysis
- ✅ Volume Analysis
- ✅ Market Regime Analysis
- ✅ Relative Strength Analysis
- ✅ Candlestick Pattern Analysis

### Signal Layer

- ✅ SignalResult
- ✅ SignalRegistry
- ✅ Signal Threshold Configuration
- ✅ EntrySignalAnalyzer
- ✅ SignalEngine

---

## Next Sprint

#### Sprint 8.4 — Position Sizing Engine

Objectives:

- Introduce PositionSizingAnalyzer
- Calculate recommended position sizes
- Support configurable risk-per-trade
- Integrate with Decision Layer
- Full unit test coverage

---

## Upcoming Milestones

### Sprint 8.4

Position Sizing

### Sprint 8.5

Portfolio Engine

### Sprint 8.6

Risk Manager

### Future

- Trade Planner
- Paper Trading
- Broker Integration
- AI Assistant
- Professional Desktop GUI

All future development will continue following the established layered architecture.

# 5. Architecture Principles

Project Orion is built around a number of core architectural principles.

## Deterministic Behaviour

Identical input must always produce identical output.

No randomness is allowed inside:

- indicator calculations
- analysis
- signal generation
- decision making
- portfolio calculations

---

## Single Responsibility

Every component performs exactly one responsibility.

Examples:

IndicatorEngine

Calculates indicators.

AnalysisEngine

Coordinates analyzers.

SignalEngine

Coordinates signal analyzers.

AnalyzerRunner

Executes registered analyzers.

---

## Registry Pattern

Every expandable processing layer uses a registry.

Current registries:

- AnalyzerRegistry
- SignalRegistry

Future:

- DecisionRegistry

---

## Composition over Inheritance

Shared infrastructure is implemented through reusable components instead of deep inheritance hierarchies.

AnalyzerRunner is the first implementation of this philosophy.

Future processing engines will reuse this infrastructure.

---

## Explainability

Every recommendation must remain explainable.

Every score must be traceable.

Artificial Intelligence explains deterministic calculations but never replaces them.

# 6. Project Health

Current Version

v0.8.3.3-alpha

Current Status

🟢 Active Development

Architecture

🟢 Stable

Documentation

🟢 Current

Regression Tests

🟢 58 tests passing

Technical Debt

🟢 Low

Overall Assessment

Project Orion has successfully completed the analytical foundation of the platform.

The project now contains:

- deterministic data acquisition
- deterministic technical analysis
deterministic signal generation

The next phase will transform trading signals into deterministic investment decisions through the introduction of the Decision Layer.

The long-term architecture remains stable and no architectural redesigns are currently anticipated.