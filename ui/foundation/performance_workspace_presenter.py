from services.benchmark.benchmark_service import BenchmarkService
from ui.foundation.benchmark_presenter import BenchmarkPresenter
from ui.foundation.performance_presenter import PerformancePresenter
from ui.foundation.models import GuiWorkspace


class PerformanceWorkspacePresenter:
    """
    Builds the Performance Workspace including benchmark comparison.
    """

    def __init__(self):
        self._performance_presenter = PerformancePresenter()
        self._benchmark_service = BenchmarkService()
        self._benchmark_presenter = BenchmarkPresenter()

    def create_workspace(self, portfolio_state):
        # ----------------------------
        # 1. PERFORMANCE DATA
        # ----------------------------
        performance_result = portfolio_state.performance_result

        performance_charts = self._performance_presenter.present(
            performance_result
        )

        # ----------------------------
        # 2. BENCHMARK DATA
        # ----------------------------
        benchmark_result = self._benchmark_service.calculate(
            performance_result.equity_curve,
            portfolio_state.benchmark_curve,
        )

        benchmark_charts = self._benchmark_presenter.present(
            benchmark_result
        )

        benchmark_sections = self._benchmark_presenter.create_sections(
            benchmark_result
        )

        # ----------------------------
        # 3. COMBINE INTO WORKSPACE
        # ----------------------------
        return GuiWorkspace(
            cards=[],
            charts=[
                performance_charts["equity"],
                performance_charts["drawdown"],
                benchmark_charts["comparison_chart"],
                benchmark_charts["alpha_chart"],
            ],
            sections=benchmark_sections,
        )