from models.position_management_summary import PositionManagementSummary


def run():

    summary = PositionManagementSummary(
        symbol="AAPL",
        current_price=112.0,
        stop_loss=106.4,
        status="GOOD",
        score=85,
        actions=[
            "MOVE_STOP_TO_BREAK_EVEN",
            "UPDATE_TRAILING_STOP",
        ],
        warnings=[],
    )

    print(summary)

    assert summary.symbol == "AAPL"
    assert summary.current_price == 112.0
    assert summary.stop_loss == 106.4
    assert summary.status == "GOOD"
    assert summary.score == 85

    assert summary.has_actions is True
    assert summary.has_warnings is False

    print("PASS")


if __name__ == "__main__":
    run()