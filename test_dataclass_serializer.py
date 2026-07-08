from datetime import datetime

from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from services.serialization.dataclass_serializer import (
    DataclassSerializer,
)


def test_serialize_and_restore_paper_portfolio():
    portfolio = PaperPortfolio(
        cash=250.0,
        positions={
            "AAPL": PaperPosition(
                symbol="AAPL",
                quantity=2,
                entry_price=100.0,
                current_price=110.0,
            )
        },
    )

    serializer = DataclassSerializer()

    data = serializer.to_dict(portfolio)

    restored = serializer.from_dict(
        PaperPortfolio,
        data,
    )

    assert restored.cash == 250.0
    assert "AAPL" in restored.positions
    assert restored.positions["AAPL"].quantity == 2
    assert restored.positions["AAPL"].market_value == 220.0


def test_serialize_datetime():
    serializer = DataclassSerializer()

    value = datetime(2026, 7, 8, 17, 30)

    data = serializer.to_dict(value)

    restored = serializer.from_dict(
        datetime,
        data,
    )

    assert restored == value