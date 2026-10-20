"""Fuente de las escenas del video #3: genera escenas.json (prompts) y comprueba que los textos cubren toda la narración.

Uso: python3 videos/03-medieval-night/escenas.py
Cada escena: (texto narrado exacto, sin etiquetas de voz | descripción de la imagen | medidor opcional).
El medidor ("meter") se mantiene hasta que otra escena lo cambie. Aquí son las probabilidades de ver el amanecer.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent


def M(value, **kw):
    return {"value": value, "label": "SUNRISE ODDS", **kw}


S = [
    # 0. Gancho
    ("It's midnight. You went to bed four hours ago.", "Dark one-room peasant hut at night lit only by blue moonlight through a small window. Red lying in a straw bed under a patched wool blanket, eyes closed, a full moon visible through the window."),
    ("And now you're wide awake.", "Red sitting bolt upright in his straw bed in the dark moonlit hut, eyes huge and wide awake, looking straight at the viewer."),
    ("And so is everyone else in your house.", "Red's whole family (mother, father, grandmother, two small kids) all sitting up calmly in the same big straw bed in the moonlit hut, all wide awake and relaxed, Red in the middle looking around at them in surprise."),
    ("Because for most of history, people didn't sleep through the night.", "A row of medieval cottages at night seen from outside, in each small window a sleepy round-headed figure sitting up awake in bed, deep blue night sky with stars."),
    ("They slept twice.", "Red asleep in bed, a simple drawing of two moons side by side floating above his head like a dream bubble, peaceful deep blue night."),
    ("Welcome to night in medieval England.", "Wide establishing shot of a small medieval English village at night with no lights at all: dark thatched cottages, a small stone church, bare trees, a huge starry sky and a full moon, Red small in the foreground looking up. Deep blues.", M("100")),
    ("Up to sixteen hours of darkness, no light switch,", "Red in his dark hut feeling along the mud wall with both hands, searching for a light switch that does not exist, puzzled face, only faint moonlight."),
    ("and a whole list of things out there that want you.", "Red peeking out of his cottage door into the dark night: in the black trees and shadows around the village, many pairs of glowing eyes and spooky silhouettes stare back. Spooky but funny."),
    ("That meter in the corner? Your odds of seeing sunrise.", "Red standing in the dark village lane pointing up toward the top-right corner of the frame with a nervous face, leaving the top-right corner empty. Deep blue night."),
    ("And stick around, because one man's midnight habit got so bad,", "Inside a dark stone castle bedchamber, a silhouette of a medieval knight in a nightshirt standing on his bed with closed eyes, swinging a sword wildly in the moonlight."),
    ("his own family moved out.", "A medieval noble lady and two children tiptoeing out of a castle door at night carrying bundles and a candle, looking back nervously over their shoulders."),
    # 1. 6 PM
    ("Let's start at sunset.", "A medieval English village at sunset, the sun sinking behind bare hills, orange and purple sky, villagers walking home with tools on their shoulders, Red among them."),
    ("In winter, that's before four in the afternoon.", "Red standing in a frosty field holding a hoe, staring in disbelief at the sun already setting behind the trees while it is still afternoon, long shadows."),
    ("And for you, the day is basically over.", "Red closing the wooden door of his small thatched cottage from the inside as the last orange light fades outside, resigned face."),
    ("Light costs money, and you don't have money.", "Red holding up a tiny dim rushlight (a thin reed dipped in fat burning in a small iron clip), looking at its weak flame, then at his empty leather purse turned upside down."),
    ("So you do what everyone does.", "Night view of the village: in every cottage the last little light goes out one by one, deep blue."),
    ("You eat, you pray,", "Red's family sitting on stools around the small open fire in the middle of the hut floor, eating pottage from wooden bowls, then hands folded in prayer, warm firelight."),
    ("and you go to bed. Early. Really early.", "Red climbing into the straw bed, yawning hugely, while through the window the sky is still dusky purple, not even fully dark."),
    ("You already know the bed situation. Straw, wool blanket, the whole family.", "Red squeezed in the middle of a straw mattress on the floor between his father, mother, grandmother and two small siblings, all under one rough wool blanket, a sleeping dog at their feet, dim firelight."),
    ("Cozy.", "Close-up of Red in the crowded family bed with a little brother's foot pressing against his cheek and grandma snoring loudly beside him, Red with a sarcastic tired smile."),
    ("And here's a detail you didn't expect.", "Red sitting up in bed holding a finger up as if he just remembered something surprising, eyebrows raised, warm candle glow."),
    ("Medical books, from the late Middle Ages onward, told you exactly how to lie:", "An open old medical book on a wooden table lit by a candle, with simple painted pictures of a sleeping man on a bed and curved arrows. Pictures only, absolutely no letters, words or numbers."),
    ("on your right side for your first sleep,", "Red lying in bed on his right side, eyes closed, a big friendly curved arrow drawn in the air pointing to his right side. Calm deep blue night."),
    ("then turn to your left.", "Red rolling over in bed onto his left side, with a curved motion arrow showing the turn, sleepy face."),
    ("It was supposed to help digestion.", "Cartoon cross-section of Red's round belly with a happy little bowl of pottage inside, Red lying on his side giving a sleepy thumbs up."),
    ("Even your sleeping position had instructions.", "Red lying stiff in bed like a soldier at attention, eyes open, nervously checking which side he is on, a stern medieval doctor in a robe and round cap standing beside the bed wagging a finger."),
    # 2. 9 PM
    ("So you fall asleep.", "Red peacefully asleep in the dark hut, little z's floating up, moonlight on the blanket.", M("100")),
    ("And if you wake up feeling like something heavy is sitting on your chest, well, you have a word for that.", "Red lying on his back in bed, eyes wide open in terror, unable to move, while a small hairy brown goblin-like creature with glowing yellow eyes sits on his chest grinning down at him. Spooky but funny, not gory.", M("90")),
    ("The nightmare.", "Close-up of the small hairy goblin creature sitting on the sleeper's chest, grinning straight at the viewer with glowing yellow eyes, deep purple darkness around."),
    ("And in the Middle Ages, it wasn't a bad dream.", "Red sitting up in bed pointing at the little goblin creature now sitting at the foot of the bed, Red's face saying 'that's not a dream, that's a guy'."),
    ("The \"mare\" was a creature, a spirit that sat on sleepers in the night.", "A medieval illuminated manuscript page with a small painted picture of a dark imp sitting on a sleeping person's chest, gold leaf border. Pictures only, absolutely no letters, words or numbers."),
    ("The word shows up in English around the year 1300, describing exactly that.", "A medieval monk scribe at a desk by candlelight, writing in a big book with a quill, while the little goblin creature peeks over his shoulder curiously."),
    ("And the mare wasn't the only thing out there.", "Red pulling the blanket up to his eyes in bed, while outside the small window pale ghostly shapes drift past in the night."),
    ("Around 1400, a monk at Byland Abbey, in Yorkshire,", "The large stone Cistercian abbey church of Byland in Yorkshire at night, tall gothic arches and a big round rose window, monks' candlelight glowing inside, moors around."),
    ("filled the blank pages of a manuscript with local ghost stories.", "A monk at a wooden desk writing in an old manuscript by candlelight, small pale ghostly figures rising up out of the open pages like smoke."),
    ("And these weren't ghosts that went \"boo\".", "A pale cartoon ghost in a white sheet shrugging with its arms out, with a bored face, next to Red who looks unimpressed. Night lane."),
    ("They were souls stuck in purgatory, and they wanted something.", "A pale translucent ghost of a medieval villager standing in a dark country lane at night, holding out its hand pleadingly toward a terrified peasant holding a lantern."),
    ("Usually, prayers.", "The pale ghost kneeling with its hands folded in prayer, looking hopefully at Red, who holds a small wooden prayer-bead string. Moonlight."),
    ("Sometimes, they wouldn't leave you alone until they got them.", "Red walking home at night with a lantern, the pale ghost floating right behind him, then sitting next to him at the table, then peeking over his bed, Red exhausted."),
    ("So people protected their homes.", "Red standing at the doorway of his cottage at night making the sign of the cross toward the dark outside, serious face, his family watching from the bed.", M("80")),
    ("In Chaucer's Canterbury Tales, written in the late 1300s,", "A group of medieval pilgrims on horseback riding along a road toward a distant cathedral, a cheerful round-faced poet in a grey hood riding among them, illuminated-manuscript style. Pictures only, no letters."),
    ("a carpenter says a \"night-spell\" at the four corners of his house and at the door.", "A medieval carpenter in an apron with a saw on his belt, walking to each corner of his timber house at night, solemnly making blessing gestures, then at the threshold of the door."),
    ("Basically, medieval home security.", "Red proudly standing in front of his tiny cottage at night with his arms crossed, little glowing protective sparkles around each corner of the house and the door, a ghost bouncing off an invisible shield."),
    # 3. Medianoche
    ("And now, it's midnight.", "Moonlit exterior of Red's cottage under a huge starry sky, the moon high in the middle of the sky, absolute silence, deep blue."),
    ("And you wake up.", "Red's eyes snapping open in the dark, close-up of his round white face on the straw pillow, moonlight."),
    ("Not because of a noise. Not because of the ghost.", "Red sitting up in bed glancing at the door and at the window, the pale ghost outside the window holding its hands up innocently as if to say 'not me'."),
    ("Just because it's time.", "Red sitting up in bed calmly stretching his arms and yawning, perfectly relaxed, as if it were morning, though it is the middle of the night."),
    ("Historian Roger Ekirch spent years digging through old diaries, court records and books,", "A modern historian with glasses and a cardigan sitting in an archive surrounded by towering piles of old leather books, rolled documents and diaries, reading with a magnifying glass under a desk lamp."),
    ("and found hundreds, and eventually thousands, of references to a \"first sleep\" and a \"second sleep\".", "The modern historian standing on top of an enormous mountain of old books and documents, holding one up triumphantly, papers flying."),
    ("In France, they called it \"premier somme\".", "A sleepy medieval French peasant in a nightcap sitting up in bed in a cottage, a small blue-white-red striped pennant on the wall, moonlight."),
    ("In Italy, \"primo sonno\".", "A sleepy medieval Italian peasant in a nightcap sitting up in bed in a stone house with a terracotta roof visible through the window, cypress trees outside in moonlight."),
    ("Even Chaucer mentions it.", "A cheerful medieval poet with a plain WHITE round head (not red), a small grey beard drawn on and a grey hood, writing with a quill by candlelight, winking at the viewer. He wears no red scarf."),
    ("In one of his tales, a princess goes to bed just after dark,", "A young medieval princess with a small golden crown climbing into a canopy bed in a castle room while the evening sky outside the window is still deep blue."),
    ("sleeps her \"first sleep\", and wakes up.", "The princess sitting up in her canopy bed in the middle of the night, wide awake and fresh, moonlight streaming in."),
    ("So between your two sleeps, you've got about an hour. Maybe more.", "Red sitting in his straw bed in the dark holding up one finger, a simple hourglass on the floor beside him with sand running."),
    ("In the dark.", "Almost total darkness: only Red's round white face and big eyes visible, floating in black."),
    ("What do you do with it?", "Red sitting on the edge of the bed in the dark scratching his head, looking around the moonlit hut with a thinking face."),
    # 4. Opciones
    ("Option one: you pray.", "Red kneeling beside the straw bed in the moonlight with his hands folded and eyes closed, praying peacefully.", M("80")),
    ("This was considered a perfect time for it. Quiet, dark, nobody asking you for anything.", "Red praying in the silent moonlit hut while the rest of the family sleeps soundly, the cow dozing in the corner, a calm peaceful mood."),
    ("Monks took it seriously.", "A line of medieval Benedictine monks in black habits walking through a dark stone cloister at night, each holding a candle, sleepy but determined faces."),
    ("The Rule of Saint Benedict told them to get up at the eighth hour of the night in winter, around two in the morning, for the night prayers.", "A sleepy monk being woken in a stone dormitory by another monk ringing a small hand bell, rows of simple beds, dark night, one candle."),
    ("Every night.", "The same sleepy monk with huge dark bags under his eyes walking to church holding a candle, looking exhausted, while the moon shines."),
    ("Option two: you think about your dreams.", "Red sitting up in bed, chin in hand, with a big dream bubble above his head showing a fish and a snake.", M("80")),
    ("Because to you, dreams meant something.", "Red staring seriously at the dream bubble above his head, which now shows a black cat and a golden coin, worried face."),
    ("The most popular dream book of the Middle Ages, the \"Dream Book of Daniel\",", "An old leather-bound medieval book lying open on a wooden table by candlelight, with tiny painted pictures of a fish, a snake, a crown and a tooth in rows. Pictures only, absolutely no letters, words or numbers."),
    ("was basically an alphabetical list of things you might dream about, and whether they meant good luck or bad.", "Red reading a long unrolled parchment scroll by candlelight that spills onto the floor, with little pictures next to green thumbs-up and red thumbs-down signs. Pictures only, absolutely no letters, words or numbers."),
    ("Option three: chores.", "Red getting out of bed in the dark, rolling up his sleeves, ready for work."),
    ("Check the fire.", "Red kneeling by the open fire on the stone ring in the middle of the hut floor, gently blowing on the glowing embers to keep them alive."),
    ("Check the animals.", "Red holding a tiny rushlight, checking on the brown-and-white cow and two chickens in the corner of the hut, the cow blinking sleepily at him."),
    ("Use the chamber pot, which lived under the bed.", "Red pulling a plain clay pot out from under the straw bed, making an awkward face."),
    ("Yes, in the same room.", "Red's whole sleeping family in the same small room, one eye open each, looking at Red with the pot, Red frozen with an embarrassed sweaty smile."),
    ("If you had a baby, this was feeding time.", "A tired medieval mother sitting by the embers at night holding and feeding a swaddled baby, her eyes half closed."),
    ("A French farce from the 1400s shows parents getting up at midnight to rock, walk and feed their child.", "A tired medieval father in a nightshirt pacing the dark room bouncing a crying swaddled baby, while the mother rocks an empty wooden cradle, both exhausted."),
    ("Some things never change.", "Split image: on the left a medieval father pacing with a crying baby at night, on the right a modern father in pajamas doing exactly the same with an identical pose."),
    ("Option four.", "Red looking at the viewer, slowly raising one eyebrow, slightly awkward smile.", M("80")),
    ("A French doctor in the 1500s, Laurent Joubert,", "A 16th-century French physician with a short beard, a black doctor's cap and robe, sitting at a desk writing a book with a quill, very serious."),
    ("wrote that working people had their best, ahem, \"couple time\" after the first sleep, because they weren't exhausted anymore.", "A peasant couple's feet poking out from under a wool blanket in a dark hut, little pink hearts floating above the bed, tasteful and funny, nothing explicit."),
    ("Thank you, doctor. Very helpful.", "Red facing the viewer with an awkward thumbs up and a deadpan face, the serious doctor nodding proudly in the background."),
    ("And option five: according to Ekirch's research, some people even got up and visited the neighbors.", "Red in a nightshirt holding a candle knocking on the door of the neighbor's cottage at night; the neighbor opens the door, also in a nightshirt and holding a candle.", M("75")),
    ("In the middle of the night.", "Red and his neighbor sitting on a bench outside the cottage under the stars at night, chatting and sharing a small loaf of bread, candles beside them."),
    ("Imagine your neighbor knocking at one in the morning, and that's normal.", "A modern person in pajamas opening an apartment door in the middle of the night, shocked, to find a medieval peasant with a candle waving cheerfully."),
    # 5. 1 AM
    ("But here's the thing. You probably shouldn't go far.", "Red stepping out of his cottage door into the dark lane with a candle, then pausing, looking into the pitch-black night ahead, uneasy."),
    ("Because in medieval England, the night had its own rules.", "A dark medieval town street at night with timber houses, shuttered windows, and a single lantern hanging, an ominous empty mood."),
    ("The Statute of Winchester, in 1285,", "A medieval English king with a crown seated on a throne, a clerk beside him holding up a long official parchment with a big red wax seal. Pictures only, no letters."),
    ("ordered the gates of walled towns closed from sunset to sunrise,", "The heavy wooden gates of a walled medieval town swinging shut at dusk, guards pushing them closed, the last travellers hurrying in."),
    ("and set a watch: in a city, six men at every gate, all night long.", "Six medieval watchmen with spears and lanterns standing in a row in front of a closed town gate at night, stern faces, torches on the wall."),
    ("And if you were a stranger walking around at night?", "A watchman with a lantern and spear stepping out of the shadows and blocking the way of Red, who holds a candle and makes an innocent face.", M("70")),
    ("The watch could hold you until morning.", "Red sitting on a bench in a small stone guardroom at night, arms crossed, sulking, a watchman dozing by the door with his spear."),
    ("If they still didn't like you then, they handed you over to the sheriff.", "Morning light: the watchman handing Red over to a stern medieval sheriff in a fur-trimmed coat, Red looking very worried.", M("60")),
    ("And even without the law, the dark was dangerous on its own.", "Red alone on a pitch-black country road at night holding a tiny candle, huge darkness all around him."),
    ("No streetlights, unpaved roads, ditches, rivers.", "Red tiptoeing along a muddy rutted path at night in the dark, a ditch on one side and a black river on the other, his candle flickering."),
    ("Getting lost on your way home was a real way to end your night. Permanently.", "Red's candle blowing out, Red frozen at the edge of a dark muddy ditch with one foot in the air, comic panic, only his eyes visible."),
    # 6. 3 AM
    ("Now, remember the man whose family moved out? Here he is.", "Exterior of a medieval stone castle at night under the moon, one window lit by a flickering candle."),
    ("His name was Pierre de Béarn, a French nobleman.", "Portrait of a medieval French nobleman with a neat beard in a rich blue and gold tunic, standing proudly in a castle hall, round-headed stick-figure cartoon style like the other characters."),
    ("The chronicler Jean Froissart wrote that after he killed a huge bear,", "The nobleman in a snowy forest standing triumphantly with a spear next to a huge brown bear lying defeated, cartoonish, no blood."),
    ("Pierre started getting up in his sleep and grabbing his sword, fighting nobody.", "The nobleman in a white nightshirt, eyes closed, sleepwalking through a castle bedroom at night swinging a sword at empty air, furniture knocked over."),
    ("And when he couldn't find it, he made such a racket that, in Froissart's words, it seemed like all the demons of hell were in there with him.", "The sleepwalking nobleman in a nightshirt with eyes closed yelling and stomping around a dark castle room, cartoon noise lines everywhere, servants covering their ears in the doorway."),
    ("His family eventually left.", "The nobleman's wife and children walking away from the castle at dawn on a road with packed bags and a cart, the castle behind them."),
    ("Honestly? Fair.", "Red sitting up in his own bed giving a slow understanding nod to the viewer with raised eyebrows.", M("55")),
    # 7. Segundo sueño
    ("Anyway. After an hour or so, you get sleepy again, and you go back for your second sleep, until the sun comes up.", "Red yawning and snuggling back down into the straw bed with his family, pulling up the blanket, the moon lower in the sky through the window."),
    ("And here's the crazy part.", "Red popping his head back up from under the blanket with a surprised face, a lightbulb-like candle flame above his head."),
    ("In the early 1990s, a psychiatrist named Thomas Wehr put volunteers in darkness for fourteen hours a day, for a month.", "A 1990s research lab at night: a scientist in a white coat with a clipboard standing in a darkened room with several simple beds where volunteers lie, a big wall clock, all round-headed cartoon figures."),
    ("No lamps, no screens.", "A volunteer in a dark lab bedroom reaching for a lamp that has been taken away, and a TV with its plug pulled out, confused face."),
    ("By the fourth week, their sleep had split in two all by itself.", "A simple chart on a chalkboard showing a long dark bar split into two blocks with a gap in the middle, the scientist pointing at the gap in amazement. Shapes only, absolutely no letters or numbers."),
    ("About four hours of sleep, one or two hours awake, then four more hours.", "A volunteer in a dark lab bed: asleep, then sitting up awake calmly in the dark, then asleep again, three small moments side by side."),
    ("Just like the old records described.", "The modern historian in his archive and the 1990s scientist in his lab coat shaking hands and smiling, piles of old books on one side and lab equipment on the other."),
    ("So if you sometimes wake up at three in the morning and can't sleep,", "A modern person in pajamas lying awake in a dark bedroom at night staring at the ceiling, worried."),
    ("maybe nothing's wrong with you. Maybe your body is just a little medieval.", "The same modern person in pajamas, now relaxed, sitting up in bed next to Red the medieval peasant with his red scarf, both awake in the night and smiling at each other."),
    ("To be fair, not every historian agrees.", "Two historians with glasses arguing over a big old book on a desk, one shaking his head, one nodding."),
    ("Some think \"first sleep\" could just mean the first part of one sleep, and that the waking was short.", "A skeptical historian holding a magnifying glass over an old manuscript, eyebrow raised, a thought bubble showing a sleeper waking only for a quick blink."),
    ("But the experiment is hard to ignore.", "The scientist in the lab coat holding up the chalkboard chart with the split dark bar, confident smile. Shapes only, no letters or numbers."),
    # 8. Amanecer
    ("And then, finally, the sun comes up.", "Dawn breaking over the medieval village, golden sunrise over the hills, a rooster crowing on a fence, mist in the fields.", M("70", note="you made it!")),
    ("You survived the nightmare, the ghosts, the watch, the ditches and a neighbor knocking at one in the morning.", "Red stepping out of his cottage door into the golden morning light, stretching his arms, while behind him the little goblin, a ghost, a watchman, and the neighbor with a candle wave goodbye."),
    ("And now you get to work in the fields for the next ten hours.", "Red standing in a muddy field at sunrise holding a hoe, with big dark bags under his eyes, deadpan face."),
    ("And tonight, you do it all again.", "Red looking up at the sky where the sun is already starting to set on the horizon, horrified face."),
    ("So, be honest. You wake up at midnight with an hour to kill. What are you doing?", "Red sitting on the edge of his bed at night facing the viewer, holding a candle, curious inviting expression."),
    ("Praying, chores, or visiting the neighbors? Tell me in the comments.", "Three small panels side by side: Red praying by the bed, Red blowing on the fire embers, Red knocking on the neighbor's door with a candle."),
    ("And if you want to know what else medieval peasants did when nobody was watching, you know what to do.", "Red standing in front of his cottage at dawn waving goodbye to the viewer with a big smile, his red scarf fluttering, warm golden light."),
]

BASE = (
    "Use the attached character sheet as the exact design reference for the main character \"Red\" "
    "(round plain WHITE head, large expressive eyes, thin black stick body and limbs, bright red scarf). "
    "2D hand-drawn cartoon illustration, simple clean style, clean bold black outlines, flat colors with minimal shading. "
    "{SCENE} Single clear idea, main subject large in frame, few elements, uncluttered background. Unless stated otherwise, "
    "Red is a poor medieval English peasant in a brown wool tunic, always with his bright red scarf, and the setting is "
    "medieval England at night, with a palette of flat deep night blues and warm candle or ember light. Peasant huts have "
    "a single open fire on a stone ring in the middle of the dirt floor, with no fireplace and no chimney. Historically "
    "plausible 13th-15th century details; all people drawn in the same simple round-headed stick-figure cartoon style. "
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
