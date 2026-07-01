# PROJECT ORION

# AI_CONTEXT

**Version:** v0.8.5-alpha

**Document Version:** 2.0

---

# Purpose

This document provides the complete engineering context required for any future AI assistant or developer working on Project Orion.

Unlike the Master Architecture, this document focuses on practical software development.

It defines:

- engineering philosophy
- architectural rules
- development workflow
- coding standards
- current implementation status
- future development direction

Together with:

- ORION_MASTER_ARCHITECTURE.md
- PROJECT_STATUS.md

this document forms the complete development context for Project Orion.

---

# 1. Project Overview

Project Orion is a professional deterministic swing-trading platform for the United States stock market.

Its objective is not to predict markets using opaque Artificial Intelligence.

Instead, Orion produces deterministic investment decisions using transparent technical analysis and modular processing pipelines.

Artificial Intelligence is intentionally positioned as an explanation layer.

AI may explain deterministic calculations but never replace them.

Every investment recommendation must remain:

- deterministic
- reproducible
- explainable
- testable

# 2. Current Architecture

Project Orion follows a deterministic layered architecture.

Each processing layer has exactly one responsibility and communicates only through well-defined data models.

```text
Universe Layer
        │
        ▼
Market Data Layer
        │
        ▼
Historical Data Layer
        │
        ▼
Indicator Engine
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
Portfolio Layer
        │
        ▼
Risk Manager
        │
        ▼
Trade Planner
        │
        ▼
Artificial Intelligence Layer
        │
        ▼
Graphical User Interface
```

---

## Current Core Infrastructure

Project Orion currently contains the following reusable core infrastructure:

### AnalyzerRunner

Provides generic deterministic execution of registry-driven processing pipelines.

Currently used by:

- Analysis Layer
- Signal Layer
- Decision Layer

Future layers should reuse this infrastructure whenever practical.

---

### Explainability Framework

The Explainability Framework provides structured explanations for deterministic decisions.

Core components:

- ExplanationItem
- ExplanationSeverity
- ExplanationReport

Future processing layers should use this framework instead of free-text explanations.

---

## Current Processing Layers

### Indicator Layer

Responsibilities:

- Mathematical indicator calculations
- Benchmark-aware calculations
- Produce IndicatorResult

IndicatorEngine never performs interpretation.

---

### Analysis Layer

Responsibilities:

- Interpret technical indicators
- Evaluate market structure
- Produce AnalysisResult

Current analyzers:

- TrendAnalyzer
- MomentumAnalyzer
- VolatilityAnalyzer
- StructureAnalyzer
- VolumeAnalyzer
- MarketRegimeAnalyzer
- RelativeStrengthAnalyzer
- CandlestickPatternAnalyzer

AnalysisEngine acts purely as an orchestrator.

---

### Signal Layer

Responsibilities:

- Convert AnalysisResult into SignalResult.
- Apply deterministic signal thresholds.
- Produce trading signals.

SignalEngine contains no business logic.

Signal generation is delegated to specialised analyzers through SignalRegistry.

---

### Decision Layer

Responsibilities:

- Validate trading signals.
- Validate portfolio constraints.
- Validate risk constraints.
- Produce deterministic investment decisions.

Current pipeline:

```text
SignalValidationAnalyzer

↓

PortfolioValidationAnalyzer

↓

RiskValidationAnalyzer

↓

DecisionAssemblerAnalyzer
```

DecisionEngine orchestrates the pipeline through DecisionRegistry and AnalyzerRunner.

---

Future layers should follow the same registry-driven architecture whenever practical.

# 3. Engineering Philosophy

Project Orion follows a number of fundamental engineering principles.

These principles take precedence over implementation speed.

---

## Architecture First

Architecture always takes priority over new functionality.

Whenever new functionality is introduced, it should extend the existing architecture instead of forcing architectural redesign.

Long-term maintainability always outweighs short-term convenience.

---

## Deterministic Processing

Every processing layer must produce identical output when supplied with identical input.

Randomness must never influence:

- technical analysis
- signal generation
- decision making
- portfolio management
- risk management

Determinism is considered a core architectural requirement.

---

## Single Responsibility

Every component should perform one clearly defined task.

Examples:

IndicatorEngine

Calculates indicators.

AnalysisEngine

Coordinates analyzers.

SignalEngine

Coordinates signal analyzers.

DecisionEngine

Coordinates decision analyzers.

Business logic belongs inside specialised analyzers rather than orchestration layers.

---

## Registry-Driven Architecture

Every expandable processing layer should be registry driven.

Current registry implementations:

- AnalyzerRegistry
- SignalRegistry
- DecisionRegistry

Future layers should reuse this architectural pattern whenever practical.

---

## Explainability

Every recommendation must be explainable.

Every decision must be traceable.

Every explanation should originate from deterministic calculations.

Artificial Intelligence explains deterministic results but never creates investment decisions.

---

## Composition over Inheritance

Reusable infrastructure should be shared through composition rather than deep inheritance hierarchies.

Examples include:

- AnalyzerRunner
- Explainability Framework

Future infrastructure should continue following this principle.

---

## Incremental Development

Project Orion evolves through small, fully completed sprints.

Each sprint should include:

- architecture
- implementation
- unit tests
- regression tests
- documentation
- Git commit
- GitHub push

No sprint is considered complete before all of these steps have been finished.

# 4. Current Development Status

## Current Version

Project Orion v0.8.6-alpha

---

## Completed Layers

The following layers are considered implemented and operational.

### Infrastructure

- Universe Layer
- Market Data Layer
- Historical Data Layer
- Quote Cache
- Historical Cache

---

### Analysis

- Indicator Library
- Indicator Engine
- AnalysisEngine
- AnalyzerRegistry
- AnalyzerRunner

Implemented analyzers:

- TrendAnalyzer
- MomentumAnalyzer
- VolatilityAnalyzer
- StructureAnalyzer
- VolumeAnalyzer
- MarketRegimeAnalyzer
- RelativeStrengthAnalyzer
- CandlestickPatternAnalyzer

---

### Signal Layer

Implemented:

- SignalEngine
- SignalRegistry
- BaseSignalAnalyzer
- EntrySignalAnalyzer
- SignalResult
- Signal Threshold Configuration

The Signal Layer converts deterministic technical analysis into deterministic trading signals.

---

### Decision Layer

Implemented:

- DecisionEngine
- DecisionRegistry
- BaseDecisionAnalyzer
- DecisionContext
- DecisionState
- DecisionResult

Current decision analyzers:

- SignalValidationAnalyzer
- PortfolioValidationAnalyzer
- RiskValidationAnalyzer
- DecisionAssemblerAnalyzer

The Decision Layer converts deterministic trading signals into deterministic investment decisions.

---

### Explainability

Implemented:

- ExplanationItem
- ExplanationSeverity
- ExplanationReport

The Explainability Framework is reusable across all processing layers and forms the foundation for future AI explanations, logging, reporting and audit trails.

---


### Risk Manager

Implemented:

- RiskManager
- RiskRegistry
- BaseRiskAnalyzer
- RiskProfile
- RiskContext
- RiskResult

Current risk analyzers:

- RiskSummaryAnalyzer
- TradeRiskAnalyzer
- PortfolioRiskAnalyzer
- DrawdownAnalyzer
- CapitalProtectionAnalyzer
- PositionExposureRiskAnalyzer

The Risk Manager validates capital protection and risk exposure while remaining separate from portfolio management, decision assembly and trade planning.

## Current Test Status

Current regression status:

- Analysis Layer
- Signal Layer
- Decision Layer
- Core Infrastructure

Current result:

86 passing tests

No known regressions.

---

# 5. Current Roadmap

The immediate development roadmap is:

### Sprint 8.4

Position Sizing Engine

Objectives:

- PositionSizingAnalyzer
- configurable risk-per-trade
- recommended position size
- Decision Layer integration

---

### Sprint 8.5

Portfolio Engine

Objectives:

- portfolio state
- portfolio validation
- exposure management
- registry-driven Portfolio Engine

---

### Sprint 8.6

Risk Manager

Status: Completed

Implemented:

- portfolio risk validation
- position risk validation
- drawdown validation
- capital protection

---

Next roadmap:

- Trade Planner
- Paper Trading
- Broker Integration
- Professional Desktop GUI
- Artificial Intelligence Explanation Layer

---
# 6. Development Workflow

Every development sprint follows the same workflow.

1. Design the architecture.
2. Implement the functionality.
3. Write unit tests.
4. Execute regression tests.
5. Update documentation.
6. Commit to Git.
7. Push to GitHub.

A sprint is only considered complete after all seven steps have been successfully completed.

---

# 7. Coding Standards

Project Orion follows the following coding conventions.

## Readability

Readable code is preferred over compact or clever implementations.

Future developers should understand every module quickly.

---

## Type Hints

Type hints should be used whenever practical.

---

## Complete Files

When a file changes substantially, complete file rewrites are preferred over partial snippets.

This minimizes copy/paste errors and keeps implementations consistent.

---

## Low Coupling

Modules should communicate only through clearly defined models.

Business logic should never leak into orchestration layers.

---

## High Cohesion

Each module should perform exactly one responsibility.

Examples:

- IndicatorEngine → calculations
- AnalysisEngine → orchestration
- SignalEngine → orchestration
- DecisionEngine → orchestration
- AnalyzerRunner → pipeline execution

---

# 8. Testing Standards

Testing is considered part of implementation.

Every significant module should have dedicated unit tests.

Regression tests should always be executed before documentation is updated.

Tests should remain:

- deterministic
- isolated
- reproducible
- independent from external services whenever practical

---

# 9. Documentation Standards

Documentation is treated as part of the software.

After every completed sprint the following documents should be reviewed:

- CHANGELOG.md
- TODO.md
- PROJECT_STATUS.md
- AI_CONTEXT.md

ORION_MASTER_ARCHITECTURE.md should only be updated when the long-term architecture itself changes.

Documentation should always reflect the actual implementation.

---

# 10. Instructions for Future AI Sessions

Future AI sessions should treat Project Orion as a professional software product rather than a prototype.

Always follow these principles:

- Respect the existing architecture.
- Prefer adding new modules over modifying existing ones.
- Keep orchestration separate from business logic.
- Preserve deterministic behaviour.
- Prefer architecture over short-term convenience.
- Avoid introducing technical debt.
- Update tests before updating documentation.
- Keep every layer modular and independently testable.

The preferred development order remains:

Architecture

↓

Implementation

↓

Testing

↓

Regression Tests

↓

Documentation

↓

Git Commit

↓

GitHub Push

This document, together with:

- ORION_MASTER_ARCHITECTURE.md
- PROJECT_STATUS.md

forms the complete development context for every future Orion development session.

---

# Sprint 8.4 Update

Sprint 8.4 introduced the Position Sizing Engine.

Implemented components:

- PositionSizingResult
- PositionSizingAnalyzer
- DecisionContext position sizing inputs
- DecisionState position_sizing output
- DecisionResult position_sizing output
- DecisionRegistry integration before DecisionAssemblerAnalyzer

The official regression command is now:

```bash
py -m pytest tests
```

Current validation result:

```text
63 passed
```

Position sizing remains deterministic and does not make investment decisions. It only enriches the Decision Layer output with recommended sizing information.


# Sprint 8.5 Update

Sprint 8.5 introduced the Portfolio Engine.

Implemented components:

- PortfolioState
- PortfolioPosition
- PortfolioContext
- PortfolioResult
- PortfolioEngine
- PortfolioRegistry
- BasePortfolioAnalyzer
- PortfolioSummaryAnalyzer
- CashValidationAnalyzer
- PositionCountAnalyzer
- ExistingPositionAnalyzer
- ExposureAnalyzer

Architectural rules:

- Portfolio Engine lives in `services/portfolio`.
- Portfolio Engine is registry-driven and uses AnalyzerRunner.
- Portfolio Engine evaluates portfolio state, cash, position count, existing positions and exposure.
- Portfolio Engine does not perform technical analysis, signal generation, decision assembly, position sizing, risk management or trade planning.
- Future Decision Layer integration should consume PortfolioResult instead of duplicating portfolio logic.

Validation:

- Official regression suite: `tests`
- Result: 73 passing tests
