# ORION_MASTER_ARCHITECTURE.md

> Documentation Version: v1.16  
> Architecture Version: v2.8  
> Last Updated: 2026-07-07  
> Active Branch: fix/trading-config-indicators  
> Regression Status: 46 tests PASS

---

# PROJECT ORION MASTER ARCHITECTURE

This document defines the current high-level architecture of Project Orion.

The repository remains the primary source of truth.  
If this document and the code disagree, the code wins.

Before starting any new sprint, the full repository must be reviewed.

---

# DESIGN PHILOSOPHY

Orion is a deterministic, modular, AI-assisted swing trading and paper-trading system.

Primary goals:

- deterministic
- modular
- explainable
- testable
- broker-independent
- paper-first
- safe to extend
- AI-assisted, not AI-controlled

AI may assist with:

- explanation
- summarization
- performance analysis
- recommendations
- strategy review

AI may never directly and non-deterministically generate:

- BUY decisions
- SELL decisions
- stop-loss values
- targets
- risk sizing
- broker execution
- automatic config mutation

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

Rules:

One clear responsibility per service.
One immutable Result object per orchestrator.
Business logic belongs in services.
Models remain lightweight.
No duplicated business logic.
No circular dependencies.
No anonymous dict contracts between major subsystems.
Regression tests are mandatory.
Documentation must be updated after completed sprints.
Real broker integration is forbidden until paper trading proves stable.
CURRENT SYSTEM OVERVIEW
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
PaperBroker
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
IMPLEMENTED SUBSYSTEMS
1. Market Data

Purpose:

Provide market data to the rest of Orion.

Main components:

providers/base_provider.py
providers/yahoo_provider.py
models/market_data.py

Current provider:

YahooProvider

Capabilities:

get current price
get current market data
get historical OHLCV data

Current dependency:

yfinance

Important limitation:

YahooProvider currently needs review for:

retry logic
timeout handling
caching
batching
large watchlist reliability
2. Watchlist

Main file:

config/watchlist.txt

Current status:

259 symbols

Contains:

US equities
US ETFs
Dutch .AS tickers
German .DE tickers

Rule:

Do not duplicate the watchlist unless there is a strong architectural reason.

3. Indicator / Pipeline Adapter

Purpose:

Convert historical market data into pipeline-ready indicator input.

Main components:

services/paper_trading_pipeline_adapter.py
services/indicator_builder.py
services/intelligence/intelligence_models.py

Flow:

Historical OHLCV Data
        ↓
IndicatorBuilder
        ↓
IndicatorPack
        ↓
TradingPipeline
4. Market Analysis / Trading Pipeline

Purpose:

Analyze market conditions and produce deterministic trading decisions.

Main components:

services/orchestration/trading_pipeline.py
models/trading_pipeline_result.py
services/intelligence/signal_fusion_engine.py
services/intelligence/market_intelligence_engine.py
services/intelligence/ai_context_builder.py
services/intelligence/ai_explainer.py
services/decision/adaptive_decision_engine.py
services/decision/position_sizing.py

Output:

TradingPipelineResult

Important rule:

TradingPipelineResult is the only valid contract between TradingPipeline and downstream systems.

Forbidden legacy patterns:

pipeline_output
legacy_output
result["pipeline"]
result.items()
result.keys()
result.values()
5. Risk Engine

Purpose:

Convert market and decision context into a deterministic RiskPlan.

Main components:

models/risk_plan.py
services/risk/risk_context_builder.py
services/risk/adaptive_risk_engine.py
services/risk/risk_plan_validator.py

Responsibilities:

entry price
stop loss
targets
risk percent
reward percent
risk/reward ratio
confidence
notes
validation

The Risk Engine must not:

fetch market data
execute trades
mutate portfolio state
6. Execution Layer

Purpose:

Convert deterministic trading requests into validated paper executions.

Main components:

models/execution_request.py
models/execution_context.py
models/execution_result.py
services/execution_validator.py
services/order_factory.py
services/execution_engine.py
services/execution_report_builder.py
services/paper_broker.py

Flow:

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

Execution validation rejects:

missing symbol
non-positive entry price
non-positive quantity
non-positive confidence
insufficient cash
excessive position allocation

The Execution Layer must never generate BUY/SELL decisions.

7. Paper Trading Foundation

Purpose:

Simulate trades with paper money.

Main components:

models/paper_portfolio.py
models/paper_position.py
models/trading_session.py
services/paper_trading_service.py
services/paper_position_update_service.py
services/paper_position_close_service.py
services/portfolio_manager.py

Responsibilities:

maintain cash
maintain equity
maintain positions
open paper positions
update paper positions
close paper positions

The Paper Trading subsystem must not:

scan markets
calculate indicators
generate trading decisions
8. Position Management

Purpose:

Manage already opened positions.

Main components:

models/position_state.py
services/position_state_factory.py
services/position_state_store.py
services/position_update_engine.py
services/position_manager.py
services/break_even_service.py
services/trailing_stop_service.py
services/time_stop_service.py
services/position_management_summary_builder.py

Responsibilities:

break-even logic
trailing stop logic
time stop logic
health updates
position state updates
position management summaries

Position Management must not:

open new trades
generate BUY signals
fetch market data directly
9. Trading Cycle

Purpose:

Execute one deterministic trading tick.

Main components:

models/market_snapshot.py
services/trading_cycle.py
models/trading_cycle_result.py

Input:

TradingSession + MarketSnapshot + quantity

Output:

TradingCycleResult

Responsibilities:

open positions when approved
update positions
close positions where applicable
return updated TradingSession

TradingCycle must not:

calculate indicators
rank candidates
allocate portfolio capital
10. Paper Trading Runner

Purpose:

Run multiple deterministic TradingCycles.

Main components:

services/paper_trading_runner.py
models/paper_trading_run_result.py

Responsibilities:

execute multiple TradingCycles
preserve TradingSession
collect cycle results
11. Paper Trading Demo Runner

Purpose:

Provide deterministic end-to-end demo without external data.

Main components:

models/paper_trading_demo_result.py
services/paper_trading_demo_runner.py
run_paper_trading_demo.py

Command:

python run_paper_trading_demo.py

This proves the software architecture works without relying on Yahoo Finance.

12. Live Paper Market Scanner

Purpose:

Scan live market data and produce ranked candidates.

Main components:

models/live_paper_trading_config.py
models/live_paper_trading_result.py
services/live_paper_market_scanner.py
run_live_paper_trading.py

Responsibilities:

load watchlist
fetch historical market data
run PaperTradingPipelineAdapter
produce LivePaperCandidate objects
rank candidates

Important rule:

LivePaperMarketScanner scans only.

It must not:

allocate capital
execute trades
mutate TradingSession
place broker orders
13. Portfolio Allocator

Purpose:

Choose which ranked candidates may receive paper capital.

Main components:

models/portfolio_allocation_result.py
services/portfolio_allocator.py

Responsibilities:

sort candidates by score
reject non-accepted candidates
reject already-open positions
respect max open positions
respect available cash
respect max position value
calculate integer quantity
explain allocation decision

The allocator must not:

fetch market data
run the TradingPipeline
execute trades
mutate TradingSession
14. Autonomous Paper Trading Runner

Purpose:

Run multiple live paper cycles while preserving one TradingSession.

Main components:

models/autonomous_paper_trading_config.py
models/autonomous_paper_trading_result.py
services/autonomous_paper_trading_runner.py
run_autonomous_paper_trading.py

Responsibilities:

create one TradingSession
run LivePaperMarketScanner
run PortfolioAllocator
execute approved allocations through TradingCycle
preserve session across cycles
return AutonomousPaperTradingResult

Current status:

Finite-run only

This is intentional.

No infinite unattended loop exists yet.

Command:

python run_autonomous_paper_trading.py
15. Self-Evaluation Layer

Purpose:

Allow ORION to evaluate its own paper-trading behaviour.

Main components:

models/trade_journal_entry.py
models/performance_analysis_result.py
models/strategy_recommendation.py
services/trade_journal_builder.py
services/performance_analyzer.py
services/strategy_recommendation_engine.py

Flow:

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

Current capabilities:

journal entry creation
win/loss analysis
realized P/L analysis
unrealized P/L analysis
average confidence
average expected risk
dominant regime
dominant volatility
strategy recommendations

Important safety rule:

Recommendations are informational only.

No automatic configuration mutation is currently allowed.

CURRENT OPERATIONAL COMMANDS

Run all tests:

python run_tests.py

Run deterministic paper demo:

python run_paper_trading_demo.py

Run live paper scanner:

python run_live_paper_trading.py

Run autonomous finite paper trading:

python run_autonomous_paper_trading.py
CURRENT TEST STATUS

Current regression suite:

46 tests PASS

Health:

ORION HEALTH: EXCELLENT
CURRENT ARCHITECTURE STATUS

The current architecture is stable enough to run finite autonomous paper-trading experiments.

However, before any Sprint 7E work begins, the full repository must be reviewed.

Reason:

Sprint 6E through 7D introduced many important layers:

typed pipeline result
live market scanning
portfolio allocation
autonomous runner
self-evaluation

This is the correct moment to check for technical debt before adding controlled learning.

KNOWN REVIEW TARGETS

The next architecture review must check:

Full project structure.
All models.
All services.
Orchestration layers.
Tests.
Documentation.
Dependencies.
Data flows.
Context/result patterns.
Stores.
Builders.
Validators.
Factories.
Duplicate business logic.
Circular dependencies.
Public interface stability.
Future change hotspots.
Whether result models are still clean.
Whether scanner/allocator/runner separation is correct.
Whether TradeJournalBuilder records enough execution detail.
Whether persistent journal storage is needed.
Whether open position prices are refreshed correctly.
Whether YahooProvider needs hardening.
Whether autonomous runner needs market-hours awareness.
Whether controlled learning should be the next sprint.
CURRENT TECHNICAL DEBT

Known items to review:

LivePaperTradingResult

Currently contains:

executed_trades
rejected_trades

But after Sprint 7C, scanner no longer executes trades.

Review whether these fields should remain, move, or be removed.

TradeJournalBuilder

Currently builds entries from autonomous allocation decisions.

Review whether it should also record explicit execution result details.

PaperPosition Price Updates

Review whether current prices are refreshed sufficiently across live cycles.

YahooProvider

Needs review for:

retries
caching
batching
timeouts
rate-limit resilience
Persistent State

Currently missing:

persistent journal store
persistent portfolio/session store
long-term performance history
Scheduler

Currently missing:

market-hours awareness
periodic scheduled finite run
daily report
DEVELOPMENT PHASES
Level 1 — Deterministic Paper Trading

Status:

Complete

Includes:

TradingPipeline
Risk Engine
Execution Engine
Paper Broker
Paper Portfolio
Position Management
Trading Cycle
Paper Trading Runner
Level 2 — Typed Pipeline Integration

Status:

Complete

Includes:

TradingPipelineResult
typed-only downstream flow
removal of legacy dict compatibility
Level 3 — Live Paper Trading

Status:

Complete

Includes:

YahooProvider
config/watchlist.txt
LivePaperMarketScanner
LivePaperTradingConfig
live paper CLI
Level 4 — Portfolio Allocation

Status:

Complete

Includes:

PortfolioAllocator
PortfolioAllocationDecision
PortfolioAllocationResult
Level 5 — Autonomous Finite Paper Trading

Status:

Complete

Includes:

AutonomousPaperTradingRunner
AutonomousPaperTradingConfig
AutonomousPaperTradingResult
multi-cycle session preservation
Level 6 — Self-Evaluation

Status:

Complete

Includes:

TradeJournalEntry
TradeJournalBuilder
PerformanceAnalyzer
StrategyRecommendationEngine
Level 7 — Controlled Learning

Status:

Not started

Potential future architecture:

Trade Journal
        ↓
Performance Analysis
        ↓
Recommendations
        ↓
Hypothesis Generator
        ↓
Strategy Variant Comparison
        ↓
Approved Recommendation

Important rule:

No automatic strategy mutation until controlled hypothesis evaluation exists and is regression-tested.

Level 8 — Scheduled Paper Trading

Status:

Not started

Potential future capabilities:

market-hours service
periodic finite runs
daily report
persistent state
no uncontrolled infinite loop by default
Level 9 — Broker Abstraction / Real Broker

Status:

Not started

Possible future broker adapters:

Interactive Brokers
Alpaca
Saxo
Trading212 research

Rule:

Broker adapters may only execute deterministic orders.

Broker adapters may never calculate:

BUY / SELL
stop loss
targets
position size
risk plan
confidence
DO NOT VIOLATE

Do not:

reintroduce dict pipeline contracts
bypass TradingPipeline
bypass RiskPlan
bypass ExecutionValidator
combine scanner, allocator and runner responsibilities again
let AI mutate trading config automatically
connect real broker before paper trading proves stable
create infinite unattended loops without explicit design
duplicate watchlist files
start Sprint 7E before full review
NEXT REQUIRED ACTION

The next chat/session must begin with a full repository analysis of branch:

fix/trading-config-indicators

It must not assume Sprint 7E is automatically correct.

It must first analyse:

branch
commits
project structure
models
services
orchestration layers
tests
docs
architecture
dependencies
data flows
stores
builders
validators
factories
technical debt
code smells
missing abstractions
unstable interfaces

Only after that should the next sprint be proposed.

END OF FILE