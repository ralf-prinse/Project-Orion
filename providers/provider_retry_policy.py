from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar


T = TypeVar("T")


@dataclass(frozen=True)
class ProviderRetryPolicy:
    """
    Deterministic retry policy for market data providers.

    This class contains no provider-specific logic.
    It only decides how many times an operation may be retried.
    """

    max_attempts: int = 3
    retry_delay_seconds: float = 0.0
    retry_exceptions: tuple[type[BaseException], ...] = (Exception,)

    def __post_init__(self) -> None:
        if self.max_attempts <= 0:
            raise ValueError("max_attempts must be greater than zero.")

        if self.retry_delay_seconds < 0:
            raise ValueError(
                "retry_delay_seconds must not be negative."
            )

    def run(
        self,
        operation: Callable[[], T],
    ) -> T:
        attempts = 0

        while True:
            try:
                return operation()

            except self.retry_exceptions:
                attempts += 1

                if attempts >= self.max_attempts:
                    raise

                if self.retry_delay_seconds > 0:
                    time.sleep(self.retry_delay_seconds)