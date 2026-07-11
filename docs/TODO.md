# PROJECT ORION — TODO

**Current phase:** Engine 1.0 review  
**Updated:** 2026-07-11

## Immediate

- [ ] Commit and push Sprint 8.13.3 plus synchronized documentation.
- [ ] Run final `python run_tests.py`.
- [ ] Verify no active import of `position_state_store`.
- [ ] Review `run_tests.py` names after legacy-removal tests.
- [ ] Perform Engine 1.0 architecture review.
- [ ] Create stable Engine 1.0 tag or release branch.

## Engine 1.0 Review

- [ ] Confirm `TradingSession` is the only lifecycle-state owner.
- [ ] Confirm all persistence writes originate from runner orchestration.
- [ ] Classify `JsonPaperPortfolioRepository` as compatibility or remove it in a later isolated sprint.
- [ ] Review unused services, imports and tests before deletion.
- [ ] Confirm restart, crash and integrity smoke tests remain documented.
- [ ] Freeze the active runtime diagram.

## Sprint 9.0 Candidates

Choose only after Engine 1.0 freeze:

1. Trading Dashboard integration with the consolidated engine.
2. Runtime alerts and operational metrics.
3. Performance analytics from the trade journal.
4. Portfolio intelligence and exposure analysis.
5. Configuration profiles and strategy comparison.

## Later

- broker compatibility;
- portfolio import/export;
- longer paper-trading validation;
- expectancy and exit-reason analytics;
- multi-strategy support;
- AI summaries of deterministic results.

## Out of Scope Until Proven Safe

- real-money execution;
- AI-generated BUY/SELL/EXIT decisions;
- silent strategy mutation;
- duplicate runtime state;
- new engines that overlap existing services.

## Development Checklist

Every sprint:

1. inspect the complete relevant runtime;
2. identify ownership;
3. reuse existing models and services;
4. update targeted regressions;
5. run the full suite;
6. perform runtime validation when relevant;
7. synchronize docs;
8. commit and push.

# End
