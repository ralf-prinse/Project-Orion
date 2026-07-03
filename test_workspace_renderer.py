from ui.foundation.workspace import GuiWorkspace
from ui.foundation.workspace_renderer import WorkspaceRenderer


class DummyDashboardGrid:
    def __init__(self):
        self.cleared = False
        self.cards = None

    def clear(self):
        self.cleared = True

    def add_cards(self, cards):
        self.cards = cards


class DummyChartContainer:
    def __init__(self):
        self.cleared = False
        self.widgets = []

    def clear(self):
        self.cleared = True

    def add_chart_widgets(self, widgets):
        self.widgets.extend(widgets)


class DummyChartRenderer:
    def __init__(self):
        self.charts = []

    def render(self, charts):
        self.charts = charts
        return [
            {
                "widget": "chart",
                "title": chart["title"],
            }
            for chart in charts
        ]


def test_workspace_renderer_renders_cards():
    grid = DummyDashboardGrid()
    chart_container = DummyChartContainer()
    chart_renderer = DummyChartRenderer()

    renderer = WorkspaceRenderer(
        dashboard_grid=grid,
        chart_container=chart_container,
        chart_renderer=chart_renderer,
    )

    workspace = GuiWorkspace(
        title="Dashboard",
        cards=[
            {"title": "Portfolio"},
            {"title": "Market Health"},
        ],
    )

    renderer.render(workspace)

    assert grid.cleared is True
    assert len(grid.cards) == 2
    assert chart_container.cleared is True
    assert chart_container.widgets == []
    assert chart_renderer.charts == []


def test_workspace_renderer_renders_charts_into_container():
    grid = DummyDashboardGrid()
    chart_container = DummyChartContainer()
    chart_renderer = DummyChartRenderer()

    renderer = WorkspaceRenderer(
        dashboard_grid=grid,
        chart_container=chart_container,
        chart_renderer=chart_renderer,
    )

    workspace = GuiWorkspace(
        title="Dashboard",
        charts=[
            {"title": "Equity Curve"},
        ],
    )

    renderer.render(workspace)

    assert grid.cleared is True
    assert grid.cards == []
    assert chart_container.cleared is True
    assert len(chart_container.widgets) == 1
    assert chart_container.widgets[0]["title"] == "Equity Curve"