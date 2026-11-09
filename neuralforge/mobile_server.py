"""Token-protected local mobile companion for exported-model inference."""
from __future__ import annotations
import argparse
import secrets
from pathlib import Path

HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#e9dfca"><title>NeuralForge Mobile</title>
<style>
:root{font-family:system-ui,sans-serif;color:#302b23;background:#eee8dc}body{margin:0;padding:22px;max-width:680px;margin:auto}
header,main{background:#fbf8f1;border:1px solid #d4c7ae;border-radius:12px;padding:18px;margin:12px 0}
h1{font-family:Georgia,serif;margin:0 0 6px}p{line-height:1.5;color:#62594c}
input,button{font:inherit;padding:12px;border:1px solid #b8aa91;border-radius:8px;width:100%;box-sizing:border-box;margin:7px 0}
button{background:#ded0b5;font-weight:650;cursor:pointer}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f0eadf;padding:12px;border-radius:8px}
</style></head><body><header><h1>NeuralForge</h1><p>Mobile model testing desk</p></header>
<main><label>Access token<input id="token" type="password" autocomplete="off" placeholder="Paste token from your computer terminal"></label>
<label>Model inputs (comma-separated)<input id="values" value="0,1" inputmode="decimal"></label>
<button id="run">Run prediction</button><pre id="result">Waiting for input…</pre></main>
<script>
document.getElementById('run').addEventListener('click',async()=>{
 const out=document.getElementById('result');out.textContent='Running…';
 try{
  const values=document.getElementById('values').value.split(',').map(v=>Number(v.trim()));
  if(values.some(v=>!Number.isFinite(v)))throw new Error('Enter only numeric values.');
  const response=await fetch('/api/predict',{method:'POST',headers:{'Content-Type':'application/json','X-NeuralForge-Token':document.getElementById('token').value},body:JSON.stringify({values})});
  const data=await response.json();if(!response.ok)throw new Error(data.detail||'Prediction failed');
  out.textContent=JSON.stringify(data,null,2);
 }catch(e){out.textContent='Error: '+e.message;}
});
</script></body></html>"""

def create_app(model_path, token):
    try:
        from fastapi import FastAPI, Header, HTTPException
        from fastapi.responses import HTMLResponse
    except ImportError as exc:
        raise ImportError("Install mobile dependencies: pip install 'neuralforge-ai[mobile]'") from exc
    from .core.model_io import load_model_bundle
    model, _layers, config = load_model_bundle(model_path)
    app = FastAPI(title="NeuralForge Mobile Companion", docs_url=None, redoc_url=None)

    @app.get("/", response_class=HTMLResponse)
    def home():
        return HTML

    @app.get("/api/health")
    def health():
        return {"status": "ready", "model": config.get("name", "NeuralForge model")}

    @app.post("/api/predict")
    def predict(payload: dict, x_neuralforge_token: str = Header(default="")):
        if not secrets.compare_digest(x_neuralforge_token, token):
            raise HTTPException(status_code=401, detail="Invalid access token.")
        values = payload.get("values")
        if not isinstance(values, list):
            raise HTTPException(status_code=400, detail="Send a numeric values array.")
        try:
            result = model.predict(values)[0].tolist()
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return {"prediction": result, "model": config.get("name", "NeuralForge model")}
    return app

def main():
    parser = argparse.ArgumentParser(description="Run the NeuralForge mobile inference companion.")
    parser.add_argument("--model", required=True, help="Path to an exported model bundle")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    token = secrets.token_urlsafe(24)
    app = create_app(Path(args.model), token)
    print("NeuralForge Mobile Companion")
    print(f"Open http://{args.host}:{args.port} in a browser.")
    print(f"Access token: {token}")
    if args.host == "0.0.0.0":
        print("LAN mode enabled. Share the token only with devices you trust.")
    import uvicorn
    uvicorn.run(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()
