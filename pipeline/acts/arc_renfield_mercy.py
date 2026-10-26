"""PERSONAL ARC - "The Fly-Eater's Mercy" (R. M. Renfield, the asylum at Purfleet, from the inside).
Playable: renfield.  All ids prefixed renfield_mercy_."""
from dsl import *

R = "renfield_mercy_"


def N(speaker, text, **kw):
    return dict(speaker=speaker, text=text, **kw)


def C(text, next=None, **kw):
    d = dict(text=text)
    if next:
        d["next"] = next
    d.update(kw)
    return d


def D(start, **nodes):
    return dict(start=start, nodes=nodes)


def say(t):
    return {"say": t}


def J(title, text, source="R. M. Renfield's notebook"):
    return dict(title=title, source=source, text=text)


def P(s, *a, **k):
    return prop(R + s, *a, **k)


def NP(s, *a, **k):
    return npc(R + s, *a, **k)


REN = "R. M. Renfield"
ME = "Renfield"

ARC = dict(
    id="renfield_mercy", title="The Fly-Eater's Mercy", member="renfield", portrait="renfield",
    blurb="Purfleet, the padded cell and the ledger of lives. A man of sharp mind and old family is promised lives by a voice in the dark. When the night comes, he must choose between the Master and the small mercies he owes the sparrow in his hand.",
    unlock="flag:a5_renfield_revived", unlock_text="Show Renfield mercy in his last hour (Act V).", after_credits=False,
    start=dict(location=R + "cell", protagonist="renfield", party=["renfield"], items={}, flags=[]),
    exit_to="ARC_END",
    rewards=[dict(give=R + "keepsake"), dict(give="brandy"), dict(give=R + "sugar"), dict(stat=dict(member="seward", nerve=3)),
             dict(set="renfield_mercy_done")],
    rewards_text="Renfield's notebook of lives, a bottle of brandy and a lump of sugar; +3 Nerve for Dr. Seward, Renfield's last gift.",
)

LOCATIONS = [
    dict(id=R + "cell", name="Room 12, Purfleet", date="A morning in late summer",
         desc="Padded in grey ticking where the plaster has been mended. A barred window, a cot, a tin tray. Home, of a kind."),
    dict(id=R + "ward", name="The day-room, Purfleet", date="The same morning",
         desc="Seven iron beds, three barred windows, nine lamps and a clock that is wrong in the hour. Everything here is counted by somebody."),
    dict(id=R + "study", name="Dr. Seward's study", date="Mid-morning",
         desc="Carbolic, cigar smoke and a phonograph under a cloth. Somewhere in these case-books I am a column of figures."),
    dict(id=R + "scullery", name="The scullery", date="Afternoon",
         desc="A black range, a stone sink and the good smell of a kitchen that has no idea what is kept upstairs."),
    dict(id=R + "garden", name="The asylum garden, by night", date="The night after",
         desc="Wet gravel under a thin moon, the high old wall and a water-butt. Beyond the wall, the dark mass of Carfax."),
    dict(id=R + "chapel", name="The chapel at Carfax", date="Past midnight",
         desc="Cold stone, a broken window and the smell of old earth. Someone has been bringing boxes into a holy place."),
]

LOC_DATA = {}

# ---------------------------------------------------------------------------------------------------------------- cell
LOC_DATA[R + "cell"] = dict(
    cells=[2, 2], interior=True, wall="plaster_dirty", floor="planks", ambient=AMBIENT["candle_interior"], camera=cam([2, 2]),
    lights=lights_warm([2, 2]),
    walls=dict(north=["wall_4", "wall_window_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[0, 1.5], spawns={R + "ward": [2.8, 2.0]},
    props=[
        P("bed", "bed_simple", "blue", -2.4, -2.6, name="The cot", radius=1.0, talk=R + "cell_bed",
          look="A narrow cot with a grey blanket folded square. A man who knows where he stands folds his blanket."),
        P("table", "table", "pale", 0.2, -2.8, name="Small table", radius=0.8, look="A deal table, scrubbed. The only thing in the room I am allowed to arrange."),
        P("tray", "chest", "pale", 0.2, -2.8, y=0.8, scale=0.3, name="Breakfast tray", radius=0.3,
          look="Bread, a tin cup and a smear of margarine. The attendants count the spoons; one is always missing, and they always blame me."),
        P("bucket", "barrel", "dark", 2.9, 0.4, scale=0.5, name="Slop bucket", radius=0.4, look="Enamel, chipped. It smells of the thing it is for."),
        P("stool", "chair", "black", -1.0, 0.4, rot=90, name="Stool", radius=0.4, look="A three-legged stool, bolted to nothing but to my patience."),
        P("board", "bench", "dark", -2.6, 1.6, rot=90, scale=0.5, name="Loose floorboard", radius=0.5,
          look="One board by the cot-leg sounds hollow under the heel. It wants something thin and strong to lever it.",
          use_item={R + "spoon": [{"take": R + "spoon"}, {"give": R + "ledger"}, {"set": R + "board_open"}, {"journal": R + "j_ledger"},
                                  say("The spoon-handle bites under the board. Beneath it, wrapped in a handkerchief with a crest I have not shown anyone in thirty years, lies my notebook of lives.")]},
          use_fail="That will not lift a board. Something thin, with a lever's patience."),
        P("jar", "bottle", "glass", 3.1, -2.4, scale=0.7, name="Jam jar", radius=0.3,
          look="A clean jam jar on the shelf by the window. Hodge lets me keep it for my 'pets'.",
          take=R + "jar", take_text="I take the jar. An empty jar is an invitation.", give_once=True),
        P("sill", "chest", "pale", 2.0, -3.4, scale=0.5, name="Window sill", radius=0.5, cond="!" + R + "flies_gathered",
          look="A bare stone sill. A few flies bump against the glass, but nothing holds them. They will not stay for nothing.",
          use_item={R + "sugar": [{"take": R + "sugar"}, {"set": R + "flies_gathered"}, {"journal": R + "j_flies"},
                                  say("I set the sugar on the sill, a white crumb on grey stone. Within a minute the flies are there, small and humming and entirely mine.")]},
          use_fail="That is not what a fly wants."),
        P("sill2", "chest", "pale", 2.0, -3.4, scale=0.5, name="Window sill, with flies", radius=0.5, cond=R + "flies_gathered",
          look="A dozen flies feed on the sugar, which is all that is happening, whatever the ledger says.",
          use_item={R + "jar": [{"take": R + "jar"}, {"give": R + "flies_jar"}, say("I drop the jar over the sugar, slide my palm beneath, and lift. A small furious life in glass. Eleven, by my count. The ledger will hold it.")],
                    R + "ledger": [say("Eleven flies, eleven lives. 'Each one a tithe,' I write, and the pen goes through the paper. Dr. Seward would say it is a dozen flies on a lump of sugar. Perhaps it is both.")]},
          use_fail="Nothing to do with that."),
        P("chalk", "gravestone", "plaster", -3.5, -0.6, rot=90, scale=0.4, name="Chalk marks", radius=0.4,
          look="Tallies scratched low on the padding, in groups of five. Mine. I do not remember whether they count days or lives."),
        P("rug", "rug", "cream", 0.0, 0.8, radius=0.1),
        P("candle", "candle", "white", -1.8, -3.0, y=0.0, scale=0.7, name="Candle stub", radius=0.2, look="Issued, counted and collected. I light it at dusk and give back the stub at dawn."),
        P("sconce", "sconce", "default", -3.7, 0.2, y=1.5, rot=90, radius=0.1),
        P("door", "door", "dark", 3.8, 2.0, rot=-90, name="Door of Room 12", radius=0.6, go=R + "ward",
          look="Heavy, with a grating. On the other side it has a lock; on this side it has me.",
          go_cond=R + "let_out", go_fail="Locked. Mr. Hodge has not yet decided what sort of man I am today."),
    ],
    npcs=[
        NP("hodge_c", "human_peasant_m", "villager", 1.0, 2.6, rot=180, name="Attendant Hodge", cond="!" + R + "let_out",
           look="A big, tired, kind man in a white coat, with the keys on his belt. He has been bitten twice and bears no grudge.", talk=R + "hodge_morning"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=R + "j_wake"),
                                  say("Morning at Purfleet. Tray, cup, a grey light on the padding. I am Renfield, R. M., once of a good house and a better profession; and I am in a cell with a ledger I cannot reach. First Hodge. I shall have to be a gentleman.")])],
)

# ---------------------------------------------------------------------------------------------------------------- ward
LOC_DATA[R + "ward"] = dict(
    cells=[3, 2], interior=True, wall="plaster", floor="planks", ambient=AMBIENT["warm_day_interior"], camera=cam([3, 2]),
    lights=lights_warm([3, 2], energy=2.4),
    walls=dict(north=["wall_4", "wall_door_4", "wall_4"], west=["wall_door_4", "wall_4"], east=["wall_door_4", "wall_door_4"]),
    spawn=[-4.0, 0.0], spawns={R + "cell": [-4.4, -1.0], R + "study": [0, -2.4], R + "scullery": [4.4, -1.0], R + "garden": [4.4, 1.0]},
    props=[
        P("bed1", "bed_simple", "blue", -3.6, 2.8, rot=180, name="Iron bed", radius=0.8, look="Narrow, made square. Whoever sleeps here has stopped expecting to be moved."),
        P("bed2", "bed_simple", "blue", -0.4, 2.8, rot=180, name="Iron bed", radius=0.8, look="A bed under the window. The pillow is damp from some weeping nobody mentioned."),
        P("table", "table_long", "dark", 1.8, 0.6, name="Day-room table", radius=1.4, look="A scarred table where the patients play dominoes and nobody keeps the score."),
        P("lantern", "lantern", "default", 1.8, 0.6, y=0.8, name="Ward lamp", radius=0.2, look="Turned low. One of nine lamps; I have counted them."),
        P("board", "bookshelf", "dark", -4.0, -3.4, name="Inventory board", radius=0.8, talk=R + "board",
          look="A board of the ward's inventory in Dr. Seward's neat hand, kept under glass against the patients' fingers."),
        P("cupboard", "chest", "ebony", -5.2, 2.2, rot=90, name="Locked linen-press", radius=0.6, talk=R + "cupboard",
          look="A tall press with a brass dial of three wheels. Dr. Seward keeps the patients' sugar ration in it, so they cannot hoard it."),
        P("clock", "column", "plaster_dirty", 4.6, -3.2, scale=0.9, name="Ward clock", radius=0.5,
          look="Ten past three, always, for the one day it was right. The nurses wind it on Sundays and it forgets by Monday."),
        P("bench", "bench", "oak", -2.0, -2.8, name="Window bench", radius=0.8, look="Where the patients sit to watch weather they are not allowed in."),
        P("coat", "bench", "ebony", 3.6, 2.6, rot=180, scale=0.5, name="Dark coat on a peg", radius=0.5,
          look="An attendant's greatcoat on a peg. In the half-dark it has the shape of a tall man waiting.",
          use_item={R + "ledger": [say("The coat is a tall man, patient and pale-eyed, who has come to ask after his debtors. I look again. It is Hodge's greatcoat, and it smells of pipe-smoke and wet dog. Both of these are true, and I do not know which is the lie.")]},
          use_fail="It will not take that."),
        P("rug", "rug", "red", 0.4, -1.2, radius=0.1),
        P("sconce", "sconce", "default", 0.0, -3.7, y=1.5, radius=0.1),
        P("d_cell", "door", "dark", -5.8, -2.0, rot=90, name="Door to Room 12", radius=0.6, look="My room, with its door open and its tray untouched.", go=R + "cell"),
        P("d_study", "door", "ebony", 0.0, -3.8, name="Dr. Seward's study", radius=0.6, look="The doctor's door. Brass plate, black letters. It is open when I have been good.",
          go=R + "study", go_cond=R + "let_out"),
        P("d_scul", "door", "oak", 5.8, -2.0, rot=-90, name="Scullery door", radius=0.6, look="To the scullery and the kitchen. The warm smell leaks under the door.", go=R + "scullery"),
        P("d_garden", "door", "dark", 5.8, 2.0, rot=-90, name="Garden door", radius=0.6,
          look="Iron-bound, and kept locked at dusk. Beyond it, the wall, the water-butt, and Carfax.",
          go=R + "garden", go_cond=R + "night&" + R + "hodge_asleep",
          go_fail="Locked. Hodge has the key somewhere about him, and he is awake and watching the door."),
    ],
    npcs=[
        NP("hodge_w", "human_peasant_m", "villager", 2.8, 2.6, rot=180, name="Attendant Hodge", cond="!" + R + "night&" + R + "let_out",
           look="Hodge, leaning against the wall, with his keys and his thoughts. He has the look of a man who is owed a pipe.", talk=R + "hodge_day"),
        NP("quill", "human_peasant_m", "villager", -2.6, 0.6, rot=90, name="Mr. Quill", cond="!" + R + "night",
           look="A small, grey, precise gentleman, counting under his breath. He was a clerk in the Customs and has not stopped.", talk=R + "quill"),
        NP("ashby", "human_seward", "doctor", -3.8, -1.4, rot=0, name="Mr. Ashby", cond="!" + R + "night",
           look="A tall old gentleman with a rug over his knees, sitting very straight. He wears a collar nobody has ever seen him fasten.", talk=R + "ashby"),
        NP("hodge_n", "human_peasant_m", "villager", 3.8, 0.4, rot=-90, name="Night-attendant Hodge", cond=R + "night&!" + R + "hodge_asleep",
           look="Hodge on the night watch, a lamp at his elbow and his eyelids at half-mast.", talk=R + "hodge_night"),
        NP("hodge_s", "human_peasant_m", "villager", 3.8, 0.4, rot=-90, name="Hodge, asleep", cond=R + "hodge_asleep",
           look="Hodge, snoring in the big chair with his chin on his chest. The brandy has done what it was asked."),
    ],
)

# ---------------------------------------------------------------------------------------------------------------- study
LOC_DATA[R + "study"] = dict(
    cells=[2, 2], interior=True, wall="plaster_dirty", floor="planks", ambient=AMBIENT["candle_interior"], camera=cam([2, 2]),
    lights=lights_warm([2, 2]),
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[2.4, 1.2], spawns={R + "ward": [2.8, 2.0]},
    props=[
        P("desk", "table", "ebony", -1.0, -2.6, name="Dr. Seward's desk", radius=0.9, talk=R + "notes",
          look="A desk of case-notes, ink and cigar ash. Somewhere in there is a page headed 'R. M. R., aet. 59'."),
        P("shelf", "bookshelf", "ebony", 2.0, -3.4, name="Medical shelves", radius=0.8,
          look="Maudsley, Esquirol, Pinel, and a volume of Carpenter that has been read to pieces."),
        P("fire", "fireplace", "stone_dark", -3.4, 1.4, rot=90, name="Fireplace", radius=0.9,
          look="Banked low. The mantel holds a stopped clock, a pipe, and a photograph of a young woman I am too polite to name."),
        P("armchair", "chair", "green", -0.2, 0.4, rot=0, name="Patient's chair", radius=0.4, look="The chair in which a great many troubled people have explained themselves. It is worn at the front."),
        P("decanter", "bottle", "amber", -0.4, -2.6, y=0.8, scale=0.8, name="Brandy decanter", radius=0.2, look="Two fingers gone. Brandy is not a cure; it is a postponement."),
        P("bust", "bust", "plaster", 3.2, -2.0, rot=-90, scale=0.7, name="Plaster bust", radius=0.5, look="Some Greek, with a pencil-moustache added by an earlier patient. Seward leaves it."),
        P("phono", "chest", "dark", -2.2, -2.6, y=0.8, scale=0.3, name="Phonograph", radius=0.4, look="Under its cloth, a wax cylinder half full of someone's confessions. Doctors are the priests of this century."),
        P("rug", "rug", "blue", 0.0, 1.2, radius=0.1),
        P("candle", "candelabra", "default", -1.0, -2.6, y=0.8, name="Candelabra", radius=0.2, look="Three candles, burnt to the same stub. He sits up under them most nights."),
        P("sconce", "sconce", "default", -3.7, -0.8, y=1.5, rot=90, radius=0.1),
        P("door", "door", "ebony", 3.8, 2.0, rot=-90, name="Door to the day-room", radius=0.6, look="Back to the ward.", go=R + "ward"),
    ],
    npcs=[
        NP("seward", "human_seward", "doctor", 0.8, -1.0, rot=180, name="Dr. Seward",
           look="A grave young man in his thirties with the eyes of a man who has stopped sleeping and kept working. He is the only person in the house who writes down what I say.", talk=R + "seward"),
    ],
)

# ---------------------------------------------------------------------------------------------------------------- scullery
LOC_DATA[R + "scullery"] = dict(
    cells=[2, 2], interior=True, wall="plaster", floor="cobble", ambient=AMBIENT["warm_day_interior"], camera=cam([2, 2]),
    lights=lights_warm([2, 2], energy=2.2),
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_4", "wall_door_4"], east=["wall_4", "wall_4"]),
    spawn=[-2.8, 1.8], spawns={R + "ward": [-2.8, 2.0]},
    props=[
        P("range", "fireplace", "stone_dark", 2.0, -3.3, name="The black range", radius=1.0, look="A great black kitchen range, polished with a patience that deserves a better employer."),
        P("table", "table_long", "pale", 0.4, 0.0, scale=0.8, name="Kitchen table", radius=1.4, look="Flour, a rolling-pin and a half-plucked fowl. It is a scene of moderate and orderly slaughter."),
        P("barrel1", "barrel", "oak", 3.3, 1.0, name="Flour barrel", radius=0.5, look="Dusty to the rim. Mice have been at it, and Cook has been at the mice."),
        P("barrel2", "barrel", "dark", 3.0, 2.2, name="Water barrel", radius=0.5, look="Rain-water for washing the greens."),
        P("sack", "chest", "pale", 1.2, -3.3, scale=0.7, name="Sack of meal", radius=0.5, look="Oatmeal, coarse and damp at the bottom."),
        P("shelf", "bookshelf", "pale", -0.6, -3.4, name="Dresser", radius=0.8, look="Blue plates, copper pans and, behind them all, a bottle Cook says is for the gravy."),
        P("web", "deadtree", "grey", -3.0, -2.8, scale=0.4, name="Cobweb behind the range-end", radius=0.5,
          look="A wide old web in the corner behind the plate-rack, thick with dust and with something small and metal caught in it. The spider is large, fat in the way of a spider who has been fed by nobody.",
          use_item={R + "flies_jar": [{"take": R + "flies_jar"}, {"give": R + "garden_key"}, {"set": R + "spider_fed"}, {"journal": R + "j_key"},
                                      say("I tip the flies into the web. The old spider drops down, takes them one by one, and in the stir the thing in the web comes loose: an iron key, lost long ago behind the plate-rack, on a loop of tape marked 'GARDEN'. Hodge dropped it, Dr. Seward would say. The spider kept it, I would say. I am not troubled by the difference, only by the key.")],
                    R + "ledger": [say("A spider is a clerk who keeps accounts in silk. Every fly a line. This one has a very handsome set of books.")]},
          use_fail="The spider is not interested in that."),
        P("cat", "wolf", "grey", -1.6, 1.2, scale=0.28, name="Kitchen cat", radius=0.4,
          look="A fat tabby asleep in the warm. In my ledger he is the last account in the chain: sugar, flies, spiders, sparrows and the cat.",
          use_item={R + "ledger": [say("I look at the cat and the ledger looks at me. 'The cat has eaten forty sparrows,' I write, 'and the sparrows ten thousand flies.' It does not close. Nothing in this ledger closes.")]},
          use_fail="The cat declines."),
        P("lantern", "lantern", "default", 0.4, 0.0, y=0.8, scale=0.8, name="Scullery lamp", radius=0.2, look="A tin lamp, always lit. Cook says the dark in a kitchen breeds beetles."),
        P("rug", "rug", "cream", -1.4, -0.4, radius=0.1),
        P("door", "door", "oak", -3.8, 2.0, rot=90, name="Door to the day-room", radius=0.6, look="Back to the ward.", go=R + "ward"),
    ],
    npcs=[
        NP("cook", "human_peasant_f", "village_woman", 1.8, 1.8, rot=180, name="Mrs. Pargeter, the cook",
           look="A broad, floury woman who has raised six children and fed forty patients and has never in her life been afraid of a man.", talk=R + "cook"),
    ],
)

# ---------------------------------------------------------------------------------------------------------------- garden
LOC_DATA[R + "garden"] = dict(
    cells=[3, 3], interior=False, wall="stone_dark", floor="dirt", ambient=AMBIENT["night_exterior"], camera=cam([3, 3]), lights=lights_moon(2.6),
    moon=dict(pos=[-6, 12, -8]),
    scatter=dict(asset="pine", variant="dark", count=20, seed=17, avoid=[[-7, -7, 7, 7]]),
    spawn=[4.0, 1.0], spawns={R + "ward": [4.4, 1.6], R + "chapel": [-4.0, -3.0]},
    props=[
        P("d_ward", "door", "dark", 5.0, 2.8, rot=-90, name="Door to the ward", radius=0.6, look="The way back in, to Hodge, the cot and the tray.", go=R + "ward"),
        P("wall", "fence", "default", -2.0, -5.0, name="The high wall", radius=0.5, look="Ten feet of old brick, topped with broken glass. Beyond it, Carfax."),
        P("gate", "door_big", "dark", -4.0, -4.0, name="Wicket in the wall", radius=0.7,
          look="A little door in the old wall, rusted shut on the Carfax side. It has a keyhole on this one.",
          go=R + "chapel", go_cond="has:" + R + "garden_key&" + R + "garden_clear",
          go_fail="I cannot go through while the night-man is on his round, and not without the garden key."),
        P("butt", "barrel", "dark", -1.6, 0.4, scale=1.1, name="Water-butt", radius=0.7, talk=R + "hide", cond="!" + R + "garden_clear",
          look="A fat water-butt against the wall, deep in shadow. A man who knew his hour could kneel behind it."),
        P("bench", "bench", "dark", 2.4, -2.0, rot=90, name="Garden bench", radius=0.8, look="The bench where Dr. Seward sits with the quiet patients in the afternoon."),
        P("sparrow", "bat", "brown", 1.6, 1.0, scale=0.3, name="Sparrow in the wet grass", radius=0.4,
          look="A sparrow on the path with one wing hanging wrong. The cat will find it before morning.",
          take=R + "sparrow", take_text="I cup it in both hands. It is warm and it weighs nothing. It looks at me with a bead of eye, and I cannot read what it says.", give_once=True),
        P("shape", "gravestone", "stone_mossy", -3.4, -2.4, rot=20, scale=0.5, name="Pale shape by the wall", radius=0.5,
          look="Something pale in the lee of the wall, as tall as a man. It has not moved since I came out.",
          use_item={R + "ledger": [say("It is not a man. It is a heap of whitewashed stones the gardener left. It is also a patient Master waiting for the debt to be paid. The ledger does not choose between them; I will have to.")]},
          use_fail="It does not respond."),
        P("lamp", "lantern", "default", 3.0, -3.0, y=0.0, scale=0.9, name="Night-lamp on a hook", radius=0.3, look="The night-man hangs it here when he goes to the far wall. A lantern is a clock if you watch it."),
        P("stones", "rock", "mossy", -5.0, 3.0, name="Mossy stones", radius=0.5, look="A jumble of stones. A good place for beetles."),
        P("bush", "deadtree", "grey", 5.5, -1.0, scale=0.7, name="Dead pear tree", radius=0.5, look="A pear tree that stopped bearing the year the last Lord died. The sparrows love it."),
    ],
    npcs=[
        NP("blunt", "human_peasant_m", "innkeeper", 3.0, -1.0, rot=0, name="Mr. Blunt, night attendant", cond="!" + R + "garden_clear", fight=R + "scuffle",
           look="A thick-necked man with a lantern and a stick. Blunt has the night round, ten and two, and the temper of a man who thinks the patients are animals."),
    ],
)

# ---------------------------------------------------------------------------------------------------------------- chapel
LOC_DATA[R + "chapel"] = dict(
    cells=[2, 2], interior=True, wall="stone_dark", floor="stone_dark", ambient=AMBIENT["crypt"], camera=cam([2, 2]),
    lights=[dict(pos=[0, 2.4, -1.0], color="#ff9a40", energy=1.8, range=7), dict(pos=[0, 3, 3], color="#8aa6ff", energy=1.0, range=8)],
    walls=dict(north=["wall_4", "wall_window_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[3.0, 2.0], spawns={R + "garden": [3.0, 2.0]},
    props=[
        P("altar", "table", "dark", 0.0, -2.8, name="The altar", radius=0.9, talk=R + "voice",
          look="A stone altar stripped of its cloth. Someone has laid a ring of earth where the cross should stand. A voice lives here."),
        P("box", "coffin", "default", -2.2, -2.0, name="The great box", radius=1.0,
          look="A long box of black oak, new earth spilling over the lid. Whatever is within, it is a foreigner and it is patient.",
          use_item={R + "ledger": [{"set": R + "understood"}, {"journal": R + "j_sum"},
                                   say("I open the ledger on the lid and total the whole of it: every fly, every spider, every sparrow, the cat. Eleven, forty, three hundred, a thousand. It is a column that grows and never rises to the sum he promised. 'Lives', he says, and gives me none of them. He has not paid a penny in all the weeks I have kept his books.")]},
          use_fail="The box does not answer that."),
        P("cross", "crucifix_big", "silver", 2.0, -3.2, rot=0, name="Fallen crucifix", radius=0.5, look="A silver crucifix thrown into the corner, its arms bent. I do not touch it. Not yet."),
        P("pew1", "bench", "dark", -2.0, 1.0, rot=90, name="Broken pew", radius=0.9, look="A pew with the end split off. Boots have been up on it."),
        P("pew2", "bench", "dark", 1.0, 1.4, rot=90, name="Pew", radius=0.9, look="A pew with a small brass plate: 'The Gift of J. H.'"),
        P("column", "column", "stone_dark", 2.4, -0.6, name="Pillar", radius=0.5, look="Cold as a gravestone."),
        P("window", "gravestone", "stone_grey", 3.2, -2.4, rot=-90, scale=0.4, name="Broken window", radius=0.4, look="The glass is gone from the lancet. Through it, a sliver of moon and the free air."),
        P("candle", "candle", "red", 0.0, -2.8, y=0.8, scale=0.6, name="Guttering candle", radius=0.2, look="Whose hand lit it? There is a pool of wax and a smell like a burnt feather."),
        P("rug", "rug", "black", 0.0, 0.4, radius=0.1),
        P("stones", "rock", "dark", -3.2, 2.6, name="Fallen masonry", radius=0.5, look="A heap of plaster and dust where the north roof has begun to think about the floor."),
        P("door", "door", "dark", 3.8, 2.0, rot=-90, name="Door to the garden", radius=0.6, look="The little door through the wall.", go=R + "garden"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=R + "j_chapel"),
                                  say("Carfax. A chapel I watched from the window for three months and never entered. The air is thick and sweet as a root cellar. Something is here that is not entirely here, and my hands, for the first time in weeks, are quite steady.")])],
)

# ---------------------------------------------------------------------------------------------------------------- dialogue
DIALOGUE = {}

DIALOGUE[R + "hodge_morning"] = D("n0",
    n0=N("Hodge", "Morning, Mr. Renfield. Slept? Your tray's there. The doctor says if you're quiet this morning he'll see you in his study. Well. Are you going to be quiet?",
         choices=[
             C("I am quite myself, Mr. Hodge. A man of sense, I hope, and a gentleman. May I be let out to the day-room?", "calm", cond="!" + R + "let_out"),
             C("Let me out! Every hour you keep me here, a thousand lives go by and none of them are mine!", "frenzy", cond="!" + R + "let_out"),
             C("[Ask about the spoon]", "spoon"),
             C("[Say nothing]", end=True)]),
    calm=N("Hodge", "Ah, there you are. Well said, sir, and well said again. That's the voice they ought to put in the books. Come along, then. Mind the step; I'll leave the door off the latch. Dr. Seward'll want a word.",
           do=[{"set": R + "let_out"}, {"set": R + "calm"}, {"journal": R + "j_calm"}], end=True),
    frenzy=N("Hodge", "Now then. NOW then. That's the other voice, is it? Steady, Mr. Renfield, steady, I've got you. There, there, there. A turn in the wet sheet and you'll be fit for company. Come on. Out you come; I'm sorry for it.",
             do=[{"set": R + "let_out"}, {"set": R + "frenzy"}, {"journal": R + "j_frenzy"},
                 say("Hodge's arms are like a barrel's hoops. He holds me till the strength runs out of me, and then he opens the door as gently as though I had been a child. I hate him for it. I hate myself rather more.")],
             end=True),
    spoon=N("Hodge", "Spoon? Gone again, I'll be bound. If you ever find it, it's no business of mine, but it'd be well to look under things. And you'd never use a spoon for anything wicked, sir. You'd be the first.", next="n0"),
)

DIALOGUE[R + "hodge_day"] = D("n0",
    n0=N("Hodge", "Mr. Renfield. Keep to the day-room if you please. The doctor's in his study. And Cook'll want to see you, I fancy; she's had a soft spot since the business with the mice.",
         choices=[
             C("Where is the garden key kept?", "key", cond="!journal:" + R + "j_round"),
             C("Who is on the night round, Mr. Hodge?", "round"),
             C("[Leave him to his pipe]", end=True)]),
    key=N("Hodge", "Garden key? I lost it, sir, three weeks back. Hung it on a hook in the scullery and it was gone by dinner. Dr. Seward does not know, so you'll oblige me by not knowing either. Between ourselves, I think the mice have it.",
          do=[{"journal": R + "j_hodge_key"}], next="n0"),
    round=N("Hodge", "Blunt. Ten and two. He walks out to the far wall, stops to light his pipe under the lamp there, and walks back. Same as he's done for ten years. Not a man for surprises. If he ever turned round before the pipe was lit, I'd call a doctor.",
            do=[{"journal": R + "j_round"}], next="n0"),
)

DIALOGUE[R + "hodge_night"] = D("n0",
    n0=N("Hodge", "Ho, who's that. Mr. Renfield? Back to your bed, sir. I'm on till six and the Doctor says no wandering after dark.",
         choices=[
             C("A drop of something, Mr. Hodge, for your nerves. I could not drink it myself. You have been so kind.", "brandy", cond="has:brandy"),
             C("[Say you could not sleep]", "sleep"),
             C("[Go back]", end=True)]),
    sleep=N("Hodge", "None of us can, sir. Go on, now. Back to your room, and I'll bring you a cup of cocoa.", next="n0"),
    brandy=N("Hodge", "Well. Well, that's very handsome of you, sir. Just the one, mind. For the damp. I never saw you do a mean thing in all the time I've known you, not once, whatever they write in the book...",
             do=[{"take": "brandy"}, {"set": R + "hodge_asleep"}, {"journal": R + "j_hodge"},
                 say("He drinks, sighs, sets his chin on his chest. In five minutes he is breathing like a bellows, and the keys on his belt do not stir. I tell myself I have done him no harm. A man should be allowed to sleep.")],
             end=True),
)

DIALOGUE[R + "quill"] = D("n0",
    n0=N("Mr. Quill", "Seven, seven, seven. One, two, three. Do you know, Mr. Renfield, that in this room there are nine lamps? I counted them as a boy of ten at my mother's. They all go out at the same hour, and still I count.",
         choices=[
             C("How many beds are in this room?", "beds"),
             C("And windows?", "windows"),
             C("Why do you count?", "why"),
             C("[Leave him to his arithmetic]", end=True)]),
    beds=N("Mr. Quill", "Seven beds. Seven. You'd say eight, because of the one by the stair, but it isn't a bed. It's a bier.", next="n0"),
    windows=N("Mr. Quill", "Three, with bars, and a fourth that is only a painting of one. The doctor calls them 'inventory'. He puts them in his book in the order: beds, windows, lamps. A tidy man, the doctor.",
              do=[{"journal": R + "j_count"}], next="n0"),
    why=N("Mr. Quill", "Because if I stop, sir, I begin to think about the things that can't be counted. And those are what put me in here.", next="n0"),
)

DIALOGUE[R + "ashby"] = D("n0",
    n0=N("Mr. Ashby", "Renfield. You were once Mr. Renfield of the firm, I think. A good house. There is a crest on your handkerchief, and in my day we did not carry the crest of a bad house in our pockets.",
         choices=[
             C("I was a man of business once, Mr. Ashby. My father kept a good library.", "family"),
             C("Do you hear the voice, Mr. Ashby?", "voice"),
             C("[Bow and leave]", end=True)]),
    family=N("Mr. Ashby", "I knew it. One can tell a man of breeding by what he does with the cutlery. Whatever they say of you, you have never once been vulgar. Hold to that, Renfield. It is the only furniture we are permitted to bring in with us.", next="n0"),
    voice=N("Mr. Ashby", "The voice? My dear fellow. Everyone in this house hears a voice. Mine tells me the price of consols. Yours, I think, promises you something. Be careful what you accept from a voice that has never once been in need.", next="n0"),
)

DIALOGUE[R + "board"] = D("n0",
    n0=N(ME, "The ward inventory, under glass, in Dr. Seward's hand: 'Beds, 7. Windows (barred), 3. Lamps, 9. Clock, 1 (defective).' And below it, in a fainter pencil, 'Sugar ration: Press, key by dial. Do not tell R.'",
         choices=[
             C("[Copy the numbers into my head]", "copy"),
             C("[Leave it]", end=True)]),
    copy=N(ME, "Seven. Three. Nine. In that order, beds, windows, lamps. I never forget a figure. It is the last sane thing about me.",
           do=[{"journal": R + "j_count"}], end=True),
)

DIALOGUE[R + "cupboard"] = D("n0",
    n0=N(ME, "The linen-press, with its three brass wheels. The sugar ration is in there, and with it the whole of my little world of flies.",
         choices=[
             C("[Dial 3-7-9]", "bad"), C("[Dial 9-3-7]", "bad"), C("[Dial 7-3-9]", "good", cond="!" + R + "sugar_got"), C("[Dial 7-9-3]", "bad"),
             C("[Step away]", end=True)]),
    bad=N(ME, "The wheels turn and stop. The press does not budge. An error of arithmetic; I will not make another.", next="n0"),
    good=N(ME, "Seven. Three. Nine. The wheels click, the latch drops and there it is, on a blue paper, fine as snow: a lump of sugar. Just one. Dr. Seward counts them. I count him.",
           do=[{"give": R + "sugar"}, {"set": R + "sugar_got"}, {"journal": R + "j_sugar"}], end=True),
)

DIALOGUE[R + "notes"] = D("n0",
    n0=N(ME, "A case-book open on the blotter: 'R. M. Renfield, aet. 59. Zoophagous (life-eating) maniac. Sanguine temperament, great physical strength, morbid selfishness. Collects: flies (sugar), spiders, sparrows, a cat. Keeps accounts. Perfectly lucid on matters of family and law.'",
         choices=[
             C("[Read on]", "more"),
             C("[Close the book]", end=True)]),
    more=N(ME, "'His dread of the unseen is genuine. He does not lie. He says a Master will come for the lives, and that he has been promised a great number. I do not know what to make of a delusion so well-regulated. He is the only patient who thanks me for my notes.'",
           do=[{"journal": R + "j_notes"}], end=True),
)

DIALOGUE[R + "seward"] = D("n0",
    n0=N("Dr. Seward", "Renfield. Good morning. Sit, if you wish. I confess I did not expect to see you out and about so early. You look, if I may say, like a man who has not slept.",
         choices=[
             C("[Ask to be moved from this house]", "ask", cond="!" + R + "plea_made"),
             C("[Ask what the doctor thinks of the notes]", "notes", cond="!" + R + "plea_made"),
             C("[Thank him]", "thanks", cond=R + "plea_made"),
             C("[Withdraw]", end=True)]),
    notes=N("Dr. Seward", "My notes? I note what I see. You collect, you count, and you cannot be argued out of the account. I find it rather admirable and I do not know what to do with it.", next="n0"),
    ask=N("Dr. Seward", "Moved? Where? This is a good house, as houses go, and I have no other bed.",
          choices=[
              C("He is coming, doctor. I feel him through the wall. I beg you, send me away before he comes! [Raving]", "bad"),
              C("[Offer the ledger of lives]", "good", cond="has:" + R + "ledger&" + R + "calm"),
              C("[Offer the ledger of lives]", "wary", cond="has:" + R + "ledger&" + R + "frenzy"),
              C("[Say nothing more]", "n0")]),
    bad=N("Dr. Seward", "I see. 'He is coming.' It is a symptom, Renfield, I wish it were not; I wish you could say it to me without rolling your eyes. I will note it. Come back when you can tell me what you mean in plain figures.", next="n0"),
    good=N("Dr. Seward", "Your ledger. Good God, man. Every fly, every sparrow, in a clerk's hand. It is a perfectly rational document, and I have never read a sadder one. Very well. I shall move you to the quiet wing on Monday, and I want no more of this 'Master'. Take this note to the day-room; Hodge will see it honoured.",
           do=[{"give": R + "transfer_note"}, {"set": R + "plea_made"}, {"journal": R + "j_plea"}], next="n0"),
    wary=N("Dr. Seward", "You are the man who raised his voice at Hodge this morning, Renfield. But this ledger is the first honest thing you have shown me. Very well, Monday, the quiet wing. Hodge will keep an eye on you; you will not mind.",
           do=[{"give": R + "transfer_note"}, {"set": R + "plea_made"}, {"set": R + "seward_wary"}, {"journal": R + "j_plea"}], next="n0"),
    thanks=N("Dr. Seward", "Do not thank me yet. Monday is Monday. Try to be quiet tonight, Renfield. It is a thing I can say to you without writing it down.", next="n0"),
)

DIALOGUE[R + "cook"] = D("n0",
    n0=N("Mrs. Pargeter", "Mr. Renfield! Get along with you, out from under my feet. Though if you've the wit for it, I've a riddle. Sing a song of sixpence, a pocket full of rye; four and twenty blackbirds, baked in a...?",
         choices=[
             C("...pie.", "pie", cond="!" + R + "got_brandy"),
             C("...cage.", "wrong", cond="!" + R + "got_brandy"),
             C("...net, with the wings still moving.", "wrong", cond="!" + R + "got_brandy"),
             C("Why do you keep the cat so fat, Mrs. Pargeter?", "cat"),
             C("[Withdraw]", end=True)]),
    wrong=N("Mrs. Pargeter", "Ha. No, no, no. Not that. The nursery rhyme, dear. I had a brother who told it the wrong way too, God rest him, and they put him in a place like this one.", next="n0"),
    cat=N("Mrs. Pargeter", "He earns it, the beast. He's the bravest in the house, sir. Eats whatever the garden sends, and sleeps in the warm. I keep him fat so he doesn't need to hunt.", next="n0"),
    pie=N("Mrs. Pargeter", "...Baked in a pie! There, you've a head on your shoulders. Now: Doctor says you're not to have anything stronger than cocoa, and I say a man who can finish a rhyme can have a drop in a cup for his nerves. Take it, hide it, and do not tell the Doctor that Cook says so.",
          do=[{"give": "brandy"}, {"set": R + "got_brandy"}, {"journal": R + "j_cook"}], next="n0"),
)

DIALOGUE[R + "cell_bed"] = D("n0",
    n0=N(ME, "The cot, and the grey blanket. It is early afternoon and the whole house is waiting for something.",
         choices=[
             C("[Lie down and wait for night]", "wait", cond=R + "plea_made&!" + R + "night&has:" + R + "garden_key&has:brandy"),
             C("[Think what a prudent man needs before the dark]", "notyet", cond=R + "plea_made&!" + R + "night"),
             C("[Not yet]", end=True)]),
    notyet=N(ME, "A prudent man gets his house in order before the dark: a key to the garden, a drop of brandy for the keeper. And a ward to wait for, only when I hold them all.", next="n0"),
    wait=N(ME, "I lie down and let the afternoon pass over me. When I wake the lamps are lit and the house is quiet. Somewhere a bell strikes ten.",
           do=[{"card": "That night, at Purfleet."}, {"set": R + "night"}, {"journal": R + "j_night"}], end=True),
)

DIALOGUE[R + "hide"] = D("n0",
    n0=N(ME, "I crouch behind the water-butt, in the wet. The night-man's lantern comes along the gravel, swinging. He is walking out to the far wall.",
         choices=[
             C("[Run for the wicket now, while he is walking away]", "run"),
             C("[Wait until he has stopped under the far lamp and bent over his pipe]", "wait"),
             C("[Wait until he has gone indoors]", "late"),
             C("[Withdraw]", end=True)]),
    run=N(ME, "I get three strides before the lantern swings round. 'Who's that?' I am back behind the butt with my heart in my mouth. He turns again. The lantern goes on.", next="n0"),
    late=N(ME, "I wait, and wait. He does not go in; he is on the bench with his pipe. It is a long, cold, wet quarter of an hour. Nothing has changed.", next="n0"),
    wait=N(ME, "He reaches the far wall, stops under the lamp, bends to his pipe, a match flaring in his cupped hands. His back is to me. I cross twelve yards of gravel in my stockinged feet, and not a stone speaks.",
           do=[{"set": R + "garden_clear"}, {"journal": R + "j_garden"}], end=True),
)

DIALOGUE[R + "voice"] = D("n0",
    n0=N("The Voice", "Renfield. You have come. You have kept my books faithfully, and I have kept my promise. I told you: lives. Not flies, not spiders, not a bird in the grass: lives. Great ones. Do you hold something for me?",
         choices=[
             C("[Offer the sparrow: 'Yes, Master. A life, as you taught me.']", "loyal", cond="has:" + R + "sparrow"),
             C("[Say: 'I have totalled the ledger. It does not close, Master. You owe me, not I you.']", "refuse", cond="has:" + R + "sparrow&" + R + "understood"),
             C("[Write something for Dr. Seward on the altar cloth]", "note", cond="has:" + R + "pencil&!" + R + "warned"),
             C("[Say you have nothing yet, and withdraw]", end=True)]),
    note=N(ME, "I tear a clean page from the back of the ledger and write, in the clerk's hand I have never lost: 'Doctor, he is real. The box is in the chapel. Do not come alone. Garlic, a cross, and the sunlight. I am sorry for the trouble. R. M. R.' I tuck it beneath the candle where the morning will find it.",
           do=[{"set": R + "warned"}, {"journal": R + "j_warning"}], next="n0"),
    loyal=N("The Voice", "Ahh. Yes. Good servant. Give it me, and the bird shall be the first of many. Seven, then seventy, then seven thousand. You have only to be faithful.",
            choices=[
                C("[Close my hand around it]", "loyal_end"),
                C("...No. Wait.", "n0")]),
    loyal_end=N(ME, "I do what I have done a hundred times. It is a small, warm, brief thing and it is over before the voice has finished its blessing. And then there is no blessing: only the pale smell of earth, and a feather on my thumb, and the silence of a house that has taken what it asked for and will give nothing back.",
                choices=[C("[Go out into the night]", end=True, do=[
                    {"card": "In the morning they found Mr. Renfield asleep on the chapel floor with a feather in his hand. He said very little. He did not eat for two days, and then he asked, very civilly, for a clean ledger. He never again counted a fly. Dr. Seward wrote it down. He did not write down what it cost him to see it."},
                    {"set": R + "loyal"}, {"journal": R + "j_end_loyal"}, {"arc_end": 1}])]),
    refuse=N("The Voice", "You dare. You, who ate a thousand little lives in my name! You are mine, Renfield. You are a vessel, a thing I fill. What is one sparrow to a man who has eaten ten thousand?",
             choices=[
                 C("[Stand quite still. 'I am Renfield. I was a man of business, and I have totalled the account. Nothing is owed.']", "calm_end"),
                 C("[Scream at it, strike the altar, and beat the box till my knuckles split]", "frenzy_end")]),
    calm_end=N(ME, "The word 'Renfield' goes through the chapel like a coin on stone. The voice thins. I cross to the broken window, open my hands, and the sparrow shakes itself once, and flies out of my fingers and over the wall into the grey. It does not look back. It is the best bookkeeping I have ever done.",
               choices=[C("[Go out into the night]", end=True, do=[
                   {"card": "In the morning they found Mr. Renfield in the chapel, wide awake and quite calm, with a torn page beside him and nothing in his hands. He asked for Dr. Seward, and he was gentle with Hodge. In his last hour he gave the doctor what a sick man has to give: a little courage, a little brandy and the truth. Seward never forgot it."},
                   {"set": R + "mercy"}, {"journal": R + "j_end_mercy"}, {"arc_end": 1}])]),
    frenzy_end=N(ME, "I roar. I beat the lid until the voice is a sound like paper tearing, and when I come to myself I am on my knees with split hands, and the sparrow is still alive, trembling in the crook of my arm. I lift it to the window. It goes, in a flurry. I laugh, I think, or weep.",
                 choices=[C("[Go out into the night]", end=True, do=[
                     {"card": "In the morning they found Mr. Renfield in the chapel, bruised, bleeding and quite awake. He asked for Dr. Seward and said, 'I have been a long time wrong, doctor, but I think I have been right once.' In his last hour he repaid it as best he could. Seward never forgot him."},
                     {"set": R + "mercy"}, {"journal": R + "j_end_mercy"}, {"arc_end": 1}])]),
)

# ---------------------------------------------------------------------------------------------------------------- items
ITEMS = {
    R + "spoon": dict(name="Tin spoon", asset="key", variant="gold", desc="A bent tin spoon that has seen better dinners. A lever for a loose board."),
    R + "ledger": dict(name="Notebook of lives", asset="book", variant="diary", desc="Renfield's ledger: every fly, spider and sparrow, in a clerk's hand. A sane document about an insane account."),
    R + "sugar": dict(name="Lump of sugar", asset="chest", variant="pale", desc="A white lump, blue-papered. The bait for the smallest and most numerous of lives."),
    R + "jar": dict(name="Jam jar", asset="bottle", variant="glass", desc="An empty glass jar with a ring of old jam at the lip."),
    R + "flies_jar": dict(name="Jar of flies", asset="bottle", variant="green", desc="A jar of eleven small furious lives, held in a palm."),
    R + "garden_key": dict(name="Garden key", asset="key", variant="gold", desc="An iron key on a loop of tape marked 'GARDEN'. The spider's, or Hodge's."),
    R + "sparrow": dict(name="Injured sparrow", asset="bat", variant="brown", desc="A small brown bird with a hurt wing, warm in the hand. It weighs nothing, and it weighs everything."),
    R + "transfer_note": dict(name="Dr. Seward's note", asset="book", variant="red", desc="A note in Seward's hand: 'Move R. to the quiet wing on Monday. Be gentle.'"),
    R + "pencil": dict(name="Stub of pencil", asset="stake", variant="default", desc="Dr. Seward's pencil stub. It was meant for case-notes and will do for confessions."),
    R + "keepsake": dict(name="Renfield's notebook of lives", asset="book", variant="leather", desc="A cloth-bound notebook with a faded crest. The last entry is a sparrow, crossed out."),
}

# ---------------------------------------------------------------------------------------------------------------- journal
JOURNAL = {
    R + "j_wake": J("Room 12", "Morning at Purfleet. A cell padded in grey, a tin tray, a window with the first flies. I am R. M. Renfield, once of a good house and sound mind. Today I must be a gentleman to Hodge, find my ledger, and make myself reasonable to the doctor."),
    R + "j_calm": J("A gentleman at the door", "I said, 'I am quite myself, Mr. Hodge,' and Hodge opened the door. It is astonishing what a civil tongue will do for a man in a grey ticking cell. I wish I had known as much in the Strand."),
    R + "j_frenzy": J("The wet sheet", "I raved at Hodge. He held me in his arms until the strength had left me, then opened the door as gently as for a child. I should not have shouted. It costs me more than it costs him."),
    R + "j_ledger": J("The notebook of lives", "Under the loose board, wrapped in my father's handkerchief: my notebook. Eleven flies, forty spiders, three hundred sparrows, a cat. A column of figures that grows and never closes. It is the only honest document in this house."),
    R + "j_count": J("Seven, three, nine", "Quill counts everything. The doctor's inventory board gives beds, windows, lamps: seven, three, nine. That is the order in which the doctor writes it, and so the wheels of the linen-press must be set."),
    R + "j_sugar": J("The sugar ration", "Seven, three, nine, and the press gave up one lump of sugar on a blue paper. Dr. Seward locks it away so we cannot hoard. I have hoarded other things from him, and will go on."),
    R + "j_flies": J("The sugar and the sill", "Sugar on the sill, and in a minute the flies came. Eleven. Dr. Seward would call it a dozen flies on a lump of sugar. I call it a tithe. I am not certain which of us is the more honest."),
    R + "j_hodge_key": J("The lost garden key", "Hodge dropped the garden key in the scullery three weeks ago and told nobody. Between ourselves, he thinks the mice have it. I think the spider has it. We are both of us probably right."),
    R + "j_key": J("The spider's key", "Fed the spider eleven flies; she dropped the key from her web, an iron key on a loop of tape marked 'GARDEN'. Hodge's, the doctor would say. The spider's, I say. It does not matter which, only that I have it."),
    R + "j_cook": J("Cook and the rhyme", "'Baked in a pie.' Mrs. Pargeter laughed, gave me brandy in a cup and swore me to secrecy. Her brother died in a place like mine. People are kinder than a case-book allows."),
    R + "j_notes": J("What the doctor wrote", "In Seward's notes: 'He does not lie. His dread of the unseen is genuine. I do not know what to make of a delusion so well-regulated.' It is the kindest thing anyone has written of me since my father's will."),
    R + "j_plea": J("The plea", "I asked Dr. Seward to send me away before the Master comes. The ledger did it: a clerk's hand speaks better than a madman's mouth. He has written a note: the quiet wing, on Monday. Monday is too far, but it is a start."),
    R + "j_round": J("Blunt's round", "Hodge says Blunt does the garden at ten and two: out to the far wall, a pause to light his pipe, and back. Same every night for ten years. A man who is predictable is a man who can be avoided."),
    R + "j_night": J("Night at Purfleet", "The lamps are low and the house is quiet. I have the key, the brandy and the list. Hodge sits his watch in the day-room, and I feel the Master through the wall like a second pulse."),
    R + "j_hodge": J("Hodge sleeps", "A cup of Cook's brandy for his nerves, and Hodge sleeps in his chair. I did not hurt him, or lie to him, except in the matter of why. I leave him a blanket."),
    R + "j_garden": J("The wicket", "Behind the water-butt I waited for the pipe, and when the night-man bent to his match I crossed the gravel without a sound. A man who counts can wait. It is the only virtue that madness has left me."),
    R + "j_chapel": J("Carfax", "The chapel at Carfax, the box in its aisle and the voice about it. He has not touched the ledger. He has not paid one penny of what he promised. I am quite steady, for once, and quite sure I can add."),
    R + "j_sum": J("The sum", "I totalled the ledger on his box: eleven flies, forty spiders, three hundred sparrows, the cat. It never closes, and neither does his promise. He has taken my lives and given me none. A bookkeeper knows a bad debtor when he meets one."),
    R + "j_warning": J("A note for the doctor", "I wrote Seward a page and left it under the candle: the box, the voice, the garlic, the cross, the sun. It is the first letter I have written in years. I signed it with my initials and the crest."),
    R + "j_end_mercy": J("The sparrow", "I opened my hand at the window. The sparrow went over the wall. It is the only life I ever gave back, and I will take it with me wherever I am sent. I think the doctor will have my notebook. I would rather he had that than anything else."),
    R + "j_end_loyal": J("What I took", "The sparrow was warm for a moment and then it was not. The voice said I had done well. I have never felt smaller. I think I understand now what the doctor meant by 'delusion'. It is a debt that cannot be paid."),
}

# ---------------------------------------------------------------------------------------------------------------- combat
ENEMIES_EXTRA = {
    R + "blunt": dict(name="Blunt, night attendant", model="human_peasant_m", hp=14, spd=5, dmg=[2, 4], acc=62, eva=5, tags=["human"], flee_at=0.4,
                      book="a night attendant at Purfleet (invented)"),
}
ENCOUNTERS_EXTRA = {
    R + "scuffle": dict(name="Scuffle with the night-man", time="night", enemies=[R + "blunt"], flee_ok=True,
                        intro="The lantern swings round. 'You! Back to your bed!' Blunt's stick comes up. I am a thin man of fifty-nine with a madman's strength, and I know exactly how that story ends.",
                        win="He goes down against the wall, winded, and not hurt past a bruise. I step over him and I am not proud.", location=R + "garden"),
}
_CLEAR = [{"set": R + "garden_clear"}, {"journal": R + "j_garden"}]
ENCOUNTER_HOOKS = {
    R + "scuffle": dict(
        on_win=_CLEAR + [say("The gravel is quiet again. A man does not stay a clerk after a night like this.")],
        on_lose=_CLEAR + [say("I wake behind the water-butt with a split lip. Blunt has gone indoors to fetch the doctor, cursing, and the wicket stands unwatched.")],
        on_flee=_CLEAR + [say("I scramble behind the butt. Blunt searches, swears, and goes to rouse Hodge. I have a quarter of an hour.")]),
}

# ---------------------------------------------------------------------------------------------------------------- seed variation
PALETTES = {
    R + "cell": [dict(wall="plaster_dirty", floor="planks", wood="pale", cloth="blue"), dict(wall="plaster", floor="planks", wood="dark", cloth="cream")],
    R + "ward": [dict(wall="plaster", floor="planks", wood="dark", cloth="blue"), dict(wall="plaster_dirty", floor="planks", wood="oak", cloth="green")],
    R + "study": [dict(wall="plaster_dirty", floor="planks", wood="ebony", cloth="green"), dict(wall="stone_grey", floor="planks", wood="dark", cloth="red")],
    R + "scullery": [dict(wall="plaster", floor="cobble", wood="pale", cloth="cream"), dict(wall="plaster_dirty", floor="cobble", wood="oak", cloth="blue")],
}

PLACEMENTS = {
    R + "spoon": [
        dict(prop=R + "tray", text="Under the bread, flat against the tin: the missing spoon.", hint="The bread on the tray sits oddly."),
        dict(prop=R + "bucket", text="Hooked over the inside rim of the bucket, a bent tin spoon.", hint="The bucket has a faint ring of tin-polish round its rim."),
        dict(prop=R + "stool", text="Wedged into the crack under the stool-seat, a tin spoon.", hint="The stool wobbles on one side, as if something were pushed into it."),
    ],
    R + "pencil": [
        dict(prop=R + "shelf", text="Behind Pinel, a pencil stub, the sort a doctor loses for a month.", hint="One volume on the shelf sits out of line."),
        dict(prop=R + "fire", text="On the mantel behind the stopped clock, a short pencil stub.", hint="The mantel is dusted everywhere but one corner."),
        dict(prop=R + "armchair", text="Down the back of the cushion, a pencil stub, no doubt dropped by a thoughtful patient.", hint="The cushion has been sat on and then disturbed."),
    ],
}
