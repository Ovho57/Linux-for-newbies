# Architecture

- neuralforge/ui: PySide6 interface, classic theme, visual network canvas, workspace pages and command console.
- neuralforge/core: architecture validation, NumPy model, safe math evaluator, project persistence and portable model export.
- neuralforge/cli.py: command-line inspection and inference for exported bundles.
- tests: automated core tests.
- docs: user and developer guides.

The UI uses Qt signals and a worker thread for training. The canvas is a visual sequential architecture editor, not a freeform graph editor. The current NumPy engine uses tanh hidden activations and sigmoid output. Architect activation settings currently remain descriptive metadata; full per-layer activation execution is future work. Dropout is also metadata-only.

The formula evaluator parses expressions into an AST and evaluates an explicit allow-list. Do not replace it with unrestricted eval.

Exported bundles contain NumPy weights, configuration and a standalone prediction script.
