from __future__ import annotations

from services.opportunity_service import OpportunityService
from services.orchestration.live_scanner_service import (
    LiveScannerService,
)
from ui.foundation.mission_control_presenter import (
    MissionControlPresenter,
)
from ui.workspace.mission_control_workspace import (
    MissionControlWorkspace,
)


class MissionControlController:
    """
    Controller for the Mission Control workspace.

    Responsibilities:
        - coordinate LiveScannerService
        - obtain deterministic scanner snapshots
        - build Mission Control opportunities
        - transform deterministic data into GuiWorkspace models
        - update MissionControlWorkspace

    Does NOT:
        - calculate trading signals
        - calculate indicators
        - execute trades
        - perform AI reasoning

    The controller is strictly orchestration.
    """

    def __init__(
        self,
        workspace: MissionControlWorkspace,
        scanner_service: LiveScannerService | None = None,
        presenter: MissionControlPresenter | None = None,
        opportunity_service: OpportunityService | None = None,
        available_cash_provider=None,
    ) -> None:
        self._workspace = workspace
        self._scanner_service = scanner_service or LiveScannerService()
        self._presenter = presenter or MissionControlPresenter()
        self._opportunity_service = opportunity_service or OpportunityService()
        self._available_cash_provider = available_cash_provider

    @property
    def scanner_service(self) -> LiveScannerService:
        return self._scanner_service

    def initialize(self) -> None:
        workspace = self._presenter.present(
            scanner_snapshot=self._scanner_service.last_snapshot,
            opportunities=(),
        )

        self._workspace.set_workspace(workspace)

    def refresh(self) -> None:
        snapshot = self._scanner_service.scan_once()
        opportunities = self._build_opportunities(snapshot)

        workspace = self._presenter.present(
            scanner_snapshot=snapshot,
            opportunities=opportunities,
        )

        self._workspace.set_workspace(workspace)

    def start(self) -> None:
        snapshot = self._scanner_service.start()
        opportunities = self._build_opportunities(snapshot)

        workspace = self._presenter.present(
            scanner_snapshot=snapshot,
            opportunities=opportunities,
        )

        self._workspace.set_workspace(workspace)

    def stop(self) -> None:
        self._scanner_service.stop()

    def _build_opportunities(self, snapshot) -> tuple:
        return self._opportunity_service.build_opportunities(
            snapshot=snapshot,
            available_cash=self._available_cash(),
        )

    def _available_cash(self) -> float:
        if self._available_cash_provider is None:
            return 0.0

        try:
            return float(self._available_cash_provider())
        except Exception:
            return 0.0