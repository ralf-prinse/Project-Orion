from __future__ import annotations

import json
from pathlib import Path

from models.paper_portfolio import PaperPortfolio
from services.serialization.dataclass_serializer import (
    DataclassSerializer,
)
from services.stores.repositories.paper_portfolio_repository import (
    PaperPortfolioRepository,
)


class JsonPaperPortfolioRepository(PaperPortfolioRepository):
    """
    JSON implementation of PaperPortfolioRepository.

    Uses DataclassSerializer so JSON persistence does not need to know
    the internal structure of PaperPortfolio.
    """

    def __init__(
        self,
        path: Path | str = "data/paper_portfolio.json",
        serializer: DataclassSerializer | None = None,
    ):
        self.path = Path(path)
        self.serializer = serializer or DataclassSerializer()

    def exists(self) -> bool:
        return self.path.exists()

    def load(self) -> PaperPortfolio:
        if not self.exists():
            raise FileNotFoundError(
                f"Paper portfolio not found: {self.path}"
            )

        data = json.loads(
            self.path.read_text(
                encoding="utf-8",
            )
        )

        return self.serializer.from_dict(
            PaperPortfolio,
            data,
        )

    def save(
        self,
        portfolio: PaperPortfolio,
    ) -> None:
        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = self.serializer.to_dict(portfolio)

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