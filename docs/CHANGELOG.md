# CHANGELOG

---

# Documentation Information

Documentation Version

v1.13

Architecture Version

v2.2

Last Updated

2026-07-06

---

# Sprint 5.8 — Adaptive Risk Engine

Status

✅ Completed

---

# Summary

Sprint 5.8 marks an important milestone in the evolution of Project Orion.

The platform has transitioned from fixed risk management toward deterministic adaptive risk management.

Static stop-loss and take-profit percentages have been replaced by dynamically generated Risk Plans.

Trade lifecycle management is now fully operational.

Mission Control continues to function as the operational center for opportunity discovery.

Trade Monitor now serves as the operational workspace for active positions.

---

# Architecture

## Added

- AdaptiveRiskEngine
- RiskPlan domain model
- Dynamic RiskPlan generation
- IndicatorPack price support
- Adaptive stop-loss calculation
- Adaptive profit target calculation
- Risk / Reward calculation
- Adaptive risk notes

---

## Changed

- TradingPipeline now generates deterministic RiskPlans.
- IndicatorBuilder now supplies the latest market price.
- IndicatorPack now contains live price information.
- Open Trade workflow now consumes RiskPlans instead of fixed percentages.
- Risk management architecture is fully separated from BUY/HOLD/SELL decision logic.

---

## Preserved

The following architectural rules remain unchanged

- TradingPipeline remains the only deterministic BUY / HOLD / SELL engine.
- AdaptiveDecisionEngine remains responsible for deterministic trading decisions.
- AdaptiveRiskEngine remains responsible only for deterministic risk planning.
- ExitEvaluationService remains the only deterministic EXIT engine.
- Artificial Intelligence remains explainability only.

---

# Backend

## Added

- AdaptiveRiskEngine
- RiskPlan
- Adaptive risk calculation
- Dynamic stop-loss generation
- Dynamic target generation
- Risk / Reward calculation

---

## Improved

- TradingPipeline integration
- IndicatorBuilder
- IndicatorPack
- Trade creation workflow
- Risk calculation architecture

---

# Desktop

## Improved

Mission Control

- Improved opportunity ranking
- Top 10 opportunities
- Expanded watchlist support

Trading Workspace

- Adaptive RiskPlan integration
- Improved Open Trade workflow

Trade Monitor

- Live monitoring improvements
- Dynamic trade refresh
- Close Trade workflow
- Trade lifecycle synchronization

Portfolio

- Stable capital persistence
- FX-aware buying power

---

# Validation

Regression

```powershell
python run_tests.py
```

Additional validation

```powershell
python test_adaptive_risk_engine.py
```

Desktop validation

```powershell
python app.py
```

Validated

✔ Regression tests pass

✔ AdaptiveRiskEngine tests pass

✔ Desktop launches

✔ Mission Control operational

✔ Trading Workspace operational

✔ Trade Monitor operational

✔ Portfolio operational

✔ History operational

✔ Settings operational

✔ Open Trade validated

✔ Close Trade validated

✔ Live P/L validated

✔ Adaptive RiskPlan validated

✔ Manual GUI validation completed

---

# Current Project State

Completed

✔ Deterministic TradingPipeline

✔ Mission Control

✔ Trading Workspace

✔ Trade Monitor

✔ Portfolio

✔ Trade History

✔ Trade Lifecycle

✔ Adaptive Risk Engine

✔ Live Position Monitoring

✔ Dynamic Risk Planning

✔ Stable desktop architecture

Project Orion now provides a complete deterministic workflow from market scanning through trade lifecycle management.

---

# Next Sprint

Sprint 5.9 — Intelligent Risk Management

Objectives

- Display complete RiskPlan
- Display Target 1
- Display Target 2
- Display Target 3
- Display Risk / Reward ratio
- ATR-aware stop-loss
- Dynamic trailing stop
- Break-even support
- Partial profit taking

---

# End of CHANGELOG