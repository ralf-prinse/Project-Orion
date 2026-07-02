from ui.workspace.base_workspace import BaseWorkspace
from ui.foundation.models import GuiWorkspace


class PerformanceWorkspace(BaseWorkspace):

    def __init__(self, theme):
        super().__init__(
            theme=theme,
            title="Performance",
            intro="Analyse van rendement en risico.",
        )

    def set_workspace(self, workspace: GuiWorkspace):
        self._clear_rendered_content()

        if workspace.charts:
            row = self._create_chart_row(workspace)
            self.add_workspace_widget(row)

        self.set_sections(workspace.sections)

    def _create_chart_row(self, workspace):
        from PySide6.QtWidgets import QWidget, QHBoxLayout
        from ui.widgets.chart_widget import ChartWidget

        row = QWidget()
        layout = QHBoxLayout()

        for chart in workspace.charts:
            layout.addWidget(
                ChartWidget(self.theme, chart)
            )

        row.setLayout(layout)
        return row