# NeuralForge AI

**A classic desktop laboratory for building, training, inspecting and understanding neural networks.**

NeuralForge AI is a local Python desktop application with a deliberately old-school scientific-software interface: warm cream workspaces, beige tool panels, traditional menus and practical engineering layouts.

The project is being developed in stages. The current foundation includes a working desktop shell, editable feed-forward network architecture, a NumPy neural-network engine, a mathematical workbench, CSV dataset loading, training and prediction workflows, and local project saving.

> **Status:** Early development. This repository is not yet a finished product. Features are marked according to what is actually implemented.

## Design philosophy

- Classic 2003–2008 engineering-software aesthetic.
- Local-first: core work does not require an AI API or internet connection.
- Educational: explain the mathematics behind model operations.
- Practical: generated models and saved projects belong to the user.
- Honest: no fake training progress or placeholder success messages.

## Current features

- [x] PySide6 desktop window with classic cream/beige styling.
- [x] Dashboard and workspace navigation.
- [x] Add, remove and reorder Dense, Input, Dropout and Output layer definitions.
- [x] Validate feed-forward architecture dimensions.
- [x] NumPy multilayer perceptron with forward pass and backpropagation.
- [x] Train a small classifier on CSV data or the built-in XOR example.
- [x] Training loss history and accuracy reporting.
- [x] Mathematical Workbench with Beginner, Intermediate and Advanced explanations.
- [x] Editable demonstration values for weighted sums.
- [x] Save and load model weights and project configuration locally.
- [x] Test predictions using numeric input values.
- [x] Unit tests for the model engine and mathematics utilities.

## Planned modules

The following are planned, not yet complete: visual node-and-connection canvas, convolutional and recurrent networks, custom Python layers, advanced tensor tracing, computer vision and NLP labs, plugin manager, experiment comparison, integrated terminal, mobile companion, installer and signed releases.

## Requirements

- Python 3.10 or newer
- Windows 10/11 initially; other platforms may work but are not yet officially tested

## Install

Create and activate a virtual environment:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run:

```powershell
python main.py
```

If PowerShell blocks activation, use the environment's interpreter directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

## Tests

```powershell
python -m unittest discover -s tests -v
```

## Project data

Projects are saved in the user's Documents folder under `NeuralForge/projects` by default. Model weights are stored as NumPy `.npz` files and configuration as JSON.

## Safety and execution

NeuralForge does not execute arbitrary user-entered formulas with Python `eval`. The formula utility accepts a restricted mathematical expression grammar. Custom Python layer execution and a general-purpose integrated terminal are not implemented in this initial foundation.

## License

No license has been selected yet. Until a license is added, standard copyright applies to contributions in this repository.
