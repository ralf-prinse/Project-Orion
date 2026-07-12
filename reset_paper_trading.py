from __future__ import annotations

import argparse
import shutil
from datetime import UTC, datetime
from pathlib import Path

from models.paper_portfolio import PaperPortfolio
from models.trading_session import TradingSession
from services.stores.json_paper_portfolio_repository import (
    JsonPaperPortfolioRepository,
)
from services.stores.json_trading_session_repository import (
    JsonTradingSessionRepository,
)


DEFAULT_SESSION_PATH = Path("data/trading_session.json")
DEFAULT_PORTFOLIO_PATH = Path("data/paper_portfolio.json")
DEFAULT_BACKUP_DIRECTORY = Path("data/backups")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Reset Orion paper trading to a clean TradingSession "
            "while preserving journals."
        ),
    )

    parser.add_argument(
        "--capital",
        type=float,
        default=10_000.0,
        help="Starting paper cash. Default: 10000.",
    )

    parser.add_argument(
        "--session-path",
        type=Path,
        default=DEFAULT_SESSION_PATH,
    )

    parser.add_argument(
        "--portfolio-path",
        type=Path,
        default=DEFAULT_PORTFOLIO_PATH,
    )

    parser.add_argument(
        "--backup-directory",
        type=Path,
        default=DEFAULT_BACKUP_DIRECTORY,
    )

    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Reset without backing up the existing session files.",
    )

    return parser


def validate_capital(capital: float) -> float:
    value = round(float(capital), 2)

    if value <= 0:
        raise ValueError(
            "Capital must be greater than zero."
        )

    return value


def create_backup(
    *,
    source: Path,
    backup_directory: Path,
    timestamp: str,
) -> Path | None:
    if not source.exists():
        return None

    backup_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    backup_path = backup_directory / (
        f"{source.stem}_{timestamp}{source.suffix}"
    )

    shutil.copy2(
        source,
        backup_path,
    )

    return backup_path


def build_clean_session(
    capital: float,
) -> TradingSession:
    return TradingSession(
        name="Orion Autonomous Paper Trading",
        portfolio=PaperPortfolio(
            cash=capital,
            positions={},
        ),
        position_states={},
        risk_plans={},
        status="ACTIVE",
    )


def reset_paper_trading(
    *,
    capital: float,
    session_path: Path,
    portfolio_path: Path,
    backup_directory: Path,
    create_backups: bool,
) -> TradingSession:
    validated_capital = validate_capital(capital)

    timestamp = datetime.now(UTC).strftime(
        "%Y%m%dT%H%M%SZ"
    )

    session_backup = None
    portfolio_backup = None

    if create_backups:
        session_backup = create_backup(
            source=session_path,
            backup_directory=backup_directory,
            timestamp=timestamp,
        )

        portfolio_backup = create_backup(
            source=portfolio_path,
            backup_directory=backup_directory,
            timestamp=timestamp,
        )

    session = build_clean_session(
        validated_capital
    )

    session_repository = (
        JsonTradingSessionRepository(
            path=session_path,
        )
    )

    portfolio_repository = (
        JsonPaperPortfolioRepository(
            path=portfolio_path,
        )
    )

    session_repository.save(session)
    portfolio_repository.save(session.portfolio)

    loaded_session = session_repository.load()
    loaded_portfolio = portfolio_repository.load()

    if loaded_session.cash != validated_capital:
        raise RuntimeError(
            "TradingSession cash verification failed."
        )

    if loaded_portfolio.cash != validated_capital:
        raise RuntimeError(
            "Portfolio mirror cash verification failed."
        )

    if loaded_session.open_positions != 0:
        raise RuntimeError(
            "Open-position reset verification failed."
        )

    if loaded_session.position_states:
        raise RuntimeError(
            "Position-state reset verification failed."
        )

    if loaded_session.risk_plans:
        raise RuntimeError(
            "Risk-plan reset verification failed."
        )

    print()
    print("=========================================")
    print("ORION PAPER TRADING RESET")
    print("=========================================")
    print(f"Cash:             EUR {loaded_session.cash:.2f}")
    print(f"Equity:           EUR {loaded_session.equity:.2f}")
    print(f"Open positions:   {loaded_session.open_positions}")
    print(
        "Position states:  "
        f"{len(loaded_session.position_states)}"
    )
    print(
        "Risk plans:       "
        f"{len(loaded_session.risk_plans)}"
    )
    print(f"Status:           {loaded_session.status}")
    print(f"Session file:     {session_path}")
    print(f"Portfolio mirror: {portfolio_path}")

    if session_backup is not None:
        print(f"Session backup:   {session_backup}")

    if portfolio_backup is not None:
        print(f"Portfolio backup: {portfolio_backup}")

    print("Journals:         preserved")
    print("=========================================")
    print()

    return loaded_session


def main() -> None:
    args = build_parser().parse_args()

    reset_paper_trading(
        capital=args.capital,
        session_path=args.session_path,
        portfolio_path=args.portfolio_path,
        backup_directory=args.backup_directory,
        create_backups=not args.no_backup,
    )


if __name__ == "__main__":
    main()