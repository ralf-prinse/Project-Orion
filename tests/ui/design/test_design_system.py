from ui.design import ORION_DARK_PALETTE, ORION_DARK_THEME, ORION_ICONS, ORION_SPACING, ORION_TYPOGRAPHY
from ui.foundation.models import GuiPage


def test_orion_palette_exposes_semantic_colours():
    colours = ORION_DARK_PALETTE.as_dict()

    assert colours["background"] == "#111827"
    assert colours["surface"] == "#1F2937"
    assert colours["primary"] == "#2563EB"
    assert colours["danger"] == "#DC2626"


def test_typography_scale_generates_font_rule():
    rule = ORION_TYPOGRAPHY.font_rule(18, ORION_TYPOGRAPHY.weight_bold)

    assert "font-family" in rule
    assert "font-size: 18px" in rule
    assert "font-weight: 700" in rule


def test_spacing_scale_generates_css_helpers():
    assert ORION_SPACING.css_padding(8, 16) == "padding: 8px 16px;"
    assert ORION_SPACING.css_margin(12) == "margin: 12px 12px;"


def test_theme_generates_application_stylesheet():
    stylesheet = ORION_DARK_THEME.application_stylesheet()

    assert "QWidget" in stylesheet
    assert ORION_DARK_THEME.palette.background in stylesheet
    assert ORION_DARK_THEME.palette.primary in stylesheet


def test_icons_are_stable_for_navigation_pages():
    assert ORION_ICONS.for_page(GuiPage.DASHBOARD) == "◈"
    assert ORION_ICONS.for_page(GuiPage.SETTINGS) == "⚙"
