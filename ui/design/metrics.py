from dataclasses import dataclass


@dataclass(frozen=True)
class GuiMetrics:
    """
    Shared sizing constants for the desktop shell.
    """

    sidebar_width: int = 244
    toolbar_height: int = 56
    status_bar_height: int = 28
    card_radius: int = 14
    panel_radius: int = 18
    border_width: int = 1
    default_window_width: int = 1280
    default_window_height: int = 820


ORION_GUI_METRICS = GuiMetrics()
