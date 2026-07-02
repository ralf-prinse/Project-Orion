# ORION AI CONTEXT

---

# Current Phase

## Sprint 4.1 — Dashboard 2.0

Project Orion has completed its deterministic backend foundation.

The backend is now considered stable.

Current development is focused entirely on the professional desktop experience.

No new trading logic is currently being added.

Development focuses on presentation, visualization and workspace architecture while preserving the deterministic backend.

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

Dashboard 2.0 is now under active development.

Completed:

✅ DashboardGrid

✅ DashboardWorkspace

✅ DashboardData

✅ Dashboard2Presenter

✅ Portfolio Summary

✅ Cash Widget

✅ Equity Widget

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
DashboardWorkspace
```

---

# UI Architecture

The desktop UI now follows a presentation-driven architecture.

ApplicationController coordinates all communication.

Presenters transform deterministic backend output into presentation models.

Qt Widgets render presentation models only.

Business logic is prohibited inside widgets.

---

# Important Architectural Discovery

During Sprint 4.1 an existing reusable widget infrastructure was discovered.

Already present:

- GuiMetricCard
- MetricCard
- GuiWorkspace
- GuiChart

Temporary DashboardCard and DashboardCardModel were introduced during early Dashboard development.

These temporary components have now been removed.

Next sprint begins the migration toward the existing MetricCard architecture.

Target architecture:

```
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

This removes duplicate presentation components and standardizes dashboard rendering.

---

# Current Infrastructure

Completed

✅ TradingConfig

✅ LoggingService

✅ YahooProvider

✅ IndicatorBuilder

✅ TradingPipeline

✅ AIMarketScanner

✅ BacktestEngine

✅ ApplicationController

✅ Dashboard 2.0 Foundation

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

Current result throughout Sprint 4.1:

```
Passed: 6
Failed: 0
```

Regression tests are mandatory before every Git commit.

---

# Current Priority

Complete Dashboard 2.0 using the existing Orion presentation architecture.

Immediate objectives:

- migrate Dashboard to MetricCard
- remove remaining temporary dashboard presentation models
- introduce reusable dashboard widget library
- improve professional desktop experience
- preserve deterministic backend

No backend redesign is planned.

---

# Long-Term Vision

Project Orion will evolve into a professional deterministic AI-assisted trading platform featuring:

- Live Market Analysis
- Explainable AI
- Portfolio Intelligence
- Professional Dashboard
- Historical Backtesting
- Watchlists
- Paper Trading
- Broker Integration

while preserving deterministic calculations as the only source of trading decisions.