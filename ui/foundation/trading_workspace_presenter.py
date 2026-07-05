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

        confidence = self._number(pipeline.get("confidence", 0.0))
        pressure_score = self._number(pipeline.get("pressure_score", 0.0))
        position_size = self._number(pipeline.get("position_size", 0.0))
        risk_score = self._number(pipeline.get("risk_score", 0.0))
        expected_risk = self._number(pipeline.get("expected_risk", 0.0))

        return TradingWorkspaceViewModel(
            decision=str(pipeline.get("decision", "-")),
            decision_reason=self._decision_reason(pipeline),

            confidence=f"{confidence:.1%}",
            confidence_subtitle=self._confidence_explanation(confidence),

            pressure_score=f"{pressure_score:.3f}",
            pressure_subtitle=self._pressure_explanation(pressure_score, pipeline),

            position_size=f"€{position_size:,.2f}",
            position_subtitle=self._position_explanation(
                position_size=position_size,
                expected_risk=expected_risk,
            ),

            risk_score=f"{risk_score:.4f}",
            risk_subtitle=self._risk_explanation(risk_score, pipeline),

            explanation=self._explanation_text(
                explanation=explanation,
                pipeline=pipeline,
            ),

            status="Analyse voltooid.",
        )

    def _decision_reason(self, pipeline: dict) -> str:
        decision = str(pipeline.get("decision", "-")).upper()
        reason = str(pipeline.get("reason", "")).strip()

        if decision == "BUY":
            prefix = "Koopsignaal volgens de deterministische pipeline."
        elif decision == "SELL":
            prefix = "Verkoopsignaal volgens de deterministische pipeline."
        elif decision == "HOLD":
            prefix = "Geen duidelijke koop- of verkoopsituatie."
        else:
            prefix = "Pipeline-uitkomst beschikbaar."

        if reason:
            return f"{prefix} {reason}"

        return prefix

    def _confidence_explanation(self, confidence: float) -> str:
        if confidence >= 0.80:
            label = "Hoog"
            meaning = "de signalen ondersteunen de beslissing sterk."
        elif confidence >= 0.60:
            label = "Gemiddeld"
            meaning = "de signalen ondersteunen de beslissing redelijk."
        else:
            label = "Laag"
            meaning = "de signalen zijn gemengd of zwak."

        return f"{label} vertrouwen: {meaning}"

    def _pressure_explanation(self, pressure_score: float, pipeline: dict) -> str:
        features = pipeline.get("features", {})

        trend = self._number(features.get("trend", 0.0))
        momentum = self._number(features.get("momentum", 0.0))
        rsi = self._number(features.get("rsi", 0.0))
        volatility = self._number(features.get("volatility", 0.0))

        if pressure_score >= 0.75:
            label = "Sterke positieve marktdruk"
        elif pressure_score >= 0.60:
            label = "Matig positieve marktdruk"
        elif pressure_score >= 0.45:
            label = "Neutrale marktdruk"
        else:
            label = "Zwakke marktdruk"

        return (
            f"{label}. Gebaseerd op trend ({trend:.2f}), "
            f"momentum ({momentum:.2f}), RSI ({rsi:.2f}) "
            f"en volatiliteit ({volatility:.4f})."
        )

    def _position_explanation(
        self,
        position_size: float,
        expected_risk: float,
    ) -> str:
        if position_size <= 0:
            return (
                "Geen positie voorgesteld. Dit kan komen door onvoldoende "
                "kapitaal of onvoldoende sterke signalen."
            )

        return (
            "Aanbevolen positiewaarde op basis van beschikbaar kapitaal, "
            f"signaalsterkte en volatiliteit. Verwacht risico: €{expected_risk:,.2f}."
        )

    def _risk_explanation(self, risk_score: float, pipeline: dict) -> str:
        volatility = str(pipeline.get("volatility", "UNKNOWN")).upper()
        features = pipeline.get("features", {})
        trend = self._number(features.get("trend", 0.0))

        if risk_score < 0.01:
            label = "Zeer laag risico"
        elif risk_score < 0.05:
            label = "Laag risico"
        elif risk_score < 0.15:
            label = "Gemiddeld risico"
        else:
            label = "Hoog risico"

        return (
            f"{label}. Gebaseerd op volatiliteit ({volatility}) "
            f"en trendsterkte ({trend:.2f})."
        )

    def _explanation_text(self, explanation: dict, pipeline: dict) -> str:
        details = explanation.get("details", [])

        lines = [
            "Deze analyse is deterministisch berekend door de Orion TradingPipeline.",
            "",
            "Wat betekenen de belangrijkste waarden?",
            "",
            f"• Pressure Score: {self._pressure_explanation(self._number(pipeline.get('pressure_score', 0.0)), pipeline)}",
            f"• Confidence: {self._confidence_explanation(self._number(pipeline.get('confidence', 0.0)))}",
            f"• Risk: {self._risk_explanation(self._number(pipeline.get('risk_score', 0.0)), pipeline)}",
            "",
            "AI-uitleg:",
        ]

        if details:
            lines.extend(f"• {line}" for line in details)
        else:
            lines.append("• Geen aanvullende AI-uitleg beschikbaar.")

        return "\n".join(lines)

    def _number(self, value) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0