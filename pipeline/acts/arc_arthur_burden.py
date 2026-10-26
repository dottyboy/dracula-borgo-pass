"""PERSONAL ARC - "The Lord's Burden" (Arthur Holmwood, later Lord Godalming).  Ids prefixed arthur_burden_."""
from dsl import *

F = "arthur_burden_"


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


def IF(cond, **kw):
    return {"if": cond, **kw}


def say(t):
    return {"say": t}


def P(s, *a, **k):
    return prop(F + s, *a, **k)


def NP(s, *a, **k):
    return npc(F + s, *a, **k)


ARC = dict(
    id="arthur_burden", title="The Lord's Burden", member="arthur", portrait="arthur",
    blurb="Arthur Holmwood nurses a dying father, wins Lucy Westenra's hand, and inherits a title with a secret. Will he keep the comfortable lie, or tell the hard truth?",
    unlock="roster:arthur", unlock_text="Meet Arthur Holmwood (Act II).", after_credits=False,
    start=dict(location=F + "sickroom", protagonist="arthur", party=["arthur"], items={}, flags=[]),
    exit_to="ARC_END",
    rewards=[dict(give="sword_cane"), dict(give="lords_riding_coat"), dict(give="silver")] * 5 + [dict(give=F + "signet"), dict(stat=dict(member="arthur", nerve=4, hp=3, dmg=1)),
                                         dict(set=F + "lords_burden_done")],
    rewards_text="Godalming's signet ring, five silver coins; +4 Nerve, +3 HP and +1 damage for Arthur Gear: a sword-cane and a riding coat.",
)

LOCATIONS = [
    dict(id=F + "sickroom", name="The Lord's chamber, The Ring", desc="The great bed with its faded hangings. The fire is kept high, and the whole room smells of camphor and old paper.", date="Early summer, 1888"),
    dict(id=F + "hall", name="The hall, The Ring", desc="Black oak, stag's heads and portraits of Holmwoods who all look as if they had been told bad news.", date="The Ring"),
    dict(id=F + "grounds", name="The grounds of The Ring", desc="Lawn, limes and the grey flank of the house. The chapel roof shows above the yews, and the Home Wood darkens the hill.", date="The Ring"),
    dict(id=F + "garden", name="The garden at Hillingham", desc="Lucy's mother's garden: roses, a lawn that has never seen a weed, and Lucy herself under the arbour.", date="June"),
    dict(id=F + "summerhouse", name="The summer-house, Hillingham", desc="A little octagon of white wood and glass at the garden's end. We have taken our tea here for three weeks.", date="July"),
    dict(id=F + "office", name="The estate office", desc="Ledgers to the ceiling, and a stove which has not been lit since my father last came down these stairs.", date="After the funeral"),
    dict(id=F + "village", name="The village green", desc="Cottages of old brick round a pond. The tenants wait outside the Holmwood Arms and do not take off their hats.", date="After the funeral"),
    dict(id=F + "wood", name="The Home Wood, by night", desc="Black oaks and bracken. Somewhere ahead, a lantern is shuttered, and a wire snare sings in the wind.", date="After the funeral, night"),
    dict(id=F + "chapel", name="The family chapel", desc="Cold stone, a worn altar and the brasses of my ancestors in the floor. A single bell hangs in the little tower.", date="After the funeral"),
    dict(id=F + "vault", name="The Holmwood vault", desc="Steps down into the earth. The air is dry, the lamp-flames lean away from the farther dark.", date="After the funeral"),
    dict(id=F + "muniment", name="The muniment room", desc="Iron-bound chests of deeds and a desk with a green lamp. The window has been bricked up for a century.", date="After the funeral"),
]

LOC_DATA = {}

# ----------------------------------------------------------------------------------------------------------- sickroom
LOC_DATA[F + "sickroom"] = dict(
    cells=[2, 2], interior=True, wall="plaster_dirty", floor="planks", ambient=AMBIENT["candle_interior"], camera=cam([2, 2]),
    lights=lights_warm([2, 2]),
    walls=dict(north=["wall_4", "wall_window_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[2.5, 1.5], spawns={F + "hall": [2.8, 2.0]},
    props=[
        P("bed", "bed", "red", -1.8, -2.4, name="The Lord's bed", radius=1.2, look="The four-poster in which three Lords of Godalming have died. My father lies small and grey among the pillows."),
        P("desk", "table", "dark", 2.2, -3.0, name="The Lord's writing-desk", radius=0.9,
          look="A lacquered desk with a brass-bound drawer. The drawer is locked; he has kept the key from me all my life.",
          use_item={F + "desk_key": [say("The key turns stiffly. Inside lie a folded letter in my father's hand and a small velvet box."),
                                     {"give": F + "intro_letter"}, {"give": F + "ring"}, {"set": F + "desk_open"}]},
          use_fail="Nothing here fits the drawer. I want its key."),
        P("bedside", "table", "oak", -3.0, -0.4, scale=0.6, name="Bedside table", radius=0.5,
          look="Physic-bottles, a water-glass, a Bible. The spectacles have been wanted for two days and found by nobody."),
        P("specs", "key", "gold", -3.0, -0.4, y=0.55, scale=0.6, name="Father's spectacles", radius=0.2,
          look="Gold-rimmed spectacles, folded under the Bible where the nurse has laid them.",
          take=F + "spectacles", take_text="I take his spectacles. He will want them to read any message.", give_once=True),
        P("cabinet", "chest", "dark", 3.1, 0.2, rot=-90, name="Medicine cabinet", radius=0.6,
          look="Dr. Lenox's travelling cabinet: lint, lancets and a cordial in a green bottle.",
          take=F + "cordial", take_text="I take the green bottle of cordial. 'For the evening dose', says the label.", give_once=True),
        P("fire", "fireplace", "stone_dark", -3.4, 2.2, rot=90, name="Fire", radius=0.9, look="Kept high all summer. My father says the cold is waiting for him in the corridor."),
        P("chair", "chair", "green", -0.8, -0.8, rot=90, name="Bedside chair", radius=0.4, look="The chair in which I have sat for eleven nights."),
        P("books", "bookshelf", "dark", 3.3, -1.6, rot=-90, name="Bookcase", radius=0.7, look="Burke's Peerage, Debrett and a long row of Hansard. A family that read about itself."),
        P("rug", "rug", "red", 0.4, 0.8, radius=0.1),
        P("candle", "candelabra", "default", 2.2, -3.0, y=0.8, name="Candelabra", radius=0.2, look="Three candles, and the fourth socket empty. Nobody has had the heart to replace it."),
        P("sconce", "sconce", "default", 3.7, -2.8, y=1.5, rot=-90, radius=0.1),
        P("door", "door", "dark", 3.8, 2.0, rot=-90, name="Door to the hall", radius=0.6, look="To the stairs and the hall.", go=F + "hall"),
    ],
    npcs=[
        NP("lord", "human_seward", "doctor", -0.4, -2.2, rot=-90, name="Lord Godalming", look="My father, the old Lord, propped against his pillows. Time has cut him down to bone, but the eyes are still the eyes of a man who rules a county.", talk=F + "lord_talk"),
        NP("doctor", "human_seward", "doctor", 1.0, 1.2, rot=180, name="Dr. Lenox", look="The family physician, with a face trained to give no news.", talk=F + "doctor_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_sickroom")])],
)

# ----------------------------------------------------------------------------------------------------------- hall
LOC_DATA[F + "hall"] = dict(
    cells=[3, 2], interior=True, wall="stone_dark", floor="planks", ambient=AMBIENT["candle_interior"], camera=cam([3, 2]),
    lights=lights_warm([3, 2], energy=2.8),
    walls=dict(north=["wall_4", "wall_door_4", "wall_window_4"], west=["wall_door_4", "wall_4"], east=["wall_door_4", "wall_door_4"]),
    spawn=[3.0, 1.5], spawns={F + "sickroom": [-4.4, -2.0], F + "office": [4.4, -2.0], F + "grounds": [4.6, 2.0], F + "muniment": [0, -2.4], F + "summerhouse": [3.0, 1.5]},
    props=[
        P("table", "table_long", "ebony", 0.2, 0.4, name="Long table", radius=1.6, look="Thirty could dine here. Lately it has held telegrams, black-edged cards and bills."),
        P("salver", "chest", "pale", 0.2, 0.4, y=0.8, scale=0.25, name="Silver salver", radius=0.3,
          look="A salver with two letters on it and a pink telegram.",
          take=F + "telegram", take_text="From Mrs. Westenra: 'Lucy begs you will come to Hillingham when your father is easier. Do not stay away for fear of us.'", give_once=True),
        P("bust", "bust", "plaster", -4.6, -3.2, name="Bust of the first Lord", radius=0.5, look="Sir Hugh Holmwood in plaster, with the nose broken in some forgotten game of ours."),
        P("shelf", "bookshelf", "dark", 5.0, -3.4, name="Bookcase", radius=0.7, look="Hunting-books, county histories and a red Bradshaw."),
        P("chest", "chest", "oak", -5.2, 0.6, rot=90, name="Hall chest", radius=0.6, look="Rugs and old ulsters. It smells of dogs."),
        P("fire", "fireplace", "stone_dark", -2.5, -3.4, name="Great hearth", radius=1.0, look="Enough hearth to roast an ox, now holding a single log."),
        P("chair1", "chair", "black", 3.4, 0.2, rot=-90, name="High-backed chair", radius=0.4, look="Carved with the Holmwood arms: three rings on a field of grey."),
        P("chair2", "chair", "black", -3.2, 1.8, rot=90, name="High-backed chair", radius=0.4, look="Nobody sits in this one. It was my grandfather's."),
        P("rug", "rug", "red", 0.0, 2.2, radius=0.1),
        P("candelabra", "candelabra", "default", 0.2, 0.4, y=0.8, scale=0.8, radius=0.2),
        P("sconce1", "sconce", "default", -5.7, 1.2, y=1.5, rot=90, radius=0.1),
        P("sconce2", "sconce", "default", 5.7, 1.0, y=1.5, rot=-90, radius=0.1),
        P("d_sick", "door", "dark", -5.8, -2.0, rot=90, name="Stairs to the Lord's chamber", radius=0.6, look="The way up to my father's room.", go=F + "sickroom", cond="!" + F + "lord_dead"),
        P("d_office", "door", "oak", 5.8, -2.0, rot=-90, name="Estate office", radius=0.6, look="The steward's office. Brass plate: 'W. Wilkes'.", go=F + "office"),
        P("d_out", "door_big", "oak", 5.8, 2.0, rot=-90, name="Front door", radius=0.7, look="The front door, and the lime avenue beyond.", go=F + "grounds"),
        P("d_muniment", "door", "ebony", 0.0, -3.8, name="Muniment-room door", radius=0.6,
          look="Iron-bound, with a lock of three wards and a recess the shape of a seal. Only the Lord opens it.",
          go=F + "muniment", go_cond="has:" + F + "muniment_key&has:" + F + "signet",
          go_fail="Locked. It wants a key, and the recess beside the keyhole wants a seal pressed into it, my father's signet."),
    ],
    npcs=[
        NP("bates", "human_coachman", "driver", -3.8, 2.8, rot=90, name="Bates, the butler", look="Seventy years in service. He has buried one Lord already and is working hard at not burying a second.", talk=F + "bates_talk"),
        NP("pennefather", "human_harker", "harker", 2.8, -1.4, rot=180, name="Mr. Pennefather, solicitor", cond=F + "lord_dead",
           look="A thin gentleman in black, with a document-case held against his chest like a shield.", talk=F + "pennefather_talk"),
        NP("crowle", "human_quincey", "texan", -1.8, 2.4, rot=0, name="Mr. Crowle, banker", cond=F + "lord_dead",
           look="Crowle of Crowle & Aske, round, rosy and kind. Everything about him is soft except the way he reads other people's faces.", talk=F + "crowle_talk"),
    ],
    on_enter=[IF(F + "lord_dead", once=True, do=[dict(journal=F + "j_death")])],
)

# ----------------------------------------------------------------------------------------------------------- grounds
LOC_DATA[F + "grounds"] = dict(
    cells=[3, 3], interior=False, wall="stone_dark", floor="grass", ambient=AMBIENT["day_exterior"], camera=cam([3, 3]), lights=lights_day(3.0),
    scatter=dict(asset="pine", variant="green", count=22, seed=5, avoid=[[-7, -7, 7, 7]]),
    spawn=[5.0, 0.0], spawns={F + "hall": [4.0, -3.0], F + "chapel": [-4.0, -2.0], F + "village": [5.0, 3.0], F + "wood": [-2.0, 3.0], F + "garden": [4.0, 3.0], F + "summerhouse": [4.0, 3.0]},
    props=[
        P("house", "castle_keep", "stone_grey", 3.4, -6.8, scale=0.7, name="The Ring", radius=1.5, look="Grey, gabled, very old. A Holmwood has lived here since the Wars of the Roses, and not one of them has lived here cheaply."),
        P("d_house", "door_big", "oak", 5.0, -3.4, name="Front door", radius=0.7, look="Back into the hall.", go=F + "hall"),
        P("carriage", "carriage", "dark", 5.2, 2.6, rot=-70, name="Carriage to the station", radius=1.2,
          look="The brougham stands waiting. I may go to Hillingham when I hold the telegram, my father's blessing and a ring.",
          go=F + "garden", go_cond="has:" + F + "telegram&has:" + F + "ring&has:" + F + "intro_letter&" + F + "blessed",
          go_fail="Not yet. I will not leave until he has blessed this, and until I have what I need to say it: the telegram, my mother's ring and my father's letter.",
          cond="!" + F + "lord_dead"),
        P("sign_village", "signpost", "oak", 4.4, 4.2, rot=-20, name="Path to the village", radius=0.3, look="'Ring Green, half a mile.' Someone has scratched 'and a bad road' underneath.", go=F + "village", cond=F + "lord_dead"),
        P("arch_chapel", "arch", "stone_mossy", -6.2, -2.0, rot=90, name="Yew walk to the chapel", radius=0.8, look="Yews clipped to black pillars, and the chapel beyond.", go=F + "chapel", cond=F + "lord_dead"),
        P("gate_wood", "arch", "stone_dark", -2.0, 5.6, name="Gate to the Home Wood", radius=0.8, look="The Home Wood gate hangs open. It is never open.", go=F + "wood", cond=F + "lord_dead"),
        P("lime1", "pine_small", "green", -3.0, 0.0, name="Lime", radius=0.4, look="My grandfather planted the avenue. I climbed this one at nine and broke my collar-bone."),
        P("bench", "bench", "oak", 0.5, 1.2, name="Garden bench", radius=0.9, look="Lucy's letter lay open on this bench the day I read it twice."),
        P("lamp", "lantern", "default", 1.8, -2.8, name="Lantern", radius=0.3, look="Unlit by day."),
        P("rock", "rock", "mossy", -4.8, 3.4, name=None, radius=0.5),
        P("fence1", "fence", "default", 0.0, 5.0, radius=0.3),
        P("fence2", "fence", "default", 4.0, 5.0, radius=0.3),
    ],
    npcs=[
        NP("groom", "human_peasant_m", "villager", 3.2, 1.6, rot=90, name="Tom the groom", cond="!" + F + "lord_dead",
           look="He has had the horses harnessed since breakfast.", talk=F + "groom_talk"),
        NP("gardener", "human_peasant_m", "innkeeper", -3.4, 3.0, rot=0, name="Old Pike, the gardener", cond=F + "lord_dead",
           look="Leans on his rake and watches the Home Wood. He has not raked anything in an hour.", talk=F + "pike_talk"),
    ],
)

# ----------------------------------------------------------------------------------------------------------- garden
LOC_DATA[F + "garden"] = dict(
    cells=[3, 2], interior=False, wall="plaster", floor="grass", ambient=AMBIENT["day_exterior"], camera=cam([3, 2]), lights=lights_day(3.4),
    scatter=dict(asset="pine_small", variant="green", count=14, seed=9, avoid=[[-7, -5, 7, 5]]),
    spawn=[4.0, 2.4], spawns={F + "summerhouse": [-4.4, -2.0], F + "grounds": [4.0, 2.4]},
    props=[
        P("arbour", "arch", "plaster", -2.4, -3.0, name="Rose arbour", radius=0.8,
          look="Lucy's arbour, thick with roses. The wild one at the foot has opened first, as she says it always does.",
          take="wild_rose", take_text="I pick the wild rose from the arbour's foot. The thorn takes a drop of my blood, and I do not mind.", give_once=True),
        P("table", "table", "pale", 1.5, -0.5, name="Tea-table", radius=0.9, look="Lace cloth, a pot of Darjeeling and a plate of what Lucy calls seed-cake and Mrs. Westenra calls cake."),
        P("chair1", "chair", "blue", 0.2, -0.5, rot=90, name="Garden chair", radius=0.4, look="Mrs. Westenra's. She likes it with its back to the wind."),
        P("chair2", "chair", "blue", 2.9, -0.5, rot=-90, name="Garden chair", radius=0.4, look="Lucy's."),
        P("bench", "bench", "pale", -4.6, 1.0, rot=90, name="Stone bench", radius=0.9, look="A bench for reading and for pretending to read."),
        P("urn", "column_short", "plaster", 4.4, -2.8, name="Urn on a plinth", radius=0.4, look="Full of geraniums, in military ranks."),
        P("vase", "bottle", "green", 1.5, -0.5, y=0.8, name="Vase of roses", radius=0.2, look="A dozen pale roses, nearly as pale as Lucy."),
        P("fence1", "fence", "default", -4.0, 3.8, radius=0.3),
        P("fence2", "fence", "default", 0.0, 3.8, radius=0.3),
        P("fence3", "fence", "default", 4.0, 3.8, radius=0.3),
        P("house", "tower", "plaster", 3.0, -6.6, scale=0.6, name="Hillingham", radius=1.2, look="A white house, a long lawn, and every window open."),
        P("d_summer", "door", "pale", -5.5, -2.0, rot=90, name="Path to the summer-house", radius=0.6, look="A gravel walk between lavender, to the little white pavilion.", go=F + "summerhouse", go_cond=F + "engaged", go_fail="Not yet. I have something to ask first."),
    ],
    npcs=[
        NP("lucy", "human_lucy", "lucy", 1.6, 1.4, rot=180, name="Lucy Westenra", look="Lucy, in a white morning frock with her hair half down, laughing at something nobody has said.", talk=F + "lucy_talk"),
        NP("mrsw", "human_peasant_f", "innkeeper_wife", -0.8, -1.4, rot=-90, name="Mrs. Westenra", look="Lucy's mother, in grey silk, with a heart she cannot spare and a sharp eye for settlements.", talk=F + "mrsw_talk"),
        NP("quincey", "human_quincey", "texan", -3.4, 2.4, rot=45, name="Mr. Quincey Morris", look="Lanky, brown, easy. He was also going to ask. He has the grace of a man who knows.", talk=F + "quincey_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_hillingham")])],
)

# ----------------------------------------------------------------------------------------------------------- summerhouse
LOC_DATA[F + "summerhouse"] = dict(
    cells=[2, 2], interior=True, wall="plaster", floor="planks", ambient=AMBIENT["warm_day_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2], energy=2.8),
    walls=dict(north=["wall_window_4", "wall_window_4"], west=["wall_door_4", "wall_window_4"], east=["wall_window_4", "wall_4"]),
    spawn=[-2.4, -1.0], spawns={F + "garden": [-2.8, -2.0]},
    props=[
        P("mallets", "hammer", "default", -2.0, 1.4, name="Croquet mallets", radius=0.4, look="Lucy cheats at croquet and loses with enormous dignity.",
          set=F + "mem_a", set_text="We played until dusk, Lucy and I and Quincey, and she knocked my ball into the pond and called it strategy. I could not stop laughing. I had not laughed in a year."),
        P("music", "chest", "pale", 2.8, -2.6, rot=-90, name="Lucy's music-box", radius=0.5, look="Her old music-box. It plays one waltz and a half.",
          set=F + "mem_b", set_text="She wound it and we danced three turns on the boards of the summer-house with no one watching. I trod on her hem twice, and she forgave me twice."),
        P("poems", "book", "red", 0.2, -0.6, y=0.8, name="Lucy's poetry book", radius=0.2, look="Tennyson, much underlined.",
          set=F + "mem_c", set_text="She read me 'Maud' aloud, and then looked up and said I was the only person who did not mind a bad reader. We read until the lamp was lit."),
        P("table", "table", "pale", 0.2, -0.6, name="Round table", radius=0.9, look="Two cups, always, and a saucer of lemon."),
        P("chair1", "chair", "blue", -1.0, -0.6, rot=90, radius=0.4, name="Wicker chair", look="Mine, by long custom."),
        P("chair2", "chair", "blue", 1.4, -0.6, rot=-90, radius=0.4, name="Wicker chair", look="Hers, by every custom."),
        P("rug", "rug", "cream", 0.2, 1.8, radius=0.1),
        P("lamp", "lantern", "default", 2.2, 2.0, name="Summer lantern", radius=0.3, look="Paper-shaded, lit at dusk."),
        P("d_garden", "door", "pale", -3.8, -2.0, rot=90, name="Door to the garden", radius=0.6, look="Back to the lawn.", go=F + "garden"),
    ],
    npcs=[
        NP("lucy", "human_lucy", "lucy", 1.8, 0.5, rot=-90, name="Lucy", look="Lucy, engaged to be married and shining with it.", talk=F + "lucy_summer_talk"),
        NP("servant", "human_peasant_m", "villager", -1.0, 2.8, rot=0, name="Hillingham footman", cond=F + "mem_a&" + F + "mem_b&" + F + "mem_c",
           look="The footman, hat in hand, hesitating. He holds a yellow envelope.", talk=F + "footman_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_summer")])],
)

# ----------------------------------------------------------------------------------------------------------- office
LOC_DATA[F + "office"] = dict(
    cells=[2, 2], interior=True, wall="plaster_dirty", floor="planks", ambient=AMBIENT["candle_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2]),
    walls=dict(north=["wall_4", "wall_window_4"], west=["wall_door_4", "wall_4"], east=["wall_4", "wall_4"]),
    spawn=[-2.4, -1.0], spawns={F + "hall": [-2.8, -2.0]},
    props=[
        P("desk", "table", "oak", 1.8, -2.4, name="Steward's desk", radius=0.9, look="Blotter, seals, a bowl of wafers and a ledger held shut by a strap."),
        P("ledger", "book", "leather", 1.8, -2.4, y=0.8, name="Estate ledger", radius=0.2,
          look="The ledger of arrears. I open it where the strap has left a crease. Red ink, page after page.",
          take=F + "ledger", take_text="I take the ledger. The arrears column runs to four figures, then to five. Rents unpaid for three years; interest due to Crowle & Aske in a hand I do not know. Someone has been paying the tenants' debts out of borrowed money.", give_once=True),
        P("shelf1", "bookshelf", "dark", -3.3, -2.6, rot=90, name="Rent-rolls", radius=0.7, look="Rent-rolls back to the Restoration."),
        P("shelf2", "bookshelf", "pale", 3.4, 1.0, rot=-90, name="Estate maps", radius=0.7, look="Hand-coloured maps. The Home Wood is edged in red pencil with a question-mark."),
        P("stove", "fireplace", "soot", -3.4, 1.2, rot=90, name="Cold stove", radius=0.9, look="Cold. In July, that means money."),
        P("chair", "chair", "black", 1.8, -1.2, rot=180, name="Steward's chair", radius=0.4, look="Worn to the shape of one man's anxieties."),
        P("clock", "barrel", "oak", 3.2, -3.0, name="Parish barrel", radius=0.4, look="For the Harvest Home subscription. It rattles with very little."),
        P("rug", "rug", "black", 0.0, 1.0, radius=0.1),
        P("lamp", "lantern", "default", -1.4, -3.0, y=1.4, radius=0.2),
        P("d_hall", "door", "oak", -3.8, -2.0, rot=90, name="Door to the hall", radius=0.6, look="Back to the hall.", go=F + "hall"),
    ],
    npcs=[NP("wilkes", "human_peasant_m", "innkeeper", 0.2, -1.2, rot=90, name="Mr. Wilkes, steward", look="Grey, upright, thirty years a Holmwood servant. He has the face of a man holding a door shut with his back.", talk=F + "wilkes_talk")],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_office")])],
)

# ----------------------------------------------------------------------------------------------------------- village
LOC_DATA[F + "village"] = dict(
    cells=[3, 2], interior=False, wall="plaster", floor="grass", ambient=AMBIENT["day_exterior"], camera=cam([3, 2]), lights=lights_day(3.0),
    scatter=dict(asset="pine_small", variant="green", count=14, seed=13, avoid=[[-7, -5, 7, 5]]),
    spawn=[4.4, 2.4], spawns={F + "grounds": [4.4, 2.4]},
    props=[
        P("sign", "inn_sign", "oak", -2.4, -3.0, name="The Holmwood Arms", radius=0.5, look="Three rings on a swinging board, painted by someone who has never counted to three."),
        P("pump", "column_short", "stone_grey", 0.4, 0.0, name="Village pump", radius=0.4, look="The pump handle was a gift of my grandfather. It has not given water since."),
        P("barrel1", "barrel", "dark", -1.2, -3.4, name="Cider barrel", radius=0.4, look="The Arms' barrel, rolled out onto the green for the occasion. Nobody is drinking from it."),
        P("barrel2", "barrel", "oak", -0.4, -3.4, radius=0.4, name="Barrel", look="Water-butt."),
        P("cart", "carriage", "oak", 3.4, -2.6, rot=45, scale=0.7, name="Hay-cart", radius=1.0, look="A hay-cart with a broken axle. It has been broken since Lady Day."),
        P("bench", "bench", "dark", -4.4, 1.6, rot=90, name="Bench by the pond", radius=0.9, look="Where old men watch ducks and mutter about Lords."),
        P("lamp", "lantern", "default", 2.0, 1.4, name=None, radius=0.2),
        P("fence1", "fence", "default", -4.0, 3.8, radius=0.3),
        P("fence2", "fence", "default", 0.0, 3.8, radius=0.3),
        P("rock", "rock", "grey", 5.0, -0.6, radius=0.5),
        P("sign_back", "signpost", "oak", 5.6, 3.0, rot=-100, name="Road to the Ring", radius=0.3, look="'The Ring, half a mile.'", go=F + "grounds"),
    ],
    npcs=[
        NP("marsh", "human_peasant_m", "villager", 1.2, 1.4, rot=180, name="Gideon Marsh, tenant farmer", look="Spokesman of the tenants, because he is the only one who has never owed anyone a penny. Hat on, jaw set.", talk=F + "marsh_talk"),
        NP("wife", "human_peasant_f", "village_woman", -2.6, 1.6, rot=45, name="Mrs. Marsh", look="Arms folded over her apron, not unkindly.", talk=F + "marshwife_talk"),
        NP("miller", "human_peasant_m", "villager", 3.2, 0.6, rot=-90, name="The miller", look="White to the eyebrows. His mill-race was my grandfather's gift and my father's loan.", talk=F + "miller_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_village")])],
)

# ----------------------------------------------------------------------------------------------------------- wood
LOC_DATA[F + "wood"] = dict(
    cells=[3, 2], interior=False, wall="stone_dark", floor="dirt", ambient=AMBIENT["night_exterior"], camera=cam([3, 2]), lights=lights_moon(2.8), moon=dict(pos=[-6, 12, -8]),
    scatter=dict(asset="pine", variant="dark", count=34, seed=21, avoid=[[-6, -4, 6, 4]]),
    spawn=[0.0, 3.0], spawns={F + "grounds": [0.0, 3.0]},
    props=[
        P("snare", "fence", "default", -3.0, 0.4, name="Wire snare", radius=0.3, look="A brass wire loop pegged across a run. Not a rabbit-run; the loop is too big."),
        P("fire", "lantern", "default", 3.0, -1.4, name="Shuttered lantern", radius=0.3, look="Warm still. They did not go far."),
        P("log", "bench", "dark", 1.2, 0.6, rot=60, name="Fallen oak", radius=0.9, look="A felled oak, two hundred years old, sawn in the dark."),
        P("deer", "wolf", "grey", -4.0, -2.8, scale=0.4, name="Dead hind", radius=0.5, look="Stiff in the bracken. She was not killed by any poacher's wire; the throat has been torn out."),
        P("rock1", "rock", "mossy", 4.8, 2.0, radius=0.5),
        P("rock2", "rock_big", "dark", -4.8, 3.0, radius=0.9),
        P("dead", "deadtree", "grey", 0.0, -3.2, name="Dead beech", radius=0.4, look="Struck by lightning in my grandfather's time. Poachers hang their bags in it."),
        P("gate", "arch", "stone_dark", 0.0, 5.0, name="Back to the grounds", radius=0.8, look="The gate to the lawns.", go=F + "grounds"),
    ],
    npcs=[
        NP("hobbs", "human_peasant_m", "szgany", -1.6, 2.6, rot=45, name="Hobbs the keeper", look="The keeper, with a shotgun he is not sure he is allowed to use against another man.", talk=F + "hobbs_talk"),
        NP("poachers", "human_peasant_m", "szgany", 3.4, -2.6, rot=180, name="Poachers", look="Three shapes by a shuttered light: two men and something low at their feet that growls like a dog and is not.",
           fight=F + "poachers", cond="!won:" + F + "poachers"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_wood_in")])],
)

# ----------------------------------------------------------------------------------------------------------- chapel
LOC_DATA[F + "chapel"] = dict(
    cells=[2, 3], interior=True, wall="stone_dark", floor="stone_grey", ambient=AMBIENT["cold_interior"], camera=cam([2, 3]),
    lights=[dict(pos=[0, 2.6, -3], color="#a8b4ff", energy=1.6, range=12), dict(pos=[0, 1.9, 3], color="#ff9a40", energy=1.4, range=10)],
    walls=dict(north=["wall_window_4", "wall_window_4"], west=["wall_4", "wall_4", "wall_door_4"], east=["wall_4", "wall_4", "wall_4"]),
    spawn=[-2.4, 4.0], spawns={F + "vault": [2.0, -2.4], F + "grounds": [-2.8, 4.0]},
    props=[
        P("altar", "table", "ebony", 0.0, -4.4, name="Altar", radius=1.0, look="Plain stone and oak, with a cloth that was white once."),
        P("cross", "crucifix_big", "silver", 0.0, -4.6, y=0.8, name="Altar cross", radius=0.3, look="Silver, heavy, tarnished along the arms. Someone had polished it recently, I think."),
        P("brass1", "gravestone", "stone_grey", -2.6, -1.2, scale=0.7, name="Brass: Sir Hugh Holmwood", radius=0.5,
          look="'SIR HUGH HOLMWOOD, BUILDER OF THE RING, FELL AT EDGEHILL ON THE XXIII OF OCTOBER, 1642. HIS BODY WAS NOT RECOVERED.'"),
        P("brass2", "gravestone", "stone_grey", -2.6, 1.0, scale=0.7, name="Brass: his son's inscription", radius=0.5,
          look="'HERE, IN THE YEAR 1643, HIS SON FOUND HIM IN A FIELD AND BROUGHT HIM HOME. HERE HE RESTS.' The last two words have been rubbed bright by thumbs."),
        P("brass3", "gravestone", "stone_grey", 2.6, -1.2, scale=0.7, name="Brass: the title", radius=0.5,
          look="'IN THE YEAR 1688 THE LORDSHIP OF GODALMING WAS CONFERRED UPON THE HOUSE OF HOLMWOOD FOR SERVICES TO THE CROWN.'"),
        P("bench1", "bench", "dark", 2.4, 1.0, rot=90, name="Pew", radius=0.9, look="Worn smooth by four hundred years of Holmwood boredom."),
        P("bench2", "bench", "dark", -2.4, 3.2, rot=90, name="Pew", radius=0.9, look="My mother's. She sat here every Sunday of my childhood."),
        P("candle", "candelabra", "default", -1.2, -4.2, y=0.8, name="Candles", radius=0.2, look="Nobody lit them. I think."),
        P("bell", "column_short", "stone_dark", 3.2, 2.4, name="Bell-rope", radius=0.3, look="The rope hangs perfectly still. The bell rang once, a moment ago."),
        P("d_vault", "door_big", "ebony", 0.0, -5.8, name="Vault door", radius=0.8,
          look="A black door set in the north wall, cut with a name: 'HERE HE RESTS'. A dial of years is set into the lock. What year is a man's resting, if not his death?",
          talk=F + "vault_lock"),
        P("d_out", "door", "dark", -3.8, 4.0, rot=90, name="Door to the grounds", radius=0.6, look="The yew walk, and daylight.", go=F + "grounds"),
    ],
    npcs=[NP("nurse", "human_peasant_f", "village_woman", 0.6, 0.2, rot=180, name="A figure at the pew", look="A woman in grey, kneeling, so still she might have been carved.", talk=F + "nurse_talk")],
    on_enter=[dict(once=True, do=[say("A single stroke of the bell, from the tower, though the rope hangs still. At the far pew, someone kneels who was not there when I came in."), dict(journal=F + "j_chapel")])],
)
LOC_DATA[F + "chapel"]["walls"]["north"] = ["wall_4", "wall_4"]
# the vault door is in the north wall: make that piece a door piece
LOC_DATA[F + "chapel"]["walls"]["north"] = ["wall_door_4", "wall_4"]
LOC_DATA[F + "chapel"]["props"] = [p for p in LOC_DATA[F + "chapel"]["props"]]
for _p in LOC_DATA[F + "chapel"]["props"]:
    if _p["id"] == F + "d_vault":
        _p["pos"] = [-2.0, 0, -5.8 + 0.0]
    if _p["id"] == F + "altar":
        _p["pos"] = [1.4, 0, -4.4]
    if _p["id"] == F + "cross":
        _p["pos"] = [1.4, 0.8, -4.6]
    if _p["id"] == F + "candle":
        _p["pos"] = [2.4, 0.0, -3.4]
    if _p["id"] == F + "brass1":
        _p["pos"] = [-3.0, 0, 0.4]
    if _p["id"] == F + "brass2":
        _p["pos"] = [-3.0, 0, 2.0]

# ----------------------------------------------------------------------------------------------------------- vault
LOC_DATA[F + "vault"] = dict(
    cells=[2, 2], interior=True, wall="stone_tomb", floor="stone_dark", ambient=AMBIENT["crypt"], camera=cam([2, 2]),
    lights=[dict(pos=[0, 2.2, 0], color="#ffb060", energy=1.8, range=10)],
    walls=dict(north=["wall_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_4"]),
    spawn=[0, 2.5], spawns={F + "chapel": [0, 2.5]},
    props=[
        P("coffin", "coffin", "ebony", 0.0, -1.2, name="My father's coffin", radius=0.9,
          look="Black oak, brass handles, the arms of Godalming. The old man, at last, is perfectly still.", talk=F + "coffin_talk"),
        P("tomb1", "tomb", "stone_tomb", -2.4, -2.4, name="Tomb of an ancestor", radius=0.9, look="A Holmwood in stone armour, hands crossed. Someone has placed a pebble on his chest."),
        P("tomb2", "tomb", "stone_tomb", 2.4, -2.4, name="Tomb of an ancestor", radius=0.9, look="A Lady Godalming in stone lace, with a stone spaniel at her feet."),
        P("tomb3", "tomb", "stone_tomb", -2.4, 0.4, rot=90, name="Tomb of my mother", radius=0.9, look="'ELIZABETH, LADY GODALMING. SHE LOVED HER SON.' She is the only ancestor with a verb in her epitaph."),
        P("col1", "column_short", "stone_tomb", 2.6, 0.4, radius=0.3),
        P("lamp", "lantern", "default", 0.0, 1.0, name="Vault lamp", radius=0.3, look="The lamp I carried down. Its flame leans toward the farther wall, where there is no door."),
        P("steps", "stairs", "stone_dark", 0.0, 3.6, rot=180, name="Steps up to the chapel", radius=0.8, look="Up, to the chapel and the light.", go=F + "chapel"),
        P("sconce", "sconce", "default", 3.6, -1.2, y=1.5, rot=-90, radius=0.1),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_vault")])],
)

# ----------------------------------------------------------------------------------------------------------- muniment room
LOC_DATA[F + "muniment"] = dict(
    cells=[2, 2], interior=True, wall="stone_dark", floor="stone_grey", ambient=AMBIENT["candle_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2]),
    walls=dict(north=["wall_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[2.6, 2.0], spawns={F + "hall": [2.8, 2.0]},
    props=[
        P("desk", "table", "ebony", -0.8, -2.2, name="The Lord's muniment-desk", radius=0.9, look="A green-shaded lamp, a pen-tray, and two things laid squarely in the middle of the blotter by someone who meant them to be found."),
        P("mortgage", "book", "red", -1.4, -2.2, y=0.8, name="Deed of mortgage", radius=0.2,
          look="A long deed with three red seals: the Ring, the Home Farm and the Home Wood pledged to Crowle & Aske, for a sum I had to read twice.",
          take=F + "mortgage", take_text="I read it standing. The whole estate is mortgaged. My father borrowed against the Ring four years ago, and again last winter, and paid the tenants' arrears out of it so that no one on the Holmwood land would ever be turned out in his time.", give_once=True),
        P("letter", "book", "diary", -0.2, -2.2, y=0.8, name="Letter, addressed to Arthur", radius=0.2,
          look="'ARTHUR - to be opened by my son when the Lord is dead.' My father's hand, much steadier than in life.",
          take=F + "fathers_letter", take_text="'I have kept this from you, God forgive me, because I was afraid you would think yourself a fortune-hunter when you went to Lucy. I mortgaged the Ring so the tenants should not suffer, and I lied to you for four years. Do not lie as I did. A name can bear a debt; it cannot bear a lie. - Your father.'", give_once=True),
        P("chest1", "chest", "ebony", -3.2, -3.0, name="Deed chest", radius=0.6, look="Charters, leases, the 1688 patent of nobility. Dull and very heavy."),
        P("chest2", "chest", "ebony", 3.0, -3.0, name="Deed chest", radius=0.6, look="Marriage-settlements. My mother's is on top, with a ribbon."),
        P("shelf", "bookshelf", "dark", -3.4, 0.8, rot=90, name="Pigeon-holes", radius=0.7, look="Pigeon-holes of rolled parchment, tied with faded tape."),
        P("portrait", "mirror", "default", 0.0, -3.9, y=1.4, name="Portrait frame", radius=0.4, look="A face I almost know, in a frame gone dark. The glass catches my own face over it."),
        P("chair", "chair", "black", -0.8, -1.0, rot=180, radius=0.4, name="Lord's chair", look="His chair. I do not sit in it."),
        P("lamp", "lantern", "default", 2.4, -2.0, radius=0.2),
        P("rug", "rug", "black", 0.4, 1.4, radius=0.1),
        P("d_hall", "door", "ebony", 3.8, 2.0, rot=-90, name="Door to the hall", radius=0.6, look="Back to the hall.", go=F + "hall"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_muniment")])],
)

# ----------------------------------------------------------------------------------------------------------- dialogue
DIALOGUE = {}

DIALOGUE[F + "lord_talk"] = D(
    "n0",
    n0=N("Lord Godalming", "Arthur. Is that the light, or is it the evening?",
         choices=[C("Evening, sir. Dr. Lenox says you must rest.", "n_rest"),
                  C("Your spectacles, sir. I found them under the Bible.", "n_specs", cond="has:" + F + "spectacles&!" + F + "father_specs"),
                  C("The cordial, sir. Dr. Lenox's evening dose.", "n_cordial", cond="has:" + F + "cordial&!" + F + "father_lucid"),
                  C("There is a telegram from Hillingham, sir.", "n_tele", cond="has:" + F + "telegram&" + F + "father_specs&" + F + "father_lucid&!" + F + "blessed"),
                  C("There is a telegram from Hillingham, sir.", "n_tele_not", cond="has:" + F + "telegram&!" + F + "blessed&!" + F + "father_lucid"),
                  C("Tell me about the Ring, sir.", "n_ring"),
                  C("[Leave him to rest]", end=True)]),
    n_rest=N("Lord Godalming", "Rest? I have rested for forty years in that chair downstairs, and look what it has done to my eyes. Talk to me.", next="n0"),
    n_specs=N("Lord Godalming", "Ah. Now there is a thing. A man cannot be a Lord without his spectacles; the tenants would see right through him.", do=[{"take": F + "spectacles"}, {"set": F + "father_specs"}],
              next="n0"),
    n_cordial=N("Lord Godalming", "Foul stuff. Lenox swears by it. Well, I shall be brave for you.", do=[{"take": F + "cordial"}, {"set": F + "father_lucid"}, say("The colour comes back into his face, a little. His voice is stronger.")], next="n0"),
    n_tele_not=N("Lord Godalming", "I cannot read it, Arthur, with the whole room swimming. Come back when I can see.", next="n0"),
    n_tele=N("Lord Godalming", "'...do not stay away for fear of us.' Then go, boy. Go to her. A Holmwood who waits for a death before he lives has not understood the family business.",
             do=[{"set": F + "blessed"}], next="n_tele2"),
    n_tele2=N("Lord Godalming", "There is a ring in my desk. Your mother's. And a letter to Mrs. Westenra, in case her heart needs persuading. The key is somewhere in the hall; I hid it from myself years ago and I have been ashamed ever since.",
              do=[{"journal": F + "j_blessing"}], end=True),
    n_ring=N("Lord Godalming", "The Ring is the house, the land, and four hundred people who think it will outlast them. It is a burden, Arthur. I hope you will carry it better than I.", next="n0"),
)

DIALOGUE[F + "doctor_talk"] = D(
    "n0",
    n0=N("Dr. Lenox", "The Lord rallies when he has company, Mr. Holmwood. Anything that interests him is medicine. But no excitement.",
         choices=[C("What is wrong with him?", "n_ill"), C("Is there any hope?", "n_hope"), C("[Leave]", end=True)]),
    n_ill=N("Dr. Lenox", "The heart, and the strain of carrying too much. Worry is the real disease. He has been worrying for years. About what, I have never been told.", next="n0"),
    n_hope=N("Dr. Lenox", "Weeks, perhaps. He wants to see you settled. I would see to it, if I were you. The green bottle in my cabinet will steady him for conversation.", next="n0"),
)

DIALOGUE[F + "bates_talk"] = D(
    "n0",
    n0=N("Bates", "Master Arthur. The household is at your disposal, sir, as it always was at his.",
         choices=[C("Have you seen my father's desk-key?", "n_key"), C("Who is Crowle of Crowle & Aske?", "n_crowle"), C("[Leave]", end=True)]),
    n_key=N("Bates", "His lordship hid it himself, sir, in the hall, and told no one where. He said once it was safest in company with something that had never been opened: books, old Sir Hugh, or the chest.", next="n0"),
    n_crowle=N("Bates", "The Lord's banker, sir. He came often in the winter. The Lord asked me never to announce him. I thought it discreet.", next="n0"),
)

DIALOGUE[F + "groom_talk"] = D(
    "n0",
    n0=N("Tom", "The brougham will go as soon as you say, sir. Only the Lord gave me orders. No one goes to Hillingham without a word of his blessing, and a letter from him to carry.",
         choices=[C("I will have both before I go.", end=True)]),
)

DIALOGUE[F + "mrsw_talk"] = D(
    "n0",
    n0=N("Mrs. Westenra", "Mr. Holmwood. Lucy has told me nothing, which means she has told me everything. Have you anything for me, from your father?",
         choices=[C("[Give her the Lord's letter]", "n_letter", cond="has:" + F + "intro_letter&!" + F + "mrs_approved"),
                  C("Only my respects, madam.", "n_none", cond="!" + F + "mrs_approved"),
                  C("Thank you for your kindness, madam.", "n_thanks", cond=F + "mrs_approved"),
                  C("[Leave]", end=True)]),
    n_none=N("Mrs. Westenra", "Respects are very nice, but a mother likes a signature.", next="n0"),
    n_thanks=N("Mrs. Westenra", "Go on. Lucy is waiting. I have never seen her so fond of a lawn.", end=True),
    n_letter=N("Mrs. Westenra", "I see. He writes beautifully. But a mother must ask what a letter cannot say. Is the Ring in good heart? I do not ask about money. Only whether it will keep my daughter warm.",
               do=[{"take": F + "intro_letter"}],
               choices=[C("It is sound, madam. Entirely sound.", "n_lie", do=[{"set": F + "lied_to_mrs"}]),
                        C("It is burdened, madam. My father's illness has cost us dear. But my honour is not for sale.", "n_truth", do=[{"set": F + "told_mrs"}])]),
    n_lie=N("Mrs. Westenra", "Splendid. I am so glad. (She says it too quickly, as if she had made up her mind first and asked afterward.)", do=[{"set": F + "mrs_approved"}, {"journal": F + "j_mrs"}], end=True),
    n_truth=N("Mrs. Westenra", "Thank you. That is the first plain answer a gentleman has given me in thirty years. I shall not hold your father's debts against you; I shall hold your honesty for you. Go and find my daughter.",
              do=[{"set": F + "mrs_approved"}, {"journal": F + "j_mrs"}], end=True),
)

DIALOGUE[F + "quincey_talk"] = D(
    "n0",
    n0=N("Quincey Morris", "Say, Art. I had a speech ready. Three fine paragraphs. I reckon I'll keep it for the next wedding. Go on. She's by the roses.",
         choices=[C("You are a better man than I, Quincey.", "n1"), C("Thank you, old fellow.", end=True)]),
    n1=N("Quincey Morris", "Hell, no. I'm a worse shot at the heart. You hit it dead centre without even aiming. I'd call that luck, but I'd rather call it honest.", end=True),
)

DIALOGUE[F + "lucy_talk"] = D(
    "n0",
    n0=N("Lucy", "Arthur! You have come after all. Mamma has been unbearable about it. She says you shall decide to like us on a full stomach.",
         choices=[C("[Offer the wild rose and the ring]", "n_ask", cond="has:wild_rose&has:" + F + "ring&" + F + "mrs_approved&!" + F + "engaged"),
                  C("I have something to ask you, but I am not ready.", "n_notready", cond="!" + F + "engaged"),
                  C("I am so glad to see you.", "n_glad", cond=F + "engaged"),
                  C("[Leave]", end=True)]),
    n_notready=N("Lucy", "Then I shall wait. A girl who has had three proposals in a day knows the smell of a fourth. (She smiles.) Mamma must approve of the thing first, and the rose arbour is so lovely this month.", next="n0"),
    n_glad=N("Lucy", "And I of you. Go and sit in the summer-house, we are expected for tea.", end=True),
    n_ask=N("Arthur", "Lucy, my father is dying. The house I shall inherit is old and tired and heavy with duty. I have nothing to offer you but the whole of myself and my mother's ring. Will you take it?",
            do=[{"take": "wild_rose"}, {"take": F + "ring"}],
            choices=[C("[Wait for her answer]", "n_yes")]),
    n_yes=N("Lucy", "Oh, Arthur. Yes. I have been saying yes for six weeks; you were simply not listening. (She laughs, and takes the rose, and puts the ring on, and wipes her eyes with her wrist.)",
            do=[{"set": F + "engaged"}, {"give": F + "ribbon"}, {"journal": F + "j_proposal"}, say("She gives me a blue ribbon from her hair, 'for luck, and for remembering'.")], end=True),
)

DIALOGUE[F + "lucy_summer_talk"] = D(
    "n0",
    n0=N("Lucy", "Sit by me, Arthur. No one has the right to look so solemn in a summer-house.",
         choices=[C("Tell me what you would do with the Ring.", "n_ring"), C("I want to remember every hour of this.", "n_rem"), C("[Leave]", end=True)]),
    n_ring=N("Lucy", "Open all the windows. And invite the whole village to tea. I am quite certain nobody has ever done it.", next="n0"),
    n_rem=N("Lucy", "Then look about you. The mallets, the music-box, the poems. They are all here, and they will keep.", next="n0"),
)

DIALOGUE[F + "footman_talk"] = D(
    "n0",
    n0=N("Footman", "A telegram, Mr. Holmwood. From the Ring. I am sorry to bring it.",
         choices=[C("[Read it]", "n1")]),
    n1=N("Arthur", "'LORD GODALMING SINKING. COME AT ONCE. BATES.' Lucy turns her face into my shoulder, and does not speak, and does not need to.",
         do=[{"journal": F + "j_telegram_back"}, {"card": "Hillingham stood on its lawn in the last of the light. By the time the train reached the Ring, the Lord had died."},
             {"set": F + "lord_dead"}, {"goto": F + "hall"}], end=True),
)

DIALOGUE[F + "pennefather_talk"] = D(
    "n0",
    n0=N("Mr. Pennefather", "My lord. I mean, the title is yours, as of this morning. I am obliged to tell you the estate is encumbered. I am not at liberty to tell you how. Mr. Wilkes can; the muniment room can; I should rather not.",
         choices=[C("Who holds the key to the muniment room?", "n_key"), C("And the seal?", "n_seal"), C("[Leave]", end=True)]),
    n_key=N("Mr. Pennefather", "The steward holds the key, and, I fancy, an oath to the late Lord not to give it up. You will have to persuade him, my lord. With the ledger, I should think.", next="n0"),
    n_seal=N("Mr. Pennefather", "Your father's signet. It lies with him, in the vault, as is the custom. A custom, my lord, is only a rule you have not been asked to break.", next="n0"),
)

DIALOGUE[F + "crowle_talk"] = D(
    "n0",
    n0=N("Mr. Crowle", "My lord. My deepest sympathy. Business can wait a day, but only a day. May I speak plainly?",
         choices=[C("Please do.", "n_terms", cond="!" + F + "got_terms"),
                  C("What are your terms?", "n_terms_again", cond=F + "got_terms&!has:" + F + "mortgage"),
                  C("I have read the deed, Mr. Crowle.", "n_decide", cond="has:" + F + "mortgage"),
                  C("[Leave]", end=True)]),
    n_terms=N("Mr. Crowle", "Your father borrowed against the Ring. It is no scandal; half the peerage does. But the debt is large, and the interest is hungry. Sell the Home Wood and the Green to a syndicate I know, say nothing to the village, and the whole matter dissolves by Michaelmas. No one need ever know.",
              do=[{"give": F + "terms"}, {"set": F + "got_terms"}, {"journal": F + "j_terms"}], next="n0"),
    n_terms_again=N("Mr. Crowle", "As I said, my lord. A comfortable arrangement. Bring me the deed when you have read it, and I shall draw it up.", next="n0"),
    n_decide=N("Mr. Crowle", "Then you know. Now, my lord: your father's way was a lie, and mine is a quiet sale. What will you do?",
               choices=[C("[Accept Crowle's terms, say nothing]", "n_end_lie"),
                        C("[Refuse, and tell the truth to the tenants]", "n_end_truth", cond="has:" + F + "fathers_letter&has:" + F + "petition"),
                        C("[Refuse, but I am not ready yet]", "n_wait", cond="!has:" + F + "petition"),
                        C("[Not yet]", end=True)]),
    n_wait=N("Mr. Crowle", "My lord, you do not have the tenants with you. A truth with nobody behind it is only a confession.", next="n0"),
    n_end_lie=N("Mr. Crowle", "A wise young man. The Wood will be down by spring. Nobody will say your name unkindly; nobody will say it at all.",
                do=[{"journal": F + "j_end_lie"},
                    {"card": "Arthur signed. The Home Wood was sold by Michaelmas. The Ring was saved, and the village never knew what it had been spared or what it had lost. He wore the signet for the rest of his life and never quite got used to its weight."},
                    {"arc_end": 1}], end=True),
    n_end_truth=N("Mr. Crowle", "I see. Then you are your father's son after all, in the way that matters. I shall extend the term. I would rather lend to a man who tells me how it stands.",
                  do=[{"journal": F + "j_end_truth"},
                      {"card": "Arthur read his father's letter aloud on the village green, with the deed in his hand and Gideon Marsh at his side. The Ring was mortgaged for twenty years more; the tenants gave what they could; the Home Wood stood. In the autumn he stood at Lucy's side in Hillingham church, and was, for an hour, only a man."},
                      {"arc_end": 1}], end=True),
)

DIALOGUE[F + "wilkes_talk"] = D(
    "n0",
    n0=N("Mr. Wilkes", "My lord. Condolences. The funeral was well attended. The estate is... in its customary order.",
         choices=[C("Show him the ledger of arrears.", "n_ledger", cond="has:" + F + "ledger&!" + F + "steward_confessed"),
                  C("Tell me the truth about the estate.", "n_truth", cond="!has:" + F + "ledger&!" + F + "steward_confessed"),
                  C("Thank you for your thirty years, Mr. Wilkes.", "n_thanks", cond=F + "steward_confessed"),
                  C("[Leave]", end=True)]),
    n_truth=N("Mr. Wilkes", "The estate is... as it has been. I am sworn to say no more, my lord. You must look in the ledger on my desk yourself, if you want proof.", next="n0"),
    n_thanks=N("Mr. Wilkes", "It was a privilege, my lord. I hope I have not cost you more than I saved.", end=True),
    n_ledger=N("Mr. Wilkes", "...Where did you find it? Never mind. It is on the page. There is no sense hiding what you can read. The Lord made me swear. I have served him thirty years and I will say it plainly: he borrowed to keep every cottage warm. And I let him.",
               choices=[C("You did right, Mr. Wilkes. Give me the key to the muniment room.", "n_key"),
                        C("You lied to me for four years.", "n_blame")]),
    n_blame=N("Mr. Wilkes", "I did, my lord. Dismiss me if you like. But the Lord asked, and I owed him more than I owed you. I do not know whether that was loyalty or cowardice. Perhaps they are the same.",
              choices=[C("Forgive me. Give me the key, and stay.", "n_key"), C("[Leave]", end=True)]),
    n_key=N("Mr. Wilkes", "Here, my lord. It opens the muniment room, but the lock has a recess for the seal, and the seal is your father's signet. It lies with him in the vault.",
            do=[{"give": F + "muniment_key"}, {"set": F + "steward_confessed"}, {"journal": F + "j_steward"}], end=True),
)

DIALOGUE[F + "marsh_talk"] = D(
    "n0",
    n0=N("Gideon Marsh", "Lord Godalming. We're sorry for your loss. We're sorrier, I'll not lie, for our own. A new Lord is a new landlord.",
         choices=[C("What do the tenants fear?", "n_fear"),
                  C("I want to help.", "n_help"),
                  C("Hobbs says there are men in the Home Wood.", "n_wood", cond="!won:" + F + "poachers"),
                  C("The Home Wood is clear, Mr. Marsh.", "n_proof", cond="won:" + F + "poachers&!" + F + "petition_got&" + F + "wood_cleared"),
                  C("[Leave]", end=True)]),
    n_fear=N("Gideon Marsh", "That the rent goes up, that the Wood goes down, that the Green goes to a railway. Your father kept it all as it was. We never asked how.", next="n0"),
    n_help=N("Gideon Marsh", "Words. Fine words. Show us. There's men in the Home Wood, snaring the Lord's hinds and worse, and no one's gone in. If the new Lord will walk in his own wood by night, we'll listen to what he says by day.", next="n0"),
    n_wood=N("Gideon Marsh", "Aye. Go and see to them yourself. Not Hobbs. You.", next="n0"),
    n_proof=N("Gideon Marsh", "Hobbs has told us. You went in yourself. That's something none of your family's done since the old Sir Hugh. Now tell us the rest, my lord. The whole of it.",
              choices=[C("The estate is mortgaged to its roof, but not a cottage will be sold.", "n_honest", cond="has:" + F + "ledger"),
                       C("The estate is entirely sound, Mr. Marsh.", "n_liar"),
                       C("[Leave]", end=True)]),
    n_liar=N("Gideon Marsh", "...Sound. Is that so. The miller's rent was paid by a bank, my lord, and every one of us knows it. Come back when you can look at us and tell it straight.", next="n0"),
    n_honest=N("Gideon Marsh", "...Well. That's a new thing to hear from a Lord. (He takes his hat off, and the miller does the same.) We've a petition. Thirty names. We'll stand surety for the interest, if you'll stand surety for the cottages.",
               do=[{"give": F + "petition"}, {"set": F + "petition_got"}, {"journal": F + "j_tenants"}], end=True),
)

DIALOGUE[F + "marshwife_talk"] = D(
    "n0",
    n0=N("Mrs. Marsh", "Gideon speaks for all of us. I only speak for the one who'd rather you didn't pretend. Your father pretended beautifully, and never fooled any of us.",
         choices=[C("What would you have me do?", "n1"), C("[Leave]", end=True)]),
    n1=N("Mrs. Marsh", "Tell us the truth. Even a bad truth. People can build a house on it.", end=True),
)

DIALOGUE[F + "miller_talk"] = D(
    "n0",
    n0=N("The miller", "The mill-race was your father's loan, my lord, and I'll be paying it till I'm dead. I never knew who he borrowed from. I thought it came from the Lord's own pocket.",
         choices=[C("It came from a bank. I am sorry.", "n1"), C("[Leave]", end=True)]),
    n1=N("The miller", "A bank! Well. I'd rather have known. A man likes to know whose bread he's eating.", end=True),
)

DIALOGUE[F + "hobbs_talk"] = D(
    "n0",
    n0=N("Hobbs", "My lord! Don't come further. There are three of them by the old beech, and I swear one is a wolf, or something wolfish. There hasn't been a wolf in England since the Stuarts.",
         choices=[C("I will deal with them myself.", "n1"), C("Where did the hind come from?", "n2"), C("[Leave]", end=True)]),
    n1=N("Hobbs", "God bless you, my lord. Aim for the dog first. The men will run when the dog does.", end=True),
    n2=N("Hobbs", "Dead by the log, my lord. Throat torn, not cut. I thought the poachers killed it. Now I think the poachers are as frightened of it as we are.", next="n0"),
)

DIALOGUE[F + "pike_talk"] = D(
    "n0",
    n0=N("Pike", "My lord. The Wood gate was open last night, though I locked it myself. Hobbs says there's trouble in there.",
         choices=[C("I shall see to it.", end=True)]),
)

DIALOGUE[F + "nurse_talk"] = D(
    "n0",
    n0=N("The kneeling woman", "Hush, Master Arthur. It's only old Nan, who nursed you and your mother. I come when the bell tells me there's a Holmwood in grief. I thought you would find the vault.",
         choices=[C("The bell rang by itself.", "n_bell"), C("How does one open the vault, Nan?", "n_vault"), C("[Leave]", end=True)]),
    n_bell=N("Nan", "It rings for the family. It rang for your mother, and for your father this morning. The sexton says it's the wind. Wind or not, I answer.", next="n0"),
    n_vault=N("Nan", "It's a lock of years, dear. The first Lord's 'resting', the old brass says. Read the brasses. Not when he fell, my dear. When he came home.",
              do=[{"set": F + "nan_hint"}], next="n0"),
)

DIALOGUE[F + "vault_lock"] = D(
    "n0",
    n0=N("The vault lock", "A dial of years. 'HERE HE RESTS.' Which year is that?",
         choices=[C("1642.", "n_wrong"), C("1643.", "n_right", cond="!" + F + "vault_open"), C("1688.", "n_wrong"),
                  C("[Go in]", "n_go", cond=F + "vault_open"),
                  C("[Step back]", end=True)]),
    n_wrong=N("The vault lock", "The dial turns. Nothing. Not that year.", next="n0"),
    n_right=N("The vault lock", "The dial clicks. The black door sags inward onto a stair that has not been used since Mother's funeral.", do=[{"set": F + "vault_open"}, {"journal": F + "j_vault_open"}], next="n0"),
    n_go=N("The vault lock", "[You descend the steps]", do=[{"goto": F + "vault"}], end=True),
)

DIALOGUE[F + "coffin_talk"] = D(
    "n0",
    n0=N("Arthur", "My father is in there. The signet lies on his folded hands, as the custom is.",
         choices=[C("[Take the signet from his hand]", "n1", cond="!has:" + F + "signet&!" + F + "signet_taken"),
                  C("[Say a prayer]", "n2"), C("[Step away]", end=True)]),
    n1=N("Arthur", "His fingers are cold. The ring slips off the way it does when a man has grown thin. I whisper that I shall wear it better than I have worn the weeks.",
         do=[{"give": F + "signet"}, {"set": F + "signet_taken"}], next="n0"),
    n2=N("Arthur", "Our father, who art in heaven. I cannot get past 'forgive us our debts', and I stand there for a long time.", next="n0"),
)

# ----------------------------------------------------------------------------------------------------------- items
ITEMS = {
    F + "spectacles": dict(name="Father's spectacles", asset="key", variant="gold", desc="Gold-rimmed, folded in the dying Lord's own hand-writing."),
    F + "cordial": dict(name="Dr. Lenox's cordial", asset="bottle", variant="green", desc="Foul, steadying, and prescribed."),
    F + "telegram": dict(name="Telegram from Hillingham", asset="book", variant="diary", desc="'Do not stay away for fear of us.'"),
    F + "desk_key": dict(name="The Lord's desk-key", asset="key", variant="gold", desc="Brass, small, worn by a thumb. It opens the writing-desk."),
    F + "ring": dict(name="My mother's ring", asset="key", variant="gold", desc="A small old ring with a pale stone, in a velvet box."),
    F + "intro_letter": dict(name="The Lord's letter to Mrs. Westenra", asset="book", variant="leather", desc="A letter of introduction in my father's handwriting."),
    F + "ribbon": dict(name="Lucy's blue ribbon", asset="book", variant="red", desc="Blue silk, still faintly smelling of lavender."),
    F + "ledger": dict(name="Estate ledger", asset="book", variant="leather", desc="Arrears, interest, and the name Crowle & Aske."),
    F + "muniment_key": dict(name="Muniment-room key", asset="key", variant="gold", desc="Three wards, heavy as a hymn-book."),
    F + "signet": dict(name="Godalming's signet ring", asset="key", variant="gold", desc="Heavy, worn smooth. Three rings on a field of grey: the Holmwood arms."),
    F + "mortgage": dict(name="Deed of mortgage", asset="book", variant="red", desc="Three red seals. The whole estate, pledged."),
    F + "fathers_letter": dict(name="My father's letter", asset="book", variant="diary", desc="'Do not lie as I did.'"),
    F + "terms": dict(name="Mr. Crowle's terms", asset="book", variant="leather", desc="A neat sheet: sell the Wood, sell the Green, and say nothing."),
    F + "petition": dict(name="The tenants' petition", asset="book", variant="diary", desc="Thirty names, some of them only crosses."),
}

# ----------------------------------------------------------------------------------------------------------- journal
J = lambda title, text: dict(title=title, source="Arthur Holmwood's recollection", text=text)
JOURNAL = {
    F + "j_sickroom": J("The long illness", "My father has been dying since Candlemas. We have a nurse, a physician and a rug over his knees. He would prefer his spectacles, his cordial, and news from Hillingham, in that order. I have not slept a whole night in a fortnight."),
    F + "j_blessing": J("My father's blessing", "He read Mrs. Westenra's telegram with trembling hands and told me to go to Lucy. There is a ring in his desk, a letter, and a key hidden somewhere in the hall. He looked ashamed when he spoke of the key. I did not ask why."),
    F + "j_hillingham": J("Hillingham", "Lucy in the garden, Mrs. Westenra under her parasol, and Quincey Morris making an elegant exit with the air of a man who has lost a bet and enjoyed it. I had come to propose and my hands were damp."),
    F + "j_mrs": J("Mrs. Westenra's question", "She asked whether the Ring was in good heart. I answered as I did. Whatever I said, she watched my face while I said it, and I knew I would remember her look when I was older."),
    F + "j_proposal": J("The ring and the rose", "She said yes. I said many foolish things first. She gave me a blue ribbon from her hair, and I have worn it against my watch since, and I think I am the happiest man in England."),
    F + "j_summer": J("The summer-house", "Three weeks of tea, croquet and Tennyson. I had not known that life could be so light. Lucy cheats at croquet. Mrs. Westenra pretends not to see. Quincey, to his credit, loses at it with great ceremony."),
    F + "j_telegram_back": J("The telegram", "'LORD GODALMING SINKING.' I left Hillingham in the dusk with Lucy's hand in mine until the carriage moved. I did not reach the Ring in time. He had died at four, with Bates beside him, and a window open that he had asked for."),
    F + "j_death": J("My father is dead", "I am Lord Godalming. The title sits on my shoulders like a coat cut for a larger man. Bates has wept, Dr. Lenox has not, and Mr. Pennefather has the face of a man bringing me a bill. He is, I think, bringing me a bill."),
    F + "j_office": J("The steward's office", "Wilkes keeps the ledgers as another man keeps a conscience: carefully and out of sight. There was a book on his desk with a strap round it. The red ink in it looked less like arithmetic than like a wound."),
    F + "j_steward": J("Wilkes confesses", "Thirty years' service, and he held the secret for my father for four of them. I could not be angry for more than a minute. He gave me the key to the muniment room, and the knowledge that I would need my father's signet to use it."),
    F + "j_village": J("The village green", "The tenants did not take off their hats. I did not blame them. Marsh spoke for them, with Mrs. Marsh listening and the miller scowling. They want to see whether the new Lord will do more than inherit."),
    F + "j_wood_in": J("The Home Wood", "A hind with her throat torn. Three shapes in the dark, and something growling that was not entirely a dog. I will not be afraid in my own wood. I will merely be careful."),
    F + "j_chapel": J("The family chapel", "The bell rang once, though the rope was still, and there was a woman kneeling at the far pew. She was Nan, my nurse. I have decided that the bell was the wind, and that I am not afraid of it."),
    F + "j_vault_open": J("The year of resting", "'Here he rests.' Not the year Sir Hugh fell, but the year his son carried him home. A house which marks its burials as homecomings is a house I do not wish to disgrace."),
    F + "j_vault": J("My father's coffin", "The vault is dry and ordered. My mother is here. He is by her. I stood a long time. The signet was on his hands, as custom says. I took it and I will wear it."),
    F + "j_tenants": J("The tenants' petition", "I told Marsh the truth: the estate is mortgaged to its roof, and not a cottage will be sold if I can help it. He took off his hat. They have given me thirty names and their promise to stand by me."),
    F + "j_muniment": J("The muniment room", "I broke the seal of silence. My father left a deed and a letter, side by side on the blotter, as though he were waiting for me. He is, in a manner of speaking. I read them standing."),
    F + "j_terms": J("Mr. Crowle's kindness", "A very reasonable man. Sell the Wood, say nothing, be rid of it all by Michaelmas. It is the most comfortable thing anyone has offered me in a month, and I know that is exactly what is wrong with it."),
    F + "j_end_lie": J("The comfortable lie", "I signed. The Wood is gone, the debt is small, and no one spoke of it again. I am a very good Lord Godalming by every measure but one, and that one I do not take out to look at often."),
    F + "j_end_truth": J("The hard truth", "I stood on the green and said it all. The village did not cheer; it did something better and went home to count what it could give. I know now that a name can bear a debt but not a lie. I wear the signet in good conscience."),
}

# ----------------------------------------------------------------------------------------------------------- combat
ENEMIES_EXTRA = {
    F + "poacher": dict(name="Poacher", model="human_peasant_m", hp=11, spd=5, dmg=[2, 4], acc=62, eva=6, tags=["human"], flee_at=0.4,
                        book="the Home Wood poachers (invented)"),
    F + "lean_wolf": dict(name="Starved wolf", model="wolf", hp=9, spd=6, dmg=[3, 4], acc=66, eva=12, tags=["beast"], flee_at=0.4, nerve_hit=1,
                          book="the escaped wolf of the Home Wood (invented)"),
}
ENCOUNTERS_EXTRA = {
    F + "poachers": dict(name="Poachers in the Home Wood", time="night", enemies=[F + "poacher", F + "poacher", F + "lean_wolf"], flee_ok=True,
                         intro="A shutter drops and a lantern blazes. Two men and a starved wolf come out of the bracken. 'It's the new Lord,' one of them says, and then, to the beast, 'Get him.'",
                         win="The wolf bolts. The men cry for quarter and I give it. The tenants will hear of this by dawn.", location=F + "wood"),
}
_HOOK = [{"set": F + "wood_cleared"}, {"journal": F + "j_wood_out"}]
ENCOUNTER_HOOKS = {
    F + "poachers": dict(
        on_win=_HOOK + [say("The Wood is still. I did it myself, and that is the whole of the point.")],
        on_lose=_HOOK + [say("I wake against the beech with a split lip. Hobbs found the men gone and the wolf gone, and swears he saw them run from the Lord's name rather than from his arm.")],
        on_flee=_HOOK + [say("I retreat to the gate. The wolf does not follow. By morning the poachers have melted away and the village believes I drove them off. I let it.")]),
}
JOURNAL[F + "j_wood_out"] = J("The Wood is clear", "Two poachers and a starved wolf, driven out of my grandfather's oaks by a man with a club and a worse temper than he knew he had. Hobbs wept. The tenants will want to hear it from me.")

# ----------------------------------------------------------------------------------------------------------- seed variation
PALETTES = {
    F + "sickroom": [dict(wall="plaster_dirty", floor="planks", wood="dark", cloth="red"), dict(wall="plaster", floor="planks", wood="oak", cloth="green")],
    F + "hall": [dict(wall="stone_dark", floor="planks", wood="ebony", cloth="red"), dict(wall="stone_grey", floor="planks", wood="dark", cloth="black")],
    F + "office": [dict(wall="plaster_dirty", floor="planks", wood="oak", cloth="black"), dict(wall="plaster", floor="planks", wood="pale", cloth="blue")],
    F + "garden": [dict(wall="plaster", floor="grass", wood="pale", cloth="blue"), dict(wall="plaster", floor="grass", wood="oak", cloth="green")],
}

PLACEMENTS = {
    F + "desk_key": [
        dict(prop=F + "bust", text="Taped to the underside of the plaster bust's base, a small brass key: the desk-key.", hint="Sir Hugh's plaster base sits slightly crooked."),
        dict(prop=F + "shelf", text="Behind the red Bradshaw, a small brass key hung on a nail: the desk-key.", hint="The red Bradshaw sits one inch proud of the rest."),
        dict(prop=F + "chest", text="At the bottom of the hall chest, in the toe of an old riding-boot, a small brass key: the desk-key.", hint="The hall chest lid has been put down in a hurry."),
    ],
}
