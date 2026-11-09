"""Classic cream engineering-software palette and Qt stylesheet."""
STYLE = """
QMainWindow, QWidget { background: #e9e2d2; color: #302d27; font-family: Tahoma; font-size: 9pt; }
QMenuBar, QMenu { background: #ded6c6; color: #302d27; border: 1px solid #b2a894; }
QMenuBar::item { padding: 4px 9px; background: transparent; }
QMenuBar::item:selected, QMenu::item:selected { background: #cbd3c0; }
QToolBar { background: #d8d0be; border: 1px solid #b2a894; spacing: 5px; padding: 4px; }
QPushButton { background: #eee8da; color: #302d27; border: 1px solid #9e947f; border-top-color: #fffaf0; border-left-color: #fffaf0; padding: 5px 10px; }
QPushButton:hover { background: #e2dfd0; }
QPushButton:pressed { border-top-color: #8d826e; border-left-color: #8d826e; border-bottom-color: #fffaf0; border-right-color: #fffaf0; }
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QPlainTextEdit, QTextEdit, QTableWidget, QListWidget {
 background: #f7f3e9; color: #302d27; border: 1px solid #a99f8c; selection-background-color: #cbd3c0; selection-color: #302d27;
}
QGroupBox { border: 1px solid #b2a894; margin-top: 9px; padding: 7px; font-weight: bold; }
QGroupBox::title { subcontrol-origin: margin; left: 8px; padding: 0 3px; }
QTabWidget::pane { border: 1px solid #aaa08c; background: #f3eee2; }
QTabBar::tab { background: #ddd5c5; border: 1px solid #aaa08c; padding: 5px 10px; }
QTabBar::tab:selected { background: #f3eee2; border-bottom-color: #f3eee2; }
QHeaderView::section { background: #ddd5c5; border: 1px solid #aaa08c; padding: 4px; }
QStatusBar { background: #d8d0be; border-top: 1px solid #a99f8c; }
QProgressBar { border: 1px solid #9e947f; background: #f7f3e9; text-align: center; }
QProgressBar::chunk { background: #aab59c; }
"""
