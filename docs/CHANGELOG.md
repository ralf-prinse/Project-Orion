# CHANGELOG

---

# Sprint 4.5 — ChartCanvas Framework (In Progress)

---

## Overview

Sprint 4.5 focuses on the introduction and expansion of the ChartCanvas Framework.

The goal is to fully separate:

- rendering orchestration
- widget composition
- canvas painting
- reusable drawing layers

while preserving deterministic backend architecture.

---

# Added

## ChartCanvas Framework Core

Introduced the foundational rendering engine:

- ChartCanvas
- ChartViewport
- ChartLayer abstraction

These components form the reusable rendering surface for all charts.

---

## Rendering Layers

Added reusable chart rendering layers:

- AxisLayer
- GridLayer
- LineSeriesLayer
- ValueLabelLayer

Each layer is fully presentation-only.

No business logic allowed.

No calculations beyond rendering math.

---

## Overlay System

Introduced OverlayLayer:

- reserved extension point for future visual features
- supports future:
  - crosshair
  - trade markers
  - annotations
  - selections
  - indicators

---

## ChartCanvasBuilder

Introduced ChartCanvasBuilder:

- central composition point for chart rendering
- converts GuiChart → ChartCanvas
- selects correct rendering layers
- keeps widgets lightweight

---

## Widget Refactor

### LineChartWidget

Refactored into:

- lightweight UI container
- delegates rendering to ChartCanvasBuilder
- removed internal painting logic
- removed duplicate canvas implementation

---

# Changed

## Rendering Architecture

Old structure:

# Release Summary

---

# Sprint 4.5 — ChartCanvas Framework

## Status

🚧 In Progress (Feature-complete foundation stage)

---

## Completed Components

### Core Framework

✔ ChartCanvas  
✔ ChartViewport  
✔ ChartLayer system  

---

### Rendering Layers

✔ AxisLayer  
✔ GridLayer  
✔ LineSeriesLayer  
✔ ValueLabelLayer  
✔ OverlayLayer  

---

### Composition Layer

✔ ChartCanvasBuilder  

---

### Widget Layer

✔ LineChartWidget refactor (lightweight container)  

---

# Architecture Impact

## Before Sprint 4.5

- Widgets directly handled painting
- Chart logic embedded in UI components
- Tight coupling between UI and rendering

---

## After Sprint 4.5
