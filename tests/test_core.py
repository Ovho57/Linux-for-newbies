import tempfile
import unittest
from pathlib import Path
import numpy as np

from neuralforge.core.architecture import LayerSpec, validate_architecture
from neuralforge.core.math_engine import safe_evaluate, weighted_sum_trace
from neuralforge.core.mlp import MLP
from neuralforge.core.project_store import save_project, load_project


class MathEngineTests(unittest.TestCase):
    def test_safe_expression(self):
        self.assertAlmostEqual(safe_evaluate("sin(pi / 2) + 3**2"), 10.0)

    def test_rejects_python_execution(self):
        with self.assertRaises((ValueError, TypeError)):
            safe_evaluate("__import__('os').system('echo unsafe')")

    def test_weighted_sum_trace(self):
        trace = weighted_sum_trace([0.5, 0.8], [2, 3], 0.2)
        self.assertAlmostEqual(trace["z"], 3.6)


class ArchitectureTests(unittest.TestCase):
    def test_valid_architecture(self):
        layers = [LayerSpec("Input", 2), LayerSpec("Dense", 4), LayerSpec("Output", 1)]
        self.assertEqual(validate_architecture(layers), [])

    def test_requires_input_and_output(self):
        self.assertTrue(validate_architecture([LayerSpec("Dense", 3), LayerSpec("Output", 1)]))


class MLPTests(unittest.TestCase):
    def test_xor_learns(self):
        x = np.array([[0,0],[0,1],[1,0],[1,1]], dtype=float)
        y = np.array([[0],[1],[1],[0]], dtype=float)
        model = MLP([2, 8, 1], seed=4)
        history = model.train(x, y, epochs=5000, learning_rate=0.1)
        predictions = (model.predict(x) > 0.5).astype(int)
        self.assertLess(history[-1], history[0])
        self.assertEqual(predictions.reshape(-1).tolist(), [0, 1, 1, 0])

    def test_save_and_load(self):
        model = MLP([2, 3, 1])
        expected = model.predict([[0.2, 0.7]])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "weights.npz"
            model.save(path)
            loaded = MLP.load(path, [2, 3, 1])
            np.testing.assert_allclose(loaded.predict([[0.2, 0.7]]), expected)


class ProjectStoreTests(unittest.TestCase):
    def test_project_roundtrip(self):
        layers = [LayerSpec("Input", 2), LayerSpec("Dense", 4), LayerSpec("Output", 1)]
        with tempfile.TemporaryDirectory() as directory:
            save_project(directory, "Example", layers)
            data, loaded = load_project(directory)
            self.assertEqual(data["name"], "Example")
            self.assertEqual([layer.units for layer in loaded], [2, 4, 1])


if __name__ == "__main__":
    unittest.main()
