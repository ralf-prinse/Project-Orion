# ORION TODO

---

# ✅ Completed

## Core Architecture

- [x] Deterministic service architecture
- [x] Desktop workspace architecture
- [x] Presenter architecture
- [x] Renderer architecture
- [x] Widget Factory architecture
- [x] ApplicationController architecture
- [x] Architecture Freeze v1.7

---

## Backend (Completed)

- [x] Yahoo Provider abstraction
- [x] Historical data provider
- [x] Market Service
- [x] TradingPipeline
- [x] IndicatorBuilder
- [x] IndicatorPack
- [x] Signal Fusion Engine
- [x] Market Intelligence Engine
- [x] Adaptive Decision Engine
- [x] Position Sizing Engine
- [x] Risk Engine
- [x] AI Context Builder
- [x] AI Explanation Engine
- [x] Backtest Engine Suite

Backend architecture is considered production stable.

No structural backend work is currently planned.

---

## Desktop Foundation

- [x] GuiWorkspace
- [x] Dashboard Workspace
- [x] Trading Workspace
- [x] Portfolio Workspace foundation
- [x] WorkspaceRenderer
- [x] DashboardGrid
- [x] ChartRenderer
- [x] ChartWidgetFactory
- [x] ChartContainer
- [x] LineChartWidget
- [x] ApplicationController integration

---

## ChartCanvas Framework

Completed:

- [x] ChartCanvas
- [x] ChartViewport
- [x] ChartLayer abstraction
- [x] GridLayer
- [x] AxisLayer
- [x] AxisLabelLayer
- [x] LineSeriesLayer
- [x] ValueLabelLayer
- [x] CrosshairLayer foundation
- [x] SignalLayer foundation
- [x] OverlayLayer
- [x] ChartCanvasBuilder
- [x] ChartContainer integration
- [x] Dashboard rendering integration

---

## Dashboard

Completed:

- [x] Dashboard cards
- [x] Dashboard chart integration
- [x] Dashboard chart summary
- [x] Dashboard chart legend foundation
- [x] Dashboard market scan button
- [x] Yahoo Finance historical close-price integration
- [x] Professional chart-card foundation

Dashboard now renders fetched Yahoo Finance market history.

The dashboard no longer displays demonstration chart data.

---

## Testing

Completed:

- [x] Presentation tests
- [x] ChartCanvas tests
- [x] ChartLayer tests
- [x] Renderer tests
- [x] WidgetFactory tests
- [x] LineChartWidget tests
- [x] Regression runner

Current validation:

- [x] Desktop application starts
- [x] Dashboard renders
- [x] Trading renders
- [x] Dashboard chart renders
- [x] Analyseer markt works
- [x] Trading Analyze works

---

# 🚧 Current Sprint

## Sprint 4.7 — Professional Chart UX

Primary objective:

Transform the technically working ChartCanvas implementation into a production-quality visualization framework.

Completed:

- [x] ChartCanvas visible inside Dashboard
- [x] Professional chart card
- [x] Summary information
- [x] Chart legend foundation
- [x] Axis label foundation
- [x] Yahoo Finance integration
- [x] Dashboard rendering pipeline stabilization

Current work:

- [ ] Real X-axis market dates
- [ ] Hover tooltip
- [ ] Nearest datapoint detection
- [ ] Crosshair snapping
- [ ] Better axis formatting
- [ ] Improved legend styling
- [ ] Professional chart spacing
- [ ] Production chart UX

---
# 📊 Current Focus Areas

## Professional Chart UX

Highest priority:

- Real market date labels on X-axis
- Adaptive Y-axis formatting
- Hover tooltip with market data
- Nearest datapoint detection
- Crosshair snapping
- Better legend positioning
- Professional spacing
- Chart resizing improvements
- Better value formatting
- Chart interaction polish

---

## Dashboard

Current objectives:

- [ ] Replace placeholder X-axis labels with Yahoo market dates
- [ ] Tooltip showing:
  - date
  - close price
  - percentage change
- [ ] Better chart status indicator
- [ ] Distinguish latest scan-data from future streaming data
- [ ] Better legend styling
- [ ] Multiple dashboard charts
- [ ] Dashboard responsiveness
- [ ] Better empty-state handling

---

## Trading Workspace

Next objectives:

- [ ] Remove remaining mock presentation model
- [ ] Reconnect deterministic TradingPipeline
- [ ] Trading chart
- [ ] BUY markers
- [ ] SELL markers
- [ ] HOLD markers
- [ ] Indicator overlays
- [ ] Signal visualization
- [ ] Confidence visualization
- [ ] Risk visualization
- [ ] Position visualization

Trading will reuse the existing ChartCanvas Framework.

---

## Portfolio Workspace

Planned:

- [ ] Portfolio allocation chart
- [ ] Portfolio overview table
- [ ] Unrealized P/L
- [ ] Realized P/L
- [ ] Historical equity
- [ ] Allocation breakdown
- [ ] Portfolio timeline
- [ ] Portfolio heatmap

Portfolio visualization will reuse ChartCanvas.

---

## Performance Workspace

Planned:

- [ ] Equity curve
- [ ] Drawdown chart
- [ ] Monthly performance
- [ ] Benchmark comparison
- [ ] Rolling returns
- [ ] Performance statistics
- [ ] Risk statistics

---

## Scanner Workspace

Planned:

- [ ] Scanner dashboard
- [ ] Opportunity timeline
- [ ] Sector heatmap
- [ ] Confidence gauges
- [ ] Market breadth visualization
- [ ] Scanner statistics
- [ ] Opportunity ranking

---

## ChartCanvas Evolution

Next technical improvements:

- [ ] Hover tooltip layer
- [ ] Datapoint selection layer
- [ ] Annotation layer
- [ ] Multiple line-series support
- [ ] Candlestick renderer
- [ ] Area chart renderer
- [ ] Zoom support
- [ ] Pan support
- [ ] Chart synchronization
- [ ] Shared crosshair
- [ ] Theme-aware rendering
- [ ] Performance optimization

---

## Live Dashboard

Planned:

- [ ] Automatic refresh
- [ ] Configurable refresh interval
- [ ] Background market scanning
- [ ] Scheduled updates
- [ ] Live portfolio metrics
- [ ] Streaming provider abstraction
- [ ] WebSocket integration
- [ ] Live notification framework

---

# 🚀 Upcoming Sprints

---

## Sprint 4.8 — Trading Visualization

Primary goals:

- [ ] Restore deterministic TradingPipeline integration
- [ ] Remove Trading mock presentation model
- [ ] Trading chart
- [ ] Indicator visualization
- [ ] BUY / SELL markers
- [ ] Position overlays
- [ ] Confidence overlays
- [ ] Risk overlays
- [ ] AI explanation synchronization

---

## Sprint 4.9 — Portfolio Visualization

Primary goals:

- [ ] Portfolio allocation chart
- [ ] Historical equity visualization
- [ ] Unrealized P/L chart
- [ ] Allocation timeline
- [ ] Exposure analysis
- [ ] Portfolio statistics
- [ ] Historical portfolio replay

---

## Sprint 5.0 — Live Dashboard

Primary goals:

- [ ] Background refresh engine
- [ ] Configurable refresh interval
- [ ] Streaming market updates
- [ ] Live dashboard widgets
- [ ] Market notifications
- [ ] Live portfolio updates
- [ ] Watchlist support

---

## Sprint 5.x

Long-term goals:

- [ ] Paper Trading
- [ ] Replay Engine
- [ ] Strategy Comparison
- [ ] Broker abstraction
- [ ] Broker integrations
- [ ] Portfolio Intelligence
- [ ] Scanner Intelligence
- [ ] Multi-monitor desktop support

---

# 🧠 Architecture Rules

These rules are mandatory.

Backend

- Trading logic only inside backend services.
- Indicator calculations only inside backend.
- Risk calculations only inside backend.
- AI never performs calculations.
- TradingPipeline remains the single source of truth.

Presentation

- Widgets contain presentation only.
- Renderers perform rendering orchestration only.
- Presenters transform deterministic output only.
- ChartCanvas paints only.
- ChartLayers draw only.
- ChartCanvasBuilder composes only.
- ApplicationController orchestrates only.

General

- No duplicated rendering implementations.
- No duplicated business logic.
- No backend calculations inside UI.
- Every new visualization must reuse ChartCanvas.
- Every new chart must use GuiChart models.

---

# 🧪 Validation

Before every commit:

```powershell
python run_tests.py
```

Before every push:

```powershell
python app.py
```

Manual validation checklist:

- [ ] Application starts
- [ ] Dashboard renders
- [ ] Trading renders
- [ ] Portfolio renders
- [ ] Navigation works
- [ ] Analyseer markt works
- [ ] Dashboard chart renders
- [ ] Dashboard cards update
- [ ] Trading Analyze works
- [ ] No console exceptions
- [ ] Window resize works

---

# 📋 Documentation Rules

Every completed sprint requires:

- [ ] Documentation updated
- [ ] PROJECT_STATUS synchronized
- [ ] AI_CONTEXT synchronized
- [ ] ARCHITECTURE synchronized
- [ ] TODO synchronized
- [ ] CHANGELOG synchronized
- [ ] Git commit created
- [ ] GitHub push completed

---

# 🔄 New Chat Workflow

Before every new Project Orion conversation:

1. Finish the current sprint documentation.
2. Commit all documentation changes.
3. Push to GitHub.
4. Create a new chat.
5. Upload:
   - the complete Project Orion ZIP;
   - all updated `.md` files.
6. The new chat must first:
   - read every Markdown file completely;
   - inspect the complete project source;
   - analyse the current architecture;
   - determine the current sprint;
   - determine completed work;
   - determine remaining work.
7. Only after the complete project analysis may implementation begin.

This workflow is mandatory.

---

# 🎯 Long-Term Vision

Project Orion evolves into a professional deterministic AI-assisted desktop trading platform.

The long-term vision includes:

- reusable desktop architecture
- reusable ChartCanvas Framework
- professional dashboard
- deterministic TradingPipeline
- explainable AI
- portfolio intelligence
- scanner intelligence
- historical analysis
- paper trading
- broker connectivity

Artificial Intelligence never makes trading decisions.

Artificial Intelligence explains deterministic outputs only.

The TradingPipeline remains the single source of truth.

---

# End of TODO