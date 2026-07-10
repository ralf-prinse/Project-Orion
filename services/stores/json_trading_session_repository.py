from __future__ import annotations

import json
from pathlib import Path

from models.trading_session import TradingSession
from services.serialization.dataclass_serializer import (
    DataclassSerializer,
)
from services.stores.repositories.trading_session_repository import (
    TradingSessionRepository,
)


class JsonTradingSessionRepository(TradingSessionRepository):
    """
    JSON persistence for a complete TradingSession.

    Persists:
    - paper portfolio
    - position states
    - risk plans
    - session metadata

    Contains no trading decisions or position-management logic.
    """

    def __init__(
        self,
        path: Path | str = "data/trading_session.json",
        serializer: DataclassSerializer | None = None,
    ):
        self.path = Path(path)
        self.serializer = serializer or DataclassSerializer()

    def exists(self) -> bool:
        return self.path.exists()

    def load(self) -> TradingSession:
        if not self.exists():
            raise FileNotFoundError(
                f"Trading session not found: {self.path}"
            )

        data = json.loads(
            self.path.read_text(
                encoding="utf-8",
            )
        )

        return self.serializer.from_dict(
            TradingSession,
            data,
        )

    def save(
        self,
        session: TradingSession,
    ) -> None:
        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = self.serializer.to_dict(session)

        self.path.write_text(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def delete(self) -> None:
        if self.exists():
            self.path.unlink()