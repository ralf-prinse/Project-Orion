# ORION MASTER ARCHITECTURE

---

# Architecture Version

**Architecture Freeze v1.6**

Status

🟢 Production Foundation Stable

Current Phase

🚧 Sprint 4.5 — ChartCanvas Framework

---

# System Philosophy

Project Orion is a deterministic AI-assisted desktop trading platform.

Every architectural layer has exactly one responsibility.

AI never performs calculations.

AI only explains deterministic outputs.

The Trading Pipeline is the single source of truth.

---

# Core Principles

## Deterministic First

All trading decisions must be:

- reproducible
- deterministic
- traceable

No randomness is allowed.

No AI-generated trading decisions are allowed.

---

## Strict Layer Separation

The architecture strictly enforces separation:


Business Logic
↓
Services
↓
Presenters
↓
Presentation Models
↓
Renderers
↓
Widget Factories
↓
Widgets
↓
ChartCanvasBuilder
↓
ChartCanvas
↓
ChartLayers
↓
Qt Painting


Each layer has exactly one responsibility.

No cross-layer business logic is allowed.

---

## Forbidden in UI Layer

Never allowed in:

- Widgets
- Renderers
- ChartCanvas
- ChartLayers
- ChartCanvasBuilder

Forbidden content:

- trading logic
- AI logic
- portfolio calculations
- indicator calculations

Allowed ONLY in backend services:

- TradingPipeline
- IndicatorBuilder
- Signal Fusion Engine
- Position Sizing Engine

---

# Production Trading Architecture


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


---

# Desktop Rendering Architecture


GuiChart
↓
ChartWidgetFactory
↓
LineChartWidget
↓
ChartCanvasBuilder
↓
ChartCanvas
↓
ChartLayers


---

# ChartCanvas Framework

The ChartCanvas Framework is the reusable rendering engine of Orion.

It replaces widget-owned painting with a layered rendering system.

---

## Core Components

### ChartCanvas

- owns paint lifecycle
- delegates drawing to layers
- contains no business logic
- contains no calculations

---

### ChartCanvasBuilder

- composes ChartCanvas instances
- translates GuiChart → ChartLayers
- keeps widgets lightweight
- centralizes composition logic

---

### ChartLayers

Reusable drawing units:

- AxisLayer
- GridLayer
- LineSeriesLayer
- ValueLabelLayer
- OverlayLayer

Each layer is:

- presentation-only
- reusable
- stateless where possible

---

# Rendering Flow


GuiChart
↓
ChartWidgetFactory
↓
LineChartWidget
↓
ChartCanvasBuilder
↓
ChartCanvas
↓
ChartLayers


---

# Overlay System

OverlayLayer is the extension point for future visual features:

- crosshair
- trade markers
- annotations
- selection highlights
- indicator overlays

It ensures extensibility without architectural changes.

---

# Responsibility Map

- ApplicationController → orchestration
- Presenters → transformation
- GuiWorkspace → composition
- WidgetFactory → creation
- Widgets → UI only
- Builder → composition only
- Canvas → painting only
- Layers → drawing only

---
# Roadmap Status

---

## Phase 1 — Backend Foundation

✔ Completed

- Deterministic Trading Pipeline
- Indicator Engine
- Signal Fusion
- Position Sizing
- Market Intelligence
- Backtesting System

---

## Phase 2 — Desktop Foundation

✔ Completed

- ApplicationController
- Workspace Architecture
- Presenter Layer
- Renderer Layer
- Widget Factory Layer

---

## Phase 3 — Chart System Foundation

✔ Completed

- GuiChart models
- ChartRenderer
- ChartWidgetFactory
- LineChartWidget
- ChartContainer

---

## Phase 4 — ChartCanvas Framework

🚧 In Progress

This phase introduces a fully reusable rendering engine.

### Completed

✔ ChartCanvas  
✔ ChartViewport  
✔ ChartLayer abstraction  
✔ AxisLayer  
✔ GridLayer  
✔ LineSeriesLayer  
✔ ValueLabelLayer  
✔ OverlayLayer  
✔ ChartCanvasBuilder  
✔ LineChartWidget refactor  

---

### Current Focus

- annotation system
- crosshair system
- indicator overlays
- portfolio visualization
- gauge widgets
- advanced chart types

---

## Phase 5 — Desktop Visualization

⬜ Planned

- Portfolio Allocation charts
- Heatmaps
- Candlestick charts
- Dashboard Layout 2.0
- UX polishing

---

## Phase 6 — Live Dashboard

⬜ Planned

- real-time updates
- background scanning
- live portfolio metrics
- live charts

---

## Phase 7 — Portfolio Intelligence

⬜ Planned

- portfolio analytics
- risk modeling
- allocation optimization
- performance tracking

---

## Phase 8 — Paper Trading

⬜ Planned

- virtual trading engine
- trade simulation
- strategy comparison
- replay system

---

# Architecture Freeze

Version: v1.6

Status: ACTIVE

---

## Rules (Non-Negotiable)

- No business logic in UI
- No AI logic in frontend
- No calculations in widgets
- No calculations in ChartCanvas
- No calculations in ChartLayers
- All trading logic lives in backend only

---

# System Health

Backend:
🟢 Stable

Desktop:
🟢 Active Development

Chart System:
🟢 Stable foundation + expansion phase

---

# Definition of Done

A sprint task is ONLY complete when:

✔ Implementation complete  
✔ Tests pass  
✔ No architecture violations  
✔ Documentation updated  
✔ Git commit created  
✔ GitHub push done  

---

# Final Statement

The ChartCanvas Framework is now the core rendering engine of Project Orion.

All future visualization systems will be built on top of this architecture.

The backend remains deterministic and unchanged.

AI remains explainability-only.

---

# End of Architecture Document