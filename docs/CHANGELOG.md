# PROJECT ORION

## v0.9.8-alpha

### Added

* Added GUI Scanner Dashboard Integration.
* Added `ScannerPresenter` for display-only scanner dashboard sections.
* Extended `DashboardComposer` with scanner result support.
* Extended `GuiShell` with `build_scanner_dashboard()`.
* Updated GUI application version to `v0.9.8-alpha`.
* Added dedicated scanner presenter and integration unit tests.

### Architecture

Sprint 9.8 connects scanner outputs to the Professional GUI Foundation without introducing scanner, market-data, ranking or analysis logic into the GUI.

The GUI receives completed scanner result objects and projects them into `GuiSection` and `GuiMetric` view models. The presenter uses presentation-safe access so importing GUI modules does not instantiate market-data providers or external data dependencies.

This preserves provider independence and keeps the GUI strictly display-only while preparing Orion for a professional scanner dashboard and top-opportunities workflow.

### Validation

Successfully validated through:

* `tests/ui`
* `tests`

195 tests passed.

No regressions introduced in the official `tests` regression suite.

---

## v0.9.7-alpha

### Added

* Added Unified GUI Dashboard Composition.
* Added `DashboardComposer` for combining deterministic GUI sections from multiple result types.
* Extended `GuiShell` with `build_unified_dashboard()`.
* Updated GUI application version to `v0.9.7-alpha`.
* Added dedicated dashboard composer unit tests.

### Architecture

Sprint 9.7 introduces a display-only dashboard composition layer inside the Professional GUI Foundation.

The composer combines already completed deterministic outputs such as `PerformanceResult`, `PaperTradingResult`, `TradePlanResult` and `AIExplanationResult` into one unified dashboard view. It delegates formatting to existing presenters and does not calculate performance, execute paper trades, plan trades, explain decisions, generate signals or make investment decisions.

This prepares Orion for a professional desktop workflow where multiple engine outputs can be presented together while preserving strict separation between deterministic services and GUI presentation.

### Validation

Successfully validated through:

* `tests/ui`
* `tests`

190 tests passed.

No regressions introduced in the official `tests` regression suite.

---

## v0.9.6-alpha

### Added

* Added GUI Trade Planner Integration.
* Added `TradePlanPresenter` for display-only trade plan dashboard sections.
* Extended `GuiPage` and `NavigationRegistry` with a Trade Planner page.
* Extended `GuiShell` with `build_trade_plan_dashboard()`.
* Updated GUI application version to `v0.9.6-alpha`.
* Added dedicated trade plan presenter unit tests.

### Architecture

Sprint 9.6 connects the Trade Planner to the Professional GUI Foundation without introducing planning logic into the GUI.

The GUI receives completed `TradePlanResult` objects from the deterministic Trade Planner and projects them into display-only `GuiSection` and `GuiMetric` view models. The GUI does not calculate entries, stops, targets, reward/risk ratios, position sizes, risk approval, portfolio state or investment decisions.

This preserves the boundary between deterministic engines and presentation: services produce results, presenters format results, and the GUI shell displays them.

### Validation

Successfully validated through:

* `tests/ui`
* `tests`

186 tests passed.

No regressions introduced in the official `tests` regression suite.

---

## v0.9.5-alpha

### Added

* Added GUI Paper Trading Integration.
* Added `PaperTradingPresenter` for display-only paper trading dashboard sections.
* Extended `GuiShell` with `build_paper_trading_dashboard()`.
* Updated GUI application version to `v0.9.5-alpha`.
* Added dedicated paper trading presenter unit tests.

### Architecture

Sprint 9.5 connects the Paper Trading Engine to the Professional GUI Foundation without introducing execution logic into the GUI.

The GUI receives completed `PaperTradingResult` objects from the deterministic Paper Trading Engine and projects them into display-only `GuiSection` and `GuiMetric` view models. The GUI does not execute trades, mutate paper accounts, simulate fills, calculate signals, change portfolio state or make investment decisions.

This preserves the boundary between deterministic engines and presentation: services produce results, presenters format results, and the GUI shell displays them.

### Validation

Successfully validated through:

* `tests/ui`
* `tests`

181 tests passed.

No regressions introduced in the official `tests` regression suite.

---

## v0.9.4-alpha

### Added

* Added GUI Performance Dashboard Integration.
* Added `PerformanceDashboardPresenter` for dashboard-ready performance sections.
* Extended `GuiShell` with `build_performance_dashboard()`.
* Updated GUI application version to `v0.9.4-alpha`.
* Added dedicated performance dashboard presenter unit tests.

### Architecture

Sprint 9.4 connects Performance Analytics to the Professional GUI Foundation without introducing calculations into the GUI.

The GUI receives completed `PerformanceResult` objects from the deterministic Performance Analytics layer and projects them into display-only `GuiSection` and `GuiMetric` view models. The GUI does not calculate win rate, profit factor, expectancy, drawdown, portfolio state, risk approval or trading decisions.

This preserves the boundary between deterministic engines and presentation: services calculate results, presenters format results, and the GUI shell displays them.

### Validation

Successfully validated through:

* `tests/ui`
* `tests`

177 tests passed.

No regressions introduced in the official `tests` regression suite.

---

## v0.9.3-alpha

### Added

* Added GUI Explanation Integration.
* Added `ExplanationPresenter` for display-only AI explanation sections.
* Extended `GuiShell` with `build_explanation()`.
* Updated GUI application version to `v0.9.3-alpha`.
* Added dedicated GUI explanation presenter unit tests.

### Architecture

Sprint 9.3 connects the AI Explanation Layer to the Professional GUI Foundation without introducing trading logic into the GUI.

The GUI receives existing `AIExplanationResult` objects and projects them into deterministic `GuiSection` and `GuiMetric` view models. It does not call external AI providers, make investment decisions, calculate signals, size positions, approve risk, mutate portfolios or generate trade plans.

This keeps the architectural boundary intact: deterministic engines produce results, the AI Explanation Layer explains those results, and the GUI displays them.

### Validation

Successfully validated through:

* `tests/ui`
* `tests`

173 tests passed.

No regressions introduced in the official `tests` regression suite.

---

## v0.9.2-alpha

### Added

* Added `services/ai` package.
* Added AI Explanation Layer Foundation.
* Added `AIExplanationContext`.
* Added `AIExplanationConfig`.
* Added `AIExplanationResult`.
* Added `AIExplanationSection`.
* Added `ExplanationAudience`.
* Added `AIExplanationEngine`.
* Added `AIExplanationRegistry`.
* Added `BaseAIExplanationAnalyzer`.
* Added deterministic explanation analyzers for decisions, trade plans, performance analytics and structured explainability reports.
* Added dedicated AI Explanation Layer unit tests.

### Architecture

Sprint 9.2 introduces the foundation for Orion's AI Explanation Layer.

The layer does not make investment decisions, generate signals, calculate position sizes, approve risk, mutate portfolios, execute trades or call an external AI model. Instead, it converts existing deterministic Orion outputs into structured, reproducible explanation sections and summaries that are safe for GUI display, reporting and future LLM-based natural-language summarisation.

The AI Explanation Layer follows the same registry-driven architecture as the earlier expandable processing layers and uses `AnalyzerRunner` for deterministic orchestration.

### Validation

Successfully validated through:

* `tests/ai`
* `tests`

169 tests passed.

No regressions introduced in the official `tests` regression suite.

---

## v0.9.1-alpha

### Added

* Added Professional Desktop GUI Foundation.
* Added toolkit-independent GUI foundation package in `ui/foundation`.
* Added `GuiPage`, `GuiNavigationItem`, `GuiMetric`, `GuiSection`, `GuiApplicationConfig` and `GuiShellState`.
* Added deterministic `NavigationRegistry`.
* Added `GuiShell` for presentation state and navigation orchestration.
* Added `DashboardPresenter` for display-only dashboard sections.
* Added `PerformancePresenter` for display-only performance analytics sections.
* Added dedicated GUI foundation unit tests.

### Architecture

Sprint 9.1 introduces the professional GUI foundation without placing trading logic inside the GUI layer.

The new GUI foundation is intentionally toolkit-independent. PySide6 screens can consume the shell, navigation registry and presenters later, while deterministic market analysis, signal generation, decision making, portfolio management, risk management, backtesting, paper trading and performance calculations remain inside their own service layers.

The GUI layer formats and presents deterministic outputs only.

### Validation

Successfully validated through:

* `tests/ui`
* `tests`

155 tests passed.

No regressions introduced in the official `tests` regression suite.

## v0.9.0-alpha

### Added

* Added `services/performance` package.
* Added `PerformanceTrade`.
* Added `EquityCurvePoint`.
* Added `PerformanceConfig`.
* Added `PerformanceContext`.
* Added `PerformanceResult`.
* Added `PerformanceEngine`.
* Added `PerformanceRegistry`.
* Added `BasePerformanceAnalyzer`.
* Added `InputValidationAnalyzer`.
* Added `TradeMetricsAnalyzer`.
* Added `EquityCurveAnalyzer`.
* Added adapters for `BacktestResult` and closed `PaperAccount` trades.
* Added dedicated Performance Analytics unit tests.

### Architecture

Sprint 9.0 introduces a dedicated registry-driven Performance Analytics layer.

The Performance Analytics layer consumes already completed or simulated trade results and calculates professional deterministic metrics such as win rate, loss rate, gross profit, gross loss, net P/L, average win, average loss, expectancy, profit factor, payoff ratio, equity curve, total return and maximum drawdown.

The layer is intentionally separated from Backtesting and Paper Trading. Backtesting simulates historical execution, Paper Trading simulates forward virtual execution and Performance Analytics evaluates the results. It does not generate signals, make decisions, mutate portfolios, approve risk, create trade plans, execute broker orders or use AI reasoning.

### Validation

Successfully validated through:

* `tests/performance`
* `tests`

141 tests passed.

No regressions introduced in the official `tests` regression suite.

---

## v0.8.9-alpha

### Added

* Added `services/paper_trading` package.
* Added `PaperAccount`.
* Added `PaperPosition`.
* Added `PaperTradeRecord`.
* Added `PaperTradingConfig`.
* Added `PaperTradingContext`.
* Added `PaperTradingResult`.
* Added `PaperTradingEngine`.
* Added `PaperTradingRegistry`.
* Added `BasePaperTradingAnalyzer`.
* Added `InputValidationAnalyzer`.
* Added `TradeExecutionAnalyzer`.
* Added `MarkToMarketAnalyzer`.
* Added `PositionCloseAnalyzer`.
* Added `AccountSummaryAnalyzer`.
* Added dedicated Paper Trading unit tests.

### Architecture

Sprint 8.9 introduces a dedicated registry-driven Paper Trading Engine.

The Paper Trading Layer consumes existing deterministic `TradePlanResult` objects and applies them to a virtual cash account. It can open simulated BUY positions, update open positions with market prices, close positions deterministically and report cash, equity, realized P/L, unrealized P/L and open position count.

The Paper Trading Engine does not perform technical analysis, generate signals, make investment decisions, calculate position sizing, approve risk, backtest historical candles, route broker orders or use AI reasoning. It is a simulation layer that prepares Orion for performance analytics, GUI workflows and future broker integration.

### Validation

Successfully validated through:

* `tests/paper_trading`
* `tests`

128 tests passed.

No regressions introduced in the official `tests` regression suite.

---

## v0.8.8-alpha

### Added

* Added `services/backtesting` package.
* Added `BacktestCandle`.
* Added `BacktestConfig`.
* Added `BacktestContext`.
* Added `BacktestTrade`.
* Added `BacktestResult`.
* Added `BacktestEngine`.
* Added `BacktestRegistry`.
* Added `BaseBacktestAnalyzer`.
* Added `TradeSimulator`.
* Added `InputValidationAnalyzer`.
* Added `TradeSimulationAnalyzer`.
* Added `PerformanceSummaryAnalyzer`.
* Added dedicated Backtesting unit tests.

### Architecture

Sprint 8.8 introduces a dedicated registry-driven Backtesting Foundation.

The Backtesting Layer simulates existing deterministic `TradePlanResult` objects over historical candles. This keeps the layer focused on simulation and performance measurement, while preserving the separation between analysis, signals, decisions, position sizing, portfolio management, risk management and trade planning.

The default same-candle behaviour is conservative: when stop-loss and target are both reached within the same candle, the stop-loss is assumed to trigger first. This prevents optimistic assumptions when simulating trades on daily OHLC data.

### Validation

Successfully validated through:

* `tests/backtesting`
* `tests`

113 tests passed.

No regressions introduced in the official `tests` regression suite.

---

## v0.8.7-alpha

### Added

* Added `services/planner` package.
* Added `TradePlanContext` model.
* Added `TradePlannerConfig` model.
* Added `TradePlanResult` model.
* Added `TradePlanner`.
* Added `TradePlanRegistry`.
* Added `BaseTradePlanAnalyzer`.
* Added `InputValidationAnalyzer`.
* Added `TargetPriceAnalyzer`.
* Added `RiskRewardAnalyzer`.
* Added `TradePlanSummaryAnalyzer`.
* Added dedicated Trade Planner unit tests.

### Architecture

Sprint 8.7 introduces a dedicated registry-driven Trade Planner.

The Trade Planner transforms approved deterministic inputs into an executable trade plan with entry price, stop-loss, target price, share quantity, position value and reward/risk metrics.

The Trade Planner does not perform technical analysis, generate signals, make investment decisions, manage portfolio state, calculate position sizing or approve risk. It consumes outputs from earlier layers and prepares structured trade-plan output for GUI, reporting, paper trading and future broker integration.

### Validation

Successfully validated through:

* `tests/planner`
* `tests`

98 tests passed.

No regressions introduced in the official `tests` regression suite.

---

## v0.8.6-alpha

### Added

* Added `services/risk` package.
* Added `RiskProfile` model.
* Added `RiskContext` model.
* Added `RiskResult` model.
* Added `RiskManager`.
* Added `RiskRegistry`.
* Added `BaseRiskAnalyzer`.
* Added `RiskSummaryAnalyzer`.
* Added `TradeRiskAnalyzer`.
* Added `PortfolioRiskAnalyzer`.
* Added `DrawdownAnalyzer`.
* Added `CapitalProtectionAnalyzer`.
* Added `PositionExposureRiskAnalyzer`.
* Added dedicated Risk Manager unit tests.

### Architecture

Sprint 8.6 introduces a dedicated registry-driven Risk Manager.

The Risk Manager validates proposed trade risk, total portfolio risk, drawdown, minimum cash reserve and position exposure while remaining separate from technical analysis, signal generation, decision assembly, portfolio management, position sizing and trade planning.

The new `RiskResult` model prepares Orion for future integration with the Decision Layer, Portfolio Engine, Trade Planner, GUI, reporting and AI explanation layer.

### Validation

Successfully validated through:

* `tests/risk`
* `tests`

86 tests passed.

No regressions introduced in the official `tests` regression suite.

---

## v0.8.3.3-alpha

### Added

* Added core Explainability Framework.
* Added `ExplanationItem`.
* Added `ExplanationSeverity`.
* Added `ExplanationReport`.
* Added dedicated explainability unit tests.

### Architecture

Project Orion now has a reusable explainability foundation that can be used by:

* Analysis Layer
* Signal Layer
* Decision Layer
* Risk Manager
* Portfolio Engine
* GUI
* Artificial Intelligence Layer

This prepares Orion for structured explanations, audit trails, backtesting diagnostics and future AI-generated summaries.

### Validation

Successfully validated through:

* `tests/core`

5 core tests passed.

No regressions introduced.

---

## v0.8.3.2-alpha

### Added

* Added `PortfolioValidationAnalyzer`.
* Added `RiskValidationAnalyzer`.
* Extended `DecisionRegistry`.
* Added portfolio validation tests.
* Added risk validation tests.

### Changed

* Decision Layer now validates portfolio capacity before assembling a final decision.
* Decision Layer now validates basic risk context before assembling a final decision.
* `DecisionAssemblerAnalyzer` now respects portfolio and risk blockers.

### Architecture

The Decision Layer now follows a validation pipeline:

* SignalValidationAnalyzer
* PortfolioValidationAnalyzer
* RiskValidationAnalyzer
* DecisionAssemblerAnalyzer

This prepares Orion for future portfolio management, risk management and position sizing.

### Validation

Successfully validated through:

* `tests/decisions`

11 decision tests passed.

No regressions introduced.

---

## v0.8.3.1-alpha

### Added

* Added Decision Layer foundation.
* Added `DecisionAction`.
* Added `DecisionContext`.
* Added `DecisionState`.
* Added `DecisionResult`.
* Added `BaseDecisionAnalyzer`.
* Added `SignalValidationAnalyzer`.
* Added `DecisionAssemblerAnalyzer`.
* Added `DecisionRegistry`.
* Added `DecisionEngine`.

### Architecture

Project Orion now contains a modular Decision Layer.

The Decision Layer converts `SignalResult` and `DecisionContext` into deterministic `DecisionResult` objects.

The layer follows the same registry-driven architecture as the Analysis Layer and Signal Layer.

### Validation

Successfully validated through:

* `tests/decisions`

9 decision tests passed.

No regressions introduced.

---

## v0.8.2.1-alpha

### Added

* Added `AnalyzerRunner` as a reusable orchestration component.
* Added generic registry execution infrastructure.
* Added dedicated unit tests for `AnalyzerRunner`.

### Changed

* `SignalEngine` now delegates analyzer execution to `AnalyzerRunner`.
* `AnalysisEngine` now delegates analyzer execution to `AnalyzerRunner`.
* Removed duplicated orchestration logic from both engines.
* Preserved deterministic execution order and backwards compatibility.

### Architecture

Project Orion now shares a common orchestration layer for registry-driven engines.

Current registry-driven engines:

* AnalysisEngine
* SignalEngine

Future engines such as `DecisionEngine` can reuse the same orchestration infrastructure without duplicating code.

### Validation

Successfully validated through:

* `tests/core`
* `tests/analysis`
* `tests/signals`

42 tests passed.

No regressions introduced.

---

## v0.8.2-alpha

### Added

* Added complete Signal Layer foundation.
* Added `SignalEngine`.
* Added `SignalRegistry`.
* Added `SignalAnalyzerDefinition`.
* Added `BaseSignalAnalyzer`.
* Added `EntrySignalAnalyzer`.
* Added `SignalResult`.
* Added `Signal` enum.
* Added configurable signal thresholds.
* Added dedicated Signal Layer unit tests.

### Changed

* Introduced deterministic signal generation based on `AnalysisResult`.
* Added registry-driven signal execution.
* Centralised signal thresholds into a dedicated configuration module.
* Prepared the architecture for future trading strategies and backtesting.

### Architecture

Project Orion now contains three modular processing layers:

* Indicator Layer
* Analysis Layer
* Signal Layer

The Signal Layer follows the same architectural principles as the Analysis Layer:

* Registry-driven
* Modular analyzers
* Deterministic behaviour
* Single Responsibility
* Fully testable

### Validation

Successfully validated through:

* `test_signal_engine.py`
* `test_signal_registry.py`
* `test_signal_thresholds.py`

10 Signal Layer tests passed.

No regressions introduced.

---

## v0.8.1.1-alpha

### Added

* Added `AnalyzerRegistry`.
* Added `AnalyzerDefinition`.
* Added deterministic analyzer registration.
* Added registry unit tests.

### Changed

* `AnalysisEngine` now retrieves analyzers from `AnalyzerRegistry`.
* Analyzer execution is now registry-driven instead of hardcoded.
* Overall score calculation now iterates over registered analyzers.
* Raw candle data is automatically passed only to analyzers that require it.

### Architecture

The Analysis Layer now uses a central Analyzer Registry.

Future analyzers can be added by registering them instead of modifying `AnalysisEngine`.

This further reduces coupling and keeps `AnalysisEngine` focused exclusively on orchestration.

### Validation

Successfully validated through:

* `test_analyzer_registry.py`
* `test_analysis_engine.py`
* Complete Analysis Layer regression tests

30 analysis tests passed.

No regressions introduced.

## v0.8.1-alpha

### Added

* Added `CandlestickPatternAnalyzer` to the modular Analysis Layer.
* Added `candlestick_score` to `AnalysisResult`.
* Added deterministic candlestick pattern detection.
* Added unit tests for `CandlestickPatternAnalyzer`.

### Supported Patterns

Bullish

* Hammer
* Bullish Engulfing
* Piercing Line

Bearish

* Shooting Star
* Bearish Engulfing
* Dark Cloud Cover

### Changed

* `AnalysisEngine` now orchestrates eight specialised analyzers.
* `CandlestickPatternAnalyzer` receives raw candle data directly.
* Analysis score weighting now includes candlestick analysis.

### Architecture

The Analysis Layer now distinguishes between:

* Technical indicators
* Market structure
* Relative strength
* Price action

Candlestick pattern recognition is intentionally separated from the IndicatorEngine because candlestick analysis is based on raw price action rather than derived technical indicators.

### Validation

Successfully validated through:

* `test_analysis_engine.py`
* `test_candlestick_pattern_analyzer.py`
* Complete Analysis Layer regression tests
* Manual Scan Pipeline validation

No regressions were introduced.

## v0.8.0-alpha

### Added

* Added `RelativeStrengthAnalyzer` to the modular Analysis Layer.
* Added `relative_strength_score` to `AnalysisResult`.
* Added benchmark support to `IndicatorEngine`.
* Added SPY benchmark integration to `TechnicalScanner`.
* Added configurable analysis weights (`analysis_weights.py`).
* Added unit tests for `RelativeStrengthAnalyzer`.
* Added unit tests for benchmark calculations inside `IndicatorEngine`.

### Changed

* `AnalysisEngine` now orchestrates seven specialised analyzers:

  * TrendAnalyzer
  * MomentumAnalyzer
  * VolatilityAnalyzer
  * StructureAnalyzer
  * VolumeAnalyzer
  * MarketRegimeAnalyzer
  * RelativeStrengthAnalyzer

* `IndicatorEngine.calculate()` now supports optional `benchmark_candles`.
* Relative Strength is now incorporated into the overall technical score.
* Score weights have been centralized in a dedicated configuration module.

### Architecture

The Analysis Layer now distinguishes between:

* Technical quality scoring
* Market context
* Relative market performance

MarketRegimeAnalyzer remains excluded from the overall score because it provides market context rather than technical quality.

RelativeStrengthAnalyzer becomes a first-class technical component within the Analysis Layer.

### Validation

Successfully validated through:

* `test_analysis_engine.py`
* `test_market_regime_analyzer.py`
* `test_relative_strength_analyzer.py`
* `test_indicator_engine_relative_strength.py`
* Complete Analysis Layer regression tests
* Manual Scan Pipeline validation

No regressions were introduced.

## v0.7.9-alpha

### Added

* Added `MarketRegimeAnalyzer` to the modular Analysis Layer.
* Added `market_regime_score` to `AnalysisResult`.
* Added `test_market_regime_analyzer.py`.
* Added `test_analysis_engine.py` integration tests for AnalysisEngine orchestration.

### Changed

* `AnalysisEngine` now orchestrates six specialized analyzers:

  * TrendAnalyzer
  * MomentumAnalyzer
  * VolatilityAnalyzer
  * StructureAnalyzer
  * VolumeAnalyzer
  * MarketRegimeAnalyzer

* `MarketRegimeAnalyzer` provides market context but is intentionally not included in `overall_score` to avoid double counting.

### Architecture

The Analysis Layer now provides both:

* technical quality scoring through `overall_score`
* market context through `market_regime_score`

This prepares Orion for future Signal Engine and Decision Engine logic.

### Validation

Successfully validated through:

* `test_market_regime_analyzer.py`
* `test_analysis_engine.py`
* `tests/analysis`
* manual `test_scan_pipeline.py`

No regressions were introduced.

## v0.7.8-alpha

### Added

* Added `VolumeAnalyzer` to the modular Analysis Layer.
* Extended `IndicatorEngine` with volume-derived metrics:

  * `latest_volume`
  * `average_volume_20`
  * `relative_volume_20`
  * `previous_average_volume_20`
  * `volume_trend_20`
* Added `test_volume_analyzer.py`.

### Changed

* `AnalysisEngine` now orchestrates five specialized analyzers:

  * TrendAnalyzer
  * MomentumAnalyzer
  * VolatilityAnalyzer
  * StructureAnalyzer
  * VolumeAnalyzer
* Added `volume_score` to `AnalysisResult`.
* Updated overall technical score weighting:

  * Trend: **30%**
  * Momentum: **25%**
  * Volatility: **15%**
  * Structure: **15%**
  * Volume: **15%**

### Architecture

The Analysis Layer now consists of:

* IndicatorEngine
* TrendAnalyzer
* MomentumAnalyzer
* VolatilityAnalyzer
* StructureAnalyzer
* VolumeAnalyzer
* AnalysisEngine

This architecture allows new analyzers to be added with minimal impact on existing components.

### Validation

Successfully validated through:

* `test_trend_analyzer.py`
* `test_momentum_analyzer.py`
* `test_volatility_analyzer.py`
* `test_structure_analyzer.py`
* `test_volume_analyzer.py`
* `test_analysis_engine.py`
* `test_scan_pipeline.py`

No regressions were introduced.


* Introduced `BaseAnalyzer` as the common abstract interface for all analyzers.
* Added `StructureAnalyzer` for deterministic market structure analysis.
* Extended `IndicatorEngine` with structure-related values:

  * `latest_close`
  * `recent_high_20`
  * `recent_low_20`
  * `previous_high_20`
  * `previous_low_20`
* Added `test_structure_analyzer.py`.

### Changed

* `AnalysisEngine` now orchestrates four specialized analyzers:

  * TrendAnalyzer
  * MomentumAnalyzer
  * VolatilityAnalyzer
  * StructureAnalyzer
* Overall technical score now includes `structure_score`.
* Updated score weighting:

  * Trend: **35%**
  * Momentum: **30%**
  * Volatility: **20%**
  * Structure: **15%**

### Architecture

The Analysis Layer now follows a fully modular analyzer architecture:

```text
Indicator Engine
        │
        ▼
Trend Analyzer
Momentum Analyzer
Volatility Analyzer
Structure Analyzer
        │
        ▼
Analysis Engine
```

This establishes a standardized framework for future analyzers such as:

* Volume Analyzer
* Relative Strength Analyzer
* Market Regime Analyzer
* Candlestick Pattern Analyzer
* Signal Engine

### Validation

Successfully validated through:

* `test_trend_analyzer.py`
* `test_momentum_analyzer.py`
* `test_volatility_analyzer.py`
* `test_structure_analyzer.py`
* `test_analysis_engine.py`
* `test_scan_pipeline.py`

No regressions were introduced.


## v0.7.6-alpha

Refactored Analysis Layer into dedicated analyzers

Introduced Trend Analyzer

Introduced Momentum Analyzer

Introduced Volatility Analyzer

Analysis Engine now acts primarily as an orchestration layer

Separated trend, momentum and volatility scoring into independent modules

Improved maintainability through Single Responsibility architecture

Added deterministic unit tests for:

* Trend Analyzer
* Momentum Analyzer
* Volatility Analyzer

Validated full Analysis Engine regression tests

Validated complete scanner pipeline after refactoring

No behavioural changes introduced

Scanner results remain fully backwards compatible


## v0.7.5-alpha

Migrated Technical Scanner to Analysis Layer

Removed duplicate indicator calculations from Technical Scanner

Technical Scanner now uses Analysis Engine for all technical scoring

Analysis Engine is now the single source of truth for technical analysis

Integrated AnalysisResult into Technical Scanner

Unified deterministic scanner pipeline

Refactored scanner architecture

Historical Data

↓

Indicator Engine

↓

Analysis Engine

↓

Technical Scanner

↓

Ranking Engine

Improved Analysis Engine regression test

Removed dependency on live Yahoo Finance data for core analysis testing

Validated complete scanner pipeline after migration


## v0.7.4-alpha

Added complete Analysis Layer

Added Indicator Library

Implemented SMA20

Implemented SMA50

Implemented EMA20

Implemented EMA50

Implemented RSI14

Implemented MACD

Implemented ATR14

Implemented Bollinger Bands

Implemented ADX14

Added Analysis Scoring

Trend Score

Momentum Score

Volatility Score

Overall Technical Score

Refactored architecture

Historical Data

↓

Indicator Library

↓

Indicator Engine

↓

Analysis Engine
## v0.8.4-alpha

### Added

* Added `PositionSizingResult` model.
* Added `PositionSizingAnalyzer` to the Decision Layer pipeline.
* Added configurable position sizing inputs to `DecisionContext`:
  * `entry_price`
  * `stop_loss`
  * `risk_per_trade`
  * `max_position_value`
* Added `position_sizing` output to `DecisionState` and `DecisionResult`.
* Added dedicated position sizing unit tests.
* Added Decision Engine integration tests for position sizing.

### Changed

* `DecisionRegistry` now executes `PositionSizingAnalyzer` before `DecisionAssemblerAnalyzer`.
* `DecisionEngine` now carries structured position sizing data into `DecisionResult`.
* `position_size` remains available as a backwards-compatible alias for recommended shares.

### Architecture

Sprint 8.4 introduces deterministic fixed-fractional position sizing while preserving Orion's layered architecture.

`PositionSizingAnalyzer` only enriches `DecisionState`. It does not make investment decisions, manage portfolio state or create trade plans.

The new `PositionSizingResult` model prepares Orion for future Portfolio Engine, Risk Manager and Trade Planner integration.

### Validation

Successfully validated through:

* `tests/decisions`
* `tests`

63 tests passed.

No regressions introduced in the official `tests` regression suite.

## v0.8.5-alpha

### Added

* Added `services/portfolio` package.
* Added `PortfolioState` model.
* Added `PortfolioPosition` model.
* Added `PortfolioContext` model.
* Added `PortfolioResult` model.
* Added `PortfolioEngine`.
* Added `PortfolioRegistry`.
* Added `BasePortfolioAnalyzer`.
* Added `PortfolioSummaryAnalyzer`.
* Added `CashValidationAnalyzer`.
* Added `PositionCountAnalyzer`.
* Added `ExistingPositionAnalyzer`.
* Added `ExposureAnalyzer`.
* Added dedicated Portfolio Engine unit tests.

### Architecture

Sprint 8.5 introduces a dedicated registry-driven Portfolio Engine.

The Portfolio Engine evaluates portfolio state, cash availability, open position count, existing positions and exposure limits while remaining separate from technical analysis, signal generation, decision assembly, position sizing, risk management and trade planning.

The new `PortfolioResult` model prepares Orion for future integration with the Decision Layer, Risk Manager, Trade Planner, GUI and reporting layer.

### Validation

Successfully validated through:

* `tests/portfolio`
* `tests`

73 tests passed.

No regressions introduced in the official `tests` regression suite.

