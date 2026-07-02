class BenchmarkService:
    """
    Compares portfolio vs benchmark index.
    """

    def calculate(self, portfolio_values, benchmark_values):

        if not portfolio_values or not benchmark_values:
            return {
                "portfolio_curve": [],
                "benchmark_curve": [],
                "alpha_curve": [],
                "final_alpha_pct": 0.0,
            }

        n = min(len(portfolio_values), len(benchmark_values))

        portfolio_curve = portfolio_values[:n]
        benchmark_curve = benchmark_values[:n]

        alpha_curve = [
            p - b for p, b in zip(portfolio_curve, benchmark_curve)
        ]

        final_alpha_pct = 0.0
        if benchmark_curve[-1] != 0:
            final_alpha_pct = (
                (portfolio_curve[-1] - benchmark_curve[-1])
                / benchmark_curve[-1]
            ) * 100

        return {
            "portfolio_curve": portfolio_curve,
            "benchmark_curve": benchmark_curve,
            "alpha_curve": alpha_curve,
            "final_alpha_pct": final_alpha_pct,
        }