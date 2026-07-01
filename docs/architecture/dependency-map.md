# Project Orion Dependency Map

## Sprint 10.13 Scope

Sprint 10.13 focuses on maturing the dependency-injection foundation without performing a risky project-wide migration.

## Current Composition Root

```text
app.py
  └── OrionWindow

ApplicationContainer
  ├── ScanPipeline
  └── ScanOrchestrator
        └── ScanPipeline
```

## Intended Direction

```text
app.py
  └── ApplicationContainer
        ├── Configuration
        ├── ScanPipeline
        ├── ScanOrchestrator
        ├── AnalysisEngine        (future migration)
        ├── SignalEngine          (future migration)
        ├── DecisionEngine        (future migration)
        └── OrionWindow           (future migration)
```

## Lifetime Guidance

### Singleton Candidates

- Configuration services
- Scan pipeline composition
- Scan orchestrator
- Registries
- Provider adapters with shared cache/state

### Transient Candidates

- Per-scan context objects
- Temporary report builders
- Request-specific adapters
- Test doubles when isolation is required

## Dependency Rules

- Application-level construction belongs in `core/container`.
- Orchestration belongs in `core/orchestration`.
- Business logic remains in `services`.
- UI presentation remains in `ui`.
- Providers remain isolated from decision and analysis logic.

## Technical Debt Notes

- `app.py` still constructs the GUI directly. This is acceptable for now, but GUI construction should eventually move behind the composition root.
- Some legacy root-level tests remain outside the official `tests` regression suite.
- `engines/` and `services/` both exist. This should be reviewed before v1.0 to ensure responsibilities remain clear.
