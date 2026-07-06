import json
from pathlib import Path

from models.portfolio import Portfolio


class PortfolioStore:
    def __init__(self, path: str = "data/portfolio.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> Portfolio:
        if not self.path.exists():
            portfolio = Portfolio(
                cash=300.00,
                currency="EUR",
                max_position_percentage=1.0,
            )
            self.save(portfolio)
            return portfolio

        with self.path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        max_position_percentage = float(
            data.get("max_position_percentage", 1.0)
        )

        if max_position_percentage == 0.35:
            max_position_percentage = 1.0

        portfolio = Portfolio(
            cash=float(data.get("cash", 300.00)),
            currency=data.get("currency", "EUR"),
            max_position_percentage=max_position_percentage,
            positions=data.get("positions", {}),
        )

        self.save(portfolio)

        return portfolio

    def save(self, portfolio: Portfolio) -> None:
        data = {
            "cash": getattr(portfolio, "cash", 300.00),
            "currency": getattr(portfolio, "currency", "EUR"),
            "max_position_percentage": getattr(
                portfolio,
                "max_position_percentage",
                1.0,
            ),
            "positions": getattr(portfolio, "positions", {}),
        }

        with self.path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)