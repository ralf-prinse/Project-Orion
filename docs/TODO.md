# TODO.md

> Documentation Version: v1.17
> Architecture Version: v3.1
> Last Updated: 2026-07-08
> Active Branch: fix/trading-config-indicators
> Regression Status: 58 tests PASS

---

# PROJECT ORION TODO

Current state:

```text
Sprint 8.3 in progress

Current priority:
Large universe scanning + long-running paper-trading readiness

Status:
STABLE / ACTIVE DEVELOPMENT

Regression status:
58 PASS
0 FAIL
```

---

# COMPLETED

## Sprint 5.9 — Advanced Position Management

* MarketStructure
* RiskContext
* AdaptiveRiskEngine V2
* ATR Stop Loss
* Risk Distance Targets
* RiskPlanValidator
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

---

## Sprint 6 — Paper Trading Foundation

* ExecutionRequest
* ExecutionContext
* Order
* ExecutionResult
* ExecutionValidator
* OrderFactory
* ExecutionEngine
* PaperBroker
* PaperPortfolio
* PaperPosition
* PortfolioManager
* ExecutionReportBuilder
* TradingSession
* PaperTradingService
* PaperPositionUpdateService
* PaperPositionCloseService
* TradingCycle
* PaperTradingRunner

---

## Sprint 6E — TradingPipelineResult Integration

* Define TradingPipelineResult
* Add typed pipeline result regression test
* Connect TradingPipeline output to typed paper flow
* Add PaperTradingPipelineAdapter
* Convert market data into IndicatorPack
* Run TradingPipeline automatically
* Pass typed pipeline result into TradingCycle
* Add typed paper trading flow test
* Add adapter regression test

---

## Sprint 6F — Remove Legacy Pipeline Interface

* Remove pipeline_output
* Remove legacy_output
* Remove dict-style pipeline access
* Remove result["pipeline"]
* Remove .items(), .keys(), .values() compatibility
* Update MarketScanner to use typed result
* Update BacktestEngine to use typed result
* Update tests to typed-only contract
* Confirm full regression suite PASS

---

## Sprint 7A — Deterministic Paper Trading Demo Runner

* Add PaperTradingDemoResult
* Add PaperTradingDemoRunner
* Add run_paper_trading_demo.py
* Add deterministic demo regression test
* Run synthetic end-to-end paper trading demo

---

## Sprint 7B — Live Paper Market Scanner

* Confirm live-data scanner path
* Add LivePaperTradingConfig
* Add LivePaperCandidate
* Add LivePaperTradingResult
* Add LivePaperMarketScanner
* Add run_live_paper_trading.py
* Add live paper scanner regression test
* Support configurable max_symbols
* Use YahooProvider for historical data
* Produce ranked candidates from real market data

---

## Sprint 7C — Autonomous Paper Trading Orchestration

* Split scanner from execution
* Add PortfolioAllocationDecision
* Add PortfolioAllocationResult
* Add PortfolioAllocator
* Add AutonomousPaperTradingConfig
* Add AutonomousPaperTradingCycleResult
* Add AutonomousPaperTradingResult
* Add AutonomousPaperTradingRunner
* Add run_autonomous_paper_trading.py
* Add portfolio allocator regression test
* Add autonomous runner regression test
* Preserve one TradingSession across multiple cycles
* Execute only approved allocation decisions
* Keep runner finite-run only

---

## Sprint 7D — Self-Evaluation Layer

* Add TradeJournalEntry
* Add PerformanceAnalysisResult
* Add StrategyRecommendation
* Add StrategyRecommendationResult
* Add TradeJournalBuilder
* Add PerformanceAnalyzer
* Add StrategyRecommendationEngine
* Add trade journal builder regression test
* Add performance analyzer regression test
* Add strategy recommendation engine regression test
* Confirm ORION can evaluate its own paper trading behaviour
* Keep recommendations informational only
* Confirm no automatic config mutation

---

## Sprint 7E — Controlled Learning / Hypothesis Evaluation

* Add StrategyHypothesis
* Add HypothesisEvaluationContext
* Add HypothesisEvaluation
* Add HypothesisEvaluationReport
* Add HypothesisContextBuilder
* Add HypothesisEvaluator
* Add HypothesisEvaluationService
* Add HypothesisReportBuilder
* Integrate hypothesis findings into StrategyRecommendationEngine
* Add hypothesis evaluator regression tests
* Add hypothesis service/report regression tests
* Add recommendation-with-hypotheses regression test
* Confirm no automatic config mutation

---

## Sprint 7F — Deterministic Learning Pipeline

* Add StrategyIdea
* Add StrategyIdeaBuilder
* Add LearningPipelineResult
* Add LearningPipeline
* Add learning pipeline regression test
* Keep StrategyIdea as intent-only contract
* Do not generate concrete parameter values yet
* Do not create strategy variants automatically

---

## Sprint 8.1 — Persistent Paper Portfolio Infrastructure

* Add DataclassSerializer
* Add serializer regression tests
* Add PaperPortfolioRepository interface
* Add JsonPaperPortfolioRepository
* Add JSON portfolio repository regression test
* Make PaperTradingService repository-aware
* Add PaperTradingService persistence regression test
* Make AutonomousPaperTradingRunner load existing portfolio when repository exists
* Make AutonomousPaperTradingRunner save portfolio after cycles
* Add autonomous runner persistence regression test
* Add TradeJournalRepository interface
* Add JsonlTradeJournalRepository
* Add JSONL trade journal repository regression test

---

## Sprint 8.2 — Continuous Paper Trading Runner

* Add ContinuousRunnerConfig
* Add ContinuousPaperTradingRunResult
* Add ContinuousPaperTradingRunner
* Add continuous runner regression test
* Add run_continuous_paper_trading.py
* Reuse AutonomousPaperTradingRunner instead of duplicating trading logic
* Support Ctrl+C clean stop
* Support max_iterations for deterministic tests
* Support interval-based repeated runs

---

## Sprint 8.3 — Risk-Based Allocation + WatchlistService Routing

Completed so far:

* Increase LivePaperTradingConfig max_symbols for larger scans
* Raise max_open_positions as legacy safety cap
* Add max_position_size_pct
* Add max_portfolio_exposure
* Add min_cash_reserve_pct
* Update PortfolioAllocator to use:

  * available cash
  * cash reserve
  * max portfolio exposure
  * max position size percent
  * max nominal position value
  * legacy max open positions cap
* Update allocator regression test
* Route LivePaperMarketScanner through WatchlistService
* Remove duplicate _load_symbols logic from LivePaperMarketScanner
* Confirm full regression suite PASS

---

# CURRENT WORK

## Sprint 8.3 continued — Large Universe / Scalable Scanner Hardening

Priority:

```text
HIGH
```

Status:

```text
NEXT
```

Goal:

Prepare ORION to scan a broader universe safely and measurably before enabling long-running multi-week paper trading.

Current architectural rule:

```text
WatchlistService is the only source for symbol loading.
Do not create duplicate universe managers unless the repository clearly requires it.
```

Tasks:

* Confirm `data/universes/swing.csv` exists and contains the intended symbols.
* Confirm symbol count.
* Confirm `LivePaperTradingConfig.watchlist_path` points to the intended default universe.
* Confirm `LivePaperMarketScanner` uses WatchlistService only.
* Add scan duration measurement.
* Add scanned/failed/succeeded symbol metrics if not already sufficient.
* Profile sequential scan performance with:

  * 25 symbols
  * 100 symbols
  * 250 symbols
* Review YahooProvider for:

  * retry handling
  * timeout handling
  * caching
  * batching
  * large universe reliability
* Add provider tests with fake provider behaviour.
* Only consider bounded parallel scanning after baseline measurements are known.

Acceptance criteria:

```text
Full regression suite remains green.
Scanner source-of-truth is WatchlistService.
Large scan behaviour is measurable.
YahooProvider failure behaviour is explicit.
No duplicate watchlist/universe layer is introduced.
```

---

# REVIEW QUESTIONS

The next architecture review must answer:

* Is `data/universes/swing.csv` the correct primary universe file?
* Should `config/watchlist.txt` remain, be deprecated, or become a compatibility file?
* Should `LivePaperTradingConfig.watchlist_path` default to `data/universes/swing.csv`?
* Should `WatchlistService` support multiple universe files later?
* Should large universe scans remain sequential for now?
* When is parallel scanning justified?
* What is the safe maximum Yahoo request rate?
* Should YahooProvider support explicit timeout config?
* Should YahooProvider support retry count config?
* Should YahooProvider support local caching?
* Should scan duration be stored in a result model?
* Should `LivePaperTradingResult` include scan timing?
* Should `LivePaperTradingResult` still contain `executed_trades` and `rejected_trades`?
* Should `AutonomousPaperTradingResult` include richer execution detail?
* Should `TradeJournalBuilder` consume execution results instead of allocation decisions only?
* Should `JsonlTradeJournalRepository` be integrated directly into autonomous/continuous runs?
* Should current prices for open PaperPosition objects refresh every continuous iteration?
* Should position exits be triggered from stop-loss/targets during live cycles?
* Should continuous runner align scans to exact wall-clock times?
* Should market-hours awareness come before or after parallel scanning?

---

# PROBABLE NEXT SPRINTS

## Sprint 8.4 — Scan Metrics + YahooProvider Hardening

Potential goal:

Make large scans observable and reliable.

Potential tasks:

* Add scan timing fields to LivePaperTradingResult or new scanner metrics model.
* Add provider timeout handling.
* Add provider retry handling.
* Add fake provider regression tests.
* Add better symbol-level failure reporting.
* Add scan performance test with fake data.
* Keep scan sequential until measured.

---

## Sprint 8.5 — Market Scheduler

Potential goal:

Run ORION on fixed market-aware scan intervals.

Potential tasks:

* Add schedule config.
* Add market-hours service.
* Add wall-clock aligned scan loop.
* Skip weekends.
* Support US/EU market sessions.
* Print next scan time.
* Avoid uncontrolled background work by default.
* Add deterministic scheduler tests.

---

## Sprint 8.6 — Position Lifecycle for Long-Running Paper Trading

Potential goal:

Make multi-day paper positions more realistic.

Potential tasks:

* Refresh open position prices every cycle.
* Apply trailing stop updates during live cycles.
* Apply break-even updates during live cycles.
* Close positions on stop-loss hit.
* Close positions on target hit.
* Record close events in trade journal.
* Add position lifecycle regression tests.

---

## Sprint 8.7 — Parallel / Batched Scanner

Potential goal:

Scale ORION toward 300–800 instruments.

Only start after sequential scan metrics exist.

Potential tasks:

* Add bounded worker count.
* Add deterministic result ordering.
* Add timeout per symbol.
* Add failure aggregation.
* Avoid unbounded concurrent Yahoo calls.
* Add fake provider concurrency tests.

---

## Sprint 8.8 — Daily Reports / Equity Curve

Potential goal:

Make weeks-long paper-trading results analyzable.

Potential tasks:

* Add daily summary result.
* Add equity curve entries.
* Add daily report writer.
* Add JSON/CSV export.
* Add performance-over-time tests.

---

## Sprint 9 — Controlled Replay / Strategy Validation

Potential goal:

Validate strategy ideas using historical or paper-trading data before any configuration change is considered.

Potential tasks:

* Add ProposalGenerator.
* Add StrategyVariantProposalResult.
* Add ReplayEngine.
* Add StrategyComparisonResult.
* Compare current strategy vs candidate strategy.
* Keep auto-tuning disabled.

---

# IMPORTANT FUTURE WORK

## Portfolio Statistics

Goal:

Expand performance analytics.

Potential metrics:

* total return
* win rate
* average gain
* average loss
* profit factor
* expectancy
* max drawdown
* cash utilization
* exposure
* open position risk
* realized vs unrealized P/L

---

## Broker Compatibility

Planned only after paper trading proves stable.

Possible broker targets:

* Interactive Brokers
* Alpaca
* Saxo
* Trading212 research

Broker adapters may only execute deterministic orders.

Broker adapters may never calculate:

* BUY / SELL
* stop loss
* targets
* position size
* risk plan
* confidence

---

# DO NOT DO YET

* Do not connect a real broker.
* Do not enable automatic config mutation.
* Do not bypass TradingPipeline.
* Do not bypass RiskPlan.
* Do not bypass ExecutionValidator.
* Do not duplicate watchlist/universe-loading logic.
* Do not reintroduce dict pipeline contracts.
* Do not add parallel Yahoo scanning before baseline scan timing exists.
* Do not let AI decide trades or modify live configuration.
* Do not treat `max_open_positions` as the primary allocation mechanism.
* Do not create a second continuous runner that duplicates AutonomousPaperTradingRunner logic.

END OF FILE
