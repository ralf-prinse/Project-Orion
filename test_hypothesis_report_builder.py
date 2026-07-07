from datetime import datetime

from models.hypothesis_evaluation import HypothesisEvaluation
from models.hypothesis_evaluation_report import (
    HypothesisEvaluationReport,
)
from models.strategy_hypothesis import StrategyHypothesis
from services.hypothesis_report_builder import (
    HypothesisReportBuilder,
)


def build_hypothesis() -> StrategyHypothesis:
    return StrategyHypothesis(
        hypothesis_id="HYP-001",
        title="Increase win rate",
        description="Regression test.",
        metric_name="win_rate",
        expected_direction="INCREASE",
        minimum_sample_size=10,
        created_at=datetime(2026, 7, 7),
    )


def build_evaluation(
    status: str,
    supported: bool,
) -> HypothesisEvaluation:
    return HypothesisEvaluation(
        hypothesis=build_hypothesis(),
        sample_size=25,
        metric_value=0.60,
        expected_value=0.55,
        confidence=0.92,
        supported=supported,
        status=status,
        reason="Regression test.",
    )


def test_build_report():
    evaluations = [
        build_evaluation(
            status="SUPPORTED",
            supported=True,
        ),
        build_evaluation(
            status="REJECTED",
            supported=False,
        ),
        build_evaluation(
            status="INSUFFICIENT_DATA",
            supported=False,
        ),
    ]

    report = HypothesisReportBuilder().build(
        evaluations=evaluations,
    )

    assert isinstance(
        report,
        HypothesisEvaluationReport,
    )

    assert report.total == 3
    assert report.supported == 1
    assert report.rejected == 1
    assert report.insufficient_data == 1
    assert report.support_ratio == round(1 / 3, 4)