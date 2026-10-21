"""Fuente de las escenas del video #4: genera escenas.json (prompts) y comprueba que los textos cubren toda la narración.

Uso: python3 videos/04-medieval-law/escenas.py
Cada escena: (texto narrado exacto, sin etiquetas de voz | descripción de la imagen o R("ruta") para reutilizar | medidor opcional).
El medidor ("meter") se mantiene hasta que otra escena lo cambie. Aquí es lo seguro que está tu cuello.
Objetivo de ahorro (21-oct-2026): ~70 escenas, con imágenes reutilizadas de videos anteriores y del propio video.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent


def M(value, **kw):
    return {"value": value, "label": "NECK METER", **kw}


def R(path):
    """Reutiliza una imagen ya generada (ruta desde la raíz del repo) en lugar de generar una nueva."""
    return {"reuse": path}


PIG = "Inside a small medieval courtroom, a pink pig standing upright in the wooden dock wearing a small brown jacket and gloves, looking smug, a stern medieval judge in a dark robe and cap behind a bench, a few onlookers. Funny, cartoonish."
CROSS = "Red barefoot in a long plain white robe, carrying a small wooden cross in both hands, walking alone along a dusty country road toward a distant harbor with ships, villagers by the road staring at him."

S = [
    # 0. Gancho
    ("You're hungry. Nobody's looking.", "A medieval English market on a sunny morning. Red, skinny, with a growling belly, stares at a round loaf of bread on a baker's stall while the baker has his back turned, chatting to someone."),
    ("And you're about to commit a crime in medieval England.", "Red slipping the round loaf of bread under his red scarf with a guilty little grin, glancing sideways, market stall behind him."),
    ("Bad news: somebody saw you. So what happens now?", "A medieval village woman with a basket pointing straight at Red with her mouth wide open in a shout, while Red freezes mid-step with the loaf poking out of his scarf, eyes huge.", M("100")),
    ("That meter in the corner? That's how safe your neck is. Every step from here, it can go up, or down.", R("videos/piloto-black-death/imagenes/009.png")),
    ("And stick around, because by the end, you'll meet the defendant who got the strangest trial in history.", "A dim medieval courtroom seen from the back of the room: a stern judge behind a high bench, and in the wooden dock a small mysterious figure completely covered by a dark cloth, curious onlookers leaning forward."),
    ("It was a pig.", PIG),
    # 1. ¡Al ladrón!
    ("First, your neighbor shouts. This is called the \"hue and cry,\" and it's not optional.", "A medieval villager cupping his hands around his mouth shouting at the top of his lungs in a village lane, while doors fly open and villagers burst out of their cottages holding pitchforks, brooms and sticks."),
    ("Under the Statute of Winchester, from 1285, when the cry goes up, everyone has to drop what they're doing and chase you.", R("videos/piloto-black-death/imagenes/128.png")),
    ("From town to town, until you're handed to the sheriff.", "A long chase across green rolling hills: Red running with the loaf, a crowd of villagers chasing him through one village and on toward the next, and far ahead a stern sheriff in a cloak waiting at a crossroads with his arms crossed."),
    ("And if they don't? The whole area can be held responsible for the theft.", "A royal official at a table in a village square collecting coins from a long line of grumpy villagers, each dropping a coin into a wooden chest."),
    ("So your neighbors aren't chasing you because they care about bread. They're chasing you because you're about to cost them money.", "Angry villagers running with pitchforks, each with a little gold coin floating in a thought bubble above his head, chasing Red across a field."),
    ("There's no police force. There's just everyone.", "Wide shot of half a medieval village chasing Red across a field: farmers, a blacksmith in an apron, an old granny with a broom, a small kid and a barking dog, Red running in front with the loaf.", M("85")),
    # 2. Una multa
    ("Now, here's something movies won't tell you. Most medieval crime never reached a gallows.", "Red stopping to catch his breath, holding up one finger to the viewer, while far away on a grassy hill an old empty wooden gallows stands covered in ivy and cobwebs, clearly unused. No people on it."),
    ("It ended up in the local manor court.", "A simple hall inside a medieval manor house: the lord's steward sitting at a wooden table, a clerk beside him with a long parchment roll and quill, a line of peasants waiting their turn, Red among them."),
    ("Skipped court? Two pence. Let your cow wander into someone's field? A fine. Brewed bad ale? Another fine.", "A brown-and-white cow happily munching cabbages in a neighbor's garden while the furious neighbor waves his arms and the cow's sheepish owner hands two small silver coins to the clerk."),
    ("The court rolls are full of these. Thousands of tiny, boring punishments.", "A gigantic parchment court roll unrolling across the whole floor of the manor hall and out of the door, the clerk sitting on top of it yawning hugely. Scribbles only, absolutely no letters, words or numbers."),
    ("So if you're lucky, this ends with a fine and a very awkward week with your neighbors.", "Red at the village well with a bucket, giving an awkward smile while three neighbors glare at him sideways with their arms crossed.", M("95")),
    # 3. Panaderos y picota
    ("Unless you sold the bread. Because medieval towns took bread very, very seriously.", "A stern medieval town official weighing a small loaf on a big brass balance scale at a bakery counter, frowning, while the nervous baker in a floury apron sweats."),
    ("In London, a baker caught selling loaves that were too light could be tied to a wooden frame called a hurdle and dragged through the streets. A record from 1316 shows exactly that happening.", "A medieval London street with timber houses: a baker in a floury apron lying tied on top of a flat woven wooden hurdle that a horse slowly pulls along the muddy street, the baker with an embarrassed face, townspeople watching and pointing. Humiliating, not violent."),
    ("And a 14th-century picture from Bristol shows a baker being punished with the bad loaf hanging around his neck.", "A medieval manuscript-style illustration on old parchment with a gold border: a baker on a wooden hurdle pulled by a horse, a small loaf of bread hanging from a string around his neck. Pictures only, absolutely no letters, words or numbers."),
    ("Then there was the pillory. Your head and hands locked in wood, in the market square,", "Red locked in a wooden pillory on a small platform in a busy medieval market square, his head and both hands through the holes, the loaf of bread hanging from a string around his neck."),
    ("while the whole town walks past.", "Townspeople walking past Red in the pillory: two women giggling behind their hands, a man pointing, a little kid sticking his tongue out, a goose staring at him."),
    ("The real punishment wasn't the wood. It was being seen.", "Close-up of Red in the pillory, blushing bright red with embarrassment, eyes squeezed shut, wishing he could disappear.", M("80")),
    # 4. Iron maiden
    ("Okay, but what about the torture? The iron maiden, the spikes, all of that?", "A dim museum room with a tall closed iron cabinet shaped like a woman with a carved face, a few spikes visible at the open edge, Red gulping nervously in front of it. Spooky but cartoonish, no blood, no victims."),
    ("Here's the uncomfortable part. There's no known mention of the iron maiden before the 1800s.", "Red surrounded by towering piles of old medieval books, holding a magnifying glass, flipping through pages and finding nothing, shrugging at the viewer."),
    ("The famous one in Nuremberg was a hoax, and showmen built copies to charge people money to look at them.", "A 19th-century showman in a top hat and checked suit standing outside a fair tent, holding out his hand for coins from a queue of Victorian visitors, the iron cabinet visible inside the tent."),
    ("A lot of \"medieval torture\" you've seen in museums is basically Victorian clickbait.", "A Victorian craftsman with a big mustache in a workshop, cheerfully screwing fake spikes onto a newly built iron cabinet and winking at the viewer, sawdust and tools around."),
    ("The real system was stranger than that.", "Red turning his back on the iron cabinet and walking away from the museum toward a sunny medieval village, looking back over his shoulder with a raised eyebrow."),
    # 5. Ordalías y jurado
    ("Let's say your case is serious. Before 1215, how does the court decide if you're guilty? It asks God.", "Red standing nervously before a stern medieval lord-judge in a stone hall; the judge and a priest beside him both look up toward a beam of golden light coming through a high window."),
    ("It's called trial by ordeal. In one version, the priest heats a piece of iron,", "Inside a stone church, a priest in white vestments holding a short iron bar with long tongs over a glowing fire, blessing it, Red watching in horror from the side."),
    ("you carry it a set number of steps,", "Red holding a glowing orange iron bar out in front of him with both hands, taking careful steps along a line of small marks on the church floor, sweating, eyes watering. Cartoonish, no injuries."),
    ("and your hand is bandaged. If it heals cleanly after a few days, you're innocent. If it doesn't...", "Red sitting on a bench with his hand wrapped in a big white bandage, while the priest slowly starts to unwrap it, both leaning in to look, Red sweating."),
    ("In another, you're thrown into blessed water.", "Red with a rope tied around his waist standing at the edge of a village pond, a priest blessing the water with raised hand, villagers holding the other end of the rope."),
    ("And here's the twist: if you sink, that's good. The water \"accepted\" you.", "Underwater view of the pond: Red sinking gently to the bottom, giving a confused thumbs up, a fish staring at him, the rope going up to the surface where villagers hold it."),
    ("Floating meant guilty.", "Red floating on the surface of the pond like a cork, arms out, while the villagers on the bank all point at him with stern faces."),
    ("Then, in 1215, the Church's Fourth Lateran Council banned priests from blessing ordeals. Without the priest, the whole thing collapsed. In England, it was replaced by something new.", "A grand hall full of bishops in white mitres seated in rows, the pope on a throne raising his hand to speak, solemn and important."),
    ("A jury. Made of your neighbors.", "Twelve medieval villagers sitting in a row on a long wooden bench with their arms crossed, looking at Red, who stands in front of them."),
    ("The same neighbors who just chased you across three villages.", "The same twelve jurors on the bench, still muddy and sweaty, holding pitchforks and brooms, panting and glaring at Red, one with a leaf in his hair.", M("60")),
    # 6. Las dos salidas
    ("But you have two secret exits. Exit number one: run into a church.", "Red sprinting and throwing his arms around the big wooden door of a stone village church, while the chasing villagers skid to a sudden stop behind him."),
    ("It's called sanctuary. Inside, they can't drag you out.", R("videos/piloto-black-death/imagenes/075.png")),
    ("For up to forty days, you're protected and fed.", "Inside a stone church, a kind monk handing Red a bowl of steaming pottage, while through the open door the villagers wait outside, bored, sitting on the grass."),
    ("But then you have a choice: face trial, or \"abjure the realm.\"", R("videos/piloto-black-death/imagenes/091.png")),
    ("That means you confess, lose your property, and leave England forever.", "A medieval coroner in a dark robe holding a scroll, while Red sadly hands over all his belongings to an official: a cooking pot, a stool and a goat on a rope."),
    ("You walk to the port they pick for you, barefoot, carrying a wooden cross so everyone knows what you are.", CROSS),
    ("And if no ship is sailing? You walk into the sea every day, to show you really mean it.", "Red in his white robe holding the small wooden cross, wading knee-deep into a grey sea, looking at an empty horizon with no ships, a seagull watching."),
    ("Historians estimate hundreds of people a year took this road.", "A long line of barefoot people in plain white robes, each carrying a small wooden cross, walking along a coastal road toward a harbor."),
    ("Exit number two: read. Clergy were tried in Church courts, which didn't hang people.", "A tonsured monk walking happily out of a church court with a bishop giving him only a gentle scolding finger-wag, while outside a royal sheriff looks annoyed."),
    ("And from 1351, anyone who could read could claim to be clergy.", "Red standing before a judge holding up a big open book, sweating, the judge leaning forward curiously."),
    ("The test was usually the first verse of Psalm 51. People called it the \"neck verse,\" because reading it saved your neck. Some people who couldn't read just memorized it.", "Red holding the big book upside down with his eyes closed, reciting from memory with confidence, while the judge raises a suspicious eyebrow. The pages show only squiggles, no real letters."),
    ("After 1488, that trick only worked once. If you weren't really a priest, they branded your thumb so you couldn't use it again.", "Red staring at his raised thumb, which has a small neat black mark on it (no wound), while the judge points at it sternly.", M("75")),
    # 7. Doce peniques
    ("Now let's talk about what you actually stole. Because in medieval England, everything came down to twelve pence.", "A big wooden balance scale: on one side Red's round loaf of bread, on the other a small pile of silver pennies, the scale almost perfectly balanced, Red watching it closely."),
    ("Steal something worth less than a shilling, and it's \"petty larceny\": usually a whipping.", "Red wincing next to a wooden post in the village square while an official stands nearby holding a thin switch, before anything happens. No injuries."),
    ("Steal something worth more, and it's a felony. And the punishment for felony theft was hanging.", "A lonely wooden gallows silhouetted on a distant hill against an orange dusk sky, a few crows flying. No people, nothing graphic."),
    ("One penny could be the difference. So, how much was your bread worth?", "Red holding the loaf in one hand and counting on the fingers of the other, worried face, sweat drop.", M("40")),
    # 8. El verdugo
    ("If it goes wrong, you meet the executioner. And his life was weird too.", "A serious man in a dark cloak walking down a narrow German town street, while townspeople cross to the other side to avoid him and mothers pull their children away."),
    ("Just after the Middle Ages, in Nuremberg, an executioner named Frantz Schmidt kept a diary of his whole career. It lists three hundred sixty-one executions, and hundreds of smaller punishments.", "The same man, Frantz Schmidt, with a short beard, writing in a thick diary by candlelight in a small room, the steep red roofs of Nuremberg and its castle visible through the window. The pages show only squiggles, no real letters."),
    ("He didn't choose the job. His father was a woodsman, picked out of a crowd by a cruel local lord and forced to carry out an execution.", "A cruel-looking 16th-century German nobleman on horseback pointing straight at a frightened woodsman with an axe in a crowd of peasants."),
    ("After that, nobody would treat the family normally again. The job was inherited, like a curse.", "The woodsman's small family eating alone at a table in their house, a little boy among them, while neighbors whisper and point through the window."),
    ("But here's the part nobody expects. Schmidt was also a healer.", "Frantz Schmidt gently bandaging a peasant's leg in his house, shelves full of herb jars and bottles behind him, kind face."),
    ("By his own count, he treated about fifteen thousand patients. The man people avoided in the street was the one they secretly visited when they got sick.", "At night, a long line of townspeople wrapped in cloaks sneaking to Schmidt's back door, looking around to make sure nobody sees them, Schmidt holding the door open with a lantern."),
    ("And at seventy, he finally got what he'd wanted his whole life. In 1624, the Emperor officially restored his family's honor.", "An old Frantz Schmidt with a white beard holding an official parchment with a big red imperial wax seal, smiling for the first time, his family around him. Pictures only, no letters."),
    # 9. El cerdo
    ("And now, the trial I promised you. Falaise, France, 1386. A pig attacked and killed a small child.", "A medieval French town square under a big stone castle on a rock, townspeople gathered looking shocked, a pig being held on a rope by a guard. Nothing graphic, no child shown."),
    ("So the town did what towns did back then. They put the pig on trial. It was found guilty and sentenced to death.", R("@006")),
    ("And according to the records, it was dressed in human clothes for the execution.", "The pig, wearing a little jacket and gloves, being led through the medieval town square by two officials, a big crowd watching, Red in the crowd with his jaw dropped."),
    ("The executioner even filed a receipt for his fee. Justice, medieval style.", "A medieval executioner in a hood sitting at a desk handing a small parchment receipt to a town clerk, who pays him a few coins, both shrugging. Pictures only, no letters."),
    # 10. Veredicto
    ("So let's add it up. If you stole cheap, you'd probably get a fine or a whipping. If you got caught selling bad bread, the pillory.", "Red sitting on a tree stump counting on his fingers, with three small thought bubbles above his head: two coins, a wooden pillory, and a wooden post."),
    ("If the case got serious, you could run to a church and leave the country forever, or bet your life on one Latin sentence.", R("@044")),
    ("Your odds were better than the movies say. But they weren't great.", "Red finally eating his round loaf of bread with relief on a sunny village lane, but nervously glancing at a distant gallows on a hill.", M("70")),
    ("So, which exit would you have taken: the church, the boat, or the neck verse? Tell me in the comments.", R("videos/piloto-black-death/imagenes/109.png")),
    ("And if you want to know what you'd have done at night after all that, this one's next.", R("videos/03-medieval-night/imagenes/006.png")),
]

BASE = (
    "Use the attached character sheet as the exact design reference for the main character \"Red\" "
    "(round plain WHITE head, large expressive eyes, thin black stick body and limbs, bright red scarf). "
    "2D hand-drawn cartoon illustration, simple clean style, clean bold black outlines, flat colors with minimal shading. "
    "{SCENE} Single clear idea, main subject large in frame, few elements, uncluttered background. Unless stated otherwise, "
    "Red is a poor medieval English peasant in a brown wool tunic, always with his bright red scarf, and the setting is "
    "medieval England in daylight, with a bright, warm palette of flat greens, browns and sky blues. "
    "Historically plausible 13th-15th century details; all people drawn in the same simple round-headed stick-figure cartoon style. "
    "Never show blood, wounds or anyone being hurt. No text, no letters, no watermark, no border, full-bleed. 16:9."
)

scenes = []
for i, item in enumerate(S, 1):
    scene = {"id": f"{i:03d}", "text": item[0]}
    if isinstance(item[1], dict):
        ref = item[1]["reuse"]
        scene["reuse"] = f"videos/04-medieval-law/imagenes/{ref[1:]}.png" if ref.startswith("@") else ref
    else:
        scene["SCENE"] = item[1]
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
new = sum("SCENE" in s for s in scenes)
print(f"ok  {len(scenes)} escenas: {new} nuevas ({new * 0.5:g} créditos), {len(scenes) - new} reutilizadas")
