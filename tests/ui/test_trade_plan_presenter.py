from services.planner.models import TradePlanResult
from ui.foundation.gui_shell import GuiShell
from ui.foundation.models import GuiPage
from ui.foundation.navigation import NavigationRegistry
from ui.foundation.trade_plan_presenter import TradePlanPresenter


def _sample_trade_plan() -> TradePlanResult:
    return TradePlanResult(
        symbol="MSFT",
        action="BUY",
        valid_plan=True,
        entry_price=100.0,
        stop_loss=95.0,
        target_price=110.0,
        shares=20,
        position_value=2000.0,
        risk_per_share=5.0,
        total_risk_amount=100.0,
        expected_reward_per_share=10.0,
        expected_reward_amount=200.0,
        reward_risk_ratio=2.0,
        currency="USD",
    )


def test_trade_plan_presenter_creates_core_sections():
    sections = TradePlanPresenter().create_sections(_sample_trade_plan())

    assert [section.title for section in sections] == [
        "Trade Plan Summary",
        "Entry, Stop & Target",
        "Planned Position",
        "Reward / Risk",
    ]
    assert sections[0].metrics[0].value == "MSFT"
    assert sections[0].metrics[1].value == "BUY"
    assert sections[0].metrics[2].value == "Yes"


def test_trade_plan_presenter_formats_price_and_reward_risk_metrics():
    sections = TradePlanPresenter().create_sections(_sample_trade_plan())

    price_section = sections[1]
    position_section = sections[2]
    reward_risk_section = sections[3]

    assert [metric.value for metric in price_section.metrics] == [
        "100.00",
        "95.00",
        "110.00",
        "5.00",
    ]
    assert [metric.value for metric in position_section.metrics] == [
        "20",
        "2000.00",
        "100.00",
    ]
    assert reward_risk_section.metrics[-1].value == "2.00"


def test_trade_plan_presenter_includes_diagnostics_when_available():
    result = _sample_trade_plan()
    result.add_warning("Reward/risk ratio below preferred threshold.")
    result.add_reason("Trade plan summary assembled.")

    sections = TradePlanPresenter().create_sections(result)

    assert sections[-1].title == "Trade Plan Diagnostics"
    assert sections[-1].metrics[0].label == "Warning 1"
    assert sections[-1].metrics[0].value == "Reward/risk ratio below preferred threshold."
    assert sections[-1].metrics[1].label == "Reason 1"


def test_gui_shell_builds_trade_plan_dashboard_without_planning_trades():
    state = GuiShell().build_trade_plan_dashboard(_sample_trade_plan())

    assert state.current_page == GuiPage.TRADE_PLANNER
    assert state.status_message == "Trade plan dashboard updated"
    assert state.sections[0].title == "Trade Plan Summary"
    assert state.sections[1].metrics[0].value == "100.00"


def test_navigation_registry_contains_trade_planner_page():
    items = NavigationRegistry().get_items()

    assert any(item.page == GuiPage.TRADE_PLANNER for item in items)
    assert [item.page for item in items].index(GuiPage.TRADE_PLANNER) > [
        item.page for item in items
    ].index(GuiPage.PAPER_TRADING)
