from services.position_management_summary_builder import (
    PositionManagementSummaryBuilder,
)
from services.risk.break_even_service import BreakEvenResult
from services.risk.position_health_service import PositionHealthResult
from services.risk.time_stop_service import TimeStopResult
from services.risk.trailing_stop_service import TrailingStopResult


def run():

    builder = PositionManagementSummaryBuilder()

    summary = builder.build(
        symbol="aapl",
        current_price=112.0,
        stop_loss=106.4,
        break_even=BreakEvenResult(
            activated=True,
            new_stop_loss=100.0,
            reason="Target 1 reached.",
        ),
        trailing_stop=TrailingStopResult(
            activated=True,
            new_stop_loss=106.4,
            highest_price=112.0,
            reason="Trailing stop updated.",
        ),
        time_stop=TimeStopResult(
            activated=False,
            days_open=4,
            maximum_days=10,
            reason="Holding period still valid.",
        ),
        position_health=PositionHealthResult(
            status="GOOD",
            score=85,
            warnings=[],
            summary="GOOD position health with score 85.",
        ),
    )

    print(summary)

    assert summary.symbol == "AAPL"
    assert summary.current_price == 112.0
    assert summary.stop_loss == 106.4
    assert summary.status == "GOOD"
    assert summary.score == 85

    assert "MOVE_STOP_TO_BREAK_EVEN" in summary.actions
    assert "UPDATE_TRAILING_STOP" in summary.actions
    assert "TIME_STOP_ACTIVE" not in summary.actions

    assert summary.has_actions is True
    assert summary.has_warnings is False

    print("PASS")


if __name__ == "__main__":
    run()