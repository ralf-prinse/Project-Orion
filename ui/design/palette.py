from dataclasses import dataclass


@dataclass(frozen=True)
class OrionPalette:
    """
    Central colour palette for the Orion desktop interface.

    The GUI should consume these semantic colours instead of hard-coded hex
    values. This keeps future theme changes isolated from presenters and pages.
    """

    background: str = "#111827"
    background_elevated: str = "#172033"
    surface: str = "#1F2937"
    surface_hover: str = "#263244"
    surface_selected: str = "#1E3A8A"
    border: str = "#374151"
    border_subtle: str = "#263244"

    primary: str = "#2563EB"
    primary_hover: str = "#1D4ED8"
    accent: str = "#06B6D4"

    success: str = "#16A34A"
    warning: str = "#F59E0B"
    danger: str = "#DC2626"
    info: str = "#38BDF8"
    neutral: str = "#64748B"

    text: str = "#F9FAFB"
    text_secondary: str = "#D1D5DB"
    text_muted: str = "#9CA3AF"
    text_disabled: str = "#6B7280"

    def as_dict(self) -> dict[str, str]:
        return self.__dict__.copy()


ORION_DARK_PALETTE = OrionPalette()
