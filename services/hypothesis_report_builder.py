from __future__ import annotations

from models.hypothesis_evaluation import HypothesisEvaluation
from models.hypothesis_evaluation_report import HypothesisEvaluationReport


class HypothesisReportBuilder:
    """
    Builds immutable hypothesis evaluation reports.

    No AI.
    No trading decisions.
    No configuration changes.
    """

    def build(
        self,
        evaluations: list[HypothesisEvaluation],
    ) -> HypothesisEvaluationReport:
        return HypothesisEvaluationReport(
            evaluations=evaluations,
        )