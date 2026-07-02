from dataclasses import dataclass


@dataclass(frozen=True)
class ChartStyle:
    """
    Shared chart styling contract for Orion chart widgets.

    This keeps chart rendering visually consistent across all future workspaces.
    """

    background_color: str = "#111827"
    border_color: str = "#1F2937"
    grid_color: str = "#374151"
    axis_color: str = "#6B7280"
    text_color: str = "#E5E7EB"
    muted_text_color: str = "#9CA3AF"
    primary_line_color: str = "#F9FAFB"
    point_color: str = "#F9FAFB"
    border_radius: int = 10
    padding: int = 16
    grid_lines: int = 4


ORION_CHART_STYLE = ChartStyle()