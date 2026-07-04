# ORION AI CONTEXT

---

# Current Phase

## Sprint 4.7 — Professional Chart UX & Live Dashboard Integration

Project Orion has completed its deterministic backend foundation.

The backend is considered production stable.

Current development is focused entirely on the professional desktop experience.

No new trading logic is being added.

Development currently focuses on:

- reusable chart rendering
- professional chart UX
- live market-data presentation
- dashboard visualization
- overlay infrastructure
- desktop interaction polish

while preserving the deterministic backend.

Sprint 4.5 introduced the ChartCanvas Framework.

Sprint 4.6 made the ChartCanvas visible inside the dashboard and connected it to the workspace rendering pipeline.

Sprint 4.7 is now focused on making the chart understandable and useful for real users.

---

# Current Sprint Status

## Completed

Completed components:

- ChartCanvas
- ChartViewport
- ChartLayer
- AxisLayer
- GridLayer
- AxisLabelLayer
- LineSeriesLayer
- ValueLabelLayer
- OverlayLayer
- CrosshairLayer
- SignalLayer
- ChartCanvasBuilder
- Lightweight LineChartWidget refactor
- ChartContainer layout mounting
- Dashboard chart rendering
- Dashboard live market-data trigger
- Yahoo Finance close-price chart integration
- Professional chart-card shell
- Chart summary metadata
- Chart legend foundation
- X/Y axis label foundation

---

# Current Working State

The desktop application starts successfully.

The Dashboard page renders:

- Portfolio Value card
- Cash card
- Positions card
- Analyseer markt button
- SPY price chart after market scan

The Trading page renders:

- Symbol input
- Analyze button
- Decision card
- Confidence card
- Pressure card
- Position Size card
- Risk card
- AI Explanation panel
- Status panel

The Trading Analyze button currently updates the UI with a mock view model.

The Dashboard Analyseer markt button currently fetches Yahoo Finance historical close prices and renders them through the ChartCanvas pipeline.

The dashboard chart is no longer demo-only.

The chart now displays actual fetched market close data, but it is not streaming live data yet.

The label "live" must be interpreted as latest scan-fetched market data, not real-time streaming.

---

# Architecture Principles

## Deterministic First

All trading decisions originate from the Trading Pipeline.

Artificial Intelligence never calculates anything.

Artificial Intelligence only explains deterministic outputs.

No AI-generated trading decisions are allowed.

The Trading Pipeline remains the single source of truth.

---

## Layer Separation

Business logic lives only in backend services.

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

↓

Qt Painting

---

## Responsibilities

ApplicationController

- Coordinates UI events.
- Coordinates dashboard refresh.
- Coordinates market scan actions.
- Coordinates trading analysis actions.
- Does not own trading logic.
- Does not calculate trading decisions.

Presenters

- Transform backend/provider output into presentation models.
- Perform presentation-only formatting.
- Do not perform trading decisions.
- Do not perform AI calculations.

GuiWorkspace

- Owns dashboard presentation composition.
- Contains cards, charts, chart sections, sections, status and metadata.
- Contains no business logic.

Renderers

- Convert presentation models into widgets.
- Own rendering orchestration only.
- Contain no business logic.

Widget Factories

- Select widget implementations.
- Centralize widget creation.
- Contain no business logic.

Widgets

- Own UI composition only.
- Display presentation models.
- Contain no trading logic.
- Contain no AI logic.
- Contain no backend calculations.

ChartCanvasBuilder

- Composes ChartCanvas instances.
- Selects ChartLayers.
- Translates GuiChart presentation models into rendering layers.
- Contains no trading logic.

ChartCanvas

- Owns paint lifecycle.
- Owns mouse interaction forwarding.
- Delegates drawing to layers.
- Contains no business logic.

ChartLayers

- Own reusable drawing logic.
- Draw grid, axes, labels, lines, overlays and markers.
- Contain no backend logic.

---

# Rendering Pipeline

Current chart rendering pipeline:

GuiChart

↓

ChartRenderer

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

AxisLabelLayer

↓

LineSeriesLayer

↓

ValueLabelLayer

↓

CrosshairLayer

↓

SignalLayer

↓

OverlayLayer

---

# Dashboard Rendering Pipeline

Current dashboard pipeline:

ApplicationController

↓

DashboardWorkspacePresenter

↓

GuiWorkspace

↓

DashboardWorkspace

↓

WorkspaceRenderer

↓

DashboardGrid

↓

ChartContainer

↓

ChartRenderer

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

The ChartCanvas Framework is now the core visualization engine.

It is reusable across:

- dashboard line charts
- future candlestick charts
- future portfolio charts
- future heatmaps
- future gauge widgets
- future performance charts
- future scanner visualizations

The framework currently supports:

- reusable canvas rendering
- reusable grid rendering
- reusable axis rendering
- reusable axis labels
- reusable line-series rendering
- reusable high/low value labels
- reusable overlay extension point
- crosshair foundation
- signal overlay foundation

---

# ChartCanvasBuilder

ChartCanvasBuilder is responsible for composing reusable chart layers.

Current line chart layer composition:

- GridLayer
- AxisLayer
- AxisLabelLayer
- LineSeriesLayer
- ValueLabelLayer
- CrosshairLayer
- SignalLayer
- OverlayLayer

ChartCanvasBuilder remains presentation-only.

It must not perform trading logic.

It must not perform AI logic.

It must not access backend services directly.

---

# Dashboard Live Data Integration

The dashboard currently uses Yahoo Finance historical close prices when the user clicks Analyseer markt.

Current behavior:

- Dashboard starts with cards and no active chart data.
- User clicks Analyseer markt.
- ApplicationController requests close-price history.
- DashboardWorkspacePresenter creates a GuiChart.
- ChartRenderer creates a LineChartWidget.
- LineChartWidget displays the chart-card and ChartCanvas.
- ChartCanvas draws the close-price line.

Important distinction:

This is scan-fetched historical market data.

This is not yet streaming real-time data.

Future live-dashboard work must introduce scheduled refresh or background update orchestration.

---

# Professional Chart UX Status

Completed:

- Chart-card wrapper
- Chart title
- Chart subtitle
- Summary metadata area
- Legend foundation
- Source label
- Last value
- High value
- Low value
- Change percentage
- Data point count
- Y-axis value labels
- X-axis label foundation

Still needed:

- clearer X-axis date labels
- real date labels from Yahoo data
- hover tooltip
- nearest datapoint detection
- cursor value display
- crosshair snapping
- improved legend placement
- better axis formatting
- clearer status wording
- distinction between scan-data and streaming-live data

---

# Current UI Reality

Dashboard:

- Cards work.
- Analyseer markt works.
- SPY chart appears after scan.
- Chart uses Yahoo Finance close prices.
- Chart is readable but not yet production-grade.

Trading:

- Analyze button works.
- Trading UI updates with a mock view model.
- Real TradingPipeline integration is not yet restored.
- No trading chart is shown yet.

Portfolio:

- Portfolio workspace renders.
- No chart integration yet.

Performance:

- No chart integration yet.

Scanner:

- No chart integration yet.

---

# Current Development Focus

Immediate focus:

- polish the current dashboard chart
- replace index-based X-axis labels with real date labels
- add hover tooltip with date and close price
- clarify scan-data versus streaming-live status
- improve legend clarity
- keep all UI logic presentation-only

Next focus:

- connect Trading page to deterministic TradingPipeline
- add Trading chart visualization
- add Portfolio allocation visualization
- add Performance equity/PnL chart
- prepare Live Dashboard refresh cycle

---

# Current Rules

Strict rules remain active:

- No business logic in UI.
- No calculations in widgets beyond presentation formatting.
- No AI logic in frontend.
- No trading logic outside backend services.
- ChartCanvas owns painting only.
- ChartLayers own drawing only.
- ChartCanvasBuilder owns composition only.
- Widgets own UI composition only.
- Presenters transform deterministic/backend/provider output into presentation models.
- Every file update must be delivered as a complete file.
- No patches.
- No loose snippets.
- No half implementations.

---

# Testing Status

Current known validation:

- `python run_tests.py` previously passed with 6 passed.
- The desktop app starts.
- Dashboard cards render.
- Trading page renders.
- Analyze button updates Trading UI.
- Analyseer markt updates Dashboard state and chart.
- ChartCanvas is visible inside Dashboard.
- Chart line renders.

Required next validation after each implementation:

```powershell
python run_tests.py
python app.py