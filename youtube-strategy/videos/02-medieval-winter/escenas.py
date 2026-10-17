"""Fuente de las escenas del video #2: genera escenas.json (prompts) y comprueba que los textos cubren toda la narración.

Uso: python3 videos/02-medieval-winter/escenas.py
Cada escena: (texto narrado exacto, sin etiquetas de voz | descripción de la imagen | medidor opcional).
El medidor ("meter") se mantiene hasta que otra escena lo cambie. Aquí son las probabilidades de llegar a la primavera.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent


def M(value, **kw):
    return {"value": value, "label": "SPRING ODDS", **kw}


S = [
    # 0. Gancho
    ("Your house has no chimney.", "Red coughing inside a small one-room medieval hut filled with grey smoke from an open fire burning in the middle of the dirt floor, no chimney, smoke curling under the thatch. Orange firelight, cold blue shadows."),
    ("Your bed is made of straw, and you're sharing it with your entire family.", "Red squeezed in the middle of a straw mattress on the floor between his mother, father, grandmother and three small siblings, all under one rough wool blanket, dim firelight."),
    ("And just on the other side of the room, there's a cow.", "Red lying in the crowded family straw bed, slowly turning his head to see a big brown-and-white cow standing a few steps away inside the same room, staring back at him."),
    ("That's not a punishment.", "Close-up of the brown-and-white family cow chewing calmly and looking straight at the viewer, inside a dim hut lit by an open fire on the floor, warm firelight on its face. No fireplace, no other people."),
    ("That's your heating system.", "Inside a dim hut, Red happily snuggled up against the side of the brown-and-white cow lying in the straw, warm steam rising from the cow, little wavy heat lines, frost on the walls behind. No fireplace."),
    ("Welcome to winter, in medieval England.", "Wide establishing shot of a small medieval English village buried in deep snow at dusk: thatched cottages with snow on their roofs, a little stone church, bare trees, smoke rising through the thatch, Red small in the foreground. Cold blues and warm orange windows.", M("100")),
    ("You have five months to survive.", "Red standing in the open doorway of his hut staring out at endless snow, five tally marks scratched into the wooden door frame beside him, worried face."),
    ("And see that meter in the corner? Those are your odds of making it to spring.", "Red in snow pointing up toward the top-right corner of the frame with a curious face, leaving the top-right corner empty."),
    ("They're about to have a very bad November.", "Red shivering in the snow with a forced, nervous grin, giving a shaky thumbs up, icicles hanging from his nose."),
    ("And stick around, because in one of these winters, it got so cold that people were buying their wine by the pound.", "A medieval market stall in snow: a merchant placing a solid block of frozen red wine, shaped like the jug it came from, on a big balance scale, Red staring at it in disbelief."),
    # 1. Noviembre
    ("Let's start with November.", "Red standing next to a big round painted wooden board divided into four pie slices showing the seasons as tiny pictures: green spring field, golden harvest, a pig in brown autumn, white snow. His finger points at the brown autumn slice. Plain wooden rim with no inscriptions. Pictures only, absolutely no letters, words or numbers anywhere."),
    ("The old English name for this month was Blotmonath.", "An Anglo-Saxon monk with a tonsure writing in a large old book with a quill by candlelight in a cold stone cell, frost on the small window."),
    ("Blood month.", "A medieval illuminated parchment page with a small painted picture of a pig and a farmer, the whole page glowing deep red, Red standing beside it gulping nervously. Pictures only, absolutely no letters, words, numbers or grid."),
    ("And the name is honest.", "Red standing face to face with his fat pink pig in a muddy yard, the pig looking up at him trustingly, Red hiding a butcher's knife behind his back with a guilty face. Cartoonish, no blood."),
    ("Around now, families slaughtered a lot of their animals.", "A grey late-autumn medieval village with bare trees and the first frost: families leading pigs and sheep across the lane toward a barn, sad-faced animals. No blood, nothing graphic."),
    ("Not out of cruelty. Out of math.", "Red sitting on a stool doing sums with tally marks scratched on a wooden board, looking back and forth between three cows and one small haystack, thinking hard."),
    ("Grass stops growing in winter. Hay is limited.", "A frosty brown field with dead grass, a single small haystack under grey sky, a thin cow sniffing the frozen ground."),
    ("You can't feed every animal until spring, so you keep the ones you need, the breeding stock and the ones that pull the plough, and the rest become dinner.", "Inside a barn, Red standing proudly next to two strong oxen with a plough yoke and one cow, while a pig tiptoes away behind them toward the door with a nervous sweat drop."),
    ("And because there's no fridge, the meat gets salted, smoked or dried.", "Red (white round head, red scarf) throwing handfuls of coarse salt into a wooden barrel full of chunks of meat, hams and sausages hanging from the smoky rafters above him."),
    ("A family pig, killed around Saint Martin's Day, on the 11th of November,", "A medieval English village gathered on a cold November feast day in front of the stone church, a painted church banner showing a knight on horseback cutting his cloak in half to share it, villagers bundled up."),
    ("could be the difference between eating meat this winter and not.", "Red hugging a big cured ham protectively with both arms, eyes closed in relief, snow falling outside the hut door."),
    ("Very, very salty meat. For months.", "Red biting a rock-hard strip of salted meat, face puckered and lips shriveled, desperately gulping from a water jug.", M("85")),
    # 2. Tu casa
    ("Now, let's look at your house.", "Red standing in the snow in front of his small thatched cottage, gesturing at it proudly like a tour guide."),
    ("One main room.", "Cutaway view of the inside of a small medieval peasant cottage: a single room with a dirt floor, a few stools, a chest, straw beds along the walls and a fire in the middle."),
    ("Walls of wattle and daub, which is woven sticks covered in mud and dung.", "Close-up of a cottage wall being built: thin sticks woven together like a basket, Red smearing brown mud onto it with his hands and a disgusted face, flies buzzing."),
    ("A thatched roof.", "A thick thatched straw roof covered in snow with a row of icicles hanging from its edge."),
    ("And in the middle of the floor, an open fire.", "A simple open fire on a ring of stones in the middle of a dirt floor, smoke rising, family stools around it."),
    ("No chimney.", "Red looking straight up from the fire at a smoke-blackened roof with no chimney, just soot-covered rafters and smoke."),
    ("Chimneys and fireplaces were spreading in richer homes, but in a lot of ordinary houses the smoke just drifted up into the roof and found its own way out.", "Split scene in the snow: on the left a rich stone manor house with a proper chimney puffing smoke, on the right Red's little hut with smoke seeping out everywhere through the thatch."),
    ("Eventually.", "Red inside the smoky hut waving his arms to clear the smoke, eyes red and teary."),
    ("So you're always either too smoky or too cold. Usually both.", "Red standing half in thick grey smoke and half covered in white frost, unhappy on both sides."),
    ("Your face is roasting and your back is freezing.", "Red's family sitting on stools around the central fire, faces lit warm orange with rosy cheeks and little sweat drops, normal skin color, while their backs are covered in frost and little icicles."),
    ("And in some parts of England, like Dartmoor, people lived in longhouses.", "A long low stone longhouse with a thatched roof on a bleak snowy moorland with granite rocks, smoke rising, Red walking up to the door."),
    ("One long building, with the family at one end, a passage in the middle, and the cattle at the other end, under the same roof, especially in the coldest months.", "Cutaway view of a long stone farmhouse: on the left the family around a fire, a passage with two doors in the middle, on the right cows in stalls, all under one long thatched roof."),
    ("Is it smelly? Absolutely.", "Red pinching his nose with a green face, the cows right behind him, little stink lines in the air."),
    ("But a cow is basically a big, warm radiator that eats grass.", "Red warming his hands against the side of the brown-and-white cow as if it were a fireplace, the cow glowing warm orange, chewing hay."),
    ("In January, you stop complaining about the smell.", "Red fast asleep and smiling, curled up against the cow, snow piled up against the outside of the window."),
    ("As for clothes, the strategy is simple: wear everything you own.", "Red standing next to a wooden chest pulling out clothes and putting on layer after layer as fast as he can."),
    ("A linen shirt, wool tunics on top of each other, wool hose on your legs, a cloak, and a hood if you have one.", "Red wearing so many brown and grey wool layers, cloak and hood that he is as round as a ball, only his eyes and his red scarf peeking out, arms sticking out stiffly."),
    ("Women spun the wool themselves, so every layer you're wearing took someone in your family hours to make.", "Red's mother sitting by the fire spinning wool with a drop spindle, a basket of raw wool beside her, Red watching gratefully."),
    ("And your shoes are thin leather.", "Close-up of a pair of thin, simple medieval leather shoes standing in the snow."),
    ("There are no rubber boots. Every time you go outside, your feet get wet.", "Red stepping into ankle-deep slush outside his hut, his thin leather shoes soaked, wincing, water splashing."),
    ("And there is no dryer. Just the smoky fire, and a lot of patience.", "Red sitting by the fire holding his soaked shoes on a stick over the flames, steam rising, bored face, chin on hand."),
    # 3. La oscuridad
    ("Here's something we forget.", "Red in snow raising one finger like he's about to share a secret."),
    ("In the middle of an English winter, the sun sets before four in the afternoon.", "A snowy medieval field where peasants are still working, looking up in surprise as the sun is already setting low on the horizon, long blue shadows, orange sky."),
    ("And then it's dark. Really dark.", "An almost completely black scene, only Red's two big white eyes visible in the darkness."),
    ("No electricity, obviously.", "Red in a pitch-dark hut feeling his way along the wall with his hands, bumping into a stool."),
    ("Good candles were made of beeswax, and those were for churches and rich people.", "Inside a medieval stone church: tall golden beeswax candles glowing beautifully on the altar, a priest lighting them, Red peeking enviously from the door."),
    ("Beeswax could cost about three times as much as tallow, which is candles made from animal fat.", "A big balance scale: one golden beeswax candle on one side balanced by three greasy yellowish tallow candles on the other, a small pile of coins next to the beeswax one."),
    ("And a lot of poor families couldn't even afford that.", "Red turning his empty leather purse upside down, only a moth flying out."),
    ("They used rushlights: dried rushes dipped in fat, burning for a few minutes each.", "Red sitting by the fire peeling long green rushes and dipping them in a small pan of melted grease, a bundle of dried rushes beside him."),
    ("Your whole evening, lit by a greasy plant.", "Red's family squinting around a single tiny flickering rushlight held in a small iron clip, the rest of the hut in deep shadow."),
    ("And then a bell rings,", "A village stone church tower at night in the snow, its bell swinging, little sound lines, stars above."),
    ("and it's time to cover the fire, to keep it from burning down the house, and the whole village with it.", "Red carefully placing a round clay cover with holes over the glowing embers of the fire, a thatched village visible through the door behind him."),
    ("That bell had a name in Old French: cuevrefeu.", "A Norman bell-ringer in a tunic pulling the bell rope inside a stone tower at night, very serious."),
    ("\"Cover fire\". Which is where we get the word \"curfew\".", "Red looking at the viewer amazed, pointing at the covered fire glowing faintly through the holes of the clay cover.", M("70")),
    # 4. La cama
    ("So, bedtime.", "Red yawning hugely, holding a dying rushlight, the hut almost dark."),
    ("Your mattress is a sack of straw, on the floor or up in a loft.", "A lumpy sack stuffed with straw lying on the dirt floor, straw poking out, and a small wooden loft above with another one."),
    ("And you're not alone in it.", "Red lying on a lumpy straw sack on the floor with a peaceful smile while two small siblings climb in on both sides. The straw sack is plain, no faces or eyes on it."),
    ("Families slept together, huddled up, because body heat is free.", "Red's whole family huddled together in one pile under a wool blanket, Red squashed in the middle, only his head and red scarf sticking out."),
    ("And here's where it gets interesting.", "Red lying awake in the dark, eyes wide open, everyone around him snoring with little Z's."),
    ("According to historian Roger Ekirch, for centuries, Europeans often didn't sleep in one long block.", "A modern historian with glasses at a desk piled with old books and a lamp, reading an old diary with a magnifying glass. Generic character, not a real likeness."),
    ("They had a \"first sleep\", then woke up in the middle of the night for an hour or so, and then went back for a \"second sleep\".", "A snowy cottage at night under a big moon, cut in two: on the left the family asleep, in the middle Red sitting up awake by the embers, on the right everyone asleep again."),
    ("In that gap, people prayed, did small chores, talked, visited neighbors,", "Midnight inside the hut: grandmother praying with a rosary, mother mending clothes by the embers, father chatting quietly with a neighbor at the door."),
    ("and, well, made more peasants.", "Red covering his eyes with both hands, embarrassed, in front of a drawn curtain around the parents' bed, a few little hearts floating above it. Family friendly."),
    ("With fourteen hours of darkness, you'd probably wake up in the middle too.", "Red looking straight at the viewer in the dark, wide awake, shrugging."),
    # 5. Diciembre
    ("Then comes December, and the best news of the whole winter: Christmas.", "A snowy medieval village at night, the lord's big manor house on the hill glowing with warm light, holly and ivy on the doors, smoke from its chimney."),
    ("And for you, Christmas is a big deal, because it's one of the few times in the year when the work actually stops.", "Red happily throwing his spade and pitchfork over his shoulder into the snow, arms raised in celebration."),
    ("On a lot of manors, tenants owed the lord some rent at Christmas, often paid in food.", "The lord's steward in a fine cloak at a table outside the manor door, checking notched wooden tally sticks as peasants line up in the snow carrying food."),
    ("Hens, bread, ale.", "A still life on a table: two live hens, round loaves of bread and a clay jug of ale."),
    ("So you walk up to the big house, holding your chickens.", "Red trudging up the snowy hill toward the glowing manor house with a hen tucked under each arm, the hens looking annoyed."),
    ("And on some manors, there was a feast for the tenants.", "A great hall with a long wooden table, a roaring fireplace, roasted meat and bread, peasants sitting down to eat."),
    ("But the tradition, according to some accounts, was that you brought your own plate. And your own firewood.", "Red arriving at the great hall door holding his own wooden plate in one hand and a log of firewood under the other arm, slightly confused."),
    ("Still, it's meat, it's warm, and nobody is making you work.", "Red at the long feast table with a huge grin, holding a big piece of roast meat, cheeks full."),
    ("Twelve days of Christmas, right through to Twelfth Night.", "Villagers dancing in a circle in a warm hall decorated with holly and ivy, a musician playing a pipe, Red dancing in the middle."),
    ("And then, on the first Monday after, the party's over.", "The morning after: holly decorations on the floor, cold grey light, Red slumped at the empty table looking exhausted."),
    ("In parts of England this was called Plough Monday.", "A group of village men dragging a wooden plough decorated with ribbons through the snowy village street, cheering."),
    ("Which tells you exactly what you're doing that day.", "Red pushing a heavy plough through a hard frozen field with a deeply tired face.", M("75")),
    # 6. Las grandes heladas
    ("Now we get to the hard part.", "Red bracing himself in a field as a huge dark wall of blizzard rolls toward him."),
    ("Some medieval winters were brutal.", "A medieval village almost completely buried in snow, only the roofs and the church tower sticking out, howling wind."),
    ("In 1410, according to a London chronicle, a frost lasted fourteen weeks", "A friar in a grey habit writing in a big chronicle book by candlelight in a cold stone friary, frost creeping across the window and the inkwell."),
    ("and the Thames froze so solid that people could walk, and even ride horses, across it.", "A wide frozen river Thames with old London Bridge and its many arches and houses in the background, medieval Londoners walking across the ice and a man riding a horse on it."),
    ("In the winter of 1281 to 1282, when the ice finally broke, it smashed arches of London Bridge.", "Huge blocks of river ice crashing into the arches of medieval London Bridge, stones and timbers breaking and falling."),
    ("People had been crossing the river on foot.", "Medieval Londoners in cloaks happily strolling across a frozen river, a child sliding on the ice."),
    ("Dry-shod.", "Red standing in the middle of the frozen river lifting one foot to proudly show a perfectly dry leather shoe."),
    ("And the winter of 1205 is the one I promised you.", "Red pointing at the viewer with a knowing wink, snow falling."),
    ("A frost that started in mid-January and lasted until late March.", "A frozen English countryside: a frozen pond, white trees, a frozen windmill, a pale low sun."),
    ("No one could work the ground.", "Red swinging a pickaxe at the frozen ground and it bouncing off with a clang, his whole body vibrating."),
    ("And, according to an old account of great English frosts, ale and wine froze so hard that they were sold by weight.", "A medieval market in the snow: a merchant weighing solid blocks of frozen red wine and frozen ale on a big balance scale, customers waiting with coins."),
    ("You haven't truly lived until you've had to chew your beer.", "Red gnawing on a block of frozen golden ale with his teeth, eyes watering from brain freeze."),
    ("In the winter of 1434, the Thames froze from London Bridge all the way down to Gravesend, from Christmas Day to the 10th of February.", "Bird's-eye view of a long white frozen river winding from medieval London toward the sea, ships frozen in place along it."),
    ("Ships couldn't get through, so goods had to be hauled into London overland.", "Wooden medieval cargo ships stuck in the ice, while a line of horse-drawn carts full of barrels and sacks heads along a snowy road toward the city."),
    ("Which, in medieval roads covered in snow, is about as fun as it sounds.", "Red pushing a cart full of barrels that is stuck deep in snow and mud, the horse looking back at him unimpressed."),
    ("And if you want to see what February looked like back then, there's a famous painting.", "Red standing in front of a big gilded medieval painting on a wall, hand on chin like a museum visitor."),
    ("In a French prayer book made for a duke around 1412 to 1416, Les Très Riches Heures,", "A luxurious illuminated medieval prayer book lying open on a lectern, with gold leaf, deep blue borders and tiny painted scenes, candlelight. No legible text."),
    ("the page for February shows a snowy farm. Sheep huddled in their pen. A man hauling firewood.", "A snowy medieval farmyard in the style of a 15th-century illuminated calendar page: sheep huddled in a wattle pen, beehives under snow, a man carrying firewood, a donkey, birds pecking in the snow."),
    ("And peasants inside, sitting as close to the fire as humanly possible, trying to thaw out.", "Inside a small farmhouse with the front wall open like a doll's house, peasants sitting right up against the fire with their robes lifted a little to warm their shins, steam rising. Family friendly."),
    ("Six hundred years later, it's still the most relatable painting of winter ever made.", "Red sitting in exactly the same pose by the fire, shins toward the flames, looking at the viewer as if to say 'same'."),
    ("And here's the real danger.", "Red holding open a small sack of seed grain, looking worried."),
    ("When the ground freezes for months, you can't plough or sow.", "A plough frozen solid into a white field, icicles hanging from its handles."),
    ("And a late spring means a late, small harvest.", "A sparse, thin wheat field with short stalks under a grey sky, Red holding up a tiny bundle of wheat."),
    ("Which means next winter, you start with even less.", "Red looking into an almost empty grain store with just a few sacks, his shadow long behind him.", M("40")),
    # 7. Marzo
    ("If you make it to March, congratulations.", "Red, thin and tired, stepping out of the hut into melting grey snow, a single sad piece of confetti falling."),
    ("You've reached the most dangerous part.", "Close-up of Red's tired smile slowly dropping into worry."),
    ("Historians sometimes call it the hungry gap.", "An almost empty barn: one small sack of grain, empty barrels, cobwebs, a mouse looking disappointed."),
    ("Your salted meat is running out.", "Red reaching deep into a big wooden barrel, scraping the very bottom, only one small scrap of meat left."),
    ("The grain is running low.", "Red holding an almost empty sack of grain upside down, a few grains falling out."),
    ("And the new crops won't be ready for months.", "A muddy field with tiny green sprouts barely poking out, Red kneeling and staring at them impatiently."),
    ("The first wild greens are only just starting to show up.", "Red in a thawing forest picking small wild greens and nettles, flinching from the stings."),
    ("And the Church timing doesn't help: this is also Lent, forty days of fasting with no meat.", "A priest at the church door wagging his finger at Red, who is hiding a small ham behind his back."),
    ("So your diet becomes salted herring. And hope.", "Red at the table staring at a single dried salted herring on his wooden plate, hands clasped in hope.", M("25")),
    # 8. El peor caso
    ("And sometimes, it's not one bad winter.", "Red looking up at a heavy grey sky, rain starting to fall."),
    ("It's a string of bad years.", "Pages of a calendar flying away in the wind and rain over a muddy village."),
    ("Starting in 1315, it rained, and rained, and stayed cold, across Northern Europe.", "Endless heavy rain over flooded fields and a village, cold grey light, a stream overflowing its banks."),
    ("Crops rotted in the fields, year after year.", "Blackened, flattened wheat rotting in a waterlogged field, Red standing in it up to his ankles, devastated."),
    ("It became known as the Great Famine.", "Thin, tired medieval villagers lining up at a monastery gate where a monk hands out small loaves of bread. Sad but not graphic."),
    ("It hit a region of around thirty million people, from Ireland to Poland,", "An old parchment-style map of northern Europe from Ireland to Poland slowly darkening with grey rain clouds, only coastlines and little painted villages. Absolutely no labels, letters, words or names anywhere."),
    ("and the crops kept failing until the harvest of 1317.", "Red holding up a tiny, sad, half-rotten bundle of wheat in the rain while his family watches."),
    ("And right after it came a cattle plague that, in some places, killed most of the herds.", "A green pasture with just a few cows, surrounded by many faded ghostly outlines of cows that are no longer there."),
    ("The cows that kept you warm, and alive.", "Red hugging his brown-and-white cow tightly around the neck with sad eyes."),
    ("Some historians see this as the start of a colder era in Europe, often called the Little Ice Age.", "Frost creeping across an old map-like landscape of European villages and fields, everything turning icy blue. No text."),
    ("Exactly when it began is still debated,", "Three historians in modern clothes arguing around a table covered in old charts and ice cores, each pointing at a different spot."),
    ("but your grandchildren's winters weren't getting any easier.", "An old Red with a white beard and his red scarf, surrounded by grandchildren, all shivering together in a snowstorm.", M("5", blink=True, note="it was a bad decade")),
    # 9. Primavera
    ("But let's say you made it.", "Red pushing open the door of his hut, bright sunlight pouring in on his face, squinting."),
    ("The snow melts.", "Snow melting off a thatched roof, water dripping from the eaves, puddles shining."),
    ("The days get longer.", "A bright sun high over green fields with patches of melting snow, birds flying."),
    ("The first green shoots come up.", "Close-up of bright green shoots pushing up through the last patch of snow."),
    ("The cow, somehow, is still alive.", "The brown-and-white cow standing in a fresh spring meadow looking smug, a flower in its mouth, Red beside it amazed.", M("60", note="you made it!")),
    ("You've survived five months of smoke, salt, darkness, frozen beer and a bed shared with six people and a cow.", "Red outside in the spring sun taking a deep breath of fresh air, his family and the cow behind him, a smoky hut in the background."),
    ("And in about seven months, you get to do it all again.", "Red's happy smile freezing as a single autumn leaf and then a snowflake drift down in front of his face."),
    ("So, be honest: how many months would you have lasted? November? February? Tell me in the comments.", "Red pointing at the viewer with a playful grin, a round painted wheel behind him with five little picture slices: a pig, a candle, a holly branch, a snowflake and a herring. Pictures only, absolutely no letters, words or numbers anywhere."),
    ("And if you want to find out what else you wouldn't survive, you know what to do.", "Red standing in front of three glowing doorways showing ancient Rome, a Viking longship and an Egyptian pyramid."),
    ("Red needs all the help he can get.", "Red waving goodbye with a big smile, standing in the snow, his red scarf blowing in the wind."),
]

BASE = (
    "Use the attached character sheet as the exact design reference for the main character \"Red\" "
    "(round white head, large expressive eyes, thin black stick body and limbs, bright red scarf). "
    "2D hand-drawn cartoon illustration, warm comic style, clean bold black outlines, flat colors with soft shading. "
    "{SCENE} Single clear idea, main subject large in frame. Unless stated otherwise, Red is a poor medieval English "
    "peasant in a brown wool tunic and hood, always with his bright red scarf, and the setting is medieval England in "
    "winter, with a palette of cold snowy blues and warm orange firelight. Peasant huts have a single open fire on a stone ring in the middle of the dirt floor, with no fireplace and no chimney. Historically plausible 13th-15th century details; "
    "all people drawn in the same simple round-headed stick-figure cartoon style. "
    "No text, no letters, no watermark, no border, full-bleed. 16:9."
)

scenes = []
for i, item in enumerate(S, 1):
    scene = {"id": f"{i:03d}", "text": item[0], "SCENE": item[1]}
    if len(item) > 2:
        scene["meter"] = item[2]
    scenes.append(scene)

# Comprobación: los textos juntos deben ser exactamente la narración (sin etiquetas de voz).
narration = re.sub(r"\[(pause|sarcastic|whispers)\]\s*", "", (HERE / "narracion.txt").read_text())
got, want = " ".join(s["text"] for s in scenes).split(), narration.split()
if got != want:
    k = next(i for i, (a, b) in enumerate(zip(got + [""], want + [""])) if a != b)
    raise SystemExit(f"los textos no cuadran con narracion.txt en la palabra {k}: {got[k - 5:k + 5]} vs {want[k - 5:k + 5]}")

(HERE / "escenas.json").write_text(json.dumps({
    "reference": "imagenes/red-ficha/red-oficial.png",
    "model": "seedream_5_0_flash",
    "params": ["--aspect-ratio", "16:9", "--resolution", "2k"],
    "base": BASE,
    "scenes": scenes,
}, indent=1, ensure_ascii=False) + "\n")
print(f"ok  {len(scenes)} escenas")
