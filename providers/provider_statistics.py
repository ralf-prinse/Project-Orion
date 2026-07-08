from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ProviderStatistics:
    """
    Runtime statistics for market data provider calls.

    Informational only.
    Does not influence trading decisions.
    """

    requests: int = 0
    successes: int = 0
    failures: int = 0
    retries: int = 0
    total_latency_seconds: float = 0.0

    def record_success(
        self,
        latency_seconds: float,
    ) -> None:
        self.requests += 1
        self.successes += 1
        self.total_latency_seconds = round(
            self.total_latency_seconds + latency_seconds,
            6,
        )

    def record_failure(
        self,
        latency_seconds: float,
    ) -> None:
        self.requests += 1
        self.failures += 1
        self.total_latency_seconds = round(
            self.total_latency_seconds + latency_seconds,
            6,
        )

    def record_retry(self) -> None:
        self.retries += 1

    @property
    def success_rate(self) -> float:
        if self.requests == 0:
            return 0.0

        return round(
            self.successes / self.requests,
            6,
        )

    @property
    def failure_rate(self) -> float:
        if self.requests == 0:
            return 0.0

        return round(
            self.failures / self.requests,
            6,
        )

    @property
    def average_latency_seconds(self) -> float:
        if self.requests == 0:
            return 0.0

        return round(
            self.total_latency_seconds / self.requests,
            6,
        )