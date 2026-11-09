# NeuralForge AI

A local Python desktop laboratory for designing, training, inspecting and exporting small neural networks. Its interface uses a classic cream-and-beige engineering-software aesthetic.

## Current release: 0.2.0 — active development

### Implemented
- PySide6 desktop shell, cream theme and navigation.
- Interactive sequential architecture diagram: select layers, edit properties, add/remove and reorder hidden layers.
- Feed-forward architecture validation.
- NumPy multilayer perceptron with forward propagation and backpropagation.
- XOR demonstration training in a background worker.
- CSV dataset preview and numeric target selection.
- Mathematical Workbench with three explanation levels and a restricted formula evaluator.
- Prediction testing with intermediate forward-pass activations.
- Save/load architecture project JSON.
- Portable model export with weights, configuration, standalone prediction script and requirements.
- CLI commands to inspect and run exported models.
- In-app Python command console.
- Offline user manual.

### Not yet implemented
Convolutional/recurrent execution, true custom-layer execution, dropout training, GPU acceleration, full tensor-level gradient tracing, mobile companion, plugin manager, installer and signed release.

## Install on Windows

Create an environment:
    py -3 -m venv .venv
    .\.venv\Scripts\Activate.ps1
Install:
    python -m pip install --upgrade pip
    pip install -r requirements.txt
Run:
    python main.py

If activation is blocked:
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    .\.venv\Scripts\python.exe main.py

## CLI

Install editable:
    pip install -e .
Inspect a model:
    neuralforge info PATH_TO_EXPORTED_MODEL
Run inference:
    neuralforge run PATH_TO_EXPORTED_MODEL --input 0,1

From the repository root you can instead use:
    python -m neuralforge.cli info PATH_TO_EXPORTED_MODEL
    python -m neuralforge.cli run PATH_TO_EXPORTED_MODEL --input 0,1

## Tests

    python -m unittest discover -s tests -v

## Export bundle

An export contains config.json, weights.npz, predict.py, requirements.txt and README.md. A trained bundle can run without opening the desktop app, but the target computer still needs Python and NumPy unless separately packaged.

## Honest limitations

The current trainer is a small educational dense network. The canvas edits a sequential architecture; it is not a freeform graph editor. Dropout is metadata only and not applied by the trainer. The mathematical workbench has editable worked calculations, not complete live symbolic tracing of every model gradient.

## License

No license has been selected. Standard copyright applies until one is added.
