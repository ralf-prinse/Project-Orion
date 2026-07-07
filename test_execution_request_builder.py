from services.execution_request_builder import ExecutionRequestBuilder


def run():
    builder = ExecutionRequestBuilder()

    pipeline_output = {
        "symbol": "AAPL",
        "confidence": 0.91,
        "risk_plan": {
            "symbol": "AAPL",
            "entry_price": 100.0,
            "stop_loss": 95.0,
            "target_1": 110.0,
            "target_2": 120.0,
            "target_3": 130.0,
            "risk_percent": 5.0,
            "reward_percent": 10.0,
            "risk_reward_ratio": 2.0,
            "confidence": 0.91,
            "notes": "test",
        },
    }

    request = builder.build(
        pipeline_output=pipeline_output,
        quantity=2,
    )

    print(request)

    assert request.symbol == "AAPL"
    assert request.action == "OPEN_POSITION"
    assert request.entry_price == 100.0
    assert request.quantity == 2
    assert request.risk_plan.stop_loss == 95.0
    assert request.confidence == 0.91

    print("PASS")


if __name__ == "__main__":
    run()