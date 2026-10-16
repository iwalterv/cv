# Prueba de 30 s de punta a punta (paso 3.8), 15-oct-2026

Resultado: `video.mp4` (37,6 s, 1920x1080, 30 fps). Solo local, no está en git y no se publicó.

| Etapa | Cómo | Costo |
|---|---|---|
| Guion | Párrafo de `voz/parrafo-prueba.md` | — |
| Voz | ElevenLabs (web), Holden, Eleven v4 → `voz.mp3` (36,4 s) | ~580 créditos de ElevenLabs |
| Tiempos | `ffmpeg silencedetect` para ubicar las pausas → `tiempos.json` | Gratis |
| Imágenes | `scripts/generar_escenas.py escenas.json` (Seedream 5.0 Flash + ficha de Red) | 3 créditos de Higgsfield |
| Montaje | `scripts/montar_video.py tiempos.json` (zoom lento alternado + fundido de 0,3 s) | Gratis, ~12 s de proceso |

Pendientes para el piloto:
- Voz por **API de ElevenLabs** (en vez de la web) para automatizarlo.
- Tiempos con **Whisper local** (palabra por palabra) en vez de pausas, para videos de 12 min.
- La escena 03 no mostró bien "su propia parcela abandonada": en las escenas con dos ideas hay que simplificar el prompt.
