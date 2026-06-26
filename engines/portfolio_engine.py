from models.portfolio import Portfolio


class PortfolioEngine:
    """
    Berekent of een trade binnen het beschikbare portfolio past.
    """

    def calculate_buy_quantity(
        self,
        portfolio: Portfolio,
        price: float,
    ) -> int:
        if price <= 0:
            raise ValueError("Prijs moet groter zijn dan 0.")

        max_value = portfolio.max_position_value()
        quantity = int(max_value // price)

        return quantity

    def calculate_position_value(
        self,
        quantity: int,
        price: float,
    ) -> float:
        if quantity < 0:
            raise ValueError("Aantal mag niet negatief zijn.")

        if price <= 0:
            raise ValueError("Prijs moet groter zijn dan 0.")

        return quantity * price