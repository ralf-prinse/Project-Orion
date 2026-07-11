# PROJECT ORION — TRADING STRATEGY

**Status:** Deterministic engine operational  
**Updated:** 2026-07-11

## Mission

Orion supports swing-trading decisions through transparent deterministic rules. It does not predict markets and does not delegate decisions to AI.

## Principles

- capital preservation first;
- every position has a predefined `RiskPlan`;
- every result is reproducible;
- missing a trade is acceptable;
- uncontrolled losses are not;
- no duplicate trading logic;
- AI explains only.

## Deterministic Workflow

```text
Market Data
    ↓
Indicators and Analysis
    ↓
Signals
    ↓
BUY / HOLD / SELL
    ↓
Risk Validation
    ↓
Adaptive RiskPlan
    ↓
Portfolio Allocation
    ↓
Paper Execution
    ↓
Managed Position Lifecycle
    ↓
Deterministic Exit
```

## Entry

A position can open only after:

- deterministic BUY output;
- confidence and portfolio validation;
- accepted allocation;
- valid quantity;
- complete `RiskPlan`;
- successful paper execution.

## RiskPlan

Current lifecycle uses:

- entry price;
- stop loss;
- target 1;
- target 2;
- target 3;
- risk percentage;
- reward percentage;
- risk/reward ratio;
- confidence;
- notes.

## Position Lifecycle

```text
Open
→ update price
→ update highest price
→ activate break-even when rules are met
→ activate/update trailing stop
→ record target hits
→ evaluate exit
→ close
→ remove PositionState and RiskPlan
```

All lifecycle state is owned by `TradingSession` and persists across restarts.

## Exit Evaluation

Managed positions use persisted:

- current stop;
- target levels;
- target-hit flags;
- break-even state;
- trailing-stop state;
- deterministic exit reasons.

Legacy positions without complete lifecycle metadata may use the fixed-percentage fallback until deliberately migrated.

## Journals

- trade journal records executed opens and closes;
- decision journal records approved and rejected allocation decisions.

## Operational Rules

- no live broker orders;
- no real money;
- no AI decisions;
- no silent parameter changes;
- configuration changes require explicit review and validation.

## Success Criteria

A strategy is acceptable only when it is:

- deterministic;
- risk-bounded;
- explainable;
- regression tested;
- restart safe;
- operationally stable;
- measurable through actual trade outcomes.

# End
