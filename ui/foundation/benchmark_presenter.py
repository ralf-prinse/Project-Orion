from ui.foundation.models import GuiChart, GuiChartPoint, GuiSection


class BenchmarkPresenter:
    """
    Converts BenchmarkService output into:
    - Dual-line GuiChart (Portfolio vs Benchmark)
    - Alpha KPI GuiSection
    """

    def present(self, benchmark_result):
        portfolio_points = [
            GuiChartPoint(str(i), v)
            for i, v in enumerate(benchmark_result["portfolio_curve"])
        ]

        benchmark_points = [
            GuiChartPoint(str(i), v)
            for i, v in enumerate(benchmark_result["benchmark_curve"])
        ]

        alpha_points = [
            GuiChartPoint(str(i), v)
            for i, v in enumerate(benchmark_result["alpha_curve"])
        ]

        return {
            "comparison_chart": GuiChart(
                title="Portfolio vs Benchmark",
                description="Relative performance comparison",
                chart_type="line",
                points=[],  # base container (used for compatibility)
                unit="€",
                overlays={
                    "portfolio": portfolio_points,
                    "benchmark": benchmark_points,
                },
            ),
            "alpha_chart": GuiChart(
                title="Alpha Curve",
                description="Outperformance vs benchmark",
                chart_type="line",
                points=alpha_points,
                unit="€",
            ),
        }

    def create_sections(self, benchmark_result):
        """
        KPI section for benchmark performance
        """

        return [
            GuiSection(
                title="Benchmark Performance",
                metrics=[
                    type("Metric", (), {"value": f"{benchmark_result['final_alpha_pct']:.2f}%"})(),
                    type("Metric", (), {"value": "Alpha (vs benchmark)"})(),
                ],
            ),
            GuiSection(
                title="Comparison Summary",
                metrics=[
                    type("Metric", (), {"value": str(len(benchmark_result["portfolio_curve"]))})(),
                    type("Metric", (), {"value": "Data points"})(),
                ],
            ),
        ]