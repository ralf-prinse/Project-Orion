from services.market_data.base_provider import MarketDataProviderStats, MarketQuote
from ui.foundation.models import GuiMetric, GuiSection


class MarketDataPresenter:
    """
    Builds display-only market data dashboard sections for the GUI.

    The presenter consumes Quote objects and optional MarketDataProviderStats from the
    Market Data / Scanner infrastructure. It formats already retrieved market
    data for presentation only and never downloads quotes, validates providers,
    calculates indicators, generates signals or makes trading decisions.
    """

    def create_sections(
        self,
        quotes: list[MarketQuote],
        stats: MarketDataProviderStats | None = None,
    ) -> list[GuiSection]:
        return [
            self._create_summary_section(quotes, stats),
            self._create_quote_table_section(quotes),
            self._create_statistics_section(stats),
        ]

    def _create_summary_section(
        self,
        quotes: list[MarketQuote],
        stats: MarketDataProviderStats | None,
    ) -> GuiSection:
        symbols = [quote.symbol.upper() for quote in quotes]
        return GuiSection(
            title="Market Data Dashboard",
            description="Display-only view of deterministic market data output.",
            metrics=[
                GuiMetric("Quote Count", str(len(quotes))),
                GuiMetric("Symbols", ", ".join(symbols) if symbols else "None"),
                GuiMetric("Requested Symbols", str(stats.requested_symbols) if stats else "N/A"),
                GuiMetric("Presentation Only", "Yes"),
            ],
        )

    def _create_quote_table_section(self, quotes: list[MarketQuote]) -> GuiSection:
        metrics: list[GuiMetric] = []
        for quote in sorted(quotes, key=lambda item: item.symbol.upper()):
            metrics.extend(
                [
                    GuiMetric(f"{quote.symbol.upper()} Price", self._format_money(quote.price)),
                    GuiMetric(f"{quote.symbol.upper()} Volume", self._format_int(quote.volume)),
                    GuiMetric(
                        f"{quote.symbol.upper()} Previous Close",
                        self._format_optional_money(quote.previous_close),
                    ),
                    GuiMetric(
                        f"{quote.symbol.upper()} Change %",
                        self._format_optional_percent(quote.change_percent),
                    ),
                ]
            )

        if not metrics:
            metrics.append(GuiMetric("Quotes", "None"))

        return GuiSection(
            title="Quotes",
            description="Latest quote values supplied by the market data layer before reaching the GUI.",
            metrics=metrics,
        )

    def _create_statistics_section(self, stats: MarketDataProviderStats | None) -> GuiSection:
        if stats is None:
            metrics = [GuiMetric("Statistics", "N/A")]
        else:
            metrics = [
                GuiMetric("Requested Symbols", str(stats.requested_symbols)),
                GuiMetric("Provider", stats.provider_name or "N/A"),
                GuiMetric("Received Quotes", str(stats.received_quotes)),
                GuiMetric("Missing Quotes", str(stats.missing_quotes)),
                GuiMetric("Duration Seconds", f"{stats.duration_seconds:.2f}"),
            ]

        return GuiSection(
            title="Quote Service Statistics",
            description="Operational statistics produced outside the GUI layer.",
            metrics=metrics,
        )

    def _format_money(self, value: float) -> str:
        return f"${value:.2f}"

    def _format_optional_money(self, value: float | None) -> str:
        if value is None:
            return "N/A"
        return self._format_money(value)

    def _format_optional_percent(self, value: float | None) -> str:
        if value is None:
            return "N/A"
        return f"{value:.2f}%"

    def _format_int(self, value: int) -> str:
        return f"{value:,}"
