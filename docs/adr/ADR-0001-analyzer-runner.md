# ADR-0001: AnalyzerRunner for Registry-Driven Pipelines

## Status

Accepted

## Context

Project Orion contains multiple deterministic processing layers. Analysis, signal generation and decision making all require predictable execution of registered analyzers.

## Decision

Use `AnalyzerRunner` as the reusable orchestration component for registry-driven analyzer pipelines.

## Consequences

- Engines remain orchestration-only.
- Business logic stays inside specialized analyzers.
- Execution order remains deterministic.
- Future registry-driven layers can reuse the same infrastructure.

## Alternatives Considered

- Hardcoded engine execution order.
- Inheritance-heavy base engine hierarchy.
- Dynamic plugin discovery at runtime.

These alternatives were rejected because they increase coupling, reduce clarity or introduce unnecessary complexity for the current alpha architecture.
