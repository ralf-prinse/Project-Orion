# AI_CONTEXT.md

> Documentation Version: v1.16  
> Architecture Version: v2.8  
> Last Updated: 2026-07-07  
> Active Branch: fix/trading-config-indicators  
> Regression Status: 46 tests PASS

---

# PROJECT ORION

## Mission

Project Orion is a deterministic, modular swing trading and paper-trading platform.

The long-term objective is to operate as an autonomous paper-trading system first, and only later as a real broker-connected trading system if the strategy proves itself.

Project Orion must remain:

- deterministic
- explainable
- testable
- broker-independent
- modular
- AI-assisted, never uncontrolled by AI

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
One orchestrator
        ↓
One immutable Result output

Existing examples:

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

Business logic belongs in services.

Models must remain lightweight data contracts.

No duplicated business logic.

No circular dependencies.

No uncontrolled AI behaviour.

Regression tests are mandatory after every logical step.

CURRENT SYSTEM STATUS
Regression

Current full regression suite:

46 tests PASS

Project health:

ORION HEALTH: EXCELLENT
COMPLETED SUBSYSTEMS
Market Analysis

Status: Complete.

Contains:

Market Scanner
AI Market Scanner
AI Scanner Presenter
Signal Fusion
Market Intelligence
IndicatorBuilder
TradingPipeline
TradingPipelineResult

Produces:

deterministic trading decisions
confidence
position sizing
risk plan
AI context
AI explanation

Important architectural note:

TradingPipelineResult is now the typed contract between the TradingPipeline and downstream layers.

Legacy dictionary compatibility has been removed.

No pipeline_output.

No legacy_output.

No result["pipeline"].

No .items() compatibility.

Trading Pipeline Integration

Status: Complete.

The pipeline now feeds typed downstream paper-trading flow.

Current typed route:

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

The old anonymous dictionary contract is removed.

Risk Engine

Status: Complete.

Contains:

RiskContext
RiskContextBuilder
AdaptiveRiskEngine
ATR-based risk planning
RiskPlan
RiskPlanValidator

Produces:

deterministic RiskPlan
stop loss
targets
risk percent
reward percent
risk/reward ratio
confidence
notes
Execution Layer

Status: Complete.

Contains:

ExecutionRequest
ExecutionContext
ExecutionValidator
OrderFactory
ExecutionEngine
PaperBroker
ExecutionReportBuilder

Produces:

ExecutionEngineResult
deterministic validation
deterministic order creation
paper broker execution
updated paper portfolio snapshot

Important behaviour:

Execution validation rejects invalid orders, including:

missing symbol
non-positive entry price
non-positive quantity
non-positive confidence
insufficient cash
excessive position allocation
Paper Trading Foundation

Status: Complete.

Contains:

PaperPortfolio
PaperPosition
TradingSession
PaperTradingService
PaperPositionUpdateService
PaperPositionCloseService
PaperTradingRunner
PaperTradingRunResult

Supports:

paper BUY/open position
paper position update
paper close
multi-cycle deterministic replay
session-level cash/equity/open-position tracking
Position Management

Status: Complete.

Contains:

PositionManager
PositionUpdateEngine
BreakEvenService
TrailingStopService
TimeStopService
PositionState
PositionStateFactory
PositionStateStore
PositionManagementSummary
PositionManagementSummaryBuilder

Supports:

break-even management
trailing stop management
time stop management
position state updates
position health summaries
Live Market Data

Status: Available.

Current provider:

YahooProvider
BaseMarketProvider

Supports:

current market data
historical OHLCV data
configurable period and interval

Important file:

providers/yahoo_provider.py

Current live data dependency:

yfinance
Watchlist

Status: Available.

Main watchlist:

config/watchlist.txt

Contains:

259 symbols

The watchlist includes:

US equities
US ETFs
Dutch .AS tickers
German .DE tickers

Examples:

AAPL
MSFT
NVDA
ASML
SPY
QQQ
ASML.AS
INGA.AS
SAP.DE
BMW.DE

This file must be reused for live paper trading.

Do not create a duplicate watchlist unless there is a strong architectural reason.

Paper Trading Demo Runner

Status: Complete.

Contains:

PaperTradingDemoResult
PaperTradingDemoRunner
run_paper_trading_demo.py

Purpose:

deterministic end-to-end paper trading demo
synthetic market history
no external API dependency
proves architecture works without live data

Command:

python run_paper_trading_demo.py
Live Paper Market Scanner

Status: Complete.

Contains:

LivePaperTradingConfig
LivePaperCandidate
LivePaperTradingResult
LivePaperMarketScanner
run_live_paper_trading.py

Current responsibility:

load symbols from config/watchlist.txt
download historical market data through YahooProvider
run PaperTradingPipelineAdapter
produce ranked candidates

Important architectural rule after Sprint 7C:

LivePaperMarketScanner scans only.

It must not:

allocate portfolio capital
execute trades
mutate TradingSession
place real broker orders
Portfolio Allocator

Status: Complete.

Contains:

PortfolioAllocationDecision
PortfolioAllocationResult
PortfolioAllocator

Responsibility:

select accepted BUY candidates
respect available cash
respect max open positions
respect max position value
calculate integer quantities
explain approval/rejection

It must not:

fetch market data
run TradingPipeline
execute trades
mutate TradingSession
Autonomous Paper Trading Runner

Status: Complete.

Contains:

AutonomousPaperTradingConfig
AutonomousPaperTradingCycleResult
AutonomousPaperTradingResult
AutonomousPaperTradingRunner
run_autonomous_paper_trading.py

Responsibility:

preserve one TradingSession across multiple cycles
call LivePaperMarketScanner
call PortfolioAllocator
execute approved allocations through TradingCycle
return immutable autonomous result

Current runner is finite.

It does not run forever.

This is intentional.

Command:

python run_autonomous_paper_trading.py
Self-Evaluation Layer

Status: Complete.

Contains:

TradeJournalEntry
PerformanceAnalysisResult
StrategyRecommendation
StrategyRecommendationResult
TradeJournalBuilder
PerformanceAnalyzer
StrategyRecommendationEngine

Purpose:

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

This is the first foundation for ORION learning from its own behaviour.

Important safety rule:

The recommendation engine is informational only.

It must not automatically modify config.

No auto-tuning is currently allowed.

CURRENT HIGH-LEVEL FLOW

The current full architecture is:

config/watchlist.txt
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
LivePaperMarketScanner
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
TradeJournalBuilder
        ↓
PerformanceAnalyzer
        ↓
StrategyRecommendationEngine
IMPORTANT ARCHITECTURAL DECISIONS
Scanner / Allocator / Runner Separation

Sprint 7C introduced a key architecture improvement.

Responsibilities are now separated:

LivePaperMarketScanner = scan and rank
PortfolioAllocator = choose what can be bought
AutonomousPaperTradingRunner = orchestrate cycles and execute approved trades

This prevents LivePaperMarketScanner from becoming too broad.

Do not collapse these responsibilities back into one service.

Typed-Only Pipeline

The pipeline is now typed-only.

Use:

TradingPipelineResult

Do not reintroduce anonymous dictionaries as pipeline contracts.

Paper Before Real Broker

ORION must prove itself with paper money before any real broker integration.

Current paper capital examples:

€500 paper cash
max 25 symbols per run initially
max 3 open positions
max €150 per position
minimum confidence 0.75

These are configuration values, not hard-coded strategy laws.

CURRENT TECHNICAL DEBT / REVIEW TARGETS

A full architecture review is required before Sprint 7E.

Review targets:

Confirm all new live/autonomous/self-evaluation services have clean boundaries.
Check whether LivePaperTradingResult should keep executed_trades and rejected_trades now that the scanner no longer executes.
Check whether autonomous paper trading needs a persistent journal store.
Check whether TradeJournalBuilder should record only allocation decisions or also execution results.
Check whether current unrealized P/L handling is sufficient.
Check if portfolio position prices should be refreshed every autonomous cycle.
Check if market-hours awareness is needed before longer live paper sessions.
Check if YahooProvider needs batching, caching or retry handling before scanning all 259 symbols.
Check if config objects should move toward explicit Context objects per orchestrator.
Check whether recommendation output should feed a future Hypothesis Generator rather than direct config mutation.
NEXT RECOMMENDED STEP

Do not start Sprint 7E immediately.

First perform a full architecture review of the current branch:

fix/trading-config-indicators

The review must cover:

complete project structure
all models
all services
orchestration layers
tests
documentation
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

Only after that review should the next sprint be selected.

Likely direction after review:

Sprint 7E — Controlled Learning / Hypothesis Evaluation

Possible future flow:

Trade Journal
        ↓
Performance Analysis
        ↓
Recommendations
        ↓
Hypothesis Generator
        ↓
Replay / Paper comparison
        ↓
Approved strategy changes

But this must not be assumed before repository analysis.

DEVELOPMENT RULES

Never bypass existing engines.

Never duplicate logic.

Never reintroduce legacy dict contracts.

Every subsystem must have:

models
services
tests

Regression tests must pass before every commit.

Architecture changes must be documented.

Use repository code as the source of truth.

Work from the current branch.

Do not assume an older sprint plan remains correct.

CURRENT PROJECT HEALTH

Architecture:

Stable, but ready for review

Regression:

46 tests PASS

Execution Layer:

Complete

Paper Trading:

Operational

Live Paper Trading:

Operational, finite-run

Autonomous Paper Trading:

Operational, finite-run

Self-Evaluation:

Operational, recommendation-only

Next focus:

Full architecture review before Sprint 7E

END OF FILE