"""Fuente de las escenas del piloto: genera escenas.json (prompts) y comprueba que los textos cubren toda la narración.

Uso: python3 videos/piloto-black-death/escenas.py
Cada escena: (texto narrado exacto, sin etiquetas de voz | descripción de la imagen | medidor opcional).
El medidor ("meter") se mantiene hasta que otra escena lo cambie.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent

S = [
    # 0. Gancho
    ("You wake up with a fever.", "Red as a medieval English peasant waking up at night on a straw mattress, sweating, eyes wide, a single candle. Dark blue and warm candle tones."),
    ("There's a lump under your arm the size of an egg.", "Red as a medieval peasant lifting one arm and peeking under it in pure horror, a plain white egg floating beside him for size comparison (comedic, nothing graphic). Dim hut interior."),
    ("Your neighbor is already dead.", "Red as a medieval peasant peeking out of a small hut window at the neighbor's closed, silent hut across a muddy lane, a black crow on its thatched roof. Gloomy grey morning."),
    ("And the smartest doctors in Europe have just announced what's causing all this.", "A solemn group of medieval university scholars in long dark academic robes and caps standing in a stone hall, looking very confident. Rich reds and browns."),
    ("Jupiter.", "Medieval scholars in robes all pointing dramatically up at a giant glowing planet Jupiter in the night sky, totally sure of themselves."),
    ("And Saturn. And Mars. Basically, the sky.", "Medieval scholars pointing in every direction at a night sky crowded with planets (Saturn with rings, red Mars), Red as a peasant standing among them, deeply confused."),
    ("Welcome to England, 1348.", "Wide establishing shot of a small medieval English village with thatched cottages, a stone church and green fields, Red as a peasant standing in front, small in the frame. Earthy browns and muted greens."),
    ("Today we're finding out exactly why you wouldn't survive the Black Death.", "Red as a medieval peasant gulping nervously, looking straight at the viewer, while dark storm clouds gather over the village behind him."),
    ("And see that little meter in the corner? Those are your odds of making it to the end of this video.", "Red as a medieval peasant pointing up toward the top-right corner of the frame with a curious face, leaving the top-right corner empty."),
    ("Spoiler: they're going down.", "Red as a medieval peasant with a forced, sweaty, nervous grin, giving a shaky thumbs up."),
    ("But stick around until the end, because the few people who did survive got something nobody in your village could have imagined.", "Red as a medieval peasant on a hilltop at golden sunrise, holding up a shiny gold coin that sparkles, hopeful expression."),
    # 1. Un año antes
    ("But let's rewind a year. It's the spring of 1347.", "A cheerful medieval English village in spring: blossoming trees, lambs, sunshine, peasants working the fields. Fresh greens and soft yellows."),
    ("You're a peasant in a small village in the south of England, and honestly? Life is fine.", "Red as a medieval peasant in a rough brown wool tunic standing in a muddy village lane, giving the viewer an awkward nervous smile and a small shrug."),
    ("Terrible, but fine.", "Red as a medieval peasant sitting in a mud puddle in the rain, soaked, still giving a calm thumbs up."),
    ("You own almost nothing.", "Red as a medieval peasant turning out his empty pockets, small in the foreground, while a huge stone castle towers on a distant hill. Overcast sky."),
    ("You owe your lord a couple of days of work in his fields every week, before you're allowed to touch your own.", "Red as an exhausted medieval peasant pushing a heavy wooden plow through the lord's large field, while his own tiny plot sits overgrown with weeds in the background."),
    ("And dinner is bread. With a little pottage, if things are going well.", "Red as a medieval peasant at a rough wooden table in a dark smoky hut, staring unimpressed at a loaf of dark bread and a small bowl of thin pottage. Warm dim firelight."),
    ("Then the merchants at the market start talking about a sickness in the East.", "A busy medieval market: two merchants whispering behind their hands with worried faces, Red as a peasant leaning in to eavesdrop."),
    ("By October 1347, it's in Sicily, arriving on ships at Messina.", "Medieval wooden trading galleys arriving in a sunny Mediterranean harbor town in Sicily, an ominous dark cloud following the ships. No people visible up close."),
    ("Within months, it's in Italy. Then France. Then everywhere ships can go.", "An old parchment-style map of Europe and the Mediterranean with a dark creeping shadow spreading along the sea routes and coasts. No labels, no text."),
    ("And you do what everyone does. You assume it's somebody else's problem.", "Red as a medieval peasant in a cozy village tavern, holding a wooden mug of ale, shrugging carelessly."),
    ("England is an island. God is clearly on your side. And Sicily is very, very far away.", "Red as a medieval peasant lying relaxed on a grassy English cliff top, hands behind his head, looking out over a calm sea, totally carefree."),
    ("It is not that far away.", "Red as a medieval peasant smiling innocently at the viewer while an enormous dark shadow with glowing eyes looms right behind him. Dramatic contrast, deep reds and black."),
    # 2. Llega
    ("In June 1348, according to a chronicle written by friars in King's Lynn,", "A medieval friar in a grey habit writing a chronicle with a quill in a big book by candlelight, in a stone friary."),
    ("two ships land at Melcombe, in Dorset.", "Two small medieval cargo ships (cogs) sailing into a small English harbor town on a bright summer day, gulls overhead."),
    ("On one of them is a sailor from Gascony, in France, and he's already sick.", "A pale, sweaty, coughing medieval sailor stepping off a ship onto a wooden dock, while Red as a peasant on the dock waves at him cheerfully, unaware."),
    ("The chronicle blames him. Historians aren't so sure it was that simple.", "Three modern historians with glasses and stacks of books squinting skeptically at an old chronicle, one raising an eyebrow."),
    ("Bristol and Southampton also have a claim to being first. Nobody wins this competition.", "Three medieval town criers from three different port towns each raising a hand eagerly to be first, while Red as a peasant facepalms."),
    ("From the coast, the plague moves the way everything moves in medieval England: along roads, rivers and markets.", "A dark shadow creeping along a winding dirt road and a river through the English countryside, past carts and travelers who don't notice it."),
    ("Bristol by the summer. London by the autumn.", "Medieval London in autumn seen from across the Thames: old London Bridge with houses on it, the tall spire of old St Paul's, gloomy orange sky."),
    ("Over the next year, it reaches almost every corner of the country. Including your village.", "Red as a medieval peasant in his village looking up in alarm as a huge dark cloud rolls over the hill toward the cottages."),
    ("And just like that, about half the people around you are not going to make it.", "Red as a medieval peasant standing in a crowd of villagers, half of whom have turned pale grey and faded like ghosts, Red looking around in shock.", "50"),
    ("We haven't even gotten to the bad part.", "Close-up of Red as a medieval peasant staring at the viewer with deadpan horror, one eye twitching."),
    ("Now, you've probably heard that rats spread it. That's partly true.", "A fat cartoon rat sitting on a barrel in a medieval street, Red as a peasant stepping back warily."),
    ("The disease is caused by a bacterium called Yersinia pestis, and it's carried by fleas. Fleas live on rats.", "A giant wingless cartoon flea (six legs, no wings) riding a rat like a tiny knight on a horse, looking proud, Red peeking at them in disbelief. Funny, not gross."),
    ("But some researchers now think that in Europe, human fleas and body lice did a lot of the work, jumping from person to person in crowded, unwashed homes.", "Tiny cartoon fleas leaping happily between medieval peasants squeezed together in a cramped hut, little motion lines showing the jumps. Funny, not gross."),
    ("And your home is very crowded. And very unwashed.", "Red's large peasant family crammed shoulder to shoulder in a tiny dirty one-room hut, everyone grimy, Red squeezed in the middle."),
    ("You share one room with your whole family. Possibly also with the animals.", "Inside a one-room medieval hut: Red's family sleeping on straw next to a cow, a pig and chickens, the cow's head right next to Red's face."),
    # 3. Síntomas
    ("So, let's say a flea finds you. Here's what happens next.", "Close-up of a tiny cartoon flea landing on Red's arm, Red looking the other way, unaware."),
    ("First, fever. A headache. Chills.", "Red as a medieval peasant in bed with a wet cloth on his forehead, shivering under a thin blanket, sweat drops."),
    ("Then a painful swelling appears in your groin, your armpit or your neck.", "Red as a medieval peasant in bed clutching his neck and armpit with a pained face. Nothing graphic, no visible wounds."),
    ("It's called a bubo, and that's where the name \"bubonic\" comes from.", "Red dressed as a medieval teacher pointing with a stick at a simple diagram of a stick figure with red circles marking the neck, armpit and groin. No words."),
    ("That's the bubonic version, and believe it or not, it's the \"good\" one.", "Red as a sick medieval peasant in bed giving a weak, wobbly thumbs up with a tired smile."),
    ("Even today, the World Health Organization estimates that untreated bubonic plague kills between 30 and 60 percent of the people who catch it.", "A modern doctor in a white coat holding a clipboard next to a big pie chart that is about half red, Red as a medieval peasant looking at it nervously."),
    ("So it's basically a coin flip.", "Red as a medieval peasant watching a giant gold coin spin in the air above him, eyes following it, sweating.", "50"),
    ("There's a worse version. If the infection reaches your lungs, it becomes pneumonic plague.", "Cartoon cross-section of Red's chest showing two lungs glowing an alarming red, Red looking down at his own chest in horror."),
    ("Now it spreads through coughing, person to person, no flea required.", "Red as a medieval peasant coughing into his elbow while villagers around him jump back in alarm."),
    ("Untreated, it's almost always fatal, sometimes within a day.", "Red as a medieval peasant in bed next to a large hourglass whose sand is running out very fast, Red staring at it in panic.", "1"),
    ("And in 1348, nothing is treated. Because nobody knows what's happening.", "A group of medieval villagers all scratching their heads with big question marks floating above them, Red in the middle looking at the viewer."),
    # 4. Médicos
    ("Let's talk about your doctors.", "A wealthy medieval physician in a fine red robe and round hat, holding a glass flask up to the light, looking important."),
    ("Well, you're a peasant. You don't have a doctor.", "Red as a medieval peasant behind a wooden fence watching the rich physician walk into a big manor house, the gate closing."),
    ("But the people who do aren't doing much better.", "A rich medieval noble sick in a canopy bed while the physician beside him scratches his head, completely puzzled."),
    ("In 1348, the King of France asked the top medical experts at the University of Paris to explain the plague.", "A 14th-century French king on a throne with blue and gold fleur-de-lis drapes, addressing a row of nervous scholars in robes."),
    ("Their official answer? The planets.", "Medieval Paris scholars proudly presenting an astrological chart with planets and circles to the king. No words."),
    ("Specifically, a conjunction of Saturn, Jupiter and Mars on the 20th of March, 1345, which supposedly corrupted the air.", "Saturn, Jupiter and Mars lined up in a dark night sky while a sickly green mist drifts down onto a medieval city below."),
    ("That idea, poisoned air, or \"miasma\", was the best science of the time.", "Red as a medieval peasant pinching his nose inside a swirling cloud of green 'bad air'."),
    ("So the cures actually make sense, in a terrible way.", "Red as a medieval peasant with a thoughtful hand on his chin, then a slow reluctant nod, a little lightbulb above his head."),
    ("Carry flowers or herbs, so you're breathing something nicer.", "Red as a medieval peasant with a big bunch of flowers and herbs stuffed against his nose, walking around very seriously."),
    ("Splash vinegar around.", "Red as a medieval peasant splashing vinegar from a clay jug all over his hut, droplets flying, very committed."),
    ("Burn something that smells strong.", "Red as a medieval peasant waving smoke from a smoking pot of burning herbs, coughing, eyes watering."),
    ("Don't bathe too much.", "Red as a medieval peasant looking suspiciously at a wooden bathtub as if it were dangerous, backing away."),
    ("The Paris experts listed bathing right next to too much exercise and too much sex, as things that made your body more vulnerable.", "A stern medieval scholar in robes wagging his finger at three things: a wooden bathtub, a man running, and a closed curtained bed. Family friendly."),
    ("Honestly, for a medieval peasant, that one wasn't hard to follow.", "Red as a very dirty medieval peasant, covered in mud with a couple of cartoon flies around his head, smiling proudly."),
    ("And of course, bloodletting, which was the medieval answer to almost everything.", "A medieval barber-surgeon holding a small metal bowl next to Red's outstretched arm, Red looking away nervously. Nothing graphic, no blood visible."),
    ("Feeling weak and feverish? Let's remove some of your blood.", "Red as a medieval peasant, very pale and dizzy with swirly eyes, while the barber-surgeon smiles cheerfully.", "-10"),
    ("Even the Pope, Clement the Sixth, in Avignon, was advised by his physician to keep fires burning to purify the air.", "A 14th-century pope in white robes and papal tiara sitting on a throne between two large roaring fires in a stone palace hall, sweating heavily."),
    ("And to be fair, he survived. Maybe the fire helped. Maybe he was just lucky.", "The pope fanning himself with a hand, shrugging with a relieved but uncertain smile."),
    ("Oh, and that creepy bird mask you're imagining? The plague doctor with the long beak?", "A classic plague doctor in a long black coat, wide-brimmed hat and long white beaked mask standing in a dark alley, creepy."),
    ("Not here. That costume shows up in the 1600s, about three hundred years later.", "Red as a medieval peasant holding up a hand to stop the beak-masked plague doctor, who looks embarrassed, a big red X over the doctor."),
    ("In 1348, the person treating you looks like... a guy. Probably a very nervous guy.", "An ordinary medieval man in a plain brown tunic holding a few herbs, sweating and very nervous, standing at Red's bedside."),
    # 5. Todo se cae
    ("We're about halfway through, and your odds are not looking great.", "Red as a medieval peasant looking at a half-empty hourglass, worried."),
    ("But remember: if you make it to the end, things get weirdly good.", "Red as a medieval peasant daydreaming, a thought bubble above him showing a table full of roast meat and ale."),
    ("First, though... it gets worse.", "The thought bubble popping, Red's face falling as rain pours on him."),
    ("So the doctors can't help. What about the Church?", "A small stone medieval English village church with a bell tower under a grey sky."),
    ("For you, in 1348, the Church is everything.", "Red as a medieval peasant kneeling and praying inside a candlelit stone church, colored light from a stained-glass window."),
    ("And the worst thing that can happen isn't dying. It's dying without confession.", "Red as a sick medieval peasant in bed reaching anxiously toward an empty open doorway, waiting for someone who doesn't come."),
    ("Here's the problem. Priests visit the sick.", "A kind medieval priest with a small cross and a lantern knocking at a peasant's hut door."),
    ("Priests catch the plague. Priests die.", "An empty church pulpit with a single candle that has just been blown out, a thin wisp of smoke. Somber."),
    ("So many that in January 1349, the Bishop of Bath and Wells sent an emergency message to his diocese:", "A medieval bishop in a mitre writing an urgent letter by candlelight, a wax seal ready, a messenger waiting at the door."),
    ("if no priest can be found, the dying can confess to an ordinary person.", "Red as a sick medieval peasant in bed whispering his confession to a surprised ordinary peasant neighbor sitting beside him."),
    ("And if no man is available... even to a woman.", "A medieval peasant woman sitting at Red's bedside, listening kindly, while Red looks surprised."),
    ("For the medieval Church, that was a five-alarm fire.", "A group of medieval bishops in mitres running around in panic in a cathedral, one ringing a bell."),
    ("Nobody is safe. Not even the top of society.", "Medieval nobles at a long banquet table looking nervously at each other, one dropping a goblet."),
    ("In 1348, the King's own daughter, Princess Joan, died of plague near Bordeaux, on her way to marry a Spanish prince.", "A young medieval princess with a small golden crown looking out of a royal carriage window, dark clouds gathering over the road ahead. Somber."),
    ("In 1349, the man chosen to be Archbishop of Canterbury died.", "An ornate archbishop's mitre resting on an empty carved chair in a cathedral."),
    ("Then his replacement died too, just weeks after taking the job.", "A second archbishop's mitre placed on a second empty chair beside the first, Red as a peasant staring at both in disbelief."),
    ("In London, the churchyards filled up.", "A crowded medieval London churchyard full of simple wooden crosses, seen from a distance, grey sky. Nothing graphic."),
    ("So the city opened new emergency cemeteries, with long trenches for the dead.", "A distant view of an open field outside medieval London with long dug trenches and a few workers with shovels. No bodies visible."),
    ("In 2011, scientists pulled the plague's DNA from skeletons buried at one of them, East Smithfield.", "Modern scientists in white lab coats and gloves examining an old bone with a magnifying glass in a lab, Red as a medieval peasant peeking in from behind them."),
    ("More than six hundred and fifty years later, the culprit was finally confirmed.", "A cartoon rod-shaped bacterium with a guilty face standing in a police lineup, Red as a medieval peasant pointing at it triumphantly."),
    # 5b. Opciones
    ("So, what can you actually do? Let's look at your options.", "Red as a medieval peasant standing at a crossroads with three wooden signposts pointing different ways, scratching his head. Signs blank."),
    ("Option one: run. That's what the rich did.", "Wealthy medieval nobles in a fancy horse-drawn carriage speeding away from a city, luggage piled on top."),
    ("In Florence, the writer Giovanni Boccaccio described wealthy families leaving the city for their country houses and waiting it out.", "Elegant 14th-century Florentines relaxing in the garden of a Tuscan country villa with cypress trees, telling stories, Florence's dome far away on the horizon."),
    ("Great plan. If you have a country house.", "Red as a medieval peasant giving a sarcastic thumbs up with a flat unimpressed face."),
    ("You don't. You're tied to your lord's land.", "Red as a medieval peasant holding a small travel sack, looking at the road out of the village, while the lord's stern steward watches him from the field."),
    ("Leaving without permission can get you into serious trouble.", "A stern medieval steward with a wooden staff blocking the village road, wagging a finger at Red."),
    ("And even if you did leave, where would you go? Every village is dealing with the same thing.", "Red as a medieval peasant on a hilltop looking out over several distant villages, each one under its own dark cloud."),
    ("And the plague is usually already there, waiting for you.", "A dark shadowy figure leaning casually against the gate of the next village, waving at Red as he arrives."),
    ("Option two: pray harder.", "Red as a medieval peasant praying extremely hard, eyes squeezed shut, hands clasped, sweat drops."),
    ("Across Europe, groups called flagellants marched from town to town, whipping themselves in public to beg God for mercy.", "A long procession of barefoot medieval penitents in plain brown and grey tunics, heads uncovered (no hoods, no pointed hats), walking in a line through a town behind a large wooden cross, seen from a distance, holding knotted cords. Nothing graphic."),
    ("In 1349, a group of them crossed over from Holland and Zeeland and put on a show in London.", "The same procession of barefoot penitents in plain brown tunics, heads uncovered (no hoods, no pointed hats), walking behind a wooden cross down a medieval London street near old St Paul's, seen from a distance."),
    ("The Londoners watched. Mostly, they did not join in. Very English.", "A row of medieval Londoners watching the procession with crossed arms and raised eyebrows, deeply unimpressed, Red among them."),
    ("Option three, and this is the dark one: blame someone.", "A single candle burning in the dark beside an old torn parchment. Serious, somber mood, muted colors."),
    ("In many parts of Europe, terrified people blamed Jewish communities for poisoning the wells, and thousands of innocent people were murdered.", "A lonely medieval stone well in an empty town square at dusk, a few wilted flowers and a candle placed on its edge. Somber, respectful, no people."),
    ("In England, there were no Jewish communities left to blame. They had been expelled in 1290.", "An empty, quiet street in a medieval English town at dusk, closed shutters, long shadows. Somber, no people."),
    ("It's one of the most shameful chapters of the whole pandemic, and a reminder that fear can be as deadly as any disease.", "Red as a medieval peasant standing alone in the dark holding a small candle, sad and thoughtful."),
    ("So: you can't run, praying doesn't seem to work, and blaming people is horrifying.", "Red as a medieval peasant sitting on the floor hugging his knees, looking defeated."),
    ("Which leaves you with option four. Wait. And hope.", "Red as a medieval peasant sitting on his doorstep at dusk, waiting, a small candle at his feet, a tiny hopeful smile."),
    ("Be honest: which one would you have picked? Tell me in the comments.", "Red as a medieval peasant pointing straight at the viewer with a playful, curious expression."),
    # 6. Cifras
    ("So, how bad was it really? Historians still argue about the exact numbers.", "Two modern historians arguing across a table piled with books, pointing at each other, Red watching from the side."),
    ("Medieval record-keeping wasn't great, and it's hard to count when the people counting are also dying.", "A confused medieval scribe counting on his fingers with a long scroll, sneezing, ink splattered."),
    ("But most estimates for England land somewhere between 40 and 60 percent of the population, dead, in about two years.", "A simple parchment-style map of England where about half of the little villages have turned grey and faded. No labels, no text."),
    ("Across Europe, estimates range from about a third to more than half.", "A simple parchment-style map of Europe with large areas turned grey. No labels, no text."),
    ("And it's not just people. A chronicler in Leicester, Henry Knighton, wrote that sheep and cattle wandered loose through the fields and the crops, because there was no one left to drive them.", "Sheep and cows wandering loose through an unharvested wheat field with nobody around, an abandoned shepherd's crook on the ground."),
    ("Harvests rotted in the ground. There simply weren't enough hands.", "A drooping, rotting wheat field under a grey sky with a lone scythe stuck in the ground."),
    ("Picture your village. A hundred people.", "Red's medieval village seen from above, crowded with many little villagers going about their day."),
    ("The miller. The blacksmith. Your neighbors.", "A cheerful miller with a flour sack and a burly blacksmith with a hammer waving at Red as a peasant."),
    ("The annoying guy who always borrows your plow without asking.", "A sneaky medieval villager tiptoeing away with Red's wooden plow while Red glares at him with crossed arms."),
    ("By 1350, around half of them are gone.", "Red's village seen from above with half of the little villagers faded to grey and the lanes much emptier."),
    ("Statistically... so are you.", "Red as a medieval peasant looking down at his own hands, which are fading and semi-transparent, with a resigned shrug.", "≈50"),
    # 7. Giro
    ("But let's say you're lucky. Let's say you're one of the people who make it. What's your life like now?", "Red as a medieval peasant slowly standing up at sunrise, weak but alive, golden light on his face."),
    ("Weirdly... better.", "Red as a medieval peasant with a surprised face and a big question mark above his head, sunshine breaking through clouds.", "WAGES"),
    ("Think about it. Half the workers are gone. The fields still need plowing.", "Huge empty fields with an abandoned plow and nobody working, the lord's manor in the background."),
    ("Suddenly, your lord needs you more than you need him.", "A medieval lord in fine clothes on his knees begging, while Red as a peasant stands with his arms crossed and his nose up."),
    ("So peasants start asking for higher wages. And they get them.", "Red as a medieval peasant grinning as coins are dropped into his open hands by an annoyed steward."),
    ("The people in charge hate this.", "A group of medieval nobles fuming, red-faced, steam coming out of their ears."),
    ("In 1349, King Edward the Third issued the Ordinance of Labourers, and in 1351 Parliament passed the Statute of Labourers.", "A 14th-century English king with a crown and beard angrily signing a long scroll with a quill, royal red and gold."),
    ("Both tried to force wages back to what they were before the plague, and punished anyone who refused to work.", "A stern royal official reading a scroll aloud in a village square to unhappy peasants, Red rolling his eyes."),
    ("It didn't really work. Wages kept creeping up. Workers moved to wherever paid better.", "Red as a medieval peasant walking cheerfully down a road with his sack toward another village whose lord is waving him in."),
    ("And over the following generations, many ordinary people ate more meat, drank more ale and lived better than their parents ever had.", "Red as a medieval peasant at a table full of roast meat, bread and a big mug of ale, with a satisfied smile, warm golden light."),
    ("About thirty years later, in 1381, all that tension exploded into the Peasants' Revolt. But that's a story for another video.", "A crowd of medieval peasants with pitchforks and banners marching toward a city, seen from a distance."),
    ("So congratulations, again. You probably wouldn't survive the Black Death.", "Red as a medieval peasant looking at the viewer with a wry smile, raising a mug."),
    ("But if you did... you might finally get something more than bread.", "Red as a medieval peasant proudly holding up a big piece of roast meat with a huge grin."),
    # 8. Cierre
    ("Oh, and one last thing. \"Ring Around the Rosie\"? Not about the plague.", "Victorian-era children in 1880s clothes holding hands and dancing in a ring in a park, a big red stamp-like circle with a slash over the scene."),
    ("The rhyme first appeared in print in 1881, and folklorists only connected it to the plague in the twentieth century. Sorry.", "Red as a medieval peasant holding an old Victorian printed book open, giving an apologetic shrug."),
    ("If you want to know what it was like to be the person who walked into plague houses on purpose, the next video is right here.", "Red as a medieval peasant pointing to the right side of the frame, where the silhouette of a beak-masked plague doctor stands in a doorway."),
    ("And subscribe, because this little guy in the red scarf has a lot more centuries to suffer through.", "Red waving goodbye with a big smile, standing in front of three glowing doorways showing ancient Rome, a Viking longship and an Egyptian pyramid."),
]

BASE = (
    "Use the attached character sheet as the exact design reference for the main character \"Red\" "
    "(round white head, large expressive eyes, thin black stick body and limbs, bright red scarf). "
    "2D hand-drawn cartoon illustration, warm comic style, clean bold black outlines, flat colors with soft shading. "
    "{SCENE} Single clear idea, main subject large in frame. Historically plausible 14th-century details unless stated otherwise; "
    "all people drawn in the same simple round-headed stick-figure cartoon style. "
    "No text, no letters, no watermark, no border, full-bleed. 16:9."
)

scenes = []
for i, item in enumerate(S, 1):
    scene = {"id": f"{i:03d}", "text": item[0], "SCENE": item[1]}
    if len(item) > 2:
        scene["meter"] = item[2]
    scenes.append(scene)
scenes[6]["meter"] = "100"  # "Welcome to England, 1348": aparece el medidor

# Comprobación: los textos juntos deben ser exactamente la narración (sin etiquetas de voz).
narration = re.sub(r"\[(pause|sarcastic|whispers)\]\s*", "", (HERE / "narracion.txt").read_text())
assert " ".join(s["text"] for s in scenes).split() == narration.split(), "los textos no cuadran con narracion.txt"

(HERE / "escenas.json").write_text(json.dumps({
    "reference": "imagenes/red-ficha/red-oficial.png",
    "model": "seedream_5_0_flash",
    "params": ["--aspect-ratio", "16:9", "--resolution", "2k"],
    "base": BASE,
    "scenes": scenes,
}, indent=1, ensure_ascii=False) + "\n")
print(f"ok  {len(scenes)} escenas")
