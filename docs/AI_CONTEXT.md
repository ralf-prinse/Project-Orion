# ORION AI CONTEXT

---

# Current Phase

## Sprint 3.13 — Stabilization

Project Orion has transitioned from a prototype into a deterministic AI-assisted desktop trading platform.

The backend architecture is considered stable.

Current development focuses on:

- architecture stabilization
- configuration centralization
- UI integration
- test coverage
- documentation
- production readiness

No new backend engines should be introduced before Sprint 4.0.

---

# Core Trading Flow

```
Yahoo Finance
        ↓
IndicatorBuilder
        ↓
IndicatorPack
        ↓
Trading Pipeline
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
```

Every calculation remains deterministic.

Artificial Intelligence never changes investment decisions.

---

# Desktop Flow

```
MainWindow
        ↓
ApplicationController
        ↓
Trading Workspace

or

Dashboard

or

Scanner
        ↓
Presenters
        ↓
Qt Widgets
```

ApplicationController is now the central UI orchestrator.

---

# Market Scanner

The legacy scanner has been superseded by the AI Market Scanner.

Current flow:

```
Yahoo Finance
        ↓
IndicatorBuilder
        ↓
Trading Pipeline
        ↓
AIMarketScanner
        ↓
AIScannerPresenter
        ↓
Scanner Workspace
```

Trading and Scanner now share the exact same AI pipeline.

There is only one source of truth.

---

# Current Components

Completed

✅ IndicatorBuilder

✅ TradingPipeline

✅ TradingWorkspace

✅ TradingWorkspacePresenter

✅ AIMarketScanner

✅ AIScannerPresenter

✅ TradingConfig

✅ ApplicationController

✅ Live Yahoo integration

✅ Dashboard integration

✅ Scanner integration

✅ Backtesting

---

# Current Priority

Sprint 3.13 Stabilization

Objectives

- Central configuration
- Logging
- Increased test coverage
- Documentation
- Production cleanup

No architectural redesigns are planned.

---

# Sprint 4.0 Preview

Planned

- Live dashboard
- Watchlists
- Auto refresh
- Equity visualization
- Portfolio intelligence
- Broker integration preparation

Backend architecture remains unchanged.