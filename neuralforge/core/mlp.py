"""Configurable NumPy neural network with dropout and inspectable backpropagation."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np


class MLP:
    """Dense network. Activations/dropout are configured per trainable layer.

    Dropout uses inverted scaling during training and is disabled for inference.
    trace_forward() exposes every pre-activation and activation tensor.
    trace_gradients() returns forward tensors, deltas and parameter gradients.
    """
    ACTIVATIONS = {"linear", "relu", "sigmoid", "tanh", "softmax"}

    def __init__(self, dimensions: list[int], seed: int = 7,
                 activations: list[str] | None = None,
                 dropout_rates: list[float] | None = None):
        if len(dimensions) < 2 or any(int(v) < 1 for v in dimensions):
            raise ValueError("Provide at least two positive layer dimensions.")
        self.dimensions = [int(v) for v in dimensions]
        count = len(self.dimensions) - 1
        self.activations = list(activations or ["tanh"] * (count - 1) + ["sigmoid"])
        self.dropout_rates = list(dropout_rates or [0.0] * count)
        if len(self.activations) != count or len(self.dropout_rates) != count:
            raise ValueError("One activation and dropout rate is required per trainable layer.")
        if any(a not in self.ACTIVATIONS for a in self.activations):
            raise ValueError(f"Activations must be one of {sorted(self.ACTIVATIONS)}.")
        if any(not 0 <= float(r) < 1 for r in self.dropout_rates):
            raise ValueError("Dropout rates must be in [0, 1).")
        self.dropout_rates = [float(r) for r in self.dropout_rates]
        rng = np.random.default_rng(seed)
        self.weights = [rng.normal(0, np.sqrt(2 / self.dimensions[i]),
                                   (self.dimensions[i], self.dimensions[i + 1]))
                        for i in range(count)]
        self.biases = [np.zeros((1, self.dimensions[i + 1])) for i in range(count)]
        self.last_trace = None

    @staticmethod
    def _sigmoid(z):
        z = np.clip(z, -40, 40)
        return 1.0 / (1.0 + np.exp(-z))

    @classmethod
    def activate(cls, z, name):
        if name == "linear": return z
        if name == "relu": return np.maximum(0, z)
        if name == "sigmoid": return cls._sigmoid(z)
        if name == "tanh": return np.tanh(z)
        if name == "softmax":
            shifted = z - np.max(z, axis=1, keepdims=True)
            exp = np.exp(shifted)
            return exp / np.sum(exp, axis=1, keepdims=True)
        raise ValueError(f"Unknown activation: {name}")

    @staticmethod
    def activation_derivative(z, a, name):
        if name == "linear": return np.ones_like(z)
        if name == "relu": return (z > 0).astype(float)
        if name == "sigmoid": return a * (1 - a)
        if name == "tanh": return 1 - a ** 2
        if name == "softmax":
            # Diagonal approximation for the educational MSE trainer.
            return a * (1 - a)
        raise ValueError(f"Unknown activation: {name}")

    def trace_forward(self, x, training=False, rng=None):
        rng = rng or np.random.default_rng(0)
        current = np.asarray(x, dtype=float)
        if current.ndim == 1: current = current.reshape(1, -1)
        if current.ndim != 2 or current.shape[1] != self.dimensions[0]:
            raise ValueError(f"Expected input shape (batch, {self.dimensions[0]}).")
        activations, pre_activations, masks = [current], [], []
        for i, (weight, bias) in enumerate(zip(self.weights, self.biases)):
            z = current @ weight + bias
            a = self.activate(z, self.activations[i])
            mask = np.ones_like(a)
            rate = self.dropout_rates[i] if training and i < len(self.weights) - 1 else 0.0
            if rate:
                mask = (rng.random(a.shape) >= rate).astype(float) / (1.0 - rate)
                a = a * mask
            pre_activations.append(z)
            masks.append(mask)
            activations.append(a)
            current = a
        return {"activations": activations, "pre_activations": pre_activations,
                "dropout_masks": masks}

    def forward(self, x):
        trace = self.trace_forward(x, training=False)
        self.last_trace = trace
        return trace["activations"]

    def predict(self, x):
        return self.forward(np.atleast_2d(x))[-1]

    def trace_gradients(self, x, y):
        """Return tensor-level forward/backward details without changing weights."""
        x, y = np.asarray(x, float), np.asarray(y, float)
        if x.ndim == 1: x = x.reshape(1, -1)
        if y.ndim == 1: y = y.reshape(1, -1)
        if len(x) != len(y) or x.shape[1] != self.dimensions[0] or y.shape[1] != self.dimensions[-1]:
            raise ValueError("Input/target shapes do not match the model.")
        trace = self.trace_forward(x, training=False)
        acts, zs = trace["activations"], trace["pre_activations"]
        error = acts[-1] - y
        delta = (2.0 / error.size) * error * self.activation_derivative(
            zs[-1], acts[-1], self.activations[-1])
        deltas = [None] * len(self.weights)
        grad_w, grad_b = [None] * len(self.weights), [None] * len(self.weights)
        for i in reversed(range(len(self.weights))):
            deltas[i] = delta.copy()
            grad_w[i] = acts[i].T @ delta
            grad_b[i] = np.sum(delta, axis=0, keepdims=True)
            if i:
                delta = (delta @ self.weights[i].T) * self.activation_derivative(
                    zs[i-1], acts[i], self.activations[i-1])
        return {**trace, "target": y, "error": error, "deltas": deltas,
                "weight_gradients": grad_w, "bias_gradients": grad_b,
                "loss": float(np.mean(error ** 2))}

    def train(self, x, y, epochs=500, learning_rate=0.1, callback=None):
        x, y = np.asarray(x, float), np.asarray(y, float)
        if x.ndim != 2 or y.ndim != 2 or len(x) != len(y):
            raise ValueError("X and y must be 2D arrays with the same number of rows.")
        if x.shape[1] != self.dimensions[0] or y.shape[1] != self.dimensions[-1]:
            raise ValueError("Dataset dimensions do not match the network architecture.")
        if epochs < 1 or learning_rate <= 0:
            raise ValueError("Epochs and learning rate must be positive.")
        history, rng = [], np.random.default_rng()
        for epoch in range(int(epochs)):
            trace = self.trace_forward(x, training=True, rng=rng)
            acts, zs, masks = trace["activations"], trace["pre_activations"], trace["dropout_masks"]
            prediction = acts[-1]
            error = prediction - y
            loss = float(np.mean(error ** 2))
            delta = (2.0 / error.size) * error * self.activation_derivative(
                zs[-1], prediction, self.activations[-1])
            grad_w, grad_b = [None] * len(self.weights), [None] * len(self.biases)
            for i in reversed(range(len(self.weights))):
                grad_w[i] = acts[i].T @ delta
                grad_b[i] = np.sum(delta, axis=0, keepdims=True)
                if i:
                    delta = (delta @ self.weights[i].T) * self.activation_derivative(
                        zs[i-1], acts[i], self.activations[i-1]) * masks[i-1]
            for i in range(len(self.weights)):
                self.weights[i] -= learning_rate * grad_w[i]
                self.biases[i] -= learning_rate * grad_b[i]
            history.append(loss)
            if callback and (epoch == 0 or (epoch + 1) % max(1, epochs // 100) == 0 or epoch == epochs - 1):
                callback(epoch + 1, int(epochs), loss)
        return history

    def save(self, path):
        payload = {"metadata": np.asarray(json.dumps({
            "dimensions": self.dimensions, "activations": self.activations,
            "dropout_rates": self.dropout_rates}))}
        for i, (weight, bias) in enumerate(zip(self.weights, self.biases)):
            payload[f"W{i}"], payload[f"b{i}"] = weight, bias
        np.savez(path, **payload)

    @classmethod
    def load(cls, path, dimensions=None):
        with np.load(path, allow_pickle=False) as data:
            if "metadata" in data:
                meta = json.loads(str(data["metadata"].item()))
                dimensions = meta["dimensions"]
                model = cls(dimensions, activations=meta["activations"],
                            dropout_rates=meta["dropout_rates"])
            else:
                model = cls(dimensions)
            for i in range(len(model.weights)):
                model.weights[i], model.biases[i] = data[f"W{i}"].copy(), data[f"b{i}"].copy()
        return model
