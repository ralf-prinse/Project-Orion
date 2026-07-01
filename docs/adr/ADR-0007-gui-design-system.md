# ADR-0007 — GUI Design System

## Status

Accepted

## Context

Project Orion now contains a broad deterministic backend and a growing desktop GUI foundation. The existing GUI presenters correctly avoid trading logic, but visual styling can easily become inconsistent if every screen defines colours, spacing and typography independently.

A professional desktop product requires a central design language before the GUI is expanded further.

## Decision

Introduce an explicit GUI Design System under `ui/design` and a small component model library under `ui/components`.

The first version contains:

- semantic colour palette;
- typography scale;
- spacing scale;
- GUI metrics;
- lightweight icon mapping;
- theme object capable of generating Qt stylesheets;
- toolkit-independent component view models for cards, metric tiles, badges, section headers, sidebars and panels.

The design system remains intentionally simple and deterministic. It does not introduce external GUI dependencies, automatic styling discovery or runtime theming magic.

## Consequences

Positive:

- Future screens can share one consistent visual language.
- Presenters remain free of business logic.
- Styling changes can be made centrally.
- The GUI can evolve toward a professional product without rewriting the backend.

Trade-offs:

- Existing screens still need gradual migration to the component library.
- The first sprint focuses on visual infrastructure rather than visible feature expansion.

## Alternatives Considered

### Continue styling widgets directly

Rejected because it would increase visual inconsistency and make a future professional redesign expensive.

### Use an external design framework

Rejected for now because Orion should keep its GUI foundation lightweight, explicit and easy to test.

### Rebuild the GUI from scratch

Rejected because the existing presenter/foundation layer is useful and should be evolved rather than discarded.
