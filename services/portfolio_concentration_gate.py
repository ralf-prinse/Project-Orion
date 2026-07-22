from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from models.trading_session import TradingSession


@dataclass(frozen=True)
class InstrumentRiskMetadata:
    symbol: str
    sector: str = ""
    correlation_cluster: str = ""


@dataclass(frozen=True)
class ConcentrationDecision:
    allowed: bool
    reason: str


class PortfolioConcentrationGate:
    """Market, sector and manually curated correlation concentration gate."""

    def __init__(self, metadata_path: Path | str) -> None:
        self.metadata_path = Path(metadata_path)

    def evaluate(
        self,
        *,
        session: TradingSession,
        symbol: str,
        proposed_value: float,
        max_positions_per_market: int,
        max_market_exposure_pct: float,
        max_positions_per_sector: int,
        max_sector_exposure_pct: float,
        max_positions_per_correlation_cluster: int,
        pending_positions: list[tuple[str, float]] | None = None,
    ) -> ConcentrationDecision:
        equity = session.equity
        if equity <= 0:
            return ConcentrationDecision(False, "Portfolio equity is invalid.")

        metadata = self._load()
        candidate_symbol = symbol.strip().upper()
        candidate_market = self._market(candidate_symbol)
        candidate_meta = metadata.get(candidate_symbol)

        market_count = 0
        market_value = 0.0
        sector_count = 0
        sector_value = 0.0
        cluster_count = 0

        for position in session.portfolio.positions.values():
            position_symbol = position.symbol.strip().upper()
            value = position.market_value
            if self._market(position_symbol) == candidate_market:
                market_count += 1
                market_value += value

            position_meta = metadata.get(position_symbol)
            if candidate_meta is not None and position_meta is not None:
                if (
                    candidate_meta.sector
                    and position_meta.sector == candidate_meta.sector
                ):
                    sector_count += 1
                    sector_value += value
                if (
                    candidate_meta.correlation_cluster
                    and position_meta.correlation_cluster
                    == candidate_meta.correlation_cluster
                ):
                    cluster_count += 1

        for pending_symbol, pending_value in pending_positions or []:
            normalized_pending = pending_symbol.strip().upper()
            if self._market(normalized_pending) == candidate_market:
                market_count += 1
                market_value += pending_value
            pending_meta = metadata.get(normalized_pending)
            if candidate_meta is not None and pending_meta is not None:
                if (
                    candidate_meta.sector
                    and pending_meta.sector == candidate_meta.sector
                ):
                    sector_count += 1
                    sector_value += pending_value
                if (
                    candidate_meta.correlation_cluster
                    and pending_meta.correlation_cluster
                    == candidate_meta.correlation_cluster
                ):
                    cluster_count += 1

        if market_count + 1 > max_positions_per_market:
            return ConcentrationDecision(
                False,
                f"Maximum {candidate_market} position count reached.",
            )
        if (market_value + proposed_value) / equity > max_market_exposure_pct:
            return ConcentrationDecision(
                False,
                f"Maximum {candidate_market} market exposure exceeded.",
            )

        if candidate_meta is not None and candidate_meta.sector:
            if sector_count + 1 > max_positions_per_sector:
                return ConcentrationDecision(
                    False,
                    f"Maximum sector count reached for {candidate_meta.sector}.",
                )
            if (
                sector_value + proposed_value
            ) / equity > max_sector_exposure_pct:
                return ConcentrationDecision(
                    False,
                    f"Maximum sector exposure exceeded for {candidate_meta.sector}.",
                )
        if (
            candidate_meta is not None
            and candidate_meta.correlation_cluster
            and cluster_count + 1 > max_positions_per_correlation_cluster
        ):
            return ConcentrationDecision(
                False,
                "Maximum correlation-cluster position count reached for "
                f"{candidate_meta.correlation_cluster}.",
            )

        return ConcentrationDecision(
            True,
            "Portfolio concentration controls allow the position.",
        )

    def _load(self) -> dict[str, InstrumentRiskMetadata]:
        if not self.metadata_path.exists():
            return {}
        values: dict[str, InstrumentRiskMetadata] = {}
        with self.metadata_path.open(
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as handle:
            for row in csv.DictReader(handle):
                symbol = str(row.get("symbol", "")).strip().upper()
                if symbol:
                    values[symbol] = InstrumentRiskMetadata(
                        symbol=symbol,
                        sector=str(row.get("sector", "")).strip().upper(),
                        correlation_cluster=str(
                            row.get("correlation_cluster", "")
                        ).strip().upper(),
                    )
        return values

    @staticmethod
    def _market(symbol: str) -> str:
        if symbol.endswith(".AS"):
            return "EURONEXT_AMSTERDAM"
        if symbol.endswith(".DE"):
            return "XETRA"
        return "UNITED_STATES"
