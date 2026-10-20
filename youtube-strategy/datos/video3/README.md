# Análisis viral para el video #3 (20-oct-2026)

Primer video con el **formato nuevo** aprobado el 20-oct (`08-investigacion-crecimiento.md`): preguntas de curiosidad sobre la vida diaria medieval, contadas desde TU perspectiva con Red.

## Método
1. **Autocompletado de YouTube** (EE. UU., en inglés) para "what did medieval peasants/people", "how did medieval people/peasants", "did medieval people", "medieval peasants".
2. **Outliers del nicho** (`datos/viral-video2/outliers.tsv`, 26 canales, 12 meses).
3. **Top 25 de búsqueda** para 11 candidatos (`busquedas/*.tsv`: vistas, fecha, duración, canal, suscriptores, título, id). Para cada uno se mide:
   - la **mediana** de vistas;
   - cuántos videos pasan de **1 M**;
   - cuántos videos **del último año** pasan de 100K (demanda viva);
   - cuántos videos del último año se quedan **por debajo de 1K** (saturación de copias);
   - cuántos videos de **canales de menos de 200K suscriptores** pasan de 100K (si un canal pequeño puede ganar).

## Autocompletado (lo que la gente escribe)
- "what did medieval peasants" → **eat**, wear, **do for fun**, **do all day**
- "how did medieval people" → **survive winter** (ya es nuestro video #2), **sleep**, live, talk, brush their teeth
- "how did medieval peasants" → do shopping, live, eat, wear, **where did medieval peasants sleep**
- "did medieval people" → **bathe**, believe in ghosts, eat breakfast
- "medieval peasants" → daily life, **worked less**, food, winter

## Resultados
| Tema | Mediana | >1 M | Último año >100K | Último año <1K | Canales pequeños >100K |
|---|---|---|---|---|---|
| **how did medieval people sleep** | **119K** | 4 | **5** | 0 | **7** |
| **what did medieval peasants eat** | **271K** | **10** | **5** | 1 | 3 |
| what did medieval peasants do for fun | 190K | 8 | 1 | 6 | 1 |
| **what did medieval people do at night** | 1,3K | 4 | 3 | 12 | **6** |
| what did medieval peasants do all day | 751 | 3 | 1 | 15 | 1 |
| did medieval people bathe | 484 | 3 | 0 | 11 | 0 |
| medieval peasants worked less | 371 | 1 | 0 | 14 | 0 |
| how did medieval people go to the bathroom | 232 | 1 | 1 | 15 | 1 |
| how did medieval people have privacy | 76 | 0 | 1 | 16 | 1 |
| what did medieval people do when they got sick | 27 | 2 | 0 | 21 | 0 |
| how did medieval people brush their teeth | 22 | 2 | 0 | 15 | 0 |

### Noche y sueño (las dos búsquedas devuelven casi los mismos videos)
- **Canales pequeños que ganan hace poco:**
  - Medieval History (31,8K suscriptores): "Why Medieval People Slept in Two Shifts?", **644K**.
  - The Stache Chronicles (13,2K): "Inside the Medieval Night: What People Did After Dark", **408K**.
  - History and Coffee (109K): "Medieval Nights: The Lost Tradition of Two Sleeps", **491K**.
- **Grandes, en 2026:** Infographics Show, 851K (abr-2026); Modern History TV, 1,08 M (sep-2026).
- **Plantilla exacta con monigotes:** Zenn, "What Did Ancient Humans Do at Night?", **8,0 M** (258× su mediana). Entre las miniaturas ganadoras del nicho también está "2 SLEEPS?".
- **Competencia de monigotes en medieval:** casi ninguna. Every Life Explained (34 min, 31K vistas) y Basically Primitive (2K).
- La mitad de lo más visto es "historia para dormir" de 2 horas (Sleepless Historian, Boring History Secrets): otro público y otro formato, no compite con un video de 10 min.

### Comida
- La demanda más grande y duradera (10 videos de más de 1 M), pero la dominan **Modern History TV y Tasting History** (1-4,5 M de suscriptores), con muchos videos de 2018-2021.
- Hay sitio para una versión con monigotes ("What Did Ancient Humans Actually Eat?" de Zenn: 896K, 29×), pero un canal pequeño tiene menos opciones de entrar en esa búsqueda.

### Diversión
- Buena demanda histórica (Weird History, "How Medieval Peasants Spent Their Free Time", 992K), pero solo 1 video reciente pasa de 100K.

### Descartados por ahora
Baños, dientes, privacidad, enfermedad, "worked less": la mediana es de 22-751 vistas y está llena de copias recientes con menos de 1K.

## Recomendación
| # | Tema | Título A / B | Por qué |
|---|---|---|---|
| **3** | **La noche medieval** | **"What Did Medieval Peasants Do at Night?"** / "How Did Medieval People Actually Sleep?" | Es la plantilla del mayor outlier del nicho (Zenn, 8 M). Tiene demanda viva en 2025-26, varios **canales pequeños ganan**, y casi no hay versiones medievales con monigotes. Gancho fuerte: el "primer sueño" y el "segundo sueño" (A. Roger Ekirch) |
| 4 | Comida | "What Did Medieval Peasants Actually Eat?" | La demanda más grande y duradera. Al ser el segundo video del formato, el canal ya tendrá algo de señal |
| 5 | Diversión / tiempo libre | "What Did Medieval Peasants Do for Fun?" | El autocompletado lo pide en las dos búsquedas. Weird History lo llevó a casi 1 M |

**Cuidado con lo que se repite del video #2**, que tenía secciones de oscuridad y cama (velas de junco, toque de queda, la cama de paja compartida). El #3 tiene que contar cosas nuevas: los dos sueños y qué se hacía en el rato despierto, el miedo a la noche (fantasmas, ladrones, la ronda nocturna), el orinal, la luz de luna y el calendario, los sueños como presagio. Lo del #2 entra solo en una frase.

**Miniatura** (al estilo de las v2, clara y minimalista): Red sentado en la cama, despierto en plena noche, con la familia dormida y un reloj de luna. Texto "2 AM?" o "AWAKE?". El A/B decide.

**Producción:**
- Quedan unos **69 créditos de Higgsfield**. Un video de unas 110 escenas (0,5 c/u, ~55) más 3 miniaturas (~6) entra justo.
- Hay que revisar los caracteres que le quedan a ElevenLabs Starter (se renueva el 15).

Limitación: no vemos el CTR ni la retención de otros canales, y ningún análisis garantiza un viral. Esto sube la probabilidad.
