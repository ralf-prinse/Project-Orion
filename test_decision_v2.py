from engines.decision_engine import DecisionEngine
from models.technical_analysis import TechnicalAnalysis


decision_engine = DecisionEngine()

analysis = TechnicalAnalysis(
    rsi=22.90,
    rsi_signal="oversold",
    ema_20=295.43,
    ema_50=290.21,
    trend_signal="uptrend",
)

action_without_position = decision_engine.decide(
    technical_analysis=analysis,
    has_position=False,
)

action_with_position = decision_engine.decide(
    technical_analysis=analysis,
    has_position=True,
)

print("=== DECISION V2 TEST ===")
print(f"Actie zonder positie: {action_without_position}")
print(f"Actie met positie: {action_with_position}")