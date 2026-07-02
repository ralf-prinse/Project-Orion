from dataclasses import dataclass
from typing import Any

from providers.yahoo_provider import YahooProvider
from services.intelligence.indicator_builder import IndicatorBuilder
from services.logging_service import LoggingService
from services.orchestration.trading_pipeline import TradingPipeline


@dataclass(frozen=True)
class AIMarketScanItem:
    symbol: str
    decision: str
    confidence: float
    pressure_score: float
    buy_pressure: float
    sell_pressure: float
    strength: float
    position_size: float
    risk_score: float
    expected_risk: float
    explanation: str
    pipeline_result: dict[str, Any]


@dataclass(frozen=True)
class AIMarketScanResult:
    total_requested: int
    total_scanned: int
    total_failed: int
    best_trade: AIMarketScanItem | None
    ranked: list[AIMarketScanItem]
    failed_symbols: list[str]


class AIMarketScanner:
    """
    AI-powered multi-asset scanner.

    Flow

    Symbol
        ↓
    YahooProvider
        ↓
    IndicatorBuilder
        ↓
    TradingPipeline
        ↓
    Ranked AI scan result
    """

    def __init__(
        self,
        provider: YahooProvider | None = None,
        indicator_builder: IndicatorBuilder | None = None,
        trading_pipeline: TradingPipeline | None = None,
    ):
        self.logger = LoggingService.get_logger("AIMarketScanner")

        self.provider = provider or YahooProvider()
        self.indicator_builder = indicator_builder or IndicatorBuilder()
        self.trading_pipeline = trading_pipeline or TradingPipeline()

    def scan(
        self,
        symbols: list[str],
        portfolio_state,
        period: str = "6mo",
        interval: str = "1d",
    ) -> AIMarketScanResult:

        cleaned_symbols = self._clean_symbols(symbols)

        self.logger.info(
            "Starting market scan (%d symbols)",
            len(cleaned_symbols),
        )

        scanned: list[AIMarketScanItem] = []
        failed_symbols: list[str] = []

        for symbol in cleaned_symbols:

            try:

                self.logger.info(
                    "Scanning %s",
                    symbol,
                )

                item = self.scan_symbol(
                    symbol=symbol,
                    portfolio_state=portfolio_state,
                    period=period,
                    interval=interval,
                )

                scanned.append(item)

                self.logger.info(
                    "%s complete | %s | confidence=%.3f",
                    item.symbol,
                    item.decision,
                    item.confidence,
                )

            except Exception as error:

                failed_symbols.append(symbol)

                self.logger.exception(
                    "Scan failed for %s: %s",
                    symbol,
                    error,
                )

        ranked = sorted(
            scanned,
            key=self._ranking_score,
            reverse=True,
        )

        self.logger.info(
            (
                "Market scan completed | "
                "requested=%d scanned=%d failed=%d"
            ),
            len(cleaned_symbols),
            len(ranked),
            len(failed_symbols),
        )

        return AIMarketScanResult(
            total_requested=len(cleaned_symbols),
            total_scanned=len(ranked),
            total_failed=len(failed_symbols),
            best_trade=ranked[0] if ranked else None,
            ranked=ranked,
            failed_symbols=failed_symbols,
        )

    def scan_symbol(
        self,
        symbol: str,
        portfolio_state,
        period: str = "6mo",
        interval: str = "1d",
    ) -> AIMarketScanItem:

        cleaned_symbol = symbol.strip().upper()

        if not cleaned_symbol:
            raise ValueError("Symbol may not be empty.")

        history = self.provider.get_historical_data(
            cleaned_symbol,
            period=period,
            interval=interval,
        )

        indicators = self.indicator_builder.build(
            symbol=cleaned_symbol,
            history=history,
        )

        result = self.trading_pipeline.run(
            indicator_data=indicators,
            portfolio_state=portfolio_state,
        )

        pipeline = result["pipeline"]
        explanation = result["explanation"]

        explanation_text = self._format_explanation(
            explanation
        )

        return AIMarketScanItem(
            symbol=pipeline["symbol"],
            decision=pipeline["decision"],
            confidence=pipeline["confidence"],
            pressure_score=pipeline["pressure_score"],
            buy_pressure=pipeline["buy_pressure"],
            sell_pressure=pipeline["sell_pressure"],
            strength=pipeline["strength"],
            position_size=pipeline["position_size"],
            risk_score=pipeline["risk_score"],
            expected_risk=pipeline["expected_risk"],
            explanation=explanation_text,
            pipeline_result=result,
        )

    def actionable_trades(
        self,
        scan_result: AIMarketScanResult,
        minimum_confidence: float = 0.60,
    ) -> list[AIMarketScanItem]:

        return [
            item
            for item in scan_result.ranked
            if item.decision in ("BUY", "SELL")
            and item.confidence >= minimum_confidence
        ]

    def _clean_symbols(
        self,
        symbols: list[str],
    ) -> list[str]:

        cleaned = []

        for symbol in symbols:

            value = symbol.strip().upper()

            if value and value not in cleaned:
                cleaned.append(value)

        return cleaned

    def _ranking_score(
        self,
        item: AIMarketScanItem,
    ) -> float:

        return (
            item.pressure_score
            * item.confidence
            * item.strength
            - item.risk_score
        )

    def _format_explanation(
        self,
        explanation: dict[str, Any],
    ) -> str:

        details = explanation.get(
            "details",
            [],
        )

        if not details:
            return "Geen AI-uitleg beschikbaar."

        return "\n".join(
            f"• {line}"
            for line in details
        )