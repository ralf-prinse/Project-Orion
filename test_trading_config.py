from config.trading_config import TRADING_CONFIG


def main():
    print("\n=========================================")
    print("ORION TRADING CONFIG TEST")
    print("=========================================\n")

    print(f"Broker: {TRADING_CONFIG.broker_name}")
    print(f"Account currency: {TRADING_CONFIG.account_currency}")
    print(f"Default market currency: {TRADING_CONFIG.default_market_currency}")
    print(f"Default universe: {TRADING_CONFIG.default_universe}")

    for market in TRADING_CONFIG.supported_markets:
        print(
            f"- {market.name} | {market.country} | "
            f"{market.currency} | {', '.join(market.exchanges)}"
        )

    assert TRADING_CONFIG.broker_name == "DEGIRO"
    assert TRADING_CONFIG.account_currency == "EUR"
    assert TRADING_CONFIG.default_market_currency == "USD"
    assert len(TRADING_CONFIG.supported_markets) >= 1

    print("\nTRADING CONFIG: PASS ✅\n")


if __name__ == "__main__":
    main()