"""
Centrale signaalconfiguratie voor Project Orion.

Deze waarden bepalen hoe AnalysisResult later wordt vertaald naar
deterministische handelssignalen.

Sprint 8.2:
- Alleen het default-profiel is actief.
- Aggressive en conservative profielen kunnen later worden toegevoegd.
- Signaalregels horen niet hardcoded in analyzers te staan.
"""

DEFAULT_PROFILE = "default"

SIGNAL_THRESHOLDS = {
    "default": {
        "buy": {
            "overall_score": 75,
            "trend_score": 75,
            "momentum_score": 65,
            "structure_score": 65,
            "volume_score": 50,
            "relative_strength_score": 70,
            "candlestick_score": 50,
        },
        "watch": {
            "overall_score": 60,
            "trend_score": 60,
            "momentum_score": 55,
            "structure_score": 55,
            "relative_strength_score": 55,
        },
        "sell": {
            "overall_score": 35,
            "trend_score": 35,
            "momentum_score": 35,
            "structure_score": 35,
        },
    }
}


def get_signal_thresholds(
    profile: str = DEFAULT_PROFILE,
) -> dict:
    """
    Retourneert de signaaldrempels voor een strategieprofiel.
    """
    if profile not in SIGNAL_THRESHOLDS:
        raise ValueError(f"Unknown signal threshold profile: {profile}")

    return SIGNAL_THRESHOLDS[profile]