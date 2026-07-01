from core.explainability import ExplanationItem, ExplanationReport, ExplanationSeverity
from services.ai import AIExplanationContext, AIExplanationEngine
from services.decisions.models import DecisionAction, DecisionResult, PositionSizingResult
from services.performance.models import PerformanceResult
from services.planner.models import TradePlanResult


def test_engine_returns_invalid_result_without_sources():
    engine = AIExplanationEngine()

    result = engine.explain(AIExplanationContext(symbol="AAPL"))

    assert result.valid_explanation is False
    assert result.source_count == 0
    assert "geen deterministische bronresultaten" in result.summary.lower()
    assert result.warnings


def test_engine_explains_decision_result():
    decision = DecisionResult(
        symbol="AAPL",
        action=DecisionAction.BUY,
        confidence=82,
        risk_level=25,
        position_sizing=PositionSizingResult(
            recommended_shares=10,
            position_value=1500.0,
        ),
        reasons=["Signal validation passed."],
    )
    engine = AIExplanationEngine()

    result = engine.explain(
        AIExplanationContext(symbol="AAPL", decision_result=decision)
    )

    assert result.valid_explanation is True
    assert result.source_count == 1
    assert result.sections[0].title == "Decision explanation"
    assert any("BUY" in bullet for bullet in result.sections[0].bullets)
    assert any("10 aandelen" in bullet for bullet in result.sections[0].bullets)
    assert "AI neemt geen investeringsbeslissing" in result.summary


def test_engine_explains_trade_plan_result():
    trade_plan = TradePlanResult(
        symbol="MSFT",
        valid_plan=True,
        entry_price=100.0,
        stop_loss=95.0,
        target_price=110.0,
        shares=20,
        position_value=2000.0,
        reward_risk_ratio=2.0,
    )
    engine = AIExplanationEngine()

    result = engine.explain(AIExplanationContext(trade_plan_result=trade_plan))

    assert result.symbol == "MSFT"
    assert any(section.title == "Trade plan explanation" for section in result.sections)
    trade_section = next(section for section in result.sections if section.title == "Trade plan explanation")
    assert any("Entry: 100.0" in bullet for bullet in trade_section.bullets)
    assert any("Reward/risk: 2.0" in bullet for bullet in trade_section.bullets)


def test_engine_explains_performance_result():
    performance = PerformanceResult(
        label="Backtest AAPL",
        valid_analysis=True,
        total_trades=10,
        win_rate=60.0,
        net_pnl=1250.0,
        profit_factor=1.8,
        max_drawdown_pct=7.5,
        expectancy=125.0,
    )
    engine = AIExplanationEngine()

    result = engine.explain(AIExplanationContext(performance_result=performance))

    performance_section = next(section for section in result.sections if section.title == "Performance explanation")
    assert any("Aantal trades: 10" in bullet for bullet in performance_section.bullets)
    assert any("Profit factor: 1.8" in bullet for bullet in performance_section.bullets)


def test_engine_explains_structured_explainability_report():
    report = ExplanationReport()
    report.add_item(
        ExplanationItem(
            code="RISK_BLOCKER",
            category="risk",
            severity=ExplanationSeverity.BLOCKER,
            title="Risk blocked",
            message="Trade exceeds maximum allowed risk.",
        )
    )
    engine = AIExplanationEngine()

    result = engine.explain(AIExplanationContext(explanation_report=report))

    section = next(section for section in result.sections if section.title == "Structured explainability")
    assert any("BLOCKER" in bullet for bullet in section.bullets)
    assert "Explainability report bevat" in result.warnings[0]


def test_engine_combines_multiple_sources():
    decision = DecisionResult(symbol="NVDA", action=DecisionAction.WATCH, confidence=70)
    trade_plan = TradePlanResult(symbol="NVDA", valid_plan=True, entry_price=50.0)
    performance = PerformanceResult(total_trades=3, win_rate=66.67)
    engine = AIExplanationEngine()

    result = engine.explain(
        AIExplanationContext(
            decision_result=decision,
            trade_plan_result=trade_plan,
            performance_result=performance,
        )
    )

    assert result.symbol == "NVDA"
    assert result.source_count == 3
    assert len(result.sections) == 3
    assert "3 bronresulta" in result.summary
