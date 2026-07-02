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

    Runs smoke tests and integration tests in a predictable order.
    """

    def __init__(self):
        self.commands = [
            TestCommand(
                name="Trading Pipeline",
                command=[sys.executable, "test_trading_pipeline.py"],
            ),
            TestCommand(
                name="Decision Smoke",
                command=[sys.executable, "test_decision_smoke.py"],
            ),
            TestCommand(
                name="Intelligence Layer",
                command=[sys.executable, "test_intelligence_layer.py"],
            ),
            TestCommand(
                name="AI Market Scanner",
                command=[sys.executable, "test_ai_market_scanner.py"],
            ),
            TestCommand(
                name="AI Scanner Presenter",
                command=[sys.executable, "test_ai_scanner_presenter.py"],
            ),
            TestCommand(
                name="Backtest Visualizer",
                command=[sys.executable, "test_backtest_visualizer.py"],
            ),
        ]

    def run(self):
        print("\n=========================================")
        print("ORION REGRESSION TESTS")
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
        print(f"{result.name:<25} {status}")

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