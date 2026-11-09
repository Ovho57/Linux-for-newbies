# NeuralForge AI — User Manual

## Start
Install requirements and run python main.py from the repository root.

## Dashboard
Shows the application version, execution mode, model engine and default project folder.

## Neural Network Architect
Select a node in the diagram. Edit its type, unit count, activation or dropout metadata in the inspector, then Apply properties. Add Dense or Dropout hidden entries, remove hidden entries and move them left or right. Input must be first and Output last.

The current NumPy trainer executes dense/output transformations. Dropout is metadata only and is not applied during training.

## Mathematical Workbench
Choose Beginner, Intermediate or Advanced. Edit weights, inputs and bias, then calculate the weighted sum. The formula evaluator supports arithmetic, powers, parentheses, pi, e and selected mathematical functions. It uses a restricted parser, not arbitrary Python execution.

## Dataset Studio
Open a CSV and select a numeric target. Other numeric columns become inputs. The preview shows up to 100 rows. The original CSV is not modified.

## Training Center
Load the built-in XOR example or a numeric CSV. Set epochs and learning rate, then start training. A Qt worker keeps the interface responsive and reports mean squared error.

## Testing Laboratory
Enter comma-separated values matching the input width. Results include the prediction and intermediate forward-pass activations.

## Save and load
Use Save project and Load project in the Architect page. Projects are JSON files.

## Export a trained model
Train a model, select Export trained model and choose a destination. The bundle contains config.json, weights.npz, predict.py and requirements.txt. Install NumPy and run python predict.py in the exported folder.

## Command line
Install the repository in editable mode using pip install -e . Then use neuralforge info PATH or neuralforge run PATH --input 0,1. From the repository root, use python -m neuralforge.cli.

## Limitations
CNN/RNN execution, real dropout training, GPU acceleration, custom executable layers, full shell terminal, mobile companion, plugin system and installer are not included yet.


## Advanced PyTorch backend

Install the optional backend with `pip install -e ".[torch]"`. The Python API in `neuralforge.core.torch_engine` supports dense, dropout, Conv1D and RNN layers. Conv1D inputs use batch/channel/sequence order; RNN inputs use batch/sequence/feature order. The backend selects CUDA when PyTorch reports it is available, otherwise CPU. The desktop Training Center currently uses the NumPy dense engine.

## Dropout and gradient inspection

Dense layer activation and dropout properties are executed by the NumPy training engine. Dropout is active only during training and disabled during inference. For an educational tensor trace, call `model.trace_gradients(inputs, targets)`; it returns forward activations, pre-activations, errors, deltas and weight/bias gradients.

## Plugins

Open Plugin Manager and select Discover installed plugins. Plugins are Python entry points in the `neuralforge.plugins` group. Select one and choose Load selected plugin. Loading executes third-party Python code with the same permissions as NeuralForge; install only trusted plugins. Plugin installation and permission sandboxing are not yet provided in the UI.

## Desktop builds

The GitHub Actions workflow named Build desktop packages can be manually run or triggered by a version tag. It produces Windows and Linux executable-folder archives. These builds are unsigned; signing needs release-owner credentials.
