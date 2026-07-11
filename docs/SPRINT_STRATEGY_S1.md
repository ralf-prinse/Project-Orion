# Sprint Strategy S1 — Investment Thesis Foundation

## Goal

Create a richer, explainable strategy assessment without changing active autonomous trading behaviour.

## Delivered

- immutable `InvestmentThesis` and `ThesisFactor` models;
- deterministic `InvestmentThesisBuilder`;
- seven transparent factors:
  - trend;
  - momentum;
  - pressure confirmation;
  - market regime;
  - contextual RSI;
  - volatility quality;
  - risk/reward;
- BUY / WATCH / AVOID thesis stance;
- supporting reasons, risk reasons and invalidation conditions;
- thesis attached to `TradingPipelineResult`;
- two focused regression modules;
- strategy-intelligence audit.

## Architectural Rule

The thesis runs in shadow mode. `AdaptiveDecisionEngine` remains the active BUY/HOLD/SELL owner. No paper trade is approved, sized, opened, held or closed because of the thesis in this sprint.

## Validation

Run:

```powershell
python test_investment_thesis_builder.py
python test_strategy_thesis_pipeline.py
python run_tests.py
```

Expected central baseline after installation:

```text
Passed: 73
Failed: 0
```
