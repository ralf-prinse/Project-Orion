from dataclasses import dataclass

from ui.design.metrics import GuiMetrics, ORION_GUI_METRICS
from ui.design.palette import OrionPalette, ORION_DARK_PALETTE
from ui.design.spacing import SpacingScale, ORION_SPACING
from ui.design.typography import TypographyScale, ORION_TYPOGRAPHY


@dataclass(frozen=True)
class OrionTheme:
    """
    Complete design-system object for Orion.

    This class is intentionally framework-light. It can produce Qt stylesheets
    today, while presenters and tests can consume the same semantic values
    without importing PySide6.
    """

    name: str = "Orion Dark"
    palette: OrionPalette = ORION_DARK_PALETTE
    typography: TypographyScale = ORION_TYPOGRAPHY
    spacing: SpacingScale = ORION_SPACING
    metrics: GuiMetrics = ORION_GUI_METRICS

    def application_stylesheet(self) -> str:
        p = self.palette
        t = self.typography
        s = self.spacing
        m = self.metrics
        return f"""
        QWidget {{
            background-color: {p.background};
            color: {p.text};
            {t.font_rule(t.body_size)}
        }}
        QMainWindow {{
            background-color: {p.background};
        }}
        QLabel {{
            background-color: transparent;
            color: {p.text};
        }}
        QPushButton {{
            background-color: {p.surface};
            color: {p.text_secondary};
            border: {m.border_width}px solid {p.border_subtle};
            border-radius: {m.card_radius}px;
            {s.css_padding(s.md, s.lg)}
            text-align: left;
        }}
        QPushButton:hover {{
            background-color: {p.surface_hover};
            border-color: {p.border};
        }}
        QPushButton:pressed {{
            background-color: {p.surface_selected};
            border-color: {p.primary};
        }}
        QFrame#OrionCard, QFrame#OrionPanel {{
            background-color: {p.surface};
            border: {m.border_width}px solid {p.border_subtle};
            border-radius: {m.card_radius}px;
        }}
        QFrame#OrionSidebar {{
            background-color: #0B1120;
            border-right: {m.border_width}px solid {p.border_subtle};
        }}
        QFrame#OrionStatusBar {{
            background-color: {p.background_elevated};
            border-top: {m.border_width}px solid {p.border_subtle};
        }}
        """

    def title_style(self) -> str:
        return f"color: {self.palette.text}; {self.typography.font_rule(self.typography.display_size, self.typography.weight_bold)}"

    def section_title_style(self) -> str:
        return f"color: {self.palette.text}; {self.typography.font_rule(self.typography.section_size, self.typography.weight_semibold)}"

    def muted_text_style(self) -> str:
        return f"color: {self.palette.text_muted}; {self.typography.font_rule(self.typography.body_size)}"

    def card_style(self) -> str:
        p = self.palette
        m = self.metrics
        return (
            f"background-color: {p.surface}; "
            f"border: {m.border_width}px solid {p.border_subtle}; "
            f"border-radius: {m.card_radius}px;"
        )


ORION_DARK_THEME = OrionTheme()
