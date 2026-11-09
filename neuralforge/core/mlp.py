"""A small NumPy multilayer perceptron with real forward/backprop training."""
from __future__ import annotations
import numpy as np


class MLP:
    def __init__(self, dimensions: list[int], seed: int = 7):
        if len(dimensions) < 2 or any(int(v) < 1 for v in dimensions):
            raise ValueError("Provide at least two positive layer dimensions.")
        self.dimensions = [int(v) for v in dimensions]
        rng = np.random.default_rng(seed)
        self.weights = [rng.normal(0, np.sqrt(2 / dimensions[i]), (dimensions[i], dimensions[i + 1]))
                        for i in range(len(dimensions) - 1)]
        self.biases = [np.zeros((1, dimensions[i + 1])) for i in range(len(dimensions) - 1)]

    @staticmethod
    def _sigmoid(z):
        z = np.clip(z, -40, 40)
        return 1.0 / (1.0 + np.exp(-z))

    def forward(self, x):
        activations = [np.asarray(x, dtype=float)]
        current = activations[0]
        for index, (weight, bias) in enumerate(zip(self.weights, self.biases)):
            z = current @ weight + bias
            current = self._sigmoid(z) if index == len(self.weights) - 1 else np.tanh(z)
            activations.append(current)
        return activations

    def predict(self, x):
        return self.forward(np.atleast_2d(x))[-1]

    def train(self, x, y, epochs=500, learning_rate=0.1, callback=None):
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        if x.ndim != 2 or y.ndim != 2 or len(x) != len(y):
            raise ValueError("X and y must be 2D arrays with the same number of rows.")
        if x.shape[1] != self.dimensions[0] or y.shape[1] != self.dimensions[-1]:
            raise ValueError("Dataset dimensions do not match the network architecture.")
        if epochs < 1 or learning_rate <= 0:
            raise ValueError("Epochs and learning rate must be positive.")
        history = []
        for epoch in range(int(epochs)):
            activations = self.forward(x)
            prediction = activations[-1]
            error = prediction - y
            loss = float(np.mean(error ** 2))
            delta = (2.0 / error.size) * error * prediction * (1.0 - prediction)
            grad_w = [None] * len(self.weights)
            grad_b = [None] * len(self.biases)
            for layer_index in reversed(range(len(self.weights))):
                grad_w[layer_index] = activations[layer_index].T @ delta
                grad_b[layer_index] = np.sum(delta, axis=0, keepdims=True)
                if layer_index > 0:
                    hidden = activations[layer_index]
                    delta = (delta @ self.weights[layer_index].T) * (1.0 - hidden ** 2)
            for i in range(len(self.weights)):
                self.weights[i] -= learning_rate * grad_w[i]
                self.biases[i] -= learning_rate * grad_b[i]
            history.append(loss)
            if callback and (epoch == 0 or (epoch + 1) % max(1, epochs // 100) == 0 or epoch == epochs - 1):
                callback(epoch + 1, int(epochs), loss)
        return history

    def save(self, path):
        payload = {}
        for i, (weight, bias) in enumerate(zip(self.weights, self.biases)):
            payload[f"W{i}"] = weight
            payload[f"b{i}"] = bias
        np.savez(path, **payload)

    @classmethod
    def load(cls, path, dimensions):
        model = cls(dimensions)
        data = np.load(path)
        for i in range(len(model.weights)):
            model.weights[i] = data[f"W{i}"]
            model.biases[i] = data[f"b{i}"]
        return model
