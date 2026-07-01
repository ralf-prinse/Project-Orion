from dataclasses import dataclass, field

import pytest

from core.orchestration import ScanContext, ScanOrchestrator, ScanStatistics


@dataclass
class FakePipelineStatus:
    technical_results_count: int = 2
    opportunities_count: int = 1
    quote_seconds: float = 0.1
    price_filter_seconds: float = 0.2
    volume_filter_seconds: float = 0.3
    liquidity_filter_seconds: float = 0.4
    relative_strength_seconds: float = 0.5
    momentum_seconds: float = 0.6
    technical_scanner_seconds: float = 0.7
    ranking_seconds: float = 0.8
    messages: list[str] = field(default_factory=lambda: ["Pipeline klaar."])


@dataclass
class FakePipelineResult:
    opportunities: list[str]
    status: FakePipelineStatus


class FakePipeline:
    def __init__(self):
        self.received_symbols: list[str] = []

    def run(self, symbols: list[str]) -> FakePipelineResult:
        self.received_symbols = list(symbols)
        return FakePipelineResult(
            opportunities=["AAPL"],
            status=FakePipelineStatus(),
        )


class FailingPipeline:
    def run(self, symbols: list[str]):
        raise RuntimeError("provider unavailable")


class FakeClock:
    def __init__(self):
        self.value = 0.0

    def __call__(self):
        self.value += 1.0
        return self.value


def test_scan_context_resolves_symbols_deterministically():
    context = ScanContext(symbols=[" aapl ", "MSFT", "aapl", "", " nvda"])

    assert context.resolved_symbols() == ["AAPL", "MSFT", "NVDA"]


def test_scan_context_emits_progress_updates():
    updates = []
    context = ScanContext(
        symbols=["AAPL"],
        progress_callback=updates.append,
    )

    context.emit_progress(
        stage="test",
        message="Testing",
        percent=50.0,
        current=1,
        total=2,
    )

    assert len(updates) == 1
    assert updates[0].stage == "test"
    assert updates[0].message == "Testing"
    assert updates[0].percent == 50.0


def test_scan_statistics_records_timings_messages_and_errors():
    statistics = ScanStatistics()

    statistics.add_timing("analysis", 1.23456789)
    statistics.add_message("message")
    statistics.add_error("error")

    assert statistics.timings[0].stage == "analysis"
    assert statistics.timings[0].duration_seconds == 1.234568
    assert statistics.messages == ["message"]
    assert statistics.errors == ["error"]
    assert statistics.success is False


def test_scan_orchestrator_runs_pipeline_with_clean_symbols():
    pipeline = FakePipeline()
    orchestrator = ScanOrchestrator(
        scan_pipeline=pipeline,
        clock=FakeClock(),
    )

    summary = orchestrator.run([" aapl ", "MSFT", "aapl"])

    assert pipeline.received_symbols == ["AAPL", "MSFT"]
    assert summary.success is True
    assert summary.opportunities == ["AAPL"]
    assert summary.opportunities_count == 1
    assert summary.statistics.symbols_requested == 2
    assert summary.statistics.symbols_processed == 2
    assert summary.statistics.symbols_failed == 0
    assert "Pipeline klaar." in summary.messages


def test_scan_orchestrator_copies_pipeline_timings():
    orchestrator = ScanOrchestrator(
        scan_pipeline=FakePipeline(),
        clock=FakeClock(),
    )

    summary = orchestrator.run(["AAPL"])
    timing_stages = [timing.stage for timing in summary.statistics.timings]

    assert "scan_pipeline" in timing_stages
    assert "quotes" in timing_stages
    assert "technical_scanner" in timing_stages
    assert "ranking" in timing_stages


def test_scan_orchestrator_handles_empty_symbol_list_without_pipeline_call():
    pipeline = FakePipeline()
    orchestrator = ScanOrchestrator(
        scan_pipeline=pipeline,
        clock=FakeClock(),
    )

    summary = orchestrator.run([])

    assert pipeline.received_symbols == []
    assert summary.success is True
    assert summary.opportunities == []
    assert summary.statistics.symbols_requested == 0
    assert "Geen symbolen ontvangen." in summary.messages


def test_scan_orchestrator_records_pipeline_errors_when_continue_on_error():
    orchestrator = ScanOrchestrator(
        scan_pipeline=FailingPipeline(),
        clock=FakeClock(),
    )

    summary = orchestrator.run(ScanContext(symbols=["AAPL"], continue_on_error=True))

    assert summary.success is False
    assert summary.opportunities == []
    assert summary.statistics.symbols_failed == 1
    assert summary.errors == ["Scan failed: provider unavailable"]


def test_scan_orchestrator_reraises_pipeline_errors_when_strict():
    orchestrator = ScanOrchestrator(
        scan_pipeline=FailingPipeline(),
        clock=FakeClock(),
    )

    with pytest.raises(RuntimeError, match="provider unavailable"):
        orchestrator.run(ScanContext(symbols=["AAPL"], continue_on_error=False))


def test_scan_orchestrator_emits_start_and_completion_progress():
    updates = []
    orchestrator = ScanOrchestrator(
        scan_pipeline=FakePipeline(),
        clock=FakeClock(),
    )

    orchestrator.run(
        ScanContext(
            symbols=["AAPL"],
            progress_callback=updates.append,
        )
    )

    assert updates[0].stage == "scan"
    assert updates[0].percent == 0.0
    assert updates[-1].completed is True
    assert updates[-1].percent == 100.0

from core.orchestration import ScanStepResult


class RecordingStep:
    def __init__(self, name: str, suffix: str):
        self.name = name
        self.suffix = suffix
        self.received_payload = None

    def run(self, payload):
        self.received_payload = payload
        return ScanStepResult(
            payload=f"{payload}|{self.suffix}",
            messages=[f"{self.name} done"],
        )


class OpportunityStep:
    name = "opportunity_step"

    def run(self, payload):
        return ScanStepResult(
            payload=payload,
            opportunities=["MSFT", "NVDA"],
            symbols_processed=2,
            symbols_failed=1,
            opportunities_count=2,
        )


def test_scan_orchestrator_runs_configured_scan_steps_in_order():
    first = RecordingStep(name="first_step", suffix="first")
    second = RecordingStep(name="second_step", suffix="second")
    orchestrator = ScanOrchestrator(
        scan_steps=[first, second],
        clock=FakeClock(),
    )

    summary = orchestrator.run(["AAPL"])

    assert first.received_payload == ["AAPL"]
    assert second.received_payload == "['AAPL']|first"
    assert summary.stage_results["first_step"] == "['AAPL']|first"
    assert summary.stage_results["second_step"] == "['AAPL']|first|second"
    assert "first_step" in [timing.stage for timing in summary.statistics.timings]
    assert "second_step" in [timing.stage for timing in summary.statistics.timings]


def test_scan_orchestrator_collects_step_level_summary_data():
    orchestrator = ScanOrchestrator(
        scan_steps=[OpportunityStep()],
        clock=FakeClock(),
    )

    summary = orchestrator.run(["AAPL", "MSFT", "NVDA"])

    assert summary.opportunities == ["MSFT", "NVDA"]
    assert summary.statistics.symbols_processed == 2
    assert summary.statistics.symbols_failed == 1
    assert summary.statistics.opportunities_count == 2
    assert summary.stage_results["opportunity_step"] == ["AAPL", "MSFT", "NVDA"]


def test_scan_orchestrator_emits_progress_for_each_configured_step():
    updates = []
    orchestrator = ScanOrchestrator(
        scan_steps=[
            RecordingStep(name="first_step", suffix="first"),
            RecordingStep(name="second_step", suffix="second"),
        ],
        clock=FakeClock(),
    )

    orchestrator.run(
        ScanContext(
            symbols=["AAPL"],
            progress_callback=updates.append,
        )
    )

    stages = [update.stage for update in updates]

    assert "scan" in stages
    assert "first_step" in stages
    assert "second_step" in stages
    assert updates[-1].stage == "scan"
    assert updates[-1].completed is True
