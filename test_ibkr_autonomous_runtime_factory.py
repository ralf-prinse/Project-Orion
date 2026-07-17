from __future__ import annotations

from models.autonomous_paper_trading_config import (
    AutonomousPaperTradingConfig,
)
from services.ibkr.ibkr_autonomous_runtime_factory import (
    IbkrAutonomousRuntimeFactory,
)
from services.ibkr.ibkr_broker import IbkrBroker


PAPER_ACCOUNT_ID = "DU1234567"


def create_runtime(
    *,
    allow_order_submission: bool = False,
):
    factory = IbkrAutonomousRuntimeFactory()

    return factory.build(
        paper_account_id=PAPER_ACCOUNT_ID,
        config=AutonomousPaperTradingConfig(
            cycles=1,
            sleep_seconds=0,
        ),
        allow_order_submission=allow_order_submission,
    )


def test_builds_ibkr_autonomous_runtime() -> None:
    runtime = create_runtime()

    assert runtime.runner is not None
    assert runtime.transport is not None
    assert runtime.broker is not None
    assert runtime.execution_engine is not None
    assert runtime.paper_trading_service is not None
    assert runtime.trading_cycle is not None
    assert runtime.position_exit_execution_service is not None
    assert runtime.account_service is not None
    assert runtime.trading_session_sync_service is not None
    assert runtime.price_provider is not None


def test_execution_engine_uses_ibkr_broker() -> None:
    runtime = create_runtime()

    assert isinstance(
        runtime.execution_engine.broker,
        IbkrBroker,
    )
    assert runtime.execution_engine.broker is runtime.broker


def test_buy_and_sell_share_execution_engine() -> None:
    runtime = create_runtime()

    buy_execution_engine = (
        runtime
        .trading_cycle
        .paper_trading_service
        .execution_engine
    )

    sell_execution_engine = (
        runtime
        .position_exit_execution_service
        .execution_engine
    )

    assert buy_execution_engine is runtime.execution_engine
    assert sell_execution_engine is runtime.execution_engine
    assert buy_execution_engine is sell_execution_engine


def test_runner_uses_composed_ibkr_services() -> None:
    runtime = create_runtime()

    assert (
        runtime.runner.trading_cycle
        is runtime.trading_cycle
    )

    assert (
        runtime.runner.position_exit_execution_service
        is runtime.position_exit_execution_service
    )

    assert (
        runtime.runner.trading_session_sync_service
        is runtime.trading_session_sync_service
    )

    assert (
        runtime.runner.price_provider
        is runtime.price_provider
    )


def test_wires_separate_decision_journal_repository() -> None:
    repository = object()

    runtime = IbkrAutonomousRuntimeFactory().build(
        paper_account_id=PAPER_ACCOUNT_ID,
        decision_journal_repository=repository,
    )

    assert runtime.runner.decision_journal_repository is repository


def test_wires_persistent_session_repositories() -> None:
    session_repository = object()
    portfolio_repository = object()

    runtime = IbkrAutonomousRuntimeFactory().build(
        paper_account_id=PAPER_ACCOUNT_ID,
        trading_session_repository=session_repository,
        portfolio_repository=portfolio_repository,
    )

    assert (
        runtime.runner.trading_session_repository
        is session_repository
    )
    assert runtime.runner.portfolio_repository is portfolio_repository


def test_wires_market_hours_to_buy_and_sell_paths() -> None:
    runtime = create_runtime()

    assert runtime.runner.market_session_service is not None
    assert (
        runtime.runner.scanner.market_session_service
        is runtime.runner.market_session_service
    )


def test_order_submission_is_disabled_by_default() -> None:
    runtime = create_runtime()

    assert runtime.transport.allow_order_submission is False


def test_order_submission_can_be_enabled_explicitly() -> None:
    runtime = create_runtime(
        allow_order_submission=True,
    )

    assert runtime.transport.allow_order_submission is True


def test_uses_separate_ibkr_client_ids() -> None:
    runtime = create_runtime()

    assert runtime.account_service.client_id == 110
    assert runtime.transport.client_id == 120
    assert (
        runtime.account_service.client_id
        != runtime.transport.client_id
    )


def test_uses_ibkr_paper_port() -> None:
    runtime = create_runtime()

    assert runtime.account_service.port == 7497
    assert runtime.transport.port == 7497


def test_rejects_empty_account_id() -> None:
    factory = IbkrAutonomousRuntimeFactory()

    try:
        factory.build(
            paper_account_id="",
        )
    except ValueError as exc:
        assert "must not be empty" in str(exc)
    else:
        raise AssertionError(
            "Expected empty IBKR account ID to fail."
        )


def test_rejects_non_paper_account_id() -> None:
    factory = IbkrAutonomousRuntimeFactory()

    try:
        factory.build(
            paper_account_id="U1234567",
        )
    except ValueError as exc:
        assert "starting with 'DU'" in str(exc)
    else:
        raise AssertionError(
            "Expected non-paper IBKR account ID to fail."
        )


def run() -> None:
    tests = [
        test_builds_ibkr_autonomous_runtime,
        test_execution_engine_uses_ibkr_broker,
        test_buy_and_sell_share_execution_engine,
        test_runner_uses_composed_ibkr_services,
        test_wires_separate_decision_journal_repository,
        test_wires_persistent_session_repositories,
        test_wires_market_hours_to_buy_and_sell_paths,
        test_order_submission_is_disabled_by_default,
        test_order_submission_can_be_enabled_explicitly,
        test_uses_separate_ibkr_client_ids,
        test_uses_ibkr_paper_port,
        test_rejects_empty_account_id,
        test_rejects_non_paper_account_id,
    ]

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print()
    print(
        "IBKR AUTONOMOUS RUNTIME FACTORY TESTS: "
        f"{len(tests)} passed"
    )


if __name__ == "__main__":
    run()
