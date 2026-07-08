# PROJECT_STATUS.md

> Documentation Version: v1.17
> Architecture Version: v3.1
> Last Updated: 2026-07-08
> Active Branch: fix/trading-config-indicators
> Regression Status: 58 tests PASS

---

# PROJECT STATUS

Project Orion is now a deterministic, AI-assisted, typed, live paper-trading platform with autonomous finite-run orchestration, continuous paper-trading support, persistent portfolio/journal infrastructure, a self-evaluation layer, and a first controlled-learning foundation.

The system can:

* scan a live market universe
* load symbols through `WatchlistService`
* fetch real market data through Yahoo Finance
* build indicators
* produce deterministic typed trading decisions
* rank candidates
* allocate paper capital with risk-based portfolio limits
* execute approved paper trades
* preserve a TradingSession across multiple cycles
* persist paper portfolio state across restarts
* persist trade journal entries through JSONL
* run repeated autonomous paper-trading iterations until stopped
* build trade journal entries
* analyze its own performance
* produce strategy recommendations
* evaluate deterministic hypotheses
* build deterministic learning ideas

The system does **not** use real money.

The system does **not** automatically modify strategy configuration.

The system does **not** connect to a real broker.

---

# CURRENT PHASE

Current phase:

```text
Sprint 8.3 — Long-running paper trading preparation / scalable scanning foundation

IMPLEMENTED AND PUSHED

Project Health:
EXCELLENT

Regression Tests:
58 PASS
0 FAIL
```

Current priority:

```text
Prepare ORION for weeks-long paper-trading validation with larger watchlists, persistent state, scheduler support, and provider hardening.
```

---

# COMPLETED SPRINTS / MILESTONES

## Sprint 6E — TradingPipelineResult Integration

Status: Complete.

Delivered:

* TradingPipelineResult
* typed pipeline output
* typed paper-trading flow
* compatibility bridge during migration
* regression coverage

Purpose:

Replace anonymous pipeline dictionaries with a typed immutable result model.

---

## Sprint 6F — Remove Legacy Pipeline Interface

Status: Complete.

Delivered:

* removal of pipeline_output
* removal of legacy_output
* removal of dict compatibility
* removal of result["pipeline"]
* typed-only downstream pipeline integration

Current rule:

```text
TradingPipelineResult is the only valid pipeline contract.
```

---

## Sprint 7A — Deterministic Paper Trading Demo Runner

Status: Complete.

Delivered:

* PaperTradingDemoResult
* PaperTradingDemoRunner
* run_paper_trading_demo.py
* regression test

Purpose:

Prove end-to-end paper trading with deterministic synthetic data.

Command:

```text
python run_paper_trading_demo.py
```

Validated:

* synthetic demo flow works
* TradingPipeline produces typed output
* TradingCycle opens/updates paper positions
* cash/equity updates correctly

---

## Sprint 7B — Live Paper Market Scanner

Status: Complete.

Delivered:

* LivePaperTradingConfig
* LivePaperCandidate
* LivePaperTradingResult
* LivePaperMarketScanner
* run_live_paper_trading.py
* regression test

Purpose:

Use real Yahoo Finance market data and the configured watchlist/universe to produce ranked paper-trading candidates.

Command:

```text
python run_live_paper_trading.py
```

Validated:

* live scanner can scan real Yahoo data
* candidates are ranked
* rejected candidates include reasons
* scanner does not execute trades

---

## Sprint 7C — Autonomous Paper Trading Orchestration

Status: Complete.

Delivered:

* PortfolioAllocationDecision
* PortfolioAllocationResult
* PortfolioAllocator
* AutonomousPaperTradingConfig
* AutonomousPaperTradingCycleResult
* AutonomousPaperTradingResult
* AutonomousPaperTradingRunner
* run_autonomous_paper_trading.py
* regression tests

Purpose:

Separate scanning, allocation and execution into clean layers.

Current responsibility split:

```text
LivePaperMarketScanner = scan and rank
PortfolioAllocator = allocate paper capital
AutonomousPaperTradingRunner = orchestrate cycles and execute approved trades
```

Command:

```text
python run_autonomous_paper_trading.py
```

Validated:

* autonomous paper trading works
* completed cycles tracked
* failed cycles tracked
* executed trades tracked
* rejected trades tracked
* failed symbols tracked
* open positions maintained

---

## Sprint 7D — Self-Evaluation Layer

Status: Complete.

Delivered:

* TradeJournalEntry
* PerformanceAnalysisResult
* StrategyRecommendation
* StrategyRecommendationResult
* TradeJournalBuilder
* PerformanceAnalyzer
* StrategyRecommendationEngine
* regression tests

Purpose:

Allow ORION to evaluate its own paper-trading behaviour and produce recommendations.

Current rule:

```text
Recommendations are informational only.
No automatic config mutation.
```

---

## Sprint 7E — Controlled Learning / Hypothesis Evaluation

Status: Complete.

Delivered:

* StrategyHypothesis
* HypothesisEvaluationContext
* HypothesisEvaluation
* HypothesisEvaluationReport
* HypothesisContextBuilder
* HypothesisEvaluator
* HypothesisEvaluationService
* HypothesisReportBuilder
* StrategyRecommendationEngine integration
* regression tests

Purpose:

Evaluate deterministic strategy hypotheses against performance metrics without modifying production strategy configuration.

Current flow:

```text
PerformanceAnalysisResult
        ↓
HypothesisContextBuilder
        ↓
HypothesisEvaluationContext
        ↓
HypothesisEvaluator
        ↓
HypothesisEvaluation
        ↓
HypothesisReportBuilder
        ↓
HypothesisEvaluationReport
        ↓
StrategyRecommendationEngine
```

Current rule:

```text
Hypothesis evaluation is informational only.
No automatic strategy mutation.
```

---

## Sprint 7F — Deterministic Learning Pipeline

Status: Complete.

Delivered:

* StrategyIdea
* StrategyIdeaBuilder
* LearningPipelineResult
* LearningPipeline
* regression tests

Purpose:

Create the first vertical slice of the Learning Domain.

Current flow:

```text
PerformanceAnalysisResult
        ↓
StrategyRecommendationEngine
        ↓
StrategyRecommendationResult
        ↓
StrategyIdeaBuilder
        ↓
StrategyIdea[]
        ↓
LearningPipelineResult
```

Current rule:

```text
StrategyIdea captures intent only.
It does not propose concrete parameter values.
```

---

## Sprint 8.1 — Persistent Paper Portfolio Infrastructure

Status: Complete.

Delivered:

* DataclassSerializer
* PaperPortfolioRepository
* JsonPaperPortfolioRepository
* TradeJournalRepository
* JsonlTradeJournalRepository
* PaperTradingService repository awareness
* AutonomousPaperTradingRunner portfolio load/save support
* regression tests

Purpose:

Allow ORION to persist state across application restarts.

Current persistence flow:

```text
PaperPortfolio
        ↓
PaperPortfolioRepository
        ↓
JsonPaperPortfolioRepository
        ↓
data/paper_portfolio.json
```

```text
TradeJournalEntry
        ↓
TradeJournalRepository
        ↓
JsonlTradeJournalRepository
        ↓
data/trade_journal.jsonl
```

Current rule:

```text
Trading services depend on repository interfaces, not file formats.
```

---

## Sprint 8.2 — Continuous Paper Trading Runner

Status: Complete.

Delivered:

* ContinuousRunnerConfig
* ContinuousPaperTradingRunResult
* ContinuousPaperTradingRunner
* run_continuous_paper_trading.py
* regression tests

Purpose:

Allow ORION to repeatedly run finite autonomous paper-trading iterations until stopped.

Current flow:

```text
ContinuousPaperTradingRunner
        ↓
AutonomousPaperTradingRunner
        ↓
LivePaperMarketScanner
        ↓
PortfolioAllocator
        ↓
TradingCycle
```

Command:

```text
python run_continuous_paper_trading.py
```

Current behaviour:

* runs until Ctrl+C
* supports finite `max_iterations` for tests
* sleeps between iterations
* prints iteration summaries
* reuses AutonomousPaperTradingRunner
* avoids duplicate trading logic

Current limitation:

```text
Interval-based sleep exists.
Wall-clock aligned scheduler / market-hours awareness is not implemented yet.
```

---

## Sprint 8.3 — Risk-Based Allocation + WatchlistService Scanner Routing

Status: Partially complete.

Delivered:

* `LivePaperTradingConfig.max_symbols` increased for larger scans
* `LivePaperTradingConfig.max_open_positions` raised as a legacy safety cap
* `max_position_size_pct`
* `max_portfolio_exposure`
* `min_cash_reserve_pct`
* PortfolioAllocator updated to use risk-based allocation limits
* LivePaperMarketScanner now uses WatchlistService
* duplicate scanner symbol-loading logic removed
* regression tests remain green

Purpose:

Prepare ORION for larger watchlists and more realistic portfolio scaling.

Current allocation direction:

```text
Use risk-based exposure/cash/position limits instead of relying on a tiny fixed max-open-position value.
```

Current symbol-loading rule:

```text
WatchlistService is the only source for symbol loading.
```

---

# COMPLETED MAJOR SYSTEMS

## Trading Core

Status: Complete.

Includes:

* TradingPipeline
* TradingPipelineResult
* AdaptiveDecisionEngine
* MarketScanner
* AI MarketScanner
* AI Scanner Presenter
* SignalFusionEngine
* MarketIntelligenceEngine
* AIContextBuilder
* AIExplainer

Capabilities:

* deterministic BUY / HOLD / SELL decisions
* confidence scoring
* market intelligence analysis
* AI context generation
* explanation generation

---

## Indicator / Market Data Integration

Status: Operational.

Includes:

* IndicatorBuilder
* PaperTradingPipelineAdapter
* YahooProvider
* BaseMarketProvider

Capabilities:

* build IndicatorPack from historical OHLCV data
* fetch historical candles from Yahoo Finance
* fetch current market data from Yahoo Finance

Current review target:

* YahooProvider retry handling
* timeout handling
* caching
* batching
* large watchlist reliability

---

## Watchlist / Universe Loading

Status: Operational.

Main service:

```text
services/watchlist_service.py
```

Default file:

```text
data/universes/swing.csv
```

Current behaviour:

* reads symbols from universe file
* ignores empty lines
* ignores comment lines
* uppercases symbols
* deduplicates symbols
* returns sorted symbols

Current rule:

```text
Do not duplicate watchlist/universe-loading logic.
LivePaperMarketScanner must use WatchlistService.
```

---

## Risk Engine

Status: Complete.

Includes:

* MarketStructure
* RiskContext
* RiskContextBuilder
* AdaptiveRiskEngine
* ATR stop logic
* RiskPlan
* RiskPlanValidator

Capabilities:

* build deterministic RiskPlan
* calculate stop loss
* calculate targets
* validate risk plan

---

## Position Management

Status: Complete.

Includes:

* PositionState
* PositionStateFactory
* PositionUpdateEngine
* PositionManager
* BreakEvenService
* TrailingStopService
* TimeStopService
* PositionHealthService
* PositionStateStore
* PositionManagementSummary
* PositionManagementSummaryBuilder

Capabilities:

* update position state
* apply break-even logic
* apply trailing stop logic
* apply time stop logic
* summarize position management state

---

## Execution Layer

Status: Complete.

Includes:

* ExecutionRequest
* ExecutionContext
* Order
* ExecutionResult
* ExecutionValidator
* OrderFactory
* ExecutionEngine
* PaperBroker
* ExecutionReportBuilder

Capabilities:

* validate paper execution request
* reject invalid or unaffordable orders
* create broker-neutral order
* execute order through PaperBroker
* update PaperPortfolio
* build execution report

---

## Paper Trading Foundation

Status: Complete.

Includes:

* PaperPortfolio
* PaperPosition
* TradingSession
* PaperTradingService
* PaperPositionUpdateService
* PaperPositionCloseService
* TradingCycle
* PaperTradingRunner
* PaperTradingRunResult

Capabilities:

* open paper positions
* update paper positions
* close paper positions
* maintain cash
* maintain equity
* maintain open positions
* run multiple deterministic cycles
* persist portfolio when repository is injected

---

## Live Paper Trading

Status: Operational.

Includes:

* LivePaperTradingConfig
* LivePaperCandidate
* LivePaperTradingResult
* LivePaperMarketScanner
* run_live_paper_trading.py

Current capabilities:

* load symbols through WatchlistService
* scan configurable number of symbols
* fetch live/historical market data through Yahoo Finance
* produce ranked candidates
* do not execute trades inside scanner

---

## Portfolio Allocation

Status: Operational.

Includes:

* PortfolioAllocationDecision
* PortfolioAllocationResult
* PortfolioAllocator

Current capabilities:

* sort candidates by score
* reject non-accepted candidates
* reject already-open positions
* enforce available cash
* enforce max position value
* enforce max position size percentage
* enforce max portfolio exposure
* enforce minimum cash reserve
* retain max open positions as a legacy safety cap
* calculate integer quantity
* return approved and rejected allocation decisions

---

## Autonomous Paper Trading

Status: Operational.

Includes:

* AutonomousPaperTradingConfig
* AutonomousPaperTradingCycleResult
* AutonomousPaperTradingResult
* AutonomousPaperTradingRunner
* run_autonomous_paper_trading.py

Current capabilities:

* preserve one TradingSession across multiple cycles
* call scanner
* call allocator
* execute approved allocations through TradingCycle
* summarize completed cycles, failed cycles, executed trades, rejected trades and failed symbols
* load existing paper portfolio when repository is provided
* save paper portfolio after cycles when repository is provided

Current limitation:

```text
The runner is finite-run only.
This is intentional.
```

---

## Continuous Paper Trading

Status: Operational.

Includes:

* ContinuousRunnerConfig
* ContinuousPaperTradingRunResult
* ContinuousPaperTradingRunner
* run_continuous_paper_trading.py

Current capabilities:

* repeatedly call AutonomousPaperTradingRunner
* run until Ctrl+C
* support max_iterations for tests
* track failed iterations
* print iteration summary
* support persistent portfolio through injected repository on the underlying autonomous runner

Current limitation:

```text
Uses interval sleep.
Does not yet align scans to exact clock times.
Does not yet know market hours.
```

---

## Persistence

Status: Operational foundation.

Includes:

* DataclassSerializer
* PaperPortfolioRepository
* JsonPaperPortfolioRepository
* TradeJournalRepository
* JsonlTradeJournalRepository

Current capabilities:

* serialize dataclasses
* restore nested dataclasses
* persist PaperPortfolio as JSON
* append TradeJournalEntry records as JSONL
* load persisted journal entries
* delete test persistence files

Current limitation:

```text
No daily report store yet.
No equity curve store yet.
No SQLite/PostgreSQL implementation yet.
```

---

## Self-Evaluation Layer

Status: Operational.

Includes:

* TradeJournalEntry
* TradeJournalBuilder
* PerformanceAnalysisResult
* PerformanceAnalyzer
* StrategyRecommendation
* StrategyRecommendationResult
* StrategyRecommendationEngine

Current capabilities:

* convert autonomous paper trading results into journal entries
* calculate performance summary
* calculate win rate
* calculate realized and unrealized P/L
* calculate average confidence and risk
* detect dominant market regime and volatility
* generate strategy recommendations

Current limitation:

```text
No automatic strategy mutation.
```

---

## Controlled Learning Foundation

Status: Operational.

Includes:

* StrategyHypothesis
* HypothesisEvaluationContext
* HypothesisEvaluation
* HypothesisEvaluationReport
* HypothesisContextBuilder
* HypothesisEvaluator
* HypothesisEvaluationService
* HypothesisReportBuilder
* StrategyRecommendationEngine hypothesis integration

Current capabilities:

* evaluate hypothesis support/rejection
* detect insufficient data
* produce immutable hypothesis report
* feed hypothesis findings into recommendations

Current limitation:

```text
No automatic strategy tuning.
No replay comparison yet.
```

---

## Learning Pipeline

Status: Operational.

Includes:

* StrategyIdea
* StrategyIdeaBuilder
* LearningPipelineResult
* LearningPipeline

Current capabilities:

* convert performance analysis into recommendations
* convert recommendations into strategy ideas
* preserve recommendation intent
* avoid concrete parameter mutation

Current limitation:

```text
No ProposalGenerator yet.
No StrategyComparisonEngine yet.
No ReplayEngine yet.
```

---

# CURRENT CAPABILITY

ORION can now:

* scan real market data
* process configured symbol universes through WatchlistService
* build indicators
* produce typed pipeline results
* rank trading candidates
* allocate paper capital using risk-based constraints
* execute paper trades
* maintain portfolio cash and equity
* preserve one session across multiple cycles
* persist paper portfolio across restarts
* append trade journal records
* run repeated autonomous iterations through the continuous runner
* build journal entries
* analyze journal entries
* produce strategy recommendations
* evaluate hypotheses
* produce learning ideas

---

# CURRENT LIMITATIONS

The following limitations remain:

* No market-hours scheduler.
* No exact wall-clock aligned scan schedule.
* No batching/caching/retry hardening for YahooProvider.
* No parallel scanner yet.
* No scan-duration metrics yet.
* No daily report.
* No equity curve store.
* No completed ProposalGenerator.
* No controlled replay comparison.
* No real broker integration.
* No automatic strategy tuning.
* LivePaperTradingResult still contains execution counters even though the scanner no longer executes trades; this should be reviewed.
* Position lifecycle close logic during long-running live paper sessions needs further validation.

---

# TECHNICAL DEBT TO REVIEW

The next sprint/session should explicitly review:

* scanner / allocator / runner boundaries after continuous runner
* whether execution counters belong in LivePaperTradingResult
* whether TradeJournalBuilder should use execution results instead of allocation decisions only
* whether current unrealized P/L calculation is sufficient
* whether PaperPosition current prices are refreshed correctly across cycles
* whether AutonomousPaperTradingRunner should produce richer per-cycle execution details
* whether JsonlTradeJournalRepository should be integrated directly into autonomous/continuous runs
* whether YahooProvider requires retry, caching or batching before 250+ symbol scanning
* whether continuous runner needs exact wall-clock scheduling
* whether market-hours awareness is needed before multi-week runs
* whether context/result patterns remain consistent after persistence and learning additions

---

# NEXT STEP

Recommended next sprint:

```text
Sprint 8.3 continued — Large Universe / Scalable Scanner Hardening
```

Primary goals:

* confirm `data/universes/swing.csv` exists and contains the intended symbol universe
* profile scan duration with larger `max_symbols`
* add scan timing metrics
* harden YahooProvider with retry/timeout handling
* add failure reporting suitable for large scans
* consider bounded parallel scanning only after sequential baseline profiling
* keep WatchlistService as the only symbol-loading source

Do not start real broker integration.

Do not enable automatic configuration mutation.

Do not duplicate watchlist/universe-loading logic.

END OF FILE
