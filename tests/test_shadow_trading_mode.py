from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from models.autonomous_paper_trading_config import AutonomousPaperTradingConfig
from models.live_paper_trading_config import LivePaperTradingConfig
from models.order import Order
from models.paper_position import PaperPosition
from run_autonomous_ibkr_paper import build_config
from services.autonomous_paper_trading_runner import (
    AutonomousPaperTradingRunner,
)
from services.ibkr.ibkr_autonomous_runtime_factory import (
    IbkrAutonomousRuntimeFactory,
)
from services.shadow_broker import ShadowBroker


PAPER_ACCOUNT_ID = "DU1234567"


def shadow_config() -> AutonomousPaperTradingConfig:
    return AutonomousPaperTradingConfig(
        execution_mode=AutonomousPaperTradingConfig.SHADOW,
        live_config=LivePaperTradingConfig(
            news_mode=LivePaperTradingConfig.NEWS_DISABLED,
        ),
        cycles=1,
        sleep_seconds=0.0,
    )


def test_shadow_runtime_has_no_ibkr_execution_or_sync_path() -> None:
    runtime = IbkrAutonomousRuntimeFactory().build(
        paper_account_id=PAPER_ACCOUNT_ID,
        config=shadow_config(),
        position_adoption_service=object(),
        allow_order_submission=False,
    )

    assert isinstance(runtime.broker, ShadowBroker)
    assert runtime.execution_engine.broker is runtime.broker
    assert runtime.runner.trading_session_sync_service is None
    assert runtime.trading_session_sync_service is None
    assert runtime.runner.position_adoption_service is None
    assert runtime.runner.protective_execution_reconciler is None
    assert runtime.transport.allow_order_submission is False


def test_shadow_runtime_rejects_order_permission_fail_closed() -> None:
    with pytest.raises(ValueError, match="cannot be combined"):
        IbkrAutonomousRuntimeFactory().build(
            paper_account_id=PAPER_ACCOUNT_ID,
            config=shadow_config(),
            allow_order_submission=True,
        )


def test_shadow_broker_preserves_reference_price_without_external_order() -> None:
    broker = ShadowBroker(slippage_pct_per_side=0.001)
    buy = broker.execute(_order(side="BUY"))
    sell = broker.execute(_order(side="SELL"))

    assert buy.accepted is True
    assert buy.status == "SHADOW_FILLED"
    assert buy.executed_price == 100.0
    assert sell.executed_price == 100.0
    assert "slippage is reserved by the cost model" in buy.message
    assert "no external order submitted" in buy.message


def test_entrypoint_shadow_config_disables_live_execution_controls() -> None:
    config = build_config(
        execution_mode=AutonomousPaperTradingConfig.SHADOW,
    )

    assert config.execution_mode == AutonomousPaperTradingConfig.SHADOW
    assert config.live_config.enable_execution_quality_gate is False
    assert config.live_config.enable_native_protective_orders is False


def test_shadow_exit_journal_records_strategy_costs_and_net_result() -> None:
    journal = MemoryJournal()
    runner = AutonomousPaperTradingRunner(
        config=shadow_config(),
        trade_journal_repository=journal,
    )
    position = PaperPosition(
        symbol="ASML.AS",
        quantity=2,
        entry_price=100.0,
        current_price=110.0,
        currency="EUR",
    )

    runner._append_broker_exit_journal_entry(
        position=position,
        decision=SimpleNamespace(
            action="TAKE_PROFIT",
            reason="Shadow target reached.",
            estimated_round_trip_costs=0.0,
            estimated_net_profit_loss=0.0,
        ),
        execution=SimpleNamespace(
            executed_quantity=2,
            executed_price=110.0,
            executed_at=datetime.now(UTC),
        ),
        cycle_number=1,
        session_id="shadow-test",
        trade_id="trade-1",
        fully_closed=False,
    )

    entry = journal.entries[0]
    assert entry.strategy_name == "ORION_SHADOW"
    assert entry.realized_profit_loss == 20.0
    assert entry.estimated_trading_costs > 0
    assert entry.estimated_net_profit_loss < entry.realized_profit_loss


class MemoryJournal:
    def __init__(self) -> None:
        self.entries = []

    def append(self, entry) -> None:
        self.entries.append(entry)

    def load_all(self):
        return list(self.entries)


def _order(*, side: str) -> Order:
    return Order(
        symbol="ASML.AS",
        side=side,
        quantity=2,
        order_type="MARKET",
        price=100.0,
        created_at=datetime.now(UTC),
    )
