from core.orchestration.analyzer_runner import AnalyzerRunner
from services.analysis.models import AnalysisResult
from services.signals.models import SignalResult
from services.signals.signal_registry import SignalRegistry


class SignalEngine:
    """
    Centrale Signal Engine van Project Orion.

    De Signal Engine vertaalt AnalysisResult naar SignalResult.

    Sprint 8.2.1:
    - gebruikt AnalyzerRunner voor generieke orchestratie
    - haalt signal analyzers op uit SignalRegistry
    - voert analyzers uit in deterministische volgorde
    - bevat zelf geen tradinglogica
    """

    def __init__(
        self,
        signal_registry: SignalRegistry | None = None,
        analyzer_runner: AnalyzerRunner | None = None,
    ):
        self.signal_registry = signal_registry or SignalRegistry()
        self.analyzer_runner = analyzer_runner or AnalyzerRunner()

    def generate(
        self,
        analysis_result: AnalysisResult,
    ) -> SignalResult:
        signal_result = SignalResult(
            symbol=analysis_result.symbol,
        )

        signal_result = self.analyzer_runner.run(
            registry=self.signal_registry,
            result=signal_result,
            analyzer_executor=lambda analyzer_definition, result: (
                analyzer_definition.analyzer.analyze(
                    analysis_result=analysis_result,
                    signal_result=result,
                )
            ),
        )

        signal_result.add_note(
            f"Final signal: {signal_result.signal.value} "
            f"with confidence {signal_result.confidence}"
        )

        return signal_result