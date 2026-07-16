from __future__ import annotations

from dataclasses import dataclass

from models.autonomous_paper_trading_config import (
    AutonomousPaperTradingConfig,
)
from models.live_paper_trading_config import (
    LivePaperTradingConfig,
)
from models.live_paper_trading_result import (
    LivePaperTradingResult,
)
from models.paper_portfolio import PaperPortfolio
from models.trading_session import TradingSession
from services.autonomous_paper_trading_runner import (
    AutonomousPaperTradingRunner,
)


class FakeSyncService:
    def __init__(self) -> None:
        self.call_count = 0

    def synchronize(
        self,
        session: TradingSession,
    ) -> TradingSession:
        self.call_count += 1
        session.portfolio = PaperPortfolio(
            cash=9999.0,
            positions={},
        )
        return session


class FakeScanner:
    def __init__(
        self,
        sync_service: FakeSyncService,
    ) -> None:
        self.sync_service = sync_service
        self.called = False

    def run(
        self,
        session: TradingSession,
    ) -> LivePaperTradingResult:
        self.called = True

        assert self.sync_service.call_count == 1
        assert session.cash == 9999.0

        return LivePaperTradingResult(
            session=session,
            scanned_symbols=0,
            succeeded_symbols=0,
            failed_symbols=0,
            failed_symbol_errors={},
            scan_duration_seconds=0.0,
            candidates=[],
            executed_trades=0,
            rejected_trades=0,
        )


class FakeAllocator:
    @dataclass(frozen=True)
    class Result:
        decisions: list

        @property
        def approved_count(self) -> int:
            return 0

        @property
        def rejected_count(self) -> int:
            return 0

    def allocate(
        self,
        session,
        candidates,
        config,
    ) -> Result:
        return self.Result(decisions=[])


def test_runner_syncs_before_scan() -> None:
    sync_service = FakeSyncService()
    scanner = FakeScanner(sync_service)

    runner = AutonomousPaperTradingRunner(
        config=AutonomousPaperTradingConfig(
            cycles=1,
            sleep_seconds=0,
            live_config=LivePaperTradingConfig(),
        ),
        scanner=scanner,
        allocator=FakeAllocator(),
        trading_session_sync_service=sync_service,
    )

    result = runner.run()

    assert result.completed_cycles == 1
    assert result.failed_cycles == 0
    assert result.session.cash == 9999.0
    assert sync_service.call_count == 1
    assert scanner.called is True


def run() -> None:
    test_runner_syncs_before_scan()

    print(
        "PASS: test_runner_syncs_before_scan"
    )
    print()
    print(
        "AUTONOMOUS RUNNER IBKR SYNC TESTS: 1 passed"
    )


if __name__ == "__main__":
    run()