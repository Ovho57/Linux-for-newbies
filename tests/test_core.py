import tempfile
import unittest
from pathlib import Path
import numpy as np
from neuralforge.core.architecture import LayerSpec,validate_architecture
from neuralforge.core.math_engine import safe_evaluate,weighted_sum_trace
from neuralforge.core.mlp import MLP
from neuralforge.core.project_store import save_project,load_project
from neuralforge.core.model_io import save_model_bundle,load_model_bundle,architecture_dimensions
from neuralforge.core.model_builder import build_mlp

class MathTests(unittest.TestCase):
 def test_expression(self):self.assertAlmostEqual(safe_evaluate("sin(pi / 2) + 3**2"),10)
 def test_no_code_execution(self):
  with self.assertRaises((ValueError,TypeError)):safe_evaluate("__import__('os').system('echo unsafe')")
 def test_weighted_sum(self):self.assertAlmostEqual(weighted_sum_trace([.5,.8],[2,3],.2)["z"],3.6)
class ArchitectureTests(unittest.TestCase):
 def test_valid(self):self.assertEqual(validate_architecture([LayerSpec("Input",2),LayerSpec("Dense",4,"tanh"),LayerSpec("Output",1,"sigmoid")]),[])
 def test_dimensions(self):self.assertEqual(architecture_dimensions([LayerSpec("Input",2),LayerSpec("Dense",4),LayerSpec("Output",1)]),[2,4,1])
class ModelTests(unittest.TestCase):
 def test_xor(self):
  x=np.array([[0,0],[0,1],[1,0],[1,1]],float); y=np.array([[0],[1],[1],[0]],float); m=MLP([2,8,1],seed=4); h=m.train(x,y,5000,.1)
  self.assertLess(h[-1],h[0]); self.assertEqual((m.predict(x)>.5).astype(int).reshape(-1).tolist(),[0,1,1,0])
 def test_bundle(self):
  layers=[LayerSpec("Input",2),LayerSpec("Dense",3,"tanh"),LayerSpec("Output",1,"sigmoid")]; m=MLP([2,3,1]); expected=m.predict([[.1,.9]])
  with tempfile.TemporaryDirectory() as d:
   save_model_bundle(Path(d)/"bundle",m,layers,"Test"); loaded,_,cfg=load_model_bundle(Path(d)/"bundle")
   np.testing.assert_allclose(loaded.predict([[.1,.9]]),expected); self.assertEqual(cfg["name"],"Test")
class AdvancedModelTests(unittest.TestCase):
 def test_gradient_trace_shapes(self):
  m=MLP([2,3,1],seed=3,activations=["relu","sigmoid"])
  trace=m.trace_gradients([[1.,0.]],[[1.]])
  self.assertEqual(trace["weight_gradients"][0].shape,(2,3))
  self.assertEqual(trace["weight_gradients"][1].shape,(3,1))
  self.assertTrue(np.isfinite(trace["loss"]))
 def test_dropout_layer_is_executed(self):
  layers=[LayerSpec("Input",3),LayerSpec("Dense",5,"relu"),LayerSpec("Dropout",5,"linear",.35),LayerSpec("Output",1,"sigmoid")]
  model=build_mlp(layers)
  self.assertEqual(model.dropout_rates,[.35,0.0])
  self.assertEqual(model.activations,["relu","sigmoid"])
 def test_activation_and_dropout_roundtrip(self):
  model=MLP([2,3,1],activations=["relu","linear"],dropout_rates=[.25,0])
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/"weights.npz"; model.save(path); loaded=MLP.load(path)
   self.assertEqual(loaded.activations,["relu","linear"])
   self.assertEqual(loaded.dropout_rates,[.25,0.0])
class ProjectTests(unittest.TestCase):
 def test_project(self):
  layers=[LayerSpec("Input",2),LayerSpec("Dense",4),LayerSpec("Output",1)]
  with tempfile.TemporaryDirectory() as d:
   save_project(d,"Example",layers); data,loaded=load_project(d); self.assertEqual(data["name"],"Example"); self.assertEqual([x.units for x in loaded],[2,4,1])
if __name__=="__main__":unittest.main()
