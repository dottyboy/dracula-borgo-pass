"""Personal arc: Mina Murray - 'The Typewriter and the Trance'.
Exeter (school, typewriter, Bradshaw, the lost letter, Lucy's confidences) -> Whitby (notebook, Swales, coastguard, a quiet scare)
-> the first deliberate trance (water, wood, the swinging plumb) and the dream of the dark hold."""
from dsl import *

Q = "mina_records_"
M = "Mina Murray's journal"


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


def clue(speaker, text, jid, extra_set=None):
    """A one-node examine dialogue that records a journal entry."""
    do = [dict(journal=Q + jid)]
    if extra_set:
        do.append(dict(set=Q + extra_set))
    return D("a", a=N(speaker, text, do=do, end=True))


ARC = dict(
    id="mina_records", title="The Typewriter and the Trance", member="mina", portrait="mina",
    blurb="Before Dracula, there was Mina Murray: a schoolroom mystery, a stubborn typewriter, a lost letter chased through Bradshaw's "
          "timetables, and a dream of water and creaking wood that she is only beginning to understand.",
    unlock="roster:mina", unlock_text="Meet Mina in Whitby (Act II).", after_credits=False,
    start=dict(location=Q + "schoolroom", protagonist="mina", party=["mina"], items={Q + "notebook": 1}, flags=[]),
    exit_to="ARC_END",
    rewards=[dict(give="travel_shawl"), dict(give=Q + "keepsake"), dict(give="brandy"), dict(give="silver"),
             dict(stat=dict(member="mina", nerve=4, faith=1, acc=2)), dict(set=Q + "done")],
    rewards_text="+4 Nerve, +1 Faith, +2 Accuracy for Mina; her typewriter ribbon and shorthand notebook; a flask of brandy and a silver coin Gear: a travelling shawl.",
)

LOCATIONS = [
    dict(id=Q + "schoolroom", name="The schoolroom, Exeter", desc="Rows of ink-stained desks, a stove, a smell of chalk and wet wool. Somebody has stolen the speech-day prize.", date="May"),
    dict(id=Q + "typing_room", name="The typewriting room", desc="A narrow room under the eaves that Miss Hallam lets me use after lessons. One Remington stands under a dust-sheet, and it has not spoken for a year.", date="May"),
    dict(id=Q + "exeter_rooms", name="My rooms, Exeter", desc="Two small rooms over a draper's, a gas-ring, a window on the cathedral close and a table piled with shorthand exercises.", date="May"),
    dict(id=Q + "station", name="St. David's station, Exeter", desc="Steam, porters and the clatter of milk-churns. Everything here runs by the minute, and it is the only place in Exeter where I am entirely at ease.", date="May"),
    dict(id=Q + "whitby_rooms", name="The Crescent, Whitby", desc="Our lodgings on the West Cliff. Lucy's mother has the best chair and Lucy has the best view; I have the writing table.", date="July"),
    dict(id=Q + "east_cliff", name="East Cliff churchyard, dusk", desc="The seat on the cliff above the harbour, the Abbey black against a red sky, and the gravestones that tell such confident lies.", date="July"),
    dict(id=Q + "coastguard", name="The coastguard hut", desc="Charts, a brass telescope and a stove that smells of tarred rope.", date="July"),
    dict(id=Q + "whitby_night", name="Our bedroom, Whitby, at night", desc="Two beds, one sleeping girl, a curtain that breathes, and the sea saying one long word under the window.", date="July, night"),
    dict(id=Q + "dream", name="The dark hold", desc="Water laps somewhere. Timber creaks. I know this place and I have never been here.", date="Dream"),
]

LOC_DATA = {}

# ------------------------------------------------------------------------------------------------ SCHOOLROOM
LOC_DATA[Q + "schoolroom"] = dict(
    cells=[3, 2], interior=True, wall="plaster", floor="planks", ambient=AMBIENT["warm_day_interior"], camera=cam([3, 2]),
    lights=lights_warm([3, 2], energy=2.8),
    walls=dict(north=["wall_4", "wall_window_4", "wall_4"], west=["wall_door_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[0, 2.6], spawns={Q + "typing_room": [-4.4, -2.0], Q + "exeter_rooms": [4.4, 2.0]},
    props=[
        prop(Q + "s_hdesk", "table", "dark", -3.5, -2.6, name="Headmistress's desk", radius=0.9,
             look="Miss Hallam's desk: a ledger, a bell, and a pen-tray laid out as if for inspection."),
        prop(Q + "s_blotter", "book", "diary", -3.5, -2.6, y=0.8, name="Blotter", radius=0.2, talk=Q + "blotter"),
        prop(Q + "s_mdesk", "table", "oak", 2.5, -2.6, name="My desk", radius=0.9, look="Shorthand primers, a ruler, and a tin of hairpins I confiscated from the third form."),
        prop(Q + "s_pin", "key", "default", 2.0, -2.6, y=0.8, name="Hairpin", radius=0.2,
             look="A stout steel hairpin, the sort Pitman's disciples use to clean their pens.",
             take=Q + "hairpin", take_text="I take a hairpin. It has got more people out of trouble than any other single invention.", give_once=True),
        prop(Q + "s_redink", "bottle", "amber", 3.1, -2.6, y=0.8, name="Red ink", radius=0.2, talk=Q + "redink"),
        prop(Q + "s_cupboard", "bookshelf", "pale", 0.0, -3.6, name="Prize cupboard", radius=0.8, talk=Q + "cupboard"),
        prop(Q + "s_desk1", "table", "pale", -3.5, 0.6, name="Pupils' desk", radius=0.8, look="Initials cut with a compass-point, and a poem to a boy called Ernest."),
        prop(Q + "s_desk2", "table", "pale", -0.5, 0.6, name="Pupils' desk", radius=0.8, look="Tidy to a fault. Edith Marsh sits here and trusts nobody's blotting-paper but her own."),
        prop(Q + "s_desk3", "table", "pale", 2.5, 0.6, name="Pupils' desk", radius=0.8, look="Dora Pike's desk, with a page of sums folded very small under the lid."),
        prop(Q + "s_chair1", "chair", "black", -3.5, 1.6, rot=180, radius=0.4),
        prop(Q + "s_chair2", "chair", "black", -0.5, 1.6, rot=180, radius=0.4),
        prop(Q + "s_chair3", "chair", "black", 2.5, 1.6, rot=180, radius=0.4),
        prop(Q + "s_pegs", "bench", "oak", -5.4, 1.8, rot=90, name="Coat-pegs", radius=0.7, look="Eleven small hats, eleven small shawls, and one rain-cape that belongs to nobody."),
        prop(Q + "s_stove", "fireplace", "soot", 5.3, -1.2, rot=-90, name="Stove", radius=0.8, look="Banked for the summer. The kettle on top is the only warm thing in the room."),
        prop(Q + "s_bust", "bust", "plaster", 5.0, -3.2, name="Plaster Homer", radius=0.4, look="Blind, noble and chalk-dusted. The girls draw spectacles on him in Lent."),
        prop(Q + "s_rug", "rug", "cream", 0, 1.8, radius=0.1),
        prop(Q + "s_sconce", "sconce", "default", -5.7, 0.0, y=1.5, rot=90, radius=0.1),
        prop(Q + "s_sconce2", "sconce", "default", 5.7, 0.8, y=1.5, rot=-90, radius=0.1),
        prop(Q + "s_door_type", "door", "pale", -5.8, -2.0, rot=90, name="Door to the typewriting room", radius=0.6,
             look="A narrow door with a keyhole. Miss Hallam keeps it locked since the winter of the burst pipe.",
             go=Q + "typing_room", go_cond=f"has:{Q}typing_key", go_fail="Locked. Miss Hallam holds the key, and Miss Hallam will not lend it while a prize is missing from her cupboard."),
        prop(Q + "s_door_out", "door", "pale", 5.8, 2.0, rot=-90, name="Door to the street", radius=0.6,
             look="The way out, to my rooms and to the station.", go=Q + "exeter_rooms"),
    ],
    npcs=[
        npc(Q + "hallam", "human_peasant_f", "innkeeper_wife", -4.6, -1.0, rot=90, name="Miss Hallam",
            look="The headmistress, upright as a ruler, with spectacles she looks over rather than through.", talk=Q + "hallam_talk"),
        npc(Q + "edith", "human_peasant_f", "village_woman", -1.5, 2.6, rot=180, name="Edith Marsh",
            look="A girl of thirteen with a notebook of her own, in which she records, I suspect, the faults of her elders.", talk=Q + "edith_talk"),
        npc(Q + "dora", "human_peasant_f", "village_woman", 3.8, 2.4, rot=180, name="Dora Pike",
            look="Pale, quiet, a good hand at sums. Her sleeve-cuffs have been turned and re-turned until they are thin as paper.", talk=Q + "dora_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=Q + "j_morning")])],
)

# ------------------------------------------------------------------------------------------------ TYPING ROOM
LOC_DATA[Q + "typing_room"] = dict(
    cells=[2, 2], interior=True, wall="plaster_dirty", floor="planks", ambient=AMBIENT["candle_interior"], camera=cam([2, 2]),
    lights=lights_warm([2, 2]),
    walls=dict(north=["wall_4", "wall_window_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[2.4, -2.0], spawns={Q + "schoolroom": [2.8, -2.0]},
    props=[
        prop(Q + "t_table", "table", "ebony", -1.5, -2.2, name="Typing table", radius=0.9, look="A heavy table with four ink-rings and a place worn pale by two generations of elbows."),
        prop(Q + "t_machine", "chest", "ebony", -1.5, -2.2, y=0.8, scale=0.4, name="Remington typewriter", radius=0.5, talk=Q + "typewriter",
             use_item={
                 Q + "hairpin": [dict(say="I slide the hairpin under the tangled type-bars and ease them apart. Two of them click free, like a sigh."), dict(set=Q + "tw_freed")],
                 "oil": [dict(say="A drop on every pivot and a little on the carriage rail. The machine stops groaning."), dict(set=Q + "tw_oiled")],
                 Q + "ribbon": [dict(say="I wind the new ribbon onto the spools, black and sleek as a cat's back."), dict(set=Q + "tw_ribboned")],
             },
             use_fail="That will not help the Remington."),
        prop(Q + "t_dictation", "book", "diary", -2.2, -2.2, y=0.8, name="Dictation sheet", radius=0.2, talk=Q + "dictation"),
        prop(Q + "t_oil", "bottle", "amber", 0.4, -2.2, y=0.8, name="Oil-can", radius=0.2, look="A little can with a long spout, left by a mechanic who did not return.",
             take="oil", take_text="I take the oil-can's last good drops, decanted into a medicine phial.", give_once=True),
        prop(Q + "t_cupboard", "chest", "oak", 3.2, -3.0, name="Stationery cupboard", radius=0.6, look="Foolscap, quills, sealing-wax, and a great many tins that once held something else."),
        prop(Q + "t_shelf", "bookshelf", "dark", -3.5, -3.6, name="Shelf of primers", radius=0.8, look="Pitman, Gurney, Taylor: three fierce loyalties in one dusty row."),
        prop(Q + "t_basket", "barrel", "pale", 3.0, 0.2, scale=0.6, name="Waste-paper basket", radius=0.4, look="Spoiled pages, each wrong in a different and instructive way."),
        prop(Q + "t_chair", "chair", "green", -1.5, -1.0, rot=180, name="Typing chair", radius=0.4, look="Low and wobbly. A girl does not sit in it for pleasure."),
        prop(Q + "t_sconce", "sconce", "default", -3.7, 0.0, y=1.5, rot=90, radius=0.1),
        prop(Q + "t_rug", "rug", "blue", 0, 1.0, radius=0.1),
        prop(Q + "t_door", "door", "pale", 3.8, -2.0, rot=-90, name="Door to the schoolroom", radius=0.6, look="Back to chalk and girls.", go=Q + "schoolroom"),
    ],
    npcs=[
        npc(Q + "tuck", "human_peasant_f", "innkeeper_wife", -3.0, 0.8, rot=90, name="Miss Tuck",
            look="Retired from shorthand after forty years, she still taps her fingers on every table as if it were one.", talk=Q + "tuck_talk"),
    ],
)

# ------------------------------------------------------------------------------------------------ EXETER ROOMS
LOC_DATA[Q + "exeter_rooms"] = dict(
    cells=[3, 2], interior=True, wall="plaster", floor="planks", ambient=AMBIENT["warm_day_interior"], camera=cam([3, 2]),
    lights=lights_warm([3, 2], energy=2.6),
    walls=dict(north=["wall_4", "wall_window_4", "wall_4"], west=["wall_door_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[0, 2.6], spawns={Q + "schoolroom": [-4.4, -2.0], Q + "station": [4.4, 2.0]},
    props=[
        prop(Q + "r_table", "table", "oak", -1.0, -1.8, name="Exercise table", radius=0.9, look="Forty shorthand exercises, a pot of ink, a cold cup of tea. A pen lies where I put it down to think of Jonathan."),
        prop(Q + "r_exercises", "book", "leather", -1.5, -1.8, y=0.8, name="Shorthand exercises", radius=0.2, look="'Dear Sir, I beg to acknowledge...' in the fastest hand I have. Somewhere in the pile is a letter to Jonathan I have not dared send."),
        prop(Q + "r_shelf", "bookshelf", "dark", -4.0, -3.6, name="Book-shelf", radius=0.8, look="Bradshaw's Guide in four monthly numbers, the Bible, Tennyson, and a Baedeker for places I shall not see."),
        prop(Q + "r_bradshaw", "book", "red", -4.0, -3.5, y=1.2, name="Bradshaw's Guide", radius=0.2,
             look="My favourite reading. I could take the 7.15 to Plymouth with my eyes shut and tell you where it stops."),
        prop(Q + "r_window", "sconce", "default", 0.0, -3.7, y=1.9, name="Window on the Close", radius=0.2, look="The cathedral towers over the chimney-pots. The rooks quarrel about it every evening."),
        prop(Q + "r_sofa", "bench", "oak", 3.5, -3.0, name="Sofa", radius=0.9, look="Horsehair, and ruthless to the spine. Lucy says it was designed by someone who hated guests."),
        prop(Q + "r_gas", "candle", "white", 3.0, -1.0, y=0.0, scale=1.4, name="Gas-ring", radius=0.4, look="The gas-ring and its kettle. I have boiled a thousand eggs on it and loved none of them."),
        prop(Q + "r_rug", "rug", "red", 0.5, 1.0, radius=0.1),
        prop(Q + "r_trunk", "chest", "dark", -4.8, 1.0, rot=90, name="Travelling trunk", radius=0.6, talk=Q + "trunk"),
        prop(Q + "r_sconce", "sconce", "default", -5.7, 0.0, y=1.5, rot=90, radius=0.1),
        prop(Q + "r_sconce2", "sconce", "default", 5.7, 0.8, y=1.5, rot=-90, radius=0.1),
        prop(Q + "r_door_school", "door", "pale", -5.8, -2.0, rot=90, name="Door to the school", radius=0.6, look="Down the stairs and across the Close.", go=Q + "schoolroom"),
        prop(Q + "r_door_station", "door", "pale", 5.8, 2.0, rot=-90, name="Door to the street", radius=0.6, look="Ten minutes' walk to the station, eight if I do not look at the shop windows.", go=Q + "station"),
    ],
    npcs=[
        npc(Q + "pym", "human_peasant_f", "village_woman", 3.0, 1.6, rot=-90, name="Mrs. Pym",
            look="My landlady, who keeps the draper's below and a ledger of every letter that comes to the house.", talk=Q + "pym_talk"),
        npc(Q + "lucy_ex", "human_lucy", "lucy", 1.0, 0.4, rot=0, name="Lucy Westenra", cond=f"{Q}letter_got",
            look="Lucy, in a travelling dress, with a flush of excitement and a hat-box she has forgotten to unpack.", talk=Q + "lucy_night"),
    ],
)

# ------------------------------------------------------------------------------------------------ STATION
LOC_DATA[Q + "station"] = dict(
    cells=[3, 2], interior=False, wall="stone_grey", floor="cobble", ambient=AMBIENT["day_exterior"], camera=cam([3, 2]),
    lights=lights_day(),
    scatter=dict(asset="pine", variant="green", count=12, seed=21, avoid=[[-6, -4, 6, 4]]),
    spawn=[4.4, 2.0], spawns={Q + "exeter_rooms": [4.4, 2.0]},
    props=[
        prop(Q + "st_stand", "table", "dark", -4.0, -2.8, name="Timetable stand", radius=0.9, look="A slanting stand under glass, with a rail for the great books."),
        prop(Q + "st_bradshaw", "book", "red", -4.0, -2.8, y=0.8, name="Bradshaw's Guide (station copy)", radius=0.2, talk=Q + "bradshaw"),
        prop(Q + "st_carriage", "carriage", "dark", -1.0, -1.8, name="Third-class carriage", radius=1.2, look="A standing train: a carriage with a lamp for the dark and hard seats for the honest."),
        prop(Q + "st_office", "chest", "oak", 3.0, -3.0, name="Telegraph window", radius=0.7, look="A brass grille in a mahogany box. Behind it a young man listens to the whole country ticking."),
        prop(Q + "st_bench", "bench", "oak", 4.5, -1.0, rot=-90, name="Waiting bench", radius=0.8, look="Someone has carved 'Tiverton 14' in the seat, for reasons known to the carver."),
        prop(Q + "st_lamp", "lantern", "default", 1.5, -3.2, y=0.0, scale=1.3, name="Platform lamp", radius=0.3, look="A lamp that is lit at four every afternoon, even in June."),
        prop(Q + "st_churns", "barrel", "pale", 4.0, 2.4, name="Milk-churns", radius=0.5, look="Stamped with the name of a Devon farm and a number I find reassuring."),
        prop(Q + "st_fence", "fence", "default", -5.0, 2.6, radius=0.8),
        prop(Q + "st_sign", "signpost", "oak", 5.2, 2.2, name="Way to the town", radius=0.5, look="'To the city and the Close.'", go=Q + "exeter_rooms"),
    ],
    npcs=[
        npc(Q + "pomfret", "human_peasant_m", Q + "pomfret_v", 0.4, 0.8, rot=0, name="Mr. Pomfret, station-master",
            look="A man in a frock-coat who has not been late in nineteen years and does not intend to begin.", talk=Q + "pomfret_talk"),
        npc(Q + "hobbs", "human_peasant_m", Q + "coast_v", 2.6, -1.6, rot=0, name="Hobbs, telegraph clerk",
            look="A young clerk with ink on his cuffs and a faraway look, as if the wires hummed in his teeth.", talk=Q + "hobbs_talk"),
        npc(Q + "porter", "human_peasant_m", "villager", -2.6, 1.8, rot=90, name="Porter",
            look="A big man leaning on a barrow, eating a pasty with the concentration of a scholar.", talk=Q + "porter_talk"),
    ],
)

# ------------------------------------------------------------------------------------------------ WHITBY ROOMS
LOC_DATA[Q + "whitby_rooms"] = dict(
    cells=[3, 2], interior=True, wall="plaster", floor="planks", ambient=AMBIENT["warm_day_interior"], camera=cam([3, 2]),
    lights=lights_warm([3, 2], energy=2.8),
    walls=dict(north=["wall_4", "wall_window_4", "wall_window_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[3.5, 2.0], spawns={Q + "east_cliff": [4.4, 2.0], Q + "whitby_night": [-3.0, -1.0]},
    props=[
        prop(Q + "w_table", "table", "dark", -1.5, -1.0, name="Writing table", radius=0.9, look="Tide-tables, picture post-cards, and a clear space exactly the size of my notebook."),
        prop(Q + "w_notes", "book", "leather", -1.5, -1.0, y=0.8, name="Dream notes", radius=0.2, talk=Q + "dreamnotes"),
        prop(Q + "w_fire", "fireplace", "plaster", 0, -3.4, name="Fireplace", radius=0.9, look="Cold, with a ship in a bottle on the mantel that Mrs. Westenra thinks is an ornament and the landlord thinks is sacred."),
        prop(Q + "w_shelf", "bookshelf", "pale", 5.4, -2.0, rot=-90, name="Book-shelf", radius=0.7, look="Murray's Guide, Mrs. Radcliffe, and a single volume of sermons that has never been opened."),
        prop(Q + "w_settee", "bench", "oak", 2.2, -2.2, name="Settee", radius=0.9, look="Lucy's place. She lies on it and reads the end of novels."),
        prop(Q + "w_chair", "chair", "blue", -1.5, 0.5, rot=180, name="Writing chair", radius=0.4, look="Mine, by right of possession."),
        prop(Q + "w_window", "sconce", "default", 0.0, -3.7, y=1.9, name="Window on the harbour", radius=0.2, look="Boats come in by the dozen at four. From here I can count them and make myself no happier."),
        prop(Q + "w_rug", "rug", "green", 0.5, 1.0, radius=0.1),
        prop(Q + "w_sconce", "sconce", "default", -5.7, 0.0, y=1.5, rot=90, radius=0.1),
        prop(Q + "w_sconce2", "sconce", "default", 5.7, -0.5, y=1.5, rot=-90, radius=0.1),
        prop(Q + "w_stairs", "stairs", "planks", -4.6, -1.8, rot=90, name="Stairs to our bedroom", radius=0.9,
             look="Fourteen steps, of which the ninth complains.", go=Q + "whitby_night",
             go_cond=f"has:{Q}plumb", go_fail="It is still day, and I have one thing to do before I go up: I have something in mind to hang by a cord."),
        prop(Q + "w_door", "door", "pale", 5.8, 2.0, rot=-90, name="Front door", radius=0.6, look="Out to the cliff, the churchyard and the sea.", go=Q + "east_cliff"),
    ],
    npcs=[
        npc(Q + "lucy_w", "human_lucy", "lucy", 2.8, 1.0, rot=-90, name="Lucy Westenra", look="Lucy, rosy from the sea air, with a pencil behind one ear and the post-card of a lighthouse in her hand.", talk=Q + "lucy_whitby"),
        npc(Q + "maid_w", "human_peasant_f", Q + "westenra_v", -3.4, 1.6, rot=90, name="Mrs. Westenra",
            look="Lucy's mother, in grey silk and a lace cap, enjoying her tea with the air of a woman who has been told not to excite herself.", talk=Q + "westenra_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=Q + "j_whitby")])],
)

# ------------------------------------------------------------------------------------------------ EAST CLIFF
LOC_DATA[Q + "east_cliff"] = dict(
    cells=[3, 2], interior=False, wall="stone_grey", floor="grass", ambient=AMBIENT["dusk_exterior"], camera=cam([3, 2]),
    lights=lights_day(2.0), moon=dict(pos=[-6, 8, -6]),
    scatter=dict(asset="rock", variant="grey", count=14, seed=31, avoid=[[-6, -4, 6, 4]]),
    spawn=[4.4, 2.0], spawns={Q + "whitby_rooms": [4.4, 2.0], Q + "coastguard": [-3.0, 2.0]},
    props=[
        prop(Q + "c_seat", "bench", "dark", -3.5, -2.8, name="Mr. Swales' seat", radius=0.9, look="A bench of black wood, carved with the initials of four generations and one rude word."),
        prop(Q + "c_tomb1", "gravestone", "stone_grey", -1.0, -1.6, scale=1.1, name="Gravestone of Hannah Brough", radius=0.5, talk=Q + "tomb1"),
        prop(Q + "c_tomb2", "gravestone_point", "stone_mossy", 1.2, -1.2, scale=1.1, name="Gravestone of John Anson", radius=0.5, talk=Q + "tomb2"),
        prop(Q + "c_tomb3", "gravestone", "stone_dark", 3.2, -2.0, scale=1.1, name="Gravestone of Mary Dale", radius=0.5, talk=Q + "tomb3"),
        prop(Q + "c_cross", "grave_cross", "stone_mossy", -4.8, -0.4, name="Leaning cross", radius=0.4, look="It leans toward the sea, as if it wanted to be a sailor too."),
        prop(Q + "c_abbey", "tower", "stone_grey", 0.0, -7.0, scale=1.1, name="The Abbey", radius=1.6, look="Broken against the red sky. The sexton says a White Lady is seen in the great window at sunset."),
        prop(Q + "c_signal", "signpost", "oak", -5.0, 2.2, name="Path to the coastguard hut", radius=0.5, look="A zig-zag path down the cliff toward the pier.", go=Q + "coastguard"),
        prop(Q + "c_lamp", "lantern", "default", 4.3, -0.6, scale=1.2, name="Cliff lamp", radius=0.3, look="A lamp that the harbour-master lights when it pleases him."),
        prop(Q + "c_door", "signpost", "dark", 5.4, 2.3, name="Way up to the Crescent", radius=0.5, look="The road back to our lodgings.", go=Q + "whitby_rooms"),
    ],
    npcs=[
        npc(Q + "swales", "human_peasant_m", Q + "swales_v", -2.2, -1.6, rot=0, name="Mr. Swales",
            look="An ancient fisherman with a face like a walnut, smoking a pipe nobody has ever seen him light.", talk=Q + "swales_talk"),
        npc(Q + "bats", "bat", "black", 2.5, 1.4, rot=0, name="Bats under the eaves", radius=0.7, cond=f"!{Q}bats_driven",
            look="Two bats out hunting early, turning over my head in tighter and tighter circles. I do not like how they look at me.",
            fight=Q + "dusk_bats"),
    ],
    on_enter=[dict(once=True, do=[dict(say="The sun is going down behind the Abbey. A tiny bat flickers over the nearest tomb, and then another.")])],
)

# ------------------------------------------------------------------------------------------------ COASTGUARD
LOC_DATA[Q + "coastguard"] = dict(
    cells=[2, 2], interior=True, wall="plaster_dirty", floor="planks", ambient=AMBIENT["warm_day_interior"], camera=cam([2, 2]),
    lights=lights_warm([2, 2], energy=2.6),
    walls=dict(north=["wall_4", "wall_window_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[2.4, -2.0], spawns={Q + "east_cliff": [2.8, -2.0]},
    props=[
        prop(Q + "g_table", "table", "dark", -1.0, -2.4, name="Chart table", radius=0.9, look="Charts weighted with a mug, a knife and a sleeping cat."),
        prop(Q + "g_tide", "book", "diary", -1.4, -2.4, y=0.8, name="Tide-table", radius=0.2, talk=Q + "tidetable"),
        prop(Q + "g_scope", "lantern", "default", 0.0, -2.4, y=0.8, scale=1.3, name="Brass telescope", radius=0.2, look="A long brass glass lashed to its stand. It points at nothing at all right now, which is the best sort of target."),
        prop(Q + "g_stove", "fireplace", "soot", -3.4, -2.0, rot=90, name="Stove", radius=0.7, look="A stove that is always lit. The tea on it is a legend."),
        prop(Q + "g_rope", "barrel", "dark", 3.0, 0.8, name="Barrel of cordage", radius=0.5, look="Neat coils of spare line, tarred and ready."),
        prop(Q + "g_chest", "chest", "oak", -3.2, 1.2, name="Sea-chest", radius=0.6, look="Lead-lines and a dented flask. Locked, and it looks as if it likes being locked."),
        prop(Q + "g_sconce", "sconce", "default", -3.7, 0.0, y=1.5, rot=90, radius=0.1),
        prop(Q + "g_door", "door", "dark", 3.8, -2.0, rot=-90, name="Door to the cliff", radius=0.6, look="Out to the cliff path.", go=Q + "east_cliff"),
    ],
    npcs=[
        npc(Q + "coastguard_n", "human_peasant_m", Q + "coast_v", 0.6, 0.6, rot=0, name="The coastguard",
            look="A broad man who talks to the sea in a low voice, as one might to a large and doubtful dog.", talk=Q + "coastguard_talk"),
    ],
)

# ------------------------------------------------------------------------------------------------ WHITBY NIGHT
LOC_DATA[Q + "whitby_night"] = dict(
    cells=[3, 2], interior=True, wall="plaster", floor="planks", ambient=AMBIENT["cold_interior"], camera=cam([3, 2]),
    lights=[dict(pos=[0, 2.4, -1.0], color="#7090c0", energy=1.2, range=14), dict(pos=[-3.0, 1.9, 1.6], color="#ff9a40", energy=0.8, range=7)],
    walls=dict(north=["wall_4", "wall_window_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_4"]),
    spawn=[0, 2.6], spawns={Q + "whitby_rooms": [-4.0, -1.0], Q + "dream": [0, 2.6]},
    props=[
        prop(Q + "n_bed_l", "bed", "blue", 3.8, -2.0, name="Lucy's bed", radius=1.0, look="Lucy sleeps with one hand under her cheek, like a child in a picture."),
        prop(Q + "n_bed_m", "bed_simple", "green", -3.0, -2.4, name="My bed", radius=1.0, look="I have not slept in it yet. I am writing at the foot of it, which is almost the same."),
        prop(Q + "n_table", "table", "pale", -0.4, -2.6, name="Bedside table", radius=0.7,
             use_item={Q + "candle": [dict(say="I set the candle in its dish and strike a match. One flame, standing quite still."), dict(set=Q + "t_light")]},
             use_fail="That does not belong on the table.", look="A candle-dish, a prayer-book and a pencil."),
        prop(Q + "n_basin", "chest", "pale", -4.6, 0.8, rot=90, scale=0.8, name="Wash-basin", radius=0.6,
             use_item={"water": [dict(say="I pour the water into the basin, slowly. It laps once against the china, and laps again."), dict(set=Q + "t_water")]},
             use_fail="The basin wants water.", look="A china basin on a washstand, white as milk."),
        prop(Q + "n_jug", "bottle", "glass", -4.6, 1.8, y=0.0, scale=1.4, name="Water-jug", radius=0.3, look="A big jug of cold water, sweating on the boards.",
             take="water", take_text="I take the jug's water, a cupful poured into my little flask.", give_once=True),
        prop(Q + "n_bracket", "sconce", "default", 0.6, -3.5, y=2.2, name="Gas bracket", radius=0.3,
             use_item={Q + "plumb": [dict(say="I knot the cord to the bracket and let the plumb hang. It turns, very slowly, with a small bright eye in the candle-light."), dict(set=Q + "t_plumb")]},
             use_fail="Nothing hangs from there.", look="A dead gas bracket that nobody has lit since the gas was cut off."),
        prop(Q + "n_chair", "chair", "red", 0.0, 0.4, rot=180, name="Rocking-chair", radius=0.6, talk=Q + "trance",
             look="A rocking-chair that came with the room and has opinions about it."),
        prop(Q + "n_mantel", "fireplace", "plaster", 5.4, -1.4, rot=-90, name="Mantel", radius=0.8, look="A ship in a bottle and a small brass clock that has stopped at ten past three."),
        prop(Q + "n_chest", "chest", "dark", 4.8, 1.8, name="Linen chest", radius=0.6, look="Sheets, lavender, and the ghost of Mrs. Westenra's moth-balls."),
        prop(Q + "n_dresser", "bookshelf", "pale", -5.4, -0.8, rot=90, name="Dresser", radius=0.8, look="Hair-brushes, a hand-glass, and a small mirror that has never once flattered me."),
        prop(Q + "n_window", "sconce", "default", 0.0, -3.7, y=1.9, name="Window on the cliff", radius=0.2, talk=Q + "n_window_talk"),
        prop(Q + "n_rug", "rug", "blue", 0.5, 1.0, radius=0.1),
        prop(Q + "n_stairs", "stairs", "planks", -5.0, 2.4, rot=90, name="Stairs down", radius=0.9, look="Back down to the sitting-room.", go=Q + "whitby_rooms"),
    ],
    npcs=[
        npc(Q + "lucy_sleep", "human_lucy", "nightgown", 3.8, -0.6, rot=90, name="Lucy, asleep",
            look="Lucy, fast asleep, murmuring something about a ring. She looks entirely happy. I would not wake her for the world.", talk=Q + "lucy_sleeps"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=Q + "j_scare"), dict(say="The ninth stair complains behind me. I turn. Nobody is there, but the curtain is moving, and the window is shut.")])],
)

# ------------------------------------------------------------------------------------------------ DREAM
LOC_DATA[Q + "dream"] = dict(
    cells=[3, 2], interior=True, wall="planks", floor="planks", ambient=AMBIENT["crypt"], camera=cam([3, 2]),
    lights=[dict(pos=[0, 2.4, -1.0], color="#4060a0", energy=1.4, range=14), dict(pos=[3.0, 1.8, 1.8], color="#ffb060", energy=0.7, range=7)],
    walls=dict(north=["wall_4", "wall_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_4"]),
    spawn=[0, 2.6], spawns={Q + "whitby_night": [0, 2.6]},
    props=[
        prop(Q + "d_barrel1", "barrel", "dark", -3.4, -2.6, name="Dripping barrel", radius=0.6, talk=Q + "d_water"),
        prop(Q + "d_barrel2", "barrel", "ebony", -2.0, -3.0, radius=0.5),
        prop(Q + "d_timber", "table_long", "dark", 1.0, -3.0, name="Great timber", radius=1.2, talk=Q + "d_wood"),
        prop(Q + "d_chest", "chest", "ebony", 4.6, -2.0, name="Sea-chest", radius=0.6, look="Locked, rope-bound, wet to the touch. Wherever it was bound, it was not meant to be opened by me."),
        prop(Q + "d_crates", "chest", "dark", 4.8, 0.6, scale=0.8, radius=0.5),
        prop(Q + "d_lamp", "lantern", "default", 3.0, -1.0, scale=1.4, name="Swinging lantern", radius=0.3, look="It swings. It is the only thing in the room that moves with the water, and it is all I can look at."),
        prop(Q + "d_rope", "barrel", "pale", -4.6, 0.8, scale=0.6, name="Coil of rope", radius=0.4, look="A neat coil of rope. One end leads up, into the dark, toward a square of grey that might be the sky."),
        prop(Q + "d_cord", "stairs", "planks", 0.0, -0.6, scale=0.8, name="The cord and the ladder", radius=0.9, talk=Q + "d_cord",
             look="A ladder, and a cord beside it, a thread so fine I can feel it more than see it."),
        prop(Q + "d_hatch", "door", "ebony", -5.8, -2.0, rot=90, name="Hatch back to the bedroom", radius=0.6, look="A square of the room I fell asleep in.", go=Q + "whitby_night"),
    ],
    npcs=[],
    on_enter=[dict(once=True, do=[dict(say="Water laps. Timber creaks. My own breath sounds like someone else's. I tell myself it is a dream and that I may wake whenever I choose; I am not sure that is true.")])],
)

# ================================================================================================ DIALOGUE
DIALOGUE = {}

# ---- school mystery
DIALOGUE[Q + "hallam_talk"] = D(
    "n0",
    n0=N("Miss Hallam", "'Miss Murray. The Tennyson for Speech Day was in the cupboard at four last night. At eight this morning it was not. The cupboard was locked. Do you imagine, as I do, that books have no legs?'",
         choices=[
             C("Tell me exactly what was taken.", "n_what"),
             C("I think I can find out who did it.", "n_find", cond=f"!{Q}book_found&!{Q}hallam_asked", do=[dict(set=Q + "hallam_asked")]),
             C("Here is your Tennyson, Miss Hallam.", "n_return", cond=f"has:{Q}prize_book&!{Q}key_given"),
             C("About the typewriting room...", "n_type", cond=f"{Q}key_given"),
             C("[Leave]", end=True),
         ]),
    n_what=N("Miss Hallam", "'Tennyson's poems, in green morocco, with a gilt edge. Worth four guineas, and worth more to the girl who is to receive it. The cupboard shows no scratch; I keep the only key on the staff-room hook. Look to the cupboard, the blotter, and the girls, in that order.'", next="n0"),
    n_find=N("Miss Hallam", "'You are a young woman of more sense than the rest of the staff together. Find it, and I shall give you the key to the typewriting room, which you have been looking at like a dog at a butcher's shop since Christmas.'",
             do=[dict(journal=Q + "j_task")], next="n0"),
    n_return=N("Miss Hallam", "'Green morocco, gilt edge, not a thumb-mark. Who...? No. I shall not ask.' She takes a small iron key from her chatelaine. 'The typewriting room is yours after lessons. Do not teach the girls to use it before they have learned to spell.'",
               do=[dict(take=Q + "prize_book"), dict(give=Q + "typing_key"), dict(set=Q + "key_given"), dict(journal=Q + "j_key")], next="n0"),
    n_type=N("Miss Hallam", "'The Remington is a temperamental animal. Old Miss Tuck sits with it on Thursdays and understands it better than anyone. She taps on the table, which I take to be encouragement.'", next="n0"),
)

DIALOGUE[Q + "edith_talk"] = D(
    "n0",
    n0=N("Edith", "'Miss Murray! I have seen nothing. I have only heard everything, which is not the same.'",
         choices=[
             C("Who was in the schoolroom yesterday evening?", "n_who"),
             C("Is anyone in the form having a difficult time?", "n_dora", cond=f"{Q}edith_who"),
             C("You are a great help, Edith.", "n_help", cond=f"{Q}edith_who&!{Q}edith_praised", do=[dict(set=Q + "edith_praised")]),
             C("[Leave]", end=True),
         ]),
    n_who=N("Edith", "'Dora stayed to dust the staff-room. She does it on Wednesdays for her penny. Her mother is poorly in Heavitree, you know. Dora sews at night to pay for the doctor, and she does not like anyone to say so.'",
            do=[dict(set=Q + "edith_who"), dict(journal=Q + "j_edith")], next="n0"),
    n_dora=N("Edith", "'She has been writing letters in the dinner-hour. Always on the cheapest paper and always rubbing them out, as if the words were wrong. I should not tell, but you asked kindly.'", next="n0"),
    n_help=N("Edith", "'Then I shall expect to be Head Girl.' She writes something in her notebook. I should very much like to know what.", next="n0"),
)

DIALOGUE[Q + "dora_talk"] = D(
    "n0",
    n0=N("Dora", "'Good morning, Miss Murray. Is it about the book? I know nothing, truly.'",
         choices=[
             C("Show me your hands, Dora.", "n_cuff", cond=f"!journal:{Q}j_cuff"),
             C("Dora. The red smear on the cupboard lock, the letter on the blotter: I know it was you.", "n_accuse",
               cond=f"journal:{Q}j_cuff&journal:{Q}j_blotter&journal:{Q}j_cupboard&!{Q}book_found"),
             C("I think you took the book, but I cannot prove it yet.", "n_deny"),
             C("Thank you, Dora. [Leave]", end=True),
         ]),
    n_cuff=N("Mina", "She holds out her hands. They are clean. But the cuff of her sleeve has a mark on it, brick-red and shining, the shape of a thumb, and she keeps turning the mark inward as if she could hide it by looking away.",
             do=[dict(journal=Q + "j_cuff")], next="n0"),
    n_deny=N("Dora", "'You cannot prove anything because there is nothing, miss. I swear it on my mother.' She looks at the floor; there is a great deal of floor in that look.", next="n0"),
    n_accuse=N("Dora", "She says nothing for a long moment. Then her face crumples. 'I only wanted to copy out one poem. Mama has no books, and she cannot read much now, but I read to her, and she cried at the Tennyson when I read it from Edith's lesson. I meant to put it back on Friday. I used the red ink for the date, so I would remember when to return it. I never meant to keep it.'",
               choices=[
                   C("Take the book back and tell no one how it was found.", "n_forgive", do=[dict(set=Q + "dora_forgiven")]),
                   C("You must tell Miss Hallam yourself, Dora. I shall stand beside you.", "n_truth", do=[dict(set=Q + "dora_truth")]),
               ]),
    n_forgive=N("Dora", "She puts the book in my hands as if it were hot. 'Thank you. I shall copy it out by hand this Sunday, and put a penny in the poor-box for each verse.' I think she will.",
                do=[dict(give=Q + "prize_book"), dict(set=Q + "book_found"), dict(journal=Q + "j_book_found")], end=True),
    n_truth=N("Dora", "'Yes, miss.' She trembles, but she gets the words out. When the three of us stand at Miss Hallam's desk, the headmistress looks at the girl for a long moment and says only, 'You have chosen the hard way, Dora Pike, which is the only honest one.' The Tennyson goes into my hands, and later, I believe, a second copy goes into Dora's.",
              do=[dict(give=Q + "prize_book"), dict(set=Q + "book_found"), dict(journal=Q + "j_book_found")], end=True),
)

DIALOGUE[Q + "blotter"] = clue("Mina", "I hold Miss Hallam's blotter up to the mirror by the window. A letter, backwards, in a round hand that makes its capital D with a loop: 'Dearest Mama, I have it safe and I will read you the part about the Lady of Shalott. Do not tell Dr. B. that I...' The rest is smudged. The hand is a girl's.", "j_blotter")
DIALOGUE[Q + "redink"] = clue("Mina", "Red ink, which only the staff are supposed to use, for marking. The bottle is a quarter lower than it was last week. Someone has been dipping a pen where no pupil should.", "j_redink")
DIALOGUE[Q + "cupboard"] = clue("Mina", "The lock is unscratched, the hasp is whole: nobody forced it. On the brass escutcheon is a tiny smear of red ink, shining, a thumb-print. Whoever opened it had the key from the hook, and had been writing with the staff's red pen not an hour before.", "j_cupboard")

# ---- typing room
DIALOGUE[Q + "tuck_talk"] = D(
    "n0",
    n0=N("Miss Tuck", "'You have the key! I thought you would, in the end. Sit down, child. The Remington is a good machine with a bad temper. Ask it what it wants.'",
         choices=[
             C("What is wrong with it?", "n_wrong"),
             C("How do I free a jammed type-bar?", "n_jam", cond=f"!{Q}tw_freed"),
             C("The ribbon is dry as a leaf.", "n_ribbon", cond=f"!{Q}tw_ribboned"),
             C("It squeals like a gate.", "n_oil", cond=f"!{Q}tw_oiled"),
             C("Tell me something about shorthand.", "n_short"),
             C("[Leave]", end=True),
         ]),
    n_wrong=N("Miss Tuck", "'Three things, child, always three. The bars stick, the ribbon dries, the pivots rust. When a Remington is silent for a year, it has all three, like a bad marriage.'", next="n0"),
    n_jam=N("Miss Tuck", "'Something thin, steel, and not your fingernail. Girls have been unjamming type-bars with hairpins since the machine came over from America.'", next="n0"),
    n_ribbon=N("Miss Tuck", "'A new ribbon. They used to be kept in the stationery cupboard, or the shelf, or sometimes the waste-basket, when some careless girl had thrown away a perfectly good one. Look about.'", next="n0"),
    n_oil=N("Miss Tuck", "'There is an oil-can on the table. Do not use it all at once. A drop on every pivot, no more.'", next="n0"),
    n_short=N("Miss Tuck", "'It is the quickest way to learn what people mean rather than what they say. You will be a great help to your young man with it. Is he fond of dictation?' 'He has never dictated to me in his life, Miss Tuck.' 'Then he is a fool or a gentleman. Probably both.'", next="n0"),
)

DIALOGUE[Q + "dictation"] = D(
    "a",
    a=N("Mina", "The dictation sheet is in my own shorthand, from Mr. Hawkins's last letter to the school: 'Please confirm that the old house at Purfleet, called Carfax, with its chapel and twenty acres, is secured for the Count, and that the deeds go to Transylvania by the post of the ninth instant.' Twenty acres, the ninth instant, Carfax at Purfleet. I commit it to memory.",
        do=[dict(journal=Q + "j_dictation")], end=True))

DIALOGUE[Q + "typewriter"] = D(
    "n0",
    n0=N("Mina", "The Remington sits under its dust-sheet like a patient waiting to be seen.",
         choices=[
             C("Try the keys.", "n_jam", cond=f"!{Q}tw_freed"),
             C("Try the keys.", "n_oil", cond=f"{Q}tw_freed&!{Q}tw_oiled"),
             C("Try the keys.", "n_ribbon", cond=f"{Q}tw_freed&{Q}tw_oiled&!{Q}tw_ribboned"),
             C("Type the dictation sheet.", "n_type", cond=f"{Q}tw_freed&{Q}tw_oiled&{Q}tw_ribboned&!{Q}typed"),
             C("Post the typed page to Mr. Hawkins.", "n_post", cond=f"{Q}typed&!{Q}posted"),
             C("[Step back]", end=True),
         ]),
    n_jam=N("Mina", "Three keys rise and refuse to come down; the type-bars have tangled in a little steel knot. Something thin would free them.", next="n0"),
    n_oil=N("Mina", "The bars move now, but the carriage squeals like a gate and the pivots grind. It wants oil.", next="n0"),
    n_ribbon=N("Mina", "The keys strike beautifully, and leave nothing behind. The ribbon is dry as a dead leaf. It wants a new one.", next="n0"),
    n_type=N("Mina", "The Remington is mended. I feed in a sheet of foolscap, and the machine waits with a little ratchet-click for me to begin. What did the sheet say?",
             choices=[
                 C("'... Carfax at Purfleet, with its chapel and twenty acres, the deeds to go by the post of the ninth instant.'", "n_good", cond=f"journal:{Q}j_dictation"),
                 C("'... Carfax at Purfleet, with its chapel and twelve acres, the deeds by the ninth instant.'", "n_bad"),
                 C("'... Carfax at Whitby, with twenty acres, the deeds by the nineteenth instant.'", "n_bad"),
                 C("[Look at the dictation sheet again]", "n0"),
             ]),
    n_bad=N("Mina", "The page comes out clean and wrong. Miss Tuck, passing, taps the table. 'No, child. Read it again.' I rip it out, and feed in another sheet.", next="n_type"),
    n_good=N("Mina", "The keys go down like rain on a roof, and the carriage bell rings at every line. Eleven lines, no errors, and the margins as straight as a ruled slate. It is the most satisfying thing I have done since I learned my times-tables.",
             do=[dict(give=Q + "typed_page"), dict(set=Q + "typed"), dict(journal=Q + "j_typed")], next="n0"),
    n_post=N("Mina", "I fold the page, direct it to Mr. Hawkins's office, and drop it into the post-box in the passage, with a note: 'Miss W. Murray, if the Remington is spoken of at all.' It is the first thing I have sent that has not been written in my own hand. I expect nothing and hope for everything.",
             do=[dict(take=Q + "typed_page"), dict(set=Q + "posted")], next="n0"),
)

# ---- Exeter rooms
DIALOGUE[Q + "pym_talk"] = D(
    "n0",
    n0=N("Mrs. Pym", "'Good day, Miss Murray. Nothing in the post for you today, I am afraid. Nothing, nothing.' She has a sad way of saying it, as though the letters were her own children kept from her.",
         choices=[
             C("Is there a reply from Mr. Hawkins's office?", "n_reply", cond=f"{Q}posted&!{Q}reply_got"),
             C("Nothing from Mr. Harker at all?", "n_none", cond=f"!{Q}reply_got"),
             C("Thank you for waiting up for me, Mrs. Pym.", "n_thanks", cond=f"{Q}reply_got"),
             C("[Leave]", end=True),
         ]),
    n_none=N("Mrs. Pym", "'Not a line since he went abroad, my dear. And no one in the town knows where abroad is. I did hear Mr. Hawkins is quite uneasy himself.'", next="n0"),
    n_reply=N("Mrs. Pym", "'This came by the afternoon delivery. Typed, so it must be important. A clerk wrote it for Mr. Hawkins. He says...' She hands me the envelope. 'You had better read it yourself, dear.'",
              do=[dict(give=Q + "hawkins_reply"), dict(set=Q + "reply_got"), dict(journal=Q + "j_reply")], next="n0"),
    n_thanks=N("Mrs. Pym", "'There, there. Go and be clever at the station, if it will make you feel better. Though I wish you would take a shawl.'", next="n0"),
)

DIALOGUE[Q + "lucy_night"] = D(
    "n0",
    n0=N("Lucy", "'Mina! Do not look at me like that. I am here for the whole night and I intend to sit up on your sofa and be miserable on principle. Have you heard from Jonathan?' 'Not a word, Lucy. But I have this.' I put the letter in her hand.",
         choices=[
             C("Read the letter aloud.", "n_read", cond=f"!{Q}c1"),
             C("Lucy, tell me about the three men.", "n_suitors", cond=f"!{Q}c2"),
             C("Lucy, I have a strange dream. I want to tell someone.", "n_dream", cond=f"!{Q}c3"),
             C("Good night, Lucy.", "n_night", cond=f"{Q}c1&{Q}c2&{Q}c3&!{Q}confided"),
             C("[Not yet]", end=True),
         ]),
    n_read=N("Mina", "I read the letter, the one that took twelve days and a Taunton stationmaster to reach me: 'Beloved Mina, I write from the Golden Krone at Bistritz. The landlady pressed a little cross on me at parting and cried; I took it to be superstition and humoured her. Tomorrow I drive into the mountains, and I shall be among strangers for a month. I wish you were beside me, with your shorthand and your timetables. Wait for me, and do not be anxious. Your own Jonathan.' Lucy has her hand at her mouth. 'Oh, Mina.'",
             do=[dict(set=Q + "c1"), dict(journal=Q + "j_letter")], next="n0"),
    n_suitors=N("Lucy", "'Three of them, Mina! Dr. Seward, who looks at me as if I were an interesting case; Mr. Morris, who is a Texan and makes me laugh; and Arthur Holmwood, who is a gentleman, and kind, and very big and very blushing. I cannot decide. How does one decide?' 'I think,' I say, 'one doesn't. One finds that one has.' Lucy thinks this over. 'Why can't a girl marry all three?' 'I have absolutely no answer.'",
                 do=[dict(set=Q + "c2")], next="n0"),
    n_dream=N("Mina", "'I dream of water, Lucy. Always the same: lapping, very close, and then the creak of wood, as of a floor or a ship's side, and then I am not in my body at all, and something calls me by a name I cannot catch. In the morning I am perfectly well and perfectly tired.' Lucy, who tells me everything, is quiet. 'That would frighten me,' she says, at last. 'It frightens me too,' I say. 'But only in the way a locked door does: because I do not know what is behind it.'",
              do=[dict(set=Q + "c3"), dict(journal=Q + "j_firstdream")], next="n0"),
    n_night=N("Lucy", "'Mina, I mean to say this once.' She takes my hand. 'He will write. He is not the kind of man who forgets. And if he does not, I shall find him myself and shake him. Meanwhile, come to Whitby with Mother and me. The sea air will cure your dreams, or at least change them.' We lie awake until the rooks begin, talking in whispers about men and trains.",
             do=[dict(set=Q + "confided"), dict(journal=Q + "j_confide")], end=True),
)

DIALOGUE[Q + "trunk"] = D(
    "n0",
    n0=N("Mina", "My travelling trunk stands open. Shorthand, a spare petticoat, a favourite novel, and a space where the hope goes.",
         choices=[
             C("Pack, and take the morning train to Whitby.", "n_go", cond=f"{Q}confided"),
             C("Not yet; there is still something to do in Exeter.", "n_wait", cond=f"!{Q}confided"),
             C("[Leave it open]", end=True),
         ]),
    n_wait=N("Mina", "I cannot leave Exeter with the question of Jonathan's letter still open in my head.", next="n0"),
    n_go=N("Mina", "I close the lid. The key turns, like a small decision.",
           do=[dict(card="July. Whitby. The summer I would later call the happiest and the saddest of my life: and the one in which I first heard the sea call my name."), dict(goto=Q + "whitby_rooms")], end=True),
)

# ---- station
DIALOGUE[Q + "bradshaw"] = D(
    "a",
    a=N("Mina", "I know the book by heart, but I read it anyway, the way other people say their prayers. The pages for the Bristol line: 'Exeter St. David's, dep. 10.20, stops at Tiverton (10.55), Taunton 11.30. Dep. 10.50, express, non-stop, Taunton 11.40. Dep. 11.15, stops at Tiverton, Taunton 12.05.' A girl could live and die by a table like this.",
        do=[dict(journal=Q + "j_bradshaw")], end=True))

DIALOGUE[Q + "porter_talk"] = D(
    "n0",
    n0=N("Porter", "'Mornin', Miss. Lovely weather for trains.' He swallows. 'Mr. Pomfret's in a stew over a bag.'",
         choices=[
             C("What kind of bag?", "n_bag"),
             C("Did you see the mail-bag go?", "n_see", cond=f"{Q}reply_got"),
             C("[Leave]", end=True),
         ]),
    n_bag=N("Porter", "'A mail-bag, with a registered letter in it. The sorter says it went on the first train after the half-past-ten sorting. I say it never did.'", next="n0"),
    n_see=N("Porter", "'Well, I heard the guard say as the train had blown clean through Tiverton, which as you know it never does. So it was not a stopper, Miss. That's all I know.'",
            do=[dict(set=Q + "porter_clue")], next="n0"),
)

DIALOGUE[Q + "pomfret_talk"] = D(
    "n0",
    n0=N("Mr. Pomfret", "'Miss Murray. I know you; you are the young lady who corrects my timetable. I shall have you know it was a misprint.'",
         choices=[
             C("Mr. Hawkins's clerk writes that a registered letter for me has gone astray on this line.", "n_letter", cond=f"has:{Q}hawkins_reply&!{Q}told"),
             C("I think I know where the bag went.", "n_wire", cond=f"{Q}told&!{Q}wired"),
             C("Thank you, Mr. Pomfret. [Leave]", end=True),
         ]),
    n_letter=N("Mr. Pomfret", "'Ah. The Taunton bag. The sorter swears it went on the first train out after the half-past-ten sorting. The porter swears it did not stop at Tiverton, since the guard saw it on the van-floor when they roared through. I only know that it is somewhere between here and Bristol. Name me the train, and Hobbs will wire the right station-master.'",
               do=[dict(set=Q + "told"), dict(journal=Q + "j_bradshaw2")], next="n0"),
    n_wire=N("Mr. Pomfret", "'Which train, then? Think, Miss Murray. You have Bradshaw by heart.'",
             choices=[
                 C("The 10.20, which stops at Tiverton.", "n_wrong"),
                 C("The 10.50 express, non-stop to Taunton.", "n_right", cond=f"journal:{Q}j_bradshaw&journal:{Q}j_bradshaw2"),
                 C("The 11.15, which stops at Tiverton.", "n_wrong"),
                 C("[Let me check Bradshaw again]", end=True),
             ]),
    n_wrong=N("Mr. Pomfret", "'That train called at Tiverton, Miss Murray, or left before the half-past-ten sorting, or both. It could not have carried the bag. Think again.'", next="n_wire"),
    n_right=N("Mr. Pomfret", "He consults his watch, then Bradshaw, then me. 'The ten-fifty. After the sorting, and clean through Tiverton. By George, Miss Murray, if you ever tire of teaching, I shall find you a place at the Great Western.' He snaps his fingers at Hobbs. 'Wire Taunton.'",
                do=[dict(set=Q + "wired"), dict(journal=Q + "j_wire")], end=True),
)

DIALOGUE[Q + "hobbs_talk"] = D(
    "n0",
    n0=N("Hobbs", "'The wire is warm, miss. Mr. Pomfret has had me tapping to Taunton since the clock struck.'",
         choices=[
             C("Is there any answer from Taunton?", "n_answer", cond=f"{Q}wired&!{Q}letter_got"),
             C("What are you listening for?", "n_what"),
             C("[Leave]", end=True),
         ]),
    n_what=N("Hobbs", "'The click before the click, miss. You can hear a man hesitate over a word. That is the thing no one writes in the books.'", next="n0"),
    n_answer=N("Hobbs", "He reads off the tape. '\"Bag found under van seat, registered letter M. Murray, Exeter, intact. Forwarded by next down train.\" And here it is, miss, in the guard's own hand.' A thick envelope, soft at the corners, with a foreign stamp and Jonathan's handwriting. I have to sit on the bench.",
              do=[dict(give=Q + "lost_letter"), dict(set=Q + "letter_got"), dict(journal=Q + "j_letter_found")], end=True),
)

# ---- Whitby
DIALOGUE[Q + "dreamnotes"] = clue("Mina", "My notebook of dreams, in shorthand, tucked behind the tide-tables where Lucy will never look. 'It always begins with the water, lapping, near enough to touch. Then the wood, a creak, then another. Then the darkness, a single point turning in it, and I forget my name. Water, wood, swing. Always in that order, and always before I wake.' I underline 'always'.", "j_dreamorder")

DIALOGUE[Q + "lucy_whitby"] = D(
    "n0",
    n0=N("Lucy", "'Mina, you have been writing for two hours! Mother says you will ruin your eyes, and I say you have ruined your appetite. Come and see Mr. Swales this evening: he tells the most dreadful stories.'",
         choices=[
             C("What does he say about the tombs?", "n_tombs"),
             C("Have you seen the coastguard?", "n_coast"),
             C("[Leave]", end=True),
         ]),
    n_tombs=N("Lucy", "'That every stone in the churchyard lies, and that you can tell which by doing sums. He is a terrible old humbug. He says the dead are not more than a dozen yards from the sea, and that the sea does not give them up.'", next="n0"),
    n_coast=N("Lucy", "'The one with the telescope? He is a dear. He lets me look at the ships. He will let you, too, if you ask him about the tides: it is the only thing he is ever vain of.'", next="n0"),
)

DIALOGUE[Q + "westenra_talk"] = D(
    "a",
    a=N("Mrs. Westenra", "'Mina, dear. You must not stand about. And the damp! Lucy, put a shawl on. I have been told the sea air is excellent for the nerves, and my nerves are certainly in need of something.' She sips her tea and looks thoughtfully at the window. 'I am so glad you came.'", end=True))

DIALOGUE[Q + "swales_talk"] = D(
    "n0",
    n0=N("Mr. Swales", "'Eh, lass. Ye're the one wi' the notebook. Sit ye down and ask. I'll tell ye nowt for nowt, but I'll tell ye plenty for a good question.'",
         choices=[
             C("They say the stones here lie, Mr. Swales.", "n_lie"),
             C("Which of these three tombs tells the biggest lie?", "n_pick", cond=f"{Q}swales_asked&!{Q}tomb_solved"),
             C("How do the tides run, Mr. Swales?", "n_tides", cond=f"!{Q}has_rule"),
             C("What do you make of the creak and the lap of the sea?", "n_creak", cond=f"{Q}tomb_solved"),
             C("Good evening, Mr. Swales. [Leave]", end=True),
         ]),
    n_lie=N("Mr. Swales", "'Aye, every one. They bury a man and write down what pleases the widow. But there's one o' them three as cannot do a sum, and a stone that cannot count is a stone that's lying. Find it, and I'll show ye summat the parson doesn't know.'",
            do=[dict(set=Q + "swales_asked"), dict(journal=Q + "j_swales")], next="n0"),
    n_pick=N("Mr. Swales", "'Well, lass? Which stone cannot count?' (Read the three stones: Hannah Brough, John Anson, Mary Dale. Compare birth, death and age.)",
             choices=[
                 C("Hannah Brough: born 1785, died 1830, aged 43.", "n_right", cond=f"journal:{Q}j_tomb1&journal:{Q}j_tomb2&journal:{Q}j_tomb3"),
                 C("John Anson: born 1765, died 1795, aged 30.", "n_wrong"),
                 C("Mary Dale: born 1790, died 1810, aged 20.", "n_wrong"),
                 C("[Go and read the stones again]", end=True),
             ]),
    n_wrong=N("Mr. Swales", "'Nay. Count it again, lass, from the year she was born to the year she died.'", next="n_pick"),
    n_right=N("Mr. Swales", "'Aye! Eighteen thirty less seventeen eighty-five is forty-five, and the stone says forty-three. The widower paid the mason by the letter, ye see.' He chuckles, then rummages in his coat and produces a dog-eared almanac. 'Here. The sea keeps a calendar, too. Tides run later by fifty minutes each day. Every sailor knows it. Take it, and make the coastguard a fool for once.'",
              do=[dict(set=Q + "tomb_solved"), dict(set=Q + "has_rule"), dict(give=Q + "almanac"), dict(journal=Q + "j_almanac")], next="n0"),
    n_tides=N("Mr. Swales", "'Ask me that when ye've shown me ye can count.'", next="n0"),
    n_creak=N("Mr. Swales", "'The sea speaks to them as listens, lass. I've heard it call my name on a dead-calm night. Ye'd best not answer it till ye're sure who is calling.' He looks at me sideways. 'Ye've a listening face, lass. Mind it.'", next="n0"),
)

DIALOGUE[Q + "tomb1"] = clue("Mina", "'Hannah Brough, born 1785, died 1830, aged 43 years. She was a faithful wife and a good neighbour, and a boat's width from her husband.' Born 1785, died 1830; I put the numbers away to be added up in a quiet moment.", "j_tomb1")
DIALOGUE[Q + "tomb2"] = clue("Mina", "'John Anson, master mariner, born 1765, died 1795, aged 30 years. Lost off the Scar and not found.' A stone over an empty grave. The figures are neat and the sum is good.", "j_tomb2")
DIALOGUE[Q + "tomb3"] = clue("Mina", "'Mary Dale, spinster, born 1790, died 1810, aged 20 years. She died as she lived: quietly.' The lettering is deep and clean and the sum is exactly right.", "j_tomb3")

DIALOGUE[Q + "tidetable"] = D(
    "a",
    a=N("Mina", "The coastguard's tide-table, pinned flat with a mug. It lists only Monday: high water at 4.10 in the morning and 4.35 in the afternoon. 'Next high water on Wednesday?' has been pencilled in the margin by a hand that has clearly given up on its own arithmetic.",
        do=[dict(journal=Q + "j_tide")], end=True))

DIALOGUE[Q + "coastguard_talk"] = D(
    "n0",
    n0=N("Coastguard", "'Miss. Come in, mind the cat.' He is very proud of the tide-table and a little embarrassed about the pencil in the margin. 'Hmm. Tell me, now you are here: Monday's afternoon high water is at 4.35. When will it be on Wednesday afternoon?'",
         choices=[
             C("A quarter past six, by my reckoning.", "n_right", cond=f"journal:{Q}j_tide&journal:{Q}j_almanac&!{Q}tide_solved"),
             C("Half past five.", "n_wrong", cond=f"!{Q}tide_solved"),
             C("Seven o'clock.", "n_wrong", cond=f"!{Q}tide_solved"),
             C("Four o'clock, the same as Monday.", "n_wrong", cond=f"!{Q}tide_solved"),
             C("Tell me about the telescope.", "n_scope"),
             C("[Leave]", end=True),
         ]),
    n_wrong=N("Coastguard", "'No, miss. The tide does not keep pace with the town clock. Look at the table again, and ask someone who knows the rule.'", next="n0"),
    n_right=N("Coastguard", "'Fifty minutes later each day, two days on: a hundred minutes. Four thirty-five and an hour forty makes a quarter past six. Right to the minute, miss!' He is delighted, and a little hurt. 'Here, a gift for a young woman who can count.' He unhooks a brass plumb-bob from a lead-line, a cord knotted round the neck. 'A plumb is a pendulum, miss; hang it in a room and it will tell you what the room is thinking.'",
              do=[dict(set=Q + "tide_solved"), dict(give=Q + "plumb"), dict(journal=Q + "j_plumb")], next="n0"),
    n_scope=N("Coastguard", "'It looks at what I cannot see. That's the whole of the trade. A coastguard is a man paid to expect something.' He glances out at the sea, and for a moment looks very tired. 'I have been expecting it for thirty years.'", next="n0"),
)

DIALOGUE[Q + "n_window_talk"] = D(
    "a",
    a=N("Mina", "Outside: the cliff, the churchyard, the sea. On the sill, a damp mark the shape of a small hand, as of someone who stood outside and looked in. It dries as I watch. I tell myself it is only the sea air. I do not tell Lucy.",
        do=[dict(journal=Q + "j_window")], end=True))

DIALOGUE[Q + "lucy_sleeps"] = D(
    "a", a=N("Lucy", "She murmurs 'Arthur...' and turns over. I tuck the sheet round her. Whatever else the summer brings, she is happy tonight, and I should like that to be the first thing recorded about it.", end=True))

# ---- the trance
DIALOGUE[Q + "trance"] = D(
    "n0",
    n0=N("Mina", "The rocking-chair stands in the middle of the room, as if it had been put there for the purpose. The candle is lit, the water waits in the basin, the plumb hangs from the bracket. I sit.",
         choices=[
             C("Begin.", "n_start", cond=f"{Q}t_light&{Q}t_water&{Q}t_plumb&!{Q}trance_done"),
             C("I am not ready: there is something in the room still unprepared.", "n_notready"),
             C("[Get up]", end=True),
         ]),
    n_notready=N("Mina", "A trance wants three things: a flame to look at, water to listen to, and something that hangs and turns. The candle, the basin, the plumb. I must prepare them before I sit.", next="n0"),
    n_start=N("Mina", "The room goes quiet. What should I do first? In my dream notes there is an order, and I have always obeyed it.",
              choices=[
                  C("Listen to the water lapping in the basin.", "n_s2"),
                  C("Rock the chair so that the boards creak.", "n_break"),
                  C("Watch the plumb turn in the candle-light.", "n_break"),
              ]),
    n_s2=N("Mina", "Lap. Lap. A small, slow water, very near, like a hand being passed gently over a face. I forget the room.",
           choices=[
               C("Rock the chair so that the boards creak.", "n_s3"),
               C("Watch the plumb turn in the candle-light.", "n_break"),
           ]),
    n_s3=N("Mina", "The chair rocks. The boards creak: one, two, a long groan like a ship at her moorings. I am not in the room any more, or only the least part of me is.",
           choices=[
               C("Watch the plumb turn in the candle-light.", "n_win"),
               C("Listen to the water again.", "n_break"),
           ]),
    n_break=N("Mina", "It does not work. The water is only water, the boards only boards, and the plumb a dull weight on a string. I feel foolish and a little relieved. The old order must be kept. I try again.", next="n_start"),
    n_win=N("Mina", "The plumb turns: a small bright eye. The candle lengthens into a line. The lapping comes from everywhere, and I am no longer Mina Murray in a rocking-chair, but a listening thing in a very dark place that is also a very quiet one...",
            do=[dict(set=Q + "trance_done"), dict(journal=Q + "j_trance"),
                dict(card="She did not know it, but it was the first time she had walked into that country on purpose. Years later, in a London drawing-room, the Professor would say: 'Where are you now, Madam Mina? What do you hear?' And she would answer him with the very words she found tonight."),
                dict(goto=Q + "dream")], end=True),
)

# ---- the dream
DIALOGUE[Q + "d_water"] = D(
    "a",
    a=N("Mina", "The barrel drips: a slow, loud plink into a puddle that has no bottom. I put a hand on it and the lapping rises through the wood into my wrist. Water, near and rhythmic. This is the first of the three, as it always is.",
        do=[dict(set=Q + "heard_water"), dict(journal=Q + "j_hold1")], end=True))
DIALOGUE[Q + "d_wood"] = D(
    "a",
    a=N("Mina", "The great timber groans as the hull settles. It has a voice, long and patient, like an old man shifting in his sleep. I listen until I can tell it from my own heartbeat. Wood, the second of the three.",
        do=[dict(set=Q + "heard_wood"), dict(journal=Q + "j_hold2")], end=True))
DIALOGUE[Q + "d_cord"] = D(
    "n0",
    n0=N("Mina", "The cord is thin as a hair and cold as a wire. It leads up the ladder and out of the hold. I cannot see its end.",
         choices=[
             C("Follow the cord, and listen for what it is tied to.", "n_follow", cond=f"{Q}heard_water&{Q}heard_wood"),
             C("Not yet: I have not listened enough.", "n_wait", cond=f"!{Q}heard_water|!{Q}heard_wood"),
             C("[Step back]", end=True),
         ]),
    n_wait=N("Mina", "I know better than to climb a thing I have not first listened to. The water, the wood: I must hear them both.", next="n0"),
    n_follow=N("Mina", "I take the cord between two fingers, and it hums. Somewhere far above me a bell is struck; somewhere far away a man is breathing, deep in the dark, and does not know I am here. I open my eyes in Whitby, in the rocking-chair, with the candle burned to a stub, the plumb still, and Lucy sound asleep.\n\nI shall tell no one. Not yet.",
             do=[dict(journal=Q + "j_end"),
                 dict(card="The Typewriter and the Trance. She kept the ribbon from the Remington and the notebook from Whitby in the same drawer, and neither was ever empty of use. When Dr. Seward's asylum, the Count's Carfax and a ship called the Demeter drew the threads together, she knew the sound of the dark, because she had been listening to it for years."),
                 dict(arc_end=1)], end=True),
)

# ================================================================================================ ITEMS
ITEMS = {
    Q + "notebook": dict(name="Shorthand notebook", asset="book", variant="leather", desc="Mina's shorthand notebook: tides, timetables, dreams, and the unanswered questions about Jonathan."),
    Q + "hairpin": dict(name="Steel hairpin", asset="key", variant="default", desc="A stout steel hairpin that frees jammed type-bars."),
    Q + "ribbon": dict(name="Typewriter ribbon", asset="rug", variant="black", desc="A fresh, glossy black ribbon for the Remington."),
    Q + "prize_book": dict(name="Tennyson prize book", asset="book", variant="red", desc="The Speech Day Tennyson in green morocco, gilt-edged and recovered."),
    Q + "typing_key": dict(name="Typewriting-room key", asset="key", variant="gold", desc="A small iron key from Miss Hallam's chatelaine."),
    Q + "typed_page": dict(name="Typed page", asset="book", variant="diary", desc="A beautifully typed letter, eleven lines with no errors."),
    Q + "hawkins_reply": dict(name="Mr. Hawkins's reply", asset="book", variant="leather", desc="A typed note from Mr. Hawkins's office: a registered letter for Miss Murray has gone astray on the Bristol line."),
    Q + "lost_letter": dict(name="Jonathan's lost letter", asset="book", variant="diary", desc="Jonathan's letter from Bistritz, twelve days late, soft at the corners."),
    Q + "almanac": dict(name="Swales' almanac", asset="book", variant="leather", desc="A dog-eared almanac. The margin notes: 'Tides run fifty minutes later each day.'"),
    Q + "plumb": dict(name="Brass plumb-bob", asset="key", variant="gold", desc="A brass plumb-bob on a knotted cord, from the coastguard's lead-line."),
    Q + "candle": dict(name="Candle", asset="candle", variant="white", desc="A tall white candle for the bedside table."),
    Q + "keepsake": dict(name="Typewriter ribbon and shorthand book", asset="book", variant="diary", desc="The Remington's ribbon wound round Mina's Whitby notebook: the two instruments of her gift."),
}

# ================================================================================================ JOURNAL
JOURNAL = {
    Q + "j_tomb1": dict(title="Stone of Hannah Brough", source=M, text="'Hannah Brough, born 1785, died 1830, aged 43.' A faithful wife and a good neighbour. I copy the figures to be added up in a quiet moment."),
    Q + "j_tomb2": dict(title="Stone of John Anson", source=M, text="'John Anson, master mariner, born 1765, died 1795, aged 30.' Lost off the Scar and not found. The figures are neat and the sum is good."),
    Q + "j_tomb3": dict(title="Stone of Mary Dale", source=M, text="'Mary Dale, spinster, born 1790, died 1810, aged 20.' She died as she lived: quietly. The lettering is clean and the sum exactly right."),
    Q + "j_morning": dict(title="Exeter. A missing Tennyson", source=M, text="Miss Hallam's speech-day prize, the Tennyson in green morocco, has vanished from a locked cupboard. I am to look into it, as I seem to be the only member of staff who reads the small print. I am rather pleased."),
    Q + "j_task": dict(title="Miss Hallam's bargain", source=M, text="Miss Hallam will give me the key to the typewriting room if I find the book. I have wanted that key since Christmas. Cupboard, blotter, girls, she said, in that order. I shall keep the order but not, I think, the temper."),
    Q + "j_edith": dict(title="Edith's gossip", source=M, text="Dora Pike dusts the staff-room on Wednesdays for a penny. Her mother is ill in Heavitree, and she sews at night to pay the doctor. I do not like where this points; I like it less that it points so clearly."),
    Q + "j_blotter": dict(title="The blotter in the mirror", source=M, text="Held to the glass, Miss Hallam's blotter gives a backward letter in a girl's round hand, with a looped capital D: 'Dearest Mama, I have it safe...' So the thief is a daughter, not a magpie. That is a different crime and wants a different kindness."),
    Q + "j_cupboard": dict(title="The unforced lock", source=M, text="No scratch on the lock, no mark on the hasp. Only a tiny shining thumb-print of red ink on the brass. Whoever took the book had the staff-room key and had been writing with the staff's red ink. Not a burglar: a borrower."),
    Q + "j_redink": dict(title="Red ink, a quarter lower", source=M, text="The red ink is a quarter lower than last week. Red ink is for the staff alone, so someone has been where she should not, and for longer than a moment."),
    Q + "j_cuff": dict(title="Dora's cuff", source=M, text="Dora Pike's hands are clean, but her sleeve-cuff carries a red thumb-mark the exact colour of the staff ink. She keeps turning it inward. I like her, and I wish I did not know what I now know."),
    Q + "j_book_found": dict(title="The Tennyson returned", source=M, text="Dora confessed: she wanted to read the Lady of Shalott to her mother. The book is back in my hands, undamaged. What we do with a child who steals for love is not in any rule-book, and I am glad of it."),
    Q + "j_key": dict(title="The key to the typewriting room", source=M, text="Miss Hallam asked no questions and gave me the key. A small iron thing; I wear it on a ribbon at my throat like a cross. Tomorrow I shall learn to make a machine speak."),
    Q + "j_dictation": dict(title="The dictation sheet", source=M, text="From Mr. Hawkins's office: the house at Purfleet, called Carfax, with its chapel and twenty acres, secured for the Count, deeds to follow by the post of the ninth instant. A dull letter; I copy it as I would any other, with all my care."),
    Q + "j_typed": dict(title="The Remington speaks", source=M, text="I freed the type-bars, oiled the pivots and wound on a new ribbon. Eleven lines, no errors. If Jonathan's firm ever wants a typist, here is one who has never been told she could not."),
    Q + "j_reply": dict(title="Mr. Hawkins replies", source=M, text="A clerk writes for Mr. Hawkins: a registered letter for me, in Jonathan's hand, was posted at Exeter and has been lost on the Bristol line. So Jonathan wrote. Whatever else the silence means, he wrote."),
    Q + "j_bradshaw": dict(title="Bradshaw, the Bristol line", source=M, text="The morning trains: 10.20, stopping at Tiverton, Taunton at 11.30; 10.50, express, Taunton at 11.40; 11.15, stopping at Tiverton, Taunton at 12.05. I could set a clock by it. I would rather set a man free."),
    Q + "j_bradshaw2": dict(title="Where the bag went", source=M, text="Mr. Pomfret: the bag went on the first train after the half-past-ten sorting, and the guard saw it on the van floor as the train roared through Tiverton. So not a stopper, and not before half-past ten."),
    Q + "j_wire": dict(title="The ten-fifty", source=M, text="After the sorting, clean through Tiverton: the 10.50 express. Mr. Pomfret has had Hobbs wire Taunton. Nobody has ever called me a detective, but I do believe I solved a thing with Bradshaw today."),
    Q + "j_letter_found": dict(title="Jonathan's letter, at last", source=M, text="Under a van seat at Taunton for twelve days. Soft at the corners, smelling of coal and tobacco, and the dearest paper I own. Bistritz, the Golden Krone, the little cross the landlady pressed on him. He wrote. He did write."),
    Q + "j_letter": dict(title="'Wait for me'", source=M, text="'I wish you were beside me, with your shorthand and your timetables. Wait for me, and do not be anxious.' I read it twice aloud to Lucy and a third time alone. I shall wait. It is what I am best at, though I wish it were not."),
    Q + "j_firstdream": dict(title="The dream I told Lucy", source=M, text="I told Lucy of the dream: water lapping, wood creaking, and a call I cannot catch. I thought she would laugh; she did not. It is odd how heavy a thing becomes once it is said aloud."),
    Q + "j_confide": dict(title="A night of whispers", source=M, text="We lay awake until the rooks began, and Lucy told me of three suitors and I told her of one absent man. She says I shall come to Whitby, and that the sea air will cure my dreams. I am less sure that I want them cured."),
    Q + "j_whitby": dict(title="Whitby", source=M, text="Whitby, on the West Cliff. The harbour, the Abbey, the church on its hill, and Lucy at the window counting boats. I took one look at the sea and felt at once that it knew my name."),
    Q + "j_swales": dict(title="Mr. Swales and the stones", source=M, text="Old Mr. Swales swears that every stone in this churchyard lies and that one of three cannot count. I am to find it. He told me this with the cheerful malice of a man who has been telling it for fifty years."),
    Q + "j_almanac": dict(title="The sea keeps a calendar", source=M, text="Mr. Swales gave me his almanac: tides run later by fifty minutes each day. The stone that could not count was Hannah Brough's: forty-five by the calendar, and forty-three on the stone. I shall remember that when anyone tells me a sum is no matter."),
    Q + "j_tide": dict(title="The coastguard's tide-table", source=M, text="The table gives only Monday: high water 4.10 in the morning and 4.35 in the afternoon. Somebody has pencilled 'Wednesday?' in the margin and given up. I would not mind helping."),
    Q + "j_plumb": dict(title="A plumb-bob", source=M, text="The coastguard gave me a brass plumb on a cord: 'A pendulum, miss; hang it in a room and it will tell you what the room is thinking.' I have thought of something else to do with it, and I am a little ashamed."),
    Q + "j_bats": dict(title="Bats at the Abbey", source=M, text="Two bats at dusk, rather too close to my hair. I took the umbrella to them like a sensible woman, and they went. I do not think they were bats only. I do not know why I think so."),
    Q + "j_scare": dict(title="A small fright", source=M, text="The ninth stair complained behind me, and when I turned the curtain was moving, though the window was shut. Lucy slept through it. I told myself it was the draught. I lit the candle all the same."),
    Q + "j_window": dict(title="A damp hand on the sill", source=M, text="On the sill, a damp mark the shape of a small hand, drying as I watched. The sea air, the damp, a cat. I have a great many reasonable explanations and not one I would put my name to."),
    Q + "j_dreamorder": dict(title="Water, wood, swing", source=M, text="From my dream notes: it begins with the water, lapping near; then the wood, a creak; then the dark, a single point turning, and I forget my name. Water, wood, swing. Always in that order, before I wake."),
    Q + "j_trance": dict(title="The first deliberate trance", source=M, text="I sat in the rocking-chair, listened to the water in the basin, rocked until the boards creaked, and watched the plumb turn. It worked. I do not know whether to be proud or afraid, and I suspect the two are the same."),
    Q + "j_hold1": dict(title="The lapping", source=M, text="In the dark hold, a barrel drips. The water is near and slow and the sound comes up through the wood into my wrist. Water first, always."),
    Q + "j_hold2": dict(title="The creak", source=M, text="The great timber groans as the hull settles. Wood is the second sound, patient and old. I can tell it now from my own heartbeat."),
    Q + "j_end": dict(title="The thread", source=M, text="I woke with a candle-stub and a still plumb and a fine cord between my fingers that was not there. Somewhere, a man is breathing in the dark. I shall tell no one yet. But I know that I can follow the thread when I must."),
}

# ================================================================================================ SEED VARIATION
PALETTES = {
    Q + "schoolroom": [dict(wall="plaster", floor="planks", wood="pale", cloth="green"),
                       dict(wall="plaster_dirty", floor="planks", wood="oak", cloth="blue")],
    Q + "typing_room": [dict(wall="plaster_dirty", floor="planks", wood="ebony", cloth="green"),
                        dict(wall="stone_grey", floor="planks", wood="dark", cloth="red")],
    Q + "exeter_rooms": [dict(wall="plaster", floor="planks", wood="oak", cloth="red"),
                         dict(wall="plaster", floor="planks", wood="dark", cloth="blue")],
    Q + "whitby_rooms": [dict(wall="plaster", floor="planks", wood="dark", cloth="blue"),
                         dict(wall="plaster", floor="planks", wood="pale", cloth="green")],
    Q + "whitby_night": [dict(wall="plaster", floor="planks", wood="pale", cloth="blue"),
                         dict(wall="plaster_dirty", floor="planks", wood="oak", cloth="green")],
    Q + "coastguard": [dict(wall="plaster_dirty", floor="planks", wood="dark", cloth="red"),
                       dict(wall="stone_grey", floor="planks", wood="oak", cloth="blue")],
    Q + "east_cliff": [dict(floor="grass"), dict(floor="dirt")],
    Q + "station": [dict(floor="cobble"), dict(floor="dirt")],
}

PLACEMENTS = {
    Q + "ribbon": [
        dict(prop=Q + "t_cupboard", text="At the back of the stationery cupboard, in a tin that says 'Biscuits', a fresh black ribbon in its paper.", hint="One tin in the cupboard is far too clean to hold biscuits."),
        dict(prop=Q + "t_shelf", text="Behind Taylor's primer, a new typewriter ribbon in its wrapper.", hint="One primer stands proud of the row, as if something is behind it."),
        dict(prop=Q + "t_basket", text="Under a drift of spoiled pages, a spare ribbon, quite good, and cast away by a girl who knew no better.", hint="The basket rustles in a way that suggests it is hiding something."),
    ],
    Q + "candle": [
        dict(prop=Q + "n_mantel", text="Behind the ship in the bottle on the mantel, a tall white candle.", hint="The ship in the bottle sits oddly on the mantel."),
        dict(prop=Q + "n_chest", text="Wrapped in a sheet at the top of the linen chest, a tall white candle.", hint="The linen chest smells of wax as well as lavender."),
        dict(prop=Q + "n_dresser", text="In the dresser's top drawer, among the hair-pins, a tall white candle.", hint="One drawer of the dresser sticks as if something rolls inside."),
    ],
}

GATES = {
    Q + "w_stairs": [
        dict(cond=f"has:{Q}plumb", fail="It is still day, and I have one thing to do before I go up: I have something in mind to hang by a cord.", needs=Q + "plumb"),
    ],
}

# ================================================================================================ COMBAT (optional)
ENCOUNTERS_EXTRA = {
    Q + "dusk_bats": {"name": "Bats at the Abbey", "time": "dusk", "enemies": ["bat", "bat"], "flee_ok": True,
                      "intro": "Two bats wheel over the tombs and drop toward my hair. I have an umbrella, and rather more nerve than I knew.",
                      "win": "The bats fall back and are gone into the Abbey ruins.", "location": Q + "east_cliff"},
}
ENCOUNTER_HOOKS = {
    Q + "dusk_bats": dict(
        on_win=[dict(set=Q + "bats_driven"), dict(journal=Q + "j_bats"), dict(give="brandy")],
        on_lose=[dict(say="The bats flurry about my head, but they do me no harm; they are gone before I have found my umbrella."), dict(set=Q + "bats_driven")],
        on_flee=[dict(say="I walk very steadily away from the tombs. I do not run. I want that noted.")],
    ),
}

# ================================================================================================ LOOKS
VARIANTS = {
    "human_peasant_m": {
        Q + "swales_v": human_colors(skin=T("skin", "#cfa383"), hair=T("hair", "#e0e0e0"), top=T("wool", "#3a4a5a"), bottom=T("wool", "#2a2e36")),
        Q + "pomfret_v": human_colors(skin=T("skin", "#e0b896"), hair=T("hair", "#4a4a4a"), top=T("wool", "#1a2338"), bottom=T("wool", "#1a2338")),
        Q + "coast_v": human_colors(skin=T("skin", "#d9b08c"), hair=T("hair", "#3a3a3a"), top=T("wool", "#1f2c44"), bottom=T("wool", "#1f2530")),
    },
    "human_peasant_f": {
        Q + "westenra_v": human_colors(skin=T("skin", "#e8c3a0"), hair=T("hair", "#c8c8c8"), top=T("wool", "#6a6a74"), bottom=T("wool", "#4a4a54")),
    },
}
