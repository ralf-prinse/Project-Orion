from typing import Any

from core.orchestration.scan_step import ScanStepResult


class ScanPipelineStep:
    """
    Adapter that exposes the existing scanner pipeline as a ScanStep.

    This keeps the current scanner implementation intact while allowing the
    ScanOrchestrator to coordinate it through the same deterministic step
    contract that future universe, market-data, decision, planner and GUI/API
    integration steps can use.
    """

    name = "scan_pipeline"

    def __init__(self, scan_pipeline: Any):
        self.scan_pipeline = scan_pipeline

    def run(self, payload: Any) -> ScanStepResult:
        symbols = list(payload or [])
        pipeline_result = self.scan_pipeline.run(symbols)

        opportunities = list(getattr(pipeline_result, "opportunities", []) or [])
        pipeline_status = getattr(pipeline_result, "status", None)

        symbols_processed = None
        symbols_failed = None
        opportunities_count = len(opportunities)
        messages: list[str] = []

        if pipeline_status is not None:
            technical_results_count = getattr(
                pipeline_status,
                "technical_results_count",
                None,
            )
            if technical_results_count is not None:
                symbols_processed = int(technical_results_count)
                symbols_failed = max(0, len(symbols) - symbols_processed)

            status_opportunities_count = getattr(
                pipeline_status,
                "opportunities_count",
                None,
            )
            if status_opportunities_count is not None:
                opportunities_count = int(status_opportunities_count)

            messages.extend(getattr(pipeline_status, "messages", []) or [])

        return ScanStepResult(
            payload=pipeline_result,
            opportunities=opportunities,
            pipeline_status=pipeline_status,
            symbols_processed=symbols_processed,
            symbols_failed=symbols_failed,
            opportunities_count=opportunities_count,
            messages=messages,
        )
