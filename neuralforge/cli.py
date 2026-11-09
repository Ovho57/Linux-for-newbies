"""Command-line interface for exported NeuralForge model bundles."""
import argparse
import json
import sys
from .core.model_io import load_model_bundle

def main(argv=None):
    parser=argparse.ArgumentParser(prog="neuralforge",description="NeuralForge local model runner")
    sub=parser.add_subparsers(dest="command",required=True)
    run=sub.add_parser("run",help="Run a prediction"); run.add_argument("model_folder"); run.add_argument("--input")
    info=sub.add_parser("info",help="Show model configuration"); info.add_argument("model_folder")
    args=parser.parse_args(argv)
    try:
        model,layers,config=load_model_bundle(args.model_folder)
        if args.command=="info":print(json.dumps(config,indent=2)); return 0
        raw=args.input if args.input is not None else input("Enter comma-separated inputs: ")
        values=[float(v.strip()) for v in raw.split(",") if v.strip()]
        print("Prediction:",model.predict([values])[0]); return 0
    except (OSError,ValueError,KeyError,json.JSONDecodeError) as exc:
        print(f"NeuralForge error: {exc}",file=sys.stderr); return 2

if __name__=="__main__":raise SystemExit(main())
