# TODO.md

> Documentation Version: v1.14
> Last Updated: 2026-07-07

---

# PROJECT ORION

Current Sprint

Sprint 5.9 — Advanced Position Management

Overall Progress

████████████████████░ 90%

Regression Status

✅ ALL TESTS PASS

---

# SPRINT 5.9

## Completed

### Risk Engine

- [x] RiskContext
- [x] RiskContextBuilder
- [x] AdaptiveRiskEngine V2
- [x] ATR Stop-Loss
- [x] Risk Distance Targets
- [x] RiskPlanValidator

---

### Position Management

- [x] PositionState
- [x] PositionStateFactory
- [x] PositionUpdateEngine
- [x] PositionManager
- [x] BreakEvenService
- [x] TrailingStopService

---

### Architecture

- [x] MarketStructure introduced
- [x] RiskContext architecture
- [x] Position Management architecture
- [x] Runtime PositionState
- [x] Deterministic validation pipeline

---

# Remaining Sprint 5.9

## Position Management

### TimeStopService

Priority

HIGH

Purpose

Close trades that remain inactive for too long.

Planned Features

- Maximum holding period
- Adaptive holding period
- Trade Horizon support

---

### PositionHealthService

Priority

HIGH

Purpose

Determine the health of an open position.

Metrics

- Trend
- Momentum
- ATR
- Distance to Stop
- Distance to Target
- Confidence

Output

- Healthy
- Neutral
- Weak
- Critical

---

### PositionStateStore

Priority

MEDIUM

Purpose

Central runtime storage of PositionState objects.

Future Responsibilities

- Live monitoring
- Paper Trading
- Broker synchronization

---

### TradeLifecycle Integration

Priority

HIGH

Integrate

- PositionManager

Into

- TradeLifecycleService

---

# Sprint 6

Paper Trading

Priority

VERY HIGH

Modules

- Paper Portfolio
- Paper Orders
- Simulated Broker
- Daily Portfolio Updates
- Portfolio Statistics
- PositionManager Integration

---

# Sprint 6.1

Portfolio Intelligence

Planned

- Portfolio Heat
- Exposure
- Sector Allocation
- Risk Allocation
- Drawdown Analysis

---

# Sprint 6.2

Broker Compatibility

Planned

- Broker Adapter
- Order Translation
- Position Synchronization
- Account Synchronization

Supported Brokers

- Interactive Brokers
- Alpaca
- Trading212 (research)
- Others (future)

---

# Sprint 7

Autonomous Trading

Long-Term Goal

The user defines

- Initial capital
- Maximum risk
- Markets
- Trading universe

Orion autonomously

- scans markets
- opens trades
- manages positions
- protects capital
- compounds returns

using deterministic trading rules.

---

# Documentation

Before every new sprint

Required

- [ ] AI_CONTEXT.md
- [ ] PROJECT_STATUS.md
- [ ] TODO.md
- [ ] CHANGELOG.md
- [ ] ORION_MASTER_ARCHITECTURE.md

must always be synchronized with the GitHub repository.

---

END OF FILE