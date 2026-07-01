# ADR-0006 — Event-Driven Logging and Metrics Listeners

## Status

Accepted

## Context

Sprint 10.14 introduced a deterministic synchronous Event Bus. The Event Bus makes it possible for diagnostics, GUI progress, metrics, AI explanations and future plugins to observe scan activity without being directly coupled to `ScanOrchestrator`.

The next architectural step is to prove this mechanism with low-risk listeners that do not change trading behaviour.

## Decision

Project Orion introduces two first-class event listeners in `core/events`:

- `LoggingListener`
- `MetricsListener`

Both listeners are synchronous, deterministic and side-effect free.

The first implementation stores entries and metrics in memory. It does not write files, start background workers, publish network messages or affect trading decisions.

`ApplicationContainer` wires both listeners into the shared `EventBus` for the core scan lifecycle events:

- `ScanStartedEvent`
- `PipelineStepStartedEvent`
- `PipelineStepCompletedEvent`
- `PipelineFailedEvent`
- `ScanCompletedEvent`

## Consequences

This keeps `ScanOrchestrator` focused on orchestration while enabling diagnostics and future GUI progress panels to consume scan information through events.

The architecture also prepares Orion for future operational tooling:

- file logging
- scan diagnostics
- performance metrics
- GUI live progress
- plugin listeners
- broker/audit events

## Alternatives Considered

### Direct logging inside ScanOrchestrator

Rejected because this would couple diagnostics directly to orchestration and make future GUI or plugin integrations harder.

### Python logging only

Rejected for this sprint because standard logging alone does not provide structured in-memory event metrics for tests and future UI dashboards.

### Async Event Bus

Rejected for now. Orion must remain deterministic and simple. Async event dispatch can be introduced later if a real performance need appears.
