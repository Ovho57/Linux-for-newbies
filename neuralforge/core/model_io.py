"""Portable model bundle export and loading."""
import json
from pathlib import Path
from .architecture import LayerSpec
from .mlp import MLP

def architecture_dimensions(layers):
    if not layers or layers[0].kind.lower()!="input":raise ValueError("Architecture must begin with Input.")
    dims=[layers[0].units]
    for layer in layers[1:]:
        if layer.kind.lower() in {"dense","output"}:dims.append(layer.units)
    if len(dims)<2:raise ValueError("Architecture needs a trainable layer.")
    return dims

def save_model_bundle(destination,model,layers,name="NeuralForgeModel"):
    target=Path(destination); target.mkdir(parents=True,exist_ok=True)
    model.save(target/"weights.npz")
    config={"name":name,"format_version":1,"engine":"NeuralForge NumPy MLP",
            "dimensions":model.dimensions,"activations":model.activations,"dropout_rates":model.dropout_rates,"layers":[layer.to_dict() for layer in layers]}
    (target/"config.json").write_text(json.dumps(config,indent=2),encoding="utf-8")
    script='''"""Standalone prediction example for an exported NeuralForge model."""
import json
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
config=json.loads((HERE/"config.json").read_text(encoding="utf-8"))
weights=np.load(HERE/"weights.npz")
def activate(z, name):
    if name == "linear": return z
    if name == "relu": return np.maximum(0, z)
    if name == "tanh": return np.tanh(z)
    if name == "sigmoid": return 1/(1+np.exp(-np.clip(z,-40,40)))
    if name == "softmax":
        e=np.exp(z-np.max(z,axis=1,keepdims=True)); return e/e.sum(axis=1,keepdims=True)
    raise ValueError("Unknown activation: "+name)
def predict(values):
    x=np.asarray(values,dtype=float).reshape(1,-1)
    if x.shape[1]!=config["dimensions"][0]:
        raise ValueError(f"Expected {config['dimensions'][0]} input values")
    for i in range(len(config["dimensions"])-1):
        x=x@weights[f"W{i}"]+weights[f"b{i}"]
        x=activate(x,config["activations"][i])
    return x[0]
if __name__=="__main__":
    values=[float(v.strip()) for v in input("Inputs: ").split(",")]
    print("Prediction:",predict(values))
'''
    (target/"predict.py").write_text(script,encoding="utf-8")
    (target/"requirements.txt").write_text("numpy>=1.26\n",encoding="utf-8")
    (target/"README.md").write_text(f"# {name}\n\nExported from NeuralForge AI.\n\nInstall with: python -m pip install -r requirements.txt\nRun: python predict.py\n",encoding="utf-8")
    return target

def load_model_bundle(folder):
    folder=Path(folder); config=json.loads((folder/"config.json").read_text(encoding="utf-8"))
    model=MLP.load(folder/"weights.npz",config["dimensions"])
    layers=[LayerSpec.from_dict(item) for item in config["layers"]]
    return model,layers,config
