# Mathematics behind a neural network

## 1. Weighted sum

A neuron combines its inputs using weights and a bias:

```
z = w1*x1 + w2*x2 + ... + wn*xn + b
```

Each input is multiplied by its weight. The products are added, then the bias is added.

Example:

- x1 = 2, w1 = 0.5
- x2 = 3, w2 = 0.8
- b = 0.2

Then:

```
z = (0.5 * 2) + (0.8 * 3) + 0.2
z = 1.0 + 2.4 + 0.2
z = 3.6
```

## 2. Activation

The activation function transforms z. The initial NumPy model uses tanh in hidden layers and sigmoid in its output layer.

Sigmoid:

```
sigmoid(z) = 1 / (1 + exp(-z))
```

It maps real-valued inputs to values between zero and one.

## 3. Matrix form

For a batch of examples:

```
Z = XW + b
A = activation(Z)
```

X contains input rows, W contains weights, b is the bias vector and A contains activations.

## 4. Loss

The first trainer uses mean squared error:

```
MSE = mean((prediction - target)^2)
```

A lower loss means predictions are, on average, closer to the target values under this measure. It does not by itself guarantee that a model generalizes well.

## 5. Gradient descent

Training adjusts weights in the direction that reduces loss:

```
W = W - learning_rate * gradient
```

The learning rate controls the update size. Too large can make training unstable; too small can make learning slow.

## 6. Backpropagation

Backpropagation applies the chain rule to calculate how each weight contributes to the loss. The gradients are then used by the optimizer to update weights and biases.

The current implementation calculates gradients for its supported dense network and updates parameters using full-batch gradient descent.
