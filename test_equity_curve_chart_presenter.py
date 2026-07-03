from ui.foundation.chart_models import GuiChartType
from ui.foundation.equity_curve_chart_presenter import EquityCurveChartPresenter


def test_equity_curve_chart_presenter_returns_line_chart():
    presenter = EquityCurveChartPresenter()

    chart = presenter.present(
        equity_values=[1000.0, 1050.0, 1100.0],
        labels=["Day 1", "Day 2", "Day 3"],
    )

    assert chart.title == "Equity Curve"
    assert chart.subtitle == "Portfolio performance"
    assert chart.chart_type == GuiChartType.LINE
    assert chart.status == "ready"

    assert len(chart.series) == 1
    assert chart.series[0].name == "Portfolio"
    assert chart.series[0].values == [1000.0, 1050.0, 1100.0]
    assert chart.series[0].labels == ["Day 1", "Day 2", "Day 3"]

    assert chart.x_axis.label == "Time"
    assert chart.y_axis.label == "Portfolio Value"

    assert chart.legend.visible is True
    assert chart.legend.position == "bottom"

    assert chart.metadata["widget"] == "equity_curve"
    assert chart.metadata["version"] == "4.3"


def test_equity_curve_chart_presenter_defaults_to_empty_series():
    presenter = EquityCurveChartPresenter()

    chart = presenter.present()

    assert chart.chart_type == GuiChartType.LINE
    assert len(chart.series) == 1
    assert chart.series[0].values == []
    assert chart.series[0].labels == []