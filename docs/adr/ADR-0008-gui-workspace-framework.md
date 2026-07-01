# ADR-0008 — GUI Workspace Framework

## Status

Accepted

## Context

Project Orion has a growing GUI foundation with presenters, reusable components and a design system. As the product moves toward a professional desktop application, isolated screens are no longer sufficient. Scanner, portfolio, risk, performance, AI, logs and settings should behave as panels inside a coherent desktop workspace.

## Decision

Introduce a toolkit-independent Workspace Framework under `ui/workspace/`.

The workspace provides:

- stable workspace regions;
- deterministic panel registration;
- toolbar action models;
- status-bar item models;
- layout specifications derived from the design system;
- an `OrionWorkspace` facade that composes shell state into workspace state.

The workspace does not create PySide6 widgets and does not perform trading logic.

## Consequences

Positive:

- Future GUI screens can be implemented as panels instead of isolated windows.
- Layout decisions become testable without launching Qt.
- The GUI can evolve toward a professional dockable desktop shell.
- Backend services remain fully separated from presentation.

Trade-offs:

- Real Qt docking behavior still needs a later implementation sprint.
- Existing `ui/main_window.py` is not yet migrated to the workspace.

## Alternatives Considered

### Direct PySide6 Dock Widgets

Rejected for this sprint because it would couple the architectural model directly to Qt too early.

### Continue with ad-hoc page widgets

Rejected because it would make the GUI harder to scale as Orion adds more dashboards and panels.
