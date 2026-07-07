from datetime import datetime

from models.order import Order
from services.paper_broker import PaperBroker


def run():
    broker = PaperBroker()

    order = Order(
        symbol="AAPL",
        side="BUY",
        quantity=2,
        order_type="MARKET",
        price=100.0,
        created_at=datetime.now(),
    )

    result = broker.execute(order)

    print(result)

    assert result.accepted is True
    assert result.status == "FILLED"
    assert result.executed_price == 100.0
    assert result.executed_quantity == 2

    print("PASS")


if __name__ == "__main__":
    run()