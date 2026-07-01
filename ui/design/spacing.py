from dataclasses import dataclass


@dataclass(frozen=True)
class SpacingScale:
    """
    Consistent spacing scale for layouts and components.
    """

    xs: int = 4
    sm: int = 8
    md: int = 12
    lg: int = 16
    xl: int = 24
    xxl: int = 32
    xxxl: int = 48

    def css_padding(self, vertical: int, horizontal: int | None = None) -> str:
        selected_horizontal = vertical if horizontal is None else horizontal
        return f"padding: {vertical}px {selected_horizontal}px;"

    def css_margin(self, vertical: int, horizontal: int | None = None) -> str:
        selected_horizontal = vertical if horizontal is None else horizontal
        return f"margin: {vertical}px {selected_horizontal}px;"


ORION_SPACING = SpacingScale()
