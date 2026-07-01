from ui.workspace.models import WorkspaceToolbarAction


class WorkspaceToolbar:
    """
    Deterministic toolbar model builder for the desktop shell.
    """

    def default_actions(self) -> list[WorkspaceToolbarAction]:
        return [
            WorkspaceToolbarAction("run_scan", "Run Scan", "▶", order=10),
            WorkspaceToolbarAction("open_watchlist", "Watchlist", "★", order=20),
            WorkspaceToolbarAction("open_settings", "Settings", "⚙", order=90),
        ]

    def ordered_actions(self, actions: list[WorkspaceToolbarAction] | None = None) -> list[WorkspaceToolbarAction]:
        source = actions if actions is not None else self.default_actions()
        return sorted((action for action in source if action.enabled), key=lambda action: action.order)
