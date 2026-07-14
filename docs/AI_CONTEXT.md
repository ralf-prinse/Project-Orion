# PROJECT ORION — AI CONTEXT

**Status:** Stable autonomous paper runtime; IBKR Paper integration started  
**Active branch:** `feature-ibkr-integration`  
**Stable validation tag:** `v0.9-paper-validation`  
**Regression baseline:** `75 passed, 0 failed`  
**Updated:** 2026-07-14

## Purpose

Read this document first when continuing Project Orion in a new development chat.

Then consult, only when relevant:

- `PROJECT_STATUS.md`
- `TODO.md`
- `ORION_MASTER_ARCHITECTURE.md`
- `TRADING_STRATEGY.md`
- `CHANGELOG.md`

Do not assume older sprint documents describe the current runtime.

## Mission

Project Orion is a deterministic trading system intended for short swing trades, normally held for no more than 24–48 hours.

Artificial Intelligence may explain and analyse deterministic results. It must not independently decide, approve, size, open, manage or close trades.

## Current State

The internal paper-trading runtime is operational and restart-safe.

Validated capabilities include:

- deterministic market scanning and decision flow;
- adaptive `RiskPlan` generation;
- opportunity ranking;
- portfolio allocation and paper execution;
- complete `TradingSession` persistence;
- managed position lifecycle;
- break-even and trailing-stop management;
- deterministic stop, target and 48-hour exits;
- restart and crash recovery;
- continuous execution with graceful shutdown;
- separate trade, decision and runtime-event journals;
- DST-aware European and United States market sessions;
- `MARKETS_IDLE` behaviour when every configured market is closed;
- central quote validation;
- rejection of `None`, `NaN`, infinity, zero and negative prices;
- preservation of the previous valid price after a bad quote.

## Canonical Runtime State

```text
TradingSession
├── PaperPortfolio
├── dict[str, PositionState]
└── dict[str, RiskPlan]

Rules:

TradingSession is the sole managed-position state owner.
TradingSessionRepository is the authoritative persistence boundary.
JsonPaperPortfolioRepository is only a compatibility mirror.
No second lifecycle store may be introduced.
Runtime data under data/ is not normal source code and should not be committed.
Active Runtime
ContinuousPaperTradingRunner
        ├── MarketSessionService
        ├── RuntimeSupervisor
        └── AutonomousPaperTradingRunner
                ↓
        TradingSessionRepository
                ↓
        TradingSession
                ↓
        Position update and management
                ↓
        PositionMonitor
                ↓
        ExitEngine

When all configured markets are closed:

MARKETS_IDLE
→ no scan
→ no price revaluation
→ no BUY or SELL
→ no failed iteration
→ periodic market-open check

European and United States sessions use IANA time zones, so daylight-saving transitions are not represented by hardcoded Dutch clock times.

Market-Data Safety

All prices entering the provider or position-update pipeline must be:

convertible to float;
finite;
greater than zero.

Invalid quotes are rejected per symbol. They must never make portfolio equity NaN or fail an entire iteration.

Journals
data/trade_journal.jsonl
- executed OPEN_POSITION
- executed CLOSE_POSITION

data/decision_journal.jsonl
- approved and rejected allocation decisions

data/runtime_events.jsonl
- runtime lifecycle
- completed and failed iterations
- market-idle events

These files contain runtime evidence and are not normally committed.

Current Paper Validation Profile

Current validation target:

starting capital: €10,000;
maximum open positions: 20;
maximum position value: approximately €500;
maximum holding period: 48 elapsed hours;
regular market sessions only;
internal PaperBroker;
strategy parameters frozen during clean comparison runs.

The purpose of this capital is rapid data collection. A later pre-live validation must be repeated with the intended live starting capital, currently approximately €500.

IBKR Status

Interactive Brokers is the intended external broker.

Completed:

IBKR account approved;
Paper Trading account active;
paper balance set to €10,000;
Trader Workstation installed;
TWS Paper connection configured on 127.0.0.1:7497;
socket clients enabled;
Read-Only API enabled;
official ibapi installed;
test_ibkr_connection.py passes;
test_ibkr_account_reader.py passes;
account cash, net liquidation and positions can be read.

Not yet completed:

production IbkrAccountService;
IBKR contract mapping;
market-data integration;
order-status and fill handling;
controlled IBKR paper order;
IbkrBroker.execute();
portfolio reconciliation;
autonomous execution through IBKR Paper.

TWS must remain in Read-Only mode until the explicit controlled-order milestone.

Existing Execution Architecture
ExecutionEngine
        ↓
broker.execute(order)

PaperBroker already implements the required execute() shape.

The intended next implementation is an IbkrBroker with the same practical interface. Do not build an unnecessary multi-broker plugin platform or large broker factory.

Non-Negotiable Development Rules
Inspect the complete relevant chain before changing code.
Reuse existing models and services.
Do not create duplicate decision, risk, execution or lifecycle owners.
Keep trading behaviour deterministic.
Keep GUI and presenters free of trading logic.
Prefer complete-file replacements for user-applied changes.
Add targeted tests for every behaviour change.
Run python run_tests.py after targeted tests.
Commit and push only after all tests pass.
Never allow new IBKR code to reach the live account during development.
Immediate Next Step

Before submitting any IBKR order:

extract the proven read-only account code from the test script into a production service;
map IBKR account and position data into Orion models;
test connect/read/disconnect behaviour with test doubles;
preserve TWS Read-Only mode;
then design one explicitly controlled IBKR Paper order test.
New Chat Opening Instruction

A new development chat must first:

inspect branch feature-ibkr-integration;
read this file and PROJECT_STATUS.md;
inspect the relevant execution and IBKR files;
confirm the current regression suite passes;
verify TWS is connected to Paper Trading, not Live;
propose one small commit before changing code.