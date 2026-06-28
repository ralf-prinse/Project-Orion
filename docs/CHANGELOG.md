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