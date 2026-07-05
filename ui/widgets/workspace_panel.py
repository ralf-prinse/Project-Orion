from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget

from ui.foundation.workspace import GuiWorkspacePanel


class WorkspacePanel(QFrame):
    """
    Generic presentation-only workspace panel.

    Renders GuiWorkspacePanel models produced by presenters.

    No business logic.
    No trading calculations.
    No scanner orchestration.
    No AI logic.
    """

    opportunity_selected = Signal(str)

    def __init__(
        self,
        theme,
        panel: GuiWorkspacePanel,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.theme = theme
        self.panel = panel

        self.setObjectName("WorkspacePanel")
        self.setStyleSheet(self._style(panel))

        self.title_label = QLabel(panel.title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.title_label.setStyleSheet(self._title_style(panel))
        self.title_label.setVisible(bool(panel.title))

        self.subtitle_label = QLabel(panel.subtitle)
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setStyleSheet(self._subtitle_style())
        self.subtitle_label.setVisible(bool(panel.subtitle))

        self.items_container = QWidget()
        self.items_layout = QVBoxLayout(self.items_container)
        self.items_layout.setContentsMargins(0, 0, 0, 0)
        self.items_layout.setSpacing(self._item_spacing(panel))

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)

        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.items_container)

        self.setLayout(layout)

        self._render_items(panel.items)

    def set_panel(self, panel: GuiWorkspacePanel) -> None:
        self.panel = panel
        self.setStyleSheet(self._style(panel))

        self.title_label.setText(panel.title)
        self.title_label.setStyleSheet(self._title_style(panel))
        self.title_label.setVisible(bool(panel.title))

        self.subtitle_label.setText(panel.subtitle)
        self.subtitle_label.setVisible(bool(panel.subtitle))

        self.items_layout.setSpacing(self._item_spacing(panel))

        self._clear_items()
        self._render_items(panel.items)

    def _render_items(self, items: list[Any]) -> None:
        if not items:
            empty_label = QLabel("Geen gegevens beschikbaar")
            empty_label.setStyleSheet(self._empty_style())
            self.items_layout.addWidget(empty_label)
            return

        for index, item in enumerate(items, start=1):
            self.items_layout.addWidget(self._build_item_widget(item, index))

    def _build_item_widget(self, item: Any, index: int) -> QWidget:
        if self._is_opportunity_item(item):
            return self._build_opportunity_button(item, index)

        label = QLabel(str(item))
        label.setWordWrap(True)
        label.setStyleSheet(self._item_style())
        return label

    def _build_opportunity_button(
        self,
        item: dict[str, Any],
        index: int,
    ) -> QPushButton:
        symbol = str(item.get("symbol", "")).strip()
        display_text = str(item.get("display_text", symbol or item))

        button = QPushButton(display_text)
        button.setObjectName("OpportunityButton")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setFlat(True)
        button.setCheckable(False)
        button.setAutoDefault(False)
        button.setDefault(False)
        button.setMinimumHeight(96)
        button.setStyleSheet(self._opportunity_button_style(index))

        if symbol:
            button.clicked.connect(
                lambda checked=False, selected_symbol=symbol: self.opportunity_selected.emit(
                    selected_symbol
                )
            )

        return button

    def _clear_items(self) -> None:
        while self.items_layout.count():
            layout_item = self.items_layout.takeAt(0)
            widget = layout_item.widget()

            if widget is not None:
                widget.deleteLater()

    def _is_opportunity_item(self, item: Any) -> bool:
        return (
            isinstance(item, dict)
            and item.get("type") == "opportunity"
            and bool(item.get("symbol"))
        )

    def _style(self, panel: GuiWorkspacePanel) -> str:
        return f"""
        QFrame#WorkspacePanel {{
            background-color: {self._background_color(panel)};
            border: 1px solid {self._border_color(panel)};
            border-radius: 16px;
        }}

        QFrame#WorkspacePanel:hover {{
            border: 1px solid {self._accent_color(panel)};
        }}
        """

    def _title_style(self, panel: GuiWorkspacePanel) -> str:
        return f"""
        color: {self._accent_color(panel)};
        font-size: 15px;
        font-weight: 800;
        letter-spacing: 0.4px;
        """

    def _subtitle_style(self) -> str:
        return """
        color: #9ca3af;
        font-size: 12px;
        font-weight: 500;
        """

    def _item_style(self) -> str:
        return """
        color: #f9fafb;
        font-size: 13px;
        font-weight: 500;
        """

    def _empty_style(self) -> str:
        return """
        color: #6b7280;
        font-size: 13px;
        font-weight: 500;
        font-style: italic;
        """

    def _opportunity_button_style(self, index: int) -> str:
        if index == 1:
            border_color = self._accent_color(self.panel)
            background_color = "#111f1a"
            font_weight = 800
        else:
            border_color = "#374151"
            background_color = "#0f172a"
            font_weight = 650

        return f"""
        QPushButton#OpportunityButton {{
            background-color: {background_color};
            border: 1px solid {border_color};
            border-radius: 12px;
            color: #f9fafb;
            font-size: 13px;
            font-weight: {font_weight};
            padding: 12px 14px;
            text-align: left;
            line-height: 145%;
        }}

        QPushButton#OpportunityButton:hover {{
            background-color: #111827;
            border: 1px solid {self._accent_color(self.panel)};
        }}

        QPushButton#OpportunityButton:pressed {{
            background-color: #020617;
            border: 1px solid #60a5fa;
        }}
        """

    def _item_spacing(self, panel: GuiWorkspacePanel) -> int:
        if panel.panel_type == "top_opportunities":
            return 10

        return 8

    def _background_color(self, panel: GuiWorkspacePanel) -> str:
        if panel.status == "success":
            return "#0f2419"

        if panel.status == "warning":
            return "#2b1f0d"

        if panel.status == "danger":
            return "#2b1111"

        if panel.status == "info":
            return "#0f2033"

        return "#111827"

    def _border_color(self, panel: GuiWorkspacePanel) -> str:
        if panel.status == "success":
            return "#22c55e"

        if panel.status == "warning":
            return "#f59e0b"

        if panel.status == "danger":
            return "#ef4444"

        if panel.status == "info":
            return "#3b82f6"

        return "#374151"

    def _accent_color(self, panel: GuiWorkspacePanel) -> str:
        if panel.status == "success":
            return "#22c55e"

        if panel.status == "warning":
            return "#f59e0b"

        if panel.status == "danger":
            return "#ef4444"

        if panel.status == "info":
            return "#3b82f6"

        return "#9ca3af"