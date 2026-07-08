# CHANGELOG.md

> Documentation Version: v1.17
> Architecture Version: v3.1
> Last Updated: 2026-07-08
> Active Branch: fix/trading-config-indicators
> Regression Status: 58 tests PASS

---

# CHANGELOG

---

# v1.17 — Controlled Learning + Persistent Continuous Paper Trading Foundation

Status:

```text
Completed / Sprint 8.3 still in progress

Regression:
58 tests PASS

Date:
2026-07-08
```

## Summary

Version v1.17 extends ORION from a finite autonomous paper-trading system into the foundation for a long-running paper trader.

Major milestones completed:

* Controlled Learning / Hypothesis Evaluation
* Deterministic Learning Pipeline
* Persistent PaperPortfolio infrastructure
* Persistent TradeJournal infrastructure
* Continuous Paper Trading Runner
* Risk-based portfolio allocation limits
* WatchlistService-based scanner symbol loading

The system can now persist paper portfolio state, append trade journal records, repeatedly run autonomous paper-trading iterations, and prepare for larger universe scanning while keeping all trading logic deterministic.

No real broker integration was added.

No automatic strategy mutation was added.

---

# Sprint 7E — Controlled Learning / Hypothesis Evaluation

Status:

```text
Completed
```

## Added

* models/strategy_hypothesis.py
* models/hypothesis_evaluation_context.py
* models/hypothesis_evaluation.py
* models/hypothesis_evaluation_report.py
* services/hypothesis_context_builder.py
* services/hypothesis_evaluator.py
* services/hypothesis_evaluation_service.py
* services/hypothesis_report_builder.py
* regression tests for hypothesis evaluation flow

## Changed

* StrategyRecommendationEngine can incorporate hypothesis evaluation findings.
* Recommendations remain informational only.
* No configuration mutation was introduced.

## Purpose

Create a deterministic hypothesis evaluation layer between performance analysis and future strategy improvement work.

## Flow

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

## Result

ORION can now evaluate whether a deterministic strategy hypothesis is supported, rejected or inconclusive based on available performance data.

---

# Sprint 7F — Deterministic Learning Pipeline

Status:

```text
Completed
```

## Added

* models/strategy_idea.py
* models/learning_pipeline_result.py
* services/strategy_idea_builder.py
* services/learning_pipeline.py
* test_learning_pipeline.py

## Architectural decision

The originally considered `LearningCycle` direction was replaced by `LearningPipeline`.

Reason:

```text
TradingPipeline transforms market/indicator input into TradingPipelineResult.
LearningPipeline transforms performance analysis into LearningPipelineResult.
```

This keeps the architecture consistent.

## Purpose

Create the first complete vertical slice of the Learning Domain.

## Flow

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

## Result

ORION can now convert performance analysis into deterministic strategy ideas without generating concrete parameter changes.

## Safety rule

`StrategyIdea` is intent-only.

It must not:

* change configuration
* propose concrete parameter values
* execute trades
* use AI

---

# Sprint 8.1 — Persistent Paper Portfolio Infrastructure

Status:

```text
Completed
```

## Added

* services/serialization/dataclass_serializer.py
* services/stores/repositories/paper_portfolio_repository.py
* services/stores/json_paper_portfolio_repository.py
* services/stores/repositories/trade_journal_repository.py
* services/stores/jsonl_trade_journal_repository.py
* test_dataclass_serializer.py
* test_json_paper_portfolio_repository.py
* test_paper_trading_service_persistence.py
* test_autonomous_paper_trading_runner_persistence.py
* test_jsonl_trade_journal_repository.py

## Changed

* PaperTradingService can receive a PaperPortfolioRepository.
* PaperTradingService saves portfolio state after execution when a repository is provided.
* AutonomousPaperTradingRunner can load an existing portfolio when a repository exists.
* AutonomousPaperTradingRunner saves portfolio state after cycles when a repository is provided.

## Purpose

Allow ORION to survive application restarts without losing paper portfolio state.

## Portfolio Persistence Flow

```text
PaperPortfolio
        ↓
DataclassSerializer
        ↓
JsonPaperPortfolioRepository
        ↓
data/paper_portfolio.json
```

## Trade Journal Persistence Flow

```text
TradeJournalEntry
        ↓
DataclassSerializer
        ↓
JsonlTradeJournalRepository
        ↓
data/trade_journal.jsonl
```

## Architecture impact

Trading services depend on repository interfaces, not JSON.

This enables future storage implementations such as:

* SQLite
* PostgreSQL
* cloud storage

without changing trading-domain services.

---

# Sprint 8.2 — Continuous Paper Trading Runner

Status:

```text
Completed
```

## Added

* models/continuous_runner_config.py
* services/continuous_paper_trading_runner.py
* run_continuous_paper_trading.py
* test_continuous_paper_trading_runner.py

## Purpose

Allow ORION to repeatedly run finite autonomous paper-trading iterations until manually stopped.

## Flow

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

## Current behaviour

* runs until Ctrl+C
* supports max_iterations for deterministic tests
* sleeps between iterations
* tracks completed iterations
* tracks failed iterations
* prints iteration summaries
* reuses AutonomousPaperTradingRunner
* avoids duplicate trading logic

## Command

```text
python run_continuous_paper_trading.py
```

## Limitation

The runner currently uses interval sleep.

It does not yet:

* align scans to exact wall-clock times
* understand market hours
* skip weekends
* produce daily reports

---

# Sprint 8.3 — Risk-Based Allocation + WatchlistService Scanner Routing

Status:

```text
Partially completed
```

## Added / Changed

* LivePaperTradingConfig default max_symbols prepared for larger scans.
* LivePaperTradingConfig max_open_positions raised as legacy safety cap.
* Added max_position_size_pct.
* Added max_portfolio_exposure.
* Added min_cash_reserve_pct.
* PortfolioAllocator now uses risk-based allocation constraints.
* PortfolioAllocator still keeps max_open_positions as a safety cap.
* LivePaperMarketScanner now uses WatchlistService.
* Duplicate `_load_symbols()` logic removed from LivePaperMarketScanner.
* test_portfolio_allocator.py updated to make legacy allocation assumptions explicit.

## Purpose

Prepare ORION to scan more than 25 symbols and allocate capital more realistically.

## New allocation model

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

## Watchlist loading

Before:

```text
LivePaperMarketScanner
        ↓
_load_symbols()
```

After:

```text
LivePaperMarketScanner
        ↓
WatchlistService
        ↓
data/universes/swing.csv
```

## Architecture impact

Symbol loading now has a single source of truth:

```text
services/watchlist_service.py
```

Do not create duplicate watchlist/universe-loading logic unless a future repository review clearly justifies it.

---

# Validated Runtime Behaviour

## Paper Trading Demo

Command:

```text
python run_paper_trading_demo.py
```

Validated:

* IndicatorBuilder works.
* TradingPipeline produces typed BUY result.
* PaperTradingService opens a paper position.
* TradingCycle updates the same position.
* Portfolio cash/equity is updated.
* P/L is calculated.

## Live Paper Trading

Command:

```text
python run_live_paper_trading.py
```

Validated:

* Yahoo data can be fetched.
* Symbols can be scanned.
* Candidates can be ranked.
* Budget/risk filters can reject candidates safely.
* Scanner does not execute trades.

## Autonomous Paper Trading

Command:

```text
python run_autonomous_paper_trading.py
```

Validated:

* 3 cycles completed in runtime test.
* 0 failed cycles.
* 0 failed symbols.
* paper trades executed.
* paper portfolio updated.
* allocation rejected excess candidates safely.
* open positions maintained.

## Continuous Paper Trading

Command:

```text
python run_continuous_paper_trading.py
```

Validated by regression:

* repeated finite runs are possible.
* runner respects max_iterations.
* runner handles failing iterations.
* runner can stop cleanly.

---

# Current Operational Commands

Run full regression:

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

# Current Status

Project Health:

```text
EXCELLENT
```

Architecture:

```text
Stable, actively evolving toward long-running paper trading
```

Regression:

```text
58 tests PASS
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
Operational, interval-based
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

---

# Known Review Items

Current review targets:

* LivePaperTradingResult execution counters now that scanner does not execute.
* TradeJournalBuilder may need execution-result detail.
* JsonlTradeJournalRepository is not yet integrated into autonomous/continuous runs as an automatic journal sink.
* Open PaperPosition current prices must be validated in continuous runs.
* YahooProvider needs batching/caching/retries/timeouts.
* Large universe scans need performance profiling.
* Continuous runner needs market-hours awareness.
* Continuous runner should eventually use wall-clock aligned scheduling.
* Position lifecycle needs stronger live close/update validation.
* ProposalGenerator / ReplayEngine / StrategyComparisonEngine are not complete.
* Real broker integration remains forbidden.

---

# Upcoming Work

Recommended next work:

```text
Sprint 8.3 continued — Large Universe / Scalable Scanner Hardening
```

Likely focus:

* confirm `data/universes/swing.csv`
* measure scan duration
* add scan timing metrics
* harden YahooProvider
* improve failure reporting
* profile 25 / 100 / 250 symbol scans
* only then consider bounded parallel scanning

Do not define real broker work yet.

Do not enable automatic strategy mutation.

END OF FILE
