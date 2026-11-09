"""Architecture-to-execution helpers."""
from .architecture import LayerSpec
from .mlp import MLP


def build_mlp(layers, seed=7):
    """Build the executable dense model from editor layer specifications."""
    if not layers or layers[0].kind.lower() != "input":
        raise ValueError("Architecture must start with Input.")
    dimensions = [layers[0].units]
    activations, dropout = [], []
    pending_dropout = 0.0
    for layer in layers[1:]:
        kind = layer.kind.lower()
        if kind == "dropout":
            if not 0 <= layer.dropout < 1:
                raise ValueError("Dropout rate must be in [0, 1).")
            if dropout:
                dropout[-1] = layer.dropout
            else:
                pending_dropout = layer.dropout
            continue
        if kind not in {"dense", "output"}:
            raise ValueError(f"Layer type {layer.kind!r} is not executable by the NumPy dense engine.")
        dimensions.append(layer.units)
        activations.append(layer.activation)
        dropout.append(max(pending_dropout, layer.dropout))
        pending_dropout = 0.0
    if len(dimensions) < 2:
        raise ValueError("Architecture needs at least one Dense or Output layer.")
    return MLP(dimensions, seed=seed, activations=activations, dropout_rates=dropout)
