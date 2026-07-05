from __future__ import annotations

from datetime import datetime
from typing import Any

from services.orchestration.live_scanner_service import LiveScannerSnapshot
from ui.foundation.workspace import GuiWorkspace, GuiWorkspacePanel


class MissionControlPresenter:
    """
    Presentation-only Mission Control presenter.

    Builds GuiWorkspace models for the primary Mission Control workspace.
    """

    TOP_OPPORTUNITY_LIMIT = 5
    REASON_PREVIEW_LIMIT = 4

    def present(
        self,
        scanner_snapshot: LiveScannerSnapshot | None = None,
        opportunities: tuple = (),
    ) -> GuiWorkspace:
        return GuiWorkspace(
            title="Mission Control",
            subtitle=self._subtitle(scanner_snapshot),
            panels=[
                self._scanner_status_panel(scanner_snapshot),
                self._scan_duration_panel(scanner_snapshot),
                self._market_data_panel(scanner_snapshot),
                self._universe_coverage_panel(scanner_snapshot),
                self._market_status_panel(scanner_snapshot),
                self._top_opportunities_panel(
                    scanner_snapshot,
                    opportunities,
                ),
            ],
            charts=[],
            metadata={
                "source": "mission_control_presenter",
            },
        )

    def _subtitle(
        self,
        snapshot: LiveScannerSnapshot | None,
    ) -> str:
        if snapshot is None:
            return "Wacht op live scanner-data."

        return (
            f"Laatste scan: {snapshot.timestamp.strftime('%Y-%m-%d %H:%M:%S')} "
            f"• symbolen: {snapshot.total_symbols} "
            f"• quotes: {snapshot.total_quotes} "
            f"• resultaten: {snapshot.total_results}"
        )

    def _scanner_status_panel(
        self,
        snapshot: LiveScannerSnapshot | None,
    ) -> GuiWorkspacePanel:
        if snapshot is None:
            return GuiWorkspacePanel(
                panel_type="scanner_status",
                title="Scanner Status",
                subtitle="Nog geen scanner-snapshot beschikbaar.",
                items=[],
                status="warning",
                metadata={},
            )

        status = "warning" if snapshot.has_errors else "success"
        subtitle = (
            "Scanner uitgevoerd met waarschuwingen."
            if snapshot.has_errors
            else "Scanner succesvol uitgevoerd."
        )

        items = [
            self._item("Symbolen", snapshot.total_symbols),
            self._item("Quotes", snapshot.total_quotes),
            self._item("Technische resultaten", snapshot.total_results),
        ]

        if snapshot.errors:
            items.extend(
                self._item("Fout", error)
                for error in snapshot.errors
            )

        return GuiWorkspacePanel(
            panel_type="scanner_status",
            title="Scanner Status",
            subtitle=subtitle,
            items=items,
            status=status,
            metadata={
                "timestamp": snapshot.timestamp.isoformat(),
                "has_errors": snapshot.has_errors,
            },
        )

    def _scan_duration_panel(
        self,
        snapshot: LiveScannerSnapshot | None,
    ) -> GuiWorkspacePanel:
        if snapshot is None:
            return GuiWorkspacePanel(
                panel_type="scan_duration",
                title="Scan Duration",
                subtitle="Nog geen scanduur beschikbaar.",
                items=[],
                status="neutral",
                metadata={},
            )

        duration = snapshot.duration_seconds

        if duration <= 1:
            status = "success"
            subtitle = "Scan snel uitgevoerd."
        elif duration <= 5:
            status = "info"
            subtitle = "Scan normaal uitgevoerd."
        else:
            status = "warning"
            subtitle = "Scan duurde langer dan verwacht."

        return GuiWorkspacePanel(
            panel_type="scan_duration",
            title="Scan Duration",
            subtitle=subtitle,
            items=[
                self._item("Duur", f"{duration:.3f} sec"),
                self._item(
                    "Tijdstip",
                    snapshot.timestamp.strftime("%H:%M:%S"),
                ),
            ],
            status=status,
            metadata={
                "duration_seconds": duration,
            },
        )

    def _market_data_panel(
        self,
        snapshot: LiveScannerSnapshot | None,
    ) -> GuiWorkspacePanel:
        if snapshot is None:
            return GuiWorkspacePanel(
                panel_type="market_data",
                title="Market Data",
                subtitle="Nog geen marktdata beschikbaar.",
                items=[],
                status="neutral",
                metadata={},
            )

        market_timestamp = getattr(
            snapshot,
            "latest_market_data_timestamp",
            None,
        )

        if market_timestamp is None:
            return GuiWorkspacePanel(
                panel_type="market_data",
                title="Market Data",
                subtitle="Marktdata-tijd onbekend.",
                items=[
                    self._item(
                        "Laatste scan",
                        snapshot.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    ),
                ],
                status="warning",
                metadata={
                    "scan_timestamp": snapshot.timestamp.isoformat(),
                },
            )

        market_timestamp = self._normalize_datetime(market_timestamp)
        scan_timestamp = self._normalize_datetime(snapshot.timestamp)

        age_seconds = max(
            0,
            int((scan_timestamp - market_timestamp).total_seconds()),
        )

        age_text = self._data_age_text(age_seconds)
        status = self._market_data_status(age_seconds)
        subtitle = self._market_data_subtitle(age_seconds)

        return GuiWorkspacePanel(
            panel_type="market_data",
            title="Market Data",
            subtitle=subtitle,
            items=[
                self._item(
                    "Laatste handelsdag",
                    market_timestamp.strftime("%A %d-%m-%Y"),
                ),
                self._item("Leeftijd marktdata", age_text),
                self._item(
                    "Databron",
                    "Yahoo Finance (dagcandles)",
                ),
                self._item(
                    "Laatste scan",
                    scan_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                ),
            ],
            status=status,
            metadata={
                "market_timestamp": market_timestamp.isoformat(),
                "scan_timestamp": scan_timestamp.isoformat(),
                "age_seconds": age_seconds,
            },
        )

    def _universe_coverage_panel(
        self,
        snapshot: LiveScannerSnapshot | None,
    ) -> GuiWorkspacePanel:
        if snapshot is None:
            return GuiWorkspacePanel(
                panel_type="universe_coverage",
                title="Universe Coverage",
                subtitle="Nog geen universe coverage beschikbaar.",
                items=[],
                status="neutral",
                metadata={},
            )

        total_symbols = snapshot.total_symbols
        total_quotes = snapshot.total_quotes
        total_results = snapshot.total_results
        total_errors = len(snapshot.errors)

        quote_coverage = self._percentage(total_quotes, total_symbols)
        analysis_coverage = self._percentage(total_results, total_symbols)

        if total_symbols == 0:
            status = "warning"
            subtitle = "Geen symbolen beschikbaar in de universe."
        elif analysis_coverage >= 80 and not snapshot.has_errors:
            status = "success"
            subtitle = "Universe coverage gezond."
        elif analysis_coverage >= 50:
            status = "info"
            subtitle = "Universe coverage gedeeltelijk beschikbaar."
        else:
            status = "warning"
            subtitle = "Universe coverage beperkt; controleer scannerdata."

        return GuiWorkspacePanel(
            panel_type="universe_coverage",
            title="Universe Coverage",
            subtitle=subtitle,
            items=[
                self._item("Universe", f"{total_symbols} symbolen"),
                self._item(
                    "Quotes ontvangen",
                    f"{total_quotes} ({quote_coverage:.1f}%)",
                ),
                self._item(
                    "Technisch geanalyseerd",
                    f"{total_results} ({analysis_coverage:.1f}%)",
                ),
                self._item("Scanner errors", total_errors),
            ],
            status=status,
            metadata={
                "total_symbols": total_symbols,
                "total_quotes": total_quotes,
                "total_results": total_results,
                "quote_coverage": quote_coverage,
                "analysis_coverage": analysis_coverage,
                "errors": total_errors,
            },
        )

    def _market_status_panel(
        self,
        snapshot: LiveScannerSnapshot | None,
    ) -> GuiWorkspacePanel:
        if snapshot is None:
            return GuiWorkspacePanel(
                panel_type="market_status",
                title="Market Status",
                subtitle="Nog geen marktstatus beschikbaar.",
                items=[],
                status="neutral",
                metadata={},
            )

        if snapshot.total_results == 0:
            return GuiWorkspacePanel(
                panel_type="market_status",
                title="Market Status",
                subtitle="Geen technische resultaten beschikbaar.",
                items=[
                    self._item("Quotes", snapshot.total_quotes),
                    self._item("Errors", len(snapshot.errors)),
                ],
                status="warning" if snapshot.has_errors else "neutral",
                metadata={},
            )

        scores = [
            result.technical_score
            for result in snapshot.technical_results
        ]

        average_score = sum(scores) / len(scores)
        top_score = max(scores)
        opportunity_count = len(
            [
                score
                for score in scores
                if score >= 70
            ]
        )

        if average_score >= 70:
            status = "success"
            summary = "Sterke marktconditie."
        elif average_score >= 50:
            status = "info"
            summary = "Neutrale marktconditie."
        else:
            status = "warning"
            summary = "Zwakke marktconditie."

        return GuiWorkspacePanel(
            panel_type="market_status",
            title="Market Status",
            subtitle=summary,
            items=[
                self._item("Gemiddelde technische score", f"{average_score:.1f}"),
                self._item("Hoogste technische score", f"{top_score:.1f}"),
                self._item("Aantal resultaten", snapshot.total_results),
                self._item("Kansen score ≥ 70", opportunity_count),
            ],
            status=status,
            metadata={
                "average_score": average_score,
                "top_score": top_score,
                "opportunity_count": opportunity_count,
            },
        )

    def _top_opportunities_panel(
        self,
        snapshot: LiveScannerSnapshot | None,
        opportunities: tuple,
    ) -> GuiWorkspacePanel:
        if snapshot is None:
            return GuiWorkspacePanel(
                panel_type="top_opportunities",
                title="Top Opportunities",
                subtitle="Nog geen opportunities beschikbaar.",
                items=[],
                status="neutral",
                metadata={},
            )

        visible_opportunities = tuple(opportunities[: self.TOP_OPPORTUNITY_LIMIT])

        if not visible_opportunities:
            return GuiWorkspacePanel(
                panel_type="top_opportunities",
                title="Top Opportunities",
                subtitle="Geen opportunities gevonden.",
                items=[],
                status="neutral",
                metadata={
                    "count": 0,
                },
            )

        best_score = max(
            self._numeric(getattr(opportunity, "technical_score", 0.0))
            for opportunity in visible_opportunities
        )

        actionable_count = len(
            [
                opportunity
                for opportunity in visible_opportunities
                if self._is_actionable_signal(
                    getattr(opportunity, "signal", "")
                )
            ]
        )

        if best_score >= 80:
            status = "success"
        elif best_score >= 60:
            status = "info"
        else:
            status = "warning"

        return GuiWorkspacePanel(
            panel_type="top_opportunities",
            title="Top Opportunities",
            subtitle=(
                f"Top {len(visible_opportunities)} live kansen • "
                f"{actionable_count} actionable • "
                "live position sizing actief."
            ),
            items=[
                self._opportunity_item(index, opportunity)
                for index, opportunity in enumerate(
                    visible_opportunities,
                    start=1,
                )
            ],
            status=status,
            metadata={
                "count": len(visible_opportunities),
                "best_score": best_score,
                "actionable_count": actionable_count,
            },
        )

    def _opportunity_item(self, index: int, opportunity) -> dict[str, Any]:
        symbol = getattr(opportunity, "symbol", "Onbekend")
        technical_score = getattr(opportunity, "technical_score", "-")
        signal = getattr(opportunity, "signal", "geen signaal")
        reason = getattr(opportunity, "reason", "")
        price = getattr(opportunity, "price", 0.0)
        sizing = getattr(opportunity, "position_sizing", None)

        signal_label = self._signal_label(signal)
        trend_label = self._trend_label(opportunity)

        return {
            "type": "opportunity",
            "symbol": symbol,
            "rank": index,
            "signal": signal_label,
            "score": technical_score,
            "score_label": self._score_label(technical_score),
            "trend": trend_label,
            "priority": self._priority_label(
                technical_score,
                signal_label,
            ),
            "reason": reason,
            "price": price,
            "position_sizing": sizing,
            "display_text": self._format_opportunity(
                index=index,
                symbol=symbol,
                technical_score=technical_score,
                signal_label=signal_label,
                trend_label=trend_label,
                reason=reason,
                price=price,
                sizing=sizing,
            ),
        }

    def _format_opportunity(
        self,
        index: int,
        symbol: str,
        technical_score,
        signal_label: str,
        trend_label: str,
        reason: str,
        price,
        sizing,
    ) -> str:
        lines = [
            (
                f"{self._rank_medal(index)} {symbol} • "
                f"{self._priority_label(technical_score, signal_label)}"
            ),
            (
                f"{signal_label} • Score {technical_score} / 100 "
                f"• {self._score_label(technical_score)}"
            ),
            f"Aandeelprijs: ${self._format_money(price)} USD",
        ]

        lines.extend(self._position_sizing_lines(sizing))

        lines.extend(
            [
                f"Trend: {trend_label}",
                self._reason_summary(reason),
            ]
        )

        return "\n".join(lines)

    def _position_sizing_lines(self, sizing) -> list[str]:
        if sizing is None:
            return [
                "Aantal aandelen: niet beschikbaar",
                "Budgetstatus: geen handelskapitaal beschikbaar",
            ]

        shares = int(getattr(sizing, "shares", 0))
        investment = getattr(sizing, "investment", 0.0)
        remaining_cash = getattr(sizing, "remaining_cash", 0.0)
        available_cash = getattr(sizing, "available_cash", 0.0)
        available_market_cash = getattr(sizing, "available_market_cash", 0.0)
        account_currency = getattr(sizing, "account_currency", "EUR")
        market_currency = getattr(sizing, "market_currency", "USD")
        fx_rate = getattr(sizing, "fx_rate", 1.0)
        is_affordable = bool(getattr(sizing, "is_affordable", False))

        if not is_affordable:
            return [
                "Aantal aandelen: 0",
                f"Budget: {self._format_currency(available_cash, account_currency)}",
                f"Beschikbaar op beurs: {self._format_currency(available_market_cash, market_currency)}",
                f"Wisselkoers: 1 {account_currency} = {fx_rate:.4f} {market_currency}",
                "Budgetstatus: onvoldoende budget",
            ]

        return [
            f"Aantal aandelen: {shares}",
            f"Investering: {self._format_currency(investment, account_currency)}",
            f"Resterend budget: {self._format_currency(remaining_cash, account_currency)}",
            f"Budget: {self._format_currency(available_cash, account_currency)}",
            f"Beschikbaar op beurs: {self._format_currency(available_market_cash, market_currency)}",
            f"Wisselkoers: 1 {account_currency} = {fx_rate:.4f} {market_currency}",
            "Budgetstatus: binnen budget",
        ]

    def _format_currency(self, value, currency: str) -> str:
        currency = str(currency).strip().upper()
        amount = self._numeric(value)

        if currency == "EUR":
            return f"€{amount:,.2f}"

        if currency == "USD":
            return f"${amount:,.2f}"

        return f"{amount:,.2f} {currency}"

    def _reason_summary(self, reason: str) -> str:
        clean_reason = str(reason or "").strip()

        if not clean_reason:
            return "Setup: geen aanvullende scannerreden beschikbaar."

        parts = [
            part.strip()
            for part in clean_reason.split(".")
            if part.strip()
        ]

        if not parts:
            return f"Setup: {clean_reason}"

        visible = parts[: self.REASON_PREVIEW_LIMIT]
        remaining = max(0, len(parts) - len(visible))

        summary = " | ".join(visible)

        if remaining:
            summary = f"{summary} | +{remaining} meer"

        return f"Setup: {summary}"

    def _rank_medal(self, index: int) -> str:
        if index == 1:
            return "🥇"

        if index == 2:
            return "🥈"

        if index == 3:
            return "🥉"

        return f"#{index}"

    def _score_label(self, score) -> str:
        value = self._numeric(score)

        if value >= 85:
            return "elite setup"

        if value >= 75:
            return "sterk"

        if value >= 65:
            return "interessant"

        if value >= 50:
            return "neutraal"

        return "zwak"

    def _priority_label(self, score, signal_label: str) -> str:
        value = self._numeric(score)

        if signal_label == "BUY" and value >= 80:
            return "HIGH PRIORITY"

        if signal_label == "BUY" and value >= 65:
            return "WATCHLIST"

        if signal_label == "SELL":
            return "AVOID / RISK"

        if value >= 70:
            return "MONITOR"

        return "LOW PRIORITY"

    def _signal_label(self, signal) -> str:
        value = str(signal).strip().upper()

        if value in {"BUY", "LONG", "BULLISH"}:
            return "BUY"

        if value in {"SELL", "SHORT", "BEARISH"}:
            return "SELL"

        if value in {"HOLD", "NEUTRAL"}:
            return "HOLD"

        if value in {"IGNORE", "NONE", "", "GEEN SIGNAAL"}:
            return "Geen signaal"

        return str(signal)

    def _trend_label(self, opportunity) -> str:
        analysis = getattr(opportunity, "analysis", None)

        if analysis is None:
            return "niet beschikbaar"

        trend_score = getattr(analysis, "trend_score", None)

        if trend_score is None:
            return "niet beschikbaar"

        value = self._numeric(trend_score)

        if value >= 75:
            return f"sterk stijgend ({value:.0f}/100)"

        if value >= 60:
            return f"stijgend ({value:.0f}/100)"

        if value >= 40:
            return f"neutraal ({value:.0f}/100)"

        if value >= 25:
            return f"zwak ({value:.0f}/100)"

        return f"dalend / zwak ({value:.0f}/100)"

    def _market_data_status(self, age_seconds: int) -> str:
        if age_seconds <= 20 * 60:
            return "success"

        if age_seconds <= 24 * 60 * 60:
            return "info"

        return "warning"

    def _market_data_subtitle(self, age_seconds: int) -> str:
        if age_seconds <= 20 * 60:
            return "Vrijwel live marktdata."

        if age_seconds <= 24 * 60 * 60:
            return "Marktdata is van vandaag."

        return "Analyse gebruikt oudere marktdata."

    def _data_age_text(self, age_seconds: int) -> str:
        days = age_seconds // 86_400
        hours = (age_seconds % 86_400) // 3_600
        minutes = (age_seconds % 3_600) // 60

        if days > 0:
            return f"{days} dagen, {hours} uur"

        if hours > 0:
            return f"{hours} uur, {minutes} minuten"

        if minutes > 0:
            return f"{minutes} minuten"

        return "minder dan 1 minuut"

    def _normalize_datetime(self, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value

        return value.replace(tzinfo=None)

    def _is_actionable_signal(self, signal) -> bool:
        return self._signal_label(signal) in {"BUY", "SELL"}

    def _percentage(self, value: int, total: int) -> float:
        if total <= 0:
            return 0.0

        return round((value / total) * 100, 1)

    def _numeric(self, value) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def _format_money(self, value) -> str:
        return f"{self._numeric(value):,.2f}"

    def _format_eur(self, value) -> str:
        return f"€{self._numeric(value):,.2f}"

    def _item(self, label: str, value) -> str:
        return f"{label}: {value}"