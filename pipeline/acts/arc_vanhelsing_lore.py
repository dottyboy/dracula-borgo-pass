"""PERSONAL ARC - "The Amsterdam Lectures" (Professor Abraham Van Helsing).  Ids prefixed vanhelsing_lore_."""
from dsl import *

F = "vanhelsing_lore_"


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


ENC = F + "vigil"

ARC = dict(
    id="vanhelsing_lore", title="The Amsterdam Lectures", member="vanhelsing", portrait="vanhelsing",
    blurb="Before London and the Count there was Amsterdam: a study full of books, a sick wife, a rival who calls it all peasant nonsense, and one winter night in a Styrian churchyard that taught Abraham Van Helsing which of his old fears were facts.",
    unlock="roster:vanhelsing", unlock_text="Meet Professor Van Helsing (Act III).", after_credits=False,
    start=dict(location=F + "study", protagonist="vanhelsing", party=["vanhelsing"], items={}, flags=[]),
    exit_to="ARC_END",
    rewards=[dict(give="black_frock_coat"), dict(set="rites"), dict(give="host"), dict(give="host"), dict(give="host"), dict(give=F + "bag"),
             dict(stat=dict(member="vanhelsing", faith=2, nerve=3, hp=1))],
    rewards_text="The rites are yours: holy-water, sacred-bullet and consecrated-knife recipes unlock. Three Sacred Wafers, the Professor's black medical bag; +2 Faith, +3 Nerve, +1 HP for Van Helsing Gear: a black frock coat.",
)

LOCATIONS = [
    dict(id=F + "study", name="Van Helsing's study, Amsterdam", desc="Books to the ceiling, a skull on the globe, and a lamp that has burned late every night for twenty years.", date="A winter in the 1860s"),
    dict(id=F + "home", name="The house on the Herengracht", desc="Upstairs, where the stove is kept high and the voices are lowered. The kitchen smells of cloves and onions.", date="The same winter"),
    dict(id=F + "street", name="The Herengracht, Amsterdam", desc="Gabled houses lean over the black canal. Skaters on the ice, a barrel-organ, and the bells of the Oude Kerk.", date="The same winter"),
    dict(id=F + "lecture", name="The lecture-room", desc="Tiered benches, a long blackboard and the smell of chalk and wet wool. The students are early. The Dean is earlier.", date="The same winter"),
    dict(id=F + "library", name="The University library", desc="Alcoves of calf and vellum under green lamps. At the end of the hall, a press of oak with a brass lock: the rare books.", date="The same winter"),
    dict(id=F + "chapel", name="The chapel of St. Nicholas", desc="Cold stone and thin candlelight. Father Pieter keeps the altar plain and the sacristy tidy.", date="The same winter"),
    dict(id=F + "village", name="Kirchdorf, Styria", desc="A mountain village under snow: low roofs, one inn, a church with an onion-spire. The peasants stop talking as the stranger passes.", date="Two weeks later"),
    dict(id=F + "inn", name="The inn at Kirchdorf", desc="Black beams, a tiled stove, and a long table where nobody wants to sit with their back to the door.", date="Two weeks later"),
    dict(id=F + "churchyard", name="The churchyard, by night", desc="Leaning crosses in the snow. The moon shows three old stones at the north wall, and a fourth shadow that is not a stone.", date="That night"),
]

LOC_DATA = {}

# ----------------------------------------------------------------------------------------------------------- study
LOC_DATA[F + "study"] = dict(
    cells=[2, 2], interior=True, wall="plaster_dirty", floor="planks", ambient=AMBIENT["candle_interior"], camera=cam([2, 2]),
    lights=lights_warm([2, 2]),
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_door_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[2.8, 2.0], spawns={F + "home": [-2.8, -2.0], F + "street": [2.8, 2.0]},
    props=[
        P("desk", "table", "dark", -0.6, -2.6, name="The writing-desk", radius=0.9, look="Quills, pounce, a blotter ruled by years of thinking, and a Latin note pinned flat under a paperweight."),
        P("latin", "book", "diary", -0.6, -2.6, y=0.8, name="Latin note", radius=0.2,
          look="A slip in a small crabbed hand, from Arminius's last parcel. 'Read it before you read anything else', he has added in German.", talk=F + "latin_note"),
        P("casebook", "book", "leather", 0.6, -2.6, y=0.8, name="My casebook", radius=0.2, look="Cases, dates, observations. I write what I saw and what I was told in separate columns, as a physician should.",
          take=F + "casebook", take_text="I take my casebook. A man who lectures on evidence should carry some.", give_once=True),
        P("shelf1", "bookshelf", "dark", -3.3, 1.0, rot=90, name="Medical shelf", radius=0.7, look="Boerhaave, Sydenham, Hunter. My dead masters, standing shoulder to shoulder."),
        P("shelf2", "bookshelf", "oak", 3.4, -1.8, rot=-90, name="Shelf of heresies", radius=0.7, look="Paracelsus, Agrippa, Glanvill on witches, Calmet on vampires. 'Read the madmen too', my teacher said. 'Madmen are sometimes right by accident, and then you must know it.'"),
        P("bust", "bust", "plaster", 2.4, -3.2, name="Bust of Boerhaave", radius=0.5, look="The great Boerhaave in plaster, who taught that the bedside is the only true library."),
        P("clock", "column_short", "plaster", -3.2, -3.2, name="Tall clock", radius=0.5, look="It loses four minutes a week, and I forgive it, because it was my father's."),
        P("cabinet", "chest", "ebony", -3.0, -0.4, rot=90, name="Locked cabinet", radius=0.6,
          look="Where I keep what my friend Arminius sends from Buda-Pesth. I lock it because I do not wish my students to see how many of my theories began in somebody else's letter.",
          use_item={F + "cabinet_key": [{"take": F + "cabinet_key"}, say("The lock gives. A bundle of letters in a small clear hand, tied with black tape."), {"give": F + "letters"}, {"set": F + "cabinet_open"}]},
          use_fail="The cabinet is locked. I laid its key somewhere sensible, which means somewhere I cannot remember."),
        P("table", "table", "oak", 1.6, 0.2, name="Work-table", radius=0.9,
          look="A bare oak table scrubbed white. Here I mix, mend and put things together.",
          use_item={"host": [{"take": "host"}, {"set": F + "ward_host"}, say("I lay the consecrated Wafer on a clean linen square. The heart of the thing.")],
                    F + "child_cross": [{"take": F + "child_cross"}, {"set": F + "ward_cross"}, say("The small silver cross, set beside the Wafer. It was made for a smaller hand than mine, and it is no less strong for that.")],
                    "garlic": [{"take": "garlic"}, {"set": F + "ward_garlic"}, say("Garlic, braided with red thread, for the doors and the windows and the throat.")]},
          use_fail="That does not belong in the ward. It wants a Wafer, a cross, and garlic."),
        P("ward_case", "chest", "dark", 1.6, 0.2, y=0.8, scale=0.3, name="The assembled ward", radius=0.3, cond=F + "ward_host&" + F + "ward_cross&" + F + "ward_garlic",
          look="Linen, silver, red thread and white bread: all that I know of protection, folded small.",
          take=F + "ward", take_text="I fold the linen over and bind it with the red thread. It weighs nothing, and it weighs a great deal.", give_once=True),
        P("stake_case", "chest", "dark", 3.0, 1.6, rot=-90, name="Travelling case", radius=0.6,
          look="My travelling case, packed for the field. Ash stakes, a mallet, a crucifix, and Hunter's lancet for the sort of cases that need one.",
          set=F + "case_seen", set_text="I check the case: two stakes of ash, a hammer of good steel, my small crucifix. I take the whole."),
        P("stake", "stake", "default", 3.0, 1.0, rot=-90, name="Ash stake", radius=0.2, cond=F + "case_seen", look="Ash, seasoned, sharpened by my own hand.",
          take="stake", take_text="The ash stake goes inside my coat.", give_once=True),
        P("hammer", "hammer", "default", 3.0, 2.2, rot=-90, name="Hammer", radius=0.2, cond=F + "case_seen", look="A mallet of good steel.",
          take="hammer", take_text="I take the hammer.", give_once=True),
        P("crucifix", "crucifix", "silver", 1.4, 0.2, y=0.8, name="Silver crucifix", radius=0.2, look="The little crucifix I have carried since my ordination to nothing in particular.",
          take="crucifix", take_text="I put the crucifix in my breast pocket.", give_once=True),
        P("globe", "barrel", "oak", 0.6, 1.8, scale=0.6, name="Globe on its stand", radius=0.4, look="A globe, worn pale across the Carpathians where my thumb goes."),
        P("rug", "rug", "red", 0.2, 0.6, radius=0.1),
        P("lamp", "lantern", "default", 0.2, -3.4, y=1.4, radius=0.2),
        P("d_home", "door", "dark", -3.8, -2.0, rot=90, name="Door to the house", radius=0.6, look="Upstairs to the stove, and my wife.", go=F + "home"),
        P("d_street", "door", "oak", 3.8, 2.0, rot=-90, name="Street door", radius=0.6, look="To the Herengracht and the world.", go=F + "street"),
    ],
    npcs=[],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_study")])],
)
LOC_DATA[F + "study"]["props"].append(P(
    "final", "book", "red", -0.0, -2.6, y=0.8, name="Arminius's last letter", radius=0.2, cond=F + "vigil_done",
    look="Black-edged, it has come while I was in Styria. I know the hand before I turn it over.", talk=F + "final_letter"))

# ----------------------------------------------------------------------------------------------------------- home
LOC_DATA[F + "home"] = dict(
    cells=[2, 2], interior=True, wall="plaster", floor="planks", ambient=AMBIENT["warm_day_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2], energy=2.2),
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[2.8, -2.0], spawns={F + "study": [2.8, -2.0]},
    props=[
        P("bed", "bed", "blue", -2.0, -2.4, name="My wife's bed", radius=1.2, look="The bed is turned toward the window so that she can see the canal and the skaters and the boys who do not fall."),
        P("stove", "fireplace", "stone_grey", -3.4, 1.8, rot=90, name="Tiled stove", radius=0.9, look="Blue Delft tiles, a fire of peat and a kettle that has never been allowed to go off the boil."),
        P("cradle", "chest", "pale", 0.8, -3.0, scale=0.6, name="A small cradle", radius=0.4,
          look="Not a cradle any more; she has put her sewing in it. She will not let the maid move it. I have not asked her to."),
        P("sewing", "book", "red", 0.8, -3.0, y=0.5, name="Sewing-basket", radius=0.2, look="Half a child's coat, in grey wool, never finished. The needle is still in it."),
        P("table", "table", "pale", 2.0, 0.6, name="Kitchen table", radius=0.9, look="Scrubbed pine. A dish of onions, a loaf, a jug of Hollands gin that the doctor does not need to know about."),
        P("chair1", "chair", "blue", 0.6, 0.6, rot=90, radius=0.4, name="Chair", look="Mine, by the bed, wherever the bed is."),
        P("chair2", "chair", "blue", -3.0, -0.2, rot=90, radius=0.4, name="Chair", look="Where the maid sits when I am at the University."),
        P("garland", "garlic", "default", 3.4, 2.0, y=1.4, rot=-90, name="Garlic braid", radius=0.2, look="The housekeeper hangs these for the cook-pot and for the winter ague. Mostly for the winter ague."),
        P("rug", "rug", "blue", -0.4, 1.8, radius=0.1),
        P("lamp", "candelabra", "default", 2.0, 0.6, y=0.8, radius=0.2),
        P("d_study", "door", "oak", 3.8, -2.0, rot=-90, name="Door to the study", radius=0.6, look="Down the narrow stair to my books.", go=F + "study"),
    ],
    npcs=[
        NP("wife", "human_peasant_f", "innkeeper_wife", -1.0, -1.4, rot=-90, name="My wife", look="She is thin and very straight against the pillows, and she greets me with the small dry joke she uses instead of complaint.", talk=F + "wife_talk"),
        NP("keeper", "human_peasant_f", "village_woman", 1.6, 2.4, rot=180, name="Mevrouw Bakker, the housekeeper", look="Floured to the elbow. Stout, sixty, and a better judge of the sick than half the Faculty.", talk=F + "keeper_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_home")])],
)

# ----------------------------------------------------------------------------------------------------------- street
LOC_DATA[F + "street"] = dict(
    cells=[3, 2], interior=False, wall="plaster", floor="cobble", ambient=AMBIENT["day_exterior"], camera=cam([3, 2]), lights=lights_day(3.0),
    scatter=dict(asset="pine_small", variant="green", count=8, seed=17, avoid=[[-7, -5, 7, 5]]),
    spawn=[4.4, 2.4], spawns={F + "study": [4.4, 2.4], F + "lecture": [-3.0, -2.0], F + "library": [0.0, -2.0], F + "chapel": [3.0, -2.0]},
    props=[
        P("d_study", "door_big", "dark", 5.2, -2.6, name="My own front door", radius=0.7, look="Number 44, with the brass knocker polished by Mevrouw Bakker.", go=F + "study"),
        P("a_lecture", "arch", "stone_grey", -4.6, -2.8, name="University lecture-hall", radius=0.8, look="The Faculty's grey arch. 'Veritas', says the keystone, and a hundred and fifty years of pigeons have commented.", go=F + "lecture"),
        P("a_library", "arch", "stone_dark", 0.2, -3.6, name="University library", radius=0.8, look="Under the Latin motto, a smaller notice: 'Silence'.", go=F + "library"),
        P("a_chapel", "arch", "stone_mossy", 3.0, -3.6, name="Chapel of St. Nicholas", radius=0.8, look="A low door beneath a lantern, and the smell of wax.", go=F + "chapel", rot=0),
        P("carriage", "carriage", "oak", -4.6, 2.6, rot=70, name="The post-coach to Cologne", radius=1.2,
          look="The coach for the Rhine, the railway and then south, to the Styrian mountains. Arminius's friend, the pastor, has written. I should go, with whatever I can carry.",
          go=F + "village", go_cond="has:" + F + "ward&has:stake&has:hammer&flag:" + F + "letters_read&flag:" + F + "latin_read",
          go_fail="Not yet. I must go prepared: the ward made up, stake and hammer in my bag, the Latin note understood and my friend's letters read."),
        P("lamp1", "lantern", "default", -2.0, -1.4, name="Gas-lamp", radius=0.3, look="Lit at four in winter, and always a minute late."),
        P("lamp2", "lantern", "default", 2.0, 0.4, radius=0.3),
        P("bench", "bench", "dark", 0.4, 1.2, name="Canal bench", radius=0.9, look="A bench for watching skaters and not noticing the cold."),
        P("barrel", "barrel", "oak", 5.2, 0.8, name="Herring barrel", radius=0.4, look="Pickled herring, the fuel of the Dutch intellect."),
        P("fence1", "fence", "default", -4.0, 4.0, radius=0.3),
        P("fence2", "fence", "default", 0.0, 4.0, radius=0.3),
        P("fence3", "fence", "default", 4.0, 4.0, radius=0.3),
        P("rock", "rock", "grey", 5.8, 3.0, radius=0.5),
    ],
    npcs=[
        NP("cabby", "human_coachman", "driver", -3.0, 1.0, rot=90, name="Jan, the cab-driver", look="Wrapped in three coats, in the way of men who wait out of doors for a living.", talk=F + "cabby_talk"),
        NP("student", "human_peasant_m", "villager", 1.8, -1.0, rot=180, name="A student with a stack of books", look="One of mine. Bright, anxious, and carrying the wrong volume under the right one.", talk=F + "student_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_street")])],
)

# ----------------------------------------------------------------------------------------------------------- lecture
LOC_DATA[F + "lecture"] = dict(
    cells=[2, 2], interior=True, wall="plaster", floor="planks", ambient=AMBIENT["warm_day_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2], energy=2.6),
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[2.8, 2.0], spawns={F + "street": [2.8, 2.0]},
    props=[
        P("board", "mirror", "default", -1.8, -3.9, y=1.2, scale=1.8, name="The blackboard", radius=0.9,
          look="In a square hand: 'BELIEVE NOTHING YE CANNOT TEST. DISBELIEVE NOTHING YE HAVE NOT TESTED.' Below, two columns. TESTED: the bite of the rabid dog; the trance under mesmerism in Charcot's wards; blood passed from a sound man to a dying one. UNPROVED: the evil eye; a hanged man's rope as a cure for fever; the ringing of bells to turn the hail.",
          set=F + "board_read", set_text="I read the board twice. The Dean will use my own words against me, so I had better know them."),
        P("lectern", "table", "dark", 1.0, -2.6, name="Lectern", radius=0.8, look="Scarred oak with a brass lamp. A drip of tallow marks the page where I lost my place in 1858 and found a new theory."),
        P("skeleton", "bust", "stone_grey", 3.1, -3.0, name="Anatomical bust", radius=0.5, look="A plaster skull on a wooden stand, with the sutures painted in. A student has hung a cap on it."),
        P("bench1", "bench", "oak", -2.2, 0.2, name="Student bench", radius=0.9, look="Initials carved through two generations, and one drawing I will not describe."),
        P("bench2", "bench", "oak", -2.2, 2.0, name="Student bench", radius=0.9, look="The back row. All the best students sit here, and all the worst."),
        P("bench3", "bench", "oak", 0.0, 0.8, name="Student bench", radius=0.9, look="The front row, for those who wish to be seen to understand."),
        P("cabinet", "bookshelf", "pale", 3.4, 0.2, rot=-90, name="Specimen cabinet", radius=0.7, look="Jars, calipers and a stomach in spirits. I do not say whose."),
        P("stove", "fireplace", "stone_grey", -3.4, -0.6, rot=90, name="Lecture-room stove", radius=0.9, look="A tall iron stove that warms the first row and no one else."),
        P("rug", "rug", "green", 0.4, -0.8, radius=0.1),
        P("d_street", "door", "oak", 3.8, 2.0, rot=-90, name="Door to the street", radius=0.6, look="Back to the canal.", go=F + "street"),
    ],
    npcs=[
        NP("verhoeven", "human_arthur", "lord", 0.2, -1.4, rot=180, name="Professor Verhoeven, the Dean", look="A tall man in a perfect black coat, who has been exactly right in public for thirty years. He holds the key to the rare-book press and the Faculty's good opinion, and I want the first more than the second.", talk=F + "verhoeven_talk"),
        NP("seward", "human_seward", "doctor", 2.4, 0.6, rot=-90, name="A young Englishman, John Seward", look="A visiting student from London. Earnest, quiet, and clever in the way that frightens his tutors. He has a half-healed scar on the back of his hand.", talk=F + "seward_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_lecture")])],
)

# ----------------------------------------------------------------------------------------------------------- library
LOC_DATA[F + "library"] = dict(
    cells=[3, 2], interior=True, wall="plaster_dirty", floor="planks", ambient=AMBIENT["candle_interior"], camera=cam([3, 2]), lights=lights_warm([3, 2], energy=2.4),
    walls=dict(north=["wall_4", "wall_door_4", "wall_4"], west=["wall_window_4", "wall_4"], east=["wall_4", "wall_window_4"]),
    spawn=[0.0, -2.4], spawns={F + "street": [0.0, -2.4]},
    props=[
        P("press", "chest", "ebony", 4.4, -3.0, scale=1.2, name="The rare-book press", radius=0.7,
          look="An oak press with a brass lock, kept by the Dean. Inside, behind iron grilles, the books no one wants to be seen reading.",
          use_item={F + "library_key": [{"take": F + "library_key"}, say("The brass lock turns. I take down the one volume I came for, an old Ordo, in a binding gone black with handling."), {"give": F + "rituale"}, {"set": F + "press_open"}]},
          use_fail="Locked. The key is with the Dean, and the Dean does not lend it to men he disagrees with."),
        P("shelf1", "bookshelf", "dark", -4.4, -3.0, name="Theology", radius=0.7, look="Aquinas, Suarez, and a thousand folios of the Fathers. Nobody has taken out Suarez since the Treaty of Utrecht."),
        P("shelf2", "bookshelf", "oak", -2.2, -3.0, name="Natural philosophy", radius=0.7, look="Boyle, Newton, Leeuwenhoek. A man could be happy here and never need the truth."),
        P("shelf3", "bookshelf", "pale", 2.0, -3.0, name="Folklore and travels", radius=0.7, look="Voyages to Muscovy, Carpathian tales, Calmet. They are shelved with Natural History, which is about right.",
          set=F + "shelf_read", set_text="Among the travellers I find an old German account of a Styrian village that 'sealed its north grave with ash and iron in the year of the great snow'. I copy the page number and say nothing."),
        P("desk", "table", "dark", -1.0, 0.2, name="Reading-desk", radius=0.9, look="A green lamp, an inkstand and a ticket for borrowed books, forty-two of them in the name of one Van Helsing."),
        P("globe", "barrel", "dark", -4.4, 1.4, scale=0.6, name="Celestial globe", radius=0.4, look="The constellations in gilded wire, many of them wrongly placed."),
        P("table2", "table_long", "oak", 1.6, 1.6, name="Long study-table", radius=1.6, look="Three students, asleep, and a fourth pretending to be."),
        P("bust", "bust", "plaster", 5.0, 1.2, name="Bust of Erasmus", radius=0.5, look="Erasmus, who laughed at the Church and loved it all the same."),
        P("lamp1", "lantern", "default", -2.4, 2.4, y=0.0, radius=0.3),
        P("lamp2", "candelabra", "default", -1.0, 0.2, y=0.8, radius=0.2, name="Reading lamp", look="A single steady flame, the only kind a library trusts."),
        P("rug", "rug", "green", 0.0, 0.2, radius=0.1),
        P("d_street", "door", "oak", 0.0, -3.8, name="Door to the street", radius=0.6, look="Back out into the cold.", go=F + "street"),
    ],
    npcs=[
        NP("librarian", "human_harker", "harker", -3.0, 1.0, rot=90, name="Mijnheer de Vries, the librarian", look="Pale as his parchment and twice as dry. He speaks in a whisper, even when the library is empty.", talk=F + "librarian_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_library")])],
)

# ----------------------------------------------------------------------------------------------------------- chapel
LOC_DATA[F + "chapel"] = dict(
    cells=[2, 3], interior=True, wall="stone_dark", floor="stone_grey", ambient=AMBIENT["cold_interior"], camera=cam([2, 3]),
    lights=[dict(pos=[0, 2.6, -3], color="#a8b4ff", energy=1.6, range=12), dict(pos=[0, 1.9, 3], color="#ff9a40", energy=1.4, range=10)],
    walls=dict(north=["wall_4", "wall_4"], west=["wall_4", "wall_window_4", "wall_door_4"], east=["wall_4", "wall_window_4", "wall_4"]),
    spawn=[-2.8, 4.0], spawns={F + "street": [-2.8, 4.0]},
    props=[
        P("altar", "table", "ebony", 0.0, -4.4, name="Altar", radius=1.0, look="Plain stone under a white cloth. A small altar, for a small chapel, kept as though a bishop might arrive."),
        P("cross", "crucifix_big", "silver", 0.0, -4.6, y=0.8, name="Altar cross", radius=0.3, look="Silver, worn at the arms by generations of lips."),
        P("candles", "candelabra", "default", -1.4, -4.2, y=0.8, name="Altar candles", radius=0.2, look="Beeswax, honey-sweet, and burning straight."),
        P("sacristy", "chest", "oak", 3.0, -1.0, rot=-90, name="Sacristy chest", radius=0.6,
          look="Albs, stoles, corporals and a tin of unleavened bread for the next Mass. Father Pieter has marked the tin: 'Not yet blessed.'",
          take=F + "wafers", take_text="Father Pieter nods from the altar. I take the tin of unblessed wafers; they are only flour and water, as yet.", give_once=True),
        P("font", "column_short", "stone_grey", -2.8, 1.8, name="Stone font", radius=0.5, look="A shallow basin with a skin of ice at the edges. Even the holy water is cold in St. Nicholas."),
        P("pew1", "bench", "dark", -2.2, -0.4, rot=90, name="Pew", radius=0.9, look="Wood worn smooth by the sailors' wives."),
        P("pew2", "bench", "dark", 2.2, 1.2, rot=-90, name="Pew", radius=0.9, look="The sailors' widows' pew. It is always full."),
        P("pew3", "bench", "dark", -2.2, 2.0, rot=90, name="Pew", radius=0.9, look="Mine, when I come, which is less often than Father Pieter hopes."),
        P("window", "mirror", "default", 3.7, 0.2, y=1.6, rot=-90, name="Stained window", radius=0.4, look="St. Nicholas and three drowned boys, in lead and blue glass."),
        P("rug", "rug", "red", 0.0, 0.8, radius=0.1),
        P("d_street", "door", "dark", -3.8, 4.0, rot=90, name="Door to the street", radius=0.6, look="The canal, and the bells of the Oude Kerk.", go=F + "street"),
    ],
    npcs=[
        NP("pieter", "human_harker", "travel", -0.8, -2.4, rot=0, name="Father Pieter", look="Fifty, round, mild. A confessor first, a scholar second, and a very good Latinist whenever there is no one to see.", talk=F + "pieter_talk"),
        NP("sexton", "human_peasant_m", "innkeeper", 2.4, -2.8, rot=180, name="The sacristan, old Gerrit", look="Deaf in the left ear, and fiercely proud of the candle-ends he has saved for forty years.", talk=F + "gerrit_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_chapel")])],
)

# ----------------------------------------------------------------------------------------------------------- village
LOC_DATA[F + "village"] = dict(
    cells=[3, 2], interior=False, wall="plaster", floor="grass", ambient=AMBIENT["dusk_exterior"], camera=cam([3, 2]), lights=lights_day(2.2),
    scatter=dict(asset="pine", variant="snow", count=24, seed=33, avoid=[[-7, -5, 7, 5]]),
    spawn=[0.0, 3.4], spawns={F + "inn": [-3.8, 0.4], F + "churchyard": [4.0, 0.4]},
    props=[
        P("church", "tower", "plaster", 3.6, -5.4, scale=0.8, name="The church", radius=1.3, look="A small church with an onion-spire, whitewashed against the weather and clearly built to be looked at nervously."),
        P("d_inn", "door", "dark", -5.2, -0.6, rot=90, name="The inn", radius=0.6, look="'Zum Schwarzen Hahn', says the sign: the Black Cock. A lantern burns by the door in daylight.", go=F + "inn"),
        P("a_churchyard", "arch", "stone_mossy", 5.2, -1.0, rot=-90, name="Lychgate to the churchyard", radius=0.8, look="A roofed gate of black timber, hung with dried herbs and a very recent iron nail.",
          go=F + "churchyard", go_cond="flag:" + F + "pastor_leave&flag:" + F + "know_stone", go_fail="The sexton stands before the gate with his arms folded. 'Not without the Pfarrer's word, Herr, and not unless you know which grave you are going to.'"),
        P("well", "column_short", "stone_grey", -1.0, 0.6, name="Village well", radius=0.4, look="Iced over. The women fetch water in pairs and in daylight."),
        P("cart", "carriage", "oak", 1.6, 3.0, rot=20, scale=0.7, name="Hay-sledge", radius=1.0, look="A sledge piled with hay and a pitchfork stuck, tines up, in the top of it."),
        P("barrel", "barrel", "dark", -3.0, 3.0, name="Barrel", radius=0.4, look="Frozen sauerkraut."),
        P("sign", "signpost", "oak", 3.6, 3.4, rot=-20, name="Signpost", radius=0.3, look="'Graz, 31 Kilometer.' Somebody has scratched a cross under the 31."),
        P("lamp", "lantern", "default", 0.2, -1.4, radius=0.3, name="Lantern", look="Lit well before dusk."),
        P("fence1", "fence", "default", -4.0, 4.0, radius=0.3),
        P("fence2", "fence", "default", 4.0, 4.0, radius=0.3),
    ],
    npcs=[
        NP("pastor", "human_captain", "captain", 2.4, -0.2, rot=-90, name="Pfarrer Albrecht", look="The village priest, tall, grey and badly shaved. He has not slept properly in a month, and is ashamed to have written for help.", talk=F + "pastor_talk"),
        NP("sexton", "human_peasant_m", "szgany", 4.0, 1.0, rot=180, name="The sexton, Matthias", look="Stooped and strong from forty years of digging. He leans on his spade as though the village might ask him to dig another.", talk=F + "sexton_talk"),
        NP("widow", "human_peasant_f", "village_woman", -2.6, -1.8, rot=45, name="Old Frau Lindner", look="Black shawl, black skirt, a white face like a shaved apple. She was eight when the great snow came, and she has not forgotten it.", talk=F + "widow_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(journal=F + "j_village")])],
)

# ----------------------------------------------------------------------------------------------------------- inn
LOC_DATA[F + "inn"] = dict(
    cells=[2, 2], interior=True, wall="plaster_dirty", floor="planks", ambient=AMBIENT["candle_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2], energy=2.6),
    walls=dict(north=["wall_4", "wall_window_4"], west=["wall_door_4", "wall_4"], east=["wall_4", "wall_4"]),
    spawn=[-2.8, -2.0], spawns={F + "village": [-2.8, -2.0]},
    props=[
        P("stove", "fireplace", "stone_grey", 3.3, -2.4, rot=-90, name="Tiled stove", radius=0.9, look="Green tiles, a bench round it, and all the village's feet stretched toward it."),
        P("table", "table_long", "dark", 0.2, 0.4, name="Long table", radius=1.6, look="Scarred, wine-stained, with a bowl of dumplings going cold because nobody has the heart for them."),
        P("bench", "bench", "dark", 0.2, 1.6, name="Bench", radius=0.9, look="The wall side. Nobody sits there."),
        P("barrels", "barrel", "dark", 3.2, 2.0, name="Beer barrels", radius=0.4, look="Marzen, and a little plum brandy."),
        P("shelf", "bookshelf", "pale", -3.4, 1.0, rot=90, name="Dresser", radius=0.7, look="Pewter plates, a Bible, and a very old tarot pack that the landlord claims is for patience."),
        P("garlic", "garlic", "default", 3.6, 0.2, y=1.4, rot=-90, name="Garlic strings", radius=0.2, look="Strings of it over every window. There is more garlic than the soup could ever need."),
        P("crucifix", "crucifix_big", "silver", -3.6, -2.6, y=1.6, rot=90, name="Wall crucifix", radius=0.3, look="Carved lime-wood, painted, with a fresh sprig of fir behind it."),
        P("lamp", "candelabra", "default", 0.2, 0.4, y=0.8, radius=0.2),
        P("rug", "rug", "red", -0.8, -1.6, radius=0.1),
        P("d_out", "door", "dark", -3.8, -2.0, rot=90, name="Door to the street", radius=0.6, look="The snow, and the church.", go=F + "village"),
    ],
    npcs=[
        NP("host", "human_peasant_m", "innkeeper", -1.8, 2.0, rot=45, name="Landlord Huber", look="A big man with a small voice. He has stopped telling anyone it is late.", talk=F + "huber_talk"),
        NP("farmer", "human_peasant_m", "villager", 2.2, 1.4, rot=-90, name="A herdsman", look="Sits with his back to the wall and his eyes on the door.", talk=F + "herdsman_talk"),
    ],
)

# ----------------------------------------------------------------------------------------------------------- churchyard
LOC_DATA[F + "churchyard"] = dict(
    cells=[3, 3], interior=False, wall="stone_dark", floor="grass", ambient=AMBIENT["night_exterior"], camera=cam([3, 3]), lights=lights_moon(2.8), moon=dict(pos=[-6, 12, -8]),
    scatter=dict(asset="pine", variant="snow", count=22, seed=29, avoid=[[-7, -7, 7, 7]]),
    spawn=[4.4, 0.6], spawns={F + "village": [4.4, 0.6]},
    props=[
        P("a_gate", "arch", "stone_mossy", 5.4, 1.2, rot=-90, name="Lychgate", radius=0.8, look="Back to the village and the lamps.", go=F + "village"),
        P("stone_a", "gravestone", "stone_mossy", -4.4, -4.0, name="Stone: Anna Pfeifer", radius=0.5,
          look="'ANNA PFEIFER, WIDOW. DIED 1791, AGED EIGHTY. SHE SLEPT WELL.' The lichen has overgrown the 'well'.",
          use_item={F + "ward": [say("Nothing stirs. The snow is smooth, and the old woman sleeps as she was told to.")]}, use_fail="This is not the place."),
        P("stone_k", "gravestone_point", "stone_mossy", -0.4, -4.0, name="Stone: Katharina Lindner", radius=0.5,
          look="'KATHARINA LINDNER, WIFE AND MOTHER, DIED 1812, AGED NINETEEN, IN THE SPRING AFTER HER WEDDING.' Three iron nails have been driven in a row across the top of the stone. The soil about it is not frozen.",
          use_item={F + "ward": [{"take": F + "ward"}, {"set": F + "circle_made"},
                                 say("I kneel in the snow and lay the linen square upon the stone. I scatter the garlic in a ring, the Wafer at the head, the little silver cross at the foot, and I draw the circle closed with my finger in the frost. Then I wait, and the cold comes down.")]},
          use_fail="Nothing I carry will serve here but the ward."),
        P("stone_j", "grave_cross", "stone_mossy", 3.6, -4.0, name="Cross: Josef Hauer", radius=0.5,
          look="'JOSEF HAUER, 1799. HANGED AT GRAZ FOR SHEEP-STEALING.' Poor wretch. The village has put a cross on him to make him comfortable, and perhaps to keep him down.",
          use_item={F + "ward": [say("Nothing stirs. A thief is only a thief, and he is dead.")]}, use_fail="This is not the place."),
        P("t1", "gravestone", "stone_grey", -4.4, 0.0, radius=0.5, name="Old stone", look="Worn smooth. Whoever it was is no longer anyone's business."),
        P("t2", "grave_cross", "stone_grey", -2.4, 1.6, radius=0.5, name="Leaning cross", look="One arm is gone."),
        P("t3", "gravestone_point", "stone_grey", 3.0, 0.6, radius=0.5, name="Child's stone", look="A small stone with a lamb on it. I look away, then back. Then I look away again."),
        P("t4", "tomb", "stone_tomb", 0.4, 2.6, radius=0.9, name="Family tomb", look="A squat tomb of the Pfeifer family, shut, and clean of snow."),
        P("deadtree", "deadtree", "grey", -5.6, 3.0, radius=0.4, name="Dead yew", look="A yew older than the church, black and hollow."),
        P("lamp", "lantern", "default", 4.4, -1.6, radius=0.3, name="Gate-lantern", look="The sexton's. It will not stay lit beyond the third stone."),
        P("rock", "rock", "mossy", 1.6, 4.2, radius=0.5),
    ],
    npcs=[
        NP("revenant", "human_lucy", "undead", -0.4, -2.2, rot=0, name="The girl at the grave", cond=F + "circle_made&!won:" + ENC,
           look="She wears a wedding-dress gone grey. She has no footprints in the snow, and she has turned her face toward me with great interest.", fight=ENC),
    ],
    on_enter=[dict(once=True, do=[say("The moon stands over the north wall. I can smell cold earth, and under it, faint and sweet, something that is not earth. Three stones, three stories. I must be sure of the right one, because the right one is the only one I can afford to kneel at.")])],
)

# ----------------------------------------------------------------------------------------------------------- dialogue
DIALOGUE = {}

DIALOGUE[F + "latin_note"] = D(
    "n0",
    n0=N("Latin note", "'Mortuus non est qui nocte surgit. Per diem in terra sua iacet. Ligno cor transfige, caput abscinde, os allio imple.' Beneath: 'And beware of the sacrament, A. - it is a thing, not a sentiment.'",
         choices=[C("'He who rises at night is not dead. By day he sleeps in his own earth. Pierce the heart with iron, burn the body, fill the mouth with earth.'", "n_bad", cond="!" + F + "latin_read"),
                  C("'He who rises at night is not dead. By day he lies in his own earth. Pierce the heart with wood, cut off the head, fill the mouth with garlic.'", "n_good", cond="!" + F + "latin_read"),
                  C("'The dead do not rise at night. By night he lies in his own earth. Bind the heart with wood, hide the head, fill the mouth with salt.'", "n_bad", cond="!" + F + "latin_read"),
                  C("[Read it again]", "n0", cond=F + "latin_read"),
                  C("[Put it down]", end=True)]),
    n_bad=N("Van Helsing", "No. 'Ligno' is wood and 'transfige' is pierce; 'os allio imple' will not turn into salt however much I wish it. And 'per diem' is by day. A careless translation could get a man killed.", next="n0"),
    n_good=N("Van Helsing", "Wood, not iron; day, not night; garlic, not earth. It is exact, and it is horrible, and my friend Arminius has not troubled himself to say how he came to know.",
             do=[{"set": F + "latin_read"}, {"journal": F + "j_latin"}], next="n0"),
)

DIALOGUE[F + "letters_read"] = D(
    "n0",
    n0=N("Arminius's letters", "Three letters, tied with black tape. The paper is Hungarian, the hand beautiful, the content not.",
         choices=[C("[Read the first, on the Voivode]", "n1"), C("[Read the second, on Scholomance]", "n2", cond=F + "r1"),
                  C("[Read the third, on Styria]", "n3", cond=F + "r2"), C("[Put them away]", end=True)]),
    n1=N("Arminius", "'My dear Abraham, you ask who he was. A Voivode of the Wallachian line, a general, a statesman, a man of cunning and of iron. Beaten at Kossovo and, they say, betrayed. In the Szekelys' tales his blood is the river of a nation. I do not believe a word, my friend, but I have never found his grave.'",
         do=[{"set": F + "r1"}], next="n0"),
    n2=N("Arminius", "'The tales speak of a school: the Scholomance, in the mountains over the Hermannstadt lake, where the Devil himself was said to take ten scholars in seven, and keep the tenth as his due. They learned the language of beasts, the weather, the use of thunder. One of those scholars, the Szekelys say, was of this Voivode's blood.'",
         do=[{"set": F + "r2"}], next="n0"),
    n3=N("Arminius", "'Now a practical matter. Pfarrer Albrecht of Kirchdorf, in Styria, has written me about a grave in his churchyard. The village will not let him open it. I cannot go, being old and immovable. You are neither. Go prepared, Abraham, and do not go to disprove it. Go to find out.'",
         do=[{"set": F + "letters_read"}, {"journal": F + "j_letters"}], next="n0"),
)
# reading station: a chair at the study desk, once the letters are in the bag
LOC_DATA[F + "study"]["props"].append(P(
    "reading_chair", "chair", "green", 0.2, -0.6, rot=0, name="Reading chair", radius=0.4, cond="has:" + F + "letters",
    look="My wing-chair, with a lamp at its elbow. A man should read bad news sitting down.", talk=F + "letters_read"))

DIALOGUE[F + "wife_talk"] = D(
    "n0",
    n0=N("My wife", "You are late, Abraham, which means you have found a theory. Tell me, quickly, before Mevrouw Bakker scolds us both.",
         choices=[C("How are you today?", "n_how"), C("Tell me about the little coat.", "n_coat", cond="!" + F + "got_cross"),
                  C("Is there anything you need?", "n_need", cond="!" + F + "got_cross&" + F + "n_coat_done"),
                  C("[Sit with her a while]", "n_sit"), C("[Leave]", end=True)]),
    n_how=N("My wife", "The doctor says my lungs are 'no worse'. I told him that was not a diagnosis, it was a courtesy. I watched the skaters today. One boy fell and got up again. I counted it a sign.", next="n0"),
    n_coat=N("My wife", "I began it in March, for a boy who would have been four. I stop when I think I will finish it. Do not look at me like a case. It is only wool.",
             do=[{"set": F + "n_coat_done"}], next="n_coat2"),
    n_coat2=N("My wife", "You are the cleverest man in Amsterdam, my dear, and you cannot save a child who has already gone. But you will save somebody's. I think that is why you read the heresies.", next="n0"),
    n_need=N("My wife", "Yes. There is a silver cross in the cradle, under the wool. It was his christening gift from Arminius. It is made for a small hand. I would rather it went into the world doing a work than lay in a cradle. Take it, Abraham. Take it for the next one.",
             do=[{"give": F + "child_cross"}, {"set": F + "got_cross"}, {"journal": F + "j_cross"}], next="n0"),
    n_sit=N("Van Helsing", "I sit by her until the lamp needs trimming. We do not talk of the child. We talk of Boerhaave and her father's boat and whether the ice will hold until Sunday. It is the best afternoon of the winter.", next="n0"),
)

DIALOGUE[F + "keeper_talk"] = D(
    "n0",
    n0=N("Mevrouw Bakker", "She ate two spoons of the barley broth, Herr Professor. Two! If you could see your face, you would think it was the end of the world.",
         choices=[C("Mevrouw, I need garlic for a ward.", "n_garlic", cond="!" + F + "got_garlic"),
                  C("What do you make of all this, Mevrouw?", "n_think"),
                  C("[Leave her to her onions]", end=True)]),
    n_garlic=N("Mevrouw Bakker", "A ward? Is that what they call it at the University? My grandmother hung garlic in Zeeland to keep the plague away. Take the best braid, Professor, and put it where it does the most good.",
               do=[{"give": "garlic"}, {"set": F + "got_garlic"}], next="n0"),
    n_think=N("Mevrouw Bakker", "I think you work too hard, I think she is braver than any of us, and I think a house with a sick-room needs one woman who says nothing clever. That is me. Eat something.", next="n0"),
)

DIALOGUE[F + "cabby_talk"] = D(
    "n0",
    n0=N("Jan", "Cold, Herr Professor. Colder than the Zuider Zee in March. Cab? The coach for Cologne goes from the corner when you are ready, and not before.",
         choices=[C("What do you hear of the south?", "n_south"), C("Where might a man lose a key in my house?", "n_key"), C("[Nod and move on]", end=True)]),
    n_south=N("Jan", "The post-boys say the Styrian road is cut at Kirchdorf with snow, and that no one in the village will say why they close their doors at four. A rumour, Professor. I always say: a rumour is a draught that has found a keyhole.", next="n0"),
    n_key=N("Jan", "Where would a clever man hide a thing from himself, Professor? Under his own nose. I once found my watch in my boot. Check what you look at every day without seeing it.", next="n0"),
)

DIALOGUE[F + "student_talk"] = D(
    "n0",
    n0=N("The student", "Professor! Is it true the Dean means to have you disgraced on Friday? They say he has the whole Faculty behind him.",
         choices=[C("Never mind the Dean. What does he say about me?", "n_dean"), C("What are you reading under that Boerhaave?", "n_book"), C("[Move on]", end=True)]),
    n_dean=N("The student", "That you put stories of ghouls in your lectures and call them medicine. That a physician who believes in peasants' tales has no business teaching the sons of the Burghers.", next="n0"),
    n_book=N("The student", "Calmet. On vampires. I thought it was a joke, but Herr Seward from London says you gave it him to read. Are you cross?", next="n_book2"),
    n_book2=N("Van Helsing", "I am delighted. A student who reads the foolish book is a student who learns to ask what is true in it. Keep it. But read the column that is written in the margin, not the one that is printed.", next="n0"),
)

DIALOGUE[F + "seward_talk"] = D(
    "n0",
    n0=N("John Seward", "Professor! I thought it best to be early, in case the Dean tried to take the best seat.",
         choices=[C("How is your hand, Mr. Seward?", "n_hand"), C("Does the Dean ask the same questions every time?", "n_dean"), C("[Leave him to his notes]", end=True)]),
    n_hand=N("John Seward", "Healed, Sir. Thanks entirely to you. I cut myself at the dissection of the septic case, and the surgeon wished to take the hand. You would not allow it. You opened the wound with your own knife and drew out the poison with your mouth. I remember thinking you were mad.",
             next="n_hand2"),
    n_hand2=N("Van Helsing", "I was mad with fear, Mr. Seward. I had lost enough that winter. A physician may refuse to lose another. It is a very stupid thing and an excellent reason.", next="n0"),
    n_dean=N("John Seward", "Always the same three, Sir: the peasant's remedy, the mesmerist, and the thing he calls your 'Carpathian superstition'. If I were you I would look at your own blackboard. Everything he needs is there, and everything you need.", next="n0"),
)

DIALOGUE[F + "verhoeven_talk"] = D(
    "n0",
    n0=N("Professor Verhoeven", "Van Helsing. Still pinning ghost-stories to your lectures, I hear. The Faculty is gravely concerned that a physician of your gifts has gone to the dogs.",
         choices=[C("I have come for the key to the rare-book press, Dean.", "n_key", cond="!" + F + "debate_won"),
                  C("I think we should settle this today, in the open.", "n_start", cond="!" + F + "debate_won&" + F + "board_read"),
                  C("(That blackboard has the answers. I should read it first.)", "n0b", cond="!" + F + "debate_won&!" + F + "board_read"),
                  C("[Nod and step back]", end=True)]),
    n0b=N("Van Helsing", "I will study the board before I give him my reasons. A man ought to know his own argument.", next="n0"),
    n_key=N("Professor Verhoeven", "The key stays where it is. Prove to me that you are a man of science and not a man of rumours, and you shall have it. I shall ask you three questions. Fail one, and we begin again.",
            next="n0"),
    n_start=N("Professor Verhoeven", "Splendid. Three questions, then. The first: the peasants of this country swear that a hanged man's rope, bound round the brow, cures a fever. Fact, or superstition?",
              choices=[C("Fact. The peasants have observed it for centuries.", "n_fail1"),
                       C("Superstition. It has never been tested.", "q2"),
                       C("It is none of a physician's business what peasants believe.", "n_fail3")]),
    n_fail1=N("Professor Verhoeven", "Centuries of observation by whom? By people who also stopped hail with bells? It seems your own blackboard disagrees with you, Van Helsing. Again.", next="n_start"),
    n_fail3=N("Professor Verhoeven", "A physician who will not look at what the peasants believe will never learn what the peasants know. That is no answer. Again.", next="n_start"),
    q2=N("Professor Verhoeven", "Good. The second: the mesmerism in the Salpetriere, where a sleeper obeys a command given hours before. Another peasants' marvel?",
         choices=[C("No. It is observed under witness and repeated; it is fact, though we do not understand it.", "q3"),
                  C("Yes. If we cannot explain it, it cannot be real.", "n_fail2"),
                  C("It is a hoax of the French.", "n_fail2")]),
    n_fail2=N("Professor Verhoeven", "'If we cannot explain it, it cannot be real.' You wrote the opposite on the board. Begin again.", next="n_start"),
    q3=N("Professor Verhoeven", "And the third. In the Carpathians, they say, the dead rise by night and drink the blood of the living. I take it you will call that superstition by your own rule.",
         choices=[C("By my rule I may not call it so until I have tested it. I will not deny what I have not examined.", "n_won"),
                  C("It is nonsense, of course, as I have always said.", "n_fail4"),
                  C("It is certainly true. I have seen it.", "n_fail4")]),
    n_fail4=N("Professor Verhoeven", "Neither of those is your own doctrine. You are either lying to me or to yourself. Begin again.", next="n_start"),
    n_won=N("Professor Verhoeven", "...Hm. 'Disbelieve nothing you have not tested.' You have beaten me with my own favourite sentence. Very well. Take the key. But understand I will watch the day you bring the Faculty a case.",
            do=[{"give": F + "library_key"}, {"set": F + "debate_won"}, {"journal": F + "j_debate"}], next="n_won2"),
    n_won2=N("Professor Verhoeven", "And, Van Helsing. For what it is worth, my own grandmother hung garlic at her door. I should be very sorry to find she was right.", end=True),
)

DIALOGUE[F + "librarian_talk"] = D(
    "n0",
    n0=N("Mijnheer de Vries", "(whispering) Professor. The Ordo you want is in the press. The Dean has the key. The Dean also has the opinion that you should not have it.",
         choices=[C("What is the Ordo, exactly?", "n_ordo"), C("What have you in the way of Styrian travellers?", "n_styria", cond="!" + F + "shelf_read"),
                  C("Does the Dean ever read the rare books himself?", "n_dean"), C("[Nod and tiptoe away]", end=True)]),
    n_ordo=N("Mijnheer de Vries", "A rituale of the old Dutch rite. It is dull in ordinary hands. The chapter on the blessing of bread and the making of a circle is the only part anyone has ever read, and that only once, in 1731.", next="n0"),
    n_styria=N("Mijnheer de Vries", "The Folklore and Travels. Third shelf from the west, among the Natural History where they cannot do any harm.", next="n0"),
    n_dean=N("Mijnheer de Vries", "Every Sunday, in the dark, with the lamp turned down. He thinks I do not know. I should hate to be the one to tell him I have always known.", next="n0"),
)

DIALOGUE[F + "pieter_talk"] = D(
    "n0",
    n0=N("Father Pieter", "Professor. You come into my chapel perhaps twice in the year. Either you are very troubled, or you are working.",
         choices=[C("I have the Ordo and a tin of wafers. I need to consecrate them, Father.", "r0", cond="has:" + F + "rituale&has:" + F + "wafers&!" + F + "rite_done"),
                  C("What do you think of a man who tests his religion?", "n_test"),
                  C("What makes the Host the Host, Father?", "n_host"),
                  C("[Leave him to his prayers]", end=True)]),
    n_test=N("Father Pieter", "I think he is a better Christian than the man who never tests it. Faith that cannot bear a question is not faith but fear.", next="n0"),
    n_host=N("Father Pieter", "Nothing you could measure on a scale. The bread is bread, until the words and the intent are laid on it in the right order, and then it is what it is. The order matters, Professor. Do not let any man tell you it is only ceremony.", next="n0"),
    r0=N("Father Pieter", "Hm. You have the Ordo. Then let us do this properly. I will not guess at the order; you shall read it to me, and I will do as you direct. What comes first?",
         choices=[C("The priest is shriven.", "r1"), C("The hands are washed.", "f1"), C("The Collect is said over the bread.", "f1"), C("The pyx is sealed.", "f1")]),
    f1=N("Father Pieter", "(frowning) No, that is not what the Ordo says. 'Before the bread is blessed the hands must be washed; before the hands are washed the priest must be shriven.' Let us begin again.", next="r0"),
    r1=N("Father Pieter", "(He kneels, speaks low, rises lighter.) I am shriven. What now?",
         choices=[C("The hands are washed.", "r2"), C("The Collect is said over the bread.", "f1"), C("The pyx is sealed.", "f1")]),
    r2=N("Father Pieter", "(He washes his hands in the font, breaking the ice with his knuckles.) Clean. And now?",
         choices=[C("The Collect is said over the bread.", "r3"), C("The pyx is sealed.", "f1")]),
    r3=N("Father Pieter", "(Over the wafers, in a voice I have not heard him use before, the Latin runs like water.) And last?",
         choices=[C("The pyx is sealed.", "r4")]),
    r4=N("Father Pieter", "(He closes the little silver box and presses the cross on its lid.) It is done. These are no longer bread. Take them with the blessing of this house, and may you never need them. And if you do, Professor, remember that the Host is not a charm but a reproach: it works only on those who know what it is.",
         do=[{"take": F + "wafers"}, {"give": "host"}, {"set": F + "rite_done"}, {"journal": F + "j_rite"}], end=True),
)

DIALOGUE[F + "gerrit_talk"] = D(
    "n0",
    n0=N("Old Gerrit", "WHAT? Ah, the Professor! I was saying, the Father is a good man but he washes his hands with a great deal of ice about it.",
         choices=[C("Is there anything in the order of the Mass that people forget?", "n_order"), C("[Smile and move on]", end=True)]),
    n_order=N("Old Gerrit", "Forget? Forty years I have set the table for it. Confess first, wash after, bless the bread, close the box. The Father mutters if I put the water out before he has been to the box. Sacristans know these things, Professor. We just never get asked.", next="n0"),
)

DIALOGUE[F + "pastor_talk"] = D(
    "n0",
    n0=N("Pfarrer Albrecht", "Professor Van Helsing? Thank God. I have written to nine men and been answered by one. I had begun to think my letter was a kind of madness.",
         choices=[C("Tell me what you know.", "n_tale"), C("I wish to see the churchyard, Pfarrer.", "n_leave", cond="flag:" + F + "heard_tale&!" + F + "pastor_leave"),
                  C("[Leave him]", end=True)]),
    n_tale=N("Pfarrer Albrecht", "Four children of the village have wasted this winter. Pale, listless, two small marks at the throat. I buried one of them. Then I found, at dawn, that the snow on the north side of the churchyard had gone as if a fire had been lit under it. One grave only. I will not say which, for I have not the courage. Ask the old ones.",
             do=[{"set": F + "heard_tale"}], next="n0"),
    n_leave=N("Pfarrer Albrecht", "(He closes his eyes.) You will do it by night? I have no right to refuse; I have only the fear of a priest who has seen what a Christian burial cannot hold. Go. Matthias has the gate. Say a Pater for me at whichever grave it is.",
              do=[{"set": F + "pastor_leave"}, {"journal": F + "j_pastor"}], next="n0"),
)

DIALOGUE[F + "sexton_talk"] = D(
    "n0",
    n0=N("Matthias", "I do not talk of it, Herr. I dig. I do not ask who it is I dig for.",
         choices=[C("The grave that has no snow upon it. Do you know which?", "n_snow", cond=F + "heard_tale&!" + F + "know_stone"),
                  C("A girl, nineteen. A wedding-dress. Is it Katharina Lindner?", "n_yes", cond=F + "widow_tale&!" + F + "know_stone"),
                  C("Is there anything I should know about the gate?", "n_gate"), C("[Leave him]", end=True)]),
    n_snow=N("Matthias", "Three stones are by the north wall. Anna Pfeifer, who was a saint. Josef Hauer, who was a thief. And a third. Ask the old Frau Lindner; she is the only one who still says the name.", next="n0"),
    n_yes=N("Matthias", "(He crosses himself.) I have driven three iron nails into that stone with my own hand. Twice the nails were out by morning. Yes, Herr. She is the one. God help me for saying it aloud.",
            do=[{"set": F + "know_stone"}, {"journal": F + "j_grave"}], next="n0"),
    n_gate=N("Matthias", "The lantern will not stay lit beyond the third stone. Go by the moon. And, Herr, do not step on the snow where it has thawed.", next="n0"),
)

DIALOGUE[F + "widow_talk"] = D(
    "n0",
    n0=N("Frau Lindner", "A stranger. A doctor, they say. Then you are the one who will open the grave, and I will tell you what I should have said to the Pfarrer's face seventy years ago.",
         choices=[C("Who lies there, Frau Lindner?", "n_who"), C("[Sit and listen to the whole story]", "n_story", cond="flag:" + F + "heard_tale&!" + F + "widow_tale"),
                  C("[Thank her and go]", end=True)]),
    n_who=N("Frau Lindner", "My aunt. She was nineteen, a bride of the spring, and the prettiest girl in three parishes. Ask me no more until you have listened.", next="n0"),
    n_story=N("Frau Lindner", "It was the year of the great snow, when the wolves came into the street. My aunt Katharina wed the miller's son in March and was dead by Easter. She lay in the church for three days with a bloom on her cheek like a living girl. The priest, who was old and wise, drove an ash-nail through the coffin-lid, and the sexton nailed three more to the stone. Still the children sickened.",
            next="n_story2"),
    n_story2=N("Frau Lindner", "My mother used to say she walked on the night of the great thaw, and that she asked for her husband by name at his window. Katharina Lindner. A bride of the spring. Say it once to the sexton, Herr, and he will give you the gate.",
               do=[{"set": F + "widow_tale"}], end=True),
)

DIALOGUE[F + "huber_talk"] = D(
    "n0",
    n0=N("Landlord Huber", "A hot wine for the Herr Doctor. Or a hot soup. We have both, and I fear that is all we have.",
         choices=[C("Why so much garlic on the windows?", "n_garlic"), C("When did the trouble begin?", "n_begin"), C("[Thank him]", end=True)]),
    n_garlic=N("Landlord Huber", "My wife's idea. Do not ask me if it works; ask me if I sleep. I do. That is all the evidence I need.", next="n0"),
    n_begin=N("Landlord Huber", "At the first thaw. A child at the Meyer farm, then a girl at the mill. By the Feast of the Three Kings the village shut its doors at four. They say the Pfarrer wrote for help to a man in Holland. We did not think he would come.", next="n0"),
)

DIALOGUE[F + "herdsman_talk"] = D(
    "n0",
    n0=N("The herdsman", "You are the learned gentleman. Tell me, Herr, is it true that you can tell by looking at a man whether he is sick of body or sick of mind?",
         choices=[C("Sometimes. Why?", "n_why"), C("[Leave him]", end=True)]),
    n_why=N("The herdsman", "My daughter Resi has been weak since the thaw. She says a pretty lady stands at her window and sings. I told her it was a dream. The Pfarrer says it is not, and I dare not hear him say why.", next="n0"),
)

DIALOGUE[F + "final_letter"] = D(
    "n0",
    n0=N("Van Helsing", "Arminius has written again. The black edge is not for himself; it is for the friend who died in Buda-Pesth last month. At the foot, in his shaking hand, a postscript: 'Abraham, what I told you of the Voivode - a letter came to me from a Transylvanian monk. The name that he used for the family in the end was not Voivode, but Dracula.'",
         choices=[C("[Put the letter in the casebook]", "n_end")]),
    n_end=N("Van Helsing", "I sit with it for a long time, the lamp low, the snow falling across the canal. Upstairs she coughs and sleeps. I had thought I was putting a ghost to rest. It is very clear to me tonight that I have only learned what the ghost looks like. The fight is not over, and I am not, I think, the man who will finish it. But I shall teach the man who will.",
            do=[{"journal": F + "j_end"}, {"card": "Years later, a London doctor wrote to an old teacher in Amsterdam: 'Come at once, if convenient; if not, come anyhow.'"}, {"arc_end": 1}], end=True),
)

# ----------------------------------------------------------------------------------------------------------- items
ITEMS = {
    F + "casebook": dict(name="Van Helsing's casebook", asset="book", variant="leather", desc="Two columns on every page: what I saw, and what I was told."),
    F + "cabinet_key": dict(name="Cabinet key", asset="key", variant="gold", desc="A small brass key, for the cabinet where Arminius's letters are kept."),
    F + "letters": dict(name="Arminius's letters", asset="book", variant="diary", desc="Three Hungarian letters on the Voivode, the Scholomance and a Styrian village."),
    F + "library_key": dict(name="The Dean's brass key", asset="key", variant="gold", desc="Cold brass, warm only where the Dean's thumb has held it. Opens the rare-book press."),
    F + "rituale": dict(name="Old Dutch Ordo", asset="book", variant="red", desc="'Before the bread is blessed the hands must be washed; before the hands are washed the priest must be shriven; the Collect is said over the bread, and the pyx is sealed last.'"),
    F + "wafers": dict(name="Tin of unblessed wafers", asset="chest", variant="pale", desc="Flour and water, cut thin. Not yet a sacrament."),
    F + "child_cross": dict(name="A child's silver cross", asset="crucifix", variant="silver", desc="Small, bright and made for a christening. It was not made to be put away."),
    F + "ward": dict(name="The ward", asset="book", variant="diary", desc="A linen square holding a consecrated Wafer, a child's silver cross and a braid of garlic, bound in red thread."),
    F + "bag": dict(name="Van Helsing's black medical bag", asset="chest", variant="dark", desc="Scarred black leather, brass clasps. Lancets, a stethoscope, a bottle of brandy, and in the lid a pyx of consecrated wafers."),
}

# ----------------------------------------------------------------------------------------------------------- journal
J = lambda title, text: dict(title=title, source="Van Helsing's casebook", text=text)
JOURNAL = {
    F + "j_study": J("The study", "My study, with the lamp lit before dark. Arminius's last parcel lies half-opened: a Latin note, a locked cabinet, and a letter I have not dared to read twice. I must see to my wife, my lecture, my friend, and at last that terrible village in Styria."),
    F + "j_latin": J("The Latin note", "'Wood not iron; day not night; garlic not earth.' Arminius has the exactness of a man who has had it wrong once and paid. I wrote it out three times, since a physician who mistranslates a prescription kills a man."),
    F + "j_home": J("My wife", "She lay turned to the window, with the little grey coat in her lap. Mevrouw Bakker says the broth is a triumph. I stood in the doorway and could not enter for a full minute. We have lost one child. I do not intend to lose the rest of the world."),
    F + "j_cross": J("The silver cross", "She gave me the christening cross from the cradle. 'Take it for the next one', she said. I am a Doctor of Medicine and Law, but I could find no word, and so I held her hand. Some wounds are not the business of surgery."),
    F + "j_street": J("The Herengracht", "Skaters, a barrel-organ, the bells of the Oude Kerk. The Dean of the Faculty means to humiliate me on Friday. My students are afraid for me. They are fond of me, which is more than I deserve and a great deal more than I can bear in the open street."),
    F + "j_lecture": J("The lecture-room", "Verhoeven stood where I stand, with his gloves in one hand and my own board behind him. He has the key to the rare books, and a rule: no man gets it who cannot defend his methods. Young Seward, with that scar on his hand, whispered that I should read what I wrote."),
    F + "j_debate": J("The Dean is answered", "Three questions, three answers from my own blackboard. Verhoeven gave me the key and a word I shall not forget: his grandmother hung garlic at her door. Everyone has one such grandmother. The trick is to listen to her before the Faculty tells you not to."),
    F + "j_library": J("The rare-book press", "Calf, vellum and a smell of mice. Mijnheer de Vries whispers, and the Dean's press is oak and brass. Inside it is the only book I wanted: a rituale of the old rite, and the order of the blessing of bread, in a Latin that has lasted since the Reformation."),
    F + "j_letters": J("Arminius's letters", "The Voivode, the Scholomance, the Devil's tenth scholar. Arminius does not believe a word, but he copies every one. And at the end a request: a churchyard in Styria, a priest afraid of his own graves. I shall go, but not to disprove. To find out."),
    F + "j_chapel": J("St. Nicholas", "Father Pieter at his altar, Gerrit counting the candle-ends. The sacrament is not a charm but a rite, and a rite has its order. That is the one thing a physician and a priest can agree on: if you do it out of sequence, you have done something else."),
    F + "j_rite": J("The Host consecrated", "Confession, ablution, the Collect, the seal. I read the order and Father Pieter followed it, and when the little silver box closed, something in the room changed that I have no instrument to measure. I did not pretend that I understood it. I merely wrote it down."),
    F + "j_village": J("Kirchdorf", "Snow, an onion-spire, doors shut at four. A priest with a month of sleeplessness in his face. The village is afraid of its own churchyard. I have not yet asked what it is afraid of. I have only looked at the garlic on the windows, and counted."),
    F + "j_pastor": J("Pfarrer Albrecht", "Four children weak, one buried, and a grave that melts the snow. He asked me to say a Pater at whichever one it is. I said I would. I did not say that I had never until that night said a Pater with a stake in my other hand."),
    F + "j_grave": J("Katharina Lindner", "A bride of nineteen, dead by Easter in the year of the great snow, nailed in by an old priest and an older sexton. Three nails on the stone, and the earth about it not frozen. It is not a theory any longer. It is a name."),
    F + "j_vigil": J("The vigil", "She came at midnight, hair pale in the moon, as lovely as the legend said. The circle held. She did not. When she lay helpless in the snow, I did what must be done, and I said the Pater, and I wept afterward, as a physician does when a patient is lost. She was somebody's niece."),
    F + "j_end": J("What I have learned", "Verhoeven was right to demand evidence, and the peasants were right to be afraid, and the truth was in neither camp but between them. Arminius has sent a name: Dracula. I do not know what lies behind it. I have a casebook, a ward, and a certain faith that works when the evidence runs out."),
}

# ----------------------------------------------------------------------------------------------------------- combat
ENEMIES_EXTRA = {
    F + "revenant": dict(name="Katharina Lindner", model="human_lucy", hp=20, spd=5, dmg=[3, 5], acc=66, eva=10, tags=["vampire", "undead"], nerve_hit=2,
                         abilities=["charm", "bite"], book="the Styrian churchyard (invented)"),
}
ENCOUNTERS_EXTRA = {
    ENC: dict(name="The vigil at Kirchdorf", time="night", enemies=[F + "revenant", "wolf"], flee_ok=True,
              intro="The snow does not crunch beneath her. She stands at the edge of the circle, smiling the smile of a girl of nineteen, and behind her in the dark a great grey wolf comes to heel like a dog. 'You are very far from home, Herr Doktor,' she says in a village dialect seventy years out of date.",
              win="She falls, and does not rise. The wolf is gone. In the snow, there is only a girl in a grey dress, and no more than nineteen.", location=F + "churchyard"),
}
_END = [{"set": F + "vigil_done"}, {"journal": F + "j_vigil"},
        {"card": "The snow stops before dawn. The Pfarrer reads the burial service himself over a grave that is at last, and only now, a grave. Two weeks later, Amsterdam."},
        {"goto": F + "study"}]
ENCOUNTER_HOOKS = {
    ENC: dict(
        on_win=[say("It is over. It is not nothing, to have done it.")] + _END,
        on_lose=[say("I come to myself in the snow with the circle in tatters. The Pfarrer's lantern bobs by the gate, and somebody, I think the old sexton, has done what I could not. The grave is quiet.")] + _END,
        on_flee=[say("I retreat through the lychgate with the creature's laughter behind me. Matthias and the Pfarrer, with ash and iron, finish the work by dawn. I am ashamed, and alive.")] + _END),
}

# ----------------------------------------------------------------------------------------------------------- seed variation
PALETTES = {
    F + "study": [dict(wall="plaster_dirty", floor="planks", wood="dark", cloth="red"), dict(wall="plaster", floor="planks", wood="oak", cloth="green")],
    F + "library": [dict(wall="plaster_dirty", floor="planks", wood="dark", cloth="green"), dict(wall="plaster", floor="planks", wood="ebony", cloth="black")],
    F + "home": [dict(wall="plaster", floor="planks", wood="pale", cloth="blue"), dict(wall="plaster_dirty", floor="planks", wood="oak", cloth="red")],
    F + "lecture": [dict(wall="plaster", floor="planks", wood="oak", cloth="green"), dict(wall="plaster_dirty", floor="planks", wood="dark", cloth="black")],
}

PLACEMENTS = {
    F + "cabinet_key": [
        dict(prop=F + "bust", text="Under the plaster bust of Boerhaave, a small brass key: the cabinet key.", hint="Boerhaave stands a finger's width off his usual ring on the shelf."),
        dict(prop=F + "clock", text="Taped inside the case of the tall clock, a small brass key: the cabinet key.", hint="The tall clock has been opened; the pendulum is lopsided."),
        dict(prop=F + "shelf1", text="Behind a volume of Sydenham, on a nail, a small brass key: the cabinet key.", hint="One volume of Sydenham sits proud of the rest."),
    ],
}
