"""Functional first-release workspace pages."""
from pathlib import Path
import numpy as np
import pandas as pd
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QComboBox, QSpinBox, QDoubleSpinBox, QFormLayout,
    QGroupBox, QMessageBox, QFileDialog, QPlainTextEdit, QTabWidget, QLineEdit,
    QProgressBar, QHeaderView, QSplitter)
from ..core.architecture import LayerSpec, validate_architecture
from ..core.math_engine import weighted_sum_trace, safe_evaluate
from ..core.mlp import MLP
from ..core.project_store import default_project_dir, save_project, load_project


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h1>NeuralForge AI</h1><h3>Local Neural Network Engineering Laboratory</h3>"))
        intro = QLabel("Build networks, inspect their mathematics, prepare data, train models and test predictions.\n\nThis is an early development release. Use the navigation panel to open a workspace.")
        intro.setWordWrap(True)
        layout.addWidget(intro)
        box = QGroupBox("Workspace overview")
        form = QFormLayout(box)
        form.addRow("Application version", QLabel("0.1.0 — early development"))
        form.addRow("Execution mode", QLabel("Local / offline"))
        form.addRow("Model engine", QLabel("NumPy feed-forward network"))
        form.addRow("Project directory", QLabel(str(default_project_dir())))
        layout.addWidget(box)
        layout.addStretch(1)


class ArchitectPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layers = [LayerSpec("Input", 2, "linear"), LayerSpec("Dense", 4, "tanh"), LayerSpec("Output", 1, "sigmoid")]
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h2>Neural Network Architect</h2>"))
        layout.addWidget(QLabel("Edit a feed-forward network. The current engine supports Input, Dense, Dropout (definition only) and Output layer definitions; training currently uses Dense/Output layers."))
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Layer type", "Units", "Activation", "Dropout"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        buttons = QHBoxLayout()
        for label, kind in (("Add Dense", "Dense"), ("Add Dropout", "Dropout"), ("Add Output", "Output")):
            button = QPushButton(label)
            button.clicked.connect(lambda checked=False, k=kind: self.add_layer(k))
            buttons.addWidget(button)
        remove = QPushButton("Remove selected")
        remove.clicked.connect(self.remove_layer)
        buttons.addWidget(remove)
        up = QPushButton("Move up")
        up.clicked.connect(lambda: self.move_layer(-1))
        down = QPushButton("Move down")
        down.clicked.connect(lambda: self.move_layer(1))
        buttons.addWidget(up); buttons.addWidget(down)
        layout.addLayout(buttons)
        self.validation = QLabel()
        layout.addWidget(self.validation)
        self.table.itemChanged.connect(self.read_table)
        self.refresh()

    def refresh(self):
        self.table.blockSignals(True)
        self.table.setRowCount(len(self.layers))
        for row, layer in enumerate(self.layers):
            self.table.setItem(row, 0, QTableWidgetItem(layer.kind))
            self.table.setItem(row, 1, QTableWidgetItem(str(layer.units)))
            self.table.setItem(row, 2, QTableWidgetItem(layer.activation))
            self.table.setItem(row, 3, QTableWidgetItem(str(layer.dropout)))
        self.table.blockSignals(False)
        self.validate()

    def read_table(self):
        for row in range(self.table.rowCount()):
            try:
                self.layers[row] = LayerSpec(
                    self.table.item(row, 0).text().strip(),
                    int(self.table.item(row, 1).text()),
                    self.table.item(row, 2).text().strip().lower(),
                    float(self.table.item(row, 3).text()))
            except (ValueError, AttributeError):
                self.validation.setText("Invalid value: units must be an integer and dropout a number.")
                return
        self.validate()

    def validate(self):
        errors = validate_architecture(self.layers)
        self.validation.setText("Architecture valid." if not errors else " • ".join(errors))

    def add_layer(self, kind):
        index = max(1, len(self.layers) - 1)
        self.layers.insert(index, LayerSpec(kind, 8, "relu", 0.1 if kind == "Dropout" else 0.0))
        self.refresh()

    def remove_layer(self):
        row = self.table.currentRow()
        if row <= 0 or row >= len(self.layers) - 1:
            QMessageBox.information(self, "Remove layer", "Select a hidden layer. Input and Output layers are required.")
            return
        self.layers.pop(row)
        self.refresh()

    def move_layer(self, offset):
        row = self.table.currentRow()
        target = row + offset
        if row <= 0 or row >= len(self.layers) - 1 or target <= 0 or target >= len(self.layers) - 1:
            return
        self.layers[row], self.layers[target] = self.layers[target], self.layers[row]
        self.refresh()
        self.table.selectRow(target)

    def get_layers(self):
        self.read_table()
        return list(self.layers)


class MathPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h2>Mathematical Workbench</h2>"))
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        self.levels = {}
        for level in ("Beginner", "Intermediate", "Advanced"):
            panel = QWidget()
            panel_layout = QVBoxLayout(panel)
            description = QLabel()
            description.setWordWrap(True)
            if level == "Beginner":
                description.setText("A neuron multiplies each input by a weight, adds the products, then adds a bias. An activation function transforms that total.")
            elif level == "Intermediate":
                description.setText("For inputs x and weights w, the pre-activation is z = Σ(wᵢxᵢ) + b. The activation is a = f(z).")
            else:
                description.setText("For a batch X ∈ Rⁿˣᵈ, weights W ∈ Rᵈˣᵐ and bias b ∈ R¹ˣᵐ: Z = XW + b; A = φ(Z).")
            panel_layout.addWidget(description)
            form = QFormLayout()
            self.levels[level] = {}
            defaults = [("Weight 1", "0.5"), ("Input 1", "2"), ("Weight 2", "0.8"), ("Input 2", "3"), ("Bias", "0.2")]
            for label, value in defaults:
                field = QLineEdit(value)
                self.levels[level][label] = field
                form.addRow(label, field)
            panel_layout.addLayout(form)
            result = QLabel("Weighted sum: 3.6")
            result.setTextInteractionFlags(Qt.TextSelectableByMouse)
            panel_layout.addWidget(result)
            button = QPushButton("Calculate")
            button.clicked.connect(lambda checked=False, lev=level, out=result: self.calculate(lev, out))
            panel_layout.addWidget(button)
            panel_layout.addStretch(1)
            self.tabs.addTab(panel, level)
        self.formula = QGroupBox("Safe formula evaluator")
        f_layout = QFormLayout(self.formula)
        self.expression = QLineEdit("sin(pi / 2) + 3**2")
        self.formula_result = QLabel("Result: —")
        run = QPushButton("Evaluate expression")
        run.clicked.connect(self.evaluate_formula)
        f_layout.addRow("Expression", self.expression)
        f_layout.addRow(run, self.formula_result)
        layout.addWidget(self.formula)

    def calculate(self, level, output):
        try:
            values = self.levels[level]
            trace = weighted_sum_trace(
                [float(values["Weight 1"].text()), float(values["Weight 2"].text())],
                [float(values["Input 1"].text()), float(values["Input 2"].text())],
                float(values["Bias"].text()))
            output.setText(f"z = ({trace['terms'][0]['weight']} × {trace['terms'][0]['input']}) + "
                           f"({trace['terms'][1]['weight']} × {trace['terms'][1]['input']}) + "
                           f"{trace['bias']} = {trace['z']:.6g}")
        except (ValueError, TypeError) as exc:
            output.setText(f"Calculation error: {exc}")

    def evaluate_formula(self):
        try:
            self.formula_result.setText(f"Result: {safe_evaluate(self.expression.text()):.10g}")
        except Exception as exc:
            self.formula_result.setText(f"Error: {exc}")


class DataPage(QWidget):
    def __init__(self):
        super().__init__()
        self.x = self.y = None
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h2>Dataset Studio</h2>"))
        layout.addWidget(QLabel("Load a CSV file. Choose the target column; remaining numeric columns become model inputs."))
        row = QHBoxLayout()
        load = QPushButton("Open CSV dataset")
        load.clicked.connect(self.load_csv)
        self.target = QComboBox()
        self.target.currentTextChanged.connect(self.prepare_data)
        row.addWidget(load); row.addWidget(QLabel("Target column:")); row.addWidget(self.target, 1)
        layout.addLayout(row)
        self.preview = QTableWidget()
        layout.addWidget(self.preview)
        self.info = QLabel("No dataset loaded.")
        layout.addWidget(self.info)

    def load_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV files (*.csv)")
        if not path:
            return
        try:
            self.frame = pd.read_csv(path)
            self.target.clear()
            self.target.addItems([str(c) for c in self.frame.columns])
            self.preview.setRowCount(min(100, len(self.frame)))
            self.preview.setColumnCount(len(self.frame.columns))
            self.preview.setHorizontalHeaderLabels([str(c) for c in self.frame.columns])
            for r in range(min(100, len(self.frame))):
                for c in range(len(self.frame.columns)):
                    self.preview.setItem(r, c, QTableWidgetItem(str(self.frame.iloc[r, c])))
            self.prepare_data()
        except Exception as exc:
            QMessageBox.critical(self, "Dataset error", str(exc))

    def prepare_data(self):
        if not hasattr(self, "frame") or not self.target.currentText():
            return
        try:
            numeric = self.frame.select_dtypes(include="number").dropna()
            target = self.target.currentText()
            if target not in numeric.columns or len(numeric.columns) < 2:
                self.x = self.y = None
                self.info.setText("Select a numeric target and provide at least one numeric input column.")
                return
            self.y = numeric[[target]].to_numpy(dtype=float)
            self.x = numeric.drop(columns=[target]).to_numpy(dtype=float)
            self.info.setText(f"Prepared {len(self.x)} rows; {self.x.shape[1]} input columns; 1 numeric target. Non-numeric columns and rows with missing numeric values are excluded.")
        except Exception as exc:
            self.info.setText(f"Preparation error: {exc}")

    def get_data(self):
        return self.x, self.y


class TrainingWorker(QThread):
    progress = Signal(int, int, float)
    completed = Signal(object, object)
    failed = Signal(str)

    def __init__(self, model, x, y, epochs, rate):
        super().__init__()
        self.model, self.x, self.y, self.epochs, self.rate = model, x, y, epochs, rate

    def run(self):
        try:
            history = self.model.train(self.x, self.y, self.epochs, self.rate,
                callback=lambda epoch, total, loss: self.progress.emit(epoch, total, loss))
            self.completed.emit(self.model, history)
        except Exception as exc:
            self.failed.emit(str(exc))


class TrainingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.architecture_provider = lambda: [LayerSpec("Input", 2), LayerSpec("Dense", 4), LayerSpec("Output", 1)]
        self.model = None
        self.worker = None
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h2>Training Center</h2>"))
        form = QFormLayout()
        self.epochs = QSpinBox(); self.epochs.setRange(1, 100000); self.epochs.setValue(1500)
        self.rate = QDoubleSpinBox(); self.rate.setRange(0.0001, 2.0); self.rate.setDecimals(4); self.rate.setSingleStep(0.01); self.rate.setValue(0.1)
        form.addRow("Epochs", self.epochs); form.addRow("Learning rate", self.rate)
        layout.addLayout(form)
        row = QHBoxLayout()
        demo = QPushButton("Use XOR demonstration")
        demo.clicked.connect(self.use_demo)
        self.train_button = QPushButton("Train model")
        self.train_button.clicked.connect(self.start_training)
        row.addWidget(demo); row.addWidget(self.train_button)
        layout.addLayout(row)
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        self.log = QPlainTextEdit(); self.log.setReadOnly(True)
        layout.addWidget(self.log)
        self.x = self.y = None

    def set_architecture_provider(self, provider):
        self.architecture_provider = provider

    def use_demo(self):
        self.x = np.array([[0,0],[0,1],[1,0],[1,1]], dtype=float)
        self.y = np.array([[0],[1],[1],[0]], dtype=float)
        self.log.appendPlainText("Loaded built-in XOR dataset (4 examples, 2 inputs, 1 output).")

    def start_training(self):
        if self.worker and self.worker.isRunning():
            QMessageBox.information(self, "Training", "Training is already running.")
            return
        if self.x is None:
            self.use_demo()
        layers = self.architecture_provider()
        errors = validate_architecture(layers)
        if errors:
            QMessageBox.warning(self, "Invalid architecture", "\n".join(errors)); return
        dimensions = [layers[0].units] + [layer.units for layer in layers[1:] if layer.kind.lower() in {"dense", "output"}]
        try:
            self.model = MLP(dimensions)
            self.train_button.setEnabled(False)
            self.log.appendPlainText(f"Training network {dimensions} ...")
            self.worker = TrainingWorker(self.model, self.x, self.y, self.epochs.value(), self.rate.value())
            self.worker.progress.connect(self.on_progress)
            self.worker.completed.connect(self.on_completed)
            self.worker.failed.connect(self.on_failed)
            self.worker.start()
        except Exception as exc:
            self.train_button.setEnabled(True)
            QMessageBox.critical(self, "Training error", str(exc))

    def on_progress(self, epoch, total, loss):
        self.progress.setMaximum(total); self.progress.setValue(epoch)
        self.log.appendPlainText(f"Epoch {epoch}/{total} — MSE: {loss:.7f}")

    def on_completed(self, model, history):
        self.model = model
        self.train_button.setEnabled(True)
        self.log.appendPlainText(f"Training finished. Final MSE: {history[-1]:.7f}")

    def on_failed(self, message):
        self.train_button.setEnabled(True)
        self.log.appendPlainText(f"Training failed: {message}")
        QMessageBox.critical(self, "Training failed", message)

    def get_model(self):
        return self.model


class TestingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.model_provider = lambda: None
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h2>Testing Laboratory</h2>"))
        layout.addWidget(QLabel("Enter comma-separated numeric inputs matching the trained model's input dimension."))
        self.inputs = QLineEdit("0, 1")
        self.output = QPlainTextEdit(); self.output.setReadOnly(True)
        run = QPushButton("Run prediction")
        run.clicked.connect(self.predict)
        layout.addWidget(self.inputs); layout.addWidget(run); layout.addWidget(self.output)

    def set_model_provider(self, provider):
        self.model_provider = provider

    def predict(self):
        model = self.model_provider()
        if model is None:
            self.output.setPlainText("No trained model is available. Train a model first.")
            return
        try:
            values = [float(part.strip()) for part in self.inputs.text().split(",")]
            if len(values) != model.dimensions[0]:
                raise ValueError(f"Expected {model.dimensions[0]} values.")
            result = model.predict(np.array([values]))
            self.output.setPlainText(f"Model output:\n{result[0]}")
        except Exception as exc:
            self.output.setPlainText(f"Prediction error: {exc}")


class ManualPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h2>NeuralForge User Manual</h2>"))
        text = QPlainTextEdit()
        text.setReadOnly(True)
        text.setPlainText(
            "GETTING STARTED\n\n"
            "1. Open Neural Network Architect.\n"
            "2. Edit the input, hidden and output layer definitions.\n"
            "3. Open Mathematical Workbench to explore weighted sums.\n"
            "4. Open Dataset Studio to load a numeric CSV, or use the XOR example in Training Center.\n"
            "5. Set epochs and learning rate, then select Train model.\n"
            "6. Open Testing Laboratory and enter inputs matching the network's input size.\n\n"
            "NEURAL NETWORK ARCHITECT\n"
            "The first layer defines input width. Dense and Output layers define trainable transformations. "
            "The current NumPy trainer supports tanh hidden activations and sigmoid output activation. "
            "Dropout is currently a layer definition only and is not applied by the initial trainer.\n\n"
            "MATHEMATICAL WORKBENCH\n"
            "Beginner, Intermediate and Advanced tabs explain a weighted sum. Edit values and press Calculate. "
            "The safe formula evaluator supports +, -, *, /, **, %, parentheses, pi, e, sin, cos, tan, sqrt, log, log10, exp and abs.\n\n"
            "DATASET STUDIO\n"
            "Load a CSV, select a numeric target column, and the remaining numeric columns become model inputs. "
            "Rows with missing numeric values are excluded from the prepared arrays.\n\n"
            "TRAINING CENTER\n"
            "Use XOR demonstration to load a small example. Training runs in a worker thread so the interface remains responsive. "
            "The current trainer uses full-batch mean squared error and backpropagation.\n\n"
            "LIMITATIONS\n"
            "This is an early foundation. CNNs, RNNs, custom executable layers, integrated shell, mobile app, "
            "installer and full visual node editor are planned but not yet implemented."
        )
        layout.addWidget(text)
