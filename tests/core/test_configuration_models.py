from core.configuration import OrionConfiguration


def test_configuration_roundtrip_preserves_profile_values():
    configuration = OrionConfiguration()

    restored = OrionConfiguration.from_dict(configuration.to_dict())

    assert restored == configuration


def test_configuration_from_dict_uses_defaults_for_missing_sections():
    configuration = OrionConfiguration.from_dict({"profile_name": "custom"})

    assert configuration.profile_name == "custom"
    assert configuration.scan.max_opportunities == 3
    assert configuration.trading_risk.risk_per_trade == 0.01
    assert configuration.planner.minimum_reward_risk_ratio == 2.0
