from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SignalInterpretation:

    title: str

    conviction: float

    strengths: list[str]

    weaknesses: list[str]


class SignalInterpreter:

    def interpret(
        self,
        *,
        trend: float,
        momentum: float,
        buy_pressure: float,
        volatility: float,
    ) -> SignalInterpretation:

        strengths: list[str] = []
        weaknesses: list[str] = []

        conviction = 50.0

        # Trend
        if trend >= 0.80:
            conviction += 15
            strengths.append("Trend is sterk")
        elif trend < 0.40:
            conviction -= 15
            weaknesses.append("Trend is zwak")

        # Momentum
        if momentum >= 0.80:
            conviction += 15
            strengths.append("Momentum versnelt")
        elif momentum < 0.40:
            conviction -= 15
            weaknesses.append("Momentum valt weg")

        # Koopdruk
        if buy_pressure >= 0.60:
            conviction += 10
            strengths.append("Koopdruk domineert")
        else:
            conviction -= 10
            weaknesses.append("Verkoopdruk loopt op")

        # Volatiliteit
        if volatility <= 0.70:
            conviction += 10
            strengths.append("Gezonde volatiliteit")
        else:
            conviction -= 10
            weaknesses.append("Te hoge volatiliteit")

        conviction = max(0.0, min(100.0, conviction))

        if conviction >= 80:
            title = "High Conviction Breakout"

        elif conviction >= 65:
            title = "Momentum Continuation"

        elif conviction >= 50:
            title = "Watch"

        else:
            title = "Avoid"

        return SignalInterpretation(
            title=title,
            conviction=conviction,
            strengths=strengths,
            weaknesses=weaknesses,
        )