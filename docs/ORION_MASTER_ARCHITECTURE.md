# PROJECT ORION

# ORION_MASTER_ARCHITECTURE.md

**Document Type:** Architectural Blueprint

---

# 1. Purpose

This document defines the long-term software architecture of Project Orion.

It describes the architectural principles that should remain stable throughout the lifetime of the project.

Implementation details belong in source code.

Current progress belongs in PROJECT_STATUS.md.

Engineering workflow belongs in AI_CONTEXT.md.

---

# 2. Product Vision

Project Orion is a professional deterministic swing-trading platform.

Its goal is to assist traders by producing transparent, reproducible and explainable investment analyses.

Project Orion is intentionally not an automated trading bot.

All investment decisions remain deterministic.

Artificial Intelligence exists solely to explain deterministic outputs.

---

# 3. High-Level Architecture

```
                Desktop GUI
                     │
                     ▼
          AI Explanation Layer
                     │
                     ▼
             Trade Planner
                     │
                     ▼
             Risk Manager
                     │
                     ▼
           Portfolio Engine
                     │
                     ▼
            Decision Engine
                     │
                     ▼
             Signal Engine
                     │
                     ▼
            Analysis Engine
                     │
                     ▼
           Indicator Engine
                     │
                     ▼
          Historical Data Layer
                     │
                     ▼
            Market Data Layer
                     │
                     ▼
             Universe Layer
```

---

# 4. Architectural Principles

The following principles are considered non-negotiable.

## Layered Architecture

Every processing layer has one responsibility.

Layers communicate only through defined models.

---

## Deterministic Behaviour

Equal input always produces equal output.

No randomness may influence:

- analysis
- signals
- decisions
- portfolio
- risk
- planning

---

## Registry-Driven Processing

Every extensible processing layer should be registry driven.

Examples:

- AnalyzerRegistry
- SignalRegistry
- DecisionRegistry
- PortfolioRegistry
- RiskRegistry

---

## Dependency Injection

Application wiring belongs to the composition root.

Concrete implementations should not create dependencies directly.

---

## Event-Driven Infrastructure

Infrastructure communicates through the Event Bus.

Domain calculations remain deterministic.

Infrastructure listeners may observe events but never modify business decisions.

---

## Explainability

Every recommendation must be explainable.

Every calculation must be traceable.

Every score must be reproducible.

---

## Composition over Inheritance

Reusable behaviour is shared through composition.

Inheritance is kept shallow.

---

## Separation of Concerns

Business logic never belongs inside:

- GUI
- infrastructure
- configuration
- orchestration

---

# 5. GUI Architecture

The GUI is presentation-only.

Responsibilities:

- display data
- navigation
- layout
- user interaction

The GUI never performs:

- calculations
- trading logic
- risk validation
- signal generation
- decision making

Future architecture:

Workspace

↓

Navigation

↓

Dashboard Router

↓

Presenters

↓

View Models

↓

Qt Widgets

---

# 6. Core Infrastructure

Current shared infrastructure:

- ApplicationContainer
- ServiceRegistry
- Event Bus
- Scan Orchestrator
- Configuration Framework
- Explainability Framework
- AnalyzerRunner

These systems should be reused whenever practical.

---

# 7. Development Philosophy

Project Orion evolves through incremental improvements.

Architecture is reviewed before implementation.

Small verified changes are preferred over large speculative rewrites.

The repository is the single source of truth.

---

# 8. Long-Term Vision

Future development may include:

- Broker integrations
- Multi-monitor workspace
- Alerts
- Watchlists
- Cloud synchronisation
- Advanced reporting
- AI-assisted explanations
- Plugin architecture

These features must fit within the existing architectural principles.

---

# 9. Architectural Decision Records

Major architectural changes should be documented through ADRs.

Examples:

- Dependency Injection
- Event Bus
- Workspace Framework
- Explainability
- Configuration Framework

---

# 10. Conclusion

This document defines the architectural identity of Project Orion.

All future development should preserve these principles.

When implementation conflicts with architecture, architecture takes precedence.