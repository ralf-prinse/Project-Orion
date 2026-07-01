# ADR-0002: ScanOrchestrator as Application Scan Entry Point

## Status

Accepted

## Context

Orion has grown from separate analytical services into a multi-layer platform containing scanning, analysis, signals, decisions, risk, portfolio, planning, performance, AI and GUI presentation components.

The application needs one stable public entry point for complete scan execution.

## Decision

Introduce `ScanOrchestrator` in `core/orchestration` as the central scan coordination component.

The orchestrator coordinates scan execution, timing, progress reporting and error handling. It does not contain market-data, analysis, signal, decision, risk, portfolio, planning, AI or GUI business logic.

## Consequences

- GUI, CLI, schedulers and future APIs can call one stable scan interface.
- Progress reporting and timing can be centralized.
- Scan steps can be adapted without changing presentation code.
- The orchestrator must remain orchestration-only to avoid becoming a God object.

## Alternatives Considered

- Letting the GUI call individual services directly.
- Keeping scan coordination inside scanner services.
- Building a full async job system immediately.

These alternatives were rejected because Orion first needs a simple deterministic orchestration boundary before adding asynchronous execution or external APIs.
