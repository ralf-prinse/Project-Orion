from dataclasses import dataclass, field


@dataclass
class Position:
    symbol: str
    quantity: int
    average_price: float
    currency: str = "EUR"

    def market_value(self, current_price: float) -> float:
        return self.quantity * current_price


@dataclass
class Portfolio:
    cash: float
    currency: str = "EUR"
    max_position_percentage: float = 0.35
    positions: dict[str, Position] = field(default_factory=dict)

    def max_position_value(self) -> float:
        return self.cash * self.max_position_percentage

    def has_position(self, symbol: str) -> bool:
        symbol = symbol.upper()
        position = self.positions.get(symbol)
        return position is not None and position.quantity > 0

    def get_position_quantity(self, symbol: str) -> int:
        symbol = symbol.upper()
        position = self.positions.get(symbol)

        if position is None:
            return 0

        if isinstance(position, dict):
            return int(position.get("quantity", 0))

        return int(position.quantity)

    def buy(self, symbol: str, quantity: int, price: float) -> None:
        symbol = symbol.upper()

        if quantity <= 0:
            return

        total_cost = quantity * price

        if total_cost > self.cash:
            return

        existing_position = self.positions.get(symbol)

        if existing_position is None:
            self.positions[symbol] = Position(
                symbol=symbol,
                quantity=quantity,
                average_price=price,
                currency=self.currency,
            )
        else:
            if isinstance(existing_position, dict):
                old_quantity = int(existing_position.get("quantity", 0))
                old_average_price = float(existing_position.get("average_price", price))
            else:
                old_quantity = existing_position.quantity
                old_average_price = existing_position.average_price

            new_quantity = old_quantity + quantity
            new_average_price = (
                (old_quantity * old_average_price) + (quantity * price)
            ) / new_quantity

            self.positions[symbol] = Position(
                symbol=symbol,
                quantity=new_quantity,
                average_price=new_average_price,
                currency=self.currency,
            )

        self.cash -= total_cost

    def sell(self, symbol: str, quantity: int, price: float) -> None:
        symbol = symbol.upper()

        if quantity <= 0:
            return

        existing_position = self.positions.get(symbol)

        if existing_position is None:
            return

        if isinstance(existing_position, dict):
            current_quantity = int(existing_position.get("quantity", 0))
            average_price = float(existing_position.get("average_price", price))
        else:
            current_quantity = existing_position.quantity
            average_price = existing_position.average_price

        sell_quantity = min(quantity, current_quantity)
        self.cash += sell_quantity * price

        remaining_quantity = current_quantity - sell_quantity

        if remaining_quantity <= 0:
            self.positions.pop(symbol, None)
            return

        self.positions[symbol] = Position(
            symbol=symbol,
            quantity=remaining_quantity,
            average_price=average_price,
            currency=self.currency,
        )

    def to_dict(self) -> dict:
        positions = {}

        for symbol, position in self.positions.items():
            if isinstance(position, dict):
                positions[symbol] = position
            else:
                positions[symbol] = {
                    "symbol": position.symbol,
                    "quantity": position.quantity,
                    "average_price": position.average_price,
                    "currency": position.currency,
                }

        return {
            "cash": self.cash,
            "currency": self.currency,
            "max_position_percentage": self.max_position_percentage,
            "positions": positions,
        }