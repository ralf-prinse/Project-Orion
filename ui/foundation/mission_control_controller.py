from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from models.portfolio import Portfolio
from services.opportunity_service import Opportunity
from services.orchestration.market_pipeline_scanner_service import (
    MarketPipelineScannerService,
    MarketPipelineScannerSnapshot,
    MarketPipelineScanResult,
)
from services.position_sizing_service import PositionSizingService
from ui.foundation.mission_control_presenter import (
    MissionControlPresenter,
)
from ui.workspace.mission_control_workspace import (
    MissionControlWorkspace,
)


@dataclass(frozen=True)
class MissionPipelineResultAdapter:
    symbol: str
    technical_score: float
    signal: str
    reason: str
    analysis: object | None = None


@dataclass(frozen=True)
class MissionPipelineSnapshotAdapter:
    timestamp: datetime
    symbols: tuple[str, ...]
    technical_results: tuple[MissionPipelineResultAdapter, ...]
    errors: tuple[str, ...]
    duration_seconds: float
    latest_market_data_timestamp: datetime | None = None

    @property
    def total_symbols(self) -> int:
        return len(self.symbols)

    @property
    def total_quotes(self) -> int:
        return len(self.technical_results)

    @property
    def total_results(self) -> int:
        return len(self.technical_results)

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)


class MissionControlController:
    """
    Controller for the Mission Control workspace.

    Responsibilities:
        - coordinate MarketPipelineScannerService
        - obtain deterministic pipeline scanner snapshots
        - transform pipeline BUY/HOLD/SELL results into Mission Control opportunities
        - transform deterministic data into GuiWorkspace models
        - update MissionControlWorkspace

    Does NOT:
        - calculate trading signals
        - calculate indicators
        - execute trades
        - perform AI reasoning

    TradingPipeline is the single source for BUY / HOLD / SELL decisions.
    """

    def __init__(
        self,
        workspace: MissionControlWorkspace,
        scanner_service: MarketPipelineScannerService | None = None,
        presenter: MissionControlPresenter | None = None,
        position_sizing_service: PositionSizingService | None = None,
        available_cash_provider=None,
    ) -> None:
        self._workspace = workspace
        self._scanner_service = scanner_service or MarketPipelineScannerService()
        self._presenter = presenter or MissionControlPresenter()
        self._position_sizing_service = (
            position_sizing_service or PositionSizingService()
        )
        self._available_cash_provider = available_cash_provider
        self._last_snapshot: MarketPipelineScannerSnapshot | None = None

    @property
    def scanner_service(self) -> MarketPipelineScannerService:
        return self._scanner_service

    def initialize(self) -> None:
        workspace = self._presenter.present(
            scanner_snapshot=None,
            opportunities=(),
        )

        self._workspace.set_workspace(workspace)

    def refresh(self) -> None:
        portfolio = self._portfolio_state()

        snapshot = self._scanner_service.scan(
            portfolio_state=portfolio,
        )

        self._last_snapshot = snapshot

        opportunities = self._build_opportunities(snapshot)
        snapshot_view = self._adapt_snapshot(snapshot)

        workspace = self._presenter.present(
            scanner_snapshot=snapshot_view,
            opportunities=opportunities,
        )

        self._workspace.set_workspace(workspace)

    def start(self) -> None:
        self.refresh()

    def stop(self) -> None:
        return None

    def _build_opportunities(
        self,
        snapshot: MarketPipelineScannerSnapshot,
        limit: int = 10,
    ) -> tuple[Opportunity, ...]:
        opportunities: list[Opportunity] = []
        available_cash = self._available_cash()

        for result in snapshot.top_buy_results[:limit]:
            sizing = None

            if available_cash > 0 and result.price > 0:
                sizing = self._position_sizing_service.calculate(
                    symbol=result.symbol,
                    available_cash=available_cash,
                    price=result.price,
                    account_currency="EUR",
                    market_currency=self._market_currency(result.symbol),
                )

            opportunities.append(
                Opportunity(
                    symbol=result.symbol,
                    price=result.price,
                    signal=result.decision,
                    technical_score=round(result.confidence * 100, 2),
                    reason=result.reason,
                    analysis=None,
                    position_sizing=sizing,
                )
            )

        return tuple(opportunities)

    def _adapt_snapshot(
        self,
        snapshot: MarketPipelineScannerSnapshot,
    ) -> MissionPipelineSnapshotAdapter:
        technical_results = tuple(
            self._adapt_result(result)
            for result in snapshot.results
        )

        return MissionPipelineSnapshotAdapter(
            timestamp=snapshot.timestamp,
            symbols=snapshot.symbols,
            technical_results=technical_results,
            errors=snapshot.errors,
            duration_seconds=snapshot.duration_seconds,
            latest_market_data_timestamp=snapshot.timestamp,
        )

    def _adapt_result(
        self,
        result: MarketPipelineScanResult,
    ) -> MissionPipelineResultAdapter:
        return MissionPipelineResultAdapter(
            symbol=result.symbol,
            technical_score=round(result.confidence * 100, 2),
            signal=result.decision,
            reason=result.reason,
            analysis=None,
        )

    def _portfolio_state(self) -> Portfolio:
        return Portfolio(
            cash=self._available_cash(),
            currency="EUR",
            max_position_percentage=1.0,
        )

    def _available_cash(self) -> float:
        if self._available_cash_provider is None:
            return 0.0

        try:
            return float(self._available_cash_provider())
        except Exception:
            return 0.0

    def _market_currency(self, symbol: str) -> str:
        normalized_symbol = str(symbol).strip().upper()

        if normalized_symbol.endswith(".AS"):
            return "EUR"

        return "USD"