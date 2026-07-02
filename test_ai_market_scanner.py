from services.orchestration.ai_market_scanner import AIMarketScanner


class FakePortfolio:
    cash = 10000
    position_size = 0
    exposure = 0


def run():
    print("START AI MARKET SCANNER TEST")

    scanner = AIMarketScanner()

    symbols = [
        "MSFT",
        "NVDA",
        "AAPL",
    ]

    result = scanner.scan(
        symbols=symbols,
        portfolio_state=FakePortfolio(),
    )

    print("\nSCAN SUMMARY")
    print("Total requested:", result.total_requested)
    print("Total scanned:", result.total_scanned)
    print("Total failed:", result.total_failed)
    print("Failed symbols:", result.failed_symbols)

    print("\nBEST TRADE")
    if result.best_trade:
        print("Symbol:", result.best_trade.symbol)
        print("Decision:", result.best_trade.decision)
        print("Confidence:", f"{result.best_trade.confidence:.1%}")
        print("Pressure:", f"{result.best_trade.pressure_score:.3f}")
        print("Position:", f"{result.best_trade.position_size:.2f}")
        print("Risk:", f"{result.best_trade.risk_score:.4f}")
    else:
        print("No best trade found.")

    print("\nRANKED RESULTS")
    for index, item in enumerate(result.ranked, start=1):
        print(
            f"{index}. {item.symbol} | "
            f"{item.decision} | "
            f"conf={item.confidence:.1%} | "
            f"pressure={item.pressure_score:.3f} | "
            f"strength={item.strength:.3f} | "
            f"risk={item.risk_score:.4f}"
        )

    print("\nEND AI MARKET SCANNER TEST")


if __name__ == "__main__":
    run()