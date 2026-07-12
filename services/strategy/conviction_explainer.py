from __future__ import annotations


class ConvictionExplainer:
    """
    Verklaart waarom Orion overtuigd is van een trade.

    BELANGRIJK:

    Deze service neemt GEEN beslissingen.

    Hij vertaalt uitsluitend analyse naar
    begrijpelijke argumenten.
    """

    def explain(
        self,
        *,
        trend: float,
        momentum: float,
        buy_pressure: float,
        volatility: float,
        risk_reward: float,
        market_regime: str,
    ) -> tuple[list[str], list[str]]:

        strengths: list[str] = []
        weaknesses: list[str] = []

        # Trend
        if trend >= 0.80:
            strengths.append("Sterke kortetermijntrend")
        elif trend < 0.40:
            weaknesses.append("Trend is zwak")

        # Momentum
        if momentum >= 0.80:
            strengths.append("Momentum versnelt")
        elif momentum < 0.40:
            weaknesses.append("Momentum neemt af")

        # Koopdruk
        if buy_pressure >= 0.60:
            strengths.append("Koopdruk overheerst")
        else:
            weaknesses.append("Verkoopdruk neemt toe")

        # Volatiliteit
        if volatility <= 0.70:
            strengths.append("Volatiliteit is gecontroleerd")
        else:
            weaknesses.append("Verhoogde volatiliteit")

        # Risk / Reward
        if risk_reward >= 2.5:
            strengths.append("Risk/Reward is aantrekkelijk")
        elif risk_reward < 1.5:
            weaknesses.append("Risk/Reward onvoldoende")

        # Marktregime
        if market_regime.upper() == "BULL":
            strengths.append("Bull market ondersteunt trade")
        elif market_regime.upper() == "BEAR":
            weaknesses.append("Bear market vergroot risico")

        return strengths, weaknesses