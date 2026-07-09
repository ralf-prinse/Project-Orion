from __future__ import annotations

from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from services.portfolio_revaluation_service import (
    PortfolioRevaluationService,
)


def test_portfolio_revaluation_updates_current_prices():
    service = PortfolioRevaluationService()

    portfolio = PaperPortfolio(
        cash=100.0,
        positions={
            "TEST": PaperPosition(
                symbol="TEST",
                quantity=2,
                entry_price=100.0,
                current_price=100.0,
            )
        },
    )

    result = service.revalue(
        portfolio=portfolio,
        prices={
            "TEST": 108.0,
        },
    )

    assert result.cash == 100.0
    assert result.positions["TEST"].current_price == 108.0
    assert result.positions["TEST"].market_value == 216.0
    assert result.positions["TEST"].unrealized_profit_loss == 16.0


def test_portfolio_revaluation_keeps_position_when_price_is_missing():
    service = PortfolioRevaluationService()

    portfolio = PaperPortfolio(
        cash=100.0,
        positions={
            "TEST": PaperPosition(
                symbol="TEST",
                quantity=1,
                entry_price=100.0,
                current_price=101.0,
            )
        },
    )

    result = service.revalue(
        portfolio=portfolio,
        prices={},
    )

    assert result.positions["TEST"].current_price == 101.0


def main():
    print("\n=========================================")
    print("ORION PORTFOLIO REVALUATION TEST")
    print("=========================================\n")

    test_portfolio_revaluation_updates_current_prices()
    test_portfolio_revaluation_keeps_position_when_price_is_missing()

    print("PORTFOLIO REVALUATION: PASS ✅")


if __name__ == "__main__":
    main()