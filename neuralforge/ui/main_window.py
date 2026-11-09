"""Main classic desktop window and navigation."""
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QStackedWidget, QToolBar, QStatusBar, QMessageBox)
from PySide6.QtGui import QAction
from .theme import STYLE
from .pages import DashboardPage, ArchitectPage, MathPage, DataPage, TrainingPage, TestingPage, ManualPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NeuralForge AI — Model Studio")
        self.resize(1280, 820)
        self.setMinimumSize(900, 620)
        self.setStyleSheet(STYLE)
        self._make_menus()
        self._make_toolbar()
        root = QWidget()
        layout = QHBoxLayout(root)
        layout.setContentsMargins(5, 5, 5, 5)
        self.navigation = QListWidget()
        self.navigation.setFixedWidth(190)
        self.stack = QStackedWidget()
        self.pages = [
            ("Dashboard", DashboardPage()),
            ("Neural Network Architect", ArchitectPage()),
            ("Mathematical Workbench", MathPage()),
            ("Dataset Studio", DataPage()),
            ("Training Center", TrainingPage()),
            ("Testing Laboratory", TestingPage()),
            ("Application Manual", ManualPage()),
        ]
        for title, page in self.pages:
            self.navigation.addItem(title)
            self.stack.addWidget(page)
        layout.addWidget(self.navigation)
        layout.addWidget(self.stack, 1)
        self.setCentralWidget(root)
        self.navigation.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.navigation.setCurrentRow(0)
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready — local workspace")
        self._connect_pages()

    def _make_menus(self):
        for title in ("File", "Edit", "View", "Project", "Architecture", "Training", "Tools", "Help"):
            self.menuBar().addMenu(title)
        help_menu = self.menuBar().addMenu("About")
        action = help_menu.addAction("About NeuralForge AI")
        action.triggered.connect(self._about)

    def _make_toolbar(self):
        toolbar = QToolBar("Main toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        for label, page in (("Dashboard", 0), ("Architect", 1), ("Math", 2), ("Datasets", 3), ("Train", 4), ("Test", 5), ("Manual", 6)):
            action = QAction(label, self)
            action.triggered.connect(lambda checked=False, index=page: self.navigation.setCurrentRow(index))
            toolbar.addAction(action)

    def _connect_pages(self):
        architect = self.pages[1][1]
        training = self.pages[4][1]
        testing = self.pages[5][1]
        training.set_architecture_provider(architect.get_layers)
        testing.set_model_provider(training.get_model)

    def _about(self):
        QMessageBox.about(self, "About NeuralForge AI",
            "NeuralForge AI 0.1.0\nA local neural-network engineering and learning laboratory.\nClassic interface, modern Python engine.")
