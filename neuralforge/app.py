"""Application entry point and Qt setup."""
import sys
from PySide6.QtWidgets import QApplication
from .ui.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("NeuralForge AI")
    app.setOrganizationName("NeuralForge")
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    return app.exec()
