# PROJECT ORION — STRATEGY INTELLIGENCE AUDIT

## Scope

This audit reviews the deterministic BUY/HOLD/SELL intelligence already present in Orion and defines the safest path toward a more capable strategy engine.

## Active Autonomous Entry Chain

```text
Historical OHLCV
→ IndicatorBuilder
→ IndicatorPack
→ SignalFusionEngine
→ MarketIntelligenceEngine
→ AdaptiveDecisionEngine
→ AdaptiveRiskEngine
→ LivePaperMarketScanner
→ PortfolioAllocator
→ Paper execution
```

## What Orion Already Has

- deterministic indicator construction;
- trend, momentum, RSI and volatility inputs;
- market structure with ATR, support, resistance and swing levels;
- signal fusion with buy and sell pressure;
- market regime and volatility classification;
- adaptive BUY/HOLD/SELL thresholds;
- adaptive stop and three target levels;
- portfolio exposure, cash reserve and position-count limits;
- persisted position lifecycle with break-even, trailing stop and time stop;
- hypothesis evaluation and strategy recommendation components outside the active autonomous decision chain.

## Main Findings

### 1. The active decision is narrower than the repository suggests

The autonomous path primarily decides from trend, momentum, RSI and volatility. Richer analysis services for structure, volume, relative strength, candlesticks and hypotheses exist, but they do not currently form one active and validated strategy contract.

### 2. Multiple decision implementations exist

The repository contains several decision packages and engines. New strategy work must not introduce another competing decision owner. The active pipeline remains authoritative until a replacement is validated in shadow mode.

### 3. Trend semantics are inconsistent

`MarketSignal` documents trend as -1.0 to 1.0, while the active `IndicatorBuilder` calculates latest price divided by a moving average and clamps that result to 0.0 to 1.0. Values above the average therefore collapse to 1.0 and values slightly below the average remain strongly positive. This can make BULL regime detection far too easy. Because correcting it changes active trades, this sprint documents the issue but leaves execution unchanged until benchmark and backtest coverage is added.

### 4. RSI is treated too linearly in the active fusion score

A higher normalized RSI currently contributes more positively to buy pressure. This does not distinguish healthy momentum from extreme overextension. The thesis layer therefore interprets RSI contextually without changing active execution yet.

### 5. HOLD is mostly lifecycle-based

Managed positions are held until deterministic stop or target conditions trigger. The original entry thesis is not yet periodically rebuilt and compared with the current market state.

### 6. Position sizing is capital-limited, not fully risk-budgeted

The allocator limits position value, exposure, open positions and cash reserve. It does not yet size quantity from a fixed portfolio risk budget divided by entry-to-stop distance.

## Chosen First Step: Investment Thesis Shadow Mode

Sprint Strategy S1 adds an `InvestmentThesis` to every `TradingPipelineResult`.

The thesis:

- reuses existing deterministic data;
- exposes weighted factor contributions;
- distinguishes BUY, WATCH and AVOID;
- records supporting reasons and risk reasons;
- records explicit invalidation conditions;
- does not change BUY/HOLD/SELL execution;
- does not mutate `TradingSession`;
- does not size or approve trades.

This allows Orion to collect and compare richer strategy assessments before they are allowed to affect paper execution.

## Next Recommended Steps

1. Persist thesis-at-entry in the trade journal.
2. Rebuild the thesis for every open position on each managed cycle.
3. Produce a deterministic position review: HOLD, TIGHTEN_STOP, PARTIAL_EXIT or FULL_EXIT.
4. Introduce risk-budget position sizing using entry-to-stop distance.
5. Extend backtesting to compare active decisions against shadow-thesis decisions.
6. Promote thesis decisions only after out-of-sample and walk-forward validation.
