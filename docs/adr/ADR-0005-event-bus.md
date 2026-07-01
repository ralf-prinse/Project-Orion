# ADR-0005 — Event Bus Foundation

## Status

Accepted

## Context

Project Orion now contains a central ScanOrchestrator, a configuration framework
and a dependency-injection foundation. Future product features such as GUI
progress updates, structured logging, diagnostics, performance metrics, broker
integration, scheduling and plugins need to react to scan activity.

Directly coupling all of those features to the orchestrator would increase
maintenance cost and create dependency pressure on the core scan pipeline.

## Decision

Introduce a small synchronous Event Bus in `core/events`.

The first implementation supports:

- explicit event classes;
- explicit subscription;
- synchronous deterministic publishing;
- deterministic handler execution order;
- no external dependencies;
- no asynchronous execution;
- no reflection or automatic discovery.

The initial events are:

- `ScanStartedEvent`
- `PipelineStepStartedEvent`
- `PipelineStepCompletedEvent`
- `PipelineFailedEvent`
- `ScanCompletedEvent`

The ScanOrchestrator may publish lifecycle events, but it remains responsible
only for orchestration. Subscribers decide independently how to react.

## Consequences

Positive consequences:

- GUI, logging, metrics and future plugins can observe scan lifecycle events
  without direct coupling to the orchestrator.
- The orchestrator remains deterministic and testable.
- Future listeners can be added without modifying orchestration logic.
- The architecture prepares Orion for diagnostics and plugin-style extension.

Trade-offs:

- Event handlers currently run synchronously, so handlers must remain lightweight.
- The first version intentionally does not support async dispatch or background
  processing.
- Event schemas must be maintained carefully as public infrastructure models.

## Alternatives Considered

### Direct callbacks only

Rejected because callbacks are useful for one consumer, but do not scale well to
multiple independent subscribers such as logging, GUI, metrics and broker logic.

### Full async event system

Rejected for now because it would increase complexity and could introduce
non-deterministic execution concerns before Orion needs that capability.

### External event-bus library

Rejected because Orion currently needs a small deterministic internal mechanism,
not a framework dependency.
