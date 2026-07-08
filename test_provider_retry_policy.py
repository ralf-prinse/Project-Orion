from __future__ import annotations

from providers.provider_retry_policy import ProviderRetryPolicy


class TemporaryProviderError(Exception):
    pass


class PermanentProviderError(Exception):
    pass


def test_retry_policy_succeeds_after_temporary_failures():
    attempts = {"count": 0}

    policy = ProviderRetryPolicy(
        max_attempts=3,
        retry_delay_seconds=0.0,
        retry_exceptions=(TemporaryProviderError,),
    )

    def operation() -> str:
        attempts["count"] += 1

        if attempts["count"] < 3:
            raise TemporaryProviderError("Temporary failure")

        return "OK"

    result = policy.run(operation)

    assert result == "OK"
    assert attempts["count"] == 3


def test_retry_policy_raises_after_max_attempts():
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
        policy.run(operation)
    except TemporaryProviderError:
        pass
    else:
        raise AssertionError("Expected TemporaryProviderError")

    assert attempts["count"] == 2


def test_retry_policy_does_not_retry_unlisted_exception():
    attempts = {"count": 0}

    policy = ProviderRetryPolicy(
        max_attempts=3,
        retry_delay_seconds=0.0,
        retry_exceptions=(TemporaryProviderError,),
    )

    def operation() -> str:
        attempts["count"] += 1
        raise PermanentProviderError("Permanent failure")

    try:
        policy.run(operation)
    except PermanentProviderError:
        pass
    else:
        raise AssertionError("Expected PermanentProviderError")

    assert attempts["count"] == 1


def main():
    print("\n=========================================")
    print("ORION PROVIDER RETRY POLICY TEST")
    print("=========================================\n")

    test_retry_policy_succeeds_after_temporary_failures()
    test_retry_policy_raises_after_max_attempts()
    test_retry_policy_does_not_retry_unlisted_exception()

    print("PROVIDER RETRY POLICY: PASS ✅")


if __name__ == "__main__":
    main()