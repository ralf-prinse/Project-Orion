from __future__ import annotations

from models.hypothesis_evaluation import HypothesisEvaluation
from models.hypothesis_evaluation_context import (
    HypothesisEvaluationContext,
)


class HypothesisEvaluator:
    """
    Deterministic evaluator for strategy hypotheses.

    Architecture:

        HypothesisEvaluationContext
                    ↓
          HypothesisEvaluator
                    ↓
         HypothesisEvaluation

    No AI.
    No trading.
    No configuration changes.
    """

    def evaluate(
        self,
        context: HypothesisEvaluationContext,
    ) -> HypothesisEvaluation:

        confidence = self._calculate_confidence(context)

        supported = self._is_supported(context)

        status = self._status(context, supported)

        reason = self._reason(context, supported)

        return HypothesisEvaluation(
            hypothesis=context.hypothesis,
            sample_size=context.sample_size,
            metric_value=round(context.metric_value, 6),
            expected_value=round(context.expected_value, 6),
            confidence=confidence,
            supported=supported,
            status=status,
            reason=reason,
        )

    def _is_supported(
        self,
        context: HypothesisEvaluationContext,
    ) -> bool:

        hypothesis = context.hypothesis

        if context.sample_size < hypothesis.minimum_sample_size:
            return False

        if hypothesis.expected_direction == "INCREASE":
            return context.metric_value >= context.expected_value

        if hypothesis.expected_direction == "DECREASE":
            return context.metric_value <= context.expected_value

        return abs(
            context.metric_value - context.expected_value
        ) <= 0.000001

    def _calculate_confidence(
        self,
        context: HypothesisEvaluationContext,
    ) -> float:

        hypothesis = context.hypothesis

        if context.sample_size <= 0:
            return 0.0

        sample_confidence = min(
            1.0,
            context.sample_size / hypothesis.minimum_sample_size,
        )

        distance = abs(
            context.metric_value - context.expected_value
        )

        if context.expected_value == 0:
            metric_confidence = (
                1.0 if distance == 0 else 0.5
            )
        else:
            metric_confidence = min(
                1.0,
                distance / abs(context.expected_value),
            )

        return round(
            (sample_confidence * 0.7)
            + (metric_confidence * 0.3),
            6,
        )

    def _status(
        self,
        context: HypothesisEvaluationContext,
        supported: bool,
    ) -> str:

        if (
            context.sample_size
            < context.hypothesis.minimum_sample_size
        ):
            return "INSUFFICIENT_DATA"

        if supported:
            return "SUPPORTED"

        return "REJECTED"

    def _reason(
        self,
        context: HypothesisEvaluationContext,
        supported: bool,
    ) -> str:

        hypothesis = context.hypothesis

        if context.sample_size < hypothesis.minimum_sample_size:
            return (
                "Insufficient data to evaluate hypothesis. "
                f"Sample size={context.sample_size}, "
                f"required={hypothesis.minimum_sample_size}."
            )

        if supported:
            return (
                f"Hypothesis supported. "
                f"{hypothesis.metric_name}: "
                f"{context.metric_value:.6f} "
                f"(expected {context.expected_value:.6f})."
            )

        return (
            f"Hypothesis rejected. "
            f"{hypothesis.metric_name}: "
            f"{context.metric_value:.6f} "
            f"(expected {context.expected_value:.6f})."
        )