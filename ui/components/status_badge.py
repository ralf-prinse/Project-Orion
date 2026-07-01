from dataclasses import dataclass
from enum import Enum

from ui.design import ORION_DARK_THEME, OrionTheme


class BadgeStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    DISABLED = "disabled"


@dataclass(frozen=True)
class StatusBadgeViewModel:
    label: str
    status: BadgeStatus
    color: str


class StatusBadgeComponent:
    def __init__(self, theme: OrionTheme | None = None):
        self.theme = theme or ORION_DARK_THEME

    def create(self, label: str, status: BadgeStatus | str = BadgeStatus.IDLE) -> StatusBadgeViewModel:
        normalized_status = status if isinstance(status, BadgeStatus) else BadgeStatus(str(status).lower())
        return StatusBadgeViewModel(
            label=label.strip().upper(),
            status=normalized_status,
            color=self._color_for_status(normalized_status),
        )

    def _color_for_status(self, status: BadgeStatus) -> str:
        palette = self.theme.palette
        return {
            BadgeStatus.IDLE: palette.neutral,
            BadgeStatus.RUNNING: palette.info,
            BadgeStatus.SUCCESS: palette.success,
            BadgeStatus.WARNING: palette.warning,
            BadgeStatus.ERROR: palette.danger,
            BadgeStatus.DISABLED: palette.text_disabled,
        }[status]
