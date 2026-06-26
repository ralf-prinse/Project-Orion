from dataclasses import dataclass, field
import time

from services.scanner.quote_service import QuoteService
from services.scanner.price_filter import PriceFilter
from services.scanner.volume_filter import VolumeFilter
from services.scanner.liquidity_filter import LiquidityFilter
from services.scanner.relative_strength_filter import RelativeStrengthFilter
from services.scanner.momentum_filter import MomentumFilter
from services.scanner.technical_scanner import TechnicalScanner
from services.scanner.ranking_engine import RankingEngine, RankedOpportunity


@dataclass
class ScanPipelineStatus:
    universe_count: int = 0

    quotes_count: int = 0
    quote_cache_hits: int = 0
    quote_fresh_downloads: int = 0
    quote_missing: int = 0
    quote_negative_cache_hits: int = 0

    market_data_provider: str = ""
    provider_requested_symbols: int = 0
    provider_received_quotes: int = 0
    provider_missing_quotes: int = 0
    provider_seconds: float = 0.0

    after_price_filter: int = 0
    after_volume_filter: int = 0
    after_liquidity_filter: int = 0
    after_relative_strength_filter: int = 0
    after_momentum_filter: int = 0
    technical_candidates_count: int = 0
    technical_results_count: int = 0
    opportunities_count: int = 0

    quote_seconds: float = 0.0
    price_filter_seconds: float = 0.0
    volume_filter_seconds: float = 0.0
    liquidity_filter_seconds: float = 0.0
    relative_strength_seconds: float = 0.0
    momentum_seconds: float = 0.0
    technical_scanner_seconds: float = 0.0
    ranking_seconds: float = 0.0
    total_seconds: float = 0.0

    messages: list[str] = field(default_factory=list)


@dataclass
class ScanPipelineResult:
    opportunities: list[RankedOpportunity]
    status: ScanPipelineStatus


class ScanPipeline:
    """
    Nieuwe schaalbare scanner-pipeline voor Project Orion.

    Verantwoordelijkheid:
    - Alleen orkestreren.
    - Geen analyse-logica in deze klasse.
    - Houdt bij hoeveel aandelen per stap overblijven.
    - Meet performance per pipeline-stap.
    - Legt gebruikte market data provider vast.
    """

    def __init__(
        self,
        quote_service: QuoteService | None = None,
        price_filter: PriceFilter | None = None,
        volume_filter: VolumeFilter | None = None,
        liquidity_filter: LiquidityFilter | None = None,
        relative_strength_filter: RelativeStrengthFilter | None = None,
        momentum_filter: MomentumFilter | None = None,
        technical_scanner: TechnicalScanner | None = None,
        ranking_engine: RankingEngine | None = None,
        technical_candidate_limit: int = 100,
    ):
        self.quote_service = quote_service or QuoteService()
        self.price_filter = price_filter or PriceFilter()
        self.volume_filter = volume_filter or VolumeFilter()
        self.liquidity_filter = liquidity_filter or LiquidityFilter()
        self.relative_strength_filter = (
            relative_strength_filter or RelativeStrengthFilter()
        )
        self.momentum_filter = momentum_filter or MomentumFilter()
        self.technical_scanner = technical_scanner or TechnicalScanner()
        self.ranking_engine = ranking_engine or RankingEngine()
        self.technical_candidate_limit = technical_candidate_limit

    def run(self, symbols: list[str]) -> ScanPipelineResult:
        total_start = time.perf_counter()

        status = ScanPipelineStatus(universe_count=len(symbols))

        if not symbols:
            status.messages.append("Geen symbolen ontvangen.")
            status.total_seconds = time.perf_counter() - total_start
            return ScanPipelineResult(opportunities=[], status=status)

        start = time.perf_counter()
        quotes = self.quote_service.get_quotes(symbols)
        status.quote_seconds = time.perf_counter() - start

        status.quotes_count = len(quotes)
        status.quote_cache_hits = self.quote_service.stats.cached_quotes
        status.quote_fresh_downloads = self.quote_service.stats.fresh_quotes
        status.quote_missing = self.quote_service.stats.missing_quotes
        status.quote_negative_cache_hits = self.quote_service.stats.negative_cache_hits

        provider_stats = self.quote_service.provider.stats
        status.market_data_provider = provider_stats.provider_name
        status.provider_requested_symbols = provider_stats.requested_symbols
        status.provider_received_quotes = provider_stats.received_quotes
        status.provider_missing_quotes = provider_stats.missing_quotes
        status.provider_seconds = provider_stats.duration_seconds

        if not quotes:
            status.messages.append("Geen quote-data ontvangen.")
            status.total_seconds = time.perf_counter() - total_start
            return ScanPipelineResult(opportunities=[], status=status)

        start = time.perf_counter()
        quotes = self.price_filter.apply(quotes)
        status.price_filter_seconds = time.perf_counter() - start
        status.after_price_filter = len(quotes)

        start = time.perf_counter()
        quotes = self.volume_filter.apply(quotes)
        status.volume_filter_seconds = time.perf_counter() - start
        status.after_volume_filter = len(quotes)

        start = time.perf_counter()
        quotes = self.liquidity_filter.apply(quotes)
        status.liquidity_filter_seconds = time.perf_counter() - start
        status.after_liquidity_filter = len(quotes)

        start = time.perf_counter()
        quotes = self.relative_strength_filter.apply(
            quotes,
            limit=1000,
        )
        status.relative_strength_seconds = time.perf_counter() - start
        status.after_relative_strength_filter = len(quotes)

        start = time.perf_counter()
        quotes = self.momentum_filter.apply(
            quotes,
            limit=500,
        )
        status.momentum_seconds = time.perf_counter() - start
        status.after_momentum_filter = len(quotes)

        technical_candidates = quotes[: self.technical_candidate_limit]
        status.technical_candidates_count = len(technical_candidates)

        start = time.perf_counter()
        technical_results = self.technical_scanner.scan(technical_candidates)
        status.technical_scanner_seconds = time.perf_counter() - start
        status.technical_results_count = len(technical_results)

        start = time.perf_counter()
        opportunities = self.ranking_engine.rank(
            technical_results,
            limit=3,
        )
        status.ranking_seconds = time.perf_counter() - start
        status.opportunities_count = len(opportunities)

        if not opportunities:
            status.messages.append("Geen hoogwaardige koopkansen gevonden.")

        status.total_seconds = time.perf_counter() - total_start

        return ScanPipelineResult(
            opportunities=opportunities,
            status=status,
        )