# Architecture notes

NeuralForge is organized into four initial layers:

1. **UI** — PySide6 widgets and workspaces in `neuralforge/ui`.
2. **Core** — framework-independent model, math, architecture and persistence logic in `neuralforge/core`.
3. **Data** — CSV preparation through the Dataset Studio.
4. **Entry point** — `main.py` delegates to `neuralforge.app`.

## Model engine

The first implementation uses a small NumPy multilayer perceptron so the core learning path can work without downloading a deep-learning framework. It supports fully connected layers, tanh hidden activations, sigmoid output activation, mean-squared-error training and backpropagation.

The visual architecture currently records Input, Dense, Dropout and Output definitions. The first trainer only executes Dense and Output transformations. Dropout is not yet applied. Other layer families and custom Python layers are future work.

## Mathematics

The formula evaluator parses Python's expression syntax into an AST but evaluates only a small allow-list of numeric nodes and functions. Never replace this with unrestricted `eval`.

## Threading

Training uses a QThread worker and signals to keep the Qt interface responsive. Model state should only be read after the worker completes.

## Future extension points

- A QGraphicsScene-based visual node editor.
- A backend interface for NumPy and PyTorch engines.
- Layer registry and shape inference.
- Structured execution traces for the Mathematical Workbench.
- Versioned project format and migration support.
