from core.orchestration.analyzer_runner import AnalyzerRunner
from services.risk.models import RiskContext, RiskProfile, RiskResult
from services.risk.risk_registry import RiskRegistry


class RiskManager:
    """
    Centrale Risk Manager van Project Orion.

    De Risk Manager beoordeelt of voorgestelde risico's binnen het ingestelde
    risicoprofiel passen.

    De manager:
    - bevat zelf geen risk-validatielogica
    - gebruikt RiskRegistry voor analyzer-volgorde
    - gebruikt AnalyzerRunner voor generieke orchestratie
    - retourneert een deterministisch RiskResult
    """

    def __init__(
        self,
        risk_registry: RiskRegistry | None = None,
        analyzer_runner: AnalyzerRunner | None = None,
    ):
        self.risk_registry = risk_registry or RiskRegistry()
        self.analyzer_runner = analyzer_runner or AnalyzerRunner()

    def evaluate(
        self,
        risk_context: RiskContext,
        risk_profile: RiskProfile | None = None,
    ) -> RiskResult:
        profile = risk_profile or RiskProfile()

        risk_result = RiskResult(
            symbol=risk_context.symbol.upper(),
        )

        return self.analyzer_runner.run(
            registry=self.risk_registry,
            result=risk_result,
            analyzer_executor=lambda analyzer_definition, result: (
                analyzer_definition.analyzer.analyze(
                    risk_context=risk_context,
                    risk_profile=profile,
                    risk_result=result,
                )
            ),
        )
