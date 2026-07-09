# PROJECT ORION

# TODO

**Purpose:** Active Development Backlog  
**Status:** Sprint 8.6

---

# Current Sprint

## Sprint 8.6 – Dashboard & Trading Analytics

Status:

```text
IN PROGRESS
```

Current objective:

Transform Orion from an autonomous trading engine into a professional trading platform with live monitoring and performance analytics.

---

# High Priority

## 1. Trading Dashboard CLI

Status:

```text
NEXT
```

Objectives:

- Live portfolio overview
- Cash
- Equity
- Open P/L
- Closed P/L
- Winrate
- Active positions
- Recent trades

Deliverable:

```text
run_dashboard.py
```

---

## 2. Closed Trade Analytics

Status:

```text
PLANNED
```

Track for every completed trade:

- entry
- exit
- holding time
- realized profit
- realized loss
- exit reason
- AI confidence
- indicator values
- trade score

Purpose:

Provide historical data for optimisation.

---

## 3. Dashboard GUI

Status:

```text
PLANNED
```

Display:

- Portfolio
- Equity
- Cash
- Open positions
- Closed trades
- Live signals
- Recent BUY/SELL events

The GUI will consume DashboardService rather than containing business logic.

---

# Medium Priority

## Adaptive Exit Optimizer

Replace fixed exits with dynamic exits based on:

- volatility
- ATR
- confidence
- market regime
- trend strength

---

## Decision Log Separation

Split runtime output into:

```text
trade_journal.jsonl
```

Contains:

- BUY
- SELL
- CLOSE_POSITION

and

```text
decision_log.jsonl
```

Contains:

- rejected trades
- insufficient cash
- existing position
- confidence failures
- validation failures

---

## Performance Analytics

Calculate:

- winrate
- profit factor
- expectancy
- average winner
- average loser
- average holding time
- best trade
- worst trade
- equity curve

---

# Long-Term Roadmap

## Self Learning

Analyse historical trades.

Improve:

- confidence weighting
- indicator weighting
- exit optimisation

Trading decisions remain deterministic.

Learning adjusts configuration, never deterministic calculations.

---

## Broker Integration

Future support:

- Interactive Brokers
- Trading212
- Other supported brokers

Only after paper trading has been extensively validated.

---

## Live Trading

Requirements before implementation:

- Stable dashboard
- Stable analytics
- Adaptive exits
- Positive paper trading performance
- Extensive regression testing

Paper trading remains mandatory before enabling real-money execution.

---

# Development Rules

Every completed feature must satisfy:

- architecture review
- implementation
- regression tests
- manual validation
- documentation update
- Git commit
- Git push

No feature is considered complete until all steps have been finished.

---

# End of TODO