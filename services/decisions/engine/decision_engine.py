from core.orchestration.analyzer_runner import AnalyzerRunner
from services.decisions.models import DecisionContext, DecisionResult, DecisionState
from services.decisions.registry import DecisionRegistry
from services.signals.models import SignalResult


class DecisionEngine:
    """
    Centrale Decision Engine van Project Orion.

    De Decision Engine vertaalt SignalResult en DecisionContext naar
    DecisionResult.

    De engine:
    - bevat zelf geen beslislogica
    - gebruikt DecisionRegistry voor analyzer-volgorde
    - gebruikt AnalyzerRunner voor generieke orchestratie
    - retourneert een deterministisch DecisionResult
    """

    def __init__(
        self,
        decision_registry: DecisionRegistry | None = None,
        analyzer_runner: AnalyzerRunner | None = None,
    ):
        self.decision_registry = decision_registry or DecisionRegistry()
        self.analyzer_runner = analyzer_runner or AnalyzerRunner()

    def decide(
        self,
        signal_result: SignalResult,
        decision_context: DecisionContext | None = None,
    ) -> DecisionResult:
        context = decision_context or DecisionContext()

        decision_state = DecisionState(
            symbol=signal_result.symbol,
        )

        decision_state = self.analyzer_runner.run(
            registry=self.decision_registry,
            result=decision_state,
            analyzer_executor=lambda analyzer_definition, state: (
                analyzer_definition.analyzer.analyze(
                    signal_result=signal_result,
                    decision_context=context,
                    decision_state=state,
                )
            ),
        )

        return self._build_result(decision_state)

    def _build_result(
        self,
        decision_state: DecisionState,
    ) -> DecisionResult:
        return DecisionResult(
            symbol=decision_state.symbol,
            action=decision_state.proposed_action,
            confidence=decision_state.confidence,
            position_size=decision_state.position_size,
            risk_level=decision_state.risk_level,
            reasons=list(decision_state.reasons),
            warnings=list(decision_state.warnings),
        )