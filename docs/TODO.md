# PROJECT ORION — TODO

**Branch:** `feature-ibkr-integration`  
**Updated:** 2026-07-14

---

# Current Phase

Sprint 9.3 — Interactive Brokers Paper Integration

The deterministic paper engine is considered operational.

Current work focuses exclusively on integrating Interactive Brokers Paper Trading without changing trading behaviour.

---

# Highest Priority

## IBKR Integration

### 1. Production Account Service

Status:

IN PROGRESS

Goal:

Replace the validated test account reader with a production-quality `IbkrAccountService`.

Requirements:

- connect;
- read account;
- read positions;
- map to Orion models;
- disconnect cleanly;
- full regression coverage.

---

### 2. IbkrBroker

Status:

NOT STARTED

Implement a production broker using the existing execution architecture.

The broker must:

- submit paper orders;
- receive execution status;
- receive fills;
- report failures;
- return Orion execution models.

---

### 3. Controlled Paper Order

Status:

NOT STARTED

Submit one intentionally controlled paper BUY order.

Validation:

- order accepted;
- fill received;
- position visible;
- Orion state updated;
- no duplicate execution.

---

### 4. Portfolio Synchronization

Status:

NOT STARTED

Synchronize:

- IBKR positions;
- Orion positions;
- account balances;
- execution results.

Detect inconsistencies before trading continues.

---

### 5. Continuous IBKR Runner

Status:

NOT STARTED

Create:

```text
run_continuous_ibkr_paper.py
```

The runtime should replace only the broker implementation while preserving the existing deterministic pipeline.

---

# Runtime Validation

Continue validating:

- idle behaviour;
- DST transitions;
- quote validation;
- persistence;
- managed exits;
- restart recovery;
- runtime stability.

No strategy changes during validation.

---

# Strategy

No active strategy work.

Future improvements remain:

- thesis comparison;
- risk-budget sizing;
- advanced ranking evaluation;
- position review.

These remain frozen until the IBKR integration is operational.

---

# GUI

Low priority.

Future work:

- dashboard;
- portfolio panels;
- runtime monitor;
- performance analytics.

---

# Technical Debt

Future review:

- dependency cleanup;
- execution service simplification;
- provider cleanup;
- unused legacy code removal.

Only perform cleanup when it reduces complexity without changing behaviour.

---

# Rules

Always:

- inspect existing architecture first;
- avoid duplicate services;
- preserve deterministic behaviour;
- write targeted tests first;
- execute the full regression suite;
- commit only after all tests pass.

---

# Success Criteria

Sprint 9.3 completes when:

- Orion can connect to IBKR Paper.
- Orion can read account data.
- Orion can submit paper orders.
- Orion receives fills.
- Orion manages paper positions through the existing lifecycle.
- The continuous runner operates through IBKR Paper with zero regression failures.

Live trading is explicitly outside the scope of this sprint.