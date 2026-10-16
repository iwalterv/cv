# Paso 4: banco de 30 ideas validadas con datos

Fuente: `datos/paso4/`. Son las listas completas de videos de 16 canales (monigotes de referencia + competidores directos del formato "TÚ en la historia") y 36 búsquedas de YouTube (18 por época o tema y 18 de títulos candidatos). Se extrajo todo con `yt-dlp` (solo metadatos) el 15 de octubre de 2026. No se cuentan los Shorts (menos de 3 min).

## 1. Lo que dicen los datos

**Formatos que funcionan (con videos de 1 M o más):**

| Formato | Quién lo hace bien | Prueba |
|---|---|---|
| "Why You Wouldn't Survive [época]" | Chat History | Egipto 3,8 M, Grecia 2,3 M, Roma 2,3 M, Japón feudal 2,1 M, Oregon Trail 1,6 M, aztecas 1,3 M |
| "Why It Sucked to Be a [oficio]" | StickTory | Verdugo medieval 2,1 M, herrero 1,4 M, asesino 1,3 M, faraón 1,2 M (con una mediana de 77K en el canal) |
| "Worst / Miserable Jobs in History" | Chat History | 2,9 M, 2,1 M, 2,0 M, 1,7 M |
| "Your Life as [persona]" | Serious History | Musashi 4,0 M, Carton de Wiart 1,6 M |
| "What Did Ancient Humans Do…?" | Ink Explainer, Zenn, Axen | 14 M, 8 M, 3,3 M… |

**Dónde NO meterse:** "What did [época] do all day?". La mitad de los canales nuevos de monigotes hace exactamente eso con vikingos, romanos y Egipto, y la mediana de vistas en esas búsquedas es de **28 a 327**. "Ancient humans" también está saturado. Los competidores directos del formato "tú" (Unlucky Ancestors, Yesteryou, You Back Then, Ancestor Mode) tienen entre 1 y 21 vistas: el formato no basta, hacen falta un tema con demanda y una buena ejecución.

**Dónde hay demanda y poca oferta de monigotes:**
- **Peste Negra:** 17 de 25 resultados superan 1 M vistas, pero la versión "Why you wouldn't survive" solo tiene 12,6K.
- **Invierno medieval:** 4,3 M, 3,9 M y 2,5 M, y es **de temporada** (noviembre a enero).
- **Londres victoriano:** BlueJay 5,3 M y History Hit 1,6 M; ningún canal de monigotes con fuerza.
- **Piratas:** Sam O'Nella 19,9 M; las versiones "Your life as a pirate" con monigotes no pasan de 140K.
- **Higiene / "antes de X existiera"** (jabón, dentistas, inodoros): Weird History tiene 3,5 M y Modern History TV 1,2 M, y casi no hay monigotes.

## 2. Cómo puntuamos

- **Demanda** (1-5): vistas de los mejores videos del tema (no solo del formato).
- **Hueco** (1-5): cuánta competencia directa hay con el mismo ángulo y formato (5 = casi nada).
- **Encaje** (1-5): si funciona con Red en primera persona, con escenas claras y si es apto para anunciantes.
- **Prioridad** = Demanda + Hueco + Encaje (máximo 15).

## 3. Las 30 ideas

### Prioridad A (13-15): para los primeros videos

| # | Título (inglés) | Formato | Época | Texto miniatura | D | H | E | Total | Validación (dato) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Why You Wouldn't Survive the Black Death** | Survive | Edad Media | **1348?** | 5 | 4 | 5 | **14** | Tema: 17/25 resultados >1 M (Infographics 9,1 M; Weird History "How You Could Have Survived the Black Plague" 5,1 M). Mismo ángulo con "you": 12,6K y 21K. Ya tenemos el gancho y las escenas de prueba |
| 2 | **Why You Wouldn't Survive a Medieval Winter** | Survive | Edad Media | **-20°?** | 5 | 3 | 5 | **13** | Sleepless Historian 4,3 M; MedievalMadness 3,9 M; Tasting History 2,0 M. Versión monigote: no hay. Copias "you": 107K y 771. **De temporada: publicar en noviembre** |
| 3 | **Your Life as a Golden Age Pirate** | Your Life as | Piratas | **SCURVY?** | 5 | 4 | 4 | **13** | Sam O'Nella "Why It Sucked to Be a Pirate" 19,9 M; CGP Grey 12 M. "Your life as a pirate": máximo 140K (POV) |
| 4 | **Why You Wouldn't Survive Victorian London** | Survive | Victoriana | **SOOT?** | 5 | 3 | 5 | **13** | BlueJay 5,3 M; Timeline 1,7 M; History Hit 1,6 M y 1,3 M. Monigotes: no hay |
| 5 | **What Did Medieval People Eat for Breakfast?** | What Did | Edad Media | **NO BREAKFAST?** | 5 | 3 | 5 | **13** | MHTV "What did peasants eat" 6,9 M; Tasting History "Did Medieval People Eat Breakfast?" 1,8 M. Monigotes: 583 |
| 6 | **What Did People Do Before Soap?** | What Did | Varias | **NO SOAP?** | 4 | 5 | 4 | **13** | MHTV "Soap and washing" 1,2 M; Weird History higiene 3,5 M. Copias directas: 91 y 5 vistas (sin ejecución) |
| 7 | **Why It Sucked to Be a Plague Doctor** | Sucked | Edad Media / s. XVII | **THE MASK?** | 5 | 3 | 5 | **13** | TED-Ed "beaked masks" 2,4 M; "Trust Me Bro" mismo título 403K (único fuerte). Encaja con #1 (serie de la peste) |
| 8 | **The Worst Jobs in Medieval England** | Worst Jobs | Edad Media | **GONG FARMER?** | 5 | 4 | 4 | **13** | Chat History "Absolute Worst Jobs" 2,9 M; MedievalMadness 883K; Absolute History 712K. Versiones de monigotes: 823 y 726 |

### Prioridad B (11-12): buenas, para rotar épocas

| # | Título | Formato | Época | Miniatura | Total | Validación |
|---|---|---|---|---|---|---|
| 9 | Your Life as a Pyramid Builder | Your Life as | Egipto | **PAID IN BEER?** | 12 | Chat History Egipto 3,8 M; Odyssey "your life in ancient Egypt" 1,5 M. Este ángulo exacto: máximo 1K (hueco total, demanda indirecta) |
| 10 | The Worst Jobs in Victorian London | Worst Jobs | Victoriana | **TOSHER?** | 12 | Timeline 881K; Simple History "Tosher" 810K; Absolute History 715K. Monigotes: no hay |
| 11 | What Did People Do Before Dentists? | What Did | Varias | **PLIERS?** | 12 | MHTV "rotten teeth" 1,3 M; dentistería 168K. Copias: 729, 107, 72 |
| 12 | Why You Wouldn't Survive the Wild West | Survive | Lejano Oeste | **DYSENTERY?** | 12 | BlueJay 4,8 M; Simple History 3,5 M; Chat History Oregon 1,6 M. Ojo: Nutty History tiene el mismo título (658K): usar otro ángulo ("a Week in…") |
| 13 | Why It Sucked to Be a Victorian Child | Sucked | Victoriana | **AGE 6?** | 12 | BlueJay 5,3 M; Serious History "Disturbing Jobs for Kids" 511K. Sin versión directa |
| 14 | What Did Medieval People Do Without Toilets? | What Did | Edad Media | **NO PAPER?** | 12 | MHTV sanitation 458K; Weird History higiene 3,5 M. Copias: 5K y 0 |
| 15 | Your Life as a Medieval Peasant (It Was Worse Than You Think) | Your Life as | Edad Media | **BREAD AGAIN?** | 11 | MTD "24 Hours" 2,9 M; Simple History 2,4 M; MHTV 2,0 M. "Your life as" de monigotes: 6K y 29K |
| 16 | Why You Wouldn't Last 24 Hours in a Medieval Castle | Survive | Edad Media | **NO HEAT?** | 11 | MTD 24h 2,9 M; Infographics "castles freezing" 841K. Copias exactas: 638 y 394 |
| 17 | What Did Sailors Do When the Food Ran Out? | What Did | Era de la vela | **BISCUIT WORMS?** | 11 | History Hit "Nelson's Navy food" 1,4 M; Pirate Times 560K. Casi sin monigotes |
| 18 | What Did People Do Before Refrigerators? | What Did | Varias | **NO ICE?** | 11 | Adam Ragusea 1,6 M; MTD 223K. Copias: 19K, 308, 256 |
| 19 | Your Life as a Ronin | Your Life as | Japón feudal | **NO MASTER?** | 11 | Serious History Musashi 4,1 M; "Every Samurai Rank" 1,2 M; "What were Ronin?" 600K. Past in Ink cubre samuráis (88K) |
| 20 | Your Life in Tenochtitlan | Your Life as | Aztecas | **CHOCOLATE MONEY?** | 11 | Weird History aztecas 2,3 M; Invicta "Growing up Aztec" 1,8 M; POVrank 191K. Evitar los sacrificios como tema central (anunciantes) |
| 21 | Why You Wouldn't Survive the Ice Age | Survive | Edad de Hielo | **-40°?** | 11 | 2,5 M, 1,0 M y 949K, pero con mucha competencia de monigotes ("ancient humans"): diferenciarse con Red y datos concretos |
| 22 | What Did Medieval People Do When They Got Sick? | What Did | Edad Media | **LEECHES?** | 11 | Good Enough "Failed cures for the plague" 3,8 M; MedievalMadness. Copias de "ancient humans sick": 44K |

### Prioridad C (9-10): reserva, o validar mejor antes

| # | Título | Época | Miniatura | Total | Por qué está en reserva |
|---|---|---|---|---|---|
| 23 | Why It Sucked to Be a Gladiator | Roma | **THUMBS DOWN?** | 10 | Demanda amplia pero dispersa; Bernard POV 146K |
| 24 | Why It Sucked to Be a Roman Soldier's Mule (the Legionary) | Roma | **60 LBS?** | 10 | StickTory ya hizo "Roman Soldier" (326K); Unlucky Ancestors (6 vistas) |
| 25 | What Did Medieval People Do for Fun? | Edad Media | **FOOTBALL?** | 10 | MedievalMadness 159K; "What We Did Before" 175K (2026). Demanda media |
| 26 | Your Life on the Oregon Trail | Lejano Oeste | **DYSENTERY?** | 10 | Chat History ya tiene 1,6 M con ese tema; se solapa con #12 |
| 27 | Why You Wouldn't Survive as a Viking | Vikingos | **BERSERK?** | 10 | Búsquedas de vikingos con monigotes: mediana de 28-82 vistas. Lo salva la compilación de Chat History (3,2 M) |
| 28 | Why It Sucked to Be a Medieval Monk | Edad Media | **SILENCE?** | 9 | Demanda no verificada |
| 29 | What Did Romans Do for Fun? | Roma | **CHARIOTS?** | 9 | Folks of Yore 667K, pero las copias de monigotes tienen entre 43K y 842 |
| 30 | Why You Wouldn't Survive Ancient Sparta | Grecia | **AGE 7?** | 9 | Chat History "Ancient Greece" 2,3 M; Sparta sin búsqueda propia (validar) |

## 4. Recomendación para el piloto

**#1 "Why You Wouldn't Survive the Black Death".**
- Es el tema con más demanda del banco (17 de 25 resultados con más de 1 M) y la versión "you" con monigotes casi no existe (12,6K).
- Ya tenemos el gancho escrito (el campesino de 1347 y el barco de Melcombe), las escenas de prueba y la paleta medieval.
- Abre una **serie de la peste**: #7 (Plague Doctor) y #22 (When They Got Sick). Si funciona, el algoritmo recomienda los siguientes a la misma audiencia.
- Cuidado con la política de YouTube: es un tema de enfermedad, así que hay que tratarlo como historia, con datos verificados y sin morbo gráfico.

**Calendario sugerido de los primeros 6 (rotando épocas):**
1. Black Death (Edad Media), el piloto.
2. Medieval Winter (Edad Media), en **noviembre**, por temporada.
3. Your Life as a Golden Age Pirate (piratas).
4. Victorian London (era victoriana).
5. Before Soap (varias épocas, formato "What Did").
6. Plague Doctor (continúa la serie de la peste, si el piloto funciona).

## 5. Reglas para que los títulos sigan siendo originales
- Se toma el **tema**, nunca el texto ni la estructura de un video concreto.
- Si un competidor tiene **el mismo título exacto con más de 100K vistas**, cambiamos el ángulo (por ejemplo, #12).
- Cada guion lleva **fuentes verificadas** (al menos 2 por dato clave).
