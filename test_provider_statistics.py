from __future__ import annotations

from providers.provider_retry_policy import ProviderRetryPolicy
from providers.provider_statistics import ProviderStatistics


class TemporaryProviderError(Exception):
    pass


def test_provider_statistics_records_success():
    statistics = ProviderStatistics()

    statistics.record_success(
        latency_seconds=0.25,
    )

    assert statistics.requests == 1
    assert statistics.successes == 1
    assert statistics.failures == 0
    assert statistics.retries == 0
    assert statistics.total_latency_seconds == 0.25
    assert statistics.success_rate == 1.0
    assert statistics.failure_rate == 0.0
    assert statistics.average_latency_seconds == 0.25


def test_provider_statistics_records_failure():
    statistics = ProviderStatistics()

    statistics.record_failure(
        latency_seconds=0.5,
    )

    assert statistics.requests == 1
    assert statistics.successes == 0
    assert statistics.failures == 1
    assert statistics.retries == 0
    assert statistics.total_latency_seconds == 0.5
    assert statistics.success_rate == 0.0
    assert statistics.failure_rate == 1.0
    assert statistics.average_latency_seconds == 0.5


def test_retry_policy_updates_statistics_after_retry_success():
    statistics = ProviderStatistics()
    attempts = {"count": 0}

    policy = ProviderRetryPolicy(
        max_attempts=3,
        retry_delay_seconds=0.0,
        retry_exceptions=(TemporaryProviderError,),
    )

    def operation() -> str:
        attempts["count"] += 1

        if attempts["count"] < 2:
            raise TemporaryProviderError("Temporary failure")

        return "OK"

    result = policy.run(
        operation,
        statistics=statistics,
    )

    assert result == "OK"
    assert attempts["count"] == 2
    assert statistics.requests == 1
    assert statistics.successes == 1
    assert statistics.failures == 0
    assert statistics.retries == 1
    assert statistics.success_rate == 1.0


def test_retry_policy_updates_statistics_after_final_failure():
    statistics = ProviderStatistics()
    attempts = {"count": 0}

    policy = ProviderRetryPolicy(
        max_attempts=2,
        retry_delay_seconds=0.0,
        retry_exceptions=(TemporaryProviderError,),
    )

    def operation() -> str:
        attempts["count"] += 1
        raise TemporaryProviderError("Temporary failure")

    try:
        policy.run(
            operation,
            statistics=statistics,
        )
    except TemporaryProviderError:
        pass
    else:
        raise AssertionError("Expected TemporaryProviderError")

    assert attempts["count"] == 2
    assert statistics.requests == 1
    assert statistics.successes == 0
    assert statistics.failures == 1
    assert statistics.retries == 1
    assert statistics.failure_rate == 1.0


def main():
    print("\n=========================================")
    print("ORION PROVIDER STATISTICS TEST")
    print("=========================================\n")

    test_provider_statistics_records_success()
    test_provider_statistics_records_failure()
    test_retry_policy_updates_statistics_after_retry_success()
    test_retry_policy_updates_statistics_after_final_failure()

    print("PROVIDER STATISTICS: PASS ✅")


if __name__ == "__main__":
    main()