from services.orchestration.backtest_engine import BacktestEngine
from services.orchestration.backtest_visualizer import BacktestVisualizer
from services.intelligence.intelligence_models import IndicatorPack


class FakePortfolio:
    cash = 10000
    position_size = 0
    exposure = 0


def run():
    print("START TEST")

    dataset = [
        [
            IndicatorPack("TSLA", rsi=72, trend=0.6, volatility=0.25, momentum=68),
            IndicatorPack("AAPL", rsi=60, trend=0.3, volatility=0.35, momentum=55),
        ],
        [
            IndicatorPack("TSLA", rsi=75, trend=0.7, volatility=0.22, momentum=72),
            IndicatorPack("AAPL", rsi=52, trend=0.1, volatility=0.40, momentum=48),
        ],
        [
            IndicatorPack("TSLA", rsi=58, trend=0.2, volatility=0.45, momentum=50),
            IndicatorPack("AAPL", rsi=80, trend=0.65, volatility=0.20, momentum=75),
        ],
    ]

    backtest = BacktestEngine()
    visualizer = BacktestVisualizer()

    result = backtest.run(dataset, FakePortfolio())

    print("\nRAW BACKTEST RESULT")
    print(result)

    equity_curve = visualizer.build_equity_curve(result)
    summary = visualizer.build_trade_summary(result)

    print("\n📈 EQUITY CURVE DATA")
    for point in equity_curve["points"]:
        print(point)

    print("\n📊 TRADE SUMMARY")
    for key, value in summary.items():
        print(f"{key}: {value}")

    print("\n📒 TRADE LOG")
    for trade in result["trade_log"]:
        print(trade)

    print("\n🏁 FINAL EQUITY")
    print(equity_curve["final_equity"])

    print("\nEND TEST")


if __name__ == "__main__":
    run()