"""Optional PyTorch execution backend for dense, Conv1D and recurrent networks."""
from __future__ import annotations

try:
    import torch
    from torch import nn
except ImportError as exc:  # optional dependency
    raise ImportError("Install the optional backend with: pip install 'neuralforge-ai[torch]'") from exc

_CUSTOM_LAYERS = {}

def register_layer(name, factory):
    """Register a trusted custom nn.Module factory under a unique layer name."""
    if not name or not callable(factory):
        raise ValueError("A non-empty name and callable factory are required.")
    if name in _CUSTOM_LAYERS:
        raise ValueError(f"Layer {name!r} is already registered.")
    _CUSTOM_LAYERS[name] = factory

def _activation(name):
    choices = {"relu": nn.ReLU, "sigmoid": nn.Sigmoid, "tanh": nn.Tanh,
               "linear": nn.Identity, "softmax": lambda: nn.Softmax(dim=-1),
               "gelu": nn.GELU, "leaky_relu": nn.LeakyReLU}
    if name not in choices:
        raise ValueError(f"Unsupported activation: {name}")
    return choices[name]()

class NeuralForgeTorchModel(nn.Module):
    """Executable sequential network. Conv1D input: [batch, channels, length].
    RNN input: [batch, sequence_length, features]. Dense accepts flattened tensors.
    """
    def __init__(self, layers, device=None):
        super().__init__()
        if len(layers) < 2 or layers[0].kind.lower() != "input":
            raise ValueError("Architecture must begin with an Input layer.")
        modules, previous_kind = [], "input"
        previous_units = layers[0].units
        for spec in layers[1:]:
            kind = spec.kind.lower()
            if kind == "dropout":
                modules.append(nn.Dropout(float(spec.dropout)))
            elif kind in {"dense", "output"}:
                modules.extend([nn.Flatten(start_dim=1), nn.LazyLinear(spec.units),
                                _activation(spec.activation)])
            elif kind in {"conv1d", "convolution1d"}:
                modules.extend([nn.Conv1d(previous_units, spec.units, kernel_size=3, padding=1),
                                _activation(spec.activation)])
                previous_units = spec.units
            elif kind in {"rnn", "recurrent"}:
                modules.append(nn.RNN(previous_units, spec.units, batch_first=True))
                modules.append(_LastSequence())
                modules.append(_activation(spec.activation))
                previous_units = spec.units
            elif spec.kind in _CUSTOM_LAYERS:
                module = _CUSTOM_LAYERS[spec.kind](spec)
                if not isinstance(module, nn.Module):
                    raise TypeError("Custom layer factory must return torch.nn.Module.")
                modules.append(module)
            else:
                raise ValueError(f"Unsupported executable layer: {spec.kind}")
            previous_kind = kind
        self.network = nn.Sequential(*modules)
        requested = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.device = torch.device(requested)
        if self.device.type == "cuda" and not torch.cuda.is_available():
            raise RuntimeError("CUDA was requested but is not available.")
        self.to(self.device)

    def forward(self, x):
        return self.network(torch.as_tensor(x, dtype=torch.float32, device=self.device))

    def fit(self, x, y, epochs=100, learning_rate=0.001, callback=None):
        self.train()
        inputs = torch.as_tensor(x, dtype=torch.float32, device=self.device)
        targets = torch.as_tensor(y, dtype=torch.float32, device=self.device)
        optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate)
        loss_fn = nn.MSELoss()
        history = []
        for epoch in range(int(epochs)):
            optimizer.zero_grad(set_to_none=True)
            predictions = self(inputs)
            loss = loss_fn(predictions, targets)
            loss.backward()
            optimizer.step()
            value = float(loss.detach().cpu())
            history.append(value)
            if callback:
                callback(epoch + 1, int(epochs), value)
        self.eval()
        return history

    def gradient_trace(self, x, y):
        """Return named parameter gradients and loss for tensor-level inspection."""
        self.train()
        self.zero_grad(set_to_none=True)
        inputs = torch.as_tensor(x, dtype=torch.float32, device=self.device)
        targets = torch.as_tensor(y, dtype=torch.float32, device=self.device)
        predictions = self(inputs)
        loss = nn.functional.mse_loss(predictions, targets)
        loss.backward()
        result = {"loss": float(loss.detach().cpu()), "prediction": predictions.detach().cpu().numpy(),
                  "gradients": {name: p.grad.detach().cpu().numpy().copy()
                                for name, p in self.named_parameters() if p.grad is not None}}
        self.eval()
        return result

class _LastSequence(nn.Module):
    def forward(self, output):
        sequence, _state = output
        return sequence[:, -1, :]
