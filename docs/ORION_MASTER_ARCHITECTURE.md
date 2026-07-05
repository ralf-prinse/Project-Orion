# ORION MASTER ARCHITECTURE

---

# Project Orion

## Documentation Information

Documentation Version

v1.11

Architecture Version

v2.0

Status

🟢 Active Development

Current Sprint

🚧 Sprint 5.5 — Trade Lifecycle

Last Updated

2026-07-05

---

# Purpose

This document is the single architectural source of truth for Project Orion.

Every architectural decision, system boundary, rendering pipeline, backend orchestration, workspace composition and design principle is defined here.

No other documentation file may duplicate architectural specifications.

Other documentation may reference this document but must never redefine architecture.

---

# Vision

Project Orion is a deterministic AI-assisted desktop trading workstation for short-term trading of highly liquid equities.

Its objective is not to predict markets.

Its objective is to continuously discover deterministic trading opportunities, analyse individual symbols, size positions, monitor active trades and explain every recommendation through transparent reasoning.

Artificial Intelligence never generates trading decisions.

Artificial Intelligence only explains deterministic output produced by backend services.

Mission Control is the operational center of Orion.

Trade Monitor / Trade Lifecycle is the next major functional area.

---

# Core Philosophy

Project Orion is built around six non-negotiable principles.

---

## 1. Deterministic First

Every BUY, HOLD, SELL or EXIT recommendation originates exclusively from deterministic backend services.

Signals must always be:

- deterministic
- reproducible
- explainable
- testable
- traceable

Random behaviour is forbidden.

---

## 2. AI Explainability

Artificial Intelligence may:

- explain
- summarize
- compare
- translate deterministic output into natural language

Artificial Intelligence may never:

- generate BUY signals
- generate SELL signals
- generate EXIT signals
- calculate indicators
- calculate confidence
- calculate risk
- calculate position size
- override deterministic output

AI always operates after deterministic backend services have completed.

---

## 3. Separation of Responsibilities

Every architectural layer owns exactly one responsibility.

```text
Providers
    ↓
Deterministic Services
    ↓
Controllers
    ↓
Presenters
    ↓
Presentation Models
    ↓
Workspaces
    ↓
Widgets / Panels / Charts
```

Responsibilities never overlap.

Business logic never enters the UI.

Rendering never enters backend services.

Controllers orchestrate only.

Presenters format only.

Workspaces render only.

---

## 4. Architecture Before Features

Architecture always has priority over implementation speed.

Reusable components are preferred over feature-specific implementations.

Duplicate implementations are forbidden.

Every new feature must fit into the existing architecture before implementation begins.

---

## 5. Mission Control

Mission Control is the primary workspace of Orion.

Its objective is operational awareness.

Within seconds the user must understand:

- current market state
- strongest opportunities
- available trading capital
- recommended position size
- active risks
- required actions

Mission Control is designed as a professional trading workstation rather than a traditional dashboard.

---

## 6. Visible Progress

Every development sprint must end with:

- deterministic backend validation
- successful automated tests
- successful desktop launch
- manual GUI validation
- documentation synchronization
- Git commit
- GitHub push

Every sprint should produce a visible improvement inside the desktop application.

Architecture remains stable while functionality grows incrementally.

---

# High-Level System Overview

```text
                    Market Data Providers
                            │
                            ▼
                      Quote / History Data
                            │
                            ▼
                    Technical Analysis Layer
                            │
          ┌─────────────────┴─────────────────┐
          ▼                                   ▼
   Trading Decision Flow              Exit Decision Flow
          │                                   │
          ▼                                   ▼
    TradingPipeline                  ExitEvaluationService
          │                                   │
          ▼                                   ▼
 BUY / HOLD / SELL                 HOLD / EXIT Advice
          │                                   │
          ▼                                   ▼
  Trading Workspace               Trade Monitor / Position Monitor
          │                                   │
          └─────────────────┬─────────────────┘
                            ▼
                    AI Explainability Layer
                            │
                            ▼
                    Desktop Presentation
```

---

# System Objectives

Project Orion continuously answers six questions.

1. What is happening in the market right now?

2. Which symbols deserve immediate attention?

3. Should a new position be opened?

4. How large should the position be?

5. Is an open trade still healthy?

6. Should an existing trade be closed?

Every subsystem ultimately supports one or more of these objectives.

---

# Current Development Direction

The architectural foundation is considered stable.

Current development focuses on the Trade Lifecycle.

Current priorities are:

- Mission Control
- Trading Workspace
- Portfolio-aware position sizing
- Trade Monitor
- Exit Intelligence
- Open Trade persistence
- Trade History
- Paper Trading

The deterministic backend remains the single source of truth.

TradingPipeline remains the only source of BUY / HOLD / SELL decisions.

ExitEvaluationService is the deterministic source of open-trade exit advice.

AI remains explainability-only.

---

# Architecture Layers

Project Orion consists of five major architectural layers.

---

## 1. Providers

Providers own external data access.

Providers may:

- retrieve market data
- retrieve historical candle data
- validate symbols
- normalize provider responses
- expose provider-specific errors

Providers may never:

- create trading decisions
- calculate final signals
- format UI output
- render widgets
- call AI

Examples:

- YahooProvider
- YahooHistoricalDataProvider

---

## 2. Deterministic Services

Deterministic services own business logic.

They may:

- calculate indicators
- analyse technical conditions
- scan markets
- evaluate opportunities
- calculate position size
- evaluate open trades
- calculate exit score
- produce deterministic decision data

They may never:

- render UI
- own Qt widgets
- produce natural-language AI output
- execute broker orders unless explicitly designed as broker services

Examples:

- TradingPipeline
- AnalysisEngine
- RiskEngine
- PositionSizingEngine
- LiveScannerService
- OpportunityService
- PositionSizingService
- PositionAnalysisService
- PositionMonitorService
- ExitEvaluationService

---

## 3. Controllers

Controllers orchestrate user actions.

They may:

- receive user input from workspaces
- call services
- call presenters
- update workspaces with view models
- handle service errors

They may never:

- calculate indicators
- create BUY / HOLD / SELL decisions
- create exit decisions
- format presentation text
- render widgets

Examples:

- TradingController
- MissionControlController
- PositionMonitorController

---

## 4. Presentation

Presentation components transform deterministic data into readable UI models.

They may:

- format labels
- format values
- create summaries
- create panel text
- produce ViewModels
- prepare GuiWorkspace models

They may never:

- calculate indicators
- create trading decisions
- create exit decisions
- fetch market data
- call providers
- render widgets

Examples:

- TradingWorkspacePresenter
- MissionControlPresenter
- PositionMonitorPresenter
- HistoryPresenter
- SettingsPresenter

---

## 5. Rendering

Rendering components own desktop display.

They may:

- render workspaces
- render panels
- render widgets
- render charts
- handle layout
- forward user actions

They may never:

- calculate business logic
- call market providers
- create deterministic decisions
- call AI
- calculate technical indicators

Examples:

- BaseWorkspace
- MissionControlWorkspace
- TradingWorkspace
- PositionMonitorWorkspace
- PortfolioWorkspace
- WorkspacePanel
- WorkspaceRenderer
- ChartCanvas

---

# Backend Architecture

The backend is the deterministic core of Orion.

Every trading decision originates exclusively from deterministic backend services.

The backend owns:

- market data acquisition
- historical data acquisition
- indicator calculations
- technical analysis
- market scanning
- opportunity discovery
- position sizing
- trade monitoring
- exit evaluation
- risk management
- persistence
- AI context generation

The backend never owns:

- desktop rendering
- widgets
- layouts
- styling
- presentation formatting

---

# Deterministic Decision Architecture

Project Orion now contains two deterministic decision flows.

They are separate by design.

---

## 1. Entry Decision Flow

The entry decision flow determines whether a new position should be opened.

```text
Symbol / Market Data
        ↓
YahooProvider
        ↓
IndicatorBuilder
        ↓
TradingPipeline
        ↓
BUY / HOLD / SELL
        ↓
TradingWorkspacePresenter
        ↓
Trading Workspace
```

TradingPipeline is the only source of BUY / HOLD / SELL decisions.

No UI component may determine:

- BUY
- HOLD
- SELL
- confidence
- position size
- risk

No AI component may determine:

- BUY
- HOLD
- SELL

---

## 2. Exit Decision Flow

The exit decision flow determines whether an existing trade should be held or exited.

```text
Trade
        ↓
PositionAnalysisService
        ↓
YahooProvider
        ↓
AnalysisEngine
        ↓
AnalysisResult
        ↓
PositionMonitorService
        ↓
ExitEvaluationService
        ↓
HOLD / EXIT Advice
        ↓
PositionMonitorPresenter
        ↓
Position Monitor Workspace
```

ExitEvaluationService is the deterministic source of open-trade exit advice.

No UI component may determine:

- HOLD_POSITION
- TAKE_PROFIT
- STOP_LOSS
- TRAILING_STOP
- EXIT_DUE_TO_WEAKNESS
- EXIT_DUE_TO_TIME_LIMIT
- exit score
- exit reasons

No AI component may determine exit advice.

---

# Shared Technical Analysis

The AnalysisEngine is shared infrastructure.

It may be used by:

- TechnicalScanner
- PositionAnalysisService
- future Trade Monitor services
- future Paper Trading analysis services

The AnalysisEngine produces AnalysisResult.

AnalysisResult may contain:

- trend_score
- momentum_score
- volatility_score
- structure_score
- volume_score
- market_regime_score
- relative_strength_score
- candlestick_score
- overall_score
- notes

AnalysisEngine does not create BUY / SELL decisions.

AnalysisEngine provides deterministic technical scoring.

TradingPipeline and ExitEvaluationService interpret technical analysis differently.

This prevents duplicate indicator logic.

---

# Service Architecture

Every backend service owns one clearly defined responsibility.

Services communicate through domain models rather than UI objects.

---

## Market Data Layer

### YahooProvider

Responsibilities

- Retrieve historical price data.
- Retrieve current market prices.
- Normalize provider responses.
- Handle provider-specific errors.

Never responsible for

- Trading decisions
- Exit decisions
- Indicator calculations
- Presentation

---

## Analysis Layer

### AnalysisEngine

Responsibilities

- Calculate deterministic technical analysis.
- Produce AnalysisResult.
- Calculate technical scores.
- Aggregate indicator output.

Never responsible for

- BUY / SELL decisions
- EXIT decisions
- Presentation
- AI output

---

### IndicatorBuilder

Responsibilities

- Build reusable indicator packs.
- Calculate deterministic indicators.
- Supply TradingPipeline.

Never responsible for

- Trading decisions
- Exit decisions

---

## Trading Layer

### TradingPipeline

Responsibilities

- Interpret deterministic technical analysis.
- Generate BUY / HOLD / SELL.
- Calculate confidence.
- Calculate risk.
- Calculate recommended position size.

TradingPipeline is the only source of BUY / HOLD / SELL decisions.

---

### OpportunityService

Responsibilities

- Assemble Mission Control opportunities.
- Merge deterministic analysis.
- Prepare presentation-ready opportunity objects.

OpportunityService never creates trading decisions.

---

### PositionSizingService

Responsibilities

- Calculate recommended position size.
- Validate available trading capital.
- Calculate required investment.

PositionSizingService never determines BUY or SELL.

---

## Trade Lifecycle Layer

### Trade

Trade is the central domain model of Orion.

Trade represents an open or closed position.

A Trade may contain

- symbol
- quantity
- entry price
- entry date
- stop-loss
- take-profit
- trailing stop
- highest price
- lowest price
- current price
- realized profit
- unrealized profit
- status
- notes

Trade contains data only.

Trade never performs business logic.

---

### PositionAnalysisService

Responsibilities

- Retrieve historical market data.
- Execute AnalysisEngine.
- Produce AnalysisResult for existing trades.

PositionAnalysisService performs no trading decisions.

---

### PositionMonitorService

Responsibilities

- Combine Trade information.
- Combine AnalysisResult.
- Delegate exit evaluation.
- Produce PositionMonitorResult.

PositionMonitorService does not decide exits itself.

---

### ExitEvaluationService

Responsibilities

- Evaluate open trades.
- Calculate Exit Score.
- Generate deterministic exit advice.
- Generate deterministic exit reasons.
- Evaluate trade health.

Supported decisions

- HOLD_POSITION
- TAKE_PROFIT
- STOP_LOSS
- EXIT_DUE_TO_WEAKNESS

Future support

- TRAILING_STOP
- EXIT_DUE_TO_TIME_LIMIT

ExitEvaluationService is the only source of deterministic exit decisions.

---

# Controller Architecture

Controllers orchestrate.

Controllers never calculate.

Current controllers

- MissionControlController
- TradingController
- PositionMonitorController

Typical controller flow

```text
Workspace

↓

Controller

↓

Deterministic Services

↓

Presenter

↓

Workspace
```

Controllers own

- orchestration
- error handling
- workflow coordination

Controllers never own

- calculations
- AI
- rendering
- indicator logic

---

# Presenter Architecture

Presenters convert deterministic output into presentation models.

Presenters own

- labels
- summaries
- formatting
- readable explanations
- UI models

Presenters never own

- calculations
- trading logic
- exit logic
- provider access

Current presenters

- MissionControlPresenter
- TradingWorkspacePresenter
- PositionMonitorPresenter

---

# Workspace Architecture

Workspaces own interaction.

They never own business logic.

Current workspaces

- Mission Control
- Trading Workspace
- Portfolio
- Position Monitor

Future workspaces

- Trade History
- Paper Trading
- Strategy Lab

Every workspace follows the same pattern.

```text
User

↓

Workspace

↓

Controller

↓

Services

↓

Presenter

↓

Workspace
```

This keeps all desktop behaviour predictable, testable and reusable.

---

# Trade Lifecycle Architecture

The Trade Lifecycle is Orion's newest architectural domain.

Its purpose is to manage the complete lifecycle of a trade while preserving deterministic behaviour.

Current lifecycle

```text
Opportunity

↓

Trading Analysis

↓

BUY Decision

↓

Position Sizing

↓

Trade Created

↓

Trade Monitoring

↓

Exit Intelligence

↓

Trade Closed

↓

Trade History
```

Only the first seven stages are currently implemented.

Trade persistence and Trade History will follow in later sprints.

---

# Trade Lifecycle Responsibilities

Each stage owns one responsibility.

| Stage | Responsibility |
|--------|----------------|
| Opportunity | Discover deterministic opportunities |
| Trading | Determine BUY / HOLD / SELL |
| Position Sizing | Determine recommended position size |
| Trade | Store lifecycle state |
| Position Monitor | Monitor current trade |
| Exit Evaluation | Determine deterministic exit advice |
| Trade History | Preserve completed trades |

Responsibilities never overlap.

---

# Mission Control Architecture

Mission Control is the operational heart of Orion.

Mission Control never performs calculations.

Mission Control presents deterministic information produced by backend services.

Mission Control currently presents

- Market Status
- Scanner Status
- Scan Duration
- Market Data
- Universe Coverage
- Top Opportunities
- Current Market Price
- Position Size
- Required Investment
- Remaining Capital
- Budget Status

Future versions will additionally present

- Open Trades
- Portfolio Exposure
- Trade Health
- Active Risk
- Daily Performance

Mission Control remains the first workspace users interact with.

---

# Trading Workspace Architecture

Trading Workspace evaluates a single symbol.

Flow

```text
User Symbol

↓

TradingController

↓

YahooProvider

↓

IndicatorBuilder

↓

TradingPipeline

↓

TradingWorkspacePresenter

↓

Trading Workspace
```

Trading Workspace owns

- BUY / HOLD / SELL presentation
- Confidence presentation
- Pressure presentation
- Risk presentation
- Position Size presentation
- AI explanation

Trading Workspace never owns

- indicator calculations
- provider logic
- AI decision making

---

# Position Monitor Architecture

Position Monitor is the first implementation of the Trade Lifecycle.

Flow

```text
Trade

↓

PositionMonitorController

↓

PositionAnalysisService

↓

AnalysisEngine

↓

PositionMonitorService

↓

ExitEvaluationService

↓

PositionMonitorPresenter

↓

Position Monitor Workspace
```

Position Monitor owns

- Trade monitoring
- Exit Intelligence presentation
- Profit/Loss presentation
- Trade Health presentation

Position Monitor never owns

- exit calculations
- technical analysis
- market data retrieval

Current implementation supports manual trade entry.

Future versions will load persisted trades automatically.

---

# Artificial Intelligence Architecture

Artificial Intelligence exists only after deterministic processing has completed.

AI consumes deterministic output.

AI produces natural-language explanations.

AI may

- explain trades
- explain opportunities
- summarize technical analysis
- explain risk
- explain exit advice

AI may never

- create BUY signals
- create SELL signals
- create EXIT signals
- calculate indicators
- calculate confidence
- calculate risk
- calculate position size
- override deterministic output

Deterministic services always remain authoritative.

---

# Dependency Rules

The following dependency rules are mandatory.

Providers

↓

Services

↓

Controllers

↓

Presenters

↓

Workspaces

↓

Widgets

↓

Qt

Higher layers may never depend on lower presentation layers.

Widgets may never call services directly.

Presenters may never call providers.

Controllers may never perform calculations.

Services may never render UI.

These rules are mandatory for every future sprint.

---

# Future Architecture

The current architecture is intentionally designed to support future expansion without requiring structural redesign.

The planned evolution of Orion is:

```text
Market Intelligence

↓

Mission Control

↓

Trading Workspace

↓

Position Sizing

↓

Trade Lifecycle

↓

Trade History

↓

Paper Trading

↓

Broker Integration
```

Every new capability must fit within the existing architectural layers.

No shortcut implementations are allowed.

---

# Current Implementation Status

## Completed

### Deterministic Backend

- TradingPipeline
- AnalysisEngine
- TechnicalScanner
- MarketScanner
- RiskEngine
- IndicatorBuilder
- OpportunityService
- PositionSizingService
- PositionAnalysisService
- PositionMonitorService
- ExitEvaluationService

### Desktop

- Workspace architecture
- Presenter architecture
- Mission Control
- Trading Workspace
- Portfolio
- Position Monitor
- Chart framework
- Scrollable workspaces

### Trade Lifecycle

Implemented

- Trade domain model
- Manual trade creation
- Trade monitoring
- Exit Intelligence
- Shared AnalysisEngine
- Exit Score
- Exit Reasons
- Trend Status
- Momentum Status
- Risk Status

---

# Planned Implementation

## Sprint 5.5

Trade Lifecycle

- Improve Trade Monitor
- Improve lifecycle presentation
- Connect Trading Workspace to Trade creation
- Prepare Open Trade persistence
- Prepare Trade History

---

## Sprint 6.0

Paper Trading

- Virtual Broker
- Order execution simulation
- Portfolio tracking
- Statistics
- Performance reporting

---

## Future

Broker Integration

Possible future integrations

- Interactive Brokers
- Alpaca
- Trading212
- Degiro (if APIs become available)

Broker integrations will never replace deterministic decision making.

They only execute deterministic decisions.

---

# Architectural Rules

Every future implementation must satisfy the following requirements.

✔ One responsibility per class

✔ One responsibility per service

✔ Controllers orchestrate only

✔ Presenters format only

✔ Workspaces render only

✔ Services calculate only

✔ Providers retrieve data only

✔ TradingPipeline remains the only BUY / HOLD / SELL decision engine

✔ ExitEvaluationService remains the only deterministic EXIT decision engine

✔ AnalysisEngine remains the shared technical analysis engine

✔ AI remains explainability only

✔ No duplicated indicator calculations

✔ No duplicated business logic

✔ No business logic inside Qt widgets

✔ No direct provider access from UI

✔ No rendering inside backend services

---

# Development Workflow

Every development sprint follows the same lifecycle.

Architecture

↓

Implementation

↓

Regression Tests

↓

Desktop Launch

↓

Manual GUI Validation

↓

Documentation Synchronization

↓

Git Commit

↓

GitHub Push

Only after documentation has been synchronized is a sprint considered complete.

---

# Source of Truth

Project Orion has one primary source of truth.

1. GitHub repository
2. ORION_MASTER_ARCHITECTURE.md
3. AI_CONTEXT.md
4. PROJECT_STATUS.md
5. TODO.md
6. CHANGELOG.md

The GitHub repository always reflects the latest implementation.

Documentation must always be synchronized with the repository before a new development sprint begins.

---

# End of ORION_MASTER_ARCHITECTURE