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