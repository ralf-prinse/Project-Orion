# ORION TODO

---

# Documentation Information

Documentation Version

v1.11

Architecture Version

v2.0

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
- [x] PortfolioStore
- [x] OpportunityService
- [x] PositionSizingService
- [x] Trade domain model
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
- [x] Position sizing presentation
- [x] Share quantity
- [x] Required investment
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

---

## Position Monitor

Completed

- [x] Trade model
- [x] Manual trade input
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
- [x] Position Monitor loads
- [x] Scan Market works
- [x] Exit Intelligence works
- [x] Opportunity cards validated
- [x] Manual GUI validation completed

Latest validation

✔ 6 passed

---

# Sprint 5.5 — Trade Lifecycle

Current Sprint

## Trade Monitor

- [ ] Rename Position Monitor conceptually to Trade Monitor
- [ ] Improve information hierarchy
- [ ] Improve trade summary presentation
- [ ] Improve Exit Intelligence presentation
- [ ] Show trade health more visually
- [ ] Improve professional desktop UX

---

## Trade Lifecycle

- [ ] Introduce Open Trade workflow
- [ ] Create trade directly from Trading Workspace
- [ ] Create trade directly from Mission Control
- [ ] Connect Position Monitor to persisted trades
- [ ] Show current open trades
- [ ] Prepare Trade History architecture

---

## Exit Intelligence

- [ ] Add Trailing Stop evaluation
- [ ] Add Time-based Exit evaluation
- [ ] Improve Exit Score weighting
- [ ] Improve Exit explanations
- [ ] Add technical indicator explanations
- [ ] Add market regime influence
- [ ] Add volatility interpretation

---

## Mission Control

- [ ] Show open positions
- [ ] Show portfolio exposure
- [ ] Show available buying power
- [ ] Show active trades
- [ ] Show watchlist integration

---

## Trading Workspace

- [ ] One-click trade creation
- [ ] Display expected lifecycle
- [ ] Improve trade checklist
- [ ] Improve AI explanation readability

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

- [ ] Rename Position Monitor to Trade Monitor throughout the application.
- [ ] Introduce persistent TradeStore.
- [ ] Connect Trade creation to Trading Workspace.
- [ ] Connect Trade creation to Mission Control.
- [ ] Remove remaining placeholder texts in Exit Intelligence.
- [ ] Improve professional terminology throughout the desktop.
- [ ] Extend automated regression tests for Trade Lifecycle.

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

1. Trade Lifecycle
2. Trade Monitor
3. Open Trade persistence
4. Trade History
5. Exit Intelligence improvements
6. Paper Trading

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