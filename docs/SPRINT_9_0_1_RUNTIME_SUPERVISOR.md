# Sprint 9.0.1 — Runtime Supervisor

## Status

Implemented for local validation.

## Goal

Add operational supervision to the continuous autonomous paper-trading runtime without introducing a second trading-state owner.

## Ownership rule

`TradingSession` remains the only owner of:

- `PaperPortfolio`;
- `PositionState`;
- `RiskPlan`;
- managed-position lifecycle state.

`RuntimeSupervisor` owns operational metadata only. It observes runtime events and never modifies a `TradingSession`.

## Runtime chain

```text
ContinuousPaperTradingRunner
        ├── AutonomousPaperTradingRunner
        └── RuntimeSupervisor
                ├── RuntimeHealth
                └── RuntimeEventRepository
                        └── JsonlRuntimeEventRepository
```

## Runtime events

The supervisor records:

- `RUNTIME_STARTED`;
- `ITERATION_STARTED`;
- `ITERATION_COMPLETED`;
- `ITERATION_FAILED`;
- `RUNTIME_STOPPED`.

Default file:

```text
data/runtime_events.jsonl
```

Isolated runtime file:

```text
data/optimization_runtime_events.jsonl
```

## Runtime health

The in-memory health model exposes:

- runtime status;
- start and stop timestamps;
- last heartbeat;
- current iteration;
- completed and failed iteration counts;
- last iteration duration;
- last exception;
- open-position, position-state and risk-plan counts.

## Safety boundaries

The supervisor does not:

- generate trading decisions;
- calculate risk;
- size positions;
- open or close positions;
- persist trading sessions;
- recover or mutate lifecycle state.

## Validation

Targeted tests:

```powershell
python test_runtime_supervisor.py
python test_jsonl_runtime_event_repository.py
python test_run_continuous_paper_trading.py
python test_continuous_paper_trading_runner.py
```

Full regression:

```powershell
python run_tests.py
```

The central runner now contains two additional test modules, so the expected command baseline becomes:

```text
71 passed
0 failed
```
