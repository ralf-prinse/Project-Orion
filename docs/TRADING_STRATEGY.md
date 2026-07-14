# PROJECT ORION — TRADING STRATEGY

**Status:** Active Paper Validation  
**Updated:** 2026-07-14

---

# Strategy Objective

Project Orion executes deterministic swing trades with an intended holding period of approximately **24–48 hours**.

The objective is consistent, explainable and risk-controlled trading rather than maximizing trade frequency.

Missing a trade is acceptable.

Taking uncontrolled risk is not.

---

# Trading Philosophy

Every position must satisfy all deterministic requirements before execution.

No trade may exist without:

- deterministic BUY decision;
- validated market data;
- complete RiskPlan;
- approved portfolio allocation;
- predefined exit conditions.

Artificial Intelligence never participates in trade approval.

---

# Trading Pipeline

```text
Market Data
        ↓
Quote Validation
        ↓
Indicators
        ↓
Analysis
        ↓
Signals
        ↓
BUY / HOLD / SELL
        ↓
Adaptive RiskPlan
        ↓
Portfolio Allocation
        ↓
Execution
        ↓
Managed Position
        ↓
Exit
```

Every stage has exactly one owner.

---

# Market Data

Trading begins only after quote validation.

Every price must be:

- finite;
- greater than zero;
- not NaN;
- not None.

Invalid quotes are rejected before entering the strategy.

---

# Entry Conditions

A position may open only when:

- deterministic BUY;
- sufficient confidence;
- allocation approved;
- quantity greater than zero;
- RiskPlan complete;
- execution succeeds.

No discretionary override exists.

---

# RiskPlan

Every position receives a deterministic RiskPlan containing:

- entry price;
- stop loss;
- target 1;
- target 2;
- target 3;
- expected risk;
- expected reward;
- risk/reward ratio;
- confidence;
- supporting notes.

The RiskPlan is immutable after entry except for managed stop adjustments.

---

# Position Management

After entry Orion manages:

- current price;
- highest price;
- break-even activation;
- trailing stop;
- target progress;
- holding time.

TradingSession owns all lifecycle state.

---

# Exit Conditions

A position closes only through deterministic rules.

Possible exit reasons include:

- stop loss;
- target reached;
- trailing stop;
- maximum holding time;
- other deterministic lifecycle conditions.

No manual AI exit exists.

---

# Market Sessions

Trading only occurs while configured exchanges are open.

Features:

- European sessions;
- United States sessions;
- daylight-saving aware;
- automatic idle mode.

When every configured market is closed:

- no new scans;
- no new positions;
- no portfolio updates;
- runtime remains healthy.

---

# Portfolio Rules

Current validation profile:

- maximum 20 positions;
- approximately €500 per position;
- maximum 90% exposure;
- minimum cash reserve;
- deterministic allocation.

These limits exist to collect statistically useful paper-trading data while controlling portfolio risk.

---

# Journaling

Every important event is recorded.

Trade Journal

- opened positions;
- closed positions.

Decision Journal

- accepted allocations;
- rejected allocations.

Runtime Events

- runtime lifecycle;
- failures;
- idle transitions.

---

# Current Broker

Current execution backend:

```text
PaperBroker
```

Interactive Brokers Paper integration is under development.

The strategy itself must remain unchanged.

Only the execution backend will be replaced.

---

# Validation Policy

During validation:

- no indicator tuning;
- no strategy tuning;
- no ranking adjustments;
- no exit tuning.

Only stability and correctness fixes are allowed.

---

# Success Criteria

The strategy is considered production-ready only when it is:

- deterministic;
- reproducible;
- regression tested;
- restart safe;
- operationally stable;
- successfully validated through extensive paper trading.

Only then may live deployment be considered.

# End