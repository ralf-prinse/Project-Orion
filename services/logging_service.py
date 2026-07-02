from __future__ import annotations

import logging
from pathlib import Path


class LoggingService:
    """
    Central logging service for Project Orion.

    Responsibilities
    ----------------
    - Configure application logging
    - Provide named loggers
    - Write to both console and file
    """

    _configured = False

    @classmethod
    def configure(cls) -> None:
        if cls._configured:
            return

        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "orion.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )

        cls._configured = True

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        cls.configure()
        return logging.getLogger(name)