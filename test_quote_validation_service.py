from __future__ import annotations

import math

from services.quote_validation_service import (
    QuoteValidationService,
)


def test_accepts_positive_finite_float():
    service = QuoteValidationService()

    result = service.validate(
        symbol="aapl",
        value=123.45,
    )

    assert result.valid is True
    assert result.symbol == "AAPL"
    assert result.normalized_price == 123.45
    assert result.reason == "Quote price is valid."


def test_accepts_numeric_string():
    service = QuoteValidationService()

    result = service.validate(
        symbol="ASML.AS",
        value="987.65",
    )

    assert result.valid is True
    assert result.normalized_price == 987.65


def test_rejects_none():
    service = QuoteValidationService()

    result = service.validate(
        symbol="AAPL",
        value=None,
    )

    assert result.valid is False
    assert result.normalized_price is None
    assert result.reason == "Quote value is missing."


def test_rejects_nan():
    service = QuoteValidationService()

    result = service.validate(
        symbol="AAPL",
        value=float("nan"),
    )

    assert result.valid is False
    assert result.normalized_price is None
    assert result.reason == "Quote value is not finite."


def test_rejects_positive_infinity():
    service = QuoteValidationService()

    result = service.validate(
        symbol="AAPL",
        value=float("inf"),
    )

    assert result.valid is False
    assert result.reason == "Quote value is not finite."


def test_rejects_negative_infinity():
    service = QuoteValidationService()

    result = service.validate(
        symbol="AAPL",
        value=float("-inf"),
    )

    assert result.valid is False
    assert result.reason == "Quote value is not finite."


def test_rejects_zero():
    service = QuoteValidationService()

    result = service.validate(
        symbol="AAPL",
        value=0,
    )

    assert result.valid is False
    assert (
        result.reason
        == "Quote price must be greater than zero."
    )


def test_rejects_negative_price():
    service = QuoteValidationService()

    result = service.validate(
        symbol="AAPL",
        value=-10.0,
    )

    assert result.valid is False
    assert (
        result.reason
        == "Quote price must be greater than zero."
    )


def test_rejects_boolean():
    service = QuoteValidationService()

    result = service.validate(
        symbol="AAPL",
        value=True,
    )

    assert result.valid is False
    assert (
        result.reason
        == "Boolean values are not valid prices."
    )


def test_rejects_non_numeric_text():
    service = QuoteValidationService()

    result = service.validate(
        symbol="AAPL",
        value="unknown",
    )

    assert result.valid is False
    assert (
        result.reason
        == "Quote value cannot be converted to float."
    )


def test_require_valid_price_returns_float():
    service = QuoteValidationService()

    price = service.require_valid_price(
        symbol="AAPL",
        value="100.25",
    )

    assert isinstance(price, float)
    assert price == 100.25
    assert math.isfinite(price)


def test_require_valid_price_raises_for_nan():
    service = QuoteValidationService()

    try:
        service.require_valid_price(
            symbol="AAPL",
            value=float("nan"),
        )

    except ValueError as error:
        assert "Invalid quote for AAPL" in str(error)
        assert "not finite" in str(error)

    else:
        raise AssertionError(
            "Expected invalid NaN quote to raise ValueError."
        )


def test_requires_symbol():
    service = QuoteValidationService()

    try:
        service.validate(
            symbol="",
            value=100.0,
        )

    except ValueError as error:
        assert (
            str(error)
            == "Symbol is required for quote validation."
        )

    else:
        raise AssertionError(
            "Expected empty symbol to raise ValueError."
        )


def run():
    test_accepts_positive_finite_float()
    test_accepts_numeric_string()
    test_rejects_none()
    test_rejects_nan()
    test_rejects_positive_infinity()
    test_rejects_negative_infinity()
    test_rejects_zero()
    test_rejects_negative_price()
    test_rejects_boolean()
    test_rejects_non_numeric_text()
    test_require_valid_price_returns_float()
    test_require_valid_price_raises_for_nan()
    test_requires_symbol()

    print("QUOTE VALIDATION SERVICE: PASS")


if __name__ == "__main__":
    run()