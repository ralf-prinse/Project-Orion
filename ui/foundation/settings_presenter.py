from ui.foundation.models import GuiMetric, GuiSection


class SettingsPresenter:
    """
    Builds presentation-only settings sections for the SettingsWorkspace.

    This presenter formats existing configuration and state only. It does not
    load providers, mutate settings, calculate trading logic or access services.
    """

    def create_sections(
        self,
        universe_name: str,
        symbol_count: int,
        max_position_percentage: float,
    ) -> list[GuiSection]:
        return [
            GuiSection(
                title="Actieve instellingen",
                description="Overzicht van de huidige applicatieconfiguratie.",
                metrics=[
                    GuiMetric(
                        label="Universe",
                        value=universe_name,
                        helper_text="De actieve aandelen-universe voor scans.",
                    ),
                    GuiMetric(
                        label="Aantal symbols",
                        value=str(symbol_count),
                        helper_text="Aantal symbols dat beschikbaar is binnen deze universe.",
                    ),
                    GuiMetric(
                        label="Max positiegrootte",
                        value=f"{max_position_percentage * 100:.0f}% van cash",
                        helper_text="Maximale positiegrootte per trade.",
                    ),
                    GuiMetric(
                        label="Handelsstijl",
                        value="Swing trading",
                        helper_text="Trades van enkele uren tot enkele dagen.",
                    ),
                ],
            ),
            GuiSection(
                title="Applicatie",
                description="Project Orion draait in deterministische desktopmodus.",
                metrics=[
                    GuiMetric(
                        label="Architectuur",
                        value="Presenter Architecture",
                        helper_text="Services leveren data, presenters maken GuiSections.",
                    ),
                    GuiMetric(
                        label="AI",
                        value="Explanation-only",
                        helper_text="AI verklaart deterministische uitkomsten maar neemt geen beslissingen.",
                    ),
                ],
            ),
        ]