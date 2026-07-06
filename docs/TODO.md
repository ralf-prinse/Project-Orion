# ORION TODO

---

# Documentation Information

Documentation Version

v1.13

Architecture Version

v2.2

Status

🟢 Active Development

Current Sprint

🚧 Sprint 5.9 — Intelligent Risk Management

Last Updated

2026-07-06

---

# Completed Foundation

## Backend

- [x] YahooProvider
- [x] IndicatorBuilder
- [x] AnalysisEngine
- [x] TechnicalScanner
- [x] MarketScanner
- [x] TradingPipeline
- [x] SignalFusionEngine
- [x] MarketIntelligenceEngine
- [x] AdaptiveDecisionEngine
- [x] AdaptiveRiskEngine
- [x] PositionSizer
- [x] OpportunityService
- [x] PortfolioStore
- [x] OpenTradeStore
- [x] TradeHistoryStore
- [x] TradeLifecycleService
- [x] TradeMonitorService
- [x] PositionAnalysisService
- [x] ExitEvaluationService
- [x] AIContextBuilder
- [x] AIExplainer
- [x] TradingConfig
- [x] IndicatorConfig
- [x] FxRateService

---

## Desktop Foundation

- [x] Workspace architecture
- [x] Presenter architecture
- [x] Controller architecture
- [x] Mission Control
- [x] Trading Workspace
- [x] Trade Monitor
- [x] Portfolio
- [x] Performance
- [x] History
- [x] Settings
- [x] Stable navigation
- [x] Automatic refresh
- [x] Responsive layouts

---

## Mission Control

Completed

- [x] Scan Market
- [x] Market Status
- [x] Universe Coverage
- [x] Scan Duration
- [x] Top 10 Opportunities
- [x] Opportunity Ranking
- [x] Current Price
- [x] BUY / HOLD / SELL
- [x] Confidence
- [x] Position Size
- [x] Required Investment
- [x] Remaining Capital
- [x] Buying Power
- [x] Live FX conversion
- [x] Expanded Watchlist
- [x] Personal Universe V1
- [x] Automatic refresh

---

## Trading Workspace

Completed

- [x] TradingPipeline integration
- [x] BUY / HOLD / SELL
- [x] Confidence
- [x] Pressure Score
- [x] Risk Score
- [x] Position Size
- [x] AI Explanation
- [x] Pipeline caching
- [x] Open Trade workflow
- [x] Adaptive Risk Engine integration
- [x] Dynamic RiskPlan generation

---

## Trade Monitor

Completed

- [x] Open Trades
- [x] Live Current Price
- [x] Live Unrealized Profit/Loss
- [x] Live Position Value
- [x] Stop Loss
- [x] Take Profit
- [x] Exit Score
- [x] Trend Status
- [x] Momentum Status
- [x] Risk Status
- [x] Exit Reasons
- [x] Close Trade
- [x] Automatic refresh
- [x] Trade lifecycle synchronization
- [x] TradeHistory integration

---

## Portfolio

Completed

- [x] Trading Capital
- [x] Portfolio persistence
- [x] FX-aware buying power
- [x] Position sizing context
- [x] Restart persistence

---

## Validation

Completed

- [x] Application starts
- [x] Navigation works
- [x] Mission Control loads
- [x] Trading Workspace loads
- [x] Trade Monitor loads
- [x] Portfolio loads
- [x] History loads
- [x] Settings loads
- [x] Scan Market works
- [x] Open Trade works
- [x] Close Trade works
- [x] Live P/L updates
- [x] Automatic refresh works
- [x] Adaptive Risk Engine works
- [x] Dynamic RiskPlan generation
- [x] Regression tests pass
- [x] Manual GUI validation completed

---

# Sprint 5.9 — Intelligent Risk Management

## Highest Priority

### RiskPlan Presentation

- [ ] Display RiskPlan in Trade Monitor
- [ ] Display Risk %
- [ ] Display Reward %
- [ ] Display Risk / Reward ratio
- [ ] Display Target 1
- [ ] Display Target 2
- [ ] Display Target 3
- [ ] Display Adaptive Risk Notes

---

### Adaptive Risk Engine V2

- [ ] ATR-aware stop-loss
- [ ] Volatility multiplier
- [ ] Dynamic support/resistance stops
- [ ] Strong trend target expansion
- [ ] Weak trend target reduction
- [ ] Confidence-weighted targets
- [ ] Portfolio-aware risk adjustment

---

### Trade Monitor UX

- [ ] Better trade cards
- [ ] RiskPlan panel
- [ ] Better color coding
- [ ] Profit target progress
- [ ] Stop-loss visualization
- [ ] Risk visualization
- [ ] Better opportunity icons

---

### Lifecycle Intelligence

- [ ] Trailing stop
- [ ] Break-even stop
- [ ] Partial profit taking
- [ ] Dynamic stop updates
- [ ] Holding period analysis
- [ ] Maximum favorable excursion
- [ ] Maximum adverse excursion

---

### Mission Control

- [ ] Portfolio exposure
- [ ] Portfolio heatmap
- [ ] Open risk overview
- [ ] Sector diversification
- [ ] Portfolio allocation
- [ ] Open trade overview

---

### Trading Workspace

- [ ] RiskPlan preview before opening trade
- [ ] Risk visualization
- [ ] Position preview improvements
- [ ] Better explanation layout

---

# Sprint 6.0 — Paper Trading

- [ ] Virtual Broker
- [ ] Order lifecycle
- [ ] Simulated fills
- [ ] Commission model
- [ ] Slippage model
- [ ] Equity curve
- [ ] Daily statistics
- [ ] Trade Journal
- [ ] Portfolio performance
- [ ] Win/Loss statistics

---

# Future Development

## Artificial Intelligence

AI remains explainability only.

Future AI features

- [ ] Daily Market Briefing
- [ ] Weekly Market Summary
- [ ] Portfolio Summary
- [ ] Trade Summary
- [ ] Opportunity Comparison
- [ ] Market Narrative

AI will never generate deterministic BUY, SELL or EXIT decisions.

---

## Market Expansion

- [ ] London Stock Exchange
- [ ] SIX Swiss Exchange
- [ ] Toronto Stock Exchange
- [ ] Nordic Markets

---

## Portfolio Intelligence

- [ ] Portfolio Risk Dashboard
- [ ] Sector Exposure
- [ ] Correlation Analysis
- [ ] Drawdown Analysis
- [ ] Allocation Optimizer

---

## Broker Compatibility

- [ ] Portfolio import
- [ ] Portfolio synchronization
- [ ] CSV import/export
- [ ] Assisted order preparation

Broker execution will remain outside Orion.

---