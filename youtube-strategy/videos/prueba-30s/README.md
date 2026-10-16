# Prueba de 30 s de punta a punta (paso 3.8), 15-oct-2026

Resultado: `video.mp4` (37,6 s, 1920x1080, 30 fps). Solo local, no está en git y no se publicó.

| Etapa | Cómo | Costo |
|---|---|---|
| Guion | Párrafo de `voz/parrafo-prueba.md` | — |
| Voz | ElevenLabs (web), Holden, Eleven v4 → `voz.mp3` (36,4 s) | ~580 créditos de ElevenLabs |
| Tiempos | `ffmpeg silencedetect` para ubicar las pausas → `tiempos.json` | Gratis |
| Imágenes | `scripts/generar_escenas.py escenas.json` (Seedream 5.0 Flash + ficha de Red) | 3 créditos de Higgsfield |
| Subtítulos | `scripts/subtitulos.py tiempos.json`: whisper.cpp (large-v3-turbo, local) para los tiempos de cada palabra + texto del guion → `subtitulos.ass` (quemados) y `subtitulos.srt` (para YouTube) | Gratis |
| Montaje | `scripts/montar_video.py tiempos.json` (zoom lento alternado + fundido de 0,3 s) | Gratis, ~12 s de proceso |

Pendientes para el piloto:
- Voz por **API de ElevenLabs** (en vez de la web) para automatizarlo.
- Usar los tiempos de Whisper también para cortar las escenas (hoy salen de las pausas).
- "BRIEFLY" en rojo sobre fondo rojo se lee menos: en escenas rojas, resaltar en amarillo o blanco.
- La escena 03 no mostró bien "su propia parcela abandonada": en las escenas con dos ideas hay que simplificar el prompt.
