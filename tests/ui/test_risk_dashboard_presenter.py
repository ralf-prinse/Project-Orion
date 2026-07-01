from services.risk.models import RiskContext, RiskProfile, RiskResult
from ui.foundation.models import GuiPage
from ui.foundation.navigation import NavigationRegistry
from ui.foundation.risk_dashboard_presenter import RiskDashboardPresenter


def test_risk_dashboard_presenter_creates_core_sections():
    result = RiskResult(
        symbol="AAPL",
        risk_allowed=True,
        portfolio_value=100000.0,
        proposed_risk_ratio=0.01,
        total_portfolio_risk=0.04,
        drawdown=0.02,
        cash_reserve_after_trade=0.35,
        position_exposure=0.12,
    )

    sections = RiskDashboardPresenter().create_sections(result)

    assert [section.title for section in sections] == [
        "Risk Dashboard",
        "Risk Limit Status",
        "Risk Metrics",
    ]
    assert sections[0].metrics[0].value == "AAPL"
    assert sections[0].metrics[1].value == "Yes"
    assert sections[2].metrics[0].value == "0.0100"


def test_risk_dashboard_presenter_formats_blocked_risk_result():
    result = RiskResult(
        symbol="TSLA",
        risk_allowed=False,
        trade_risk_allowed=False,
        portfolio_risk_allowed=False,
        drawdown_allowed=True,
        capital_protection_allowed=True,
        position_exposure_allowed=False,
    )

    sections = RiskDashboardPresenter().create_sections(result)
    limit_metrics = {metric.label: metric.value for metric in sections[1].metrics}

    assert sections[0].metrics[1].value == "No"
    assert limit_metrics["Trade Risk Allowed"] == "No"
    assert limit_metrics["Portfolio Risk Allowed"] == "No"
    assert limit_metrics["Position Exposure Allowed"] == "No"
    assert limit_metrics["Drawdown Allowed"] == "Yes"


def test_risk_dashboard_presenter_can_include_context_and_profile():
    result = RiskResult(symbol="MSFT", risk_allowed=True)
    context = RiskContext(
        symbol="msft",
        portfolio_value=75000.0,
        cash_available=25000.0,
        current_portfolio_risk=0.03,
        proposed_position_value=9000.0,
        proposed_risk_amount=750.0,
    )
    profile = RiskProfile(
        max_risk_per_trade=0.015,
        max_portfolio_risk=0.08,
        max_drawdown=0.12,
        min_cash_reserve=0.15,
        max_position_exposure=0.20,
    )

    sections = RiskDashboardPresenter().create_sections(
        risk_result=result,
        risk_context=context,
        risk_profile=profile,
    )

    assert [section.title for section in sections] == [
        "Risk Dashboard",
        "Risk Limit Status",
        "Risk Metrics",
        "Risk Context",
        "Risk Profile",
    ]
    assert sections[3].metrics[0].value == "MSFT"
    assert sections[4].metrics[0].value == "0.0150"


def test_risk_dashboard_presenter_adds_diagnostics_when_available():
    result = RiskResult(symbol="NVDA", risk_allowed=False)
    result.add_reason("Trade risk exceeds configured limit.")
    result.add_warning("Cash reserve would be below target.")

    sections = RiskDashboardPresenter().create_sections(result)

    assert sections[-1].title == "Risk Diagnostics"
    assert sections[-1].metrics[0].label == "Reason 1"
    assert sections[-1].metrics[1].label == "Warning 1"


def test_navigation_registry_contains_risk_page():
    registry = NavigationRegistry()

    assert registry.contains_page(GuiPage.RISK) is True

    labels_by_page = {item.page: item.label for item in registry.get_items()}
    assert labels_by_page[GuiPage.RISK] == "Risk"
