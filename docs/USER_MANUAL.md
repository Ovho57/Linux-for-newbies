# NeuralForge AI — User Manual

## 1. Start the application

Install dependencies from `requirements.txt`, then run `python main.py`.

## 2. Dashboard

The Dashboard describes the local application, current model engine and default project folder.

## 3. Neural Network Architect

The first row is the Input layer and the last row is the Output layer. Edit units and activation values directly in the table. Add Dense or Dropout layers, remove hidden layers, and move hidden layers up or down. The status message reports architecture validation.

The initial trainer uses the input width and the widths of Dense and Output layers. Dropout entries are currently definitions only and do not affect training.

## 4. Mathematical Workbench

Select Beginner, Intermediate or Advanced. Edit the weights, inputs and bias, then calculate the weighted sum. The Safe Formula Evaluator supports arithmetic, powers, parentheses, pi, e and selected math functions.

## 5. Dataset Studio

Open a CSV file. Select a numeric target column. Other numeric columns become inputs. The preview displays up to 100 rows. Rows with missing numeric values and non-numeric columns are excluded from the prepared arrays.

## 6. Training Center

Select **Use XOR demonstration** to load a four-row example, or load a numeric CSV in Dataset Studio. Set epochs and learning rate, then train. Training progress and mean squared error are displayed.

The current engine is a teaching-focused, full-batch NumPy MLP. It is not intended for large-scale deep learning.

## 7. Testing Laboratory

After training, enter comma-separated numeric values matching the model input width and select Run prediction.

## 8. Current limitations

This release does not yet include a graphical node canvas, convolutional/recurrent model execution, custom Python layer execution, GPU training, an integrated operating-system terminal, or a mobile app. These are planned features, not completed functionality.
