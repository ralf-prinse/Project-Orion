# AI_CONTEXT.md

> Documentation Version: v1.17
> Architecture Version: v3.1
> Last Updated: 2026-07-08
> Active Branch: fix/trading-config-indicators
> Regression Status: 58 tests PASS

---

# PROJECT ORION

## Mission

Project Orion is a deterministic, modular, AI-assisted swing trading and paper-trading platform.

The long-term objective is to operate first as a long-running autonomous paper-trading system that can monitor a broad market universe over days or weeks. Only after the paper-trading strategy proves stable and measurable should real broker integration be considered.

Project Orion must remain:

* deterministic
* explainable
* testable
* broker-independent
* modular
* paper-first
* AI-assisted, never AI-controlled

AI may help explain, summarize, evaluate and recommend, but AI must never make undocumented or non-deterministic trading decisions.

---

# SOURCE OF TRUTH

The repository is the primary source of truth.

Documentation supports the code, but if documentation and code disagree, the code wins.

Before any new sprint, architecture proposal, code change or refactor:

1. Analyse the full repository.
2. Work only from the current branch: `fix/trading-config-indicators`.
3. Verify current branch, commits, structure, models, services, tests and docs.
4. Do not assume older sprint plans are still correct.
5. Determine the next step objectively from the actual repository.

---

# ARCHITECTURE PRINCIPLES

Project Orion follows strict deterministic architecture rules.

Every orchestrator should move toward this pattern:

```text
One Context or State input
        ↓
One orchestrator / service
        ↓
One immutable Result output
```

Existing examples:

```text
RiskContext
        ↓
AdaptiveRiskEngine
        ↓
RiskPlan

ExecutionContext
        ↓
ExecutionEngine
        ↓
ExecutionEngineResult

TradingPipeline
        ↓
TradingPipelineResult

MarketSnapshot
        ↓
TradingCycle
        ↓
TradingCycleResult

AutonomousPaperTradingRunner
        ↓
AutonomousPaperTradingResult

LearningPipeline
        ↓
LearningPipelineResult

ContinuousPaperTradingRunner
        ↓
ContinuousPaperTradingRunResult
```

Business logic belongs in services.

Models must remain lightweight data contracts.

No duplicated business logic.

No circular dependencies.

No uncontrolled AI behaviour.

Regression tests are mandatory after every logical step.

---

# CURRENT SYSTEM STATUS

## Regression

Current full regression suite:

```text
58 tests PASS
0 tests FAIL
```

Project health:

```text
ORION HEALTH: EXCELLENT
```

---

# COMPLETED SUBSYSTEMS

## Market Analysis

Status: Complete.

Contains:

* MarketScanner
* AI MarketScanner
* AI Scanner Presenter
* SignalFusionEngine
* MarketIntelligenceEngine
* IndicatorBuilder
* TradingPipeline
* TradingPipelineResult

Produces:

* deterministic trading decisions
* confidence
* position sizing
* risk plan
* AI context
* AI explanation

Important architectural note:

`TradingPipelineResult` is now the typed contract between the TradingPipeline and downstream layers.

Legacy dictionary compatibility has been removed.

Forbidden legacy patterns:

* `pipeline_output`
* `legacy_output`
* `result["pipeline"]`
* `.items()` compatibility
* `.keys()` compatibility
* `.values()` compatibility

---

## Trading Pipeline Integration

Status: Complete.

The pipeline now feeds typed downstream paper-trading flow.

Current typed route:

```text
Market History
        ↓
IndicatorBuilder
        ↓
TradingPipeline
        ↓
TradingPipelineResult
        ↓
MarketSnapshot
        ↓
TradingCycle
        ↓
PaperTradingService
        ↓
ExecutionRequestBuilder
        ↓
ExecutionEngine
```

The old anonymous dictionary contract is removed.

---

## Risk Engine

Status: Complete.

Contains:

* RiskContext
* RiskContextBuilder
* AdaptiveRiskEngine
* ATR-based risk planning
* RiskPlan
* RiskPlanValidator

Produces:

* deterministic RiskPlan
* stop loss
* targets
* risk percent
* reward percent
* risk/reward ratio
* confidence
* notes

---

## Execution Layer

Status: Complete.

Contains:

* ExecutionRequest
* ExecutionContext
* ExecutionValidator
* OrderFactory
* ExecutionEngine
* PaperBroker
* ExecutionReportBuilder

Produces:

* ExecutionEngineResult
* deterministic validation
* deterministic order creation
* paper broker execution
* updated paper portfolio snapshot

Important behaviour:

Execution validation rejects invalid orders, including:

* missing symbol
* non-positive entry price
* non-positive quantity
* non-positive confidence
* insufficient cash
* excessive position allocation

---

## Paper Trading Foundation

Status: Complete.

Contains:

* PaperPortfolio
* PaperPosition
* TradingSession
* PaperTradingService
* PaperPositionUpdateService
* PaperPositionCloseService
* PaperTradingRunner
* PaperTradingRunResult

Supports:

* paper BUY/open position
* paper position update
* paper close
* multi-cycle deterministic replay
* session-level cash/equity/open-position tracking

PaperTradingService is now repository-aware and can persist portfolio state through a `PaperPortfolioRepository`.

---

## Position Management

Status: Complete.

Contains:

* PositionManager
* PositionUpdateEngine
* BreakEvenService
* TrailingStopService
* TimeStopService
* PositionState
* PositionStateFactory
* PositionStateStore
* PositionManagementSummary
* PositionManagementSummaryBuilder

Supports:

* break-even management
* trailing stop management
* time stop management
* position state updates
* position health summaries

---

## Live Market Data

Status: Available.

Current provider:

* YahooProvider
* BaseMarketProvider

Supports:

* current market data
* historical OHLCV data
* configurable period and interval

Important file:

```text
providers/yahoo_provider.py
```

Current live data dependency:

```text
yfinance
```

Current review target:

YahooProvider still needs hardening for:

* retry handling
* timeout handling
* caching
* batching
* rate-limit resilience
* large watchlist scans

---

## Watchlist / Universe Loading

Status: Operational.

Current source of truth for symbol loading:

```text
services/watchlist_service.py
```

Default universe file:

```text
data/universes/swing.csv
```

WatchlistService:

* loads symbols from the configured universe file
* ignores blank lines
* ignores comment lines starting with `#`
* uppercases symbols
* deduplicates symbols
* returns sorted symbols

Important rule:

Do not create duplicate watchlist/universe-loading logic.

`LivePaperMarketScanner` now routes symbol loading through `WatchlistService`.

---

## Paper Trading Demo Runner

Status: Complete.

Contains:

* PaperTradingDemoResult
* PaperTradingDemoRunner
* run_paper_trading_demo.py

Purpose:

* deterministic end-to-end paper trading demo
* synthetic market history
* no external API dependency
* proves architecture works without live data

Command:

```text
python run_paper_trading_demo.py
```

Validated behaviour:

* IndicatorBuilder works
* TradingPipeline produces typed BUY result
* PaperTradingService opens paper positions
* TradingCycle updates positions across cycles
* portfolio cash/equity updates correctly

---

## Live Paper Market Scanner

Status: Complete.

Contains:

* LivePaperTradingConfig
* LivePaperCandidate
* LivePaperTradingResult
* LivePaperMarketScanner
* run_live_paper_trading.py

Current responsibility:

```text
WatchlistService
        ↓
YahooProvider
        ↓
PaperTradingPipelineAdapter
        ↓
LivePaperMarketScanner
        ↓
LivePaperCandidate[]
        ↓
LivePaperTradingResult
```

Important architectural rule:

`LivePaperMarketScanner` scans only.

It must not:

* allocate portfolio capital
* execute trades
* mutate TradingSession
* place real broker orders
* duplicate watchlist loading logic

Validated live scanner behaviour:

* real Yahoo data can be fetched
* symbols can be scanned
* candidates are ranked
* rejected candidates explain why they were rejected
* scanner does not execute paper trades

---

## Portfolio Allocator

Status: Complete / recently improved.

Contains:

* PortfolioAllocationDecision
* PortfolioAllocationResult
* PortfolioAllocator

Responsibility:

* select accepted BUY candidates
* reject non-accepted candidates
* reject already-open positions
* respect available cash
* respect legacy max open positions
* respect max position value
* respect max position size percentage
* respect max portfolio exposure
* respect minimum cash reserve
* calculate integer quantities
* explain approval/rejection

It must not:

* fetch market data
* run TradingPipeline
* execute trades
* mutate TradingSession

Current allocation config fields:

* `max_position_value`
* `max_position_size_pct`
* `max_portfolio_exposure`
* `min_cash_reserve_pct`
* `max_open_positions`

Important architectural direction:

`max_open_positions` remains as a safety cap, but portfolio allocation is now moving toward risk-based limits instead of a small fixed number of positions.

---

## Autonomous Paper Trading Runner

Status: Operational.

Contains:

* AutonomousPaperTradingConfig
* AutonomousPaperTradingCycleResult
* AutonomousPaperTradingResult
* AutonomousPaperTradingRunner
* run_autonomous_paper_trading.py

Responsibility:

* preserve one TradingSession across multiple cycles
* call LivePaperMarketScanner
* call PortfolioAllocator
* execute approved allocations through TradingCycle
* return immutable autonomous result
* optionally load and save portfolio state through a PaperPortfolioRepository

Current runner is finite.

This remains intentional.

Command:

```text
python run_autonomous_paper_trading.py
```

Validated autonomous paper-trading behaviour:

* completed cycles
* failed cycles tracked
* executed trades tracked
* rejected trades tracked
* failed symbols tracked
* open paper positions maintained
* portfolio cash/equity updated

---

## Continuous Paper Trading Runner

Status: Operational.

Contains:

* ContinuousRunnerConfig
* ContinuousPaperTradingRunner
* ContinuousPaperTradingRunResult
* run_continuous_paper_trading.py

Purpose:

Run repeated autonomous paper-trading iterations until stopped.

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
        ↓
PaperTradingService
```

Responsibilities:

* repeatedly run finite autonomous paper-trading iterations
* wait between iterations
* support max_iterations for safe tests
* stop cleanly on KeyboardInterrupt
* optionally continue after exceptions
* print iteration summaries

It must not:

* generate trading decisions
* allocate capital directly
* execute trades directly
* mutate strategy configuration
* duplicate AutonomousPaperTradingRunner logic

Command:

```text
python run_continuous_paper_trading.py
```

Current default continuous interval:

```text
300 seconds
```

The current interval is a starting point for longer paper-trading experiments, not a final trading law.

---

## Persistence Layer

Status: Operational foundation.

Contains:

* DataclassSerializer
* PaperPortfolioRepository
* JsonPaperPortfolioRepository
* TradeJournalRepository
* JsonlTradeJournalRepository

Purpose:

Enable ORION to persist paper-trading state across application restarts.

Current persistence architecture:

```text
PaperPortfolio
        ↓
DataclassSerializer
        ↓
JsonPaperPortfolioRepository
        ↓
data/paper_portfolio.json
```

```text
TradeJournalEntry
        ↓
DataclassSerializer
        ↓
JsonlTradeJournalRepository
        ↓
data/trade_journal.jsonl
```

Important rules:

* Trading services depend on repository interfaces, not concrete file formats.
* JSON is an implementation detail.
* Future SQLite/PostgreSQL repositories should reuse the same contracts.
* Repositories must not contain trading business logic.
* Serialization logic belongs in DataclassSerializer, not in each repository.

---

## Self-Evaluation Layer

Status: Complete.

Contains:

* TradeJournalEntry
* PerformanceAnalysisResult
* StrategyRecommendation
* StrategyRecommendationResult
* TradeJournalBuilder
* PerformanceAnalyzer
* StrategyRecommendationEngine

Purpose:

```text
Autonomous Paper Trading Result
        ↓
TradeJournalBuilder
        ↓
TradeJournalEntry[]
        ↓
PerformanceAnalyzer
        ↓
PerformanceAnalysisResult
        ↓
StrategyRecommendationEngine
        ↓
StrategyRecommendationResult
```

Important safety rule:

The recommendation engine is informational only.

It must not automatically modify config.

No auto-tuning is currently allowed.

---

## Controlled Learning / Hypothesis Evaluation

Status: Complete as deterministic foundation.

Contains:

* StrategyHypothesis
* HypothesisEvaluationContext
* HypothesisEvaluation
* HypothesisEvaluationReport
* HypothesisEvaluator
* HypothesisContextBuilder
* HypothesisEvaluationService
* HypothesisReportBuilder
* StrategyRecommendationEngine integration

Purpose:

Evaluate strategy hypotheses against performance metrics without mutating production strategy configuration.

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

Important rules:

* No AI.
* No trading decisions.
* No automatic config mutation.
* No automatic strategy tuning.
* Hypothesis evaluation is informational only.

---

## Learning Pipeline

Status: Complete as deterministic first vertical slice.

Contains:

* StrategyIdea
* StrategyIdeaBuilder
* LearningPipelineResult
* LearningPipeline

Purpose:

Convert performance analysis into deterministic strategy ideas through recommendations.

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

Important rules:

* LearningPipeline does not execute trades.
* LearningPipeline does not create strategy variants.
* LearningPipeline does not perform replay testing.
* LearningPipeline does not mutate configuration.
* StrategyIdea contains intent only, not concrete parameter values.

---

## Strategy Variant Foundation

Status: Started.

Contains:

* StrategyVariant
* StrategyVariantProposal
* StrategyIdea

Important design decision:

ORION must not jump directly from recommendation to concrete parameter mutation.

Preferred future chain:

```text
StrategyRecommendation
        ↓
StrategyIdea
        ↓
ProposalGenerator
        ↓
StrategyVariantProposal
        ↓
StrategyVariant
        ↓
Controlled replay / comparison
```

Reason:

Builders should assemble, not decide.

Concrete parameter changes must be generated only by deterministic, tested proposal logic.

---

# CURRENT HIGH-LEVEL FLOW

The current full runtime architecture is:

```text
data/universes/swing.csv
        ↓
WatchlistService
        ↓
LivePaperMarketScanner
        ↓
YahooProvider
        ↓
PaperTradingPipelineAdapter
        ↓
IndicatorBuilder
        ↓
TradingPipeline
        ↓
TradingPipelineResult
        ↓
LivePaperCandidate[]
        ↓
PortfolioAllocator
        ↓
PortfolioAllocationDecision[]
        ↓
TradingCycle
        ↓
PaperTradingService
        ↓
ExecutionEngine
        ↓
PaperPortfolio / TradingSession
        ↓
AutonomousPaperTradingRunner
        ↓
ContinuousPaperTradingRunner
```

The current self-evaluation / learning architecture is:

```text
AutonomousPaperTradingResult
        ↓
TradeJournalBuilder
        ↓
TradeJournalEntry[]
        ↓
PerformanceAnalyzer
        ↓
PerformanceAnalysisResult
        ↓
StrategyRecommendationEngine
        ↓
StrategyRecommendationResult
        ↓
LearningPipeline
        ↓
StrategyIdea[]
```

The current persistence architecture is:

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

---

# IMPORTANT ARCHITECTURAL DECISIONS

## Scanner / Allocator / Runner Separation

Responsibilities are separated:

```text
LivePaperMarketScanner = scan and rank
PortfolioAllocator = choose what can be bought
AutonomousPaperTradingRunner = orchestrate cycles and execute approved trades
ContinuousPaperTradingRunner = repeat finite autonomous runs over time
```

Do not collapse these responsibilities back into one service.

---

## Typed-Only Pipeline

The pipeline is typed-only.

Use:

```text
TradingPipelineResult
```

Do not reintroduce anonymous dictionaries as pipeline contracts.

---

## Paper Before Real Broker

ORION must prove itself with paper money before any real broker integration.

Current paper examples:

* €500 paper cash
* 250 max symbols configured for larger scans
* risk-based portfolio allocation
* max €150 nominal position value
* max 10% position size by equity
* max 95% portfolio exposure
* 5% minimum cash reserve
* minimum confidence 0.75
* continuous runner interval: 300 seconds

These are configuration values, not hard-coded strategy laws.

---

## Persistence Before Long-Term Evaluation

Long-running paper trading requires persistent state.

Current persistence foundation exists for:

* PaperPortfolio
* TradeJournalEntry

Still required for stronger long-term analysis:

* richer daily reports
* equity curve history
* position lifecycle journal events
* close-event persistence
* market-hours aware scheduling

---

## AI Safety Rule

AI may assist with:

* explanations
* summaries
* reports
* recommendations
* architecture review

AI may not:

* place trades
* mutate strategy config
* bypass deterministic services
* invent BUY/SELL decisions
* override RiskPlan
* override ExecutionValidator

---

# CURRENT TECHNICAL DEBT / REVIEW TARGETS

Current review targets:

* YahooProvider still needs retry, timeout, caching and batching.
* LivePaperTradingResult still contains executed_trades and rejected_trades even though the scanner does not execute.
* TradeJournalBuilder may need richer execution result details.
* PaperPosition current prices must be reviewed during long-running sessions.
* Position lifecycle should close positions based on stop/target logic during live cycles.
* Market-hours scheduler is not implemented yet.
* Continuous runner currently uses sleep interval, not exact wall-clock aligned scheduling.
* WatchlistService is now the symbol-loading source; avoid duplicate universe managers unless needed.
* Large watchlist scans need profiling before parallel scanning.
* No real broker integration.
* No automatic strategy mutation.
* StrategyVariant / ProposalGenerator / Replay Comparison are not complete yet.

---

# NEXT RECOMMENDED STEP

Current branch:

```text
fix/trading-config-indicators
```

Current status:

```text
58 tests PASS
```

The next sprint should be selected from the actual repository state.

Recommended next direction:

```text
Sprint 8.3 — Large Universe / Scalable Scanner Hardening
```

Suggested goals:

1. Confirm `data/universes/swing.csv` content and symbol count.
2. Increase scan universe carefully.
3. Profile scan duration.
4. Add scan timing metrics.
5. Add YahooProvider retry/timeout handling.
6. Add provider failure reporting.
7. Consider bounded parallel scanning only after baseline timing is known.
8. Keep WatchlistService as the only source of symbol loading.

Do not jump directly to real broker integration.

Do not enable automatic config mutation.

Do not create duplicate watchlist/universe-loading layers.

---

# DEVELOPMENT RULES

Never bypass existing engines.

Never duplicate logic.

Never reintroduce legacy dict contracts.

Every subsystem must have:

* models
* services
* tests

Regression tests must pass before every commit.

Architecture changes must be documented.

Use repository code as the source of truth.

Work from the current branch.

Do not assume an older sprint plan remains correct.

---

# CURRENT PROJECT HEALTH

Architecture:

```text
Stable and actively evolving toward long-running paper trading
```

Regression:

```text
58 tests PASS
```

Execution Layer:

```text
Complete
```

Paper Trading:

```text
Operational
```

Live Paper Trading:

```text
Operational
```

Autonomous Paper Trading:

```text
Operational, finite-run, portfolio persistence supported
```

Continuous Paper Trading:

```text
Operational, interval-based, manually stoppable
```

Persistence:

```text
Operational foundation
```

Self-Evaluation:

```text
Operational, recommendation-only
```

Controlled Learning:

```text
Operational foundation, no auto-tuning
```

Next focus:

```text
Scalable market universe scanning, YahooProvider hardening, scheduler, and long-running paper-trading validation
```

END OF FILE
