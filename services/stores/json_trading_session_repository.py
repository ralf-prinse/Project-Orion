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
from services.trading_session_integrity_service import (
    TradingSessionIntegrityService,
)


class JsonTradingSessionRepository(TradingSessionRepository):
    """
    JSON persistence for a complete TradingSession.

    Persists:
    - paper portfolio
    - position states
    - risk plans
    - session metadata

    Integrity is validated before save and after load.
    The repository contains no trading decisions.
    """

    def __init__(
        self,
        path: Path | str = "data/trading_session.json",
        serializer: DataclassSerializer | None = None,
        integrity_service: TradingSessionIntegrityService | None = None,
    ):
        self.path = Path(path)
        self.serializer = serializer or DataclassSerializer()
        self.integrity_service = (
            integrity_service
            or TradingSessionIntegrityService()
        )

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

        session = self.serializer.from_dict(
            TradingSession,
            data,
        )

        self.integrity_service.validate(session)

        return session

    def save(
        self,
        session: TradingSession,
    ) -> None:
        self.integrity_service.validate(session)

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
