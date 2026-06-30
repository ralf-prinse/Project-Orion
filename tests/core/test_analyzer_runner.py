from core.orchestration.analyzer_runner import AnalyzerRunner


class StubRegistry:
    def get_analyzers(self):
        return [
            "first",
            "second",
            "third",
        ]


def test_analyzer_runner_executes_registry_in_order():
    executed = []

    runner = AnalyzerRunner()

    result = runner.run(
        registry=StubRegistry(),
        result=[],
        analyzer_executor=lambda analyzer, result: (
            executed.append(analyzer),
            result,
        )[1],
    )

    assert result == []

    assert executed == [
        "first",
        "second",
        "third",
    ]


def test_analyzer_runner_returns_updated_result():
    runner = AnalyzerRunner()

    result = runner.run(
        registry=StubRegistry(),
        result=0,
        analyzer_executor=lambda analyzer, value: value + 1,
    )

    assert result == 3