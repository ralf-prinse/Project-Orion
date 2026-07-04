# PROJECT ORION

# PROJECT STATUS

---

# Project Version

**v1.3.0-alpha**

Status

🟢 Active Development

Current Milestone

🚧 Sprint 4.7 — Professional Chart UX

Architecture Freeze

**v1.6**

---

# Executive Summary

Project Orion is a deterministic AI-assisted desktop trading platform.

The deterministic backend is considered production stable.

Current development is fully focused on desktop visualization, reusable presentation architecture and professional user experience.

No new trading logic is currently being introduced.

The Trading Pipeline remains the single source of truth for all trading decisions.

Current work is focused on:

- reusable ChartCanvas infrastructure
- professional dashboard visualization
- live market-data presentation
- reusable chart components
- dashboard UX improvements
- preparation for portfolio and performance visualization

---

# Core Principle

Artificial Intelligence NEVER makes trading decisions.

All deterministic decisions originate exclusively from:

👉 TradingPipeline

Artificial Intelligence only explains deterministic outputs.

---

# Current System State

## Backend

🟢 Production Stable

Completed:

- TradingPipeline
- IndicatorBuilder
- IndicatorPack
- Signal Fusion Engine
- Market Intelligence
- Adaptive Decision Engine
- Position Sizing Engine
- AI Context Builder
- AI Explanation Engine
- Backtesting Engine

No structural backend changes are planned.

---

## Desktop Foundation

🟢 Stable

Completed:

- Workspace architecture
- ApplicationController
- GuiWorkspace
- Presenter architecture
- Renderer architecture
- Widget Factory architecture
- Dashboard workspace
- Trading workspace
- Portfolio workspace foundation

---

## Dashboard

🟢 Functional

Implemented:

- Portfolio cards
- Cash card
- Positions card
- DashboardGrid
- WorkspaceRenderer integration
- ChartContainer integration
- Analyseer markt button

Current behaviour:

- Dashboard loads correctly.
- Analyseer markt requests Yahoo Finance historical market data.
- Dashboard renders a professional chart-card.
- Dashboard displays fetched SPY close-price history.

---

## Trading

🟢 Functional

Implemented:

- Symbol input
- Analyze button
- Decision card
- Confidence card
- Pressure card
- Position Size card
- Risk card
- AI Explanation panel
- Status panel

Current behaviour:

Trading currently displays a mock presentation model.

TradingPipeline integration will be restored after dashboard visualization reaches production quality.

---

## Chart System

🟢 Foundation Complete

The ChartCanvas Framework is now operational.

Implemented:

- ChartCanvas
- ChartViewport
- ChartLayer abstraction
- GridLayer
- AxisLayer
- AxisLabelLayer
- LineSeriesLayer
- ValueLabelLayer
- CrosshairLayer
- SignalLayer
- OverlayLayer
- ChartCanvasBuilder
- ChartContainer
- LineChartWidget

Chart rendering is fully separated from widgets.

Widgets no longer perform painting.

Rendering is delegated to ChartCanvas.

---

## Live Market Data

🟢 Implemented

Dashboard currently retrieves market history from Yahoo Finance.

Current workflow:

Analyseer markt

↓

Yahoo Provider

↓

Historical Close Prices

↓

DashboardWorkspacePresenter

↓

GuiChart

↓

ChartRenderer

↓

LineChartWidget

↓

ChartCanvas

↓

ChartLayers

Current implementation renders scan-fetched historical market data.

Streaming real-time updates have NOT yet been implemented.

# Current Architecture

The desktop rendering pipeline is now fully layered.

ApplicationController

↓

Presenters

↓

GuiWorkspace

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

↓

Qt Painting

Each layer owns exactly one responsibility.

No architectural violations are currently known.

---

# Professional Chart UX

## Completed

✔ Professional chart card

✔ Chart title

✔ Chart subtitle

✔ Summary information panel

✔ Chart legend foundation

✔ Source information

✔ Last value

✔ Highest value

✔ Lowest value

✔ Change percentage

✔ Data point counter

✔ Grid rendering

✔ Axis rendering

✔ Axis label foundation

✔ High/Low value labels

✔ Crosshair foundation

---

## In Progress

- clearer X-axis date labels
- improved Y-axis formatting
- hover tooltip
- nearest datapoint detection
- cursor value display
- crosshair snapping
- improved legend styling
- professional spacing
- dashboard chart polish

---

# Portfolio Workspace

🟡 Foundation Ready

Current state:

- Workspace available
- Navigation available
- No portfolio visualization yet

Planned:

- allocation chart
- position overview
- unrealized P/L
- historical equity
- allocation breakdown

---

# Performance Workspace

🟡 Planned

Will reuse ChartCanvas.

Planned visualizations:

- equity curve
- cumulative return
- drawdown
- monthly returns
- benchmark comparison

---

# Scanner Workspace

🟡 Planned

Will reuse ChartCanvas.

Planned visualizations:

- scanner overview
- sector heatmap
- opportunity timeline
- confidence gauges
- market breadth

---

# Testing Status

Current status:

✔ Desktop starts correctly

✔ Dashboard loads

✔ Trading loads

✔ Portfolio loads

✔ Navigation works

✔ Analyseer markt works

✔ Trading Analyze works

✔ Dashboard cards update

✔ ChartCanvas renders

✔ ChartContainer renders

✔ WorkspaceRenderer renders

✔ ChartRenderer renders

✔ WidgetFactory renders

Known limitations:

- X-axis still uses placeholder labels
- hover tooltip not implemented
- real-time streaming not implemented
- TradingPipeline not yet reconnected to Trading workspace

---

# Validation Procedure

Before every commit:

```powershell
python run_tests.py
```

Before every push:

```powershell
python app.py
```

Manual validation:

- application starts
- Dashboard renders
- Trading renders
- Analyseer markt updates dashboard
- chart renders
- no exceptions
- resize works
- navigation works

---
# Current Sprint

## Sprint 4.7 — Professional Chart UX

Primary objective:

Transform the working ChartCanvas implementation into a professional visualization framework.

Current priorities:

1. Replace placeholder X-axis labels with real market dates.
2. Add hover tooltip with nearest datapoint information.
3. Improve crosshair behaviour.
4. Improve legend positioning and styling.
5. Clearly distinguish latest scan-data from future streaming live data.
6. Prepare reusable chart widgets for all Orion workspaces.

---

# Upcoming Sprint

## Sprint 4.8 — Dashboard & Trading Integration

Primary goals:

- Restore deterministic TradingPipeline integration.
- Replace Trading mock presentation model.
- Add Trading chart.
- Add signal visualization.
- Add indicator overlays.
- Add portfolio chart integration.

---

# Future Roadmap

## Desktop Visualization

Planned:

- Portfolio Allocation chart
- Performance chart
- Drawdown visualization
- Portfolio timeline
- Watchlist visualization
- Scanner dashboard
- Heatmaps
- Candlestick charts
- Indicator overlays
- Multi-series charts

---

## Live Dashboard

Future work:

- automatic refresh
- configurable refresh interval
- background scanner
- live portfolio metrics
- streaming market data
- notification framework

---

## Portfolio Intelligence

Future work:

- allocation optimization
- historical performance
- risk decomposition
- exposure analysis
- benchmark comparison

---

## Paper Trading

Future work:

- virtual broker
- simulated orders
- replay engine
- strategy comparison
- execution statistics

---

# Architecture Status

Backend

🟢 Production Stable

Desktop

🟢 Stable Foundation

ChartCanvas Framework

🟢 Stable Foundation

Professional Chart UX

🟡 Active Development

Trading Workspace

🟡 Integration Phase

Portfolio Workspace

🟡 Planned Expansion

Performance Workspace

🟡 Planned Expansion

---

# Known Limitations

Current limitations are presentation-related only.

Remaining work:

- real market date labels
- hover tooltip
- nearest datapoint detection
- crosshair snapping
- indicator overlays
- multi-series support
- streaming updates

No deterministic backend limitations are known.

---

# Definition of Done

A sprint task is ONLY complete when:

✔ Implementation complete

✔ Architecture respected

✔ Presentation layer remains free of business logic

✔ Tests pass

✔ Desktop application starts

✔ Manual UI validation completed

✔ Documentation updated

✔ Git commit created

✔ GitHub push completed

---

# New Chat Procedure

Before starting a new conversation:

1. Update all project `.md` files.
2. Commit documentation.
3. Push to GitHub.
4. Create a new chat.
5. Upload:
   - the complete Project Orion ZIP;
   - all updated `.md` files.
6. The new chat **must first**:
   - read every `.md` file;
   - inspect the complete project source;
   - analyse the current architecture before writing any code.
7. Only after the full analysis may implementation begin.

This procedure is mandatory to preserve architectural continuity between chats.

---

# Project Vision

Project Orion is evolving into a professional deterministic AI-assisted desktop trading platform.

Core objectives:

- deterministic decision making
- reusable visualization framework
- professional desktop UX
- explainable AI
- reusable ChartCanvas engine
- portfolio intelligence
- scanner intelligence
- backtesting
- paper trading
- future broker connectivity

Artificial Intelligence never makes trading decisions.

Artificial Intelligence explains deterministic results produced by the TradingPipeline.

The TradingPipeline remains the single source of truth for every trading decision.

---

# End of Project Status