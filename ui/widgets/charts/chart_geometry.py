from dataclasses import dataclass


@dataclass(frozen=True)
class ChartGeometry:
    """
    Screen-space geometry for chart rendering.

    This model contains only rendering coordinates.
    It performs no business logic.
    """

    left: int
    top: int
    right: int
    bottom: int

    @property
    def width(self) -> int:
        return max(self.right - self.left, 1)

    @property
    def height(self) -> int:
        return max(self.bottom - self.top, 1)