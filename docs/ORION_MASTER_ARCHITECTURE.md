# PROJECT ORION

## Master Architecture Document

**Document Version:** 1.0 (Draft)
**Project Status:** Active Development
**Architecture Owner:** Project Orion Development Team

---

# 1. Introduction

## 1.1 Purpose of this Document

This document defines the complete software architecture of **Project Orion**.

Its purpose is not only to describe how the software is built today, but also to establish the long-term technical vision of the project. Every future sprint, feature, refactoring effort and architectural decision should be evaluated against the principles described in this document.

This document serves as the primary technical source of truth for Project Orion.

It is intended for:

* Software developers
* Future contributors
* Architects
* Test engineers
* Future maintainers
* AI-assisted development

Whenever uncertainty exists about how Orion should evolve, this document takes precedence over individual implementation decisions.

---

# 1.2 What is Project Orion?

Project Orion is an AI-driven swing trading assistant designed to analyse thousands of publicly traded U.S. stocks every day and identify only the highest quality trading opportunities.

Instead of requiring a trader to manually inspect thousands of charts, Orion performs the complete technical analysis pipeline automatically.

The objective is simple:

> Reduce thousands of potential investments into a very small number of objectively high-quality opportunities.

Project Orion is not designed to predict the future.

Instead, it identifies statistically attractive technical setups based on predefined, explainable and continuously improving analysis models.

Every recommendation must be traceable.

Every score must be explainable.

Every decision must be reproducible.

Transparency is considered a core design principle of the entire platform.

---

# 1.3 Vision

The long-term vision of Project Orion is to become a professional decision-support platform for swing traders.

Orion should eventually function as a digital trading analyst that continuously scans the market, evaluates technical conditions, measures risk, proposes trade plans and explains every recommendation in plain language.

Rather than replacing the trader, Orion is designed to augment the trader's decision-making process.

The software should answer questions such as:

* Which stocks deserve my attention today?
* Why are these opportunities interesting?
* How strong is the current trend?
* How much risk does this trade involve?
* Where should I enter?
* Where should I place my stop-loss?
* Where should I take profits?
* How confident is Orion in this setup?

The goal is to make high-quality market analysis available within seconds.

---

# 1.4 Mission

The mission of Project Orion is to provide objective, data-driven swing trading analysis through a modular and scalable software architecture.

Every recommendation produced by Orion must satisfy three conditions:

1. It is based on measurable market data.
2. It can be explained to the user.
3. It can be reproduced by the software.

The project deliberately avoids black-box decision making.

Artificial Intelligence may assist with explanations and summarisation, but final recommendations are always grounded in deterministic market analysis.

---

# 1.5 The Problem

Modern financial markets generate an enormous amount of information.

Every trading day thousands of stocks produce new price movements, volume changes, earnings reactions and technical patterns.

A human trader cannot realistically evaluate every opportunity.

As a result, many potentially profitable setups remain undiscovered.

Traditional stock screeners reduce the workload, but still require extensive manual interpretation.

The trader must:

* open individual charts,
* inspect technical indicators,
* compare relative strength,
* evaluate momentum,
* estimate risk,
* and finally decide whether a trade is attractive.

This process is time-consuming, inconsistent and highly dependent on human judgement.

Project Orion exists to automate this analysis pipeline while keeping the decision process transparent and explainable.

---

# 1.6 The Orion Solution

Project Orion introduces a layered analysis architecture.

Instead of treating market analysis as a single operation, Orion divides the process into independent components.

Each layer has one clearly defined responsibility.

Examples include:

* Universe Management
* Market Data Collection
* Historical Data Management
* Technical Analysis
* Signal Generation
* Decision Making
* Portfolio Management
* Risk Management
* Trade Planning
* Graphical Presentation

This separation of responsibilities improves maintainability, scalability and testability.

It also allows future expansion without redesigning the core architecture.

---

# 1.7 Design Philosophy

Several principles guide every architectural decision within Orion.

## Single Responsibility

Every module should perform exactly one task.

## Explainability

Every recommendation must be explainable.

## Modularity

Components should communicate through clearly defined interfaces.

## Provider Independence

Business logic must never depend directly on external market data providers.

## Testability

Every important component should be testable in isolation.

## Scalability

The architecture should scale from several thousand to tens of thousands of symbols without structural redesign.

## Maintainability

New developers should be able to understand the architecture quickly.

## Long-Term Stability

Architectural decisions should favour long-term maintainability over short-term convenience.

---

# 1.8 Project Scope

Project Orion focuses on medium-term swing trading.

The system is specifically designed for identifying opportunities with an expected holding period of several days to several weeks.

High-frequency trading is explicitly outside the scope of the project.

Likewise, Orion is not intended to predict market movements or replace human judgement.

Its role is to analyse, rank and explain trading opportunities using objective technical criteria.

---

# 1.9 Long-Term Vision

Project Orion is intended to evolve far beyond a traditional stock screener.

The long-term objective is to create an intelligent trading assistant capable of supporting every stage of the investment process.

Future versions will include:

* advanced technical analysis,
* AI-assisted explanations,
* portfolio optimisation,
* position sizing,
* automated trade planning,
* paper trading,
* broker integrations,
* interactive dashboards,
* historical performance analysis,
* and personalised trading workflows.

While these capabilities will be introduced gradually, every architectural decision made today should support this long-term vision.

This document defines the foundation upon which those future capabilities will be built.

# 2. System Architecture

## 2.1 Introduction

Project Orion follows a layered software architecture.

Each layer has a single responsibility and communicates only with adjacent layers. This separation reduces coupling, improves maintainability and allows individual components to evolve independently.

The architecture deliberately avoids placing business logic inside the user interface or inside external data providers.

Instead, all intelligence resides within dedicated engine components.

---

# 2.2 Architectural Overview

```
                        PROJECT ORION

                AI Swing Trading Assistant

                             │
                             ▼

                    Universe Management

                             │
                             ▼

                     Market Data Layer

                             │
                             ▼

                  Historical Data Layer

                             │
                             ▼

                     Analysis Engine

                             │
                             ▼

                      Signal Engine

                             │
                             ▼

                     Decision Engine

                             │
                             ▼

                     Portfolio Engine

                             │
                             ▼

                       Risk Manager

                             │
                             ▼

                      Trade Planner

                             │
                             ▼

                         GUI Layer
```

Every layer transforms information into a more intelligent representation.

The GUI never performs analysis.

The Analysis Engine never downloads market data.

The Market Data Layer never decides whether a stock should be bought.

Each layer performs exactly one task.

---

# 2.3 Data Flow

A complete Orion scan follows the sequence below.

```
Universe
      │
      ▼
Load Symbols

      │
      ▼
Download Quotes

      │
      ▼
Price Filter

      │
      ▼
Volume Filter

      │
      ▼
Liquidity Filter

      │
      ▼
Relative Strength Filter

      │
      ▼
Momentum Filter

      │
      ▼
Historical Data

      │
      ▼
Analysis Engine

      │
      ▼
Signal Engine

      │
      ▼
Decision Engine

      │
      ▼
Ranking Engine

      │
      ▼
Top Opportunities
```

Each stage reduces complexity.

The system gradually transforms a universe of several thousand stocks into a very small number of high-quality opportunities.

---

# 2.4 Layer Responsibilities

## Universe Layer

Purpose:

Maintain the complete investment universe.

Responsibilities:

* Download symbol lists
* Import exchanges
* Remove delisted stocks
* Maintain watchlists
* Maintain sector information
* Validate ticker symbols

Output:

```
list[str]
```

Example:

```
AAPL
MSFT
PANW
NVDA
```

---

## Market Data Layer

Purpose:

Retrieve the latest market information.

Responsibilities:

* Latest price
* Daily volume
* Previous close
* Market capitalization
* Quote caching
* Provider abstraction

Supported providers:

* Yahoo Finance
* Polygon.io (future)
* Alpaca (future)
* Finnhub (future)

Output:

```
Quote
```

---

## Historical Data Layer

Purpose:

Provide historical candle data.

Responsibilities:

* Batch downloads
* Persistent cache
* Cache validation
* TTL management
* Provider abstraction

Output:

```
Pandas DataFrame
```

Historical data is shared across the entire application.

No module downloads historical candles directly.

---

## Analysis Engine

Purpose:

Convert raw historical data into objective technical information.

Input:

Historical candles

Output:

AnalysisResult

Responsibilities:

* Calculate indicators
* Measure trend
* Measure momentum
* Measure volatility
* Detect market structure
* Detect support and resistance

The Analysis Engine never decides whether a stock should be bought.

Its only purpose is analysis.

---

## Signal Engine

Purpose:

Interpret analysis results.

Responsibilities:

* Bullish signals
* Bearish signals
* Neutral signals
* Trend confirmation
* Momentum confirmation
* Signal weighting

Output:

```
SignalResult
```

---

## Decision Engine

Purpose:

Convert signals into investment advice.

Possible outputs:

BUY

WATCH

HOLD

IGNORE

Every decision includes:

* Confidence score
* Supporting arguments
* Risk estimate

---

## Portfolio Engine

Purpose:

Manage positions.

Responsibilities:

* Open positions
* Closed positions
* Portfolio allocation
* Sector diversification
* Position sizing inputs

The Portfolio Engine does not determine technical quality.

It manages capital allocation.

---

## Risk Manager

Purpose:

Protect capital.

Responsibilities:

* Maximum position size
* Maximum exposure
* Risk percentage
* Stop-loss calculations
* Drawdown protection

Risk management always has priority over opportunity selection.

---

## Trade Planner

Purpose:

Transform an approved opportunity into a complete trading plan.

Generated values include:

* Entry price
* Stop-loss
* Take-profit
* Risk / Reward ratio
* Estimated holding period
* Position size

---

## GUI Layer

Purpose:

Present information.

The GUI contains no trading logic.

It requests data from the engines and visualises the results.

Responsibilities include:

* Dashboard
* Charts
* Tables
* Progress indicators
* Portfolio overview
* Trade details
* AI explanation

---

# 2.5 Dependency Rules

To preserve maintainability, Orion follows strict dependency rules.

Allowed:

```
GUI

↓

Decision Engine

↓

Signal Engine

↓

Analysis Engine

↓

Historical Data Layer

↓

Market Data Layer

↓

Providers
```

Not allowed:

GUI downloading market data.

Decision Engine calling Yahoo Finance.

Analysis Engine calculating portfolio allocation.

Market Data Layer calculating RSI.

Every layer remains independent.

---

# 2.6 Architectural Principles

Every new feature introduced into Orion should satisfy the following principles.

## Single Responsibility

Every module performs exactly one task.

---

## Low Coupling

Modules know as little as possible about each other.

---

## High Cohesion

Everything within a module belongs together.

---

## Provider Independence

External services may change.

Business logic must remain unchanged.

---

## Testability

Every important module must be testable independently.

---

## Extensibility

Adding a new indicator should never require rewriting existing components.

Adding a new market data provider should never affect technical analysis.

Adding a new GUI screen should never affect business logic.

---

# 2.7 Future Architecture

The current architecture is intentionally designed to support future expansion.

Examples include:

Artificial Intelligence

Broker Integration

Paper Trading

Machine Learning

News Analysis

Economic Calendar

Sentiment Analysis

Mobile Applications

Cloud Synchronisation

REST API

Multi-user Support

Because each responsibility is isolated inside its own layer, these future capabilities can be introduced with minimal impact on the existing architecture.

---

# 2.8 Architectural Goals

The architecture should ultimately satisfy the following objectives.

Performance

Daily scans should complete within seconds, even for several thousand symbols.

Scalability

The system should support future expansion without structural redesign.

Reliability

Failures in external providers should not crash the application.

Maintainability

New contributors should understand the architecture quickly.

Transparency

Every recommendation should be explainable.

Professionalism

Project Orion should resemble the architecture of professional trading platforms rather than a collection of scripts.

---

# End of Chapter 2

The following chapter defines the complete internal project structure, including folders, modules, naming conventions and coding standards that every future component must follow.

# 3. Project Structure & Development Standards

## 3.1 Introduction

A professional software architecture is not only defined by the components it contains, but also by the way those components are organised.

As Project Orion continues to grow, maintaining a clear and consistent project structure becomes increasingly important.

Every folder, module and class should have a single purpose.

Developers should be able to navigate the codebase without needing to understand the entire application.

For that reason, Project Orion follows a strict modular structure.

Every major responsibility is isolated inside its own package.

---

# 3.2 High-Level Directory Structure

The long-term target structure of Project Orion is shown below.

```text
Project-Orion/

│
├── app.py
├── requirements.txt
├── README.md
│
├── config/
│
├── docs/
│
├── core/
│
├── models/
│
├── database/
│
├── data/
│
│   ├── cache/
│   ├── universes/
│   ├── history/
│   ├── portfolio/
│   └── exports/
│
├── services/
│
│   ├── universe/
│   ├── market_data/
│   ├── analysis/
│   ├── signals/
│   ├── decisions/
│   ├── portfolio/
│   ├── risk/
│   ├── planner/
│   ├── scanner/
│   └── ai/
│
├── providers/
│
├── ui/
│
├── output/
│
└── tests/
```

This layout intentionally separates business logic from presentation, configuration, storage and external integrations.

---

# 3.3 Folder Responsibilities

## app.py

Application entry point.

Responsibilities:

* Application startup
* Dependency construction
* GUI launch
* Configuration loading

The application entry point should remain as small as possible.

Business logic should never be implemented here.

---

## config/

Contains configuration files.

Examples:

* application settings
* scan configuration
* provider settings
* trading profile
* environment configuration

Configuration files should contain no executable business logic.

---

## docs/

Contains all documentation.

Examples:

* Master Architecture
* Project Status
* Sprint Documentation
* User Manual
* API Documentation

Documentation is considered part of the project itself and should evolve together with the codebase.

---

## core/

Contains application-wide infrastructure.

Examples:

* dependency injection
* application startup
* service registration
* global utilities

The Core package should not contain trading logic.

---

## models/

Contains shared domain models.

Examples:

```text
Quote

HistoricalBar

AnalysisResult

TradePlan

Position

Portfolio

RiskProfile

Signal

Decision
```

Models should contain data only.

Business logic belongs inside services.

---

## database/

Contains persistence logic.

Responsibilities:

* SQLite
* future PostgreSQL
* repositories
* migrations

The rest of Orion should never communicate directly with SQL.

Instead it communicates with repositories.

---

## data/

Stores runtime data.

Examples:

```text
cache/

historical/

universes/

trade_history/

exports/

logs/
```

This directory is intentionally separated from source code.

---

## services/

This is the heart of Orion.

Every major subsystem lives here.

Each package performs one responsibility.

---

## providers/

Contains external integrations.

Examples:

Yahoo Finance

Polygon

Finnhub

Interactive Brokers

Alpaca

External providers should never contain business decisions.

They simply provide data.

---

## ui/

Contains the graphical interface.

Responsibilities:

* windows
* widgets
* charts
* dialogs
* themes

No trading logic belongs here.

---

## tests/

Contains automated tests.

Every important module should eventually have dedicated tests.

---

# 3.4 Service Architecture

The Services package is intentionally divided into specialised engines.

```text
services/

    universe/

    market_data/

    analysis/

    signals/

    decisions/

    portfolio/

    risk/

    planner/

    scanner/

    ai/
```

Each package represents a complete subsystem.

---

# 3.5 Analysis Package

The Analysis package becomes the mathematical heart of Orion.

Target structure:

```text
analysis/

    indicator_engine.py

    trend_analyzer.py

    momentum_analyzer.py

    volatility_analyzer.py

    structure_analyzer.py

    support_resistance.py

    indicator_library/

        moving_averages.py

        rsi.py

        macd.py

        atr.py

        bollinger.py

        adx.py

        stochastic.py

        volume.py
```

The Analysis Engine performs calculations only.

It never decides whether a stock should be bought.

---

# 3.6 Signal Package

Responsibilities:

Interpret analysis.

Generate signals.

Examples:

Bullish crossover

Oversold

Strong trend

Breakout

High volatility

Low volatility

The output consists of objective signals.

---

# 3.7 Decision Package

The Decision package combines all available information.

Inputs include:

Trend

Momentum

Volatility

Market Structure

Support

Resistance

Risk

Portfolio

Outputs include:

BUY

WATCH

HOLD

IGNORE

Confidence Score

Reasoning

---

# 3.8 Portfolio Package

Responsibilities:

Current positions

Cash

Sector exposure

Diversification

Position sizing

Trade history

Performance metrics

---

# 3.9 Risk Package

Responsibilities:

Maximum exposure

Maximum position size

Daily risk

Portfolio risk

Stop-loss calculations

Take-profit calculations

Drawdown control

Risk calculations should always override opportunity quality.

Capital preservation has priority.

---

# 3.10 Planner Package

Generates executable trade plans.

Output:

Entry

Stop-loss

Take-profit

Risk / Reward

Estimated duration

Capital allocation

Expected return

The planner transforms an opportunity into an actionable trading plan.

---

# 3.11 AI Package

This package does not replace deterministic analysis.

Instead it explains and summarises it.

Future responsibilities:

Natural language explanations

Trading summaries

Market reports

Portfolio commentary

Educational feedback

Future AI implementations should always use the outputs produced by deterministic engines.

The AI should explain decisions rather than invent them.

---

# 3.12 Naming Conventions

Consistency is considered a quality feature.

Classes:

PascalCase

Example:

```text
HistoricalDataProvider

TechnicalScanner

DecisionEngine
```

Methods:

snake_case

Example:

```text
calculate_rsi()

load_universe()

generate_trade_plan()
```

Constants:

UPPER_CASE

Variables:

snake_case

---

# 3.13 Module Design Rules

Every module should answer one question.

Examples:

RSI module

Calculates RSI.

Nothing else.

MACD module

Calculates MACD.

Nothing else.

Decision Engine

Combines information.

Nothing else.

Violations of the Single Responsibility Principle should be considered architectural issues.

---

# 3.14 Dependency Rules

Allowed:

Analysis → Models

Decision → Analysis

GUI → Decision

Not Allowed:

GUI → Yahoo

Decision → Yahoo

Analysis → SQLite

Scanner → GUI

The dependency graph should always point downward.

---

# 3.15 Coding Philosophy

The architecture values:

Readability over cleverness.

Maintainability over speed of implementation.

Explicitness over hidden behaviour.

Composition over duplication.

Long-term stability over short-term optimisation.

Whenever there is doubt between writing less code or writing clearer code, clarity should take precedence.

---

# End of Chapter 3

The next chapter introduces the complete Market Data Architecture, describing how Orion collects, caches, validates and distributes real-time and historical market data throughout the entire platform.
# 4. Market Data Architecture

## 4.1 Introduction

The Market Data Layer is the foundation of the entire Orion platform.

Every calculation, technical indicator, trading signal and investment decision ultimately depends on reliable market data.

For that reason, Orion isolates all market data collection inside a dedicated architecture layer.

No other component within the application is allowed to communicate directly with external data providers.

This design provides several important advantages:

* Provider independence
* Centralised caching
* Easier testing
* Higher reliability
* Better performance
* Simplified future expansion

The Market Data Layer is therefore considered one of the core pillars of the Orion architecture.

---

# 4.2 Responsibilities

The Market Data Layer is responsible for obtaining every piece of external market information required by Orion.

Its responsibilities include:

* Current stock prices
* Previous closing prices
* Daily trading volume
* Average trading volume
* Market capitalisation
* Bid/Ask prices (future)
* Dividend information (future)
* Corporate actions (future)
* Exchange information (future)

It does **not** perform technical analysis.

It does **not** make investment decisions.

Its only responsibility is supplying clean, validated market data.

---

# 4.3 Architecture

```text
                    External Providers
                           │
                           │
         ┌─────────────────┴─────────────────┐
         │                                   │
     Yahoo Finance                     Future Providers
         │                                   │
         └─────────────────┬─────────────────┘
                           │
                           ▼
                Market Data Provider Interface
                           │
                           ▼
                 YahooMarketDataProvider
                           │
                           ▼
                    Quote Cache Manager
                           │
                           ▼
                     QuoteService
                           │
                           ▼
                  Rest of Project Orion
```

Every module above the QuoteService receives identical Quote objects, regardless of which provider is currently active.

---

# 4.4 Provider Abstraction

Orion follows the Dependency Inversion Principle.

Business logic never depends on Yahoo Finance.

Instead it depends on an abstract provider interface.

Current implementation:

```text
BaseMarketDataProvider

        ▲

        │

YahooMarketDataProvider
```

Future providers may include:

* Polygon.io
* Alpaca
* Finnhub
* Twelve Data
* Interactive Brokers
* Local database

Replacing a provider should require no changes to the Analysis Engine or Decision Engine.

---

# 4.5 Quote Model

The Quote object represents a single stock snapshot.

Minimum required fields:

```text
Symbol

Current Price

Previous Close

Daily Volume

Average Volume

Market Capitalisation

Timestamp
```

Future versions may extend the model with:

* Bid
* Ask
* Spread
* Float
* Short Interest
* Beta
* Sector
* Industry

The Quote model acts as the standard market data format throughout Orion.

---

# 4.6 Quote Service

The QuoteService acts as the central coordinator.

Responsibilities:

* Request quotes
* Batch requests
* Cache results
* Retry failed requests
* Validate data
* Return Quote objects

No other module should download quotes directly.

All quote requests flow through the QuoteService.

---

# 4.7 Batch Processing

Downloading thousands of stocks individually would be inefficient.

Therefore Orion groups requests into batches.

Example:

```text
6204 symbols

↓

Batch 1
100 symbols

↓

Batch 2
100 symbols

↓

...

↓

Final Batch
```

Batch sizes may change depending on provider limitations.

The rest of the application should never need to know how batching works.

---

# 4.8 Caching Strategy

Market data changes continuously.

However, repeated downloads during the same scan are unnecessary.

The Quote Cache therefore stores downloaded market data temporarily.

Benefits:

* Faster scans
* Lower provider load
* Fewer network requests
* Improved responsiveness

Cache duration may differ depending on market conditions.

Future versions may dynamically adjust cache lifetimes.

---

# 4.9 Validation

Downloaded market data must pass validation before entering the rest of Orion.

Validation includes:

Current price exists.

Volume exists.

Symbol is valid.

Price is positive.

Volume is non-negative.

Timestamp is available.

Invalid quotes are discarded.

The Analysis Engine should never receive incomplete market data.

---

# 4.10 Error Handling

External providers occasionally fail.

The Market Data Layer should never allow provider failures to crash the application.

Instead:

Retry download.

Skip unavailable symbols.

Continue processing.

Log failures.

Return statistics.

Robustness is preferred over completeness.

Processing 6,180 symbols successfully is better than aborting because 24 symbols failed.

---

# 4.11 Performance Goals

Target performance:

Universe Size

≈ 6,000 symbols

Maximum Quote Download

< 5 seconds

Average Scan Time

< 10 seconds

Memory Usage

Stable throughout scan

The Market Data Layer should be designed to scale significantly beyond the current universe size.

---

# 4.12 Statistics

Every provider should expose runtime statistics.

Example:

```text
Provider

YahooMarketDataProvider

Requested

6204

Received

6188

Missing

16

Cache Hits

5700

Fresh Downloads

488

Duration

3.42 sec
```

These statistics assist both debugging and future optimisation.

---

# 4.13 Future Improvements

The Market Data Layer is expected to evolve over time.

Potential enhancements include:

* Parallel downloads
* Async providers
* WebSocket live prices
* Multiple provider fallback
* Smart provider selection
* Regional exchanges
* Extended market data
* Real-time streaming

Because the architecture is provider-independent, these improvements can be introduced without affecting higher application layers.

---

# 4.14 Design Principles

The Market Data Layer follows five fundamental principles.

**Provider Independence**
Business logic must never depend on a specific external API.

**Reliability**
Provider failures should degrade gracefully rather than stop the application.

**Performance**
Downloads should be batched and cached whenever possible.

**Consistency**
All consumers receive identical Quote objects regardless of provider.

**Scalability**
The architecture should support future expansion without structural redesign.

---

# End of Chapter 4

The next chapter defines the complete Historical Data Architecture, including candle storage, persistent caching, cache invalidation, historical providers and how technical analysis consumes historical market data.

# 5. Historical Data Architecture

## 5.1 Introduction

While the Market Data Layer provides the latest market snapshot, technical analysis requires historical market behaviour.

Every moving average, momentum calculation, volatility measurement and trend analysis depends on historical candle data.

Project Orion therefore introduces a dedicated Historical Data Layer.

This layer has one responsibility:

> Provide reliable, validated and efficiently cached historical market data to every analytical component inside Orion.

No analysis module should ever communicate directly with an external provider.

Historical data is considered a shared resource across the entire application.

---

# 5.2 Responsibilities

The Historical Data Layer is responsible for:

* Downloading historical candles
* Persistent caching
* Cache validation
* Batch downloads
* Provider abstraction
* Historical data statistics
* Future multi-provider support

It is **not** responsible for:

* Technical indicators
* Trend analysis
* Signal generation
* Investment decisions

Its only purpose is to deliver historical price data.

---

# 5.3 Architectural Overview

```text
                External Historical Providers

                          │

        ┌─────────────────┴─────────────────┐

        │                                   │

     Yahoo Finance                    Future Providers

        │                                   │

        └─────────────────┬─────────────────┘

                          ▼

              HistoricalDataProvider Interface

                          ▼

             YahooHistoricalDataProvider

                          ▼

                  Historical Cache

                          ▼

                  HistoricalDataService

                          ▼

                  Analysis Engine

                          ▼

                   Signal Engine
```

This separation guarantees that analytical components never depend on an external API.

---

# 5.4 Provider Abstraction

Historical data providers implement a common interface.

Current implementation:

```text
HistoricalDataProvider

        ▲

        │

YahooHistoricalDataProvider
```

Future providers may include:

* Polygon.io
* Alpaca
* Interactive Brokers
* Twelve Data
* Local Database

Switching providers should require no changes to the Analysis Engine.

---

# 5.5 Historical Candle Model

Each historical candle represents one completed trading interval.

Minimum required fields:

```text
Timestamp

Open

High

Low

Close

Volume
```

Future extensions may include:

* Adjusted Close
* VWAP
* Dividend Adjustments
* Split Information
* Extended Hours
* Corporate Actions

Historical candles remain immutable after download.

---

# 5.6 Historical Cache

Downloading six months of data for thousands of stocks every scan would be inefficient.

To minimise network traffic, Orion maintains a persistent cache.

Current implementation:

```text
data/

    cache/

        historical/
```

Each cache entry contains:

* Symbol
* Period
* Interval
* Download timestamp
* Candle data

---

# 5.7 Cache Strategy

Every request follows this sequence.

```text
Request History

       │

       ▼

Check Cache

       │

 ┌─────┴─────┐

 │           │

Valid     Expired

 │           │

 ▼           ▼

Return    Download

               │

               ▼

          Store Cache

               │

               ▼

          Return History
```

Whenever valid cached data exists, no external download occurs.

---

# 5.8 Cache Lifetime

Historical data changes only when new market sessions complete.

For this reason Orion uses a configurable cache lifetime.

Current implementation:

Default TTL

24 hours

Future versions may dynamically adjust cache duration based on:

* Market open
* Market close
* Intraday scans
* Weekend behaviour
* Holidays

---

# 5.9 Batch Downloads

Downloading one symbol at a time is inefficient.

Historical providers therefore download data in batches.

Example:

```text
6000 symbols

↓

Batch 1

↓

Batch 2

↓

Batch 3

↓

...
```

Batch size depends on provider limitations.

Higher application layers remain unaware of batching.

---

# 5.10 Statistics

Every historical provider exposes runtime statistics.

Example:

```text
Provider

YahooHistoricalDataProvider

Requested

6204

Received

6204

Missing

0

Cache Hits

6188

Fresh Downloads

16

Duration

4.10 sec
```

These statistics are useful for optimisation and debugging.

---

# 5.11 Validation

Downloaded historical data is validated before entering the Analysis Engine.

Validation rules include:

Minimum candle count

No empty datasets

Valid timestamps

Positive prices

Valid OHLC structure

Chronological ordering

Invalid datasets are discarded.

The Analysis Engine should never process corrupted historical data.

---

# 5.12 Performance Objectives

Target performance:

Historical downloads should occur only when necessary.

Repeated scans should primarily use cached data.

Cache hit rates should exceed 95% during normal operation.

Memory usage should remain stable regardless of scan size.

Future versions may preload historical data asynchronously.

---

# 5.13 Failure Recovery

Provider failures must never terminate an Orion scan.

If historical data cannot be obtained:

* Record failure
* Skip symbol
* Continue scan
* Log statistics

The system should always produce the best possible result with available data.

---

# 5.14 Historical Data Lifecycle

The complete lifecycle of historical data is shown below.

```text
Request

↓

Cache Lookup

↓

Download (if needed)

↓

Validation

↓

Persistent Storage

↓

Analysis Engine

↓

Indicators

↓

Signals

↓

Decision Engine
```

Historical data is downloaded exactly once whenever possible.

Every analytical subsystem consumes the same validated dataset.

---

# 5.15 Future Enhancements

The Historical Data Layer has been designed to support future capabilities without architectural changes.

Examples include:

* Incremental candle updates
* Multiple timeframe support
* Weekly candles
* Monthly candles
* Intraday data
* Live candle streaming
* Automatic cache compression
* Database-backed history
* Distributed cache
* Cloud synchronisation

These features can be introduced independently because the provider abstraction already exists.

---

# 5.16 Architectural Principles

The Historical Data Layer follows six guiding principles.

**Single Source of Truth**
Every module uses the same historical dataset.

**Provider Independence**
Analysis never depends on Yahoo Finance directly.

**Persistent Caching**
Historical data should only be downloaded when necessary.

**Reliability**
Provider failures should never stop the application.

**Scalability**
The architecture must support tens of thousands of symbols.

**Performance**
Cache usage should always be prioritised over network requests.

---

# End of Chapter 5

The next chapter introduces the **Analysis Engine**, the mathematical core of Project Orion. It defines how raw historical candles are transformed into objective technical indicators, trend measurements, momentum analysis and volatility scores that ultimately drive every investment decision.

# 6. Analysis Engine Architecture

## 6.1 Introduction

The Analysis Engine is the mathematical core of Project Orion.

While previous layers are responsible for collecting and validating market data, the Analysis Engine transforms that raw information into objective technical knowledge.

Historical candles have little value on their own.

The Analysis Engine converts them into measurable characteristics such as trend strength, momentum, volatility, market structure and technical quality.

No investment decisions are made inside this layer.

Its only purpose is to analyse the market as objectively and consistently as possible.

---

# 6.2 Mission

The mission of the Analysis Engine is to answer one question:

> **"What does the market currently look like?"**

Not:

> **"Should we buy?"**

That decision belongs to later layers.

The Analysis Engine simply measures reality.

---

# 6.3 Architectural Position

```text
Historical Data Layer

        │

        ▼

   Analysis Engine

        │

        ▼

    Signal Engine

        │

        ▼

   Decision Engine
```

This separation ensures deterministic analysis.

Given identical historical candles, the Analysis Engine should always produce identical results.

---

# 6.4 Core Responsibilities

The Analysis Engine is responsible for:

* Technical indicators
* Trend analysis
* Momentum analysis
* Volatility analysis
* Market structure
* Support & resistance
* Volume analysis
* Technical scoring

It is **not** responsible for:

* BUY / SELL decisions
* Position sizing
* Portfolio management
* Stop-loss calculations
* Risk management

---

# 6.5 High-Level Architecture

```text
Historical Candles

        │

        ▼

Indicator Engine

        │

        ▼

Trend Analyzer

        │

        ▼

Momentum Analyzer

        │

        ▼

Volatility Analyzer

        │

        ▼

Structure Analyzer

        │

        ▼

Volume Analyzer

        │

        ▼

Analysis Result
```

Each analyser focuses on exactly one domain.

---

# 6.6 Package Structure

Target directory:

```text
services/

    analysis/

        __init__.py

        indicator_engine.py

        trend_analyzer.py

        momentum_analyzer.py

        volatility_analyzer.py

        structure_analyzer.py

        volume_analyzer.py

        analysis_engine.py

        models.py

        indicator_library/

            moving_averages.py

            rsi.py

            macd.py

            atr.py

            adx.py

            bollinger.py

            stochastic.py

            roc.py

            obv.py

            volume_profile.py
```

This package becomes the analytical heart of Orion.

---

# 6.7 Analysis Pipeline

Every stock follows the same pipeline.

```text
Historical Candles

↓

Indicators

↓

Trend

↓

Momentum

↓

Volatility

↓

Market Structure

↓

Volume Analysis

↓

AnalysisResult
```

Every stage enriches the available information.

No stage modifies historical market data.

---

# 6.8 Indicator Engine

The Indicator Engine is responsible for calculating every mathematical indicator used throughout Orion.

It should become the only location where indicator calculations exist.

Examples:

Simple Moving Average

Exponential Moving Average

Relative Strength Index

Moving Average Convergence Divergence

Average True Range

Average Directional Index

Bollinger Bands

Rate of Change

On Balance Volume

VWAP

Stochastic RSI

Future indicators can be added without modifying the rest of Orion.

---

# 6.9 Trend Analyzer

Purpose:

Determine the direction and quality of the current trend.

Responsibilities:

Current trend

Trend strength

Trend consistency

Moving average alignment

Higher highs

Higher lows

Slope analysis

Output example:

```text
Trend

Bullish

Strength

91

Confidence

95%
```

---

# 6.10 Momentum Analyzer

Purpose:

Measure buying pressure.

Indicators:

RSI

MACD

ROC

Momentum

Moving Average Distance

Acceleration

Output:

```text
Momentum

Strong

Score

84
```

---

# 6.11 Volatility Analyzer

Purpose:

Measure price movement intensity.

Indicators:

ATR

Average Daily Range

Bollinger Width

True Range

Gap Analysis

Output:

```text
Volatility

Moderate

Score

68
```

---

# 6.12 Structure Analyzer

Purpose:

Understand market structure.

Responsibilities:

Higher Highs

Higher Lows

Lower Highs

Lower Lows

Breakouts

Breakdowns

Consolidation

Trend Channels

Support

Resistance

Output:

```text
Structure

Bullish Breakout

Strength

92
```

---

# 6.13 Volume Analyzer

Purpose:

Determine participation.

Measurements:

Relative Volume

Average Volume

Volume Trend

Volume Confirmation

Volume Spikes

Institutional Activity (future)

Output:

```text
Volume

High Participation

Score

87
```

---

# 6.14 AnalysisResult

Every analyzer contributes to one shared model.

Example:

```text
AnalysisResult

Trend

Momentum

Volatility

Structure

Volume

Indicators

Overall Technical Data
```

This model becomes the standard input for the Signal Engine.

---

# 6.15 Deterministic Behaviour

The Analysis Engine must always be deterministic.

Given identical historical candles:

Input

↓

Analysis Engine

↓

Always identical output

Randomness is never allowed.

Machine Learning is not used here.

AI explanations are introduced only after deterministic analysis has completed.

---

# 6.16 Performance Goals

Target performance:

6200 stocks

↓

Complete analysis

↓

< 5 seconds

The engine should remain CPU-efficient and avoid duplicate calculations.

Indicators shared between analyzers should only be calculated once.

---

# 6.17 Future Expansion

The architecture has been designed for future analytical modules.

Examples:

Pattern Recognition

Candlestick Recognition

Market Breadth

Sector Rotation

Relative Performance

Machine Learning Features

Statistical Models

Factor Analysis

None of these additions should require redesigning the existing architecture.

---

# 6.18 Design Principles

The Analysis Engine follows eight architectural principles.

**Objective**

Every calculation must be measurable.

**Deterministic**

Identical input always produces identical output.

**Reusable**

Indicator calculations should never be duplicated.

**Modular**

Each analyzer performs one responsibility.

**Independent**

No analyzer depends on another analyzer's internal implementation.

**Extensible**

New indicators should integrate without architectural changes.

**Efficient**

Indicators should only be calculated once.

**Transparent**

Every output must be explainable.

---

# 6.19 Long-Term Vision

The Analysis Engine is intended to become Orion's technical intelligence.

Future versions should be capable of analysing thousands of securities in real time while producing a complete technical profile for every stock.

The goal is not merely to calculate indicators, but to build a comprehensive understanding of market behaviour that can support reliable, explainable and scalable investment decisions.

This layer forms the foundation upon which every future Orion capability—including the Signal Engine, Decision Engine, AI explanations and Trade Planner—will be built.

---

# End of Chapter 6

The next chapter defines the **Indicator Engine** in detail. It specifies every supported technical indicator, calculation methodology, dependencies, shared calculations and optimisation strategy. This chapter will serve as the blueprint for the implementation of Sprint 7.x.
# 7. Indicator Engine

## 7.1 Introduction

The Indicator Engine is the mathematical foundation of Project Orion.

Its responsibility is straightforward:

> Transform historical market data into objective technical indicators.

Unlike the Analysis Engine, which interprets technical information, the Indicator Engine performs only calculations.

It does not determine whether a market is bullish or bearish.

It does not generate BUY or SELL signals.

It simply produces accurate, reusable technical measurements that can be consumed by higher layers.

The Indicator Engine is therefore considered the numerical core of the entire Orion platform.

---

# 7.2 Design Philosophy

Every indicator follows the same principles.

Indicators must be:

* Deterministic
* Independent
* Reusable
* Testable
* Provider Independent
* Stateless

No indicator should depend on another indicator unless mathematically required.

Each calculation should be reproducible from historical candle data alone.

---

# 7.3 Responsibilities

The Indicator Engine is responsible for:

* Calculating indicators
* Returning structured results
* Avoiding duplicate calculations
* Sharing calculations across analyzers
* Maintaining mathematical consistency

It is **not** responsible for:

* BUY signals
* Trend interpretation
* Confidence scores
* Portfolio logic
* Risk calculations

---

# 7.4 Package Structure

```text
services/

    analysis/

        indicator_engine.py

        indicator_library/

            moving_averages.py

            rsi.py

            macd.py

            atr.py

            adx.py

            bollinger.py

            stochastic.py

            roc.py

            obv.py

            volume.py

            volatility.py
```

Each indicator is isolated in its own module.

---

# 7.5 Indicator Engine Workflow

```text
Historical Candles

↓

Validation

↓

Shared Calculations

↓

Indicator Calculations

↓

Indicator Objects

↓

Analysis Engine
```

Every stock passes through the exact same workflow.

---

# 7.6 Shared Calculations

Many indicators require identical intermediate values.

For example:

Close prices

Typical Price

True Range

Exponential Moving Average

Rolling Mean

Rolling Standard Deviation

Rather than recalculating these values multiple times, Orion calculates them once and shares them.

Benefits include:

* Lower CPU usage
* Less duplicated code
* Faster scans
* Easier maintenance

---

# 7.7 Supported Indicators

The first production release of Orion should support the following indicators.

---

## Trend Indicators

Simple Moving Average (20)

Simple Moving Average (50)

Simple Moving Average (100)

Simple Moving Average (200)

Exponential Moving Average (9)

Exponential Moving Average (20)

Exponential Moving Average (50)

Exponential Moving Average (100)

Exponential Moving Average (200)

---

## Momentum Indicators

Relative Strength Index (14)

Moving Average Convergence Divergence

Rate of Change

Momentum

Stochastic RSI

---

## Volatility Indicators

Average True Range

True Range

Average Daily Range

Bollinger Bands

Bollinger Width

---

## Trend Strength

Average Directional Index

Directional Movement Index

Positive Directional Indicator

Negative Directional Indicator

---

## Volume Indicators

Average Volume

Relative Volume

On Balance Volume

Volume Moving Average

Volume Ratio

---

## Price Structure

Highest High

Lowest Low

Rolling High

Rolling Low

Price Distance

Gap Detection

---

# 7.8 Indicator Objects

Each indicator should return an object rather than a primitive value.

Example:

```text
RSI

Current Value

58.2

Previous Value

55.8

Slope

Positive

Signal

Neutral

Status

Healthy
```

This allows future analyzers to use richer information.

---

# 7.9 Calculation Rules

Every indicator follows identical rules.

Inputs:

Historical candles

Outputs:

Indicator Object

Failures:

Return None

Warnings:

Recorded

Exceptions:

Never propagate into higher layers

Indicators should fail gracefully.

---

# 7.10 Numerical Precision

All calculations should maintain consistent precision.

Guidelines:

Prices

4 decimal places

Percentages

2 decimal places

Ratios

3 decimal places

Internal calculations may use higher precision.

Presentation formatting belongs to the GUI.

---

# 7.11 Performance Strategy

Indicators should never perform unnecessary calculations.

Example:

If SMA20 is already available:

MACD should reuse EMA calculations.

Trend Analyzer should reuse moving averages.

Decision Engine should never recalculate indicators.

Every calculation should happen once.

---

# 7.12 Validation

Indicators validate their inputs before calculation.

Requirements:

Minimum candle count

Valid timestamps

No duplicate candles

Chronological order

Positive prices

Sufficient history

Insufficient history results in a skipped indicator rather than an application failure.

---

# 7.13 Testing Strategy

Every indicator receives dedicated unit tests.

Example:

RSI Tests

* Rising market
* Falling market
* Flat market
* Missing candles
* Short datasets

MACD Tests

* Bullish crossover
* Bearish crossover
* Constant prices

ATR Tests

* High volatility
* Low volatility
* Gap behaviour

Testing every indicator independently ensures mathematical correctness before higher-level analysis begins.

---

# 7.14 Future Indicators

The architecture has been designed for continuous expansion.

Possible additions include:

Ichimoku Cloud

SuperTrend

Keltner Channels

Donchian Channels

Parabolic SAR

Money Flow Index

Accumulation Distribution

Chaikin Oscillator

Ease of Movement

Volume Profile

Anchored VWAP

Relative Volume at Time

None of these additions should require modification of existing indicators.

---

# 7.15 Long-Term Vision

The Indicator Engine should eventually become a standalone mathematical library that can be reused throughout Orion.

Every analytical subsystem—including the Analysis Engine, Signal Engine, Decision Engine and AI Layer—should consume the exact same indicator outputs.

By centralising all technical calculations, Orion ensures mathematical consistency, reduces duplication and establishes a single source of truth for technical market measurements.

This architecture allows the platform to grow for years without requiring fundamental redesign.

---

# End of Chapter 7

The next chapter introduces the **Signal Engine**, responsible for transforming raw indicator values into meaningful bullish, bearish and neutral market signals. This marks the transition from mathematical calculations to trading intelligence.

# 8. Signal Engine Architecture

## 8.1 Introduction

The Analysis Engine measures the market.

The Signal Engine interprets those measurements.

This distinction is fundamental to the Orion architecture.

An RSI value of **58** is merely a mathematical observation.

Whether that value is considered bullish, neutral or bearish depends on the broader market context.

The purpose of the Signal Engine is therefore to transform objective numerical measurements into structured market signals that can be evaluated by the Decision Engine.

The Signal Engine is the first layer where Orion begins to interpret market behaviour rather than merely measuring it.

---

# 8.2 Mission

The mission of the Signal Engine is:

> Convert technical measurements into consistent and explainable market signals.

Signals should always be:

* deterministic
* explainable
* reproducible
* independent
* context aware

The Signal Engine never decides whether a stock should be bought.

Instead it answers questions such as:

* Is momentum increasing?
* Is the trend healthy?
* Is volatility acceptable?
* Is volume confirming the move?
* Is the breakout convincing?

---

# 8.3 Position Inside Orion

```text
Historical Data

        │

        ▼

Analysis Engine

        │

        ▼

Signal Engine

        │

        ▼

Decision Engine
```

Every layer increases the intelligence level.

Historical Data

↓

Indicators

↓

Signals

↓

Decision

---

# 8.4 Responsibilities

The Signal Engine is responsible for:

* interpreting indicators
* combining related indicators
* generating bullish signals
* generating bearish signals
* detecting confirmations
* detecting contradictions
* assigning signal strengths

The Signal Engine is **not** responsible for:

* portfolio management
* risk calculations
* position sizing
* trade planning
* AI explanations

---

# 8.5 Signal Categories

Signals are divided into independent categories.

## Trend Signals

Examples:

Bullish Trend

Strong Bullish Trend

Weak Bullish Trend

Sideways

Weak Bearish Trend

Bearish Trend

Strong Bearish Trend

---

## Momentum Signals

Examples:

Momentum Increasing

Momentum Decreasing

Momentum Exhaustion

Momentum Recovery

Momentum Breakout

---

## Volume Signals

Examples:

Volume Confirmation

Low Participation

High Participation

Volume Spike

Institutional Volume

---

## Volatility Signals

Examples:

Healthy Volatility

High Volatility

Low Volatility

Expanding Volatility

Contracting Volatility

---

## Structure Signals

Examples:

Higher High

Higher Low

Breakout

Failed Breakout

Trend Channel

Consolidation

Support Bounce

Resistance Rejection

---

# 8.6 Signal Objects

Every generated signal should follow a standard structure.

Example:

```text
Signal

Trend Confirmation

Category

Trend

Strength

92

Direction

Bullish

Confidence

95%

Supporting Indicators

EMA20

EMA50

ADX

Market Structure

Timestamp
```

This allows downstream engines to consume signals in a consistent manner.

---

# 8.7 Signal Strength

Signals should not simply be true or false.

Every signal receives a strength score.

Example:

```text
0-20

Very Weak

21-40

Weak

41-60

Neutral

61-80

Strong

81-100

Very Strong
```

This enables nuanced decision making instead of binary logic.

---

# 8.8 Signal Confirmation

Professional traders rarely rely on a single indicator.

Neither should Orion.

Instead multiple indicators should confirm each other.

Example:

RSI

Bullish

*

MACD

Bullish

*

EMA Alignment

Bullish

*

ADX

Strong Trend

↓

Strong Bullish Signal

This reduces false positives.

---

# 8.9 Signal Conflicts

Indicators do not always agree.

Example:

Trend

Bullish

Momentum

Bearish

Volume

Weak

Volatility

High

Rather than ignoring contradictions, Orion records them explicitly.

Conflicting signals reduce confidence.

They never disappear.

Transparency remains a core design principle.

---

# 8.10 Signal Scoring

Every category produces its own score.

Example:

```text
Trend

92

Momentum

81

Volume

74

Volatility

63

Structure

89
```

These category scores become inputs for the Decision Engine.

---

# 8.11 Composite Signals

Higher-level signals are generated by combining lower-level signals.

Example:

Bullish Breakout

requires:

Trend

Strong

Momentum

Strong

Volume

Above Average

Structure

Breakout

Only when all required conditions are met should the composite signal be generated.

---

# 8.12 Explainability

Every signal stores its own reasoning.

Example:

```text
Trend Signal

Bullish

Reason

Price above EMA20

EMA20 above EMA50

ADX above 25

Higher Highs detected
```

This information later becomes the basis for Orion's AI explanations.

---

# 8.13 SignalResult

The output of the Signal Engine is a complete SignalResult object.

Example:

```text
SignalResult

Trend Signals

Momentum Signals

Volume Signals

Volatility Signals

Structure Signals

Composite Signals

Overall Signal Strength
```

No BUY recommendation exists yet.

Only interpreted market behaviour.

---

# 8.14 Future Expansion

The Signal Engine has been designed for continuous growth.

Future signals may include:

Sector Rotation

Relative Strength Leaders

Institutional Buying

News Confirmation

Options Flow

Market Breadth

Index Confirmation

Sentiment Analysis

Machine Learning Signals

These additions should integrate without affecting existing signal generation.

---

# 8.15 Architectural Principles

The Signal Engine follows seven guiding principles.

**Context over Individual Indicators**

One indicator is rarely sufficient.

Signals should evaluate relationships between multiple indicators.

---

**Transparency**

Every signal must explain itself.

---

**Determinism**

Identical analysis results always produce identical signals.

---

**Independence**

Signals remain independent from portfolio management and trade execution.

---

**Scalability**

New signals should be introduced without modifying existing implementations.

---

**Consistency**

All signals follow identical object structures.

---

**Reusability**

Signals may be reused by multiple future modules, including AI explanations and strategy evaluation.

---

# 8.16 Long-Term Vision

The Signal Engine is intended to become Orion's interpretation layer.

It bridges the gap between raw technical calculations and intelligent investment decisions.

Rather than relying on isolated indicators, Orion evaluates how multiple technical observations reinforce—or contradict—each other.

This layered interpretation enables more robust decision making and creates a foundation for transparent, explainable recommendations.

---

# End of Chapter 8

The next chapter introduces the **Decision Engine**, where all generated signals are combined into actionable recommendations such as **BUY**, **WATCH**, **HOLD** or **IGNORE**, together with confidence scores and complete reasoning. This is the layer where Orion begins to behave like an experienced trading analyst rather than a collection of technical indicators.
# 9. Decision Engine Architecture

## 9.1 Introduction

The Decision Engine is the central intelligence layer of Project Orion.

Previous layers collect market data, calculate technical indicators and generate technical signals.

The Decision Engine combines all of this information into one coherent investment recommendation.

Its purpose is not merely to answer the question:

> "Is this stock interesting?"

Instead it answers:

* Is this opportunity worth taking?
* How confident is Orion?
* Why does Orion reach this conclusion?
* What are the strongest arguments?
* What are the risks?
* How does this opportunity compare to every other stock in today's market?

The Decision Engine transforms technical analysis into actionable investment intelligence.

---

# 9.2 Mission

The mission of the Decision Engine is:

> Convert technical market signals into explainable investment recommendations.

Every recommendation must satisfy five requirements.

It must be:

* Objective
* Explainable
* Repeatable
* Consistent
* Transparent

No recommendation may depend on randomness.

No recommendation may depend on subjective interpretation.

---

# 9.3 Position Inside Orion

```text
Historical Data

        │

        ▼

Analysis Engine

        │

        ▼

Signal Engine

        │

        ▼

Decision Engine

        │

        ▼

Portfolio Engine
```

The Decision Engine is therefore the final analytical layer before portfolio management begins.

---

# 9.4 Responsibilities

The Decision Engine is responsible for:

* Combining signals
* Weighing strengths
* Evaluating weaknesses
* Measuring confidence
* Ranking opportunities
* Generating explanations
* Producing final recommendations

It is **not** responsible for:

* Position sizing
* Stop-loss calculation
* Portfolio allocation
* Trade execution

Those responsibilities belong to later components.

---

# 9.5 Decision Workflow

Every candidate follows the same process.

```text
Signals

↓

Quality Evaluation

↓

Score Calculation

↓

Risk Evaluation

↓

Confidence Calculation

↓

Decision

↓

Explanation
```

This workflow ensures that every opportunity is evaluated consistently.

---

# 9.6 Decision Categories

Every analysed stock receives one recommendation.

Current categories:

```text
BUY

WATCH

HOLD

IGNORE
```

Future versions may introduce:

STRONG BUY

SPECULATIVE BUY

SELL

REDUCE

EXIT

The architecture has been designed to support these extensions without structural changes.

---

# 9.7 Confidence Score

Every recommendation includes a confidence score.

Range:

```text
0 — 100
```

Example:

```text
Confidence

96

Very High
```

The confidence score reflects the quality of the technical setup, not the certainty of future market behaviour.

Markets remain uncertain.

Confidence measures the strength of available evidence.

---

# 9.8 Decision Factors

The Decision Engine evaluates multiple independent dimensions.

Examples include:

Trend

Momentum

Volume

Volatility

Market Structure

Support

Resistance

Relative Strength

Liquidity

Risk

Every factor contributes independently.

No single indicator should dominate the decision.

---

# 9.9 Weighting Strategy

The Decision Engine combines category scores using configurable weights.

Example:

```text
Trend

30%

Momentum

25%

Structure

15%

Volume

10%

Volatility

10%

Relative Strength

10%
```

The exact values remain configurable and may evolve as Orion improves.

The architecture therefore separates configuration from implementation.

---

# 9.10 Positive Factors

Examples of positive evidence:

Price above EMA20

Price above EMA50

Strong ADX

Healthy RSI

Positive MACD crossover

Increasing volume

Higher highs

Higher lows

Strong relative strength

Bullish breakout

Each positive factor increases confidence.

---

# 9.11 Negative Factors

Examples:

Weak volume

Bearish divergence

Falling momentum

High volatility

Resistance rejection

Overbought conditions

Poor liquidity

Sideways market

Conflicting signals

Each negative factor reduces confidence.

---

# 9.12 Contradictions

Markets are rarely perfect.

Example:

Trend

Strong

Momentum

Weak

Volume

Average

Volatility

Healthy

Rather than ignoring contradictions, Orion records them.

The final recommendation should always reflect both strengths and weaknesses.

---

# 9.13 DecisionResult

The Decision Engine returns a structured object.

Example:

```text
DecisionResult

Recommendation

BUY

Confidence

92

Overall Score

89

Strengths

Weaknesses

Supporting Signals

Warnings

Timestamp
```

This object becomes the standard output for the Portfolio Engine and GUI.

---

# 9.14 Explainability

Every recommendation must be fully explainable.

Example:

```text
Recommendation

BUY

Reasoning

Strong long-term trend.

Healthy momentum.

Volume confirms breakout.

ADX indicates trend strength.

RSI remains below overbought levels.

No significant technical weaknesses detected.
```

The explanation is generated from deterministic analysis.

Future AI modules may improve readability but should never invent reasons.

---

# 9.15 Ranking Engine

The Decision Engine works closely with the Ranking Engine.

Example:

```text
6204 Stocks

↓

487 Candidates

↓

39 High Quality

↓

11 Excellent

↓

Top 3 Opportunities
```

Ranking always compares opportunities relative to each other.

The highest scoring opportunities become today's recommendations.

---

# 9.16 Configuration

Decision thresholds should remain configurable.

Example:

```text
BUY

85+

WATCH

70-84

HOLD

50-69

IGNORE

Below 50
```

Configuration files allow future optimisation without changing application code.

---

# 9.17 Performance

Decision making should require minimal computation.

Most calculations have already been completed inside earlier layers.

The Decision Engine primarily performs:

* comparisons
* weighting
* ranking
* explanation generation

Target processing time:

```text
6200 Stocks

↓

< 1 second
```

---

# 9.18 Future Expansion

Future versions may include:

Machine learning confidence adjustment

Sector rotation influence

Economic calendar awareness

Earnings risk detection

News sentiment

Macroeconomic filters

Portfolio-aware recommendations

Adaptive scoring

Strategy-specific decision profiles

Because the Decision Engine consumes abstract signals rather than raw indicators, these additions can be integrated without redesign.

---

# 9.19 Architectural Principles

The Decision Engine follows eight guiding principles.

**Evidence Based**

Recommendations depend on measurable technical evidence.

---

**Explainable**

Every recommendation must justify itself.

---

**Consistent**

Identical input always produces identical output.

---

**Balanced**

Positive and negative evidence are both considered.

---

**Transparent**

The complete reasoning chain remains visible.

---

**Configurable**

Thresholds and weights may evolve without architectural changes.

---

**Independent**

Decision logic remains isolated from portfolio management and execution.

---

**Extensible**

Future analytical techniques can be added without rewriting existing components.

---

# 9.20 Long-Term Vision

The Decision Engine represents Orion's digital trading analyst.

Its purpose is not to predict markets with certainty.

Instead it evaluates available evidence objectively, weighs competing technical observations and produces consistent, transparent recommendations.

Ultimately, this engine should provide the same structured reasoning that an experienced discretionary trader would use—while remaining deterministic, measurable and reproducible.

The Decision Engine is therefore the heart of Orion's investment intelligence.

---

# End of Chapter 9

The next chapter introduces the **Portfolio Engine**, where Orion transitions from analysing markets to managing capital. This chapter defines position management, capital allocation, diversification, portfolio tracking and how individual trading opportunities become part of a coherent investment strategy.
# 10. Portfolio Engine Architecture

## 10.1 Introduction

Up to this point, Project Orion has answered one fundamental question:

> **"Which stocks represent the best technical opportunities?"**

The Portfolio Engine answers the next question:

> **"Given the available opportunities, how should capital be allocated?"**

Finding a strong technical setup is only part of successful investing.

A professional trading system must also determine:

* How many positions should be opened?
* How much capital should be allocated to each position?
* Is the portfolio sufficiently diversified?
* Is total portfolio risk acceptable?
* Does a new opportunity improve the existing portfolio?

The Portfolio Engine transforms independent trade ideas into a coherent investment portfolio.

---

# 10.2 Mission

The mission of the Portfolio Engine is:

> Maximise long-term portfolio quality while maintaining controlled risk.

The Portfolio Engine is not concerned with predicting markets.

Instead, it manages capital intelligently using the recommendations generated by the Decision Engine.

---

# 10.3 Position Inside Orion

```text
Decision Engine

        │

        ▼

Portfolio Engine

        │

        ▼

Risk Manager

        │

        ▼

Trade Planner
```

This ordering is intentional.

First determine which opportunities are attractive.

Then determine whether they fit inside the portfolio.

Only afterwards calculate position size and trade execution.

---

# 10.4 Responsibilities

The Portfolio Engine is responsible for:

* Portfolio construction
* Position tracking
* Cash management
* Capital allocation
* Diversification
* Exposure monitoring
* Portfolio statistics
* Portfolio performance

It is **not** responsible for:

* Technical analysis
* Risk calculations
* Stop-loss generation
* Order execution

---

# 10.5 Portfolio Philosophy

Project Orion does not attempt to own every attractive stock.

Instead it attempts to own the **best combination** of attractive stocks.

This distinction is important.

Example:

Suppose today's scan produces:

```text
NVDA

AMD

TSM

ASML
```

All four companies belong to the semiconductor industry.

Buying all four may technically satisfy the Decision Engine but could expose the portfolio to unnecessary sector concentration.

The Portfolio Engine therefore evaluates opportunities within the context of the entire portfolio.

---

# 10.6 Portfolio Model

The portfolio consists of three primary components.

```text
Cash

Open Positions

Closed Positions
```

Every position includes:

Ticker

Entry Date

Entry Price

Current Price

Quantity

Allocated Capital

Current Profit

Stop-loss

Take-profit

Decision Confidence

Sector

Industry

Status

---

# 10.7 Capital Allocation

The Portfolio Engine determines how available capital should be distributed.

Example:

```text
Portfolio

€25,000

Cash

€7,000

Invested

€18,000

Open Positions

9
```

Allocation strategies may evolve over time.

Initial implementation:

Equal-weight allocation.

Future implementations:

Confidence-weighted allocation.

Risk-weighted allocation.

Volatility-adjusted allocation.

Kelly Criterion.

Portfolio optimisation.

---

# 10.8 Position Limits

The engine enforces portfolio constraints.

Examples:

Maximum positions

15

Maximum sector exposure

25%

Maximum single position

10%

Minimum cash reserve

10%

Maximum correlated positions

3

These values remain configurable.

---

# 10.9 Diversification

Diversification is evaluated across several dimensions.

Examples:

Sector

Industry

Market Capitalisation

Growth vs Value

Volatility

Geography (future)

Correlation (future)

The objective is to reduce concentration risk.

---

# 10.10 Portfolio Statistics

The Portfolio Engine continuously calculates portfolio metrics.

Examples:

Current Value

Cash Balance

Invested Capital

Available Capital

Open Profit

Closed Profit

Win Rate

Average Gain

Average Loss

Profit Factor

Maximum Drawdown

Average Holding Time

Sharpe Ratio (future)

Sortino Ratio (future)

These statistics provide insight into portfolio quality over time.

---

# 10.11 Position Lifecycle

Every position follows a defined lifecycle.

```text
Opportunity

↓

Approved

↓

Purchased

↓

Open Position

↓

Managed

↓

Closed

↓

Archived
```

Historical information is never discarded.

Every completed trade contributes to long-term performance analysis.

---

# 10.12 Portfolio Evaluation

Whenever Orion discovers a new opportunity, it evaluates several questions.

Example:

Is enough cash available?

Does this increase concentration risk?

Does this improve expected portfolio quality?

Should another position be replaced?

Does this exceed risk limits?

Only if the portfolio benefits should the opportunity proceed to the Risk Manager.

---

# 10.13 Portfolio Quality Score

Future versions will calculate an overall Portfolio Quality Score.

Example:

```text
Diversification

91

Capital Allocation

88

Sector Balance

95

Risk Exposure

84

Cash Reserve

92

Overall Portfolio Quality

90
```

This allows Orion to evaluate not only individual trades, but the health of the entire investment portfolio.

---

# 10.14 Historical Performance

Every completed trade contributes to Orion's learning database.

Stored information includes:

Entry

Exit

Holding Period

Maximum Drawdown

Maximum Gain

Final Return

Risk / Reward

Decision Confidence

Sector

Strategy

Future analytical modules can use this information to evaluate strategy performance over long periods.

---

# 10.15 Future Expansion

Future capabilities may include:

Portfolio optimisation

Tax-aware allocation

Dividend tracking

Currency exposure

Correlation matrix

Monte Carlo simulation

Scenario analysis

Benchmark comparison

Multi-account support

Institutional portfolio management

The architecture has been designed to accommodate these additions without restructuring existing components.

---

# 10.16 Design Principles

The Portfolio Engine follows the following principles.

**Capital Preservation**

Protect capital before seeking returns.

---

**Diversification**

Avoid unnecessary concentration.

---

**Objectivity**

Allocation decisions should be based on measurable portfolio characteristics.

---

**Configurability**

Portfolio rules remain configurable.

---

**Historical Integrity**

Historical trades are never deleted.

---

**Scalability**

The portfolio architecture should support both private investors and significantly larger portfolios.

---

# 10.17 Long-Term Vision

The Portfolio Engine is intended to become Orion's investment manager.

Rather than evaluating trades in isolation, it continuously considers the broader portfolio context.

As Orion evolves, the Portfolio Engine will transform from a simple position tracker into a sophisticated portfolio optimisation system capable of balancing opportunity, diversification, risk and capital efficiency.

Its purpose is not merely to own good stocks, but to build the strongest possible portfolio from the opportunities available at any given time.

---

# End of Chapter 10

The next chapter introduces the **Risk Management Architecture**, where Orion determines acceptable exposure, calculates position sizing, evaluates drawdown risk and ensures that capital preservation always takes precedence over return generation.
# 11. Risk Management Architecture

## 11.1 Introduction

Professional trading is not primarily about finding winning trades.

It is about managing risk.

A trader can identify excellent opportunities and still lose money if position sizing, exposure and capital preservation are ignored.

For this reason, Risk Management is treated as a completely independent subsystem within Project Orion.

Risk Management does not attempt to maximise returns.

Its purpose is to ensure that losses remain controlled while allowing profitable strategies to perform over the long term.

Within Orion, **risk always has priority over opportunity**.

---

# 11.2 Mission

The mission of the Risk Manager is:

> Preserve capital while enabling sustainable long-term portfolio growth.

Every recommendation generated by Orion must first pass through the Risk Manager before becoming an executable trade.

Even the strongest BUY recommendation may be rejected if portfolio risk exceeds acceptable limits.

---

# 11.3 Position Inside Orion

```text
Decision Engine

        │

        ▼

Portfolio Engine

        │

        ▼

Risk Manager

        │

        ▼

Trade Planner

        │

        ▼

GUI
```

The Risk Manager acts as the final safety layer before a trade plan is generated.

---

# 11.4 Responsibilities

The Risk Manager is responsible for:

* Position sizing
* Portfolio exposure
* Maximum drawdown protection
* Daily risk monitoring
* Stop-loss distance validation
* Risk/Reward evaluation
* Capital preservation
* Risk statistics

It is **not** responsible for:

* Technical analysis
* Indicator calculations
* Signal generation
* Portfolio optimisation
* Trade execution

---

# 11.5 Core Philosophy

The following principles guide every risk calculation.

### Rule 1

Never risk unnecessary capital.

### Rule 2

Protect the portfolio before seeking additional return.

### Rule 3

No single trade should materially damage the portfolio.

### Rule 4

Risk should be measurable before a position is opened.

### Rule 5

Risk must remain visible at all times.

---

# 11.6 Risk Categories

The Risk Manager evaluates several independent dimensions.

## Trade Risk

Risk associated with a single trade.

Examples:

Entry price

Stop-loss distance

Risk per share

Risk percentage

Expected reward

Risk / Reward ratio

---

## Portfolio Risk

Risk associated with the entire portfolio.

Examples:

Total exposure

Cash reserve

Open positions

Sector concentration

Correlation

---

## Market Risk

Future versions may evaluate:

High VIX

Major index weakness

Economic events

Interest rate decisions

Market breadth

These factors may influence maximum allowable exposure.

---

# 11.7 Position Sizing

One of the primary responsibilities of the Risk Manager is determining position size.

Example:

```text
Portfolio Value

€20,000

Maximum Risk

1%

Maximum Loss

€200
```

If the calculated stop-loss distance equals:

```text
€4 per share
```

Maximum position:

```text
€200 / €4

=

50 shares
```

This calculation should be fully automated.

---

# 11.8 Exposure Limits

Future configuration:

```text
Maximum Portfolio Exposure

90%

Maximum Single Position

8%

Maximum Sector Exposure

25%

Maximum Industry Exposure

20%

Minimum Cash

10%
```

All limits remain configurable.

---

# 11.9 Risk / Reward

Every proposed trade receives a Risk / Reward calculation.

Example:

```text
Entry

$100

Stop Loss

$95

Take Profit

$115

Risk

$5

Reward

$15

Risk / Reward

1 : 3
```

Trades below the configured minimum ratio may be rejected.

---

# 11.10 Stop-Loss Validation

The Risk Manager validates proposed stop-loss levels.

Future techniques include:

ATR-based stop

Swing Low

Support Level

Moving Average

Volatility Stop

Trailing Stop

The Trade Planner may suggest levels, but the Risk Manager validates them.

---

# 11.11 Portfolio Heat

Future versions will calculate Portfolio Heat.

Portfolio Heat represents the total capital currently at risk.

Example:

```text
Trade 1

0.8%

Trade 2

1.0%

Trade 3

0.7%

Trade 4

0.9%

Portfolio Heat

3.4%
```

Maximum Portfolio Heat remains configurable.

---

# 11.12 Drawdown Protection

Protecting capital during losing periods is critical.

Future safeguards include:

Maximum Daily Loss

Maximum Weekly Loss

Maximum Monthly Drawdown

Consecutive Losing Trades

Reduced Position Sizes

Trading Pause

These rules prevent emotional overtrading.

---

# 11.13 RiskResult

Every evaluation produces a structured object.

Example:

```text
RiskResult

Position Size

Maximum Risk

Risk Percentage

Exposure

Portfolio Heat

Risk / Reward

Approved

Warnings
```

This object becomes input for the Trade Planner.

---

# 11.14 Historical Risk Statistics

The Risk Manager maintains long-term statistics.

Examples:

Average Risk

Average Position Size

Average Drawdown

Largest Winning Trade

Largest Losing Trade

Average Risk / Reward

Average Holding Time

Maximum Portfolio Heat

These statistics help evaluate the effectiveness of the overall trading strategy.

---

# 11.15 Future Expansion

Potential future enhancements include:

Dynamic Position Sizing

Kelly Criterion

Volatility Targeting

Correlation-Based Exposure

Beta Exposure

Monte Carlo Risk

Stress Testing

Scenario Simulation

Machine Learning Risk Adjustment

Institutional Risk Models

The modular architecture allows these capabilities to be integrated gradually.

---

# 11.16 Design Principles

The Risk Manager follows the following principles.

**Capital First**

Capital preservation always takes priority.

---

**Consistency**

Identical portfolio conditions should always produce identical risk calculations.

---

**Transparency**

Every risk calculation should be explainable.

---

**Configurability**

Risk limits should be adjustable without changing application code.

---

**Isolation**

Risk calculations remain independent from technical analysis.

---

**Scalability**

Risk management should support portfolios of any practical size.

---

# 11.17 Long-Term Vision

The Risk Manager is intended to become Orion's capital protection system.

Its purpose is not to prevent losses entirely—losses are an unavoidable part of investing—but to ensure that no individual trade, sequence of trades or market event can threaten the long-term health of the portfolio.

In future versions, the Risk Manager will evolve into a comprehensive portfolio risk platform capable of continuously evaluating exposure, drawdown, diversification, market conditions and capital allocation in real time.

Together with the Portfolio Engine and Decision Engine, it forms the foundation of Orion's investment discipline.

---

# End of Chapter 11

The next chapter introduces the **Trade Planner**, where approved investment opportunities are transformed into complete, executable trading plans containing entry price, stop-loss, take-profit, position size, estimated holding period and execution guidance.
# 12. Trade Planner Architecture

## 12.1 Introduction

A BUY recommendation alone is not sufficient for professional trading.

Knowing *what* to buy is only one part of the decision-making process.

A trader must also determine:

* When to enter.
* How much to buy.
* Where to place a stop-loss.
* Where to take profits.
* What the expected holding period is.
* Whether the reward justifies the risk.

The Trade Planner transforms an approved investment opportunity into a complete and executable trading plan.

Its objective is to eliminate uncertainty after a BUY recommendation has been made.

Rather than leaving execution entirely to the trader, Orion provides a structured plan that can be reviewed, adjusted if necessary and executed with confidence.

---

# 12.2 Mission

The mission of the Trade Planner is:

> Transform a technically approved opportunity into a practical trading plan.

Every generated plan should be:

* Objective
* Explainable
* Consistent
* Risk-aware
* Ready for execution

The Trade Planner does not decide **whether** a stock should be bought.

That decision has already been made by the Decision Engine.

Instead, it answers:

> **"How should this trade be executed?"**

---

# 12.3 Position Inside Orion

```text
Decision Engine

        │

        ▼

Portfolio Engine

        │

        ▼

Risk Manager

        │

        ▼

Trade Planner

        │

        ▼

GUI
```

The Trade Planner is therefore the final analytical component before information reaches the user.

---

# 12.4 Responsibilities

The Trade Planner is responsible for:

* Entry price calculation
* Stop-loss proposal
* Take-profit proposal
* Position size integration
* Risk / Reward calculation
* Trade summary generation
* Execution checklist
* Trade metadata

It is **not** responsible for:

* Technical analysis
* Indicator calculation
* Signal generation
* Portfolio optimisation
* Broker execution

---

# 12.5 Trade Lifecycle

Every approved opportunity follows the same process.

```text
BUY Recommendation

↓

Risk Validation

↓

Trade Planning

↓

Execution Plan

↓

User Review

↓

Trade Execution

↓

Position Monitoring
```

This lifecycle ensures that every position enters the market in a structured and repeatable manner.

---

# 12.6 Entry Strategy

The Trade Planner proposes an entry based on market conditions.

Future strategies may include:

Current Market Price

Breakout Entry

Pullback Entry

Limit Order

Stop Order

VWAP Entry

Support Bounce

Gap Entry

The selected strategy should be configurable.

---

# 12.7 Stop-Loss Strategy

Every trade requires a clearly defined exit point in case the market moves against the position.

Future stop-loss techniques include:

ATR Stop

Swing Low

Support Level

Moving Average

Percentage Stop

Volatility Stop

Dynamic Stop

Trailing Stop

Each generated stop-loss should include a justification.

---

# 12.8 Take-Profit Strategy

The Trade Planner proposes one or more target levels.

Examples:

Fixed Risk / Reward

Resistance Level

Measured Move

ATR Projection

Trend Continuation

Partial Profit Levels

Future versions may support multiple sequential targets.

Example:

```text
Target 1

25%

Target 2

50%

Target 3

100%
```

---

# 12.9 Holding Period

Every trade receives an estimated holding period.

Examples:

Very Short

1–3 days

Swing Trade

4–15 days

Position Trade

15–60 days

The estimate is based on historical behaviour and current market structure.

---

# 12.10 TradePlan Object

Every generated plan returns a structured object.

Example:

```text
TradePlan

Ticker

Entry Price

Stop Loss

Take Profit

Risk / Reward

Position Size

Holding Period

Expected Return

Confidence

Execution Notes
```

This object becomes the standard representation of a proposed trade throughout Orion.

---

# 12.11 Execution Checklist

To encourage disciplined trading, every TradePlan includes an execution checklist.

Example:

```text
✓ Trend confirmed

✓ Volume confirms breakout

✓ Stop-loss defined

✓ Risk below portfolio limit

✓ Position size approved

✓ Reward exceeds minimum requirement
```

The checklist provides a final review before execution.

---

# 12.12 Trade Summary

The Trade Planner generates a concise summary suitable for display in the GUI.

Example:

```text
PANW

Recommendation

BUY

Confidence

94%

Entry

$214.30

Stop Loss

$206.10

Take Profit

$231.80

Risk / Reward

1 : 2.9

Estimated Duration

8–14 trading days
```

The summary is intended for quick decision making.

---

# 12.13 Explainability

Every proposed trade should explain itself.

Example:

```text
Reasoning

Entry is placed above recent consolidation.

Stop-loss is positioned below confirmed support.

Target is based on previous resistance.

Risk / Reward satisfies portfolio requirements.

Volume confirms breakout.
```

This information may later be expanded by the AI Layer into natural language.

---

# 12.14 Future Expansion

The Trade Planner has been designed for future capabilities such as:

Multiple entry strategies

Scaling into positions

Scaling out of positions

Trailing stop automation

Broker order generation

Options strategies

Futures contracts

Automatic execution templates

Paper trading integration

Broker-specific order formatting

The modular architecture allows these features to be introduced incrementally.

---

# 12.15 Design Principles

The Trade Planner follows the following principles.

**Execution Ready**

Every approved trade should result in a practical execution plan.

---

**Consistency**

Trades generated under identical market conditions should produce identical plans.

---

**Risk Awareness**

Every recommendation must respect the limits defined by the Risk Manager.

---

**Transparency**

Every proposed level should include an explanation.

---

**Configurability**

Execution strategies should remain configurable.

---

**Extensibility**

Future trading styles should integrate without redesigning the architecture.

---

# 12.16 Long-Term Vision

The Trade Planner represents the final step before execution.

Rather than presenting isolated technical information, it translates Orion's complete analytical process into a structured trading plan that a disciplined trader can review and execute.

As Orion evolves, the Trade Planner will become increasingly sophisticated, supporting multiple execution strategies, adaptive exits, partial profit-taking and broker integration.

Its purpose is to bridge the gap between market analysis and real-world trading execution while maintaining the transparency and consistency that define the Orion architecture.

---

# End of Chapter 12

The next chapter introduces the **Artificial Intelligence Layer**—one of the most ambitious components of Project Orion. This layer will not replace deterministic analysis but will explain, summarise and communicate Orion's reasoning in clear, human language, transforming complex technical analysis into insights that every trader can understand.
# 13. Artificial Intelligence Layer

## 13.1 Introduction

Artificial Intelligence is one of the defining characteristics of Project Orion.

However, Orion deliberately takes a fundamentally different approach from many modern AI-driven financial applications.

The AI Layer is **not responsible for making investment decisions.**

Instead, it serves as an intelligent communication layer that translates complex technical analysis into clear, structured and understandable explanations.

The AI Layer never invents information.

It never predicts markets.

It never overrides deterministic analysis.

Its responsibility is to explain what Orion already knows.

---

# 13.2 Mission

The mission of the AI Layer is:

> Transform deterministic market analysis into human-readable intelligence.

Rather than replacing technical analysis, AI enhances accessibility.

Its objective is to help traders understand why Orion reaches a particular conclusion.

---

# 13.3 Position Inside Orion

```text
Historical Data

        │

        ▼

Analysis Engine

        │

        ▼

Signal Engine

        │

        ▼

Decision Engine

        │

        ▼

Trade Planner

        │

        ▼

Artificial Intelligence Layer

        │

        ▼

GUI
```

The AI Layer is intentionally positioned **after** every deterministic calculation.

This ensures that AI never influences objective analysis.

---

# 13.4 Responsibilities

The AI Layer is responsible for:

* Explaining recommendations
* Summarising analysis
* Translating technical language
* Writing trade reports
* Generating portfolio summaries
* Answering "Why?" questions
* Educational assistance

It is **not** responsible for:

* Technical calculations
* Indicator generation
* Risk calculations
* Trade execution
* Portfolio management

---

# 13.5 Core Philosophy

Project Orion follows one simple principle:

**AI explains. Engines decide.**

This philosophy prevents hallucinations and ensures every recommendation remains grounded in measurable data.

If the Decision Engine cannot justify a BUY recommendation, the AI Layer must not invent one.

---

# 13.6 AI Input

The AI Layer never accesses raw market data directly.

Instead it consumes structured outputs produced by previous engines.

Example:

```text
DecisionResult

AnalysisResult

TradePlan

PortfolioSummary

RiskResult
```

This keeps AI independent from market data providers and mathematical calculations.

---

# 13.7 AI Output

The AI Layer may generate several types of content.

Examples:

Trade Explanation

Portfolio Summary

Daily Market Brief

Weekly Performance Review

Risk Explanation

Indicator Explanation

Educational Feedback

Every output should be understandable for both beginners and experienced traders.

---

# 13.8 Example Trade Explanation

Example:

```text
Recommendation

BUY

Confidence

94%

Explanation

PANW is currently trading above both the 20-day and
50-day moving averages, indicating a healthy upward trend.

Momentum remains positive, supported by a bullish MACD
configuration and an RSI of 59, suggesting additional upside
potential without entering overbought territory.

Trading volume is above the recent average,
confirming participation from market participants.

Overall, the current technical structure supports
a medium-term swing trade.
```

The explanation should describe—not reinterpret—the deterministic analysis.

---

# 13.9 Portfolio Commentary

Future versions may summarise the entire portfolio.

Example:

```text
Portfolio Summary

You currently hold nine open positions.

Technology represents 28% of your exposure.

Cash allocation remains healthy at 18%.

Average portfolio confidence is 91%.

Current portfolio risk remains within configured limits.
```

---

# 13.10 Daily Market Report

The AI Layer may generate daily summaries.

Example:

```text
Good morning.

Today's scan analysed 6,204 US stocks.

487 passed the initial filters.

23 showed strong technical characteristics.

Three exceptional opportunities were identified.

Overall market momentum remains moderately bullish,
with technology continuing to outperform most sectors.
```

This report should be generated automatically from deterministic statistics.

---

# 13.11 Educational Mode

One long-term objective is helping users improve as traders.

Examples:

"What is RSI?"

"Why is ADX important?"

"Why was this opportunity rejected?"

"What does a bullish MACD crossover mean?"

Educational explanations should always reference Orion's own analysis.

---

# 13.12 AI Safety Principles

The AI Layer follows strict safety rules.

AI must never:

Predict guaranteed returns.

Promise profits.

Recommend ignoring risk management.

Invent technical signals.

Invent numerical values.

Override deterministic analysis.

Transparency takes priority over creativity.

---

# 13.13 Explainability

Every AI-generated explanation should remain traceable.

Example:

```text
Statement

Trend is bullish.

↓

Source

Trend Analyzer

↓

Evidence

EMA20 > EMA50

Higher Highs

ADX = 31
```

Every sentence produced by the AI should ultimately be traceable to measurable evidence.

---

# 13.14 Future Capabilities

The AI Layer has been designed for continuous expansion.

Potential future features include:

Voice explanations

Interactive AI chat

Trade journaling

Portfolio coaching

Market education

Strategy comparison

Historical trade reviews

Personalised learning

Multi-language support

Speech synthesis

These features can be added without changing the deterministic architecture.

---

# 13.15 Design Principles

The AI Layer follows the following principles.

**Truthfulness**

Every statement must be supported by deterministic analysis.

---

**Transparency**

The user should always understand where conclusions originate.

---

**Education**

The AI should improve the trader's understanding over time.

---

**Consistency**

Similar market situations should produce similar explanations.

---

**Modularity**

The AI Layer remains independent from mathematical calculations.

---

**Extensibility**

Future AI models should integrate without redesigning the Orion architecture.

---

# 13.16 Long-Term Vision

The Artificial Intelligence Layer represents Orion's communication interface rather than its analytical brain.

Its purpose is to make advanced market analysis accessible, understandable and actionable without sacrificing transparency or technical accuracy.

In the long term, Orion should feel less like a traditional stock screener and more like an experienced market analyst sitting beside the trader—capable of explaining every recommendation, answering questions and providing meaningful context while remaining firmly grounded in deterministic analysis.

The AI Layer is therefore not intended to replace the trader, but to make better-informed trading decisions possible.

---

# End of Chapter 13

The next chapter introduces the **Graphical User Interface (GUI) Architecture**, where every Orion subsystem comes together in a professional desktop application. This chapter defines the dashboard, interactive charts, portfolio screens, market overview, AI assistant and overall user experience that will ultimately become the public face of Project Orion.
# 14. Graphical User Interface (GUI) Architecture

## 14.1 Introduction

The Graphical User Interface represents the public face of Project Orion.

While previous architectural layers perform market analysis, portfolio management and risk evaluation, the GUI is responsible for presenting this information in a professional, intuitive and highly interactive manner.

The GUI should never contain business logic.

Its responsibility is limited to visualisation, interaction and user workflow.

Every number displayed on screen originates from deterministic engines elsewhere in the architecture.

The GUI simply transforms structured data into a user experience.

---

# 14.2 Vision

The long-term vision for the Orion GUI is to create a professional desktop trading application comparable in quality to commercial trading platforms.

The application should immediately communicate professionalism, confidence and clarity.

Opening Orion should feel like opening a Bloomberg Terminal, TradingView Desktop or a professional institutional trading workstation.

The interface should prioritise:

* clarity
* speed
* consistency
* readability
* actionable information

The user should never need to search for important information.

The most valuable insights should always be immediately visible.

---

# 14.3 Design Philosophy

The Orion GUI follows five guiding principles.

### Information First

Important information should always receive the most visual emphasis.

---

### Minimal Noise

Decorative elements should never distract from decision making.

---

### Progressive Disclosure

Simple information should be visible immediately.

Detailed analysis should appear when requested.

---

### Consistency

Every screen should behave similarly.

Buttons, colours and layouts should remain predictable.

---

### Speed

The application should feel responsive at all times.

Animations should support usability rather than decoration.

---

# 14.4 High-Level Layout

```text id="gui01"
┌────────────────────────────────────────────────────────────────────┐
│ PROJECT ORION                               MARKET OPEN ● LIVE     │
├────────────────────────────────────────────────────────────────────┤
│ Dashboard │ Scanner │ Portfolio │ History │ AI │ Settings          │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│ Universe Summary                    Top Opportunities              │
│ Market Overview                     Watchlist                      │
│ Portfolio Snapshot                  Recent Activity                │
│                                                                    │
├────────────────────────────────────────────────────────────────────┤
│                    Interactive Market Analysis                     │
│                                                                    │
│                    Candlestick Chart                               │
│                                                                    │
├──────────────────────────────┬─────────────────────────────────────┤
│ Technical Indicators         │ AI Analysis                         │
├──────────────────────────────┼─────────────────────────────────────┤
│ RSI                          │ Why Orion selected this stock       │
│ MACD                         │                                     │
│ EMA                          │ Trade Summary                       │
│ ADX                          │                                     │
│ ATR                          │ Risk Assessment                     │
└──────────────────────────────┴─────────────────────────────────────┘
```

---

# 14.5 Primary Navigation

The main application consists of several workspaces.

Dashboard

Scanner

Portfolio

Trade History

AI Assistant

Settings

Future versions may introduce additional workspaces without changing the navigation philosophy.

---

# 14.6 Dashboard

The Dashboard serves as Orion's home screen.

Its purpose is to answer one question:

> **"What do I need to know right now?"**

The dashboard should display:

Current market status

Universe size

Number of scanned stocks

Active opportunities

Portfolio value

Cash available

Open positions

Market sentiment

Recent scan duration

Cache status

The Dashboard should remain informative without overwhelming the user.

---

# 14.7 Scanner Screen

The Scanner is Orion's primary analytical workspace.

Each opportunity should be displayed as a professional information card.

Example:

```text id="gui02"
Ticker

PANW

Recommendation

BUY

Confidence

96%

Overall Score

94

Trend

Excellent

Momentum

Strong

Risk

Low
```

Selecting an opportunity opens the detailed analysis screen.

---

# 14.8 Stock Analysis Screen

The detailed stock view combines all analytical layers.

Example layout:

```text id="gui03"
Ticker

PANW

Current Price

$214.30

Recommendation

BUY

Confidence

96%

Trend

Excellent

Momentum

Strong

Structure

Bullish

Risk

Low
```

Below this summary, Orion displays the interactive chart and analytical panels.

---

# 14.9 Interactive Chart

The candlestick chart is the visual centrepiece of Orion.

Features include:

Daily candles

Weekly candles

Monthly candles

Volume

EMA overlays

SMA overlays

Bollinger Bands

Support lines

Resistance lines

Trend lines

Zoom

Pan

Crosshair

Indicator overlays

Future versions may include drawing tools and multi-chart layouts.

---

# 14.10 Indicator Panel

The Indicator Panel displays Orion's technical measurements.

Example:

```text id="gui04"
RSI

58.2

Healthy

MACD

Bullish

ADX

31

Strong Trend

ATR

2.81

Moderate Volatility

EMA20

Above EMA50

Bullish
```

Each indicator links directly to its deterministic calculation.

---

# 14.11 AI Analysis Panel

The AI panel translates technical information into natural language.

Example:

```text id="gui05"
Why Orion selected PANW

Strong long-term trend.

Healthy momentum.

Increasing trading volume.

No significant technical weaknesses detected.

Risk profile remains favourable.

Historical setups with similar characteristics
performed well in previous market conditions.
```

This explanation is generated entirely from deterministic engine outputs.

---

# 14.12 Trade Plan Panel

Every BUY recommendation includes a complete trade plan.

Example:

```text id="gui06"
Entry

214.30

Stop Loss

206.10

Take Profit

231.80

Risk / Reward

1 : 2.9

Estimated Duration

7-14 trading days

Suggested Position Size

48 shares
```

This panel represents the practical execution layer of Orion.

---

# 14.13 Portfolio Screen

The Portfolio workspace displays:

Current holdings

Open profit

Closed profit

Cash balance

Allocation

Sector exposure

Performance graph

Historical equity curve

Portfolio quality score

Future versions may include benchmark comparison and performance attribution.

---

# 14.14 Watchlist

The Watchlist tracks interesting opportunities that are not yet BUY candidates.

Each entry should display:

Ticker

Current Price

Trend

Momentum

Confidence

Distance to BUY threshold

Recent changes

This allows users to monitor developing opportunities.

---

# 14.15 Historical Trades

Every completed trade remains accessible.

Information includes:

Entry

Exit

Return

Holding period

Decision confidence

Trade notes

Risk

Sector

Outcome

Historical trades become an important learning resource.

---

# 14.16 Theme

The Orion interface follows a professional dark theme.

Design principles:

Dark neutral background

High contrast typography

Limited accent colours

Green for positive information

Red for warnings

Blue for informational content

Colours should support interpretation rather than decoration.

---

# 14.17 Responsiveness

The GUI should remain responsive during scans.

Long-running operations should execute asynchronously.

Progress indicators should continuously inform the user.

The interface should never appear frozen.

---

# 14.18 Future Capabilities

The GUI has been designed for future expansion.

Potential additions include:

Multiple monitor support

Detachable panels

Workspace layouts

Floating charts

News feed

Economic calendar

AI chat window

Options analysis

Heat maps

Sector rotation dashboard

Broker integration

Mobile companion application

---

# 14.19 Design Principles

The GUI follows the following principles.

**Presentation Only**

Business logic belongs exclusively to the engine layers.

---

**Consistency**

Every screen should behave predictably.

---

**Speed**

Interactions should feel immediate.

---

**Professional Appearance**

The application should resemble institutional trading software.

---

**Scalability**

New screens should integrate without redesigning the interface.

---

**Explainability**

Every displayed value should be traceable to deterministic calculations.

---

# 14.20 Long-Term Vision

The Graphical User Interface is intended to become the complete operational workspace for Project Orion.

It should seamlessly combine deterministic analysis, intelligent explanations, portfolio management and trade planning into a single coherent experience.

The ultimate goal is that opening Orion feels like working alongside a professional market analyst—where every opportunity is supported by transparent analysis, every recommendation is actionable and every decision is backed by measurable evidence.

The GUI is not merely a visual layer.

It is the window through which users experience the entire Orion platform.

---

# End of Chapter 14

The next chapter introduces the **Testing & Quality Assurance Architecture**, defining unit testing, integration testing, regression testing, performance testing, coding standards and continuous quality control. This chapter establishes how Orion maintains reliability as the project grows in complexity.
# 15. Testing & Quality Assurance Architecture

## 15.1 Introduction

Reliability is one of the most important characteristics of Project Orion.

A trading platform that occasionally produces incorrect calculations, inconsistent recommendations or unexpected behaviour cannot be trusted.

For this reason, testing is not considered an optional development activity.

Testing is an integral part of Orion's architecture.

Every new module introduced into the system should be accompanied by an appropriate testing strategy before it becomes part of the production codebase.

Quality Assurance is therefore viewed as a continuous engineering discipline rather than a final development phase.

---

# 15.2 Mission

The mission of Orion's Quality Assurance architecture is:

> Ensure that every component behaves predictably, consistently and correctly throughout the lifetime of the project.

Every architectural change should increase functionality without reducing reliability.

---

# 15.3 Testing Philosophy

Project Orion follows several core testing principles.

## Test Everything Important

Critical business logic should never remain untested.

---

## Test Independently

Every module should be testable without requiring the complete application.

---

## Test Automatically

Whenever possible, tests should execute automatically.

---

## Test Before Integration

Individual components should be verified before they interact with other systems.

---

## Prevent Regression

Every bug that is fixed should receive a dedicated regression test.

---

# 15.4 Testing Pyramid

Project Orion follows a layered testing strategy.

```text id="test01"
                 Manual GUI Tests

                      ▲

              Integration Tests

                      ▲

                Unit Tests

                      ▲

           Mathematical Validation
```

The majority of testing effort should be concentrated at the lower layers.

Unit tests are significantly faster, simpler and more reliable than GUI tests.

---

# 15.5 Unit Testing

Every mathematical component should receive dedicated unit tests.

Examples include:

Indicator calculations

Trend analysis

Momentum analysis

Signal generation

Decision logic

Risk calculations

Trade planning

Each test should focus on one behaviour only.

---

# 15.6 Integration Testing

Integration tests verify communication between multiple modules.

Examples:

Historical Provider → Analysis Engine

Analysis Engine → Signal Engine

Signal Engine → Decision Engine

Decision Engine → Portfolio Engine

Portfolio Engine → Risk Manager

Risk Manager → Trade Planner

These tests ensure that interfaces remain compatible.

---

# 15.7 End-to-End Testing

Complete Orion workflows should also be tested.

Example:

```text id="test02"
Universe

↓

Market Data

↓

Historical Data

↓

Analysis

↓

Signals

↓

Decision

↓

Trade Plan

↓

GUI
```

The objective is to verify that complete market scans produce valid results.

---

# 15.8 Mathematical Validation

Every technical indicator should be verified against known reference values.

Examples:

RSI

EMA

MACD

ATR

ADX

Bollinger Bands

Moving Averages

Validation should compare Orion's calculations against trusted financial references whenever possible.

---

# 15.9 Regression Testing

Whenever a defect is discovered:

1.

Reproduce the issue.

2.

Write a failing test.

3.

Fix the issue.

4.

Verify that the test passes.

This process prevents previously solved problems from reappearing.

---

# 15.10 Performance Testing

As Orion grows, performance becomes increasingly important.

Performance tests should monitor:

Scan duration

Indicator calculation time

Memory usage

Cache efficiency

Provider latency

Portfolio calculations

Historical loading speed

Performance targets should be reviewed after every major release.

---

# 15.11 Stress Testing

Future versions should evaluate Orion under heavy workloads.

Examples:

10,000 symbols

50,000 symbols

Multiple portfolios

Simultaneous scans

Provider failures

Large historical datasets

Stress testing ensures long-term scalability.

---

# 15.12 Failure Testing

External systems occasionally fail.

The platform should remain operational under adverse conditions.

Examples:

Provider unavailable

Missing candles

Corrupted cache

Invalid symbol

Network timeout

Partial downloads

Unexpected data

The objective is graceful degradation rather than application failure.

---

# 15.13 GUI Testing

Although the GUI contains no business logic, it should still be validated.

Examples:

Window loading

Chart rendering

Navigation

Portfolio display

Theme consistency

Progress indicators

Error dialogs

The GUI should accurately represent deterministic engine outputs.

---

# 15.14 Test Organisation

Recommended directory structure:

```text id="test03"
tests/

    analysis/

    indicators/

    signals/

    decisions/

    portfolio/

    risk/

    planner/

    providers/

    integration/

    regression/

    performance/

    gui/
```

Each subsystem maintains its own dedicated test suite.

---

# 15.15 Continuous Quality

Every sprint should conclude with:

✓ Unit tests

✓ Integration tests

✓ Regression tests

✓ Manual verification

✓ Documentation updates

✓ Git commit

✓ Git push

A sprint is not considered complete until all quality checks have passed.

---

# 15.16 Coding Standards

Quality Assurance extends beyond testing.

General coding standards include:

Readable code

Consistent naming

Single Responsibility Principle

Small functions

Clear documentation

Meaningful commit messages

Predictable module structure

These standards improve long-term maintainability.

---

# 15.17 Metrics

Future versions may monitor development quality through measurable metrics.

Examples:

Code coverage

Average scan time

Cache hit ratio

Bug frequency

Regression count

Average test duration

Module complexity

These metrics help maintain engineering quality as Orion grows.

---

# 15.18 Long-Term Vision

Quality Assurance is not intended to slow development.

Instead, it provides confidence that Project Orion can continue evolving without sacrificing correctness or reliability.

As the project expands to include additional providers, AI capabilities, portfolio optimisation and broker integrations, the testing architecture should evolve alongside it.

The ultimate objective is a trading platform where every calculation is verifiable, every recommendation is reproducible and every release improves the software without compromising its stability.

---

# End of Chapter 15

The next chapter introduces the **Development Roadmap & Release Strategy**, describing the planned evolution of Project Orion from its current development stage to a complete professional trading platform, including release milestones, versioning philosophy and long-term objectives.
# 16. Development Roadmap & Release Strategy

## 16.1 Introduction

Project Orion is not intended to be developed as a collection of isolated features.

Instead, it follows a structured, long-term development roadmap in which every release contributes to a clearly defined vision.

Each development phase builds upon the previous one.

Earlier layers establish the foundation.

Later layers introduce intelligence, automation and user experience.

The roadmap therefore represents the planned evolution of Orion from a market scanner into a complete AI-assisted trading platform.

---

# 16.2 Development Philosophy

Every Orion release follows three simple principles.

### Stability before Features

New functionality should never compromise existing reliability.

---

### Foundation before Automation

Automation should only be introduced after the underlying analytical models have matured.

---

### Explainability before Intelligence

Every automated recommendation must remain understandable.

Artificial Intelligence should improve communication rather than replace deterministic analysis.

---

# 16.3 Current Development Status

Current architectural progress:

```text id="roadmap01"
✓ Universe Layer

✓ Market Data Layer

✓ Historical Data Layer

✓ Technical Scanner

✓ Scanner Pipeline

✓ Historical Cache

✓ Ranking Engine

✓ Basic GUI

⬜ Analysis Engine

⬜ Signal Engine

⬜ Decision Engine 2.0

⬜ Portfolio Engine

⬜ Risk Manager

⬜ Trade Planner

⬜ AI Layer

⬜ Professional GUI
```

The project currently possesses a solid technical foundation upon which higher-level intelligence will be built.

---

# 16.4 Orion Version Strategy

The Orion platform is divided into major development generations.

Each generation introduces a new level of capability rather than simply adding isolated features.

---

# Orion 0.x

Prototype Phase

Objectives:

Validate architecture

Build market data layer

Develop scanner

Implement historical cache

Create deterministic analysis pipeline

Status:

Current Development Phase

---

# Orion 1.0

Professional Swing Trading Platform

Primary Objectives:

Complete Analysis Engine

Complete Signal Engine

Complete Decision Engine

Portfolio Management

Risk Management

Trade Planning

Professional Desktop GUI

Daily scanning

Historical trade database

This version represents Orion's first production-ready release.

---

# Orion 2.0

Portfolio Intelligence

Objectives:

Portfolio optimisation

Adaptive position sizing

Sector allocation

Correlation analysis

Advanced statistics

Portfolio quality scoring

Historical performance analytics

This version transforms Orion into a complete portfolio assistant.

---

# Orion 3.0

Artificial Intelligence

Objectives:

AI explanations

Daily reports

Interactive AI assistant

Educational mode

Portfolio coaching

Trade journaling

Natural language summaries

AI remains entirely grounded in deterministic analysis.

---

# Orion 4.0

Execution Platform

Objectives:

Paper Trading

Broker integration

Order generation

Trade monitoring

Position management

Automatic alerts

Execution workflows

At this stage Orion becomes an end-to-end trading platform.

---

# Orion 5.0

Professional Platform

Potential features:

Cloud synchronisation

Multi-device support

REST API

Plugin system

Custom strategies

Marketplace

Institutional reporting

Advanced dashboards

Machine learning research

---

# 16.5 Sprint Strategy

Development follows iterative sprints.

Each sprint should produce:

A clearly defined objective.

Working software.

Passing tests.

Updated documentation.

Git commit.

GitHub push.

A sprint is considered complete only when all six conditions have been satisfied.

---

# 16.6 Architectural Growth

Every subsystem should mature independently.

Example:

```text id="roadmap02"
Historical Data

↓

Analysis

↓

Signals

↓

Decision

↓

Portfolio

↓

Risk

↓

Trade Planner

↓

AI

↓

GUI
```

Each layer builds upon completed work rather than replacing it.

---

# 16.7 Release Philosophy

Releases should prioritise quality over speed.

Guidelines:

Small releases

Frequent validation

Incremental improvements

Continuous refactoring

Stable architecture

Breaking changes should be avoided whenever possible.

---

# 16.8 Technical Debt

Technical debt should be managed continuously.

Whenever architectural improvements become necessary:

Refactor early.

Avoid temporary solutions.

Maintain modularity.

Update documentation.

Preserve backwards compatibility whenever practical.

Short-term convenience should never outweigh long-term maintainability.

---

# 16.9 Documentation Strategy

Documentation evolves together with the code.

Every completed subsystem should update:

Master Architecture

Project Status

Sprint Documentation

Developer Notes

Future developers should always understand the current architecture by reading the documentation.

---

# 16.10 Versioning

Recommended versioning:

```text id="roadmap03"
Major

Architectural milestones

Minor

New functionality

Patch

Bug fixes
```

Example:

Version 1.2.4

Major:

1

Minor:

2

Patch:

4

This versioning strategy communicates both maturity and compatibility.

---

# 16.11 Success Criteria

Project Orion should ultimately satisfy the following objectives.

Professional architecture

Reliable calculations

Deterministic analysis

Explainable recommendations

Scalable performance

High-quality GUI

Robust testing

Comprehensive documentation

Modular design

Long-term maintainability

---

# 16.12 Long-Term Vision

Project Orion is not intended to become merely another stock screener.

Its long-term ambition is to become a professional decision-support platform that combines deterministic market analysis, disciplined portfolio management and transparent Artificial Intelligence into a single cohesive environment.

Every release should move Orion closer to that objective without sacrificing the architectural principles established in this document.

Success will not be measured solely by the number of implemented features, but by the consistency, reliability and professionalism of the entire platform.

---

# End of Chapter 16

The next chapter defines the **Coding Standards & Engineering Guidelines**, establishing the development principles, naming conventions, documentation requirements and engineering practices that every future contribution to Project Orion must follow. This chapter ensures that the codebase remains clean, maintainable and scalable as the project continues to grow.
# 17. Coding Standards & Engineering Guidelines

## 17.1 Introduction

A professional software architecture requires more than well-designed modules.

It also requires a consistent engineering philosophy.

As Project Orion continues to grow, multiple subsystems, contributors and future AI-assisted development will interact with the same codebase.

Without clear engineering standards, software quality gradually deteriorates.

The purpose of this chapter is to define the engineering principles that every contribution to Project Orion should follow.

These standards are intended to maximise readability, maintainability, scalability and long-term stability.

---

# 17.2 Engineering Philosophy

Project Orion follows one fundamental principle:

> **Code is written once, but read thousands of times.**

Therefore, readability is considered more valuable than writing the shortest possible implementation.

Future maintainability always takes priority over temporary convenience.

---

# 17.3 General Principles

Every contribution should satisfy the following principles.

### Simplicity

Prefer simple solutions over complex ones.

---

### Readability

Code should explain itself whenever possible.

---

### Consistency

Similar problems should be solved in similar ways.

---

### Maintainability

Future developers should understand the code quickly.

---

### Scalability

New functionality should integrate without requiring major refactoring.

---

### Testability

Every important component should be testable independently.

---

# 17.4 Module Design

Each module should answer one question.

Examples:

```text id="code01"
RSI Module

Calculates RSI.

Nothing else.
```

```text id="code02"
Historical Provider

Downloads historical candles.

Nothing else.
```

```text id="code03"
Risk Manager

Calculates portfolio risk.

Nothing else.
```

Modules that perform multiple unrelated responsibilities should be refactored.

---

# 17.5 Class Design

Classes should represent logical concepts.

Examples:

```text id="code04"
HistoricalDataProvider

AnalysisEngine

SignalEngine

DecisionEngine

TradePlanner
```

Avoid "God Classes" that perform dozens of unrelated tasks.

---

# 17.6 Function Design

Functions should:

Perform one task.

Remain short whenever practical.

Have descriptive names.

Avoid hidden side effects.

Return predictable results.

Whenever a function becomes difficult to understand, it should be decomposed into smaller functions.

---

# 17.7 Naming Conventions

Classes

PascalCase

Example:

```text id="code05"
AnalysisEngine

PortfolioManager

TradePlanner
```

Methods

snake_case

Example:

```text id="code06"
calculate_rsi()

generate_trade_plan()

load_universe()
```

Variables

snake_case

Constants

UPPER_CASE

Private members

Leading underscore

Example:

```text id="code07"
_cache

_provider
```

---

# 17.8 Documentation

Every public class should include documentation.

Every complex algorithm should explain:

Purpose

Inputs

Outputs

Important assumptions

Mathematical references (when appropriate)

Documentation should describe **why**, not merely **what**.

---

# 17.9 Comments

Comments should explain intent rather than implementation.

Avoid:

```python
# Increment i
i += 1
```

Prefer:

```python
# Skip incomplete historical datasets to avoid
# invalid technical calculations.
```

Good code reduces the need for comments.

Good comments explain architectural reasoning.

---

# 17.10 Error Handling

Errors should be handled explicitly.

Guidelines:

Never ignore exceptions.

Log meaningful information.

Fail gracefully.

Protect the user experience.

Continue processing whenever possible.

External failures should not terminate the application unnecessarily.

---

# 17.11 Logging

Logging should provide useful operational insight.

Recommended levels:

DEBUG

Development diagnostics

INFO

Normal operations

WARNING

Recoverable problems

ERROR

Failed operations

CRITICAL

Application-threatening failures

Log messages should be descriptive and actionable.

---

# 17.12 Configuration

Configuration values should never be hardcoded.

Examples:

Indicator periods

Risk limits

Portfolio limits

Provider selection

Cache lifetime

Theme settings

These values belong in configuration files.

---

# 17.13 Dependency Management

Modules should depend upon abstractions rather than concrete implementations.

Example:

Good:

```text id="code08"
AnalysisEngine

↓

HistoricalProvider Interface
```

Avoid:

```text id="code09"
AnalysisEngine

↓

Yahoo Finance
```

This principle enables future provider replacement without architectural changes.

---

# 17.14 Testing Expectations

Every important feature should include:

Unit tests

Integration tests

Regression tests (where appropriate)

Manual verification

A feature without tests should not be considered complete.

---

# 17.15 Git Workflow

Every completed sprint should follow the same workflow.

```text id="code10"
Implement

↓

Test

↓

Update Documentation

↓

Git Status

↓

Commit

↓

Push

↓

Verify
```

Meaningful commit messages are required.

Example:

```text id="code11"
Sprint 7.2

Implemented Signal Engine foundation

Added deterministic signal generation

Updated architecture documentation
```

---

# 17.16 Code Reviews

Before major changes become permanent, they should be reviewed against the following checklist.

Architecture respected?

Naming consistent?

Documentation updated?

Tests passing?

Performance acceptable?

Single Responsibility maintained?

No duplicated logic?

Configuration externalised?

If any answer is negative, improvements should be made before merging.

---

# 17.17 Refactoring Philosophy

Refactoring is encouraged.

However:

Behaviour should remain unchanged.

Tests should continue passing.

Documentation should be updated.

Architecture should become clearer.

Refactoring should improve the codebase rather than simply changing it.

---

# 17.18 Performance Philosophy

Performance optimisation should follow three stages.

1.

Correctness

2.

Readability

3.

Performance

Premature optimisation should be avoided.

Measure first.

Optimise second.

---

# 17.19 AI-Assisted Development

Project Orion actively embraces AI-assisted software development.

However, AI-generated code should always satisfy the same engineering standards as manually written code.

Every generated contribution should be:

Reviewed

Tested

Documented

Integrated consistently

AI is treated as a development assistant rather than an autonomous software engineer.

---

# 17.20 Long-Term Engineering Vision

The engineering standards defined in this chapter exist to ensure that Project Orion remains understandable and maintainable as it evolves into a significantly larger software platform.

The objective is not merely to produce working code.

The objective is to produce software that remains reliable, elegant and extensible for many years.

Every future architectural decision should reinforce these engineering principles.

---

# End of Chapter 17

The next and final chapter concludes the Master Architecture Document by describing Orion's long-term future, architectural vision, guiding philosophy and the principles that should continue to shape the project beyond version 1.0.
# 18. Future Vision

## 18.1 Introduction

Project Orion began as an idea:

> *Can market analysis be automated in a way that remains transparent, deterministic and genuinely useful to traders?*

From that initial question grew a software architecture whose purpose extends far beyond building another stock screener.

The long-term ambition of Orion is to become an intelligent decision-support platform that assists traders throughout the complete investment lifecycle.

This final chapter describes that long-term vision.

It is not a list of planned features.

It is the philosophy that should continue guiding every architectural decision as Orion evolves.

---

# 18.2 The Orion Philosophy

Project Orion is built upon one simple belief.

**Technology should improve human decision making, not replace it.**

Financial markets are uncertain.

No software can predict the future with certainty.

Orion therefore does not attempt to become an automated fortune teller.

Instead, it aims to become the most reliable analytical partner possible.

Every recommendation should help a trader make a better-informed decision.

The final decision always remains with the user.

---

# 18.3 Explainable Intelligence

Many modern AI systems operate as black boxes.

Project Orion deliberately follows a different path.

Every recommendation must remain explainable.

Every calculation must be reproducible.

Every conclusion must be traceable.

Artificial Intelligence is introduced only after deterministic analysis has been completed.

This ensures that users can always understand *why* Orion reached a particular conclusion.

Trust is earned through transparency.

---

# 18.4 Professional Software

Project Orion should ultimately resemble professional financial software rather than a personal coding project.

This means:

* Clear architecture
* Consistent engineering
* Comprehensive documentation
* Reliable testing
* Predictable behaviour
* High-quality user experience

The project should remain understandable regardless of its future size.

---

# 18.5 Continuous Evolution

The architecture described in this document is intentionally modular.

Future capabilities may include:

Multi-market support

European equities

Asian markets

Cryptocurrency

Forex

Options

Futures

Economic calendars

Fundamental analysis

Institutional order flow

Machine learning research

Cloud synchronisation

REST APIs

Mobile applications

Collaboration features

Because Orion separates responsibilities into independent layers, these additions can be introduced gradually without redesigning the platform.

---

# 18.6 User Experience

The ultimate Orion experience should feel effortless.

A trader should be able to open the application and immediately understand:

What happened yesterday.

What matters today.

Which opportunities deserve attention.

Why Orion recommends them.

How they should be traded.

What risks are involved.

The software should reduce information overload rather than increase it.

---

# 18.7 Learning Platform

One long-term ambition is for Orion to become an educational platform.

Instead of merely producing recommendations, Orion should gradually help users become better traders.

Examples include:

Explaining technical indicators.

Explaining rejected trades.

Teaching risk management.

Reviewing historical trades.

Identifying behavioural patterns.

Providing personalised educational insights.

Over time, Orion should not only improve investment decisions but also improve the trader.

---

# 18.8 Engineering Vision

The codebase should continue to evolve according to the architectural principles established throughout this document.

Future contributors should prioritise:

Readability.

Maintainability.

Scalability.

Deterministic behaviour.

Comprehensive testing.

Well-documented architecture.

Every architectural decision should strengthen the platform rather than introduce unnecessary complexity.

---

# 18.9 Success Definition

Success for Project Orion is **not** measured solely by profitability.

Instead, success is measured by several characteristics.

Accuracy.

Reliability.

Transparency.

Performance.

Maintainability.

Professional design.

User trust.

If Orion consistently helps traders make more informed and disciplined decisions, it has achieved its primary objective.

---

# 18.10 The Future of Orion

The architecture presented in this document represents the foundation—not the final destination.

Technology will continue to evolve.

Financial markets will continue to evolve.

Artificial Intelligence will continue to evolve.

Project Orion is intentionally designed to evolve alongside them.

Future versions may introduce new technologies, additional analytical techniques and entirely new capabilities.

However, the architectural principles established within this document should remain stable.

They provide the foundation upon which every future release should be built.

---

# 18.11 Final Statement

Project Orion is more than a software application.

It is a long-term engineering project built upon the principles of transparency, determinism and professional software design.

Its purpose is not to replace traders, but to provide them with the information, structure and confidence required to make better investment decisions.

Every line of code, every architectural decision and every future feature should contribute to that objective.

As Orion grows, this document should continue to serve as its architectural compass.

Whenever uncertainty arises, developers should return to these principles before making implementation decisions.

The architecture may evolve.

The technology may change.

The markets will certainly change.

But Orion's commitment to clarity, quality and explainable decision support should remain constant.

---

# Document Status

**Document Name:** ORION_MASTER_ARCHITECTURE.md

**Version:** 1.0 Draft

**Status:** Living Architecture Document

**Last Updated:** Continuously maintained throughout development.

This document should be reviewed and updated whenever major architectural changes are introduced.

---

# End of Master Architecture Document

*"Good architecture is not built for today. It is built so that tomorrow's ideas have a place to live."*

**— Project Orion**


# Dependency Injection and Composition Root

## Dependency Injection and Composition Root

Project Orion uses an explicit dependency-injection foundation located in `core/container`.

The purpose of this layer is to centralize application-level object construction while avoiding hidden runtime magic. Orion intentionally uses a small custom `ApplicationContainer` and `ServiceRegistry` instead of reflection, decorators or an external IoC framework.

Current responsibilities:

* register application services explicitly;
* resolve scan-level infrastructure deterministically;
* support singleton and transient lifetimes;
* support controlled replacement for tests and future provider swaps;
* preserve a clear composition root as Orion grows toward v1.0.

The container must not contain trading logic. Business logic remains in services and analyzers.
