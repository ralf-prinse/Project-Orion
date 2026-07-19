from pathlib import Path

from services.orchestration.trading_pipeline import TradingPipeline
from services.trading_decision import AdaptiveDecisionEngine, PositionSizer


ROOT = Path(__file__).resolve().parents[1]


def test_trading_pipeline_owns_one_canonical_decision_implementation():
    pipeline = TradingPipeline()

    assert isinstance(pipeline.decision_engine, AdaptiveDecisionEngine)
    assert isinstance(pipeline.sizer, PositionSizer)


def test_removed_legacy_decision_and_scanner_paths_do_not_return():
    removed_paths = (
        ROOT / "services" / "decision",
        ROOT / "services" / "scanner_service.py",
        ROOT / "engines",
    )

    assert all(not path.exists() for path in removed_paths)


def test_autonomous_runtime_does_not_activate_learning_or_research_decisions():
    runtime_sources = (
        ROOT / "run_autonomous_ibkr_paper.py",
        ROOT / "services" / "autonomous_paper_trading_runner.py",
        ROOT / "services" / "ibkr" / "ibkr_autonomous_runtime_factory.py",
    )
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in runtime_sources
    )

    assert "services.decisions" not in combined
    assert "LearningPipeline" not in combined
    assert "strategy_recommendation" not in combined
