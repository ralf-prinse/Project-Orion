# ORION AI CONTEXT

---

# Documentation Information

Documentation Version

v1.8

Architecture Version

v1.8

Current Sprint

🚧 Sprint 4.8 — Mission Control Foundation

Last Updated

2026-07-04

---

# Purpose

This document provides the minimum context required for a new Orion development session.

It complements:

- ORION_MASTER_ARCHITECTURE.md
- PROJECT_STATUS.md
- TRADING_STRATEGY.md

Architectural details are intentionally omitted here to avoid duplication.

---

# Current Project State

Project Orion has completed its deterministic backend foundation.

Current development focuses on transforming the desktop application into **Mission Control**, a professional deterministic trading workstation.

The backend architecture is considered stable.

The frontend architecture is transitioning from a dashboard-oriented application into a reusable panel-based Mission Control interface.

---

# Current Sprint

## Sprint 4.8 — Mission Control Foundation

Primary objectives:

- LiveScannerService
- Mission Control panels
- TradingPipeline UI reintegration
- Position Monitoring preparation
- GuiWorkspace panel architecture

---

# Current Working Components

Backend

✔ TradingPipeline

✔ TechnicalScanner

✔ MarketScanner

✔ AnalysisEngine

✔ PositionSizingEngine

✔ RiskEngine

✔ AI Context Builder

✔ AI Explanation Engine

Desktop

✔ Workspace architecture

✔ Presenter architecture

✔ WorkspaceRenderer

✔ ChartCanvas Framework

✔ Dashboard

✔ Trading Workspace

✔ LiveScannerService foundation

✔ GuiWorkspace panel support

Current validation:

✔ python run_tests.py

Latest result:

6 passed

# Development Rules

Every Orion implementation must follow these rules.

Backend

- Trading logic only inside backend services.
- TradingPipeline remains the single source of truth.
- LiveScannerService performs orchestration only.
- Position monitoring remains deterministic.

Presentation

- Widgets contain presentation only.
- Panels contain presentation only.
- Presenters transform deterministic output only.
- WorkspaceRenderer owns rendering only.
- ChartCanvas owns painting only.

Artificial Intelligence

AI may:

- explain
- summarize
- compare
- generate natural language

AI may never:

- generate BUY signals
- generate SELL signals
- calculate indicators
- size positions
- override deterministic output

---

# Current Development Focus

Immediate priorities:

1. Mission Control implementation.
2. LiveScannerService scheduling.
3. Trading Workspace deterministic reintegration.
4. Position Monitor.
5. Paper Trading foundation.

Current long-term objective:

Transform Orion into a professional deterministic trading workstation for short-term equity trading.

---

# Validation

After every complete file:

```powershell
python run_tests.py
```

Before every commit:

```powershell
python app.py
```

Current validation:

✔ 6 tests passed

---

# Documentation

The official Orion documentation consists of:

- PROJECT_VISION.md
- ORION_MASTER_ARCHITECTURE.md
- TRADING_STRATEGY.md
- PROJECT_STATUS.md
- TODO.md
- CHANGELOG.md
- AI_CONTEXT.md

Architectural information belongs only inside ORION_MASTER_ARCHITECTURE.md.

---

# New Chat Workflow

Every new Orion development session must follow this workflow.

1. Upload the complete Project Orion ZIP.

2. Upload all synchronized documentation.

3. Read every documentation file.

4. Analyse the complete project source tree.

5. Determine:

- architecture version
- current sprint
- completed work
- active work
- next implementation step

6. Only after the complete analysis may implementation begin.

Rules:

- No assumptions.
- No snippets.
- Always provide complete files.
- One file at a time.
- Test after every file.

---

# End of AI_CONTEXT