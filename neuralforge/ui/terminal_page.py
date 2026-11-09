"""Restricted in-app Python command console for NeuralForge CLI commands."""
import shlex,sys
from PySide6.QtCore import QProcess
from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QLineEdit,QPushButton,QPlainTextEdit

class TerminalPage(QWidget):
    def __init__(self):
        super().__init__(); self.process=QProcess(self)
        layout=QVBoxLayout(self); layout.addWidget(QLabel("<h2>NeuralForge Command Console</h2>"))
        layout.addWidget(QLabel("Runs Python commands through the current interpreter; it is not a general operating-system shell."))
        self.output=QPlainTextEdit(); self.output.setReadOnly(True); layout.addWidget(self.output,1)
        row=QHBoxLayout(); self.command=QLineEdit(); self.command.setPlaceholderText("python -m neuralforge.cli --help")
        run=QPushButton("Run"); run.clicked.connect(self.run_command); row.addWidget(self.command,1); row.addWidget(run); layout.addLayout(row)
        self.process.readyReadStandardOutput.connect(self.read_output); self.process.readyReadStandardError.connect(self.read_error)
        self.process.finished.connect(lambda code,status:self.output.appendPlainText(f"[Process finished: {code}]"))
        self.output.appendPlainText("Try: python -m neuralforge.cli --help")
    def run_command(self):
        raw=self.command.text().strip()
        if not raw:return
        if self.process.state()!=QProcess.NotRunning:self.output.appendPlainText("A command is already running.");return
        try:parts=shlex.split(raw,posix=False)
        except ValueError as exc:self.output.appendPlainText(str(exc));return
        if not parts or parts[0].lower() not in {"python","py"}:
            self.output.appendPlainText("Only Python commands are accepted. This prevents accidental shell execution.");return
        self.output.appendPlainText("> "+raw); self.process.start(sys.executable,parts[1:])
    def read_output(self):self.output.appendPlainText(bytes(self.process.readAllStandardOutput()).decode(errors="replace").rstrip())
    def read_error(self):self.output.appendPlainText(bytes(self.process.readAllStandardError()).decode(errors="replace").rstrip())
