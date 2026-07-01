from core.configuration import (
    ConfigurationValidator,
    OrionConfiguration,
    ScanProfileConfig,
    TradingRiskProfileConfig,
)


def test_default_configuration_is_valid():
    result = ConfigurationValidator().validate(OrionConfiguration())

    assert result.is_valid
    assert result.errors == []


def test_validator_rejects_invalid_risk_values():
    configuration = OrionConfiguration(
        trading_risk=TradingRiskProfileConfig(
            account_equity=0,
            risk_per_trade=0,
            max_position_value=-1,
        )
    )

    result = ConfigurationValidator().validate(configuration)

    assert not result.is_valid
    assert "trading_risk.account_equity must be greater than zero." in result.errors
    assert "trading_risk.risk_per_trade must be greater than zero." in result.errors
    assert "trading_risk.max_position_value must be greater than zero when configured." in result.errors


def test_validator_warns_for_high_risk_per_trade():
    configuration = OrionConfiguration(
        trading_risk=TradingRiskProfileConfig(risk_per_trade=0.075)
    )

    result = ConfigurationValidator().validate(configuration)

    assert result.is_valid
    assert "trading_risk.risk_per_trade is above 5%." in result.warnings


def test_validator_rejects_negative_scan_limits():
    configuration = OrionConfiguration(scan=ScanProfileConfig(max_opportunities=-1))

    result = ConfigurationValidator().validate(configuration)

    assert not result.is_valid
    assert "scan.max_opportunities must be zero or greater." in result.errors
