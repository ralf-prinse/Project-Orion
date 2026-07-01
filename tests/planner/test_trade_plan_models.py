from services.planner.models import TradePlanContext, TradePlanResult


def test_trade_plan_context_normalizes_action():
    context = TradePlanContext(
        symbol="aapl",
        action=" buy ",
        entry_price=100.0,
        stop_loss=95.0,
        recommended_shares=10,
    )

    assert context.normalized_action() == "BUY"


def test_trade_plan_result_collects_reasons_and_warnings():
    result = TradePlanResult(symbol="AAPL")

    result.add_reason("reason")
    result.add_warning("warning")

    assert result.reasons == ["reason"]
    assert result.warnings == ["warning"]
