from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

from providers.provider_statistics import ProviderStatistics


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
        statistics: ProviderStatistics | None = None,
    ) -> T:
        attempts = 0
        started_at = time.perf_counter()

        while True:
            try:
                result = operation()

                if statistics is not None:
                    statistics.record_success(
                        latency_seconds=round(
                            time.perf_counter() - started_at,
                            6,
                        )
                    )

                return result

            except self.retry_exceptions:
                attempts += 1

                if attempts >= self.max_attempts:
                    if statistics is not None:
                        statistics.record_failure(
                            latency_seconds=round(
                                time.perf_counter() - started_at,
                                6,
                            )
                        )

                    raise

                if statistics is not None:
                    statistics.record_retry()

                if self.retry_delay_seconds > 0:
                    time.sleep(self.retry_delay_seconds)