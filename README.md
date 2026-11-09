# NeuralForge AI

NeuralForge AI is a local neural-network engineering laboratory with a classic cream-and-beige desktop interface. It is designed to help learners build architectures, train models, inspect calculations and export predictions without depending on a hosted AI service.

## Current development

### Working in the desktop application
- PySide6 desktop shell and classic engineering-software theme.
- Sequential architecture editor with editable layer sizes, activations and dropout settings.
- Dense NumPy network training with real ReLU, sigmoid, tanh, linear and softmax activation functions.
- Inverted dropout during training; dropout is disabled during prediction.
- Tensor-level dense forward and backpropagation traces, including activations, errors, deltas and parameter gradients.
- XOR demonstration, CSV dataset preview, training progress and prediction testing.
- Project JSON save/load, portable model export and command-line inference.
- In-app mathematical workbench and Python command console.
- Automated unit tests.

### Optional advanced execution backend
Install PyTorch support with:

```bash
python -m pip install ".[torch]"
```

The optional `neuralforge.core.torch_engine` backend provides executable Dense, Dropout, Conv1D and RNN layers, automatic device selection (CUDA when available, otherwise CPU), model fitting and named tensor-gradient inspection. Sequence input shapes:
- Conv1D: `[batch, channels, sequence_length]`
- RNN: `[batch, sequence_length, features]`

This advanced backend is a Python API at this stage; the desktop Training Center still uses the NumPy dense engine. CNN/RNN models are not yet editable and trainable end-to-end from the desktop UI.

### Extension and distribution infrastructure
- In-app Plugin Manager for discovering and loading installed Python entry-point plugins.
- Trusted custom PyTorch layer registration through `register_layer`.
- GitHub Actions packaging workflow for Windows and Linux executable folders.

Plugins are Python code and can access the same permissions as the application. Only install plugins from trusted sources.

## Install on Windows

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
python main.py
```

If PowerShell activation is blocked:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe main.py
```

## Install on Ubuntu / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
python main.py
```

For the optional advanced engine, install `pip install -e ".[torch]"`.

## CLI

```bash
pip install -e .
neuralforge info PATH_TO_EXPORTED_MODEL
neuralforge run PATH_TO_EXPORTED_MODEL --input 0,1
```

Or use `python -m neuralforge.cli` from the repository root.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Desktop packages

The `.github/workflows/package.yml` workflow builds Windows and Linux packages when manually dispatched or when a version tag such as `v0.3.0` is pushed. These builds are unsigned. Windows code-signing requires a certificate and protected signing credentials supplied by the release owner.

## Still outstanding

- Connect the optional PyTorch CNN/RNN backend to the desktop architecture editor and Training Center.
- Add in-app plugin installation/uninstallation and per-plugin permission isolation.
- Build and test a mobile companion interface against real phones.
- Produce signed releases after signing credentials are configured.
- Add end-to-end GUI tests on Windows and Linux and test packaged binaries on clean machines.

NeuralForge is an actively developed local application, not a foundation-model trainer. It is intended for learning and experimenting with smaller neural networks.
