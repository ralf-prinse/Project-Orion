from core.explainability import (
    ExplanationItem,
    ExplanationReport,
    ExplanationSeverity,
)


def test_explanation_item_stores_structured_information():
    item = ExplanationItem(
        code="TREND_001",
        category="trend",
        severity=ExplanationSeverity.INFO,
        title="Trend Strength",
        message="Trend score exceeds threshold.",
        current_value=82,
        threshold=75,
        passed=True,
    )

    assert item.code == "TREND_001"
    assert item.category == "trend"
    assert item.severity == ExplanationSeverity.INFO
    assert item.current_value == 82
    assert item.threshold == 75
    assert item.passed is True


def test_explanation_report_groups_items_by_severity():
    report = ExplanationReport()

    report.add_item(
        ExplanationItem(
            code="INFO_001",
            category="test",
            severity=ExplanationSeverity.INFO,
            title="Info",
            message="Info message.",
        )
    )

    report.add_item(
        ExplanationItem(
            code="WARN_001",
            category="test",
            severity=ExplanationSeverity.WARNING,
            title="Warning",
            message="Warning message.",
        )
    )

    report.add_item(
        ExplanationItem(
            code="BLOCK_001",
            category="test",
            severity=ExplanationSeverity.BLOCKER,
            title="Blocker",
            message="Blocker message.",
        )
    )

    assert len(report.infos()) == 1
    assert len(report.warnings()) == 1
    assert len(report.blockers()) == 1
    assert report.has_blockers() is True


def test_explanation_report_has_no_blockers_by_default():
    report = ExplanationReport()

    assert report.items == []
    assert report.has_blockers() is False