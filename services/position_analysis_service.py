from services.analysis.analysis_engine import AnalysisEngine
from providers.yahoo_provider import YahooProvider


class PositionAnalysisService:
    """
    Retrieves the latest technical analysis for an existing position.

    Responsibilities
    ----------------
    - download historical market data
    - execute AnalysisEngine
    - return AnalysisResult

    No UI.
    No trading decisions.
    No exit decisions.
    """

    def __init__(
        self,
        market_provider: YahooProvider | None = None,
        analysis_engine: AnalysisEngine | None = None,
    ):
        self.market_provider = market_provider or YahooProvider()
        self.analysis_engine = analysis_engine or AnalysisEngine()

        self.period = "6mo"
        self.interval = "1d"

    def analyze_position(
        self,
        symbol: str,
    ):
        history = self.market_provider.get_historical_data(
            symbol=symbol,
            period=self.period,
            interval=self.interval,
        )

        return self.analysis_engine.analyze(
            symbol=symbol,
            candles=history,
        )