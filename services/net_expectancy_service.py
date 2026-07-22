from __future__ import annotations

from dataclasses import dataclass

from models.completed_trade_record import CompletedTradeRecord


@dataclass(frozen=True)
class NetExpectancyResult:
    sample_size: int
    win_rate: float
    average_net_winner: float
    average_net_loser: float
    net_expectancy_per_trade: float
    total_net_profit_loss: float
    sufficient_sample: bool


class NetExpectancyService:
    """Offline-only analysis of immutable completed-trade records."""

    def analyze(
        self,
        records: list[CompletedTradeRecord],
        *,
        minimum_sample_size: int = 30,
    ) -> NetExpectancyResult:
        values = [record.estimated_net_profit_loss for record in records]
        winners = [value for value in values if value > 0]
        losers = [value for value in values if value < 0]
        sample_size = len(values)
        win_rate = len(winners) / sample_size if sample_size else 0.0
        average_winner = sum(winners) / len(winners) if winners else 0.0
        average_loser = sum(losers) / len(losers) if losers else 0.0
        expectancy = (
            win_rate * average_winner
            + (1.0 - win_rate) * average_loser
        ) if sample_size else 0.0
        return NetExpectancyResult(
            sample_size=sample_size,
            win_rate=round(win_rate, 4),
            average_net_winner=round(average_winner, 2),
            average_net_loser=round(average_loser, 2),
            net_expectancy_per_trade=round(expectancy, 2),
            total_net_profit_loss=round(sum(values), 2),
            sufficient_sample=sample_size >= minimum_sample_size,
        )

    def analyze_grouped(
        self,
        records: list[CompletedTradeRecord],
        *,
        field_name: str,
        minimum_sample_size: int = 30,
    ) -> dict[str, NetExpectancyResult]:
        allowed_fields = {
            "symbol",
            "strategy_name",
            "entry_regime",
            "entry_volatility",
        }
        if field_name not in allowed_fields:
            raise ValueError(
                "field_name must be symbol, strategy_name, entry_regime "
                "or entry_volatility."
            )
        groups: dict[str, list[CompletedTradeRecord]] = {}
        for record in records:
            key = str(getattr(record, field_name) or "UNKNOWN").upper()
            groups.setdefault(key, []).append(record)
        return {
            key: self.analyze(
                values,
                minimum_sample_size=minimum_sample_size,
            )
            for key, values in sorted(groups.items())
        }
