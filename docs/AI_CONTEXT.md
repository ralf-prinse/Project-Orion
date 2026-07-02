# ORION AI CONTEXT

---

# Current Phase

## Sprint 4.1 — Dashboard 2.0

Project Orion has completed its deterministic backend foundation.

The backend is now considered production-stable.

Current development is focused entirely on the professional desktop experience.

No new trading logic is currently being added.

Development focuses on presentation, visualization and workspace architecture while preserving the deterministic backend.

The Dashboard presentation architecture has now been successfully migrated to the shared Orion presentation framework.

Dashboard now uses the reusable GuiMetricCard / MetricCard infrastructure throughout the presentation layer.

No temporary dashboard presentation components remain.

---

# Development Philosophy

Project Orion follows several non-negotiable engineering principles.

## Deterministic First

Every trading decision must be reproducible.

Identical market data must always generate identical output.

Artificial Intelligence never performs calculations.

Artificial Intelligence only explains deterministic results.

The Trading Pipeline remains the single source of truth.

---

## Layer Separation

Business logic exists only inside Services.

Presentation logic exists only inside Presenters.

Qt Widgets contain no business logic.

ApplicationController coordinates communication between UI and backend.

Widgets are purely responsible for rendering presentation models.

---

## Production Workflow

Every sprint follows the same workflow.

Feature

↓

Testing

↓

Documentation

↓

Git Commit

↓

GitHub Push

No sprint is considered complete until all five stages have finished.

---

# Core Trading Flow

```
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
AI Context
        ↓
AI Explanation
        ↓
Presenters
        ↓
Qt Desktop
```

Every architectural layer owns exactly one responsibility.

---

# AI Market Scanner

The AI Market Scanner uses the exact same Trading Pipeline as the Trading Workspace.

```
ApplicationController
        ↓
YahooProvider
        ↓
IndicatorBuilder
        ↓
TradingPipeline
        ↓
AIMarketScanner
        ↓
AIScannerPresenter
        ↓
Scanner Workspace
```

There is only one deterministic source of truth.

No duplicate trading logic may exist.

---

# Dashboard 2.0

Dashboard 2.0 is now fully integrated into Orion's shared presentation architecture.

Completed:

✅ DashboardGrid

✅ DashboardWorkspace

✅ DashboardData

✅ Dashboard2Presenter

✅ Portfolio Summary

✅ Cash Widget

✅ Equity Widget

✅ Today's P/L placeholder

✅ Open Positions

✅ Portfolio Exposure

✅ Confidence Gauge

✅ Pressure Gauge

✅ Risk Gauge

✅ Best Trade Card

✅ Market Health

✅ Portfolio Allocation

✅ Equity Curve placeholder

Dashboard data now flows through:

```
ApplicationController
        ↓
DashboardData
        ↓
Dashboard2Presenter
        ↓
GuiMetricCard
        ↓
MetricCard
        ↓
DashboardGrid
        ↓
DashboardWorkspace
```

---

# UI Architecture

The desktop UI follows a presentation-driven architecture.

ApplicationController coordinates all communication.

Presenters transform deterministic backend output into presentation models.

Qt Widgets render presentation models only.

Business logic is prohibited inside widgets.

The Dashboard now reuses the same reusable presentation components that are available throughout Orion.

No Dashboard-specific presentation components remain.

---

# Dashboard Presentation Architecture

Sprint 4.1 completed the migration from the temporary Dashboard presentation layer to the shared Orion widget framework.

Dashboard presentation flow:

```
ApplicationController
        ↓
DashboardData
        ↓
Dashboard2Presenter
        ↓
GuiMetricCard
        ↓
MetricCard
        ↓
DashboardGrid
        ↓
DashboardWorkspace
```

Dashboard2Presenter now produces GuiMetricCard presentation models.

DashboardGrid is responsible only for arranging reusable MetricCard widgets.

DashboardWorkspace coordinates presentation only.

MetricCard is now the single reusable dashboard card implementation inside Orion.

Duplicate presentation widgets are prohibited.

---

# Current Infrastructure

Completed

✅ TradingConfig

✅ LoggingService

✅ YahooProvider

✅ IndicatorBuilder

✅ TradingPipeline

✅ Signal Fusion Engine

✅ Market Intelligence Engine

✅ Adaptive Decision Engine

✅ Position Sizing Engine

✅ AI Context Builder

✅ AI Explanation Engine

✅ AIMarketScanner

✅ BacktestEngine

✅ BacktestSimulator

✅ BacktestVisualizer

✅ ApplicationController

✅ Dashboard 2.0 Foundation

✅ DashboardData

✅ Dashboard2Presenter

✅ DashboardGrid

✅ DashboardWorkspace

✅ Shared MetricCard infrastructure

✅ Trading Workspace

✅ Scanner Workspace

---

# Logging

Centralized logging is active.

Coverage:

✅ ApplicationController

✅ YahooProvider

✅ IndicatorBuilder

✅ TradingPipeline

✅ AIMarketScanner

✅ BacktestEngine

Destination:

```
logs/orion.log
```

The logging system provides a complete audit trail from user interaction to deterministic trading result.

---

# Testing

Regression testing remains centralized.

Official command:

```powershell
python run_tests.py
```

Current result:

```
Passed: 6
Failed: 0
```

Regression tests are mandatory before every Git commit.

---

# Current Priority

Sprint 4.1 Dashboard architecture refactor has been completed successfully.

Completed during this sprint:

✅ Dashboard2Presenter now produces GuiMetricCard presentation models.

✅ DashboardGrid now renders reusable MetricCard widgets.

✅ DashboardWorkspace now consumes GuiMetricCard directly.

✅ Temporary Dashboard presentation components have been removed.

✅ Dashboard now fully reuses Orion's shared presentation architecture.

The deterministic backend remained unchanged throughout the migration.

Regression testing confirms compatibility:

```
Passed: 6
Failed: 0
```

Current development now shifts toward Dashboard UX improvements and reusable desktop widgets.

Immediate objectives:

- Introduce reusable dashboard widget library
- Improve professional desktop experience
- Add Hero KPI cards
- Add Market Health banner
- Improve dashboard spacing
- Improve dashboard typography
- Implement Equity Curve visualization
- Implement Portfolio Allocation chart
- Implement professional Gauge widgets

No backend redesign is planned.

The Trading Pipeline remains the single deterministic source of truth.

---

# Long-Term Vision

Project Orion will evolve into a professional deterministic AI-assisted trading platform featuring:

- Professional Desktop Dashboard
- Portfolio Intelligence
- Live Market Analysis
- Explainable AI
- Historical Backtesting
- Watchlists
- Paper Trading
- Broker Integration

while preserving deterministic calculations as the only source of trading decisions.

---

# Current Project Health

Architecture

🟢 Stable

Backend

🟢 Production Ready

Desktop

🟢 Active Development

Dashboard

🟢 Shared Presentation Architecture Complete

Logging

🟢 Complete

Regression Testing

🟢 Passing

Technical Debt

🟢 Low

Documentation

🟢 Current

---

# Next Sprint Focus

Sprint 4.2 will continue building upon the completed Dashboard architecture.

The primary focus shifts from architectural migration to professional desktop functionality and reusable UI components while preserving Orion's deterministic architecture.