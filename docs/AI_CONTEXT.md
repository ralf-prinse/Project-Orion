# PROJECT ORION

# AI_CONTEXT

**Purpose**

This document provides the development context required for any future AI assistant or developer working on Project Orion.

Unlike the Master Architecture, this document focuses on practical development rules, engineering philosophy and the current implementation approach.

Every future development session should use this document together with:

* ORION_MASTER_ARCHITECTURE.md
* PROJECT_STATUS.md

Together these three documents form the complete source of truth for Project Orion.

---

# 1. Project Overview

Project Orion is a deterministic swing-trading platform designed for the United States stock market.

The objective is **not** to predict future prices using opaque AI models.

Instead, Orion performs transparent technical analysis using deterministic algorithms that can always be reproduced and explained.

Artificial Intelligence is used only as a communication layer.

AI never makes investment decisions.

Every recommendation originates from deterministic calculations.

---

# 2. Development Philosophy

Project Orion follows several strict engineering principles.

## Architecture First

Architecture always takes priority over implementation speed.

Whenever a new feature is introduced, it must fit into the existing architecture rather than forcing architectural changes.

Short-term convenience should never compromise long-term maintainability.

---

## Small Working Sprints

Development proceeds through small, fully functional sprints.

Every sprint must produce working software.

Incomplete implementations should be avoided whenever possible.

Each sprint concludes with:

* Working implementation
* Successful tests
* Documentation updates
* Git commit
* GitHub push

Only then is a sprint considered complete.

---

## Incremental Development

Large rewrites are avoided.

Instead, Project Orion evolves through incremental improvements.

Future functionality should extend existing modules rather than replacing them.

This philosophy has already proven successful during the implementation of:

* Universe Layer
* Market Data Layer
* Historical Data Layer
* Analysis Layer

---

## Deterministic Software

Every calculation should produce identical results when supplied with identical input.

Randomness should never influence:

* Technical analysis
* Signal generation
* Decision making
* Portfolio calculations
* Risk management

Reproducibility is considered essential.

---

## Explainability

Every recommendation should be explainable.

Every score should be traceable.

Every AI explanation should reference deterministic calculations rather than generating speculative reasoning.

Transparency always takes priority over sophistication.

---

## Current Development Phase

Current Version:

Project Orion v0.8.1-alpha

Current Phase:

Advanced Modular Analysis Layer

Current Sprint Status:

Sprint 8.1.1 completed.

The Analysis Layer now consists of eight specialised analyzers:

- TrendAnalyzer
- MomentumAnalyzer
- VolatilityAnalyzer
- StructureAnalyzer
- VolumeAnalyzer
- MarketRegimeAnalyzer
- RelativeStrengthAnalyzer
- CandlestickPatternAnalyzer

AnalysisEngine functions exclusively as an orchestration layer.

IndicatorEngine calculates technical indicators and benchmark-aware metrics.

CandlestickPatternAnalyzer analyses raw candle data directly and is intentionally separated from IndicatorEngine because candlestick recognition is based on price action rather than derived indicators.

Overall score weighting is centrally managed through the Analysis Layer configuration.

MarketRegimeAnalyzer provides market context and remains excluded from the overall technical score.

RelativeStrengthAnalyzer contributes market-relative performance.

CandlestickPatternAnalyzer contributes deterministic price-action analysis.
AnalyzerRegistry now centrally manages all analyzers.

AnalysisEngine no longer owns individual analyzer instances.

Analyzer execution is registry-driven and remains fully deterministic.

Each registered analyzer defines:

- execution order
- score field
- raw candle requirement
- overall score participation

Future analyzers should be added by registering them in AnalyzerRegistry rather than modifying AnalysisEngine.

The analytical foundation required for the future Signal Engine is now considered complete.
# 4. Current Architecture

Project Orion currently follows the following layered architecture.

```text id="arch01"
Universe Layer

↓

Market Data Layer

↓

Historical Data Layer

↓

Indicator Library

↓

Indicator Engine

↓

Analysis Engine

↓

Signal Engine

↓

Decision Engine

↓

Portfolio Engine

↓

Risk Manager

↓

Trade Planner

↓

Artificial Intelligence Layer

↓

GUI
```

Only the first six layers are currently implemented.

Every future module should integrate into this architecture rather than introducing alternative processing pipelines.

---

# 5. Current Engineering Status

The following components are fully operational.

Infrastructure

Infrastructure

* Universe Management
* Market Data
* Historical Data
* Quote Cache
* Historical Cache
* Benchmark-aware IndicatorEngine
* Central Analysis Weight Configuration
* Raw Candle Analysis

Scanner

* Scan Pipeline
* Ranking Engine
* Technical Scanner

Analysis

* Indicator Library
* Indicator Engine
* Analysis Engine

Analysis Framework

* BaseAnalyzer
* Trend Analyzer
* Momentum Analyzer
* Volatility Analyzer
* Structure Analyzer
* Volume Analyzer
* Analysis Engine orchestration
* Dedicated analyzer unit tests
* MarketRegimeAnalyzer
* RelativeStrengthAnalyzer
* CandlestickPatternAnalyzer


Scanner Integration

* Technical Scanner migrated to Analysis Layer
* Unified technical scoring
* AnalysisResult integration


Indicators

* SMA20
* SMA50
* EMA20
* EMA50
* RSI14
* MACD
* ATR14
* Bollinger Bands
* ADX14

Scoring

* Trend Score
* Momentum Score
* Volatility Score
* Structure Score
* Volume Score
* Market Regime Score
* Relative Strength Score
* Candlestick Score
* Overall Technical Score

These modules should be considered stable unless future architectural improvements clearly justify modification.
# 6. Engineering Rules

The following engineering rules should be respected throughout the lifetime of Project Orion.

---

## Single Responsibility

Every class should perform one clearly defined task.

Examples:

Universe Loader

Loads stock universes.

Historical Provider

Downloads historical candles.

Indicator Engine

Calculates indicators.

Analysis Engine

Interprets indicators.

Signal Engine

Produces trading signals.

Each layer should remain independent from unrelated responsibilities.

---

## Modular Design

Future functionality should be added by extending the architecture rather than modifying unrelated modules.

Example:

A new indicator should only require changes within:

```text
services/analysis/indicator_library/
```

The Analysis Engine should automatically benefit from the new indicator without architectural redesign.

---

## Reusability

Every calculation should be reusable.

Indicator calculations should never be embedded inside business logic.

Instead:

```text
Indicator Library

↓

Indicator Engine

↓

Analysis Engine
```

This separation makes testing significantly easier.

---

## Low Coupling

Modules should know as little as possible about each other.

For example:

The Indicator Engine should not know anything about:

* BUY signals
* Portfolio management
* Risk calculations
* GUI rendering

Similarly:

The GUI should never contain business logic.

---

## High Cohesion

Each module should focus exclusively on its own responsibility.

Examples:

Indicator Library

Only mathematics.

Analysis Engine

Only interpretation.

Signal Engine

Only signal generation.

Decision Engine

Only investment decisions.

This principle keeps Orion maintainable as the codebase grows.

---

# 7. Coding Style

The following coding style should be used consistently.

## Readability over Cleverness

Readable code is preferred over compact code.

Avoid unnecessarily complex implementations.

Future developers should understand the code quickly.

---

## Descriptive Naming

Variable names should describe their purpose.

Good examples:

```python
historical_data

trend_score

overall_score

indicator_result
```

Avoid abbreviated names unless universally recognised.

---

## Type Hints

Type hints should be used whenever practical.

Example:

```python
def calculate_rsi(
    close: pd.Series,
    period: int = 14,
) -> float | None:
```

Type hints improve readability and simplify future maintenance.

---

## Documentation

Every public class should contain a descriptive docstring.

Every important function should explain:

* Purpose
* Parameters
* Return value

Code should explain intent rather than implementation details.

---

## Avoid Duplication

Whenever similar code appears more than once, consider extracting reusable functionality.

Project Orion should favour reusable components over duplicated logic.

---

# 8. Sprint Workflow

Development follows a fixed workflow.

Step 1

Design the architecture.

Step 2

Implement the architecture.

Step 3

Implement functionality.

Step 4

Write or update tests.

Step 5

Run all relevant tests.

Step 6

Update documentation.

Step 7

Commit changes.

Step 8

Push to GitHub.

A sprint is never considered complete before all eight steps have been finished.

---

# 9. Testing Philosophy

Every significant module should have an associated test file.

Tests should be deterministic.

External APIs should be isolated whenever practical.

New functionality should be verified immediately after implementation.

Whenever possible:

One module

↓

One test file

↓

One responsibility

This philosophy has already been successfully applied throughout the current project.

---

# 10. Documentation Rules

Documentation is treated as part of the software.

Every completed sprint should update:

PROJECT_STATUS.md

CHANGELOG.md

TODO.md

AI_CONTEXT.md (when architectural or development practices change)

ORION_MASTER_ARCHITECTURE.md (only when the architecture itself changes)

Documentation should always reflect the actual implementation.

Future developers should never need to inspect the codebase merely to understand the project's current status.
# 11. Instructions for Future AI Sessions

Every future AI session should assume that Project Orion is an actively maintained professional software project.

The project should never be treated as a prototype.

Large architectural redesigns should be avoided unless explicitly requested.

The existing architecture should always be respected.

---

## Respect Existing Architecture

Before proposing new modules or redesigns, first determine whether equivalent functionality already exists.

Whenever functionality already exists, extend it instead of replacing it.

Future AI sessions should assume that the Master Architecture represents the intended long-term design.

---

## Never Rebuild Completed Sprints

Completed sprints should be considered stable.

Future development should build upon completed functionality rather than replacing it.

Examples of completed work include:

* Universe Layer
* Market Data Layer
* Historical Data Layer
* Indicator Library
* Indicator Engine
* Analysis Engine

These modules should only be modified for bug fixes, optimisation or architectural improvements.

---

## One Responsibility Per Sprint

Future development should remain incremental.

A sprint should introduce one clearly defined capability.

Examples:

Sprint

↓

Signal Engine

NOT

Signal Engine

*

Portfolio

*

Risk Manager

*

GUI

Keeping sprints focused makes testing, documentation and debugging significantly easier.

---

## Preserve Modularity

Whenever new functionality is introduced, ask:

Can this be implemented by adding a new module?

If the answer is yes, avoid modifying existing modules unnecessarily.

Project Orion should continue growing by adding layers rather than rewriting previous ones.

---

## Backwards Compatibility

Whenever practical, new functionality should remain compatible with existing code.

Avoid introducing breaking changes without a compelling architectural reason.

---

# 12. Communication Preferences

Development sessions should remain practical and structured.

The preferred workflow is:

Architecture

↓

Implementation

↓

Testing

↓

Git

↓

Documentation

The AI should guide development one step at a time.

Avoid introducing several unrelated features simultaneously.

---

## Complete Files

The preferred coding style is to provide complete files rather than isolated code snippets.

Whenever a file changes substantially, rewrite the entire file.

This reduces copy/paste mistakes and keeps implementations consistent.

---

## Small Steps

Large implementations should be divided into manageable steps.

Each completed step should be tested before continuing.

This approach has consistently produced stable progress throughout Orion's development.

---

## Testing First

Immediately after implementing new functionality, provide a corresponding test.

Testing should occur before moving to the next implementation step.

---

## Documentation Last

Documentation should be updated after implementation and testing have been completed.

The preferred order is:

Implementation

↓

Testing

↓

Git Commit

↓

GitHub Push

↓

Documentation

This ensures that documentation always reflects working software.

---

# 13. Current Development Focus

## Current Development Focus

Sprint 8.1 successfully introduced CandlestickPatternAnalyzer.

The Analysis Layer now consists of eight specialised analyzers.

- TrendAnalyzer
- MomentumAnalyzer
- VolatilityAnalyzer
- StructureAnalyzer
- VolumeAnalyzer
- MarketRegimeAnalyzer
- RelativeStrengthAnalyzer
- CandlestickPatternAnalyzer
- Analyzer Registry completed
- Signal Engine next

The immediate development objective is to continue expanding analytical intelligence while preserving the modular architecture.

The next planned components are:

- CandlestickPatternAnalyzer
- Signal Engine
- Decision Engine
- Portfolio Engine

Future development should continue favouring specialised analyzers over monolithic implementations.

# 14. Immediate Next Sprint

Sprint 8.2

Objective:

Implement Signal Engine

Planned work:

- Introduce SignalResult
- Build modular SignalEngine
- Convert AnalysisResult into deterministic trading signals
- Preserve modular architecture
- Maintain full backwards compatibility
- Add complete unit test coverage

Expected outcome:

The Analysis Layer will feed a dedicated Signal Engine capable of generating deterministic BUY, WATCH, HOLD and SELL signals while keeping AnalysisEngine focused exclusively on technical analysis.
---

# 15. Long-Term Vision

Project Orion is intended to become a professional desktop application capable of assisting investors throughout the complete investment process.

Future capabilities include:

* Market scanning
* Technical analysis
* Signal generation
* Investment decisions
* Portfolio management
* Risk analysis
* Trade planning
* AI explanations
* Paper trading
* Broker integration

Artificial Intelligence should remain an explanatory layer rather than a decision-making engine.

Deterministic analysis should always remain the foundation of every recommendation generated by Orion.
# 16. Developer Notes

The following notes describe the development practices that have proven successful throughout the development of Project Orion.

These are not architectural requirements, but engineering conventions that should be preserved whenever practical.

---

## Build the Foundation First

Project Orion has consistently been developed from the bottom upwards.

Infrastructure always precedes intelligence.

The development order is intentionally structured as follows:

```text
Universe

↓

Market Data

↓

Historical Data

↓

Indicator Library

↓

Indicator Engine

↓

Analysis Engine

↓

Signal Engine

↓

Decision Engine

↓

Portfolio Engine

↓

Risk Manager

↓

Trade Planner

↓

Artificial Intelligence

↓

GUI
```

Future development should continue respecting this order whenever possible.

---

## Complete One Layer Before Starting the Next

Development should avoid partially implemented systems.

Instead:

Finish one layer completely.

Test it.

Document it.

Commit it.

Only then continue to the next layer.

This methodology has resulted in a highly stable codebase with very little technical debt.

---

## Prefer Architecture Over Features

Whenever choosing between:

Adding another feature

or

Improving architecture

Architecture should generally take priority.

A solid architecture enables future features to be implemented more rapidly and with fewer defects.

---

## Keep Documentation Current

Documentation is considered part of the software.

Documentation should never lag behind implementation.

After each completed sprint the following workflow should be followed:

```text
Implementation

↓

Testing

↓

Git Commit

↓

GitHub Push

↓

Documentation
```

The documentation should always describe the current implementation.

---

## Complete Files Instead of Partial Snippets

When making significant changes to a file, complete file rewrites are preferred over isolated snippets.

Providing complete files reduces copy-and-paste errors and ensures consistent formatting.

Future AI sessions should continue using this approach whenever practical.

---

## One Step at a Time

Development sessions should proceed incrementally.

Avoid introducing multiple unrelated systems simultaneously.

Instead:

Design.

↓

Implement.

↓

Test.

↓

Commit.

↓

Document.

↓

Continue.

This approach has proven significantly more reliable than attempting to implement large features in a single step.

---

## Maintain Professional Standards

Although Orion is currently an alpha project, it should always be treated as a professional software product.

Every new component should meet the same quality standards as production software.

This includes:

* Clear architecture
* Modular implementation
* Readable code
* Comprehensive testing
* Up-to-date documentation
* Version control
* Deterministic behaviour

---

# 17. Final Statement

Project Orion has evolved beyond a simple programming exercise.

It is now a structured software platform with a documented architecture, deterministic analytical core and a clearly defined long-term roadmap.

Future development should preserve the principles established throughout the project:

* Build incrementally.
* Respect the architecture.
* Keep modules independent.
* Test continuously.
* Document consistently.
* Prefer clarity over complexity.
* Ensure every recommendation remains deterministic and explainable.

By following these principles, Orion can continue to grow into a professional swing-trading platform while remaining maintainable, scalable and understandable for both developers and AI assistants.

---

# End of AI Context

This document should accompany every future development session together with:

* ORION_MASTER_ARCHITECTURE.md
* PROJECT_STATUS.md

These three documents collectively define the complete development context for Project Orion and should be regarded as the authoritative source of truth throughout the lifetime of the project.
