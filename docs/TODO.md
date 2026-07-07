# TODO.md

> Documentation Version: v1.16  
> Architecture Version: v2.8  
> Last Updated: 2026-07-07  
> Active Branch: fix/trading-config-indicators  
> Regression Status: 46 tests PASS

---

# PROJECT ORION TODO

Current state:

```text
Post-Sprint 7D

Current priority:

Full architecture review before Sprint 7E

Status:

STABLE / REVIEW REQUIRED

Regression status:

46 PASS
0 FAIL
COMPLETED
Sprint 5.9 — Advanced Position Management
 MarketStructure
 RiskContext
 AdaptiveRiskEngine V2
 ATR Stop Loss
 Risk Distance Targets
 RiskPlanValidator
 PositionState
 PositionStateFactory
 PositionUpdateEngine
 PositionManager
 BreakEvenService
 TrailingStopService
 TimeStopService
 PositionHealthService
 PositionStateStore
 PositionManagementSummary
 PositionManagementSummaryBuilder
Sprint 6 — Paper Trading Foundation
 ExecutionRequest
 ExecutionContext
 Order
 ExecutionResult
 ExecutionValidator
 OrderFactory
 ExecutionEngine
 PaperBroker
 PaperPortfolio
 PaperPosition
 PortfolioManager
 ExecutionReportBuilder
 TradingSession
 PaperTradingService
 PaperPositionUpdateService
 PaperPositionCloseService
 TradingCycle
 PaperTradingRunner
Sprint 6E — TradingPipelineResult Integration
 Define TradingPipelineResult
 Add typed pipeline result regression test
 Connect TradingPipeline output to typed paper flow
 Add PaperTradingPipelineAdapter
 Convert market data into IndicatorPack
 Run TradingPipeline automatically
 Pass typed pipeline result into TradingCycle
 Add typed paper trading flow test
 Add adapter regression test
Sprint 6F — Remove Legacy Pipeline Interface
 Remove pipeline_output
 Remove legacy_output
 Remove dict-style pipeline access
 Remove result["pipeline"]
 Remove .items(), .keys(), .values() compatibility
 Update MarketScanner to use typed result
 Update BacktestEngine to use typed result
 Update tests to typed-only contract
 Confirm full regression suite PASS
Sprint 7A — Deterministic Paper Trading Demo Runner
 Add PaperTradingDemoResult
 Add PaperTradingDemoRunner
 Add run_paper_trading_demo.py
 Add deterministic demo regression test
 Run synthetic end-to-end paper trading demo
Sprint 7B — Live Paper Market Scanner
 Confirm config/watchlist.txt exists
 Confirm watchlist contains 259 symbols
 Reuse existing watchlist
 Add LivePaperTradingConfig
 Add LivePaperCandidate
 Add LivePaperTradingResult
 Add LivePaperMarketScanner
 Add run_live_paper_trading.py
 Add live paper scanner regression test
 Support configurable max_symbols
 Use YahooProvider for historical data
 Produce ranked candidates from real market data
Sprint 7C — Autonomous Paper Trading Orchestration
 Split scanner from execution
 Add PortfolioAllocationDecision
 Add PortfolioAllocationResult
 Add PortfolioAllocator
 Add AutonomousPaperTradingConfig
 Add AutonomousPaperTradingCycleResult
 Add AutonomousPaperTradingResult
 Add AutonomousPaperTradingRunner
 Add run_autonomous_paper_trading.py
 Add portfolio allocator regression test
 Add autonomous runner regression test
 Preserve one TradingSession across multiple cycles
 Execute only approved allocation decisions
 Keep runner finite-run only
Sprint 7D — Self-Evaluation Layer
 Add TradeJournalEntry
 Add PerformanceAnalysisResult
 Add StrategyRecommendation
 Add StrategyRecommendationResult
 Add TradeJournalBuilder
 Add PerformanceAnalyzer
 Add StrategyRecommendationEngine
 Add trade journal builder regression test
 Add performance analyzer regression test
 Add strategy recommendation engine regression test
 Confirm ORION can evaluate its own paper trading behaviour
 Keep recommendations informational only
 Confirm no automatic config mutation
CURRENT WORK
Full Architecture Review

Priority:

CRITICAL

Status:

NEXT

Before starting Sprint 7E, perform a full repository review of branch:

fix/trading-config-indicators

The review must cover:

 current branch
 latest commits
 full repository structure
 all models
 all services
 all orchestration layers
 all tests
 all documentation
 dependencies
 data flows
 context/result patterns
 stores
 builders
 validators
 factories
 technical debt
 duplicate business logic
 circular dependencies
 public interface stability
 files likely to need future changes
 subsystem boundaries
 missing abstractions
 documentation/code mismatch
REVIEW QUESTIONS

The next architecture review must answer:

 Is LivePaperMarketScanner cleanly limited to scanning?
 Is PortfolioAllocator the correct place for capital allocation?
 Is AutonomousPaperTradingRunner too broad or still acceptable?
 Should LivePaperTradingResult still contain executed_trades and rejected_trades?
 Should allocation and execution be represented by separate result models?
 Should TradeJournalBuilder consume allocation decisions, execution results, or both?
 Should TradeJournal entries be persisted?
 Is TradeJournalEntry rich enough for future self-learning?
 Is unrealized P/L calculated from current market price or stale entry price?
 Should PaperPosition current prices refresh every cycle?
 Does YahooProvider need retry logic?
 Does YahooProvider need caching or batching before scanning all 259 symbols?
 Should autonomous trading become scheduled or remain finite-run for now?
 Should config become context-based per orchestrator?
 Are all public interfaces stable enough for Sprint 7E?
PROBABLE NEXT SPRINT

Do not start this until after the architecture review.

Sprint 7E — Controlled Learning / Hypothesis Evaluation

Potential goal:

Trade Journal
        ↓
Performance Analyzer
        ↓
Strategy Recommendation Engine
        ↓
Hypothesis Generator
        ↓
Controlled Paper/Replay Comparison
        ↓
Recommended Strategy Variant

Potential tasks:

 Define hypothesis model
 Define strategy variant model
 Define comparison result model
 Generate deterministic strategy hypotheses from recommendations
 Compare strategy variants without mutating production config
 Rank hypotheses by expected value
 Keep auto-tuning disabled by default
 Add regression tests

Important rule:

No automatic strategy mutation until controlled evaluation exists.
IMPORTANT FUTURE WORK
Persistent Trade Journal

Goal:

Store ORION's journal entries across runs.

Possible tasks:

 Define journal store interface
 Add file-based journal store
 Add CSV or JSONL export
 Add load historical journal entries
 Add journal replay analysis
 Add tests
Portfolio Statistics

Goal:

Expand performance analytics.

Potential metrics:

 total return
 win rate
 average gain
 average loss
 profit factor
 expectancy
 max drawdown
 cash utilization
 exposure
 open position risk
 realized vs unrealized P/L
Market Scheduler

Goal:

Run ORION periodically during market hours.

Potential tasks:

 Define schedule config
 Define market-hours service
 Add finite scheduled run
 Add daily report
 Prevent endless background process by default
 Add tests
Position Lifecycle Improvements

Goal:

Improve autonomous position management.

Potential tasks:

 Refresh open position prices
 Apply trailing stop updates during live cycles
 Apply break-even updates during live cycles
 Close positions on stop-loss hit
 Close positions on target hit
 Record close events in trade journal
 Add tests
YahooProvider Hardening

Goal:

Make large watchlist scans more reliable.

Potential tasks:

 Add retry handling
 Add timeout handling
 Add symbol failure reporting
 Add local cache
 Add batch strategy if supported
 Add tests with fake provider
Broker Compatibility

Planned only after paper trading proves stable.

Possible broker targets:

Interactive Brokers
Alpaca
Saxo
Trading212 research

Broker adapters may only execute deterministic orders.

Broker adapters may never calculate:

BUY / SELL
stop loss
targets
position size
risk plan
confidence
DO NOT DO YET
 Do not connect a real broker.
 Do not enable automatic config mutation.
 Do not create an infinite unattended trading loop.
 Do not bypass TradingPipeline.
 Do not bypass RiskPlan.
 Do not bypass ExecutionValidator.
 Do not duplicate watchlist files.
 Do not reintroduce dict pipeline contracts.
 Do not assume Sprint 7E is final before architecture review.

END OF FILE