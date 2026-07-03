# ORION AI CONTEXT

---

# Current Phase

## Sprint 4.5 — ChartCanvas Framework

Project Orion has completed its deterministic backend foundation.

The backend is considered production stable.

Current development is focused entirely on the professional desktop experience.

No new trading logic is being added.

Development focuses on:

- presentation architecture
- reusable renderers
- reusable widgets
- reusable chart infrastructure
- desktop UX improvements

while preserving the deterministic backend.

---

# Sprint 4.5 Status

Sprint 4.5 has evolved into the ChartCanvas Framework foundation.

Completed components:

- ChartCanvas
- ChartViewport
- ChartLayer
- AxisLayer
- GridLayer
- LineSeriesLayer
- ValueLabelLayer
- OverlayLayer
- ChartCanvasBuilder
- Lightweight LineChartWidget refactor

---

# Architecture Principles

## Deterministic First

All trading decisions originate from the Trading Pipeline.

AI never calculates anything.

AI only explains deterministic outputs.

---

## Layer Separation

Business logic lives ONLY in backend services.

Presentation flow:

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

---

## Responsibilities

- ApplicationController → orchestration
- Presenters → transformation only
- GuiWorkspace → composition only
- Renderers → orchestration only
- WidgetFactory → creation only
- Widgets → UI composition only
- ChartCanvasBuilder → canvas composition only
- ChartCanvas → painting only
- ChartLayers → drawing only

No layer may contain:
- trading logic
- AI logic
- portfolio calculations

---

# Rendering Pipeline

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
GridLayer  
↓  
AxisLayer  
↓  
LineSeriesLayer  
↓  
ValueLabelLayer  
↓  
OverlayLayer  

---

# ChartCanvas Framework

The ChartCanvas Framework is now the core visualization engine.

It is reusable across:

- line charts
- candlestick charts (future)
- portfolio charts
- heatmaps
- gauges
- dashboards

---

# ChartCanvasBuilder

Responsible for:

- translating GuiChart → ChartCanvas
- selecting correct ChartLayers
- keeping widgets lightweight
- centralizing composition logic

---

# Overlay System

OverlayLayer introduces extension point for:

- crosshair
- trade markers
- annotations
- indicators
- selections
- highlights

---

# Current Architecture Status

Backend: Stable  
UI: Active development  
Chart system: Fully refactored foundation  
Sprint: 4.5 in progress  

---

# Current Focus

Next improvements:

- reusable layer expansion
- annotation system
- crosshair system
- indicator overlays
- portfolio visualizations
- gauge widgets
- dashboard layout 2.0
- live updates

No backend changes planned.

---

# Rules (STRICT)

- No business logic in UI
- No calculations in widgets
- No AI logic in frontend
- ChartCanvas = painting only
- ChartLayers = drawing only
- Builder = composition only
- Widgets = UI only

---

# Architecture Freeze

v1.6 (MUST NOT CHANGE)

---

# Long-Term Vision

A deterministic AI-assisted desktop trading platform:

- professional dashboard
- reusable chart engine
- live visualization system
- explainable AI
- backtesting
- portfolio tools

AI never makes trading decisions.
Only explains them.