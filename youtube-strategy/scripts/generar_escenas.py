"""Genera las escenas de un video con Higgsfield usando la ficha de Red como referencia.

Uso: python3 scripts/generar_escenas.py videos/<video>/escenas.json
Guarda videos/<video>/imagenes/<id>.png y se salta las que ya existen.
"""
import json
import os
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
config_path = Path(sys.argv[1]).resolve()
config = json.loads(config_path.read_text())
out_dir = config_path.parent / "imagenes"
out_dir.mkdir(exist_ok=True)


def build_prompt(scene):
    prompt = config["base"]
    for key, value in scene.items():
        if isinstance(value, str):
            prompt = prompt.replace("{" + key + "}", value)
    return prompt


def generate(scene):
    out = out_dir / f"{scene['id']}.png"
    if out.exists():
        return f"ya existe  {out.name}"
    cmd = ["higgsfield", "generate", "create", config["model"], "--prompt", build_prompt(scene),
           "--image-references", str(ROOT / config["reference"]), *config["params"], "--wait", "--json"]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    try:
        urllib.request.urlretrieve(json.loads(res.stdout)[0]["result_url"], out)
        return f"ok         {out.name}"
    except Exception as e:
        return f"ERROR      {scene['id']}: {e} {res.stderr[-300:]}"


# Starter: máx. 4 trabajos simultáneos en Higgsfield (WORKERS=1 si ya hay otro lote corriendo).
with ThreadPoolExecutor(max_workers=int(os.environ.get("WORKERS", 3))) as pool:
    for line in pool.map(generate, config["scenes"]):
        print(line)
