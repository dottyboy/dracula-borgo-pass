"""PERSONAL ARC - "The Last Summer" (Lucy Westenra).  Ids prefixed lucy_summer_."""
from dsl import *

F = "lucy_summer_"


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
    id="lucy_summer", title="The Last Summer", member="lucy", portrait="lucy",
    blurb="Lucy Westenra, three suitors, a garden and a sea she cannot stop dreaming of. A bright life, told in flowers and letters, and what she chooses to leave behind.",
    unlock="flag:a4_staked&flag:a4_arthur_peace_done",
    unlock_text="Lay Lucy to rest with Arthur at her side (Act IV).",
    after_credits=False,
    start=dict(location=F + "room", protagonist="lucy", party=["lucy"], items={}, flags=[]),
    exit_to="ARC_END",
    rewards=[dict(give=F + "pressed_letter"), dict(give="garlic"), dict(give="garlic"),
             dict(stat=dict(member="arthur", nerve=3)), dict(stat=dict(member="mina", nerve=2)),
             dict(set=F + "last_summer_done")],
    rewards_text="Lucy's pressed-flower letter and two heads of garlic; her gift of courage: +3 Nerve for Arthur, +2 Nerve for Mina.",
)

LOCATIONS = [
    dict(id=F + "room", name="Lucy's room, Hillingham", desc="A white bedroom on the first floor, window open on the lawn. It smells of lavender and of a morning that has not yet decided to be anything but happy.", date="Spring, 1889"),
    dict(id=F + "parlour", name="The parlour, Hillingham", desc="Chintz, a piano nobody plays well, and a vase that is not equal to the occasion. Mamma's workbasket sits where a cat would, if she permitted a cat.", date="Spring, 1889"),
    dict(id=F + "garden", name="The garden, Hillingham", desc="A long lawn, a rose arbour and a bench in the shade. Every window of the house is open, and there is a smell of cut grass.", date="Spring, 1889"),
    dict(id=F + "lodging", name="Crescent lodgings, Whitby", desc="Two narrow beds under a sloping ceiling, a window full of sea and a landlady who believes in draughts. We have the best rooms in the Crescent, Mamma says, and the worst stairs.", date="August, 1890 (as the book has it)"),
    dict(id=F + "cliff", name="East Cliff, Whitby", desc="Grass, wind and gulls. The Abbey stands over the town, and below it the old churchyard hangs on to the edge of the cliff by its fingernails.", date="Whitby, high summer"),
    dict(id=F + "cliff_night", name="East Cliff, by night", desc="The same cliff, the same seat, and no one else on the whole headland but me and the moon. And a bell somewhere, tolling slowly, that has no business ringing at this hour.", date="Whitby, a moonlit night"),
    dict(id=F + "steps", name="The Abbey steps, by night", desc="A hundred steps down, then a hundred more, between graves and the black water. I do not know how I came to be halfway down.", date="Whitby, the same night"),
    dict(id=F + "last_room", name="Lucy's room, Hillingham", desc="My own room again, with the window open and a smell in it that is not lavender. Someone is always in the chair beside the bed. Tonight it is Dr. Seward, asleep with two fingers on my wrist.", date="September, 1890"),
]

LOC_DATA = {}

# ----------------------------------------------------------------------------------------------------------- room
LOC_DATA[F + "room"] = dict(
    cells=[2, 2], interior=True, wall="plaster", floor="planks", ambient=AMBIENT["warm_day_interior"], camera=cam([2, 2]),
    lights=lights_warm([2, 2], energy=2.8),
    walls=dict(north=["wall_4", "wall_window_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[2.5, 1.5], spawns={F + "parlour": [2.8, 2.0]},
    props=[
        P("bed", "bed", "blue", -2.2, -2.4, name="My bed", radius=1.2, look="White counterpane, blue hangings, and the dent where I read until the candle guttered. It has never once failed to be comfortable."),
        P("dresser", "table", "pale", 2.2, -3.0, name="Dressing-table", radius=0.9, look="Brushes, ribbons and a hand-glass. Far too many ribbons."),
        P("mirror", "mirror", "default", 2.2, -3.7, y=1.3, name="Looking-glass", radius=0.4, look="A girl in it with a pink face and her hair half up. She looks as though she has been told a secret."),
        P("arthur_letter", "book", "diary", 2.2, -3.0, y=0.8, name="Arthur's letter", radius=0.2,
          look="A thin cream envelope in Arthur's careful, upright hand, addressed to me and not yet opened.",
          take=F + "arthur_letter", take_text="I read it at the window. It is the shortest letter I have ever had from a gentleman, and I read it four times.", give_once=True),
        P("bedside", "table", "oak", -3.0, -0.4, scale=0.6, name="Bedside table", radius=0.5, look="A candle, a novel, a glass of water and a little pot of forget-me-not seeds from Mina."),
        P("ink", "bottle", "amber", -3.0, -0.4, y=0.55, scale=0.6, name="Inkwell", radius=0.2,
          look="A squat bottle of black ink. Mamma says I use more ink than the whole of the Admiralty.",
          take=F + "ink", take_text="I take the inkwell. If I am to write to Mina this week, I shall want it.", give_once=True),
        P("wardrobe", "chest", "ebony", -3.3, 2.0, rot=90, name="Wardrobe", radius=0.6, look="Seven white frocks and one blue. I have been told this is unadventurous."),
        P("shelf", "bookshelf", "pale", 3.3, -0.8, rot=-90, name="My bookshelf", radius=0.7, look="Tennyson, a lady's cookery-book that is only a disguise, and Mina's pressed fern in a green frame."),
        P("rug", "rug", "cream", 0.2, 0.8, radius=0.1),
        P("chair", "chair", "blue", -0.4, 0.6, rot=45, name="Little chair", radius=0.4, look="Where I sit to be pinned into things."),
        P("candle", "candelabra", "default", -3.0, 1.2, y=0.0, scale=0.7, radius=0.2),
        P("sconce", "sconce", "default", 3.7, 0.4, y=1.5, rot=-90, radius=0.1),
        P("door", "door", "pale", 3.8, 2.0, rot=-90, name="Door to the landing", radius=0.6, look="To the stairs and the parlour.", go=F + "parlour"),
    ],
    npcs=[NP("hannah", "human_peasant_f", "village_woman", 0.6, -1.2, rot=0, name="Hannah, the maid",
             look="Hannah, with an armful of linen and a look of fond despair.", talk=F + "hannah_talk")],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_room")])],
)

# ----------------------------------------------------------------------------------------------------------- parlour
LOC_DATA[F + "parlour"] = dict(
    cells=[3, 2], interior=True, wall="plaster", floor="planks", ambient=AMBIENT["warm_day_interior"], camera=cam([3, 2]),
    lights=lights_warm([3, 2], energy=2.8),
    walls=dict(north=["wall_4", "wall_window_4", "wall_4"], west=["wall_door_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[-4.4, -1.5], spawns={F + "room": [-4.4, -1.5], F + "garden": [4.4, -1.5]},
    props=[
        P("table", "table", "pale", 0.4, 0.4, name="Tea-table", radius=1.0, look="Set for six. Mamma's count of the guests increases whenever she looks at it."),
        P("stand", "table", "oak", -2.0, 2.4, scale=0.7, name="Flower-stand", radius=0.5,
          look="A stand with a green jar on it and the sad stalks of last week's arrangement. A vase is not a flower until someone has taken some trouble over it.",
          talk=F + "arrange_talk"),
        P("escritoire", "chest", "ebony", 3.0, -3.0, name="Escritoire", radius=0.7,
          look="Mamma's walnut escritoire, with a little brass lock. Mina's letters are kept in the left-hand drawer.",
          use_item={F + "escritoire_key": [say("The little key turns. Inside are a bundle of Mina's letters tied in blue ribbon, and a pad of good paper."),
                                           {"give": F + "mina_letter"}, {"give": F + "paper"}, {"journal": F + "j_mina_letter"}, {"set": F + "desk_open"}]},
          use_fail="Locked. Mamma keeps the key somewhere only she knows. She would like it to be a proof of something."),
        P("writing", "table", "pale", 3.0, -1.4, scale=0.8, name="Writing-table", radius=0.6,
          look="A small table by the window, where the light is best for letters.", talk=F + "letter_talk"),
        P("sidetable", "table", "dark", -3.0, -3.0, scale=0.7, name="Side-table", radius=0.6, look="A silver tray for cards. It has been very full this week."),
        P("card", "book", "red", -3.0, -3.0, y=0.8, name="Mr. Morris's card", radius=0.2,
          look="A card, slightly bent, left by a tall gentleman who would not wait to be announced.",
          take=F + "quincey_card", take_text="A card in a large, rapid hand. It will not stay in my pocket for long without being read.", give_once=True),
        P("piano", "bookshelf", "dark", -5.0, 1.0, rot=90, name="Piano", radius=0.7, look="A square piano with music open on it. I have been playing the same page since February."),
        P("sofa", "bench", "pale", 0.4, -2.4, name="Sofa", radius=0.9, look="Chintz roses on a sofa. Real roses in the garden look rather superior."),
        P("chair1", "chair", "green", -0.8, 1.6, rot=180, radius=0.4, name="Armchair", look="Mamma's. She sits with her back to the draught and her face to the door."),
        P("chair2", "chair", "green", 2.0, 1.6, rot=180, radius=0.4, name="Armchair", look="The visitors' chair. Occupied this month by a succession of men who all want to be somewhere else."),
        P("rug", "rug", "cream", 0.4, 0.4, radius=0.1),
        P("lamp", "lantern", "default", 4.6, 1.8, radius=0.3, name="Standard lamp", look="Unlit by day; it is waiting for a better occasion."),
        P("d_room", "door", "pale", -5.8, -2.0, rot=90, name="Stairs to my room", radius=0.6, look="Up to the first floor and my own room.", go=F + "room"),
        P("d_garden", "door", "pale", 5.8, -2.0, rot=-90, name="French window to the garden", radius=0.6, look="Open to the lawn.", go=F + "garden"),
    ],
    npcs=[NP("mamma", "human_peasant_f", "innkeeper_wife", 1.6, 1.4, rot=180, name="Mamma", look="Mrs. Westenra, in grey silk, with a heart she cannot spare and a talent for seeing exactly what she wants to see.", talk=F + "mamma_talk")],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_parlour")])],
)

# ----------------------------------------------------------------------------------------------------------- garden
LOC_DATA[F + "garden"] = dict(
    cells=[3, 2], interior=False, wall="plaster", floor="grass", ambient=AMBIENT["day_exterior"], camera=cam([3, 2]), lights=lights_day(3.4),
    scatter=dict(asset="pine_small", variant="green", count=14, seed=7, avoid=[[-7, -5, 7, 5]]),
    spawn=[-4.4, -1.5], spawns={F + "parlour": [-4.4, -1.5]},
    props=[
        P("arbour", "arch", "plaster", -2.4, -3.0, name="Rose arbour", radius=0.8,
          look="The arbour is thick with roses, and the wild one at its foot has opened first, as it does every year.",
          take="wild_rose", take_text="I pick the wild rose from the foot of the arbour. The thorn takes a drop of blood and I suck my thumb like a child.", give_once=True),
        P("lilies", "column_short", "plaster", 3.4, -2.8, name="Lily border", radius=0.5,
          look="Tall white lilies, standing in a row like bridesmaids.",
          take=F + "lilies", take_text="I cut three white lilies, as tall as my elbow. They will do for the back of any vase.", give_once=True),
        P("sundial", "column_short", "stone_grey", 0.8, -3.2, name="Sundial", radius=0.4,
          look="A stone sundial with forget-me-nots growing round its foot. The motto reads: 'I count only the sunny hours'. It must be very slow work.",
          take=F + "forget_me_nots", take_text="A handful of forget-me-nots, small and blue, no taller than my finger.", give_once=True),
        P("bench", "bench", "pale", -4.6, 1.0, rot=90, name="Stone bench", radius=0.9, look="A bench in the shade, for reading and for pretending to read."),
        P("seward_note", "book", "leather", -4.6, 1.0, y=0.5, name="Dr. Seward's note", radius=0.2,
          look="A folded sheet left on the bench. It has my name on it in a hand I have seen on medical charts.",
          take=F + "seward_note", take_text="Dr. Seward must have left it before he went in to Mamma. I read it, and then I fold it very small.", give_once=True),
        P("table", "table", "pale", 1.5, 0.4, name="Tea-table", radius=0.9, look="Lace cloth, a pot of Darjeeling and a plate of what Mamma calls seed-cake."),
        P("chair1", "chair", "blue", 0.2, 0.4, rot=90, radius=0.4, name="Garden chair", look="Mamma's."),
        P("chair2", "chair", "blue", 2.9, 0.4, rot=-90, radius=0.4, name="Garden chair", look="Mine."),
        P("urn", "column_short", "plaster", 4.6, 1.8, name="Urn", radius=0.4, look="Geraniums in military ranks."),
        P("house", "tower", "plaster", 3.4, -6.4, scale=0.6, name="Hillingham", radius=1.2, look="A white house with every window open."),
        P("fence1", "fence", "default", -4.0, 3.8, radius=0.3),
        P("fence2", "fence", "default", 0.0, 3.8, radius=0.3),
        P("fence3", "fence", "default", 4.0, 3.8, radius=0.3),
        P("d_parlour", "door", "pale", -5.5, -2.0, rot=90, name="French window to the parlour", radius=0.6, look="Back to the house.", go=F + "parlour"),
    ],
    npcs=[
        NP("seward", "human_seward", "doctor", -1.2, 1.4, rot=90, name="Dr. John Seward", cond=F + "bouquet_given&!" + F + "refused_seward",
           look="Dr. Seward, young, grave, and visibly rehearsing something under his breath. He holds his hat as though it were a patient.", talk=F + "seward_talk"),
        NP("quincey", "human_quincey", "texan", 4.0, 2.2, rot=-90, name="Mr. Quincey Morris", cond=F + "refused_seward&!" + F + "refused_quincey",
           look="Mr. Morris of Texas, lounging against the fence like it was built for him. His boots are covered in Surrey.", talk=F + "quincey_talk"),
        NP("arthur", "human_arthur", "lord", -3.0, 2.4, rot=45, name="Mr. Arthur Holmwood", cond=F + "refused_quincey&!" + F + "engaged",
           look="Arthur Holmwood, tall and fair and very pale with nerves. He has a rose in his buttonhole, and has forgotten it is there.", talk=F + "arthur_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_garden")])],
)

# ----------------------------------------------------------------------------------------------------------- lodging
LOC_DATA[F + "lodging"] = dict(
    cells=[2, 2], interior=True, wall="plaster_dirty", floor="planks", ambient=AMBIENT["warm_day_interior"], camera=cam([2, 2]),
    lights=lights_warm([2, 2], energy=2.6),
    walls=dict(north=["wall_window_4", "wall_window_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[2.5, 1.5], spawns={F + "cliff": [2.8, 2.0]},
    props=[
        P("bed", "bed", "blue", -2.2, -2.4, name="My bed", radius=1.2, look="The narrower bed, nearer the window. Mina took the other, and the key, and the habit of locking the door.", talk=F + "bed_talk"),
        P("bed_mina", "bed_simple", "green", 2.0, -2.6, name="Mina's bed", radius=1.0, look="Mina's bed, made with a neatness that is almost a reproach."),
        P("trunk", "chest", "dark", 3.2, -0.4, rot=-90, name="My trunk", radius=0.6, look="Everything I own that is not on the road to Whitby, folded in tissue."),
        P("windowseat", "bench", "pale", 0.0, -3.3, name="Window-seat", radius=0.9, look="A window-seat, cushioned in faded cretonne, with a long view of the harbour and the Abbey."),
        P("slippers", "chest", "pale", -3.0, 0.4, scale=0.25, name="My slippers", radius=0.3,
          look="My white slippers, which I left clean by the bed last night. The soles are grey with mud, and the hems of my nightgown are wet.",
          set=F + "slippers_seen", set_text="Wet grass, and sand on the toes. I have not been out. Mina says I have; I say I have not. The slippers do not say."),
        P("table", "table", "oak", -3.0, 2.0, scale=0.8, name="Washstand", radius=0.5, look="A jug, a bowl and a cracked soap-dish."),
        P("mirror", "mirror", "default", -3.7, -0.4, y=1.3, rot=90, name="Looking-glass", radius=0.4, look="I look rather pale this week. I think it is the Whitby light."),
        P("wardrobe", "bookshelf", "pale", 3.3, 1.0, rot=-90, name="Cupboard", radius=0.7, look="Mina's books on one shelf and my novels on another, shelved with a sort of silent argument."),
        P("rug", "rug", "blue", 0.2, 0.6, radius=0.1),
        P("lantern", "lantern", "default", 1.0, -3.2, y=0.0, radius=0.3, name="Oil lamp", look="Mina keeps it filled. She says she will not be caught out in the dark."),
        P("door", "door", "pale", 3.8, 2.0, rot=-90, name="Door to the Crescent", radius=0.6, look="Down to the street, and up to the cliff.", go=F + "cliff"),
    ],
    npcs=[NP("mamma", "human_peasant_f", "innkeeper_wife", 0.4, 1.4, rot=180, name="Mamma", look="Mamma, in a shawl, anxious about draughts and about nothing in particular.", talk=F + "mamma_whitby_talk")],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_whitby")])],
)

# ----------------------------------------------------------------------------------------------------------- cliff (day)
LOC_DATA[F + "cliff"] = dict(
    cells=[3, 3], interior=False, wall="stone_grey", floor="grass", ambient=AMBIENT["day_exterior"], camera=cam([3, 3]), lights=lights_day(3.2),
    scatter=dict(asset="rock", variant="grey", count=10, seed=19, avoid=[[-7, -7, 7, 7]]),
    spawn=[5.0, 2.8], spawns={F + "lodging": [5.0, 2.8]},
    props=[
        P("cliffseat", "bench", "pale", -1.0, -1.2, rot=0, name="The seat on the cliff", radius=0.9,
          look="Our seat, facing the sea. A brass plate on the back says it was given in loving memory of someone who sat here for forty years. The wind is cold on the back of my neck."),
        P("abbey", "tower", "stone_dark", 3.4, -5.6, scale=0.8, name="Whitby Abbey", radius=1.4, look="The ruins stand over the town like an unfinished sentence."),
        P("steps", "stairs", "stone_mossy", -4.8, -3.0, rot=90, name="The Abbey steps", radius=0.9, look="Stone steps cut into the cliff, down to the town and the harbour. Mr. Swales swears there are one hundred and ninety-nine."),
        P("grave1", "gravestone", "stone_mossy", 2.2, -2.2, scale=0.8, name="Weathered gravestone", radius=0.4, look="'Sacred to the memory of a mariner, lost at sea.' I read that on every one of them. The sea has an enormous appetite for stones."),
        P("grave2", "gravestone_point", "stone_grey", 3.8, -1.2, scale=0.8, name="Old gravestone", radius=0.4, look="Lichen has taken the last of the name."),
        P("grave3", "grave_cross", "stone_mossy", 1.0, -3.4, scale=0.8, name="Leaning cross", radius=0.4, look="The cross leans seaward, as though it has been listening."),
        P("bench2", "bench", "dark", -3.4, 1.8, rot=90, name="Old men's bench", radius=0.9, look="Smoothed by generations of people who know exactly what the weather is going to do."),
        P("lantern", "lantern", "default", 1.4, 3.0, radius=0.3, name="Lamp-post", look="A coastguard's lamp, not yet lit."),
        P("sign", "signpost", "oak", 5.6, 1.4, rot=-100, name="Path to the Crescent", radius=0.3, look="'To the Crescent and the town.'", go=F + "lodging"),
        P("fence", "fence", "default", 0.0, 5.0, radius=0.3),
    ],
    npcs=[
        NP("mina", "human_mina", "mina", 0.6, 1.2, rot=180, name="Mina", look="Mina Murray, in a straw hat, with a writing-pad on her knee and anxious eyes.", talk=F + "mina_talk"),
        NP("swales", "human_peasant_m", "innkeeper", -3.4, 1.8, rot=90, name="Mr. Swales", look="Old Swales of the East Cliff, nearly ninety, and as hard as the stones he sits among.", talk=F + "swales_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_cliff")])],
)

# ----------------------------------------------------------------------------------------------------------- cliff (night)
LOC_DATA[F + "cliff_night"] = dict(
    cells=[3, 3], interior=False, wall="stone_dark", floor="grass", ambient=AMBIENT["night_exterior"], camera=cam([3, 3]),
    lights=lights_moon(3.0), moon=dict(pos=[-6, 12, -9]),
    scatter=dict(asset="rock", variant="dark", count=8, seed=23, avoid=[[-7, -7, 7, 7]]),
    spawn=[0.0, 2.0], spawns={},
    props=[
        P("seat_n", "bench", "pale", -1.0, -1.2, rot=0, name="The seat", radius=0.9, look="Our seat. The wood is cold and damp, and I am sitting on it. I do not remember sitting down."),
        P("abbey", "tower", "stone_dark", 3.4, -5.6, scale=0.8, name="Whitby Abbey", radius=1.4, look="Black against a dark blue sky, and one window lit that has no business being lit."),
        P("bell", "column_short", "stone_dark", 4.4, -1.4, name="The tolling", radius=0.4,
          look="There is no bell here. The sound comes from the headland, from the harbour, from inside my own chest, slow, slow, slow."),
        P("steps", "stairs", "stone_mossy", -4.8, -3.0, rot=90, name="The Abbey steps", radius=0.9,
          look="The steps go down into the dark. Down is the way home, if I can stand up.",
          go=F + "steps", go_cond=F + "free", go_fail="I cannot make my feet move. He is looking at me, and my feet have decided to stay. I will have to hold on to something first."),
        P("grave1", "gravestone", "stone_mossy", 2.2, -2.2, scale=0.8, radius=0.4),
        P("grave2", "grave_cross", "stone_grey", 3.8, -1.0, scale=0.8, radius=0.4),
        P("bat", "bat", "black", 1.4, -3.4, y=2.6, scale=1.0, name="Something small and black", radius=0.3, look="It flutters at the edge of my sight and is gone when I turn."),
    ],
    npcs=[NP("figure", "human_dracula", "count", 1.6, -0.4, rot=180, name="A tall dark figure",
             look="Tall, dark, and pale, with eyes that are very red when they look at me. He has been waiting.", talk=F + "figure_talk")],
    on_enter=[dict(once=True, do=[say("I wake sitting on the seat in my nightgown, with my feet bare on the wet grass. The bell is tolling, and a tall dark man is standing by the Abbey wall, watching me with red eyes. I did not walk here. I did not choose this. I want to go home."),
                                  dict(journal=F + "j_night")])],
)

# ----------------------------------------------------------------------------------------------------------- steps (night)
LOC_DATA[F + "steps"] = dict(
    cells=[2, 3], interior=False, wall="stone_dark", floor="cobble", ambient=AMBIENT["night_exterior"], camera=cam([2, 3]),
    lights=lights_moon(2.6), moon=dict(pos=[-5, 11, -8]),
    scatter=dict(asset="rock", variant="dark", count=6, seed=31, avoid=[[-5, -7, 5, 7]]),
    spawn=[0.0, -4.0], spawns={F + "cliff_night": [0.0, -4.0]},
    props=[
        P("count", "stairs", "stone_mossy", 0.0, -2.0, name="The steps", radius=1.0,
          look="Step after step after step, worn into hollows by the feet of sailors' wives. I must go down. I must not lose count.", talk=F + "count_talk"),
        P("grave1", "gravestone", "stone_mossy", -2.8, 0.0, scale=0.9, name="Gravestone", radius=0.4, look="'In memory of ... who departed this life.' Everyone departs; it is only a matter of whose bell they hear."),
        P("grave2", "grave_cross", "stone_mossy", 2.8, -1.0, scale=0.9, name="Leaning cross", radius=0.4, look="The cross points downhill, to the harbour."),
        P("grave3", "gravestone_point", "stone_dark", -2.6, 3.0, scale=0.8, radius=0.4, name="Black gravestone", look="Lichen, cold and wet, the same dead colour as the sea."),
        P("bat", "bat", "brown", 1.0, 0.0, y=2.4, name="A bat", radius=0.3, look="A bat, flitting in and out of the moon. I used to think they were charming."),
        P("lamp", "lantern", "default", 2.4, 4.0, name="Harbour lamp", radius=0.3, look="A single lamp at the bottom of the steps, swinging in the wind."),
    ],
    npcs=[NP("mina", "human_mina", "mina", 0.6, 3.6, rot=180, name="Mina", cond=F + "steps_counted",
             look="Mina, in her dressing-gown with a shawl over her arm and her hair in a plait. She looks as though she has been running.", talk=F + "mina_rescue_talk")],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_steps")])],
)

# ----------------------------------------------------------------------------------------------------------- last room
LOC_DATA[F + "last_room"] = dict(
    cells=[2, 2], interior=True, wall="plaster", floor="planks", ambient=AMBIENT["cold_interior"], camera=cam([2, 2]),
    lights=[dict(pos=[0, 2.6, -1.0], color="#ffb878", energy=2.0, range=10), dict(pos=[-2.6, 1.9, 1.2], color="#9aa8ff", energy=0.9, range=8)],
    walls=dict(north=["wall_4", "wall_window_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_4"]),
    spawn=[0.0, 2.4], spawns={},
    props=[
        P("bed", "bed", "blue", -2.2, -2.4, name="My bed", radius=1.2, look="Blue hangings, white counterpane, and a heap of white flowers on the pillow, which Dr. Van Helsing says is medicine. They smell exactly like a kitchen."),
        P("garlic", "garlic", "default", -2.0, -2.0, y=0.8, scale=1.5, name="Garlic flowers", radius=0.3, look="A great ugly wreath of garlic blossoms. I am told not to take it off."),
        P("desk", "table", "pale", 2.2, -3.0, name="My writing-desk", radius=0.9,
          look="Pen, paper, ink. A long, steady sheet of paper with nothing yet written on it. The window beyond it is open to a night I am going to remember for a very short time.",
          talk=F + "last_desk_talk"),
        P("pressed", "book", "diary", 2.2, -3.0, y=0.8, name="Father's pressed-flower letter", radius=0.2,
          look="My father's letter, written to me when I was ten, with forget-me-nots pressed in every fold. I held it in Whitby on the night I would have died, and it held me back. I know what I shall do with it."),
        P("rug", "rug", "cream", 0.2, 0.8, radius=0.1),
        P("chair", "chair", "red", -0.4, -0.4, rot=90, name="Bedside chair", radius=0.4, look="Someone has sat in it every night this month. I have stopped asking who."),
        P("candle", "candelabra", "default", -3.0, 0.4, scale=0.7, radius=0.2),
        P("sconce", "sconce", "default", 3.7, 0.4, y=1.5, rot=-90, radius=0.1),
        P("shelf", "bookshelf", "pale", 3.3, -0.8, rot=-90, name="My bookshelf", radius=0.7, look="Tennyson, and Mina's pressed fern in its green frame. The shelves look as bright as they did in the spring; it is odd that they should."),
    ],
    npcs=[
        NP("seward", "human_seward", "doctor", -0.8, -0.2, rot=-90, name="Dr. Seward", look="Dr. Seward in the bedside chair, asleep, his hand on my wrist. The best friend any foolish girl ever refused.", talk=F + "seward_last_talk"),
        NP("mamma", "human_peasant_f", "innkeeper_wife", 1.8, 1.2, rot=180, name="Mamma", look="Mamma, asleep in an armchair with her hands folded over her heart, on Dr. Van Helsing's strict orders.", talk=F + "mamma_last_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_last")])],
)

# ----------------------------------------------------------------------------------------------------------- dialogue
DIALOGUE = {}

DIALOGUE[F + "hannah_talk"] = D(
    "n0",
    n0=N("Hannah", "Miss Lucy! Mrs. Westenra says there are to be gentlemen to tea and the parlour vase is to be a credit to the house. And the flowers want doing properly, if I may say so.",
         choices=[C("How do you arrange a vase properly, Hannah?", "n_rule"),
                  C("What do you think of my gentlemen, Hannah?", "n_men"),
                  C("[Leave]", end=True)]),
    n_rule=N("Hannah", "Mrs. Westenra's rule, miss, and her mother's before her: height at the back, then the middle, then the shortest in front, so the eye can walk in. Lilies behind, rose between, little blue things before.",
             do=[{"set": F + "rule_known"}], next="n0"),
    n_men=N("Hannah", "I think the doctor will bring a book, and the American will bring a horse, and Mr. Holmwood will bring his whole heart in his two hands and not know where to put it. I'd say that last is the one for you, miss, but it's not for the likes of me to say.",
            next="n0"),
)

DIALOGUE[F + "mamma_talk"] = D(
    "n0",
    n0=N("Mamma", "Lucy, there is a tea at four and a vase that looks as though it has been in a fight. I want a bouquet in this room before the doctor comes, and I shall not be put off with half the garden in a jam-jar.",
         choices=[C("[Give her the bouquet]", "n_bq", cond="has:" + F + "bouquet&!" + F + "bouquet_given"),
                  C("What do you want in the vase, Mamma?", "n_flowers", cond="!" + F + "bouquet_given"),
                  C("Mamma, may we speak of Whitby?", "n_whitby", cond=F + "engaged&" + F + "letter_sent"),
                  C("I am very tired today, Mamma.", "n_tired"),
                  C("[Leave]", end=True)]),
    n_flowers=N("Mamma", "Flowers, child. White lilies, a wild rose from the arbour, and the forget-me-nots Mina sent seed for. Arrange them yourself; you have the best eye in Hillingham and the worst patience.", next="n0"),
    n_tired=N("Mamma", "You have been tired all spring, my darling, and rosy with it. It is the gentlemen. When they are settled you will sleep like a log. (She pats my cheek, and her hand is trembling a little.)", next="n0"),
    n_bq=N("Mamma", "Oh, Lucy. It is exactly right. The lilies stand up, the rose looks out, and the little blue things hold hands in front. I could weep. Take Mina's key; I have been keeping it from you since Tuesday for no reason except that I like to be asked.",
           do=[{"take": F + "bouquet"}, {"give": F + "escritoire_key"}, {"set": F + "bouquet_given"}, {"journal": F + "j_flowers"}],
           next="n0"),
    n_whitby=N("Mamma", "Whitby! Mina has been scribbling about it for weeks, and the sea air will do you good, and so shall poor Mrs. Murray's gossip. Pack your trunk, Lucy. The Crescent is taken, and I shall travel with you.",
               do=[{"journal": F + "j_pack"},
                   {"card": "In the summer Lucy went to Whitby, with her mother and her best friend, and a trunk full of white frocks. She took a bright laugh with her, and the sea took notice."},
                   {"goto": F + "lodging"}], end=True),
)

DIALOGUE[F + "arrange_talk"] = D(
    "n0",
    n0=N("Lucy", "A green jar, empty. I have the stalks to fill it, if I have the flowers.",
         choices=[C("[Arrange the flowers]", "n_back", cond="has:" + F + "lilies&has:wild_rose&has:" + F + "forget_me_nots&!has:" + F + "bouquet&!" + F + "bouquet_given"),
                  C("I haven't all I need.", "n_miss", cond="!has:" + F + "bouquet&!" + F + "bouquet_given&!has:" + F + "lilies"),
                  C("I haven't all I need.", "n_miss", cond="!has:" + F + "bouquet&!" + F + "bouquet_given&has:" + F + "lilies&!has:wild_rose"),
                  C("I haven't all I need.", "n_miss", cond="!has:" + F + "bouquet&!" + F + "bouquet_given&has:" + F + "lilies&has:wild_rose&!has:" + F + "forget_me_nots"),
                  C("[Leave it]", end=True)]),
    n_miss=N("Lucy", "I need three things: white lilies, a wild rose and forget-me-nots. All in the garden, if I know the garden.", next="n0"),
    n_back=N("Lucy", "Which flowers go at the back of the jar, to stand highest?",
             choices=[C("The lilies.", "n_mid"), C("The wild rose.", "n_wrong_back"), C("The forget-me-nots.", "n_wrong_back")]),
    n_wrong_back=N("Lucy", "I put it there, and it sinks. The jar looks lopsided and apologetic. The tallest should be at the back, I think, so the others can lean on it.", next="n_back"),
    n_mid=N("Lucy", "And in the middle, standing between the lilies and the front?",
            choices=[C("The wild rose.", "n_front"), C("The forget-me-nots.", "n_wrong_mid")]),
    n_wrong_mid=N("Lucy", "The forget-me-nots flop forward like little blue sleepers and the rose is left behind them. I take them out. The middle is the rose's.", next="n_mid"),
    n_front=N("Lucy", "And last, the front?",
              choices=[C("The forget-me-nots, in a fringe at the front.", "n_done"), C("Nothing; leave it with its lilies and its rose.", "n_wrong_front")]),
    n_wrong_front=N("Lucy", "It looks bare. There is a rule against bare vases, and I am married to rules at the moment. The blue ones go in front.", next="n_front"),
    n_done=N("Lucy", "I stand back and look. The tall lilies stand and the wild rose looks out between them, and the small blue things hold hands in the front. It is the first thing I have done well all spring.",
             do=[{"take": F + "lilies"}, {"take": "wild_rose"}, {"take": F + "forget_me_nots"}, {"give": F + "bouquet"}, {"set": F + "arranged"}], end=True),
)

DIALOGUE[F + "seward_talk"] = D(
    "n0",
    n0=N("Dr. Seward", "Miss Westenra... Lucy. I came to speak to you. I have a note somewhere, but I think I had better say it myself. I have thought of nothing else. I should like very much to ask for your hand.",
         choices=[C("[Answer him]", "n_ask")]),
    n_ask=N("Lucy", "He is the dearest man, and I cannot marry him. But what shall I say?",
            choices=[C("Not yet, John. Ask me again in a year, and I'll see how I feel.", "n_hope"),
                     C("Dr. Seward, I like you better than almost anyone, and I cannot marry you. I will not keep you hoping.", "n_right"),
                     C("You are far too grave for me, John! You would bury me in your casebooks.", "n_cruel")]),
    n_hope=N("Dr. Seward", "A year. Yes. Of course. I shall wait. I am a patient man, you know; it is the whole of my profession. (He smiles, and my heart sinks, because I have given him a hook to hang a year on.)",
             next="n_ask"),
    n_cruel=N("Dr. Seward", "...I see. I beg your pardon. (He turns his hat in his hands, and says nothing, and I am ashamed of myself for the rest of the day.)", next="n_ask"),
    n_right=N("Dr. Seward", "Thank you. That was kind, and it was plain, and I would rather have it so than the other way. I knew, I think, before I asked. May I still be your friend?",
              choices=[C("Always. You will be Jack to me as long as you like.", "n_end")]),
    n_end=N("Dr. Seward", "Then I shall go and be of use to someone. Good day, Lucy. Be happy; it is a medical prescription.",
            do=[{"set": F + "refused_seward"}, {"journal": F + "j_seward"}], end=True),
)

DIALOGUE[F + "quincey_talk"] = D(
    "n0",
    n0=N("Quincey Morris", "Miss Lucy. I'll be as brief as a Texan can. I've ridden a long way and shot a few things and I'd like to ask if you'd take me on as a husband. That's the whole speech. The rest is for you.",
         choices=[C("[Answer him]", "n_ask")]),
    n_ask=N("Lucy", "I must not make him sit through a speech. But I must not be too short either.",
            choices=[C("Mr. Morris, one cannot speak so quickly of such things, and one must consider the whole situation, and the position, and one's dear Mamma, and the prospects, and...", "n_long"),
                     C("No, Mr. Morris. I am sorry. I am proud you asked, and I should like us to be friends.", "n_right"),
                     C("Perhaps, if you were to stay in England a few more months, I might think of it.", "n_hope")]),
    n_long=N("Quincey Morris", "That's a heap of words, ma'am, for what I reckon is a no. I'd have gone easier with the plain article. (He takes off his hat, and puts it on again.)", next="n_ask"),
    n_hope=N("Quincey Morris", "More months? Hell, Miss Lucy, I'd stay years. I'd stay till the Thames froze over. (He is smiling. I have just made a very kind, very stupid mistake.)", next="n_ask"),
    n_right=N("Quincey Morris", "No hard feelings, ma'am. A man gets to say it, and a woman gets to say the other, and neither of us gets to be sorry for the saying. But if you ever want a man to ride out in the rain for you, you whistle.",
              choices=[C("I shall whistle badly, Quincey, but I shall whistle.", "n_end")]),
    n_end=N("Quincey Morris", "That's the girl. Now, I reckon there's a gentleman waiting for you behind that rose-bush who's been standing there for half an hour. Good luck, Miss Lucy.",
            do=[{"set": F + "refused_quincey"}, {"journal": F + "j_quincey"}], end=True),
)

DIALOGUE[F + "arthur_talk"] = D(
    "n0",
    n0=N("Arthur Holmwood", "Lucy... I had a long speech and I've dropped it somewhere in the lilies. I only want to ask whether you could be happy with me. If you could, I should be the most fortunate man in England. If you couldn't, I should try to deserve it.",
         choices=[C("[Answer him]", "n_ask")]),
    n_ask=N("Lucy", "I do not need a speech either. I only need to be myself for once, and plain.",
            choices=[C("I must ask Mamma, Arthur, and then I shall tell you, at some convenient time next week.", "n_mamma"),
                     C("Yes, Arthur. Plainly, and you shall not have to ask a second time.", "n_right"),
                     C("Ask me tomorrow. I shall think it over.", "n_think")]),
    n_mamma=N("Arthur Holmwood", "Of course. Mrs. Westenra. Next week. (His face is a perfect picture of a man who has been ordered to stand in the rain.)", next="n_ask"),
    n_think=N("Arthur Holmwood", "Tomorrow. Yes. I shall be at the Station Hotel and I shall not sleep. (And I know, watching him go white, that I have done wrong, and I want to run after him.)", next="n_ask"),
    n_right=N("Arthur Holmwood", "Lucy! ...Lucy. (He takes my hand, and discovers the rose in his buttonhole, and puts it in my hair, and I laugh until I cry.) My mother's ring is in my pocket. May I?",
              choices=[C("[Hold out my hand]", "n_end")]),
    n_end=N("Lucy", "It is a small old ring with a pale stone, and it fits. I wish, oh I wish one girl could marry all three of them. Jack, who sees what is wrong; Quincey, who is the one you want in a storm; Arthur, who is the one you want at home. But there is only one of me, and I have said yes to the one I love.",
            do=[{"give": F + "ring"}, {"set": F + "engaged"}, {"journal": F + "j_arthur"}], end=True),
)

DIALOGUE[F + "letter_talk"] = D(
    "n0",
    n0=N("Lucy", "A desk, a window and the best light in the house. Mina's letters are always so careful. Mine always have the postscript first.",
         choices=[C("[Write to Mina]", "w1", cond="has:" + F + "ink&has:" + F + "paper&has:" + F + "mina_letter&" + F + "engaged&!" + F + "letter_sent"),
                  C("I have nothing to tell her yet.", "n_notyet", cond="!" + F + "engaged"),
                  C("I need ink, paper and Mina's last letter first.", "n_missing", cond=F + "engaged&!" + F + "letter_sent&!has:" + F + "ink"),
                  C("I need ink, paper and Mina's last letter first.", "n_missing", cond=F + "engaged&!" + F + "letter_sent&has:" + F + "ink&!has:" + F + "paper"),
                  C("I need ink, paper and Mina's last letter first.", "n_missing", cond=F + "engaged&!" + F + "letter_sent&has:" + F + "ink&has:" + F + "paper&!has:" + F + "mina_letter"),
                  C("[Read Mina's letter again]", "n_read", cond="has:" + F + "mina_letter"),
                  C("[Leave]", end=True)]),
    n_notyet=N("Lucy", "I have nothing settled to tell her. Not about the gentlemen, anyway. I shall come back when my heart has stopped changing its mind.", next="n0"),
    n_missing=N("Lucy", "The ink from my room, the paper from Mamma's escritoire, and Mina's own letter to answer. It is in the left-hand drawer.", next="n0"),
    n_read=N("Mina", "'Dearest Lucy, you must tell me everything, but not in the order it comes to you, for your letters are all middle. Begin with what you see out of the window; then the people in the house; then what you cannot tell anyone else; and last, your love, always your love. It makes a letter into a path.' - Mina.", next="n0"),
    w1=N("Lucy", "'Dearest Mina.' How do I begin?",
         choices=[C("The window: 'The roses are out, the lawn is cut, and the whole house smells of tea.'", "w2"),
                  C("The secret: 'Mina, I have had THREE proposals in a single afternoon!'", "w1_secret"),
                  C("My health: 'I am so very tired lately, Mina, and I cannot think why.'", "w1_tired")]),
    w1_secret=N("Lucy", "I cross it out. She would read no further than that and answer by return of post in alarm. Mina said to begin with the window.", next="w1"),
    w1_tired=N("Lucy", "I cross it out. She worries too easily; I must give her something steady first.", next="w1"),
    w2=N("Lucy", "And next?",
         choices=[C("The people: 'Mamma is well, the doctor has been twice, and Hannah has opinions about everything.'", "w3"),
                  C("My love, quickly, so it is not forgotten.", "w2_love"),
                  C("The postscript: 'P.S. Please do not tell Jonathan anything.'", "w2_ps")]),
    w2_love=N("Lucy", "Too soon. A path should have somewhere to go before it ends.", next="w2"),
    w2_ps=N("Lucy", "I smile, because it is exactly my habit, and cross it out. Not yet; it is the middle of the letter, not the end.", next="w2"),
    w3=N("Lucy", "And then, the part I have been burning to write?",
         choices=[C("The secret: Jack, Quincey, Arthur, and why can't one girl marry all three?", "w4"),
                  C("Sign off now; she has enough.", "w3_off"),
                  C("More about the roses.", "w3_roses")]),
    w3_off=N("Lucy", "I cannot stop there. She would know there was something I was not telling her, and she would write me four pages of worry. The secret goes before the love.", next="w3"),
    w3_roses=N("Lucy", "The roses have had their turn. The bit Mina wants is the bit I have been avoiding.", next="w3"),
    w4=N("Lucy", "And at the end?",
         choices=[C("'My love, always, and come to Whitby if you can. I shall keep the other bed made up. - Lucy.'", "w_done"),
                  C("'Burn this when you have read it.'", "w4_burn")]),
    w4_burn=N("Lucy", "She would never burn it. She would put it in the blue ribbon with the rest. I write what I really mean.", next="w4"),
    w_done=N("Lucy", "It is a good letter. I read it through, blot it, fold it, and give it to Hannah for the post. Mina will have the whole of it by Friday, in order, as she asked.",
             do=[{"set": F + "letter_sent"}, {"journal": F + "j_letter"}], end=True),
)

DIALOGUE[F + "mamma_whitby_talk"] = D(
    "n0",
    n0=N("Mamma", "Lucy, my pet, I have unpacked everything but your trunk. Your father's letter, the one with the forget-me-nots... I cannot find it anywhere. You took it out of the trunk at Hillingham, I remember, and you never let it out of your sight.",
         choices=[C("I have lost Papa's letter?", "n_lost", cond="!" + F + "knows_lost"),
                  C("Where might I have left it, Mamma?", "n_where", cond=F + "knows_lost&!has:" + F + "pressed_letter"),
                  C("I found it, Mamma. It is safe.", "n_found", cond="has:" + F + "pressed_letter"),
                  C("[Leave]", end=True)]),
    n_lost=N("Mamma", "It has the pressed forget-me-nots, my dear, and your father's hand. If you left it anywhere, it was in your trunk, or the window-seat by the harbour, or on that wretched seat on the cliff where you and Mina sit.",
             do=[{"set": F + "knows_lost"}, {"journal": F + "j_lost"}], next="n0"),
    n_where=N("Mamma", "The trunk, the window-seat, the seat on the cliff. I have looked in none, because you are the only one who ever knows where she put things down.", next="n0"),
    n_found=N("Mamma", "Thank heaven. Keep it safe, my darling; it is the one thing of his I have left you.", next="n0"),
)

DIALOGUE[F + "mina_talk"] = D(
    "n0",
    n0=N("Mina", "Lucy! There you are. I have been keeping the seat warm, which in this wind is like keeping a promise to a gull. How are you?",
         choices=[C("Mina, did I walk in my sleep last night?", "n_walk", cond="!" + F + "mina_talk"),
                  C("Any news of Jonathan?", "n_jon"),
                  C("What do you make of Whitby?", "n_whitby"),
                  C("[Leave]", end=True)]),
    n_walk=N("Mina", "I am afraid you did, dearest. I woke in the night and your bed was empty and the door was open. I found you at the window, in your nightgown, looking at the Abbey. I put you back to bed, and I have taken the key to our door and put it under my pillow.",
             do=[{"set": F + "mina_talk"}, {"journal": F + "j_mina_walk"}], next="n0"),
    n_jon=N("Mina", "Nothing since the letter from Buda-Pesth. I dare not hope and I dare not not hope. Let us not speak of it; you have enough to be going on with.", next="n0"),
    n_whitby=N("Mina", "A town built like a staircase. Churchyard on the cliff, old graves, and tombstones for people who were buried at sea. It is the saddest place I have ever loved. Mr. Swales is the oldest man on the cliff, and the most disagreeable; he knows every story in it.", next="n0"),
)

DIALOGUE[F + "swales_talk"] = D(
    "n0",
    n0=N("Mr. Swales", "Eh, look who's come. T' lady wi' t' pretty frocks. Sit tha down. Nay, not on yon seat. It's a rare place for a lass to be lonely, that seat.",
         choices=[C("How many steps are there down to the town, Mr. Swales?", "n_steps"),
                  C("What do you know of the seat?", "n_seat"),
                  C("Why do they say there is a bell at night?", "n_bell"),
                  C("[Leave]", end=True)]),
    n_steps=N("Mr. Swales", "A hundred and ninety-nine, miss. I've counted 'em wi' coffins on my shoulder. Tha counts 'em right, tha's off the cliff in no time; get it wrong and tha's on the cliff all night, wi' no way down but the long one.",
              do=[{"set": F + "swales_steps"}, {"journal": F + "j_swales"}], next="n0"),
    n_seat=N("Mr. Swales", "Folk sit there to look at the sea. It's been there longer nor I. Sailors' wives sat there to watch for t' ships, and some of 'em sat so long they forgot to go home.", next="n0"),
    n_bell=N("Mr. Swales", "There's no bell, lass. There's a bell on the sea, a buoy, that rings when t' water's rough. Other folk say it's the Abbey's old bell, rung by monks that never left. I say a bell's what you hear when tha wants to be called.", next="n0"),
)

DIALOGUE[F + "bed_talk"] = D(
    "n0",
    n0=N("Lucy", "My bed. It is evening, and Mina has taken the key. I am to sleep the sleep of the just, if only I knew what I am to be just about.",
         choices=[C("[Go to sleep]", "n_sleep", cond="has:" + F + "pressed_letter&" + F + "mina_talk&" + F + "swales_steps&" + F + "slippers_seen"),
                  C("I cannot go to bed yet. Father's letter is lost.", "n_h1", cond="!has:" + F + "pressed_letter"),
                  C("I want to speak to Mina first.", "n_h2", cond="has:" + F + "pressed_letter&!" + F + "mina_talk"),
                  C("I should like to speak to old Mr. Swales first.", "n_h3", cond="has:" + F + "pressed_letter&" + F + "mina_talk&!" + F + "swales_steps"),
                  C("Something about my slippers worries me.", "n_h4", cond="has:" + F + "pressed_letter&" + F + "mina_talk&" + F + "swales_steps&!" + F + "slippers_seen"),
                  C("[Not yet]", end=True)]),
    n_h1=N("Lucy", "I am not going to bed without it. I want it under my pillow. I shall look in the trunk, the window-seat and on the cliff.", next="n0"),
    n_h2=N("Lucy", "Mina would know about last night. She was awake. She will be on the cliff.", next="n0"),
    n_h3=N("Lucy", "Mr. Swales knows the cliff and what is on it. I should like to ask him something first.", next="n0"),
    n_h4=N("Lucy", "My slippers are by the bed; I should look at them before I do anything else.", next="n0"),
    n_sleep=N("Lucy", "I lie down with Papa's letter on the pillow beside me, and the window open on the sea, and Mina's key under her head. I count sheep, then waves, then steps. I do not remember falling asleep.",
              do=[{"set": F + "slept"}, {"card": "That night Lucy slept. And at some hour of the night, the key stayed under Mina's pillow and the door stayed locked, and Lucy was not in her bed."},
                  {"goto": F + "cliff_night"}], end=True),
)

DIALOGUE[F + "figure_talk"] = D(
    "n0",
    n0=N("The tall dark figure", "There you are, little one. I have waited. The sea has been calling you for weeks, and you have been such a good listener. Sit with me. Cold, are you? Come closer.",
         choices=[C("[Sit beside him]", "n_sit"),
                  C("[Hold up Arthur's ring and say his name]", "n_ring", cond="has:" + F + "ring&!" + F + "anchor_a"),
                  C("[Press Mina's letter to your chest and say her name]", "n_mina", cond="has:" + F + "mina_letter&!" + F + "anchor_m"),
                  C("[Hold Father's pressed-flower letter and say his name]", "n_father", cond="has:" + F + "pressed_letter&!" + F + "anchor_p"),
                  C("[Turn away. Walk.]", "n_free", cond=F + "anchor_a&" + F + "anchor_m&" + F + "anchor_p&!" + F + "free"),
                  C("[Look at his eyes]", "n_look"),
                  C("[Leave]", end=True)]),
    n_sit=N("Lucy", "I take one step toward the seat. My feet are wet. My head is full of waves. The bell is very close now, and very warm, and I want to lie down. I must hold on to something. I have something in my hands.", next="n0"),
    n_look=N("The tall dark figure", "Yes, that's it. You see me now. No need to speak. Your pulse is lovely, did you know? Quick as a bird. Come.", next="n_look2"),
    n_look2=N("Lucy", "The red goes on forever. I think I am falling into it. There was a ring on my finger. There was a letter in my hand. There were people.", next="n0"),
    n_ring=N("Lucy", "Arthur. Arthur Holmwood. My ring is cold in my hand and Arthur's name is warm in my mouth. 'Arthur,' I say. He flinches, very slightly, as if I had thrown something.",
             do=[{"set": F + "anchor_a"}, {"journal": F + "j_anchor_a"}], next="n0"),
    n_mina=N("Lucy", "Mina. Mina Murray. Her letter is folded in four and I read the first line aloud, 'Begin with what you see out of the window.' I see a dark man, and a Moon, and a path home. 'Mina,' I say. He hisses.",
             do=[{"set": F + "anchor_m"}, {"journal": F + "j_anchor_m"}], next="n0"),
    n_father=N("Lucy", "Papa. A man I barely remember, writing to a girl of ten with flowers pressed in every fold. I hold it against my heart. 'Papa,' I say. The forget-me-nots are stiff and dry and exactly real.",
               do=[{"set": F + "anchor_p"}, {"journal": F + "j_anchor_p"}], next="n0"),
    n_free=N("The tall dark figure", "Stay. Stay, little one. You are mine. Not tonight, then. Not tonight.",
             do=[{"set": F + "free"}, {"journal": F + "j_free"}, say("Behind me, no footstep. In front of me, the dark steps down, and I walk toward them with three names in my mouth like stones.")],
             end=True),
)

DIALOGUE[F + "count_talk"] = D(
    "n0",
    n0=N("Lucy", "I am on the top of the steps, in my nightgown. The tolling follows me down. If I lose count, I shall be lost. How many steps are there from the cliff to the town?",
         choices=[C("One hundred and ninety-nine.", "n_right", cond="!" + F + "steps_counted"),
                  C("A hundred.", "n_wrong"),
                  C("Two hundred.", "n_wrong"),
                  C("A hundred and ninety.", "n_wrong"),
                  C("[Go down to Mina]", end=True, cond=F + "steps_counted"),
                  C("[Wait]", end=True)]),
    n_wrong=N("Lucy", "...ninety-eight, ninety-nine, a hundred... no. I am not sure. The tolling swells and I lose the place and begin again from the top, my heart going like a bird in a net. Count again.", next="n0"),
    n_right=N("Lucy", "I count them down, step by step, aloud, as I would count out Arthur's name. Ninety-seven, ninety-eight, ninety-nine. Eventually the cobbles. One hundred and ninety-nine. At the bottom, a lamp swings, and somebody is running.",
              do=[{"set": F + "steps_counted"}, {"journal": F + "j_counted"}], end=True),
)

DIALOGUE[F + "mina_rescue_talk"] = D(
    "n0",
    n0=N("Mina", "Lucy! Oh, Lucy. I woke and the door was locked and you were gone and the key was still under my pillow. I ran all the way. Your feet. Your poor feet! Come, come, put this round you.",
         choices=[C("Mina, there was a man on the seat. A tall dark man with red eyes.", "n_man"),
                  C("Take me home, Mina.", "n_home")]),
    n_man=N("Mina", "There is no one, dearest. Only the moon on the grave-stones. But I believe that you saw it. Come away. I shall keep the key under my pillow as long as you need me to.", next="n_home"),
    n_home=N("Mina", "Look at me. You are shivering and your cheeks are white, and you are alive, which is all that matters. Home, and warm milk, and in the morning we shall tell Mamma that we saw the sunrise.",
             do=[{"journal": F + "j_mina_rescue"},
                 {"card": "Lucy was found on the Abbey steps and put to bed. But the pallor stayed, and the dreams stayed, and by September she was at Hillingham again, and nothing that anyone could say was strong enough to make her well."},
                 {"goto": F + "last_room"}], end=True),
)

DIALOGUE[F + "seward_last_talk"] = D(
    "n0",
    n0=N("Dr. Seward", "(He stirs, but does not wake. His lips move: 'Lucy... a little more time.') ", next="n1"),
    n1=N("Lucy", "Dear Jack. You asked me for one thing and I said no, and you have given me everything else. I shall not wake him; he has had so little sleep.", end=True),
)

DIALOGUE[F + "mamma_last_talk"] = D(
    "n0",
    n0=N("Lucy", "Mamma is sleeping with a handkerchief in her hand, her heart as fragile as mine. I should like to say something to her, but there is nothing she could hear that would not frighten her. I shall leave her to dream I am well.", end=True),
)

DIALOGUE[F + "last_desk_talk"] = D(
    "n0",
    n0=N("Lucy", "Paper, a pen, ink. Dr. Van Helsing is somewhere in the house and Arthur is on his way. I have not much time. Two letters to write and one thing to leave: Papa's pressed-flower letter. Who shall have it?",
         choices=[C("[Write to Arthur]", "a1", cond="!" + F + "arthur_written"),
                  C("[Write to Mina]", "m1", cond=F + "arthur_written&!" + F + "mina_written"),
                  C("[Decide where Papa's letter goes]", "k1", cond=F + "arthur_written&" + F + "mina_written"),
                  C("[Rest a little]", end=True)]),
    a1=N("Lucy", "Arthur. Dear Arthur. What shall I tell him?",
         choices=[C("'Do not be small with grief. Live, and love again, when you can. I shall not mind.'", "n0",
                    do=[{"set": F + "arthur_written"}, {"set": F + "a_release"}, {"journal": F + "j_a_release"}]),
                  C("'Remember me in the garden, with the rose in my hair, and be the man I knew.'", "n0",
                    do=[{"set": F + "arthur_written"}, {"set": F + "a_remember"}, {"journal": F + "j_a_remember"}])]),
    m1=N("Lucy", "Mina. Dear Mina. What do I tell her?",
         choices=[C("'Watch over Arthur for me; he does not know how to be alone.'", "n0",
                    do=[{"set": F + "mina_written"}, {"set": F + "m_arthur"}, {"journal": F + "j_m_arthur"}]),
                  C("'Keep writing, everything you see, in order, as you taught me. One day someone will need it.'", "n0",
                    do=[{"set": F + "mina_written"}, {"set": F + "m_write"}, {"journal": F + "j_m_write"}])]),
    k1=N("Lucy", "Papa's letter, pressed with forget-me-nots, the one thing that held me back from the sea. Where shall it go?",
         choices=[C("[Leave it for Arthur, with the ring]", cond=F + "a_release", do=[{"journal": F + "j_end_arthur"}, {"card": "Lucy left Arthur her father's letter, and a line begging him to live. In time, he did. The pressed flowers were the last thing she gave him, and he kept them against his heart, and eventually he learned to let them rest."}, {"arc_end": 1}]),
                  C("[Leave it for Arthur, with the ring]", cond=F + "a_remember", do=[{"journal": F + "j_end_arthur"}, {"card": "Lucy left Arthur her father's letter, with the line 'remember the garden'. He read it in the vault by lamplight, on the night she was lost, and kept it in his breast pocket until the day he died. The roses at Ring bloomed white for years after."}, {"arc_end": 1}]),
                  C("[Leave it for Mina]", cond=F + "m_arthur", do=[{"journal": F + "j_end_mina"}, {"card": "Lucy left her father's letter to Mina, and Mina, true to her promise, put it in her writing-case with the others, and when the time came she did watch over Arthur, who did not know how to be alone."}, {"arc_end": 1}]),
                  C("[Leave it for Mina]", cond=F + "m_write", do=[{"journal": F + "j_end_mina"}, {"card": "Lucy left her father's letter to Mina, and Mina pressed it in the back of her journal, and kept every word. In the end it was Mina's notes, made in order, in a clear hand, that told the whole of it."}, {"arc_end": 1}]),
                  C("[Keep it in my hands]", cond=F + "a_release", do=[{"journal": F + "j_end_keep"}, {"card": "Lucy kept her father's letter in her folded hands. She was buried in Kingstead churchyard with the forget-me-nots against her heart, and wore, in the moonlight, a look of such peace that those who saw it forgot, for a while, to be afraid."}, {"arc_end": 1}]),
                  C("[Keep it in my hands]", cond=F + "a_remember", do=[{"journal": F + "j_end_keep"}, {"card": "Lucy kept her father's letter in her hands. They found it there, pressed flat, when the tomb was opened, and Arthur, who never forgot the garden, did not take it. Some things, he said, should go where they were meant to."}, {"arc_end": 1}]),
                  ]),
)

# ----------------------------------------------------------------------------------------------------------- items
ITEMS = {
    F + "ink": dict(name="Inkwell", asset="bottle", variant="amber", desc="A squat bottle of black ink. Mamma says it is the Admiralty's, borrowed."),
    F + "paper": dict(name="Pad of letter-paper", asset="book", variant="leather", desc="Good cream paper from Mamma's escritoire. Rather too good for my writing."),
    F + "escritoire_key": dict(name="Escritoire key", asset="key", variant="gold", desc="A tiny brass key. It opens the walnut escritoire in the parlour."),
    F + "mina_letter": dict(name="Mina's last letter", asset="book", variant="diary", desc="'Begin with what you see out of the window; then the people in the house; then what you cannot tell anyone else; and last, your love.'"),
    F + "lilies": dict(name="White lilies", asset="garlic", variant="default", desc="Three tall white lilies. The back of the vase."),
    F + "forget_me_nots": dict(name="Forget-me-nots", asset="garlic", variant="default", desc="A fistful of small blue flowers. The front of the vase."),
    F + "bouquet": dict(name="Hillingham bouquet", asset="garlic", variant="default", desc="Lilies behind, the rose between, and a fringe of forget-me-nots in front. It is exactly right."),
    F + "arthur_letter": dict(name="Arthur's letter", asset="book", variant="diary", desc="'I am no hand at speeches. I only want to know whether I might hope, and I shall not mind a plain answer.'"),
    F + "seward_note": dict(name="Dr. Seward's note", asset="book", variant="leather", desc="'If I am to be refused, let it be plainly done. I could not bear to be managed, or kept dangling, or laughed at kindly.'"),
    F + "quincey_card": dict(name="Mr. Morris's card", asset="book", variant="red", desc="'Say it short, Miss Lucy, and say it to my face. I won't mind either, but I'd mind being talked round.'"),
    F + "ring": dict(name="Arthur's ring", asset="key", variant="gold", desc="His mother's ring: a small old band with a pale stone, a little too loose."),
    F + "pressed_letter": dict(name="Lucy's pressed-flower letter", asset="book", variant="diary", desc="My father's last letter, written when I was ten, with forget-me-nots pressed in every fold. It still smells faintly of summer."),
}

# ----------------------------------------------------------------------------------------------------------- journal
J = lambda title, text: dict(title=title, source="Lucy Westenra's diary", text=text)
JOURNAL = {
    F + "j_room": J("Hillingham in spring", "The window is open, there is a lawn outside it and three gentlemen coming to tea. I have never felt so bright in my life. Hannah says I am rosy, Mamma says I am tired, and the mirror says I look like a girl who has been told a secret."),
    F + "j_parlour": J("Mamma's parlour", "The parlour is chintz and bad piano music. Mamma has a theory about flowers and a larger one about gentlemen. I have decided to ignore both and arrange the vase myself."),
    F + "j_garden": J("The garden in May", "Lilies like bridesmaids, a sundial that counts only sunny hours, a bench in the shade. Dr. Seward left a note on it. I read it and pretended not to."),
    F + "j_flowers": J("Mamma is pleased", "Tallest at the back, the rose in the middle, forget-me-nots in front. Mamma wept a little, which is how she shows she is pleased, and handed me the key of the escritoire as though she were giving me the Crown jewels."),
    F + "j_mina_letter": J("Mina's letters", "A bundle of them in blue ribbon. She writes with a straight back, if letters can; every page begins with the weather and ends with love. I envy her, but only a little."),
    F + "j_seward": J("Dr. Seward", "He asked, and I refused, plainly, because he asked to be refused plainly. He took it like the good man he is, and asked if we might still be friends. I could have wept. He is the sort of man one wishes were one's brother."),
    F + "j_quincey": J("Mr. Morris", "He asked in four sentences and I answered in two. We shook hands like a pair of fellow-conspirators. He told me there was a gentleman behind the rose-bush who had been standing there half an hour. I am quite fond of him."),
    F + "j_arthur": J("Arthur", "Oh, my dear Arthur! He dropped his speech in the lilies and gave me his mother's ring instead. I said yes in the plainest words I knew. Why can't a girl marry three men? Jack to heal me, Quincey to defend me, Arthur to love me."),
    F + "j_letter": J("To Mina", "I wrote in order, as she told me: the window, the house, the secret, and the love. It is the first letter I have ever written without a postscript. She will read it on Friday and write me four pages by return, and I shall love every line."),
    F + "j_pack": J("Whitby", "Mamma wants sea air for me, Mina has taken the Crescent, and I am to bring my trunk and my appetite. The Hillingham lawn looked so well as I left it that I felt, for a moment, as if I were leaving a person."),
    F + "j_whitby": J("The Crescent lodgings", "Two beds under a sloping roof, a window full of sea and a landlady who has opinions about draughts. Mina has taken the bed nearest the door. She says it is for the light. I think it is for the key."),
    F + "j_lost": J("A letter lost", "Papa's letter has gone. I had it in my hand at Hillingham; I may have put it down anywhere in Whitby. If I find it I shall never put it down again. Mamma thinks the trunk, the window-seat, or the seat on the cliff."),
    F + "j_cliff": J("The East Cliff", "A churchyard over the sea, an Abbey over the churchyard, and a seat over everything. Mina writes. I watch the ships and the gulls and the great red sun. Everyone is kind. I am so tired, and I cannot think why."),
    F + "j_mina_walk": J("Mina's key", "Mina tells me I walked in my sleep last night. She found me at the window, in my nightgown, looking at the Abbey. I remember nothing. She has taken the key of our door and put it under her pillow, and she says she shall not sleep until I am well."),
    F + "j_swales": J("Mr. Swales and the steps", "A hundred and ninety-nine, he said. He has carried coffins on his shoulder down every one. It is a curious thing to know exactly how far it is from the cliff to the town. I shall remember it."),
    F + "j_night": J("The seat in the night", "I woke on the seat on the cliff. I did not walk there. There was a bell, and a man on the Abbey wall, tall and dark and red-eyed, watching me with the patience of the grave. I was not afraid. That was the terrible part."),
    F + "j_anchor_a": J("A name to hold", "I said 'Arthur,' and he flinched. Arthur's ring was cold in my hand, and his name was warm in my mouth, and for that moment I was Lucy Westenra and not a thing on a seat."),
    F + "j_anchor_m": J("Another name", "I said 'Mina.' Her letter was folded in four in my hand, and the first line was a rule for finding the way. Begin with what you see out of the window. I saw a Moon and a dark man and a path."),
    F + "j_anchor_p": J("A third name", "I said 'Papa.' I held his letter against my heart with its stiff old forget-me-nots, and the man on the seat looked at it and could not look at me."),
    F + "j_free": J("Walking away", "I turned my back on him and walked. It was the hardest thing I ever did. There was no footstep behind me. In front, the steps went down into the dark, and I went with three names in my mouth like pebbles."),
    F + "j_steps": J("The Abbey steps", "A hundred and ninety-nine steps in a nightgown, between graves, with the sea below and the bell behind. If I lose count I shall be on the cliff all night, and there will be nothing to hold me but the seat."),
    F + "j_counted": J("Counted", "One hundred and ninety-nine, aloud, as I would count Arthur's name. At the bottom, a lamp swung, and somebody ran toward me with a shawl and a plait of dark hair."),
    F + "j_mina_rescue": J("Mina found me", "She ran all the way in her dressing-gown. She said she woke and the key was under her pillow and the door was locked and I was gone. She has a gift for being right when I am wrong. I am so glad. I am so tired."),
    F + "j_last": J("September, Hillingham", "Home, and no better. The pallor has stayed. Dr. Seward sits with me, and Dr. Van Helsing, and Arthur comes when he can. Everyone is very kind, and everyone looks at me as though I were already a photograph. I do not want to be a photograph."),
    F + "j_a_release": J("To Arthur", "I wrote: 'Do not be small with grief. Live, and love again, when you can. I shall not mind.' It is the hardest line I have ever written. It is also the truest."),
    F + "j_a_remember": J("To Arthur", "I wrote: 'Remember me in the garden, with the rose in my hair, and be the man I knew.' He will do it. He does everything I ask, bless him, even when it hurts him."),
    F + "j_m_arthur": J("To Mina", "I wrote: 'Watch over Arthur for me; he does not know how to be alone.' She will. She keeps promises as she keeps her letters, in order and in blue ribbon."),
    F + "j_m_write": J("To Mina", "I wrote: 'Keep writing, everything you see, in order, as you taught me. One day someone will need it.' She has always written for the pleasure of it. I would like her to write for the use of it."),
    F + "j_end_arthur": J("What I left for Arthur", "Papa's letter, with the forget-me-nots, tied with the ring-ribbon. Arthur will understand. He always does, in the end."),
    F + "j_end_mina": J("What I left for Mina", "Papa's letter, tucked in with her own letters in blue ribbon. She keeps everything, and what she keeps, she keeps right."),
    F + "j_end_keep": J("What I kept", "I folded Papa's letter in my hands. If it is to be forgotten, let it be forgotten with me. The forget-me-nots, I think, will be glad of the company."),
}

# ----------------------------------------------------------------------------------------------------------- seed variation
PALETTES = {
    F + "room": [dict(wall="plaster", floor="planks", wood="pale", cloth="blue"), dict(wall="plaster", floor="planks", wood="oak", cloth="green")],
    F + "parlour": [dict(wall="plaster", floor="planks", wood="pale", cloth="green"), dict(wall="plaster", floor="planks", wood="dark", cloth="red")],
    F + "garden": [dict(wall="plaster", floor="grass", wood="pale", cloth="blue"), dict(wall="plaster", floor="grass", wood="oak", cloth="green")],
    F + "lodging": [dict(wall="plaster_dirty", floor="planks", wood="oak", cloth="blue"), dict(wall="plaster", floor="planks", wood="dark", cloth="green")],
    F + "last_room": [dict(wall="plaster", floor="planks", wood="pale", cloth="blue"), dict(wall="plaster_dirty", floor="planks", wood="oak", cloth="red")],
}

PLACEMENTS = {
    F + "pressed_letter": [
        dict(prop=F + "trunk", text="Under the last layer of tissue in the trunk, flat and a little crumpled, Papa's letter, where I put it so that nobody would sit on it.",
             hint="The trunk lid does not quite close."),
        dict(prop=F + "windowseat", text="Down the back of the cretonne window-seat, where I must have dropped it while watching the harbour: Papa's letter, safe.",
             hint="The cushion of the window-seat is rumpled, as though someone had searched it in a hurry."),
        dict(prop=F + "cliffseat", text="Tucked behind the board at the back of the cliff seat, damp at one corner but intact: Papa's letter, with its forget-me-nots.",
             hint="The cliff seat has a loose board at the back."),
    ],
}
