"""ACT II - Whitby (novel chapters 5-8).  Protagonist: Mina Murray (short cutaway: Dr. Seward at the asylum)."""
from dsl import *


def N(speaker, text, **kw):
    return dict(speaker=speaker, text=text, **kw)


def C(text, next=None, **kw):
    d = dict(text=text)
    if next:
        d["next"] = next
    d.update(kw)
    return d


def IF(cond, **kw):
    return {"if": cond, **kw}


def D(start, **nodes):
    return dict(start=start, nodes=nodes)


ACT = dict(
    id=2, title="Whitby",
    start=dict(location="a2_whitby_lodging", protagonist="mina", party=["mina"], items={}, flags=[]),
    exit_to="a3_asylum_study",
)

LOCATIONS = [
    dict(id="a2_whitby_lodging", name="The Crescent, Whitby", desc="Our lodgings on the West Cliff: a sitting-room with a view of the sea, and Lucy's mother fussing over her tea-things.", date="24 July"),
    dict(id="a2_seward_study", name="Dr. Seward's study, the asylum", desc="A cutaway to Dr. Seward's study at the asylum, where the phonograph waits and Renfield is always near.", date="25 April"),
    dict(id="a2_east_cliff", name="East Cliff churchyard", desc="The churchyard above the harbour. From the seat on the old tomb one sees the whole of Whitby, the Abbey and the grey sea.", date="Whitby"),
    dict(id="a2_harbour", name="Tate Hill Pier and the harbour", desc="Fishing boats, nets and the smell of tar. The coastguard hut stands under the cliff, its door padlocked.", date="Whitby"),
    dict(id="a2_coastguard_hut", name="The coastguard hut", desc="A snug hut of stove, charts and ropes, smelling of tobacco and paraffin.", date="Whitby"),
    dict(id="a2_abbey_ruins", name="Whitby Abbey", desc="Broken arches against the sky. The sexton says the White Lady shows herself in the great window at sunset.", date="Whitby"),
    dict(id="a2_cliff_storm", name="East Cliff, in the storm", desc="The whole town stands on the cliff in the howling dark, watching the sea come in.", date="6 August, midnight"),
    dict(id="a2_demeter_deck", name="Deck of the Demeter", desc="The Russian schooner lies broken on the sand, her sails in rags, her helm still manned by a dead man.", date="7 August"),
    dict(id="a2_demeter_cabin", name="The Demeter's cabin and hold", desc="Below decks it is dark and stinks of damp earth. Great boxes fill the hold.", date="7 August"),
    dict(id="a2_lucy_bedroom", name="Lucy's bedroom", desc="Two beds side by side, the window looking out on the sea. Lucy sleeps with a faint smile.", date="10 August"),
    dict(id="a2_night_steps", name="The steps and lanes, by night", desc="The fog lamps burn dull orange. Somewhere above, the clock of St. Mary's strikes one.", date="11 August, night"),
    dict(id="a2_east_cliff_night", name="East Cliff, by moonlight", desc="Moonlight on the tombs. On the seat, something white, and something black bending over it.", date="11 August, night"),
]

# --------------------------------------------------------------------------------------------------------------------
# location data
# --------------------------------------------------------------------------------------------------------------------
LOC_DATA = {}

LOC_DATA["a2_whitby_lodging"] = dict(
    cells=[3, 2], wall="plaster", floor="planks", interior=True,
    ambient=AMBIENT["warm_day_interior"], camera=cam([3, 2]), lights=lights_warm([3, 2], energy=2.8),
    walls=dict(north=["wall_4", "wall_4", "wall_window_4"], west=["wall_door_4", "wall_window_4"], east=["wall_4", "wall_door_4"]),
    spawn=[3.5, 2.0], spawns={"a2_east_cliff": [4.6, 2.0], "a2_lucy_bedroom": [-4.4, -2.0], "a2_seward_study": [0, 1.5], "a2_night_steps": [4.6, 2.0]},
    props=[
        prop("a2_l_fire", "fireplace", "plaster", 0, -3.4, name="Fireplace", radius=0.9,
             look="Cold in August, with a vase of sea-pinks in the grate. Mrs. Westenra says the chimney draws better empty."),
        prop("a2_l_baro", "mirror", "default", -4.0, -3.7, y=1.0, scale=0.6, name="Weather-glass", radius=0.4,
             talk="a2_barometer"),
        prop("a2_l_shelf", "bookshelf", "dark", 5.5, -2.0, rot=-90, name="Bookcase", radius=0.7,
             look="Guide-books, a Bible and three novels with their pages uncut. Lucy reads only the ends."),
        prop("a2_l_table", "table", "dark", -1.5, -0.8, name="Writing table", radius=0.9,
             look="My shorthand notebook, the blotter, and a place where I have written 'Jonathan' and nothing after it."),
        prop("a2_l_letter", "book", "diary", -1.5, -0.8, y=0.8, name="Lucy's letter", radius=0.2,
             look="Lucy's long letter, three pages crossed. I have read it twice and shall read it again.",
             take="a2_lucy_letter", take_text="I put Lucy's letter in my pocket. It is the only complete account of that wild afternoon."),
        prop("a2_l_notes", "book", "leather", -1.0, -0.8, y=0.8, name="Shorthand notebook", radius=0.2,
             look="My notebook of Whitby: tides, the price of tea, and the unanswered questions about Jonathan."),
        prop("a2_l_chair1", "chair", "blue", -1.5, 0.5, rot=180, name="Writing chair", radius=0.4, look="My own chair, with the cushion Lucy embroidered badly."),
        prop("a2_l_settee", "bench", "oak", 2.2, -1.8, name="Settee", radius=0.9, look="Lucy's favourite. She says the springs are exactly right for novel-reading."),
        prop("a2_l_rug", "rug", "cream", 0.5, 1.0, name=None, radius=0.1),
        prop("a2_l_basket", "chest", "pale", -5.0, 2.6, rot=90, scale=0.6, name="Sewing-basket", radius=0.5,
             look="Cottons, a thimble, a card of buttons and a paper of safety-pins, which Lucy borrows daily.",
             take="a2_pin", take_text="I take the largest safety-pin. One never knows.", give_once=True),
        prop("a2_l_sconce", "sconce", "default", -5.7, 0.0, y=1.5, rot=90, name=None, radius=0.1),
        prop("a2_l_sconce2", "sconce", "default", 5.7, 0.5, y=1.5, rot=-90, name=None, radius=0.1),
        prop("a2_l_flowers", "bottle", "green", 4.0, -3.0, y=0.9, name="Vase of sea-pinks", radius=0.2, look="Lucy gathers them on the cliff every morning."),
        # doors
        prop("a2_l_door_bed", "door", "pale", -5.8, -2.0, rot=90, name="Bedroom door", radius=0.6,
             look="The door to the room Lucy and I share.", go="a2_lucy_bedroom"),
        prop("a2_l_door_day", "door", "pale", 5.8, 2.0, rot=-90, name="Front door", radius=0.6, cond="!a2_night",
             look="The way down to the town and the East Cliff.", go="a2_east_cliff"),
        prop("a2_l_door_day2", "door", "pale", 5.8, 2.0, rot=-90, name="Front door", radius=0.6, cond="a2_lucy_home",
             look="The way down to the town and the East Cliff.", go="a2_east_cliff"),
        prop("a2_l_door_night", "door", "pale", 5.8, 2.0, rot=-90, name="Front door (ajar)", radius=0.6, cond="a2_night&!a2_lucy_home",
             look="Ajar, and the night air coming in. She has gone out into the fog.", go="a2_night_steps"),
        prop("a2_l_trunk", "chest", "dark", -3.0, -3.2, name="Travelling trunk", radius=0.6, talk="a2_depart"),
    ],
    npcs=[
        npc("a2_lucy_l", "human_lucy", "lucy", 2.8, 1.0, rot=-90, name="Lucy Westenra", cond="!a2_night",
            look="Lucy, pretty and fair, smiling over her tea. She has the colour of a girl who sleeps well.", talk="a2_lucy_talk"),
        npc("a2_lucy_l_b", "human_lucy", "lucy", 2.8, 1.0, rot=-90, name="Lucy Westenra", cond="a2_lucy_home",
            look="Lucy, pretty and fair, smiling over her tea. She has the colour of a girl who sleeps well.", talk="a2_lucy_talk"),
        npc("a2_mrs_w", "human_peasant_f", "a2_mrs_w", -3.5, 1.5, rot=90, name="Mrs. Westenra", cond="!a2_night",
            look="Lucy's mother, in grey silk and a lace cap, with a weak heart and a strong opinion on draughts.", talk="a2_westenra_talk"),
        npc("a2_mrs_w_b", "human_peasant_f", "a2_mrs_w", -3.5, 1.5, rot=90, name="Mrs. Westenra", cond="a2_lucy_home",
            look="Lucy's mother, in grey silk and a lace cap, with a weak heart and a strong opinion on draughts.", talk="a2_westenra_talk"),
        npc("a2_maid", "human_peasant_f", "village_woman", 3.6, -2.4, rot=0, name="Housemaid", cond="!a2_night",
            look="A plain, quick girl from the town. She knows everything the fishwives know.", talk="a2_maid_talk"),
        npc("a2_maid_b", "human_peasant_f", "village_woman", 3.6, -2.4, rot=0, name="Housemaid", cond="a2_lucy_home",
            look="A plain, quick girl from the town. She knows everything the fishwives know.", talk="a2_maid_talk"),
        npc("a2_postman", "human_peasant_m", "villager", 4.4, 0.4, rot=-90, name="Postman", cond="a2_lucy_home",
            look="A postman in a sea-damp coat, holding a foreign envelope with a convent seal.", talk="a2_postman_talk"),
    ],
    on_enter=[
        IF("a2_lucy_home", once=True, do=[dict(journal="a2_j_decline")]),
        dict(once=True, do=[dict(journal="a2_j_arrive")]),
    ],
)

LOC_DATA["a2_seward_study"] = dict(
    cells=[2, 2], wall="plaster_dirty", floor="planks", interior=True,
    ambient=AMBIENT["candle_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2]),
    walls=dict(north=["wall_4", "wall_window_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_4"]),
    spawn=[0, 2.0], spawns={"a2_whitby_lodging": [0, 2.0]},
    props=[
        prop("a2_s_desk", "table", "ebony", -1.0, -1.5, name="Seward's desk", radius=0.9,
             look="Papers in rows, a blotter, and the case-book of the asylum, open at a name I cannot read from here."),
        prop("a2_s_phono", "chest", "dark", -1.0, -1.5, y=0.8, scale=0.35, name="Phonograph", radius=0.4, talk="a2_phono"),
        prop("a2_s_casebook", "book", "red", -0.4, -1.5, y=0.8, name="Case-book", radius=0.2,
             look="'R. M. Renfield, aetat 59. Sanguine temperament; great physical strength; morbidly excitable; periods of gloom ending in some fixed idea.'"),
        prop("a2_s_shelf", "bookshelf", "ebony", -2.0, -3.4, name="Medical shelves", radius=0.8,
             look="Maudsley, Esquirol, Pinel, and a row of bottles with tight stoppers and tighter labels."),
        prop("a2_s_cabinet", "bottle", "amber", 3.2, -3.0, y=0.9, name="Medicine cabinet", radius=0.3,
             look="Chloral, morphia and brandy, all measured, all locked. The key is left in because Seward trusts himself.",
             take="chloral", take_text="Seward waves a hand: 'Take one dose, Miss Murray, in case Miss Lucy cannot sleep.' I bottle it carefully.", give_once=True),
        prop("a2_s_jars", "bottle", "glass", 1.5, -3.0, y=0.9, name="Jar of flies", radius=0.2,
             look="A sugar-smeared jar of flies, confiscated from the patient in Room 12. They buzz without hope."),
        prop("a2_s_chair", "chair", "green", 0.5, 0.5, rot=180, name="Visitor's chair", radius=0.4, look="Well sat in. Many a mad man has told his story here."),
        prop("a2_s_window", "sconce", "default", -3.7, 0.0, y=1.5, rot=90, name=None, radius=0.1),
        prop("a2_s_rug", "rug", "blue", 0, 1.0, name=None, radius=0.1),
        prop("a2_s_fire", "fireplace", "soot", 3.4, 0.0, rot=-90, name="Fireplace", radius=0.8, look="Banked low. The room smells of carbolic and cigar smoke."),
    ],
    npcs=[
        npc("a2_attendant", "human_peasant_m", "a2_attendant", -3.0, 1.5, rot=90, name="Attendant Hennessey",
            look="A large, kind man in a white coat who has been bitten twice and bears no grudge.", talk="a2_attendant_talk"),
        npc("a2_renfield", "human_renfield", "asylum", 2.5, 1.0, rot=-90, name="R. M. Renfield",
            look="A thin, pale man of nearly sixty, quite calm, with a little line of sugar on the table before him and an eye on the window.", talk="a2_renfield_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="a2_j_seward_intro")])],
)

LOC_DATA["a2_east_cliff"] = dict(
    cells=[4, 3], wall="stone_grey", floor="grass", interior=False,
    ambient=AMBIENT["day_exterior"], camera=cam([4, 3]), lights=lights_day(),
    scatter=dict(asset="rock", variant="mossy", count=12, seed=3, avoid=[[-8, -6, 8, 6]]),
    spawn=[6.4, 3.0], spawns={"a2_whitby_lodging": [6.4, 3.0], "a2_harbour": [-6.2, 3.4], "a2_abbey_ruins": [6.2, -0.5]},
    props=[
        prop("a2_c_tomb", "tomb", "stone_mossy", -1.0, -3.0, name=None, radius=0.9),
        prop("a2_c_seat", "bench", "oak", -1.0, -3.0, y=0.55, name="Lucy's seat", radius=0.9,
             look="A seat fixed on the flat tomb of the suicide's grave. Lucy and I come here every fine afternoon, and the sea breathes up at us."),
        prop("a2_c_stone_canon", "gravestone", "stone_grey", -5.2, -2.2, name="Stone of George Canon", radius=0.5,
             look="'HERE LYETH THE BODY OF GEORGE CANON, WHO DIED, IN HOPE OF A GLORIOUS RESURRECTION, ON JULY 29, 1873, FALLING FROM THE ROCKS AT KETTLENESS. THIS TOMB WAS ERECTED BY HIS SORROWING MOTHER TO HER DEARLY BELOVED SON. HE WAS THE ONLY SON OF HIS MOTHER, AND SHE WAS A WIDOW.' Lichen at the foot has been disturbed.",
             take="a2_hut_key", take_text="Pressed into the moss at the stone's foot, a small iron key on a loop of tarred twine. The coastguard's spare, if Mr. Swales is to be believed.", give_once=True),
        prop("a2_c_stone_wilson", "gravestone_point", "stone_mossy", -3.4, 0.2, name="Stone of Thomas Wilson", radius=0.5,
             look="'Sacred to the memory of Thomas Wilson, mariner, lost with all hands in the Providence, 1859. His wife and five children mourn.' Fresh flowers lie at the base."),
        prop("a2_c_stone_jonas", "gravestone", "stone_dark", -6.0, 1.4, name="Stone of Mary Jonas", radius=0.5,
             look="'Mary Jonas, widow, aged 91 years. She was beloved of many.' She had, the stone suggests, several sons."),
        prop("a2_c_stone_sailor", "gravestone_point", "stone_grey", 3.2, -0.8, name="Mariner's stone", radius=0.5,
             look="Worn smooth. A carved anchor and a ship. The inscription began 'In loving memory' and then lost patience."),
        prop("a2_c_cross", "grave_cross", "stone_grey", 5.0, -3.2, name="Stone cross", radius=0.4, look="A plain cross for a child. Someone has set a shell on it."),
        prop("a2_c_church", "tower", "stone_grey", 5.5, -6.8, scale=0.6, name="St. Mary's church", radius=1.2,
             look="Square, grey and enduring, with the hundred and ninety-nine steps going down beside it."),
        prop("a2_c_bench2", "bench", "dark", -4.4, 3.0, name="Weathered bench", radius=0.9, look="Mr. Swales's bench, black with sea-wet and tobacco."),
        prop("a2_c_fence1", "fence", "default", -4.0, 5.2, name=None, radius=0.3),
        prop("a2_c_fence2", "fence", "default", 0.0, 5.2, name=None, radius=0.3),
        prop("a2_c_fence3", "fence", "default", 4.0, 5.2, name=None, radius=0.3),
        prop("a2_c_lamp", "lantern", "default", 1.8, -4.6, name="Churchyard lamp", radius=0.3, look="Unlit by day. It has a lovely view and no flame."),
        prop("a2_c_steps", "stairs", "stone_grey", -6.8, 3.6, rot=90, name="Steps to Tate Hill Pier", radius=0.8,
             look="The steep way down to the harbour.", go="a2_harbour"),
        prop("a2_c_arch", "arch", "stone_grey", 7.0, -0.5, rot=-90, name="Path to the Abbey", radius=0.8,
             look="A grass path, and the broken Abbey beyond.", go="a2_abbey_ruins"),
        prop("a2_c_sign", "signpost", "dark", 6.4, 3.4, rot=-30, name="Path to the Crescent", radius=0.3,
             look="'West Cliff and the Crescent.' Under it, in pencil: 'Mind the steps.'", go="a2_whitby_lodging"),
    ],
    npcs=[
        npc("a2_swales", "human_peasant_m", "a2_swales", -4.4, 2.6, rot=0, name="Old Mr. Swales", cond="!a2_log_ordered",
            look="A very old man, weather-beaten like a sea-wall, leaning on a stick and clearly enjoying a young lady's company.", talk="a2_swales_talk"),
        npc("a2_swales_dead", "human_peasant_m", "a2_swales", -1.0, -2.0, rot=0, name="Mr. Swales", cond="a2_swales_dead",
            look="He lies on the seat, his neck broken, his face frozen in fear and horror. The coastguard says he fell. I do not think he fell.", radius=0.6),
        npc("a2_visitor", "human_peasant_f", "innkeeper_wife", 2.4, 3.0, rot=180, name="Visitor from Leeds",
            look="A stout lady in a bonnet, a guide-book in one hand and a parasol in the other, pleased with everything.", talk="a2_visitor_talk"),
    ],
    on_enter=[
        IF("a2_log_ordered", once=True, do=[dict(set="a2_swales_dead"), dict(journal="a2_j_swales_dead")]),
        dict(once=True, do=[dict(journal="a2_j_east_cliff")]),
    ],
)

LOC_DATA["a2_harbour"] = dict(
    cells=[4, 3], wall="plaster_dirty", floor="cobble", interior=False,
    ambient=AMBIENT["sea_fog"], camera=cam([4, 3]), lights=lights_day(2.8),
    walls=dict(north=["wall_4", "wall_door_4", "wall_4", "wall_4"]),
    scatter=dict(asset="rock", variant="dark", count=10, seed=7, avoid=[[-8, -6, 8, 6]]),
    spawn=[6.0, -2.4], spawns={"a2_east_cliff": [8.4, -1.0], "a2_coastguard_hut": [-2.0, -4.4], "a2_demeter_deck": [4.0, 1.0], "a2_cliff_storm": [0, 3.0]},
    props=[
        prop("a2_h_hut_door", "door", "oak", -2.0, -5.8, name="Coastguard hut", radius=0.6,
             look="A tarred door under a tarred lintel. A padlock that has seen more of the sea than of oil.",
             go="a2_coastguard_hut", go_cond="has:a2_hut_key",
             go_fail="Padlocked. The coastguard is out on the pier, and nobody else holds the key. There might be a spare hidden somewhere."),
        prop("a2_h_cliff1", "cliff_face", "dark", 12.6, -1.0, rot=-90, name="The East Cliff", radius=1.5, look="The cliff drops straight into the harbour here, black and dripping."),
        prop("a2_h_cliff2", "cliff_face", "dark", 12.6, -8.0, rot=-90, name="The East Cliff", radius=1.5, look="Gulls nest on every ledge."),
        prop("a2_h_cliff3", "cliff_face", "dark", 12.6, 6.0, rot=-90, name="The East Cliff", radius=1.5, look="The same wet black rock, down to the waterline."),
        prop("a2_h_stairs", "cliff_stairs", "stone_grey", 10.2, -1.0, rot=-90, name="Steps up to the East Cliff", radius=1.3,
             look="Hundreds of years of feet have worn the steps hollow. The iron rail is cold and wet.", go="a2_east_cliff"),
        prop("a2_h_stall", "table", "pale", -5.0, -2.0, name="Chandler's stall", radius=0.9,
             look="Twine, tar, tallow and lamp-glass, and a bunch of garlic hung up by the sailors for luck."),
        prop("a2_h_garlic", "garlic", "default", -5.0, -2.0, y=0.8, name="Garlic bulbs", radius=0.2,
             look="Sailors hang garlic to keep off fever and the evil eye.",
             take="garlic", take_text="The chandler waves me on: 'Take it, miss, it's no use to me. Lucy'd not like the smell.'", give_once=True),
        prop("a2_h_barrel1", "barrel", "dark", -6.6, 2.6, name="Herring barrel", radius=0.4, look="Salt and scales and the afternoon's catch."),
        prop("a2_h_barrel2", "barrel", "oak", -6.0, 3.6, name=None, radius=0.4),
        prop("a2_h_crate", "chest", "pale", -2.5, 3.5, scale=0.8, name="Fish crate", radius=0.5, look="Empty and smelling it."),
        prop("a2_h_lamp", "lantern", "default", -6.2, -4.8, name="Harbour lamp", radius=0.3, look="The lighthouse lanthorn keeps better time than the town clocks."),
        prop("a2_h_heap", "rock_big", "mossy", 6.5, 3.8, name="Sand and gravel heap", radius=1.0,
             look="Tate Hill Pier gathers sand and gravel at its foot. A ship driven here would stick fast."),
        prop("a2_h_fence1", "fence", "default", -3.0, 5.2, name=None, radius=0.3),
        prop("a2_h_fence2", "fence", "default", 0.0, 5.2, name=None, radius=0.3),
        prop("a2_h_fence3", "fence", "default", 3.0, 5.2, name=None, radius=0.3),
        prop("a2_h_pier", "pier", "dark", -12.4, 1.2, rot=0, name=None, radius=0.1, y=0.0),
        prop("a2_h_boat1", "boat", "tarred", -11.0, 4.6, rot=25, y=-0.62, name="Beached rowing boat", radius=0.7, look="Tarred planks and a pair of oars. The coastguard's, by the number on her bow."),
        prop("a2_h_boat2", "boat", "white", 10.4, -1.6, rot=-70, y=-0.62, name=None, radius=0.1),
        prop("a2_h_lamp2", "lamp_post", "default", 6.6, -5.2, name=None, radius=0.2),
        prop("a2_h_lamp3", "lamp_post", "default", -6.4, 4.6, name=None, radius=0.2),
        prop("a2_h_crates", "crate_stack", "oak", -3.4, -4.6, name="Net crates", radius=0.7, look="Cork floats, coils of net and a dead gull somebody swept in."),
        prop("a2_h_bollard1", "bollard", "default", -1.5, 5.0, name=None, radius=0.2),
        prop("a2_h_bollard2", "bollard", "default", 2.0, 5.0, name=None, radius=0.2),
        prop("a2_h_rope", "rope_coil", "default", 0.8, 4.4, name=None, radius=0.2),
        prop("a2_h_wreck", "a2_schooner", "weathered", 4.2, 1.6, rot=90, name="The Demeter", radius=2.0, cond="a2_storm_over",
             look="A schooner of Varna, aground on the sand with her sails in tatters. A cordon of ropes keeps the crowd back.",
             go="a2_demeter_deck", go_cond="a2_pass",
             go_fail="A constable bars the gangway: 'No one aboard till the Board of Trade man comes, miss. Someone must speak for you.'"),
    ],
    npcs=[
        npc("a2_chandler", "human_peasant_f", "innkeeper_wife", -5.0, -0.6, rot=180, name="Mrs. Pinder, chandler",
            look="A broad woman with arms like rope. She has sold twine to three generations of drowned men.", talk="a2_chandler_talk"),
        npc("a2_fisher", "human_peasant_m", "a2_fisher", -0.6, 2.4, rot=0, name="Old fisherman",
            look="Mending a net with fingers like knots of tarred rope. His eyes never leave the sky.", talk="a2_fisher_talk"),
        npc("a2_constable", "human_peasant_m", "a2_constable", 1.5, -0.8, rot=90, name="Constable", cond="a2_storm_over",
            look="Helmeted, stout, and fully aware of the importance of his rope.", talk="a2_constable_talk"),
        npc("a2_billington", "human_seward", "doctor", -1.2, -0.4, rot=-90, name="Mr. S. F. Billington", cond="a2_storm_over",
            look="A tidy, worried solicitor with a pencil behind his ear and fifty boxes he did not order on his conscience.", talk="a2_billington_talk"),
        npc("a2_dog", "wolf_big", "grey", 6.5, -1.5, rot=-90, name="Huge dog", cond="a2_storm_over", roam=True, radius=0.7,
            look="A great grey brute, cowering under the pier. It sprang from the ship and none can say whose it is.", fight="a2_dog_pier"),
    ],
    on_enter=[
        IF("a2_storm_over", once=True, do=[dict(journal="a2_j_wreck_morning")]),
        dict(once=True, do=[dict(journal="a2_j_harbour")]),
    ],
)

LOC_DATA["a2_coastguard_hut"] = dict(
    cells=[2, 2], wall="plaster_dirty", floor="planks", interior=True,
    ambient=AMBIENT["candle_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2]),
    walls=dict(north=["wall_door_4", "wall_window_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_4"]),
    spawn=[-2.0, -2.6], spawns={"a2_harbour": [-2.0, -2.6]},
    props=[
        prop("a2_t_door", "door", "dark", -2.0, -3.8, name="Hut door", radius=0.6, look="Back out to the harbour.", go="a2_harbour"),
        prop("a2_t_fire", "fireplace", "soot", -3.5, 0.0, rot=90, name="Stove", radius=0.8, look="A black stove with a kettle that never quite boils."),
        prop("a2_t_bunk", "bed_simple", "black", 2.4, -2.4, name="Bunk", radius=0.7, look="Blankets that smell of tobacco and wet dog. No dog."),
        prop("a2_t_desk", "table", "dark", 0.0, -0.4, name="Chart table and log desk", radius=0.9, talk="a2_log_desk"),
        prop("a2_t_knife", "key", "default", 0.4, 0.05, y=0.8, scale=2.5, name="Sailor's knife", radius=0.35,
             look="A good steel splicing knife with a horn handle, left on the desk.",
             take="knife", take_text="A knife is no weapon against what is coming, but it cuts rope and ash wood and I take it.", give_once=True),
        prop("a2_t_chair", "chair", "green", 0.0, 0.7, rot=180, name="Chair", radius=0.4, look="The coastguard's chair, worn to his shape."),
        prop("a2_t_board", "bookshelf", "dark", 0.0, -3.5, name="Notice-board and ledgers", radius=0.8, talk="a2_notice_read"),
        prop("a2_t_chest", "chest", "dark", -3.0, 2.6, rot=90, name="Tool-chest", radius=0.6,
             look="Marline-spikes, a sail-needle, a short iron crowbar for stubborn lids.",
             take="a2_crowbar", take_text="I take the crowbar. A lid that will not open will open to this.", give_once=True),
        prop("a2_t_lantern", "lantern", "default", 3.2, 2.6, name="Storm lantern", radius=0.3,
             look="A stout storm lantern, wick trimmed.", take="a2_lantern", take_text="I take the storm lantern. A hold is a dark place.", give_once=True),
        prop("a2_t_oil", "barrel", "dark", 3.4, 1.2, scale=0.7, name="Oil keg", radius=0.4,
             look="Paraffin, topped up that morning.", take="oil", take_text="I fill a flask from the keg.", give_once=True),
        prop("a2_t_water", "barrel", "pale", -3.4, -2.6, scale=0.7, name="Water butt", radius=0.4,
             look="Rain water, cold and clean.", take="water", take_text="I fill a little flask with clean water.", give_once=True),
        prop("a2_t_sconce", "sconce", "default", 3.7, -0.5, y=1.5, rot=-90, name=None, radius=0.1),
        prop("a2_t_rug", "rug", "red", 0.3, 1.2, name=None, radius=0.1),
    ],
    npcs=[
        npc("a2_coastguard", "human_peasant_m", "a2_coast", -0.6, 1.8, rot=180, name="Coastguard Officer Dunn",
            look="A square, patient man whose eyes are always on the weather even indoors.", talk="a2_coastguard_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="a2_j_hut")])],
)

LOC_DATA["a2_abbey_ruins"] = dict(
    cells=[4, 4], wall="stone_mossy", floor="grass", interior=False,
    ambient=AMBIENT["day_exterior"], camera=cam([4, 4]), lights=lights_day(),
    scatter=dict(asset="rock", variant="mossy", count=14, seed=21, avoid=[[-8, -8, 8, 8]]),
    scatter2=dict(asset="deadtree", variant="grey", count=5, seed=2, avoid=[[-8, -8, 8, 8]]),
    spawn=[6.0, 4.4], spawns={"a2_east_cliff": [6.0, 4.4]},
    props=[
        prop("a2_a_arch1", "arch", "stone_mossy", 0.0, -6.2, name="Great east window", radius=1.0,
             look="Where the White Lady shows herself at sunset, in the legend, in the same pose as a woman at a high window. The glass is gone, and the light is lovely."),
        prop("a2_a_arch2", "arch", "stone_mossy", -4.5, -4.0, rot=30, name="Broken arch", radius=0.9, look="Half an arch against the sky. The other half is the sea's now."),
        prop("a2_a_arch3", "arch", "stone_mossy", 4.5, -4.0, rot=-30, name=None, radius=0.9),
        prop("a2_a_col1", "column", "stone_mossy", -2.0, -3.0, name=None, radius=0.35),
        prop("a2_a_col2", "column", "stone_mossy", 2.0, -3.0, name=None, radius=0.35),
        prop("a2_a_col3", "column_short", "stone_mossy", -3.0, 1.0, name="Broken pillar", radius=0.3, look="Cut off at the knee by seven centuries."),
        prop("a2_a_col4", "column_short", "stone_mossy", 3.0, 0.5, name=None, radius=0.3),
        prop("a2_a_slab", "tomb", "stone_tomb", 0.0, 0.0, name="Founder's slab", radius=0.9,
             look="The slab of some forgotten abbot. A single line of Latin is left: 'Dominus custodiat introitum tuum.' May the Lord guard thy coming in."),
        prop("a2_a_rose", "pine_small", "green", -5.5, -1.0, scale=0.35, name="Wild-rose briar", radius=0.4,
             look="Pale wild roses growing out of the broken stones. The sexton says they bloom here in defiance of the wind.",
             take="wild_rose", take_text="I pick one sprig, careful of the thorns. Wild rose is a good flower for a grave.", give_once=True),
        prop("a2_a_bough", "deadtree", "grey", -6.0, 3.6, scale=0.4, name="Fallen ash bough", radius=0.5,
             look="A bough of ash, broken in some gale, clean and straight.",
             take="wood", take_text="I break off a straight piece. Ash is good, hard wood.", give_once=True),
        prop("a2_a_font", "barrel", "pale", 5.0, -0.5, scale=0.6, name="Rain-filled font", radius=0.4,
             look="A hollow stone full of rain, collected for nobody.", take="water", take_text="I fill my flask. Rain-water from the Abbey is as pure as any.", give_once=True),
        prop("a2_a_stone", "gravestone_point", "stone_mossy", 2.0, 4.2, name="Mossy stone", radius=0.4, look="No name left. Lucy says its owner dislikes visitors."),
        prop("a2_a_steps", "stairs", "stone_grey", 6.8, 5.0, rot=-90, name="Path to the churchyard", radius=0.8, look="The way back up to the churchyard.", go="a2_east_cliff"),
    ],
    npcs=[
        npc("a2_sexton", "human_peasant_m", "villager", 3.8, 2.2, rot=180, name="Sexton",
            look="An elderly man with a spade, who talks to the stones as if they were shy parishioners.", talk="a2_sexton_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="a2_j_abbey")])],
)

LOC_DATA["a2_cliff_storm"] = dict(
    cells=[4, 3], wall="stone_dark", floor="grass", interior=False, night=True,
    ambient=AMBIENT["storm_exterior"], camera=cam([4, 3]), lights=lights_moon(2.2), moon=dict(pos=[-10, 14, -22]),
    scatter=dict(asset="rock", variant="dark", count=12, seed=5, avoid=[[-8, -6, 8, 6]]),
    spawn=[0, 4.2], spawns={},
    props=[
        prop("a2_st_rail", "fence", "default", 0.0, 4.4, name="Cliff-edge railing", radius=0.8, talk="a2_storm_watch"),
        prop("a2_st_rail2", "fence", "default", -3.2, 4.4, name=None, radius=0.3),
        prop("a2_st_rail3", "fence", "default", 3.2, 4.4, name=None, radius=0.3),
        prop("a2_st_light", "lantern", "default", 6.0, -1.0, scale=2.0, name="The new searchlight", radius=0.6,
             look="The new searchlight on the summit of the East Cliff, untried until tonight. It sweeps the sea like a white finger."),
        prop("a2_st_seat", "bench", "oak", -1.0, -3.0, y=0.55, name="Lucy's seat", radius=0.9, look="Wet, empty and humming in the wind."),
        prop("a2_st_tomb", "tomb", "stone_mossy", -1.0, -3.0, name=None, radius=0.9),
        prop("a2_st_stone1", "gravestone", "stone_dark", -5.2, -2.2, name=None, radius=0.5),
        prop("a2_st_stone2", "gravestone_point", "stone_mossy", -3.4, 0.2, name=None, radius=0.5),
        prop("a2_st_stone3", "gravestone", "stone_grey", 3.2, -0.8, name=None, radius=0.5),
        prop("a2_st_cross", "grave_cross", "stone_grey", 5.0, -3.2, name=None, radius=0.4),
        prop("a2_st_lamp", "lantern", "default", -6.0, 3.0, name="Swinging lamp", radius=0.3, look="Swinging so wildly it throws two shadows at once."),
        prop("a2_st_church", "tower", "stone_grey", 5.5, -6.8, scale=0.6, name=None, radius=1.2),
    ],
    npcs=[
        npc("a2_st_officer", "human_peasant_m", "a2_coast", 5.0, 0.8, rot=-90, name="Coastguard officer",
            look="Shouting orders into the wind that the wind sends back unfinished.", talk="a2_officer_talk"),
        npc("a2_st_swales", "human_peasant_m", "a2_swales", -5.0, 1.0, rot=90, name="Mr. Swales",
            look="Soaked and delighted. He has predicted this and is not displeased to be right.", talk="a2_swales_storm"),
        npc("a2_st_crowd1", "human_peasant_f", "village_woman", -2.0, 2.5, rot=180, name="Fishwife",
            look="A fishwife in a shawl, knuckles white on the railing.", talk="a2_crowd_talk"),
        npc("a2_st_crowd2", "human_peasant_m", "villager", 1.8, 2.2, rot=180, name="Boatman",
            look="A boatman, praying aloud and quite without shame.", talk="a2_crowd_talk"),
        npc("a2_st_crowd3", "human_peasant_f", "innkeeper_wife", -6.2, -2.5, rot=90, name="Landlady",
            look="A landlady in a nightcap and her husband's coat.", talk="a2_crowd_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="a2_j_storm_rises")])],
)

LOC_DATA["a2_demeter_deck"] = dict(
    cells=[3, 2], wall="planks", floor="planks", interior=False,
    ambient=AMBIENT["sea_fog"], camera=cam([3, 2]), lights=lights_day(2.6),
    walls=dict(east=["wall_4", "wall_door_4"]),
    spawn=[-4.6, 2.0], spawns={"a2_harbour": [-4.6, 2.0], "a2_demeter_cabin": [4.6, 2.0]},
    props=[
        prop("a2_d_mast1", "column", "planks", -2.5, -1.0, name="Foremast", radius=0.3, look="The mast is intact, but its canvas has been ripped into long grey ribbons."),
        prop("a2_d_mast2", "column", "planks", 2.5, -2.0, name=None, radius=0.3),
        prop("a2_d_wheel", "a2_wheel", "oak", 0.0, 0.5, name="The ship's wheel", radius=0.6,
             look="The helm. Cords bind the spokes. Whoever stood here meant to keep this course whatever came for him."),
        prop("a2_d_locker", "chest", "dark", -4.0, -2.4, name="Ship's locker", radius=0.6,
             look="Mildewed sailcloth and rope-ends. The lock has been burst.",
             take="cloth", take_text="Clean canvas, torn from the spare sail. Good for bandages or wicks.", give_once=True),
        prop("a2_d_spike", "stake", "default", -3.6, 0.4, name="Handspike", radius=0.3,
             look="A handspike of ash, for keeping men in order, which the mate swore would suffice. The crew thought otherwise.",
             take="wood", take_text="I take the handspike. A straight length of ash is worth more than its wooden weight.", give_once=True),
        prop("a2_d_bell", "lantern", "default", 3.6, 0.4, name="Ship's lantern", radius=0.3, look="Smashed. The glass lies outward as though something inside wanted out."),
        prop("a2_d_fence1", "fence", "default", -2.0, -3.1, name=None, radius=0.3),
        prop("a2_d_fence2", "fence", "default", 1.0, -3.1, name=None, radius=0.3),
        prop("a2_d_fence3", "fence", "default", 4.0, -3.1, name=None, radius=0.3),
        prop("a2_d_barrel", "barrel", "dark", 4.0, -1.0, scale=0.8, name="Tar barrel", radius=0.4, look="Pitch. The deck-house door is bolted with it."),
        prop("a2_d_gang", "stairs", "planks", -5.2, 2.0, rot=90, name="Gangway", radius=0.8, look="Back to the pier.", go="a2_harbour"),
        prop("a2_d_cabin_door", "door", "dark", 5.8, 2.0, rot=-90, name="Deck-house door", radius=0.6,
             look="The way below. A padlock holds it, rusty and obstinate.",
             go="a2_demeter_cabin", go_cond="has:a2_cabin_key", go_fail="Locked. The captain must have kept the key by him."),
    ],
    npcs=[
        npc("a2_captain", "human_peasant_m", "a2_captain", 0.0, -0.5, rot=0, name="The dead captain",
            look="Lashed to the helm, his hands bound over a crucifix and a string of beads, his head fallen forward. Two days dead, they say, and no man in the crowd would touch him.",
            radius=0.6,
            use_item={"knife": [
                dict(say="The knots are tied tightly, fastened with his teeth. I cut the cords and lay him down with the greatest reverence I can find. A bottle is in his pocket, and I take it, and the cabin key with it."),
                dict(give="a2_log_p4"), dict(give="a2_cabin_key"), dict(give="rope"), dict(give="crucifix"), dict(give="a2_rosary"),
                dict(set="a2_captain_freed"), dict(journal="a2_j_captain"),
            ]}, use_fail="I need something sharp to cut the cords without tearing him."),
    ],
    on_enter=[dict(once=True, do=[dict(journal="a2_j_wreck")])],
)

LOC_DATA["a2_demeter_cabin"] = dict(
    cells=[3, 2], wall="planks", floor="planks", interior=True,
    ambient=AMBIENT["cold_interior"], camera=cam([3, 2]), lights=lights_warm([3, 2], n=2, energy=1.8),
    walls=dict(north=["wall_4", "wall_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[4.6, -2.0], spawns={"a2_demeter_deck": [4.6, -2.0]},
    props=[
        prop("a2_m_door", "door", "dark", 5.8, -2.0, rot=-90, name="Cabin door", radius=0.6, look="Back up to the deck and the grey light.", go="a2_demeter_deck"),
        prop("a2_m_bunk", "bed_simple", "black", -4.5, -2.5, name="Captain's bunk", radius=0.8,
             look="A straw tick, a Russian Bible and a crucifix-sized empty nail. Under the tick, damp pages.",
             take="a2_log_p2", take_text="Under the straw tick, a damp roll of paper in a seaman's hand: the second leaf of the log.", give_once=True),
        prop("a2_m_chart", "table", "dark", -0.5, -1.5, name="Chart table", radius=0.9,
             look="Charts of the Black Sea and the Channel, with a course pencilled to Gibraltar and a cross where nothing should have been.",
             take="a2_log_p3", take_text="Rolled inside the chart, a third leaf of the log, smeared with something rust-coloured.", give_once=True),
        prop("a2_m_seachest", "chest", "ebony", 2.8, -2.8, name="Captain's sea-chest", radius=0.6,
             look="Oilskins, a pipe and a ledger. The lid has been forced.",
             take="a2_log_p1", take_text="Wrapped in oilskin at the bottom: the first leaf of the log, headed Varna.", give_once=True),
        prop("a2_m_box1", "chest", "oak", -3.5, 1.5, scale=1.6, name="Box of earth", radius=0.9,
             look="A great box, sealed with nails. Stencilled: 'Clay. For Mr. S. F. Billington, 7 The Crescent, Whitby.' It stinks of old earth, and something else."),
        prop("a2_m_box2", "chest", "oak", 0.5, 2.0, scale=1.6, name="Opened box", radius=0.9,
             look="The lid is off. Earth, black and dry, fills it. In the earth, a hollow the shape of a man's back.",
             take="a2_bill", take_text="Pinned under the lid, the consignment note in two languages: fifty boxes of earth, for Billington, by Hawkins's agents.", give_once=True),
        prop("a2_m_box3", "chest", "oak", 3.5, 1.5, scale=1.6, name="Another box", radius=0.9, look="Sealed. The nails are bent outward. It has been opened and closed again from the inside."),
        prop("a2_m_toolchest", "chest", "pale", 4.5, -0.3, scale=0.8, name="Mate's tool-chest", radius=0.5,
             look="Hammer, chisel, a screwdriver. The mate used it only once.",
             take="hammer", take_text="A heavy hammer. If I ever need to drive in a stake...", give_once=True),
        prop("a2_m_sack", "rug", "black", -1.5, 0.2, name="Sail-bag", radius=0.3,
             look="Canvas bag stuffed with old sailcloth and twine.", take="cloth", take_text="A clean length of canvas from the sail-bag.", give_once=True),
        prop("a2_m_lamp", "lantern", "default", -5.0, 0.5, name="Swinging lamp", radius=0.3, look="Out of oil. The wick is black."),
        prop("a2_m_barrel", "barrel", "dark", -5.0, 2.8, name=None, radius=0.4),
    ],
    npcs=[],
    on_enter=[dict(once=True, do=[dict(journal="a2_j_boxes")])],
)

LOC_DATA["a2_lucy_bedroom"] = dict(
    cells=[2, 2], wall="plaster", floor="planks", interior=True,
    ambient=AMBIENT["candle_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2], n=2, energy=1.8),
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[3.0, -2.0], spawns={"a2_whitby_lodging": [3.0, -2.0]},
    props=[
        prop("a2_b_bed_lucy", "bed", "blue", -2.5, -2.2, name="Lucy's bed", radius=0.9, look="A four-poster with Lucy's nightgown thrown across the foot."),
        prop("a2_b_bed_mina", "bed_simple", "green", 1.0, -2.2, name="My bed", radius=0.9, talk="a2_bed_dialogue"),
        prop("a2_b_window", "fence", "default", 2.0, -3.5, y=1.0, scale=0.6, name="Window latch", radius=0.1,
             look="The sash is open to the sea air; Lucy likes it so.",
             set="a2_window_fastened", set_text="I draw the sash down and shoot the bolt. The sea will have to speak to Lucy through glass."),
        prop("a2_b_wardrobe", "bookshelf", "dark", -3.4, 0.6, rot=90, name="Wardrobe", radius=0.8, look="Dresses, hats and a very large muff."),
        prop("a2_b_chair", "chair", "red", 2.8, 1.5, rot=-90, name="Chair", radius=0.4, look="A chair with a shawl thrown over its back."),
        prop("a2_b_shawl", "rug", "cream", 2.8, 1.5, y=0.5, scale=0.3, name="Warm shawl", radius=0.3, look="A thick white shawl, the warmest we own.",
             take="a2_shawl", take_text="I lay the shawl ready by my pillow. If the worst came, she should not be cold.", give_once=True),
        prop("a2_b_dresser", "table", "pale", 0.0, 2.8, name="Dressing-table", radius=0.8, look="Brushes, a silver mirror and Lucy's whole hair-ribbon collection."),
        prop("a2_b_brandy", "bottle", "amber", 0.0, 2.8, y=0.8, name="Brandy flask", radius=0.2, look="A flask of brandy that Mrs. Westenra says is only for emergencies.",
             take="brandy", take_text="I take the flask. Emergencies, as Mrs. Westenra says.", give_once=True),
        prop("a2_b_candle", "candle", "white", -1.0, 2.8, y=0.8, name=None, radius=0.2),
        prop("a2_b_rug", "rug", "cream", 0.0, 0.2, name=None, radius=0.1),
        prop("a2_b_door", "door", "pale", 3.8, -2.0, rot=-90, name="Door", radius=0.6, cond="!a2_lucy_gone",
             look="The door to the landing, with a good lock and, as yet, no key.", go="a2_whitby_lodging",
             use_item={"a2_lucy_door_key": [dict(say="I turn the key. The bolt shoots home with a satisfying noise."), dict(set="a2_door_locked")]},
             use_fail="I have nothing to lock it with."),
        prop("a2_b_door2", "door", "pale", 3.8, -2.0, rot=-90, name="Door (locked)", radius=0.6, cond="a2_lucy_gone",
             look="The door is still locked from the inside. How did she get out?", go="a2_whitby_lodging",
             go_cond="has:a2_shawl&has:a2_pin&has:a2_lucy_door_key",
             go_fail="I cannot leave without the key, and a warm shawl and a pin to fasten it. Lucy will be cold; the night is wet."),
    ],
    npcs=[
        npc("a2_b_lucy", "human_lucy", "nightgown", -2.5, -2.2, rot=0, name="Lucy (asleep)", cond="!a2_lucy_gone",
            look="Lucy sleeps with one hand under her cheek and the sea-wind stirring her hair.", talk="a2_lucy_asleep_talk", radius=0.5),
    ],
)

LOC_DATA["a2_night_steps"] = dict(
    cells=[3, 3], wall="stone_dark", floor="cobble", interior=False, night=True,
    ambient=AMBIENT["night_exterior"], camera=cam([3, 3]), lights=lights_moon(2.2), moon=dict(pos=[12, 15, -22]),
    scatter=dict(asset="rock", variant="dark", count=8, seed=9, avoid=[[-6, -6, 6, 6]]),
    spawn=[-4.6, 3.0], spawns={"a2_whitby_lodging": [-4.6, 3.0], "a2_east_cliff_night": [0, -3.6]},
    props=[
        prop("a2_n_steps", "stairs", "stone_dark", 0.0, -5.0, name="The steps to the churchyard", radius=1.0,
             look="Stone steps up toward St. Mary's, vanishing into fog.",
             go="a2_east_cliff_night", go_cond="a2_trail_print&a2_trail_cloth&a2_trail_watch",
             go_fail="Three ways lead on from the lamps, and I have nothing to tell me which. I need some sign: a footprint, a scrap, someone who saw her."),
        prop("a2_n_gate", "door", "dark", -5.4, 3.0, rot=90, name="Back to the Crescent", radius=0.5, look="The door I came out of.", go="a2_whitby_lodging"),
        prop("a2_n_print", "rock", "grey", -2.0, 0.5, scale=0.25, name="Wet footprints", radius=0.4,
             look="Small bare footprints in the wet, going up and to the left. Lucy has gone without her slippers.",
             set="a2_trail_print", set_text="Bare feet, a woman's, heading for the foot of the steps. Bare feet! On these stones."),
        prop("a2_n_rail", "fence", "default", 3.0, -1.0, name="Iron railing", radius=0.4,
             look="Caught on a rusted spike, a scrap of white cambric the colour of Lucy's nightgown.",
             set="a2_trail_cloth", set_text="A strip of her nightgown, torn on the railing. She passed this way."),
        prop("a2_n_lamp1", "lantern", "default", -3.0, -2.0, name="Fog-lamp", radius=0.3, look="A dull orange in the thick air."),
        prop("a2_n_lamp2", "lantern", "default", 4.0, 2.4, name="Fog-lamp", radius=0.3, look="Another, equally helpless."),
        prop("a2_n_barrel", "barrel", "dark", -4.6, -3.0, name=None, radius=0.4),
    ],
    npcs=[
        npc("a2_watchman", "human_peasant_m", "a2_watchman", 4.8, -2.8, rot=-90, name="Night watchman",
            look="A tired night watchman with a lantern and a bad chest.", talk="a2_watchman_talk"),
        npc("a2_boy", "human_peasant_m", "villager", -4.2, 0.6, rot=90, name="Street boy", radius=0.4,
            look="An urchin of eleven, sitting up long past any bedtime, in a coat that was a man's.", talk="a2_boy_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="a2_j_trail")])],
)

LOC_DATA["a2_east_cliff_night"] = dict(
    cells=[4, 3], wall="stone_dark", floor="grass", interior=False, night=True,
    ambient=AMBIENT["night_exterior"], camera=cam([4, 3]), lights=lights_moon(3.2), moon=dict(pos=[-12, 16, -22]),
    scatter=dict(asset="rock", variant="mossy", count=10, seed=3, avoid=[[-8, -6, 8, 6]]),
    spawn=[0, 4.2], spawns={"a2_night_steps": [0, 4.2]},
    props=[
        prop("a2_nc_tomb", "tomb", "stone_mossy", -1.0, -3.0, name=None, radius=0.9),
        prop("a2_nc_seat", "bench", "oak", -1.0, -3.0, y=0.55, name="Lucy's seat", radius=0.9,
             look="The seat where we sit by day. By night it is a different place altogether."),
        prop("a2_nc_stone1", "gravestone", "stone_grey", -5.2, -2.2, name=None, radius=0.5),
        prop("a2_nc_stone2", "gravestone_point", "stone_mossy", -3.4, 0.2, name=None, radius=0.5),
        prop("a2_nc_stone3", "gravestone", "stone_dark", 3.2, -0.8, name=None, radius=0.5),
        prop("a2_nc_cross", "grave_cross", "stone_grey", 5.0, -3.2, name=None, radius=0.4),
        prop("a2_nc_church", "tower", "stone_grey", 5.5, -6.8, scale=0.6, name="St. Mary's church", radius=1.2,
             look="Black against the moon, with one lit window. The clock has stopped."),
        prop("a2_nc_abbey", "arch", "stone_mossy", -7.0, -4.2, name="The Abbey, in the moonlight", radius=0.8,
             look="The arch stands out with the moon behind it, and something pale seems to hang in the broken window."),
        prop("a2_nc_steps", "stairs", "stone_dark", 0.0, 4.9, rot=180, name="Back down the steps", radius=0.8,
             look="The way I came.", go="a2_night_steps"),
        prop("a2_nc_lamp", "lantern", "default", 1.8, -4.6, name=None, radius=0.3),
    ],
    npcs=[
        npc("a2_nc_lucy", "human_lucy", "nightgown", -1.0, -2.0, rot=0, name="Lucy", look="She sits upright on the seat, perfectly still, her head thrown back and her lips parted. Her nightgown is wet to the knee.",
            talk="a2_lucy_seat", radius=0.5),
        npc("a2_nc_figure", "human_dracula", "london", -0.8, -3.6, rot=0, name="Dark figure", cond="!a2_figure_gone",
            look="A tall, thin, black shape bending over her. In the moonlight, something white, and two small points of red like eyes.", talk="a2_figure_talk", radius=0.6),
    ],
    on_enter=[dict(once=True, do=[dict(journal="a2_j_arrive_seat")])],
)

# --------------------------------------------------------------------------------------------------------------------
# dialogue
# --------------------------------------------------------------------------------------------------------------------
DIALOGUE = {}

DIALOGUE["a2_lucy_talk"] = D("n0",
    n0=N("Lucy", "Mina, darling! I was just thinking of you. Do sit with me.",
         choices=[
             C("Tell me about the three proposals, Lucy.", "p1", cond="!a2_know_proposals"),
             C("Poor Dr. Seward, among his madmen. Let me hear how he fares.", "sew", cond="a2_know_proposals&!a2_cutaway_done"),
             C("How are you sleeping, Lucy?", "sleepw", cond="a2_log_ordered&!a2_lucy_home"),
             C("How do you feel today?", "decl", cond="a2_lucy_home"),
             C("Never mind. Drink your tea.", end=True),
         ]),
    p1=N("Lucy", "Oh Mina, such a day! Three proposals, and I have not breathed since. Dr. Seward first, grave and kind, very much in earnest, so I said no and felt like a wicked girl.",
         do=[dict(meet="seward"), dict(meet="quincey"), dict(meet="arthur")], next="p2"),
    p2=N("Lucy", "Then Mr. Quincey P. Morris, from Texas, who came in so drolly. I was in the middle of laughing when he told me it was serious, and then I was quite undone. He took it like the gentleman he is.", next="p3"),
    p3=N("Lucy", "And then dear Arthur, Lord Godalming's son. He had only to look at me, and I had only to say yes. Oh Mina, why can't a girl marry three men, or as many as want her, and save all this trouble?",
         do=[dict(set="a2_know_proposals"), dict(journal="a2_j_proposals")],
         choices=[
             C("You must marry the man you love, and no regrets.", "p4", do=[dict(set="a2_lucy_comforted")]),
             C("Tell them gently, and tell them soon. Delay is cruel.", "p4"),
         ]),
    p4=N("Lucy", "You are the sweetest. I shall write to them tonight, and if I weep on the paper you must not tell. Now, what shall I do with all this happiness?", end=True),
    sew=N("Lucy", "Dr. Seward? He sent me a long letter, quite exhausted. He is a man of science, he says, and likes best to be among those whose minds are broken, because he can learn from them. Poor man. Poor madmen.",
          choices=[
              C("[Let your thoughts go to the asylum]", "sew2"),
              C("Not now.", end=True),
          ]),
    sew2=N("Mina", "I close my eyes, and for a moment I am somewhere else, in a study full of books and the smell of carbolic. A phonograph is waiting...",
           do=[dict(set="a2_cutaway_started"), dict(meet="seward"), dict(card="Dr. Seward's Diary, 25 April. Kept in phonograph."), dict(protagonist="seward"), dict(goto="a2_seward_study")]),
    sleepw=N("Lucy", "Like a top, Mina! Only I woke two nights ago with my feet wet and my slippers on the wrong feet, and you scolding me. Oh, and I dreamed of the sea.",
             choices=[
                 C("You walk in your sleep, Lucy. We must be careful tonight.", "sleepw2"),
                 C("Just a dream, darling.", end=True),
             ]),
    sleepw2=N("Lucy", "Do you really think so? Mother will be so alarmed. Promise not to tell her. Lock the door, if you must, and keep the key, and I will not mind a bit.", do=[dict(set="a2_know_sleepwalk")], end=True),
    decl=N("Lucy", "Tired. Terribly tired, Mina, and I sleep all night and wake worn out. The marks on my throat sting a little. I must have scratched myself on the pin, you know. You were so very good to pin my shawl.",
           do=[dict(set="a2_decline_seen"), dict(journal="a2_j_decline2")],
           choices=[
               C("Let me see. [Look at her throat]", "decl2"),
               C("You must rest. I will not leave you.", end=True),
           ]),
    decl2=N("Mina", "Two tiny punctures, white-edged and red-rimmed, such as I would not give to a pin. They are very small. I do not like the look of them, or of how pale she is.", end=True),
)

DIALOGUE["a2_westenra_talk"] = D("n0",
    n0=N("Mrs. Westenra", "Mina, dear, there is a draught, I'm certain. Lucy takes such risks with her health, you know, and her father's death, and my heart... We must keep her quiet.",
         choices=[
             C("Does Lucy have a habit of walking in her sleep?", "walk"),
             C("Where do you keep the spare key to Lucy's door?", "key", cond="a2_log_ordered"),
             C("Mr. Holmwood has proposed, I hear.", "arthur", cond="a2_know_proposals"),
             C("I'll mind the draughts.", end=True),
         ]),
    walk=N("Mrs. Westenra", "As a child, indeed. It left her after her father died. But please don't speak of it to her; she is so sensitive. And Mina, you are such a comfort.", end=True),
    key=N("Mrs. Westenra", "The spare? Lock it up in the drawer, or the basket, or the old bookcase. I always put things where I shall remember them and then I don't. Look about the sitting-room, dear.", do=[dict(set="a2_know_key")], end=True),
    arthur=N("Mrs. Westenra", "Arthur Holmwood! His poor father is so very ill. She does not know how ill, and I will not tell her until it is quite necessary. Her happiness comes first.", end=True),
)

DIALOGUE["a2_maid_talk"] = D("n0",
    n0=N("Housemaid", "Beg pardon, miss. Cook says the sea-fret will be in by tea, and she's boiled up garlic broth, as her mother taught her for fever.",
         choices=[
             C("May I have a head of that garlic?", "g", cond="!a2_got_maid_garlic"),
             C("Is there news of the town?", "gossip"),
             C("Thank you.", end=True),
         ]),
    g=N("Housemaid", "Cook says take two, miss, if you'll swear not to tell the mistress how much she puts in.", do=[dict(give="garlic"), dict(set="a2_got_maid_garlic")], end=True),
    gossip=N("Housemaid", "The new searchlight on the East Cliff, miss, they're to try it out. Folks say a storm's brewing, the fishermen's wives won't have the washing out. And there's an old lady at the Abbey sees the White Lady every dusk.", end=True),
)

DIALOGUE["a2_postman_talk"] = D("n0",
    n0=N("Postman", "Letter for Miss Murray, miss. From foreign parts, the stamp says Buda-Pesth. A convent's seal on the back, if you don't mind me noticing.",
         choices=[
             C("Give it here, quickly.", "t", cond="!a2_got_letter", do=[dict(give="a2_agatha_letter"), dict(set="a2_got_letter"), dict(journal="a2_j_agatha")]),
             C("Thank you.", end=True),
         ]),
    t=N("Mina", "My hand trembles as I break the seal. At last, at last, news of Jonathan.", end=True),
)

DIALOGUE["a2_depart"] = D("n0",
    n0=N("Mina", "My trunk. The Sister's letter says Jonathan is in the hospital of St. Joseph and St. Mary, Buda-Pesth, broken down with brain fever, and has asked for me. I must go to him. But Lucy...",
         choices=[
             C("Pack and go. Jonathan needs me, and Lucy has her mother and Arthur.", "go", cond="has:a2_agatha_letter&a2_decline_seen"),
             C("I need to read the Sister's letter and see how Lucy is first.", "nope"),
             C("[Close the trunk]", end=True),
         ]),
    go=N("Mina", "I will write to Dr. Seward as I leave and ask him to look at her. He is the one man I can think of. And I will pray, if there is any praying that will serve.",
         do=[dict(card="Mina goes to Buda-Pesth, to Jonathan. Lucy grows paler every day. Arthur, from his father's deathbed, writes to Dr. Seward: 'Come, for God's sake.'"), dict(goto="a3_asylum_study")]),
    nope=N("Mina", "I cannot go until I know both: the Sister's news for Jonathan, and how Lucy truly is.", end=True),
)

DIALOGUE["a2_barometer"] = D("n0",
    n0=N("Mina", "The glass has fallen two-tenths since morning. Mr. Swales told me he can smell the storm in his bad knee, and the sunsets have been blood-red.",
         choices=[
             C("Take Lucy's arm and go to the East Cliff to watch the sky.", "go", cond="a2_swales_met&a2_cutaway_done&!a2_storm_started"),
             C("[Leave it]", end=True),
         ]),
    go=N("Mina", "The whole town is up on the cliff to see the new searchlight tried, and a hush has fallen over the sea.",
         do=[dict(set="a2_storm_started"), dict(card="6 August, near midnight. The sea-fret rolls in and the wind rises."), dict(goto="a2_cliff_storm")]),
)

# ---- Seward cutaway
DIALOGUE["a2_attendant_talk"] = D("n0",
    n0=N("Hennessey", "Evening, doctor. Number 12 is in good spirits tonight, which is to say, in his usual spirits.",
         choices=[
             C("What exactly does Renfield do all day?", "r"),
             C("Has anyone else been able to manage him?", "m"),
             C("Thank you, Hennessey.", end=True),
         ]),
    r=N("Hennessey", "Collects flies, doctor. Sugar on the window-sill and the flies come. Then he eats them. Last month it was spiders; he fed the flies to the spiders. Then he found a sparrow...", end=True),
    m=N("Hennessey", "Only me, sir, and only when he wants. He's polite to a man who doesn't argue. He asked me yesterday whether I knew the difference between a flea and a cat.", end=True),
)

DIALOGUE["a2_renfield_talk"] = D("n0",
    n0=N("Renfield", "Doctor, you must excuse me; the flies are very busy this evening and I should not like to neglect them. I have a purpose, you see.",
         choices=[
             C("Why do you eat flies, Mr. Renfield?", "flies", do=[dict(set="a2_renfield_met")]),
             C("I would like to see your notes on the spiders.", "spiders", cond="a2_renfield_met"),
             C("Do you wish for anything, Mr. Renfield?", "wish", cond="a2_renfield_met"),
             C("[Leave him]", end=True),
         ]),
    flies=N("Renfield", "The blood is the life, doctor, as the Scripture tells us. Flies are small lives; spiders eat flies; sparrows eat spiders; a cat would eat sparrows, and a man... a man would eat many lives and grow strong. It is the life that matters.",
            choices=[C("That is a remarkable theory.", "n0"), C("[Make a note]", end=True, do=[dict(set="a2_renfield_noted")])]),
    spiders=N("Renfield", "They are all numbered in a book, doctor. Each fed from the one before, and each given a place in the account. Would you not call that mathematics? You, who work with numbers of the soul?", end=True),
    wish=N("Renfield", "A kitten, doctor. A little one. I would be very good to it. And a great deal of sugar. No, I did not say that. Please forget it. You are a good man, doctor, and I should be sorry to see you hurt.", end=True),
)

DIALOGUE["a2_phono"] = D("n0",
    n0=N("Seward", "The cylinder is ready, the needle trimmed. Lucy's refusal is still raw, but work heals more than sympathy.",
         choices=[
             C("Record today's entry on R. M. Renfield.", "rec", cond="a2_renfield_met&!a2_phono_done"),
             C("Close the lid and think of Whitby.", "back", cond="a2_phono_done"),
             C("[Not yet]", end=True),
         ]),
    rec=N("Seward", "Patient, R. M. Renfield, aetat 59. Sanguine temperament, great physical strength, morbidly excitable. Periods of gloom ending in some fixed idea which I cannot make out. I fancy he is himself a dangerous man, and I think...",
          do=[dict(set="a2_phono_done"), dict(journal="a2_j_seward_diary")], next="n0"),
    back=N("Seward", "And there, for tonight, is that. I will go on with my rounds, and think kindly of Miss Westenra, who has made a good choice, and of her chosen friend who writes such letters.",
           do=[dict(set="a2_cutaway_done"), dict(protagonist="mina"), dict(card="Whitby. Mina Murray's Journal, 24 July."), dict(goto="a2_whitby_lodging")]),
)

# ---- East cliff
DIALOGUE["a2_swales_talk"] = D("n0",
    n0=N("Mr. Swales", "Ah, 'tis the young leddy. Sit ye down, miss, and I'll tell ye the truth, which is more than the parson will. I've sat here since afore your mother was born.",
         choices=[
             C("May I sit and hear you talk?", "sit", cond="!a2_swales_met", do=[dict(set="a2_swales_met"), dict(journal="a2_j_swales")]),
             C("What do you mean, the stones lie?", "lies", cond="a2_swales_met"),
             C("Tell me about the Abbey and the legends.", "legend", cond="a2_swales_met"),
             C("Will the weather hold, Mr. Swales?", "weather", cond="a2_swales_met"),
             C("You are known to every officer on the quay. Would you vouch for me if I need to see something there?", "vouch", cond="a2_swales_met&!a2_swales_vouch"),
             C("Good day, Mr. Swales.", end=True),
         ]),
    sit=N("Mr. Swales", "Ye're a nice lass. Now these stones, they're all lies, every one. There's folk lying under 'em as ne'er were 'drowned', as ne'er were 'beloved', as ne'er did a dozen things the stone says. 'Tis the Judgement Day I fear for the carver more than the dead.", next="n0"),
    lies=N("Mr. Swales", "Aye. Look at 'em! 'Sacred to the memory.' Tchah. But there's one big lie in this yard that's a rare comfort, miss: the mother's stone, the widow's, for the lad that fell at Kettleness. 'Only son.' Aye, so it said. I'd not be surprised if a clever man who knew that lie hid something where nobody'd think to lift it.",
           do=[dict(set="a2_stone_hint"), dict(journal="a2_j_stones")], next="n0"),
    legend=N("Mr. Swales", "Old Hilda's Abbey. There's the White Lady in the window at sunset, and the Barguest dog that walks before a death. And them that took their own lives lie yonder, where your seat is, though the parson says nowt. I sat on that stone as a lad.", next="n0"),
    weather=N("Mr. Swales", "Mares'-tails and a sun like blood. There's a storm in 'em, miss. Afore the week's out ye'll see the sea come up and swallow the piers. And God help any ship at sea.", do=[dict(set="a2_swales_storm_warned")], next="n0"),
    vouch=N("Mr. Swales", "Aye, miss, I'll say a word. The constable's my nephew's lad, and he'll mind his granddad. Ye need only say: Swales sent me.", do=[dict(set="a2_swales_vouch")], next="n0"),
)

DIALOGUE["a2_visitor_talk"] = D("n0",
    n0=N("Lady from Leeds", "My dear, did you know that this very churchyard inspired the author of that famous ballad? The guide-book says so. Or the guide-book says something. And that Abbey, would you credit it, is the only ruin in England with its own ghost.",
         choices=[
             C("Have you seen the ghost?", "g"),
             C("Excuse me, I'm looking for old Mr. Swales.", "s"),
             C("Good afternoon.", end=True),
         ]),
    g=N("Lady from Leeds", "No, but the cab-driver has, twice, and the second time he was sober. The guide-book has a footnote on it.", end=True),
    s=N("Lady from Leeds", "The old man by the bench? Oh, my dear, he says the most shocking things about the stones. Quite refreshing, in a churchyard.", end=True),
)

# ---- harbour
DIALOGUE["a2_chandler_talk"] = D("n0",
    n0=N("Mrs. Pinder", "Morning, miss. Rope, twine, tar and tallow, and the best garlic for sailors' wives. What'll it be?",
         choices=[
             C("A length of good rope, if you please.", "rope", cond="!a2_got_rope"),
             C("A second head of garlic, for a friend.", "garlic", cond="!a2_got_chandler_garlic"),
             C("What are the sailors saying about the weather?", "weather"),
             C("Just looking, thank you.", end=True),
         ]),
    rope=N("Mrs. Pinder", "There y'are, six fathoms of the tarred hemp. No charge for a young lady who looks like she'll make good use of it.", do=[dict(give="rope"), dict(set="a2_got_rope")], next="n0"),
    garlic=N("Mrs. Pinder", "Two heads, then, tied with a bit of twine. Sailors swear it keeps off the ague. The old women say it keeps off worse.", do=[dict(give="garlic"), dict(set="a2_got_chandler_garlic")], next="n0"),
    weather=N("Mrs. Pinder", "That's not for me to say. But look at the gulls, miss; they've all come in off the sea, and not a one flying out. They're no fools.", end=True),
)

DIALOGUE["a2_fisher_talk"] = D("n0",
    n0=N("Old fisherman", "Mind the nets, miss. Aye, the sky wants watching. I've seen mares'-tails like that but twice, and both times someone died.",
         choices=[
             C("Is the coastguard about?", "cg"),
             C("What's your opinion of old Swales?", "sw"),
             C("I'll mind the nets.", end=True),
         ]),
    cg=N("Old fisherman", "Dunn? He keeps the hut locked, miss; he's careful. But he's a forgetful man; he leaves his spare in the churchyard, under one of them lying stones, for safety. I'd not tell you where, but I know the stone is for a widow's son. Off you go.", do=[dict(set="a2_fisher_hint")], end=True),
    sw=N("Old fisherman", "Swales? He's older than the pier. He says the dead are all liars, and the living are worse. Not a bad man to sit beside.", end=True),
)

DIALOGUE["a2_constable_talk"] = D("n0",
    n0=N("Constable", "Back, miss, if you please. The ship's under guard till the Board of Trade man comes. The dead captain's still aboard.",
         choices=[
             C("Mr. Swales sent me.", "swales", cond="a2_swales_vouch"),
             C("Mr. Billington said I might look.", "bill", cond="a2_billington_leave"),
             C("Please, constable. It is an extraordinary thing, and I'd like to see it.", "plead"),
             C("I'll wait.", end=True),
         ]),
    swales=N("Constable", "Old Swales? My grandfather's friend? Why, he'd have my hide. Go on, miss, but mind your skirts, and don't touch anything you don't have to.", do=[dict(set="a2_pass"), dict(journal="a2_j_pass")], end=True),
    bill=N("Constable", "From Mr. Billington, the solicitor? He said that? Go on, miss, but touch nothing that's evidence.", do=[dict(set="a2_pass"), dict(journal="a2_j_pass")], end=True),
    plead=N("Constable", "I'm sorry, miss, but I can't let anyone aboard on a feeling. Come with the owner's solicitor, or someone I know.", end=True),
)

DIALOGUE["a2_billington_talk"] = D("n0",
    n0=N("Mr. Billington", "Madam, I am Samuel F. Billington, of 7 The Crescent. The wretched ship is consigned to me, and I assure you I know nothing of what is in it.",
         choices=[
             C("May I look at the vessel? I should like to describe it for friends.", "leave", cond="!a2_billington_leave"),
             C("Where were the boxes to go, Mr. Billington?", "carfax", cond="has:a2_bill&!a2_carfax_learned"),
             C("I have seen the consignment note. Who is Count Dracula?", "dracula", cond="a2_carfax_learned"),
             C("Good day.", end=True),
         ]),
    leave=N("Mr. Billington", "Eh? I suppose so; it is not as if the Board of Trade will let anyone else near it. Tell the constable I said so. My clerk is distraught as it is.", do=[dict(set="a2_billington_leave")], end=True),
    carfax=N("Mr. Billington", "Ah! That note. Fifty boxes of clay to be taken to Carfax, an estate at Purfleet, bought through Mr. Hawkins of Exeter. Carter, Paterson and Co. are to cart them. It is quite regular, and quite incomprehensible.", do=[dict(set="a2_carfax_learned"), dict(journal="a2_j_carfax")], end=True),
    dracula=N("Mr. Billington", "A foreign nobleman, a client of Mr. Hawkins. Beyond that, madam, I know only that he bought a house in England and sent his earth ahead of him. The ways of the gentry are strange.", end=True),
)

# ---- hut
DIALOGUE["a2_notice_read"] = D("n0",
    n0=N("Mina", "A notice-board, thick with pins. Among the tide-tables and warnings, a hand-written note: 'In case of lock-out, spare key kept with the stone of the widow's only son. Do not tell the boys. - Dunn.'",
         do=[dict(journal="a2_j_hut_clue"), dict(set="a2_notice_read")], end=True),
)

DIALOGUE["a2_coastguard_talk"] = D("n0",
    n0=N("Officer Dunn", "Miss Murray, is it not? Come in, and mind the oil. I've been sixteen years on this coast and never seen a glass drop like that.",
         choices=[
             C("What do you think is coming?", "storm"),
             C("Might I borrow a little brandy for Lucy's nerves?", "brandy", cond="!a2_got_dunn_brandy"),
             C("I have read the log of the Demeter. What do you make of it?", "log", cond="a2_log_ordered"),
             C("I'll leave you to it.", end=True),
         ]),
    storm=N("Officer Dunn", "A big blow out of the north-east, if I'm any judge. And I'm judge of nothing else. If a ship's caught outside the piers tonight, God help her.", end=True),
    brandy=N("Officer Dunn", "Ay, here, take a nip's worth in this flask. Mind, I'd not give it to every lady.", do=[dict(give="brandy"), dict(set="a2_got_dunn_brandy")], end=True),
    log=N("Officer Dunn", "I read it, miss, in the coroner's office. A man who kept a log in a gale, and a mate who went for a knife at a ghost. I've no explanation, and neither has the coroner. He said 'open verdict.' I say a devil rode that ship.", end=True),
)

DIALOGUE["a2_log_desk"] = D("n0",
    n0=N("Mina", "A bare desk, ink-stained. If I had the leaves of the ship's log, I could lay them in order here, and read what happened. I should need all four.",
         choices=[
             C("Lay out the four leaves of the log.", "o1", cond="has:a2_log_p1&has:a2_log_p2&has:a2_log_p3&has:a2_log_p4&!a2_log_ordered"),
             C("The log is already read.", "done", cond="a2_log_ordered"),
             C("[Step away]", end=True),
         ]),
    done=N("Mina", "I have read it three times, and it has not changed.", end=True),
    o1=N("Mina", "Four leaves, all of different sizes, all dated. Which comes first?",
         choices=[
             C("The leaf dated 4 August, in a shaky hand.", "w1"),
             C("The leaf dated 29 July to 3 August, with the mate's name.", "w1"),
             C("The leaf dated 17 to 28 July, about the stranger.", "w1"),
             C("The leaf headed Varna, 6 July to 16 July.", "o2", do=[dict(set="a2_log_1")]),
         ]),
    w1=N("Mina", "No. That speaks of men already missing. Something must come before it.", next="o1"),
    o2=N("Mina", "Varna: the cargo of silver sand and boxes of earth, the Bosphorus, the Dardanelles, a man gone off the watch off Cape Matapan. And next?",
         choices=[
             C("The leaf dated 4 August.", "w2"),
             C("The leaf dated 29 July to 3 August.", "w2"),
             C("The leaf dated 17 to 28 July, about the stranger.", "o3", do=[dict(set="a2_log_2")]),
         ]),
    w2=N("Mina", "That cannot be next; it assumes the stranger, and no one has yet seen him.", next="o2"),
    o3=N("Mina", "Olgaren saw the tall thin man. The crew searched the ship, found nothing. Then Biscay and the fog, and the second mate gone. And now?",
         choices=[
             C("The leaf dated 4 August.", "w3"),
             C("The leaf dated 29 July to 3 August, with the mate.", "o4", do=[dict(set="a2_log_3")]),
         ]),
    w3=N("Mina", "He is alone in that one. The mate must still be alive in the one before.", next="o3"),
    o4=N("Mina", "The mate stabs the pale figure, and the knife passes through. He opens a box with a tool-chest, screams, and leaps into the sea. That leaves the last leaf.",
         choices=[C("Read the last leaf: 4 August.", "r1")]),
    r1=N("Captain's log", "4 August. Alone, with the thing aboard. I am lashing my hands and a crucifix to the wheel. If we go down, bury me with this where my body is found, so that He may not have my soul. Whatever comes, I have done my duty as captain and as a Christian. The knots I tie with my teeth.",
         do=[dict(set="a2_log_ordered"), dict(journal="a2_j_log")], next="r2"),
    r2=N("Mina", "A tall, pale thing came out of a box in the hold and killed the crew one by one, until the captain alone remained to bring the ship to harbour. That man, and the dog that leaped ashore, were no creatures I know. Fifty boxes. Mr. Hawkins. Jonathan's firm. I feel quite cold.", end=True),
)

# ---- sexton
DIALOGUE["a2_sexton_talk"] = D("n0",
    n0=N("Sexton", "Afternoon, miss. Mind the old slabs; one of 'em tilts. They say an abbot lies under it.",
         choices=[
             C("The White Lady, sexton, have you seen her?", "lady"),
             C("Is there anything of value in the Abbey?", "silver", cond="!a2_got_silver"),
             C("Lucy loves the seat on the cliff. Do you know it?", "seat"),
             C("Good day.", end=True),
         ]),
    lady=N("Sexton", "At sunset, in the east window, the figure of a woman in white. 'Tis only the light, and the stones, and the Westerley wind on the glass. But I'd not be the one to stand there after dark.", end=True),
    silver=N("Sexton", "Digging a drain last spring, I turned up a little coin: silver, worn smooth, a sailor's penny maybe. You may have it, miss, if you promise not to throw it in the sea.", do=[dict(give="silver"), dict(set="a2_got_silver")], next="n0"),
    seat=N("Sexton", "That's on a suicide's grave. The parson says it matters not. I say a seat is a seat, but I'd not sleep there. There's folk have seen things at it, in the dark.", end=True),
)

# ---- storm
DIALOGUE["a2_swales_storm"] = D("n0",
    n0=N("Mr. Swales", "I told 'ee so, miss! There's a hollow sound in the sea, like a giant beating on the Judgement. And a ship is out there tonight, mark my words, with her sails afire.",
         choices=[
             C("You are a prophet, Mr. Swales.", "p"),
             C("I'm frightened.", "f"),
         ]),
    p=N("Mr. Swales", "I'm an old fool, miss, who's watched the sea sixty year. The wind was the Lord's, but the warning was mine.", end=True),
    f=N("Mr. Swales", "Aye, and so ye should be. But fear's honest, miss. 'Tis the folk that aren't afraid I worry for.", end=True),
)

DIALOGUE["a2_officer_talk"] = D("n0",
    n0=N("Officer", "Stand back! Miss, you must keep clear of the searchlight. She's untried, and the sea is a madman tonight. A schooner is making for the piers.",
         choices=[
             C("Can she make it?", "can"),
             C("What flag does she fly?", "flag"),
             C("I'll stay clear.", end=True),
         ]),
    can=N("Officer", "Not by seamanship. By fool's luck, or the Devil's. The searchlight shows her sails, then loses her. She has no crew on deck that I can see.", end=True),
    flag=N("Officer", "Russian, by her cut. From Varna, I'd stake my pension. She's trying for the entrance, but the wind is dead on shore.", end=True),
)

DIALOGUE["a2_crowd_talk"] = D("n0",
    n0=N("Onlooker", "Ye gods, did you see that wave? Over the piers, it was, as high as the church! And the fog like hands, miss, like the wet hands of the drowned, touching everyone.",
         choices=[
             C("Is anyone out in a boat?", "boat"),
             C("It is a terrible sight.", end=True),
         ]),
    boat=N("Onlooker", "Not on the Lord's life. The lifeboat crew's gathered, waiting. There's a ship, though. Look! She's making straight for the harbour mouth, and no one at her helm.", end=True),
)

DIALOGUE["a2_storm_watch"] = D("n0",
    n0=N("Mina", "The wind tears at my hair. The sea below is white and black, and the fog rolls in like a wall. The searchlight swings out over the water, and stops.",
         choices=[C("Look where the light has stopped.", "w1")]),
    w1=N("Mina", "A schooner! Every sail set, plunging between the piers, with a gale behind her and no hand on the sheets. 'She will be dashed to pieces,' someone cries. The searchlight lights her helm: a man stands there, bowed, quite still.", next="w2"),
    w2=N("Mina", "She runs full tilt on the sand of Tate Hill Pier. And from below her decks an enormous dog, the size of a mastiff, leaps out upon the shore and bounds straight up the cliff, toward the churchyard, into the dark.",
         do=[dict(set="a2_saw_wreck"), dict(journal="a2_j_storm")], next="w3"),
    w3=N("Mina", "The crowd cries out. Men run for the pier. The fog is thick as milk. I cling to the railing and see nothing more.",
         choices=[
             C("Go home to Lucy, shaken and soaked.", "end", cond="a2_saw_wreck"),
             C("Stay a moment longer.", end=True),
         ]),
    end=N("Mina", "Lucy is sound asleep when I return. She has been out of bed twice, Mother says, and had to be coaxed back. We shall talk in the morning.",
          do=[dict(set="a2_storm_over"), dict(card="Next morning. The wreck lies at Tate Hill Pier."), dict(goto="a2_harbour")]),
)

# ---- night
DIALOGUE["a2_bed_dialogue"] = D("n0",
    n0=N("Mina", "Lucy sleeps. It is past eleven. I remember how she walked in her sleep as a girl, and what Mother said. I should make sure of the door, the window, a warm shawl and a pin laid by me, in case the worst comes.",
         choices=[
             C("Lie down and sleep, everything being in order.", "sleep", cond="a2_door_locked&a2_window_fastened&has:a2_shawl&has:a2_pin&has:a2_lucy_door_key&a2_log_ordered"),
             C("Lie down and sleep.", "nope"),
             C("[Not yet]", end=True),
         ]),
    nope=N("Mina", "I lie down but cannot rest. The door is not locked with the key in my keeping, or the window is not fastened, or the shawl and pin are not laid ready. And is the ship's log read? Something is wrong.", end=True),
    sleep=N("Mina", "I lock the door, put the key under my pillow, and sleep. Some hours later, I wake to a sound like a sigh. The moon is in the room.",
            do=[dict(set="a2_night"), dict(set="a2_lucy_gone"), dict(journal="a2_j_gone"), dict(card="Night of 10-11 August. 1 a.m.")], next="wake"),
    wake=N("Mina", "Lucy's bed is empty. The door is still locked, with the key under my pillow. The window, which I bolted, is open on the night. She cannot have gone by the door. I take the shawl, the pin and the key, and go.", end=True),
)

DIALOGUE["a2_lucy_asleep_talk"] = D("n0",
    n0=N("Mina", "She is lovely, asleep. I should not like to wake her. But her hands are cold, and I tuck the quilt about her as I would for a child.", end=True),
)

DIALOGUE["a2_watchman_talk"] = D("n0",
    n0=N("Watchman", "Out late, miss, and in a nightdress under that coat? Looking for someone? A girl in white went by an hour since, walking like in a dream, up to the churchyard.",
         choices=[
             C("Which way? Did she say anything?", "way"),
             C("Thank you!", end=True),
         ]),
    way=N("Watchman", "Up the steps, miss, quick and quiet. Barefoot. I called, but she never turned her head. And, begging your pardon, I saw something black behind her in the fog.", do=[dict(set="a2_trail_watch")], end=True),
)

DIALOGUE["a2_boy_talk"] = D("n0",
    n0=N("Street boy", "Yer lookin' for a white lady, miss? She went down to the quay, she did, I seen her. Ghost, mebbe.",
         choices=[
             C("Are you sure it was the quay?", "sure"),
             C("Thank you.", end=True),
         ]),
    sure=N("Street boy", "Pretty sure, miss. It was dark. Or she might 'ave gone t'other way. But the watchman 'ud know, 'e saw 'er, 'e did.", end=True),
)

DIALOGUE["a2_figure_talk"] = D("n0",
    n0=N("Mina", "I run up the last steps, calling her name. Something long and black stoops over the white shape on the seat, bent low, as if to whisper.",
         choices=[
             C("Rush forward, crying out.", "f1"),
             C("Call her name as loudly as I can.", "f1"),
         ]),
    f1=N("Mina", "The thing raises its head. In the moonlight I see a white face, and red eyes, such as Lucy described in her dream. Then a flapping of dark wings; a great bat wheels up out of the churchyard and is gone. All is quiet.",
         do=[dict(set="a2_figure_gone"), dict(journal="a2_j_seat")], end=True),
)

DIALOGUE["a2_lucy_seat"] = D("n0",
    n0=N("Mina", "Lucy sits upright on the seat, her eyes half shut and her head thrown back. She breathes in long, heavy sighs. Her lips are parted. At her throat... I can scarcely see for the shadows.",
         choices=[
             C("Wrap her in the shawl and fasten it with the safety-pin.", "pin", cond="a2_figure_gone&has:a2_shawl&has:a2_pin&!a2_lucy_rescued"),
             C("Look at her throat.", "throat", cond="a2_lucy_rescued"),
             C("Wake her gently.", "wake", cond="a2_lucy_rescued"),
             C("Lead her home.", "home", cond="a2_lucy_woken"),
             C("[Step back]", end=True),
         ]),
    pin=N("Mina", "I wrap the shawl about her and fasten it at the throat with the pin, but my hands are shaking, and I fear I must have pricked her, for she gives a little cry and puts her hand to her neck.",
          do=[dict(take="a2_shawl"), dict(take="a2_pin"), dict(set="a2_lucy_rescued"), dict(journal="a2_j_pin")], next="n0"),
    throat=N("Mina", "Beneath the shawl, on her white throat, two small red spots. I think the pin has marked her. But the marks are far apart, and I know in my heart that the pin does not make such marks.", next="n0"),
    wake=N("Lucy", "Mina? Where am I? Oh, I was dreaming. There was a sea, and a voice calling, and I walked on air. Why is my throat sore? And why are my feet wet? Did I walk in my sleep again?",
           do=[dict(set="a2_lucy_woken")], next="n0"),
    home=N("Mina", "She leans heavily on my arm. We go down the steps together in the grey light, I praying under my breath, she silent and dreamy.",
           do=[dict(set="a2_lucy_home"), dict(card="12 August. Mina's journal: 'Lucy is not herself. She is very pale. I do not like it.'"), dict(goto="a2_whitby_lodging")]),
)

# --------------------------------------------------------------------------------------------------------------------
# items
# --------------------------------------------------------------------------------------------------------------------
ITEMS = {
    "a2_lucy_letter": dict(name="Lucy's letter", asset="book", variant="diary", desc="Lucy's account of the three proposals: a girl in bliss and despair."),
    "a2_pin": dict(name="Safety-pin", asset="key", variant="default", desc="A large safety-pin. It will fasten a shawl at a throat."),
    "a2_shawl": dict(name="Warm shawl", asset="rug", variant="cream", desc="The warmest shawl we own. Lucy will need it."),
    "a2_lucy_door_key": dict(name="Key to Lucy's door", asset="key", variant="gold", desc="The key to the door of the room Lucy and I share."),
    "a2_hut_key": dict(name="Coastguard's spare key", asset="key", variant="default", desc="A small iron key on tarred twine."),
    "a2_crowbar": dict(name="Crowbar", asset="hammer", variant="default", desc="A short iron crowbar."),
    "a2_lantern": dict(name="Storm lantern", asset="lantern", variant="default", desc="A stout lantern that will not blow out."),
    "a2_cabin_key": dict(name="Cabin key", asset="key", variant="gold", desc="A key of dull brass, from the captain's pocket."),
    "a2_log_p1": dict(name="Log leaf: Varna to Matapan", asset="book", variant="leather", desc="First leaf of the log, dated from 6 July to 16 July. Varna, the Bosphorus, the Dardanelles."),
    "a2_log_p2": dict(name="Log leaf: the stranger", asset="book", variant="leather", desc="A leaf dated from 17 July to 28 July. A stranger on deck, the search, the Bay of Biscay."),
    "a2_log_p3": dict(name="Log leaf: the mate", asset="book", variant="leather", desc="A leaf dated from 29 July to 3 August. Men missing, the mate, the box."),
    "a2_log_p4": dict(name="Log leaf: the last entry", asset="book", variant="red", desc="The last entry, 4 August, from a bottle in the captain's pocket."),
    "a2_bill": dict(name="Consignment note", asset="book", variant="red", desc="Fifty boxes of earth for Mr. S. F. Billington of 7 The Crescent, forwarded by Hawkins's agents."),
    "a2_rosary": dict(name="Captain's rosary", asset="crucifix", variant="silver", desc="A string of beads and a small cross, still stiff from the cords that held them to the wheel."),
    "a2_agatha_letter": dict(name="Letter from Sister Agatha", asset="book", variant="leather", desc="From the Hospital of St. Joseph and Ste. Mary, Buda-Pesth: 'Mr. Harker has had a sharp attack of brain fever...'"),
}

# --------------------------------------------------------------------------------------------------------------------
# journal
# --------------------------------------------------------------------------------------------------------------------
M = "Mina Murray's journal"
JOURNAL = {
    "a2_j_undercroft": dict(title="Under the abbey", source="Mina Murray's journal",
                            text="A stair behind the founder's slab goes down beneath the abbey: an undercroft of old monks' graves, cold as a cellar and reeking of something sharp and animal. Someone has been here, and not a monk. The dust is scuffed, and a rag of white lawn hangs from a nail. I think of Lucy's sleeping feet, and how far they have wandered."),
    "a2_j_arrive": dict(title="24 July. Whitby", source=M, text="Lucy met me at the station and drove me to the Crescent, which looks out over the harbour and the East Cliff and the sea. I have had no letter from Jonathan since the 29th of June. Lucy's mother is sweet, and Lucy is lovelier than ever."),
    "a2_j_proposals": dict(title="Three proposals", source="Lucy Westenra's letter", text="Dr. Seward, Mr. Quincey P. Morris and Arthur Holmwood all asked for my hand on the same day. I refused two and accepted one. Why can't a girl marry three men? I am so happy and so wretched at once."),
    "a2_j_seward_intro": dict(title="Dr. Seward's study", source="Dr. Seward's diary", text="Lucy has refused me, as I feared. I must turn to work. My most interesting case is R. M. Renfield: sanguine, strong, excitable, with a fixed idea that he must eat living things to gain their life."),
    "a2_j_seward_diary": dict(title="Renfield", source="Dr. Seward's phonograph diary", text="Patient Renfield collects flies, spiders and now a sparrow. 'The blood is the life,' he says. A homicidal maniac of a peculiar kind, perhaps. I will watch him closely, and write down what he wants."),
    "a2_j_east_cliff": dict(title="The East Cliff", source=M, text="The churchyard is the nicest spot in Whitby, with seats to sit on and the sea laid out below. Lucy loves the seat on the suicide's tomb. Old men sit on the benches and talk all day, and the oldest is Mr. Swales."),
    "a2_j_swales": dict(title="Old Mr. Swales", source=M, text="'It be all lies,' said Mr. Swales of the stones. I think he is the most honest man in Whitby. He tells me the Barguest, the Abbey ghost and the dead are no worse than the living. He is ninety-five."),
    "a2_j_stones": dict(title="The lying stones", source=M, text="Mr. Swales says one stone, the widow's, for the only son George Canon who fell at Kettleness, is a bigger lie than most, and a clever man would hide something there. Is that the coastguard's spare key?"),
    "a2_j_harbour": dict(title="Tate Hill Pier", source=M, text="The harbour is full of boats, the quay is full of gossip, and the sky is full of gulls. The coastguard keeps a hut under the cliff with a heavy padlock. The fishermen talk of mares'-tails and bad weather."),
    "a2_j_hut": dict(title="The coastguard's hut", source=M, text="Officer Dunn keeps his hut in good order: a stove, charts, a tool-chest, a storm lantern and a notice-board. He tells me he has never seen the glass drop like this. There is a desk where I may set out papers."),
    "a2_j_hut_clue": dict(title="Dunn's notice", source=M, text="'Spare key kept with the stone of the widow's only son.' That is George Canon's stone in the East Cliff churchyard, whose epitaph Mr. Swales so detests. The coastguard hides his key in a lie."),
    "a2_j_abbey": dict(title="The Abbey", source=M, text="The Abbey is the loveliest ruin in the land. The sexton says the White Lady shows in the great window at sunset. I picked wild roses and found a clean ash bough and a font brimming with rain."),
    "a2_j_storm_rises": dict(title="6 August. The storm", source=M, text="Sunset blood-red, mares'-tails across the sky, and a hush on the sea. Then the wind rose, and the waves came over the piers. All the town stands on the cliff in the fog, and the searchlight sweeps the water."),
    "a2_j_storm": dict(title="The Demeter runs ashore", source=M, text="A schooner ran between the piers with every sail set and a dead man lashed to the wheel. When the keel struck sand an immense dog sprang from below, bounded up the cliff and was lost in the fog. It made for the churchyard."),
    "a2_j_wreck_morning": dict(title="7 August. The wreck", source=M, text="The Demeter of Varna lies on Tate Hill Pier, her sails in rags. A constable keeps the crowd back. Mr. Billington, to whom she is consigned, is greatly distressed. All the town speaks of the dog and the dead steersman."),
    "a2_j_pass": dict(title="Leave to go aboard", source=M, text="The constable let me through. A word from Mr. Swales, or from the consignee, is as good as a warrant in Whitby. I shall see the dead captain and the ship."),
    "a2_j_wreck": dict(title="Aboard the Demeter", source=M, text="The deck is wet and bare. The wheel is lashed with cords and the dead man's hands are bound over a crucifix. His eyes are shut; his face is quite calm. Whatever he saw, he met it as a man."),
    "a2_j_captain": dict(title="The captain", source="Log of the Demeter", text="He fastened the knots with his teeth. In his pocket, a corked bottle and a cabin key; in his hands, a crucifix and a rosary. He wished it known that he was captain, and a Christian, and he did his duty."),
    "a2_j_boxes": dict(title="Fifty boxes of earth", source=M, text="The hold is full of great boxes of mould, marked for Mr. Billington. One is open, and the earth in it has been lain in. Another has its nails bent out from within. They came from Varna with the ballast."),
    "a2_j_log": dict(title="The Log of the Demeter", source="Log of the Demeter", text="Crew uneasy off Cape Matapan; a tall thin stranger seen; men vanish one by one in fog and storm; the mate stabs the figure and the knife passes through; he opens a box, screams, leaps into the sea. The captain, alone, lashes himself to the wheel."),
    "a2_j_carfax": dict(title="Carfax", source=M, text="The fifty boxes were consigned to a house called Carfax at Purfleet, bought through Mr. Hawkins. Jonathan's firm! I cannot rid myself of the feeling that Jonathan's long silence and this ship are connected."),
    "a2_j_swales_dead": dict(title="10 August. Mr. Swales is dead", source=M, text="The captain was buried today, with a hundred boats at the funeral. When we came to Lucy's seat, Mr. Swales was lying there, his neck broken, his face frozen in horror. 'He had been dreading it,' someone said. And the dog..."),
    "a2_j_gone": dict(title="11 August. Lucy is gone", source=M, text="I woke at one in the morning and found Lucy's bed empty. The door was still locked, the key under my pillow, but the window stood open. I took the shawl, a pin and the key, and went out."),
    "a2_j_trail": dict(title="Tracking Lucy", source=M, text="The fog lamps burn like dull coals. Bare footprints in the wet, a strip of her nightgown on a railing, a watchman who saw her go up the steps toward the churchyard. I must be quick."),
    "a2_j_arrive_seat": dict(title="The churchyard at night", source=M, text="The moon is full. The clock of St. Mary's has stopped. On the seat I can see something white, and something dark that bends over it."),
    "a2_j_seat": dict(title="Red eyes on the seat", source=M, text="A long, black form leaned over Lucy, and when I called it raised a white face with red, gleaming eyes. Then it was gone, and a great bat wheeled over the churchyard. Lucy sat quite still, breathing hard."),
    "a2_j_pin": dict(title="The safety-pin", source=M, text="I wrapped her in the shawl and fastened it at her throat with a pin, so she should not catch cold. I must have pricked her, for she cried out. Two tiny red spots lay on her skin beneath it."),
    "a2_j_decline": dict(title="12 August. A pale Lucy", source=M, text="Lucy sleeps all night and wakes weary. Her cheeks are white and her lips colourless. Mrs. Westenra says it is the sea air; I fear it is something else. Those marks on her throat do not heal."),
    "a2_j_decline2": dict(title="The marks on her throat", source=M, text="Two small punctures with white edges and red rims, a quarter-inch apart. Lucy blames my pin. A pin never made such a mark, and I never pinned her twice. She is growing paler by the day."),
    "a2_j_agatha": dict(title="Sister Agatha's letter", source="Letter from Buda-Pesth", text="'Mr. Harker is with us and has had a sharp attack of brain fever. He has been raving of wolves, poison and ghosts, and of things I dare not name. Come to him, if you can; he asks for you.' - Sister Agatha."),
}

# --------------------------------------------------------------------------------------------------------------------
# seed variation
# --------------------------------------------------------------------------------------------------------------------
PALETTES = {
    "a2_whitby_lodging": [dict(wall="plaster", floor="planks", wood="dark", cloth="blue"),
                          dict(wall="plaster", floor="planks", wood="pale", cloth="green"),
                          dict(wall="plaster_dirty", floor="planks", wood="oak", cloth="cream")],
    "a2_lucy_bedroom": [dict(wall="plaster", floor="planks", wood="pale", cloth="blue"),
                        dict(wall="plaster_dirty", floor="planks", wood="oak", cloth="green")],
    "a2_coastguard_hut": [dict(wall="plaster_dirty", floor="planks", wood="dark", cloth="red"),
                          dict(wall="stone_grey", floor="planks", wood="oak", cloth="blue")],
    "a2_seward_study": [dict(wall="plaster_dirty", floor="planks", wood="ebony", cloth="green"),
                        dict(wall="stone_grey", floor="planks", wood="dark", cloth="red")],
    "a2_demeter_cabin": [dict(wall="planks", floor="planks", wood="dark", cloth="black"),
                         dict(wall="plaster_dirty", floor="planks", wood="ebony", cloth="blue")],
    "a2_east_cliff": [dict(floor="grass"), dict(floor="dirt")],
    "a2_abbey_ruins": [dict(floor="grass", wall="stone_mossy"), dict(floor="grass", wall="stone_grey")],
}

PLACEMENTS = {
    "a2_lucy_door_key": [
        dict(prop="a2_l_table", text="Under the blotter, a small brass key labelled 'Lucy's door' in Mrs. Westenra's careful hand.", hint="The blotter lies crooked on the writing table."),
        dict(prop="a2_l_shelf", text="Behind the Bible, a brass key on a ribbon: 'Lucy's door'.", hint="The Bible stands a little out from the row."),
        dict(prop="a2_l_chair1", text="Under the embroidered cushion, a brass key tagged 'Lucy's door'.", hint="The cushion of my writing chair sits lumpily."),
    ],
}

GATES = {
    "a2_d_cabin_door": [
        dict(cond="has:a2_cabin_key", fail="Locked. The captain must have kept the key by him.", needs="a2_cabin_key"),
        dict(cond="has:a2_crowbar", fail="The padlock is rusted shut. A lever might shift the hasp.", needs="a2_crowbar"),
    ],
}

# --------------------------------------------------------------------------------------------------------------------
# combat: the great dog (optional)
# --------------------------------------------------------------------------------------------------------------------
ENEMIES_EXTRA = {
    "a2_dog": {"name": "The huge dog", "model": "wolf_big", "hp": 20, "spd": 6, "dmg": [3, 6], "acc": 70, "eva": 10,
               "tags": ["beast"], "flee_at": 0.35, "nerve_hit": 2, "book": "ch.7 the immense dog that leapt from the Demeter"},
}
ENCOUNTERS_EXTRA = {
    "a2_dog_pier": {"name": "The dog under the pier", "time": "dawn", "enemies": ["a2_dog"], "flee_ok": True,
                    "intro": "It crouches, hackles up, in the shadow of the pier. It has been fed on something, and not dog-biscuit.",
                    "win": "The dog yelps and slinks away up the cliff, tail between its legs.", "location": "a2_harbour"},
}
ENCOUNTER_HOOKS = {
    "a2_dog_pier": dict(
        on_win=[dict(set="a2_dog_driven"), dict(journal="a2_j_dog_driven")],
        on_lose=[dict(say="The dog knocks me flat and is gone before I can rise; I am bruised, but unhurt."), dict(set="a2_dog_driven")],
        on_flee=[dict(say="I retreat from the pier. It does not follow.")],
    ),
}
JOURNAL["a2_j_dog_driven"] = dict(title="The dog", source=M, text="I faced the great dog under the pier, and it fled up the cliff toward the churchyard. A mastiff was found dead there the next morning, torn open, they say, by some savage thing.")

# --------------------------------------------------------------------------------------------------------------------
# new 3D assets (act_2_builders.py) + variants for existing models
# --------------------------------------------------------------------------------------------------------------------
ASSETS = [
    dict(id="a2_schooner", builder="a2_schooner", params={}),
    dict(id="a2_wheel", builder="a2_wheel", params={}),
]
VARIANTS = {
    "a2_schooner": {"default": "weathered", "weathered": {"wood": T("wood_planks", "#8a7458"), "cloth": T("cloth", "#cfc4a8"), "iron": T("iron")}},
    "a2_wheel": {"default": "oak", "oak": {"wood": T("wood_planks", "#7a6048"), "iron": T("iron")}},
    "human_peasant_m": {
        "a2_swales": human_colors(skin=T("skin", "#cfa383"), hair=T("hair", "#e0e0e0"), top=T("wool", "#3a4a5a"), bottom=T("wool", "#2a2e36")),
        "a2_captain": human_colors(skin=T("skin", "#d6c8b8"), hair=T("hair", "#6a5a48"), top=T("wool", "#27323f"), bottom=T("wool", "#1f242c")),
        "a2_coast": human_colors(skin=T("skin", "#d9b08c"), hair=T("hair", "#3a3a3a"), top=T("wool", "#1f2c44"), bottom=T("wool", "#1f2530")),
        "a2_fisher": human_colors(skin=T("skin", "#c7956e"), hair=T("hair", "#9a9a9a"), top=T("wool", "#4a5a3a"), bottom=T("wool", "#3a332a")),
        "a2_constable": human_colors(skin=T("skin", "#e0b896"), hair=T("hair", "#3a2a1a"), top=T("wool", "#1a2338"), bottom=T("wool", "#1a2338")),
        "a2_watchman": human_colors(skin=T("skin", "#d9b08c"), hair=T("hair", "#7a7a7a"), top=T("wool", "#3a3a3a"), bottom=T("wool", "#2c2c2c")),
        "a2_attendant": human_colors(skin=T("skin", "#e0b896"), hair=T("hair", "#3a2a1a"), top=T("cloth", "#e6e6e6"), bottom=T("cloth", "#d6d6d6")),
    },
    "human_peasant_f": {
        "a2_mrs_w": human_colors(skin=T("skin", "#f0cfb0"), hair=T("hair", "#b8b8b8"), top=T("cloth", "#6a6a74"), accent=T("cloth", "#e0e0e0")),
    },
}
