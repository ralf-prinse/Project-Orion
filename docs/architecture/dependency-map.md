# PROJECT ORION — DEPENDENCY MAP

**Status:** Active Architecture  
**Updated:** 2026-07-14

---

# Purpose

This document describes the high-level dependency direction within Orion.

It is intended as an architectural reference, not an implementation guide.

---

# Core Principle

Dependencies always point inward toward deterministic business logic.

Presentation and infrastructure depend on services.

Services never depend on GUI code.

---

# Current Layering

```text
GUI / CLI
        │
        ▼
Presenters
        │
        ▼
Application Services
        │
        ▼
Trading Services
        │
        ▼
Domain Models
```

Infrastructure exists beside the services:

```text
Providers
Repositories
Broker
Configuration
Runtime
```

None of these own trading decisions.

---

# Execution Flow

```text
ExecutionEngine
        │
        ▼
PaperBroker
```

Planned:

```text
ExecutionEngine
        │
        ▼
IbkrBroker
```

ExecutionEngine must remain independent from broker implementation details.

---

# Runtime Flow

```text
ContinuousPaperTradingRunner
        │
        ▼
RuntimeSupervisor
        │
        ▼
AutonomousPaperTradingRunner
        │
        ▼
TradingSessionRepository
```

TradingSession remains the only owner of runtime trading state.

---

# Ownership Rules

Trading decisions

↓

Decision Engine

Risk

↓

AdaptiveRiskEngine

Execution

↓

ExecutionEngine

Lifecycle

↓

TradingSession

Persistence

↓

Repositories

Presentation

↓

Presenters

GUI

↓

Qt

---

# Dependency Rules

Allowed:

- GUI → Presenters
- Presenters → Services
- Services → Models
- Services → Providers
- Services → Repositories
- ExecutionEngine → Broker

Forbidden:

- GUI → Services with trading mutations
- Providers → Decision logic
- Repositories → Business logic
- AI → Execution
- Broker → Strategy

---

# Future Direction

The only planned execution expansion is:

```text
PaperBroker
IbkrBroker
```

Both must satisfy the same execution contract.

No additional broker abstraction is currently planned.

---

# End