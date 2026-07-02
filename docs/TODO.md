# PROJECT ORION

# TODO.md

**Purpose:** Development roadmap

**Status:** Active

**Last Updated:** July 2026

---

# Executive Summary

Project Orion has successfully completed the deterministic trading engine
(Epic 1) and the desktop presentation architecture (Epic 2).

Epic 3 is now focused on delivering professional desktop functionality on top
of the completed architecture.

The architecture is considered stable.

Future work should prioritize user value over architectural expansion.

Current regression status:

343 passing tests

---

# Current Sprint

## Sprint 3.6 — Professional Portfolio Dashboard

Status:

🚧 In Progress

Objectives:

- Integrate WorkspaceCoordinator into MainWindow
- Render GuiWorkspace directly
- Display GuiMetricCards
- Complete Portfolio dashboard
- Improve Portfolio workspace UX

Definition of Done:

- GuiWorkspace rendered by PortfolioWorkspace
- MetricCards visible
- Regression tests passing
- Documentation updated
- Git committed

---

# Short-Term Roadmap

## Sprint 3.7 — Professional Charts

Objectives:

- Introduce reusable chart component
- Add portfolio value chart
- Add performance chart
- Preserve Workspace Composition Architecture

Deliverables:

- GuiChart
- Chart widget
- Chart presenter
- Portfolio chart integration

---

## Sprint 3.8 — Scanner Improvements

Objectives:

- Better scanner overview
- Scanner statistics
- KPI cards
- Improved filtering
- Better scan summaries

---

## Sprint 3.9 — AI Workspace

Objectives:

- Dedicated AI workspace
- Deterministic explanation panels
- Trade explanation summaries
- Decision breakdown
- Explanation history

---

# Medium-Term Roadmap

## Performance Workspace

Goals:

- Equity curve
- Performance KPIs
- Drawdown analysis
- Monthly returns
- Benchmark comparison

---

## Broker Integration

Goals:

- Broker abstraction
- Order preview
- Order validation
- Broker adapters
- Live portfolio synchronization

---

## Reporting

Goals:

- PDF export
- CSV export
- Portfolio reports
- Trade reports
- Performance reports

---

## Desktop UX

Goals:

- Docking support
- Layout persistence
- Custom dashboards
- Workspace personalization
- Keyboard shortcuts

---

# Long-Term Vision

Future development may include:

- Multi-account support
- Multi-monitor layouts
- Plugin architecture
- Cloud synchronization
- Mobile companion application
- Advanced screening
- Watchlists
- Notifications
- Strategy comparison
- Portfolio optimization

These features should extend the existing architecture rather than replacing it.

---

# Technical Debt

Current technical debt is low.

Open items:

- Complete WorkspaceCoordinator integration
- Complete GuiWorkspace migration
- Remove temporary compatibility methods
- Continue reducing MainWindow responsibilities where appropriate

None of these items block feature development.

---

# Architectural Principles

Every future feature should respect the following principles:

- Deterministic First
- Thin GUI
- Stable Public APIs
- Composition over Inheritance
- Single Responsibility Principle
- Reusable presentation models
- Workspace Composition Architecture

Architecture should only evolve when a concrete feature clearly requires it.

---

# Development Workflow

Every completed task follows the same sequence:

Architecture Review

↓

Implementation

↓

Regression Tests

↓

Documentation

↓

Git Commit

↓

Push

---

# Definition of Done

A task is considered complete only when:

✓ Feature implemented

✓ Regression tests passing

✓ Documentation updated

✓ Architecture remains consistent

✓ Git commit completed

---

# Current Priorities

Priority 1

Professional Portfolio Dashboard

Priority 2

Professional Charts

Priority 3

AI Workspace

Priority 4

Scanner Enhancements

Priority 5

Broker Integration

Priority 6

Reporting & Export

Priority 7

Desktop UX Improvements

---

# Overall Direction

Project Orion has transitioned from architecture-first development to
feature-first development.

The deterministic engine is complete.

The desktop architecture is complete.

Future work should focus on delivering a professional trading experience while
preserving the existing architecture.

---

End of document.