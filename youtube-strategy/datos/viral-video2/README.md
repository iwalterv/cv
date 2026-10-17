# Análisis de viralidad para el video #2 (16-oct-2026)

Hecho a pedido del usuario: **antes de proponer cualquier video, hacer un análisis profundo con datos.** Método reutilizable: `scripts/outliers.py`.

## Método
1. **Outliers del último año** (`outliers.tsv`): últimos 150 videos de 26 canales del nicho (`canales.txt`), solo metadatos con yt-dlp, sin Shorts. Para cada video: vistas ÷ mediana de su canal. Un 50× significa que ese tema o empaque funcionó muy por encima de lo normal **con el mismo canal y el mismo público**.
2. **Búsquedas en YouTube** (`busquedas/`): top 25 para cada tema candidato. Se mide la demanda (mediana, videos >1 M, videos recientes >100K) y la competencia directa (copias del mismo ángulo y cuánto sacan).
3. **Autocompletado de YouTube** (lo que la gente escribe de verdad).
4. Encaje con el formato (Red + Survival Meter) y con el análisis de miniaturas (`datos/miniaturas-analisis/`).

## Lo que dicen los outliers (12 meses)
| Patrón | Evidencia | Lectura |
|---|---|---|
| **Vida diaria "What did X do…"** | Zenn "What Did Ancient Humans Do at Night?" **8,0 M (258×)**; Axen "…All Day Before Jobs" 3,3 M (228×); Ink Explainer "…All Day?" 14 M (47×) | El formato estrella de los monigotes. Pero "ancient humans" ya está saturado de copias |
| **Sobrevivir al invierno** | Axen "How Did Ancient Humans Survive Deadly Winters?" 950K (**65×**); MTD "Outlaws Survived Freezing Winters" 316K (42×); MTD "Winter Heating Trick" 282K (38×); otros dos de calefacción (29× y 16×) | **Tema que se repite como outlier en varios canales distintos** |
| **"Why it sucked to be…" (oficios)** | StickTory: verdugo 2,1 M (27×), herrero 1,4 M (18×), asesino 1,3 M (17×) | Funciona, pero StickTory domina ese título |
| Dormir / noche medieval | "How Did People Sleep in Medieval Castles Without Freezing" 1,5 M y 843K (Infographics, 2026) | Cruza con el invierno |

## Candidatos
| Tema | Demanda | Competencia reciente | Autocompletado | Veredicto |
|---|---|---|---|---|
| **Invierno medieval** | Búsqueda "medieval winter survival": mediana **262K**, 15 de los recientes >100K; MedievalMadness 3,9 M, Tasting History 2,1 M, K12 (animado) **1,76 M** en feb-2026 | Copias del mismo título: Daniel Does History 107K; varias nuevas de oct-2026 con pocas vistas: **la temporada empieza ya** | **"how did medieval people survive winter" es la 1.ª sugerencia** de "how did medieval people" | ✅ **El mejor**: demanda alta y probada, outlier en varios canales, de temporada y versión animada con prueba (K12) |
| Médico de la peste | Alta pero **vieja**: Simple History 3,9 M (2017), Infographics 3,5 M (2021), TED-Ed 2,4 M (2023) | Las copias de 2026 sacan **105-292 vistas**, y una usa exactamente nuestro ángulo ("everyone else ran away") | Lo que sugiere es disfraz, meme, ASMR: entretenimiento, no historia | ⚠️ Arriesgado ahora. Se guarda el guion (`videos/02-plague-doctor/`) para cuando el piloto dé datos |
| Qué hacía la gente medieval de noche | El formato de Zenn (258×), pero la búsqueda medieval tiene mediana de **8,7K** | Lo dominan los canales de "historia para dormir" | "medieval night" sugiere ambientes y música | Prometedor como **sección** dentro del invierno (las noches largas, el "segundo sueño"), no como video aparte |
| Peores oficios medievales | Chat History 2,9 M y 1,7 M (recientes) | Chat History lo domina | — | Para más adelante |

## Decisión propuesta
**Video #2: el invierno medieval**, con una sección de noches y sueño (el cruce de los dos temas que más funcionan), publicado en la **última semana de octubre**, cuando empieza a subir la temporada.
- **Título A/B (YouTube permite probar títulos):** "Why You Wouldn't Survive a Medieval Winter" (formato de la serie, igual que el piloto) contra "How Did Medieval People Survive Winter?" (la frase exacta que la gente busca).
- **Miniatura:** Red congelado, con hielo en la bufanda, y una amenaza (lobos en la nieve o la puerta tapada de nieve) más 2 o 3 palabras ("-20°?", "NO HEAT?"), según `datos/miniaturas-analisis/`.
- **Para diferenciarnos de las copias:** Red + Survival Meter + datos concretos verificados, y nada del formato de "historia para dormir" de 2 horas.

Limitación: no podemos ver el CTR ni la retención de otros canales, y las fechas de yt-dlp son aproximadas ("hace 1 año"). Ningún análisis garantiza que un video se haga viral: esto **sube la probabilidad**.
