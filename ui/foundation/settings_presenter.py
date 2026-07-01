class SettingsPresenter:
    """
    Builds presentation-only settings summaries for the SettingsWorkspace.

    This presenter formats existing configuration and state only. It does not
    load providers, mutate settings, calculate trading logic or access services.
    """

    def create_settings_summary(
        self,
        universe_name: str,
        symbol_count: int,
        max_position_percentage: float,
    ) -> str:
        return f"""
        <div style="background:#1f2937; border-radius:16px; padding:24px;">
            <h2>Actieve instellingen</h2>
            <p><b>Universe:</b> {universe_name}</p>
            <p><b>Aantal symbols:</b> {symbol_count}</p>
            <p><b>Max positiegrootte:</b> {max_position_percentage * 100:.0f}% van cash</p>
            <p><b>Handelsstijl:</b> Swing trades van enkele uren tot enkele dagen.</p>
        </div>
        """