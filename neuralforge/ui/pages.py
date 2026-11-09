"""Functional NeuralForge workspaces."""
from pathlib import Path
import numpy as np
import pandas as pd
from PySide6.QtCore import Qt,QThread,Signal
from PySide6.QtWidgets import (QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QTableWidget,QTableWidgetItem,QComboBox,QSpinBox,QDoubleSpinBox,QFormLayout,QGroupBox,QMessageBox,QFileDialog,QPlainTextEdit,QTabWidget,QLineEdit,QProgressBar,QSplitter,QInputDialog,QListWidget)
from ..core.architecture import LayerSpec,validate_architecture
from ..core.math_engine import weighted_sum_trace,safe_evaluate
from ..core.mlp import MLP
from ..core.model_builder import build_mlp
from ..core.plugin_manager import PluginManager
from ..core.project_store import default_project_dir,save_project,load_project
from ..core.model_io import architecture_dimensions,save_model_bundle
from .network_canvas import NetworkCanvas

class DashboardPage(QWidget):
 def __init__(self):
  super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("<h1>NeuralForge AI</h1><h3>Local Neural Network Engineering Laboratory</h3>"))
  intro=QLabel("Design networks, inspect calculations, prepare datasets, train models and run predictions locally."); intro.setWordWrap(True); l.addWidget(intro)
  g=QGroupBox("Workspace status"); f=QFormLayout(g); f.addRow("Version",QLabel("0.2.0 — active development")); f.addRow("Execution",QLabel("Local / offline")); f.addRow("Engine",QLabel("NumPy multilayer perceptron")); f.addRow("Projects",QLabel(str(default_project_dir()))); l.addWidget(g)
  g=QGroupBox("Available workspaces"); f=QVBoxLayout(g)
  for s in ("Visual network architecture editor","Mathematical workbench","CSV dataset preparation","Background model training","Prediction and forward-pass inspection","Project save/load and portable model export","NeuralForge command console"):f.addWidget(QLabel("•  "+s))
  l.addWidget(g); l.addStretch(1)

class ArchitectPage(QWidget):
 def __init__(self):
  super().__init__(); self.layers=[LayerSpec("Input",2,"linear"),LayerSpec("Dense",4,"tanh"),LayerSpec("Output",1,"sigmoid")]
  l=QVBoxLayout(self); l.addWidget(QLabel("<h2>Neural Network Architect</h2>")); l.addWidget(QLabel("Select a layer in the diagram or edit its properties. Input and Output layers are required."))
  split=QSplitter(Qt.Horizontal); self.canvas=NetworkCanvas(); self.canvas.layer_selected.connect(self.select_layer); split.addWidget(self.canvas)
  w=QWidget(); f=QFormLayout(w); self.kind=QComboBox(); self.kind.addItems(["Input","Dense","Dropout","Output"]); self.units=QSpinBox(); self.units.setRange(1,8192)
  self.activation=QComboBox(); self.activation.addItems(["linear","relu","tanh","sigmoid"]); self.dropout=QDoubleSpinBox(); self.dropout.setRange(0,.95); self.dropout.setSingleStep(.05)
  f.addRow("Layer type",self.kind); f.addRow("Units / neurons",self.units); f.addRow("Activation",self.activation); f.addRow("Dropout rate",self.dropout)
  b=QPushButton("Apply properties"); b.clicked.connect(self.apply_properties); f.addRow(b); split.addWidget(w); split.setSizes([700,260]); l.addWidget(split,1)
  row=QHBoxLayout()
  for label,fn in (("Add Dense",lambda:self.add_layer("Dense")),("Add Dropout",lambda:self.add_layer("Dropout")),("Remove",self.remove_layer),("Move left",lambda:self.move_layer(-1)),("Move right",lambda:self.move_layer(1)),("Save project",self.save),("Load project",self.load)):
   b=QPushButton(label); b.clicked.connect(fn); row.addWidget(b)
  l.addLayout(row); self.status=QLabel(); l.addWidget(self.status); self.selected=1; self.refresh()
 def refresh(self):
  self.selected=min(max(0,self.selected),len(self.layers)-1); self.canvas.set_layers(self.layers); self.canvas.selected=self.selected; self.canvas.update()
  errors=validate_architecture(self.layers); self.status.setText("Architecture valid." if not errors else " | ".join(errors))
  x=self.layers[self.selected]; self.kind.setCurrentText(x.kind); self.units.setValue(x.units); self.activation.setCurrentText(x.activation if x.activation in ["linear","relu","tanh","sigmoid"] else "linear"); self.dropout.setValue(x.dropout)
 def select_layer(self,i):self.selected=i; self.refresh()
 def apply_properties(self):
  x=self.layers[self.selected]; k=self.kind.currentText()
  if self.selected==0 and k!="Input":QMessageBox.warning(self,"Layer","First layer must be Input."); return
  if self.selected==len(self.layers)-1 and k!="Output":QMessageBox.warning(self,"Layer","Last layer must be Output."); return
  x.kind=k; x.units=self.units.value(); x.activation=self.activation.currentText(); x.dropout=self.dropout.value(); self.refresh()
 def add_layer(self,k):
  i=max(1,len(self.layers)-1); self.layers.insert(i,LayerSpec(k,8,"tanh" if k=="Dense" else "linear",.1 if k=="Dropout" else 0)); self.selected=i; self.refresh()
 def remove_layer(self):
  if self.selected<=0 or self.selected>=len(self.layers)-1:QMessageBox.information(self,"Layer","Input and Output cannot be removed."); return
  self.layers.pop(self.selected); self.selected=min(self.selected,len(self.layers)-2); self.refresh()
 def move_layer(self,d):
  t=self.selected+d
  if t<=0 or t>=len(self.layers)-1:return
  self.layers[self.selected],self.layers[t]=self.layers[t],self.layers[self.selected]; self.selected=t; self.refresh()
 def get_layers(self):return list(self.layers)
 def save(self):
  folder=QFileDialog.getExistingDirectory(self,"Choose project folder",str(default_project_dir()))
  if not folder:return
  name,ok=QInputDialog.getText(self,"Project name","Name:",text="My NeuralForge Project")
  if not ok:return
  try:QMessageBox.information(self,"Saved",f"Project saved: {save_project(folder,name,self.layers)}")
  except Exception as e:QMessageBox.critical(self,"Save failed",str(e))
 def load(self):
  path,_=QFileDialog.getOpenFileName(self,"Open project",str(default_project_dir()),"Project JSON (*.json)")
  if not path:return
  try:
   data,layers=load_project(path); errors=validate_architecture(layers)
   if errors:raise ValueError("\n".join(errors))
   self.layers=layers; self.selected=0; self.refresh(); QMessageBox.information(self,"Loaded",f"Loaded {data.get('name','Untitled')}")
  except Exception as e:QMessageBox.critical(self,"Load failed",str(e))

class MathPage(QWidget):
 def __init__(self):
  super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("<h2>Mathematical Workbench</h2>")); self.tabs=QTabWidget(); l.addWidget(self.tabs); self.levels={}
  descriptions={"Beginner":"A neuron multiplies each input by a weight, adds the products, then adds a bias. An activation transforms the result.","Intermediate":"For input x and weights w: z = Σ(wᵢxᵢ) + b, then a = f(z).","Advanced":"For batch X and weights W: Z = XW + b; A = φ(Z)."}
  for level in ("Beginner","Intermediate","Advanced"):
   p=QWidget(); pl=QVBoxLayout(p); d=QLabel(descriptions[level]); d.setWordWrap(True); pl.addWidget(d); f=QFormLayout(); self.levels[level]={}
   for label,value in (("Weight 1","0.5"),("Input 1","2"),("Weight 2","0.8"),("Input 2","3"),("Bias","0.2")):
    e=QLineEdit(value); self.levels[level][label]=e; f.addRow(label,e)
   pl.addLayout(f); out=QLabel("Edit values and calculate."); pl.addWidget(out); b=QPushButton("Calculate weighted sum"); b.clicked.connect(lambda checked=False,lev=level,o=out:self.calculate(lev,o)); pl.addWidget(b); pl.addStretch(1); self.tabs.addTab(p,level)
  g=QGroupBox("Safe formula evaluator"); f=QFormLayout(g); self.expression=QLineEdit("sin(pi / 2) + 3**2"); self.result=QLabel("Result: —"); b=QPushButton("Evaluate"); b.clicked.connect(self.evaluate); f.addRow("Expression",self.expression); f.addRow(b,self.result); l.addWidget(g)
 def calculate(self,level,out):
  try:
   v=self.levels[level]; t=weighted_sum_trace([float(v["Weight 1"].text()),float(v["Weight 2"].text())],[float(v["Input 1"].text()),float(v["Input 2"].text())],float(v["Bias"].text()))
   out.setText(f"z = ({t['terms'][0]['weight']} × {t['terms'][0]['input']}) + ({t['terms'][1]['weight']} × {t['terms'][1]['input']}) + {t['bias']} = {t['z']:.8g}")
  except Exception as e:out.setText("Calculation error: "+str(e))
 def evaluate(self):
  try:self.result.setText(f"Result: {safe_evaluate(self.expression.text()):.12g}")
  except Exception as e:self.result.setText("Error: "+str(e))

class DataPage(QWidget):
 def __init__(self):
  super().__init__(); self.x=self.y=None; l=QVBoxLayout(self); l.addWidget(QLabel("<h2>Dataset Studio</h2>")); l.addWidget(QLabel("Load a CSV and choose a numeric target; remaining numeric columns become inputs."))
  row=QHBoxLayout(); b=QPushButton("Open CSV"); b.clicked.connect(self.load_csv); self.target=QComboBox(); self.target.currentTextChanged.connect(self.prepare); row.addWidget(b); row.addWidget(QLabel("Target:")); row.addWidget(self.target,1); l.addLayout(row)
  self.preview=QTableWidget(); l.addWidget(self.preview,1); self.info=QLabel("No dataset loaded."); l.addWidget(self.info)
 def load_csv(self):
  path,_=QFileDialog.getOpenFileName(self,"Open CSV","","CSV files (*.csv)")
  if not path:return
  try:
   self.frame=pd.read_csv(path); self.target.clear(); self.target.addItems([str(c) for c in self.frame.columns]); n=min(100,len(self.frame))
   self.preview.setRowCount(n); self.preview.setColumnCount(len(self.frame.columns)); self.preview.setHorizontalHeaderLabels([str(c) for c in self.frame.columns])
   for r in range(n):
    for c in range(len(self.frame.columns)):self.preview.setItem(r,c,QTableWidgetItem(str(self.frame.iloc[r,c])))
   self.prepare()
  except Exception as e:QMessageBox.critical(self,"Dataset error",str(e))
 def prepare(self):
  if not hasattr(self,"frame") or not self.target.currentText():return
  df=self.frame.select_dtypes(include="number").dropna(); target=self.target.currentText()
  if target not in df.columns or len(df.columns)<2:self.x=self.y=None; self.info.setText("Choose a numeric target and at least one numeric input."); return
  self.y=df[[target]].to_numpy(float); self.x=df.drop(columns=[target]).to_numpy(float); self.info.setText(f"Prepared {len(self.x)} rows and {self.x.shape[1]} input columns. Original CSV unchanged.")
 def get_data(self):return self.x,self.y

class TrainingWorker(QThread):
 progress=Signal(int,int,float); completed=Signal(object,object); failed=Signal(str)
 def __init__(self,model,x,y,epochs,rate):
  super().__init__(); self.model,self.x,self.y,self.epochs,self.rate=model,x,y,epochs,rate
 def run(self):
  try:
   h=self.model.train(self.x,self.y,self.epochs,self.rate,callback=lambda e,t,v:self.progress.emit(e,t,v)); self.completed.emit(self.model,h)
  except Exception as e:self.failed.emit(str(e))

class TrainingPage(QWidget):
 def __init__(self):
  super().__init__(); self.architecture_provider=lambda:[LayerSpec("Input",2),LayerSpec("Dense",4,"tanh"),LayerSpec("Output",1,"sigmoid")]
  self.model=None; self.layers=None; self.worker=None; self.history=[]; self.x=self.y=None; l=QVBoxLayout(self); l.addWidget(QLabel("<h2>Training Center</h2>"))
  f=QFormLayout(); self.epochs=QSpinBox(); self.epochs.setRange(1,100000); self.epochs.setValue(1500); self.rate=QDoubleSpinBox(); self.rate.setRange(.0001,2); self.rate.setDecimals(4); self.rate.setValue(.1); f.addRow("Epochs",self.epochs); f.addRow("Learning rate",self.rate); l.addLayout(f)
  row=QHBoxLayout(); b=QPushButton("Load XOR example"); b.clicked.connect(self.demo); self.train=QPushButton("Train model"); self.train.clicked.connect(self.start); export=QPushButton("Export trained model"); export.clicked.connect(self.export)
  row.addWidget(b); row.addWidget(self.train); row.addWidget(export); l.addLayout(row); self.progress=QProgressBar(); l.addWidget(self.progress); self.log=QPlainTextEdit(); self.log.setReadOnly(True); l.addWidget(self.log,1)
 def set_architecture_provider(self,p):self.architecture_provider=p
 def demo(self):
  self.x=np.array([[0,0],[0,1],[1,0],[1,1]],float); self.y=np.array([[0],[1],[1],[0]],float); self.log.appendPlainText("Loaded XOR: four examples, two inputs, one output.")
 def start(self):
  if self.worker and self.worker.isRunning():QMessageBox.information(self,"Training","Already running."); return
  if self.x is None:self.demo()
  self.layers=self.architecture_provider(); errors=validate_architecture(self.layers)
  if errors:QMessageBox.warning(self,"Architecture","\n".join(errors)); return
  try:
   dims=architecture_dimensions(self.layers)
   if self.x.shape[1]!=dims[0] or self.y.shape[1]!=dims[-1]:raise ValueError(f"Data dimensions {self.x.shape[1]}→{self.y.shape[1]} do not match model {dims[0]}→{dims[-1]}.")
   self.model=build_mlp(self.layers); self.train.setEnabled(False); self.progress.setValue(0); self.log.appendPlainText(f"Training architecture {dims} | activations {[v for v in self.model.activations]} | dropout {self.model.dropout_rates}")
   self.worker=TrainingWorker(self.model,self.x,self.y,self.epochs.value(),self.rate.value()); self.worker.progress.connect(self.on_progress); self.worker.completed.connect(self.done); self.worker.failed.connect(self.fail); self.worker.start()
  except Exception as e:self.train.setEnabled(True); QMessageBox.critical(self,"Training error",str(e))
 def on_progress(self,e,total,loss):self.progress.setMaximum(total); self.progress.setValue(e); self.log.appendPlainText(f"Epoch {e}/{total} — MSE {loss:.7f}")
 def done(self,model,history):self.model=model; self.history=history; self.train.setEnabled(True); self.log.appendPlainText(f"Training complete. Final MSE: {history[-1]:.7f}")
 def fail(self,msg):self.train.setEnabled(True); self.log.appendPlainText("Training failed: "+msg); QMessageBox.critical(self,"Training failed",msg)
 def get_model(self):return self.model
 def export(self):
  if self.model is None:QMessageBox.information(self,"Export","Train a model first."); return
  folder=QFileDialog.getExistingDirectory(self,"Choose export folder")
  if not folder:return
  name,ok=QInputDialog.getText(self,"Model name","Name:",text="My NeuralForge Model")
  if not ok:return
  try:
   target=Path(folder)/"NeuralForgeExport"; save_model_bundle(target,self.model,self.layers or self.architecture_provider(),name); QMessageBox.information(self,"Export complete",f"Exported to {target}. Run python predict.py")
  except Exception as e:QMessageBox.critical(self,"Export failed",str(e))

class TestingPage(QWidget):
 def __init__(self):
  super().__init__(); self.provider=lambda:None; l=QVBoxLayout(self); l.addWidget(QLabel("<h2>Testing Laboratory</h2>")); l.addWidget(QLabel("Enter comma-separated numeric inputs matching the model input width."))
  self.inputs=QLineEdit("0, 1"); b=QPushButton("Run prediction"); b.clicked.connect(self.predict); l.addWidget(self.inputs); l.addWidget(b); self.output=QPlainTextEdit(); self.output.setReadOnly(True); l.addWidget(self.output,1)
 def set_model_provider(self,p):self.provider=p
 def predict(self):
  m=self.provider()
  if m is None:self.output.setPlainText("No trained model. Train one in Training Center."); return
  try:
   vals=[float(v.strip()) for v in self.inputs.text().split(",")]; trace=m.forward([vals]); self.output.setPlainText(f"Prediction: {trace[-1][0]}\n\nForward-pass trace:")
   for i,a in enumerate(trace):self.output.appendPlainText(f"Layer {i}: {a.tolist()}")
  except Exception as e:self.output.setPlainText("Prediction error: "+str(e))

class ManualPage(QWidget):
 def __init__(self):
  super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("<h2>NeuralForge User Manual</h2>")); self.search=QLineEdit(); self.search.setPlaceholderText("Search manual text..."); self.text=QPlainTextEdit(); self.text.setReadOnly(True)
  self.text.setPlainText("GETTING STARTED\nInstall requirements and run python main.py.\n\nNEURAL NETWORK ARCHITECT\nSelect a node in the diagram, edit its properties and apply. Input must be first and Output last.\n\nMATHEMATICAL WORKBENCH\nEdit weights, inputs and bias. The formula parser supports arithmetic, powers, pi, e and selected math functions.\n\nDATASET STUDIO\nLoad a CSV and select a numeric target. Other numeric columns become inputs; original data is not modified.\n\nTRAINING CENTER\nLoad the XOR example or a numeric CSV, set epochs and learning rate, then train.\n\nTESTING LABORATORY\nEnter values matching the model input width. Results include intermediate activations.\n\nMODEL EXPORT\nExport creates config.json, weights.npz, predict.py and requirements.txt. Install NumPy and run python predict.py.\n\nCOMMAND LINE\nUse python -m neuralforge.cli info PATH or python -m neuralforge.cli run PATH --input 0,1.\n\nLIMITATIONS\nCNN/RNN, GPU acceleration, custom executable layers, real dropout, mobile app, plugins and installer remain future work.")
  l.addWidget(self.search); l.addWidget(self.text,1); self.search.textChanged.connect(self.find)
 def find(self,value):
  if value:
   c=self.text.document().find(value)
   if not c.isNull():self.text.setTextCursor(c)


class PluginPage(QWidget):
 def __init__(self):
  super().__init__(); self.manager=PluginManager(); l=QVBoxLayout(self)
  l.addWidget(QLabel("<h2>Plugin Manager</h2>"))
  warning=QLabel("Plugins are trusted Python code and run with the application's permissions. Only use plugins from developers you trust.")
  warning.setWordWrap(True); l.addWidget(warning)
  row=QHBoxLayout(); self.items=QListWidget(); row.addWidget(self.items,1)
  controls=QVBoxLayout(); refresh=QPushButton("Discover installed plugins"); refresh.clicked.connect(self.refresh); controls.addWidget(refresh)
  load=QPushButton("Load selected plugin"); load.clicked.connect(self.load_selected); controls.addWidget(load); controls.addStretch(1); row.addLayout(controls); l.addLayout(row,1)
  self.output=QPlainTextEdit(); self.output.setReadOnly(True); self.output.setMaximumHeight(150); l.addWidget(self.output)
  self.refresh()
 def refresh(self):
  self.items.clear()
  try:
   plugins=self.manager.discover()
   for item in plugins:self.items.addItem(f"{item['name']} — {item['value']}")
   self.output.setPlainText(f"Discovered {len(plugins)} installed plugin(s). Plugins are installed separately with pip.")
  except Exception as exc:self.output.setPlainText("Discovery failed: "+str(exc))
 def load_selected(self):
  item=self.items.currentItem()
  if item is None:return
  name=item.text().split(" — ",1)[0]
  try:
   plugin=self.manager.load(name)
   self.output.setPlainText(f"Loaded plugin: {name}\nEntry point result: {plugin!r}")
  except Exception as exc:self.output.setPlainText(f"Plugin load failed: {exc}")
