from dataclasses import dataclass

from ui.foundation.models import GuiMetricCard


@dataclass(frozen=True)
class DashboardCardStyle:
    """
    Presentation-only styling metadata for dashboard metric cards.

    Contains no trading, scanner, portfolio, risk or AI logic.
    """

    icon: str = ""
    status: str = "default"
    accent_color: str = ""
    size: str = "normal"


class DashboardCardCatalog:
    """
    Central catalog for Dashboard MetricCard presentation styles.

    This keeps icons, statuses, accents and card sizing centralized
    instead of scattering styling metadata across presenters.
    """

    _styles: dict[str, DashboardCardStyle] = {
        "Portfolio Summary": DashboardCardStyle(
            icon="💼",
            status="info",
            accent_color="#3b82f6",
            size="hero",
        ),
        "Cash Widget": DashboardCardStyle(
            icon="💶",
            status="success",
            accent_color="#22c55e",
            size="normal",
        ),
        "Equity Widget": DashboardCardStyle(
            icon="📈",
            status="info",
            accent_color="#38bdf8",
            size="normal",
        ),
        "Today's P/L": DashboardCardStyle(
            icon="📊",
            status="default",
            accent_color="#9ca3af",
            size="normal",
        ),
        "Open Positions": DashboardCardStyle(
            icon="📌",
            status="default",
            accent_color="#a78bfa",
            size="normal",
        ),
        "Portfolio Exposure": DashboardCardStyle(
            icon="🧭",
            status="warning",
            accent_color="#f59e0b",
            size="normal",
        ),
        "Confidence Gauge": DashboardCardStyle(
            icon="🎯",
            status="info",
            accent_color="#3b82f6",
            size="normal",
        ),
        "Pressure Gauge": DashboardCardStyle(
            icon="⚖️",
            status="default",
            accent_color="#9ca3af",
            size="normal",
        ),
        "Risk Gauge": DashboardCardStyle(
            icon="🛡️",
            status="warning",
            accent_color="#f59e0b",
            size="normal",
        ),
        "Best Trade Card": DashboardCardStyle(
            icon="⭐",
            status="success",
            accent_color="#22c55e",
            size="hero",
        ),
        "Market Health": DashboardCardStyle(
            icon="🌍",
            status="info",
            accent_color="#3b82f6",
            size="hero",
        ),
        "Portfolio Allocation": DashboardCardStyle(
            icon="🥧",
            status="default",
            accent_color="#a78bfa",
            size="normal",
        ),
        "Equity Curve": DashboardCardStyle(
            icon="📉",
            status="default",
            accent_color="#9ca3af",
            size="normal",
        ),
    }

    @classmethod
    def apply(cls, card: GuiMetricCard) -> GuiMetricCard:
        """
        Returns a new GuiMetricCard with centralized dashboard styling applied.
        """

        style = cls._styles.get(card.title, DashboardCardStyle())

        return GuiMetricCard(
            title=card.title,
            value=card.value,
            subtitle=card.subtitle,
            trend=card.trend,
            icon=card.icon or style.icon,
            accent_color=card.accent_color or style.accent_color,
            status=card.status if card.status != "default" else style.status,
            size=card.size if card.size != "normal" else style.size,
        )

    @classmethod
    def apply_all(cls, cards: list[GuiMetricCard]) -> list[GuiMetricCard]:
        """
        Applies dashboard card styling to a list of cards.
        """

        return [
            cls.apply(card)
            for card in cards
        ]