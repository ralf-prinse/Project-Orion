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
    column_span: int = 1


class DashboardCardCatalog:
    """
    Central catalog for Dashboard MetricCard presentation styles.

    Keeps all presentation metadata centralized.
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
        ),
        "Equity Widget": DashboardCardStyle(
            icon="📈",
            status="info",
            accent_color="#38bdf8",
        ),
        "Today's P/L": DashboardCardStyle(
            icon="📊",
            status="default",
            accent_color="#9ca3af",
        ),
        "Open Positions": DashboardCardStyle(
            icon="📌",
            status="default",
            accent_color="#a78bfa",
        ),
        "Portfolio Exposure": DashboardCardStyle(
            icon="🧭",
            status="warning",
            accent_color="#f59e0b",
        ),
        "Confidence Gauge": DashboardCardStyle(
            icon="🎯",
            status="info",
            accent_color="#3b82f6",
        ),
        "Pressure Gauge": DashboardCardStyle(
            icon="⚖️",
            status="default",
            accent_color="#9ca3af",
        ),
        "Risk Gauge": DashboardCardStyle(
            icon="🛡️",
            status="warning",
            accent_color="#f59e0b",
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
            column_span=3,
        ),
        "Portfolio Allocation": DashboardCardStyle(
            icon="🥧",
            status="default",
            accent_color="#a78bfa",
        ),
        "Equity Curve": DashboardCardStyle(
            icon="📉",
            status="default",
            accent_color="#9ca3af",
        ),
    }

    @classmethod
    def apply(cls, card: GuiMetricCard) -> GuiMetricCard:
        """
        Returns a GuiMetricCard enriched with centralized presentation metadata.
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
            column_span=(
                card.column_span
                if card.column_span != 1
                else style.column_span
            ),
        )

    @classmethod
    def apply_all(cls, cards: list[GuiMetricCard]) -> list[GuiMetricCard]:
        """
        Applies centralized presentation metadata to all dashboard cards.
        """

        return [
            cls.apply(card)
            for card in cards
        ]