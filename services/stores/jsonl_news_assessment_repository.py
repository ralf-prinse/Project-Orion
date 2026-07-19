from __future__ import annotations

import json
from pathlib import Path

from models.news_assessment import NewsAssessment
from services.serialization.dataclass_serializer import DataclassSerializer


class JsonlNewsAssessmentRepository:
    def __init__(
        self,
        path: Path | str = "data/ibkr_news_assessments.jsonl",
        serializer: DataclassSerializer | None = None,
    ) -> None:
        self.path = Path(path)
        self.serializer = serializer or DataclassSerializer()

    def append(self, assessment: NewsAssessment) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as file:
            file.write(
                json.dumps(
                    self.serializer.to_dict(assessment),
                    ensure_ascii=False,
                )
                + "\n"
            )

    def load_all(self) -> list[NewsAssessment]:
        if not self.path.exists():
            return []
        return [
            self.serializer.from_dict(NewsAssessment, json.loads(line))
            for line in self.path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
