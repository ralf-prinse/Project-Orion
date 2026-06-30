import pytest

from services.signals.config.signal_thresholds import (
    DEFAULT_PROFILE,
    get_signal_thresholds,
)


def test_get_signal_thresholds_returns_default_profile():
    thresholds = get_signal_thresholds()

    assert DEFAULT_PROFILE == "default"
    assert "buy" in thresholds
    assert "watch" in thresholds
    assert "sell" in thresholds


def test_buy_thresholds_contain_required_scores():
    thresholds = get_signal_thresholds()

    buy_thresholds = thresholds["buy"]

    assert buy_thresholds["overall_score"] == 75
    assert buy_thresholds["trend_score"] == 75
    assert buy_thresholds["momentum_score"] == 65
    assert buy_thresholds["structure_score"] == 65
    assert buy_thresholds["volume_score"] == 50
    assert buy_thresholds["relative_strength_score"] == 70
    assert buy_thresholds["candlestick_score"] == 50


def test_unknown_signal_threshold_profile_raises_error():
    with pytest.raises(ValueError):
        get_signal_thresholds("unknown")