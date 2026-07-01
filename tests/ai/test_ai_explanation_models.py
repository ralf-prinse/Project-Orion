from core.explainability import ExplanationItem, ExplanationReport, ExplanationSeverity
from services.ai.models import AIExplanationContext, AIExplanationResult
from services.planner.models import TradePlanResult


def test_context_resolves_explicit_symbol_first():
    context = AIExplanationContext(symbol=" aapl ")

    assert context.resolved_symbol() == "AAPL"


def test_context_resolves_symbol_from_trade_plan():
    trade_plan = TradePlanResult(symbol="msft")
    context = AIExplanationContext(trade_plan_result=trade_plan)

    assert context.resolved_symbol() == "MSFT"


def test_context_returns_unknown_without_symbol_source():
    context = AIExplanationContext()

    assert context.resolved_symbol() == "UNKNOWN"


def test_result_add_section_skips_empty_bullets():
    result = AIExplanationResult()

    result.add_section("Empty", ["", "   "])

    assert result.sections == []


def test_result_add_section_keeps_clean_bullets():
    result = AIExplanationResult()

    result.add_section("Decision", ["Beslissing: BUY."])

    assert len(result.sections) == 1
    assert result.sections[0].title == "Decision"
    assert result.sections[0].bullets == ["Beslissing: BUY."]


def test_explanation_report_can_be_used_as_source():
    report = ExplanationReport()
    report.add_item(
        ExplanationItem(
            code="TEST",
            category="unit",
            severity=ExplanationSeverity.INFO,
            title="Test item",
            message="Deterministic explanation item.",
        )
    )

    context = AIExplanationContext(explanation_report=report)

    assert context.explanation_report.items[0].code == "TEST"
