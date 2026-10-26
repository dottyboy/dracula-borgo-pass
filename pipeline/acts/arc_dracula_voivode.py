"""PERSONAL ARC - "Seven Hundred Years" (the young Voivode, later Count Dracula).  Ids prefixed dracula_voivode_.
Castle in the Carpathians -> the road to the ford and the night raid -> the Scholomance by Lake Hermannstadt -> the first night of the un-dead.
Based on the Count's own speech (ch.3) and Van Helsing's account (ch.18). Original material: Ileana, Radu's letter, Vasile the rival."""
from dsl import *

F = "dracula_voivode_"


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


def P(s, *a, **k):
    return prop(F + s, *a, **k)


def NP(s, *a, **k):
    return npc(F + s, *a, **k)


ARC = dict(
    id="dracula_voivode", title="Seven Hundred Years", member="dracula", portrait="dracula_young",
    blurb="Before the legend there was a prince: a besieged border, a ford by night, a school beneath a mountain that takes every tenth scholar, and a first night in the tomb. Who he was decides what he becomes.",
    unlock="", unlock_text="Finish the main story to hear the Count's own history.", after_credits=True,
    start=dict(location=F + "hall", protagonist="dracula", party=["dracula"], items={}, flags=[]),
    exit_to="ARC_END",
    rewards=[dict(give=F + "signet"), dict(give=F + "medal"), dict(give=F + "charm"),
             dict(stat=dict(member="vanhelsing", faith=1, nerve=2)), dict(set=F + "knowing_the_enemy")],
    rewards_text="The Voivode's dragon signet, the Order of the Dragon medal and a wolf-tooth charm; Van Helsing gains +1 Faith and +2 Nerve from knowing the enemy.",
)

LOCATIONS = [
    dict(id=F + "hall", name="The great hall, the castle in the Carpathians", desc="Black rafters, a hearth like a cave mouth and a council that has not slept. The banners hang as though the wind outside had tired of them.", date="The 1440s"),
    dict(id=F + "chamber", name="The Voivode's chamber", desc="My father's room, now mine. The bed is too large, the books too many, and the portrait does not like me.", date="The same night"),
    dict(id=F + "tower", name="The watch-tower", desc="Open battlements above the pass. Far off to the east a ridge keeps its own dark, and on it a beacon that should burn does not.", date="Night"),
    dict(id=F + "road", name="The mountain road", desc="Pines, rock and the sound of cartwheels going the wrong way: the hungry are coming up the road as the levy goes down it.", date="Dusk, three days later"),
    dict(id=F + "camp", name="The army's camp", desc="A hundred fires in a bowl of the hills. Men are cleaning mail, and none of them are talking about home.", date="Night"),
    dict(id=F + "ford", name="The Reed Ford", desc="A broad brown river and reeds as tall as a rider. Water sleeps, the Turks say, and the enemy is sleepless.", date="Before dawn"),
    dict(id=F + "lake", name="The shore of Lake Hermannstadt", desc="Black water under a low sky. A ferry-post, a ring of leaning stones and a mountain that seems to have its door open.", date="Autumn, some years on"),
    dict(id=F + "school", name="The Scholomance, the lecture hall", desc="A stone school under the mountain. The benches are worn, the torches never smoke and nobody here has ever been seen to laugh.", date="The first winter"),
    dict(id=F + "library", name="The forbidden library", desc="Shelves to the vault, chained books and a smell of cold iron and wet paper.", date="The first winter"),
    dict(id=F + "tithe", name="The tithe chamber", desc="Ten seats in a ring, a fire without smoke, and below the floor a sound like a great beast breathing.", date="The last night of the term"),
    dict(id=F + "tomb", name="The family crypt", desc="Cold stone, old wax, and no light at all but what the eyes themselves seem to give.", date="Years after"),
    dict(id=F + "chapel", name="The castle chapel, by night", desc="The little chapel above the crypt. The doors have been left unbarred and the altar candles have burned to stubs.", date="The first night"),
]

LOC_DATA = {}

# ------------------------------------------------------------------------------------------------------------- hall
LOC_DATA[F + "hall"] = dict(
    cells=[3, 2], interior=True, wall="stone_dark", floor="planks", ambient=AMBIENT["candle_interior"], camera=cam([3, 2]),
    lights=lights_warm([3, 2], energy=2.8),
    walls=dict(north=["wall_window_4", "wall_4", "wall_window_4"], west=["wall_door_4", "wall_4"], east=["wall_door_4", "wall_door_4"]),
    spawn=[0.0, 2.5], spawns={F + "chamber": [-4.4, -2.0], F + "tower": [4.4, -2.0], F + "road": [4.4, 2.0]},
    props=[
        P("throne", "throne", "black", 0.0, -3.2, name="The Voivode's seat", radius=0.8, look="Black oak, dragon-headed. It was my father's, and before him another's, and every one of them sat in it as if it were a mistake that could be corrected."),
        P("table", "table_long", "ebony", 0.2, 0.6, name="The council table", radius=1.7, look="A map of the border is pinned under three daggers. The fortress of Severin, burning in red wax, stands where the Turkish ink comes closest."),
        P("chair1", "chair", "black", -2.0, 0.6, rot=90, name="Stanciu's chair", radius=0.4, look="The counsellor's chair, with a cushion upon it for a back that has served three princes."),
        P("chair2", "chair", "red", 2.4, 0.6, rot=-90, name="Boyar's chair", radius=0.4, look="Velvet. Vlaicu will not sit in anything without it."),
        P("fire", "fireplace", "stone_dark", -3.9, -3.3, name="Great hearth", radius=1.0, look="A log the thickness of a man burns on it. Nobody who sits near it is warm."),
        P("banner", "inn_sign", "dark", 3.8, -3.7, y=1.3, name="The Dragon banner", radius=0.6,
          look="The coiled dragon of the Order, and beneath it, in faded thread: 'Founded by Sigismund, King of Hungary, in the year 1408. Whoso wears the Dragon keeps the gate of Christendom.'"),
        P("shelf", "bookshelf", "dark", -5.2, 1.8, rot=90, name="Chronicle shelf", radius=0.7, look="The annals of the principality in four hands, none of which agree about anything."),
        P("barrel", "barrel", "dark", 4.9, 0.2, rot=-90, name="Barrel of lamp-oil", radius=0.5,
          look="Lamp-oil for the beacons, in a barrel with the garrison's mark burned in the lid. Half of it is meant for the tower.",
          take="oil", take_text="I fill a flask from the barrel. The tower will want it.", give_once=True),
        P("wtable", "table", "dark", -4.2, 2.9, name="Writing-table", radius=0.8, look="Pens, sand and a pot of black ink gone to jelly. A clerk has been working at it since the siege began."),
        P("draft", "book", "diary", -4.2, 2.9, y=0.8, name="Draft order", radius=0.25,
          look="A clerk's neat draft: 'To the captains of the levy: assemble at the camp below the Reed ford...' It has no seal and so no force.",
          take=F + "draft_order", take_text="I take the draft order. It wants a seal.", give_once=True),
        P("press", "chest", "ebony", -4.2, 2.9, y=0.8, scale=0.3, name="Seal-press and wax", radius=0.3,
          look="A candle, a stick of green wax and a brass press shaped to fit a ring. It waits for the ring.", talk=F + "seal"),
        P("rug", "rug", "red", 0.4, 2.4, radius=0.1),
        P("sconce1", "sconce", "default", -5.7, 0.6, y=1.5, rot=90, radius=0.1),
        P("sconce2", "sconce", "default", 5.7, 0.4, y=1.5, rot=-90, radius=0.1),
        P("d_chamber", "door", "dark", -5.8, -2.0, rot=90, name="Door to my chamber", radius=0.6, look="To my father's chamber, and the stair beyond.", go=F + "chamber"),
        P("d_tower", "door", "oak", 5.8, -2.0, rot=-90, name="Stair to the watch-tower", radius=0.6, look="A narrow spiral up to the battlements.", go=F + "tower"),
        P("d_gate", "door_big", "oak", 5.8, 2.0, rot=-90, name="The castle gate", radius=0.7,
          look="The great gate and the road to the army. I do not leave until the order is sealed and sent, the beacon is lit, my brother is dealt with and I carry my father's hammer.",
          go=F + "road", go_cond=F + "order_sent&" + F + "beacon_lit&" + F + "radu_resolved&has:" + F + "warhammer&" + F + "council_done",
          go_fail="Not yet. The council must be answered, the order sealed and sent, the beacon lit, Radu faced, and my father's hammer in my hand."),
    ],
    npcs=[
        NP("stanciu", "human_peasant_m", F + "stanciu_v", -1.4, -1.8, rot=0, name="Stanciu, the counsellor", look="Counsellor to my father and to his father. A grey beard, a voice like a closing door, and the best advice in the principality delivered with the worst timing.", talk=F + "stanciu_talk"),
        NP("vlaicu", "human_peasant_m", F + "vlaicu_v", 3.0, -0.8, rot=180, name="Boyar Vlaicu", look="Furs, rings and a smile that arrives a moment after the thought behind it. He commands three hundred spears and mentions it often.", talk=F + "vlaicu_talk"),
        NP("radu", "human_peasant_m", F + "radu_v", 1.6, 2.6, rot=180, name="Radu, my brother", look="My younger brother, back from the Sultan's court with Turkish manners, Turkish silks and an excellent opinion of himself. We have the same eyes. I have never been sure about the rest.", talk=F + "radu_talk"),
        NP("messenger", "human_peasant_m", F + "messenger_v", 4.0, 2.6, rot=-90, name="Petru, the courier", look="A thin rider in a muddy cloak who has been waiting by the door for an order that has not come.", talk=F + "messenger_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_hall")])],
)

# --------------------------------------------------------------------------------------------------------- chamber
LOC_DATA[F + "chamber"] = dict(
    cells=[2, 2], interior=True, wall="stone_dark", floor="planks", ambient=AMBIENT["candle_interior"], camera=cam([2, 2]),
    lights=lights_warm([2, 2]),
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[2.5, -1.5], spawns={F + "hall": [2.8, -2.0]},
    props=[
        P("bed", "bed", "black", -2.4, -2.6, name="My father's bed", radius=1.1, look="Wide as a threshing-floor and cold as one. I have not yet slept in it."),
        P("chest", "chest", "ebony", -3.0, 0.6, rot=90, name="The Order chest", radius=0.7,
          look="An iron-bound chest with a dial of years on the lid. Whatever it holds, my father locked it himself.", talk=F + "chest_lock"),
        P("bust", "bust", "stone_dark", 0.2, -3.4, name="Bust of my father", radius=0.5,
          look="Vlad Dracul in marble, wearing the Order's collar. On the plinth: 'Invested 1431, at Nuremberg.' It is the year he is proudest of. It is not the year of the Order."),
        P("rack", "bookshelf", "dark", 3.3, 0.8, rot=-90, name="Armour-stand", radius=0.7,
          look="Mail, a helm and the heavy iron-headed hammer my father swung on the Danube. It is lighter than it looks, and I am not sure whether I am meant to be flattered.",
          take=F + "warhammer", take_text="I take my father's hammer. It fits my hand as if it had been waiting.", give_once=True),
        P("desk", "table", "dark", 0.0, 1.0, name="Desk", radius=0.9, look="Letters, a wax-stub and a map of the border with the Turkish side left blank, as though no one dared to draw it."),
        P("candle", "candelabra", "default", 0.0, 1.0, y=0.8, name="Candelabra", radius=0.2, look="Five candles. Four of them are lit."),
        P("fire", "fireplace", "stone_dark", -3.7, 2.6, rot=90, name="Fireplace", radius=0.9, look="Built for two. Warms one."),
        P("rug", "rug", "red", 0.4, 2.0, radius=0.1),
        P("shelf", "bookshelf", "dark", 3.4, -2.4, rot=-90, name="Books", radius=0.7, look="Hours, a Livy in Latin and three treatises on fortification, all well-thumbed. My father read to be believed."),
        P("window", "sconce", "default", -3.7, -2.0, y=1.5, rot=90, radius=0.1),
        P("d_hall", "door", "dark", 3.8, -2.0, rot=-90, name="Door to the hall", radius=0.6, look="Back to the hall.", go=F + "hall"),
    ],
    npcs=[
        NP("ileana", "human_lucy", F + "ileana_v", 1.4, -0.6, rot=-90, name="Ileana", look="Boyar Corvin's daughter. She has a clear grey stare and an unfashionable habit of saying exactly what she means. We were children together in this castle. We are not children now.", talk=F + "ileana_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_chamber")])],
)

# ---------------------------------------------------------------------------------------------------------- tower
LOC_DATA[F + "tower"] = dict(
    cells=[2, 2], interior=False, wall="stone_dark", floor="cobble", ambient=AMBIENT["night_exterior"], camera=cam([2, 2]),
    lights=lights_moon(2.6), moon=dict(pos=[-6, 9, -5]),
    scatter=dict(asset="pine", variant="dark", count=12, seed=7, avoid=[[-6, -6, 6, 6]]),
    spawn=[0.0, 2.4], spawns={F + "hall": [0.0, 2.4]},
    props=[
        P("parapet1", "fence", "default", -2.0, -3.6, radius=0.3),
        P("parapet2", "fence", "default", 2.0, -3.6, radius=0.3),
        P("merlon1", "column_short", "stone_dark", -3.6, -3.4, name="Merlon", radius=0.4, look="Cut stone, blackened by seven centuries of other people's fires."),
        P("merlon2", "column_short", "stone_dark", 3.6, -3.4, radius=0.4),
        P("pyre_dry", "fireplace", "stone_dark", 0.0, -2.0, name="The beacon, unlit", radius=0.9, cond="!" + F + "beacon_oiled",
          look="An iron brazier on a stone foot, stacked with split logs. The wood is bone dry, and so is the pitch. It would not light for weeks of trying without something to feed it.",
          use_item={"oil": [{"take": "oil"}, {"set": F + "beacon_oiled"}, say("I soak the logs through. The smell of lamp-oil is almost cheerful. It wants only fire.")]},
          use_fail="It is not wood it wants. Something to feed the flame, and then something to start it."),
        P("pyre_wet", "fireplace", "stone_dark", 0.0, -2.0, name="The beacon, soaked", radius=0.9, cond=F + "beacon_oiled&!" + F + "beacon_lit",
          look="The logs are dark with oil. A spark would finish the work.",
          use_item={"torch": [{"take": "torch"}, {"set": F + "beacon_lit"}, {"journal": F + "j_beacon"}, say("The torch touches the oil. A pillar of fire stands on the tower, and across the valley, on the ridge, a second small flame answers.")]},
          use_fail="Not that. It wants a flame."),
        P("pyre_lit", "fireplace", "soot", 0.0, -2.0, name="The beacon, burning", radius=0.9, cond=F + "beacon_lit",
          look="It roars. On the far ridge the answering flame has doubled."),
        P("torch_sconce", "sconce", "default", -3.7, 0.0, y=1.5, rot=90, name="Torch in a bracket", radius=0.3,
          look="A resin torch in an iron bracket by the stair door, the only one on the tower that is not burned out.",
          take="torch", take_text="I take the torch from its bracket.", give_once=True),
        P("lantern", "lantern", "default", 3.0, -1.0, name="Watch lantern", radius=0.3, look="Shuttered, so as not to be a target."),
        P("barrel", "barrel", "dark", 3.6, 1.0, name="Rain-barrel", radius=0.5, look="Green water. Even the pine-needles have given it up."),
        P("rock", "rock", "dark", -3.2, 2.6, radius=0.5),
        P("stair", "door", "oak", 0.0, 3.6, name="The stair down", radius=0.6, look="Back down to the hall.", go=F + "hall"),
    ],
    npcs=[
        NP("sentry", "human_peasant_m", F + "sentry_v", 2.0, 0.6, rot=-30, name="Dan, the old sentry", look="Thirty years on this tower. He knows every star by the name it has in the barracks, which is not the one in the almanac.", talk=F + "sentry_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_tower")])],
)

# ------------------------------------------------------------------------------------------------------------ road
LOC_DATA[F + "road"] = dict(
    cells=[3, 3], interior=False, wall="stone_dark", floor="dirt", ambient=AMBIENT["dusk_exterior"], camera=cam([3, 3]), lights=lights_day(2.0),
    scatter=dict(asset="pine", variant="dark", count=26, seed=3, avoid=[[-7, -7, 7, 7]]),
    spawn=[4.0, 2.0], spawns={F + "hall": [4.6, 2.0], F + "camp": [-4.6, -2.0]},
    props=[
        P("gate_back", "arch", "stone_dark", 5.2, 3.6, name="Back to the castle", radius=0.8, look="The castle gate is behind me, up the hill. The old road has taken the shape of a long habit.", go=F + "hall"),
        P("signpost", "signpost", "oak", -5.0, -2.2, rot=90, name="Signpost: the camp", radius=0.4, look="One arm points to the camp, the other to a ford with a Turkish name someone has tried to scratch out.", go=F + "camp"),
        P("cart", "carriage", "dark", 1.0, -1.0, rot=70, name="Refugees' cart", radius=1.2, look="Axle cracked, a mattress on top, three children in a heap and a grandmother in front, who has not looked back once."),
        P("prints", "rock", "dark", -2.4, 1.2, name="Hoofprints in the mud", radius=0.6,
          look="Many hooves, small, wrapped round with felt: the marks are deep and smeared, not the clean crescents of shod horses. Whoever it was came by night, and does not want to be heard.",
          set=F + "saw_prints", set_text="I kneel by the prints. Felt-wrapped hooves; silent riders. They came down from the north-east, along the reed-creek, to the river."),
        P("cross", "crucifix_big", "silver", 3.0, -3.4, name="Wayside cross", radius=0.4, look="A wooden Christ under a little roof, carved by someone who loved wood more than anatomy. Fresh flowers lie at its foot, from people who have nothing else to give."),
        P("fire", "lantern", "default", -1.0, -3.4, name="Road lantern", radius=0.3, look="A candle in a tin, left for travellers by someone who will not know their names."),
        P("rock1", "rock_big", "mossy", -5.0, 3.0, radius=0.8),
        P("stump", "deadtree", "grey", 2.4, 3.6, name="Dead tree", radius=0.5, look="Lightning took it a long time ago. Wolves use it to mark their ground."),
    ],
    npcs=[
        NP("refugee", "human_peasant_f", "village_woman", 0.2, 0.4, rot=90, name="Grandmother on the cart", look="She sits straight, with a rag-wrapped bundle on her knees. She looks through me rather than at me, which is how a prince is looked at on the road.", talk=F + "refugee_talk"),
        NP("wolves", "wolf", "black", -3.0, -0.4, rot=90, name="Wolves of the road", look="Three grey shapes at the edge of the lantern-light. They are not afraid of the cart, nor of me. They are weighing something.", fight=F + "wolves", cond="!" + F + "wolves_driven"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_road")])],
)

# ------------------------------------------------------------------------------------------------------------ camp
LOC_DATA[F + "camp"] = dict(
    cells=[3, 3], interior=False, wall="stone_dark", floor="dirt", ambient=AMBIENT["night_exterior"], camera=cam([3, 3]), lights=lights_moon(2.4),
    moon=dict(pos=[-6, 9, -5]),
    scatter=dict(asset="pine", variant="dark", count=22, seed=17, avoid=[[-7, -7, 7, 7]]),
    spawn=[4.4, 2.0], spawns={F + "road": [4.6, 2.0], F + "ford": [-4.6, 2.0]},
    props=[
        P("campfire", "fireplace", "soot", 0.0, 0.2, scale=0.6, name="Campfire", radius=0.8, look="Pine knots and a kettle. Twenty men sit round it who have all been telling stories, and are all sure the others are lying."),
        P("lamp", "lantern", "default", 0.3, 0.2, y=0.0, radius=0.2),
        P("mtable", "table", "oak", -3.4, -2.6, name="The map-table", radius=0.9, look="A trestle by the commander's tent, with a vellum map held down by four stones.", talk=F + "map_lock"),
        P("tent1", "bed_simple", "red", -4.2, 2.8, rot=90, name="Bedrolls", radius=0.8, look="Sheepskins on bracken. A boy sleeps there with his boots on, because he has been told to."),
        P("tent2", "bed_simple", "green", 3.6, -3.2, rot=-90, name="Boyars' pavilion", radius=0.8, look="A pavilion for the lords, of which only the pole stands in a convincing line."),
        P("supplies", "chest", "oak", 4.2, 0.8, rot=-90, name="Supply chest", radius=0.6, look="Rations: black bread, onions and salt pork. In a country of mountains, the army marches on onions."),
        P("barrels", "barrel", "dark", 2.8, 2.8, name="Water-barrels", radius=0.5, look="Water for the horses, and for the men who would rather it were wine."),
        P("cart", "carriage", "dark", -4.6, -0.4, rot=90, name="Baggage cart", radius=1.1, look="Forage, tents, the camp-priest's portable altar and a crate marked 'FRAGILE' in a hand nobody will claim."),
        P("rockA", "rock_big", "dark", 5.0, -2.0, radius=0.8),
        P("sign_ford", "signpost", "oak", -5.4, 2.0, rot=90, name="Path to the Reed Ford", radius=0.4,
          look="The track runs down through the reeds to the river. It is a mile of mud, and I should know exactly which ford before I walk it.",
          go=F + "ford", go_cond=F + "ford_known", go_fail="Which ford? Three crossings, and one army can only be at one. The map-table will tell me, if I weigh what the scout and the prints have said."),
        P("sign_road", "signpost", "oak", 5.4, 2.2, rot=-90, name="Back to the road", radius=0.4, look="Back up to the road and the castle.", go=F + "road"),
    ],
    npcs=[
        NP("mircea", "human_captain", F + "mircea_v", 1.8, 0.4, rot=90, name="Captain Mircea", look="Captain of my father's guard, now of mine. A neck like a bull's and the memory of every battle the principality has lost.", talk=F + "mircea_talk"),
        NP("cristea", "human_peasant_m", F + "scout_v", -2.0, 2.4, rot=-60, name="Cristea, the scout", look="Lean, wind-burned, a goatskin cloak over mail. He has just come in from the river, and it shows on his boots.", talk=F + "cristea_talk"),
        NP("prisoner", "human_peasant_m", F + "akinji_v", 3.4, -1.4, rot=-90, name="The captured Akinji", look="A Turkish light-horseman, tied to a wagon-wheel, with a dignified sulk. He glares at a spot just left of my face.", talk=F + "prisoner_talk"),
        NP("hermit", "human_seward", F + "magister_v", -1.0, -1.0, rot=0, name="The pale scholar", look="A gaunt man in black who was not here a moment ago. He has the stillness of a thing that has never had to hurry, and shadows lie wrong around his feet.",
           talk=F + "hermit_talk", cond=F + "raid_won"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_camp")])],
)

# ------------------------------------------------------------------------------------------------------------- ford
LOC_DATA[F + "ford"] = dict(
    cells=[3, 2], interior=False, wall="stone_dark", floor="dirt", ambient=AMBIENT["night_exterior"], camera=cam([3, 2]), lights=lights_moon(2.4),
    moon=dict(pos=[6, 9, -5]),
    scatter=dict(asset="deadtree", variant="grey", count=10, seed=21, avoid=[[-7, -5, 7, 5]]),
    spawn=[-4.4, 2.0], spawns={F + "camp": [-4.6, 2.0]},
    props=[
        P("reeds1", "fence", "default", -3.0, -3.4, radius=0.3),
        P("reeds2", "fence", "default", 0.0, -3.4, radius=0.3),
        P("reeds3", "fence", "default", 3.0, -3.4, radius=0.3),
        P("dead_horse", "rock_big", "dark", 2.8, 0.0, name="Dead horse", radius=0.8, look="A grey pony with felt tied round its hooves. It fell in the shallows with an arrow in its flank and the river is not yet done with it."),
        P("stakes", "fence", "default", -1.0, -2.0, name="Sharpened stakes", radius=0.4, look="Somebody already planted stakes across the shallows. They are not ours."),
        P("crate", "barrel", "dark", 4.4, 1.2, name="Raiders' cask", radius=0.5, look="Pitch and tow. They were going to burn the bridge-timbers."),
        P("standard", "signpost", "oak", 3.8, -1.6, rot=-30, name="Fallen standard", radius=0.4, look="A green horse-tail standard on a spear, snapped. A crescent of tin hangs from it by one wire.",
          take=F + "standard", take_text="I take the broken standard. I do not know why. A prince should remember what he has fought.", give_once=True),
        P("rockA", "rock_big", "dark", -4.6, -1.2, radius=0.8),
        P("back", "signpost", "oak", -5.4, 2.4, rot=90, name="Track to the camp", radius=0.4, look="Back to the camp.", go=F + "camp"),
    ],
    npcs=[
        NP("raider1", "human_peasant_m", F + "akinji_v", 0.4, 0.8, rot=90, name="Akinji raiders", look="Light cavalry, felt on their hooves and knives between their teeth. They have not seen me yet.", fight=F + "raid", cond="!" + F + "raid_won"),
        NP("raider2", "human_peasant_m", F + "akinji_v", -0.8, -0.4, rot=90, name="Akinji scout", look="He crouches in the reeds with a short bow, watching the camp-fires across the water.", fight=F + "raid", cond="!" + F + "raid_won"),
        NP("raider3", "human_peasant_m", F + "akinji_captain_v", 1.8, -1.2, rot=90, name="Akinji captain", look="A broad man in a steel cap, with a curved sword he does not draw. He is sure that tonight belongs to him.", fight=F + "raid", cond="!" + F + "raid_won"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_ford")])],
)

# ------------------------------------------------------------------------------------------------------------- lake
LOC_DATA[F + "lake"] = dict(
    cells=[3, 2], interior=False, wall="stone_dark", floor="dirt", ambient=AMBIENT["storm_exterior"], camera=cam([3, 2]), lights=lights_moon(2.0),
    moon=dict(pos=[6, 9, -5]),
    scatter=dict(asset="pine", variant="dark", count=22, seed=29, avoid=[[-7, -5, 7, 5]]),
    spawn=[0.0, 2.2], spawns={F + "school": [4.4, -1.0]},
    props=[
        P("ferry", "coffin", "ebony", 0.0, -2.6, rot=90, scale=2.2, name="The ferry", radius=1.4,
          look="A black flat boat with a lantern at the bow. It goes out into the mist without a rower and comes back without a mark on it, they say. The ferryman must be paid first.",
          go=F + "school", go_cond=F + "toll_paid", go_fail="The ferryman stands between me and the boat. He wants his toll."),
        P("stones", "gravestone_point", "stone_mossy", -4.0, -1.8, name="Ring of leaning stones", radius=0.6, look="Seven stones, none of them upright. Something older than the school stood here and was not asked."),
        P("bones", "grave_cross", "stone_mossy", 4.2, 1.6, name="Drowned scholar's cross", radius=0.4,
          look="A cairn of lake-stones with an iron cross. In the cairn, pressed in by a careful thumb, a silver coin that no passer-by has dared to take.",
          take="silver", take_text="I take the coin. 'He will not need it,' I tell the cairn, and the lake seems to hear.", give_once=True),
        P("post", "signpost", "dark", 3.6, -3.0, rot=-30, name="Ferry-post", radius=0.4, look="'Scholars only. The tenth pays more.' The last four words have been scratched deeper by a different hand."),
        P("lantern", "lantern", "default", -1.8, -3.0, name="Mist-lantern", radius=0.3, look="It burns green and gives no shadows."),
        P("tree", "deadtree", "grey", -5.2, 2.0, name="Dead pine", radius=0.4, look="Standing in the water as it has stood since its roots drowned."),
        P("rockA", "rock", "dark", 5.0, -1.4, radius=0.6),
        P("rockB", "rock_big", "mossy", -3.4, 3.2, radius=0.8),
    ],
    npcs=[
        NP("ferryman", "human_coachman", F + "ferryman_v", 1.8, -1.2, rot=-100, name="The ferryman", look="Hooded, tall, and so still that a gull has settled on his shoulder. He does not breathe visibly. He holds out his palm without turning his head.", talk=F + "ferryman_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_lake")])],
)

# ----------------------------------------------------------------------------------------------------------- school
LOC_DATA[F + "school"] = dict(
    cells=[3, 3], interior=True, wall="stone_dark", floor="cobble", ambient=AMBIENT["cold_interior"], camera=cam([3, 3]),
    lights=lights_warm([3, 3], energy=2.2),
    walls=dict(north=["wall_4", "wall_door_4", "wall_4"], west=["wall_door_4", "wall_4", "wall_4"], east=["wall_4", "wall_door_4", "wall_4"]),
    spawn=[4.0, 0.0], spawns={F + "lake": [4.4, 0.0], F + "library": [0.0, -3.0], F + "tithe": [-4.2, -3.2]},
    props=[
        P("altar", "tomb", "stone_tomb", -2.6, -0.4, name="The rite-altar", radius=1.0,
          look="A slab of black stone with three hollows in its face: one for a bowl, one for a disc, one for a lamp. What goes in them, and in what order, is for the scholar to know.", talk=F + "altar_lock"),
        P("lectern", "table", "ebony", 0.0, 2.8, name="The Master's lectern", radius=0.9, look="A single book chained to a slanted board. Nobody opens it for a reason."),
        P("benches1", "bench", "dark", -3.6, 2.6, rot=90, name="Student bench", radius=0.8, look="A bench scarred by nine scholars' knives. 'Teodor was here.' Nobody knows which Teodor."),
        P("benches2", "bench", "dark", 3.0, 3.4, rot=-90, name="Student bench", radius=0.8, look="The worn hollow where a scholar sat for an entire winter without speaking."),
        P("slate", "bookshelf", "ebony", 4.8, -1.8, rot=-90, name="The slates", radius=0.7,
          look="Rows of slates. One bears, in chalk: 'Aqua suscitat. Argentum ligat. Ignis signat.' The last word has been underlined, and then, lower, 'But always in this order.'"),
        P("mirror", "mirror", "default", -5.4, 2.0, rot=90, name="The black mirror", radius=0.5, look="It shows the room correctly, and everyone in it but me. I stand a long time before I realise how little I mind."),
        P("fire", "fireplace", "stone_dark", 2.4, -5.3, name="Smokeless fire", radius=1.0, look="It burns without smoke or sound. Held near the palm, it gives no heat."),
        P("candles", "candelabra", "default", -0.1, 2.8, y=0.8, scale=0.8, radius=0.2),
        P("rug", "rug", "black", 0.0, 0.2, radius=0.1),
        P("sconce1", "sconce", "default", -5.7, 0.8, y=1.5, rot=90, radius=0.1),
        P("sconce2", "sconce", "default", 5.7, 3.0, y=1.5, rot=-90, radius=0.1),
        P("column1", "column", "stone_dark", -1.4, 0.2, radius=0.5),
        P("column2", "column", "stone_dark", 1.4, 0.2, radius=0.5),
        P("d_lake", "door_big", "dark", 5.8, 0.0, rot=-90, name="The mountain door", radius=0.7, look="The door to the lake and the ferry.", go=F + "lake"),
        P("d_library", "door", "ebony", 0.0, -5.8, name="Door to the forbidden library", radius=0.6,
          look="Iron, black, banded with the same hollow-and-disc mark as the altar. The lock has a face like a wolf's.", go=F + "library", go_cond="has:" + F + "library_key",
          go_fail="Locked. Vasile has the key; he has the only one, and he knows it."),
        P("d_tithe", "door", "dark", -5.8, -4.0, rot=90, name="The stair down", radius=0.6, look="A spiral stair that goes further than the mountain. The tithe-chamber is below.", go=F + "tithe",
          go_cond=F + "master_met&" + F + "rite_done&" + F + "roll_seen", go_fail="The stair is closed by a black bar that lifts only for the scholar who has attended the Master, performed the rite and read the roll."),
    ],
    npcs=[
        NP("master", "human_seward", F + "magister_v", 0.0, 1.2, rot=180, name="The Master", look="Whatever he was, he has not been that for centuries. He teaches in a flat, kind, amused voice, as a cat teaches a mouse the geography of the room.", talk=F + "master_talk"),
        NP("vasile", "human_quincey", F + "vasile_v", -3.0, 0.8, rot=90, name="Vasile Cernat", look="Another scholar, my age, dark and quick, in a student's black. He keeps the library key on a cord round his neck and takes pleasure in showing it.", talk=F + "vasile_talk"),
        NP("teodor", "human_peasant_m", F + "student_v", 3.2, 1.6, rot=-90, name="Teodor, a scholar", look="A pale boy of seventeen, copying a diagram with trembling hands. He has not been home in three winters.", talk=F + "teodor_talk"),
        NP("maria", "human_peasant_f", F + "student_f_v", -1.4, 3.6, rot=180, name="Maria, a scholar", look="The only woman in the school, silent, with ink on her wrists and a face I would not wish to meet at a crossroads at midnight.", talk=F + "maria_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_school")])],
)

# --------------------------------------------------------------------------------------------------------- library
LOC_DATA[F + "library"] = dict(
    cells=[2, 3], interior=True, wall="stone_dark", floor="cobble", ambient=AMBIENT["cold_interior"], camera=cam([2, 3]),
    lights=lights_warm([2, 3], energy=2.0),
    walls=dict(north=["wall_4", "wall_4"], west=["wall_4", "wall_4", "wall_4"], east=["wall_4", "wall_4", "wall_4"]),
    spawn=[0.0, 4.4], spawns={F + "school": [0.0, 4.4]},
    props=[
        P("shelf1", "bookshelf", "ebony", -3.3, -3.6, name="The chained shelf", radius=0.7, look="Books on chains, as the old libraries did. These chains are to keep the books from the readers."),
        P("shelf2", "bookshelf", "ebony", 3.3, -3.6, rot=0, name="The weather shelf", radius=0.7, look="Treatises on storm, hail and thunder, in a flowing hand. 'To raise a tempest, find the storm already in the sky.'"),
        P("shelf3", "bookshelf", "dark", -3.6, 0.4, rot=90, name="The beast shelf", radius=0.7, look="'De Lupis,' 'On the Speech of Beasts' and a leather-bound 'Wolf-Tongue Primer' in a child's hand. The margins are sharp with bite-marks."),
        P("shelf4", "bookshelf", "dark", 3.6, 0.4, rot=-90, name="The cold shelf", radius=0.7, look="Pages that are cold to touch. I decide not to read them."),
        P("clavis", "book", "red", 0.0, -1.2, y=0.0, name="Clavis Minor", radius=0.4,
          look="A thin red codex on a reading-stand, open at a diagram of three vessels. The opening line reads: 'Three things wake a rite. Water first, to open the way. Silver next, to bind what has come. Fire last, to seal it.'",
          set=F + "read_clavis", set_text="I read it twice. Water, silver, flame. Water opens, silver binds, fire seals."),
        P("stand", "table", "ebony", 0.0, -1.2, name="Reading-table", radius=0.8, look="A black table, scarred round a single circle where something warm once stood."),
        P("roll", "chest", "ebony", -2.4, 3.0, rot=90, name="The Roll of the School", radius=0.6, look="A great scroll on rollers, signed by every scholar who has ever sat below. Ten names stand against each year. Ink is wet on the last line.", talk=F + "roll_talk"),
        P("candles", "candelabra", "default", 3.0, 3.4, name="Candles", radius=0.2, look="Candles of black wax, burning with a flame that does not wag."),
        P("rug", "rug", "black", 0.0, 2.0, radius=0.1),
        P("sconce", "sconce", "default", -3.7, 5.0, y=1.5, rot=90, radius=0.1),
        P("d_school", "door", "ebony", 0.0, 5.8, rot=180, name="Door back to the hall", radius=0.6, look="Back to the lecture hall.", go=F + "school"),
    ],
    npcs=[],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_library")])],
)

# ----------------------------------------------------------------------------------------------------------- tithe
LOC_DATA[F + "tithe"] = dict(
    cells=[2, 2], interior=True, wall="stone_tomb", floor="stone_dark", ambient=AMBIENT["crypt"], camera=cam([2, 2]),
    lights=lights_warm([2, 2], energy=1.6),
    walls=dict(north=["wall_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[2.6, -1.5], spawns={F + "school": [2.8, -2.0]},
    props=[
        P("seat1", "chair", "black", -2.6, -2.2, rot=45, name="Seat of the first scholar", radius=0.4, look="The seats are carved from the mountain itself. Ten in a ring, nine worn smooth."),
        P("seat2", "chair", "black", 0.0, -3.0, name="Seat of the ninth scholar", radius=0.4, look="Taken in a winter of thin rain. Nobody remembers his name."),
        P("seat3", "chair", "black", 2.6, -2.2, rot=-45, name="Seat of the tenth scholar", radius=0.4, look="The tenth seat. It is the only one with a cushion, and the cushion is a hide of something black."),
        P("seat4", "chair", "black", -2.8, 0.6, rot=90, radius=0.4),
        P("seat5", "chair", "black", 2.8, 0.6, rot=-90, radius=0.4),
        P("brazier", "fireplace", "soot", 0.0, 0.2, scale=0.7, name="Smokeless brazier", radius=0.8, look="A fire that gives a green light and a very faint sound like speech, three rooms off."),
        P("grate", "tomb", "stone_tomb", -3.0, 3.0, name="Iron grate", radius=0.6, look="A grating set in the floor. Beneath, a breath of warm air that smells of wet iron and horse."),
        P("sconce", "sconce", "default", -3.7, -1.0, y=1.5, rot=90, radius=0.1),
        P("d_up", "door", "dark", 3.8, -2.0, rot=-90, name="The stair up", radius=0.6, look="The way back to the school.", go=F + "school"),
    ],
    npcs=[
        NP("master2", "human_seward", F + "magister_v", 0.0, -0.8, rot=180, name="The Master of the tithe", look="He is taller down here, and his shadow now has a shape of its own, which does not agree with his.", talk=F + "tithe_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_tithe")])],
)

# ------------------------------------------------------------------------------------------------------------ tomb
LOC_DATA[F + "tomb"] = dict(
    cells=[2, 2], interior=True, wall="stone_tomb", floor="stone_dark", ambient=AMBIENT["crypt"], camera=cam([2, 2]),
    lights=[dict(pos=[0, 2.2, -1.0], color="#6a70ff", energy=1.2, range=9)],
    walls=dict(north=["wall_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_4"]),
    spawn=[0.0, 0.4], spawns={F + "chapel": [0.0, 2.5]},
    props=[
        P("coffin", "coffin", "ebony", 0.0, -1.0, name="My coffin", radius=1.0, cond="!" + F + "lid_open",
          look="The lid is nailed and sealed in lead. I am inside. I have been inside long enough that the idea no longer frightens me. Something heavy would break the lid.",
          use_item={F + "warhammer": [{"set": F + "lid_open"}, say("The iron head takes the seal at the first blow. The lid slides, cracks, tips onto the flags. I am standing in a hole in the world, and I am not hungry for air.")]},
          use_fail="Not that. The lid is lead-sealed oak. It wants weight and iron."),
        P("coffin2", "coffin", "ebony", 0.0, -1.0, name="My open coffin", radius=1.0, cond=F + "lid_open", look="Torn open, from within. A year ago I would have called that impossible."),
        P("tomb1", "tomb", "stone_tomb", -3.0, -2.0, name="My father's tomb", radius=0.9, look="'Vlad Dracul, Knight of the Dragon.' Beside it, a smaller slab: 'Mircea, his son,' for my elder brother, whom I never knew."),
        P("tomb2", "tomb", "stone_tomb", 3.0, -2.0, name="Tomb of my mother", radius=0.9, look="The dragon is cut on the lid, but her face is not. She always said the dragon would be enough."),
        P("candle", "candelabra", "default", -3.2, 1.6, name="Votive candles", radius=0.3, look="They were lit when I was carried in. Each one burned down and was replaced, until someone ceased to replace them."),
        P("column1", "column", "stone_tomb", -1.6, 0.6, radius=0.4),
        P("column2", "column", "stone_tomb", 1.6, 0.6, radius=0.4),
        P("door", "door", "ebony", 0.0, -3.8, name="The crypt door", radius=0.6, look="Iron-bound and stoutly barred from the other side. A recess in the lock is shaped to fit the family ring.",
          go=F + "chapel", go_cond=F + "lid_open&has:" + F + "signet", go_fail="The door is barred. The lock wants the Voivode's seal. And I am still lying in a coffin."),
    ],
    npcs=[],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_tomb")])],
)

# ---------------------------------------------------------------------------------------------------------- chapel
LOC_DATA[F + "chapel"] = dict(
    cells=[3, 2], interior=True, wall="stone_grey", floor="stone_dark", ambient=AMBIENT["cold_interior"], camera=cam([3, 2]),
    lights=[dict(pos=[0, 2.4, -2.0], color="#ffaa66", energy=2.0, range=14), dict(pos=[-3, 1.8, 2.0], color="#5a60ff", energy=0.8, range=10)],
    walls=dict(north=["wall_window_4", "wall_4", "wall_window_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_4"]),
    spawn=[0.0, 2.4], spawns={F + "tomb": [0.0, 2.4]},
    props=[
        P("altar", "table", "ebony", 0.0, -3.0, name="The altar", radius=0.9, look="Where the Voivode was blessed, and where the bread of the Mass is blessed. I put my hand near it and feel nothing but cold, which tells me nothing.", talk=F + "legend"),
        P("cross", "crucifix_big", "silver", 0.0, -3.0, y=0.8, scale=0.7, name="The altar cross", radius=0.3,
          look="It is only wood and silver. I look at it for a long time. It is only a cross; it does not burn; it does not even disapprove. I should have learned something from that."),
        P("pew1", "bench", "dark", -2.4, 0.4, rot=90, name="Pew", radius=0.8, look="Where the boyars sat on feast-days with their sword-belts loosened."),
        P("pew2", "bench", "dark", 2.4, 0.4, rot=-90, name="Pew", radius=0.8, look="Where I sat as a boy, bored, drawing dragons in the dust of the prayer-book."),
        P("grave", "tomb", "stone_tomb", -4.0, -1.2, rot=90, name="Ileana's tomb", radius=0.8,
          look="A new slab, still pale, and a sprig of withered rosemary. 'Ileana Corvin, who waited.' There is a small silver ring on the stone.", talk=F + "grave_talk"),
        P("candle", "candelabra", "default", 3.0, -2.6, name="Altar candles", radius=0.3, look="Down to stubs."),
        P("rug", "rug", "red", 0.0, 1.6, radius=0.1),
        P("window", "sconce", "default", 5.0, -0.4, y=1.5, rot=-90, radius=0.1),
        P("stairs", "stairs", "stone_dark", 0.0, 3.4, name="Stair to the crypt", radius=0.7, look="Down to the family vault, where I was laid.", go=F + "tomb"),
    ],
    npcs=[
        NP("priest", "human_seward", F + "priest_v", 3.4, 1.2, rot=-90, name="Father Dragomir", look="The castle's old priest, wounded and propped against a pew. A dark stain has crept across his habit. He is looking at me the way men look at the sea before a storm.", talk=F + "priest_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_chapel")])],
)

# ========================================================================================================= DIALOGUE
DIALOGUE = {}

DIALOGUE[F + "stanciu_talk"] = D(
    "n0",
    n0=N("Stanciu", "My lord. Severin has been under siege six weeks. Boyar Vlaicu says we cannot afford the grain to relieve it. I say we cannot afford not to. The council waits for your word, and your father's seat.",
         choices=[C("What is the state of the border?", "n_border"),
                  C("Tell me of the Order of the Dragon.", "n_order"),
                  C("[Hold the council]", "n_council", cond="!" + F + "council_done"),
                  C("What must be done before I march?", "n_todo", cond=F + "council_done"),
                  C("[Leave]", end=True)]),
    n_border=N("Stanciu", "The Turk comes at us across the Danube every spring, my lord, as the tide comes up the beach. We are the beach. Your father held it for twenty years with a fist; you will have to hold it with a head.", next="n0"),
    n_order=N("Stanciu", "Your father's collar: the Dragon. The lock on the chest in your chamber bears the Order's year, not your father's. Do not mix them. The founding was in the king's reign, at the very beginning of this century, in 1408, when the Turk was still a rumour. Your father was merely accepted into it much later.", do=[{"set": F + "order_hint"}], next="n0"),
    n_todo=N("Stanciu", "The order sent to the camp must be written, sealed with the Voivode's ring, and carried. The signal on the tower should be fired to call the ridge garrison. And your brother Radu has been seen in the corridors at odd hours; I do not like corridors at odd hours. Bring your father's hammer, my lord: the men follow what they remember.", next="n0"),
    n_council=N("Stanciu", "Then to the matter. Two hundred starving villagers are camped in the courtyard. They want the granary opened. Boyar Vlaicu says the granary is the army's, and will be needed for the siege. A prince must choose, my lord, between a kindness that may cost a battle and a hardness that may cost a conscience.",
                choices=[C("Open the granary to the villagers. The army will march lighter.", "n_open"),
                         C("Close the gates. The army eats first, and the weak must bear it.", "n_closed")]),
    n_open=N("Stanciu", "(He bows, very slowly.) It is the harder choice, my lord, and perhaps the wrong one. But I will see it done, and I think you will remember it. They will.",
             do=[{"set": F + "grain_open"}, {"set": F + "council_done"}, {"journal": F + "j_council_open"}], next="n0"),
    n_closed=N("Stanciu", "(A long silence.) As you command. The gates will be shut. Some of the villagers will walk away at dawn. Some will not walk. I shall see to it that none of this is said in the Voivode's name.",
               do=[{"set": F + "grain_seized"}, {"set": F + "council_done"}, {"journal": F + "j_council_closed"}], next="n0"),
)

DIALOGUE[F + "vlaicu_talk"] = D(
    "n0",
    n0=N("Vlaicu", "My lord. Three hundred spears at your service, naturally. At my own expense, naturally. One only asks that the boyars be consulted in the matter of the spoils. Of the matter of the spoils, I have a great many thoughts.",
         choices=[C("The spoils are for the soldiers who bleed, Vlaicu.", "n_honour"),
                  C("You shall have your share when Severin is relieved.", "n_share"),
                  C("[Leave]", end=True)]),
    n_honour=N("Vlaicu", "A noble sentiment, my lord. Admirably young. I trust you will find your army grows lighter in the night when it hears it.", next="n0"),
    n_share=N("Vlaicu", "Then we understand each other. And may I say how like your father you are, in the matter of understanding.", next="n0"),
)

DIALOGUE[F + "radu_talk"] = D(
    "n0",
    n0=N("Radu", "Brother. Prince. Voivode. I never know which to use first. It is a strange thing to come home and find that everyone defers to the boy who used to cheat at dice.",
         choices=[C("You returned from the Sultan's court. How was it?", "n_court"),
                  C("[Show the letter you found]", "n_confront", cond="has:" + F + "radu_letter&!" + F + "radu_resolved"),
                  C("[Leave]", end=True)]),
    n_court=N("Radu", "Very warm, very civilised, and quite unlike what the priests say of it. They gave me a horse. I did not have to cut off anyone's head to be given a horse. I commend the arrangement.", next="n0"),
    n_confront=N("Radu", "(He reads. He does not blush. He sets it down, very exactly.) Yes. I wrote it. 'The ford at the new moon, the boyars divided, the Voivode young.' I wrote it, brother, because the Sultan's hand is longer than ours, and I wanted to be on the right end of it. I did not think it would be you who read it.",
                 choices=[C("You will leave this castle tonight. I do not want to see a Turkish banner in your wake. Go with your life.", "n_exile"),
                          C("Take him to the cells. He will answer for treason.", "n_chain")]),
    n_exile=N("Radu", "(Quiet.) You are very like father at his best, Vlad. It is not a compliment. I shall be at the Sultan's court. I shall not forget your mercy, and I think it will not be quite enough.",
              do=[{"take": F + "radu_letter"}, {"set": F + "radu_spared"}, {"set": F + "radu_resolved"}, {"journal": F + "j_radu_spared"}], end=True),
    n_chain=N("Radu", "(He smiles, with a sort of tenderness.) That, too, is like father. Do as you will. When I scream, remember who taught you to put a man in a hole.",
              do=[{"take": F + "radu_letter"}, {"set": F + "radu_chained"}, {"set": F + "radu_resolved"}, {"journal": F + "j_radu_chained"}], end=True),
)

DIALOGUE[F + "chest_lock"] = D(
    "n0",
    n0=N("The Order chest", "The dial is a ring of years, the iron cold under the thumb. 'The year the Dragon was founded.' Which year?",
         choices=[C("1431.", "n_wrong"), C("1448.", "n_wrong"), C("1408.", "n_right", cond="!" + F + "chest_open"),
                  C("[Take what is inside]", "n_in", cond=F + "chest_open&!" + F + "chest_empty"), C("[Step back]", end=True)]),
    n_wrong=N("The Order chest", "The dial turns. Nothing. A year, but not that year.", next="n0"),
    n_right=N("The Order chest", "The dial clicks over. The lid breathes up an inch on a smell of cedar and old wax.", do=[{"set": F + "chest_open"}, {"journal": F + "j_chest"}], next="n0"),
    n_in=N("The Order chest", "Under a folded cloak lie my father's collar, an Order medal, and his signet, a dragon coiled round a cross. I put the ring on, and the room seems a little smaller.",
           do=[{"give": F + "signet"}, {"give": F + "medal"}, {"set": F + "chest_empty"}], end=True),
)

DIALOGUE[F + "seal"] = D(
    "n0",
    n0=N("The seal-press", "Wax, a candle and the brass press, waiting for a ring.",
         choices=[C("[Seal the draft order with my father's ring]", "n_seal", cond="has:" + F + "draft_order&has:" + F + "signet&!has:" + F + "sealed_order&!" + F + "order_sent"),
                  C("What do I need?", "n_need", cond="!has:" + F + "sealed_order&!" + F + "order_sent"),
                  C("[Step away]", end=True)]),
    n_seal=N("The seal-press", "The wax is green. The dragon stands up out of it, tail in its teeth. For the first time in its history, the order is real.",
             do=[{"take": F + "draft_order"}, {"give": F + "sealed_order"}, {"journal": F + "j_sealed"}], end=True),
    n_need=N("The seal-press", "A written order, and the Voivode's signet. The first is on the clerk's table. The second is, I think, somewhere my father hid it.", next="n0"),
)

DIALOGUE[F + "messenger_talk"] = D(
    "n0",
    n0=N("Petru", "My lord, I can carry anything to the camp in a day and a night. But the captains won't take my word and I won't bring them a word they cannot read.",
         choices=[C("[Give him the sealed order]", "n_send", cond="has:" + F + "sealed_order"),
                  C("[Wait; the order is not ready]", end=True, cond="!has:" + F + "sealed_order&!" + F + "order_sent"),
                  C("Ride well.", end=True, cond=F + "order_sent")]),
    n_send=N("Petru", "The levy will be at the camp below the Reed ford by the third night, my lord. God keep you.",
             do=[{"take": F + "sealed_order"}, {"set": F + "order_sent"}], end=True),
)

DIALOGUE[F + "ileana_talk"] = D(
    "n0",
    n0=N("Ileana", "You have your father's chair and your father's frown. Both look better on him. Are you going to speak to me, or only to your counsellors?",
         choices=[C("I am afraid, Ileana.", "n_afraid"),
                  C("What do you think of Radu?", "n_radu"),
                  C("I will come back.", "n_back", cond=F + "council_done&!" + F + "ileana_token"),
                  C("[Leave]", end=True)]),
    n_afraid=N("Ileana", "Of course you are. If you were not, I would marry Radu instead. (She smiles, and it hurts.) Fear is not the enemy. Not knowing what to do with it is.", next="n0"),
    n_radu=N("Ileana", "He comes into this room when you are away. He looks at your desk, not at me. A man who looks at a desk is a man deciding what to do with the room.",
             do=[{"set": F + "ileana_warned"}], next="n0"),
    n_back=N("Ileana", "Say it again when you are in the doorway, Vlad, with the army behind you. I will believe it then. (She presses a ribbon of grey silk into his palm.) For a ring, until you have time to buy another.",
             do=[{"give": F + "ribbon"}, {"set": F + "ileana_token"}], next="n0"),
)

DIALOGUE[F + "sentry_talk"] = D(
    "n0",
    n0=N("Dan", "The ridge answers if we fire the beacon, my lord. There's a platoon on the far crag, forty spears. But the beacon's dry as a priest's sermon. It wants lamp-oil, and a torch to set it going. The oil is down in the hall: the garrison barrel. The torch is in the bracket by the stair-door; the others are burned out.",
         choices=[C("Thank you, Dan.", end=True)]),
)

DIALOGUE[F + "refugee_talk"] = D(
    "n0",
    n0=N("The grandmother", "You are the new Voivode. You have your father's eyes, and your father's chin. Your father left the villages out of his reckoning. I hope you will count us in.",
         choices=[C("Where have you come from?", "n_from"),
                  C("Take what you need from my pack.", "n_gift", cond="!" + F + "refugee_fed"),
                  C("[Leave]", end=True)]),
    n_from=N("The grandmother", "From beyond Severin, where the Turk has been burning the barns. We walked ten days. The wolves have followed us for three. They are patient, my lord. Wolves usually are.", next="n0"),
    n_gift=N("The grandmother", "Then God bless you, young lord. It is the first kind word I have had from a man in armour.",
             do=[{"set": F + "refugee_fed"}, {"journal": F + "j_refugee"}], next="n0"),
)

DIALOGUE[F + "mircea_talk"] = D(
    "n0",
    n0=N("Mircea", "My lord. The scouts say the Turk will raid across the river before dawn, in the dark of the moon. They cannot cross at the Stone Ford, nor the Wolf's Ford. We should know which. You will find the map on the table.",
         choices=[C("What do you remember of Kossova, Captain?", "n_kossova"),
                  C("What do the men say of me?", "n_men"),
                  C("[Leave]", end=True)]),
    n_kossova=N("Mircea", "Don't ask. I was a boy. Three days in the heat, and on the third the Hungarian king ran, and the Crescent stood in the field where we had been. Your father said afterwards that the shame was not that we had lost but that we had not been trusted to lead.", next="n0"),
    n_men=N("Mircea", "They say you are your father's son. Some say it to praise you. Some say it as a warning.",
            choices=[C("Then I will be both.", "n0"), C("[Say nothing]", "n0")]),
)

DIALOGUE[F + "cristea_talk"] = D(
    "n0",
    n0=N("Cristea", "My lord. I lay in the reeds two nights. They are coming down the old creek bed in the dark, from the north-east. They walk their horses, they wrap the hooves in felt: no clatter on stone, no splash. It must be a place with reeds to hide in and soft mud to cross; not a rocky ford.",
         choices=[C("And Wolf's Ford?", "n_wolf"), C("And the Stone Ford?", "n_stone"), C("[Leave]", end=True)]),
    n_wolf=N("Cristea", "Four hours upstream, past the old mill, west of the hills. They would have to march round the whole army to reach it. No, my lord.", next="n0",
             do=[{"set": F + "scout_report"}]),
    n_stone=N("Cristea", "A causeway of slabs, a quarter-mile of echoes. A felt-wrapped horse is still a horse. They would not choose it. It is too proud a crossing for a night raid.", next="n0",
              do=[{"set": F + "scout_report"}]),
)

DIALOGUE[F + "prisoner_talk"] = D(
    "n0",
    n0=N("The Akinji", "(He speaks a little Wallachian, with the care of a man spelling a word he hates.) I will not talk. I am of the Sultan's household. You may do what you please.",
         choices=[C("[Offer him water and a blanket, and ask him plainly]", "n_parley", cond="!" + F + "prisoner_done"),
                  C("[Threaten him with the boot and the iron]", "n_break", cond="!" + F + "prisoner_done"),
                  C("[Leave him]", end=True)]),
    n_parley=N("The Akinji", "...I did not expect it. (He drinks.) We cross at the Reed Ford, where the river is slow, before dawn. Do not harm the reeds. My cousins are in them. If you must kill, kill quickly. That is all I ask.",
               do=[{"set": F + "prisoner_done"}, {"set": F + "prisoner_parley"}, {"set": F + "scout_report"}, {"journal": F + "j_prisoner_parley"}], end=True),
    n_break=N("The Akinji", "(He talks, white-faced, for a quarter of an hour. When he is finished he does not look at me, and I do not look at him.) The Reed Ford. The reed-ford. Before dawn. I have told you everything. Cut my cords.",
              do=[{"set": F + "prisoner_done"}, {"set": F + "prisoner_broken"}, {"set": F + "scout_report"}, {"journal": F + "j_prisoner_broken"}], end=True),
)

DIALOGUE[F + "map_lock"] = D(
    "n0",
    n0=N("The map", "Three fords marked in red wax. The scout says the Turks are coming down the old creek from the north-east, with felt on their hooves, to a place with reeds and soft mud. Where do I put the army?",
         choices=[C("The Stone Ford.", "n_stone"), C("Wolf's Ford.", "n_wolf"), C("The Reed Ford.", "n_reed", cond="!" + F + "ford_known"),
                  C("[Walk to the ford]", "n_go", cond=F + "ford_known"), C("[Step back]", end=True)]),
    n_stone=N("The map", "A causeway of slabs. A quarter-mile of echoes. They would not choose a ford where every hoof rings.", next="n0"),
    n_wolf=N("The map", "Four hours upstream, far from the north-east creek. The Turks would have to round the whole army to reach it.", next="n0"),
    n_reed=N("The map", "The wax shows a broad slow river, reed-banks on both shores. A creek runs in from the north-east. It is the one place where felt-wrapped horses would make no sound. I move the stones.",
             do=[{"set": F + "ford_known"}, {"journal": F + "j_map"}], next="n0"),
    n_go=N("The map", "[You take the track to the river]", do=[{"goto": F + "ford"}], end=True),
)

DIALOGUE[F + "hermit_talk"] = D(
    "n0",
    n0=N("The scholar", "A quick sword, Voivode. A quicker mind. A pity both are in service of a throne which has just been sold. Do you know that? The ford was told to the enemy by one of your own. You were meant to lose tonight.",
         choices=[C("Who are you?", "n_who"), C("Who sold the ford?", "n_sold"), C("What do you want of me?", "n_want"),
                  C("[Go with him to the school]", "n_go", cond=F + "asked_who"), C("[Send him away]", end=True)]),
    n_who=N("The scholar", "A man who collects those who do not wish to end. I keep a school, under a mountain, by a lake in Hermannstadt. A small school, ten places at a time. The tenth is the Devil's. Everyone is told that. Nobody believes it until the end of term.", do=[{"set": F + "asked_who"}], next="n0"),
    n_sold=N("The scholar", "I could tell you. But a prince should learn to read faces himself. You will read your brother's face long before you read my school-books.", next="n0"),
    n_want=N("The scholar", "To teach you to be a king who is not beaten, Voivode. Not by Turks. Not by brothers. Not by time. The price is a winter of your life and a risk you will be told about in plain language. Come, if you dare.", do=[{"set": F + "asked_who"}], next="n0"),
    n_go=N("The scholar", "Then take this token. It will open the ferry to those who carry it. Nine days' ride, and we shall begin.",
           do=[{"give": F + "token"}, {"set": F + "scholar_agreed"}, {"journal": F + "j_hermit"},
               {"card": "The Voivode held the ford that night, and the Turks went home across the water with fewer men than they came with. But the betrayal at Severin was done, and the border fortress fell on the third day. It was the first victory he could not enjoy. He went with the pale scholar the next dawn, without a word to any of his captains, to the school under the mountain that takes every tenth of its sons."},
               {"goto": F + "lake"}], end=True),
)

DIALOGUE[F + "ferryman_talk"] = D(
    "n0",
    n0=N("The ferryman", "(No sound. A long, pale finger points at the open palm. Then, in a voice like water in a cistern:) The toll. One silver, from a scholar's own hand.",
         choices=[C("[Pay the silver coin]", "n_pay", cond="has:silver&has:" + F + "token&!" + F + "toll_paid"),
                  C("[I have no coin]", "n_nocoin", cond="!has:silver&!" + F + "toll_paid"),
                  C("[The toll is paid already]", "n_paid", cond=F + "toll_paid"),
                  C("[Wait]", end=True)]),
    n_pay=N("The ferryman", "(The coin vanishes. The gull on his shoulder does not stir.) Board, scholar. Do not look at the water.", do=[{"take": "silver"}, {"set": F + "toll_paid"}], end=True),
    n_nocoin=N("The ferryman", "Nine fall short; the tenth pays more. A coin lies in the cairn, with the drowned scholar's cross. He kept it. He kept it badly.", end=True),
    n_paid=N("The ferryman", "Board.", end=True),
)

DIALOGUE[F + "master_talk"] = D(
    "n0",
    n0=N("The Master", "Voivode. You came. I remember very few who come. The winter is long and the lessons are plain. First, the lesson of names: every thing has a name that is not its name. Learn to speak to a thing in the voice it hears itself in.",
         do=[{"set": F + "master_met"}],
         choices=[C("What is the rite I must learn?", "n_rite"),
                  C("I want to read your library.", "n_lib"),
                  C("What is the tithe?", "n_tithe"),
                  C("[Leave]", end=True)]),
    n_rite=N("The Master", "Three vessels, three acts, and an order that matters more than any of them. It is written in the Clavis Minor, in the library. A scholar who cannot read it will not be able to perform it, and a scholar who cannot perform it will not earn the stair.", next="n0"),
    n_lib=N("The Master", "The key is Vasile's. I give nothing away; the school teaches by taking. You must get it from him as best you can. Princes are used to getting things from men.", next="n0"),
    n_tithe=N("The Master", "When the winter ends, ten scholars sit in a ring. One is the Devil's. He pays the tuition of all of us. Don't look so grave, Voivode. It is only a custom. The roll in the library says whose turn it is.", next="n0"),
)

DIALOGUE[F + "vasile_talk"] = D(
    "n0",
    n0=N("Vasile", "The new boy. A prince in a scholar's gown. I have the key to the library, you know. The Master gave it to me because I do not want what is in it. You do. That makes you very interesting.",
         choices=[C("[Offer him your friendship, and a share of what you learn]", "n_friend", cond="!has:" + F + "library_key"),
                  C("[Lay a hand on the dagger and ask for the key]", "n_cow", cond="!has:" + F + "library_key"),
                  C("What are you running from, Vasile?", "n_from"),
                  C("[Leave]", end=True)]),
    n_friend=N("Vasile", "(He laughs, a surprised, boyish laugh.) You are very strange, Vlad. All right. A share. But the first thing you learn, you'll teach me. (He lifts the cord over his head.) Do not lose it. And do not lose me.",
               do=[{"give": F + "library_key"}, {"set": F + "vasile_friend"}, {"journal": F + "j_vasile_friend"}], end=True),
    n_cow=N("Vasile", "(He goes quite white, and does not move.) You would not. (A long breath.) Take it. Take it. I'll remember this when I'm Master.",
            do=[{"give": F + "library_key"}, {"set": F + "vasile_cowed"}, {"journal": F + "j_vasile_cowed"}], end=True),
    n_from=N("Vasile", "From a town that taught me my place and then did not give me one. My father drank, my mother prayed and nobody did either well. I came here to be taken seriously.", next="n0"),
)

DIALOGUE[F + "teodor_talk"] = D(
    "n0",
    n0=N("Teodor", "They say one of us goes down the stair at the end of the winter, my lord. They say it is chosen by the roll. They say the roll can be read by anyone with the key, and altered by anyone with ink. I have not said any of this.",
         choices=[C("Where is the ink kept?", "n_ink"), C("[Leave]", end=True)]),
    n_ink=N("Teodor", "Everywhere, and nowhere. The Master leaves a pot out for the beginners and moves it every night. Look where a clerk would put it, and where a child would hide it.", next="n0"),
)

DIALOGUE[F + "maria_talk"] = D(
    "n0",
    n0=N("Maria", "I have learned to call the weather. It takes about three hundred hours and the loss of one's eyebrows. Do not look at me like that, prince. Do not look at any of us like that. We are all here for the same reason: nobody at home was going to teach us anything.",
         choices=[C("What is the third lesson?", "n_third"), C("[Leave]", end=True)]),
    n_third=N("Maria", "The Wolf-Tongue. In the spring the Master takes us out on the heath and teaches us to call the beasts of the wood. A wolf-tooth is the pledge. If you have ever fought wolves, they may remember you.", next="n0"),
)

DIALOGUE[F + "altar_lock"] = D(
    "n0",
    n0=N("The rite-altar", "Three hollows: a bowl, a disc, a lamp. Water, silver, flame. In what order do I begin?",
         choices=[C("[Water first]", "n_w", cond="!" + F + "rite_done"),
                  C("[Silver first]", "n_bad", cond="!" + F + "rite_done"),
                  C("[Flame first]", "n_bad", cond="!" + F + "rite_done"),
                  C("[Step back]", end=True)]),
    n_bad=N("The rite-altar", "The hollow cracks with cold and the stone spits. The order is wrong. I must start again.", next="n0"),
    n_w=N("The rite-altar", "Water in the bowl. The hollow drinks. What next?",
          choices=[C("[Silver]", "n_ws"), C("[Flame]", "n_bad")]),
    n_ws=N("The rite-altar", "The disc settles. The stone hums. And last?",
           choices=[C("[Flame]", "n_wsf"), C("[Water again]", "n_bad")]),
    n_wsf=N("The rite-altar", "The lamp lights without a match. The three hollows glow, and a cold calm falls on the room. I feel, for a moment, that I have been heard.",
            do=[{"set": F + "rite_done"}, {"journal": F + "j_rite"}], end=True),
)

DIALOGUE[F + "roll_talk"] = D(
    "n0",
    n0=N("The Roll", "A scroll as tall as a man. Ten names for this winter, in this order: Nicolae. Gheorghe. Vasile Cernat. Maria. Teodor. Anca. Bogdan. Lupu. Cosmin. And, last, in ink still wet: Vlad, Voivode of the Wallachians. The tenth to enter is the Devil's.",
         do=[{"set": F + "roll_seen"}],
         choices=[C("[Leave the roll as it is]", end=True),
                  C("[Dip the quill and write Vasile Cernat in the last place]", "n_forge", cond="has:" + F + "ink&!" + F + "forged"),
                  C("[I have no ink to change it]", "n_noink", cond="!has:" + F + "ink&!" + F + "forged"),
                  C("[Step back]", end=True)]),
    n_forge=N("The Roll", "The quill scratches. I have made a name that was Vlad's into one that is not. I have made a tenth out of a man who did nothing but tell me the truth. The ink dries at once, and does not look wet or recent. The roll accepts it, as paper accepts anything.",
              do=[{"set": F + "forged"}, {"journal": F + "j_forged"}], end=True),
    n_noink=N("The Roll", "The last line is wet and sullen. A change would need ink, and I have none.", end=True),
)

DIALOGUE[F + "tithe_talk"] = D(
    "n0",
    n0=N("The Master", "The winter is over. Ten stand in the ring. The roll is read. (He turns the scroll in the green light.)",
         choices=[C("[Listen]", "n_self", cond="!" + F + "forged"), C("[Listen]", "n_vasile", cond=F + "forged")]),
    n_self=N("The Master", "The tenth to enter is the tenth to pay. It is you, Voivode: Vlad, son of Vlad, of the House of the Dragon. It is an honour of a kind. It is not an easy one.",
             choices=[C("I will pay. It was my choice to come.", "n_pay"),
                      C("Take Vasile Cernat. He is the better scholar, and the weaker man.", "n_betray")]),
    n_pay=N("The Master", "(A long, slow smile.) Good. Hold my hand. Below the grate a sound like a great beast breathing grows loud, and then it gathers itself, and rises. When it reaches you, I think you will not scream. You will never scream again.",
            do=[{"set": F + "tithe_self"}, {"give": F + "black_book"}, {"set": F + "tithe_done"}, {"journal": F + "j_tithe_self"}], next="n_end"),
    n_betray=N("The Master", "(Interested.) A prince's choice, quick and cold. Very well. The name, spoken in the ring, becomes the debt. Vasile, come. Do not weep: you have been a good scholar.",
               do=[{"set": F + "tithe_vasile"}, {"give": F + "black_book"}, {"set": F + "tithe_done"}, {"journal": F + "j_tithe_vasile"}], next="n_end"),
    n_vasile=N("The Master", "(He reads, and stops. His eyes, for a moment, flick to mine.) The tenth to enter is Vasile Cernat. (A pause.) Strange. I had remembered it otherwise. But the roll says what the roll says, and the debt follows the ink. A prince's art, Voivode. I should have guessed.",
               do=[{"set": F + "tithe_vasile"}, {"give": F + "black_book"}, {"set": F + "tithe_done"}, {"journal": F + "j_tithe_vasile"}], next="n_end"),
    n_end=N("The Master", "The term is ended. Whatever comes up that stair belongs to the Devil and the one he leaves behind. Take this book, Voivode. It teaches the speech of wolves and the weather. It is a poor payment for what you have just seen, and it is the one I give. Go home. Rule. You will not need to wait for death to find a kind of eternity.",
            do=[{"card": "He left the school with a book of black leather, a ring of pale grey rime that never melted from his hand, and a voice that wolves came to when he spoke. Some years later, the Turk crossed the river again and the Voivode rode out to meet him, and did not ride home. The boyars carried him back by night in a closed bier, and Father Dragomir said the office over him in a hurry, and sealed the vault with lead. They were wrong to think that this was the end of it."},
                {"goto": F + "tomb"}], end=True),
)

DIALOGUE[F + "grave_talk"] = D(
    "n0",
    n0=N("Ileana's tomb", "'Ileana Corvin, who waited.' The ring on the stone is the silver ring I never gave her, which she must have had made herself.",
         choices=[C("[Take the ring]", "n_ring", cond="!has:" + F + "ring"), C("[Stay a moment]", "n_stay"), C("[Leave]", end=True)]),
    n_ring=N("Ileana's tomb", "It is very small. I can close my fist around it. I do not know why that is the thing that finally does it.", do=[{"give": F + "ring"}, {"set": F + "grave_visited"}], next="n0"),
    n_stay=N("Ileana's tomb", "'Say it again when you are in the doorway, Vlad,' she said. I am in the doorway. She is not here. I say it anyway.", do=[{"set": F + "grave_visited"}], next="n0"),
)

DIALOGUE[F + "priest_talk"] = D(
    "n0",
    n0=N("Father Dragomir", "(He tries to rise, and fails.) My lord. You are... You are cold. I sealed you myself. I said the office. And yet you stand there, and the candle does not move when you breathe. (He is quite still.) Forgive me. Are you my Voivode, or something he has become?",
         choices=[C("I am your Voivode, Father. Tell me what has happened.", "n_tell"),
                  C("What of the Turks?", "n_turks"),
                  C("What of Ileana?", "n_ileana"),
                  C("[Leave him]", end=True)]),
    n_tell=N("Father Dragomir", "The Turks took the gate the night you were laid in the vault. The boyars have gone; Vlaicu to the Sultan, they say. I stayed. Someone had to. I took a spear in the side defending the door I ought to have barred, and I think, my lord, that I will not see the morning.",
             do=[{"set": F + "priest_heard"}], next="n0"),
    n_turks=N("Father Dragomir", "They have the courtyard and the gate, and the boyars have gone, Vlaicu to the Sultan, they say.",
              do=[{"set": F + "priest_heard"}],
              choices=[C("And Radu?", "n_radu_s", cond=F + "radu_spared"), C("And Radu?", "n_radu_c", cond=F + "radu_chained")]),
    n_radu_s=N("Father Dragomir", "He rides with them, under the Sultan's green banner. You gave him his life, my lord, and he has used it to take yours.", next="n0"),
    n_radu_c=N("Father Dragomir", "He died in the cells, in the first cold. The village has not forgiven you, and does not mean to.", next="n0"),
    n_ileana=N("Father Dragomir", "She waited, my lord. She came every morning to the tower. When the news came, she walked into the lake and the people found her ring on the shore. I buried her under the stone. You will see it. She said you would come back. She said it quite crossly.",
               do=[{"set": F + "priest_heard"}], next="n0"),
)

DIALOGUE[F + "legend"] = D(
    "n0",
    n0=N("The altar", "I am standing at the altar of my own chapel, a hundred paces from where I was laid. A priest who may die by dawn lies against a pew. A wolf is howling in the hills; I understand it. I understand every word. And I am more thirsty than I have ever been. Nobody is here to tell me what to do. That, I think, is the whole point.",
         choices=[C("[Take what I need from the dying priest]", "n_priest", cond=F + "priest_heard"),
                  C("[Go out to the hills and call the wolves]", "n_wolves", cond=F + "priest_heard&has:" + F + "black_book"),
                  C("[Kneel by Ileana's tomb and wait for the sun, whatever it may do]", "n_vigil", cond=F + "priest_heard&" + F + "grave_visited"),
                  C("[I cannot decide yet]", end=True)]),
    n_priest=N("The Voivode", "He does not scream, which is the worst of it. He puts out one hand, as if to bless me, and then it falls. I think he understood. I think he forgave me. I cannot be sure which is the greater sin.",
               do=[{"set": F + "end_priest"}], next="ep_radu"),
    n_wolves=N("The Voivode", "I open the doors and call, in a tongue taught under a mountain. They come out of the dark with their breath steaming, and I choose the weakest, an old one, whose time was nearly done. It is not what I wanted. It will keep a priest alive. It will keep the chapel's door unbarred.",
               do=[{"set": F + "end_wolves"}], next="ep_radu"),
    n_vigil=N("The Voivode", "I kneel by her stone with her ring in my fist and ask whatever I have become to wait for the sun. The sun rises. It does not kill me: it only turns the whole world to glass, and the priest, who is still alive, sees that I am weeping, and says my name, and dies.",
              do=[{"set": F + "end_vigil"}], next="ep_radu"),
    ep_radu=N("The Voivode", "I remember Radu.", choices=[C("[Remember him]", "ep_r_spared", cond=F + "radu_spared"), C("[Remember him]", "ep_r_chained", cond=F + "radu_chained")]),
    ep_r_spared=N("The Voivode", "A brother sent away alive, with a green banner at his back.",
                  do=[{"card": "His brother Radu, whom he had spared, returned with the Sultan's army and was given the throne of Wallachia as a prize. He ruled it quietly, and was loved by nobody and feared by nobody. He died in bed. It was, in its way, the cruellest outcome."}], next="ep_tithe"),
    ep_r_chained=N("The Voivode", "A brother left to rot in a cell, and the village that watched me do it.",
                   do=[{"card": "His brother Radu, whom he had chained, died in the cells within the winter, and his name was struck from the family roll. The castle's servants learned the new Voivode's justice and did not forget it. When the Turks came, nobody manned the walls with any enthusiasm."}], next="ep_tithe"),
    ep_tithe=N("The Voivode", "I remember the school.", choices=[C("[Remember it]", "ep_t_self", cond=F + "tithe_self"), C("[Remember it]", "ep_t_vasile", cond=F + "tithe_vasile")]),
    ep_t_self=N("The Voivode", "I paid what I owed, in the coin I chose.",
                do=[{"card": "At the school, the Voivode had stood in the ring and taken the tithe upon himself. The Master was fascinated by this. Vasile Cernat, who lived and was a scholar to the end of his days, taught for a time at the Scholomance and left behind a book of lessons that Van Helsing would later read with a chill."}], next="ep_end"),
    ep_t_vasile=N("The Voivode", "I paid what I owed with another man's life.",
                  do=[{"card": "At the school, a name in wet ink had moved the tithe from one scholar to another. Vasile Cernat went down the stair and was not seen again. The Master never reproached the Voivode for it. It was a very princely art, and he set it among his best lessons."}], next="ep_end"),
    ep_end=N("The Voivode", "The thirst, the choice, the debt. Seven hundred years, and not one day of them without the memory.",
             choices=[C("[Remember the priest]", "ep_end_priest", cond=F + "end_priest"), C("[Remember the wolves]", "ep_end_wolves", cond=F + "end_wolves"),
                      C("[Remember the vigil]", "ep_end_vigil", cond=F + "end_vigil")]),
    ep_end_priest=N("The Voivode", "...",
                    do=[{"journal": F + "j_end_priest"}, {"card": "The Voivode rose at dusk, and fed on the only warm thing in the chapel. It was the first death for which he was, in the strictest sense, responsible. It would not be the last. By the time the Turks left the castle, he had gone into the hills, and the village learned to leave a door unbarred for the lord who no longer slept. Seven hundred years passed. The hunger did not."},
                        {"arc_end": 1}], end=True),
    ep_end_wolves=N("The Voivode", "...",
                    do=[{"journal": F + "j_end_wolves"}, {"card": "The Voivode rose at dusk, and learned that the beasts of the hills would keep his secret. He fed on the old and the dying, and left the living to their hearths. The shepherds called him the Wolf-Lord, and their children's children told it to strangers, and in time Harker heard it. In the strictest sense, he never took a man's life. It was a very thin sense, and he knew it. Seven hundred years passed."},
                        {"arc_end": 1}], end=True),
    ep_end_vigil=N("The Voivode", "...",
                   do=[{"journal": F + "j_end_vigil"}, {"card": "The Voivode rose with the sun and was not destroyed. He was something worse: the same man, with the same thirst, in a different world. At dusk he took Ileana's ring and went out. He did not feed that night, nor the next, nor for a long time, and he grew very strange and very sorrowful. Eventually he did, and the bell in the village was never rung for it. Seven hundred years passed."},
                       {"arc_end": 1}], end=True),
)

# ========================================================================================================= ITEMS
ITEMS = {
    F + "signet": dict(name="The Voivode's dragon signet", asset="key", variant="gold", desc="A dragon coiled round a cross, worn smooth by three generations of princes."),
    F + "medal": dict(name="Order of the Dragon medal", asset="key", variant="gold", desc="My father's medal, silver-gilt. 'O quam misericors est Deus', and on the reverse the dragon biting its own tail."),
    F + "charm": dict(name="Wolf-tooth charm", asset="key", variant="gold", desc="A grey wolf's fang, set in iron and hung on a thong. It does not keep wolves off. It tells them who you are."),
    F + "warhammer": dict(name="My father's war-hammer", asset="hammer", variant="default", desc="Iron-headed, ash-hafted, notched on the left. It has killed men on the Danube and it can break a lead seal."),
    F + "draft_order": dict(name="Draft order to the levy", asset="book", variant="diary", desc="The captains of the levy are to assemble at the camp. Unsealed, it is only a clerk's handwriting."),
    F + "sealed_order": dict(name="Sealed order to the levy", asset="book", variant="red", desc="A dragon stands up in green wax. The order is the Voivode's now."),
    F + "radu_letter": dict(name="Radu's letter", asset="book", variant="leather", desc="'The ford at the new moon. The boyars are divided. The Voivode is young.' Signed with a Turkish cipher and, below, in a hand I know, an R."),
    F + "ribbon": dict(name="Ileana's grey ribbon", asset="book", variant="diary", desc="A length of grey silk, still faintly perfumed with rosemary."),
    F + "token": dict(name="Scholar's token", asset="key", variant="gold", desc="A disc of black iron stamped with a wolf's mouth. Open to those who carry it."),
    F + "library_key": dict(name="The library key", asset="key", variant="gold", desc="Black iron, shaped like a wolf's head. The lock it opens is shaped like a mouth."),
    F + "ink": dict(name="Pot of black ink", asset="bottle", variant="amber", desc="Ink that dries at once and looks a year old."),
    F + "black_book": dict(name="The Master's black book", asset="book", variant="leather", desc="Lessons in the speech of beasts and the calling of weather, in a hand like barbed wire."),
    F + "ring": dict(name="Ileana's silver ring", asset="key", variant="gold", desc="A small silver ring, cut for a hand that never wore it."),
    F + "standard": dict(name="Broken Akinji standard", asset="signpost", variant="oak", desc="A green horse-tail on a snapped spear, with a tin crescent."),
}

# ========================================================================================================= JOURNAL
J = lambda title, text: dict(title=title, source="The Voivode's own account", text=text)
JOURNAL = {
    F + "j_hall": J("The hall at Severin's hour", "My father is two years dead and I am nineteen. The council meets in his hall, in his chair, with his crest on the wall, and not one man here believes I will keep it. Severin burns on the border. They look at me as at a candle, wondering how long before the draught."),
    F + "j_chamber": J("My father's chamber", "I sleep here now, or fail to. There is a chest with a dial, a stand of armour, a portrait of a man I could not please, and Ileana by the window. I was a boy in this room. It has since decided I am not."),
    F + "j_chest": J("The Order's year", "The Order of the Dragon was founded in 1408; my father was invested in 1431. The Order is older than the man. I have been inclined to forget that the men who wear a thing are less than the thing. The chest opened with the older date, the right date. It is a lesson."),
    F + "j_sealed": J("The sealed order", "A dragon in green wax. The levy has been a clerk's wish for a week. In one moment, with my father's ring, it becomes an army. I hope no man ever learns how easily paper becomes blood."),
    F + "j_council_open": J("The granary opened", "Two hundred villagers fed from the army's store. Vlaicu stormed and Stanciu bowed. The men will march on thinner rations, and the village will remember who fed it. I do not know whether I have done wisely. I know it is what I would want done to me."),
    F + "j_council_closed": J("The gates closed", "I told the villagers they could not have the grain, and the army ate. Some of the villagers walked away at dawn. Not all of them could. Stanciu says it was prudent, and does not meet my eyes. The army is fed. I cannot be sure of the rest of us."),
    F + "j_radu_spared": J("Radu sent away", "I read the letter aloud to Radu, and then I let him go. He walked out of the gate with a cloak and a horse, and his face was the face of a boy who has been caught and not whipped. I will see him again, and I will not know what he intends."),
    F + "j_radu_chained": J("Radu in the cells", "I read the letter aloud to Radu and gave him to the guard. He did not resist. The key in my hand felt as though it belonged to some more severe person. My brother is below my feet in the dark, and I tell myself it is justice."),
    F + "j_tower": J("The beacon on the tower", "Old Dan told me what the tower needs: lamp-oil from the hall and a torch from the stair-door bracket. Without a signal the ridge garrison will not know we have left. I am a prince whose first order is to arrange a bonfire."),
    F + "j_beacon": J("The ridge answers", "Oil, a torch, and a pillar of fire above the pass. Across the valley a small light answered, and then another. Forty spears on the far crag. I stood and watched it burn until Dan said politely that the wind would soon turn the sparks onto the thatch."),
    F + "j_road": J("The hungry road", "The levy goes one way down the mountain and the refugees come the other, and between them the road is no wider than a wagon. A child asked me if the Turk had a face. I said yes. She asked if I had seen it. I said no. She nodded, as one who knew better."),
    F + "j_refugee": J("The grandmother", "I gave her bread and a blanket from my pack. She did not thank me for the bread, only for the blanket. She said the bread was just, but the blanket was kind, and kindness was the thing nobody had spared for her. It cost me nothing, and I am still thinking of it."),
    F + "j_camp": J("The army's camp", "A hundred fires, ten thousand men, and none of them certain whose war this is. Mircea tells stories of Kossova and I try not to look too closely at what he leaves out. I am to put them in a ford by the dark of the moon, and I do not yet know which."),
    F + "j_prisoner_parley": J("The Akinji's name", "He gave me his name, Ahmed, and the ford, for a blanket and a cup of water. The old way says never trust a captive. The newer way, mine, says never trust a man you have starved. I think I am a poor student of both."),
    F + "j_prisoner_broken": J("The Akinji, broken", "He told me the ford. It took a quarter of an hour. I do not intend to remember how it was done, and I know I shall remember nothing else. Mircea, who has seen worse, put his hand on my shoulder and said it was necessary. That is how it begins."),
    F + "j_map": J("The Reed Ford", "Felt on the hooves, reeds on the banks, a creek from the north-east: the Stone Ford would ring, and the Wolf's Ford is too far. Reed Ford it must be. I placed three hundred spears among the reeds myself, and a hundred archers at the bend, and then I waited."),
    F + "j_ford": J("The night raid", "They came as Cristea said, low and silent, with their horses in felt. I never knew how loud a river could be until it was full of men trying not to be heard. The first one saw me at ten paces. I had my father's hammer, and I did not hesitate."),
    F + "j_hermit": J("The pale scholar", "He knew what I had not told my captains: that the ford was sold. I did not ask who sold it. I think I knew. He offered me a school, and a lesson, and an eternity, in the voice of a man selling a horse. I took the token. I cannot say why, except that I was tired of being beaten."),
    F + "j_lake": J("Lake Hermannstadt", "A black lake, a ferryman with no breath and a mountain with its door open. 'The tenth pays more,' said the scratched post. I did not ask what. I paid the first toll in silver, taken from a drowned scholar's cairn. It felt like stealing from a man who was too proud to mind."),
    F + "j_school": J("The Scholomance", "A stone school under the mountain. The Master teaches with the amused patience of a thing that has had a thousand pupils and remembers each. The lessons are of names, of weather, of the speech of wolves. Nobody laughs. Nobody leaves. In spring, they say, the tenth is taken."),
    F + "j_vasile_friend": J("Vasile's key", "I offered him a share of what I learned instead of a threat. He looked at me as though I had spoken Greek, and then he laughed, and gave me the key. It is a small thing. I find I am proud of it, and ashamed that I am surprised."),
    F + "j_vasile_cowed": J("Vasile's key", "I laid a hand on my dagger and Vasile gave me the library key as quickly as a child gives up an apple. He has not spoken to me since. I did not need to draw. That, I suppose, is what a prince's reputation is for."),
    F + "j_library": J("The forbidden library", "Chained books, black candles and a cold that has nothing to do with the weather. I read the Clavis Minor with my teeth clenched. Water to open the way, silver to bind, flame to seal. The order matters more than the things. It always does."),
    F + "j_rite": J("The rite of three", "Water, silver, flame. The altar accepted them in that order and hummed like a struck bell. I felt, for one moment, that something large had noticed me and been pleased. I do not know how to make that feeling stop being pleasant."),
    F + "j_tithe": J("The tithe chamber", "Ten seats in a ring, a green fire that gives no heat and, below the floor, something breathing. The Master read the roll in a flat kind voice. Nobody looked at anyone else. Everyone knew that one of us would not be rising from the ring."),
    F + "j_forged": J("The tenth name", "I wrote another man's name in my place. The ink dried at once. I told myself it was a prince's choice, and that Vasile would have done the same, and that it made no difference to the Master. The more I told myself, the less any of it was true."),
    F + "j_tithe_self": J("The tenth pays", "I stood in the ring and said that the tenth was mine. The Master was surprised, I think, and then very attentive. Something came up out of the grate. I do not remember what happened, only that I was cold when it ended and have been, since, one way or another."),
    F + "j_tithe_vasile": J("Vasile's debt", "Vasile went down the stair with his head up. I saw his face as he passed, and I will see it as long as I have eyes. He did not accuse me. That was the cruellest thing he could have done, and I think he knew."),
    F + "j_tomb": J("The family crypt", "I woke in a box. I have no idea how long. My throat was dry, and my father's stone lay on the left, and there was a scratching in my mouth as if my teeth were something else. The lid was lead-sealed, and I was strong enough to want it open."),
    F + "j_chapel": J("The chapel, my first night", "The altar candles are down to stubs and the doors are unbarred. A priest lies against a pew with a spear-wound. Ileana's tomb is new. The hunger in me is not a hunger I know the name of, and I am afraid it knows mine."),
    F + "j_end_priest": J("The first blood", "I took what I needed from Father Dragomir. He did not resist. That was what was unbearable. He had given me the sacraments at my christening, and I gave him this. Whatever begins here, it begins with a priest's blood and my own choice."),
    F + "j_end_wolves": J("The wolf-lord", "I called the wolves and fed on the oldest, and kept the priest alive. It was the lesser sin. It was still a sin. They looked at me with a kind of recognition, and I understood that I was now something wolves could follow."),
    F + "j_end_vigil": J("Ileana's vigil", "I knelt by her stone and asked to be spared, and the sun rose and spared me, and spared the priest, and that was the worst of all. There was no one to punish me, so I began to punish myself, and have not stopped."),
}

# ========================================================================================================= COMBAT
ENEMIES_EXTRA = {
    F + "akinji": dict(name="Akinji raider", model="human_peasant_m", hp=14, spd=6, dmg=[3, 5], acc=62, eva=10, tags=["human"], flee_at=0.3,
                       book="Turkish light horse on the Danube border (Ch.3, invented)"),
    F + "akinji_captain": dict(name="Akinji captain", model="human_peasant_m", hp=26, spd=6, dmg=[4, 7], acc=68, eva=10, tags=["human"], flee_at=0.2,
                               book="Turkish raid captain (invented)"),
}
ENCOUNTERS_EXTRA = {
    F + "raid": dict(name="The night raid at the Reed Ford", time="night", enemies=[F + "akinji", F + "akinji", F + "akinji_captain"], flee_ok=False,
                     intro="They come out of the reeds in the dark, wet and silent, with knives in their teeth. I draw my father's hammer. There are three of them and there is one of me, and I find, with some alarm, that this makes me happier than I have been in weeks.",
                     win="The last of them goes into the river and does not come up. Across the water a horn sounds the retreat. I am shaking, and the dawn is just beginning.", location=F + "ford"),
    F + "wolves": dict(name="Wolves on the mountain road", time="dusk", enemies=["wolf", "wolf", "wolf_alpha"], flee_ok=True,
                       intro="The wolves have followed the cart for three days. Tonight the great one steps forward and stands in the road. I am a prince, and I have been told that wolves are my people's emblem. Let us see.",
                       win="The alpha limps off. The others look at me, once, with an expression I can only call respect.", location=F + "road"),
}
_RAID = [{"set": F + "raid_won"}, {"journal": F + "j_ford"}]
ENCOUNTER_HOOKS = {
    F + "raid": dict(
        on_win=_RAID + [{"card": "The river ran red until noon. The Voivode stood on the bank with his father's hammer in his hand and the first grey of the day behind him, and was, for a moment, entirely at peace."}, {"goto": F + "camp"}],
        on_lose=_RAID + [say("I wake on the bank with my head split. Mircea's archers cut the rest of them down while I lay in the mud. I will not be told how close it was."), {"goto": F + "camp"}],
        on_flee=_RAID + [say("There is no running. I fought, and somehow it was enough."), {"goto": F + "camp"}]),
    F + "wolves": dict(
        on_win=[{"set": F + "wolves_driven"}, {"give": F + "charm"}, say("The alpha leaves a tooth in the mud. I pick it up: a grey fang with a perfect crown. The refugees tell the story on the road for a month.")],
        on_lose=[{"set": F + "wolves_driven"}, say("I come to on the road with the grandmother pouring water into my mouth. The wolves have gone, with their faces turned away, as if the whole thing had been a mistake.")],
        on_flee=[say("I retreat to the cart. The wolves do not follow. They only watch, as if they are saving me for another day.")]),
}

# ========================================================================================================= LOOKS / SEED VARIATION
VARIANTS = {
    "human_peasant_m": {
        F + "stanciu_v": human_colors(skin=T("skin", "#cfa383"), hair=T("hair", "#d8d8d8"), top=T("wool", "#2a2e4a"), bottom=T("wool", "#2a2a2a")),
        F + "vlaicu_v": human_colors(skin=T("skin", "#e0b896"), hair=T("hair", "#2a1c14"), top=T("cloth", "#6a1a24"), bottom=T("wool", "#2a1c14")),
        F + "radu_v": human_colors(skin=T("skin", "#d9b08c"), hair=T("hair", "#1c1410"), top=T("cloth", "#1a4a3a"), bottom=T("wool", "#1a2a24")),
        F + "messenger_v": human_colors(skin=T("skin", "#d0a888"), hair=T("hair", "#4a3322"), top=T("wool", "#4a3a2a"), bottom=T("wool", "#2a241c")),
        F + "sentry_v": human_colors(skin=T("skin", "#c9a07c"), hair=T("hair", "#9a9a9a"), top=T("wool", "#3a3a40"), bottom=T("wool", "#2a2a2a")),
        F + "scout_v": human_colors(skin=T("skin", "#c49a74"), hair=T("hair", "#2a2018"), top=T("wool", "#4a4a30"), bottom=T("wool", "#2e2c1c")),
        F + "akinji_v": human_colors(skin=T("skin", "#c49060"), hair=T("hair", "#1a1410"), top=T("cloth", "#3a5a30"), bottom=T("wool", "#2a2a1a")),
        F + "akinji_captain_v": human_colors(skin=T("skin", "#b88858"), hair=T("hair", "#1a1410"), top=T("cloth", "#2a3a5a"), bottom=T("wool", "#1a2230")),
        F + "student_v": human_colors(skin=T("skin", "#e0c0a0"), hair=T("hair", "#3a2a1c"), top=T("wool", "#1a1a1a"), bottom=T("wool", "#1a1a1a")),
    },
    "human_peasant_f": {
        F + "student_f_v": human_colors(skin=T("skin", "#e0c8b0"), hair=T("hair", "#1a1410"), top=T("wool", "#1a1a1a"), bottom=T("wool", "#1a1a1a")),
    },
    "human_captain": {F + "mircea_v": human_colors(skin=T("skin", "#c8a080"), hair=T("hair", "#5a5a5a"), top=T("wool", "#3a3028"), bottom=T("wool", "#2a2420"))},
    "human_seward": {
        F + "magister_v": human_colors(skin=T("skin", "#d8d4cc"), hair=T("hair", "#e8e8e8"), top=T("cloth", "#101010"), bottom=T("cloth", "#101010")),
        F + "priest_v": human_colors(skin=T("skin", "#d8c0a8"), hair=T("hair", "#8a8a8a"), top=T("cloth", "#1a1410"), bottom=T("cloth", "#1a1410")),
    },
    "human_quincey": {F + "vasile_v": human_colors(skin=T("skin", "#d9b898"), hair=T("hair", "#141010"), top=T("wool", "#1c1c20"), bottom=T("wool", "#1c1c20"))},
    "human_coachman": {F + "ferryman_v": human_colors(skin=T("skin", "#b8b8b0"), hair=T("hair", "#444444"), top=T("cloth", "#18181a"), bottom=T("cloth", "#18181a"), cloak=T("cloth", "#0c0c10"))},
    "human_lucy": {F + "ileana_v": human_colors(skin=T("skin", "#ead0b8"), hair=T("hair", "#2a1c14"), top=T("cloth", "#4a5a6a"), bottom=T("cloth", "#3a4452"))},
}

PALETTES = {
    F + "hall": [dict(wall="stone_dark", floor="planks", wood="ebony", cloth="red"), dict(wall="stone_grey", floor="planks", wood="dark", cloth="black")],
    F + "chamber": [dict(wall="stone_dark", floor="planks", wood="dark", cloth="black"), dict(wall="plaster_dirty", floor="planks", wood="oak", cloth="red")],
    F + "school": [dict(wall="stone_dark", floor="cobble", wood="ebony", cloth="black"), dict(wall="stone_grey", floor="cobble", wood="dark", cloth="green")],
    F + "library": [dict(wall="stone_dark", floor="cobble", wood="ebony", cloth="black"), dict(wall="stone_mossy", floor="cobble", wood="dark", cloth="red")],
    F + "chapel": [dict(wall="stone_grey", floor="stone_dark", wood="dark", cloth="red"), dict(wall="stone_dark", floor="stone_dark", wood="ebony", cloth="black")],
}

PLACEMENTS = {
    F + "radu_letter": [
        dict(prop=F + "bed", text="Folded under the pillow, a letter in a neat hand, sealed with a stranger's wax: Radu's letter.", hint="The pillow has been plumped again, too carefully."),
        dict(prop=F + "shelf", text="Between two volumes of the annals, a single sheet in Radu's writing: the letter to the Turkish agent.", hint="One volume of the annals sits proud of the rest."),
        dict(prop=F + "bust", text="Slipped behind the marble bust's plinth, a letter in Radu's neat hand: the letter.", hint="My father's marble bust has been turned a quarter of the way round."),
    ],
    F + "ink": [
        dict(prop=F + "lectern", text="Under the lectern's candlestick, a small pot of black ink that dries at once.", hint="The lectern's candles have a ring of black underneath."),
        dict(prop=F + "benches1", text="Wedged under the scholar's bench, where a beginner has been hiding it: a pot of black ink.", hint="Something rattles beneath the bench when you lean on it."),
    ],
}
