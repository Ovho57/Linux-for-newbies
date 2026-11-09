"""Local JSON project persistence."""
import json
from pathlib import Path
from .architecture import LayerSpec


def default_project_dir() -> Path:
    return Path.home() / "Documents" / "NeuralForge" / "projects"


def save_project(path: str | Path, name: str, layers: list[LayerSpec], model_file: str | None = None):
    target = Path(path)
    target.mkdir(parents=True, exist_ok=True)
    data = {"name": name, "layers": [layer.to_dict() for layer in layers], "model_file": model_file}
    file_path = target / "project.json"
    file_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return file_path


def load_project(path: str | Path):
    file_path = Path(path)
    if file_path.is_dir():
        file_path = file_path / "project.json"
    data = json.loads(file_path.read_text(encoding="utf-8"))
    layers = [LayerSpec.from_dict(item) for item in data["layers"]]
    return data, layers
