from dataclasses import dataclass


@dataclass(frozen=True)
class TradingWorkspaceViewModel:
    decision: str
    decision_reason: str

    confidence: str
    confidence_subtitle: str

    pressure_score: str
    pressure_subtitle: str

    position_size: str
    position_subtitle: str

    risk_score: str
    risk_subtitle: str

    explanation: str

    status: str


class TradingWorkspacePresenter:
    """
    Converts TradingPipeline output into UI-ready values.

    Contains presentation logic only.
    No trading logic.
    """

    def create_view_model(self, pipeline_result: dict) -> TradingWorkspaceViewModel:
        pipeline = pipeline_result.get("pipeline", {})
        explanation = pipeline_result.get("explanation", {})

        details = explanation.get("details", [])

        if details:
            explanation_text = "\n".join(
                f"• {line}" for line in details
            )
        else:
            explanation_text = "Geen AI-uitleg beschikbaar."

        return TradingWorkspaceViewModel(
            decision=str(
                pipeline.get("decision", "-")
            ),
            decision_reason=str(
                pipeline.get("reason", "")
            ),

            confidence=f"{pipeline.get('confidence', 0):.1%}",
            confidence_subtitle="Decision confidence",

            pressure_score=f"{pipeline.get('pressure_score', 0):.3f}",
            pressure_subtitle="Market pressure",

            position_size=f"{pipeline.get('position_size', 0):.2f}",
            position_subtitle="Recommended position",

            risk_score=f"{pipeline.get('risk_score', 0):.4f}",
            risk_subtitle="Estimated risk",

            explanation=explanation_text,

            status="Analyse voltooid.",
        )