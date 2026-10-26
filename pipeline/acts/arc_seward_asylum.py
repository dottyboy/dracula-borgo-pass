"""PERSONAL ARC - Dr. John Seward: "Case Notes" (the private asylum at Purfleet, late May, before Lucy's illness).
Playable: seward.  All ids prefixed seward_asylum_."""
from dsl import *

P = "seward_asylum_"


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


S = "Seward"
J = "Dr. Seward's diary"

ARC = dict(
    id="seward_asylum", title="Case Notes", member="seward", portrait="seward",
    blurb="Purfleet, May. A man who cures other men's sleeplessness cannot cure his own; then the asylum goes wrong in a single night, and Dr. Seward must trust his judgment, his medicine and his nerve.",
    unlock="roster:seward", unlock_text="Meet Dr. Seward (Act II).", after_credits=False,
    start=dict(location=P + "study", protagonist="seward", party=["seward"], items={}, flags=[]),
    exit_to="ARC_END",
    rewards=[dict(give="doctors_greatcoat"), dict(set="medicine"), dict(give="chloral"), dict(give="chloral"), dict(give="chloral"),
             dict(give=P + "cylinder"), dict(stat=dict(member="seward", hp=2, nerve=3, faith=1))],
    rewards_text="Unlocks the chloral recipe (medicine); 3 chloral and Seward's phonograph cylinder; +2 HP, +3 Nerve, +1 Faith for Dr. Seward Gear: a doctor's greatcoat.",
)

LOCATIONS = [
    dict(id=P + "study", name="Dr. Seward's study, Purfleet", date="25 May",
         desc="Carbolic, cigar smoke and the faint sweetness of chloral. The phonograph waits on the desk, and the house is quiet in the particular way of a house full of the sleepless."),
    dict(id=P + "ward", name="The patients' ward", desc="A long day-room with iron beds along the wall, a stopped clock, and the soft, continual sounds of people who talk to themselves."),
    dict(id=P + "cell", name="Room 12", desc="Renfield's room. Sugar on the table, a jar on the window-sill, and a stillness that is never quite restful."),
    dict(id=P + "dispensary", name="The dispensary", desc="Jars, scales and a locked poison-cupboard. Everything here can cure or kill, depending on a grain."),
    dict(id=P + "records", name="The records room", desc="Case-books in rows, copying-presses and a bundle of foreign letters tied with tape."),
    dict(id=P + "garden", name="The asylum garden", desc="Gravel, a water-butt and a high old wall. Beyond it, the dark mass of Carfax."),
]

LOC_DATA = {}

# --------------------------------------------------------------------------------------------------------------------
LOC_DATA[P + "study"] = dict(
    cells=[2, 2], wall="plaster_dirty", floor="planks", interior=True,
    ambient=AMBIENT["candle_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2]),
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_door_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[0, 2.0], spawns={P + "ward": [2.4, 1.6], P + "records": [-2.4, -1.4]},
    props=[
        prop(P + "s_desk", "table", "ebony", -1.0, -2.6, name="Seward's desk", radius=0.9,
             look="Case-notes in rows, a blotter, an ink-well and a good deal of cigar ash. The desk of a man who works because he cannot sleep."),
        prop(P + "s_phono", "chest", "dark", -1.6, -2.6, y=0.8, scale=0.35, name="Phonograph", radius=0.4, talk=P + "phono"),
        prop(P + "s_note", "book", "diary", -0.5, -2.6, y=0.8, name="Lucy's note", radius=0.2, talk=P + "hillingham"),
        prop(P + "s_shelf", "bookshelf", "ebony", 2.4, -3.4, name="Medical shelves", radius=0.8,
             look="Maudsley, Esquirol, Pinel, Carpenter on dreams, and a gap where a volume was borrowed by nobody."),
        prop(P + "s_fire", "fireplace", "soot", -3.4, 2.0, rot=90, name="Fireplace", radius=0.8,
             look="Banked low. On the mantel the clock has been wrong for a week, and I have not had the heart to correct it."),
        prop(P + "s_armchair", "chair", "green", 0.8, 0.8, rot=180, name="Armchair", radius=0.4, talk=P + "vigil"),
        prop(P + "s_decanter", "bottle", "amber", 2.4, -3.4, y=1.2, scale=0.8, name="Brandy decanter", radius=0.2,
             look="Two fingers gone since Sunday. Brandy is not a cure; it is a postponement."),
        prop(P + "s_rug", "rug", "blue", 0, 0.4, radius=0.1),
        prop(P + "s_sconce", "sconce", "default", -3.7, 0.2, y=1.6, rot=90, radius=0.1),
        prop(P + "s_candle", "candelabra", "default", 0.6, -2.6, y=0.8, name="Candelabra", radius=0.2,
             look="Three candles, burnt to the same stub. I have sat up under them every night this week."),
        prop(P + "s_door_rec", "door", "ebony", -3.8, -2.0, rot=90, name="Door to the records room", radius=0.6,
             look="The records room, where every patient is a handful of ruled pages.", go=P + "records"),
        prop(P + "s_door_ward", "door", "ebony", 3.8, 2.0, rot=-90, name="Door to the ward", radius=0.6,
             look="The ward door. It is kept locked, and I keep the key where I will not forget it.",
             go=P + "ward", go_cond="has:" + P + "ward_key", go_fail="Locked. I always keep the ward key somewhere sensible, which means I never remember where."),
    ],
    on_enter=[dict(once=True, do=[dict(journal=P + "j_sleepless"),
                                  say("Three nights without sleep. Lucy Westenra has refused me, kindly, and I have gone on doctoring as if nothing had happened. Perhaps the day's work will tire me. I begin with the ward, which means finding the key.")])],
)

# --------------------------------------------------------------------------------------------------------------------
LOC_DATA[P + "ward"] = dict(
    cells=[3, 2], wall="plaster", floor="planks", interior=True,
    ambient=AMBIENT["warm_day_interior"], camera=cam([3, 2]), lights=lights_warm([3, 2], energy=2.4),
    walls=dict(north=["wall_4", "wall_door_4", "wall_4"], west=["wall_door_4", "wall_door_4"], east=["wall_4", "wall_door_4"]),
    spawn=[-4.0, 1.6], spawns={P + "study": [-4.2, -1.2], P + "garden": [-4.2, 1.4], P + "cell": [0, -2.4], P + "dispensary": [4.2, 1.4]},
    props=[
        prop(P + "w_bed1", "bed_simple", "blue", -3.5, -3.0, name="Iron bed", radius=0.8, look="A narrow bed with the blanket folded square. Whoever sleeps here folds it every morning, whatever the night did."),
        prop(P + "w_bed2", "bed_simple", "blue", 3.0, -3.0, name="Iron bed", radius=0.8, look="A bed under the window. The pillow is damp from some weeping nobody mentioned."),
        prop(P + "w_clock", "column", "plaster_dirty", -5.0, -2.0, rot=90, scale=0.9, name="Ward clock", radius=0.6,
             look="A tall case-clock, hands stopped at ten past three. It has been stopped as long as I have kept the house.",
             use_item={P + "clock_key": [
                 {"set": P + "clock_wound"}, {"take": P + "clock_key"}, {"give": P + "dispensary_key"}, {"journal": P + "j_clock"},
                 say("The mainspring bites. The clock strikes ten past three, ticks, and goes on. A small door in the case swings open, and behind it hangs the dispensary key on a nail, where Hennessey has hidden it.")]},
             use_fail="It will not respond to that."),
        prop(P + "w_linen", "chest", "pale", 5.0, -3.0, name="Linen cupboard", radius=0.6,
             look="Sheets, towels, a stack of grey blankets. Everything smells of soap and boiled cotton.",
             take=P + "blanket", take_text="I take a grey wool blanket from the stack.", give_once=True),
        prop(P + "w_table", "table_long", "dark", 1.6, 0.4, name="Day-room table", radius=1.4, look="A scarred table where patients play dominoes and nobody keeps score."),
        prop(P + "w_chair1", "chair", "black", 0.2, 1.4, rot=180, name="Day-room chair", radius=0.4),
        prop(P + "w_chair2", "chair", "black", 3.0, 1.4, rot=180, name="Day-room chair", radius=0.4),
        prop(P + "w_bench", "bench", "oak", -3.4, 1.2, rot=90, name="Window bench", radius=0.8, look="Where the patients sit in the afternoon to watch weather they are not allowed in."),
        prop(P + "w_lantern", "lantern", "default", 1.6, 0.4, y=0.8, name="Ward lantern", radius=0.2, look="Turned low. The attendants say a patient will not sleep in true dark, nor in true light."),
        prop(P + "w_rug", "rug", "cream", -0.5, 2.6, radius=0.1),
        prop(P + "w_sconce", "sconce", "default", 2.0, -3.6, y=1.6, radius=0.1),
        prop(P + "w_door_study", "door", "ebony", -5.8, -2.0, rot=90, name="Door to Dr. Seward's study", radius=0.6, look="My study.", go=P + "study"),
        prop(P + "w_door_garden", "door", "oak", -5.8, 2.0, rot=90, name="Door to the garden", radius=0.6,
             look="The garden door. Hennessey locks it at dusk.", go=P + "garden"),
        prop(P + "w_door_cell", "door", "dark", 0.0, -3.8, name="Room 12", radius=0.6,
             look="A heavy door with a grille. The brass plate says 12.", go=P + "cell"),
        prop(P + "w_door_disp", "door", "ebony", 5.8, 2.0, rot=-90, name="Dispensary door", radius=0.6,
             look="The dispensary. It is locked, and the key is not on my ring.",
             go=P + "dispensary", go_cond="has:" + P + "dispensary_key", go_fail="Locked. Hennessey says the key is 'kept safe', which is no answer."),
    ],
    npcs=[
        npc(P + "hennessey", "human_peasant_m", P + "hennessey", -1.8, -1.0, rot=180, name="Attendant Hennessey",
            look="A large, kind man in a white coat who has been bitten twice and bears no grudge.", talk=P + "hennessey"),
        npc(P + "pym", "human_peasant_m", P + "pym", -4.0, 0.2, rot=90, name="Mr. Pym",
            look="A small grey man in a cardigan, who keeps glancing at the stopped clock as if it owes him an apology.", talk=P + "pym"),
        npc(P + "vane", "human_peasant_f", P + "vane", 3.6, 2.6, rot=180, name="Miss Vane",
            look="A governess of fifty, upright on the window bench, a sheaf of unsent letters on her knee.", talk=P + "vane"),
        npc(P + "pettit", "human_peasant_m", P + "pettit", 4.4, 0.4, rot=-90, name="Pettit, the dispenser's boy",
            look="A thin lad of seventeen with violet-stained fingertips, sweeping a floor that is already clean.", talk=P + "pettit"),
        npc(P + "dowling", "human_peasant_f", P + "dowling", 1.0, 2.8, rot=180, name="Nurse Dowling", cond=P + "night",
            look="The night nurse, grey-faced and steady, a lamp in her hand.", talk=P + "dowling"),
    ],
    on_enter=[
        dict(**{"if": P + "night"}, once=True, do=[dict(journal=P + "j_night"),
                                                  say("Two in the morning. Smoke is coming under the dispensary door, Room 12 is standing open, and somewhere down the corridor a lad is crying.")]),
        dict(once=True, do=[say("The ward in the grey of the afternoon. They look up as I come in, as they always do: the same faces, the same private weather.")]),
    ],
)

# --------------------------------------------------------------------------------------------------------------------
LOC_DATA[P + "cell"] = dict(
    cells=[2, 2], wall="plaster_dirty", floor="planks", interior=True,
    ambient=AMBIENT["cold_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2], energy=2.0),
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_4", "wall_door_4"], east=["wall_4", "wall_4"]),
    spawn=[-2.4, 1.6], spawns={P + "ward": [-2.4, 1.6]},
    props=[
        prop(P + "c_cot", "bed_simple", "black", 2.4, -2.6, name="Iron cot", radius=0.8, look="Made with the tightness of a soldier's. The mattress has been unpicked and sewn again, twice."),
        prop(P + "c_table", "table", "pale", -1.0, -2.0, name="Sugar table", radius=0.8, look="Sugar in a saucer, in lines, drawing the flies from the window."),
        prop(P + "c_jar", "bottle", "glass", -1.0, -2.0, y=0.8, scale=1.1, name="Jar of flies", radius=0.2,
             look="A sugar-smeared jar, perhaps two dozen flies, buzzing without hope. They are counted every morning."),
        prop(P + "c_ledger", "book", "red", -0.5, -2.0, y=0.8, name="Hennessey's diet ledger", radius=0.2, talk=P + "ledger"),
        prop(P + "c_web", "deadtree", "grey", -3.2, -3.0, scale=0.3, name="Spider-corner", radius=0.4,
             look="Webs hang in the corner like a hammock, and a fat house-spider sits in the centre of it. It has not been disturbed in weeks."),
        prop(P + "c_basket", "chest", "pale", -3.0, 0.4, scale=0.55, name="Empty basket", radius=0.4,
             look="A cat's basket. The cat is not mentioned in the ward, and nobody looks at the basket for long."),
        prop(P + "c_cage", "lantern", "default", 1.0, -2.6, y=0.0, scale=1.2, name="Empty bird-cage", radius=0.3,
             look="A wicker cage the size of a loaf. The door stands open. The sparrows are written down in the ledger, and nowhere else."),
        prop(P + "c_stool", "chair", "black", 0.8, 0.6, rot=180, name="Stool", radius=0.35, look="Bolted to the floor. Dr. Seward's stool, when he comes to listen."),
        prop(P + "c_bucket", "barrel", "dark", 3.0, 1.0, scale=0.7, name="Bucket", radius=0.3),
        prop(P + "c_rug", "rug", "black", 0.2, 0.4, scale=0.8, radius=0.05),
        prop(P + "c_sconce", "sconce", "default", -3.7, -1.0, y=1.6, rot=90, radius=0.1),
        prop(P + "c_door", "door", "dark", -3.8, 2.0, rot=90, name="Door to the ward", radius=0.6, look="The heavy door, always locked from the outside.", go=P + "ward"),
    ],
    npcs=[
        npc(P + "renfield_cell", "human_renfield", "asylum", 0.8, -0.6, rot=-90, name="R. M. Renfield", cond="!" + P + "night",
            look="A thin, pale man near sixty, calm, with an eye on the window and a little line of sugar before him.", talk=P + "renfield"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=P + "j_cell")])],
)

# --------------------------------------------------------------------------------------------------------------------
LOC_DATA[P + "dispensary"] = dict(
    cells=[2, 2], wall="stone_grey", floor="planks", interior=True,
    ambient=AMBIENT["candle_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2], energy=2.4),
    walls=dict(north=["wall_4", "wall_window_4"], west=["wall_4", "wall_door_4"], east=["wall_4", "wall_4"]),
    spawn=[-2.4, 1.6], spawns={P + "ward": [-2.4, 1.6]},
    props=[
        prop(P + "d_cupboard", "bookshelf", "ebony", -2.2, -3.4, name="Poison cupboard", radius=0.8,
             look="Laudanum, chloral, morphia, strychnine, each in its own labelled bottle. The key hangs on a string; I will not have it locked up where a man cannot reach it in the night.",
             take="chloral", take_text="I take a bottle of chloral crystals from the cupboard, signing the register out of habit.", give_once=True),
        prop(P + "d_table", "table", "pale", 0.0, -1.2, name="Dispensing table", radius=0.9, look="Mortars, a graduated glass and a pair of brass scales, all scrubbed bright."),
        prop(P + "d_scale", "goblet", "default", -0.5, -1.2, y=0.8, name="Brass scales", radius=0.2, talk=P + "scale"),
        prop(P + "d_register", "book", "red", 0.5, -1.2, y=0.8, name="Poison register", radius=0.2, talk=P + "register"),
        prop(P + "d_jug", "bottle", "green", 2.5, -3.0, y=0.9, name="Water jug", radius=0.2,
             look="Distilled, for mixing. Take what you need; it is the only thing here that cannot kill.",
             take="water", take_text="I fill a clean glass from the jug.", give_once=True),
        prop(P + "d_fire", "fireplace", "soot", 1.6, -3.4, name="Dispensary shelf, burning", radius=0.9, cond=P + "night&!" + P + "fire_out",
             look="The shelf of ether and spirits is ablaze, and the flames are climbing the wall. Water will only spread an ether fire; it must be smothered.",
             use_item={P + "wet_blanket": [{"take": P + "wet_blanket"}, {"set": P + "fire_out"}, {"journal": P + "j_fire"},
                                           say("I throw the sodden blanket over the burning shelf and lean on it with my whole weight. The flames die in a hiss of steam and a stench of scorched spirit. Black smoke curls up, and then nothing.")],
                       "water": [say("I fling the water on the flames. They leap and spread across the shelf: ether floats on water and burns on it. Fool. It must be smothered, not drowned.")]},
             use_fail="That will not stop it."),
        prop(P + "d_burnt", "bookshelf", "ebony", 1.6, -3.4, name="Scorched shelf", radius=0.8, cond=P + "fire_out",
             look="Black and steaming, but standing. The chloral, thank God, was on the other side."),
        prop(P + "d_slip", "book", "leather", 0.2, -1.2, y=0.8, name="Prescription slip", radius=0.2, cond=P + "night&!has:" + P + "forged_slip",
             talk=P + "slip"),
        prop(P + "d_crate", "barrel", "dark", 3.0, 0.2, scale=0.8, name="Sal volatile cask", radius=0.4, look="Smelling salts, in bulk."),
        prop(P + "d_lantern", "lantern", "default", 2.8, -1.4, name="Dispensary lamp", radius=0.2, look="A shaded lamp with a glass chimney, safely away from the spirit shelves."),
        prop(P + "d_rug", "rug", "cream", 0, 1.4, radius=0.1),
        prop(P + "d_door", "door", "ebony", -3.8, 2.0, rot=90, name="Door to the ward", radius=0.6, look="The ward door.", go=P + "ward"),
    ],
)

# --------------------------------------------------------------------------------------------------------------------
LOC_DATA[P + "records"] = dict(
    cells=[2, 2], wall="plaster_dirty", floor="planks", interior=True,
    ambient=AMBIENT["candle_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2], energy=2.2),
    walls=dict(north=["wall_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[2.4, -1.4], spawns={P + "study": [2.4, -1.4]},
    props=[
        prop(P + "r_shelf", "bookshelf", "dark", -2.0, -3.4, name="Case-books A to F", radius=0.8, look="Patients who have gone home, patients who have died, and a few who are neither."),
        prop(P + "r_shelf2", "bookshelf", "dark", 1.8, -3.4, name="Case-books G to Z", radius=0.8, look="The house is full of paper. Madness, it turns out, is chiefly clerical."),
        prop(P + "r_desk", "table", "pale", -0.5, -0.8, name="Copying desk", radius=0.9,
             look="A copying-press, three ink-bottles and a rack of pens. The ink is violet, the clerk's ink, which stains the fingers for a week."),
        prop(P + "r_letters", "book", "diary", 0.0, -0.8, y=0.8, name="Letters from Amsterdam", radius=0.2, talk=P + "letters"),
        prop(P + "r_chest", "chest", "dark", -3.0, 1.6, name="Old chest", radius=0.6, look="A chest of old forms, ribbons and a wooden box marked 'Edison'."),
        prop(P + "r_press", "barrel", "oak", 2.8, 0.6, scale=0.8, name="Copying-press", radius=0.4, look="A screw press for copying letters. It leaves a violet ghost on the tissue."),
        prop(P + "r_lamp", "lantern", "default", -0.5, -0.8, y=0.8, name="Reading lamp", radius=0.2, look="A green-shaded lamp."),
        prop(P + "r_rug", "rug", "red", 0.4, 1.8, radius=0.1),
        prop(P + "r_sconce", "sconce", "default", -3.7, 0.0, y=1.6, rot=90, radius=0.1),
        prop(P + "r_door", "door", "ebony", 3.8, -2.0, rot=-90, name="Door to the study", radius=0.6, look="My study.", go=P + "study"),
    ],
    on_enter=[dict(once=True, do=[say("The records room, where the dead and the discharged still sit in neat rows. Somewhere in here is a wax cylinder for the phonograph, and a bundle of letters from Amsterdam.")])],
)

# --------------------------------------------------------------------------------------------------------------------
LOC_DATA[P + "garden"] = dict(
    cells=[4, 3], wall="stone_mossy", floor="dirt", interior=False,
    ambient=AMBIENT["dusk_exterior"], camera=cam([4, 3]), lights=lights_moon(2.4), moon=dict(pos=[-6, 10, -8]),
    scatter=dict(asset="pine", variant="dark", count=22, seed=17, avoid=[[-8, -6, 8, 6]]),
    spawn=[-6.0, 2.0], spawns={P + "ward": [-6.0, 2.0]},
    props=[
        prop(P + "g_arch", "arch", "stone_grey", -7.0, 2.0, rot=90, name="Door to the ward", radius=0.8, look="The garden door, back to the ward.", go=P + "ward"),
        prop(P + "g_butt", "barrel", "oak", -4.5, 3.0, scale=1.2, name="Water-butt", radius=0.5,
             look="A great oak butt of rain-water, cold enough to make your teeth ache.",
             use_item={P + "blanket": [{"take": P + "blanket"}, {"give": P + "wet_blanket"}, say("I duck the grey blanket in the cold water and wring it just enough that it will not drip all over me. It is now a heavy, sodden shroud.")]},
             use_fail="That does not need to be wetted."),
        prop(P + "g_bench", "bench", "dark", 2.0, 2.6, name="Garden bench", radius=0.9, look="Greer's bench. He sits here in all weathers, and the weather is polite about it."),
        prop(P + "g_wall1", "wall_4", "stone_mossy", -4.0, -5.4, name="Carfax wall", radius=1.2, look="The boundary wall of Carfax, ivy and broken glass. The empty house is on the other side."),
        prop(P + "g_wall2", "wall_4", "stone_mossy", 0.0, -5.4, name="Carfax wall", radius=1.2, look="Ivy, and the stub of a ladder that someone left by a wall where no ladder is needed."),
        prop(P + "g_wall3", "wall_4", "stone_mossy", 4.0, -5.4, name="Carfax wall", radius=1.2, look="Higher than a man, and tall enough to be an ill-wisher's idea of a fence."),
        prop(P + "g_chapel", "tower", "stone_grey", -6.0, -8.6, scale=0.6, name="Carfax chapel", radius=1.0, look="The old chapel, sunk behind the wall. No one has said a service in it for a long time."),
        prop(P + "g_tree", "deadtree", "grey", 5.4, -2.6, name="Dead plane tree", radius=0.5, look="Struck by lightning years ago. The sparrows still roost in it."),
        prop(P + "g_lantern", "lantern", "default", -1.4, 1.6, name="Garden lamp", radius=0.3, look="Lit at dusk by Hennessey. It makes the dark beyond it darker."),
        prop(P + "g_rock", "rock", "mossy", 6.0, 3.0, name="Boundary stone", radius=0.5),
    ],
    npcs=[
        npc(P + "greer", "human_peasant_m", P + "greer", 2.0, 3.6, rot=180, name="Mr. Greer", cond="!" + P + "night",
            look="An old sailor in a pea-coat, with a face like a tarred rope, sitting very straight and facing the sea that is forty miles away.", talk=P + "greer"),
        npc(P + "renfield_wild", "human_renfield", "asylum", 2.5, -3.0, rot=0, name="Renfield (frenzied)", cond=P + "night&!" + P + "renfield_calm&!" + P + "renfield_understood", radius=0.6,
            look="Renfield, in the garden after midnight, shirt torn, a smear of earth on his hands. He has found the wall and cannot be reasoned with; he is staring at the moon and snarling at it.",
            fight=P + "frenzy",
            use_item={P + "draught": [{"take": P + "draught"}, {"set": P + "renfield_calm"}, {"set": P + "calm_by_draught"}, {"journal": P + "j_renfield_night"},
                                     say("I hold out the glass, speaking low: 'The sugar, Mr. Renfield. You will want your sugar.' He drinks as a child drinks medicine. In ten minutes he is quiet, and I walk him back to Room 12.")],
                      "chloral": [{"set": P + "renfield_calm"}, {"journal": P + "j_renfield_night"},
                                  say("I press a dose of chloral into his hand in a glass of water, and he swallows it, still glaring. Slowly the glare fades. It is the dose I should have measured; luck has measured it for me.")]},
            use_fail="That will not calm him."),
        npc(P + "renfield_talk", "human_renfield", "asylum", 2.5, -3.0, rot=0, name="Renfield", radius=0.6, cond=P + "night&!" + P + "renfield_calm&" + P + "renfield_understood",
            look="Renfield, hunched under the wall, breathing hard. But I have read his ledger, and I think I know what he is feeling.", talk=P + "renfield_garden"),
        npc(P + "renfield_calm_n", "human_renfield", "asylum", 2.5, -3.0, rot=0, name="Renfield", radius=0.6, cond=P + "night&" + P + "renfield_calm",
            look="Renfield, sitting on the gravel with his hands between his knees. He looks like a clerk, which he once was.", talk=P + "renfield_calmed"),
    ],
)

# --------------------------------------------------------------------------------------------------------------------
# dialogue
# --------------------------------------------------------------------------------------------------------------------
DIALOGUE = {}

DIALOGUE[P + "phono"] = D("n0",
    n0=N(S, "The phonograph waits, the wax cylinder in its place, the horn turned toward me like an ear.",
         choices=[
             C("[Dictate a diary entry]", "rec1", cond="has:" + P + "blank_cylinder&!" + P + "night&!" + P + "recorded_grief"),
             C("[Finish the night's record]", "fin1", cond=P + "night&" + P + "fire_out&" + P + "pettit_resolved&" + P + "renfield_calm&has:" + P + "blank_cylinder"),
             C("[Ask what the machine is for]", "what"),
             C("[Step away]", end=True)]),
    what=N(S, "It records a voice, so that I do not need to write by candlelight. I have kept a diary since I first saw a ward, but I cannot yet say a thing aloud and let it stand. The machine keeps its counsel better than I do.", next="n0"),
    rec1=N(S, "'Twenty-fifth May. Lucy Westenra has refused me. She was gentle, and clear, and entirely right. I do not blame her, nor Arthur, nor myself, which is a nuisance, since a man wants someone to blame. I shall not sleep. I shall dose myself with chloral, in the proper measure, and be a better doctor for it.'", next="rec2"),
    rec2=N(S, "I let the cylinder run out. The voice that comes back is thinner than my own, and braver.",
           do=[dict(set=P + "recorded_grief"), dict(journal=P + "j_grief")], next="n0"),
    fin1=N(S, "Dawn comes grey over Purfleet. The dispensary is a black ruin of one shelf, Pettit is bargaining with his conscience in the ward, and Renfield sleeps in Room 12 with his sugar untouched. I wind the cylinder and begin.", next="fin2"),
    fin2=N(S, "'Case notes, the twenty-sixth. A night in which three things went wrong and none was the worst. I used judgment where I might have used force, medicine where I might have used a stick, and nerve, I hope, where I might have run. I write this partly for the Board, but chiefly for myself, who must not forget it.'", next="fin3"),
    fin3=N(S, "'I shall write to Van Helsing in Amsterdam tomorrow. He taught me that a doctor's chief duty is to doubt himself carefully. I shall tell him that I doubted, and went on.'",
           choices=[C("[Seal the cylinder and end the night]",
                      do=[dict(take=P + "blank_cylinder"), dict(give=P + "cylinder"), dict(journal=P + "j_end"),
                          dict(card="Within a fortnight Lucy would be pale, and Arthur would send a telegram, and Dr. Seward would write, with a hand he did not quite trust, to Amsterdam. But that was later. This night he had kept his house, his patients and his head, and that was enough to be going on with."),
                          dict(arc_end=1)])]),
)

DIALOGUE[P + "hillingham"] = D("n0",
    n0=N(S, "Lucy's note, on thick cream paper in her round, schoolgirl hand. It has been folded and unfolded until the creases are soft.",
         choices=[C("[Read it again]", "n1"), C("[Put it down]", end=True)]),
    n1=N("Lucy (letter)", "'Dear Dr. Seward, I cannot say what you wish. You have been kind and gentle and clever, and I would not lose your friendship for the world. But I am promised, in my heart, to another, and it would be cruel to let you hope. Please do not think the less of me. Lucy.'", next="n2"),
    n2=N(S, "I stood in the Hillingham drawing-room with my hat in my hand and she said it more kindly than I deserved. I said I understood. I said I wished her happy. I said it twice, to be sure that I had.",
         choices=[
             C("Burn the note.", "burn"),
             C("Keep it. A doctor should keep his case-notes.", "keep", do=[dict(set=P + "hillingham_read"), dict(journal=P + "j_hillingham")])]),
    burn=N(S, "I hold it to the candle. And I cannot. I fold it back along the creases and put it in the drawer, which is a different kind of weakness, but a more honest one.", do=[dict(set=P + "hillingham_read"), dict(journal=P + "j_hillingham")], end=True),
    keep=N(S, "I shall keep it. It is no use to anyone, which is the best reason I know for keeping a thing.", end=True),
)

DIALOGUE[P + "vigil"] = D("n0",
    n0=N(S, "The armchair, with a dent in it the shape of my sleeplessness.",
         choices=[
             C("[Sit up and wait for night]", "go", cond=P + "draught_made&" + P + "renfield_understood&" + P + "hillingham_read&journal:" + P + "j_debt&!" + P + "night"),
             C("[Not yet. There is more work in the house]", end=True, cond="!" + P + "night")]),
    go=N(S, "I have the draught measured, the letters read, and Renfield's secret half understood. If I am to sit up with any of it, it may as well be tonight.",
         choices=[C("[Settle in for the long night]",
                    do=[dict(card="Purfleet. Two in the morning."), dict(set=P + "night"), dict(goto=P + "ward")])]),
)

DIALOGUE[P + "letters"] = D("n0",
    n0=N(S, "A bundle of letters from Amsterdam in a crabbed, forceful hand. Van Helsing, my old master.",
         choices=[
             C("[The letter on dosage]", "l1"), C("[The letter on open minds]", "l2"), C("[The letter of that winter]", "l3"), C("[Tie them up again]", end=True)]),
    l1=N("Van Helsing (letter)", "'My dear John. On the chloral, remember the three lines I taught you. Fifteen grains for a woman or a frail man; twenty for a strong man in his full strength; never more than thirty for anyone; and sixty is not a sedative but a funeral. Weigh twice. A sleepy patient is a patient; a sleeping doctor is a catastrophe.'", do=[dict(journal=P + "j_dose")], next="n0"),
    l2=N("Van Helsing (letter)", "'John, you doubt too much, and then you believe too much, and the middle you never visit. Believe nothing because I say it; doubt nothing because you have not seen it. Write it all down, and then look at what is written. Madness is often a theory the world has not yet been told.'", do=[dict(journal=P + "j_open_mind")], next="n0"),
    l3=N("Van Helsing (letter)", "'You thanked me again in your last. I do not recall that winter's dying, John. I recall only that you sat for three nights with a man who was nothing to you, and that I could not leave a fever to do what you had not allowed it. You owe me nothing. But if you wish to pay, then be to some other sleepless fool what I was to you.'",
         do=[dict(journal=P + "j_debt")], next="n0"),
)

DIALOGUE[P + "hennessey"] = D("n0",
    n0=N("Hennessey", "Good afternoon, sir. All quiet, bar Mr. Pym, who is taking an interest in the weather again.",
         choices=[
             C("Tell me about the ward.", "ward"),
             C("Why is the ward clock stopped?", "clock", cond="!journal:" + P + "j_pym"),
             C("Who keeps the dispensary key?", "key"),
             C("Can you write the ward log tonight, if I am busy?", "mark"),
             C("[Leave him to his work]", end=True)]),
    ward=N("Hennessey", "Mr. Pym, the watchmaker; Miss Vane, who writes letters to a man who died in India; old Mr. Greer, who sits in the garden talking to the sea. And Number Twelve, sir, who you know. All good as gold, so long as the weather holds.", next="n0"),
    clock=N("Hennessey", "Ah. That was Mrs. Pym's clock. Stopped at ten past three, the hour she went, and he's never allowed it touched. Not once. If you tell him you know what the hour was, I think he might be persuaded. But only just.",
            do=[dict(journal=P + "j_pym")], next="n0"),
    key=N("Hennessey", "Safe, sir. I've put it where Mr. Pym would never let anyone look. That's the safest place in the house.", next="n0"),
    mark=N("Hennessey", "I'd be glad to, sir, but I can't, being no scholar. I sign with my mark, and a bad one. Mother couldn't spare me to the school. The log's best left to Nurse Dowling.",
           do=[dict(journal=P + "j_hennessey_mark")], next="n0"),
)

DIALOGUE[P + "pym"] = D("n0",
    n0=N("Mr. Pym", "Don't touch it. Don't touch the clock. It is quite right. It has been right ever since.",
         choices=[
             C("Why is it stopped, Mr. Pym?", "why", cond="!journal:" + P + "j_pym"),
             C("It stopped at ten past three, the hour your wife died.", "key", cond="journal:" + P + "j_pym&!has:" + P + "clock_key&!" + P + "clock_wound"),
             C("Thank you, Mr. Pym.", end=True, cond=P + "clock_wound"),
             C("[Leave him]", end=True)]),
    why=N("Mr. Pym", "Because it is my clock, doctor, and it has told the time quite long enough.", next="n0"),
    key=N("Mr. Pym", "...Who told you? Hennessey. He is a kind man and a poor liar. Ten past three, in the morning. I had the watch in my hand, and I counted her breaths, and they stopped. I was a watchmaker forty years and I could not mend that.",
          choices=[C("It need not stay stopped. A clock that runs again is not a clock that forgets.", "give")]),
    give=N("Mr. Pym", "Hm. Hm. Perhaps. Here, doctor: the winding key. Wind it, and set it, and then give me back the key. I am not ready to hold it. But I would like to hear it tick.",
           do=[dict(give=P + "clock_key")], end=True),
)

DIALOGUE[P + "vane"] = D("n0",
    n0=N("Miss Vane", "Dr. Seward. I am writing to Edmund, as you see. He is a poor correspondent, but a very faithful one.",
         choices=[
             C("How is the ward at night, Miss Vane?", "night"),
             C("Who is Edmund?", "edmund"),
             C("[Leave her to her letters]", end=True)]),
    edmund=N("Miss Vane", "He was to be my husband. He is in India. Mrs. Pritchard tells me he is dead, but I am sure that is a mistake of the post.", next="n0"),
    night=N("Miss Vane", "Oh, quiet enough. The boy comes in at night, you know, the one with the violet fingers. He sits in the dispensary with the lamp and practises writing a name on the back of old labels, over and over. I thought it a love-letter. It is rather a long way to travel for a love-letter, to practise one signature.",
            do=[dict(journal=P + "j_vane")], next="n0"),
)

DIALOGUE[P + "greer"] = D("n0",
    n0=N("Mr. Greer", "Sit, doctor. I was mate on the old Lizzie out of Sunderland, forty years back. D'you know what happens when spirit catches in a hold?",
         choices=[
             C("Tell me.", "fire"),
             C("What do you see out there?", "sea"),
             C("[Leave him]", end=True)]),
    fire=N("Mr. Greer", "You never throw water on it. The spirit floats and spreads it, burning, to every plank. We wet the blankets and smothered it. That's all there is to it, doctor: soak the blanket, drop it on, and lean. Mind you, I've forgotten my own wife's name, but I never forgot that.",
           do=[dict(journal=P + "j_greer")], next="n0"),
    sea=N("Mr. Greer", "A ship, doctor. She will come in out of the east with a dead crew and a dead master lashed to her wheel. Mind you, we all know that story. Do you? Well, then.", next="n0"),
)

DIALOGUE[P + "pettit"] = D("n0",
    n0=N("Pettit", "Doctor. Shall I do the dispensary jars again, sir?",
         choices=[
             C("Where do you learn your Latin, Pettit?", "latin", cond="!" + P + "night"),
             C("Pettit, I have a slip for sixty grains of morphia. Written in my name.", "slip",
               cond=P + "night&!" + P + "pettit_resolved&has:" + P + "forged_slip"),
             C("[Tell him he has done enough]", end=True)]),
    latin=N("Pettit", "From the labels, sir, and from the dispenser. He lets me copy the prescriptions so as I learn the hands. My mother's very ill, sir, in Barking. She cannot be left alone.", next="n0"),
    slip=N("Pettit", "I don't... what slip, sir?",
           choices=[
               C("The ink is violet, and Miss Vane saw you practising. Hennessey cannot write, and Mrs. Dowling was on the ward. Only one person could have done it.", "conf",
                 cond="journal:" + P + "j_slip&journal:" + P + "j_vane&journal:" + P + "j_hennessey_mark"),
               C("Someone has been practising my hand, Pettit. Who might it be?", "deny")]),
    deny=N("Pettit", "I don't know, sir. I swear I don't. Perhaps Mr. Hennessey. Perhaps...", next="n0"),
    conf=N("Pettit", "...It was for my mother, sir. The doctor in Barking has given her up and the pain is... she begged me. I thought sixty grains would carry her through a month. I tried it three times before I could do your S. Then I couldn't, and I started the fire to burn the slip, and it caught the ether...",
           choices=[
               C("[Send him to the Board for it]", "report", do=[dict(set=P + "pettit_resolved"), dict(set=P + "pettit_reported"), dict(journal=P + "j_pettit")]),
               C("[Tell him his mother is a patient of mine from tomorrow]", "help", do=[dict(set=P + "pettit_resolved"), dict(set=P + "pettit_helped"), dict(journal=P + "j_pettit")])]),
    report=N(S, "I do the thing the law requires, which is to say, I write to the Board and let a boy of seventeen pay for what a doctor ought to have prevented. I do not feel clean. I do not think I am meant to.", end=True),
    help=N(S, "I make a bargain: a proper prescription, signed in my own hand, to be dispensed by the dispenser and no one else; a bed for his mother in the cottage hospital at Purfleet; a boy who works off the damage in the dispensary under Hennessey's eye. It is not in any book of regulations. It is, I think, in one of Van Helsing's.", end=True),
)

DIALOGUE[P + "dowling"] = D("n0",
    n0=N("Nurse Dowling", "Doctor, thank God. Number Twelve is empty; the grating was forced from within. Hennessey's gone out after him. And there's smoke in the dispensary.",
         choices=[
             C("Where could Renfield have gone?", "ren"),
             C("Who was last in the dispensary?", "who"),
             C("[Go]", end=True)]),
    ren=N("Nurse Dowling", "The garden, sir. He always goes to the garden wall, to look at Carfax. If I may say so, doctor, leave the stick at home. Three men would be needed.", next="n0"),
    who=N("Nurse Dowling", "Pettit, to sweep. And me. And I don't write, sir, except the log, and my hand's not a bit like yours.", next="n0"),
)

DIALOGUE[P + "slip"] = D("n0",
    n0=N(S, "A prescription slip, half-burnt at the corner. 'Morph. mur. gr. lx. Pro J. Pettit.' The body of the slip is clerkly. The signature, 'J. Seward', is a very careful forgery.",
         choices=[C("[Pick it up and examine the ink]", "e"), C("[Leave it]", end=True)]),
    e=N(S, "The ink is violet, the clerk's copying ink, which stains the fingers for a week. Sixty grains of morphia: enough to kill three men. The signature is perfect, and somewhere a hand has practised my S fifty times to get it.",
        do=[dict(give=P + "forged_slip"), dict(journal=P + "j_slip")], end=True),
)

DIALOGUE[P + "scale"] = D("n0",
    n0=N(S, "The brass scales and the tray of weights. I have measured chloral on them a hundred times. I will not do it by guesswork tonight.",
         choices=[
             C("[Weigh out ten grains]", "ten", cond="has:chloral&has:water&!" + P + "draught_made"),
             C("[Weigh out twenty grains]", "twenty", cond="has:chloral&has:water&journal:" + P + "j_dose&!" + P + "draught_made"),
             C("[Weigh out thirty grains]", "thirty", cond="has:chloral&has:water&!" + P + "draught_made"),
             C("[Weigh out sixty grains]", "sixty", cond="has:chloral&has:water&!" + P + "draught_made"),
             C("[Ask what the draught is for]", "what"),
             C("[Step away]", end=True)]),
    what=N(S, "For Renfield. If he breaks out, and the garden wall keeps its mortar poorly, a draught that is neither too weak nor too strong may be the difference between a man put to bed and a man put in the ground. I need both chloral and a clean glass of water, and I need to know the right number.", next="n0"),
    ten=N(S, "Ten grains. For Renfield, who is strong and wakeful, it would simply make him cross. I pour it away.", next="n0"),
    thirty=N(S, "Thirty grains: the limit, not the dose. It might put him down; it might stop his heart. I pour it away.", next="n0"),
    sixty=N(S, "Sixty grains is not a sedative but a funeral. I set it down before I have thought about it, and wash my hands.", next="n0"),
    twenty=N(S, "Twenty grains for a strong man in his full strength, as Van Helsing wrote. I weigh it twice and dissolve it in the water. Clear, bitter-sweet, innocent. A bottle I hope never to use.",
             do=[dict(take="chloral"), dict(take="water"), dict(give=P + "draught"), dict(set=P + "draught_made"), dict(journal=P + "j_draught")], end=True),
)

DIALOGUE[P + "register"] = D("n0",
    n0=N(S, "The poison register, a ledger of every grain that has left this room, in my hand and the dispenser's.",
         choices=[C("[Turn to Renfield's entry]", "r"), C("[Close it]", end=True)]),
    r=N(S, "'R. M. Renfield, aet. 59. Sanguine; great physical strength; fourteen stone; sleeps ill. Chloral, if needed, to the full strong-man dose, to be witnessed by the attendant.' I wrote that three months ago, and have been careful with it since.", next="n0"),
)

DIALOGUE[P + "ledger"] = D("n0",
    n0=N(S, "Hennessey's diet ledger for Room 12, his big round hand, week after week. I have read it a dozen times, but not as a series.",
         choices=[
             C("[Read about the flies]", "f"), C("[Read about the spiders]", "s"), C("[Read about the sparrows]", "b"), C("[Read about the kitten]", "k"),
             C("[Close it]", end=True)]),
    f=N(S, "'Flies, caught on sugar, 3-4 a day. Mr. R. keeps them in a jar, to hold the lives, in his own words. Eats none for first fortnight. Third week: eats them. Says they are quite delicious, and so full of life.'", do=[dict(journal=P + "j_flies")], next="n0"),
    s=N(S, "'Spiders. He feeds the flies to spiders, and swallows the spiders. Says: one spider is worth a hundred flies, for the life in it.'", do=[dict(journal=P + "j_spiders")], next="n0"),
    b=N(S, "'Sparrows. He tamed one. Wanted a cat to eat the sparrows. Now keeps them, begs for more, and one morning there is a heap of feathers. He says he should like a cat, for the spider's life is little, and the sparrow's is more. Not a word to the doctor.'", do=[dict(journal=P + "j_sparrows")], next="n0"),
    k=N(S, "'A kitten, brought by the housemaid. Wanted by him, begged for. The kitten went into his room on Tuesday and came out on Wednesday as a cap-ribbon of fur and a smear. Mr. R. ill, afterwards, as if he had been sick with grief.' I have written nothing under it. I do not need to.", do=[dict(journal=P + "j_cat")], next="n0"),
)

DIALOGUE[P + "renfield"] = D("n0",
    n0=N("Renfield", "Doctor Seward. I am quite at your service, and as sane as any man in England. Might I trouble you for another saucer of sugar?",
         choices=[
             C("How are you sleeping, Mr. Renfield?", "sleep"),
             C("Tell me about the flies.", "flies"),
             C("I have read the ledger. I think I understand what the flies were for.", "theory",
               cond="journal:" + P + "j_flies&journal:" + P + "j_spiders&journal:" + P + "j_sparrows&journal:" + P + "j_cat&!" + P + "renfield_understood"),
             C("[Leave him]", end=True)]),
    sleep=N("Renfield", "Poorly, Doctor. A man in my position has so much to keep track of. I find I count, and the counting does not stop.", next="n0"),
    flies=N("Renfield", "Flies are lives, Doctor. Small lives, but each a life. I keep them, as you keep your patients. Is it so different?", next="n0"),
    theory=N(S, "You do not eat the flies because you are hungry, Mr. Renfield. You eat them because each one is a bit of life, and you wish to gather more life into yourself. The spider for the flies, the sparrow for the spiders, and the cat for the sparrows. Each is a step up a ladder. And what did you wish to be at the top?",
             next="theory2"),
    theory2=N("Renfield", "...Doctor. You have a cleverer head than I took you for. Life, Doctor. 'The blood is the life.' I am a collector of it, in a small way. You see how the system works. I am not at all mad; I am merely early.",
              do=[dict(set=P + "renfield_understood"), dict(journal=P + "j_theory")], next="theory3"),
    theory3=N(S, "I write that down, in the ledger, in my own hand: 'Zoophagous mania, systematised; the patient believes life may be taken in by eating living things; progression from small to large.' It is a good case. It is a very bad case. I wonder what he is waiting for, that he must be early.", end=True),
)

DIALOGUE[P + "renfield_garden"] = D("n0",
    n0=N(S, "Renfield, hunched under the wall, eyes on the moon. I take a step and he turns his head, and for a moment I see the whole ladder of lives written on his face.",
         choices=[
             C("Mr. Renfield. You are not hungry. You are afraid of being too late.", "reason"),
             C("[Try to bring him down by force]", do=[dict(fight=P + "frenzy")]),
             C("[Back away]", end=True)]),
    reason=N("Renfield", "...Afraid? Yes. Of being late. Doctor, you are the first who has ever said so. I thought there was time. I kept the flies, and the spiders, and now the wall is so high. Something is coming. Something is coming and I should like to be tidy, if it comes.",
             next="reason2"),
    reason2=N(S, "'Come in out of the dew, Mr. Renfield. Number Twelve is warm, and the sugar is still there. We shall be tidy together.' He lets me take his arm, and I walk him in across the gravel while the moon sets behind Carfax.",
              do=[dict(set=P + "renfield_calm"), dict(set=P + "calm_by_reason"), dict(journal=P + "j_renfield_night")], end=True),
)

DIALOGUE[P + "renfield_calmed"] = D("n0",
    n0=N("Renfield", "Doctor. Forgive me. I was not myself, which is perhaps a mercy. I should like the sugar, in the morning.",
         choices=[C("You shall have it.", "ok", do=[dict(set=P + "renfield_settled")]), C("[Leave him to rest]", end=True)]),
    ok=N("Renfield", "And Doctor: I was truthful, about being early. Be a little early yourself.", end=True),
)

# --------------------------------------------------------------------------------------------------------------------
# items, journal
# --------------------------------------------------------------------------------------------------------------------
ITEMS = {
    P + "ward_key": dict(name="Ward key", asset="key", variant="gold", desc="The small iron key to the patients' ward."),
    P + "clock_key": dict(name="Clock-winding key", asset="key", variant="gold", desc="Mr. Pym's winding key. He wants it back."),
    P + "dispensary_key": dict(name="Dispensary key", asset="key", variant="gold", desc="Kept by Hennessey in the one place nobody would look."),
    P + "spare_key": dict(name="Spare dispensary key", asset="key", variant="gold", desc="Hennessey's spare, hidden where a patient would not look."),
    P + "blank_cylinder": dict(name="Blank wax cylinder", asset="candle", variant="white", desc="A smooth cylinder of wax for the phonograph."),
    P + "cylinder": dict(name="Seward's phonograph cylinder", asset="candle", variant="white", desc="A wax cylinder: the doctor's voice on the night that Purfleet went wrong."),
    P + "blanket": dict(name="Grey blanket", asset="rug", variant="cream", desc="Dry grey wool."),
    P + "wet_blanket": dict(name="Sodden blanket", asset="rug", variant="blue", desc="Soaked, heavy, ready to smother a fire."),
    P + "draught": dict(name="Measured draught", asset="bottle", variant="amber", desc="Twenty grains of chloral in a glass of water. Neither too weak nor too strong."),
    P + "forged_slip": dict(name="Forged prescription", asset="book", variant="leather", desc="A slip for sixty grains of morphia, in a forged hand, in violet ink."),
}

JOURNAL = {
    P + "j_sleepless": dict(title="25 May. Three nights", source=J, text="Three nights without sleep. Lucy Westenra refused me at Hillingham, with great kindness, and I have gone on doctoring as if the thing had not happened. I shall find the ward key, make my rounds and try to tire myself properly. Chloral, in the right measure, will do the rest."),
    P + "j_hillingham": dict(title="Lucy's note", source=J, text="I keep her note, though a doctor should know better. 'I am promised, in my heart, to another.' She was gentle, and clear, and right. I said I understood, and I did. It is the understanding that keeps me awake."),
    P + "j_grief": dict(title="Dictated to the phonograph", source=J, text="I spoke my grief aloud to the cylinder, and it sounded smaller than it felt. I shall not blame Lucy, nor Arthur, nor myself. I shall be a better doctor for it, if I am not a worse man."),
    P + "j_dose": dict(title="Van Helsing on the chloral", source="Letter from Amsterdam", text="Fifteen grains for a woman or a frail man; twenty for a strong man in his full strength; never more than thirty; sixty is a funeral. Weigh twice. Renfield is fourteen stone and in his strength: twenty grains, witnessed."),
    P + "j_open_mind": dict(title="Van Helsing on doubt", source="Letter from Amsterdam", text="'Believe nothing because I say it; doubt nothing because you have not seen it. Write it all down, and then look at what is written.' He wrote this to me about a case of fever. I find it applies to nearly everything."),
    P + "j_debt": dict(title="What I owe him", source=J, text="That winter I was ill, and Van Helsing sat three nights with me when he could have been abed. He says I owe him nothing but to be, to some other sleepless fool, what he was to me. I shall try. I do not yet know how."),
    P + "j_pym": dict(title="Mr. Pym's clock", source=J, text="The ward clock stopped at ten past three the night Mrs. Pym died, and her husband has let no one touch it since. Hennessey says that if I name the hour, the old man may give me the winding key. I think I understand the lock he means."),
    P + "j_greer": dict(title="Greer on fire", source=J, text="Old Greer, mate of the Lizzie out of Sunderland: never water on a spirit fire, since the spirit floats and spreads. Wet the blanket, drop it on, and lean. A mad sailor's memory is better than my own on the subject."),
    P + "j_clock": dict(title="The clock wound", source=J, text="Pym's clock ticks again, and the dispensary key hung behind it on a nail where Hennessey, wisely, hid it. Pym watched me with the face of a man receiving a verdict. I think it was a good one."),
    P + "j_vane": dict(title="Miss Vane's visitor", source=J, text="Miss Vane, who writes to a man dead in India, notes that a boy with violet-stained fingers sits in the dispensary at night practising a signature on the backs of old labels. She thinks it a love-letter. I wonder who is being courted."),
    P + "j_hennessey_mark": dict(title="Hennessey cannot write", source=J, text="Hennessey signs with a mark, being no scholar. It had not occurred to me in three years. A man who cannot write cannot forge, so I may strike one name from any list. I feel foolish for having needed to ask."),
    P + "j_cell": dict(title="Room 12", source=J, text="Renfield's room, as I always find it: the cot made tight, the sugar in lines on the saucer, the jar of flies on the sill. I have read his ledger a dozen times, but I have never read it as a series, and Van Helsing would say that is the whole of the art."),
    P + "j_flies": dict(title="Renfield: the flies", source="Hennessey's diet ledger", text="Flies caught on sugar, kept in a jar 'to hold the lives'. For a fortnight he eats none. In the third week he begins, and calls them quite delicious, and 'so full of life'."),
    P + "j_spiders": dict(title="Renfield: the spiders", source="Hennessey's diet ledger", text="He feeds the flies to spiders, and then eats the spiders. 'One spider is worth a hundred flies, for the life in it.' The system has a ladder in it; I should have seen that sooner."),
    P + "j_sparrows": dict(title="Renfield: the sparrows", source="Hennessey's diet ledger", text="He tamed a sparrow, wanted a cat to eat the sparrows, and kept a heap of feathers for his pains. 'The spider's life is little, and the sparrow's is more.' The ladder climbs, as I thought."),
    P + "j_cat": dict(title="Renfield: the kitten", source="Hennessey's diet ledger", text="The housemaid's kitten went into Room 12 on Tuesday and came out on Wednesday as a smear of fur. He was ill afterwards, as if from grief. I have written nothing under it. I did not need to."),
    P + "j_theory": dict(title="Renfield's theory", source=J, text="Zoophagous mania, systematised: the patient believes life may be gathered by eating living things, in ascending order. 'The blood is the life.' He says he is not mad, merely early. I wonder what he is early for."),
    P + "j_draught": dict(title="The twenty-grain draught", source=J, text="Twenty grains of chloral for a strong man, weighed twice and witnessed by the register. A bottle I hope never to use. The house may break, but it will be broken by the book."),
    P + "j_night": dict(title="Two in the morning", source=J, text="Smoke under the dispensary door, Room 12 standing open, and a lad crying in the ward. Three things at once, and a doctor who has not slept in three days. Good. A man with nothing to lose makes a cool physician."),
    P + "j_fire": dict(title="The fire in the dispensary", source=J, text="Old Greer told me, with the memory of forty years, never to put water on a spirit fire. I smothered it with a soaked blanket, and the chloral was saved. I must remember to thank a mad sailor in the morning."),
    P + "j_slip": dict(title="A forged prescription", source=J, text="Sixty grains of morphia, in my name, in my hand, forged beautifully, in violet copying ink. Hennessey cannot write. Miss Vane saw a lad with violet fingers practise my S. I think I know the signatory, and it breaks my heart."),
    P + "j_pettit": dict(title="Pettit", source=J, text="He did it for his mother, in Barking, in pain. I could report him, and the law would be on my side. I could help him, and the law would not. I choose, and write the choice in the book, so that I cannot pretend I did not."),
    P + "j_renfield_night": dict(title="Renfield at the wall", source=J, text="I found him in the garden under the Carfax wall, staring at the moon. I did not need force. Judgment, a measure of medicine and a steady voice did it. He said something is coming, and he would like to be tidy. I wrote it down."),
    P + "j_end": dict(title="The twenty-sixth of May", source=J, text="A night in which three things went wrong and none was the worst. I used judgment where I might have used force, medicine where I might have used a stick, and nerve where I might have run. I shall write to Van Helsing. I think I may sleep."),
}

# --------------------------------------------------------------------------------------------------------------------
# combat (optional): Renfield, in a frenzy, in the garden
# --------------------------------------------------------------------------------------------------------------------
ENCOUNTERS_EXTRA = {
    P + "frenzy": dict(name="Renfield at the garden wall", time="night", enemies=["renfield"], flee_ok=True,
                       intro="He springs at me from the shadow of the wall, with a madman's strength, snarling about lives and masters.",
                       win="Hennessey and I pin him until he is quiet.", location=P + "garden"),
}
_calm = [{"set": P + "renfield_calm"}, {"set": P + "calm_by_force"}, {"journal": P + "j_renfield_night"}]
ENCOUNTER_HOOKS = {
    P + "frenzy": dict(
        on_win=_calm + [say("He lies quiet at last, panting, and I have the cut on my hand to remember it by. I should have used the draught.")],
        on_lose=_calm + [say("I come to on the gravel with a bruised head. Hennessey and two attendants have Renfield between them, and by the time they have carried him in he is quiet.")],
        on_flee=_calm + [say("I get a dozen yards away. Hennessey and two attendants arrive, and Renfield is quieted in the end by sheer weariness.")]),
}

# --------------------------------------------------------------------------------------------------------------------
# seed variation
# --------------------------------------------------------------------------------------------------------------------
PALETTES = {
    P + "study": [dict(wall="plaster_dirty", floor="planks", wood="ebony", cloth="green"), dict(wall="stone_grey", floor="planks", wood="dark", cloth="red"),
                  dict(wall="plaster", floor="planks", wood="oak", cloth="blue")],
    P + "ward": [dict(wall="plaster", floor="planks", wood="dark", cloth="blue"), dict(wall="plaster_dirty", floor="planks", wood="oak", cloth="green")],
    P + "cell": [dict(wall="plaster_dirty", floor="planks", wood="pale", cloth="black"), dict(wall="stone_grey", floor="planks", wood="dark", cloth="black")],
    P + "dispensary": [dict(wall="stone_grey", floor="planks", wood="pale", cloth="cream"), dict(wall="plaster", floor="cobble", wood="ebony", cloth="cream")],
    P + "records": [dict(wall="plaster_dirty", floor="planks", wood="dark", cloth="red"), dict(wall="plaster", floor="planks", wood="oak", cloth="green")],
    P + "garden": [dict(floor="dirt"), dict(floor="grass")],
}

PLACEMENTS = {
    P + "ward_key": [
        dict(prop=P + "s_desk", text="Under the blotter, a small iron key on a loop of tape, labelled 'WARD' in my own hand.", hint="The blotter lies crooked on the desk."),
        dict(prop=P + "s_shelf", text="Behind Maudsley, a small iron key on a loop of tape: 'WARD'.", hint="One volume of Maudsley sits out of line."),
        dict(prop=P + "s_fire", text="On the mantel, behind the stopped clock, the small iron ward key.", hint="The mantel is dusted everywhere except one corner."),
    ],
    P + "spare_key": [
        dict(prop=P + "w_bed1", text="Under the folded blanket, a brass spare key tagged 'DISP.' in Hennessey's laboured capitals.", hint="The blanket on this bed is folded too neatly."),
        dict(prop=P + "w_bench", text="Pushed down the back of the window bench, a brass key tagged 'DISP.'", hint="The cushion of the bench has been disturbed."),
        dict(prop=P + "w_bed2", text="Tucked under the pillow, a brass key tagged 'DISP.'", hint="The pillow on this bed is lumpy."),
    ],
    P + "blank_cylinder": [
        dict(prop=P + "r_chest", text="In the old chest, wrapped in tissue, a blank wax cylinder in its cardboard tube.", hint="The old chest has been opened recently; the lid does not quite sit."),
        dict(prop=P + "r_desk", text="In the desk drawer, among the pens, a blank wax cylinder in its tube.", hint="The drawer of the copying desk is not quite closed."),
        dict(prop=P + "r_shelf", text="Behind the case-books, a cardboard tube: a blank cylinder, still smelling of new wax.", hint="Something rattles faintly behind the case-books."),
    ],
}

GATES = {
    P + "w_door_disp": [
        dict(cond="has:" + P + "dispensary_key", fail="Locked. Hennessey says the key is 'kept safe', which is no answer.", needs=P + "dispensary_key"),
        dict(cond="has:" + P + "spare_key", fail="Locked. There must be a spare somewhere on the ward; Hennessey is not the only one who hides things.", needs=P + "spare_key"),
    ],
}

# --------------------------------------------------------------------------------------------------------------------
# NPC looks
# --------------------------------------------------------------------------------------------------------------------
ASSETS = []
VARIANTS = {
    "human_peasant_m": {
        P + "hennessey": human_colors(skin=T("skin", "#d9b08c"), hair=T("hair", "#3a3a3a"), top=T("cloth", "#e8e4dc"), bottom=T("wool", "#2a2e36")),
        P + "pym": human_colors(skin=T("skin", "#d6c8b8"), hair=T("hair", "#c8c8c8"), top=T("wool", "#6a6e72"), bottom=T("wool", "#3a3a3a")),
        P + "greer": human_colors(skin=T("skin", "#c7956e"), hair=T("hair", "#9a9a9a"), top=T("wool", "#1f2c44"), bottom=T("wool", "#2a2e36")),
        P + "pettit": human_colors(skin=T("skin", "#e0b896"), hair=T("hair", "#3a2a1a"), top=T("cloth", "#8a8a96"), bottom=T("wool", "#1a2338")),
    },
    "human_peasant_f": {
        P + "vane": human_colors(skin=T("skin", "#e8c3a0"), hair=T("hair", "#9a9a9a"), top=T("wool", "#3a3e48"), bottom=T("wool", "#3a3e48")),
        P + "dowling": human_colors(skin=T("skin", "#e0b896"), hair=T("hair", "#5a4a3a"), top=T("cloth", "#e8e4dc"), bottom=T("wool", "#e8e4dc")),
    },
}
