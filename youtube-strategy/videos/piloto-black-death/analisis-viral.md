# Análisis del piloto: qué necesita para tener opciones de hacerse viral

**Siendo honestos:** nadie puede garantizar que un video se haga viral, y menos en un canal nuevo. Lo que sí se puede hacer es maximizar las dos métricas que YouTube usa para decidir si lo muestra a más gente:
1. **CTR** (cuántos hacen clic al ver la miniatura): depende del **título + miniatura**.
2. **Retención** (cuánto del video ven): depende del **gancho, el ritmo y los "bucles abiertos"**.

Con un canal nuevo, YouTube prueba el video con un grupo pequeño. Si el CTR y la retención están por encima del promedio de videos parecidos, lo muestra a un grupo mayor, y así sucesivamente. Por eso los videos de canales nuevos como Ink Explainer (14 M) o Zenn (8 M) pudieron despegar.

## 1. Diagnóstico del guion v1

| Aspecto | v1 | Problema | Cambio en la v2 |
|---|---|---|---|
| **Gancho (0-30 s)** | "It's the spring of 1347… Life is fine" | Empieza tranquilo: es justo cuando más gente se va | Empieza en el peor momento: fiebre, bubón "del tamaño de un huevo", el vecino muerto… y la culpa es de **Júpiter**. Primero el impacto, luego el chiste |
| **Promesa del título** | Se explica en el segundo 25 | Tarde | En el segundo ~15: "Today we're finding out exactly why you wouldn't survive" |
| **Recurso visual propio** | No había | Nada nos distingue de Chat History | **"Survival Meter"**: una barra de "YOUR ODDS" que va bajando con cada sección (100 → 50 → 1 → −10 % por la sangría…). Convierte el video en un juego y es la **firma de la serie** |
| **Bucles abiertos** | Solo uno (el final de "los sobrevivientes") | En el minuto 5-7 no hay motivo para seguir | Se repite la promesa a mitad del video ("if you make it to the end, things get weirdly good. First, though… it gets worse") |
| **Ritmo inicial** | Caffa + mapas (~45 s) | Lento y con un relato discutido | Quitado. Directo de Messina a "no es problema mío" |
| **Participación** | Ninguna | Los comentarios ayudan al algoritmo | Pregunta directa: "Run, pray or wait: which would you have picked? Tell me in the comments" |
| **Ritmo de los chistes** | Texto plano | La IA lee los remates sin pausa | Etiquetas de voz de ElevenLabs v4: `[pause]`, `[sarcastic]`, `[whispers]` en los remates |
| **Duración** | ~10 min | — | ~10,3 min. Bien: más de 8 min (anuncios a mitad) y sin relleno |

Se mantiene lo que ya funcionaba: segunda persona ("you"), humor seco, datos sorprendentes que rompen mitos (la máscara de pico, "Ring Around the Rosie"), el giro final positivo (salarios) y el remate "something more than bread".

## 2. Título y miniatura (lo que decide el CTR)

**Título:** "Why You Wouldn't Survive the Black Death". Es la fórmula probada (Chat History: 1,3-3,8 M con "Why You Wouldn't Survive…") y casi nadie la usa con este tema (máximo 12,6K).

**3 miniaturas para la prueba A/B de YouTube** (Test & Compare, en YouTube Studio: subes 3 y YouTube elige la que logra más tiempo de visualización):

| | Imagen | Texto | Por qué |
|---|---|---|---|
| A | Red con un ramo de flores metido en la nariz, cara de pánico | **FLOWERS?** | Curiosidad: "¿flores contra la peste?" (se responde en el min. 5) |
| B | Red mirando una moneda en el aire | **50/50?** | Ventaja: la moneda conecta con el "Survival Meter" |
| C | Red y una rata enorme mirándose fijamente | **1348?** | Clásica, clara a tamaño de celular |

Reglas de nuestra guía (paso 2): 1 a 3 palabras, la palabra clave en rojo, Red grande con una emoción fuerte y una sola idea. Se hacen con Nano Banana Pro (2 créditos cada una).

## 3. Producción (lo que sostiene la retención)

- **Una imagen nueva cada 4 a 6 segundos** (~120 escenas). En los gráficos de retención, las caídas aparecen donde la imagen se queda quieta demasiado tiempo.
- **Survival Meter** como capa fija en la esquina superior derecha, animada cuando cambia (ffmpeg con drawbox/drawtext; viene en ffmpeg-full).
- **Subtítulos** con la palabra activa en rojo (ya probados).
- **Efectos de sonido sutiles** en los remates (un "whoosh" al bajar el medidor, una moneda al lanzarla). ElevenLabs tiene Sound Effects y entra en los créditos del Starter.
- **Música de fondo baja** de la Audio Library de YouTube (gratis y sin reclamos de derechos).

## 4. Lanzamiento (las primeras 48 horas)

1. **Publicar un martes, miércoles o jueves a las 2-4 p. m. hora del Este (EE. UU.).** Es cuando el público de EE. UU. sale del trabajo o la escuela.
2. **Capítulos** en la descripción (0:00 Hook, 1:00 A year earlier, …). Ayudan a la búsqueda y a la retención.
3. **Comentario fijado** con la pregunta: "Run, pray or wait?".
4. **Subtítulos .srt** subidos (ya los generamos). Mejoran el SEO y activan la traducción automática.
5. **3 Shorts** sacados del video, publicados en los días siguientes. Llevan gente nueva al canal, que es lo que más falta hace al empezar:
   - "Doctors blamed the plague on… Jupiter" (min. 0-0:20 + París)
   - "The plague doctor mask is a lie" (la máscara de pico)
   - "Ring Around the Rosie isn't about the plague"
6. **Pantalla final** hacia el segundo video. Por eso conviene tener listo el **#2 (Medieval Winter, para noviembre)** antes o justo después de publicar el piloto: un canal con un solo video no retiene suscriptores.

## 5. Qué mirar después (paso 7)

| Métrica (YouTube Studio) | Bueno para un canal nuevo | Si sale mal |
|---|---|---|
| CTR de impresiones | > 6 % | Cambiar miniatura o título (se puede hacer después de publicar) |
| Retención a los 30 s | > 70 % | El gancho no funciona: aprender para el siguiente |
| Duración media vista | > 40 % del video | Revisar en qué minuto cae y por qué |
| Comentarios | Cualquier número | Responderlos todos los primeros días |

## 6. Costo adicional de estas mejoras

Prácticamente nada. Las 3 miniaturas cuestan ~6 créditos de Higgsfield, los efectos de sonido unos pocos créditos de ElevenLabs, y la música y el Test & Compare son gratis. El "Survival Meter" es código (ffmpeg).
