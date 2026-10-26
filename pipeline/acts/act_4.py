"""ACT IV - The Bloofer Lady (novel chapters 13-16).
Seward, Van Helsing, Arthur and Quincey: the Hampstead children, Mina's typed journal, the Westenra tomb at Kingstead,
the empty coffin, the night vigil and the laying to rest of Lucy. Exit: Act V (a5_asylum_library)."""
from dsl import *

ACT = dict(
    id=4, title="The Bloofer Lady",
    start=dict(location="a4_hampstead_heath", protagonist="seward", party=["seward", "vanhelsing"],
               items={"brandy": 1, "bandage": 1}, flags=[]),
    exit_to="a5_asylum_library",
)


# ----------------------------------------------------------------------------------------------- helpers
def N(speaker, text, *choices, next=None, do=None, end=False):
    d = dict(speaker=speaker, text=text)
    if do:
        d["do"] = do
    if choices:
        d["choices"] = list(choices)
    elif next:
        d["next"] = next
    elif end:
        d["end"] = True
    return d


def C(text, next=None, cond=None, do=None, end=False):
    d = dict(text=text)
    if next:
        d["next"] = next
    if cond:
        d["cond"] = cond
    if do:
        d["do"] = do
    if end or not next:
        d["end"] = True
    return d


def E(cond=None, once=True, do=None):
    d = {"once": once, "do": do or []}
    if cond:
        d["if"] = cond
    return d


def kid(n, s=0.62):
    n["scale"] = s
    return n


LEAVE = C("[Leave]")
S, VH, A, Q = "Dr. Seward", "Van Helsing", "Arthur Holmwood", "Quincey Morris"

# ----------------------------------------------------------------------------------------------- locations
LOCATIONS = [
    dict(id="a4_hampstead_heath", name="Hampstead Heath", date="26 September",
         desc="Furze, bracken and open sky. The Westminster Gazette speaks of a 'bloofer lady' who walks here after dark and leads small children away."),
    dict(id="a4_north_hospital", name="The North Hospital, children's ward",
         desc="White beds in a long ward. In one of them lies a small child with a bandaged throat."),
    dict(id="a4_seward_study", name="Dr. Seward's study, Purfleet", date="26 September, evening",
         desc="My own study at the asylum: the phonograph, the locked cabinet, and a workbench where I have mended many a lock for the sake of the patients."),
    dict(id="a4_paddington_hotel", name="Mina Harker's sitting-room, Paddington", date="25-26 September",
         desc="A modest hotel parlour, a typewriter on a writing-table, a basket of sewing, and two people who have lately been very near to ruin."),
    dict(id="a4_hillingham_hall", name="Hillingham, the Westenra house",
         desc="The house is quiet. White flowers have not yet been cleared from the room where Lucy lay, and the smell of wild garlic still clings to the curtains."),
    dict(id="a4_jack_straws", name="Jack Straw's Castle",
         desc="A roadside inn on the top of the Heath. A fire, a long table, a landlord who has seen worse doctors than us."),
    dict(id="a4_heath_lane", name="Heath lane by night",
         desc="A dark lane between hedges. Lamps stand far apart. Somewhere beyond the trees the church of Kingstead keeps its watch."),
    dict(id="a4_kingstead_gate", name="Kingstead churchyard, the lych-gate",
         desc="A low stone wall, a lych-gate, a notice board with the plan of the graves, and a sexton's lodge that smells of onions."),
    dict(id="a4_kingstead_churchyard", name="Kingstead churchyard, by night",
         desc="An avenue of yews, junipers marking the church path, a clump of alders, railed-off tombs ghastly white in the moonlight."),
    dict(id="a4_westenra_tomb", name="The Westenra tomb",
         desc="A marble vault, damp and sordid. Coffins on shelves, withered flowers, iron gone to rust. Lucy's lead-cased coffin rests at the far end."),
]


def pines(seed, n=22, avoid=None, asset="pine", variant="dark"):
    return dict(asset=asset, variant=variant, count=n, seed=seed, avoid=avoid or [[-4, -3, 4, 4]])


LOC_DATA = {}

# ---------------------------------------------------------------- 1. Hampstead Heath (start)
LOC_DATA["a4_hampstead_heath"] = dict(
    cells=[4, 3], interior=False, wall="dirt", floor="grass",
    ambient=AMBIENT["day_exterior"], camera=cam([4, 3]), lights=lights_day(),
    scatter=pines(21, 24, [[-8, -6, 8, 6]], "pine", "green"),
    scatter2=dict(asset="rock", variant="mossy", count=8, seed=4, avoid=[[-8, -6, 8, 6]]),
    spawn=[5.6, 3.0], spawns={"a4_north_hospital": [5.2, -1.6], "a4_seward_study": [5.6, 3.0],
                              "a4_jack_straws": [-5.4, -2.4], "a4_heath_lane": [1.0, -4.0]},
    props=[
        prop("a4_heath_bench", "bench", "dark", -5.4, -2.4, rot=90, name="The Professor's bench", radius=0.6,
             look="Van Helsing sits here with his chin on his stick, studying the grass as other men study a text.",
             talk="a4_vh_heath"),
        prop("a4_heath_lamp", "lantern", "default", -2.2, -4.4, name="Heath lamp", radius=0.3,
             look="A lamp-post standing alone on the Heath, unlit by day, as useful to a child as a church to a heathen."),
        prop("a4_clue_hollow", "rock", "mossy", 2.6, -3.4, name="Hollow under the gorse", radius=0.5,
             look="A hollow where bracken is flattened. Something small and red shows under the furze: a child's shoe, with its strap torn.",
             set="a4_clue_shoe", set_text="A child's red shoe, the strap torn through. It is smaller than my hand. I mark the place."),
        prop("a4_clue_bushes", "pine_small", "dark", -1.6, 2.6, name="Thorn bushes", radius=0.5,
             look="A thorn bush by the path. A thread of white lawn cloth has caught on it, fine as a gentlewoman's linen.",
             set="a4_clue_thread", set_text="White lawn, fine and old, no peasant's cloth. A winding-sheet might look so. I do not like where my thoughts go."),
        prop("a4_clue_trail", "rock", "grey", 4.6, 0.6, name="Trampled bracken", radius=0.5,
             look="A line of broken bracken crossing the slope, and in the soft earth the prints of bare, narrow feet heading north.",
             set="a4_clue_prints", set_text="Bare footprints, a woman's, pointing toward the church at Kingstead. They stop at the road; she walked on the grass."),
        prop("a4_heath_gorse", "pine_small", "green", -6.2, 3.8, radius=0.5),
        prop("a4_heath_fence", "fence", "default", 0.5, 4.8, radius=0.5),
        prop("a4_heath_rock", "rock_big", "mossy", 6.4, -4.6, radius=0.8),
        prop("a4_to_hospital", "carriage", "dark", 6.2, -2.6, rot=-90, name="Cab to the North Hospital", radius=1.6,
             look="A hansom waits at the roadside to carry us to the North Hospital, where the child lies.",
             go="a4_north_hospital", go_cond="has:a4_gazette&flag:a4_deduced_kingstead",
             go_fail="I should first buy the Gazette and read it, and Van Helsing wants to settle where this trail leads."),
        prop("a4_to_study", "signpost", "dark", 6.4, 3.4, name="Road to Purfleet", radius=0.3,
             look="The long road back to my asylum at Purfleet.", go="a4_seward_study", go_cond="flag:a4_saw_wound",
             go_fail="Not yet. I must see the child's wound with my own eyes before I let the Professor's theory rest."),
        prop("a4_to_inn", "door", "dark", -6.6, -0.2, rot=90, name="Jack Straw's Castle", radius=0.6,
             look="The door of the inn on the crown of the Heath.", go="a4_jack_straws", go_cond="flag:a4_seward_convinced",
             go_fail="There is nothing to be done at the inn until the Professor and I are of one mind."),
        prop("a4_to_lane", "signpost", "oak", 1.0, -5.2, name="Path to Kingstead", radius=0.3,
             look="The narrow path that runs north over the Heath toward the church of Kingstead.",
             go="a4_heath_lane", go_cond="flag:a4_dined", go_fail="It is too early. We must first dine and make our plans."),
    ],
    npcs=[
        npc("a4_newsboy", "human_peasant_m", "villager", 5.0, -0.6, rot=-90, name="Newsboy", radius=0.5,
            look="A thin lad with a satchel of papers and a loud voice.", talk="a4_newsboy"),
        npc("a4_nursemaid", "human_peasant_f", "village_woman", -3.8, 1.4, rot=90, name="Nursemaid", radius=0.5,
            look="A woman in a grey shawl, one eye always on the children, the other on a policeman.", talk="a4_nursemaid"),
        kid(npc("a4_children", "human_peasant_f", "innkeeper_wife", -2.6, 2.4, rot=60, name="Children playing", radius=0.4,
                look="Two small children playing at being the 'bloofer lady' and the baby she takes away.", talk="a4_children")),
        npc("a4_constable", "human_peasant_m", "innkeeper", 0.8, -3.4, rot=0, name="Constable", radius=0.5,
            look="A tall constable with a notebook, leaning against a rail and tired of questions.", talk="a4_constable"),
    ],
    on_enter=[E(do=[
        {"say": "26 September. The Westminster Gazette tells of children lured away on the Heath by a 'bloofer lady' and found with small wounds on the throat. Van Helsing read it on the platform and turned white. He will not say why."},
        {"journal": "a4_j_heath"}])],
)

# ---------------------------------------------------------------- 2. North Hospital
LOC_DATA["a4_north_hospital"] = dict(
    cells=[3, 3], interior=True, wall="plaster", floor="planks",
    ambient=AMBIENT["warm_day_interior"], camera=cam([3, 3]), lights=lights_warm([3, 3]),
    walls=dict(north=["wall_window_4", "wall_4", "wall_window_4"], west=["wall_4", "wall_4", "wall_4"],
               east=["wall_4", "wall_4", "wall_door_4"]),
    spawn=[4.4, 3.4], spawns={"a4_hampstead_heath": [4.4, 3.4]},
    props=[
        prop("a4_bed1", "bed_simple", "blue", -4.2, -3.4, rot=90, name="Empty cot", radius=0.9, look="A neatly made cot. Its small occupant went home this morning."),
        prop("a4_bed2", "bed_simple", "blue", -4.2, 0.0, rot=90, name="The child's cot", radius=0.9,
             look="A small child lies here, white as the sheet, a bandage at the throat."),
        prop("a4_bed3", "bed_simple", "blue", -4.2, 3.4, rot=90, name="Cot", radius=0.9, look="A sleeping boy with a bandaged hand. He knocked over a lamp, they say."),
        prop("a4_ward_cabinet", "bookshelf", "pale", 0.0, -5.3, name="Dispensary cabinet", radius=0.6,
             look="Bottles of carbolic, lint and linseed. Nothing here for a wound that will not heal."),
        prop("a4_ward_table", "table", "pale", 2.8, -3.8, name="Matron's table", radius=0.8,
             look="A table with the ward register open upon it."),
        prop("a4_ward_register", "book", "red", 2.8, -3.8, y=0.8, name="Admission register", radius=0.2,
             look="Admitted Tuesday, 4 a.m., found on the Heath near Shooter's Hill, laid on the grass 'as one lays a doll'. The same hour as the last two cases."),
        prop("a4_ward_lamp", "lantern", "default", 2.0, 0.6, name="Ward lamp", radius=0.3, look="A brass lamp turned low for the night nurse."),
        prop("a4_ward_stove", "fireplace", "plaster", 5.3, -2.0, rot=-90, name="Ward stove", radius=0.7, look="A stove warmed against the autumn. The ward smells of carbolic and boiled milk."),
        prop("a4_ward_chair", "chair", "blue", -1.8, 2.2, rot=90, name="Visitor's chair", radius=0.4, look="A chair for the mother who has not come."),
        prop("a4_ward_rug", "rug", "cream", 0.2, 1.2, radius=0.2),
        prop("a4_ward_candle", "candle", "white", -2.4, -5.0, radius=0.1),
        prop("a4_hosp_door", "door", "pale", 5.8, 4.0, rot=-90, name="Door to the street", radius=0.6, look="The way back to the Heath.", go="a4_hampstead_heath"),
    ],
    npcs=[
        npc("a4_vincent", "human_seward", "doctor", -1.4, -1.0, rot=90, name="Dr. Vincent", radius=0.5,
            look="The house surgeon, a young man with ink on his cuffs and no patience for fools or professors.", talk="a4_vincent"),
        kid(npc("a4_tuesday", "human_peasant_f", "innkeeper_wife", -4.2, 0.0, rot=90, name="The child", radius=0.4,
                look="A small girl propped on pillows, watching me with solemn eyes.", talk="a4_tuesday"), 0.55),
        npc("a4_ward_sister", "human_peasant_f", "village_woman", 1.2, 2.4, rot=180, name="Ward sister", radius=0.5,
            look="A sister in starched cap, carrying linen as if it were a standard.", talk="a4_ward_sister"),
    ],
)

# ---------------------------------------------------------------- 3. Seward's study
LOC_DATA["a4_seward_study"] = dict(
    cells=[3, 2], interior=True, wall="plaster_dirty", floor="planks",
    ambient=AMBIENT["candle_interior"], camera=cam([3, 2]), lights=lights_warm([3, 2]),
    walls=dict(north=["wall_door_4", "wall_door_4", "wall_door_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_4"]),
    spawn=[0.0, 2.2], spawns={"a4_hampstead_heath": [-4.0, -2.4], "a4_paddington_hotel": [4.0, -2.4], "a4_hillingham_hall": [0.0, -2.4]},
    props=[
        prop("a4_study_to_heath", "door", "dark", -4.0, -3.8, name="Hansom for Hampstead", radius=0.6,
             look="The door to the hall, and the cab that will carry us back to the Heath.", go="a4_hampstead_heath"),
        prop("a4_study_to_hillingham", "door", "dark", 0.0, -3.8, name="Hansom for Hillingham", radius=0.6,
             look="The cab for Hillingham, where Lucy's papers still lie.", go="a4_hillingham_hall", go_cond="flag:a4_seward_convinced",
             go_fail="Hillingham can wait; first I must be of one mind with the Professor."),
        prop("a4_study_to_hotel", "door", "dark", 4.0, -3.8, name="Hansom for Paddington", radius=0.6,
             look="The cab for the railway station and Mrs Harker's hotel.", go="a4_paddington_hotel", go_cond="flag:a4_vh_goes_paddington",
             go_fail="There is no reason yet to go to Paddington."),
        prop("a4_study_fire", "fireplace", "soot", 5.4, 0.4, rot=-90, name="Van Helsing by the fire", radius=0.8,
             look="The Professor stands with his hands to the blaze, watching me as one watches a patient who refuses a draught.",
             talk="a4_seward_vh_doubt"),
        prop("a4_study_desk", "table", "ebony", 3.4, 1.6, name="My desk", radius=0.9,
             look="My desk: the diary on the phonograph cylinders, a half-written case note, and a cold cup of tea."),
        prop("a4_study_chair", "chair", "black", 3.4, 2.8, rot=180, name="Desk chair", radius=0.4, look="Worn to the shape of an anxious man."),
        prop("a4_study_shelf", "bookshelf", "dark", -5.3, -0.8, rot=90, name="Bookshelf", radius=0.7,
             look="Medical texts and, between Gray and Bucknill, a trade catalogue: 'Chubb's Locks'. A page is turned down: falling-bolt locks, four and six levers, against spring latches.",
             set="a4_read_chubb", set_text="Chubb's catalogue. A falling-bolt lock drops its bolt by its own weight and can be opened from within; a spring latch shuts itself and cannot. Tombs in the old style are fitted with the first. Four levers or six, according to the price."),
        prop("a4_workbench", "table", "dark", -3.4, 1.8, name="Locksmith's bench", radius=0.9,
             look="My bench. I learned to cut keys as a student to help a locked-up uncle; the asylum has since put the skill to many uses.",
             talk="a4_workbench"),
        prop("a4_bench_vice", "hammer", "default", -3.4, 1.8, y=0.8, radius=0.1),
        prop("a4_key_drawer", "chest", "dark", -5.0, 2.6, rot=90, name="Drawer of blanks", radius=0.6,
             look="A drawer of key blanks, odd wards, and a rusty file."),
        prop("a4_key_tin", "bottle", "amber", -1.8, 2.4, name="Biscuit tin of keys", radius=0.3,
             look="An old biscuit tin of keys that belong to nothing I own."),
        prop("a4_key_desk_blot", "book", "diary", 3.4, 1.6, y=0.8, name="Blotter", radius=0.2,
             look="The blotter, full of ink and half-formed doubts."),
        prop("a4_black_bag", "chest", "ebony", 1.4, 2.2, name="Van Helsing's black bag", radius=0.5,
             look="The Professor's bag: it clinks in a way that has nothing to do with surgery.", talk="a4_vh_bag"),
        prop("a4_surgical_case", "chest", "pale", -0.4, 2.0, name="My post-mortem case", radius=0.5,
             look="My own case of post-mortem knives. He asked for it at Hillingham, and I did not ask why.",
             take="a4_surgical_knives", take_text="I took the case of knives. I pray God I never put them to the use I fear.", give_once=True),
        prop("a4_study_rug", "rug", "blue", 0.0, 0.6, radius=0.2),
        prop("a4_study_candle", "candelabra", "default", 2.0, -1.0, radius=0.2),
        prop("a4_tool_chest", "chest", "oak", -1.4, -2.2, name="Tool chest", radius=0.6,
             look="The asylum's tool chest: saws, a mallet, a hammer for the loose boards.",
             take="hammer", take_text="I took the heavy hammer. It will drive a stake or a nail equally.", give_once=True),
    ],
    on_enter=[
        E(cond="has:a4_typed_journal&flag:a4_jonathan_cured", once=True, do=[
            {"protagonist": "seward"},
            {"say": "Back at Purfleet with Mrs Harker's typed pages and Harker's own word that he did not dream. The Professor wants me to read them now."}]),
        E(cond="flag:a4_saw_wound", once=True, do=[
            {"say": "Evening at Purfleet. The Professor has said nothing the whole way home, and I have said nothing back."}]),
    ],
)

# ---------------------------------------------------------------- 4. Paddington hotel (Mina / Jonathan)
LOC_DATA["a4_paddington_hotel"] = dict(
    cells=[3, 2], interior=True, wall="plaster", floor="planks",
    ambient=AMBIENT["warm_day_interior"], camera=cam([3, 2]), lights=lights_warm([3, 2]),
    walls=dict(north=["wall_window_4", "wall_4", "wall_window_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[4.0, 2.0], spawns={"a4_seward_study": [4.4, 2.0]},
    props=[
        prop("a4_type_table", "table", "pale", -3.6, -1.6, name="Mina's writing-table", radius=0.9, cond="!a4_ribbon_fitted",
             look="Mina's typewriter stands here, its ribbon worn grey and faint. A folded shawl lies next to it.",
             use_item={"a4_ribbon": [{"take": "a4_ribbon"}, {"set": "a4_ribbon_fitted"},
                                     {"say": "I wound the fresh ribbon onto the spools. The keys strike black and clean."}]},
             use_fail="That will not mend the typewriter."),
        prop("a4_type_machine", "table", "pale", -3.6, -1.6, name="Typewriter, new ribbon", radius=0.9, cond="a4_ribbon_fitted",
             look="The machine is ready, the paper rolled in. Mina's shorthand diary would go well on it.",
             use_item={"a4_shorthand_diary": [{"give": "a4_typed_journal"}, {"journal": "a4_j_typed"},
                                              {"say": "Mina's fingers fly where mine stumble. In an hour the shorthand lies in clean black type: the whole of the foreign journal."}]},
             use_fail="There is nothing here to type."),
        prop("a4_workbasket", "chest", "pale", -1.2, 2.6, name="Mina's workbasket", radius=0.5,
             look="Thread, a thimble, a half-darned stocking, and a spare typewriter ribbon in blue paper.",
             take="a4_ribbon", take_text="A spare ribbon, still in its paper. Mina would not mind.", give_once=True),
        prop("a4_hotel_sofa", "bed_simple", "green", 3.0, -1.6, rot=-90, name="Sofa", radius=0.9, look="A sofa where Jonathan sits when he is not walking up and down."),
        prop("a4_timetable", "book", "red", 0.6, -1.6, y=0.8, name="Bradshaw's timetable", radius=0.2,
             look="Mina has marked the Exeter trains in pencil. 'Quick 3.34, change at Reading.'"),
        prop("a4_hotel_table2", "table", "pale", 0.6, -1.6, radius=0.7),
        prop("a4_hotel_fire", "fireplace", "plaster", -5.3, 1.2, rot=90, name="Small grate", radius=0.6, look="A small coal fire, politely lit."),
        prop("a4_hotel_chair", "chair", "green", 0.6, 1.4, rot=180, name="Chair", radius=0.4, look="A plain hotel chair."),
        prop("a4_hotel_rug", "rug", "cream", 0.0, 0.2, radius=0.2),
        prop("a4_hotel_lamp", "lantern", "default", 4.6, -2.4, name="Lamp", radius=0.3, look="An oil lamp, wick trimmed."),
        prop("a4_hotel_door", "door", "pale", 5.8, 2.0, rot=-90, name="Door to the corridor", radius=0.6, look="The hotel corridor, and the cab back to Purfleet.",
             go="a4_seward_study", go_cond="flag:a4_jonathan_cured&has:a4_typed_journal",
             go_fail="I have not finished here. I must hear Harker and Mrs Harker, and carry back the typed pages."),
    ],
    npcs=[
        npc("a4_mina", "human_mina", "mina", -2.0, 0.6, rot=180, name="Mina Harker", radius=0.5,
            look="Mina, pale and composed, has the look of a woman who has lately been very frightened and has decided to be useful.", talk="a4_mina_talk"),
        npc("a4_jonathan", "human_harker", "harker", 2.8, 0.8, rot=-90, name="Jonathan Harker", radius=0.5,
            look="Jonathan's hair is white at the temples. He looks twenty years older than the photograph on Mina's table.", talk="a4_jonathan_talk"),
    ],
    on_enter=[E(do=[
        {"protagonist": "vanhelsing"},
        {"say": "The Exeter note found me out, and so has the Paddington hotel. A young woman who has typed out a dead man's journals and a living man's nightmares: I take off my hat to her."},
        {"journal": "a4_j_mina"}])],
)

# ---------------------------------------------------------------- 5. Hillingham
LOC_DATA["a4_hillingham_hall"] = dict(
    cells=[3, 3], interior=True, wall="plaster", floor="planks",
    ambient=AMBIENT["candle_interior"], camera=cam([3, 3]), lights=lights_warm([3, 3]),
    walls=dict(north=["wall_window_4", "wall_4", "wall_window_4"], west=["wall_4", "wall_door_4", "wall_4"],
               east=["wall_4", "wall_door_4", "wall_4"]),
    spawn=[-4.4, 0.0], spawns={"a4_seward_study": [-4.4, 0.0], "a4_kingstead_gate": [4.4, 0.0]},
    props=[
        prop("a4_hill_to_study", "door", "pale", -5.8, 0.0, rot=90, name="Door to the hall", radius=0.6, look="The way to the front door and the cab for Purfleet.", go="a4_seward_study"),
        prop("a4_hill_to_gate", "door", "pale", 5.8, 0.0, rot=-90, name="Door to the carriage drive", radius=0.6, look="A cab waits for the road to Kingstead.", go="a4_kingstead_gate"),
        prop("a4_bier", "bed", "black", 0.0, -2.2, name="The bier", radius=1.0,
             look="The bed where Lucy lay, now stripped, with a tarnished outline of lilies still on the pillow."),
        prop("a4_wake_candles", "candelabra", "default", -2.0, -2.6, name="Tall wax candles", radius=0.3, look="Four tall candles, burnt to stubs. Nobody has dared to remove them."),
        prop("a4_wake_candles2", "candelabra", "default", 2.0, -2.6, radius=0.3),
        prop("a4_garlic_box", "chest", "pale", -4.2, -4.4, name="Box of wild garlic", radius=0.5,
             look="The box that came from Haarlem, addressed by the Professor: a mass of wild garlic flowers, heavy as sin.",
             take="garlic", take_text="I took a handful of the white flowers. The smell makes my eyes run.", give_once=True),
        prop("a4_garlic_vase1", "garlic", "default", -1.2, -4.6, name="Garlic in a vase", radius=0.2,
             look="Sprigs of garlic stuck into a vase beside the window.", take="garlic", take_text="I took the sprigs.", give_once=True),
        prop("a4_garlic_vase2", "garlic", "default", 4.2, -4.4, name="Garlic at the window", radius=0.2,
             look="A bunch tied with ribbon to the window latch.", take="garlic", take_text="I untied the bunch.", give_once=True),
        prop("a4_lucy_desk", "table", "oak", 3.4, -2.8, name="Lucy's writing desk", radius=0.8,
             look="A pretty desk with papers in neat stacks: Mrs Westenra's accounts, Lucy's letters, bills from the undertaker.",
             talk="a4_papers"),
        prop("a4_hall_rug", "rug", "red", 0.8, 1.6, name="Hall rug", radius=0.6, look="A thick Turkey rug, one corner turned up as if someone stepped on it in haste."),
        prop("a4_hall_bookshelf", "bookshelf", "oak", 5.2, 3.8, rot=-90, name="Mrs Westenra's bookshelf", radius=0.6,
             look="Novels, a Book of Common Prayer, the Peerage. Nothing that would help us."),
        prop("a4_kindling", "fireplace", "plaster", -5.3, -3.8, rot=90, name="Fireplace", radius=0.7,
             look="A basket of ash kindling beside the cold grate, from the garden pruning.",
             take="wood", take_text="I took a good length of ash kindling. A carpenter could make something of it.", give_once=True),
        prop("a4_letter_knife", "key", "default", 3.4, -2.8, y=0.8, name="Paper knife", radius=0.1,
             look="A bone-handled paper knife, keen enough to trim a quill or a vein.",
             take="knife", take_text="I pocketed the paper knife.", give_once=True),
        prop("a4_undertaker_coffin", "coffin", "dark", 3.8, 3.6, rot=90, name="Undertaker's sample coffin", radius=0.8,
             look="The undertaker left a pattern coffin in the hall. Lead lining, oak outer, brass handles."),
        prop("a4_vh_case", "chest", "ebony", 4.4, 1.2, name="Van Helsing's travelling case", radius=0.5, cond="flag:a4_party_assembled",
             look="The Professor's case. Inside lies the tin that came from Amsterdam.", talk="a4_vh_prep"),
    ],
    npcs=[
        npc("a4_maid", "human_peasant_f", "village_woman", -3.2, 3.2, rot=0, name="Hannah the maid", radius=0.5,
            look="A young maid with red eyes who dusts the same shelf again and again.", talk="a4_maid_talk"),
        npc("a4_marquand", "human_peasant_m", "villager", 2.4, 2.2, rot=180, name="Mr. Marquand", radius=0.5,
            look="The family solicitor, in a black coat and an air of professional sorrow, with his hat held like a shield.", talk="a4_marquand"),
        npc("a4_arthur", "human_arthur", "lord", 0.4, 3.6, rot=180, name="Arthur Holmwood", radius=0.5, cond="flag:a4_lucy_sleeping",
            look="Arthur sits with his face in his hands. He has not shaved in three days.", talk="a4_arthur_grief"),
        npc("a4_quincey", "human_quincey", "texan", -1.2, 3.8, rot=180, name="Quincey P. Morris", radius=0.5, cond="flag:a4_lucy_sleeping",
            look="Quincey leans on the mantel, slowly rolling a cigarette he does not light.", talk="a4_quincey_talk"),
    ],
    on_enter=[E(cond="flag:a4_lucy_sleeping", once=True, do=[
        {"say": "29 September. Hillingham again. Arthur has come up from Ring and will not let the Professor out of his sight."}])],
)

# ---------------------------------------------------------------- 6. Jack Straw's Castle
LOC_DATA["a4_jack_straws"] = dict(
    cells=[3, 2], interior=True, wall="plaster_dirty", floor="planks",
    ambient=AMBIENT["candle_interior"], camera=cam([3, 2]), lights=lights_warm([3, 2]),
    walls=dict(north=["wall_4", "wall_window_4", "wall_4"], west=["wall_4", "wall_door_4"], east=["wall_4", "wall_4"]),
    spawn=[-4.4, 2.0], spawns={"a4_hampstead_heath": [-4.4, 2.0]},
    props=[
        prop("a4_inn_door", "door", "dark", -5.8, 2.0, rot=90, name="Door to the Heath", radius=0.6, look="The inn door, with a bell that rings once when it opens.", go="a4_hampstead_heath"),
        prop("a4_inn_table", "table_long", "dark", 0.0, -0.6, name="Dinner table", radius=2.0,
             look="A long table with a cold joint, bread and a stone jug of ale. The Professor is already carving.", talk="a4_vh_dinner"),
        prop("a4_inn_bench1", "bench", "dark", 0.0, 0.7, rot=180, radius=0.5),
        prop("a4_inn_bench2", "bench", "dark", 0.0, -1.9, rot=0, radius=0.5),
        prop("a4_inn_fire", "fireplace", "soot", -3.8, -3.4, name="Great hearth", radius=0.9, look="A fire where a whole sheep could be roasted. It throws shadows like the wings of bats."),
        prop("a4_inn_barrel", "barrel", "oak", 4.6, -2.8, name="Ale barrel", radius=0.4, look="A cask of the landlord's best. A coil of good hemp rope hangs behind it.",
             take="rope", take_text="Behind the barrel hangs a coil of good hemp rope. I take it.", give_once=True),
        prop("a4_inn_counter", "table", "dark", 4.2, 0.6, name="Bar counter", radius=0.8, look="A rack of pewter pots, a ledger and a jar of loose change."),
        prop("a4_inn_tip", "goblet", "default", 4.2, 0.6, y=0.8, name="Tip jar", radius=0.1, look="A pewter cup holding a few coins.",
             take="silver", take_text="The landlord nods: a silver coin is mine to borrow.", give_once=True),
        prop("a4_inn_lamp", "lantern", "default", 3.0, -2.6, name="Hanging lamp", radius=0.3,
             look="A good oil lantern with a slide that opens and closes the light.",
             take="a4_oil_lamp", take_text="The landlord sells me the lamp for a florin.", give_once=True),
        prop("a4_inn_matches", "candle", "white", -1.4, 2.4, name="Candle ends and matches", radius=0.2,
             look="A box of lucifer matches and a handful of candle-ends.",
             take="a4_matches", take_text="I pocketed the matches.", give_once=True),
        prop("a4_inn_water", "bottle", "glass", 1.4, 2.4, name="Water jug", radius=0.2, look="A stone jug of spring water.",
             take="water", take_text="I filled a flask.", give_once=True),
        prop("a4_inn_map", "book", "leather", 2.4, -1.4, y=0.8, name="Survey map of the Heath", radius=0.2,
             look="An Ordnance sheet: the lanes, the Spaniards, Hampstead Lane, Kingstead church. A pencil line marks a horse patrol on the high road at half-past ten.",
             set="a4_read_map", set_text="The map marks the patrol on the high road. The Heath path by Hampstead Lane is shown unpatrolled, if dark."),
        prop("a4_inn_window", "candelabra", "default", 0.0, -3.4, radius=0.2),
    ],
    npcs=[
        npc("a4_landlord", "human_peasant_m", "innkeeper", 3.2, 2.0, rot=180, name="The landlord", radius=0.5,
            look="A square man in a leather apron who has served nightmen, resurrection men and doctors without a change of expression.", talk="a4_landlord"),
        npc("a4_patron", "human_peasant_m", "szgany", -3.2, 0.6, rot=90, name="A late carter", radius=0.5,
            look="A carter nursing a mug of ale and a grievance.", talk="a4_patron"),
    ],
)

# ---------------------------------------------------------------- 7. Heath lane by night
LOC_DATA["a4_heath_lane"] = dict(
    cells=[3, 2], interior=False, wall="dirt", floor="dirt",
    ambient=AMBIENT["night_exterior"], camera=cam([3, 2]), lights=lights_moon(), moon=dict(pos=[-12, 16, -20]),
    scatter=pines(33, 22, [[-6, -4, 6, 4]]), scatter2=dict(asset="rock", variant="dark", count=6, seed=9, avoid=[[-6, -4, 6, 4]]),
    spawn=[-4.8, 0.0], spawns={"a4_hampstead_heath": [-4.8, 0.0], "a4_kingstead_gate": [4.8, 0.0]},
    props=[
        prop("a4_lane_west", "signpost", "dark", -5.2, 0.0, name="Path to the Heath", radius=0.3, look="Back to the Heath and Jack Straw's.", go="a4_hampstead_heath"),
        prop("a4_lane_east", "signpost", "dark", 5.2, 0.0, name="To Kingstead churchyard", radius=0.3, look="The lane toward the lych-gate of Kingstead.", go="a4_kingstead_gate"),
        prop("a4_lane_lamp1", "lantern", "default", -2.4, -2.6, name="Lamp", radius=0.3, look="A lamp that gives light to itself and little else."),
        prop("a4_lane_lamp2", "lantern", "default", 2.2, 2.4, name="Lamp", radius=0.3, look="The patrol's lamp on the corner; the policeman stands under it on his round."),
        prop("a4_handoff_spot", "bench", "dark", 0.0, -1.8, name="Bench under the lamp", radius=0.7,
             look="A bench under the lamp where the policeman's beat comes round. A child laid here would be found within minutes.",
             talk="a4_handoff"),
        prop("a4_lane_hedge1", "fence", "default", -3.6, 2.6, radius=0.5),
        prop("a4_lane_hedge2", "fence", "default", 3.6, -2.8, radius=0.5),
        prop("a4_lane_stone", "rock", "dark", 0.8, 2.6, name="Milestone", radius=0.4, look="'Kingstead, 1 mile.'"),
    ],
    npcs=[
        npc("a4_patrol", "human_peasant_m", "innkeeper", 1.8, -0.8, rot=-90, name="The constable on his round", radius=0.5, cond="flag:a4_child_returned",
            look="The constable finds the child by the lantern's beam and bends to it, fumbling for his whistle.", talk="a4_patrol"),
    ],
    on_enter=[E(cond="flag:a4_child_with_us", once=True, do=[
        {"say": "Midnight is long gone. The child in my arms is breathing, and its throat bears two tiny marks. The patrol lamp is just ahead."}])],
)

# ---------------------------------------------------------------- 8. Kingstead gate (day / dusk)
LOC_DATA["a4_kingstead_gate"] = dict(
    cells=[4, 3], interior=False, wall="dirt", floor="grass",
    ambient=AMBIENT["dusk_exterior"], camera=cam([4, 3]), lights=lights_day(2.2),
    scatter=pines(41, 22, [[-8, -6, 8, 6]]), scatter2=dict(asset="gravestone", variant="stone_mossy", count=10, seed=6, avoid=[[-8, -6, 8, 6]]),
    spawn=[0.0, 4.2], spawns={"a4_heath_lane": [-6.0, 3.0], "a4_kingstead_churchyard": [0.0, -3.4], "a4_hillingham_hall": [6.0, 1.6]},
    props=[
        prop("a4_lych_gate", "arch", "stone_grey", 0.0, -4.6, radius=0.3),
        prop("a4_wicket", "door", "dark", 0.0, -4.5, name="Iron wicket", radius=0.6,
             look="A small iron wicket let into the churchyard wall. The sexton locks it at dusk.",
             go="a4_kingstead_churchyard", go_cond="flag:a4_wicket_open",
             go_fail="The wicket is locked, and the sexton has the key on his belt. I should speak to him, or find another way in."),
        prop("a4_wall1", "fence", "default", -3.6, -4.4, radius=0.5),
        prop("a4_wall2", "fence", "default", 3.6, -4.4, radius=0.5),
        prop("a4_wall3", "fence", "default", -6.4, -4.4, radius=0.5),
        prop("a4_wall4", "fence", "default", 6.4, -4.4, radius=0.5),
        prop("a4_plan_board", "signpost", "oak", 3.2, -2.8, name="Plan of the churchyard", radius=0.3,
             look="A board with the plan of Kingstead churchyard: the church path flanked by junipers, an avenue of yews going north, an alder clump in the north-west corner, railed tombs along the east. The Westenra vault stands at the head of the avenue. A hand has written beneath: 'Gate locked at dusk.'",
             set="a4_read_plan", set_text="I trace the plan with a finger: wicket, yew avenue, vault at the head; the alder clump near the north wall would hide four men. The sexton locks the main gate but the wicket opens from inside."),
        prop("a4_shed_putty", "chest", "oak", -6.0, -2.0, name="Glazier's box", radius=0.5,
             look="A glazier's box left by the church repairs, with a tub of soft putty.",
             take="a4_putty", take_text="I took a ball of the glazier's putty. It has many uses.", give_once=True),
        prop("a4_shed_plumber", "chest", "dark", -6.0, 0.4, name="Plumber's bag", radius=0.5,
             look="A plumber's bag, left for the vestry roof: a soldering iron, a stick of solder and a pot of flux.",
             take="a4_soldering_iron", take_text="I took the soldering iron.", give_once=True),
        prop("a4_shed_solder", "key", "default", -4.6, 0.4, y=0.0, name="Stick of solder", radius=0.2,
             look="A stick of plumber's solder, dull grey, forgotten on a stone.", take="a4_solder", take_text="I took the solder.", give_once=True),
        prop("a4_gate_bench", "bench", "pale", -3.2, 2.4, rot=90, name="Churchyard seat", radius=0.6, look="A seat for mourners. Its arm is carved with initials."),
        prop("a4_gate_tomb", "tomb", "stone_grey", 5.6, -1.6, name="Hollis family tomb", radius=1.2, look="The Hollis family tomb: weather-stained, mean-looking in the failing sun."),
        prop("a4_gate_to_lane", "signpost", "dark", -6.6, 3.4, name="Lane to Hampstead", radius=0.3, look="The lane back toward the Heath.", go="a4_heath_lane"),
        prop("a4_gate_cab", "carriage", "dark", 6.4, 2.6, rot=-90, name="Hansom for Hillingham", radius=1.6, look="A hansom waits, the driver dozing.",
             go="a4_hillingham_hall", go_cond="flag:a4_lucy_sleeping",
             go_fail="There is nothing for me at Hillingham until I know what we are to tell Arthur."),
    ],
    npcs=[
        npc("a4_sexton", "human_peasant_m", "villager", -1.6, -2.0, rot=180, name="The sexton", radius=0.5,
            look="A stooped man with a heavy ring of keys and a long nose reddened by weather and gin.", talk="a4_sexton"),
        npc("a4_cabman", "human_coachman", "driver", 5.2, 3.6, rot=-90, name="Cabman", radius=0.6,
            look="A sleepy cabman with a muffler over his chin.", talk="a4_cabman"),
    ],
    on_enter=[
        E(cond="flag:a4_ritual_day", once=True, do=[
            {"say": "30 September. The funeral is over, and the sexton will lock up at dusk. In the dusk we shall not be alone: Arthur, Quincey, the Professor and I."}]),
    ],
)

# ---------------------------------------------------------------- 9. Churchyard by night
LOC_DATA["a4_kingstead_churchyard"] = dict(
    cells=[4, 4], interior=False, wall="dirt", floor="grass",
    ambient=AMBIENT["night_exterior"], camera=cam([4, 4]), lights=lights_moon(3.4), moon=dict(pos=[10, 16, -22]),
    scatter=pines(52, 20, [[-8, -8, 8, 8]]),
    spawn=[0.0, 6.2], spawns={"a4_kingstead_gate": [0.0, 6.2], "a4_westenra_tomb": [0.0, -2.2]},
    props=[
        prop("a4_wicket_in", "door", "dark", 0.0, 7.4, rot=180, name="Wicket to the lane", radius=0.6, look="The way out, unlatched from within.", go="a4_kingstead_gate"),
        prop("a4_vault", "tomb", "stone_tomb", 0.0, -5.4, scale=1.5, name="The Westenra vault", radius=1.6,
             look="A pale marble vault at the head of the yew avenue. 'Lucy Westenra' on the plate, the marble gleaming like a pale ghost."),
        prop("a4_lock_plate", "crucifix", "silver", -1.5, -4.4, name="Lock-plate of the vault", radius=0.3,
             look="Beneath a brass plaque, an iron lock-plate with four lever-slots. The bolt drops by its own weight: a falling lock, not a spring one. We could not be shut in.",
             set="a4_lock_inspected", set_text="A falling lock, four levers. Not a spring latch: it will not shut and trap us inside. The Professor nods, satisfied."),
        prop("a4_tomb_door", "door_big", "dark", 0.0, -4.2, name="Door of the vault", radius=0.9,
             look="A creaky iron-banded door. The keyhole is rust-stained brass.",
             use_item={"a4_tomb_key": [{"set": "a4_tomb_unlocked"}, {"say": "The key I cut turns on the fourth lever. The bolt falls, and the door gives with a groan that must be heard in Hampstead."}]},
             use_fail="That will not open the lock.",
             go="a4_westenra_tomb", go_cond="flag:a4_tomb_unlocked&flag:a4_lock_inspected",
             go_fail="Locked. I need a key that fits a four-lever falling lock, and the Professor wants me to look at the lock before we trust it."),
        prop("a4_tomb_seal", "chest", "ebony", 1.6, -3.6, name="Door clamps and crevices", radius=0.4, cond="flag:a4_party_assembled",
             look="Where the door meets the frame there are crevices wide enough for a knife-blade. A spirit could pass where an arm could not.",
             use_item={"a4_host_putty": [{"take": "a4_host_putty"}, {"set": "a4_tomb_sealed"},
                                         {"say": "Van Helsing rolls the putty in thin strips and presses them along every crack. The white of the Host shows in the grey like frost."}]},
             use_fail="That will not seal the crevices."),
        prop("a4_yew_hide", "pine", "dark", -3.0, 1.4, name="Yew by the church path", radius=0.5, cond="flag:a4_coffin_empty",
             look="A great yew with a hollow at its foot, where two men could crouch unseen.",
             set="a4_hidden_yew", set_text="We crouch under the yew, the Professor's lantern shuttered. A clock somewhere chimes the half-hour. Then something white moves between the tombs."),
        prop("a4_alder_hide", "pine_small", "green", 5.8, -2.2, name="Alder clump", radius=0.7, cond="flag:a4_tomb_sealed",
             look="A clump of alders against the north wall, perfect cover for four men. Moonlight reaches them hardly at all.",
             set="a4_vigil_waiting",
             set_text="The four of us crouch in the alder clump: the Professor with his crucifix, Arthur with his white face, myself, and Quincey with a drawn bowie. The Professor whispers, 'Do not move until I say.'"),
        prop("a4_church", "tower", "stone_dark", -8.4, -7.6, name="Kingstead church", radius=2.0, look="The old church, its tower black against the sky. Its clock is slow."),
        prop("a4_juniper1", "pine_small", "green", -4.6, 5.4, name="Juniper", radius=0.4, look="A juniper marking the church path."),
        prop("a4_juniper2", "pine_small", "green", 4.6, 5.4, name="Juniper", radius=0.4, look="Another juniper on the path."),
        prop("a4_yew1", "pine", "dark", -2.0, -1.0, radius=0.5),
        prop("a4_yew2", "pine", "dark", 2.0, -1.0, radius=0.5),
        prop("a4_yew3", "pine", "dark", 2.0, 2.2, radius=0.5),
        prop("a4_grave1", "gravestone", "stone_mossy", -5.4, -1.0, name="Headstone", radius=0.4, look="'Ann Foulkes, aged 61. Asleep in Jesus.'"),
        prop("a4_grave2", "gravestone_point", "stone_mossy", 5.2, 0.8, name="Headstone", radius=0.4, look="A pointed stone, lichen-eaten."),
        prop("a4_grave3", "grave_cross", "stone_mossy", -5.8, 3.6, name="Cross", radius=0.4, look="A stone cross leaning toward the path."),
        prop("a4_railed_tomb", "tomb", "stone_grey", 6.0, -4.8, name="Railed tomb", radius=1.0, look="A tomb with iron railing, white against the dark."),
        prop("a4_rail", "fence", "default", 6.0, -3.4, radius=0.5),
        prop("a4_low_wall", "fence", "default", -3.0, 7.4, radius=0.5),
        prop("a4_low_wall2", "fence", "default", 3.2, 7.4, radius=0.5),
        prop("a4_unseal", "chest", "ebony", 3.0, -2.8, name="The Host-strips on the door", radius=0.4, cond="flag:a4_lucy_driven_back",
             look="The strips of consecrated putty along the door-crack gleam like frost. Lucy cannot pass them, but she must go home to her coffin before dawn.",
             talk="a4_unseal"),
    ],
    npcs=[
        npc("a4_white_n1", "human_lucy", "undead", -4.2, -1.2, rot=90, name="A white figure", radius=0.5,
            cond="flag:a4_hidden_yew&flag:a4_coffin_empty&!a4_child_with_us",
            look="A white figure drifting between the tombs, with something small in its arms.", talk="a4_n1_encounter"),
        kid(npc("a4_child_found", "human_peasant_f", "innkeeper_wife", -2.4, 2.2, rot=0, name="The lost child", radius=0.4,
                cond="flag:a4_child_with_us&!a4_child_returned", look="A small child, sleeping heavily, two red marks at its throat.", talk="a4_child_found"), 0.55),
        npc("a4_lucy_n3", "human_lucy", "undead", -3.0, -2.6, rot=90, name="The Bloofer Lady", radius=0.5,
            cond="flag:a4_vigil_waiting&!a4_lucy_driven_back",
            look="A figure in white, golden-haired, carrying a child. Her lips are red as a wound.", talk="a4_n3_lure"),
    ],
)

# ---------------------------------------------------------------- 10. The tomb
LOC_DATA["a4_westenra_tomb"] = dict(
    cells=[2, 2], interior=True, wall="stone_tomb", floor="stone_dark",
    ambient=AMBIENT["crypt"], camera=cam([2, 2]),
    lights=[dict(pos=[0, 2.4, -1.0], color="#ff9a40", energy=1.6, range=8), dict(pos=[-2.5, 1.6, 1.8], color="#8aa0ff", energy=0.6, range=6)],
    walls=dict(north=["wall_door_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_4"]),
    spawn=[-2.0, -2.4], spawns={"a4_kingstead_churchyard": [-2.0, -2.4]},
    props=[
        prop("a4_tomb_exit", "door", "dark", -2.0, -3.8, name="Door to the churchyard", radius=0.6, look="The creaking door. It lets in a little of the night.", go="a4_kingstead_churchyard"),
        prop("a4_coffin_closed", "coffin", "ebony", 1.0, -1.5, name="Lucy's coffin", radius=0.9, cond="flag:a4_tomb_lit&!a4_lid_off",
             look="Oak, with a brass plate: 'Lucy Westenra. Died 17 September 1897.' Inside, we know, a lead case.",
             use_item={"a4_turnscrew": [{"set": "a4_lid_off"}, {"say": "The Professor and I unscrew the coffin lid, one screw at a time. Each squeak rings through the vault."}]},
             use_fail="That is not what opens a coffin."),
        prop("a4_coffin_lid_off", "coffin", "ebony", 1.0, -1.5, name="Lucy's lead casing", radius=0.9, cond="flag:a4_lid_off&!a4_lead_cut",
             look="The lid lies against the wall. The lead is dull, soldered along every seam, with a faint smell of sourness leaking out.",
             use_item={"a4_fretsaw": [{"set": "a4_lead_cut"}, {"set": "a4_coffin_empty"}, {"journal": "a4_j_night1"},
                                       {"say": "A tiny hole with the turnscrew, then the fret-saw: two feet down one side, across, and the flap is bent back. The candle shows the satin and the frilled shroud, and nothing else. The coffin is empty."}]},
             use_fail="The lead is too thick for that."),
        prop("a4_coffin_empty_view", "coffin", "ebony", 1.0, -1.5, name="Lucy's coffin, opened", radius=0.9, cond="flag:a4_lead_cut&!a4_lucy_returned",
             look="The lead casing, cut back like a tin. The satin is faintly crushed where someone lay, and quite empty now."),
        prop("a4_coffin_lucy_view", "coffin", "ebony", 1.0, -1.5, name="Lucy's coffin, opened", radius=0.9, cond="flag:a4_lucy_returned",
             look="The lead casing, cut back like a tin. She lies within."),
        prop("a4_other_coffin_a", "coffin", "dark", -2.6, 0.4, rot=90, name="Old Westenra coffin", radius=0.8,
             look="A coffin with clouded silver plate, a good shelf for a candle.",
             use_item={"a4_candle_stub": [{"take": "a4_candle_stub"}, {"set": "a4_candle_placed"},
                                          {"say": "I melt the foot of the candle onto the coffin lid so that it stands upright."}]},
             use_fail="Nothing to do with that."),
        prop("a4_candle_lit", "candle", "white", -2.6, 0.4, y=0.8, name="Candle, unlit", radius=0.2, cond="flag:a4_candle_placed&!a4_tomb_lit",
             look="A candle stub on the coffin lid, waiting for a light.",
             use_item={"a4_matches": [{"take": "a4_matches"}, {"set": "a4_tomb_lit"}, {"say": "The match rasps, and the little flame stands up in the stale air. The vault leaps into being: spiders, beetles, dust, brown flowers."}]},
             use_fail="I need a light."),
        prop("a4_candle_burning", "candle", "white", -2.6, 0.4, y=0.8, name="Candle, burning", radius=0.2, cond="flag:a4_tomb_lit",
             look="The candle burns with a steady yellow flame. Wax drips on the coffin plate."),
        prop("a4_other_coffin_b", "coffin", "dark", 3.0, 0.8, rot=-90, name="Old coffin", radius=0.8, look="Another coffin, plate eaten black by the damp air."),
        prop("a4_dead_flowers", "bottle", "green", -3.0, 2.6, name="Withered flowers", radius=0.2, look="Funeral flowers, brown paper to the touch, and the smell of a drain."),
        prop("a4_tomb_lamp", "lantern", "default", 3.0, -2.8, name="Oil lamp with a blue flame", radius=0.3, cond="flag:a4_ritual_day",
             look="A small lamp with a blue-edged flame, set on the shelf: hot enough to heat an iron.",
             use_item={"a4_soldering_iron": [{"take": "a4_soldering_iron"}, {"give": "a4_hot_iron"},
                                              {"say": "I lay the iron in the blue flame until it glows dull cherry. It will bite the lead."}]},
             use_fail="That will not do for the lamp."),
        prop("a4_tomb_spider", "rock", "dark", 2.8, 2.4, name="Spider web", radius=0.3, look="A web the size of a dinner-plate, a fat spider in the middle of it."),
        prop("a4_tomb_shelf", "bookshelf", "dark", -3.4, 3.2, radius=0.5),
        prop("a4_ritual_order", "book", "red", 0.0, 1.6, name="The Professor and his missal", radius=0.4, cond="flag:a4_ritual_day",
             look="Van Helsing stands with the missal open, his lips moving. He wishes us to be of one mind about what must be done.",
             talk="a4_vh_ritual_order"),
        prop("a4_stake_point", "stake", "default", 1.0, -0.2, name="Lucy, ready for the stake", radius=0.4,
             cond="flag:a4_lucy_helpless&flag:a4_ritual_order_known&!a4_stake_placed",
             look="She lies on her back, helpless, in a trance the sun cannot break. The stake must be set above the heart.",
             use_item={"stake": [{"take": "stake"}, {"set": "a4_stake_placed"},
                                 {"say": "Arthur takes the stake. Its point rests where the heart lies beneath the pale throat. 'Now, friend Arthur,' says the Professor, 'in God's name, strike.'"}]},
             use_fail="That is not the instrument."),
        prop("a4_stake_hammer", "hammer", "default", 1.0, -0.2, name="The stake, set to strike", radius=0.4,
             cond="flag:a4_stake_placed&!a4_staked",
             look="The stake stands over her heart. All that remains is the hammer.",
             use_item={"hammer": [{"set": "a4_staked"}, {"journal": "a4_j_stake"},
                                  {"say": "Arthur drives the stake home with three blows, his face set like marble. A hideous, blood-curdling screech, the body shakes and twists in wild contortions, white sharp teeth champing, lips cut and foam-flecked. And then it is quiet."}]},
             use_fail="I need the hammer."),
        prop("a4_missal_prayers", "book", "red", -1.0, -0.4, name="The Burial Service", radius=0.2,
             cond="flag:a4_staked&!a4_prayers_read", look="The Professor reads the prayers for the dead while the body settles.",
             talk="a4_missal"),
        prop("a4_head_cut", "stake", "default", 1.0, -0.2, name="Lucy, after the prayers", radius=0.4,
             cond="flag:a4_prayers_read&!a4_beheaded",
             look="The face is wholly at rest. All that remains is what the Professor calls the old, hard duty.",
             use_item={"a4_surgical_knives": [{"set": "a4_beheaded"},
                                              {"say": "The Professor and I do what must be done, with the steadiest hands we have. The knife is quick; I will not write more of it."}]},
             use_fail="That cannot do it."),
        prop("a4_garlic_mouth", "garlic", "default", 1.0, -0.2, name="Lucy, the mouth to be filled", radius=0.3, cond="flag:a4_beheaded&!a4_garlic_in_mouth",
             look="The final rite: the mouth filled, as the Professor prescribes.",
             use_item={"garlic": [{"set": "a4_garlic_in_mouth"}, {"say": "I fill the mouth with the white flowers. The tomb is thick with their smell."}]},
             use_fail="Only garlic will serve."),
        prop("a4_solder_seam", "chest", "ebony", 1.0, -1.5, name="Lead case, ready for sealing", radius=0.9, cond="flag:a4_garlic_in_mouth&!a4_solder_laid",
             look="The lead casing, opened and laid back. The seam is waiting.",
             use_item={"a4_solder": [{"take": "a4_solder"}, {"set": "a4_solder_laid"},
                                     {"say": "I lay the solder along the cut and bend the flap of lead back down."}]},
             use_fail="I need the solder."),
        prop("a4_solder_hot", "chest", "ebony", 1.0, -1.5, name="Seam to be sealed", radius=0.9, cond="flag:a4_solder_laid&!a4_coffin_sealed",
             look="A seam of grey lead and solder waiting for heat.",
             use_item={"a4_hot_iron": [{"take": "a4_hot_iron"}, {"set": "a4_coffin_sealed"}, {"journal": "a4_j_peace"},
                                       {"say": "The iron bites and the solder runs. We lay the oak lid over the lead and screw it down. The coffin lies as if no one had ever touched it."}]},
             use_fail="The iron must be hot."),
        prop("a4_final_vow", "bust", "stone_grey", -3.0, -2.2, name="The Professor at the door", radius=0.4, cond="flag:a4_coffin_sealed&flag:a4_arthur_peace_done",
             look="Van Helsing stands at the door with his hat in his hand, and one more thing to ask of us.", talk="a4_vh_pledge"),
    ],
    npcs=[
        npc("a4_lucy_sleeping", "human_lucy", "nightgown", 1.0, -1.5, rot=180, name="Lucy, in her coffin", radius=0.5,
            cond="flag:a4_lucy_returned&flag:a4_candle_placed&!a4_ritual_order_known",
            look="Lucy lies as in life but redder, her mouth full of dark blood, her teeth long and sharp. She does not stir.",
            talk="a4_vh_lucy_sleeping"),
        npc("a4_lucy_rising", "human_lucy", "undead", 1.0, -1.5, rot=180, name="Lucy, rising", radius=0.6,
            cond="flag:a4_ritual_order_known&!a4_lucy_helpless",
            look="Dusk. The sun has set. She rises, as one who wakes from a long sleep, and the smile on her face is not hers.",
            fight="lucy_tomb"),
        npc("a4_lucy_helpless_body", "human_lucy", "undead", 1.0, -1.5, rot=180, name="Lucy, helpless", radius=0.5,
            cond="flag:a4_lucy_helpless&!a4_staked",
            look="She lies back in the coffin, eyes open and staring, the red fading from her lips. She cannot move."),
        npc("a4_lucy_at_rest", "human_lucy", "lucy", 1.0, -1.5, rot=180, name="Lucy at rest", radius=0.5, cond="flag:a4_staked",
            look="The sweetness and purity have come back to her face. She is no longer a thing of terror but only Lucy."),
        npc("a4_arthur_tomb", "human_arthur", "lord", -1.4, 1.0, rot=90, name="Arthur", radius=0.5, cond="flag:a4_coffin_sealed&!a4_arthur_peace_done",
            look="Arthur stands with his head bowed and his eyes dry, the weight of a month taken off his chest.", talk="a4_arthur_peace"),
    ],
    on_enter=[
        E(cond="flag:a4_ritual_day&party:arthur", once=True, do=[
            {"protagonist": "arthur"},
            {"say": "Nearly dusk. Lucy's coffin is open before us, and Van Helsing has asked that Arthur, who loved her, strike the blow."}]),
        E(cond="flag:a4_lucy_returned", once=True, do=[
            {"say": "Day. The sun cuts a bar through the door. The Professor lifts the lid, and I see her."}]),
    ],
)

# ----------------------------------------------------------------------------------------------- dialogue
DIALOGUE = {}

DIALOGUE["a4_newsboy"] = dict(start="n0", nodes={
    "n0": N("Newsboy", "Westminster Gazette! 'A Hampstead Mystery', the Bloofer Lady, sir! Tuppence the copy.",
            C("Buy a copy (tuppence).", "n1", cond="!a4_got_gazette", do=[{"give": "a4_gazette"}, {"set": "a4_got_gazette"}, {"journal": "a4_j_gazette"}]),
            C("What do you know of this lady?", "n2"),
            LEAVE),
    "n1": N("Newsboy", "Thank you, sir. They say she is a pretty lady in white who takes the wee ones to see the swans. Not a swan on the Heath, mind.", next="n0"),
    "n2": N("Newsboy", "Seven nights, sir. Seven children. Always a little after dark, always on the north side by Shooter's Hill. The coppers say it's a woman wanting a baby; the old ones say it's a witch. Me, I stay on the road.", next="n0"),
})

DIALOGUE["a4_nursemaid"] = dict(start="n0", nodes={
    "n0": N("Nursemaid", "Is it a doctor you are? My master's boy was out two hours on Tuesday last, and I thought I should die.",
            C("What did the child say when he came back?", "n1"),
            C("Was he marked?", "n2"),
            LEAVE),
    "n1": N("Nursemaid", "That a pretty lady with white teeth had played with him under the thorn. Smiled at him. Then she kissed him on the neck, like. He was quite happy.", next="n3",
            do=[{"set": "a4_heard_bloofer"}, {"journal": "a4_j_bloofer"}]),
    "n2": N("Nursemaid", "A scratch, sir. Two little pricks, both sore. The doctor said it was a bramble. There are not many brambles on the Heath, and there is nothing in them like that.", next="n3"),
    "n3": N(S, "She is frightened, and she is hiding it for the child's sake. It does not read like the tale of a lunatic.", next="n0"),
})

DIALOGUE["a4_children"] = dict(start="n0", nodes={
    "n0": N("A small girl", "I'm the Bloofer Lady! You must lie down and shut your eyes, and I'll take you to see the swans!",
            C("Where does the real lady live?", "n1"),
            C("Does she sing?", "n2"),
            LEAVE),
    "n1": N("A small girl", "In the big white house with the high door, past the church. She's hungry, so she's thin. She always goes back before it's light.", next="n0",
            do=[{"set": "a4_heard_children"}]),
    "n2": N("A small girl", "She sings very low, and her hair is the colour of a guinea. She had a long white dress with mud on the hem.", next="n0"),
})

DIALOGUE["a4_constable"] = dict(start="n0", nodes={
    "n0": N("Constable", "Seven this week, sir. Four at the hospital, two home, one I'd rather not say.",
            C("Where was the last found?", "n1"),
            C("What hour?", "n2"),
            LEAVE),
    "n1": N("Constable", "On the grass by Shooter's Hill, laid out neat as a doll. No sign of a struggle. The lady must have put her down.", next="n0",
            do=[{"set": "a4_heard_constable"}]),
    "n2": N("Constable", "Four in the morning, near enough. Whoever she is, she keeps good time. And I never see her. I see the wet grass, and the child.", next="n0"),
})

DIALOGUE["a4_vh_heath"] = dict(start="n0", nodes={
    "n0": N(VH, "Look at the ground, friend John. The grass tells more than the newspaper, if we are patient. A shoe, a thread, a footprint: three witnesses.",
            C("What are we looking for?", "n1"),
            C("The shoe, the thread and the prints all lead north, toward Kingstead.", "n2",
              cond="a4_clue_shoe&a4_clue_thread&a4_clue_prints&a4_heard_children"),
            LEAVE),
    "n1": N(VH, "Whatever walked here does not mind the cold. Find me anything left by the one who takes the children: cloth, a trail, a shoe. And ask the children who is the lady. A child does not invent.", next="n0"),
    "n2": N(VH, "Kingstead. Yes. A white house, a high door, bare feet on the grass. Let us go to the hospital and see the child. I have had enough of theory; it is time you saw the wound.",
            do=[{"set": "a4_deduced_kingstead"}, {"journal": "a4_j_heath_trail"}], end=True),
})

DIALOGUE["a4_vincent"] = dict(start="n0", nodes={
    "n0": N("Dr. Vincent", "Dr. Seward? I know your name. The Professor wrote ahead. Mind, the child is mine; I cannot have the dressing changed for a stranger's curiosity.",
            C("I am a physician of the same kind. Here is my card; I should be glad of your opinion on the wound.", "n1",
              do=[{"set": "a4_vincent_ok"}]),
            C("Your scruples will not matter if more children disappear.", "n2"),
            LEAVE),
    "n1": N("Dr. Vincent", "Very well. Matron saw the same marks on a boy last week. If you can name them, I will thank you. Mind, the girl is nervous; do not frighten her.", end=True),
    "n2": N("Dr. Vincent", "I resent that, sir. Come back when you can ask civilly.", next="n0"),
})

DIALOGUE["a4_tuesday"] = dict(start="n0", nodes={
    "n0": N("The child", "Are you the doctor? Mother said the doctor would bring me a sweet.",
            C("May I see your neck, little one?", "n1", cond="a4_vincent_ok&!a4_saw_wound"),
            C("Who was the pretty lady?", "n2"),
            LEAVE),
    "n1": N(S, "Two punctures on the throat, small and neat, a finger-breadth apart. The edges are white and ragged, as if the vein had been drawn by suction. I have seen their likeness before, on Lucy's neck.",
            do=[{"give": "a4_wound_notes"}, {"set": "a4_saw_wound"}, {"journal": "a4_j_child_wound"}], next="n3"),
    "n2": N("The child", "She smiled at me. She said she was thirsty and would I give her a kiss. Her teeth were long.", next="n0"),
    "n3": N(VH, "You see, friend John? The same as Lucy. Not the same hand, perhaps; the same mouth.", end=True),
})

DIALOGUE["a4_ward_sister"] = dict(start="n0", nodes={
    "n0": N("Ward sister", "I have never seen a child so pale with so little hurt. Dr. Vincent says anaemia. I say there has been something at her.",
            C("Might I trouble you for some clean linen?", "n1", cond="!a4_got_linen", do=[{"give": "cloth"}, {"set": "a4_got_linen"}]),
            C("Do any of the children speak of the lady?", "n2"),
            LEAVE),
    "n1": N("Ward sister", "Take it, sir. We have plenty. Will you put it to good use?", end=True),
    "n2": N("Ward sister", "All of them. They call her kind. That's what frightens me.", next="n0"),
})

DIALOGUE["a4_seward_vh_doubt"] = dict(start="n0", nodes={
    "n0": N(VH, "You are angry, friend John. Good. Anger shows a mind that is working. Now will you let it work?",
            C("This is madness, Professor. Lucy is dead. I saw her buried.", "n1"),
            C("Where is the proof you promise?", "n2", cond="!a4_seward_convinced"),
            C("I have read Mrs Harker's pages and your wound notes. Convince me, if you can.", "n3",
              cond="has:a4_typed_journal&has:a4_wound_notes&!a4_seward_convinced"),
            LEAVE),
    "n1": N(VH, "You have heard of bats that drink the blood of cattle in Brazil. Of the fakirs who are buried alive for months and come back. Of the tree that eats flies. Do you believe in these because you can explain them, or because you have seen them? I ask only that you believe what you have not seen.", next="n0"),
    "n2": N(VH, "There is a woman in Paddington, Mrs Harker, who has typed a document that will do what my arguments cannot. Fetch it, and bring her husband's word that he did not dream. I trust the paper; you trust paper.",
            do=[{"set": "a4_vh_goes_paddington"}, {"journal": "a4_j_doubt"}], end=True),
    "n3": N(S, "The wound in the child's neck and the wound in Lucy's: the same. A foreign nobleman who leaves not a reflection, who crawls down a wall, who is dead by day and alive by night. A man who seeks London. I cannot say I believe it. I cannot say I do not.", next="n4"),
    "n4": N(VH, "That is enough, friend John. It is the beginning of belief. Now we go to Hillingham, for Lucy's papers, and to prepare. Tonight we shall see what is in the Westenra tomb.",
            do=[{"set": "a4_seward_convinced"}, {"journal": "a4_j_belief"}], end=True),
})

DIALOGUE["a4_mina_talk"] = dict(start="n0", nodes={
    "n0": N("Mina Harker", "Professor, I have been waiting. Jonathan is awake, but he is not himself. I have your letter, and I have his journal.",
            C("Madam, I have a great need of your shorthand and your typewriter.", "n1", cond="!a4_got_shorthand"),
            C("Tell me of Lucy's last weeks, as you saw them.", "n2"),
            C("How shall I get back to London?", "n3"),
            LEAVE),
    "n1": N("Mina Harker", "Jonathan's shorthand is a private matter. But if it will help Lucy, I will let you have it. My machine wants a new ribbon; there is a spare in my workbasket, I think. I will wait.",
            do=[{"give": "a4_shorthand_diary"}, {"set": "a4_got_shorthand"}], end=True),
    "n2": N("Mina Harker", "She was sleep-walking. I found her on the seat at Whitby churchyard with something dark at her throat. It looked like a ribbon. It was not.", next="n0"),
    "n3": N("Mina Harker", "The quick 3.34 from Exeter, with a change at Reading. I have marked it in the timetable.", next="n0"),
})

DIALOGUE["a4_jonathan_talk"] = dict(start="n0", nodes={
    "n0": N("Jonathan Harker", "Professor? Mina says I wrote it all down in Buda-Pesth. I do not know whether to believe my own hand.",
            C("Your journal is not a dream, Mr Harker. I have read it, and I know where the Count has gone.", "n1", cond="!a4_jonathan_cured"),
            C("What do you remember of London?", "n3", cond="a4_jonathan_cured"),
            LEAVE),
    "n1": N("Jonathan Harker", "You... believe me? Then the castle was real? The three women, the Count in the box?",
            C("Every word. And your wife has typed it, God bless her.", "n2"),
            C("I believe what I find in the evidence. That is enough.", "n2")),
    "n2": N("Jonathan Harker", "I am cured, Professor. If I am a madman, then a madman can swing an axe. Tell me what to do.",
            do=[{"set": "a4_jonathan_cured"}, {"journal": "a4_j_jonathan"}], next="n0"),
    "n3": N("Jonathan Harker", "I saw him in Piccadilly. Younger by twenty years, outside Guiliano's, watching a girl. My heart stopped. I walked away because I could not stand it any more.", next="n0",
            do=[{"set": "a4_count_in_london"}]),
})

DIALOGUE["a4_vh_bag"] = dict(start="n0", nodes={
    "n0": N(S, "The Professor's bag clinks and rattles. He asked me to take what is needed.",
            C("Take the turnscrew, the fret-saw and the candle-end.", "n1", cond="a4_seward_convinced&!a4_got_bag",
              do=[{"give": "a4_turnscrew"}, {"give": "a4_fretsaw"}, {"give": "a4_candle_stub"}, {"set": "a4_got_bag"}]),
            C("Leave it. It is not my bag.")),
    "n1": N(S, "A turnscrew for coffin-screws, a tiny fret-saw for lead, and a candle-end. The tools of a respectable burglar.", end=True),
})

DIALOGUE["a4_workbench"] = dict(start="n0", nodes={
    "n0": N(S, "The bench is cluttered with files and wards. I can cut a key if I know the lock.",
            C("Cut a six-lever key, to be safe.", "n1", cond="has:a4_key_blank&!a4_made_key"),
            C("Cut a spring-latch key, simple and quick.", "n2", cond="has:a4_key_blank&!a4_made_key"),
            C("Cut a four-lever key for a falling-bolt lock, as the undertaker's invoice describes.", "n3",
              cond="has:a4_lock_invoice&has:a4_key_blank&!a4_made_key"),
            C("[Not yet]")),
    "n1": N(S, "Six levers is more than the lock has. The key would not drop the bolt. I abandon that and think again.", next="n0"),
    "n2": N(S, "A spring latch is not a falling lock. That is a cheap house-door pattern. The key would be useless in a tomb.", next="n0"),
    "n3": N(S, "Four levers at the depths the invoice gives, a plain bit, the shoulder cut for a falling bolt. I file for an hour. At the end the key turns smooth in my hand.",
            do=[{"take": "a4_key_blank"}, {"give": "a4_tomb_key"}, {"set": "a4_made_key"}, {"journal": "a4_j_lock"}], end=True),
})

DIALOGUE["a4_marquand"] = dict(start="n0", nodes={
    "n0": N("Mr. Marquand", "Dr. Seward. A sad business. Lord Godalming inherits everything, and has bidden me give Professor Van Helsing every liberty with Miss Lucy's papers. There is a good deal of correspondence.",
            C("Please sort the legal papers from the private ones. I shall take the private ones.", "n1", cond="!a4_marquand_ok"),
            C("Tell me about the tomb. Who has the key?", "n2"),
            LEAVE),
    "n1": N("Mr. Marquand", "Of course. The deeds, the will and the bills are to remain with me. Her private letters and her sleep-walking notes are yours. The desk is open. Do be careful of the undertaker's account; there is an item about the vault lock that has taken my fancy.",
            do=[{"set": "a4_marquand_ok"}], end=True),
    "n2": N("Mr. Marquand", "The undertaker holds one key, and the family another, held at Ring. I should not trouble either of them in this season of grief.", next="n0"),
})

DIALOGUE["a4_papers"] = dict(start="n0", nodes={
    "n0": N(S, "Three stacks of paper on Lucy's desk: deeds and the will, the undertaker's accounts, and her private letters.",
            C("The undertaker's account.", "n1", cond="a4_marquand_ok&!a4_got_invoice",
              do=[{"give": "a4_lock_invoice"}, {"set": "a4_got_invoice"}]),
            C("Her private letters and diary leaves.", "n2", cond="a4_marquand_ok&!a4_got_note",
              do=[{"give": "a4_lucy_note"}, {"set": "a4_got_note"}, {"journal": "a4_j_papers"}]),
            C("The deeds and the will.", "n3", cond="a4_marquand_ok"),
            C("[Not yet]")),
    "n1": N(S, "'To Messrs. Chubb, one four-lever falling-bolt lock for the Westenra vault, fixed to the iron-banded door, and two keys.' I fold the bill into my pocket book.", next="n0"),
    "n2": N(S, "A few lines, in Lucy's hand: 'I walk in my sleep, I think. Mina found me on the churchyard seat; my throat is sore and I am so tired.' I will let the Professor see this.", next="n0"),
    "n3": N(S, "Legal. It stays with Mr. Marquand. It is not for us.", next="n0"),
})

DIALOGUE["a4_maid_talk"] = dict(start="n0", nodes={
    "n0": N("Hannah", "Oh, sir. I did not know it was you. Is there anything you need?",
            C("A small gold crucifix is missing from the room where Miss Lucy lay.", "n1", cond="!a4_got_crucifix"),
            C("I have the pawn ticket for a crucifix that was pawned yesterday.", "n2", cond="has:a4_pawn_ticket&!a4_got_crucifix"),
            LEAVE),
    "n1": N("Hannah", "I never saw such a thing, sir! I did not! You will not blame me, for I am an honest girl...", next="n0"),
    "n2": N("Hannah", "Oh sir, I only meant to borrow it. It's gold; my mother is ill. I put it in pawn on the corner. I am so ashamed. Here, this is the ticket for it and my own wage for the redemption.",
            do=[{"give": "crucifix"}, {"set": "a4_got_crucifix"}, {"journal": "a4_j_crucifix"}], next="n3"),
    "n3": N(VH, "No punishment, Hannah. I have been poor too. But hear me: the cross is there for a reason. Pray that you never know it.", end=True),
})

DIALOGUE["a4_landlord"] = dict(start="n0", nodes={
    "n0": N("Landlord", "Doctors, gentlemen. You'll want your dinner. Is it a long walk you have tonight?",
            C("We go to Kingstead churchyard. Is the road watched?", "n1"),
            C("Anything strange on the Heath of late?", "n2"),
            LEAVE),
    "n1": N("Landlord", "The horse patrol goes by the high road at half-past ten, sir; they have been on edge with all the children. The Heath path along Hampstead Lane is dark, but there is no one on it after eleven.", next="n0",
            do=[{"set": "a4_know_patrol"}]),
    "n2": N("Landlord", "Dogs howl in the evening for no reason. Cows go dry. And the nurses all say the same lady with a smile. Shut up, Mr. Carter, we are not all frightened.", next="n0"),
})

DIALOGUE["a4_patron"] = dict(start="n0", nodes={
    "n0": N("Carter", "You gentlemen are doctors? Then tell me what takes the kiddies. My own nipper was out two nights ago and came back chuckling about a lady.",
            C("Keep him indoors after dusk, and tell the others.", "n1"),
            LEAVE),
    "n1": N("Carter", "I'd do that. Aye. And leave a crucifix by the door, as the old woman says. It can't hurt, can it?", end=True),
})

DIALOGUE["a4_vh_dinner"] = dict(start="n0", nodes={
    "n0": N(VH, "Eat, friend John. A man who tomb-robs on an empty stomach makes mistakes.",
            C("Tell me the plan again.", "n1"),
            C("Which road shall we take to Kingstead?", "n2", cond="a4_know_patrol"),
            C("I am ready. Let us go.", "n5",
              cond="has:a4_tomb_key&has:a4_turnscrew&has:a4_fretsaw&has:a4_candle_stub&has:a4_matches&has:crucifix&flag:a4_route_ok"),
            C("[Not yet]")),
    "n1": N(VH, "A falling lock, a coffin, a lead case. We shall open it and see. If Lucy is within, I am wrong and you may call me a fool for the rest of my days. If she is not, you will have no more excuses. We need the key, the turnscrew, the fret-saw, the candle and the matches, and a crucifix, since I do not want to meet her unarmed.", next="n0"),
    "n2": N(VH, "Three ways, John. Choose carefully, for a detective in the dark has no second chance.",
            C("The high road, past the Spaniards, where the lamps are.", "n3"),
            C("The Heath path by Hampstead Lane, after eleven.", "n4"),
            C("A hansom straight to the church gate.", "n3")),
    "n3": N(VH, "The horse patrol will stop us on the high road, and a hansom would be marked by every dog from here to the church. No.", next="n2"),
    "n4": N(VH, "Good. The dark path, after the patrol has passed. You are an apt pupil.", do=[{"set": "a4_route_ok"}], next="n0"),
    "n5": N(VH, "We go. And if anything within seems to move, friend John, trust the crucifix more than your eyes.",
            do=[{"set": "a4_dined"}, {"journal": "a4_j_dinner"}], end=True),
})

DIALOGUE["a4_sexton"] = dict(start="n0", nodes={
    "n0": N("Sexton", "Evening, gentlemen. I lock up at dusk. We've had folk wandering about. Not a good place for the likes of you after dark.",
            C("A silver coin, good sexton, for a doctor's quiet visit to a grave.", "n1", cond="has:silver&!a4_wicket_open"),
            C("Where is the Westenra vault?", "n2"),
            C("We shall wait until you have locked the gate, then take our chance.", "n3", cond="a4_read_plan&!a4_wicket_open"),
            LEAVE),
    "n1": N("Sexton", "Ah. Well, the wicket does lift from the inside. I'll leave the latch easy. Mind you don't leave anything behind, gentlemen.",
            do=[{"take": "silver"}, {"set": "a4_wicket_open"}], end=True),
    "n2": N("Sexton", "Head of the yew avenue, sir, up the church path, past the junipers. A fine grand vault, that; they say the young lady was beautiful.", next="n0"),
    "n3": N("Sexton", "As you please, sir. I'll lock the gate, but the wicket opens from the inside. I never saw you.", do=[{"set": "a4_wicket_open"}], end=True),
})

DIALOGUE["a4_cabman"] = dict(start="n0", nodes={
    "n0": N("Cabman", "Hillingham? Or home? It's all the same to my horse. He won't go past the churchyard after dark. Not for money.",
            C("Why does he refuse?", "n1"),
            LEAVE),
    "n1": N("Cabman", "He sweats, sir, and sidles. The cart-horses are the same. I think there's something in the place that animals know.", end=True),
})

DIALOGUE["a4_n1_encounter"] = dict(start="n0", nodes={
    "n0": N(S, "A white figure drifts between the tombs, tall, with something in her arms. She stops. She comes on again, her face turned from us.",
            C("Hold still. Let her come nearer.", "n1"),
            C("[Whisper] Professor, now?", "n1")),
    "n1": N(VH, "Wait. Wait. A little more...", next="n2"),
    "n2": N(S, "She is within ten paces. The Professor slides the lantern open, and the light falls on a lovely face, sweet and pure, and blood on her chin and on her white gown. It is Lucy.",
            C("Hold your ground, and open the lantern fully.", "n3"),
            C("[Cry out]", "n3")),
    "n3": N(VH, "Lucy! In the name of God, stand!", next="n4"),
    "n4": N(S, "She flings the child on the ground, snarls like a cat, and glides past us to the tomb. The Professor puts the crucifix between her and the vault, and she is gone in a second... through the lock-plate.", next="n5"),
    "n5": N(S, "The child is alive, breathing heavily; the bruise on its throat is no more than a prick. We must take it where the police will find it. We cannot answer questions.",
            do=[{"set": "a4_child_with_us"}, {"journal": "a4_j_child_found"}], end=True),
})

DIALOGUE["a4_child_found"] = dict(start="n0", nodes={
    "n0": N(S, "The child sleeps, curled into my coat. The wound is the twin of the others.",
            C("Carry it away to the lane."),
            C("[Wait]")),
})

DIALOGUE["a4_handoff"] = dict(start="n0", nodes={
    "n0": N(S, "The lamp, the bench, the policeman's beat. A child laid here will be found in ten minutes.",
            C("Lay the child on the bench, ring the policeman's bell and slip behind the hedge.", "n1", cond="a4_child_with_us&!a4_child_returned"),
            C("[Not yet]")),
    "n1": N(S, "We wait, hearts hammering, behind the hedge. The constable's lantern swings. 'Hullo! What's this?' He gathers it up. 'Well, there's one safe.' We go.",
            do=[{"set": "a4_child_returned"}, {"journal": "a4_j_handoff"}, {"card": "The next afternoon"}, {"set": "a4_lucy_returned"},
                {"journal": "a4_j_day2"}, {"goto": "a4_kingstead_gate"}], end=True),
})

DIALOGUE["a4_patrol"] = dict(start="n0", nodes={
    "n0": N("Constable", "Found a child, gentlemen, on the bench. Breathing, thank God. I'll take it to the station. Did you see anyone?",
            C("Nothing, constable. A good night to you."),
            C("We came across the Heath on a doctor's errand.")),
})

DIALOGUE["a4_vh_lucy_sleeping"] = dict(start="n0", nodes={
    "n0": N(VH, "Look at her, John. Not corpse, not alive. See how red the lips are, how the flesh is fuller than when she died.",
            C("Look at her lips.", "n1"),
            C("Look at her teeth.", "n2"),
            C("Look at the coffin lead.", "n4"),
            C("Professor, we must bring Arthur before tonight.", "n3", cond="a4_saw_lips&a4_saw_teeth")),
    "n1": N(S, "Redder than in life, and a fresh fleck of blood at the corner: not hers, the Professor says. It has come from some child.", do=[{"set": "a4_saw_lips"}], next="n0"),
    "n2": N(S, "The canine teeth are sharper than they were. I lift her lip. No living woman's mouth is made so.", do=[{"set": "a4_saw_teeth"}], next="n0"),
    "n4": N(VH, "There is no sign of the lead being touched since it was sealed; she is in and out of it as she chooses. Mist or moonbeam, I do not know. But she goes, and she returns before dawn.", next="n0"),
    "n3": N(VH, "Quite so. She must be put to rest, and he must see it done. Arthur will not like it. But he must be brought, or he will hate us for ever. Come, to Hillingham.",
            do=[{"set": "a4_lucy_sleeping"}, {"journal": "a4_j_lucy_sleeping"}], end=True),
})

DIALOGUE["a4_arthur_grief"] = dict(start="n0", nodes={
    "n0": N(A, "John. Professor. You come again, and say nothing, and look at me like physicians at a bed. Lucy is dead. What more is there to say?",
            C("Arthur, trust the Professor. He has asked for nothing for himself.", "n1"),
            C("We believe she is not at rest. She walks.", "n2"),
            C("Come with us at midnight, and see for yourself.", "n3")),
    "n1": N(A, "I trust you, John. But this... for God's sake, say what you want.", next="n3"),
    "n2": N(A, "She... walks? You will drive me mad, Seward. If you were any other man, I would knock you down.", next="n3"),
    "n3": N(VH, "Lord Godalming, I ask a great thing: I ask your hand to do a thing which will break your heart, and in time mend it. If you refuse, I shall not blame you. But if you consent, you will be the one who frees her.",
            C("Arthur, it is the kindest service you can do her.", "n4"),
            C("Arthur, if you refuse, I shall do it myself.", "n4")),
    "n4": N(A, "Very well. I have loved her, and I will not leave her in the hands of strangers. I will come.", next="n5",
            do=[{"recruit": "arthur"}, {"recruit": "quincey"}, {"set": "a4_party_assembled"}, {"journal": "a4_j_arthur"}]),
    "n5": N(Q, "Count me in. I've shot grizzlies, but I never shot a thing I couldn't see. I'll hold the guns, and Art holds the stake.", end=True),
})

DIALOGUE["a4_quincey_talk"] = dict(start="n0", nodes={
    "n0": N(Q, "Doc, I'll tell you plain: I've seen a lot in the wild, and nothing strikes me as hard as a man who loved a girl and is told to go and see her in her coffin.",
            C("He will bear it, Quincey. He has you.", "n1"),
            C("Do you believe the Professor?", "n2"),
            LEAVE),
    "n1": N(Q, "He's got a Texan's word. I'll be at his back, and if a lady comes at him, I'll hold him, not shoot.", next="n0"),
    "n2": N(Q, "That Dutchman knows more than any three doctors. If he says dead folk walk, I'll give him a rifle and a long night.", next="n0"),
})

DIALOGUE["a4_vh_prep"] = dict(start="n0", nodes={
    "n0": N(VH, "Here is what is needed. A little of the Host from Amsterdam, which I have by Indulgence from the Pope. The Host and the putty make a seal that no spirit passes.",
            C("Take the Host.", "n1", cond="!a4_got_host", do=[{"give": "host"}, {"give": "a4_missal"}, {"set": "a4_got_host"}, {"set": "rites"}]),
            C("Professor, please knead the Host into the putty for me.", "n2", cond="has:host&has:a4_putty&!a4_got_host_putty"),
            C("Professor, I have the ash wood but I cannot work it. Will you sharpen the stake?", "n3", cond="has:wood&!a4_got_stake"),
            LEAVE),
    "n1": N(VH, "Good. Take also the missal. You will need the prayers. And bring the garlic: a mouth full of it, when the time comes.", next="n0"),
    "n2": N(VH, "Watch my hands. A little here, a little there, until the putty is like wax. Behold: a seal against the Un-Dead.",
            do=[{"take": "host"}, {"take": "a4_putty"}, {"give": "a4_host_putty"}, {"set": "a4_got_host_putty"}], next="n0"),
    "n3": N(VH, "Give me the knife. So, a good point; we char the end to harden it. Here: a stake that will not splinter.",
            do=[{"take": "wood"}, {"give": "stake"}, {"set": "a4_got_stake"}], next="n0"),
})

DIALOGUE["a4_n3_lure"] = dict(start="n0", nodes={
    "n0": N(S, "She comes down the path between the yews, a child in her arms, red lips parted. The moon bathes her golden hair. 'Arthur,' she murmurs. 'Come to me. My arms are hungry for you.'",
            C("Hold Arthur back by the arm.", "n1"),
            C("Raise the crucifix.", "n2", cond="has:crucifix"),
            C("Stand your ground and say nothing.", "n1")),
    "n1": N(A, "Lucy! My God, Lucy... Her voice... Seward, she is calling me...", next="n2"),
    "n2": N(VH, "Stand back, all! The cross! In the name of God, I command you!",
            do=[{"fight": "a4_lucy_vigil"}], end=True),
})

DIALOGUE["a4_unseal"] = dict(start="n0", nodes={
    "n0": N(VH, "She has been driven back, and she cannot return to her coffin while the Host is on the door. She is wild with hunger and must go in before dawn. Shall we let her pass?",
            C("Remove the strips and let her go to her coffin.", "n1"),
            C("[Wait]")),
    "n1": N(VH, "The strips come away. She flows through the gap like smoke, and we hear a faint sigh within the vault. Now we wait out the day, John. Tonight we finish this.",
            do=[{"set": "a4_lucy_in_tomb"}, {"set": "a4_ritual_day"}, {"card": "30 September. The next evening."}, {"goto": "a4_kingstead_gate"}, {"protagonist": "seward"}], end=True),
})

DIALOGUE["a4_vh_ritual_order"] = dict(start="n0", nodes={
    "n0": N(VH, "Friends, we do now the work which God demands. Attend, for the order matters, and I will not repeat it in the vault. What is the first step with the Un-Dead?",
            C("Garlic in the mouth first, then the stake.", "n1"),
            C("Behead first; the heart can wait.", "n1"),
            C("The stake through the heart, the prayers, then the head, then the garlic in the mouth, and last the coffin sealed.", "n2")),
    "n1": N(VH, "No, friend. The stake first: it frees her soul. The head and the garlic follow. Think again.", next="n0"),
    "n2": N(VH, "Exactly so. The stake, driven by the hand that loved her; the prayers; the head; the garlic; the seal of lead. Arthur, you will stand here. Quincey, at the door. John, the knives. We wait for her to rise; she will be restless at the sunset.",
            do=[{"set": "a4_ritual_order_known"}], end=True),
})

DIALOGUE["a4_missal"] = dict(start="n0", nodes={
    "n0": N(VH, "Let us pray for the dead, as the Church has ordered. 'Out of the depths I have called to Thee, Lord...' Amen.",
            C("[Join the prayers]", "n1")),
    "n1": N(S, "It is the oldest ritual I know, and the least understood. When the Professor closes the book, the body is quiet, and the tomb seems to breathe out.",
            do=[{"set": "a4_prayers_read"}], end=True),
})

DIALOGUE["a4_arthur_peace"] = dict(start="n0", nodes={
    "n0": N(A, "Seward, Professor... she looked at me. At the last she smiled at me, as she used to. It was Lucy. And she is at peace.",
            C("She is at peace, Arthur. You did what only love could do.", "n1"),
            C("We mourn her, but she mourns no longer.", "n1")),
    "n1": N(A, "I thank God that He gave me the strength. And I thank you for letting me keep the last of her. From now, if there is anything I can do against the creature that did this, I am in.",
            do=[{"set": "a4_arthur_peace_done"}], end=True),
})

DIALOGUE["a4_vh_pledge"] = dict(start="n0", nodes={
    "n0": N(VH, "Friends, the work of tonight is done, but we are at the first of many. Someone made Lucy what she was, and that one is in England, in London. He is strong, and old, and patient. Will you stand with me, John, Arthur, Quincey? Will you hunt the creature that did this?",
            C("To the last, Professor.", "n1"),
            C("I will stand with you. Where do we begin?", "n1")),
    "n1": N(VH, "In your asylum, John, where there is a library and a madman who has known the master. I leave tonight for Amsterdam to find what I need. When I return, we hold council of war.",
            do=[{"journal": "a4_j_vow"}, {"card": "ACT V: THE COUNCIL OF WAR"}, {"goto": "a5_asylum_library"}], end=True),
})

# ----------------------------------------------------------------------------------------------- items
ITEMS = {
    "a4_gazette": dict(name="Westminster Gazette", asset="book", variant="leather", desc="'A Hampstead Mystery': children lured by a beautiful lady, found with small wounds on the throat."),
    "a4_wound_notes": dict(name="Notes on the wound", asset="book", variant="diary", desc="My notes on the child's throat: two punctures, a finger-breadth apart, edges white and ragged."),
    "a4_shorthand_diary": dict(name="Jonathan's shorthand journal", asset="book", variant="leather", desc="Harker's Transylvanian journal in Pitman's shorthand. Few can read it."),
    "a4_ribbon": dict(name="Typewriter ribbon", asset="book", variant="red", desc="A new ribbon, still in its blue paper."),
    "a4_typed_journal": dict(name="Mina's typed journal", asset="book", variant="diary", desc="Jonathan's journal and Mina's own, typed in clean black letters."),
    "a4_lock_invoice": dict(name="Undertaker's invoice", asset="book", variant="red", desc="A bill from Messrs. Chubb for 'one four-lever falling-bolt lock for the Westenra vault, with two keys'."),
    "a4_lucy_note": dict(name="Lucy's note", asset="book", variant="leather", desc="A note in Lucy's hand about sleep-walking and a sore throat."),
    "a4_pawn_ticket": dict(name="Pawn ticket", asset="book", variant="leather", desc="A pawnbroker's ticket: 'One small gold crucifix, 5 shillings'."),
    "a4_key_blank": dict(name="Key blank", asset="key", variant="default", desc="A blank key of good brass, uncut."),
    "a4_tomb_key": dict(name="Key of the vault", asset="key", variant="gold", desc="A four-lever key cut to the vault's falling lock."),
    "a4_turnscrew": dict(name="Turnscrew", asset="hammer", variant="default", desc="A heavy turnscrew for coffin screws, and for punching into lead."),
    "a4_fretsaw": dict(name="Fret-saw", asset="hammer", variant="default", desc="A tiny fret-saw with a blade fine enough for lead."),
    "a4_candle_stub": dict(name="Candle-end", asset="candle", variant="white", desc="A short candle-end of sperm wax."),
    "a4_matches": dict(name="Box of matches", asset="candle", variant="red", desc="Lucifer matches in a tin box."),
    "a4_oil_lamp": dict(name="Dark lantern", asset="lantern", variant="default", desc="A lantern with a slide for hiding or showing the light."),
    "a4_putty": dict(name="Glazier's putty", asset="bottle", variant="amber", desc="A ball of grey putty, soft as clay."),
    "a4_host_putty": dict(name="Host-putty", asset="bottle", variant="glass", desc="Putty kneaded with the crumbled Host: a seal against the Un-Dead."),
    "a4_soldering_iron": dict(name="Soldering iron", asset="hammer", variant="default", desc="A plumber's iron, black with use."),
    "a4_hot_iron": dict(name="Hot iron", asset="hammer", variant="default", desc="The soldering iron, heated cherry-red in the blue flame."),
    "a4_solder": dict(name="Stick of solder", asset="key", variant="default", desc="A stick of dull grey plumber's solder."),
    "a4_surgical_knives": dict(name="Post-mortem knives", asset="chest", variant="pale", desc="My case of surgical knives. The Professor asked for them."),
    "a4_missal": dict(name="Missal", asset="book", variant="red", desc="Van Helsing's missal, with the prayers for the dead."),
}

# ----------------------------------------------------------------------------------------------- journal
JOURNAL = {
    "a4_j_catacombs": dict(title="The old vaults", source="Professor Van Helsing's notes",
                           text="Beneath Kingstead lie older vaults than the Westenra tomb: lead coffins in niches, a gallery of the long dead. Lucy is not the first this churchyard has held. I look in each niche for the signs: a lid forced, earth fresh, a face too red. Most are only dead. That is not the same as being at peace."),
    "a4_j_lower": dict(title="The lower gallery", source="Professor Van Helsing's notes",
                       text="In the lower gallery one coffin lid has been prised from within; the splinters point outward. Others hunted here before us, and lost. Their stake lies in the dust, its point stained to the grain. We are not the first to learn what that kind of sleep means, and we need not be the last to pay."),
    "a4_j_heath": dict(title="26 September. Hampstead", source="Dr. Seward's diary",
                       text="The Gazette tells of children lured on the Heath by a 'bloofer lady', found with small throat wounds. Van Helsing went white when he read it, and has said only that I must see for myself. I do not like the look in his face."),
    "a4_j_gazette": dict(title="The Westminster Gazette", source="Newspaper cutting",
                         text="A HAMPSTEAD MYSTERY. Children have been missing on the Heath and found, after an interval, with small wounds on the throat. They say a 'bloofer lady' enticed them. It is a pretty name for a horrid thing."),
    "a4_j_bloofer": dict(title="The Bloofer Lady", source="Dr. Seward's diary",
                         text="A nursemaid and a ragged child both speak of a kind lady in white who kisses children on the neck. Children do not invent such tales. I begin to wonder what walks the Heath at night."),
    "a4_j_heath_trail": dict(title="The trail", source="Dr. Seward's diary",
                             text="A red shoe, a thread of fine lawn, a woman's bare footprints, all pointing north to Kingstead. The Professor says the trail is as clear as the Gazette. I see it, and I do not wish to."),
    "a4_j_child_wound": dict(title="The wound", source="Dr. Seward's diary",
                             text="I saw the child's throat at the North Hospital. Two punctures, a finger apart, white-edged and ragged. I have seen the same on Lucy's neck. There is a doctor in me who says it cannot be, and an observer who says it is."),
    "a4_j_doubt": dict(title="Doubt", source="Dr. Seward's diary",
                       text="I told Van Helsing it was madness; he did not rebuke me. He asked for belief in things unseen, and said there is a woman in Paddington whose typewriter will do what his words cannot. I am too weary to quarrel."),
    "a4_j_mina": dict(title="Mrs Harker", source="Van Helsing's note",
                      text="She has the courage of a soldier and the hands of a clerk. She reads her husband's journal and does not weep. If the world is saved, it will be by such women. I ask her only for what she can give."),
    "a4_j_typed": dict(title="The typed pages", source="Mina Harker's journal",
                       text="The ribbon was fresh, the keys clean, the shorthand surrendered. By evening the whole of Jonathan's foreign journal lay typed, clear as print. I pray it will convince the doctors, since it has convinced me."),
    "a4_j_jonathan": dict(title="Jonathan's recovery", source="Mina Harker's journal",
                          text="Jonathan wept when the Professor told him the journal was true. He has been a different man since: pale but whole. He saw the Count in Piccadilly, and fainted; but now he says he will help to the end."),
    "a4_j_belief": dict(title="Belief", source="Dr. Seward's diary",
                        text="I have read Mina Harker's pages and seen the child's wound. I cannot call it madness any longer. Van Helsing says we shall look into the Westenra tomb. If it is empty, I shall have no more reasons to disbelieve him."),
    "a4_j_papers": dict(title="Lucy's papers", source="Dr. Seward's diary",
                        text="Lucy's papers are in order, Mr. Marquand's work. Among them the undertaker's bill, which gives the make of the vault lock, and a note in her own hand about walking in her sleep. The Professor smiled sadly: 'it is all here.'"),
    "a4_j_crucifix": dict(title="The crucifix", source="Van Helsing's note",
                          text="The little gold cross was stolen by the maid, who is poor and frightened. I redeemed it, and forgave her. A wretch in need is not to be punished; a wretch in power is."),
    "a4_j_lock": dict(title="Keys", source="Dr. Seward's diary",
                      text="I cut a key for a four-lever falling lock by the undertaker's description. An hour of filing at the bench; it fits as if made by Chubb. I feel like a criminal and a physician at once."),
    "a4_j_dinner": dict(title="Dinner at the Castle", source="Dr. Seward's diary",
                        text="We dined at Jack Straw's, I with little appetite. The Professor explained his plan and chose the dark path by Hampstead Lane to avoid the patrol. Then, with turnscrew, saw, candle and cross, we set out for Kingstead."),
    "a4_j_night1": dict(title="The empty coffin", source="Dr. Seward's diary",
                        text="We opened the vault by night. The Professor unscrewed the lid, cut through the lead with a tiny saw, and held the candle over the satin. The coffin was empty. I felt as though the ground gave way."),
    "a4_j_child_found": dict(title="The child", source="Dr. Seward's diary",
                             text="We watched from under the yew. A white figure came with a child in her arms. The Professor opened the lantern, and I saw Lucy's face, her mouth wet with blood. She dropped the child and fled into the tomb."),
    "a4_j_handoff": dict(title="The constable", source="Dr. Seward's diary",
                         text="We laid the child on a bench under the lamp and hid behind the hedge. The constable found it within minutes, and we slipped home across the Heath. The Professor said nothing, and neither did I."),
    "a4_j_day2": dict(title="The afternoon", source="Dr. Seward's diary",
                      text="By day we opened the coffin again. Lucy lay sleeping, redder and more beautiful than in death, with fresh blood on her lips and her teeth sharper. The Professor said: 'Now do you believe?' I did."),
    "a4_j_lucy_sleeping": dict(title="Lucy sleeping", source="Dr. Seward's diary",
                               text="She lay as in sleep, but not at rest. The Professor says she is Un-Dead and that we must fetch Arthur: it is his right, and his burden, to see her released."),
    "a4_j_arthur": dict(title="Arthur's consent", source="Dr. Seward's diary",
                        text="Arthur agreed to come. He was white as paper, but he said that if there was any chance of releasing her, he would take it. Quincey Morris stood beside him, silent and unshakeable."),
    "a4_j_vigil": dict(title="The vigil", source="Dr. Seward's diary",
                       text="We watched under the alders. The Bloofer Lady came with a child on her arm and called Arthur by name. The Professor held up the golden crucifix, and she fell back, hissing, as if burned."),
    "a4_j_lucy_down": dict(title="At dusk", source="Dr. Seward's diary",
                           text="At sunset she rose, with a smile that was not hers. We drove her back with the cross and our hands until she lay helpless. The Professor said, 'Now, friend Arthur, strike.'"),
    "a4_j_stake": dict(title="The stake", source="Dr. Seward's diary",
                       text="Arthur set the point above her heart and drove the stake home with three blows. The body arched, screamed, and was still. The Professor read the prayers while the tomb breathed out."),
    "a4_j_peace": dict(title="Peace", source="Dr. Seward's diary",
                       text="We did what remained: the head, the garlic, the lead case soldered shut. The face wore the sweetness of the girl I had loved. Arthur said, 'She smiled at me.' I think she did."),
    "a4_j_vow": dict(title="The vow", source="Dr. Seward's diary",
                     text="We swore on the vault door to hunt down the creature that did this. The Professor asked me for the use of my asylum, and for all the help I could give. It is a hard road, but I shall walk it."),
}

# ----------------------------------------------------------------------------------------------- combat
ENCOUNTERS_EXTRA = {
    "a4_lucy_vigil": dict(name="The Bloofer Lady at the tomb", time="night", enemies=["lucy"], flee_ok=False, survive=5,
                          intro="'Come to me, Arthur. My arms are hungry for you.' The golden crucifix is raised, but the child is still in her arms.",
                          win="She shrinks from the cross, hissing, and will not pass it.",
                          dawn_text="The first grey light touches the yews. She breaks away with a snarl and is gone toward the vault.",
                          location=""),
}

ENCOUNTER_HOOKS = {
    "a4_lucy_vigil": dict(
        on_win=[{"set": "a4_lucy_driven_back"}, {"protagonist": "vanhelsing"}, {"journal": "a4_j_vigil"},
                {"say": "She falls back before the crucifix, drops the child in the grass, and cannot reach her tomb: the Host along the door-crack holds her out. The Professor takes the child; Quincey lowers his rifle."}],
        on_lose=[{"heal": 1}, {"set": "a4_lucy_driven_back"}, {"protagonist": "vanhelsing"}, {"journal": "a4_j_vigil"},
                 {"say": "She bears us down for a moment, but the Professor holds the crucifix over our heads, and she shrinks. We rise, bruised. The child is safe in the grass."}]),
    "lucy_tomb": dict(
        on_win=[{"set": "a4_lucy_helpless"}, {"journal": "a4_j_lucy_down"},
                {"say": "She sinks back in the coffin, helpless and silent, as the Professor holds the cross. Now, while she lies, the stake must be set."}],
        on_lose=[{"heal": 1}, {"set": "a4_lucy_helpless"}, {"journal": "a4_j_lucy_down"},
                 {"say": "We are flung aside, and for a moment I think it is over. But the Professor presses the cross to her breast; she freezes, cries out, and lies still. The rite can go on."}]),
}

# ----------------------------------------------------------------------------------------------- recipes
RECIPES_EXTRA = {
    "a4_host_putty": dict(name="Host-putty", needs={"host": 1, "a4_putty": 1, "cloth": 1}, makes={"a4_host_putty": 1}, unlock="flag:rites",
                          text="The Host crumbled into soft putty, rolled in a clean napkin: a seal for every crack in the vault door."),
}

# ----------------------------------------------------------------------------------------------- seed variation
PALETTES = {
    "a4_hampstead_heath": [dict(floor="grass", tree="green"), dict(floor="grass", tree="dark"), dict(floor="dirt", tree="green")],
    "a4_north_hospital": [dict(wall="plaster", floor="planks", wood="pale", cloth="blue"), dict(wall="plaster_dirty", floor="planks", wood="oak", cloth="green")],
    "a4_seward_study": [dict(wall="plaster_dirty", floor="planks", wood="dark", cloth="blue"), dict(wall="plaster", floor="planks", wood="ebony", cloth="red"),
                        dict(wall="stone_grey", floor="planks", wood="oak", cloth="green")],
    "a4_paddington_hotel": [dict(wall="plaster", floor="planks", wood="pale", cloth="green"), dict(wall="plaster", floor="planks", wood="oak", cloth="blue")],
    "a4_hillingham_hall": [dict(wall="plaster", floor="planks", wood="oak", cloth="cream"), dict(wall="plaster_dirty", floor="planks", wood="dark", cloth="red")],
    "a4_jack_straws": [dict(wall="plaster_dirty", floor="planks", wood="dark", cloth="red"), dict(wall="stone_grey", floor="cobble", wood="oak", cloth="green")],
    "a4_westenra_tomb": [dict(wall="stone_tomb", floor="stone_dark"), dict(wall="stone_mossy", floor="stone_dark"), dict(wall="stone_dark", floor="cobble")],
}

PLACEMENTS = {
    "a4_pawn_ticket": [
        dict(prop="a4_hall_rug", text="Under the corner of the rug, where the maid dropped it in haste: a pawn ticket for one small gold crucifix.",
             hint="One corner of the rug has been lifted and put back crooked."),
        dict(prop="a4_hall_bookshelf", text="Tucked in the Prayer Book, folded small: a pawnbroker's ticket for a small gold crucifix.",
             hint="The Prayer Book on the shelf sticks out a little."),
        dict(prop="a4_undertaker_coffin", text="Under the coffin's brass handle, folded flat: a pawnbroker's ticket for a small gold crucifix.",
             hint="A scrap of paper pokes from beneath the coffin's handle."),
    ],
    "a4_key_blank": [
        dict(prop="a4_key_drawer", text="In the drawer, among odd wards, a blank of good brass, uncut. It will do.",
             hint="The drawer rattles with odd wards and blanks."),
        dict(prop="a4_key_tin", text="Beneath the other keys in the biscuit tin lies an uncut blank. Odd that I forgot it.",
             hint="The tin is heavier than a few old keys should make it."),
        dict(prop="a4_key_desk_blot", text="Under the blotter, where I put it for safety months ago: a brass blank.",
             hint="The blotter lies a little proud of the leather."),
    ],
}

GATES = {}
