from core.orchestration.analyzer_runner import AnalyzerRunner
from services.portfolio.models import PortfolioContext, PortfolioResult, PortfolioState
from services.portfolio.portfolio_registry import PortfolioRegistry


class PortfolioEngine:
    """
    Centrale Portfolio Engine van Project Orion.

    De Portfolio Engine analyseert portfolio-state en voorgestelde posities.

    De engine:
    - bevat zelf geen portfolio-validatielogica
    - gebruikt PortfolioRegistry voor analyzer-volgorde
    - gebruikt AnalyzerRunner voor generieke orchestratie
    - retourneert een deterministisch PortfolioResult
    """

    def __init__(
        self,
        portfolio_registry: PortfolioRegistry | None = None,
        analyzer_runner: AnalyzerRunner | None = None,
    ):
        self.portfolio_registry = portfolio_registry or PortfolioRegistry()
        self.analyzer_runner = analyzer_runner or AnalyzerRunner()

    def evaluate(
        self,
        portfolio_state: PortfolioState,
        portfolio_context: PortfolioContext | None = None,
    ) -> PortfolioResult:
        context = portfolio_context or PortfolioContext()

        portfolio_result = PortfolioResult(
            symbol=context.symbol.upper(),
        )

        return self.analyzer_runner.run(
            registry=self.portfolio_registry,
            result=portfolio_result,
            analyzer_executor=lambda analyzer_definition, result: (
                analyzer_definition.analyzer.analyze(
                    portfolio_state=portfolio_state,
                    portfolio_context=context,
                    portfolio_result=result,
                )
            ),
        )
