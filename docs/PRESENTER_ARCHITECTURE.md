# PROJECT ORION — PRESENTER ARCHITECTURE

---

# Benchmark Presentation Layer

Benchmark system uses existing presenter architecture.

---

# Components

- BenchmarkService (deterministic)
- BenchmarkPresenter (pending)
- GuiChart (dual-line visualization)

---

# Output

Benchmark presentation produces:

- Portfolio curve
- Benchmark curve
- Alpha KPI section

---

# Rules

- Presenters do NOT compute values
- Services do NOT format values
- GUI does NOT calculate anything

---

# Integration

BenchmarkPresenter integrates into:

WorkspacePresenter → GuiWorkspace → ChartRenderer