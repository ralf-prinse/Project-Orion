from __future__ import annotations

from ui.foundation.chart_widget_factory import ChartWidgetFactory
from ui.foundation.charts import GuiChart


class ChartRenderer:
    """
    Presentation-only chart renderer.

    Converts GuiChart presentation models into chart widgets by delegating
    widget creation to ChartWidgetFactory.

    The renderer does not own layout decisions yet.
    Layout integration remains the responsibility of the workspace layer.

    No business logic.
    No calculations.
    """

    def __init__(
        self,
        chart_widget_factory: ChartWidgetFactory | None = None,
    ) -> None:
        self._chart_widget_factory = (
            chart_widget_factory
            if chart_widget_factory is not None
            else ChartWidgetFactory()
        )

    def render(self, charts: list[GuiChart]):
        widgets = []

        for chart in charts:
            widget = self._chart_widget_factory.create_widget(chart)

            if widget is not None:
                widgets.append(widget)

        return widgets