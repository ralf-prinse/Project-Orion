import json

import pytest

from core.configuration import ConfigurationService, OrionConfiguration


def test_service_loads_configuration_from_dict():
    service = ConfigurationService()

    configuration = service.load_from_dict(
        {
            "profile_name": "custom",
            "trading_risk": {"account_equity": 25000, "risk_per_trade": 0.015},
        }
    )

    assert configuration.profile_name == "custom"
    assert configuration.trading_risk.account_equity == 25000
    assert configuration.trading_risk.risk_per_trade == 0.015


def test_service_rejects_invalid_configuration_dict():
    service = ConfigurationService()

    with pytest.raises(ValueError):
        service.load_from_dict({"trading_risk": {"risk_per_trade": 0}})


def test_service_saves_and_loads_configuration_file(tmp_path):
    service = ConfigurationService()
    configuration = OrionConfiguration(profile_name="file_profile")
    path = tmp_path / "orion_profile.json"

    service.save_to_file(configuration, path)
    loaded = service.load_from_file(path)

    assert loaded == configuration
    assert json.loads(path.read_text(encoding="utf-8"))["profile_name"] == "file_profile"


def test_service_rejects_non_object_json_file(tmp_path):
    service = ConfigurationService()
    path = tmp_path / "invalid.json"
    path.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError):
        service.load_from_file(path)
