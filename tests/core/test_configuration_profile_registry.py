import pytest

from core.configuration import ConfigurationProfileRegistry, OrionConfiguration


def test_registry_exposes_default_profiles():
    registry = ConfigurationProfileRegistry()

    assert registry.list_profiles() == [
        "aggressive_swing",
        "balanced_swing",
        "conservative_swing",
    ]


def test_registry_returns_balanced_profile_as_default():
    registry = ConfigurationProfileRegistry()

    default_profile = registry.default()

    assert default_profile.profile_name == "balanced_swing"
    assert default_profile.trading_risk.risk_per_trade == 0.01


def test_registry_can_register_custom_profile():
    registry = ConfigurationProfileRegistry(profiles=[])
    custom = OrionConfiguration(profile_name="custom_profile")

    registry.register(custom)

    assert registry.get("custom_profile") == custom


def test_registry_rejects_unknown_profile():
    registry = ConfigurationProfileRegistry(profiles=[])

    with pytest.raises(KeyError):
        registry.get("missing")
