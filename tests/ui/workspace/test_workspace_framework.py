import pytest

from ui.foundation.gui_shell import GuiShell
from ui.foundation.models import GuiNavigationItem, GuiPage
from ui.workspace import (
    DockManager,
    OrionWorkspace,
    WorkspacePanel,
    WorkspaceRegion,
    WorkspaceSidebar,
    WorkspaceStatusBar,
    WorkspaceToolbar,
)
from ui.workspace.workspace_layout import WorkspaceLayoutFactory


def test_dock_manager_registers_default_workspace_panels():
    manager = DockManager()

    central_panels = manager.panels_for_region(WorkspaceRegion.CENTRAL)
    bottom_panels = manager.panels_for_region(WorkspaceRegion.BOTTOM_DOCK)

    assert central_panels[0].panel_id == "dashboard"
    assert any(panel.panel_id == "scanner" for panel in central_panels)
    assert any(panel.panel_id == "performance" for panel in bottom_panels)


def test_dock_manager_rejects_duplicate_panel_ids():
    panel = WorkspacePanel("dashboard", "Dashboard", GuiPage.DASHBOARD)
    manager = DockManager([panel])

    with pytest.raises(ValueError):
        manager.register(panel)


def test_dock_manager_can_replace_panel_for_tests_and_plugins():
    manager = DockManager([])
    original = WorkspacePanel("custom", "Custom", GuiPage.DASHBOARD)
    replacement = WorkspacePanel("custom", "Custom Updated", GuiPage.SCANNER)

    manager.register(original)
    manager.replace(replacement)

    assert manager.get("custom").title == "Custom Updated"
    assert manager.get("custom").page == GuiPage.SCANNER


def test_workspace_toolbar_returns_enabled_actions_in_order():
    actions = WorkspaceToolbar().ordered_actions()

    assert [action.action_id for action in actions] == [
        "run_scan",
        "open_watchlist",
        "open_settings",
    ]
    assert all(action.enabled for action in actions)


def test_workspace_statusbar_projects_shell_state_without_business_logic():
    shell = GuiShell()
    shell.navigate_to(GuiPage.SCANNER)

    items = WorkspaceStatusBar().from_shell_state(shell.state)

    assert items[0].key == "page"
    assert items[0].value == GuiPage.SCANNER.value
    assert items[1].key == "status"


def test_workspace_sidebar_reuses_navigation_component():
    items = [
        GuiNavigationItem(GuiPage.DASHBOARD, "Dashboard", 10),
        GuiNavigationItem(GuiPage.SCANNER, "Scanner", 20),
    ]

    buttons = WorkspaceSidebar().build_buttons(items, GuiPage.SCANNER)

    assert buttons[0].selected is False
    assert buttons[1].selected is True
    assert buttons[1].icon


def test_workspace_layout_spec_uses_design_system_metrics():
    spec = WorkspaceLayoutFactory().create_default()

    assert spec.sidebar_width > 0
    assert spec.toolbar_height > 0
    assert spec.region_minimum_size(WorkspaceRegion.SIDEBAR)[0] == spec.sidebar_width
    assert spec.region_minimum_size(WorkspaceRegion.CENTRAL)[0] >= 640


def test_orion_workspace_builds_complete_professional_shell_state():
    workspace = OrionWorkspace()

    state = workspace.build_state()

    assert state.current_page == GuiPage.DASHBOARD
    assert state.active_panel_id == "dashboard"
    assert len(state.panels) >= 5
    assert len(state.toolbar_actions) == 3
    assert any(item.key == "status" for item in state.status_items)


def test_orion_workspace_navigation_updates_active_panel():
    workspace = OrionWorkspace()

    state = workspace.navigate_to(GuiPage.SCANNER)

    assert state.current_page == GuiPage.SCANNER
    assert state.active_panel_id == "scanner"
