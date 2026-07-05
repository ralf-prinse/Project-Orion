# ORION MASTER ARCHITECTURE

---

# Project Orion

## Documentation Information

Documentation Version

v1.10

Architecture Version

v1.9

Status

🟢 Active Development

Current Sprint

🚧 Sprint 5.1 — Portfolio & Position Sizing Foundation
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

Its objective is to continuously discover deterministic trading opportunities, monitor active positions and explain every recommendation through transparent reasoning.

Artificial Intelligence never generates trading decisions.

Artificial Intelligence only explains deterministic output produced by backend services.

Mission Control is the operational center of Orion.

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

AI always operates after the TradingPipeline has completed.

---

## 3. Separation of Responsibilities

Every architectural layer owns exactly one responsibility.

```
Business Services
        │
        ▼
Presenters
        │
        ▼
Presentation Models
        │
        ▼
Workspace Renderer
        │
        ▼
Widgets
        │
        ▼
ChartCanvasBuilder
        │
        ▼
ChartCanvas
        │
        ▼
Chart Layers
        │
        ▼
Qt Painter
```

Responsibilities never overlap.

Business logic never enters the UI.

Rendering never enters backend services.

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
- portfolio health
- active risks
- required actions

Mission Control is designed as a professional trading workstation rather than a traditional dashboard.

---

## 6. Visible Progress

Every development sprint must end with:

- deterministic backend validation
- successful automated tests
- manual GUI validation
- documentation synchronization

Every sprint should produce a visible improvement inside the desktop application.

Architecture remains stable while functionality grows incrementally.

---

# High-Level System Overview

```
                 Market Data Providers
                         │
                         ▼
                   Quote Services
                         │
                         ▼
                 Technical Scanner
                         │
                         ▼
                  Analysis Engine
                         │
                         ▼
                  Market Scanner
                         │
                         ▼
                  Trading Pipeline
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
     Position Monitor        AI Context Builder
             │                       │
             ▼                       ▼
       Exit Signals          AI Explanation
             │
             ▼
      Presentation Models
             │
             ▼
      Mission Control UI
```

---

# System Objectives

Project Orion continuously answers four questions.

1. What is happening in the market right now?

2. Which symbols deserve immediate attention?

3. Should a new position be opened?

4. Should an existing position be closed?

Every subsystem ultimately supports one or more of these objectives.

---

# Current Development Direction

The architectural foundation is considered stable.

Current development focuses on expanding functionality rather than restructuring architecture.

Current priorities are:

- Mission Control
- Portfolio-aware trading
- Position Sizing
- Live Opportunities
- Position Monitoring
- Trading Workspace
- Paper Trading

The deterministic backend remains the single source of truth.

---

# Architecture Layers

Project Orion consists of four major architectural layers.

## Backend

Owns:

- market data
- indicators
- technical analysis
- opportunity discovery
- trading decisions
- position sizing
- risk management
- position monitoring

Never owns:

- rendering
- widgets
- presentation
- styling

---

## Presentation

Owns:

- formatting
- presentation models
- workspace composition
- metadata
- labels
- summaries

Never owns:

- calculations
- providers
- AI
- trading logic

---

## Rendering

Owns:

- widget composition
- layouts
- panel rendering
- chart rendering
- interaction

Never owns:

- calculations
- backend services
- AI
- providers

---

## Artificial Intelligence

Owns:

- explanations
- summaries
- natural language
- reasoning

Never owns:

- BUY decisions
- SELL decisions
- EXIT decisions
- confidence calculations
- risk calculations

Artificial Intelligence always consumes deterministic backend output.

# Backend Architecture

The backend is the deterministic core of Orion.

Every trading decision originates exclusively from backend services.

The backend owns:

- market data acquisition
- indicator calculations
- technical analysis
- market scanning
- opportunity discovery
- OpportunityService
- trading decisions
- PortfolioStore
- risk management
- PositionSizingService
- position monitoring
- AI context generation

The backend never owns:

- desktop rendering
- widgets
- layouts
- styling
- presentation formatting

---

# Deterministic Backend Pipeline

The deterministic execution pipeline is:

```
Market Data Provider
        │
        ▼
Quote Service
        │
        ▼
Technical Scanner
        │
        ▼
Analysis Engine
        │
        ▼
Market Scanner
        │
        ▼
Trading Pipeline
        │
        ▼
Signal Output
        │
        ├──────────────┐
        ▼              ▼
Position Monitor   AI Context Builder
        │              │
        ▼              ▼
Exit Signals    AI Explanation Engine
```

Every stage performs exactly one deterministic responsibility.

No stage may perform work belonging to another layer.

---

# Trading Pipeline

TradingPipeline remains the single source of truth.

No UI component may determine:

- BUY
- HOLD
- SELL
- EXIT
- confidence
- position size
- risk

No AI component may determine:

- BUY
- HOLD
- SELL
- EXIT

TradingPipeline combines deterministic output from:

Presentation-ready opportunities are assembled afterwards by OpportunityService.

OpportunityService never creates trading decisions.

It combines deterministic output for Mission Control presentation only.

- Technical Scanner
- Analysis Engine
- Market Scanner
- Risk Engine
- PositionSizing Engine

Only after TradingPipeline has finished may AI receive context.

---

## Trading Controller

Sprint 4.9 introduces the TradingController.

Responsibilities:

- request historical market data
- build IndicatorPack
- execute TradingPipeline
- invoke TradingWorkspacePresenter
- update Trading Workspace

TradingController never:

- calculates indicators
- creates trading signals
- formats presentation
- performs rendering

Flow:

```
Trading Workspace

        │
        ▼

TradingController

        │
        ▼

YahooProvider

        │
        ▼

IndicatorBuilder

        │
        ▼

TradingPipeline

        │
        ▼

TradingWorkspacePresenter

        │
        ▼

Trading Workspace
```

---

# LiveScannerService

LiveScannerService is responsible for orchestrating continuous market scanning.

It coordinates existing backend services.

It never performs trading calculations itself.

---

## Responsibilities

LiveScannerService owns:

- scanner lifecycle
- orchestration
- refresh scheduling
- provider coordination
- immutable snapshots
- scanner health
- scan duration
- error isolation

It never owns:

- indicator calculations
- BUY decisions
- SELL decisions
- rendering
- broker execution

---

# Live Scanner Flow

```
Universe

      │
      ▼

Quote Service

      │
      ▼

Technical Scanner

      │
      ▼

Analysis Engine

      │
      ▼

Market Scanner

      │
      ▼

LiveScannerSnapshot

      │
      ▼

MissionControlPresenter

      │
      ▼

Mission Control
```

---

# LiveScannerSnapshot

Every completed scan produces one immutable snapshot.

Current snapshot contains:

- timestamp
- symbols
- quotes
- technical results
- errors
- scan duration

Future versions may additionally contain:

- provider status
- scanner health
- BUY count
- HOLD count
- SELL count
- market breadth
- universe coverage

Presentation always consumes snapshots.

The UI never consumes backend services directly.

---

# Live Refresh

Mission Control refreshes automatically.

Current implementation:

```
QTimer

      │
      ▼

MissionControlController.refresh()

      │
      ▼

LiveScannerService.scan_once()

      │
      ▼

MissionControlPresenter

      │
      ▼

Mission Control
```

Refresh timing remains configurable.

Future streaming providers may replace polling without changing architecture.

---

# Live Opportunities

Sprint 4.9 introduces Live Opportunities.

Objective:

Automatically present the strongest deterministic trading candidates inside Mission Control.

Conceptual flow:

```
LiveScannerSnapshot

        │
        ▼

Top Ranked Symbols

        │
        ▼

TradingPipeline

        │
        ▼

OpportunityService

        │
        ▼

Opportunity

        │
        ▼

Mission Control
```
Opportunity currently contains

- symbol
- current market price
- signal
- technical score
- trend
- scanner reason

Future versions will additionally contain

- recommended share quantity
- required investment
- remaining capital
- stop loss
- target
- confidence


TradingPipeline remains the only decision engine.

Mission Control never calculates opportunities.

---

# Position Monitor

After a position has been opened Orion continuously evaluates it.

Input:

- symbol
- quantity
- entry price
- current price
- stop-loss
- target
- elapsed time

Output:

- HOLD_POSITION
- TAKE_PROFIT
- STOP_LOSS
- TRAILING_STOP
- EXIT_DUE_TO_WEAKNESS
- EXIT_DUE_TO_TIME_LIMIT

Position monitoring remains fully deterministic.

Artificial Intelligence explains exit signals only.

---

# Broker Strategy

Phase 1

Manual execution.

Orion proposes.

Trader executes.

---

Phase 2

Paper Trading.

---

Phase 3

Broker abstraction.

---

Phase 4

Optional live execution.

Live execution is only allowed after:

- deterministic validation
- extensive backtesting
- successful paper trading
- enforced risk controls

# Mission Control Architecture

Mission Control is the operational center of Orion.

It replaces the former Dashboard as the primary workspace.

Mission Control does not exist to display charts.

Mission Control exists to provide immediate deterministic market awareness.

Within seconds the user must understand:

- overall market condition
- strongest opportunities
- scanner status
- active positions
- current risks
- required actions

Mission Control is always the first workspace shown after application startup.

---

# Mission Control Philosophy

Mission Control is built entirely from reusable presentation panels.

Every panel receives immutable presentation models.

Panels never:

- calculate
- access providers
- execute scanners
- perform trading decisions
- generate AI output

Panels render deterministic presentation data only.
Mission Control receives immutable Opportunity objects.

Mission Control never performs position sizing calculations.

Mission Control never calculates portfolio information.

All deterministic calculations remain inside backend services.

---

# Current Workspace Composition

Mission Control currently consists of:

```
Mission Control

├── Scanner Status
├── Scan Duration
├── Market Status
├── Top Opportunities
└── Chart Area (future expansion)
```

Future panels include:

```
Mission Control

├── Scanner Status
├── Scan Duration
├── Market Status
├── Top Opportunities
├── Universe Coverage
├── Open Positions
├── Portfolio Overview
├── Alerts
├── News & Macro
├── Market Breadth
├── Watchlist
└── Selected Instrument
```

Panels may be added without modifying the rendering architecture.

---

# MissionControlController

MissionControlController coordinates the Mission Control workspace.

Responsibilities:

- initialize workspace
- request scanner refresh
- receive LiveScannerSnapshot
- invoke MissionControlPresenter
- update MissionControlWorkspace
- request OpportunityService
- obtain Portfolio trading capital
- coordinate PositionSizingService

MissionControlController never:

- performs calculations
- scans markets
- renders widgets
- generates AI output

Flow:

```
MissionControlController

        │
        ▼

LiveScannerService

        │
        ▼

MissionControlPresenter

        │
        ▼

MissionControlWorkspace
```

---

# MissionControlWorkspace

MissionControlWorkspace is the primary desktop workspace.

Responsibilities:

- own Mission Control layout
- expose Scan Market button
- host DashboardGrid
- host ChartContainer
- receive immutable GuiWorkspace models

MissionControlWorkspace never:

- performs calculations
- formats backend values
- creates signals
- accesses providers

---

# GuiWorkspace

GuiWorkspace is the canonical presentation contract.

Every workspace inside Orion is rendered from GuiWorkspace.

Current structure:

```
GuiWorkspace

├── cards
├── panels
├── charts
├── sections
├── metadata
└── status
```

GuiWorkspace remains immutable.

Backend services never create widgets directly.

---

# GuiWorkspacePanel

GuiWorkspacePanel is the generic presentation model for reusable Mission Control panels.

Every panel contains:

- panel_type
- title
- subtitle
- status
- items
- metadata

Panels remain presentation-only.

No backend objects are stored inside GuiWorkspacePanel.

---

# Workspace Presenters

Workspace Presenters transform deterministic backend output into immutable presentation models.

Responsibilities:

- formatting
- summaries
- labels
- metadata
- workspace composition

Workspace Presenters never:

- calculate indicators
- calculate confidence
- calculate risk
- create BUY signals
- create SELL signals

---

# MissionControlPresenter

MissionControlPresenter transforms immutable Opportunity objects and scanner snapshots into GuiWorkspace.

Current panels:

- Scanner Status
- Scan Duration
- Market Status
- Top Opportunities

Future panels:

- Universe Coverage
- Open Positions
- Portfolio Health
- Alerts
- Market Breadth
- Performance Summary

MissionControlPresenter contains presentation formatting only.

---

# Portfolio Architecture

Portfolio is no longer an analytics dashboard.

Portfolio is responsible for configuring the available trading capital.

Current flow

Portfolio Workspace

        │
        ▼

PortfolioStore

        │
        ▼

MissionControlController

        │
        ▼

OpportunityService

        │
        ▼

PositionSizingService

Mission Control

Portfolio never performs calculations.

Portfolio only manages deterministic configuration values.

---

# TradingWorkspacePresenter

TradingWorkspacePresenter transforms TradingPipeline output into TradingWorkspaceViewModel.

Responsibilities:

- formatting
- labels
- presentation metadata
- AI explanation formatting

TradingWorkspacePresenter never:

- executes TradingPipeline
- performs calculations
- generates AI output

---

# WorkspaceRenderer

WorkspaceRenderer is the only component responsible for translating presentation models into desktop widgets.

Responsibilities:

- render GuiWorkspace
- render cards
- render panels
- render charts
- compose layouts

WorkspaceRenderer never:

- performs calculations
- formats backend values
- accesses providers
- performs trading logic

---

# DashboardGrid

DashboardGrid owns the visual arrangement of reusable panels.

Responsibilities:

- panel placement
- layout management
- responsive resizing

DashboardGrid never:

- formats data
- performs calculations
- renders charts

---

# Chart Architecture

ChartCanvas remains the only rendering engine inside Orion.

Every chart follows:

```
GuiChart

      │
      ▼

ChartRenderer

      │
      ▼

ChartWidgetFactory

      │
      ▼

ChartCanvasBuilder

      │
      ▼

ChartCanvas

      │
      ▼

Chart Layers

      │
      ▼

Qt Painter
```

No alternative rendering implementation is allowed.

---

# Current Desktop Flow

Current desktop execution flow:

```
Backend Services

        │
        ▼

Workspace Presenter

        │
        ▼

GuiWorkspace

        │
        ▼

WorkspaceRenderer

        │
        ▼

DashboardGrid

        │
        ▼

Panels

        │
        ▼

Qt Widgets
```

Rendering remains fully independent from deterministic backend services.

---

# Manual Validation Workflow

Every GUI sprint ends with:

1. python run_tests.py
2. Start Orion desktop application
3. Manual GUI validation
4. Screenshot review
5. Documentation synchronization

A sprint is not considered complete until manual GUI validation has been performed.

---

# Current GUI Status

Completed:

✔ Mission Control is primary workspace

✔ Trading Workspace integrated

✔ WorkspaceRenderer panel support

✔ GuiWorkspacePanel support

✔ Scan Market button

✔ Automatic Mission Control refresh

✔ Scan Duration panel

✔ Market Status panel

✔ Top Opportunities panel

Current desktop validation:

✔ Application starts successfully

✔ Navigation functions correctly

✔ Mission Control renders correctly

✔ Trading Workspace renders correctly

✔ Regression tests pass (6/6)

✔ Portfolio Workspace redesigned

✔ Trading Capital persistence

✔ Market Data age

✔ Opportunity market prices

# Presentation Architecture

The presentation layer translates deterministic backend output into immutable presentation models.

Presentation never performs calculations.

Presentation never determines trading decisions.

Presentation never accesses providers.

Its only responsibility is preparing data for rendering.

---

# Presentation Pipeline

The complete presentation pipeline is:

```
Backend Services
        │
        ▼
Workspace Presenters
        │
        ▼
Presentation Models
        │
        ▼
WorkspaceRenderer
        │
        ▼
Qt Widgets
```

Presentation remains completely independent from business logic.

---

# Workspace Rules

Every workspace inside Orion follows identical rules.

A workspace may:

- receive presentation models
- own layouts
- own widgets
- own interaction
- forward user actions to controllers

A workspace may never:

- calculate indicators
- execute TradingPipeline
- access providers
- calculate confidence
- calculate risk
- determine BUY / SELL decisions

---

# Controller Architecture

Controllers coordinate interaction between the UI and backend services.

Controllers may:

- receive user actions
- invoke backend services
- invoke presenters
- update workspaces

Controllers never:

- calculate indicators
- perform rendering
- create AI explanations
- determine trading signals

Current controllers:

```
MissionControlController

TradingController
```

Future controllers:

```
PortfolioController

PerformanceController

ScannerController
```

---

# Rendering Rules

Rendering remains fully deterministic.

Rendering owns:

- widget creation
- layouts
- panel composition
- chart composition
- styling

Rendering never owns:

- providers
- calculations
- business logic
- AI

---

# Panel Rules

Every reusable panel follows the same rules.

Panels may:

- display labels
- display values
- display icons
- display metadata

Panels may never:

- calculate values
- determine trading signals
- access backend services
- call providers

Panels always receive immutable GuiWorkspacePanel objects.

---

# Chart Rules

ChartCanvas remains the only rendering engine.

Every future visualization must reuse ChartCanvas.

Examples:

- candlesticks
- moving averages
- RSI
- MACD
- Bollinger Bands
- volume
- trade markers
- annotations

Alternative rendering implementations are forbidden.

---

# Refresh Strategy

Current refresh intervals:

Mission Control

60 seconds

Trading Workspace

Manual analysis

Scanner

30 seconds (planned)

Portfolio

30 seconds (planned)

News

2–5 minutes (planned)

Future websocket providers may replace polling without changing presentation architecture.

---

# Desktop Validation

Every completed sprint must pass the following validation sequence.

Step 1

```
python run_tests.py
```

Expected result:

```
6 passed
```

Step 2

Start Orion

```
python app.py
```

Step 3

Manual GUI validation.

Verify:

- application starts
- Mission Control opens
- navigation works
- Trading Workspace works
- Scan Market button works
- automatic refresh works
- no console exceptions

Step 4

Screenshot review.

Every GUI sprint is visually reviewed before implementation continues.

Step 5

Documentation synchronization.

Only after documentation has been updated is the sprint considered complete.

---

# Development Workflow

Every Orion sprint follows the same lifecycle.

```
Architecture

↓

Implementation

↓

Regression Tests

↓

Desktop Launch

↓

GUI Validation

↓

Documentation

↓

Git Commit

↓

GitHub Push
```

This workflow is mandatory.

---

# Current Roadmap



## Sprint 5.2

Position Sizing Presentation

Objectives

- recommended shares
- investment
- remaining capital
- budget validation

---

## Sprint 4.9.2

Market Health

Objectives:

- Universe Coverage
- Scanner Health
- Last Refresh
- Scan Duration improvements
- Error Summary

---

## Sprint 4.9.3

Trading Workspace 2.0

Objectives:

- Entry
- Stop Loss
- Take Profit
- Risk / Reward
- Trade Checklist
- enhanced AI explanation

---

## Sprint 4.9.4

Position Monitor

Objectives:

- Open Positions
- Exit Signals
- Position Timeline
- Portfolio Health
- Exit Recommendations

---

## Sprint 5.0

Paper Trading

Objectives:

- virtual broker
- simulated execution
- order lifecycle
- trade journal
- performance tracking

---

# Architecture Freeze

Architecture Version

v1.9

Status

ACTIVE

Frozen principles:

- deterministic backend
- TradingPipeline is the only decision engine
- AI explainability only
- Mission Control is the primary workspace
- presentation-only UI
- GuiWorkspace presentation contract
- reusable GuiWorkspacePanel architecture
- ChartCanvas rendering engine
- one controller responsibility
- one presenter responsibility

Architecture changes require explicit approval before implementation.

# Definition of Done

A sprint is complete only when all of the following criteria have been satisfied.

## Implementation

✔ Feature implemented

✔ Architecture respected

✔ No duplicated business logic

✔ No business logic inside the UI

✔ TradingPipeline remains the single source of truth

✔ AI remains explainability only

---

## Validation

✔ Regression tests executed

Expected result:

```
python run_tests.py

6 passed
```

✔ Desktop application starts successfully

```
python app.py
```

✔ Manual GUI validation completed

✔ Screenshot review completed

✔ No console exceptions

---

## Documentation

✔ Documentation synchronized

✔ Architecture version updated (if required)

✔ Current sprint updated

✔ TODO synchronized

✔ CHANGELOG synchronized

✔ AI_CONTEXT synchronized

---

## Source Control

✔ Git commit created

✔ GitHub repository synchronized

---

# Documentation Structure

The official Orion documentation consists of exactly seven documents.

```
PROJECT_VISION.md

ORION_MASTER_ARCHITECTURE.md

TRADING_STRATEGY.md

PROJECT_STATUS.md

TODO.md

CHANGELOG.md

AI_CONTEXT.md
```

Responsibilities:

PROJECT_VISION

Long-term product vision.

---

ORION_MASTER_ARCHITECTURE

Single architectural source of truth.

---

TRADING_STRATEGY

Deterministic trading methodology.

---

PROJECT_STATUS

Current implementation status.

---

TODO

Remaining implementation work.

---

CHANGELOG

Historical implementation log.

---

AI_CONTEXT

Context required for every new Orion development session.

No architectural duplication is allowed outside ORION_MASTER_ARCHITECTURE.md.

---

# New Chat Protocol

Every new Orion development session follows exactly the same workflow.

## Phase 1

Upload:

- complete Project Orion ZIP
- all synchronized documentation

---

## Phase 2

Before writing code:

1. Read every documentation file completely.

2. Analyse the complete project source tree.

3. Determine:

- Architecture Version
- Documentation Version
- Current Sprint
- Completed work
- Work in progress
- Next logical implementation step

No implementation begins before this analysis has been completed.

---

## Phase 3

Implementation rules.

- No assumptions.
- One complete file at a time.
- No snippets.
- Full revision files only.
- Backend remains deterministic.
- AI explainability only.
- No business logic inside UI.
- TradingPipeline remains the only decision engine.
- Mission Control remains the primary workspace.
- ChartCanvas remains the only rendering engine.

---

## Phase 4

Validation after every completed file.

Run:

```powershell
python run_tests.py
```

Expected result:

```
6 passed
```

---

## Phase 5

At the end of every sprint:

1. Start Orion

```powershell
python app.py
```

2. Review the GUI.

Every sprint must produce a visible GUI improvement.

Examples:

- richer Mission Control
- improved Trading Workspace
- better charts
- improved layouts
- additional deterministic information

The GUI is reviewed before the next sprint begins.

---

## Phase 6

Documentation.

Synchronize:

- PROJECT_STATUS.md
- TODO.md
- CHANGELOG.md
- AI_CONTEXT.md

Update architecture documentation only when architectural changes have been introduced.

---

# Orion Philosophy

Project Orion is not designed to predict markets.

Project Orion continuously identifies deterministic opportunities with controlled risk.

Artificial Intelligence enhances explainability.

Deterministic backend services generate decisions.

Mission Control presents those decisions.

The human trader remains responsible for execution.

Professional architecture always has priority over implementation speed.

Every sprint should make Orion feel more like a professional trading workstation.

---

# Current State (v1.10)

Architecture

✔ Stable

Backend

✔ Stable

Desktop Foundation

✔ Stable

Mission Control

🚧 Active expansion

Current Sprint

Current Sprint

🚧 Sprint 5.1 — Portfolio & Position Sizing Foundation

Validation

✔ 6 / 6 tests passed

✔ Desktop application launches successfully

✔ Manual GUI validation completed

---

# End of ORION MASTER ARCHITECTURE