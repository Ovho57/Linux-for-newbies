"""Main classic desktop window and navigation."""
from PySide6.QtWidgets import QMainWindow,QWidget,QHBoxLayout,QListWidget,QStackedWidget,QToolBar,QStatusBar,QMessageBox
from PySide6.QtGui import QAction
from .theme import STYLE
from .pages import DashboardPage,ArchitectPage,MathPage,DataPage,TrainingPage,TestingPage,ManualPage,PluginPage
from .terminal_page import TerminalPage

class MainWindow(QMainWindow):
 def __init__(self):
  super().__init__(); self.setWindowTitle("NeuralForge AI — Model Studio"); self.resize(1280,820); self.setMinimumSize(900,620); self.setStyleSheet(STYLE)
  self._menus(); toolbar=QToolBar("Main toolbar"); toolbar.setMovable(False); self.addToolBar(toolbar)
  root=QWidget(); layout=QHBoxLayout(root); layout.setContentsMargins(5,5,5,5); self.navigation=QListWidget(); self.navigation.setFixedWidth(205); self.stack=QStackedWidget()
  self.pages=[("Dashboard",DashboardPage()),("Neural Network Architect",ArchitectPage()),("Mathematical Workbench",MathPage()),("Dataset Studio",DataPage()),("Training Center",TrainingPage()),("Testing Laboratory",TestingPage()),("Command Console",TerminalPage()),("Plugin Manager",PluginPage()),("Application Manual",ManualPage())]
  for name,page in self.pages:self.navigation.addItem(name); self.stack.addWidget(page)
  layout.addWidget(self.navigation); layout.addWidget(self.stack,1); self.setCentralWidget(root); self.navigation.currentRowChanged.connect(self.stack.setCurrentIndex); self.navigation.setCurrentRow(0)
  self.setStatusBar(QStatusBar()); self.statusBar().showMessage("Ready — local workspace")
  for label,index in (("Home",0),("Architect",1),("Math",2),("Data",3),("Train",4),("Test",5),("Console",6),("Plugins",7),("Manual",8)):
   a=QAction(label,self); a.triggered.connect(lambda checked=False,i=index:self.navigation.setCurrentRow(i)); toolbar.addAction(a)
  self.pages[4][1].set_architecture_provider(self.pages[1][1].get_layers); self.pages[5][1].set_model_provider(self.pages[4][1].get_model)
 def _menus(self):
  file=self.menuBar().addMenu("File"); exit_action=QAction("Exit",self); exit_action.triggered.connect(self.close); file.addAction(exit_action)
  for name in ("Edit","View","Project","Architecture","Training","Tools"):self.menuBar().addMenu(name)
  help=self.menuBar().addMenu("Help"); about=QAction("About NeuralForge AI",self); about.triggered.connect(self.about); help.addAction(about)
 def about(self):QMessageBox.about(self,"About","NeuralForge AI 0.2.0\nLocal neural-network engineering and learning laboratory.")
