from services.portfolio.portfolio_registry import PortfolioRegistry


def test_portfolio_registry_returns_default_analyzers_in_deterministic_order():
    registry = PortfolioRegistry()

    analyzer_names = [definition.name for definition in registry.get_analyzers()]

    assert analyzer_names == [
        "portfolio_summary",
        "cash_validation",
        "position_count",
        "existing_position",
        "exposure",
    ]
