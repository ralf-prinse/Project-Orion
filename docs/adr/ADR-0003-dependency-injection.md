# ADR-0003: Explicit Dependency Injection Container

## Status

Accepted

## Context

Project Orion now contains many services and engines. As the platform grows toward broker integration, plugins, multiple providers and production packaging, object construction must remain centralized and testable.

## Decision

Introduce an explicit `ApplicationContainer` and `ServiceRegistry` in `core/container`.

The container is intentionally small and explicit. Orion will not use reflection, automatic discovery, decorators or a third-party inversion-of-control framework at this stage.

## Consequences

- Object construction moves toward a clear composition root.
- Tests can replace services through explicit registration replacement.
- Future provider and broker swaps become easier.
- The container must grow slowly to avoid becoming a God container.

## Alternatives Considered

- Continue direct construction throughout the codebase.
- Adopt a third-party dependency-injection framework.
- Use dynamic service discovery.

Direct construction was rejected because it becomes harder to test and replace dependencies as Orion grows. Third-party DI and dynamic discovery were rejected because they add complexity before Orion needs it.
