"""Genera las imágenes de prueba de Red (paso 3.7) con varios modelos de Higgsfield.

Uso: python3 scripts/generar_prueba_red.py
Lee imagenes/prueba-red/prompts.json y guarda imagenes/prueba-red/<modelo>/<escena>.png.
Se salta las imágenes que ya existen.
"""
import json
import subprocess
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

DIR = Path(__file__).resolve().parent.parent / "imagenes" / "prueba-red"
config = json.loads((DIR / "prompts.json").read_text())


def build_prompt(scene):
    prompt = config["base"]
    for key, value in scene.items():
        prompt = prompt.replace("{" + key + "}", value)
    return prompt


def generate(model, scene):
    out = DIR / model["id"] / f"{scene['id']}.png"
    if out.exists():
        return f"ya existe  {out.relative_to(DIR)}"
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["higgsfield", "generate", "create", model["job"], "--prompt", build_prompt(scene),
           *model["params"], "--wait", "--json"]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    try:
        job = json.loads(res.stdout)[0]
        urllib.request.urlretrieve(job["result_url"], out)
        return f"ok         {out.relative_to(DIR)}"
    except Exception as e:
        return f"ERROR      {model['id']}/{scene['id']}: {e} {res.stderr[-300:]}"


jobs = [(m, s) for m in config["models"] for s in config["scenes"]]
with ThreadPoolExecutor(max_workers=3) as pool:  # Starter: máx. 4 trabajos simultáneos
    for line in pool.map(lambda a: generate(*a), jobs):
        print(line)
