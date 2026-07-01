from dataclasses import dataclass


@dataclass(frozen=True)
class TypographyScale:
    """
    Font-size and weight scale for the Orion GUI.
    """

    font_family: str = "Segoe UI"
    display_size: int = 32
    title_size: int = 24
    section_size: int = 18
    body_size: int = 14
    small_size: int = 12
    caption_size: int = 11

    weight_regular: int = 400
    weight_medium: int = 500
    weight_semibold: int = 600
    weight_bold: int = 700

    def font_rule(self, size: int, weight: int | None = None) -> str:
        selected_weight = weight if weight is not None else self.weight_regular
        return (
            f"font-family: '{self.font_family}'; "
            f"font-size: {size}px; "
            f"font-weight: {selected_weight};"
        )


ORION_TYPOGRAPHY = TypographyScale()
