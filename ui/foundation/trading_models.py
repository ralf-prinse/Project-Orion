from dataclasses import dataclass


@dataclass(frozen=True)
class TradingMetric:
    """
    Presentation-safe metric displayed inside a MetricCard.
    """

    title: str
    value: str
    subtitle: str = ""


@dataclass(frozen=True)
class TradingWorkspaceModel:
    """
    Complete presentation model for the Trading Workspace.

    This model contains only UI-ready values.
    No trading calculations belong here.
    """

    symbol: str

    decision: TradingMetric
    confidence: TradingMetric
    pressure: TradingMetric
    position: TradingMetric
    risk: TradingMetric

    explanation: str

    status: str = "Ready"