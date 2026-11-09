"""Architecture definitions and validation for feed-forward networks."""
from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class LayerSpec:
    kind: str
    units: int
    activation: str = "relu"
    dropout: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LayerSpec":
        return cls(**data)


def validate_architecture(layers: list[LayerSpec]) -> list[str]:
    errors: list[str] = []
    if len(layers) < 2:
        return ["A network needs at least an input and output layer."]
    if layers[0].kind.lower() != "input":
        errors.append("The first layer must be an Input layer.")
    if layers[-1].kind.lower() != "output":
        errors.append("The final layer must be an Output layer.")
    for index, layer in enumerate(layers):
        if layer.units < 1:
            errors.append(f"Layer {index + 1}: units must be at least 1.")
        if layer.kind.lower() not in {"input", "dense", "dropout", "output", "conv1d", "rnn", "custom"}:
            errors.append(f"Layer {index + 1}: unsupported layer type '{layer.kind}'.")
        if layer.kind.lower() == "dropout" and not 0 <= layer.dropout < 1:
            errors.append(f"Layer {index + 1}: dropout must be in [0, 1).")
        if layer.activation not in {"relu", "sigmoid", "tanh", "softmax", "linear"}:
            errors.append(f"Layer {index + 1}: unsupported activation '{layer.activation}'.")
    return errors


def trainable_dimensions(layers: list[LayerSpec]) -> list[tuple[int, int]]:
    """Return (input_units, output_units) for each trainable Dense/Output layer."""
    dimensions: list[tuple[int, int]] = []
    previous = layers[0].units if layers else 0
    for layer in layers[1:]:
        if layer.kind.lower() in {"dense", "output"}:
            dimensions.append((previous, layer.units))
            previous = layer.units
    return dimensions
