import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import OrionWindow


def main():
    app = QApplication(sys.argv)

    window = OrionWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()