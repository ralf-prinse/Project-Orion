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
                max_position_percentage=0.35,
            )
            self.save(portfolio)
            return portfolio

        with self.path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return Portfolio(
            cash=float(data.get("cash", 300.00)),
            currency=data.get("currency", "EUR"),
            max_position_percentage=float(data.get("max_position_percentage", 0.35)),
            positions=data.get("positions", {}),
        )

    def save(self, portfolio: Portfolio) -> None:
        data = {
            "cash": getattr(portfolio, "cash", 300.00),
            "currency": getattr(portfolio, "currency", "EUR"),
            "max_position_percentage": getattr(portfolio, "max_position_percentage", 0.35),
            "positions": getattr(portfolio, "positions", {}),
        }

        with self.path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)