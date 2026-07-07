 CHANGELOG.md

> Documentation Version: v1.16  
> Architecture Version: v2.8  
> Last Updated: 2026-07-07  
> Active Branch: fix/trading-config-indicators  
> Regression Status: 46 tests PASS

---

# CHANGELOG

---

# v1.16 — Typed Live Autonomous Paper Trading + Self-Evaluation

Status:

```text
Completed

Regression:

46 tests PASS

Date:

2026-07-07
Summary

Version v1.16 completes the transition from a paper-trading foundation to a typed, live-data, autonomous finite-run paper-trading system with a first self-evaluation layer.

Major milestones completed:

TradingPipeline typed result integration
removal of legacy pipeline dictionary contracts
deterministic paper trading demo
live paper market scanner using Yahoo Finance
portfolio allocation layer
autonomous paper trading runner
trade journal builder
performance analyzer
strategy recommendation engine

The system can now scan real market data, rank candidates, allocate paper capital, execute approved paper trades, preserve a TradingSession across cycles and produce self-evaluation recommendations.

Sprint 6E — TradingPipelineResult Integration

Status:

Completed
Added
models/trading_pipeline_result.py
services/paper_trading_pipeline_adapter.py
test_trading_pipeline_result.py
test_paper_trading_pipeline_adapter.py
test_typed_paper_trading_flow.py
Changed
TradingPipeline now returns TradingPipelineResult.
MarketSnapshot was prepared for typed pipeline integration.
TradingCycle was updated to support typed pipeline flow.
PaperTradingService and ExecutionRequestBuilder were aligned with typed pipeline output during the transition.
Purpose

Move away from anonymous dictionary outputs and introduce a typed immutable result object as the contract between TradingPipeline and downstream paper-trading layers.

Result

Typed pipeline output became available while maintaining regression compatibility during migration.

Sprint 6F — Remove Legacy Pipeline Interface

Status:

Completed
Changed
Removed pipeline_output.
Removed legacy_output.
Removed dict-style access from TradingPipelineResult.
Removed result["pipeline"] usage.
Removed .items(), .keys(), .values() and .get() compatibility.
Updated services/orchestration/market_scanner.py.
Updated services/orchestration/backtest_engine.py.
Updated typed pipeline tests.
Architecture Impact

TradingPipelineResult became the only valid pipeline contract.

The system is now typed-only between TradingPipeline and downstream orchestration layers.

Result

Legacy pipeline dictionary compatibility was fully removed.

Sprint 7A — Deterministic Paper Trading Demo Runner

Status:

Completed
Added
models/paper_trading_demo_result.py
services/paper_trading_demo_runner.py
run_paper_trading_demo.py
test_paper_trading_demo_runner.py
Purpose

Create a deterministic demo that proves ORION's paper-trading architecture works end-to-end without relying on external market data.

Flow
Synthetic Market History
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
PaperTradingRunner
        ↓
PaperTradingDemoResult
Command
python run_paper_trading_demo.py
Result

End-to-end deterministic paper trading can be run from the terminal.

Sprint 7B — Live Paper Market Scanner

Status:

Completed
Added
models/live_paper_trading_config.py
models/live_paper_trading_result.py
services/live_paper_market_scanner.py
run_live_paper_trading.py
test_live_paper_market_scanner.py
Confirmed

Existing watchlist:

config/watchlist.txt

Contains:

259 symbols

Includes:

US equities
US ETFs
Dutch .AS tickers
German .DE tickers
Purpose

Use real market data with paper money only.

Flow
config/watchlist.txt
        ↓
YahooProvider
        ↓
PaperTradingPipelineAdapter
        ↓
TradingPipeline
        ↓
LivePaperCandidate[]
        ↓
LivePaperTradingResult
Command
python run_live_paper_trading.py
Result

ORION can scan a configurable subset of the real watchlist and produce ranked live paper candidates.

Sprint 7C — Autonomous Paper Trading Orchestration

Status:

Completed
Added
models/portfolio_allocation_result.py
services/portfolio_allocator.py
models/autonomous_paper_trading_config.py
models/autonomous_paper_trading_result.py
services/autonomous_paper_trading_runner.py
run_autonomous_paper_trading.py
test_portfolio_allocator.py
test_autonomous_paper_trading_runner.py
Changed
LivePaperMarketScanner responsibility was narrowed.
Scanner no longer executes trades.
Scanner no longer allocates portfolio capital.
Allocation moved into PortfolioAllocator.
Autonomous orchestration moved into AutonomousPaperTradingRunner.
Architecture Impact

Responsibilities are now separated:

LivePaperMarketScanner
        ↓
scan + rank only

PortfolioAllocator
        ↓
allocate limited paper capital

AutonomousPaperTradingRunner
        ↓
orchestrate cycles + execute approved allocations
Purpose

Allow ORION to behave like a finite autonomous paper trader while maintaining clean service boundaries.

Command
python run_autonomous_paper_trading.py
Result

ORION can preserve one TradingSession across multiple cycles, scan real market data, allocate paper cash and execute approved paper trades.

Sprint 7D — Self-Evaluation Layer

Status:

Completed
Added
models/trade_journal_entry.py
models/performance_analysis_result.py
models/strategy_recommendation.py
services/trade_journal_builder.py
services/performance_analyzer.py
services/strategy_recommendation_engine.py
test_trade_journal_builder.py
test_performance_analyzer.py
test_strategy_recommendation_engine.py
Purpose

Give ORION the foundation to evaluate its own paper-trading behaviour.

Flow
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
Capabilities

ORION can now calculate:

total trades
winning trades
losing trades
win rate
realized P/L
unrealized P/L
average P/L
average return percentage
best trade
worst trade
average confidence
average expected risk
profitable confidence threshold
dominant market regime
dominant volatility

ORION can now recommend:

collecting more data
increasing confidence threshold
reducing position exposure
avoiding high expected risk setups
using profitable confidence floor
maintaining current configuration
Safety Rule

Recommendations are informational only.

No automatic strategy mutation is currently allowed.

Architecture Changes Since v1.15
1. Typed Pipeline Contract

Before:

dict pipeline output

After:

TradingPipelineResult
2. Scanner / Allocator / Runner Separation

Before:

Scanner could scan, allocate and execute

After:

Scanner = scan/rank
Allocator = allocate capital
Runner = orchestrate/execute
3. Self-Evaluation Foundation

Added:

TradeJournalEntry
PerformanceAnalysisResult
StrategyRecommendation

This enables future controlled learning and hypothesis evaluation.

Current Operational Commands

Run full regression:

python run_tests.py

Run deterministic paper demo:

python run_paper_trading_demo.py

Run live paper scanner:

python run_live_paper_trading.py

Run autonomous finite paper trading:

python run_autonomous_paper_trading.py
Current Status

Project Health:

EXCELLENT

Architecture:

Stable, but review required before next sprint

Regression:

46 tests PASS

Paper Trading:

Operational

Live Paper Trading:

Operational

Autonomous Paper Trading:

Operational, finite-run

Self-Evaluation:

Operational, recommendation-only
Known Review Items

Before Sprint 7E, review:

LivePaperTradingResult execution counters now that scanner does not execute
whether TradeJournalBuilder should record execution results more explicitly
whether TradeJournal needs persistence
whether open position current prices refresh correctly each cycle
whether YahooProvider needs batching/caching/retries
whether result models should be split further
whether context/result input patterns are still consistent
whether autonomous runner needs richer per-cycle execution detail
Upcoming Version
v1.17

Do not define v1.17 implementation before architecture review.

Likely direction:

Controlled Learning / Hypothesis Evaluation

Potential future capabilities:

generate strategy hypotheses
compare strategy variants
evaluate recommendations against historical/paper data
rank controlled strategy changes
keep auto-tuning disabled until safe

END OF FILE