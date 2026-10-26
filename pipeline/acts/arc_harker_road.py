"""PERSONAL ARC - "The Solicitor's Road": Jonathan Harker around the novel (Exeter prologue; ch.4 end, ch.9).
All ids are written with a leading '@' which is expanded to 'harker_road_' at the bottom of the file."""
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


H = "Jonathan"
M = "Jonathan Harker's diary"

ARC = dict(
    id="harker_road", title="The Solicitor's Road", member="harker", portrait="harker",
    blurb="Jonathan Harker's own road: from Mr. Hawkins's office in Exeter and the Count's letters, over the castle wall, to a sickbed in Buda-Pesth and a wedding.",
    unlock="roster:harker&journal:a1_j7",
    unlock_text="Finish Act I: Jonathan's last chance in the castle.",
    after_credits=False,
    start=dict(location="@close", protagonist="harker", party=["harker"], items={}, flags=[]),
    exit_to="ARC_END",
    rewards=[dict(give="tweed_travelling_coat"), dict(give="kukri"), dict(give="@sealed_journal"), dict(stat=dict(member="harker", hp=2, nerve=3, acc=1))],
    rewards_text="Jonathan receives a kukri and his sealed journal; +2 HP, +3 Nerve, +1 Accuracy for Harker Gear: a tweed travelling coat.",
)

LOCATIONS = [
    dict(id="@close", name="Cathedral Close, Exeter", desc="A fine May morning under the cathedral towers. Rooks, cabs, and a flower-seller with the whole of Devon in her basket.", date="May 1887"),
    dict(id="@office", name="Hawkins & Harker, Solicitors", desc="Mr. Hawkins's office: deed-boxes to the ceiling, a fire kept up in all weathers, and a quill that has signed more conveyances than the Archbishop.", date="Exeter"),
    dict(id="@archive", name="The muniment room", desc="A cool vault under the office where the firm keeps what it cannot bear to throw away.", date="Exeter"),
    dict(id="@school", name="The schoolroom", desc="Slates, a globe, a blackboard with a chalk drawing of the Exe, and the faint smell of ink and apples.", date="Exeter"),
    dict(id="@lodging", name="Jonathan's lodgings", desc="Two rooms above Mrs. Dunmore's linen-draper's. His father's trunk stands under the window, locked these many years.", date="Exeter"),
    dict(id="@churchyard", name="St. Petroc's churchyard", desc="Where the Harkers lie, in the corner by the yew where the sun comes last.", date="Exeter"),
    dict(id="@museum", name="The Reading Room, British Museum", desc="Under the great dome, a hundred readers rustle like a wood in autumn. Somewhere in these catalogues is the whole of Transylvania.", date="London"),
    dict(id="@wall", name="The castle wall, by night", desc="Hundreds of feet of sheer stone under the moon, and a window left open on the Count's side. Below, the whole country lies bright and silent.", date="Night, early summer"),
    dict(id="@count_room", name="The Count's room", desc="An empty room that is not empty. It smells of old earth, and a heap of gold lies in the corner like rubbish.", date="Night"),
    dict(id="@vault", name="The ruined chapel and its vault", desc="Down a winding stair, the dead air of an old burial-place. Fifty great boxes of earth stand in the gloom.", date="Night"),
    dict(id="@path", name="The mountain path", desc="A goat-track under the stars. Far below, a river; somewhere nearer, wolves and a Szgany fire.", date="Night"),
    dict(id="@ward", name="Hospital of St. Joseph and Ste. Mary, Buda-Pesth", desc="A long white ward where the Sisters go about in silence. A bed by the window, and a nun who does not leave it.", date="Some weeks later"),
    dict(id="@garden", name="The hospital garden", desc="Lime trees, gravel walks and a few patient convalescents in chairs.", date="Buda-Pesth"),
    dict(id="@chapel", name="The hospital chapel", desc="Small, whitewashed, bright with candles and with a wreath of white roses over the altar.", date="Buda-Pesth"),
]

LOC_DATA = {}

# ===================================================== EXETER =============================================================
LOC_DATA["@close"] = dict(
    cells=[4, 3], wall="stone_grey", floor="cobble", interior=False,
    ambient=AMBIENT["day_exterior"], camera=cam([4, 3]), lights=lights_day(),
    scatter=dict(asset="pine_small", variant="green", count=10, seed=21, avoid=[[-8, -6, 8, 6]]),
    spawn=[0, 4.0],
    spawns={"@office": [-5.4, -1.4], "@school": [5.4, -1.4], "@lodging": [0, -3.8], "@churchyard": [5.4, 2.4], "@museum": [-5.4, 3.0]},
    props=[
        prop("@c_tower", "tower", "stone_grey", 0.0, -6.2, scale=0.9, name="The cathedral", radius=1.4,
             look="Two Norman towers, a great west front, and four hundred years of rooks. Mr. Hawkins says it is the only client the firm has never sent a bill."),
        prop("@c_arch_office", "arch", "stone_grey", -6.6, -1.4, rot=90, name="Hawkins & Harker, Solicitors", radius=0.8,
             look="A brass plate worn to a shine by thirty years of the housemaid. The door of the office.", go="@office"),
        prop("@c_arch_school", "arch", "stone_grey", 6.6, -1.4, rot=-90, name="Miss Pell's School for Girls", radius=0.8,
             look="A tidy gate and a tidy bell. Mina Murray teaches the junior class here and has views on the bell.", go="@school"),
        prop("@c_arch_lodging", "arch", "stone_dark", 0.0, -4.6, name="Mrs. Dunmore's, linen-draper", radius=0.8,
             look="Bolts of calico in the window and, above, my two rooms with the green blind.", go="@lodging"),
        prop("@c_arch_church", "arch", "stone_mossy", 6.6, 2.4, rot=-90, name="Lych-gate of St. Petroc's", radius=0.8,
             look="A little roofed gate where coffins once waited for the priest. Not today, thank God.", go="@churchyard"),
        prop("@c_fountain", "column_short", "stone_grey", 0.0, 0.2, name="Drinking fountain", radius=0.7,
             look="A fountain with a tin cup on a chain, and a motto: 'Ye shall draw water with joy.'"),
        prop("@c_bench", "bench", "oak", -3.4, 1.6, rot=90, name="Bench", radius=0.8, look="Warm from the sun. A clerk is asleep upon the Times beside it."),
        prop("@c_lamp", "lantern", "default", 3.4, 0.4, name="Gas-lamp", radius=0.3, look="Unlit. Lamplighter's ladder leans on the next one, abandoned for his dinner."),
        prop("@c_post", "signpost", "dark", 4.4, 3.4, rot=-20, name="Signpost", radius=0.3,
             look="'Station 1 mile. London 194 miles.' Someone has added, in pencil, 'and back'."),
        prop("@c_cab", "carriage", "dark", -5.0, 3.6, rot=60, name="Hansom cab", radius=1.2,
             look="Stand No. 4. The cabman has a whip, a pipe, and a very low opinion of the Great Western Railway.", talk="@cabman"),
        prop("@c_barrel", "barrel", "oak", 2.4, 3.6, name="Rain-barrel", radius=0.5, look="Green water and three drowned leaves."),
        prop("@c_tomb", "gravestone", "stone_mossy", -4.6, -3.8, name=None, radius=0.5),
    ],
    npcs=[
        npc("@flower_girl", "human_peasant_f", "village_woman", 2.2, 1.6, rot=180, name="Flower-seller",
            look="A girl with a basket of violets and a very good memory for faces.", talk="@flowers"),
        npc("@cabman", "human_coachman", "driver", -4.0, 2.6, rot=90, name="Cabman",
            look="A big man in a drab coat, who has driven half of Exeter to its weddings and the other half to its funerals.", talk="@cabman"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="@j_morning")])],
)

LOC_DATA["@office"] = dict(
    cells=[3, 2], wall="plaster_dirty", floor="planks", interior=True,
    ambient=AMBIENT["warm_day_interior"], camera=cam([3, 2]), lights=lights_warm([3, 2], energy=2.6),
    walls=dict(north=["wall_4", "wall_window_4", "wall_4"], west=["wall_door_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[4.6, 1.8], spawns={"@close": [4.6, 2.0], "@archive": [-4.6, -2.0]},
    props=[
        prop("@o_desk", "table", "dark", 0.4, -1.8, name="Mr. Hawkins's desk", radius=0.9,
             look="Mahogany, leather-topped, and as orderly as a conscience. A decanter, a blotter, and a calendar open at May."),
        prop("@o_letters", "book", "red", 0.0, -1.8, y=0.8, name="The Count's letters", radius=0.2,
             look="A bundle of heavy cream letters in a small, upright foreign hand. The envelopes bear a Transylvanian stamp and the seal of a wolf's head.",
             take="@counts_letters", take_text="I tie the bundle with its pink tape and put it in my breast pocket. Mr. Hawkins has told me to keep it safe.", give_once=True),
        prop("@o_pen", "bottle", "amber", 0.9, -1.8, y=0.8, name="Pen and ink", radius=0.2,
             look="A steel pen, a bottle of Stephens' ink, and a pen-wiper in the shape of a hedgehog.",
             take="@pen", take_text="Mr. Hawkins nods as I pocket the pen. 'Take it. I have three.'", give_once=True),
        prop("@o_copybook", "book", "leather", 1.6, -1.8, y=0.8, name="Letter-press copy-book", radius=0.2,
             look="Our own replies to the Count, copied in damp tissue. A history of the purchase in nine letters.", talk="@copybook"),
        prop("@o_pell_desk", "table", "pale", -3.4, -1.2, name="Pell's high desk", radius=0.9,
             look="A tall desk with a sloping top and a stool, from which Mr. Pell has watched the street for thirty-one years."),
        prop("@o_shelf1", "bookshelf", "dark", -3.6, -3.55, name="Law reports", radius=0.8,
             look="Every volume of Chancery since the Restoration. Only the dust is complete."),
        prop("@o_shelf2", "bookshelf", "dark", 4.2, -3.55, name="Deed-boxes and ledgers", radius=0.8,
             look="Black tin boxes marked with the names of every family in Devon. 'Harker' is not among them; my father never had the money to need a solicitor."),
        prop("@o_fire", "fireplace", "plaster", 0.0, -3.5, name="Fireplace", radius=0.9,
             look="A fire kept up from October to May and sometimes in June. Mr. Hawkins says his bones are older than he is."),
        prop("@o_clock", "chest", "ebony", 4.8, -0.2, rot=-90, scale=0.6, name="Wall-clock case", radius=0.5,
             look="Seven minutes fast. Mr. Hawkins likes his clerks early, and the clock knows it."),
        prop("@o_rug", "rug", "red", 0.4, 0.4, name=None, radius=0.1),
        prop("@o_chair_client", "chair", "green", 0.4, 0.2, rot=0, name="Client's chair", radius=0.4, look="Deep, hard, and designed to make a man tell the truth."),
        prop("@o_stand", "barrel", "dark", 4.9, 3.0, scale=0.6, name="Umbrella stand", radius=0.4, look="Four umbrellas, none of them mine, and a cricket bat."),
        prop("@o_sconce", "sconce", "default", -5.7, 1.0, y=1.5, rot=90, name=None, radius=0.1),
        prop("@o_door_close", "door", "dark", 5.8, 2.0, rot=-90, name="Door to the Close", radius=0.6,
             look="The street door, with the brass plate behind it.", go="@close"),
        prop("@o_door_archive", "door", "oak", -5.8, -2.0, rot=90, name="Door to the muniment room", radius=0.6,
             look="A low oak door with an iron keyhole the size of a florin. The firm's old papers lie behind it.", go="@archive",
             go_cond="has:@archive_key", go_fail="Locked. Mr. Pell keeps the key to the muniment room, and Mr. Pell keeps it like a relic."),
    ],
    npcs=[
        npc("@hawkins", "human_seward", "doctor", 0.6, -0.4, rot=180, name="Mr. Peter Hawkins",
            look="My employer and, since my father died, something nearer to a father: white-haired, spectacled, kind, and never wrong about a deed.", talk="@hawkins"),
        npc("@pell", "human_peasant_m", "@pell", -3.4, 0.2, rot=90, name="Mr. Pell, the clerk",
            look="A narrow man in black alpaca with a pen behind each ear. He has the muniment key on a chain across his waistcoat and will tell you so.", talk="@pell"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="@j_commission")])],
)

LOC_DATA["@archive"] = dict(
    cells=[2, 2], wall="stone_grey", floor="stone_dark", interior=True,
    ambient=AMBIENT["cold_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2], energy=2.2),
    walls=dict(north=["wall_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[2.6, -2.0], spawns={"@office": [2.6, -2.0]},
    props=[
        prop("@a_door", "door", "oak", 3.8, -2.0, rot=-90, name="Door to the office", radius=0.6, look="The way back up to Mr. Hawkins's office.", go="@office"),
        prop("@a_box", "chest", "ebony", -1.6, -3.0, name="Locked deed-box", radius=0.6,
             look="A black japanned box stamped 'PURCHASES - TRANSYLVANIA - PRIVATE'. Mr. Hawkins has the surveys inside, and a lock that wants its own key.",
             use_item={"@box_key": [dict(say="The key turns with a grind of old iron. Inside, three bound surveys of London houses: Hampstead, Whitby and Purfleet."),
                                    dict(give="@surveys"), dict(set="@box_open"), dict(journal="@j_surveys")]},
             use_fail="I have nothing that fits the lock. Somewhere in this room, a spare key is kept by habit."),
        prop("@a_shelf", "bookshelf", "dark", 0.6, -3.5, name="Old conveyances", radius=0.8,
             look="Rolls and bundles in red tape. A tabby cat has made its bed in 'Smith v. Smith'."),
        prop("@a_stool", "chair", "black", 1.8, 0.0, name="Archivist's stool", radius=0.4, look="Three-legged, with a cushion that has been sat flat by clerks since the Reform Bill."),
        prop("@a_lantern", "lantern", "default", -2.8, 1.2, name="Hanging lantern", radius=0.3, look="Hung from a hook by the shelves. There are scorch marks where the clerks tapped their pipes."),
        prop("@a_barrel", "barrel", "dark", -3.0, -1.0, scale=0.7, name="Barrel of old seals", radius=0.4,
             look="Lumps of broken wax, in every colour. A box of the firm's own old stamps lies on top."),
        prop("@a_candle", "candle", "white", 0.0, 2.4, y=0.0, name=None, radius=0.2),
        prop("@a_rug", "rug", "black", 0.0, 0.8, name=None, radius=0.1),
        prop("@a_table", "table", "pale", 1.4, 2.0, name="Reading table", radius=0.8,
             look="Wet-ringed and ink-spattered. On it, a magnifying-glass and a note in Mr. Pell's hand: 'Surveys NOT to leave the room except by Mr. Hawkins.'"),
    ],
    npcs=[],
    on_enter=[dict(once=True, do=[dict(say="The air is cold and dry as paper. Everything in this room has been waiting a long time for somebody to need it.")])],
)

LOC_DATA["@school"] = dict(
    cells=[2, 2], wall="plaster", floor="planks", interior=True,
    ambient=AMBIENT["warm_day_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2], energy=2.6),
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_4", "wall_door_4"], east=["wall_4", "wall_4"]),
    spawn=[-2.6, 2.0], spawns={"@close": [-2.6, 2.0]},
    props=[
        prop("@s_door", "door", "pale", -3.8, 2.0, rot=90, name="Door to the street", radius=0.6, look="The schoolroom door, with a coat-peg for each child.", go="@close"),
        prop("@s_board", "bookshelf", "ebony", 0.0, -3.5, scale=1.0, name="Blackboard", radius=0.9,
             look="A chalk-drawn map of the Exe, and under it a line in neat shorthand. Mina has copied it out in longhand beside: 'Courage, mon ami.'"),
        prop("@s_desk", "table", "pale", 1.8, -1.4, name="Mina's desk", radius=0.9,
             look="Slates, a ruler, a jar of pens, and a pile of copybooks, marked in red with kind, firm ticks."),
        prop("@s_primer", "book", "red", 1.4, -1.4, y=0.8, name="Pitman's primer", radius=0.2,
             look="'Phonographic Teacher.' Mina has been teaching herself shorthand, so as to be useful to a husband. She has not said which one."),
        prop("@s_globe", "bust", "plaster", -2.4, -2.6, scale=0.7, name="School globe", radius=0.4,
             look="Europe, with Transylvania a smudge of green by a thumbprint. Mina has underlined it in pencil."),
        prop("@s_desks", "bench", "oak", -1.0, 0.8, rot=90, name="Children's bench", radius=0.8, look="Carved with initials, and one confession: 'H.S. loves a ginger cat.'"),
        prop("@s_desks2", "bench", "oak", 1.0, 1.8, rot=90, name=None, radius=0.6),
        prop("@s_stove", "fireplace", "plaster", 3.4, 0.0, rot=-90, name="Stove", radius=0.8, look="Cold. The children have drawn a smiling face in the soot."),
        prop("@s_plant", "bottle", "green", 2.8, -3.0, y=0.9, name="Geranium", radius=0.2, look="A red geranium on the sill, the only thing in the room not marked for punctuality."),
    ],
    npcs=[
        npc("@mina", "human_mina", "mina", 0.6, -0.4, rot=180, name="Mina Murray",
            look="Mina in her grey school dress, ink on her finger, a pencil in her hair, and the kind of attention that makes one feel the only man in Devon.", talk="@mina_school"),
        npc("@pupil", "human_peasant_f", "village_woman", -1.8, 0.2, rot=90, name="A small pupil",
            look="Seven years old and standing on the bench to see the visitor properly.", talk="@pupil"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="@j_mina")])],
)

LOC_DATA["@lodging"] = dict(
    cells=[3, 2], wall="plaster", floor="planks", interior=True,
    ambient=AMBIENT["warm_day_interior"], camera=cam([3, 2]), lights=lights_warm([3, 2], energy=2.4),
    walls=dict(north=["wall_4", "wall_window_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[4.6, 2.0], spawns={"@close": [4.6, 2.0]},
    props=[
        prop("@l_door", "door", "pale", 5.8, 2.0, rot=-90, name="Stairs to the street", radius=0.6, look="Eleven steps and the smell of calico.", go="@close"),
        prop("@l_trunk", "chest", "ebony", -3.8, -2.6, name="Father's trunk", radius=0.7,
             look="A brass-bound sea-trunk with a four-wheel combination lock, taken from my father's room when he died. I have never opened it.", talk="@trunk"),
        prop("@l_bed", "bed", "blue", 3.8, -2.4, name="My bed", radius=1.0, look="A narrow bed made with Mrs. Dunmore's hospital corners.", talk="@dream0"),
        prop("@l_table", "table", "oak", 0.4, -1.8, name="Writing-table", radius=0.9, look="My shorthand notes, a razor-strop, and a half-written letter to Mina, which I keep failing to finish."),
        prop("@l_diary", "book", "diary", 0.4, -1.8, y=0.8, name="My new diary", radius=0.2,
             look="A stout little book bound in black. Mina gave it to me for the journey and said I must keep it in shorthand 'so that nobody can read your nonsense but me'.",
             take="@diary", take_text="I put the diary in my coat. Mina is right: a traveller who writes nothing down has seen nothing.", give_once=True),
        prop("@l_valise", "chest", "pale", -0.4, 2.4, scale=0.7, name="Travelling valise", radius=0.5,
             look="Half packed. Shirts, collars, and a small box of seidlitz powders in case the Count's cooking disagrees with me."),
        prop("@l_shelf", "bookshelf", "pale", 3.6, -3.55, name="My books", radius=0.8,
             look="Blackstone, Bradshaw's Railway Guide, a dog-eared 'Murray's Handbook for the Continent', and nothing a young man should be ashamed of."),
        prop("@l_mirror", "mirror", "default", -0.2, -3.7, y=1.0, scale=0.7, name="Shaving glass", radius=0.4,
             look="It shows the same plain face as every other morning: an honest, tired young man who is going somewhere."),
        prop("@l_rug", "rug", "green", -1.0, 0.4, name=None, radius=0.1),
        prop("@l_chair", "chair", "green", 1.4, -0.4, rot=180, name="Reading chair", radius=0.4, look="Mrs. Dunmore's best, loaned on condition of no pipe."),
        prop("@l_lamp", "candle", "red", 0.0, -1.9, y=0.8, name=None, radius=0.2),
    ],
    npcs=[
        npc("@dunmore", "human_peasant_f", "innkeeper_wife", 2.8, 0.6, rot=-90, name="Mrs. Dunmore",
            look="My landlady: a stout widow with a perfect understanding of the movements of every lodger in the street.", talk="@dunmore"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="@j_lodging")])],
)

LOC_DATA["@churchyard"] = dict(
    cells=[3, 3], wall="stone_mossy", floor="grass", interior=False,
    ambient=AMBIENT["day_exterior"], camera=cam([3, 3]), lights=lights_day(2.8),
    scatter=dict(asset="pine_small", variant="dark", count=14, seed=31, avoid=[[-6, -6, 6, 6]]),
    spawn=[-5.0, 2.6], spawns={"@close": [-5.0, 2.6]},
    props=[
        prop("@y_gate", "arch", "stone_mossy", -6.6, 2.6, rot=90, name="Lych-gate", radius=0.8, look="Back to the Close.", go="@close"),
        prop("@y_stone", "gravestone", "stone_grey", 1.0, -2.6, name="Harker family stone", radius=0.5,
             look="'THOMAS HARKER, SURGEON'S ASSISTANT, AND MARGARET HIS WIFE. HE DIED IN THE FEVER OF 1874, SHE FOLLOWED HIM IN THE SPRING. THEIR SON JONATHAN WAS TEN.' Someone has put snowdrops here."),
        prop("@y_stone2", "gravestone_point", "stone_dark", -2.6, -3.0, name="Stone of an unknown child", radius=0.5,
             look="'ALICE ANN, AGED 3 YEARS. SUFFER THE LITTLE CHILDREN.' A dead wreath of pimpernels."),
        prop("@y_stone3", "gravestone", "stone_mossy", 3.8, -0.6, name="Old Sexton's stone", radius=0.5,
             look="'JOB TREMLETT, 47 YEARS SEXTON OF THIS PARISH, WHO DIGGED GRAVES FOR OTHERS AND NOW LIES IN ONE FOR HIMSELF.'"),
        prop("@y_cross", "grave_cross", "stone_grey", -4.2, -1.8, name="Stone cross", radius=0.4, look="A cross, leaning gently towards the church as if to hear the sermon."),
        prop("@y_yew", "deadtree", "grey", 5.0, -3.4, name="Ancient yew", radius=0.7,
             look="Older than the church, and holding up its limbs like a man who has seen much and said little."),
        prop("@y_bench", "bench", "dark", -1.4, 1.8, rot=90, name="Bench", radius=0.8, look="A bench in the sun."),
        prop("@y_church", "tower", "stone_grey", 0.0, -5.6, scale=0.55, name="St. Petroc's", radius=1.2, look="A stumpy Saxon tower and a Georgian porch."),
        prop("@y_flowers", "bottle", "green", 1.0, -2.0, y=0.0, name="Jar of snowdrop stalks", radius=0.2,
             look="Old stalks, kept in water by someone who loves them. The verger, perhaps. Or Mina."),
    ],
    npcs=[
        npc("@verger", "human_peasant_m", "@verger", 2.8, 1.8, rot=-90, name="The verger, Mr. Pascoe",
            look="A bent old man with a billhook and a sharp tongue, who has dug the graves of three generations of Exeter.", talk="@verger"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="@j_churchyard")])],
)

LOC_DATA["@museum"] = dict(
    cells=[3, 3], wall="plaster", floor="planks", interior=True,
    ambient=AMBIENT["warm_day_interior"], camera=cam([3, 3]), lights=lights_warm([3, 3], energy=2.8),
    walls=dict(north=["wall_4", "wall_window_4", "wall_4"], west=["wall_4", "wall_4", "wall_4"], east=["wall_4", "wall_4", "wall_door_4"]),
    spawn=[4.6, 4.0], spawns={"@close": [4.6, 4.0]},
    props=[
        prop("@m_door", "door", "dark", 5.8, 4.0, rot=-90, name="Door to Great Russell Street", radius=0.6,
             look="The way out, and back to the station.", go="@close"),
        prop("@m_catalogue", "bookshelf", "ebony", -4.4, -3.55, name="The great catalogue", radius=0.8,
             look="Ranks of leather-backed volumes of pasted slips. Under TRANSYLVANIA, one entry is marked with a red ticket: 'Geography and Ethnology of the Carpathians, press-mark K.7'. The other entries are only history."),
        prop("@m_slips", "book", "diary", -4.0, -2.2, y=0.8, name="Call-slip tray", radius=0.2,
             look="A shallow tray of printed call-slips: Title, Press-mark, Name of Reader.",
             take="@call_slip", take_text="I take a blank slip. The Museum prints them in a shade of green that makes every reader feel guilty.", give_once=True),
        prop("@m_table1", "table_long", "dark", 0.0, 0.8, name="Long reading table", radius=1.6,
             look="Green baize, brass lamps, and a notice: 'Readers are respectfully requested not to lean on the books.'", talk="@reading"),
        prop("@m_table2", "table_long", "dark", 0.0, 4.0, name="Second table", radius=1.6, look="A sleeping gentleman is using the Peerage as a pillow."),
        prop("@m_map", "rug", "cream", 4.8, -3.0, rot=-90, y=1.6, scale=0.5, name="Map of Austro-Hungary", radius=0.4,
             look="Pinned flat on the wall: Buda-Pesth, the Danube, the Carpathians. The Borgo Pass is a pencilled tick. A reader has written beside Transylvania: 'whirlpool of races'."),
        prop("@m_globe", "bust", "plaster", 4.6, -0.4, scale=0.7, name="Marble bust", radius=0.4, look="A bust of a long-forgotten trustee with a nose broken in 1851."),
        prop("@m_lamp1", "lantern", "default", -2.6, 2.4, y=0.8, name=None, radius=0.2),
        prop("@m_lamp2", "lantern", "default", 2.6, 2.4, y=0.8, name=None, radius=0.2),
        prop("@m_chair1", "chair", "red", -2.0, 1.6, rot=180, name=None, radius=0.3),
        prop("@m_chair2", "chair", "red", 2.0, 1.6, rot=180, name=None, radius=0.3),
        prop("@m_pillar", "column", "stone_tomb", -5.2, 1.0, name=None, radius=0.5),
        prop("@m_pillar2", "column", "stone_tomb", 5.2, 1.0, name=None, radius=0.5),
        prop("@m_ink", "bottle", "amber", 1.0, 0.8, y=0.8, name="Reader's inkwell", radius=0.2,
             look="An inkwell chained to the table by order of the Trustees. Even ink cannot be trusted in London."),
    ],
    npcs=[
        npc("@librarian", "human_peasant_m", "@librarian", -2.0, -2.0, rot=180, name="The Superintendent of the Reading Room",
            look="A grave, spectacled man at the high desk, who has never raised his voice and never needed to.", talk="@librarian"),
        npc("@scholar", "human_seward", "doctor", 3.2, 2.0, rot=-90, name="An elderly reader",
            look="Bald, white-bearded, buried in a folio of Hungarian wills. He has the look of a man who has read the whole of Europe and found it wanting.", talk="@scholar"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="@j_museum_arrive")])],
)

# ===================================================== THE CASTLE =============================================================
LOC_DATA["@wall"] = dict(
    cells=[3, 3], wall="stone_dark", floor="stone_dark", interior=False,
    ambient=AMBIENT["night_exterior"], camera=cam([3, 3]), lights=lights_moon(), moon=dict(pos=[-6, 9, -8]),
    walls=dict(north=["wall_4", "wall_window_4", "wall_4"]),
    scatter=dict(asset="pine", variant="dark", count=14, seed=44, avoid=[[-7, -7, 7, 6]]),
    spawn=[0, 3.2], spawns={},
    props=[
        prop("@w_sill", "chest", "ebony", 0.0, -3.4, scale=0.5, name="Jonathan's window-sill", radius=0.8,
             look="My own window, barred inside by a Count's courtesy. Beneath it, a ledge a foot wide and a drop that does not bear looking at.",
             talk="@wall_think"),
        prop("@w_ivy", "pine_small", "dark", -4.4, -3.0, scale=0.45, name="Ancient ivy", radius=0.5,
             look="A rope of ivy thick as my wrist, rooted in the stone. It runs down and to the left. The leaves are torn, as if something heavy had gone down it recently."),
        prop("@w_ring", "lantern", "default", -1.6, -3.2, y=1.3, name="Iron ring", radius=0.3,
             look="A rusted iron ring in the wall, once for a banner-pole. The rust on it is rubbed bright on the lower curve, where a hand has taken weight."),
        prop("@w_stone", "rock", "dark", 2.8, -3.0, scale=0.7, name="Loose coping-stone", radius=0.5,
             look="A stone block that has shifted a finger's breadth. Beside it the lime is pale and scraped, as if a boot-heel had caught it."),
        prop("@w_bats", "bat", "black", 4.4, -2.6, y=1.8, scale=0.8, name="Roosting bats", radius=0.5,
             look="A dozen bats under the eave. They are all facing the same window: the one on the east corner."),
        prop("@w_window", "arch", "stone_dark", 4.8, -3.0, scale=0.6, name="The Count's window", radius=0.7,
             look="Open to the night. The shutters hang back as though somebody has just gone through, and from within comes the smell of old earth.",
             go="@count_room", go_cond="@climbed", go_fail="It is twenty feet along the face, and I cannot simply walk across a sheer wall. I must find the Count's own way down and across, step by step."),
        prop("@w_window2", "arch", "stone_dark", -5.6, -3.0, scale=0.6, name="A shuttered window", radius=0.6,
             look="Shut tight; dust on the sill, no scrape, no bat-dropping. Nobody has used this one for a century."),
        prop("@w_crag", "rock_big", "dark", 0.0, 4.4, name=None, radius=1.0),
        prop("@w_moonlit", "moon", "default", -5.0, -6.2, y=7.0, name=None, radius=0.1),
    ],
    npcs=[],
    on_enter=[dict(once=True, do=[dict(journal="@j_wall")])],
)

LOC_DATA["@count_room"] = dict(
    cells=[3, 2], wall="stone_dark", floor="planks", interior=True,
    ambient=AMBIENT["candle_interior"], camera=cam([3, 2]), lights=lights_warm([3, 2], energy=2.0),
    walls=dict(north=["wall_4", "wall_window_4", "wall_4"], west=["wall_door_4", "wall_4"], east=["wall_4", "wall_4"]),
    spawn=[0, -1.8], spawns={"@wall": [0, -1.8], "@vault": [-4.6, -2.0]},
    props=[
        prop("@r_window", "arch", "stone_dark", 0.0, -3.4, scale=0.5, name="The open window", radius=0.6,
             look="The way I came in. The wall below is a thousand feet of moonlit drop.", go="@wall"),
        prop("@r_gold", "chest", "dark", 3.4, 1.8, rot=-90, name="Heap of gold", radius=0.9,
             look="A great heap of gold of every kind: Roman, British, Austrian, Hungarian, Greek and Turkish, covered with a film of dust as if it had lain long in the ground. None of it less than three hundred years old.",
             take="@gold", take_text="I fill one pocket with a handful of old coin. The Count has too much to miss it, and I may need to buy a way out.", give_once=True),
        prop("@r_goblet", "goblet", "default", -1.6, -1.6, y=0.8, name="Golden cup", radius=0.2,
             look="A cup set with jewels, and so old that its enamel has worn to the shape of a thumb."),
        prop("@r_table", "table", "ebony", -1.6, -1.6, name="Inlaid table", radius=0.9,
             look="Laid for a meal that was never eaten. Gold plate, a decanter, and no sign of a servant's hand."),
        prop("@r_bed", "bed", "red", -3.4, -3.2, name="Great bed", radius=1.2,
             look="Hung with faded velvet. The sheets have not been slept in. I think no one sleeps here."),
        prop("@r_nail", "sconce", "default", 0.2, -3.7, y=1.5, name="Bare nail", radius=0.2,
             look="A nail in the wall, high and plain, with a paler square of plaster below it. A mirror hung here once. There is none in the castle."),
        prop("@r_shelf", "bookshelf", "ebony", -4.4, 1.6, rot=90, name="Wardrobe and shelves", radius=0.8,
             look="A long wardrobe of black oak, and in the shelves, ledgers in an old Latin hand. The last entry is dated the day I arrived."),
        prop("@r_poker", "hammer", "default", 1.6, 3.0, name="Hearth poker", radius=0.3,
             look="A heavy iron poker by a hearth that has not seen a fire in my time.",
             take="@poker", take_text="I take the poker. It is heavy, and I feel better for it.", give_once=True),
        prop("@r_keys", "key", "gold", -3.0, 1.0, name="Bunch of keys", radius=0.3,
             look="A ring of keys hanging from a hook, each a different age and size."),
        prop("@r_door", "door", "ebony", -5.8, -2.0, rot=90, name="Door to the stair", radius=0.6,
             look="The door that gives, in the Count's own tower, onto the winding stair and the old chapel below.",
             go="@vault", go_cond="has:@vault_key", go_fail="Locked. The lock is as old as the door and the door is as old as the castle."),
        prop("@r_rug", "rug", "red", 0.4, 0.6, name=None, radius=0.1),
        prop("@r_lamp", "candelabra", "default", 1.0, -0.4, y=0.0, name=None, radius=0.3),
    ],
    npcs=[],
    on_enter=[dict(once=True, do=[dict(journal="@j_gold")])],
)

LOC_DATA["@vault"] = dict(
    cells=[3, 2], wall="stone_tomb", floor="stone_dark", interior=True,
    ambient=AMBIENT["crypt"], camera=cam([3, 2]), lights=lights_warm([3, 2], energy=1.6),
    walls=dict(north=["wall_4", "wall_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[4.0, -1.0], spawns={"@count_room": [4.0, -1.0], "@path": [4.4, 2.0]},
    props=[
        prop("@v_up", "stairs", "stone_dark", 5.0, -2.0, rot=-90, name="Winding stair", radius=0.8,
             look="Back up to the Count's room.", go="@count_room"),
        prop("@v_door", "door_big", "ebony", 5.8, 2.0, rot=-90, name="Postern door", radius=0.7,
             look="A great iron-bound door barred on the inside by a beam, the way the earth-boxes come and go.",
             go="@path", go_cond="@bar_lifted", go_fail="Barred. The beam is wedged into its sockets and will not lift by hand alone."),
        prop("@v_bar", "bench", "dark", 5.2, 0.4, rot=-90, name="Oak beam", radius=0.8,
             look="The bar of the postern: a trunk of oak, shot into iron staples. It will lift if levered.",
             use_item={"@poker": [dict(say="I wedge the poker under the beam and heave. With a groan it comes out of its staples, and I lean it against the wall."), dict(set="@bar_lifted")],
                       "@vault_key": [dict(say="The key opens the hidden lock in the staple, and the beam slides free."), dict(set="@bar_lifted")]},
             use_fail="I have nothing to lever or unlock the beam with."),
        prop("@v_box", "coffin", "dark", -0.6, -0.8, name="Earth-box", radius=1.1,
             look="The largest box, its lid thrown back. Within lies the Count, with open eyes like stones, red lips, and a cheek that has no breath in it.", talk="@box"),
        prop("@v_box2", "coffin", "oak", -3.2, 0.2, rot=90, name="Another earth-box", radius=1.0, look="Earth, fresh from the hills. The smell is unmistakable."),
        prop("@v_box3", "coffin", "oak", -3.4, 2.4, rot=100, name="A third box", radius=1.0, look="Earth heaped to the brim. They are all for England."),
        prop("@v_candle", "candle", "red", -0.6, -2.6, y=0.0, name="Tall candle", radius=0.3, look="A single tall candle burning at the Count's head, no taller than a thumb, and with no melted wax."),
        prop("@v_altar", "table", "ebony", -3.0, -2.6, name="Broken altar", radius=0.8, look="A stone altar cracked across. The cross above it has been taken down and put face to the wall."),
        prop("@v_tomb", "tomb", "stone_tomb", 1.6, 2.0, name="Old tomb", radius=0.9, look="A knight's tomb with the head broken. The inscription is Slavonic; I can read 'unreconciled' only."),
        prop("@v_skull", "bust", "stone_tomb", 2.4, -2.8, scale=0.4, name="Heap of bones", radius=0.4, look="Old bones, heaped by the wall. Nobody has said a prayer for them."),
        prop("@v_shovel", "hammer", "default", -1.6, 3.0, name="Rusty spade", radius=0.3,
             look="A spade, still stuck in a heap of clay. I could break the Count's skull with it; I have thought of it twice already.",
             take="@spade", take_text="I take up the spade. If the thing in the box wakes, I shall at least have an answer.", give_once=True),
    ],
    npcs=[],
    on_enter=[dict(once=True, do=[dict(journal="@j_vault")])],
)

LOC_DATA["@path"] = dict(
    cells=[4, 3], wall="stone_dark", floor="dirt", interior=False,
    ambient=AMBIENT["night_exterior"], camera=cam([4, 3]), lights=lights_moon(2.6), moon=dict(pos=[6, 9, -8]),
    scatter=dict(asset="pine", variant="dark", count=26, seed=45, avoid=[[-8, -6, 8, 6]]),
    spawn=[-6.0, 2.2], spawns={"@vault": [-6.0, 2.2]},
    props=[
        prop("@p_gap", "stairs", "stone_mossy", 4.6, -0.4, rot=-90, name="Broken footbridge", radius=1.0,
             look="A plank bridge across a deep gully, with the middle plank rotted away. A river roars below.",
             talk="@bridge"),
        prop("@p_wood", "bench", "dark", -3.4, -3.0, name="Woodpile", radius=0.9,
             look="A woodcutter's stack, split and left. There is a stout plank among the logs, long enough to bridge a gap.",
             take="wood", take_text="I drag out a long, stout plank and shoulder it.", give_once=True),
        prop("@p_fire", "lantern", "default", 1.4, 1.4, name="Szgany camp fire", radius=0.5,
             look="A fire of broken pine, and above it a cook-pot. The smell is of onion and goat. A little caravan stands in the dark beyond."),
        prop("@p_wagon", "carriage", "oak", 2.8, -1.8, rot=-30, name="Szgany wagon", radius=1.4,
             look="Painted wheels and a tarpaulin tied with rope. It is clean in a way that tells me they have been here a long time."),
        prop("@p_cross", "grave_cross", "stone_mossy", -4.0, 3.0, name="Wayside cross", radius=0.4,
             look="A crude wooden cross with a rag tied on it. Somebody has left a bunch of dried garlic at its foot."),
        prop("@p_garlic", "garlic", "default", -4.2, 2.6, name="Dried garlic", radius=0.2,
             look="A wayside offering. I take none of it.",
             take="garlic", take_text="I take a head of garlic. The peasants taught me that much, and I was a fool to laugh.", give_once=True),
        prop("@p_boulder", "rock_big", "mossy", 6.4, 3.4, name=None, radius=1.0),
        prop("@p_boulder2", "rock", "dark", -6.0, -2.4, name=None, radius=0.6),
        prop("@p_signpost", "signpost", "dark", 6.2, -3.0, rot=-30, name="Frost-split signpost", radius=0.3,
             look="'Bistritz - 28 hours. Buda-Pesth - 6 days.' Someone has scratched out 'Buda-Pesth' and written, in a bad hand, 'God knows'."),
    ],
    npcs=[
        npc("@szgany_woman", "human_peasant_f", "village_woman", 0.2, 0.6, rot=-30, name="Szgany woman at the fire",
            look="A gaunt woman in a red kerchief, who watches me over the cook-pot with a look neither friendly nor threatening.", talk="@szgany_woman"),
        npc("@herdsman", "human_peasant_m", "villager", -2.0, -0.8, rot=90, name="Slovak herdsman",
            look="An old man in sheepskin, leaning on a crook with a whistle at his lips.", talk="@herdsman"),
        npc("@wolf", "wolf", "grey", 4.0, 3.2, rot=-90, name="Wolves in the dark",
            look="Eyes in the gorse, low and yellow. They have been following me for a hundred yards.", fight="@wolves", radius=0.9),
    ],
    on_enter=[dict(once=True, do=[dict(journal="@j_path")])],
)

# ===================================================== BUDA-PESTH =============================================================
LOC_DATA["@ward"] = dict(
    cells=[3, 2], wall="plaster", floor="planks", interior=True,
    ambient=AMBIENT["warm_day_interior"], camera=cam([3, 2]), lights=lights_warm([3, 2], energy=2.4),
    walls=dict(north=["wall_4", "wall_window_4", "wall_4"], west=["wall_door_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[0, 0.4], spawns={"@garden": [4.6, 2.0], "@chapel": [-4.6, -2.0]},
    props=[
        prop("@d_door_garden", "door", "pale", 5.8, 2.0, rot=-90, name="Door to the garden", radius=0.6,
             look="Open to the lime trees and a little warm air.", go="@garden", go_cond="@woke"),
        prop("@d_door_chapel", "door", "pale", -5.8, -2.0, rot=90, name="Door to the chapel", radius=0.6,
             look="A white door with a small brass crucifix.", go="@chapel", go_cond="@woke"),
        prop("@d_bed", "bed_simple", "blue", 0.0, -2.4, name="My bed", radius=1.0, look="A plain iron-framed bed. The sheets have been changed many times; I do not remember any of them.", talk="@dream"),
        prop("@d_bed2", "bed_simple", "green", -3.6, -3.0, name="Neighbour's bed", radius=1.0, look="A tidy bed. Its occupant has recovered, and left a holy picture on the pillow."),
        prop("@d_bed3", "bed_simple", "green", 3.8, -3.0, name="Another bed", radius=1.0, look="An old Magyar peasant sleeps there, with a rosary wound round his fingers."),
        prop("@d_table", "table", "pale", 1.8, -0.4, name="Medicine table", radius=0.8,
             look="Bottles of bromide, a water-jug, and a fever chart pinned to the wall: forty-two days of it."),
        prop("@d_pen", "bottle", "amber", 1.8, -0.4, y=0.8, name="Doctor's pen", radius=0.2,
             look="A pen and inkwell left on the table after the doctor's rounds.",
             take="@ward_pen", take_text="The doctor said I might borrow his pen to write to my fiancee. I do so.", give_once=True, cond="@woke"),
        prop("@d_effects", "chest", "oak", 3.4, 1.4, scale=0.7, name="Patient's effects", radius=0.5,
             look="A small trunk with my initials, in which the Sisters keep my torn coat, my shirt and my pocket-book.",
             take="@pocket_diary", take_text="In the lining of my coat, the diary. The leather is torn and stained, but every page is there.", give_once=True, cond="@woke"),
        prop("@d_crucifix", "crucifix_big", "silver", -5.2, 0.8, rot=90, name="Crucifix", radius=0.4, look="A large crucifix in silver. I cannot look at it long without weeping."),
        prop("@d_desk", "table", "oak", -2.8, 2.4, name="Sister's writing-desk", radius=0.8,
             look="A little desk where Sister Agatha writes her letters. Paper, a sander, and a half-finished embroidery.",
             talk="@write_mina"),
        prop("@d_paper", "book", "diary", -2.8, 2.4, y=0.8, name="Writing-paper", radius=0.2,
             look="A few sheets of hospital paper with the crest of the Sisters.",
             take="@paper", take_text="Sister Agatha lets me have a sheet of her paper.", give_once=True, cond="@woke"),
        prop("@d_candle", "candle", "white", -1.0, -3.4, y=0.0, name=None, radius=0.3),
        prop("@d_rug", "rug", "cream", 0.0, 1.2, name=None, radius=0.1),
    ],
    npcs=[
        npc("@agatha", "human_peasant_f", "innkeeper_wife", 1.0, -1.0, rot=180, name="Sister Agatha",
            look="A Sister of St. Joseph, small, quick, with gentle grey eyes and a Hungarian-German English all her own.", talk="@agatha"),
        npc("@doctor", "human_seward", "doctor", -3.2, 0.6, rot=90, name="Dr. Hartenstein",
            look="The hospital's physician: a lean man in a frock-coat who makes his rounds like a drill sergeant and has the voice of a country priest.", talk="@doctor"),
        npc("@patient", "human_peasant_m", "villager", 3.4, -1.4, rot=-90, name="Magyar patient",
            look="An old drover with a bandaged leg, who has been here nearly as long as I have and keeps count of the days with matchsticks.", talk="@patient"),
        npc("@mina_ward", "human_mina", "mina", -1.0, 0.8, rot=90, name="Mina", cond="@mina_here",
            look="Mina. She has come, in her travelling dress, white from the long journey, and she is holding my hand.", talk="@mina_ward"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="@j_hospital")])],
)

LOC_DATA["@garden"] = dict(
    cells=[3, 2], wall="stone_grey", floor="grass", interior=False,
    ambient=AMBIENT["day_exterior"], camera=cam([3, 2]), lights=lights_day(2.9),
    scatter=dict(asset="pine_small", variant="green", count=12, seed=51, avoid=[[-6, -4, 6, 4]]),
    spawn=[-4.6, 0.0], spawns={"@ward": [-4.6, 0.0]},
    props=[
        prop("@g_door", "arch", "stone_grey", -5.6, 0.0, rot=90, name="Door to the ward", radius=0.8, look="Back into the cool of the hospital.", go="@ward"),
        prop("@g_lime", "pine_small", "green", 3.6, -1.4, scale=1.3, name="Lime tree", radius=0.6,
             look="Old, wide, humming with bees. The scent of blossom is almost unbearable after the castle."),
        prop("@g_bench", "bench", "oak", -0.6, -1.4, name="Convalescents' bench", radius=0.9, look="A bench with one place worn smoother than the rest."),
        prop("@g_roses", "garlic", "default", 1.6, 1.8, scale=1.6, name="White rose bush", radius=0.4,
             look="A bush of white roses, in flower. Sister Agatha says they will be wanted for a wedding.",
             take="wild_rose", take_text="Sister Agatha has said I may cut one. I choose the whitest and carry it indoors as if it were glass.", give_once=True),
        prop("@g_well", "column_short", "stone_grey", 2.2, -2.8, name="Well", radius=0.6, look="A shallow well with a rope and bucket. The water is sweet and ice-cold."),
        prop("@g_fence", "fence", "default", 5.6, 0.0, rot=90, name=None, radius=0.3),
        prop("@g_stone", "gravestone", "stone_grey", -3.2, 2.0, name="Sisters' memorial", radius=0.5,
             look="A small grey stone with seven names. Under them: 'They served the sick.'"),
        prop("@g_statue", "bust", "stone_tomb", 4.6, 2.0, scale=0.9, name="Statue of St. Joseph", radius=0.4, look="A statue of the Carpenter, with a lily and a moss-grown plane."),
    ],
    npcs=[
        npc("@gardener", "human_peasant_m", "@gardener", 1.0, -0.6, rot=180, name="Old gardener",
            look="A gnarled old man with a watering-can and the placid look of one who has seen every sort of patient go by.", talk="@gardener"),
        npc("@convalescent", "human_peasant_f", "village_woman", -3.0, -1.0, rot=90, name="A young convalescent",
            look="A girl in a shawl, mending slowly from a fever of her own.", talk="@convalescent"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="@j_garden")])],
)

LOC_DATA["@chapel"] = dict(
    cells=[2, 2], wall="plaster", floor="stone_grey", interior=True,
    ambient=AMBIENT["candle_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2], energy=2.6),
    walls=dict(north=["wall_4", "wall_window_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[2.6, -2.0], spawns={"@ward": [2.6, -2.0]},
    props=[
        prop("@h_door", "door", "pale", 3.8, -2.0, rot=-90, name="Door to the ward", radius=0.6, look="Back to the ward.", go="@ward"),
        prop("@h_altar", "table", "pale", 0.0, -3.0, name="Altar", radius=0.9,
             look="A white altar-cloth, brass candlesticks and a vase of white roses.", talk="@altar"),
        prop("@h_crucifix", "crucifix_big", "silver", 0.0, -3.7, y=1.4, name="Crucifix", radius=0.3, look="Above the altar, a crucifix and the legend 'Ecce Agnus Dei'."),
        prop("@h_candles", "candelabra", "default", -1.8, -2.6, name="Votive candles", radius=0.4,
             look="A rack of votive candles in red glass. Dripping wax has run down the rack and frozen in long tears.",
             set="@wax", set_text="I take up a stub and let wax fall on the back of my hand: warm, soft and ready for a seal. I keep a little against the need."),
        prop("@h_virgin", "bust", "plaster", -2.8, -0.4, scale=0.8, name="Shrine of the Virgin", radius=0.5,
             look="A painted shrine, with fresh flowers and rows of tiny tablets. The hospital's patients leave letters here for those who cannot be reached.",
             use_item={"@parents_letter": [dict(say="I fold the letter once more and set it at the Virgin's feet, among the others. Father, Mother: you are never any further than this."),
                                          dict(take="@parents_letter"), dict(set="@parents_left"), dict(journal="@j_parents")]},
             use_fail="I have nothing yet to leave here."),
        prop("@h_pew1", "bench", "oak", 0.0, 0.8, name="Pew", radius=0.9, look="Plain oak, with a kneeler worn by a century of knees."),
        prop("@h_pew2", "bench", "oak", 0.0, 2.2, name=None, radius=0.9),
        prop("@h_font", "barrel", "pale", 2.4, 2.4, scale=0.5, name="Holy-water stoup", radius=0.4, look="A stoup of cold holy water at the door."),
        prop("@h_rug", "rug", "red", 0.0, -0.8, name=None, radius=0.1),
    ],
    npcs=[
        npc("@chaplain", "human_vanhelsing", "vh", 2.0, -1.0, rot=90, name="The English chaplain",
            look="A grey, kind clergyman, in Buda-Pesth these thirty years for the sake of British sailors and the odd stranded traveller.", talk="@chaplain"),
        npc("@mina_chapel", "human_mina", "mina", -0.8, 1.4, rot=0, name="Mina", cond="@wedding_ready",
            look="Mina, in her travelling dress, with white roses in her hand and Jonathan's name already half on her lips.", talk="@wedding"),
        npc("@sister_chapel", "human_peasant_f", "innkeeper_wife", 1.4, 1.8, rot=-90, name="Sister Agatha", cond="@wedding_ready",
            look="Sister Agatha, dressed in her Sunday veil, standing as witness with a look of fierce delight.", talk="@wedding"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="@j_chapel")])],
)

# ====================================================================================================================
# DIALOGUE
# ====================================================================================================================
DIALOGUE = {}

DIALOGUE["@cabman"] = D("n0",
    n0=N("Cabman", "Morning, Mr. Harker. Where to? Your Mr. Hawkins has the cab-rank in his pocket, so I take it you are going somewhere dear.",
         choices=[
             C("To the station - for the London train and the Museum.", "n_london", cond="@got_commission&!@museum_done"),
             C("To the station - and then, God willing, the East.", "n_east", cond="@got_commission&@museum_done&@engaged&@packed"),
             C("Not yet. I have a few things to finish.", "n_wait"),
         ]),
    n_london=N("Cabman", "Paddington by the 9.15, then. The Museum is a step from the Underground. Mind the pickpockets in the Reading Room: they read, too.",
               do=[dict(card="By the morning train to London."), dict(goto="@museum")], end=True),
    n_east=N("Cabman", "The Great Western to town, sir, and the boat-train after that. You are the first man from this street who ever went so far. I'll tell your landlady you looked cheerful.",
             do=[dict(card="THE SOLICITOR'S ROAD\n\nBy rail and river, through Munich and Vienna, to Bistritz and the Borgo Pass...\n\nA month later: the castle."),
                 dict(goto="@wall")], end=True),
    n_wait=N("Cabman", "I am here until four, then the horse insists on his oats.", end=True),
)

DIALOGUE["@flowers"] = D("n0",
    n0=N("Flower-seller", "Violets, sir? Penny a bunch. For Miss Murray, is it? She was by this morning for geraniums and told me you were off to a great foreign place.",
         choices=[
             C("Is it that obvious?", "n1"),
             C("What do the violets mean?", "n2"),
             C("Not today, thank you.", end=True),
         ]),
    n1=N("Flower-seller", "You walk like a man counting his steps to a station, sir. I've seen soldiers go to war with less spring.", next="n0"),
    n2=N("Flower-seller", "Modesty. And faithfulness. A gentleman about to go abroad could do worse than both.", next="n0"),
)

DIALOGUE["@hawkins"] = D("n0",
    n0=N("Mr. Hawkins", "Ah, Jonathan. Come in, come in. You look as though you had not slept. Are the Count's letters still on my desk? I should like you to master them before you go.",
         choices=[
             C("Tell me again about the Count's commission.", "task", cond="!@task"),
             C("I have the surveys, sir. Let me tell you which house will suit the Count.", "pick", cond="@task&has:@surveys&!@chosen"),
             C("The Count wants nothing but Carfax, I think. May I have my instructions?", "instr", cond="@chosen&!@got_commission"),
             C("Do you think I shall like Transylvania, sir?", "think"),
             C("Is there anything else I should know before I go?", "farewell", cond="@got_commission&@museum_done&!@told_farewell"),
             C("Excuse me, sir.", end=True),
         ]),
    task=N("Mr. Hawkins", "A foreign nobleman, Count Dracula, has bought a house in England through us. He wants it large, old and solitary, with a chapel, a high wall, and no neighbours who can overlook him. The surveys are in the deed-box in the muniment room, but Pell has the key, and he will give it up only for good reasons.",
           do=[dict(set="@task"), dict(journal="@j_task")],
           choices=[C("The Count's letters, sir - may I take them?", "letters"), C("I shall see to it.", "n0")]),
    letters=N("Mr. Hawkins", "They are on the desk. Take them. Show them to Pell; he will not move without papers.", next="n0"),
    pick=N("Mr. Hawkins", "I am all attention. Which of the three would you recommend? He is a man of wealth and old habits, and he does not care to be watched.",
           choices=[
               C("The Hampstead villa: handsome, but near a good deal of neighbours.", "wrong_hampstead"),
               C("The house at Whitby: quiet, and by the sea.", "wrong_whitby"),
               C("Carfax at Purfleet: old, walled, with a chapel, a pond and only a madhouse for neighbour.", "right"),
               C("I need a little more time to study them.", "n0"),
           ]),
    wrong_hampstead=N("Mr. Hawkins", "Hampstead? The Count asks for seclusion; the villa has fourteen neighbours, a vicar and a bandstand. Look again at the surveys.", next="pick"),
    wrong_whitby=N("Mr. Hawkins", "Whitby is a fine place, but it has no chapel, and a villa on the cliff is overlooked by half the town. Look again at the surveys.", next="pick"),
    right=N("Mr. Hawkins", "Carfax. Yes. Ancient, enclosed by high stone, with the old chapel and a pond like a well. And the nearest house is Dr. Seward's asylum. A quiet neighbour, as the Count remarks. I think we have our man the house.",
            do=[dict(set="@chosen"), dict(journal="@j_carfax")],
            choices=[C("Then I must go and see him in person, sir.", "instr")]),
    instr=N("Mr. Hawkins", "Quite right. The Count is no common client, and I am too old to travel. You are to go to Castle Dracula, find his house of business, and have the deed signed. Take these - a letter of credit and the particulars - and visit the British Museum before you leave: learn what you can of the country. And, Jonathan - say goodbye to Miss Murray.",
            do=[dict(give="@commission"), dict(set="@got_commission"), dict(journal="@j_instr")], next="n0"),
    think=N("Mr. Hawkins", "A country of beauty and ignorance, I am told. Be careful what you eat, and keep your own counsel. The Count writes in a very good English, but the English of a man who has read much and spoken little.", next="n0"),
    farewell=N("Mr. Hawkins", "Only this, my boy: when you are ready to marry that girl, do it quickly. I am old; I like to see good things done in good time. I shall give you a partnership when you return.",
               do=[dict(set="@told_farewell")], next="n0"),
)

DIALOGUE["@pell"] = D("n0",
    n0=N("Mr. Pell", "Mr. Harker. The muniment room is not a public thoroughfare. May I ask what business takes you there?",
         choices=[
             C("Mr. Hawkins wants the Transylvanian surveys. Here are the Count's letters.", "give", cond="has:@counts_letters&@task&!@got_key"),
             C("Why do you keep the key so close, Mr. Pell?", "why"),
             C("What do you think of the Count's letters?", "opinion"),
             C("Never mind.", end=True),
         ]),
    give=N("Mr. Pell", "Letters. Hmm. A good hand, a foreign seal, and a request in four pages. Yes, I see you are expected. Here. Lock up after you, and put the box key back where you found it; I hide it in the room itself.",
           do=[dict(give="@archive_key"), dict(set="@got_key")], next="n0"),
    why=N("Mr. Pell", "In thirty-one years, Mr. Harker, nothing has been lost from that room. That is not luck; that is a chain.", next="n0"),
    opinion=N("Mr. Pell", "A well-bred hand, and a seal with a wolf on it. I dislike a seal with a wolf on it. I have no reason. The ink is very black, and the paper very cold.", next="n0"),
)

DIALOGUE["@copybook"] = D("n0",
    n0=N("Copy-book", "Nine letters of the firm's side of the correspondence, in Mr. Hawkins's own pressed copy. Which would you like?",
         choices=[
             C("The first: the Count's enquiry.", "l1"),
             C("The seventh: Carfax.", "l2"),
             C("The ninth: the Count's summons.", "l3"),
             C("Close the book.", end=True),
         ]),
    l1=N("Letter 1", "'My dear Sir: I am a foreigner who desires a house in England, near London, of ancient build, with ample grounds and a chapel. My friend Mr. Hawkins is recommended to me as a gentleman of probity. I am, Sir, yours truly, Dracula.'", next="n0"),
    l2=N("Letter 7", "'The house must be large, secluded, well walled, old, and not overlooked. I care little for the comforts of modern life, but a pond or well, and a chapel are required. I am not young, and I have habits.'",
         do=[dict(journal="@j_letters")], next="n0"),
    l3=N("Letter 9", "'I expect Mr. Harker at the Borgo Pass on the 5th of May. A carriage will await him. I trust he will not mind the journey, which is long; the people are simple, and their superstitions many. Be assured, I shall be a good host.'", next="n0"),
)

DIALOGUE["@mina_school"] = D("n0",
    n0=N("Mina", "Jonathan! You came, and in school hours. The headmistress has gone to the dentist, so we may talk, if we are quick and a little bit improper.",
         choices=[
             C("I am going to Transylvania, Mina. A month, perhaps more.", "go"),
             C("Mina, I have something of my mother's to give you.", "ring", cond="has:@ring&!@engaged"),
             C("Mina, will you wait for me?", "wait", cond="@engaged&!@got_ribbon"),
             C("Shall we practise the shorthand?", "short"),
             C("I should go. I just wished to see you.", end=True),
         ]),
    go=N("Mina", "I knew it, Jonathan. Mr. Hawkins told the whole parish. You will write to me. You will write to me every day, even if you cannot post it. Promise.",
         choices=[C("I promise.", "n0", do=[dict(set="@promised")]), C("I shall try, Mina.", "n0")]),
    ring=N("Mina", "A ring? It was your mother's? Oh, Jonathan. Put it on, then - quickly, before I lose my nerve. No: keep it safe, Jonathan, for the day itself. I shall wear it on my finger then, and no sooner.",
           do=[dict(set="@engaged"), dict(journal="@j_engaged")],
           choices=[C("There. I feel taller already.", "n0")]),
    wait=N("Mina", "Wait? I should wait for a Pasha's decision, Jonathan, but for you I'll do it gladly. Take this. It is the ribbon from my hair; tie your diary with it, and write to me in shorthand, and I shall learn to read it faster than a clerk.",
           do=[dict(give="@mina_ribbon"), dict(set="@got_ribbon"), dict(journal="@j_ribbon")], next="n0"),
    short=N("Mina", "Look at the board. I wrote you a line in Pitman's: 'Come back safe.' It is quite the shortest sentence in the world, and the hardest to keep.",
            next="n0"),
)

DIALOGUE["@pupil"] = D("n0",
    n0=N("Small pupil", "Are you Miss Murray's gentleman? She cries when she looks at the map. She says it is the chalk dust.",
         choices=[C("Does she, indeed?", "n1"), C("Run along, child.", end=True)]),
    n1=N("Small pupil", "And she draws your name in the margin and rubs it out. I can read it, though. It begins with a J. Is it Jonah?", end=True),
)

DIALOGUE["@dunmore"] = D("n0",
    n0=N("Mrs. Dunmore", "Mr. Harker! The trunk has stood there since the day you came, and I shall be glad to see something done with it. A man should not live with a locked box in his bedroom. It is not healthy.",
         choices=[
             C("Do you know where the combination might be?", "combo", cond="!@trunk_open"),
             C("I shall pack tonight.", "pack", cond="@trunk_open&!@packed&has:@diary&has:@museum_notes&has:@commission"),
             C("What shall I do about the dreams, Mrs. Dunmore?", "dream"),
             C("Thank you, Mrs. Dunmore.", end=True),
         ]),
    combo=N("Mrs. Dunmore", "Combination? Your father had it from the Admiralty, I was told, and he used it for the year he stopped sailing. A man puts the saddest year of his life in a lock like that. Ask the verger at St. Petroc's; he buried him.",
            do=[dict(set="@combo_hint")], next="n0"),
    pack=N("Mrs. Dunmore", "Then pack with what's in the trunk and what's on the table: your diary, the Count's papers and the notes from the Museum. I'll have the cab ready for the morning.", do=[dict(set="@packed"), dict(journal="@j_packed")], next="n0"),
    dream=N("Mrs. Dunmore", "Dreams? I never remember mine. I find it saves a deal of explaining at breakfast.", next="n0"),
)

DIALOGUE["@trunk"] = D("n0",
    n0=N("Father's trunk", "A brass-bound trunk with a four-wheel lock. The wheels read 18-- . You must set the last two digits. What year did your father die?",
         choices=[
             C("1869.", "bad", cond="!@trunk_open"),
             C("1874.", "good", cond="!@trunk_open"),
             C("1878.", "bad", cond="!@trunk_open"),
             C("I do not remember. I shall find out.", end=True),
             C("(The trunk is open.) Look inside again.", "again", cond="@trunk_open"),
         ]),
    bad=N("Father's trunk", "The wheels click, but the lock does not yield. It is not the right year. Somewhere there is a stone with the date on it.", next="n0"),
    good=N("Father's trunk", "The wheels fall into place, and the hasp springs free. Inside: my mother's ring in a twist of tissue, my father's last letter to me, and a small crucifix. The smell of camphor and thirty years.",
           do=[dict(give="@ring"), dict(give="@trunk_letter"), dict(give="crucifix"), dict(set="@trunk_open"), dict(journal="@j_trunk")], next="n0"),
    again=N("Father's trunk", "The trunk is empty but for tissue and lavender. My mother's ring and my father's letter are in my pocket now.", end=True),
)

DIALOGUE["@dream0"] = D("n0",
    n0=N("Jonathan", "I lie down for an hour. In the half-sleep I see a long road winding up into mountains, and a lit window high on a rock. Somebody is standing in it, waiting. I do not know why that should make me afraid.",
         choices=[C("(Get up.)", end=True, do=[dict(set="@dream0")])]),
)

DIALOGUE["@verger"] = D("n0",
    n0=N("Verger", "Harker, is it? I knew your father. A decent, tired man, and the fever took him in a week.",
         choices=[
             C("What year did he die, Mr. Pascoe?", "year", cond="@combo_hint"),
             C("Who tends the graves?", "who"),
             C("Thank you.", end=True),
         ]),
    year=N("Verger", "Read it from the stone, young sir; I'm not a clerk. It's the Harker stone by the yew. But I'll tell you this: it was the winter of the great frost, and the Exe froze to the bridge.", next="n0"),
    who=N("Verger", "I do. And the one who leaves the snowdrops, I won't say, though I know. She has nice handwriting.", next="n0"),
)

DIALOGUE["@reading"] = D("n0",
    n0=N("Reading-table", "A heap of folios and one reader's lamp. What do you look up?",
         choices=[
             C("Consult Bradshaw's Guide.", "bradshaw"),
             C("Leave the table.", end=True),
         ]),
    bradshaw=N("Bradshaw", "Bradshaw's Continental Guide: Munich to Vienna, thence to Klausenburg and Bistritz. There is a ten-hour delay at Klausenburg. 'Passengers are advised to take their own provisions.' I mark the page.", next="n0"),
)

DIALOGUE["@librarian"] = D("n0",
    n0=N("Superintendent", "Slip, pen, and a press-mark? We do not retrieve books by hope, sir.",
         choices=[
             C("Press-mark K.7: Geography and Ethnology of the Carpathians.", "good", cond="has:@call_slip&has:@pen&!@got_notes"),
             C("Press-mark H.2.", "bad", cond="has:@call_slip&has:@pen&!@got_notes"),
             C("Press-mark Z.19.", "bad", cond="has:@call_slip&has:@pen&!@got_notes"),
             C("I have no slip.", "noslip", cond="!has:@call_slip"),
             C("Never mind.", end=True),
         ]),
    bad=N("Superintendent", "That press-mark belongs to a treatise on cattle-breeding, sir. I recommend you consult the catalogue: the entry on Transylvania has a red ticket.", next="n0"),
    noslip=N("Superintendent", "The tray of slips is by the catalogue. We are a library, sir, not a mind-reader.", end=True),
    good=N("Superintendent", "K.7. Yes. A rare work, and a good one. I shall have it brought. You will find a table prepared.",
           do=[dict(give="@museum_notes"), dict(set="@got_notes"), dict(set="@museum_done"), dict(journal="@j_museum")],
           next="end"),
    end=N("Jonathan", "I read for three hours. The country lies in the horseshoe of the Carpathians; it is a whirlpool of races, Saxon, Wallach, Magyar and Szekely; and the Szgany, who are its gypsies. The people believe in the Evil Eye. I copy what I can. I note a mention of the Borgo Pass, and a name, Dracula, which means 'son of the dragon' and 'devil'.", end=True),
)

DIALOGUE["@scholar"] = D("n0",
    n0=N("Elderly reader", "You are reading the Carpathians, sir. Go no farther than the facts. The superstitions of that country are so numerous that every bridge has a ghost and every ghost a recipe.",
         choices=[
             C("What superstitions?", "n1"),
             C("Do you know the Dracula family?", "n2"),
             C("I'll leave you to your Hungarian wills.", end=True),
         ]),
    n1=N("Elderly reader", "The Evil Eye, for one. At midnight on St. George's Eve every evil thing in the land is abroad. The peasants hang garlic over their doors, and leave wild roses at the cross.", next="n0"),
    n2=N("Elderly reader", "A voivode's line. One of them held the Danube against the Turk, and was either a hero or a devil according to which shore you lived on. The name means 'dragon'. I should not ask about it in the village.", next="n0"),
)

DIALOGUE["@wall_think"] = D("n0",
    n0=N("Jonathan", "I lean from the sill and look down. A drop of three hundred feet, and a ledge. The Count went down this wall like a lizard, head first, with his cloak spread out. If I am to follow, I must know the way. What can I use?",
         choices=[
             C("Try the handholds, starting with the ivy.", "s1_ivy", cond="!@climbed"),
             C("Try the handholds, starting with the iron ring.", "s1_ring", cond="!@climbed"),
             C("Try the handholds, starting with the loose stone.", "s1_stone", cond="!@climbed"),
             C("(Climbed.) Continue to the window.", "done", cond="@climbed"),
             C("Wait. I must study the wall.", end=True),
         ]),
    s1_ivy=N("Jonathan", "I catch the ivy and lower my weight. It holds, and I let myself down a foot at a time to the first anchor. Now: the iron ring, or the stone?",
             choices=[C("The iron ring.", "s2_ring_after_ivy"), C("The loose stone.", "fall")]),
    s1_ring=N("Jonathan", "I try the ring first. My hand slips; the rust is smooth and I cannot reach the ivy. My fingers fail, and I scramble back to the sill, shaking.", next="n0"),
    s1_stone=N("Jonathan", "I put my foot on the stone. It shifts, and a block falls into the dark, a long time before it strikes. I scramble back with my heart in my mouth.", next="n0"),
    s2_ring_after_ivy=N("Jonathan", "The ring takes my weight. It is bright where a hand has used it. Now I can reach the stone with my toe.",
                        choices=[C("The loose stone.", "s3_good"), C("Back to the ivy.", "fall")]),
    s3_good=N("Jonathan", "The stone, which is loose only on the outside, takes my foot as it must. From there, the eastern corner is within reach. I cross the face on my belly, a foot at a time, and drop through the open window into the Count's room.",
              do=[dict(set="@climbed"), dict(journal="@j_climb")], end=True),
    fall=N("Jonathan", "I put a hand wrong and lose my grip. For a moment I hang by one arm over the abyss before I scramble back to the sill. I will try again, in a better order: ivy first, then iron, then stone.", next="n0"),
    done=N("Jonathan", "The window is waiting. I drop through into the room.", do=[dict(goto="@count_room")], end=True),
)

DIALOGUE["@box"] = D("n0",
    n0=N("Jonathan", "The Count lies in the box, looking younger than I have ever seen him. His eyes are open and stony; there is a bloated look about him; his lips are red as if with blood. A key should be on him, but I do not find one.",
         choices=[
             C("Search his pockets for the key.", "search", cond="!@searched"),
             C("Strike him with the spade.", "strike", cond="has:@spade"),
             C("Back away.", end=True),
         ]),
    search=N("Jonathan", "I search him as one searches a dead man. No key. No watch, no purse; a few gold coins loose in a pocket, and nothing else. He does not move. I cannot bring myself to look at his face again.",
             do=[dict(set="@searched"), dict(journal="@j_search")], next="n0"),
    strike=N("Jonathan", "I raise the spade, and his eyes turn toward me. The face is a mask of hate. I cannot do it. The spade slips from my hand and strikes the box, and I run.", do=[dict(set="@struck")], end=True),
)

DIALOGUE["@bridge"] = D("n0",
    n0=N("Footbridge", "The middle plank is gone, and the gully below is a black throat of water. A single plank, if you had one, might bridge it.",
         choices=[
             C("Lay the plank across and cross.", "cross", cond="has:wood"),
             C("Go back and look for something.", end=True),
         ]),
    cross=N("Jonathan", "I lay the plank across and take it step by step with the roar of the water below. On the far side a track runs down toward a valley that is, God willing, the road to civilisation. My legs give way beneath me; I rest against a boulder and the dark comes down.",
            do=[dict(take="wood"), dict(set="@crossed"), dict(journal="@j_cross"),
                dict(card="Who can say how long, or by what road?\n\nThe next that Jonathan Harker knows is the smell of linen and the sound of a woman's voice, praying in German."), dict(goto="@ward")], end=True),
)

DIALOGUE["@szgany_woman"] = D("n0",
    n0=N("Szgany woman", "Ah, the English gentleman, who walks on the mountain at night and is white as milk. Sit. Eat. The Count's people do not eat with us, but you are not one of his.",
         choices=[
             C("Can you sell me food?", "food", cond="has:@gold&!@got_food"),
             C("May I ask about the Count?", "count"),
             C("Will you help me?", "help"),
             C("I'll go on.", end=True),
         ]),
    food=N("Szgany woman", "Gold of the old kings! That has not been seen in these hills for three hundred years. Take the bread and the goat-cheese, and a flask. I'll not ask where you found it, for I do not wish to know.",
           do=[dict(take="@gold"), dict(give="brandy"), dict(set="@got_food"), dict(journal="@j_szgany")], next="n0"),
    count=N("Szgany woman", "We carry his boxes. We take his coin. We do not ask what is in them, nor why they are filled with earth. Our grandfathers bowed to his grandfathers, and we have kept the habit.", next="n0"),
    help=N("Szgany woman", "I cannot take you down the mountain; the men will say I betrayed the master. But the herdsman by the woodpile may take you to the footbridge. He is not afraid of the old man.", next="n0"),
)

DIALOGUE["@herdsman"] = D("n0",
    n0=N("Slovak herdsman", "Dobry vecer, pan. You have the look of a man who has seen something in the castle. Hush! I do not need to hear what.",
         choices=[
             C("Which way to the valley?", "way"),
             C("Is there a way over the gully?", "bridge"),
             C("Thank you, old man.", end=True),
         ]),
    way=N("Slovak herdsman", "Down the path, left at the cross, and over the gully by the old bridge. The plank is gone, but there is wood by the pile. You'll find a plank long enough.", next="n0"),
    bridge=N("Slovak herdsman", "Plank, rope, courage. Courage you have, or you wouldn't be here. Plank is at the woodpile.", next="n0"),
)

DIALOGUE["@agatha"] = D("n0",
    n0=N("Sister Agatha", "Sh, sh. Do not try to rise. You have been very ill, mein Herr, a brain fever, and you spoke much in your sleep, in English, of wolves and women and a wall. I was afraid.",
         choices=[
             C("Where am I?", "where", cond="!@woke"),
             C("What day is it? What month?", "when", cond="!@woke"),
             C("My name is Jonathan Harker. I am an English solicitor.", "name", cond="!@woke"),
             C("Sister, I must write to a lady in England.", "letter", cond="@woke&has:@ward_pen&has:@paper&!@letter_sent"),
             C("Sister, may I have my pocket-book and diary?", "diary", cond="@woke&!has:@pocket_diary&!@sealed"),
             C("Sister, I want to seal my diary. I do not want to know what is in it.", "seal", cond="has:@pocket_diary&has:@mina_ribbon&@wax&!@sealed"),
             C("Thank you, Sister.", end=True),
         ]),
    where=N("Sister Agatha", "In the Hospital of St. Joseph and Ste. Mary, in Buda-Pesth. A herd-boy found you on the road to Bistritz, weeks ago, and the doctors say you came by wagon and cart and charity. You are among friends.", next="n0"),
    when=N("Sister Agatha", "It is the second week of September, mein Herr. You were brought in at the end of August. We counted every day.", next="n0"),
    name=N("Sister Agatha", "Harker. Yes, the name was in your pocket-book, but you spoke it in your sleep, so I knew it was true. Rest. The doctor will see you at noon.",
           do=[dict(set="@woke"), dict(journal="@j_woke")], next="n0"),
    letter=N("Sister Agatha", "I will tell you what to write: the date, the place, that you are alive, and nothing more. Your friend must hear you are safe before she hears anything else. Use the writing-desk, mein Herr.", end=True),
    diary=N("Sister Agatha", "Your coat is torn. Your diary is in the lining. I have not read it; it is in shorthand, and I'm only a Sister. Take it from the patient's chest.", next="n0"),
    seal=N("Sister Agatha", "You give it to me to seal? No - to your friend. That is better. I shall pour the wax, if you will say the words. Give me the ribbon and the book.",
           choices=[
               C("I'll do it myself, Sister.", "sealed_ok"),
               C("Do it for me. I cannot bear to touch it.", "sealed_ok"),
           ]),
    sealed_ok=N("Sister Agatha", "There. The ribbon is Miss Murray's, I think? Red-white. The wax is the chapel's. Now say it, mein Herr: why do you not want to read it?",
                choices=[
                    C("Because I do not know whether it was a dream, or whether I went mad. I will not know unless some solemn duty come upon me.", "vow"),
                ]),
    vow=N("Sister Agatha", "That is the vow, then. Not to read it, and not to doubt it, unless duty. Hold the book. I shall say a prayer.",
          do=[dict(take="@pocket_diary"), dict(take="@mina_ribbon"), dict(give="@sealed_diary"), dict(set="@sealed"), dict(journal="@j_vow")], end=True),
)

DIALOGUE["@doctor"] = D("n0",
    n0=N("Dr. Hartenstein", "Ah, you are awake and sane. Good. I will tell you plainly: it was brain fever of the severest. You will not remember the first three weeks, and I advise you not to try.",
         choices=[
             C("What did I say?", "said"),
             C("May I write to England?", "write", cond="@woke"),
             C("When may I leave?", "leave"),
             C("Thank you, Doctor.", end=True),
         ]),
    said=N("Dr. Hartenstein", "You spoke of a castle in the mountains, of wolves, of women with red lips, and of a man who walks down a wall. I took it for delirium. Sister Agatha did not.", next="n0"),
    write=N("Dr. Hartenstein", "By all means. Here, you may keep my pen. A letter soothes the mind better than any bromide.", do=[dict(set="@doctor_pen")], next="n0"),
    leave=N("Dr. Hartenstein", "When the lady arrives, and we have married you, and not before. I shall not release an unmarried man in your condition.", next="n0"),
)

DIALOGUE["@patient"] = D("n0",
    n0=N("Magyar patient", "You are the Englishman. You shouted in the night. In German, in English, and once in what I think was Latin. Do you remember?",
         choices=[
             C("I remember a castle.", "n1"),
             C("I remember nothing.", "n2"),
             C("Go back to sleep, old man.", end=True),
         ]),
    n1=N("Magyar patient", "There are many castles. Only one of them you should not name. Do not name it. It has ears.", next="n0"),
    n2=N("Magyar patient", "Then you are fortunate. I broke my leg falling from a cart, and I remember every pain.", next="n0"),
)

DIALOGUE["@dream"] = D("n0",
    n0=N("Jonathan", "I lie down on the clean linen and close my eyes. The ward is quiet. At the edge of sleep I hear a soft laughter, like silver bells, and three women are in the moonlight: two dark, with hooked noses like the Count, one fair as the sun with great wavy hair. I feel a wicked, burning desire that they would kiss me with those red lips.",
         choices=[
             C("(Wake. Cross myself.)", "n1", cond="!@dream_done"),
             C("(Sleep on.)", "n2", cond="@letter_sent&!@mina_here"),
             C("(Lie quiet.)", end=True),
         ]),
    n1=N("Jonathan", "I wake with the sheet in my fists, drenched in sweat. A hand cools my forehead: Sister Agatha. 'You said the word again,' she says. 'It was a woman's name. Not a good one.' I hold her hand until the fear passes.",
         do=[dict(set="@dream_done"), dict(journal="@j_dream")], end=True),
    n2=N("Jonathan", "This time the women stand back. One of them turns her head, and for a moment she has Mina's eyes, then no eyes at all. I wake knowing that I shall never again be quite at ease in sleep. A cab-wheel sounds in the courtyard. It is morning, and a woman is on the stairs.",
         do=[dict(set="@mina_here"), dict(card="Three days later."), dict(journal="@j_mina_arrives")], end=True),
)

DIALOGUE["@write_mina"] = D("n0",
    n0=N("Writing-desk", "A sheet of hospital paper and the doctor's pen. What shall I write to Mina?",
         choices=[
             C("'I am safe, in Buda-Pesth, in the care of the Sisters. I am ill, but mending. I love you.'", "ok", cond="@woke&has:@ward_pen&has:@paper&!@letter_sent"),
             C("'I have terrible things to tell you.'", "bad", cond="@woke&has:@ward_pen&has:@paper&!@letter_sent"),
                          C("Step away.", end=True),
         ]),
    ok=N("Jonathan", "I fold the letter, and Sister Agatha writes under mine: 'He is well, but weak, and he asks that you come.' She seals it herself. 'Mr. Hawkins will be told,' she says. 'And your friend will not read a word that frightens her.'",
         do=[dict(take="@paper"), dict(set="@letter_sent"), dict(journal="@j_letter")], end=True),
    bad=N("Jonathan", "I stare at the page, and the pen shakes. I cannot say it; she must not read it. I cross it out, and begin again.", next="n0"),
)

DIALOGUE["@mina_ward"] = D("n0",
    n0=N("Mina", "Jonathan. Oh, Jonathan. Sister Agatha has told me everything; she has also told me nothing that matters. I am here. I am not going away.",
         choices=[
             C("Mina, I have something to ask.", "ask", cond="!@asked_mina"),
             C("Mina, I have my diary. I cannot read it. Will you keep it?", "journal", cond="@sealed&!@gave_journal"),
             C("Mina, a Sister says the chaplain can marry us tomorrow.", "wed", cond="@gave_journal&@parents_left&@got_ribbon&!@wedding_ready"),
             C("Rest, my dear.", end=True),
         ]),
    ask=N("Mina", "Ask, then. I have come across the sea, and I have six hours of train in my bones.",
          choices=[C("Will you marry me, here, as soon as you are rested?", "yes")]),
    yes=N("Mina", "I will marry you tomorrow. Today if the chaplain could be found. But one condition: that you let me take care of you. And that you tell me, one day, what it was that frightened you.",
          do=[dict(set="@asked_mina"), dict(journal="@j_proposal")], next="n0"),
    journal=N("Mina", "A sealed book? You wish me to keep it, unread, and to give it back only if some solemn duty comes upon us? I will, Jonathan. I do not need to know what is in it. I know what is in you.",
              do=[dict(take="@sealed_diary"), dict(set="@gave_journal"), dict(journal="@j_gave")], next="n0"),
    wed=N("Mina", "Then let us be married. I will find Sister Agatha and the white roses.", do=[dict(set="@wedding_ready"), dict(journal="@j_wedding_day"), dict(goto="@chapel")], end=True),
)

DIALOGUE["@gardener"] = D("n0",
    n0=N("Old gardener", "The Herr Englishman. I have seen you in your chair on the third bench every afternoon this week. You look better. The cherry-trees are better than the roses; roses are tricky.",
         choices=[
             C("May I cut a rose for my fiancee?", "rose"),
             C("What flowers do the Sisters prefer?", "flowers"),
             C("Thank you.", end=True),
         ]),
    rose=N("Old gardener", "A white one. White for a wedding, and white for a funeral, but never red; red is for the bold.", next="n0"),
    flowers=N("Old gardener", "Lilies for Our Lady. Roses for St. Joseph, who never asked for any. Sage for the kitchen, rue for the fever.", next="n0"),
)

DIALOGUE["@convalescent"] = D("n0",
    n0=N("Young convalescent", "You are the English one. They say you came with your hair white and your coat in ribbons.",
         choices=[C("White?", "n1"), C("I'd rather not say.", end=True)]),
    n1=N("Young convalescent", "A white streak, Sister Agatha says. She calls it a mark of grace. I think you look like a pirate.", end=True),
)

DIALOGUE["@altar"] = D("n0",
    n0=N("Altar", "The altar is bare but for a vase of white roses and two brass candlesticks. A prayer-book lies open.",
         choices=[
             C("Write a letter to my parents.", "write", cond="has:@trunk_letter&has:@ward_pen&!@parents_written"),
             C("Kneel for a moment.", "kneel"),
             C("Leave.", end=True),
         ]),
    write=N("Jonathan", "I write at the altar-rail: 'Father, Mother: I have been far from home, and nearly did not come back. I found your letter again - you never said that you were proud of me, but I knew. I am to be married. I wish you could see her. I wish you could see me now, and not the boy who ran along the Exe with a kite.' I fold it, and my hand is steadier than it has been in weeks.",
            do=[dict(give="@parents_letter"), dict(take="@trunk_letter"), dict(set="@parents_written")], next="n0"),
    kneel=N("Jonathan", "I kneel. I do not pray in words; I only think of the long road that brought me here, and of the chain of kindly hands: a herdsman, a carter, a Sister. I am not yet quite sane, but I am nearer.", next="n0"),
)

DIALOGUE["@chaplain"] = D("n0",
    n0=N("English chaplain", "You are the young man from Exeter. I have been sent a letter by your Mr. Hawkins, who writes, I may say, a very fine hand.",
         choices=[
             C("Will you marry us, sir?", "yes", cond="@wedding_ready"),
             C("Is it permitted, in a hospital chapel?", "perm"),
             C("I'll come back later.", end=True),
         ]),
    perm=N("English chaplain", "With the Sisters' leave, and the doctor's, and the Bishop's lack of objection, which I have in writing. It is not usual, but it is not forbidden. Come back when the lady is ready.", next="n0"),
    yes=N("English chaplain", "Gladly. Is there a ring? A bride must have a ring.",
          choices=[C("I have my mother's ring, sir.", "ring_ok", cond="has:@ring"), C("I lost it.", "noring")]),
    noring=N("English chaplain", "Then we wait.", end=True),
    ring_ok=N("English chaplain", "Then let us begin.", do=[dict(talk="@wedding")], end=True),
)

DIALOGUE["@wedding"] = D("n0",
    n0=N("English chaplain", "Dearly beloved. We are gathered together in the sight of God, in a little white chapel in a foreign city, to join together this man and this woman. If any man can show just cause...",
         choices=[
             C("(Take Mina's hand and answer.)", "vows", cond="has:@ring&@wedding_ready"),
             C("(Step back.)", end=True),
         ]),
    vows=N("English chaplain", "Jonathan, wilt thou have this woman to thy wedded wife, to live together after God's ordinance?",
           choices=[C("I will.", "mina_vows")]),
    mina_vows=N("Mina", "I will. For better, for worse, and for the unspoken things in the sealed book.", next="ring"),
    ring=N("Jonathan", "I slip my mother's ring on her hand. It fits. Sister Agatha weeps openly into her veil. The chaplain says the final words; the white roses breathe in the candlelight; and the world, which has been a nightmare for so long, is only a room full of people who love us.",
           do=[dict(take="@ring"), dict(set="@wed"), dict(journal="@j_wed")], next="final"),
    final=N("Mina", "Now we are husband and wife, Jonathan. Whatever comes. Whatever you saw, we shall face it together, and perhaps the sealed book can stay sealed for ever. 'Unless some solemn duty come upon us.'",
            choices=[C("[Finish this story]", do=[dict(card="Jonathan Harker and Mina Murray were married in the hospital chapel in Buda-Pesth on the twelfth of September.\n\nTheir journey home was long. Ahead, there was a house at Purfleet; a girl called Lucy; and a sealed book that would be opened at last.\n\nBut that is another story."),
                                                          dict(journal="@j_epilogue"), dict(arc_end=1)])]),
)

# ====================================================================================================================
# ITEMS
# ====================================================================================================================
ITEMS = {
    "@counts_letters": dict(name="The Count's letters", asset="book", variant="red", desc="Nine letters in a small upright hand: a large, old, secluded house, with a chapel and a high wall, no neighbours who can overlook it. The Count would also like a pond or well."),
    "@archive_key": dict(name="Muniment-room key", asset="key", variant="default", desc="Mr. Pell's own key to the firm's basement vault."),
    "@box_key": dict(name="Deed-box key", asset="key", variant="gold", desc="A small japanned key for the black deed-box."),
    "@surveys": dict(name="Three surveys", asset="book", variant="leather", desc="Hampstead: a villa among a dozen others, a bandstand in the road. Whitby: a villa on the cliff, overlooked from the church. Purfleet (Carfax): old, walled, with a chapel, a pond like a well, and the lunatic asylum as sole neighbour."),
    "@commission": dict(name="Letter of credit and particulars", asset="book", variant="diary", desc="Mr. Hawkins's letter of introduction to the Count's agents, with the draft of the deed."),
    "@call_slip": dict(name="Call-slip", asset="book", variant="diary", desc="A green Museum call-slip, blank."),
    "@pen": dict(name="Steel pen and ink", asset="bottle", variant="amber", desc="A pen and a small bottle of ink from Mr. Hawkins's desk."),
    "@museum_notes": dict(name="Museum notes", asset="book", variant="leather", desc="Notes on the Carpathians: Saxon, Wallach, Magyar and Szekely; the Szgany; the Evil Eye; the name Dracula."),
    "@ring": dict(name="Mother's ring", asset="key", variant="gold", desc="A thin gold ring, worn at the back. My mother's. She wore it for nineteen years."),
    "@trunk_letter": dict(name="Father's last letter", asset="book", variant="diary", desc="'Jonathan, if you read this I will have been gone a long while. Be a decent man. Be kind to your mother's memory. Write things down.'"),
    "@mina_ribbon": dict(name="Mina's ribbon", asset="rug", variant="red", desc="A ribbon from Mina's hair, red, slightly crumpled, still smelling of her soap."),
    "@diary": dict(name="Travelling diary", asset="book", variant="diary", desc="A small black diary bound for the journey; the shorthand pages are still blank."),
    "@gold": dict(name="Handful of old gold", asset="goblet", variant="default", desc="Old coin of five reigns, from the Count's heap."),
    "@vault_key": dict(name="The Count's key", asset="key", variant="default", desc="A heavy iron key on a ring, worn at the bow."),
    "@poker": dict(name="Hearth poker", asset="hammer", variant="default", desc="A heavy iron poker."),
    "@spade": dict(name="Rusty spade", asset="hammer", variant="default", desc="A gravedigger's spade, with a splintered haft."),
    "@wolf_tooth": dict(name="Wolf's tooth", asset="bottle", variant="glass", desc="A yellowed tooth, picked from the ground where the wolves fell back."),
    "@ward_pen": dict(name="Doctor's pen", asset="bottle", variant="amber", desc="A pen lent by the hospital physician."),
    "@paper": dict(name="Hospital paper", asset="book", variant="diary", desc="A sheet of the Sisters' writing-paper, thin and cream."),
    "@pocket_diary": dict(name="My diary (torn)", asset="book", variant="diary", desc="My journal, salvaged from the lining of my coat. I do not wish to read it."),
    "@sealed_diary": dict(name="Sealed diary", asset="book", variant="red", desc="The torn diary, tied with Mina's ribbon and sealed with the chapel's wax."),
    "@parents_letter": dict(name="Letter to my parents", asset="book", variant="diary", desc="A single sheet, folded small, addressed 'To my Father and Mother'."),
    "@sealed_journal": dict(name="Jonathan's sealed journal", asset="book", variant="red", desc="A torn black diary bound with a red ribbon and sealed in wax: the account of his captivity, which he vowed never to open 'unless some solemn duty come upon me'."),
}

# ====================================================================================================================
# JOURNAL (<= 70 words each)
# ====================================================================================================================
JOURNAL = {
    "@j_morning": dict(title="A May morning in Exeter", source=M, text="Exeter, May. Cathedral bells, a fine sun, and Mr. Hawkins's letter in my pocket. I am to go to Transylvania, a country I know only as a smudge on the school globe. The firm trusts me; I wish I trusted myself as much."),
    "@j_commission": dict(title="Mr. Hawkins's office", source=M, text="Mr. Hawkins has taken a foreign client, a Count Dracula of Castle Dracula, for the purchase of an English house. His letters are formal and exact. I am to prepare the file and, if all goes well, go to him in person. I am rather proud."),
    "@j_task": dict(title="The Count's wishes", source=M, text="The Count wants a house in England: large, old, solitary, with a chapel and a high wall, and no neighbour near enough to overlook him. The surveys are in the muniment room; Mr. Pell has the key, and Mr. Pell is not a man to be hurried."),
    "@j_surveys": dict(title="Three surveys", source=M, text="The deed-box held three surveys: a Hampstead villa, a house at Whitby, and a place at Purfleet called Carfax. Only one was old, walled and furnished with a chapel. I begin to see which the Count would choose."),
    "@j_carfax": dict(title="Carfax is chosen", source=M, text="Carfax, then. An old house at Purfleet, walled in stone, with a chapel and a pond, and only a lunatic asylum for a neighbour. Mr. Hawkins agrees. I hope the Count is as pleased with it as we are with ourselves."),
    "@j_letters": dict(title="The Count's letters", source=M, text="I read the Count's letters again. They are admirable: grave, patient, correct. But I notice what he never asks about: price. A man who does not ask the price has too much to lose, or too much to spend."),
    "@j_instr": dict(title="Instructions", source=M, text="Mr. Hawkins gives me a letter of credit and sends me to the British Museum. Then I am to go east, find the Count and have the deed signed. And, he says, say goodbye to Mina. He says it with the air of a man who is not asking."),
    "@j_museum_arrive": dict(title="The Reading Room", source=M, text="London. The great dome of the Reading Room is like the inside of a giant's skull, and the readers sit under it like thoughts. I stand a long time in the door and feel very small, and very provincial."),
    "@j_museum": dict(title="Notes on Transylvania", source=M, text="In the Museum I learn that Transylvania lies within the Carpathians, a whirlpool of Saxon, Wallach, Magyar and Szekely, with the Szgany among them. The people believe in the Evil Eye and in a name, Dracula, which means both dragon and devil."),
    "@j_mina": dict(title="Mina at the school", source=M, text="Mina in her classroom, with chalk on her cuff. She says I am foolish to go so far, and hopes I will write every day. There is a blackboard of shorthand behind her. I shall pretend not to read it."),
    "@j_trunk": dict(title="Father's trunk", source=M, text="The trunk is open at last. Inside, camphor, tissue, my mother's ring, a small crucifix and a letter in my father's hand. I did not know I had missed him so much. I must wear the ring, at least, to Mina."),
    "@j_engaged": dict(title="The ring", source=M, text="I gave Mina my mother's ring this evening, and she put it on a chain round her neck. She says she will wear it openly when I come home. I have never before had so good a reason to come home."),
    "@j_ribbon": dict(title="Mina's ribbon", source=M, text="Mina gave me the ribbon from her hair for my diary. She says I must write in shorthand and she will learn to read it. I tie it round the book and put it next to my heart."),
    "@j_packed": dict(title="Packed", source=M, text="Valise strapped, diary in my breast pocket, the Count's papers and the Museum notes in the lining. Mrs. Dunmore wept a little into her apron, and denied it. I am, I think, as ready as a man can be for a country he has only read about."),
    "@j_lodging": dict(title="Packing", source=M, text="Mrs. Dunmore has laid out my shirts. My father's trunk sits under the window, locked. I will take nothing from it, because I have never opened it, and I wonder whether I should."),
    "@j_churchyard": dict(title="Churchyard", source=M, text="I walked to St. Petroc's to see my parents' stone. The snowdrops were fresh. Somebody tends it; I know who. Mina has never said a word about it."),
    "@j_wall": dict(title="The wall", source=M, text="I am a prisoner in the Count's castle. All doors are locked; the only way is a ledge and a wall. The Count went down the wall like a lizard. If he can, I can. The alternative is waiting for the women."),
    "@j_climb": dict(title="Down the wall", source=M, text="I went down the castle wall by ivy, iron ring and loose stone, and in through the Count's open window. My hands bleed; my coat is torn. I have crossed a threshold I do not understand, and I cannot go back."),
    "@j_gold": dict(title="The Count's gold", source=M, text="In the Count's room, a heap of gold, Roman, Austrian, Turkish, Hungarian, all coated with dust, none newer than three hundred years. There is no mirror in the castle. There is not even a nail left."),
    "@j_vault": dict(title="The vault", source=M, text="Down the stair to the old chapel: fifty great boxes of earth. In one lay the Count, as if asleep, his eyes open, but nothing living in them. It is the most terrible thing I have ever seen, and I am not yet mad."),
    "@j_search": dict(title="No key", source=M, text="I searched the Count's body for the key and found none. A few gold coins in a pocket; no watch, no purse. He does not breathe. He does not wake. I wonder which of us is more afraid."),
    "@j_path": dict(title="The mountain path", source=M, text="Out through the postern in the moonlight, down a goat-path under the stars. The wolves are near; I can smell them. A fire burns below, with a Szgany wagon. I do not know whether I am escaping or falling."),
    "@j_szgany": dict(title="The Szgany fire", source=M, text="A Szgany woman sold me bread and a flask for a handful of the Count's gold, and refused to say more. Her people carry his boxes and ask no questions. I envy them both."),
    "@j_cross": dict(title="Over the gully", source=M, text="I crossed the gully on a plank with the roar of the river under me. On the far side the track runs down. Then my legs gave way, and the dark came, and I do not know what I did next."),
    "@j_hospital": dict(title="Buda-Pesth", source=M, text="I woke in a hospital in Buda-Pesth. Sister Agatha says I have had a brain fever, and have been here six weeks. I have a white streak in my hair, they tell me, and I believe them."),
    "@j_woke": dict(title="Sister Agatha", source=M, text="A small, quick Sister of St. Joseph has sat by my bed, and sent word to Mr. Hawkins. She says I spoke of wolves and a wall and three women. I told her nothing. I do not trust words yet."),
    "@j_dream": dict(title="The dream of the three", source=M, text="Again the dream: three women in the moonlight, laughing like silver bells. One fair, two dark. I wake wet to the skin. Sister Agatha says I called a woman's name, and not a kind one. She does not ask whose."),
    "@j_letter": dict(title="A letter to Mina", source=M, text="Sister Agatha has written for me; I signed. 'I am safe, in Buda-Pesth, ill but mending.' Nothing more. She said the letter must say nothing that would frighten Mina, and I agreed. I hope that I shall always be able to."),
    "@j_vow": dict(title="The vow", source=M, text="I have sealed my diary with Mina's ribbon and the chapel's wax. I do not know whether it is true or the delirium of a sick man. I will not know unless some solemn duty come upon me. So be it."),
    "@j_parents": dict(title="To my father and mother", source=M, text="I left a letter to my parents at the Virgin's feet in the chapel. They never said that they were proud of me. I think I know now why a man writes to the dead: because he can say it, and nobody can say no."),
    "@j_mina_arrives": dict(title="Mina is come", source=M, text="Mina arrived in Buda-Pesth this morning, in a cab, with a carpet-bag and a face like a lamp. She did not ask what had happened. She took my hand, and said, 'I am not going away.'"),
    "@j_proposal": dict(title="The proposal", source=M, text="Mina has said yes. Here, in a hospital ward in Buda-Pesth, to a man half-mad with fever and white at the temples. I do not deserve it, and I have never wanted anything so much."),
    "@j_gave": dict(title="The sealed book", source=M, text="I gave Mina my sealed diary. 'Keep it,' I said, 'and do not read it unless a solemn duty requires.' She tied the ribbon again, as she had before, and kissed my forehead. She is wiser than I am."),
    "@j_chapel": dict(title="The chapel", source=M, text="A small white chapel with roses on the altar, and a vase of candles. The Sisters have decked it for us. The chaplain, they say, has been an Englishman in Buda-Pesth for thirty years."),
    "@j_garden": dict(title="The garden", source=M, text="I sit in the garden under the limes and listen to the bees. I have not been in sunlight for six weeks. The old gardener says I look better. I do not remember when I last looked at all."),
    "@j_wedding_day": dict(title="The wedding day", source=M, text="Tomorrow we shall be married, with a white rose, a borrowed ring and a chaplain who says he has been waiting thirty years to see an Englishman and a girl turn up with matching faces. I am very happy."),
    "@j_epilogue": dict(title="The road home", source=M, text="Mina and I leave Buda-Pesth for England, with the sealed book in her trunk and the white streak in my hair. I have the road behind me. I shall not look at it again, unless some solemn duty come upon me."),
    "@j_wed": dict(title="Husband and wife", source=M, text="We were married in the chapel at Buda-Pesth this morning. Sister Agatha wept. I was happy, truly, for the first time since the Borgo Pass. Whatever the sealed book contains, it is not this."),
}

# ====================================================================================================================
# seed variation
# ====================================================================================================================
PALETTES = {
    "@office": [dict(wall="plaster_dirty", floor="planks", wood="dark", cloth="green"), dict(wall="plaster", floor="planks", wood="oak", cloth="blue")],
    "@school": [dict(wall="plaster", floor="planks", wood="pale", cloth="green"), dict(wall="plaster", floor="planks", wood="oak", cloth="cream")],
    "@lodging": [dict(wall="plaster", floor="planks", wood="pale", cloth="blue"), dict(wall="plaster_dirty", floor="planks", wood="oak", cloth="green")],
    "@ward": [dict(wall="plaster", floor="planks", wood="pale", cloth="blue"), dict(wall="plaster", floor="planks", wood="oak", cloth="cream")],
    "@chapel": [dict(wall="plaster", floor="stone_grey", wood="oak", cloth="red"), dict(wall="plaster", floor="stone_grey", wood="pale", cloth="blue")],
}

PLACEMENTS = {
    "@box_key": [
        dict(prop="@a_stool", text="Under the stool's flat cushion, a small japanned key tied with a pink thread.", hint="The cushion of the stool lies lumpily."),
        dict(prop="@a_barrel", text="In the barrel of old seals, a small japanned key hidden under a lump of green wax.", hint="One of the lumps of wax in the barrel looks fresh."),
        dict(prop="@a_lantern", text="On the hook behind the lantern, a japanned key on a pink thread.", hint="The lantern hangs a little crooked from its hook."),
    ],
    "@vault_key": [
        dict(prop="@r_keys", text="Among the keys on the ring, one heavy iron key with a worn bow, stamped with a tiny cross, the stair-door's own.", hint="One key on the ring hangs apart from the rest, as if used recently."),
        dict(prop="@r_table", text="Under the plate on the inlaid table, a heavy iron key with a worn bow.", hint="One of the gold plates on the table sits crookedly."),
        dict(prop="@r_shelf", text="Behind the Latin ledger, a heavy iron key with a worn bow, on a nail.", hint="The ledgers on the shelf stand a hand's breadth out from the wall."),
    ],
}

GATES = {
    "@r_door": [
        dict(cond="has:@vault_key", fail="Locked. The lock is as old as the door; a heavy key must hang somewhere in this room.", needs="@vault_key"),
        dict(cond="has:@poker", fail="Locked. The bolt is old and rusted; a lever might break the hasp.", needs="@poker"),
    ],
    "@o_door_archive": [
        dict(cond="has:@archive_key", fail="Locked. Mr. Pell keeps the key to the muniment room, and Mr. Pell keeps it like a relic.", needs="@archive_key"),
    ],
}

# ====================================================================================================================
# combat (optional): the wolves on the mountain path
# ====================================================================================================================
ENCOUNTERS_EXTRA = {
    "@wolves": {"name": "Wolves on the path", "time": "night", "enemies": ["wolf", "wolf"], "flee_ok": True,
                "intro": "The grey shapes close from either side of the track. I have a poker, a spade and my courage, in that order.",
                "win": "The wolves slink back into the gorse, one of them limping.", "location": "@path"},
}
ENCOUNTER_HOOKS = {
    "@wolves": dict(
        on_win=[dict(give="@wolf_tooth"), dict(set="@wolves_beaten"), dict(journal="@j_wolves")],
        on_lose=[dict(say="They drive me back from the path, but they do not follow. When I can stand, I find myself bruised, bleeding, and alive.")],
        on_flee=[dict(say="I run. The wolves do not follow past the cross.")],
    ),
}
JOURNAL["@j_wolves"] = dict(title="The wolves", source=M, text="Two wolves on the mountain path, hungry and bold. I fought them with a poker and a spade. One tooth I kept. I think I was braver than I have ever been, and certainly sillier.")

ASSETS = []
VARIANTS = {
    "human_peasant_m": {
        "@pell": human_colors(skin=T("skin", "#e0c4a8"), hair=T("hair", "#9a9a9a"), top=T("wool", "#1f1f24"), bottom=T("wool", "#1a1a1e")),
        "@librarian": human_colors(skin=T("skin", "#dcc0a0"), hair=T("hair", "#4a4a4a"), top=T("wool", "#2a2a32"), bottom=T("wool", "#22222a")),
        "@gardener": human_colors(skin=T("skin", "#c99a74"), hair=T("hair", "#c8c8c8"), top=T("wool", "#5a6a3a"), bottom=T("wool", "#3a3228")),
        "@verger": human_colors(skin=T("skin", "#cfa383"), hair=T("hair", "#e0e0e0"), top=T("wool", "#2e2e34"), bottom=T("wool", "#26262c")),
    },
}


# ---- expand the '@' id prefix --------------------------------------------------------------------------------------
def _x(o):
    if isinstance(o, str):
        return o.replace("@", "harker_road_")
    if isinstance(o, list):
        return [_x(i) for i in o]
    if isinstance(o, dict):
        return {_x(k): _x(v) for k, v in o.items()}
    return o


for _n in ("LOCATIONS", "LOC_DATA", "DIALOGUE", "ITEMS", "JOURNAL", "PALETTES", "PLACEMENTS", "GATES", "ENCOUNTERS_EXTRA", "ENCOUNTER_HOOKS", "ARC", "VARIANTS"):
    globals()[_n] = _x(globals()[_n])
