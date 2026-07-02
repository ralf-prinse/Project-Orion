from services.orchestration.ai_market_scanner import AIMarketScanner
from ui.foundation.ai_scanner_presenter import AIScannerPresenter


class FakePortfolio:
    cash = 10000
    position_size = 0
    exposure = 0


def run():
    print("START AI SCANNER PRESENTER TEST")

    scanner = AIMarketScanner()
    presenter = AIScannerPresenter()

    result = scanner.scan(
        symbols=["MSFT", "NVDA", "AAPL"],
        portfolio_state=FakePortfolio(),
    )

    sections = presenter.create_sections(result)

    print("\nSECTIONS")
    for section in sections:
        print("TITLE:", section.title)
        print("DESCRIPTION:", section.description)

        for metric in section.metrics:
            print(f"- {metric.label}: {metric.value}")

        print("---")

    print("\nTOTAL SECTIONS:", len(sections))
    print("END AI SCANNER PRESENTER TEST")


if __name__ == "__main__":
    run()