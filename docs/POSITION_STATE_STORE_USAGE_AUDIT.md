# Sprint 8.13.2 — PositionStateStore Usage Audit

## Scope

Analyzed active runtime chain:

`TradingCycle`
→ `PaperTradingService`
→ `PaperPositionUpdateService`
→ `PaperPositionCloseService`
→ `TradingSession`
→ `PositionStateStore`

No production code is changed in this sprint step.

## Findings

### TradingSession is the runtime read source

The active services read lifecycle state from:

- `TradingSession.position_states`
- `TradingSession.risk_plans`
- `TradingSession.portfolio.positions`

Position-management decisions do not load state from `PositionStateStore`.

### PositionStateStore is a parallel write mirror

Current writes:

| Runtime operation | TradingSession | PositionStateStore |
|---|---|---|
| Open position | Adds PositionState and RiskPlan | `save(PositionState)` |
| Update position | Replaces PositionState | `save(PositionState)` |
| Close position | Removes PositionState and RiskPlan | `remove(symbol)` |

### Store reads

No active position-management service calls `PositionStateStore.load()` to make a runtime decision.

`load()` is used by tests and explicit verification only.

## Ownership conclusion

Current authoritative runtime aggregate:

`TradingSession`

Current secondary in-memory mirror:

`PositionStateStore`

The store is not yet removed because constructors, lifecycle synchronization tests and the shared `TradingCycle` wiring still define it as part of the current compatibility contract.

## Safe migration path

1. Preserve this audit regression.
2. Remove store writes from one lifecycle service at a time.
3. Keep `TradingSession` assertions green after every change.
4. Remove shared-store constructor wiring from `TradingCycle`.
5. Remove `PositionStateStore` only after repository-wide import and test audit.
6. Run the complete regression suite after every substep.

## Recommendation for Sprint 8.13.3

First remove the store dependency from `PaperPositionUpdateService`.

Reason:

- update already reads state and RiskPlan exclusively from `TradingSession`;
- its output already returns a complete updated `TradingSession`;
- this is the smallest isolated write-mirror removal;
- open and close compatibility remain intact during that step.
