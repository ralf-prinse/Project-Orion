# ORION TODO

---

# Documentation Information

Documentation Version

v1.12

Architecture Version

v2.1

Current Sprint

🚧 Sprint 5.5 — Trade Lifecycle

Last Updated

2026-07-05

---

# Completed Foundation

## Backend

- [x] TradingPipeline
- [x] TechnicalScanner
- [x] MarketScanner
- [x] AnalysisEngine
- [x] RiskEngine
- [x] PositionSizingEngine
- [x] LiveScannerService
- [x] IndicatorBuilder
- [x] Yahoo Finance integration
- [x] FxRateService
- [x] TradingConfig
- [x] IndicatorConfig
- [x] PortfolioStore
- [x] OpportunityService
- [x] PositionSizingService
- [x] Trade domain model
- [x] OpenTradeStore
- [x] TradeHistoryStore
- [x] TradeLifecycleService
- [x] TradeMonitorService
- [x] PositionAnalysisService
- [x] PositionMonitorService
- [x] ExitEvaluationService
- [x] AI Context Builder
- [x] AI Explanation Engine

---

## Desktop Foundation

- [x] Workspace architecture
- [x] Presenter architecture
- [x] WorkspaceRenderer
- [x] GuiWorkspace
- [x] GuiWorkspacePanel
- [x] DashboardGrid
- [x] MissionControlWorkspace
- [x] MissionControlController
- [x] TradingWorkspace
- [x] TradingController
- [x] PortfolioWorkspace
- [x] PositionMonitorWorkspace
- [x] PositionMonitorController
- [x] PositionMonitorPresenter
- [x] TradeMonitorPresenter
- [x] ChartCanvas framework

---

## Mission Control

Completed

- [x] Scanner Status
- [x] Scan Duration
- [x] Market Data panel
- [x] Market Status
- [x] Universe Coverage
- [x] Top Opportunities
- [x] Opportunity Price
- [x] Live FX conversion
- [x] Position sizing presentation
- [x] Share quantity
- [x] Required EUR investment
- [x] USD buying power
- [x] Remaining capital
- [x] Budget validation
- [x] Automatic Refresh
- [x] Responsive Opportunity cards
- [x] Scrollable layout

---

## Portfolio

Completed

- [x] Portfolio redesign
- [x] Trading Capital configuration
- [x] Save workflow
- [x] PortfolioStore integration
- [x] Trading capital survives restart

---

## Trading Workspace

Completed

- [x] TradingPipeline integration
- [x] BUY / HOLD / SELL
- [x] Confidence
- [x] Pressure
- [x] Risk
- [x] Position Size
- [x] Human-readable explanations
- [x] AI Explanation
- [x] Open Trade button
- [x] Latest pipeline result caching

---

## Trade Monitor

Completed

- [x] Trade model
- [x] Manual trade input
- [x] Open Trades panel
- [x] OpenTradeStore
- [x] TradeLifecycleService
- [x] TradeMonitorService
- [x] PositionAnalysisService
- [x] PositionMonitorService
- [x] ExitEvaluationService
- [x] Exit Score
- [x] Trend Status
- [x] Momentum Status
- [x] Risk Status
- [x] Exit Reasons
- [x] Profit / Loss
- [x] Market Value
- [x] Shared AnalysisEngine
- [x] Exit Intelligence panel

---

## Validation

- [x] Application starts
- [x] Navigation works
- [x] Mission Control loads
- [x] Portfolio loads
- [x] Trading Workspace loads
- [x] Trade Monitor loads
- [x] Scan Market works
- [x] FX conversion works
- [x] TradingConfig works
- [x] OpenTradeStore works
- [x] TradeLifecycleService works
- [x] TradeMonitorService works
- [x] Exit Intelligence works
- [x] Opportunity cards validated
- [x] Manual GUI validation completed

Latest validation

✔ Regression tests pass

---

# Sprint 5.5 — Trade Lifecycle

## Highest Priority

### Open Trade Workflow

- [ ] Complete BUY → Open Trade workflow
- [ ] Save trade through TradeLifecycleService
- [ ] Persist trade in OpenTradeStore
- [ ] Auto refresh Trade Monitor
- [ ] Show newly created trade immediately

---

### Trade Monitor UX

- [ ] Replace legacy manual workflow
- [ ] Clickable Open Trades list
- [ ] Trade detail panel
- [ ] Live P/L display
- [ ] Days in trade
- [ ] Highest price
- [ ] Lowest price
- [ ] Current stop-loss
- [ ] Current take-profit
- [ ] Exit score visualization

---

### Trade Lifecycle

- [ ] Close Trade workflow
- [ ] Move closed trades into TradeHistoryStore
- [ ] Holding duration
- [ ] Trade state transitions
- [ ] Lifecycle timestamps

---

### Exit Intelligence

- [ ] Trailing Stop evaluation
- [ ] Time-based Exit evaluation
- [ ] Better Exit Score weighting
- [ ] Better Exit explanations
- [ ] Technical indicator explanations
- [ ] Market regime interpretation
- [ ] Volatility interpretation

---

### Mission Control

- [ ] Show active open trades
- [ ] Portfolio exposure
- [ ] Buying power
- [ ] Open risk
- [ ] Current portfolio P/L
- [ ] Watchlist integration

---

### Trading Workspace

- [ ] Finish Open Trade workflow
- [ ] Editable quantity dialog
- [ ] Editable entry price
- [ ] Editable stop-loss
- [ ] Editable take-profit
- [ ] Trade confirmation dialog

---

# Sprint 6.0 — Paper Trading

- [ ] Virtual Broker
- [ ] Order lifecycle
- [ ] Trade execution simulation
- [ ] Portfolio model
- [ ] Commission model
- [ ] Slippage model
- [ ] Performance statistics
- [ ] Trade journal
- [ ] Daily performance overview

---

# Future Development

## Mission Control

- [ ] Heatmaps
- [ ] Workspace layouts
- [ ] Multi-monitor support
- [ ] Watchlists
- [ ] Notifications
- [ ] Strategy comparison

---

## Market Intelligence

- [ ] Earnings Calendar
- [ ] FED Events
- [ ] CPI Events
- [ ] Macro Calendar
- [ ] News integration

---

## Artificial Intelligence

Explainability only

- [ ] Better trade explanations
- [ ] Daily Market Briefing
- [ ] Weekly Market Summary
- [ ] Trade summaries
- [ ] Portfolio summaries

AI will never generate deterministic trading decisions.

---

# Technical Debt

Current technical debt

- [ ] Finish Open Trade workflow
- [ ] Remove remaining legacy Position Monitor naming
- [ ] Replace manual Trade Monitor workflow
- [ ] Improve Open Trades presentation
- [ ] Trade detail screen
- [ ] Close Trade action
- [ ] Improve terminology
- [ ] Extend regression tests for lifecycle

Current architecture is otherwise considered clean.

---

# Documentation

Before every release

- [ ] Synchronize AI_CONTEXT.md
- [ ] Synchronize PROJECT_STATUS.md
- [ ] Synchronize CHANGELOG.md
- [ ] Synchronize TODO.md
- [ ] Synchronize PROJECT_VISION.md
- [ ] Synchronize TRADING_STRATEGY.md
- [ ] Synchronize ORION_MASTER_ARCHITECTURE.md

GitHub is the primary source of truth.

---

# Current Priority

1. Complete Open Trade workflow
2. Trade Monitor UX
3. Close Trade workflow
4. Trade History
5. Exit Intelligence improvements
6. Paper Trading
7. Broker compatibility layer

---

# Definition of Done

A task is complete only when

- [x] Feature implemented
- [x] Architecture respected
- [x] TradingPipeline remains the only BUY / HOLD / SELL decision engine
- [x] ExitEvaluationService remains the only deterministic exit decision engine
- [x] No business logic inside UI
- [x] Regression tests pass
- [x] Desktop launches
- [x] Manual GUI validation completed
- [x] Documentation synchronized
- [x] Git commit created
- [x] GitHub push completed

---

# End of TODO