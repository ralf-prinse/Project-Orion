import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TestCommand:
    name: str
    command: list[str]


@dataclass(frozen=True)
class TestResult:
    name: str
    passed: bool
    output: str


class OrionTestRunner:
    """
    Central regression test runner for Project Orion.

    Runs all deterministic regression tests in a predictable order.
    """

    def __init__(self):
        self.commands = [
            TestCommand("Trading Pipeline", [sys.executable, "test_trading_pipeline.py"]),
            TestCommand("Trading Pipeline Result", [sys.executable, "test_trading_pipeline_result.py"]),
            TestCommand("Investment Thesis Builder", [sys.executable, "test_investment_thesis_builder.py"]),
            TestCommand("Strategy Thesis Pipeline", [sys.executable, "test_strategy_thesis_pipeline.py"]),
            TestCommand("Decision Smoke", [sys.executable, "test_decision_smoke.py"]),
            TestCommand("Intelligence Layer", [sys.executable, "test_intelligence_layer.py"]),
            TestCommand("AI Market Scanner", [sys.executable, "test_ai_market_scanner.py"]),
            TestCommand("AI Scanner Presenter", [sys.executable, "test_ai_scanner_presenter.py"]),
            TestCommand("Backtest Visualizer", [sys.executable, "test_backtest_visualizer.py"]),
            TestCommand("Trading Config", [sys.executable, "test_trading_config.py"]),
            TestCommand("Live Paper Market Scanner", [sys.executable, "test_live_paper_market_scanner.py"]),
            TestCommand("Provider Retry Policy", [sys.executable, "test_provider_retry_policy.py"]),
            TestCommand("Provider Statistics", [sys.executable, "test_provider_statistics.py"]),
            TestCommand("Adaptive Risk Engine", [sys.executable, "test_adaptive_risk_engine.py"]),
            TestCommand("Break Even Service", [sys.executable, "test_break_even_service.py"]),
            TestCommand("Trailing Stop Service", [sys.executable, "test_trailing_stop_service.py"]),
            TestCommand("Hypothesis Evaluator", [sys.executable, "test_hypothesis_evaluator.py"]),
            TestCommand(
    "Hypothesis Context Builder",
    [sys.executable, "test_hypothesis_context_builder.py"],
),
TestCommand(
    "Hypothesis Evaluation Service",
    [sys.executable, "test_hypothesis_evaluation_service.py"],
),
TestCommand(
    "Hypothesis Report Builder",
    [sys.executable, "test_hypothesis_report_builder.py"],
),
TestCommand(
    "Strategy Recommendation With Hypotheses",
    [sys.executable, "test_strategy_recommendation_with_hypotheses.py"],
),
TestCommand(
    "Learning Pipeline",
    [sys.executable, "test_learning_pipeline.py"],
),
TestCommand(
    "Dataclass Serializer",
    [sys.executable, "test_dataclass_serializer.py"],
),
TestCommand(
    "JSON Paper Portfolio Repository",
    [sys.executable, "test_json_paper_portfolio_repository.py"],
),
TestCommand(
    "Paper Trading Service Persistence",
    [sys.executable, "test_paper_trading_service_persistence.py"],
),
TestCommand(
    "Autonomous Runner Persistence",
    [sys.executable, "test_autonomous_paper_trading_runner_persistence.py"],
),
TestCommand(
    "JSONL Trade Journal Repository",
    [sys.executable, "test_jsonl_trade_journal_repository.py"],
),
TestCommand(
    "Continuous Paper Trading Runner",
    [sys.executable, "test_continuous_paper_trading_runner.py"],
),
TestCommand(
    "Runtime Supervisor",
    [sys.executable, "test_runtime_supervisor.py"],
),
TestCommand(
    "JSONL Runtime Event Repository",
    [sys.executable, "test_jsonl_runtime_event_repository.py"],
),
TestCommand(
    "Portfolio Revaluation",
    [sys.executable, "test_portfolio_revaluation_service.py"],
),
TestCommand(
    "Exit Engine",
    [sys.executable, "test_exit_engine.py"],
),
TestCommand(
    "Dashboard Service",
    [sys.executable, "test_dashboard_service.py"],
),
TestCommand(
    "Trading Dashboard CLI Presenter",
    [sys.executable, "test_trading_dashboard_cli_presenter.py"],
),
TestCommand(
    "Closed Trade Analytics Service",
    [sys.executable, "test_closed_trade_analytics_service.py"],
),
TestCommand(
    "Desktop Bootstrap",
    [sys.executable, "test_desktop_bootstrap.py"],
),
TestCommand(
    "JSON Trading Session Repository",
    [sys.executable, "test_json_trading_session_repository.py"],
),
TestCommand(
    "Autonomous Position Lifecycle",
    [sys.executable, "test_autonomous_position_lifecycle.py"],
),
            TestCommand("Position Monitor", [sys.executable, "test_position_monitor.py"]),
            TestCommand("Time Stop Service", [sys.executable, "test_time_stop_service.py"]),
            TestCommand("Trade Journal Builder", [sys.executable, "test_trade_journal_builder.py"]),
            TestCommand("Performance Analyzer", [sys.executable, "test_performance_analyzer.py"]),
            TestCommand("Strategy Recommendation Engine", [sys.executable, "test_strategy_recommendation_engine.py"]),
            TestCommand("Execution Context", [sys.executable, "test_execution_context.py"]),
            TestCommand("Execution Models", [sys.executable, "test_execution_models.py"]),
            TestCommand("Execution Validator", [sys.executable, "test_execution_validator.py"]),
            TestCommand("Execution Request Builder", [sys.executable, "test_execution_request_builder.py"]),
            TestCommand("Execution Report Builder", [sys.executable, "test_execution_report_builder.py"]),
            TestCommand("Execution Engine", [sys.executable, "test_execution_engine.py"]),
            TestCommand("Order Factory", [sys.executable, "test_order_factory.py"]),
            TestCommand("Paper Broker", [sys.executable, "test_paper_broker.py"]),
            TestCommand(
                "IBKR Account Service",
                [sys.executable, "test_ibkr_account_service.py"],
            ),
            TestCommand(
                "IBKR Broker",
                [sys.executable, "test_ibkr_broker.py"],
            ),
            TestCommand(
                "Execution Engine IBKR",
                [sys.executable, "test_execution_engine_ibkr.py"],
            ),
            TestCommand(
                "IBKR Order Transport",
                [sys.executable, "test_ibkr_order_transport.py"],
            ),
            TestCommand("Portfolio Manager", [sys.executable, "test_portfolio_manager.py"]),

            TestCommand("Position State Factory", [sys.executable, "test_position_state_factory.py"]),
            TestCommand("Position State Store", [sys.executable, "test_position_state_store.py"]),
            TestCommand("Position Update Engine", [sys.executable, "test_position_update_engine.py"]),
            TestCommand("Position Manager", [sys.executable, "test_position_manager.py"]),
            TestCommand("Position Management Summary", [sys.executable, "test_position_management_summary.py"]),
            TestCommand("Position Management Summary Builder", [sys.executable, "test_position_management_summary_builder.py"]),
            TestCommand("Portfolio Allocator", [sys.executable, "test_portfolio_allocator.py"]),
            TestCommand("Autonomous Paper Trading Runner", [sys.executable, "test_autonomous_paper_trading_runner.py"]),
            TestCommand("Paper Trading Pipeline Adapter", [sys.executable, "test_paper_trading_pipeline_adapter.py"]),
            TestCommand("Paper Trading Service", [sys.executable, "test_paper_trading_service.py"]),
            TestCommand("Paper Position Update Service", [sys.executable, "test_paper_position_update_service.py"]),
            TestCommand("Paper Position Close Service", [sys.executable, "test_paper_position_close_service.py"]),
            TestCommand("Trading Cycle", [sys.executable, "test_trading_cycle.py"]),
            TestCommand("Paper Trading Runner", [sys.executable, "test_paper_trading_runner.py"]),
            TestCommand("Typed Paper Trading Flow", [sys.executable, "test_typed_paper_trading_flow.py"]),
            TestCommand("Paper Trading Demo", [sys.executable, "test_paper_trading_demo_runner.py"]),
            TestCommand("Open Trade Store", [sys.executable, "test_open_trade_store.py"]),
            TestCommand("Trade Lifecycle Service", [sys.executable, "test_trade_lifecycle_service.py"]),
            TestCommand("Trade Monitor Service", [sys.executable, "test_trade_monitor_service.py"]),
            TestCommand("Trade Monitor Presenter", [sys.executable, "test_trade_monitor_presenter.py"]),

            TestCommand("Market Pipeline Scanner Service", [sys.executable, "test_market_pipeline_scanner_service.py"]),
            TestCommand("Opportunity Ranking Engine", [sys.executable, "test_opportunity_ranking_engine.py"]),
            TestCommand("Opportunity Ranking Scanner", [sys.executable, "test_opportunity_ranking_scanner.py"]),
        ]

    def run(self):
        print("\n=========================================")
        print("ORION FULL REGRESSION TESTS")
        print("=========================================\n")

        results: list[TestResult] = []

        for test in self.commands:
            result = self._run_test(test)
            results.append(result)
            self._print_result(result)

        self._print_summary(results)

        if any(not result.passed for result in results):
            sys.exit(1)

        sys.exit(0)

    def _run_test(self, test: TestCommand) -> TestResult:
        if not Path(test.command[1]).exists():
            return TestResult(
                name=test.name,
                passed=False,
                output=f"Missing test file: {test.command[1]}",
            )

        completed = subprocess.run(
            test.command,
            capture_output=True,
            text=True,
        )

        output = completed.stdout + completed.stderr

        return TestResult(
            name=test.name,
            passed=completed.returncode == 0,
            output=output.strip(),
        )

    def _print_result(self, result: TestResult):
        status = "PASS" if result.passed else "FAIL"
        print(f"{result.name:<40} {status}")

        if not result.passed:
            print("\n--- OUTPUT ---")
            print(result.output)
            print("--------------\n")

    def _print_summary(self, results: list[TestResult]):
        passed = sum(1 for result in results if result.passed)
        failed = sum(1 for result in results if not result.passed)

        print("\n=========================================")
        print("RESULT")
        print("=========================================")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")

        if failed == 0:
            print("\nORION HEALTH: EXCELLENT ✅")
        else:
            print("\nORION HEALTH: NEEDS ATTENTION ❌")


if __name__ == "__main__":
    OrionTestRunner().run()