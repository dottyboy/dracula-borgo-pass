"""PERSONAL ARC - "The Last Voyage" (the Captain of the Demeter; book ch.7, the Log of the Demeter).
All ids are written with a leading '@' which is expanded to 'demeter_voyage_' at the bottom of the file.
Phases (flags p2..p6) advance only through the bunk in the cabin, the cast-off order, the night fight and the mate's end."""
from dsl import *


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


def J(title, text):
    return dict(title=title, source="Log of the Demeter", text=text)


CAP = "Captain"

ARC = dict(
    id="demeter_voyage", title="The Last Voyage", member="captain", portrait="captain",
    blurb="Varna to Whitby with fifty boxes of earth in the hold: the Captain of the Demeter keeps his log, counts his crew and loses them, one by one, to something that walks the deck at night.",
    unlock="", unlock_text="Finish the main story to read the Log of the Demeter in full.", after_credits=True,
    start=dict(location="@quay", protagonist="captain", party=["captain"], items={"silver": 2}, flags=[]),
    exit_to="ARC_END",
    rewards=[dict(give="captains_oilskin"), dict(give="@keepsake"), dict(give="garlic"), dict(give="garlic"), dict(give="holy_water"),
             dict(stat=dict(member="quincey", nerve=3, hp=2)), dict(stat=dict(member="arthur", nerve=2)),
             dict(set="@last_voyage_done")],
    rewards_text="The Captain's crucifix and rosary, 2 garlic, 1 holy water; +3 Nerve and +2 HP for Quincey, +2 Nerve for Arthur Gear: the Captain's oilskin.",
)

LOCATIONS = [
    dict(id="@quay", name="The quay, Varna", desc="The Black Sea port on a bright July morning. Gulls, tar, tarred rope, and a long line of Slovak carriers walking fifty boxes up a gangway as if they were carrying their own coffins.", date="6 July"),
    dict(id="@deck", name="Deck of the Demeter", desc="A Russian schooner of no great size, well found and well kept. The boards have been scrubbed white; by the end of the voyage no one will scrub them.", date="At sea"),
    dict(id="@cabin", name="The Captain's cabin", desc="A bunk, a chart table, a sea-chest and a lamp that swings. Home, for twenty years of voyages, and the only door on board that locks.", date="At sea"),
    dict(id="@hold", name="The hold", desc="Dark, close and smelling of damp earth and silver sand. Fifty boxes stand lashed in their rows, each the length of a coffin.", date="At sea"),
    dict(id="@galley", name="The galley", desc="A black stove, a rack of pans and the cook's whole kingdom in eight square feet. It is the one warm place aboard.", date="At sea"),
    dict(id="@forecastle", name="The forecastle", desc="Bunks in two tiers, sea-chests, damp oilskins, and holy pictures nailed over every pillow.", date="At sea"),
    dict(id="@bow", name="The bows", desc="The foredeck and the bowsprit, wet and narrow, with the anchor cable coiled like a sleeping snake. The fog begins here.", date="At sea"),
    dict(id="@wheelhouse", name="The wheel", desc="The quarterdeck, the binnacle, the barometer in its brass case, and the wheel itself with its worn spokes. A man could stand here forever.", date="At sea"),
]

LOC_DATA = {}

# ===================================================================================================== quay
LOC_DATA["@quay"] = dict(
    no_west_street=True, cells=[4, 3], interior=False, wall="cobble", floor="cobble", ambient=AMBIENT["day_exterior"], camera=cam([4, 3]), lights=lights_day(),
    spawn=[0.0, 3.8], spawns={"@deck": [-4.5, 2.5]},
    props=[
        prop("@q_ship", "@schooner", "weathered", -14.6, -1.0, rot=180, y=-1.35, scale=1.15, name="The Demeter", radius=2.0,
             look="Eighty tons of Russian oak, newly tarred. She looks small to be carrying fifty boxes and a secret.", go="@deck"),
        prop("@q_crates", "chest", "oak", 1.6, -3.4, scale=1.4, name="Stencilled crates", radius=0.8,
             look="Stencilled 'Hildesheim & Co., Varna'. Salt fish for Constantinople, they say; the smell is honest, at least."),
        prop("@q_barrel1", "barrel", "dark", 3.6, -3.4, name=None, radius=0.4),
        prop("@q_barrel2", "barrel", "oak", 4.4, -3.0, name=None, radius=0.4),
        prop("@q_bench", "bench", "oak", -1.2, -3.6, name="Quayside bench", radius=0.7,
             look="Worn by generations of seamen waiting for a wind."),
        prop("@q_sign", "signpost", "oak", 6.2, 3.2, name="Port signpost", radius=0.3,
             look="Constantinople, Odessa, Burgas, Varna. Not a word of Whitby, which is a very long way off."),
        prop("@q_lantern", "lantern", "default", -3.2, 3.4, name=None, radius=0.3),
        prop("@q_shrine", "crucifix_big", "silver", 6.4, -0.6, name="Quayside shrine", radius=0.4,
             look="A weathered wayside cross with a lamp. Sailors touch it going out and sometimes coming home."),
        prop("@q_fence", "fence", "default", -6.4, 1.2, name=None, radius=0.3),
        prop("@q_boxes", "chest", "ebony", -2.0, -0.4, scale=1.6, name="The last box on the quay", radius=0.9,
             look="Long, plain, nailed shut, with black earth in the cracks of the lid. Even the dockers walk round it."),
    ],
    npcs=[
        npc("@q_clerk", "human_peasant_m", "@clerk", 2.0, 0.4, name="Mr. Hildesheim's clerk", radius=0.5,
            look="Thin, inky and anxious to be elsewhere, holding the ship's papers like a man holding a hot coal.", talk="@clerk_talk"),
        npc("@q_customs", "human_peasant_m", "@customs", 5.2, 1.6, name="Customs officer", radius=0.5,
            look="A heavy man in a braided cap with one hand on the stamp and the other, discreetly, held out.", talk="@customs_talk"),
        npc("@q_widow", "human_peasant_f", "@widow", -4.0, 3.0, name="Candle-seller", radius=0.5,
            look="A widow in black with a tray of beeswax candles, selling them to sailors' wives and, today, to sailors.", talk="@widow_talk"),
        npc("@q_priest", "human_peasant_m", "@priest", 5.8, -1.8, name="Father Nikolai", radius=0.5,
            look="An old Orthodox priest in a rusty cassock, who has blessed ten thousand sailors and buried a good many.", talk="@priest_talk"),
        npc("@q_foreman", "human_peasant_m", "@foreman", -0.8, -2.0, name="Slovak foreman", radius=0.5,
            look="Broad, silent, with a rosary wound round his wrist. His men carried the boxes and wiped their hands afterwards.", talk="@foreman_talk"),
        npc("@q_mate", "human_captain", "@mate", 0.8, 2.4, name="Mr. Amramoff, first mate", radius=0.5,
            look="My first mate, a Roumanian, sturdy and short of temper. A good seaman and a bad listener.", talk="@mate_quay"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="@j_varna")])],
)

# ===================================================================================================== deck
LOC_DATA["@deck"] = dict(
    cells=[3, 2], interior=False, wall="planks", floor="planks", ambient=AMBIENT["sea_fog"], camera=cam([3, 2]), lights=lights_day(2.6),
    walls=dict(north=["wall_door_4", "wall_4", "wall_door_4"], east=["wall_door_4", "wall_4"]),
    spawn=[-4.4, 2.4], spawns={"@quay": [-4.4, 2.4], "@cabin": [4.6, -1.4], "@galley": [3.2, -2.4], "@forecastle": [-3.2, -2.4],
                               "@hold": [0.0, -0.2], "@bow": [-4.4, -1.0], "@wheelhouse": [3.6, 2.0]},
    props=[
        prop("@d_hull", "@deckshell", "weathered", 0.0, 0.0, rot=-90, y=-0.94, name=None, radius=0.0),
        prop("@d_mast1", "@mast", "weathered", -2.6, 0.2, name="Foremast", radius=0.3,
             look="Spruce, tarred, with the sail laced to it. Someone has nailed a small wooden cross to its foot."),
        prop("@d_mast2", "@mast", "weathered", 2.0, 0.2, scale=0.9, name=None, radius=0.3),
        prop("@d_hatch", "stairs", "planks", 0.0, -2.2, name="The hold hatch", radius=0.7,
             look="The main hatchway to the hold, battened and barred. A key hangs somewhere on this ship; a lever would do as well.",
             go="@hold", go_cond="has:@hold_key", go_fail="Barred and padlocked. The hold key is kept somewhere in the ship, not far from where I sleep."),
        prop("@d_locker", "chest", "dark", -4.4, -3.0, name="Deck locker", radius=0.6,
             look="Spare blocks, a marline-spike, tarred twine. Everything a ship needs and nothing a man needs."),
        prop("@d_capstan", "barrel", "oak", -1.0, 1.8, scale=0.9, name="Capstan", radius=0.4,
             look="The windlass capstan. Six men to the bars in a calm; I have fewer every week."),
        prop("@d_lantern", "lantern", "default", 2.8, 1.8, name="Deck lantern", radius=0.3,
             look="A stout lantern on the main-boom crutch. It burns all night now, and the men watch it as men watch a sleeping beast."),
        prop("@d_sky", "moon", "default", -1.2, -6.0, y=7.0, scale=0.5, name="The sky", radius=0.4,
             look="Grey above, grey below.", set="@clue_sky",
             set_text="High in the north-west, long white mares'-tails are drawing across the sky, thin as combed hair. The swell has begun to run against the wind. That is weather coming, and not far off."),
        prop("@d_gang", "stairs", "planks", -5.2, 2.4, rot=90, name="Gangway", radius=0.8, look="Back to the quay.", go="@quay", cond="!@p2"),
        prop("@d_foredeck", "stairs", "planks", -5.2, -1.0, rot=90, name="Foredeck", radius=0.8, look="Forward to the bows, where the figure was seen.", go="@bow"),
        prop("@d_stern", "stairs", "planks", 4.0, 2.4, name="Steps to the quarterdeck", radius=0.8, look="Aft to the wheel.", go="@wheelhouse"),
        prop("@d_door_fore", "door", "dark", -4.0, -3.8, name="Forecastle hatch", radius=0.6, look="Down to the men's quarters.", go="@forecastle"),
        prop("@d_door_galley", "door", "dark", 4.0, -3.8, name="Galley door", radius=0.6, look="Warm air, onions and the smell of a stove.", go="@galley"),
        prop("@d_door_cabin", "door", "oak", 5.8, -2.0, rot=-90, name="Deck-house door", radius=0.6, look="The way to my cabin.", go="@cabin"),
        prop("@d_trace", "bench", "dark", 1.4, -3.2, name="Coil of cable", radius=0.5, cond="@p3",
             look="Wet cable, thick with weed. Nothing hides in it.", set="@s_deck", set_text="I search the deck from end to end with a lantern: coils, lockers, the boat. Nothing but wet planks and my own shadow."),
    ],
    npcs=[
        npc("@d_mate", "human_captain", "@mate", 1.0, 1.2, name="Mr. Amramoff, first mate", radius=0.5, cond="!@mate_gone",
            look="The mate paces the deck with a handspike. He sleeps less than I do, and speaks to no one but the weather.", talk="@mate_talk"),
        npc("@d_petrofsky", "human_peasant_m", "@petrofsky", -2.2, 2.4, name="Petrofsky", radius=0.5, cond="!@gone_petrofsky",
            look="A young hand with a quick laugh. The laugh has gone from him since Cape Matapan.", talk="@petrofsky_talk"),
        npc("@d_dmitri", "human_peasant_m", "@dmitri", 3.0, 0.4, name="Dmitri", radius=0.5, cond="!@gone_dmitri",
            look="The youngest hand, who crosses himself every time he passes the hatch.", talk="@dmitri_talk"),
        npc("@d_ivan", "human_peasant_m", "@ivan", 5.0, 1.8, name="Ivan", radius=0.5, cond="!@gone_ivan",
            look="Big, slow, steady at the wheel in any weather. He stands as though he were rooted to the planks.", talk="@ivan_talk"),
        npc("@d_olgaren", "human_peasant_m", "@olgaren", -3.4, 0.4, name="Olgaren", radius=0.5, cond="!@gone_olgaren",
            look="A Swede among Russians, grey before his time. He is the man who keeps his eyes lowered when the fog comes in.", talk="@olgaren_talk"),
    ],
    on_enter=[
        {"if": "@p6", "once": True, "do": [say("Two of us, the mate and I. The fog does not lift. The deck is clean; even the blood would be a comfort.")]},
        {"if": "@p5", "once": True, "do": [say("Three hands, the mate and I. They sleep on deck now, back to back, with lanterns.")]},
        {"if": "@p4", "once": True, "do": [say("The Bay of Biscay, and wild weather. A hand short, and it is the lost man's mess-kit they will not touch.")]},
        {"if": "@p3", "once": True, "do": [say("A hand short. The crew stand about in twos and threes, and fall quiet when I pass.")]},
        {"if": "@p2", "once": True, "do": [say("We are under way. A fresh east wind, and eight men and myself aboard.")]},
    ],
)

# ===================================================================================================== cabin
LOC_DATA["@cabin"] = dict(
    cells=[3, 2], interior=True, wall="planks", floor="planks", ambient=AMBIENT["cold_interior"], camera=cam([3, 2]),
    lights=lights_warm([3, 2], n=2, energy=1.9),
    walls=dict(north=["wall_4", "wall_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[4.6, -1.4], spawns={"@deck": [4.6, -1.4]},
    props=[
        prop("@c_door", "door", "dark", 5.8, -2.0, rot=-90, name="Cabin door", radius=0.6, look="Back to the deck.", go="@deck"),
        prop("@c_bunk", "bed_simple", "black", -4.5, -2.4, name="Captain's bunk", radius=0.8,
             look="A straw tick and a rough Russian blanket. I have slept here with the whole Black Sea going over my head."),
        prop("@c_turn", "bed_simple", "blue", -4.5, 0.6, name="The cot: turn in", radius=0.8,
             look="A canvas cot under the port, for the hours I may spare. When I lie down, the days go by.", talk="@bunk"),
        prop("@c_log", "table", "dark", -0.4, -2.2, name="Log-desk", radius=0.9,
             look="A slanted desk with the ship's log open, an inkwell and a steel pen. Every night I must write what I know.", talk="@logbook"),
        prop("@c_book", "book", "diary", -0.4, -2.2, y=0.8, name=None, radius=0.2),
        prop("@c_watch", "table", "oak", 2.4, -2.8, name="Watch-bill and crew roll", radius=0.8,
             look="A slate nailed to the bulkhead with the names of the crew in chalk, and a roll showing who may sleep and who may stand.", talk="@roster"),
        prop("@c_chest", "chest", "ebony", 3.0, 0.4, name="Sea-chest", radius=0.6,
             look="Oilskins, a pipe, my father's compass. Under the oilskins, wrapped in a handkerchief, a small silver cross.",
             take="crucifix", take_text="My own crucifix, which my mother gave me when I first went to sea. I put it in my pocket.", give_once=True),
        prop("@c_icon", "candelabra", "default", -2.4, -3.2, name="Icon-shelf and lamp", radius=0.4,
             look="A small icon of St. Nicholas with a red lamp. Beside it hangs a string of beads, black with handling.",
             take="@rosary", take_text="The beads that were my mother's. I take them down, and I wind them round my fingers.", give_once=True),
        prop("@c_desk2", "table", "pale", 3.2, -0.8, name="Chart table", radius=0.8,
             look="Charts of the Black Sea, the Aegean and the Channel, with the course ruled in pencil. The ruled line ends at Whitby."),
        prop("@c_lamp", "lantern", "default", 0.6, 0.6, name="Swinging lamp", radius=0.3, look="Swings on its gimbals and throws the shadows about. I have stopped looking at the corners."),
        prop("@c_shelf", "bookshelf", "oak", -3.0, -3.2, name="Book-shelf", radius=0.6,
             look="Bradshaw's is the wrong book for this ship; Lloyd's Register and a Russian Bible are the right ones."),
        prop("@c_brandy", "bottle", "amber", 1.8, 0.8, name="Brandy bottle", radius=0.3,
             look="A small bottle, kept for sickness and for the last night of a bad voyage.",
             take="brandy", take_text="I take the brandy. It will be wanted.", give_once=True),
        prop("@c_bottle", "bottle", "glass", -2.4, 0.4, name="Empty rum-bottle", radius=0.3,
             look="A strong, corked bottle. It would float, if sealed with wax, and carry a message farther than any man.",
             take="@bottle", take_text="I take the bottle and set it by the log.", give_once=True),
        prop("@s_cabin_p", "chest", "pale", -1.2, 0.8, name="Locker", radius=0.5, cond="@p3",
             look="A clean locker; clean, I think, because no one else would open it.", set="@s_cabin",
             set_text="I search my own cabin: the locker, the bunk, the chart-case, the dark under the cot. Nothing, only a bad smell of damp earth in the corner, a smell I carried down myself."),
    ],
    on_enter=[dict(once=True, do=[dict(journal="@j_cabin")])],
)

# ===================================================================================================== hold
LOC_DATA["@hold"] = dict(
    cells=[4, 2], interior=True, wall="stone_dark", floor="dirt", ambient=AMBIENT["crypt"], camera=cam([4, 2]),
    lights=lights_warm([4, 2], n=2, energy=1.4),
    walls=dict(north=["wall_4", "wall_4", "wall_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[6.6, -2.0], spawns={"@deck": [6.6, -2.0]},
    props=[
        prop("@h_ladder", "door", "dark", 7.8, -2.0, rot=-90, name="Ladder to the hatch", radius=0.6, look="Up to the deck and the air.", go="@deck"),
        prop("@h_row1", "chest", "oak", -6.0, -3.0, scale=1.7, name="Boxes, first row", radius=0.9,
             look="Ten boxes, each lashed with rope, each stencilled in Cyrillic: EARTH, WHITBY. They are heavier than they should be."),
        prop("@h_row2", "chest", "oak", -3.0, -3.0, scale=1.7, name="Boxes, second row", radius=0.9,
             look="Ten more. The lids have been nailed and then painted over, like something that is meant to stay closed."),
        prop("@h_row3", "chest", "dark", 0.0, -3.0, scale=1.7, name=None, radius=0.9),
        prop("@h_row4", "chest", "dark", 3.0, -3.0, scale=1.7, name=None, radius=0.9),
        prop("@h_row5", "chest", "oak", -4.5, 0.4, scale=1.7, name="Boxes, fifth row", radius=0.9,
             look="The last row. I count them with a lantern, finger by finger.", set="@hold_counted",
             set_text="I walk the length of the hold, finger on every lid. Fifty boxes, as the paper says, fifty exactly. And the ship rides lower than fifty boxes of clay would make her."),
        prop("@h_sand", "barrel", "dark", 2.6, 0.8, name="Silver sand", radius=0.5,
             look="Casks of sand, the other half of the cargo. Cheap, grey and honest; I check them last."),
        prop("@h_tools", "chest", "pale", 5.0, 0.4, name="Tool-chest", radius=0.5,
             look="The mate's tool-chest: hammer, chisel, screw-driver. He will have it open on the third of August."),
        prop("@h_lamp", "lantern", "default", 1.8, 2.4, name=None, radius=0.3),
        prop("@h_b13", "chest", "ebony", 4.0, -0.4, scale=1.7, name="Box thirteen, unsealed", radius=0.9, cond="!@p5",
             look="This one has no customs seal on the lid and its nails shine like new. Black dust lies fresh round the base.", set="@box13_noticed",
             set_text="Box thirteen. A lid with bright nails, no seal, and the earth round it fresh, as though the box has been stirred. I could swear it was not so at Varna."),
        prop("@h_b13s", "chest", "ebony", 4.0, -0.4, scale=1.7, name="Box thirteen, nailed shut", radius=0.9, cond="@p5&!@box_open",
             look="Nailed shut. A crowbar would take the lid off; I do not like what I think is underneath.",
             use_item={"@crowbar": [say("The nails scream out of the wood one by one. The lid comes up on black earth, damp and smelling of the grave. The mate was right about the boxes, and he is not here to know it."), {"set": "@box_open"}]},
             use_fail="Nailed shut. I need a lever: the carpenter's crowbar from the forecastle chest."),
        prop("@h_b13o", "chest", "ebony", 4.0, -0.4, scale=1.7, name="Box thirteen, opened", radius=0.9, cond="@box_open",
             look="Black earth to the brim and a hollow in it the shape of a man.", talk="@box_dialogue"),
        prop("@h_trail", "rock", "dark", 5.6, 2.0, name="Spilled earth", radius=0.4, cond="@p3",
             look="A smear of black earth on the boards.", set="@trail_hold",
             set_text="A trail of earth from the foot of box thirteen to the forward hatch, wider than a dog's, narrower than a man's; and across it, wet bare footprints, one long, one long. The prints end at the ladder. They do not come back."),
        prop("@s_hold_p", "barrel", "oak", -6.2, 2.4, name="Search: behind the casks", radius=0.4, cond="@p3",
             look="A narrow gap between the casks and the hull.", set="@s_hold",
             set_text="I search the hold with lantern and lead, as the book of Rules says. Behind every row, under every lashing, between every cask. There is not a corner for a man to hide in, only the boxes. I do not like how well I know that."),
    ],
    npcs=[
        npc("@h_dark_a", "bat", "black", -1.0, 1.4, name="The dark between the boxes", radius=0.8, cond="@p5night&@box_blessed&!won:@dark_blessed",
            look="Something moves among the lashings. It breathes like a man and it is not a man.", fight="@dark_blessed"),
        npc("@h_dark_b", "bat", "black", -1.0, 1.4, name="The dark between the boxes", radius=0.8, cond="@p5night&!@box_blessed&!won:@dark_burned",
            look="Something moves among the lashings. It breathes like a man and it is not a man.", fight="@dark_burned"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="@j_hold")])],
)

# ===================================================================================================== galley
LOC_DATA["@galley"] = dict(
    cells=[2, 2], interior=True, wall="plaster_dirty", floor="planks", ambient=AMBIENT["candle_interior"], camera=cam([2, 2]),
    lights=lights_warm([2, 2]),
    walls=dict(north=["wall_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[2.8, -2.0], spawns={"@deck": [2.8, -2.0]},
    props=[
        prop("@g_door", "door", "dark", 3.8, -2.0, rot=-90, name="Galley door", radius=0.6, look="Back on deck.", go="@deck"),
        prop("@g_stove", "fireplace", "soot", 0.0, -3.0, name="The stove", radius=0.9,
             look="The cook's iron stove, hot day and night. It is the one place the men will sit with their backs to the room."),
        prop("@g_table", "table", "oak", 0.4, 0.2, name="Mess table", radius=0.8,
             look="Eight places laid and, tonight, one fewer, because Petrofsky's bowl has not been moved."),
        prop("@g_garlic", "garlic", "default", -3.0, -2.0, y=1.2, name="String of garlic", radius=0.3,
             look="Garlic, hung from the beam like beads. The cook swears by it, against colds, quarrels and ghosts.",
             take="garlic", take_text="The cook shrugs. 'Take it, Captain. It's what's it's for.' I take one head, and then another.", give_once=True),
        prop("@g_garlic2", "garlic", "default", -2.4, -1.6, y=1.2, name=None, radius=0.2),
        prop("@g_oil", "bottle", "green", -2.8, 1.8, name="Oil flask", radius=0.3,
             look="Lamp-oil, for the binnacle and the galley lamp.", take="oil", take_text="I fill a small flask with lamp-oil from the drum.", give_once=True),
        prop("@g_hook", "key", "gold", 2.4, -2.8, name="Hook by the stove", radius=0.3,
             look="Spoons, ladles and a hook where keys are hung. Most of them are not keys."),
        prop("@g_barrel", "barrel", "oak", 2.4, 1.0, name="Water cask", radius=0.4,
             look="Sweet water, rationed. The cask has been drawn down by the thirst of people who do not want to leave the galley.",
             take="water", take_text="I fill a flask with water.", give_once=True),
        prop("@g_rack", "bookshelf", "pale", -3.0, 0.4, name="Pan-rack", radius=0.5,
             look="Pans, a ladle, and a sack of salt. The cook salts the doorstep when he thinks I am not looking.",
             take="knife", take_text="A sharp galley knife, good for fish, rope and worse. I take it.", give_once=True),
        prop("@g_bandage", "chest", "pale", 3.0, 1.4, name="Medicine box", radius=0.4,
             look="Plasters, a roll of lint, a bottle of laudanum. A ship's surgeon is a captain with a steady hand.",
             take="bandage", take_text="I take a roll of clean lint.", give_once=True),
        prop("@s_galley_p", "barrel", "dark", -3.2, 2.4, name="Search: stores", radius=0.4, cond="@p3",
             look="Flour and salt-beef.", set="@s_galley", set_text="Stores, flour-barrels, salt-beef casks; I tip the lids with the cook watching. No man. Only a rat which looks at me as if I were the stranger."),
    ],
    npcs=[
        npc("@g_cook", "human_peasant_m", "@cook", 1.4, 1.6, name="Stepan the cook", radius=0.5, cond="!@gone_stepan",
            look="Round, red-faced, a lifelong cook who has never in his life been afraid of a stove and has become afraid of everything else.", talk="@cook_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="@j_galley")])],
)

# ===================================================================================================== forecastle
LOC_DATA["@forecastle"] = dict(
    cells=[3, 2], interior=True, wall="planks", floor="planks", ambient=AMBIENT["candle_interior"], camera=cam([3, 2]),
    lights=lights_warm([3, 2], n=2, energy=1.5),
    walls=dict(north=["wall_4", "wall_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[4.6, -1.4], spawns={"@deck": [4.6, -1.4]},
    props=[
        prop("@f_door", "door", "dark", 5.8, -2.0, rot=-90, name="Ladder to the deck", radius=0.6, look="Up to the deck.", go="@deck"),
        prop("@f_bunk1", "bed_simple", "green", -4.6, -2.8, name="Petrofsky's bunk", radius=0.7,
             look="A blanket tucked tight, a pipe on the pillow, a St. Nicholas pinned above. He did not come to this bed on the night he was lost.", cond="@p3"),
        prop("@f_bunk1b", "bed_simple", "green", -4.6, -2.8, name="Petrofsky's bunk", radius=0.7,
             look="Petrofsky sleeps in the lower berth with his boots on. He says the floor has begun to feel cold.", cond="!@p3"),
        prop("@f_bunk2", "bed_simple", "black", -2.0, -3.0, name="Olgaren's bunk", radius=0.7,
             look="Tidy as a drawer. A Swedish psalm-book lies open at the 23rd."),
        prop("@f_bunk3", "bed_simple", "blue", 1.0, -3.0, name="Ivan's bunk", radius=0.7, look="A big man's bunk, short of a pillow."),
        prop("@f_bunk4", "bed_simple", "red", 3.5, -3.0, name=None, radius=0.7),
        prop("@f_chest", "chest", "dark", -3.4, 0.4, name="Carpenter's chest", radius=0.6,
             look="Chisels, adze, spikes and a heavy iron crowbar, kept sharp by a man who thought he was only a carpenter.",
             take="@crowbar", take_text="The carpenter's crowbar, two feet of black iron. It will lift a lid, or a lid's nails, or a man's courage.", give_once=True),
        prop("@f_torch", "stake", "default", -1.4, 1.6, name="Pitch torches", radius=0.3,
             look="A bundle of torches dipped in pitch, for the boat in a calm and the hold in a pinch.",
             take="torch", take_text="I take a torch. A lantern shows what is there; a torch shows what flees.", give_once=True),
        prop("@f_slate", "table", "pale", 0.4, 1.2, name="Mess table and slate", radius=0.8,
             look="A slate left on the mess table, scrawled with names in three hands, with a fourth line crossed out and written again.", talk="@robin_note"),
        prop("@f_lamp", "lantern", "default", 3.4, 1.4, name=None, radius=0.3),
        prop("@f_icons", "crucifix", "silver", 2.2, -3.4, name="Holy pictures", radius=0.3,
             look="Saints nailed over every bunk, St. Nicholas, the Mother of God, St. Elias, with a small iron cross at the foot of each."),
        prop("@s_fore_p", "barrel", "pale", 3.0, 2.2, name="Search: sea-bags", radius=0.4, cond="@p3",
             look="Sea-bags and oilskins.", set="@s_fore", set_text="Every bunk, every bag, every oilskin: I turn them all out under the lantern. Prayers, a wedding-ring, a Turkish coin. No man."),
    ],
    npcs=[
        npc("@f_abramoff", "human_peasant_m", "@abramoff", -0.6, -0.8, name="Abramoff", radius=0.5, cond="!@gone_abramoff",
            look="A seamed, dark, silent hand who has sailed with me nine years. Tonight he is mending a net with hands that do not look at it.", talk="@abramoff_talk"),
        npc("@f_bolotin", "human_peasant_m", "@bolotin", 2.2, 0.2, name="Bolotin, second mate", radius=0.5, cond="!@gone_bolotin",
            look="My second mate, a quiet, bookish man who steers by compass and prays by habit.", talk="@bolotin_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="@j_fore")])],
)

# ===================================================================================================== bow
LOC_DATA["@bow"] = dict(
    cells=[2, 2], interior=False, wall="planks", floor="planks", ambient=AMBIENT["sea_fog"], camera=cam([2, 2]), lights=lights_day(2.0),
    spawn=[2.4, 1.8], spawns={"@deck": [2.4, 1.8]},
    props=[
        prop("@b_hull", "@deckshell", "weathered", 0.0, 0.0, rot=180, y=-0.94, name=None, radius=0.0),
        prop("@b_stairs", "stairs", "planks", 2.8, 2.0, rot=-90, name="Aft to the deck", radius=0.8, look="Back along the deck.", go="@deck"),
        prop("@b_cable", "barrel", "dark", -1.0, -2.0, scale=1.1, name="Anchor cable", radius=0.6,
             look="Coiled cable, stiff with salt. A man could lose a hand in it, or find one lost.",
             take="rope", take_text="I cut a length of good manila from the bitter end. A fathom, no more, and it is enough to hold a man to a wheel.", give_once=True),
        prop("@b_bowsprit", "column", "planks", 0.0, -2.8, rot=0, name="Bowsprit", radius=0.3,
             look="The bowsprit points at nothing. The fog begins at its tip."),
        prop("@b_lamp", "lantern", "default", 1.8, -1.6, name="Bow light", radius=0.3, look="The red and green lights burn dull in the fog. A passing ship would see them. None passes."),
        prop("@b_cap", "key", "gold", -0.6, 0.8, name="A sailor's cap", radius=0.25, cond="@p3",
             look="Lying wet against the rail, a blue knitted cap with a name sewn in the band: PETROFSKY.", take="@cap",
             take_text="Petrofsky's cap. I fold it in my pocket for the day his mother asks me what became of him.", give_once=True),
        prop("@b_trail", "rock", "dark", -1.6, -1.4, name="Damp earth", radius=0.4, cond="@p3",
             look="A smear of black earth on the planks.", set="@trail_bow",
             set_text="Earth, damp and black, scuffed across the planks right to the stem-head. It is the same earth as the hold. The man who left it came out of the hatch and walked forward, and has not come back."),
        prop("@s_bow_p", "chest", "pale", 2.0, -2.4, name="Search: chain locker", radius=0.5, cond="@p3",
             look="The chain-locker.", set="@s_bow", set_text="The chain-locker, the sail-bin, the dark under the windlass. Nobody, nothing. I find only the wet and a new smell on the wind that is neither tar nor salt."),
    ],
    npcs=[
        npc("@b_figure", "human_dracula", "count", -0.8, -3.0, name="A tall, thin man", radius=0.6, cond="@p6&!@mate_gone",
            look="Tall, thin, white as paper, standing quite still at the stem-head and looking out at the fog. Looking at me, now."),
    ],
    on_enter=[dict(once=True, do=[dict(journal="@j_bow")])],
)

# ===================================================================================================== wheelhouse
LOC_DATA["@wheelhouse"] = dict(
    cells=[2, 2], interior=False, wall="planks", floor="planks", ambient=AMBIENT["sea_fog"], camera=cam([2, 2]), lights=lights_day(2.2),
    spawn=[-2.4, 1.6], spawns={"@deck": [-2.4, 1.6]},
    props=[
        prop("@w_hull", "@deckshell", "weathered", -6.5, 0.0, rot=-90, y=-0.94, name=None, radius=0.0),
        prop("@w_stairs", "stairs", "planks", -2.8, 2.0, rot=90, name="Forward to the deck", radius=0.8, look="Back down the steps.", go="@deck"),
        prop("@w_wheel", "@wheel", "oak", 0.0, 0.0, name="The ship's wheel", radius=0.6,
             look="Worn smooth by twenty years of hands. The spokes are the length of a man's reach.", talk="@lash"),
        prop("@w_glass", "mirror", "default", 2.4, -2.6, name="The barometer", radius=0.3,
             look="A brass barometer in a mahogany case. The needle has been drifting down all morning.", set="@clue_glass",
             set_text="I tap the glass. The needle trembles and drops another tenth since the forenoon watch. A steady, long fall: weather from the west is coming, and not tonight."),
        prop("@w_compass", "bust", "plaster", -1.2, -2.6, scale=0.6, name="Binnacle", radius=0.3, look="The compass card, steady as a priest. For now the ship points where I tell her."),
        prop("@w_plan", "table", "dark", 2.6, 0.6, scale=0.8, name="Sail-plan board", radius=0.6,
             look="A chalk-board for the sail-plan. The mate and I argue over it. Today it is mine to settle.", talk="@weather"),
        prop("@w_lantern", "lantern", "default", -2.4, -0.4, name=None, radius=0.3),
        prop("@w_flags", "signpost", "oak", 3.2, -1.2, name="Signal locker", radius=0.3, look="Flags, a bell and a lamp. They would be a great help if there were anyone to signal."),
    ],
    npcs=[
        npc("@w_bolotin", "human_peasant_m", "@bolotin", 1.4, 1.8, name="Bolotin at the helm", radius=0.5, cond="@p4&!@gone_bolotin",
            look="He has offered to steer and watch, and keep the sail trimmed. Those are not a man's whole duties but he has taken them.", talk="@bolotin_talk"),
    ],
    on_enter=[
        {"if": "@p6", "once": True, "do": [say("The wheel stands alone. The helmsman is gone, and the spokes are still warm.")]},
        dict(once=True, do=[dict(journal="@j_wheel")]),
    ],
)

# ===================================================================================================== dialogue
DIALOGUE = {}

# ---- quay
DIALOGUE["@clerk_talk"] = D("n0",
    n0=N("Clerk", "Captain! The bill of lading, signed and sealed as Herr Hildesheim promised. Fifty boxes, silver sand and earth, consigned to Mr. S. F. Billington of Whitby. A very odd cargo for July, but the freight is paid in full.",
         choices=[C("[Take the bill of lading]", "n1", cond="!@got_manifest", do=[{"give": "@manifest"}, {"set": "@got_manifest"}, {"journal": "@j_cargo"}]),
                  C("Who orders earth by the shipload?", "n_who"), C("Why Whitby?", "n_why"), C("[Leave]", end=True)]),
    n1=N("Clerk", "Take care of it, Captain. The customs officer will want to see it, and the officer is not a man who forgets. Nor does he stamp for nothing.", next="n0"),
    n_who=N("Clerk", "A foreign nobleman, Captain. He did not come himself. Everything was by letter and by agents, and the earth came down from the mountains on Szgany carts. He paid in gold. I did not ask questions.", next="n0"),
    n_why=N("Clerk", "A quiet harbour, little watched, with deep water by the pier. That is what the gentleman's letter said. I thought it a strange thing for a gentleman to know.", next="n0"))

DIALOGUE["@customs_talk"] = D("n0",
    n0=N("Customs officer", "Papers.",
         choices=[C("[Show the bill of lading]", "n1", cond="has:@manifest&!@cleared"),
                  C("[Ask about the stamp]", "n_hint", cond="!@cleared"), C("[Leave]", end=True)]),
    n1=N("Customs officer", "Fifty boxes of earth. Irregular. Extremely irregular. For a small consideration, however, a ship may be regular in everything.",
         choices=[C("[Pay the backsheesh: one silver coin]", "n2", cond="has:silver", do=[{"take": "silver"}, {"give": "@clearance"}, {"set": "@cleared"}, {"journal": "@j_cleared"}]),
                  C("[Refuse]", end=True)]),
    n2=N("Customs officer", "Everything is in order, Captain. A good voyage. I shall never see that ship again, I think, and I do not mind it.", end=True),
    n_hint=N("Customs officer", "A stamp costs silver, Captain. The paper first; the coin second. That is how the law is read in Varna.", next="n0"))

DIALOGUE["@widow_talk"] = D("n0",
    n0=N("Candle-seller", "A beeswax candle for the icon, Captain? One silver. It has been blessed in St. Constantine's and will burn all night, whatever the wind does.",
         choices=[C("[Buy a candle: one silver coin]", "n1", cond="has:silver&!@bought_candle", do=[{"take": "silver"}, {"give": "@candle"}, {"set": "@bought_candle"}]),
                  C("What do the sailors say about this ship?", "n_say"), C("[Leave]", end=True)]),
    n1=N("Candle-seller", "Light it before the icon on the quay. Father Nikolai will say the words. A ship that has not been blessed is a ship with no mother.", next="n0"),
    n_say=N("Candle-seller", "That the Slovaks who loaded her would not look at the boxes. That they crossed themselves each time they put one down. That the last one was warm.", next="n0"))

DIALOGUE["@priest_talk"] = D("n0",
    n0=N("Father Nikolai", "A ship may sail without a blessing, my son. Sailors may not.",
         choices=[C("[Light the candle before the icon]", "n1", cond="has:@candle&!@blessed", do=[{"take": "@candle"}, {"give": "holy_water"}, {"set": "@blessed"}, {"journal": "@j_blessed"}]),
                  C("What is in the boxes, Father?", "n_q"), C("[Leave]", end=True)]),
    n1=N("Father Nikolai", "Lord, who rebuked the winds and the sea, keep this ship and every soul aboard her. Here is water from the font, Captain; use it where you must. And keep a cross about you. A cross is better than a pilot.", next="n0"),
    n_q=N("Father Nikolai", "I do not know. I know that the Szgany kissed the ground before they would touch them, and I know that the earth has a smell I have smelled once before, in a vault where a man was buried who should not have been.", next="n0"))

DIALOGUE["@foreman_talk"] = D("n0",
    n0=N("Slovak foreman", "Fifty. Not one more, not one fewer. We counted them twice.",
         choices=[C("Who carried them to the quay?", "n1"), C("Was anything wrong with them?", "n2"), C("[Leave]", end=True)]),
    n1=N("Slovak foreman", "Szgany. They came down in the night, with their carts and their dogs, and they would not take payment from us. They took it from the clerk and rode away.", next="n0"),
    n2=N("Slovak foreman", "The last box was warm, Captain. In July that is nothing. But it was warm through the night, and not from the sun.", next="n0"))

DIALOGUE["@mate_quay"] = D("n0",
    n0=N("Amramoff", "Captain. The ship is stowed. The tide is turning. If you want to sail, we can sail.",
         choices=[C("[Give the order to cast off]", "n_go", cond="@cleared&@blessed&@got_manifest&!@p2"),
                  C("[Tell me what is still needed]", "n_hint", cond="!@p2"), C("About the hold key...", "n_key"), C("[Leave]", end=True)]),
    n_go=N("Amramoff", "At noon, then. East wind, fresh. She will go like a bird.",
           do=[{"set": "@p2"}, {"journal": "@j_sail"},
               {"card": "6 July. Varna. At noon the Demeter set sail, east wind, fresh. Crew: five hands, two mates, the cook, and myself, the captain. Cargo: silver sand and fifty boxes of earth, for Whitby."},
               {"goto": "@deck"}], end=True),
    n_hint=N("Amramoff", "The papers must be stamped by the customs officer, and the men will not cast off without a priest's blessing. They are Russians, Captain. You know what that is.", next="n0"),
    n_key=N("Amramoff", "I locked the hold when the boxes were stowed. The key I hung where a captain keeps keys: near where he sleeps, or where the cook keeps his spoons, or in the locker where we keep our tools. If it is not there, the carpenter's crowbar will do the same work.", next="n0"))

# ---- deck / crew
DIALOGUE["@mate_talk"] = D("n0",
    n0=N("Amramoff", "Captain. What are your orders?",
         choices=[C("How are the men?", "n_men"),
                  C("I want the whole ship searched.", "n_search", cond="@p3&!@mate_scoffed", do=[{"set": "@mate_scoffed"}]),
                  C("The men want a double watch. I mean to grant it.", "n_watch", cond="@p4&!@clue_pair_mc", do=[{"set": "@clue_pair_mc"}]),
                  C("Do you believe there is a man aboard?", "n_man", cond="@p5"),
                  C("[It is here, I know it now...]", "n_mad", cond="@p6&!@mate_gone"),
                  C("[Leave]", end=True)]),
    n_men=N("Amramoff", "Frightened women, Captain. A handspike will cure it. A man who is afraid of a deck-house is a man who needs more work.", next="n0"),
    n_search=N("Amramoff", "A fool's errand. Sixty feet of boxes, and no man can hide in a box. I shall take the helm, and let the men search. But it is folly, and it will demoralise them.", next="n0"),
    n_watch=N("Amramoff", "Then give me the dark watch, Captain. The men will not stand with me, and I will not stand with them. I will stand with you, with a handspike and a lantern, and between us we shall keep the middle watch.", next="n0"),
    n_man=N("Amramoff", "There is no man aboard. There is what comes of men who sleep too little and think too much. I will find the cause. I shall find it if I have to open every box.", next="n0"),
    n_mad=N("Amramoff", "It is here. I know it now. On the watch last night I saw It, like a man, tall and thin and ghastly pale. It was in the bows, looking out. I crept behind It and gave It my knife, but the knife went through It, empty as the air.",
            choices=[C("Mr. Amramoff, go to your bunk.", "n_mad2"), C("What will you do?", "n_mad2")]),
    n_mad2=N("Amramoff", "It is in the hold, perhaps in one of those boxes. I shall unscrew them one by one and see. You work the helm.",
             do=[{"set": "@mate_below"}, {"say": "He takes the tool-chest and a lantern and goes down the forward hatchway. I cannot leave the wheel. I hear him knocking in the hold, patient as a carpenter."}], next="n_mad3"),
    n_mad3=N("Narrator", "Then a sudden startled scream, and he comes up the hatchway as though shot from a gun, with his eyes rolling and his face convulsed with fear. 'Save me! Save me!' He looks round on the fog, and his horror turns to despair.",
             next="n_mad4"),
    n_mad4=N("Amramoff", "You had better come too, Captain, before it is too late. He is there. I know the secret now. The sea will save me from Him, and it is all that is left!",
             do=[{"set": "@mate_gone"}, {"journal": "@j_mate"},
                 {"card": "3 August. He sprang on the bulwark and threw himself into the sea. I suppose I know the secret too, now. Lord, help me. How am I to account for all these horrors when I get to port? When I get to port! Will that ever be?"}],
             end=True))

DIALOGUE["@petrofsky_talk"] = D("n0",
    n0=N("Petrofsky", "Captain. Good watch.",
         choices=[C("You look tired, Petrofsky.", "n1"), C("Anything strange on your watch?", "n2"), C("[Leave]", end=True)]),
    n1=N("Petrofsky", "I sleep with my boots on, Captain. The floor has begun to feel cold. Cold the way a cellar is cold, not a sea.", next="n0"),
    n2=N("Petrofsky", "No. Nothing. Only that I take the larboard watch tonight, and Abramoff relieves me at eight bells, and I would rather he came early.", next="n0"))

DIALOGUE["@dmitri_talk"] = D("n0",
    n0=N("Dmitri", "Captain. It is cold on deck.",
         choices=[C("What are the men saying?", "n1"), C("[Leave]", end=True)]),
    n1=N("Dmitri", "That Petrofsky did not drown. A man who drowns makes a noise. They say he walked forward and the fog took him. Do not laugh, Captain. I will go and stand by the lantern.", next="n0"))

DIALOGUE["@ivan_talk"] = D("n0",
    n0=N("Ivan", "At the wheel, Captain. Steady as a rock.",
         choices=[C("Would you stand a watch alone?", "n1", cond="@p4"), C("[Leave]", end=True)]),
    n1=N("Ivan", "No. Not alone, Captain. If I stand it, Bolotin stands it with me. He is my kinsman, my mother's cousin's boy. He does not leave my side, and I do not leave his.", do=[{"set": "@clue_pair_ib"}], next="n0"))

DIALOGUE["@olgaren_talk"] = D("n0",
    n0=N("Olgaren", "Captain.",
         choices=[C("Something is on your mind, Olgaren.", "n_tale", cond="@p3&!@olg_tale"),
                  C("You are afraid of something.", "n_fear", cond="!@p3"), C("[Leave]", end=True)]),
    n_fear=N("Olgaren", "No, Captain. A little uneasy. I will tell you more tomorrow.", next="n0"),
    n_tale=N("Olgaren", "In my watch, Captain, I was sheltering behind the deck-house from the rain, when I saw a tall, thin man come up the companion-way, who was not like any of the crew. He walked forward along the deck and disappeared. I followed softly, but when I got to the bows, there was no one, and the hatchways were all closed.",
             do=[{"set": "@olg_tale"}, {"journal": "@j_olgaren"}], next="n0"))

# ---- galley / forecastle
DIALOGUE["@cook_talk"] = D("n0",
    n0=N("Stepan", "Captain. Soup in a quarter-hour. It will be hot, whatever else is not.",
         choices=[C("Have you any garlic?", "n_garlic", cond="!@got_garlic"),
                  C("The gulls and the weather...", "n_gulls", cond="!@clue_gulls"),
                  C("What do you make of all this?", "n_mood"), C("[Leave]", end=True)]),
    n_garlic=N("Stepan", "Garlic? There is a string over the stove. My grandmother hung it over the cradle, against what, she never said. Take it. A man should have something in his pockets besides his hands.", do=[{"set": "@got_garlic"}], next="n0"),
    n_gulls=N("Stepan", "The gulls have all gone inland, Captain, and the porpoises are running to the west. A cook knows when to put the fire out. Weather, and soon, from the south-west. I have not seen it so since Odessa.",
              do=[{"set": "@clue_gulls"}, {"say": "I note it. Gulls inland, the cook's weather-sense, and I have the sky and the glass besides."}], next="n0"),
    n_mood=N("Stepan", "They say there is a stranger aboard, Captain. I say there are fifty strangers aboard and I have been feeding them for a week. Fifty boxes. A man who eats little and sleeps all day. That is no stranger. That is a passenger.", next="n0"))

DIALOGUE["@abramoff_talk"] = D("n0",
    n0=N("Abramoff", "Captain. Mending.",
         choices=[C("Who stands which watch?", "n_watch", cond="@p4&!@clue_pair_oa"),
                  C("You relieved Petrofsky that night.", "n_pet", cond="@p3"), C("[Leave]", end=True)]),
    n_watch=N("Abramoff", "Olgaren and I sail together, Captain, or we do not sail at all. He is my friend. If he goes on deck alone, I go; if I go alone, he goes. That is understood in the forecastle.",
              do=[{"set": "@clue_pair_oa"}], next="n0"),
    n_pet=N("Abramoff", "At eight bells, as arranged. I came up and found the deck empty and the lantern burning. I looked in the bows. I did not look in the hold.", next="n0"))

DIALOGUE["@bolotin_talk"] = D("n0",
    n0=N("Bolotin", "Captain. The wheel is steady.",
         choices=[C("Will you take a watch with Ivan?", "n_ivan", cond="@p4&!@clue_pair_ib", do=[{"set": "@clue_pair_ib"}]),
                  C("[Leave]", end=True)]),
    n_ivan=N("Bolotin", "With Ivan? Gladly. He is my kinsman; I would stand with him on a burning ship. I will steer and watch, sir, if you let me. Let the others sleep.", next="n0"))

DIALOGUE["@robin_note"] = D("n0",
    n0=N("Slate", "In three different hands the men have chalked: 'We ask for double watch. We do not go on deck alone. Not one of us.' Under it, in a fourth, a note: 'Not with the mate.'",
         choices=[C("[Take the round robin]", "n1", cond="!@rr_taken", do=[{"give": "@robin"}, {"set": "@rr_taken"}, {"set": "@rr_read"}]),
                  C("[Leave it]", end=True)]),
    n1=N("Captain", "A round robin, in the sailors' way: names in a ring, so that no one signs first. I will keep it, and I will grant what it asks. Double watches. It is the least I can do.", end=True))

# ---- weather and roster puzzles
DIALOGUE["@weather"] = D("n0",
    n0=N(CAP, "The sail-plan. What do I know about the weather, and what will I do about it?",
         choices=[C("[Think over what I know]", "n_know"),
                  C("Carry all sail: the sky is clear and the wind is fair.", "n_wrong1"),
                  C("Take in sail: weather from the south-west by morning.", "n_right", cond="@clue_glass&@clue_sky&@clue_gulls"),
                  C("Run for the nearest port.", "n_wrong2"), C("[Leave]", end=True)]),
    n_know=N(CAP, "Let me count the signs. The glass: ", next="n_know2"),
    n_know2=N(CAP, "falling long and slow, if I have read it (the barometer by the wheel). The sky: mares'-tails from the north-west, if I have looked at it (from the deck). The birds and fish: the cook's own word (galley). Three signs; they must agree.", next="n0"),
    n_wrong1=N(CAP, "No. I do not trust a clear sky with a falling glass. Let me think again.", next="n0"),
    n_wrong2=N(CAP, "A harbour in this wind is a reef with a name. We hold our course; we only shorten sail.", next="n0"),
    n_right=N(CAP, "Glass falling, mares'-tails to the north-west, gulls inland, porpoises running west. That is a south-westerly gale before the next forenoon. We reef down, secure the boats, and get everything lashed. I give the orders.",
              do=[{"set": "@weather_read"}, {"journal": "@j_weather"}], end=True))

DIALOGUE["@roster"] = D("n0",
    n0=N(CAP, "The watch bill. Three watches, three pairs, and no man alone. I must match them by what the men have told me.",
         choices=[C("[Set the watch bill]", "r1", cond="@clue_pair_oa&@clue_pair_ib&@clue_pair_mc&@rr_read&!@roster_set"),
                  C("[What do I know?]", "n_know", cond="!@roster_set"),
                  C("[The watch is set]", "n_done", cond="@roster_set"), C("[Leave]", end=True)]),
    n_know=N(CAP, "Abramoff says Olgaren stands only with him. Ivan and Bolotin are kin and will not be parted. The mate says the men won't stand with him and he will stand the dark watch with me. And the round robin: nobody alone. I need to hear all of it first.", next="n0"),
    n_done=N(CAP, "The bill is chalked up: First watch, Ivan and Bolotin. Middle watch, the mate and myself, armed. Morning watch, Olgaren and Abramoff.", next="n0"),
    r1=N(CAP, "The first watch, eight bells to midnight. Who?",
         choices=[C("Ivan and Bolotin (kin, they won't be parted).", "r2"), C("Olgaren and the mate.", "w1"), C("Stepan the cook, alone, by the stove.", "w2")]),
    w1=N(CAP, "No. The men have said they will not stand with the mate. It would be better to have no watch at all.", next="r1"),
    w2=N(CAP, "Alone? The round robin says not one man alone. No.", next="r1"),
    r2=N(CAP, "The middle watch, midnight to four, the darkest. Who?",
         choices=[C("The mate and myself, armed.", "r3"), C("Olgaren and Ivan.", "w3"), C("Abramoff and Olgaren.", "w4")]),
    w3=N(CAP, "No. Ivan is already on the first watch with Bolotin and Olgaren will only stand with Abramoff.", next="r2"),
    w4=N(CAP, "No. They belong on the morning watch, a pair for the grey hours, and the middle watch needs the strongest.", next="r2"),
    r3=N(CAP, "The morning watch, four to eight. And the last pair?",
         choices=[C("Olgaren and Abramoff.", "r4"), C("Bolotin and the mate.", "w5"), C("The cook, alone.", "w6")]),
    w5=N(CAP, "No. Bolotin is on the first watch with Ivan, and the mate is with me.", next="r3"),
    w6=N(CAP, "No, no one alone.", next="r3"),
    r4=N(CAP, "There. A ship has never been better watched, and there is not a single man alone. If anything can be done by arithmetic, I have done it.",
         do=[{"set": "@roster_set"}, {"journal": "@j_roster"}], end=True))

# ---- the log (puzzle: write what is true)
DIALOGUE["@logbook"] = D("n0",
    n0=N(CAP, "The ship's log lies open. A log is not a diary; it must say only what is true, in the right order, in a steady hand.",
         choices=[C("[Entry: cargo, and the weather]", "l1", cond="@p2&@weather_read&!@log1"),
                  C("[Entry: the search of the ship]", "l2", cond="@p3&@s_hold&@s_fore&@s_galley&@s_cabin&@s_bow&@trail_hold&@trail_bow&!@log2"),
                  C("[Entry: the men lost]", "l3", cond="@p4&!@log3"),
                  C("[Final entry]", "l4", cond="@mate_gone&!@log4&has:@bottle"),
                  C("[Read the log]", "n_read"), C("[Leave]", end=True)]),
    n_read=N(CAP, "I read the log back. It is short and honest, and every line of it frightens me more than the one before.", next="n0"),
    l1=N(CAP, "What do I write of the cargo?",
         choices=[C("Fifty boxes of Carpathian clay for Hamburg.", "w_l1a"),
                  C("Silver sand and fifty boxes of earth, consigned to Mr. Billington, Whitby; customs stamped, Varna.", "l1b", cond="has:@manifest&has:@clearance"),
                  C("No cargo worth the ink.", "w_l1c")]),
    w_l1a=N(CAP, "That is not what the bill of lading says. A log that lies is not a log. I strike it out.", next="l1"),
    w_l1c=N(CAP, "The cargo is the whole point of the voyage. I strike it out.", next="l1"),
    l1b=N(CAP, "And the weather I have read?",
          choices=[C("Fair and settled.", "w_l1d"), C("Glass falling, mares'-tails NW, weather from SW by morning; reefed down.", "l1e")]),
    w_l1d=N(CAP, "No. I did not read it so, and I will not write it.", next="l1b"),
    l1e=N(CAP, "Written, and signed, and sanded. The cargo and the weather.", do=[{"set": "@log1"}, {"journal": "@j_log1"}], end=True),
    l2=N(CAP, "What did the search find?",
         choices=[C("Searched stem to stern, found nothing at all; crew's fears are folly.", "w_l2a"),
                  C("Searched stem to stern with lanterns: no man; but earth spilled from box thirteen to the bows, and Petrofsky's cap.", "l2b"),
                  C("Found a stowaway and put him in irons.", "w_l2c")]),
    w_l2a=N(CAP, "That is what the mate would write. It is not what I found.", next="l2"),
    w_l2c=N(CAP, "There is no stowaway in irons. I would have remembered.", next="l2"),
    l2b=N(CAP, "A strange entry, but a true one.", do=[{"set": "@log2"}, {"journal": "@j_log2"}], end=True),
    l3=N(CAP, "How many men have I lost since Varna?",
         choices=[C("Three: Petrofsky, Dmitri and the second mate.", "w_l3a"), C("Two: Petrofsky and Dmitri.", "l3b"), C("None; they have deserted.", "w_l3c")]),
    w_l3a=N(CAP, "Bolotin is alive; I saw him at the wheel. Let me count again.", next="l3"),
    w_l3c=N(CAP, "A man does not desert a ship in the middle of the Atlantic. No.", next="l3"),
    l3b=N(CAP, "Two men. Both off watch, neither seen again. I write it exactly so.", do=[{"set": "@log3"}, {"journal": "@j_log3"}], end=True),
    l4=N(CAP, "The final entry. What do I tell the people who find this bottle?",
         choices=[C("The mate murdered the crew and then himself.", "w_l4a"),
                  C("The mate saw It: tall, thin, pale. The knife went through It. He leapt overboard. I know the secret now, and I will lash my hands to the wheel with the cross.", "l4b"),
                  C("Pirates.", "w_l4c")]),
    w_l4a=N(CAP, "No. That is what the inquest will say, and it would be convenient. It is not what I saw.", next="l4"),
    w_l4c=N(CAP, "I will not make up a pirate for the Board of Trade.", next="l4"),
    l4b=N(CAP, "I write it as steadily as I can, and I seal it in the bottle with wax from the lamp, so that those who find it may understand. If not, all men shall know that I was true to my trust.",
          do=[{"take": "@bottle"}, {"give": "@bottle_log"}, {"set": "@log4"}, {"journal": "@j_log4"}], end=True))

# ---- turning in: the days pass
DIALOGUE["@bunk"] = D("n0",
    n0=N(CAP, "A few hours of sleep, if the ship allows it. But every night that I lie down, the ship is a man short in the morning.",
         choices=[
             C("[Turn in: the Archipelago, Matapan, the 16th of July]", do=[
                 {"set": "@p3"}, {"set": "@gone_petrofsky"}, {"journal": "@j_petrofsky"},
                 {"card": "16 July. The mate reported in the morning that one of the crew, Petrofsky, was missing. He took the larboard watch at eight bells, was relieved by Abramoff, and never reached his bunk. The men are more downcast than ever."},
                 {"goto": "@deck"}], cond="@p2&!@p3&@weather_read&@hold_counted&@log1", end=True),
             C("[Turn in: Gibraltar and the Bay of Biscay, 24 July]", do=[
                 {"set": "@p4"}, {"set": "@gone_dmitri"}, {"journal": "@j_dmitri"},
                 {"card": "24 July. There seems some doom over this ship. Already a hand short, and entering the Bay of Biscay with wild weather ahead, and last night another man lost. Like the first, he came off his watch and was not seen again."},
                 {"goto": "@deck"}], cond="@p3&!@p4&@s_deck&@s_hold&@s_fore&@s_galley&@s_cabin&@s_bow&@trail_hold&@trail_bow&@log2", end=True),
             C("[Turn in: the storm, 29 and 30 July]", do=[
                 {"set": "@p5"}, {"set": "@gone_bolotin"}, {"set": "@gone_abramoff"}, {"set": "@gone_ivan"}, {"journal": "@j_storm"},
                 {"card": "29 July. Another tragedy. The morning watch found no one but the steersman; the second mate is gone. 30 July. Last night, both the man of the watch and the steersman missing. Only myself, the mate, and two hands left to work the ship."},
                 {"goto": "@deck"}], cond="@p4&!@p5&@roster_set&@log3&@got_garlic", end=True),
             C("[Turn in: the Channel, 2 August, midnight]", do=[
                 {"set": "@p5night"}, {"journal": "@j_cry"},
                 {"card": "2 August, midnight. Woke up from a few minutes' sleep by hearing a cry, seemingly outside my port. Nothing in the fog. I ran on deck and into the mate; he heard the cry too. The hold hatch is open, and from the hold comes the sound of the boxes moving."},
                 {"goto": "@hold"}], cond="@p5&!@p5night&@box_dealt", end=True),
             C("[What is left to do before I can rest?]", "n_hint"),
             C("[Not yet]", end=True)]),
    n_hint=N(CAP, "Let me count what is wanted.", next="n_h2"),
    n_h2=N(CAP, "In general: read the weather, count the hold, write the log (July 6th to 16th); search every corner and find the trail (17th); set the watch and gather garlic (22nd to 29th); open the box and deal with it (2 August).", next="n0"))

# ---- the hold: box 13
DIALOGUE["@box_dialogue"] = D("n0",
    n0=N(CAP, "Black earth, damp, the shape of a man pressed into it. There is a smell I knew in a vault, once. This is where It lies by day. What shall I do?",
         choices=[C("[Pour the holy water into the earth]", "n_hw", cond="has:holy_water&!@box_blessed", do=[{"take": "holy_water"}]),
                  C("[Pour out the oil and set a torch to it]", "n_burn", cond="has:oil&has:torch&!@box_burned", do=[{"take": "oil"}, {"take": "torch"}]),
                  C("[Close the lid again]", end=True)]),
    n_hw=N(CAP, "The water hisses where it touches the earth, like water on a hot stove. The black soil blisters and goes grey; the smell changes from the grave to something that is only a smell. Whatever lay here has lost its bed.",
           do=[{"set": "@box_blessed"}, {"set": "@box_dealt"}, {"journal": "@j_box"}], end=True),
    n_burn=N(CAP, "The oil takes, and the torch with it. The flame is low, blue at the heart and does not like the earth. Smoke rolls along the hold. The box burns badly and the others do not burn at all; and across the boxes, in the dark, something is awake.",
             do=[{"set": "@box_burned"}, {"set": "@box_dealt"}, {"journal": "@j_box"}], end=True))

# ---- the end
DIALOGUE["@lash"] = D("n0",
    n0=N(CAP, "The wheel. The fog. The night coming on. The hands are the ship's, now; they must be tied to it.",
         choices=[
             C("[Lash myself to the wheel]", "n_end", cond="@mate_gone&has:rope&has:crucifix&has:@rosary&has:@bottle_log&has:@cabin_key"),
             C("[What do I still need?]", "n_need"),
             C("[Not yet]", end=True)]),
    n_need=N(CAP, "A rope for my hands. The crucifix and my mother's beads, which He dare not touch. The log, sealed in the bottle, in my pocket, with the cabin key. The mate gone, and the last entry written. When all is ready, I shall tie myself to the wheel.", next="n0"),
    n_end=N(CAP, "I lash my hands to the spokes with the manila, wind the rosary through my fingers, and set the crucifix between them. Come good wind or foul, I shall save my soul and my honour as a captain. I am growing weaker, and the night is coming on. God, the Blessed Virgin and the saints help a poor ignorant soul trying to do his duty.",
            do=[{"journal": "@j_end"},
                {"card": "6 August. In the great storm the Demeter ran before the wind into Whitby harbour, all sails set, and struck the sands under the East Cliff. As she struck, a great dog sprang from the deck to the shore and ran up the cliff path into the dusk; no trace of it was ever found. The captain was found lashed to the wheel, dead, his hands bound over a crucifix and a string of beads, a corked bottle and a cabin key in his pocket. The folk of Whitby buried him as a hero, on the cliff, near the seat where a girl and her friend sat watching the sea."},
                {"arc_end": 1}], end=True))

# ===================================================================================================== items
ITEMS = {
    "@manifest": dict(name="Bill of lading", asset="book", variant="diary", desc="'50 boxes of earth and silver sand, Varna to Whitby, consigned to Mr. S. F. Billington.'"),
    "@clearance": dict(name="Customs clearance", asset="book", variant="red", desc="A stamped clearance for the Demeter. The stamp is crooked, which is the best a bribe can do."),
    "@candle": dict(name="Blessed candle", asset="candle", variant="white", desc="A beeswax candle from the widow on the quay."),
    "@crowbar": dict(name="Carpenter's crowbar", asset="hammer", variant="default", desc="Two feet of black iron."),
    "@hold_key": dict(name="Hold key", asset="key", variant="gold", desc="The big brass key to the main hatch."),
    "@cabin_key": dict(name="Cabin key", asset="key", variant="gold", desc="The key to my cabin. The only lock on the ship that has never been picked."),
    "@rosary": dict(name="Mother's rosary", asset="key", variant="gold", desc="A string of black beads, worn smooth by a lifetime of prayer."),
    "@bottle": dict(name="Corked bottle", asset="bottle", variant="glass", desc="A strong bottle with a stout cork."),
    "@bottle_log": dict(name="Sealed bottle with the log", asset="bottle", variant="amber", desc="The last pages of the log of the Demeter, sealed in wax."),
    "@robin": dict(name="Round robin", asset="book", variant="leather", desc="The men's petition for a double watch, signed in a ring so that no one signs first."),
    "@cap": dict(name="Petrofsky's cap", asset="key", variant="gold", desc="A blue knitted cap, wet."),
    "@keepsake": dict(name="The Captain's crucifix and rosary", asset="crucifix", variant="silver", desc="A small silver crucifix and a string of worn black beads, carried by the Captain of the Demeter to the last."),
}

# ===================================================================================================== journal
JOURNAL = {
    "@j_varna": J("Varna", "6 July. The quay is loud and the cargo is quiet. Fifty boxes of earth and sand, for a gentleman in Whitby whom no one has met. The freight is paid in full and I am asked no question. I have been twenty years at sea and I do not like a cargo that nobody wants to talk about."),
    "@j_cargo": J("The bill of lading", "Fifty boxes of earth, silver sand, consigned to Mr. S. F. Billington of Whitby. The papers are clean. The man who ordered it did not come himself, and the Slovaks who loaded it would not look at it. I put the bill in my coat and I say nothing."),
    "@j_cleared": J("Customs", "The customs officer found the boxes 'irregular' until I found a silver coin. Then they were perfectly regular. I have been in business long enough to know that this is how the world works, and long enough to hope that it will not always be so."),
    "@j_blessed": J("The blessing", "Father Nikolai blessed the ship and gave me a small flask of holy water. 'A cross is better than a pilot,' he said. I do not argue with priests, and on this voyage I am not sure I argue with anyone."),
    "@j_sail": J("Departure", "At noon we cast off. East wind, fresh. The men sing at the capstan, a little too loudly. Five hands, two mates, the cook, and myself; a good crew who have sailed with me before. I expected nothing, and I am already uneasy."),
    "@j_cabin": J("My cabin", "My own cabin, my own lamp, my own cross in the sea-chest. I have kept the log here for twenty years. I shall keep it as long as I can hold a pen."),
    "@j_hold": J("The hold", "Fifty boxes in five rows. The ship sits lower than clay would make her. I count them twice. It is the same number, and it should be a comfort."),
    "@j_galley": J("The galley", "The cook is the most superstitious man aboard, and the only one I would trust with the ship. Garlic over the stove, salt on the step. He laughs at me, then crosses himself."),
    "@j_fore": J("The forecastle", "The men have nailed more holy pictures over their bunks than a church has walls. I say nothing. A man who prays is a man who has not given up."),
    "@j_weather": J("Reading the weather", "Glass falling, mares'-tails in the north-west, gulls inland, porpoises running west. The cook, the sky and the needle agree. We reef down before the blow; the men are quicker than I ever saw them. It is good to give orders that make sense."),
    "@j_log1": J("11 July, the Bosphorus", "11 July at dawn entered Bosphorus. Boarded by Turkish Customs officers. Backsheesh. All correct. Under way at 4 p.m. 12 July, through the Dardanelles. More Customs officers. Want us off soon. At dark passed into the Archipelago. I write it exactly, so that it can be checked."),
    "@j_petrofsky": J("Petrofsky", "16 July. Petrofsky is missing. He took the larboard watch at eight bells and was relieved by Abramoff, but he never went to his bunk. The men say they expected it. They will say no more than that there is something aboard."),
    "@j_olgaren": J("A tall thin man", "17 July. Olgaren tells me that behind the deck-house, in the rain, he saw a tall, thin man, not like any of the crew, come up the companion-way and go along the deck, and disappear. He followed and found no one, and every hatch closed. I fear that panic may spread."),
    "@j_log2": J("The search", "Searched stem to stern with lanterns, all keeping abreast. No man found; only earth spilled from box thirteen to the bows, and Petrofsky's cap. The men are relieved. The mate scowled and said nothing. I did not say what I thought."),
    "@j_dmitri": J("Dmitri", "24 July. Dmitri is gone. A second man off his watch, and not seen again. The crew have sent me a round robin asking for a double watch. They fear to be alone. The mate is angry. I fear that either he or the men will do some violence."),
    "@j_log3": J("Two men gone", "Two men lost since Varna: Petrofsky and Dmitri. Both off watch, neither seen again. I write it exactly. A log does not weep, and neither will I, until I am ashore."),
    "@j_roster": J("The watch bill", "I chalk up the watches: Ivan and Bolotin for the first, the mate and myself for the middle, Olgaren and Abramoff for the morning. No man alone. If anything can be done by arithmetic, I have done it."),
    "@j_storm": J("Four days in hell", "28 July. Four days in a maelstrom; no sleep for anyone. 29 July: the second mate gone, and only the steersman on deck. 30 July: both watch and helmsman gone. Without second mate, crew in a panic. The mate and I agree to go armed henceforth and wait for any sign of the cause."),
    "@j_box": J("Box thirteen", "With the crowbar I opened the box with the bright nails. Black earth, and in it the shape of a man. I have done what I can: it will not be a bed again. But there are forty-nine more, and I am one man."),
    "@j_cry": J("The cry", "2 August, midnight. A cry outside my port. The mate heard it too, and ran. No sign of the man on watch. One more gone. I take lantern and club to the hold, where the boxes are moving."),
    "@j_dark": J("The dark in the hold", "In the hold, with a lantern and a cross, I held off the dark until dawn. Whether it was bats, or rats, or the thing that walks on deck, I cannot swear. Something with a white face. Olgaren is gone. God, help me."),
    "@j_log4": J("The final entry", "I have written the last entry, sealed it in a bottle, and kept the cabin key in my pocket. If we are wrecked, mayhap this bottle may be found, and those who find it may understand."),
    "@j_mate": J("The mate", "3 August. The mate came on deck as if shot from a gun, his eyes rolling. 'You had better come too, Captain, before it is too late. The sea will save me from Him.' And he leapt overboard. I suppose I know the secret now."),
    "@j_bow": J("The bows", "The bow is where Olgaren saw It, and where the mate saw It. It is where the fog begins. I stand on the foredeck and I am sure that if I turn my back, it will be behind me."),
    "@j_wheel": J("The wheel", "The wheel is the only thing aboard that still obeys. I put my hands where a hundred captains have put theirs, and I decide, quietly, that mine are the last that will."),
    "@j_end": J("Lashed to the wheel", "4 August. I shall tie my hands to the wheel, and along with them I shall tie that which He dare not touch; and then, come good wind or foul, I shall save my soul, and my honour as a captain. God and the Blessed Virgin and the saints help a poor ignorant soul trying to do his duty."),
}

# ===================================================================================================== combat
ENEMIES_EXTRA = {
    "@shade": dict(name="The tall thin figure", model="human_dracula", hp=24, spd=6, dmg=[3, 5], acc=66, eva=14, tags=["vampire", "undead"], nerve_hit=3,
                   abilities=["bite"], book="the stranger aboard the Demeter (ch.7)"),
}
ENCOUNTERS_EXTRA = {
    "@dark_blessed": dict(name="The dark in the hold", time="night", enemies=["bat", "@shade"], flee_ok=False, survive=5,
                          intro="The earth in box thirteen is grey and cold. Something that has lost its bed is looking for another. A lantern swings, and the boxes shift on their lashings.",
                          win="I keep the cross between us and the dark. It does not like it.",
                          dawn_text="A grey line at the hatch. The thing among the boxes is gone, and the bat with it.", location="@hold"),
    "@dark_burned": dict(name="The dark in the hold", time="night", enemies=["bat", "bat", "bat", "@shade"], flee_ok=False, survive=5,
                         intro="The smoke is rolling; the earth is smouldering in box thirteen. The dark is full of wings and a tall shape that is not afraid of fire, only of me.",
                         win="I hold the cross against them, while the smoke thins.",
                         dawn_text="A grey line at the hatch. The wings are gone, the shape is gone, and I am alone with the burned box.", location="@hold"),
}
_HOOK = [{"set": "@dark_done"}, {"set": "@p6"}, {"set": "@gone_olgaren"}, {"set": "@gone_stepan"}, {"journal": "@j_dark"},
         {"card": "3 August. Rejoiced we are nearing England. At midnight I went to relieve the man at the wheel, and when I got to it found no one there. The wind was steady. I dared not leave it, so I shouted for the mate."},
         {"goto": "@wheelhouse"}]
ENCOUNTER_HOOKS = {
    "@dark_blessed": dict(on_win=_HOOK, on_lose=_HOOK, on_flee=_HOOK),
    "@dark_burned": dict(on_win=_HOOK, on_lose=_HOOK, on_flee=_HOOK),
}

# ===================================================================================================== seed variation
PALETTES = {
    "@cabin": [dict(wall="planks", floor="planks", wood="dark", cloth="black"), dict(wall="planks", floor="planks", wood="oak", cloth="blue")],
    "@hold": [dict(wall="stone_dark", floor="dirt", wood="ebony", cloth="black"), dict(wall="stone_grey", floor="dirt", wood="dark", cloth="black")],
    "@galley": [dict(wall="plaster_dirty", floor="planks", wood="oak", cloth="red"), dict(wall="plaster", floor="planks", wood="pale", cloth="cream")],
    "@forecastle": [dict(wall="planks", floor="planks", wood="dark", cloth="green"), dict(wall="planks", floor="planks", wood="oak", cloth="blue")],
}

PLACEMENTS = {
    "@hold_key": [
        dict(prop="@c_bunk", text="Under the straw of the bunk, a big brass key on a lanyard: the hold key.", hint="The straw in the bunk lies lumpily."),
        dict(prop="@g_hook", text="On the cook's key-hook, among the spoons, a big brass key: the hold key.", hint="One of the spoons on the cook's hook is a key."),
        dict(prop="@d_locker", text="At the bottom of the deck locker, in a coil of marline, a big brass key: the hold key.", hint="The deck locker has been rummaged and put back in a hurry."),
    ],
    "@cabin_key": [
        dict(prop="@c_shelf", text="Behind Lloyd's Register, hanging on a nail, the small iron key of the cabin door.", hint="Lloyd's Register stands a finger out from the shelf."),
        dict(prop="@c_desk2", text="Under a corner of the chart, the small iron cabin key, where I put it myself and forgot.", hint="The chart is lying crooked on the table."),
        dict(prop="@c_lamp", text="Hooked behind the swinging lamp, the small iron cabin key.", hint="The lamp swings from its gimbals with a faint jingle."),
    ],
}

GATES = {
    "@d_hatch": [
        dict(cond="has:@hold_key", fail="Barred and padlocked. The hold key is kept somewhere in the ship, not far from where the captain sleeps.", needs="@hold_key"),
        dict(cond="has:@crowbar", fail="Barred and padlocked. The carpenter's crowbar would take the hasp off.", needs="@crowbar"),
    ],
}

# Re-use the Act II schooner and wheel models through this arc's own asset ids (same builders).
ASSETS = [dict(id="@schooner", builder="a2_schooner", params={}), dict(id="@wheel", builder="a2_wheel", params={}),
          dict(id="@deckshell", builder="a2_deckshell", params={}), dict(id="@mast", builder="a2_mast", params={})]
VARIANTS = {
    "@schooner": {"default": "weathered", "weathered": {"wood": T("wood_planks", "#8a7458"), "cloth": T("cloth", "#7a6f55"), "patch": T("cloth", "#615740"), "iron": T("iron"),
                                                              "tar": T("wood_planks", "#16120f"), "trim": T("wood_planks", "#d9d2bf"), "rope": T("cloth", "#6e5c3e")}},
    "@deckshell": {"default": "weathered", "weathered": {"wood": T("wood_planks", "#8a7458"), "iron": T("iron"),
                                                         "tar": T("wood_planks", "#16120f"), "trim": T("wood_planks", "#d9d2bf")}},
    "@mast": {"default": "weathered", "weathered": {"wood": T("wood_planks", "#7a6246"), "cloth": T("cloth", "#7a6f55"), "iron": T("iron"),
                                                    "rope": T("cloth", "#6e5c3e")}},
    "@wheel": {"default": "oak", "oak": {"wood": T("wood_planks", "#7a6048"), "iron": T("iron")}},
    "human_peasant_m": {
        "@clerk": human_colors(skin=T("skin", "#e0c4a8"), hair=T("hair", "#3a3a3a"), top=T("wool", "#2a2a32"), bottom=T("wool", "#1e1e24")),
        "@customs": human_colors(skin=T("skin", "#d9a98a"), hair=T("hair", "#2a2a2a"), top=T("wool", "#1f2c44"), bottom=T("wool", "#1a1a22")),
        "@priest": human_colors(skin=T("skin", "#d8b898"), hair=T("hair", "#d0d0d0"), top=T("cloth", "#1a1a1e"), bottom=T("cloth", "#1a1a1e")),
        "@foreman": human_colors(skin=T("skin", "#c99a74"), hair=T("hair", "#4a3a2a"), top=T("wool", "#4a3a2a"), bottom=T("wool", "#2e2a24")),
        "@petrofsky": human_colors(skin=T("skin", "#e0b896"), hair=T("hair", "#6a5a3a"), top=T("wool", "#2a3e6a"), bottom=T("wool", "#26262e")),
        "@dmitri": human_colors(skin=T("skin", "#e8c3a0"), hair=T("hair", "#c8a860"), top=T("wool", "#4a5a3a"), bottom=T("wool", "#2e3028")),
        "@ivan": human_colors(skin=T("skin", "#cfa383"), hair=T("hair", "#5a3a22"), top=T("wool", "#3a4a5a"), bottom=T("wool", "#26262e")),
        "@olgaren": human_colors(skin=T("skin", "#e8c3a0"), hair=T("hair", "#d8d8d8"), top=T("wool", "#2e3a4a"), bottom=T("wool", "#2a2a30")),
        "@cook": human_colors(skin=T("skin", "#d9a98a"), hair=T("hair", "#7a5a3a"), top=T("cloth", "#e0d8c8"), bottom=T("wool", "#4a4036")),
        "@abramoff": human_colors(skin=T("skin", "#c99a74"), hair=T("hair", "#2a2a2a"), top=T("wool", "#1f2c44"), bottom=T("wool", "#22222a")),
        "@bolotin": human_colors(skin=T("skin", "#dcc0a0"), hair=T("hair", "#3a3a3a"), top=T("wool", "#2a2a38"), bottom=T("wool", "#1e1e28")),
    },
    "human_peasant_f": {
        "@widow": human_colors(skin=T("skin", "#e0c0a0"), hair=T("hair", "#3a3a3a"), top=T("wool", "#1a1a1e"), bottom=T("wool", "#1a1a1e")),
    },
    "human_captain": {
        "@mate": human_colors(skin=T("skin", "#d9a98a"), hair=T("hair", "#1e1e1e"), top=T("wool", "#3a3a40"), bottom=T("wool", "#26262c")),
    },
}


# ---- expand the '@' id prefix --------------------------------------------------------------------------------------
def _x(o):
    if isinstance(o, str):
        return o.replace("@", "demeter_voyage_")
    if isinstance(o, list):
        return [_x(i) for i in o]
    if isinstance(o, dict):
        return {_x(k): _x(v) for k, v in o.items()}
    return o


for _n in ("LOCATIONS", "LOC_DATA", "DIALOGUE", "ITEMS", "JOURNAL", "PALETTES", "PLACEMENTS", "GATES", "ENEMIES_EXTRA",
           "ENCOUNTERS_EXTRA", "ENCOUNTER_HOOKS", "ARC", "VARIANTS", "ASSETS"):
    globals()[_n] = _x(globals()[_n])
