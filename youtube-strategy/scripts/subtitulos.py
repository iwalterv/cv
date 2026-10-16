"""Genera los subtítulos de un video: quemados en pantalla (.ass) y para subir a YouTube (.srt).

Uso: python3 scripts/subtitulos.py videos/<video>/tiempos.json
- Transcribe <audio> con whisper.cpp (tiempos palabra por palabra) si no existe palabras.json.
- El TEXTO sale del guion (los "text" de tiempos.json); de Whisper solo se toman los tiempos,
  así los nombres propios quedan bien escritos aunque Whisper los oiga mal ("Melcombe" → "Malcolm").
- subtitulos.ass: 2-4 palabras por pantalla, blanco con contorno negro y la palabra que se dice en rojo de marca.
- subtitulos.srt: frases completas, para subir como subtítulos en YouTube Studio.
"""
import difflib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

WHISPER_MODEL = Path.home() / "whisper-models" / "ggml-large-v3-turbo.bin"
MAX_WORDS = 4          # palabras por pantalla
RED = "&H002828D6&"    # #D62828 (ASS usa BGR)
WHITE = "&H00FFFFFF&"

config_path = Path(sys.argv[1]).resolve()
base = config_path.parent
config = json.loads(config_path.read_text())
words_path = base / "palabras.json"


def transcribe():
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "audio.wav"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(base / config["audio"]),
                        "-ar", "16000", "-ac", "1", str(wav)], check=True)
        subprocess.run(["whisper-cli", "-m", str(WHISPER_MODEL), "-f", str(wav), "-l", "en",
                        "-ml", "1", "-sow", "-oj", "-of", str(words_path.with_suffix("")), "-np"],
                       check=True, capture_output=True)


def norm(word):
    return re.sub(r"[^a-z0-9']", "", word.lower())


if not words_path.exists():
    transcribe()
heard = [(s["offsets"]["from"] / 1000, s["offsets"]["to"] / 1000, s["text"].strip())
         for s in json.loads(words_path.read_text())["transcription"] if s["text"].strip()]

# Palabras del guion, recordando dónde termina cada frase (para cortar los subtítulos ahí).
script = []
for scene in config["scenes"]:
    script += scene["text"].split()

# Alinea guion ↔ Whisper. Los bloques distintos ("1347," vs "1347,", "two hundred" vs "200")
# reparten el tiempo de lo que oyó Whisper entre las palabras del guion.
times = [None] * len(script)
matcher = difflib.SequenceMatcher(a=[norm(w) for w in script], b=[norm(w[2]) for w in heard], autojunk=False)
for tag, a0, a1, b0, b1 in matcher.get_opcodes():
    if tag == "equal":
        for k in range(a1 - a0):
            times[a0 + k] = heard[b0 + k][:2]
    elif a1 > a0:
        start = heard[b0][0] if b1 > b0 else (times[a0 - 1][1] if a0 else 0.0)
        end = heard[b1 - 1][1] if b1 > b0 else start + 0.3 * (a1 - a0)
        step = (end - start) / (a1 - a0)
        for k in range(a1 - a0):
            times[a0 + k] = (start + k * step, start + (k + 1) * step)

# Agrupa en pantallas de hasta MAX_WORDS, cortando después de puntuación.
groups, current = [], []
for i, word in enumerate(script):
    current.append(i)
    if len(current) == MAX_WORDS or re.search(r"[.,?!…:;]$", word):
        groups.append(current)
        current = []
if current:
    groups.append(current)


def ts_ass(t):
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def ts_srt(t):
    return f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{int(t % 60):02d},{int(t * 1000 % 1000):03d}"


def clean(word):
    # Sin puntuación final en pantalla (más limpio), salvo ? y !.
    return re.sub(r"[.,;:…]+$", "", word)


events = []
for g, idx in enumerate(groups):
    group_end = times[groups[g + 1][0]][0] if g + 1 < len(groups) else times[idx[-1]][1] + 0.4
    for j, i in enumerate(idx):
        start = times[i][0] if j else times[idx[0]][0]
        end = times[idx[j + 1]][0] if j + 1 < len(idx) else group_end
        if end <= start:
            continue
        text = " ".join((f"{{\\c{RED}}}{clean(script[k]).upper()}{{\\c{WHITE}}}" if k == i
                         else clean(script[k]).upper()) for k in idx)
        events.append(f"Dialogue: 0,{ts_ass(start)},{ts_ass(end)},Caption,,0,0,0,,{text}")

ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Arial Black,78,{WHITE},{WHITE},&H00000000&,&H80000000&,0,0,0,0,100,100,1,0,1,6,3,2,80,80,70,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(events) + "\n"
(base / "subtitulos.ass").write_text(ass)

# SRT por frase (cortando en . ? !, y también en comas si la frase pasa de 12 palabras) para YouTube.
srt, sentence = [], []
for i, word in enumerate(script):
    sentence.append(i)
    long_enough = len(sentence) >= 12 and word.endswith(",")
    if re.search(r"[.?!]$", word) or long_enough or i == len(script) - 1:
        srt.append((times[sentence[0]][0], times[sentence[-1]][1], " ".join(script[k] for k in sentence)))
        sentence = []
(base / "subtitulos.srt").write_text(
    "\n".join(f"{n}\n{ts_srt(a)} --> {ts_srt(b)}\n{t}\n" for n, (a, b, t) in enumerate(srt, 1)))
print(f"ok  subtitulos.ass ({len(events)} eventos)  subtitulos.srt ({len(srt)} frases)")
