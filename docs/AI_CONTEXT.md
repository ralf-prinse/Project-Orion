# PROJECT ORION — AI CONTEXT

**Status:** Stable autonomous IBKR Paper trading platform  
**Active branch:** `feature-ibkr-integration`  
**Regression baseline:** `88 passed, 0 failed`  
**Updated:** 2026-07-16

---

# Purpose

Read this document first before continuing development.

Then consult:

1. PROJECT_STATUS.md
2. TODO.md
3. ORION_MASTER_ARCHITECTURE.md
4. CHANGELOG.md

Older sprint documents and archived notes are historical only.

---

# Mission

Project Orion is a deterministic swing-trading platform.

Artificial Intelligence assists with:

- market analysis;
- hypothesis generation;
- opportunity ranking;
- confidence estimation.

Artificial Intelligence does **not** autonomously invent trading rules.

Trading decisions remain fully deterministic and reproducible.

---

# Current Development Phase

Project Orion has completed the complete BUY execution chain using Interactive Brokers Paper Trading.

The system can now autonomously:

- scan markets;
- analyse opportunities;
- calculate deterministic risk;
- allocate capital;
- submit IBKR Paper BUY orders;
- reconcile broker fills;
- synchronize TradingSession with broker truth;
- persist runtime state;
- recover after restart.

The BUY side is considered feature complete.

Current focus has shifted to autonomous position management and SELL execution.

---

# Current Runtime

ContinuousPaperTradingRunner

↓

AutonomousPaperTradingRunner

↓

TradingPipeline

↓

PortfolioAllocator

↓

ExecutionEngine

↓

IbkrBroker

↓

IbkrOrderTransport

↓

Interactive Brokers Paper

↓

TradingSessionSyncService

↓

TradingSessionRepository

---

# Canonical Runtime State

TradingSession is the only authoritative runtime object.

TradingSession owns:

- PaperPortfolio
- PositionState
- RiskPlan

No duplicated lifecycle state may exist elsewhere.

Repositories are persistence only.

Broker state always overrides local assumptions.

---

# Completed

## Trading Engine

- deterministic scanner
- market intelligence
- signal fusion
- adaptive risk engine
- opportunity ranking
- portfolio allocation
- execution pipeline

## Paper Trading

Completed:

- PaperBroker
- TradingSession persistence
- runtime supervisor
- restart recovery
- trade journal
- runtime journal
- portfolio persistence

## Interactive Brokers

Completed:

- account service
- portfolio mapper
- portfolio service
- execution service
- broker implementation
- order transport
- managed account validation
- paper-only protection
- late fill reconciliation
- broker synchronization
- continuous IBKR runner
- autonomous BUY validation

Validated using a real IBKR Paper account.

---

# Validation Status

Current regression baseline:

88 passed
0 failed

Validated:

- BUY execution
- broker synchronization
- late fills
- continuous runtime
- TradingSession persistence
- restart safety

---

# Not Yet Implemented

The remaining major milestone is the autonomous position lifecycle.

Remaining work:

- SELL execution through IBKR
- autonomous exit engine
- stop loss execution
- take profit execution
- trailing stop execution
- break-even execution
- time stop execution
- closed trade analytics
- AI learning feedback loop

---

# Architectural Rules

Always preserve:

TradingPipeline

↓

PortfolioAllocator

↓

ExecutionEngine

↓

Broker

↓

Broker Truth Synchronization

↓

TradingSession

Never update portfolio state manually after execution.

IBKR remains the single source of truth.

---

# Development Principles

- deterministic first
- test driven
- regression safe
- broker truth over local state
- repositories never contain business logic
- services remain single responsibility
- architecture before optimisation

---

# Immediate Next Goal

Sprint 11

Autonomous Position Lifecycle

Deliver:

- complete SELL execution
- broker synchronization after SELL
- autonomous position monitoring
- full end-to-end trade lifecycle

BUY functionality is considered complete unless regressions are discovered.