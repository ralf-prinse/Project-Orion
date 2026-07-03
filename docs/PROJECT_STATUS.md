# PROJECT ORION

# PROJECT STATUS

---

# Project Version

**v1.2.0-alpha**

Status

🟢 Active Development

Current Milestone

🚧 Sprint 4.5 — ChartCanvas Framework

Architecture Freeze

**v1.6**

---

# Executive Summary

Project Orion is a deterministic AI-assisted desktop trading platform.

The deterministic backend is production stable.

Current development focuses entirely on desktop presentation architecture and visualization.

No new trading logic is being introduced.

All development is focused on:

- reusable rendering architecture
- ChartCanvas Framework expansion
- desktop UI/UX improvements
- visualization scalability

while preserving deterministic trading behavior.

---

# Core Principle

AI NEVER makes trading decisions.

All decisions originate exclusively from:

👉 TradingPipeline (deterministic source of truth)

AI only explains outputs.

---

# Current System State

## Backend

🟢 Stable / Production Ready

All trading logic is complete and locked.

---

## Desktop

🟢 Active Development

Focus:

- chart rendering system
- workspace architecture
- reusable UI components

---

## Chart System

🟢 ChartCanvas Framework in progress

Now includes:

- ChartCanvas
- ChartViewport
- ChartLayer system
- AxisLayer
- GridLayer
- LineSeriesLayer
- ValueLabelLayer
- OverlayLayer
- ChartCanvasBuilder
- LineChartWidget refactor (lightweight)

---

# Architecture Overview

# Current Sprint Details

## Sprint 4.5 — ChartCanvas Framework

### Completed

✔ Workspace Foundation integration  
✔ Chart Foundation integration  
✔ Production Chart Pipeline  
✔ ChartCanvas Framework initial implementation  

---

### ChartCanvas Framework Components

✔ ChartCanvas  
✔ ChartViewport  
✔ ChartLayer  
✔ AxisLayer  
✔ GridLayer  
✔ LineSeriesLayer  
✔ ValueLabelLayer  
✔ OverlayLayer  
✔ ChartCanvasBuilder  
✔ LineChartWidget refactor (lightweight container)

---

### Architecture Behavior

The system is now fully separated into:

- Presentation models (GuiChart)
- Widget orchestration (Factory)
- Widget composition (LineChartWidget)
- Canvas composition (ChartCanvasBuilder)
- Rendering (ChartCanvas)
- Drawing (ChartLayers)

---

# Current Focus Areas

Sprint 4.5 continues with:

### 1. Visualization Expansion
- reusable layer extensions
- overlay enhancements
- annotation system
- crosshair system

### 2. Chart System Evolution
- candlestick preparation
- portfolio allocation visualization
- heatmap rendering foundation
- gauge widgets support

### 3. UI/UX Improvements
- dashboard layout 2.0 preparation
- spacing & alignment polish
- responsive rendering improvements

---

# Technical Constraints

These rules are mandatory:

- NO business logic in UI
- NO calculations in widgets
- NO AI logic in frontend
- NO trading logic outside backend
- ChartCanvas = painting only
- ChartLayers = drawing only
- Builder = composition only
- Widgets = presentation only

---

# Validation Rules

Before every commit:

```bash
python run_tests.py