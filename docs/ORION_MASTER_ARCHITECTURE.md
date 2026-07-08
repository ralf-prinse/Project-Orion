# ORION_MASTER_ARCHITECTURE.md

> Documentation Version: v1.17
> Architecture Version: v3.1
> Last Updated: 2026-07-08
> Active Branch: fix/trading-config-indicators
> Regression Status: 58 tests PASS

---

# PROJECT ORION MASTER ARCHITECTURE

This document defines the current high-level architecture of Project Orion.

The repository remains the primary source of truth.
If this document and the code disagree, the code wins.

Before starting any new sprint, the full repository must be reviewed.

---

# DESIGN PHILOSOPHY

Orion is a deterministic, modular, AI-assisted swing trading and paper-trading system.

The project has evolved from a trading engine into a broader market monitoring and paper-trading platform.

Primary goals:

* deterministic
* modular
* explainable
* testable
* broker-independent
* paper-first
* safe to extend
* AI-assisted, not AI-controlled

AI may assist with:

* explanation
* summarization
* performance analysis
* recommendations
* strategy review
* documentation

AI may never directly and non-deterministically generate:

* BUY decisions
* SELL decisions
* stop-loss values
* targets
* risk sizing
* broker execution
* automatic config mutation

All trading decisions must remain deterministic and testable.

---

# CORE ARCHITECTURE RULES

Every subsystem should follow this pattern:

```text
Context / State / Input Model
        ↓
Service / Orchestrator
        ↓
Immutable Result Model
```

Rules:

* One clear responsibility per service.
* One immutable Result object per orchestrator.
* Business logic belongs in services.
* Models remain lightweight data contracts.
* No duplicated business logic.
* No circular dependencies.
* No anonymous dict contracts between major subsystems.
* Regression tests are mandatory.
* Documentation must be updated after completed sprints.
* Real broker integration is forbidden until paper trading proves stable.
* AI may advise, but may not control trading behaviour.

---

# CURRENT SYSTEM OVERVIEW

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
PaperPortfolioRepository
        ↓
AutonomousPaperTradingRunner
        ↓
ContinuousPaperTradingRunner
        ↓
TradeJournalRepository
        ↓
PerformanceAnalyzer
        ↓
LearningPipeline
```

---

# IMPLEMENTED SUBSYSTEMS

## 1. Market Data

Purpose:

Provide market data to the rest of Orion.

Main components:

```text
providers/base_provider.py
providers/yahoo_provider.py
models/market_data.py
```

Current provider:

```text
YahooProvider
```

Capabilities:

* get current price
* get current market data
* get historical OHLCV data

Current dependency:

```text
yfinance
```

Important limitation:

YahooProvider currently needs review for:

* retry logic
* timeout handling
* caching
* batching
* large watchlist reliability
* rate-limit resilience

---

## 2. Watchlist / Universe Loading

Purpose:

Load the symbols that Orion should scan.

Main service:

```text
services/watchlist_service.py
```

Default universe file:

```text
data/universes/swing.csv
```

Current behaviour:

* loads symbols from the configured universe file
* ignores empty lines
* ignores comment lines starting with `#`
* uppercases symbols
* deduplicates symbols
* returns sorted symbols

Rule:

```text
WatchlistService is the only source of truth for symbol loading.
```

Do not duplicate watchlist or universe-loading logic unless a future repository review clearly justifies it.

---

## 3. Indicator / Pipeline Adapter

Purpose:

Convert historical market data into pipeline-ready indicator input.

Main components:

```text
services/paper_trading_pipeline_adapter.py
services/indicator_builder.py
services/intelligence/intelligence_models.py
```

Flow:

```text
Historical OHLCV Data
        ↓
IndicatorBuilder
        ↓
IndicatorPack
        ↓
TradingPipeline
```

Responsibilities:

* receive historical market data
* build indicator input
* connect market data to the typed TradingPipeline
* keep live scanner logic separate from indicator construction

---

## 4. Market Analysis / Trading Pipeline

Purpose:

Analyze market conditions and produce deterministic trading decisions.

Main components:

```text
services/orchestration/trading_pipeline.py
models/trading_pipeline_result.py
services/intelligence/signal_fusion_engine.py
services/intelligence/market_intelligence_engine.py
services/intelligence/ai_context_builder.py
services/intelligence/ai_explainer.py
services/decision/adaptive_decision_engine.py
services/decision/position_sizing.py
```

Output:

```text
TradingPipelineResult
```

Important rule:

```text
TradingPipelineResult is the only valid contract between TradingPipeline and downstream systems.
```

Forbidden legacy patterns:

```text
pipeline_output
legacy_output
result["pipeline"]
result.items()
result.keys()
result.values()
```

The TradingPipeline must not:

* execute trades
* mutate portfolios
* persist state
* bypass RiskPlan creation

---

## 5. Risk Engine

Purpose:

Convert market and decision context into a deterministic RiskPlan.

Main components:

```text
models/risk_plan.py
services/risk/risk_context_builder.py
services/risk/adaptive_risk_engine.py
services/risk/risk_plan_validator.py
```

Responsibilities:

* entry price
* stop loss
* targets
* risk percent
* reward percent
* risk/reward ratio
* confidence
* notes
* validation

The Risk Engine must not:

* fetch market data
* execute trades
* mutate portfolio state
* persist state

---

## 6. Execution Layer

Purpose:

Convert deterministic trading requests into validated paper executions.

Main components:

```text
models/execution_request.py
models/execution_context.py
models/execution_result.py
services/execution_validator.py
services/order_factory.py
services/execution_engine.py
services/execution_report_builder.py
services/paper_broker.py
```

Flow:

```text
ExecutionRequest
        ↓
ExecutionContext
        ↓
ExecutionValidator
        ↓
OrderFactory
        ↓
PaperBroker
        ↓
PortfolioManager
        ↓
ExecutionEngineResult
```

Execution validation rejects:

* missing symbol
* non-positive entry price
* non-positive quantity
* non-positive confidence
* insufficient cash
* excessive position allocation

The Execution Layer must never generate BUY/SELL decisions.

---

## 7. Paper Trading Foundation

Purpose:

Simulate trades with paper money.

Main components:

```text
models/paper_portfolio.py
models/paper_position.py
models/trading_session.py
services/paper_trading_service.py
services/paper_position_update_service.py
services/paper_position_close_service.py
services/portfolio_manager.py
```

Responsibilities:

* maintain cash
* maintain equity
* maintain positions
* open paper positions
* update paper positions
* close paper positions
* optionally persist PaperPortfolio through PaperPortfolioRepository

The Paper Trading subsystem must not:

* scan markets
* calculate indicators
* generate trading decisions

---

## 8. Position Management

Purpose:

Manage already opened positions.

Main components:

```text
models/position_state.py
services/position_state_factory.py
services/position_state_store.py
services/position_update_engine.py
services/position_manager.py
services/break_even_service.py
services/trailing_stop_service.py
services/time_stop_service.py
services/position_management_summary_builder.py
```

Responsibilities:

* break-even logic
* trailing stop logic
* time stop logic
* health updates
* position state updates
* position management summaries

Position Management must not:

* open new trades
* generate BUY signals
* fetch market data directly

---

## 9. Trading Cycle

Purpose:

Execute one deterministic trading tick.

Main components:

```text
models/market_snapshot.py
services/trading_cycle.py
models/trading_cycle_result.py
```

Input:

```text
TradingSession + MarketSnapshot + quantity
```

Output:

```text
TradingCycleResult
```

Responsibilities:

* open positions when approved
* update existing positions
* close positions where applicable
* return updated TradingSession
* preserve deterministic cycle behaviour

TradingCycle must not:

* calculate indicators
* rank candidates
* allocate portfolio capital
* fetch live market data directly

---

## 10. Paper Trading Runner

Purpose:

Run multiple deterministic TradingCycles.

Main components:

```text
services/paper_trading_runner.py
models/paper_trading_run_result.py
```

Responsibilities:

* execute multiple TradingCycles
* preserve TradingSession
* collect cycle results
* return immutable PaperTradingRunResult

Current role:

This remains useful for deterministic and synthetic tests.

---

## 11. Paper Trading Demo Runner

Purpose:

Provide deterministic end-to-end demo without external market data.

Main components:

```text
models/paper_trading_demo_result.py
services/paper_trading_demo_runner.py
run_paper_trading_demo.py
```

Command:

```text
python run_paper_trading_demo.py
```

This proves the software architecture works without relying on Yahoo Finance.

Validated behaviour:

* synthetic market history can be converted into indicators
* TradingPipeline can produce typed output
* TradingCycle can open/update paper positions
* PaperPortfolio cash/equity updates correctly

---

## 12. Live Paper Market Scanner

Purpose:

Scan live market data and produce ranked candidates.

Main components:

```text
models/live_paper_trading_config.py
models/live_paper_trading_result.py
services/live_paper_market_scanner.py
run_live_paper_trading.py
services/watchlist_service.py
```

Responsibilities:

* load symbols through WatchlistService
* fetch historical market data
* run PaperTradingPipelineAdapter
* produce LivePaperCandidate objects
* score candidates
* return LivePaperTradingResult

Flow:

```text
WatchlistService
        ↓
LivePaperMarketScanner
        ↓
YahooProvider
        ↓
PaperTradingPipelineAdapter
        ↓
TradingPipelineResult
        ↓
LivePaperCandidate[]
```

Important rule:

```text
LivePaperMarketScanner scans only.
```

It must not:

* allocate capital
* execute trades
* mutate TradingSession
* place broker orders
* duplicate symbol-loading logic

Current limitation:

`LivePaperTradingResult` still contains `executed_trades` and `rejected_trades`, even though the scanner no longer executes trades. This should be reviewed in a future result-model cleanup.

---

## 13. Portfolio Allocator

Purpose:

Choose which ranked candidates may receive paper capital.

Main components:

```text
models/portfolio_allocation_result.py
services/portfolio_allocator.py
```

Responsibilities:

* sort candidates by score
* reject non-accepted candidates
* reject already-open positions
* respect available cash
* respect minimum cash reserve
* respect maximum portfolio exposure
* respect maximum position size percentage
* respect maximum nominal position value
* retain max open positions as a legacy safety cap
* calculate integer quantity
* explain allocation decision

Current allocation model:

```text
available cash
        ↓
cash reserve
        ↓
max portfolio exposure
        ↓
max position size %
        ↓
max nominal position value
        ↓
integer quantity
```

The allocator must not:

* fetch market data
* run the TradingPipeline
* execute trades
* mutate TradingSession

Important design direction:

`max_open_positions` is now a safety cap, not the primary portfolio sizing model.

The primary allocation direction is risk-based allocation using:

* `max_position_size_pct`
* `max_portfolio_exposure`
* `min_cash_reserve_pct`
* `max_position_value`

---

## 14. Autonomous Paper Trading Runner

Purpose:

Run multiple live paper cycles while preserving one TradingSession.

Main components:

```text
models/autonomous_paper_trading_config.py
models/autonomous_paper_trading_result.py
services/autonomous_paper_trading_runner.py
run_autonomous_paper_trading.py
```

Responsibilities:

* create or load a TradingSession portfolio
* run LivePaperMarketScanner
* run PortfolioAllocator
* execute approved allocations through TradingCycle
* preserve session across cycles
* return AutonomousPaperTradingResult
* optionally load PaperPortfolio from repository
* optionally save PaperPortfolio after cycles

Flow:

```text
AutonomousPaperTradingRunner
        ↓
LivePaperMarketScanner
        ↓
PortfolioAllocator
        ↓
TradingCycle
        ↓
TradingSession
```

Current status:

```text
Finite-run orchestrator.
```

This is intentional.

Long-running behaviour is handled by `ContinuousPaperTradingRunner`, which repeatedly calls the finite autonomous runner instead of duplicating trading logic.

Command:

```text
python run_autonomous_paper_trading.py
```

---

## 15. Continuous Paper Trading Runner

Purpose:

Run repeated finite autonomous paper-trading iterations until manually stopped.

Main components:

```text
models/continuous_runner_config.py
services/continuous_paper_trading_runner.py
run_continuous_paper_trading.py
```

Responsibilities:

* call AutonomousPaperTradingRunner repeatedly
* wait between iterations
* track completed iterations
* track failed iterations
* support max_iterations for deterministic tests
* stop cleanly on KeyboardInterrupt
* print iteration summaries

Flow:

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

Current status:

```text
Operational, interval-based.
```

Current limitations:

* not wall-clock aligned
* no market-hours awareness
* no weekend skipping
* no daily report yet

Command:

```text
python run_continuous_paper_trading.py
```

Important rule:

The continuous runner must not duplicate trading logic from `AutonomousPaperTradingRunner`.

---

## 16. Self-Evaluation Layer

Purpose:

Allow ORION to evaluate its own paper-trading behaviour.

Main components:

```text
models/trade_journal_entry.py
models/performance_analysis_result.py
models/strategy_recommendation.py
services/trade_journal_builder.py
services/performance_analyzer.py
services/strategy_recommendation_engine.py
```

Flow:

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
```

Current capabilities:

* journal entry creation
* win/loss analysis
* realized P/L analysis
* unrealized P/L analysis
* average confidence
* average expected risk
* dominant regime
* dominant volatility
* strategy recommendations

Important safety rule:

```text
Recommendations are informational only.
No automatic configuration mutation is currently allowed.
```

Current limitation:

TradeJournalBuilder should be reviewed for whether it should record richer explicit execution details.

---

## 17. Persistence Layer

Purpose:

Persist paper-trading state across application restarts.

Main components:

```text
services/serialization/dataclass_serializer.py
services/stores/repositories/paper_portfolio_repository.py
services/stores/json_paper_portfolio_repository.py
services/stores/repositories/trade_journal_repository.py
services/stores/jsonl_trade_journal_repository.py
```

Portfolio flow:

```text
PaperPortfolio
        ↓
DataclassSerializer
        ↓
JsonPaperPortfolioRepository
        ↓
data/paper_portfolio.json
```

Journal flow:

```text
TradeJournalEntry
        ↓
DataclassSerializer
        ↓
JsonlTradeJournalRepository
        ↓
data/trade_journal.jsonl
```

Responsibilities:

* serialize dataclass models
* persist PaperPortfolio snapshots
* load existing PaperPortfolio state
* append TradeJournalEntry records
* load persisted journal entries
* hide storage format behind repository interfaces

Rules:

* Trading services depend on repository interfaces, not JSON files.
* Repositories must not contain trading business logic.
* Serialization logic belongs in DataclassSerializer.
* Future SQLite/PostgreSQL stores should implement the same repository contracts.

Current status:

```text
Operational foundation.
```

Current limitations:

* no daily report store yet
* no equity curve store yet
* JsonlTradeJournalRepository is not yet automatically wired as the continuous runner journal sink

---

## 18. Controlled Learning / Learning Pipeline

Purpose:

Evaluate performance and produce deterministic learning ideas without changing production configuration.

Main components:

```text
models/strategy_hypothesis.py
models/hypothesis_evaluation_context.py
models/hypothesis_evaluation.py
models/hypothesis_evaluation_report.py
services/hypothesis_context_builder.py
services/hypothesis_evaluator.py
services/hypothesis_evaluation_service.py
services/hypothesis_report_builder.py
models/strategy_idea.py
models/learning_pipeline_result.py
services/strategy_idea_builder.py
services/learning_pipeline.py
```

Hypothesis evaluation flow:

```text
PerformanceAnalysisResult
        ↓
HypothesisEvaluationService
        ↓
HypothesisEvaluationReport
        ↓
StrategyRecommendationEngine
```

Learning pipeline flow:

```text
PerformanceAnalysisResult
        ↓
StrategyRecommendationEngine
        ↓
StrategyRecommendationResult
        ↓
StrategyIdeaBuilder
        ↓
LearningPipelineResult
```

Rules:

* No automatic strategy mutation.
* No automatic config changes.
* No AI-generated trading decisions.
* StrategyIdea is intent-only.
* Concrete strategy variants require a future ProposalGenerator.
* Replay or paper comparison must exist before any strategy change is accepted.

Current status:

```text
Operational foundation.
```

Current limitations:

* no ProposalGenerator yet
* no ReplayEngine yet
* no StrategyComparisonResult yet
* no automatic strategy tuning

---

# CURRENT OPERATIONAL COMMANDS

Run all tests:

```text
python run_tests.py
```

Run deterministic paper demo:

```text
python run_paper_trading_demo.py
```

Run live paper scanner:

```text
python run_live_paper_trading.py
```

Run autonomous finite paper trading:

```text
python run_autonomous_paper_trading.py
```

Run continuous paper trading:

```text
python run_continuous_paper_trading.py
```

---

# CURRENT TEST STATUS

Current regression suite:

```text
58 tests PASS
```

Health:

```text
ORION HEALTH: EXCELLENT
```

---

# CURRENT ARCHITECTURE STATUS

The current architecture is stable enough to run finite and continuous paper-trading experiments.

The system has moved beyond a pure trading engine and is now becoming a broader market monitoring and paper-trading platform.

Major completed architectural layers:

* typed pipeline result
* live market scanning
* WatchlistService-based symbol loading
* risk-based portfolio allocation
* autonomous finite runner
* continuous paper runner
* portfolio persistence
* trade journal persistence foundation
* self-evaluation
* controlled learning foundation

The current highest-priority technical direction is:

```text
Large Universe / Scalable Scanner Hardening
        ↓
Market Scheduler
        ↓
Weeks-long paper trading validation
        ↓
Replay / Strategy validation
        ↓
Broker abstraction research
```

---

# KNOWN REVIEW TARGETS

The next architecture review must check:

* Full project structure.
* All models.
* All services.
* Orchestration layers.
* Tests.
* Documentation.
* Dependencies.
* Data flows.
* Context/result patterns.
* Stores.
* Builders.
* Validators.
* Factories.
* Duplicate business logic.
* Circular dependencies.
* Public interface stability.
* Future change hotspots.
* Whether result models are still clean.
* Whether scanner/allocator/runner separation is still correct.
* Whether WatchlistService remains the only symbol-loading source.
* Whether TradeJournalBuilder records enough execution detail.
* Whether JsonlTradeJournalRepository should be wired into continuous runs.
* Whether open position prices are refreshed correctly.
* Whether YahooProvider needs hardening before large universe scans.
* Whether continuous runner needs market-hours awareness.
* Whether controlled learning should next move toward replay validation.

---

# CURRENT TECHNICAL DEBT

## LivePaperTradingResult

Currently contains:

```text
executed_trades
rejected_trades
```

But after scanner/allocator/runner separation, the scanner no longer executes trades.

Review whether these fields should remain, move, or be removed.

---

## TradeJournalBuilder

Currently builds entries from autonomous allocation decisions.

Review whether it should also record explicit execution result details.

---

## PaperPosition Price Updates

Review whether current prices are refreshed sufficiently across live and continuous cycles.

This is important before multi-week paper trading.

---

## YahooProvider

Needs review for:

* retries
* caching
* batching
* timeouts
* rate-limit resilience
* large universe reliability

---

## Persistent State

Current status:

```text
Portfolio persistence exists.
Trade journal persistence exists.
```

Still missing:

* automatic journal sink integration in autonomous/continuous runs
* daily report storage
* equity curve storage
* long-term performance history exports

---

## Scheduler

Currently missing:

* wall-clock aligned scanning
* market-hours awareness
* weekend skipping
* daily report generation
* scheduled session summaries

---

## Parallel Scanning

Currently not implemented.

Do not add unbounded parallel Yahoo requests.

Parallel scanning may only be considered after baseline sequential scan timing exists.

Required before implementation:

* scan duration metrics
* fake provider tests
* bounded worker count
* deterministic result ordering
* timeout/failure handling
* clear rate-limit strategy

---

## Position Lifecycle

Long-running paper trading requires stronger position lifecycle handling.

Review and improve:

* current price refresh
* stop-loss hit detection
* target hit detection
* trailing stop updates
* break-even updates
* close-event journal entries

---

## Replay / Strategy Validation

Controlled learning exists as a foundation, but replay validation is not implemented.

Still missing:

* ProposalGenerator
* StrategyVariantProposalResult
* ReplayEngine
* StrategyComparisonResult
* current strategy vs candidate strategy comparison

No strategy mutation should happen before replay validation exists.

---

# DEVELOPMENT PHASES

## Level 1 — Deterministic Paper Trading

Status:

```text
Complete
```

Includes:

* TradingPipeline
* Risk Engine
* Execution Engine
* Paper Broker
* Paper Portfolio
* Position Management
* Trading Cycle
* Paper Trading Runner

---

## Level 2 — Typed Pipeline Integration

Status:

```text
Complete
```

Includes:

* TradingPipelineResult
* typed-only downstream flow
* removal of legacy dict compatibility

---

## Level 3 — Live Paper Trading

Status:

```text
Complete
```

Includes:

* YahooProvider
* WatchlistService
* LivePaperMarketScanner
* LivePaperTradingConfig
* live paper CLI

---

## Level 4 — Portfolio Allocation

Status:

```text
Complete
```

Includes:

* PortfolioAllocator
* PortfolioAllocationDecision
* PortfolioAllocationResult
* risk-based allocation limits

---

## Level 5 — Autonomous Finite Paper Trading

Status:

```text
Complete
```

Includes:

* AutonomousPaperTradingRunner
* AutonomousPaperTradingConfig
* AutonomousPaperTradingResult
* multi-cycle session preservation

---

## Level 6 — Self-Evaluation

Status:

```text
Complete
```

Includes:

* TradeJournalEntry
* TradeJournalBuilder
* PerformanceAnalyzer
* StrategyRecommendationEngine

---

## Level 7 — Controlled Learning

Status:

```text
Complete
```

Includes:

* StrategyHypothesis
* HypothesisEvaluationService
* HypothesisEvaluationReport
* StrategyIdea
* LearningPipeline

---

## Level 8 — Persistence

Status:

```text
Complete foundation
```

Includes:

* DataclassSerializer
* PaperPortfolioRepository
* JsonPaperPortfolioRepository
* TradeJournalRepository
* JsonlTradeJournalRepository

---

## Level 9 — Continuous Paper Trading

Status:

```text
Complete foundation
```

Includes:

* ContinuousRunnerConfig
* ContinuousPaperTradingRunner
* run_continuous_paper_trading.py

---

## Level 10 — Large Universe Scanning

Status:

```text
In progress
```

Goals:

* larger universe support
* scan duration metrics
* YahooProvider hardening
* sequential baseline profiling
* future bounded parallel scanning

---

## Level 11 — Market Scheduler

Status:

```text
Not started
```

Potential future capabilities:

* wall-clock aligned scan loop
* market-hours service
* weekend skipping
* daily report
* scheduled paper sessions

---

## Level 12 — Replay / Strategy Validation

Status:

```text
Not started
```

Potential future capabilities:

* ProposalGenerator
* StrategyVariantProposal
* ReplayEngine
* StrategyComparisonResult

---

## Level 13 — Broker Abstraction / Real Broker

Status:

```text
Not started
```

Possible future broker adapters:

* Interactive Brokers
* Alpaca
* Saxo
* Trading212 research

Rule:

Broker adapters may only execute deterministic orders.

Broker adapters may never calculate:

* BUY / SELL
* stop loss
* targets
* position size
* risk plan
* confidence

---

# DO NOT VIOLATE

Do not:

* reintroduce dict pipeline contracts
* bypass TradingPipeline
* bypass RiskPlan
* bypass ExecutionValidator
* combine scanner, allocator, runner and scheduler responsibilities
* let AI mutate trading config automatically
* connect a real broker before paper trading proves stable
* duplicate watchlist/universe-loading logic
* add unbounded parallel Yahoo requests
* treat max_open_positions as the primary allocation model
* create a second continuous runner that duplicates AutonomousPaperTradingRunner logic
* mutate strategy configuration from recommendations
* allow LearningPipeline to generate executable strategy changes
* allow broker adapters to calculate decisions, risk plans or position sizing

---

# NEXT REQUIRED ACTION

Continue Sprint 8.3 on branch:

```text
fix/trading-config-indicators
```

Focus:

```text
Large Universe / Scalable Scanner Hardening
```

Required next analysis:

* confirm `data/universes/swing.csv`
* confirm symbol count
* profile scan duration
* add scan timing metrics
* review YahooProvider retry handling
* review YahooProvider timeout handling
* review YahooProvider caching/batching options
* improve symbol-level failure reporting
* keep WatchlistService as the only symbol-loading source

Only after scan performance is measurable should bounded parallel scanning be considered.

After Sprint 8.3, likely next direction:

```text
Market Scheduler
        ↓
Long-running multi-week paper trading
        ↓
Position lifecycle improvements
        ↓
Replay / Strategy validation
```

Do not start real broker integration.

Do not enable automatic strategy mutation.

---

# END OF FILE



