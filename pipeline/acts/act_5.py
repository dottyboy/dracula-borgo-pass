"""ACT V - 'The Hunt for the Boxes' (novel chapters 17-24).
Purfleet asylum, Carfax Abbey, the carriers' trail, Piccadilly, Mile End, Bermondsey; ends at Varna quay (act 6)."""
from dsl import *


# ----------------------------------------------------------------------------- dialogue helpers
def N(speaker, text, choices=None, next=None, do=None, end=False):
    d = dict(speaker=speaker, text=text)
    if do:
        d["do"] = do
    if choices:
        d["choices"] = choices
    elif next:
        d["next"] = next
    elif end:
        d["end"] = True
    return d


def C(text, next=None, do=None, cond=None, end=False):
    d = dict(text=text)
    if next:
        d["next"] = next
    if do:
        d["do"] = do
    if cond:
        d["cond"] = cond
    if end:
        d["end"] = True
    return d


LEAVE = C("[Leave it for now]", end=True)

ACT = dict(
    id=5, title="The Hunt for the Boxes",
    start=dict(location="a5_asylum_library", protagonist="seward", party=["seward", "vanhelsing", "arthur", "quincey"],
               items={"crucifix": 1, "host": 7, "garlic_wreath": 1, "stake": 1, "hammer": 1, "knife": 1, "chloral": 1},
               flags=["a5_act_start"]),
    exit_to="a6_varna_quay",
)

LOCATIONS = [
    dict(id="a5_asylum_library", name="Dr. Seward's library, Purfleet", date="29 September",
         desc="The doctor's book-lined library at the asylum. The phonograph stands on the desk, and the long table is already set for counsel."),
    dict(id="a5_typing_room", name="Mrs. Harker's typewriting room", date="30 September",
         desc="A small sunny room off the library. Mina has borrowed a typewriter and pinned the whole sad history to the wall."),
    dict(id="a5_renfield_cell", name="Renfield's room, the asylum", date="1 October",
         desc="A bare padded room with one barred window upon the park. Sugar-smears on the sill, a sealed jar of flies on the table."),
    dict(id="a5_asylum_grounds", name="The asylum grounds", date="1 October",
         desc="Lawns, a yew-tree and a high stone wall. Beyond the wall, the dark roofs of Carfax."),
    dict(id="a5_carfax_grounds", name="Carfax: the overgrown park", date="1 October",
         desc="Neglected grounds behind the high wall. The great square house stares with shuttered eyes; the chapel stands apart among the weeds."),
    dict(id="a5_carfax_chapel", name="Carfax chapel", date="1 October, dusk",
         desc="A damp, ancient chapel. The air is thick with foul earth. Dozens of great boxes lie stacked in the nave."),
    dict(id="a5_london_street", name="A London street by the cab-stand", date="2 October",
         desc="The noise of the City. Hansoms, drays and clerks. Somewhere among these streets the Count has left his trail."),
    dict(id="a5_carters_office", name="Carter, Paterson & Co., the carriers' office", date="2 October",
         desc="A smoky counting-room smelling of horse and ink. A dog-eared ledger lies open on the counter."),
    dict(id="a5_bloxam_yard", name="Potter's Court, Walworth", date="2 October",
         desc="A cramped court of carts, barrels and washing. The man I seek is said to lodge at Corcoran's."),
    dict(id="a5_agent_office", name="Mitchell, Sons & Candy, house agents", date="3 October",
         desc="A respectable office with a polished counter and a locked safe. Everything here is discretion and cash."),
    dict(id="a5_mina_bedroom", name="The Harkers' bedroom", date="3 October, night",
         desc="A bedroom behind a thick yellow blind. Gaslight, a locked door, and a cold that does not belong to October."),
    dict(id="a5_piccadilly_house", name="347 Piccadilly", date="4 October",
         desc="A stone-fronted house, high steps, a bow window, a torn 'To Let' board. Within: dust, damp and the smell of old earth."),
    dict(id="a5_mile_end_house", name="197 Chicksand Street, Mile End", date="4 October",
         desc="A tumbledown house in a poor street. The windows are boarded; the cellar smells of the grave."),
    dict(id="a5_bermondsey_house", name="Jamaica Lane, Bermondsey", date="4 October",
         desc="A damp, empty house near the river. The last of the boxes lies here."),
]

# ----------------------------------------------------------------------------- items
ITEMS = {
    "a5_cylinders": dict(name="Phonograph cylinders", asset="bottle", variant="amber",
                         desc="Dr. Seward's spoken diary, wax cylinders in a stained box. Mina begs to hear them."),
    "a5_harker_journal": dict(name="Jonathan's journal", asset="book", variant="diary",
                              desc="My husband's shorthand journal from Transylvania, held together by a strap."),
    "a5_whitby_cutting": dict(name="Mina's Whitby papers", asset="book", variant="red",
                              desc="My own diary and the Dailygraph cuttings about the wreck of the Demeter."),
    "a5_vh_memorandum": dict(name="Van Helsing's memorandum", asset="book", variant="leather",
                             desc="Van Helsing's closely written notes on Lucy's death and on the Un-Dead."),
    "a5_renfield_notebook": dict(name="Renfield's notebook", asset="book", variant="red",
                                 desc="Rows of tiny figures, pages of flies, spiders and sparrows tallied day by day."),
    "a5_typed_transcript": dict(name="The typescript", asset="book", variant="diary",
                                desc="Every paper copied in order, in triplicate. The whole case in one pile."),
    "a5_cabinet_key": dict(name="Small cabinet key", asset="key", variant="default",
                           desc="A small key, the sort a doctor hides from his own patients."),
    "a5_carfax_keys": dict(name="Carfax keys", asset="key", variant="gold",
                           desc="Heavy keys to the gate, the house and the chapel of Carfax, from Mr. Hawkins' papers."),
    "a5_chapel_key": dict(name="Chapel key", asset="key", variant="default",
                          desc="A rusty iron key. The chapel lock is old and stubborn."),
    "a5_sovereign": dict(name="Gold sovereign", asset="goblet", variant="default",
                         desc="A bright sovereign. In London, a sovereign opens more mouths than a magistrate."),
    "a5_hawkins_letter": dict(name="Letter of authority", asset="book", variant="leather",
                              desc="A letter over Jonathan's hand and Lord Godalming's seal, pleading our authority."),
    "a5_ledger_copy": dict(name="Carriers' ledger copy", asset="book", variant="red",
                           desc="A copy of the carriers' ledger: six boxes to Mile End, six to Bermondsey, nine to Piccadilly."),
    "a5_agent_keys": dict(name="Keys of 347 Piccadilly", asset="key", variant="gold",
                          desc="The keys of the Piccadilly house, handed over by the agents with a good deal of reluctance."),
    "a5_counts_keys": dict(name="The Count's keys", asset="key", variant="gold",
                           desc="A bunch of keys dropped as the Count tore through us. Each is labelled in a neat hand."),
    "a5_counts_money": dict(name="The Count's gold and notes", asset="goblet", variant="default",
                            desc="Gold and Bank of England notes, dropped from his torn coat. He paid in cash for everything."),
    "a5_lloyds_telegram": dict(name="Lloyd's telegram", asset="book", variant="leather",
                               desc="A telegram from Lloyd's: the Czarina Catherine cleared the Thames this morning for Varna."),
    "a5_ship_notes": dict(name="Notes on the Czarina Catherine", asset="book", variant="red",
                          desc="Mina's notes, in the Professor's hand: darkness, water lapping, creaking wood. A ship. Varna."),
}

# ----------------------------------------------------------------------------- journal
JOURNAL = {
    "a5_j_cellar": dict(title="Beneath the chapel", source="Professor Van Helsing's notes",
                        text="Under Carfax chapel lies a cellar of damp dressed stone, older than the house. The boxes above were carried up from here; the drag-marks on the flags are plain. Fifty boxes came to Carfax and only twenty-nine stand in the nave. The rest went out by cart, and carters keep ledgers."),
    "a5_j_labels": dict(title="Torn shipping labels", source="Professor Van Helsing's notes",
                        text="Among the straw, half-torn labels in a clerk's hand: 'Carter, Paterson and Co.' - 'Jamaica L...' - 'Piccad...' - 'to be called for'. The twenty-one missing boxes did not vanish. They were ordered, and what is ordered is written down."),
    "a5_j_vault": dict(title="The lower vault", source="Professor Van Helsing's notes",
                       text="Below the cellar, a second vault of brick where the damp stands in puddles and the air tastes of copper. If the Count made a bed in England, he made it where no church bell could reach. The cold that rises here is not the cold of stone."),
    # ch.17
    "a5_j_arrival": dict(title="29 September, Purfleet", source="Dr. Seward's diary",
                         text="Jonathan Harker and his wife arrive at the asylum. He is grey at the temples, and she is brave beyond words. Van Helsing greets them as old friends. At last, one house holds all of those who know."),
    "a5_j_harker_meet": dict(title="Jonathan Harker's journal", source="Mina Harker's journal",
                             text="Jonathan has handed Dr. Seward every page of his Transylvanian journal. I am to copy it and everything else. I know of no better use for a typewriter."),
    "a5_j_cylinders": dict(title="The locked cabinet", source="Dr. Seward's diary",
                           text="I unlocked the cabinet with the little key and gave Mrs. Harker the cylinders of my phonograph diary. She wept at Lucy's death, but said she must hear it all."),
    "a5_j_typed_cyl": dict(title="Typed: the phonograph diary", source="Mina Harker's journal",
                           text="Seward's cylinders typed. Renfield's fits, Lucy's wasting, the night at Hillingham. And a note: Renfield's wildest days fall when the Count is near the house."),
    "a5_j_typed_harker": dict(title="Typed: Jonathan's journal", source="Mina Harker's journal",
                              text="Jonathan's journal typed. The castle, the Count's boxes of earth, fifty of them in the chapel. And the shipping to Whitby, to London, to Carfax."),
    "a5_j_typed_whitby": dict(title="Typed: the Whitby papers", source="Mina Harker's journal",
                              text="My Whitby diary typed with the cuttings. A great dog leapt ashore from the Demeter, and Lucy's sleep-walking began the same week."),
    "a5_j_typed_vh": dict(title="Typed: the memorandum", source="Mina Harker's journal",
                          text="The Professor's memorandum typed: the Un-Dead cannot rest save in earth sanctified to them. They lie in their boxes by day and walk by night."),
    "a5_j_typed_renfield": dict(title="Typed: Renfield's tallies", source="Mina Harker's journal",
                                text="Renfield's notebook typed. His columns of flies and sparrows lie in a pattern. They climb and fall with the nights the Count visits."),
    "a5_j_link_carfax": dict(title="The Count's lair", source="Mina Harker's journal",
                             text="Jonathan's fifty boxes and Mr. Hawkins' deeds for Carfax. The Count sleeps among them in the old chapel next door to the asylum."),
    "a5_j_link_renfield": dict(title="Renfield is the door", source="Mina Harker's journal",
                               text="Renfield's moods and the Count's visits keep step. He is the Count's pawn, and perhaps the only one who can tell us when the Count is near."),
    "a5_j_link_whitby": dict(title="The road from Whitby", source="Mina Harker's journal",
                             text="The Demeter's cargo of fifty boxes consigned to Billington of Whitby, then by rail to London, then by carrier to Carfax. A road can be followed."),
    "a5_j_records_done": dict(title="The records are complete", source="Mina Harker's journal",
                              text="The papers are in order. Fifty boxes; the Count must rest in each of them. Destroy their holy sanctuary, and he has nowhere to hide. I told the Professor what I had found."),
    # ch.18
    "a5_j_council": dict(title="Council of war", source="Dr. Seward's diary",
                         text="We sat round the long table. Van Helsing told us all that science does not teach, and we, who laughed at it, listened. I never felt so small, nor so resolved."),
    "a5_j_rules": dict(title="What the Un-Dead are", source="Van Helsing's memorandum",
                       text="He is strong as twenty. He casts no shadow, no reflection. He cannot enter unless invited. He is powerless at noon, and cannot cross running water save at slack or flood tide. Crucifix, garlic, the Host: these he shuns."),
    "a5_j_mina_joins": dict(title="Madam Mina is one of us", source="Mina Harker's journal",
                            text="They have admitted me to counsel. The Professor says: no more secrets. I felt a great weight lift, and a greater one settle upon my heart."),
    # ch.19
    "a5_j_carfax_enter": dict(title="Carfax by lantern light", source="Dr. Seward's diary",
                              text="We went through the wall at dusk with the keys in Harker's hand. The house breathed damp. The chapel door took two of us to open. The smell of the earth was ripe."),
    "a5_j_rats": dict(title="The rats of Carfax", source="Dr. Seward's diary",
                      text="Thousands of rats, eyes like coals, poured from the crypt. Arthur's terriers went in like furies. When the lamps were held high, the swarm broke."),
    "a5_j_boxes29": dict(title="Twenty-nine of fifty", source="Jonathan Harker's journal",
                         text="We counted twenty-nine boxes, sterilised each with a crumb of the Host. Fifty came from the castle. Twenty-one are elsewhere in London, and the Count knows we are hunting."),
    # ch.20
    "a5_j_ledger": dict(title="The carriers' ledger", source="Jonathan Harker's journal",
                        text="Mr. Smollet's ledger: six boxes to 197 Chicksand Street, Mile End New Town; six to Jamaica Lane, Bermondsey; the rest nine boxes to a man called Bloxam. A sovereign opens a ledger."),
    "a5_j_bloxam": dict(title="Sam Bloxam of Walworth", source="Jonathan Harker's journal",
                        text="Bloxam carried the nine boxes to a stone-fronted house in Piccadilly, bow window, high steps, a white church nearby. An old man with a white moustache lifted a box himself."),
    "a5_j_agent": dict(title="Mitchell, Sons & Candy", source="Jonathan Harker's journal",
                       text="The house agents confirm: 347 Piccadilly sold for cash to Count de Ville. A word of Lord Godalming's, a letter and a clerk's nerves, and I have the keys."),
    "a5_j_renfield_plea": dict(title="Renfield asks to go", source="Dr. Seward's diary",
                               text="Renfield begged to be released: 'Do not let Him find me.' Not mad then, or not entirely. He feels the Count's attention. I have told Van Helsing."),
    # ch.21
    "a5_j_renfield_dead": dict(title="Renfield dying", source="Dr. Seward's diary",
                               text="We found Renfield with a broken back and a smashed skull. 'I tried to stop Him. He promised me life, and I was weak.' We are all weak. We are sworn nevertheless."),
    "a5_j_attack": dict(title="The Count in the bedroom", source="Dr. Seward's diary",
                        text="The door burst. Moonlight, mist, and Mina on her knees at the Count's chest, drinking. Jonathan in a stupor. Van Helsing held out the Host. The Count cowered back, and went."),
    "a5_j_unclean": dict(title="Unclean", source="Mina Harker's journal",
                         text="'Unclean! Unclean!' The Host burned my forehead like a hot iron. The Professor says the scar will fade when the Count is dead, and not before. I shall wear it as a sign."),
    # ch.22
    "a5_j_piccadilly": dict(title="347 Piccadilly", source="Jonathan Harker's journal",
                            text="Eight boxes in the Piccadilly hall, sterilised. Then the front door, and the Count on the threshold. He leapt through us like a cat through rats. His keys and his money fell in the hall."),
    "a5_j_keys_money": dict(title="The Count's pocketbook", source="Jonathan Harker's journal",
                            text="Notes and gold, and the bunch of keys with labels in a neat hand: Mile End, Bermondsey. He is not omnipotent. He bleeds money like any man, and he is afraid of us."),
    # ch.23
    "a5_j_mile_end": dict(title="Mile End", source="Jonathan Harker's journal",
                          text="Six boxes in a boarded cellar. Arthur's keys turned in the Count's locks. A crumb of the Host on the earth, and the hideous smell was gone."),
    "a5_j_bermondsey": dict(title="Bermondsey", source="Jonathan Harker's journal",
                            text="Six more at Jamaica Lane. Forty-nine boxes destroyed. One remains in the Count's hands, and he knows it."),
    "a5_j_bond": dict(title="The bond", source="Mina Harker's journal",
                      text="I feel him, like a cold wind with a taste. When the sun is rising or setting I seem able to follow him a little way. The Professor says this may be our only road to him."),
    "a5_j_trance1": dict(title="At sunrise", source="Mina Harker's journal",
                         text="Under the Professor's hand I heard lapping water, creaking wood, a rope taut, the hollow tramp of feet above. Darkness, and cold. I am afraid for what I said."),
    "a5_j_trance2": dict(title="At sunset", source="Mina Harker's journal",
                         text="At sunset again: dull ringing of a bell, hawsers, a cry from the deck. 'We are going, we are going.' I could not say where. The Count was close, and aware."),
    "a5_j_ship": dict(title="The Czarina Catherine", source="Mina Harker's journal",
                      text="Lloyd's reports: the Czarina Catherine cleared the Thames for Varna. A ship, water and wood, an eastbound hawser. He is returning to his own land. We must race him."),
    # ch.24
    "a5_j_plan": dict(title="Van Helsing's plan", source="Dr. Seward's diary",
                      text="By rail to Paris and the Orient Express, then Varna. The Count's ship is slow, ours fast. We shall be there first and wait for the box. All of us, save one."),
    "a5_j_left_out": dict(title="Left behind", source="Mina Harker's journal",
                          text="They have decided to go and I am not in the plan. 'It is for your safety.' I watched the cab out of sight with Jonathan's face still in my eyes. I do not mean to stay behind."),
}

# ----------------------------------------------------------------------------- locations
LOC_DATA = {}

# ---- 1. library (hub) -------------------------------------------------------
LOC_DATA["a5_asylum_library"] = dict(
    cells=[3, 2], interior=True, wall="plaster", floor="planks",
    ambient=AMBIENT["candle_interior"], camera=cam([3, 2]), lights=lights_warm([3, 2], n=3),
    walls=dict(north=["wall_window_4", "wall_door_4", "wall_window_4"], west=["wall_4", "wall_door_4"], east=["wall_door_4", "wall_door_4"]),
    spawn=[0.0, 2.6],
    spawns={"a5_typing_room": [-4.6, 2.0], "a5_renfield_cell": [4.6, -2.0], "a5_asylum_grounds": [4.6, 2.0], "a5_mina_bedroom": [0.0, -2.6]},
    props=[
        prop("a5_lib_table", "table_long", "ebony", 0, 0.2, name="Council table", radius=2.2,
             look="A long table, strewn with maps, ink and the remains of a cold supper. Here a company of strangers will become a council."),
        prop("a5_lib_candelabra", "candelabra", "default", 0, 0.2, y=0.8, name="Candelabra", radius=0.3, look="Candles enough to read by, if not to hope by."),
        prop("a5_lib_chair1", "chair", "blue", -1.5, -1.0, rot=0, radius=0.4),
        prop("a5_lib_chair2", "chair", "blue", 1.5, -1.0, rot=0, radius=0.4),
        prop("a5_lib_chair3", "chair", "green", -1.5, 1.4, rot=180, radius=0.4),
        prop("a5_lib_chair4", "chair", "green", 1.5, 1.4, rot=180, radius=0.4),
        prop("a5_lib_rug", "rug", "red", 0, 0.2, radius=0.01),
        prop("a5_lib_shelf1", "bookshelf", "dark", -2.4, -3.4, name="Medical library", radius=0.8,
             look="Rows of lunacy and physiology. I once thought they explained the world."),
        prop("a5_lib_shelf2", "bookshelf", "pale", 2.4, -3.4, name="Case-books", radius=0.8,
             look="Case-books of the asylum, with Renfield's more voluminous than most."),
        prop("a5_lib_fire", "fireplace", "soot", -5.3, -2.0, rot=90, name="Fireplace", radius=0.9,
             look="A modest fire. On the mantel, a stopped carriage-clock and a small stone bust."),
        prop("a5_lib_bust", "bust", "plaster", -5.3, -0.4, rot=90, y=0.0, name="Plaster bust", radius=0.3,
             look="A bust of Hippocrates, rather the worse for dust. Hollow, I am told, though I never tested the claim."),
        prop("a5_cabinet", "chest", "ebony", -4.7, 2.4, rot=90, name="Specimen cabinet", radius=0.6,
             look="A tall locked cabinet where I keep the more private records. A small keyhole, brass-rimmed.",
             use_item={"a5_cabinet_key": [{"say": "The little key turns. Within lie the wax cylinders of my phonograph diary, in their stained box."},
                                          {"give": "a5_cylinders"}, {"set": "a5_cabinet_open"}, {"journal": "a5_j_cylinders"}]},
             use_fail="That does not open it. The keyhole is small and brass-rimmed."),
        prop("a5_desk", "table", "dark", 4.0, -2.2, name="Writing desk", radius=0.9, look="My desk. Ink, blotter, and a pile of letters I cannot bring myself to answer."),
        prop("a5_phonograph", "chest", "pale", 4.0, -2.2, y=0.8, scale=0.45, name="Phonograph", radius=0.3,
             look="My phonograph, the Edison I use for my diary. Its horn is turned to the wall."),
        prop("a5_inkstand", "bottle", "green", 3.5, -2.2, y=0.8, name="Inkstand", radius=0.2, look="A heavy glass inkstand with a stopper."),
        prop("a5_side_table", "table", "pale", -4.4, -0.2, name="Side table", radius=0.6, look="A small table for the decanter, the one comfort of long nights."),
        prop("a5_decanter", "bottle", "amber", -4.4, -0.2, y=0.8, name="Brandy decanter", radius=0.15,
             look="Good brandy. Many a night it has served as supper.", take="brandy", take_text="I took the decanter. It has revived better men than I.", give_once=True),
        prop("a5_carafe", "bottle", "glass", -4.4, 0.4, y=0.0, name="Water carafe", radius=0.15,
             look="A carafe of fresh water on the floor beside the side-table.", take="water", take_text="I took the carafe of water.", give_once=True),
        prop("a5_mail_tray", "chest", "pale", 3.2, 2.5, scale=0.5, name="Letter tray", radius=0.3,
             look="The post tray. Nothing yet.", cond="!a5_trance2"),
        prop("a5_mail_tray_full", "chest", "pale", 3.2, 2.5, scale=0.5, name="Letter tray", radius=0.3, cond="a5_trance2",
             look="A fresh telegram lies on the tray, still sealed with the office's blue wax.",
             take="a5_lloyds_telegram", take_text="I opened the telegram. It is from Lloyd's.", give_once=True),
        prop("a5_clock", "column_short", "stone_dark", -3.2, 3.0, name="Tall clock", radius=0.3,
             look="The tall clock in the corner. When it strikes, the house goes to bed, and the nightmares wake.", talk="a5_night_prompt"),
        prop("a5_door_typing", "door", "dark", -5.8, 2.0, rot=90, name="Door to the typewriting room", radius=0.6,
             look="The door to Mina's typewriting room; the click of keys comes through it.", go="a5_typing_room"),
        prop("a5_door_ward", "door", "dark", 5.8, -2.0, rot=-90, name="Door to the wards", radius=0.6,
             look="The corridor to the wards, and Renfield's room.", go="a5_renfield_cell"),
        prop("a5_door_grounds", "door", "dark", 5.8, 2.0, rot=-90, name="Door to the garden", radius=0.6,
             look="The garden door.", go="a5_asylum_grounds"),
        prop("a5_door_guest", "door", "dark", 0, -3.8, name="Stairs to the guest rooms", radius=0.6,
             look="The stair to the guest rooms, where the Harkers are lodged.", go="a5_mina_bedroom"),
    ],
    npcs=[
        npc("a5_harker_lib", "human_harker", "harker", -3.6, -1.6, rot=90, name="Jonathan Harker",
            look="Jonathan, hair gone white at the temples, a man who has seen the mountains' other side.", talk="a5_harker_talk"),
        npc("a5_mina_lib1", "human_mina", "mina", -3.6, 1.6, rot=90, name="Mina Harker", cond="!a5_records_done",
            look="Mrs. Harker, small and straight, with a printer's patience about her. Her eyes are very bright.", talk="a5_mina_talk1"),
        npc("a5_mina_lib2", "human_mina", "mina", -3.6, 1.6, rot=90, name="Mina Harker", cond="a5_records_done&!a5_attack_done",
            look="Mina, pale and resolute. Her hands are never still: she folds, unfolds, touches the typescript.", talk="a5_mina_talk2"),
        npc("a5_mina_lib3", "human_mina", "mina", -3.6, 1.6, rot=90, name="Mina Harker", cond="a5_attack_done&!a5_boxes_done",
            look="Mina, with a linen band across her brow. She meets my eye bravely.", talk="a5_mina_talk3"),
        npc("a5_mina_lib4", "human_mina", "mina", -3.6, 1.6, rot=90, name="Mina Harker", cond="a5_boxes_done&!a5_ship_known",
            look="Mina sits in the high-backed chair, like one expecting to be questioned by a dream.", talk="a5_mina_trance"),
        npc("a5_mina_lib5", "human_mina", "mina", -3.6, 1.6, rot=90, name="Mina Harker", cond="a5_ship_known",
            look="Mina, very still. She has understood before any of us that she will not be taken.", talk="a5_mina_farewell"),
        npc("a5_vh_lib1", "human_vanhelsing", "vh", 3.4, 0.6, rot=-90, name="Professor Van Helsing", cond="!a5_records_done",
            look="A broad, keen-eyed Dutchman with a pointed beard. He carries a heavy bag as though it held sleeping children.", talk="a5_vh_talk1"),
        npc("a5_vh_lib2", "human_vanhelsing", "vh", 3.4, 0.6, rot=-90, name="Professor Van Helsing", cond="a5_records_done&!a5_council_done",
            look="The Professor, standing at the head of the table like a physician before a hard case.", talk="a5_council"),
        npc("a5_vh_lib3", "human_vanhelsing", "vh", 3.4, 0.6, rot=-90, name="Professor Van Helsing", cond="a5_council_done&!a5_attack_done",
            look="Van Helsing, at ease for once, but never idle. His bag is open.", talk="a5_vh_talk3"),
        npc("a5_vh_lib4", "human_vanhelsing", "vh", 3.4, 0.6, rot=-90, name="Professor Van Helsing", cond="a5_attack_done&!a5_boxes_done",
            look="The Professor, with the Host at his breast and grief behind his eyes.", talk="a5_vh_talk4"),
        npc("a5_vh_lib5", "human_vanhelsing", "vh", 3.4, 0.6, rot=-90, name="Professor Van Helsing", cond="a5_boxes_done&!a5_ship_known",
            look="Van Helsing, turning a gold coin over and over: the old hypnotist's trick, made grim.", talk="a5_vh_trance"),
        npc("a5_vh_lib6", "human_vanhelsing", "vh", 3.4, 0.6, rot=-90, name="Professor Van Helsing", cond="a5_ship_known",
            look="The Professor with timetables spread before him, already half in Varna.", talk="a5_vh_plan"),
        npc("a5_arthur_lib", "human_arthur", "lord", 3.4, 2.4, rot=-90, name="Arthur Holmwood",
            look="Lord Godalming, calm in a way he did not use to be. Grief has given him a quiet edge.", talk="a5_arthur_talk"),
        npc("a5_quincey_lib", "human_quincey", "texan", -0.2, 3.0, rot=180, name="Quincey Morris",
            look="The Texan, lounging with a cigar he does not light. He has already counted the doors.", talk="a5_quincey_talk"),
    ],
    on_enter=[dict(once=True, do=[{"journal": "a5_j_arrival"},
                                  {"say": "The Harkers have come. Jonathan, aged by a month in the castle. Mina, small and valiant. The Professor beams at them, like a man seeing hope at last."}])],
)

PLACEMENTS = {
    "a5_cabinet_key": [
        dict(prop="a5_inkstand", text="Under the inkstand's felt base, a small brass key.", hint="The inkstand sits a little crookedly on its blotter."),
        dict(prop="a5_lib_bust", text="The bust's head lifts; in the hollow neck, a small brass key. I knew Hippocrates had a use.", hint="The bust looks hollow."),
        dict(prop="a5_lib_candelabra", text="Tucked in the candelabra's base, a small key on a bit of ribbon.", hint="A scrap of ribbon peeps from the candelabra's foot."),
    ],
    "a5_chapel_key": [
        dict(prop="a5_gatepost", text="In a crack of the gatepost: a rusty iron key. Someone left it there, years ago.", hint="Moss has been scraped off the gatepost recently."),
        dict(prop="a5_wellhead", text="Inside the dry well-head, wrapped in oiled cloth, the chapel key.", hint="The well-cover is not as heavy as it looks."),
        dict(prop="a5_old_cross", text="At the foot of the weathered cross lies an iron key under a flat stone.", hint="One flat stone at the cross's foot has been turned."),
    ],
}

# ---- 2. typing room ---------------------------------------------------------
LOC_DATA["a5_typing_room"] = dict(
    cells=[2, 2], interior=True, wall="plaster", floor="planks",
    ambient=AMBIENT["warm_day_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2]),
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[2.6, 2.0], spawns={"a5_asylum_library": [2.6, 2.0]},
    props=[
        prop("a5_type_desk", "table", "pale", -1.6, -1.8, name="Typewriting desk", radius=0.9, look="A sturdy desk, with carbon paper in neat stacks."),
        prop("a5_typewriter", "chest", "ebony", -1.6, -1.8, y=0.8, scale=0.45, name="Typewriter", radius=0.3,
             look="A Remington, borrowed from the village. I feed it papers and it gives back order.",
             use_item={
                 "a5_cylinders": [{"say": "I played each cylinder through, and typed it. Lucy, the wasting, the sick nights. And Renfield's fits..."}, {"set": "a5_typed_cyl"}, {"journal": "a5_j_typed_cyl"}],
                 "a5_harker_journal": [{"say": "Jonathan's shorthand, page after page, into clean type. The castle, the Count, the boxes."}, {"set": "a5_typed_harker"}, {"journal": "a5_j_typed_harker"}],
                 "a5_whitby_cutting": [{"say": "My own diary, the Dailygraph cuttings, the wreck of the Demeter. Typed and cross-referenced."}, {"set": "a5_typed_whitby"}, {"journal": "a5_j_typed_whitby"}],
                 "a5_vh_memorandum": [{"say": "The Professor's memorandum, in his careful foreign English. I corrected nothing and understood a great deal."}, {"set": "a5_typed_vh"}, {"journal": "a5_j_typed_vh"}],
                 "a5_renfield_notebook": [{"say": "Renfield's tallies, copied exactly. Columns, dates, a pattern that is not quite coincidence."}, {"set": "a5_typed_renfield"}, {"journal": "a5_j_typed_renfield"}],
             },
             use_fail="I cannot type that. It is not a record."),
        prop("a5_clue_board", "bookshelf", "pale", 2.0, -3.4, name="Pinned papers", radius=0.8,
             look="Mina has pinned notes, cuttings and tickets in order. Threads of cotton link them. A wall of knowledge.", talk="a5_clue_board"),
        prop("a5_type_chair", "chair", "green", -1.6, -0.7, rot=0, radius=0.4),
        prop("a5_type_lamp", "lantern", "default", 1.0, -1.8, y=0.0, name="Reading lamp", radius=0.3, look="A good lamp, trimmed bright."),
        prop("a5_type_rug", "rug", "cream", 0, 0.5, radius=0.01),
        prop("a5_type_papers", "book", "leather", -1.0, 1.4, y=0.0, name="Carbon copies", radius=0.3, look="Three copies of everything. 'Never trust one copy,' Jonathan says."),
        prop("a5_type_basket", "barrel", "pale", 2.8, 0.0, scale=0.5, name="Waste basket", radius=0.3, look="Overflowing with spoiled sheets."),
        prop("a5_door_type_out", "door", "dark", 3.8, 2.0, rot=-90, name="Door to the library", radius=0.6, look="Back to the library.", go="a5_asylum_library"),
    ],
    npcs=[],
    on_enter=[dict(once=True, do=[{"protagonist": "mina"}, {"say": "Sunlight, a borrowed typewriter, and the whole of a terrible story to set in order. Jonathan's shorthand, Seward's cylinders, my Whitby papers, the Professor's memorandum: each must be typed, and then I will see what they say together."}])],
)

# ---- 3. Renfield's cell -----------------------------------------------------
LOC_DATA["a5_renfield_cell"] = dict(
    cells=[2, 2], interior=True, wall="plaster_dirty", floor="planks",
    ambient=AMBIENT["cold_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2], n=2, energy=1.8),
    walls=dict(north=["wall_4", "wall_window_4"], west=["wall_door_4", "wall_4"], east=["wall_4", "wall_4"]),
    spawn=[-2.6, -2.0], spawns={"a5_asylum_library": [-2.6, -2.0]},
    props=[
        prop("a5_cell_bed", "bed_simple", "black", -2.2, 2.2, rot=90, name="Iron cot", radius=0.9, look="A narrow bed with a grey blanket. The sheets are ripped in strips for some purpose of his own."),
        prop("a5_cell_table", "table", "pale", 2.0, -1.6, name="Little table", radius=0.7, look="Sugar spilled in a careful ring. Dead flies lie in rows like soldiers."),
        prop("a5_fly_jar", "bottle", "glass", 1.6, -1.6, y=0.8, name="Jar of flies", radius=0.15, look="A jar full of flies, kept for the spiders. 'Life,' Renfield calls it. 'Life, Doctor.'"),
        prop("a5_sugar", "goblet", "default", 2.4, -1.6, y=0.8, name="Sugar bowl", radius=0.15, look="Sugar for the flies. The attendants say he saves it from his tea."),
        prop("a5_renfield_book", "book", "red", 2.0, -1.2, y=0.8, name="Renfield's notebook", radius=0.2,
             look="Pages of figures, dates, little tallies of flies, spiders, sparrows. Each day is a ledger of lives. It might be that the figures themselves mean something.",
             take="a5_renfield_notebook", take_text="I took the notebook. Mina may find the pattern I cannot.", give_once=True),
        prop("a5_cell_window", "fence", "default", 2.0, -3.7, name="Barred window", radius=0.8,
             look="The sash opens only an inch, and there is a bar across it. The park beyond is grey with fog."),
        prop("a5_cell_lantern", "lantern", "default", -2.6, -0.6, name="Lamp", radius=0.3, look="A lamp turned low, the nearest thing to company he allows."),
        prop("a5_cell_chair", "chair", "black", 0, 0.4, rot=0, radius=0.4, name="Doctor's chair", look="My chair. I have sat here more nights than my own bed."),
        prop("a5_door_cell_out", "door", "dark", -3.8, -2.0, rot=90, name="Door to the corridor", radius=0.6, look="The corridor and the library beyond.", go="a5_asylum_library"),
    ],
    npcs=[
        npc("a5_renfield", "human_renfield", "asylum", 0.4, -1.8, rot=0, name="R. M. Renfield", cond="!a5_night_attack",
            look="Renfield, pale and sweating, hands twisting at his waistcoat. For once there is terror in him, not cunning.", talk="a5_renfield_plea"),
        npc("a5_renfield_dying", "human_renfield", "asylum", 0.4, 0.4, rot=0, name="Renfield, dying", cond="a5_night_attack&!a5_renfield_died",
            look="Renfield on the floor, back broken, face bruised past knowing. He lives, but only just.", talk="a5_renfield_dying"),
        npc("a5_renfield_dead", "human_renfield", "asylum", 0.4, 0.4, rot=90, name="Renfield (dead)", cond="a5_renfield_died",
            look="He is at peace at last. His hands are open.", talk="a5_renfield_dead"),
        npc("a5_attendant", "human_peasant_m", "villager", -1.6, 1.2, rot=-90, name="Simmons, the attendant",
            look="Simmons, a decent, stolid man who has seen nothing, and would rather not say so.", talk="a5_attendant_talk"),
    ],
    on_enter=[dict(**{"if": "a5_night_attack"}, once=True,
                  do=[{"protagonist": "seward"}, {"say": "A scream in the night, then silence. Simmons ran for me. Renfield lies in a glittering pool of blood. Something has been here that was not a man."}])],
)

# ---- 4. asylum grounds ------------------------------------------------------
LOC_DATA["a5_asylum_grounds"] = dict(
    cells=[3, 2], interior=False, wall="stone_grey", floor="grass",
    ambient=AMBIENT["day_exterior"], camera=cam([3, 2]), lights=lights_day(),
    scatter=dict(asset="pine", variant="dark", count=22, seed=51, avoid=[[-7, -5, 7, 5]]),
    spawn=[-4.4, 0.6], spawns={"a5_asylum_library": [-4.4, 0.6], "a5_carfax_grounds": [0.0, -2.6], "a5_london_street": [3.6, 1.6]},
    props=[
        prop("a5_g_door", "door_big", "dark", -5.4, 0.6, rot=90, name="Asylum door", radius=0.8, look="The garden door of the asylum.", go="a5_asylum_library"),
        prop("a5_g_gate", "door_big", "ebony", 0, -3.8, name="Gate in the wall", radius=0.8,
             look="A heavy oak gate, bolted on the Carfax side. Beyond lie the neglected grounds.",
             go="a5_carfax_grounds", go_cond="has:a5_carfax_keys&flag:a5_council_done",
             go_fail="The gate is locked, and we have no authority yet to break into Count's own land. Mr. Harker has Mr. Hawkins' keys, and the Professor wants counsel first."),
        prop("a5_g_fence1", "fence", "default", -3.2, -3.8, radius=0.5),
        prop("a5_g_fence2", "fence", "default", 3.2, -3.8, radius=0.5),
        prop("a5_g_yew", "pine_small", "dark", 3.8, -1.8, name="The great yew", radius=0.5,
             look="A great yew with a view over Carfax. Quincey says a man could sit there all night and see the chapel door."),
        prop("a5_g_bench", "bench", "dark", -2.0, 2.4, name="Garden bench", radius=0.6, look="A bench the patients use on fine days."),
        prop("a5_g_oil", "barrel", "dark", -4.2, -2.6, name="Oil barrel", radius=0.4,
             look="Lamp oil for the asylum, kept in a barrel by the shed.", take="oil", take_text="I filled a flask with lamp oil. Fire is a thing the Un-Dead respect.", give_once=True),
        prop("a5_g_wood", "chest", "oak", -4.6, -1.4, name="Wood-pile", radius=0.5,
             look="Stacked ash for the asylum stoves. One could make a stake of it.", take="wood", take_text="I chose a straight billet of ash.", give_once=True),
        prop("a5_g_cloth", "bench", "pale", 1.4, 3.0, name="Washing line", radius=0.5,
             look="Linen drying in the sun. Good for bandages, and torches.", take="cloth", take_text="I took a strip of clean linen.", give_once=True),
        prop("a5_g_cab", "carriage", "dark", 4.4, 1.6, rot=-90, name="Cab for town", radius=1.1,
             look="A hansom waiting for hire at the lodge. London is only an hour away.",
             go="a5_london_street", go_cond="flag:a5_missing_21",
             go_fail="We have no business in town yet. There is Carfax first, and the Professor's plan."),
        prop("a5_g_lamp", "lantern", "default", 0.2, 1.4, name="Garden lamp", radius=0.3, look="A lamp on a post, not yet lit."),
        prop("a5_g_rock", "rock", "mossy", 5.0, 3.0, radius=0.6),
    ],
    npcs=[
        npc("a5_gardener", "human_peasant_m", "villager", -2.6, -1.2, rot=90, name="Old gardener",
            look="The asylum gardener, with a billhook and a villager's longing to be somewhere else.", talk="a5_gardener_talk"),
        npc("a5_cabman", "human_peasant_m", "innkeeper", 3.2, 2.8, rot=-90, name="Cabman",
            look="A cabman with a red nose and a talent for hearing what he shouldn't.", talk="a5_cabman_talk"),
    ],
)

# ---- 5. Carfax grounds ------------------------------------------------------
LOC_DATA["a5_carfax_grounds"] = dict(
    cells=[3, 2], interior=False, wall="stone_mossy", floor="dirt",
    ambient=AMBIENT["dusk_exterior"], camera=cam([3, 2]), lights=lights_moon(2.2),
    scatter=dict(asset="deadtree", variant="grey", count=14, seed=88, avoid=[[-7, -5, 7, 5]]),
    scatter2=dict(asset="rock", variant="mossy", count=10, seed=19, avoid=[[-7, -5, 7, 5]]),
    spawn=[-4.4, 0.6], spawns={"a5_asylum_grounds": [-4.4, 0.6], "a5_carfax_chapel": [0.0, -2.6]},
    props=[
        prop("a5_cg_back", "door_big", "ebony", -5.4, 0.6, rot=90, name="Gate to the asylum", radius=0.8, look="The gate we came by.", go="a5_asylum_grounds"),
        prop("a5_cg_house", "tower", "stone_dark", -3.6, -5.4, scale=1.2, name="Carfax House", radius=1.4,
             look="A great ugly house, shuttered, with a smell of damp stone. There is no light, and there should not be."),
        prop("a5_cg_chapel_door", "door_big", "dark", 2.6, -3.8, name="Chapel door", radius=0.8,
             look="The old chapel door, iron-bound and rotten. It has been locked for years, and recently opened.",
             go="a5_carfax_chapel", go_cond="has:a5_chapel_key",
             go_fail="Locked. The great lock is rusted, but the Count's hand has oiled it. The key must be somewhere in the grounds."),
        prop("a5_gatepost", "gravestone_point", "stone_mossy", 4.8, -1.6, name="Leaning gatepost", radius=0.4,
             look="A leaning gatepost, green with moss."),
        prop("a5_wellhead", "barrel", "dark", -3.0, 1.8, name="Dry well-head", radius=0.5, look="A well-head, covered with a plank. It stinks of earth."),
        prop("a5_old_cross", "grave_cross", "stone_mossy", 3.2, 2.4, name="Weathered cross", radius=0.4, look="A cross, so old that no name remains."),
        prop("a5_cg_fence1", "fence", "default", -1.0, -3.8, radius=0.5),
        prop("a5_cg_fence2", "fence", "default", 5.0, -3.8, radius=0.5),
        prop("a5_cg_bench", "bench", "ebony", 0.0, 2.8, name="Rotten bench", radius=0.6, look="Moss has eaten the seat. No one has sat here in decades."),
        prop("a5_cg_lantern", "lantern", "default", 0.0, 0.2, name="Hurricane lamp", radius=0.3, look="Harker's lamp, set down on the path, a small yellow world."),
    ],
    npcs=[
        npc("a5_harker_cg", "human_harker", "harker", -1.6, -0.6, rot=-90, name="Jonathan Harker",
            look="Jonathan, white and silent, looking at the house as though it were the castle again.", talk="a5_harker_cg"),
    ],
    on_enter=[dict(once=True, do=[{"journal": "a5_j_carfax_enter"}, {"protagonist": "harker"},
                                  {"say": "Behind the wall: a wilderness. Carfax was always the Count's, and I held the paper that gave it to him. Now I hold the keys that may unmake him."}])],
)

# ---- 6. Carfax chapel -------------------------------------------------------
def _stack(n, label, boxes, x, z):
    """An unsterilised stack (visible once the rats are gone) and its sterilised twin."""
    return [
        prop(f"a5_box_s{n}", "coffin", "dark", x, z, scale=0.85, name=f"Boxes of earth ({boxes})", radius=0.9, cond=f"won:carfax_rats&!a5_ster_{n}",
             look=f"{label}: {boxes} great boxes of foul earth, brought from Transylvania. They hum, to my ear, with something evil.",
             use_item={"host": [{"say": f"I laid a crumb of the Host upon each of the {boxes} boxes. The earth hissed and was clean."},
                                {"set": f"a5_ster_{n}"}]},
             use_fail="Only the Sacred Host can make this earth unfit for the Count."),
        prop(f"a5_box_c{n}", "coffin", "pale", x, z, scale=0.85, name=f"Cleansed boxes ({boxes})", radius=0.9, cond=f"a5_ster_{n}",
             look="The earth is pale and dead now. The Count can never lie here again."),
    ]


LOC_DATA["a5_carfax_chapel"] = dict(
    cells=[3, 3], interior=True, wall="stone_mossy", floor="stone_dark",
    ambient=AMBIENT["crypt"], camera=cam([3, 3]), lights=[dict(pos=[0, 2.4, -2], color="#ff9a40", energy=2.4, range=12), dict(pos=[-4, 1.8, 3], color="#c88040", energy=1.4, range=9)],
    walls=dict(north=["wall_4", "wall_window_4", "wall_4"], west=["wall_4", "wall_4", "wall_4"], east=["wall_4", "wall_4", "wall_door_4"]),
    spawn=[4.6, 4.0], spawns={"a5_carfax_grounds": [4.6, 4.0]},
    props=_stack(1, "The first stack", 6, -3.6, -3.0) + _stack(2, "The second stack", 6, 3.4, -3.0) + _stack(3, "The third stack", 6, -3.8, 0.8)
          + _stack(4, "The fourth stack", 6, 3.8, 0.8) + _stack(5, "The last stack", 5, -0.4, 3.4) + [
        prop("a5_ch_altar", "tomb", "stone_tomb", 0, -4.4, name="Ruined altar", radius=0.9, look="The altar-stone is cracked. Dust and earth cover it. The Count has made a jest of the place."),
        prop("a5_ch_col1", "column", "stone_mossy", -2.0, -1.4, radius=0.35),
        prop("a5_ch_col2", "column", "stone_mossy", 2.0, -1.4, radius=0.35),
        prop("a5_ch_bench", "bench", "ebony", 0, 0.6, name="Broken pew", radius=0.6, look="A pew, rotten with age. The saints on the wall are scarcely visible."),
        prop("a5_ch_tally", "gravestone", "stone_dark", 4.8, -1.8, rot=-90, name="Chalk marks", radius=0.4,
             look="Strokes of chalk on the stone, in fives, crossed through. I count twenty-nine strokes. Someone has been counting what was brought, and not all of it came here."),
        prop("a5_ch_rat1", "bat", "brown", -1.0, 1.4, scale=0.5, cond="!won:carfax_rats", radius=0.2),
        prop("a5_ch_rat2", "bat", "brown", 1.6, 2.4, scale=0.5, cond="!won:carfax_rats", radius=0.2),
        prop("a5_ch_rat3", "bat", "brown", 2.8, -0.4, scale=0.5, cond="!won:carfax_rats", radius=0.2),
        prop("a5_ch_terrier", "wolf", "white", -1.4, 2.2, scale=0.45, cond="won:carfax_rats", name="Arthur's terrier", radius=0.3,
             look="One of Arthur's terriers, a small hard dog with a scarred nose and a conqueror's air."),
        prop("a5_ch_lantern", "lantern", "default", 1.4, -0.6, name="Hurricane lamp", radius=0.3, look="Lamps held high are the best weapon against rats."),
        prop("a5_ch_back", "door", "dark", 5.8, 4.0, rot=-90, name="Door to the park", radius=0.6, look="The door to the park.", go="a5_carfax_grounds"),
    ],
    npcs=[
        npc("a5_rat_swarm", "bat", "brown", 0.2, 0.8, rot=0, name="Swarm of rats", look="Hundreds of rats in the nave, a rolling grey tide with eyes like coals.", fight="carfax_rats"),
        npc("a5_vh_chapel", "human_vanhelsing", "vh", 2.6, 1.8, rot=-90, name="Professor Van Helsing",
            look="The Professor, bag at his feet, a pyx of consecrated Host in one gloved hand.", talk="a5_vh_chapel"),
        npc("a5_harker_chapel", "human_harker", "harker", -2.6, 2.4, rot=90, name="Jonathan Harker",
            look="Jonathan holding the lamp, counting under his breath.", talk="a5_harker_chapel"),
    ],
    on_enter=[dict(once=True, do=[{"protagonist": "vanhelsing"},
                                  {"say": "The chapel door gives with a groan. The smell: earth, old and ripe, laced with a coppery sweetness. And from the nave, a soft rushing, like a river of small feet."}])],
)

# ---- 7. London street (hub of the trail) ------------------------------------
LOC_DATA["a5_london_street"] = dict(
    cells=[3, 2], interior=False, wall="stone_grey", floor="cobble",
    ambient=AMBIENT["day_exterior"], camera=cam([3, 2]), lights=lights_day(2.8),
    spawn=[3.6, 1.6], spawns={"a5_asylum_grounds": [3.6, 1.6], "a5_carters_office": [-4.0, -2.4], "a5_agent_office": [0.0, -2.6],
                              "a5_bloxam_yard": [-4.4, 0.6], "a5_piccadilly_house": [4.0, -2.4], "a5_mile_end_house": [1.6, 2.6], "a5_bermondsey_house": [-1.6, 2.6]},
    props=[
        prop("a5_st_cab", "carriage", "dark", 4.6, 1.8, rot=-90, name="Cab to Purfleet", radius=1.1,
             look="The cab that brought us up from the asylum.", go="a5_asylum_grounds"),
        prop("a5_st_carters", "door_big", "oak", -4.0, -3.8, name="Carter, Paterson & Co.", radius=0.8,
             look="A gilt sign above a smoke-black door: 'CARTER, PATERSON & CO., CARRIERS'.", go="a5_carters_office"),
        prop("a5_st_agent", "door_big", "ebony", 0, -3.8, name="Mitchell, Sons & Candy", radius=0.8,
             look="A brass plate: 'MITCHELL, SONS & CANDY, HOUSE AGENTS AND SURVEYORS'.", go="a5_agent_office",
             go_cond="flag:a5_bloxam_done", go_fail="I have no reason to knock there yet. First I must learn where the boxes went."),
        prop("a5_st_piccadilly", "door_big", "dark", 4.0, -3.8, name="Path to 347 Piccadilly", radius=0.8,
             look="A stone-fronted house with a bow window, high steps, and a torn 'To Let' board. I have walked past it this morning.",
             go="a5_piccadilly_house", go_cond="has:a5_agent_keys&flag:a5_attack_done",
             go_fail="Not yet. We must be armed and in company, and Mina must be safe first."),
        prop("a5_st_alley", "door_big", "dark", -5.4, 0.6, rot=90, name="Walworth alley", radius=0.8,
             look="A narrow alley leads south toward Walworth and its courts.", go="a5_bloxam_yard", go_cond="flag:a5_decoded",
             go_fail="I have a scrap of paper in Mr. Smollet's spelling, but I do not know where it points. I need someone to read it with me."),
        prop("a5_st_hansom_me", "carriage", "ebony", 1.6, 3.0, rot=-90, name="Hansom to Mile End", radius=1.1,
             look="A hansom for hire. 'Mile End New Town, sir? Chicksand Street?'", go="a5_mile_end_house", go_cond="has:a5_counts_keys",
             go_fail="We do not have the keys for those houses yet; the Count's own bunch would open them."),
        prop("a5_st_hansom_b", "carriage", "oak", -1.6, 3.0, rot=-90, name="Hansom to Bermondsey", radius=1.1,
             look="A growler for hire. 'Jamaica Lane, sir? That be Bermondsey.'", go="a5_bermondsey_house", go_cond="has:a5_counts_keys",
             go_fail="We do not have the keys for those houses yet; the Count's own bunch would open them."),
        prop("a5_st_sign", "signpost", "dark", -2.4, 0.4, name="Street sign", radius=0.3,
             look="'Bartel Street' points one way, 'Piccadilly' the other, and 'Walworth Road' somewhere beyond a hundred chimneys."),
        prop("a5_st_lamp", "lantern", "default", 2.0, -1.0, name="Street lamp", radius=0.3, look="A gas-lamp, not yet lit."),
        prop("a5_st_barrel", "barrel", "dark", -3.8, 2.2, name="Coster's barrel", radius=0.4, look="A barrel of winkles, abandoned by a coster."),
        prop("a5_st_rock", "rock", "dark", 5.2, -1.6, radius=0.5),
    ],
    npcs=[
        npc("a5_harker_st", "human_harker", "travel", -2.0, 1.2, rot=0, name="Jonathan Harker",
            look="Jonathan in a plain travelling coat, notebook in hand. He has hardened since the castle.", talk="a5_harker_street"),
        npc("a5_urchin", "human_peasant_m", "villager", 1.2, -1.2, rot=0, name="Street boy",
            look="A thin boy with quick eyes. He holds out a hand without shame.", talk="a5_urchin_talk"),
    ],
    on_enter=[dict(once=True, do=[{"protagonist": "harker"},
                                  {"say": "London. The Count chose well: a city so large that fifty boxes of earth pass for ordinary freight. But boxes leave marks in ledgers, and ledgers are my trade."}])],
)

# ---- 8. carriers' office ----------------------------------------------------
LOC_DATA["a5_carters_office"] = dict(
    cells=[2, 2], interior=True, wall="plaster_dirty", floor="planks",
    ambient=AMBIENT["candle_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2]),
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[2.6, 2.0], spawns={"a5_london_street": [2.6, 2.0]},
    props=[
        prop("a5_co_counter", "table_long", "dark", 0, -1.4, name="Counter", radius=2.0, look="A scarred oak counter, laden with forms and string."),
        prop("a5_co_ledger", "book", "red", 0, -1.4, y=0.8, name="Carriers' ledger", radius=0.25,
             look="A heavy ledger, chained to the counter. Mr. Smollet keeps a hand on it. The page for last month is dog-eared."),
        prop("a5_co_shelf", "bookshelf", "oak", -2.4, -3.4, name="Dockets and waybills", radius=0.8, look="Waybills by the hundredweight."),
        prop("a5_co_parcels", "barrel", "oak", 2.4, -3.0, name="Parcels", radius=0.5, look="Parcels tied with string and labelled in four different hands."),
        prop("a5_co_stool", "chair", "black", -2.0, 0.6, name="Clerk's stool", radius=0.4, look="A high stool for an unhappy clerk."),
        prop("a5_co_lamp", "lantern", "default", 2.0, 1.0, name="Lamp", radius=0.3, look="A smoky lamp, left lit all day."),
        prop("a5_co_rug", "rug", "black", 0, 1.0, radius=0.01),
        prop("a5_co_notice", "mirror", "default", -3.5, -3.7, name="Notice", radius=0.3, look="A notice: 'Carriers are not responsible for boxes of earth, live eels, or the Devil.' A wag has added the last item."),
        prop("a5_co_door", "door", "oak", 3.8, 2.0, rot=-90, name="Door to the street", radius=0.6, look="The street.", go="a5_london_street"),
    ],
    npcs=[
        npc("a5_smollet", "human_peasant_m", "innkeeper", 0, -2.4, rot=0, name="Mr. Joseph Smollet",
            look="Mr. Smollet, foreman of the carriers: a thick man with ink on his cuffs and a cautious eye for strangers.", talk="a5_smollet_talk"),
        npc("a5_snelling", "human_peasant_m", "szgany", -2.8, 1.8, rot=90, name="Thomas Snelling",
            look="Thomas Snelling, the carter, asleep upright on a sack and smelling of beer.", talk="a5_snelling_talk"),
    ],
)

# ---- 9. Bloxam's yard -------------------------------------------------------
LOC_DATA["a5_bloxam_yard"] = dict(
    cells=[2, 2], interior=False, wall="stone_grey", floor="dirt",
    ambient=AMBIENT["day_exterior"], camera=cam([2, 2]), lights=lights_day(2.6),
    spawn=[-2.6, 1.0], spawns={"a5_london_street": [-2.6, 1.0]},
    props=[
        prop("a5_by_gate", "door_big", "dark", -3.6, 1.0, rot=90, name="Court entrance", radius=0.8, look="The mouth of the court, back to the alley.", go="a5_london_street"),
        prop("a5_by_cart", "carriage", "dark", 2.4, -1.2, rot=45, name="Hand-cart", radius=1.0, look="A long hand-cart. The planks are dented with the corners of heavy boxes."),
        prop("a5_by_barrel1", "barrel", "oak", -1.4, -2.6, name="Rain barrel", radius=0.4, look="A rain barrel with a drowned cat's-tail floating."),
        prop("a5_by_barrel2", "barrel", "dark", 3.0, 1.6, radius=0.4),
        prop("a5_by_washing", "fence", "default", -2.2, -1.0, name="Washing line", radius=0.4, look="Grey linen on a line across the court."),
        prop("a5_by_bench", "bench", "ebony", 1.0, 2.4, name="Doorstep bench", radius=0.5, look="Corcoran's bench, where Bloxam drinks."),
        prop("a5_by_lamp", "lantern", "default", 0.6, -0.4, name="Lamp", radius=0.3, look="A lamp, left lit all night by the landlady."),
        prop("a5_by_rock", "rock", "dark", 3.4, -2.6, radius=0.4),
    ],
    npcs=[
        npc("a5_bloxam", "human_peasant_m", "szgany", 0.6, 0.4, rot=180, name="Sam Bloxam",
            look="Sam Bloxam, carter, in a greasy waistcoat with a clay pipe in his teeth. He eyes my coat for what it might hold.", talk="a5_bloxam_talk"),
    ],
)

# ---- 10. house agents -------------------------------------------------------
LOC_DATA["a5_agent_office"] = dict(
    cells=[2, 2], interior=True, wall="plaster", floor="planks",
    ambient=AMBIENT["warm_day_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2]),
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[2.6, 2.0], spawns={"a5_london_street": [2.6, 2.0]},
    props=[
        prop("a5_ag_counter", "table_long", "ebony", 0, -1.4, name="Polished counter", radius=2.0, look="A polished counter with a brass hand-bell."),
        prop("a5_ag_safe", "chest", "ebony", 2.6, -3.0, name="The safe", radius=0.6, look="A black safe, bolted to the floor. A discreet agent keeps keys of let property here."),
        prop("a5_ag_shelf", "bookshelf", "dark", -2.4, -3.4, name="Deed boxes", radius=0.8, look="Deed boxes labelled with the names of London squares."),
        prop("a5_ag_map", "mirror", "default", 0.0, -3.7, name="Map of Piccadilly", radius=0.3, look="A framed map of the West End. Piccadilly is underscored in red, with the numbers 341-349 outlined."),
        prop("a5_ag_plant", "pine_small", "green", -3.2, 2.4, scale=0.3, name="Potted fir", radius=0.3, look="A potted fir, dusted twice daily."),
        prop("a5_ag_chair1", "chair", "blue", -2.0, 0.8, name="Client's chair", radius=0.4, look="A chair for clients who arrive with money."),
        prop("a5_ag_rug", "rug", "blue", 0, 1.0, radius=0.01),
        prop("a5_ag_door", "door", "ebony", 3.8, 2.0, rot=-90, name="Door to the street", radius=0.6, look="The street.", go="a5_london_street"),
    ],
    npcs=[
        npc("a5_agent_clerk", "human_peasant_m", "villager", 0, -2.6, rot=0, name="Mr. Candy's clerk",
            look="A young clerk in a high collar, nervous behind his counter, anxious to be discreet.", talk="a5_agent_talk"),
    ],
    on_enter=[dict(once=True, do=[{"say": "A discreet office on a quiet street. The agents sold 347 Piccadilly for cash to a foreign nobleman, and cash buys silence. A good name may buy back what cash has bought."}])],
)

# ---- 11. the Harkers' bedroom -----------------------------------------------
LOC_DATA["a5_mina_bedroom"] = dict(
    cells=[2, 2], interior=True, wall="plaster", floor="planks",
    ambient=AMBIENT["cold_interior"], camera=cam([2, 2]), lights=[dict(pos=[0, 2.6, -1], color="#ffb060", energy=2.0, range=9), dict(pos=[-2, 2.0, -3], color="#8aa6ff", energy=1.4, range=7)],
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[2.6, 2.0], spawns={"a5_asylum_library": [2.6, 2.0]},
    props=[
        prop("a5_bed", "bed", "blue", -1.6, -1.6, name="The Harkers' bed", radius=1.0, look="A wide bed, twisted sheets. It faces the window, and Mina has not slept in it."),
        prop("a5_bedroom_window", "fence", "default", -2.0, -3.6, name="Window with yellow blind", radius=0.8,
             look="A thick yellow blind covers the window. On a night of full moon it glows like a lantern.",
             use_item={
                 "garlic_wreath": [{"say": "I hung the garlic wreath over the window-frame. The reek of it fills the room."}, {"set": "a5_window_warded"}],
                 "crucifix": [{"say": "I set the crucifix upon the sill, facing outward. It is a small thing against so great an enemy."}, {"set": "a5_sill_crucifix"}],
             }, use_fail="That is no ward for a window."),
        prop("a5_bed_table", "table", "pale", 1.8, -2.4, name="Bedside table", radius=0.6, look="A Bible, a glass of water and Mina's hairpins."),
        prop("a5_bed_lamp", "lantern", "default", 1.8, -2.4, y=0.8, name="Gas-lamp", radius=0.2, look="The gaslight, turned low."),
        prop("a5_bed_trunk", "chest", "dark", 2.8, 0.4, name="Trunk", radius=0.6, look="Mina's trunk: dresses, writing-case, and a locket from Lucy."),
        prop("a5_bed_rug", "rug", "cream", 0.4, 0.6, radius=0.01),
        prop("a5_bed_chair", "chair", "green", -3.0, 1.4, rot=90, radius=0.4, name="Rocking chair", look="A chair where Mina sat with her mending, in the first days."),
        prop("a5_bed_door", "door", "dark", 3.8, 2.0, rot=-90, name="Door to the landing", radius=0.6, look="The door locks from within. It has a bolt.", go="a5_asylum_library"),
    ],
    npcs=[
        npc("a5_bed_harker", "human_harker", "harker", -0.6, -0.6, rot=0, name="Jonathan (in stupor)", cond="a5_night_attack&!a5_attack_done",
            look="Jonathan lies face upward in a deathlike lethargy, face flushed, breathing as a drowning man.", talk="a5_bed_harker"),
        npc("a5_count_bed", "human_dracula", "london", -1.0, -2.6, rot=0, name="Count Dracula", cond="a5_night_attack&!a5_attack_done",
            look="A tall thin man in black, face waxen, eyes red, a bloody scar upon his brow. Beside him, Mina on her knees, her mouth at his open breast.", talk="a5_attack_scene"),
        npc("a5_bed_mina", "human_mina", "mina", 0.2, -1.6, rot=-90, name="Mina (kneeling)", cond="a5_night_attack&!a5_attack_done",
            look="Mina in her nightdress, white and bloodied, on her knees at the Count's breast. Her eyes are open and there is no Mina in them."),
        npc("a5_bed_vh", "human_vanhelsing", "vh", 2.4, 0.8, rot=-90, name="Professor Van Helsing", cond="a5_night_attack&!a5_attack_done",
            look="The Professor with the Host raised in an envelope, face like a judge's.", talk="a5_attack_scene"),
        npc("a5_bed_arthur", "human_arthur", "lord", 2.6, 2.4, rot=-90, name="Arthur", cond="a5_night_attack&!a5_attack_done",
            look="Arthur with his crucifix thrust forward, trembling.", talk="a5_attack_scene"),
    ],
    on_enter=[dict(**{"if": "a5_night_attack"}, once=True, do=[
        {"say": "Mina's door is locked. Van Helsing says: 'Break it.' Quincey and I put our shoulders to it. It gives on the third heave. The room is full of a white mist, and in the mist, a tall thin figure."}])],
)

# ---- 12-14. houses ----------------------------------------------------------
def _house_box(n, label, boxes, x, z, flags, jr=None):
    return [
        prop(f"a5_hb_{n}", "coffin", "dark", x, z, scale=0.85, name=f"{label} ({boxes} boxes)", radius=0.9, cond=f"!a5_ster_{n}",
             look="Great boxes of foul earth with the Count's mark in chalk. The smell makes my head swim.",
             use_item={"host": [{"say": f"A crumb of the Host on each of the {boxes}: the earth hisses, and the smell is gone."}] + [{"set": f} for f in flags] + ([{"journal": jr}] if jr else []) + [{"set": f"a5_ster_{n}"}]},
             use_fail="Only the Sacred Host will unmake the Count's bed."),
        prop(f"a5_hc_{n}", "coffin", "pale", x, z, scale=0.85, name=f"Cleansed boxes ({boxes})", radius=0.9, cond=f"a5_ster_{n}",
             look="Dead, pale earth. This house is no longer the Count's."),
    ]


LOC_DATA["a5_piccadilly_house"] = dict(
    cells=[3, 2], interior=True, wall="plaster_dirty", floor="planks",
    ambient=AMBIENT["candle_interior"], camera=cam([3, 2]), lights=lights_warm([3, 2], n=3),
    walls=dict(north=["wall_window_4", "wall_4", "wall_window_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[4.6, 2.0], spawns={"a5_london_street": [4.6, 2.0]},
    props=_house_box("p1", "Boxes by the stair", 4, -3.0, -1.6, []) + _house_box("p2", "Boxes in the hall", 4, 0.4, -2.6, []) + [
        prop("a5_pic_desk", "table", "ebony", 3.4, -2.8, name="Desk", radius=0.9,
             look="A neat desk. Bills, receipts, a bundle of letters addressed to 'Count de Ville'. He pays in cash and writes in a very clear hand."),
        prop("a5_pic_papers", "book", "leather", 3.4, -2.8, y=0.8, name="Bundle of bills", radius=0.2,
             look="House-agent receipts, a cab-hire slip, a receipt for a steam launch's passage... All in cash, all in the one hand."),
        prop("a5_pic_sheet", "table", "dark", -3.4, 1.4, name="Covered furniture", radius=0.8, look="Dust-sheets over everything. The Count lives here as a ghost lives in a house."),
        prop("a5_pic_fire", "fireplace", "soot", -5.3, 0.6, rot=90, name="Cold fireplace", radius=0.9, look="A hearth with ash that has no warmth in it."),
        prop("a5_pic_mirror", "mirror", "default", 1.2, -3.7, name="Hall mirror", radius=0.3, look="A hall mirror. Something about it is wrong: it shows the room, and no figure that stands before it but ours."),
        prop("a5_pic_chair", "chair", "black", 2.4, 0.4, rot=180, radius=0.4, name="Chair", look="A chair set facing the door, the way a man sets a chair who expects visitors."),
        prop("a5_pic_lamp", "candelabra", "default", 0.2, 0.6, name="Candelabra", radius=0.3, look="Candles, burned down to the Count's liking: lit only for show."),
        prop("a5_pic_rug", "rug", "black", 0, 0.6, radius=0.01),
        prop("a5_pic_door", "door", "dark", 5.8, 2.0, rot=-90, name="Front door", radius=0.6, look="The front door onto Piccadilly. Its lock is fresh.", go="a5_london_street"),
    ],
    npcs=[
        npc("a5_harker_pic", "human_harker", "travel", 1.6, 2.4, rot=0, name="Jonathan Harker",
            look="Jonathan, white as paper, a knife in one hand and the Host's envelope in the other.", talk="a5_harker_pic"),
        npc("a5_vh_pic", "human_vanhelsing", "vh", -1.2, 2.0, rot=90, name="Professor Van Helsing",
            look="The Professor, calm, guiding.", talk="a5_vh_pic"),
        npc("a5_count_pic", "human_dracula", "london", 4.0, 0.0, rot=-90, name="Count Dracula", cond="a5_ster_p1&a5_ster_p2&!a5_count_fled",
            look="At the front door: tall, thin, a pale aquiline face. The Count, in the daylight, in a good coat, with a look of cold fury.", talk="a5_count_ambush"),
    ],
    on_enter=[dict(once=True, do=[{"protagonist": "harker"}, {"say": "The keys turned at the first attempt. The air inside is dead and sweet. This is the Count's town house and the Count is not at home. Not yet."}])],
)

LOC_DATA["a5_mile_end_house"] = dict(
    cells=[2, 2], interior=True, wall="plaster_dirty", floor="dirt",
    ambient=AMBIENT["cold_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2], n=2, energy=1.8),
    walls=dict(north=["wall_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[2.6, 2.0], spawns={"a5_london_street": [2.6, 2.0]},
    props=_house_box("me", "Boxes in the cellar", 6, -1.0, -1.8, ["a5_me_done"], "a5_j_mile_end") + [
        prop("a5_me_stair", "stairs", "stone_dark", -2.8, -3.2, name="Cellar stairs", radius=0.8, look="Steps down to the cellar. The smell comes up them."),
        prop("a5_me_barrel", "barrel", "dark", 2.4, -2.6, name="Empty barrel", radius=0.4, look="An empty barrel. Straw within, hollowed into a nest."),
        prop("a5_me_chair", "chair", "black", 2.0, 0.6, rot=-90, name="Broken chair", radius=0.4, look="A broken chair and a gas-bracket with no gas."),
        prop("a5_me_lamp", "lantern", "default", 0.6, 0.6, name="Dark lantern", radius=0.3, look="A dark lantern, lit and shuttered."),
        prop("a5_me_note", "book", "leather", -2.8, 1.2, y=0.0, name="Chalked tally", radius=0.3, look="The tally on the wall: six strokes. Six boxes, all here."),
        prop("a5_me_door", "door", "dark", 3.8, 2.0, rot=-90, name="Street door", radius=0.6, look="The door back to Chicksand Street.", go="a5_london_street"),
    ],
    npcs=[
        npc("a5_arthur_me", "human_arthur", "lord", 0.8, 2.0, rot=180, name="Arthur Holmwood",
            look="Lord Godalming, a lamp in one hand and the Count's keys in the other. He has not smiled since Lucy.", talk="a5_arthur_me"),
    ],
    on_enter=[dict(once=True, do=[{"protagonist": "arthur"}, {"say": "The Count's own key turned in a Mile End lock. A poor street, a cellar like a grave, and six pits of foul earth."}])],
)

LOC_DATA["a5_bermondsey_house"] = dict(
    cells=[2, 2], interior=True, wall="plaster_dirty", floor="dirt",
    ambient=AMBIENT["cold_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2], n=2, energy=1.8),
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[2.6, 2.0], spawns={"a5_london_street": [2.6, 2.0]},
    props=_house_box("b", "Boxes in the back room", 6, -1.0, -1.8, ["a5_b_done"], "a5_j_bermondsey") + [
        prop("a5_b_boards", "fence", "default", 1.6, -3.5, name="Boarded window", radius=0.8, look="The window is boarded. River-damp comes through the cracks."),
        prop("a5_b_sack", "barrel", "oak", 2.4, -1.4, name="Sacking", radius=0.5, look="Sacking, the sort used to pack and muffle."),
        prop("a5_b_chair", "chair", "black", 2.0, 1.0, rot=-90, radius=0.4, name="Stool", look="A stool left by the carters."),
        prop("a5_b_hook", "lantern", "default", -2.6, 1.0, name="Lamp", radius=0.3, look="A lamp with no oil in it; I refilled it."),
        prop("a5_b_door", "door", "dark", 3.8, 2.0, rot=-90, name="Street door", radius=0.6, look="The door to Jamaica Lane.", go="a5_london_street"),
    ],
    npcs=[
        npc("a5_quincey_b", "human_quincey", "texan", 0.8, 2.0, rot=180, name="Quincey Morris",
            look="Quincey, rifle in the crook of his arm. He keeps one eye on the stair and one on the door.", talk="a5_quincey_b"),
    ],
    on_enter=[dict(once=True, do=[{"protagonist": "quincey"}, {"say": "The last of the earth. Quincey Morris has put a bullet through worse in the Texas brush, but he has never been so careful about a door."}])],
)

# ----------------------------------------------------------------------------- dialogue
DIALOGUE = {}

# ---- arrival: the Harkers, the records --------------------------------------
DIALOGUE["a5_harker_talk"] = dict(start="n0", nodes={
    "n0": N("Jonathan Harker", "Dr. Seward. I would rather be of no use at all than of the use I am. But I will give you everything I have.", choices=[
        C("Mr. Harker, may I have your journal? Mrs. Harker will copy it.", "n_meet", cond="!a5_harker_met"),
        C("How is Mrs. Harker?", "n_mina"),
        C("The Carfax papers, Mr. Harker?", "n_papers", cond="a5_council_done&!a5_hawkins_given"),
        C("What do you make of this house?", "n_house"),
        LEAVE]),
    "n_meet": N("Jonathan Harker", "Here. Every shorthand page, from the Golden Krone to the castle chapel. Mina will read it, and I cannot. Not yet. Take it, Doctor, and let her put it in type.", next="n0",
                do=[{"set": "a5_harker_met"}, {"recruit": "harker"}, {"give": "a5_harker_journal"}, {"journal": "a5_j_harker_meet"}]),
    "n_mina": N("Jonathan Harker", "She is braver than I. She wants to be of use, always. I fear she will insist on being of too much.", next="n0"),
    "n_house": N("Jonathan Harker", "It is a good house, Doctor. But the wall at the end of your garden... I have seen that sort of wall before.", next="n0"),
    "n_papers": N("Jonathan Harker", "Mr. Hawkins left them to me. The deeds to Carfax, a bunch of heavy keys, and a letter I once carried to a Count. Here are the keys, and a letter of authority over Lord Godalming's seal. The carriers, the agents: they will talk to you, if you show them this.", next="n0",
                  do=[{"set": "a5_hawkins_given"}, {"give": "a5_carfax_keys"}, {"give": "a5_hawkins_letter"}]),
})

DIALOGUE["a5_mina_talk1"] = dict(start="n0", nodes={
    "n0": N("Mina Harker", "Doctor Seward, may I ask a great favour? I have a typewriter, and I have a head for order. Let me copy everything in the case. Jonathan's journal, your phonograph diary, my Whitby papers, the Professor's notes.", choices=[
        C("Mrs. Harker, I shall be glad of your help.", "n_task", cond="!a5_mina_met"),
        C("Where should I begin?", "n_where", cond="a5_mina_met"),
        C("What will you do with them?", "n_why"),
        LEAVE]),
    "n_task": N("Mina Harker", "Thank you. Here are my own papers: my Whitby diary and the cuttings from the Dailygraph. The rest I shall ask for as I need them. Bring them to the room off the library, and I will type each one. Then we shall see what they say together.", next="n0",
                do=[{"set": "a5_mina_met"}, {"give": "a5_whitby_cutting"}]),
    "n_where": N("Mina Harker", "Four things I need: Jonathan's journal, which he keeps; your phonograph cylinders, Doctor, which I think you keep locked; the Professor's memorandum; and my Whitby papers, which you have. And if Mr. Renfield keeps notes, I should like to see them too. The typewriter is in the little room west of the library.", next="n0"),
    "n_why": N("Mina Harker", "A story told in six voices is a story nobody has heard. Typed in order, it may speak.", next="n0"),
})

DIALOGUE["a5_vh_talk1"] = dict(start="n0", nodes={
    "n0": N("Professor Van Helsing", "Friend John! The mountain has come to Mahomet. The Harkers are here, and the work begins. Madam Mina has the eye of a lawyer and the heart of a nurse.", choices=[
        C("Professor, Mrs. Harker asks for your memorandum.", "n_memo", cond="!a5_vh_met"),
        C("What do you think of the case?", "n_think"),
        C("Is the Host safe in your bag?", "n_host"),
        LEAVE]),
    "n_memo": N("Professor Van Helsing", "Ah, yes! My memorandum. It tells of Miss Lucy, and of what I think, and of what I do not yet dare to think. Give it to her, and tell her to be gentle with my English.", next="n0",
                do=[{"set": "a5_vh_met"}, {"give": "a5_vh_memorandum"}]),
    "n_think": N("Professor Van Helsing", "There is a man, or a thing, in London. He has fifty boxes of earth, and we cannot kill him until we know where all of them lie. When Madam Mina has finished her typewriting, we shall be wiser. And then we hold the council.", next="n0"),
    "n_host": N("Professor Van Helsing", "Seven wafers, from my own priest in Amsterdam. Not a toy, not a charm. A thing to be used with care, and in faith. Do not waste a crumb.", next="n0"),
})

DIALOGUE["a5_clue_board"] = dict(start="n0", nodes={
    "n0": N("Mina Harker", "The whole story, in threads and pins. Each paper I have typed is pinned in its place, and I try to make them agree. What shall I ask the papers?", choices=[
        C("Where does the Count lie in London?", "n_carfax", cond="journal:a5_j_typed_harker&journal:a5_j_typed_cyl"),
        C("How did he come from Transylvania?", "n_whitby", cond="journal:a5_j_typed_whitby&journal:a5_j_typed_harker"),
        C("Why does Renfield know him?", "n_renf", cond="journal:a5_j_typed_cyl"),
        C("What can be done against him?", "n_rules", cond="journal:a5_j_typed_vh"),
        C("[Say the Count sleeps in Whitby churchyard]", "n_wrong1"),
        C("[Say Renfield is only a madman]", "n_wrong2"),
        C("[Fit all the threads together]", "n_done", cond="a5_dedu_carfax&a5_dedu_whitby&a5_dedu_renf&a5_dedu_rules"),
        LEAVE]),
    "n_carfax": N("Mina Harker", "Jonathan wrote that fifty boxes were brought from the castle chapel. The Doctor's cylinders say that Renfield screams loudest from the window that looks over the wall. And Mr. Hawkins sold the Count a house on the other side of that wall. He rests at Carfax, among his boxes, in the old chapel.", next="n0",
                  do=[{"set": "a5_dedu_carfax"}, {"journal": "a5_j_link_carfax"}]),
    "n_whitby": N("Mina Harker", "The Demeter put into Whitby in the storm with a dead crew and a great dog that leapt ashore. Jonathan's boxes were aboard her, fifty of them. The dog was the Count. Then the boxes went to London by rail, consigned to Billington of Whitby and forwarded by the carriers.", next="n0",
                  do=[{"set": "a5_dedu_whitby"}, {"journal": "a5_j_link_whitby"}]),
    "n_renf": N("Mina Harker", "Doctor Seward noted that Renfield grows violent when the night is clear, and eats the flies and sparrows with an increasing greed, 'to take their life into his own'. Each turn corresponds to the Count's visits. He is the Count's pawn, and may be the Count's door.", next="n0",
                do=[{"set": "a5_dedu_renf"}, {"journal": "a5_j_link_renfield"}]),
    "n_rules": N("Mina Harker", "He needs his native earth to rest. He cannot enter a house unasked. He fears the crucifix, garlic, the Host. If every box of earth is made unfit for him, he will have nowhere to lie by day. That is what we must do: find every box, and sanctify every one.", next="n0",
                 do=[{"set": "a5_dedu_rules"}]),
    "n_wrong1": N("Mina Harker", "Whitby is where Lucy first met him, but he does not rest there. There is no box in that churchyard. Look again at Jonathan's pages.", next="n0"),
    "n_wrong2": N("Mina Harker", "A madman, Doctor Seward calls him. But no madman keeps a record that matches the Count's movements. Look again at the cylinders.", next="n0"),
    "n_done": N("Mina Harker", "Yes. It is all one story, and now I can say it plainly: the Count lies at Carfax, in the fifty boxes, and the fifty boxes must be found and sanctified. I will take it to the Professor.", end=True,
                do=[{"set": "a5_records_done"}, {"journal": "a5_j_records_done"}, {"give": "a5_typed_transcript"}, {"protagonist": "seward"}]),
})

# ---- the council of war -----------------------------------------------------
DIALOGUE["a5_mina_talk2"] = dict(start="n0", nodes={
    "n0": N("Mina Harker", "I have given the Professor the typescript. He wishes us all to meet at the long table. I think it is a council, Doctor, and I think I am afraid that I shall be asked to leave it.", choices=[
        C("You have earned a seat, Mrs. Harker.", "n_seat"),
        C("Is there anything that troubles you?", "n_trouble", cond="a5_council_done"),
        LEAVE]),
    "n_seat": N("Mina Harker", "Thank you. I do not mean to be a burden. But if I am in the dark, I fear I shall be a greater one.", next="n0"),
    "n_trouble": N("Mina Harker", "A dream, only. A great white mist about the window. I woke, and the garlic wreath on the sill had curled, as though it, too, felt something. Pray set it at my window, Doctor, if you can find a reason.", next="n0"),
})

DIALOGUE["a5_council"] = dict(start="n0", nodes={
    "n0": N("Professor Van Helsing", "Friends! Madam Mina has done what no man of us could do. She has made the story one. Now I must tell you what I know, which is what none of you wish to hear. Sit, and listen, and do not laugh.", next="n_menu"),
    "n_menu": N("Professor Van Helsing", "Ask, and I will answer. You may ask in any order. When you know enough, we shall settle the matter of Madam Mina.", choices=[
        C("What is it that we hunt?", "n_powers"),
        C("How can he be harmed?", "n_weak"),
        C("Why does he need the boxes of earth?", "n_earth"),
        C("Can he enter this house?", "n_invite"),
        C("[Propose that Mrs. Harker be one of us]", "n_mina", cond="a5_lore_weak&a5_lore_earth"),
        C("[Leave the council for a moment]", end=True)]),
    "n_powers": N("Professor Van Helsing", "The Nosferatu does not die like other things. He has the strength of twenty men; he can command the wolf, the rat, the owl, the bat, the moth; he can come on moonlight as mist, as dust. He casts no shadow and no reflection. And he feeds on blood, and those who feed him become his.", next="n_menu", do=[{"set": "a5_lore_powers"}]),
    "n_weak": N("Professor Van Helsing", "In the daylight he is powerless. He cannot cross running water save at ebb or flow of the tide. The crucifix, the garlic, the wild rose, the Sacred Host: all these he must obey. And the stake through the heart and the sword to the head will give his body peace.", next="n_menu",
                do=[{"set": "a5_lore_weak"}, {"journal": "a5_j_rules"}]),
    "n_earth": N("Professor Van Helsing", "He is bound to his native earth. He must rest in it by day, or he withers. That is why he brought fifty boxes from Transylvania. If we can make each unfit for him, in sanctified ground he cannot lie. We find the boxes. We hallow the earth. It is a work of days, but it is a work we can do.", next="n_menu",
                 do=[{"set": "a5_lore_earth"}]),
    "n_invite": N("Professor Van Helsing", "He may not enter unless he is invited. That is why he needs a door. That is why a man like Renfield is dangerous. A lunatic does not know what an invitation is, and the Count will give him a reason to say yes.", next="n_menu",
                  do=[{"set": "a5_lore_invite"}]),
    "n_mina": N("Professor Van Helsing", "Madam Mina has read every paper we have. She has the best brain in the house. She is also the woman whose friend he took, and the woman whose husband he tormented. I think she has a right. But she is delicate. What do you say?", choices=[
        C("Agreed. We keep no secrets from her.", "n_end", do=[{"set": "a5_council_done"}, {"recruit": "mina"}, {"journal": "a5_j_council"}, {"journal": "a5_j_mina_joins"}]),
        C("Think of the danger to her.", "n_danger")]),
    "n_danger": N("Professor Van Helsing", "I have thought of it. But a woman kept in the dark by love is a woman in greater danger than a woman who knows. Think again.", next="n_mina"),
    "n_end": N("Professor Van Helsing", "Then we are six, and God help us. Tomorrow, to Carfax, the chapel, the boxes. Mr. Harker has the keys. Take the Host, take the crucifix, take the lamps. Let Lord Godalming's dogs go before us. And let us all swear, here, on this table, to put an end to this thing.", end=True),
})

DIALOGUE["a5_vh_talk3"] = dict(start="n0", nodes={
    "n0": N("Professor Van Helsing", "Friend John. We stand on the edge of a long road. Ask me what you will.", choices=[
        C("What do we do now, Professor?", "n_next"),
        C("How should the Host be used?", "n_host"),
        C("A ward for Mrs. Harker's room?", "n_ward"),
        C("I am out of the Host, Professor.", "n_refill", cond="!has:host"),
        LEAVE]),
    "n_next": N("Professor Van Helsing", "First Carfax, the chapel. There lie twenty-nine boxes, or so I judge. Each must be sanctified with a crumb of the Host. Go with the keys from Harker. Beware the rats: the Count is a master of them. Then, when we have counted what we found, we shall know how many are elsewhere. Then the carriers, the ledgers, the agents.", next="n0"),
    "n_host": N("Professor Van Helsing", "A crumb upon the earth in each box, with the true intent of the heart. There are five stacks in the chapel; I count one wafer for each. Do not waste it on one box when a stack will do. And remember, we have use for it elsewhere.", next="n0"),
    "n_ward": N("Professor Van Helsing", "Yes. The garlic wreath at the window, the crucifix on the sill. They are not proof against him, but they will tell us if he has come. Do it quietly. Madam Mina must not think we mistrust her sleep.", next="n0"),
    "n_refill": N("Professor Van Helsing", "Then take another. There is one more in the pyx. Be careful with it: they are not easily come by.", next="n0", do=[{"give": "host"}]),
})

DIALOGUE["a5_arthur_talk"] = dict(start="n0", nodes={
    "n0": N("Arthur Holmwood", "Seward. I have my terriers in the yard, a good rope, and a very bad conscience. I wish to end this thing, for Lucy's sake.", choices=[
        C("Lord Godalming, might I have a length of rope?", "n_rope", cond="!a5_got_rope"),
        C("How are you bearing up, Art?", "n_bear"),
        C("What of your dogs?", "n_dogs"),
        LEAVE]),
    "n_rope": N("Arthur Holmwood", "Take it. Good Sussex hemp. It has hauled many a fox from its earth.", next="n0", do=[{"give": "rope"}, {"set": "a5_got_rope"}]),
    "n_bear": N("Arthur Holmwood", "I think of her every day, and then I think of what she became, and I do not know which thought is worse. Mina is a fine woman. I shall protect her.", next="n0"),
    "n_dogs": N("Arthur Holmwood", "Three terriers, hard as nails. If the Count's rats come, they will meet something that bites back.", next="n0"),
})

DIALOGUE["a5_quincey_talk"] = dict(start="n0", nodes={
    "n0": N("Quincey Morris", "Doc. I have a Winchester in my room and a bowie knife under my coat. Say the word, and I'll shoot at anything that moves after dark.", choices=[
        C("Quincey, I am told you carry the purse.", "n_purse", cond="a5_council_done&!a5_got_sov"),
        C("What do you make of the Professor?", "n_vh"),
        C("What do you make of this whole business?", "n_biz"),
        LEAVE]),
    "n_purse": N("Quincey Morris", "Sure thing. Three sovereigns. Pay for a clerk's silence, a carter's thirst, and keep a spare. In this town gold talks louder than a judge.", next="n0",
                 do=[{"give": "a5_sovereign"}, {"give": "a5_sovereign"}, {"give": "a5_sovereign"}, {"set": "a5_got_sov"}]),
    "n_vh": N("Quincey Morris", "He's the first man I met who looks at a ghost the way my father looked at a bear. Calm. Practical. I'd follow him anywhere.", next="n0"),
    "n_biz": N("Quincey Morris", "I've seen more of the world than most. Never believed in witches. Now I believe in everything.", next="n0"),
})

# ---- Renfield ---------------------------------------------------------------
DIALOGUE["a5_renfield_plea"] = dict(start="n0", nodes={
    "n0": N("Renfield", "Doctor! Dr. Seward! I must speak with you. Not of the flies, nor the spiders, but of myself. Of what is coming.", choices=[
        C("What is troubling you, Renfield?", "n_plea", cond="!a5_renfield_warned"),
        C("Tell me again about the Master.", "n_master", cond="a5_renfield_warned"),
        C("[Show him the garlic wreath]", "n_garlic", cond="a5_renfield_warned&has:garlic_wreath"),
        LEAVE]),
    "n_plea": N("Renfield", "Let me go, Doctor! Let me go home. I am not safe here. He is near, nearer than ever, and he will want something. I cannot refuse him and live. I cannot obey him and be saved.", choices=[
        C("Tell me what you fear. I will listen.", "n_calm"),
        C("[Give him the chloral]", "n_calm", cond="has:chloral", do=[{"take": "chloral"}]),
        C("I cannot release you. Quiet, or I will call the attendants.", "n_refuse")]),
    "n_refuse": N("Renfield", "Then I am lost! Then I am his! No! NO!", end=True, do=[{"fight": "renfield_frenzy"}]),
    "n_calm": N("Renfield", "Thank you, Doctor. I am sorry. He promised me lives, thousands of them, if I would be his. He has come before, in the mist. He will come again. If he asks me in, I... I do not know what I shall do. Keep him from my window. Keep him from hers.", next="n0",
                do=[{"set": "a5_renfield_warned"}, {"journal": "a5_j_renfield_plea"}]),
    "n_master": N("Renfield", "He is no master of mine. He is a tyrant, a tempter. He showed me a swarm of rats. He said they would be mine, and I should have an endless supply of lives. All I had to do was say 'Come in.' I said nothing. Doctor, I said nothing.", choices=[
        C("Swear that you will not invite him.", "n_swear"),
        C("If he comes, will you call out?", "n_signal"),
        C("[Say nothing]", "n0")]),
    "n_swear": N("Renfield", "I swear it, Doctor. On the flies. On my own life, which is not much of a stake. But I am afraid I am a weak vessel.", next="n_master", do=[{"set": "a5_renfield_swore"}]),
    "n_signal": N("Renfield", "I will scream till the roof comes down. But I fear the roof is not the thing he needs. He needs a door, and I am one.", next="n_master", do=[{"set": "a5_renfield_signal"}]),
    "n_garlic": N("Renfield", "Keep it off me, Doctor! Not for me. For her window. Garlic the lady's window and there is not a cloud that can cross it. But he may find another way.", next="n0"),
})

DIALOGUE["a5_renfield_dying"] = dict(start="n0", nodes={
    "n0": N("Renfield", "Doctor... Doctor, my back... I cannot... lips...", choices=[
        C("[Moisten his lips with brandy]", "n_revive", cond="has:brandy", do=[{"take": "brandy"}, {"set": "a5_renfield_revived"}]),
        C("[Moisten his lips with water]", "n_revive", cond="has:water", do=[{"take": "water"}, {"set": "a5_renfield_revived"}]),
        C("Who did this, Renfield?", "n_who", cond="a5_renfield_revived"),
        C("[Wait]", end=True)]),
    "n_revive": N("Renfield", "That is better. Thank you, Doctor. I must tell you quickly. While I can.", next="n0"),
    "n_who": N("Renfield", "He came through the mist. I had not asked him in, but he came. And I knew what he meant to do, and I begged him to spare her. He laughed. Then he took me up and broke me against the floor like a child's toy. Doctor, he is going to the lady. Now. This minute.", choices=[
        C("Where? Which room?", "n_end")]),
    "n_end": N("Renfield", "The room... of the Harkers. Go! GO! Tell her... tell her I was not wholly his...", end=True,
               do=[{"set": "a5_renfield_died"}, {"journal": "a5_j_renfield_dead"}, {"set": "a5_alarm"}]),
})

DIALOGUE["a5_renfield_dead"] = dict(start="n0", nodes={
    "n0": N("Dr. Seward", "He is dead. Poor Renfield. He tried to be a man at the end. I will see to it that he is buried with the dignity he never had in life.", end=True),
})

DIALOGUE["a5_attendant_talk"] = dict(start="n0", nodes={
    "n0": N("Simmons", "Evenin', Doctor. He's been quiet today. Quiet's worse. He writes in that book of his, columns of numbers, day and night.", choices=[
        C("What numbers?", "n_num"),
        C("Has anyone visited him?", "n_vis"),
        LEAVE]),
    "n_num": N("Simmons", "Flies, sir. Spiders. Sparrows. He ticks each one off. Says they're the 'lives', and he's collecting a hundred for the one big life.", next="n0"),
    "n_vis": N("Simmons", "Not as I've seen, sir. But the window... I have heard a sound on it more than once. Like a bat at the glass.", next="n0"),
})

DIALOGUE["a5_night_prompt"] = dict(start="n0", nodes={
    "n0": N("Dr. Seward", "The tall clock stands at ten. The house is quiet, and quiet in this house is rarely rest.", choices=[
        C("[Retire for the night. Let the Count come if he will.]", "n_night", cond="a5_ledger_seen&a5_bloxam_done&a5_agent_done&a5_renfield_warned"),
        C("What have I yet to do?", "n_todo"),
        C("Not yet.", end=True)]),
    "n_todo": N("Dr. Seward", "Mina's records, the council, Carfax, the carriers, the trace to Piccadilly, and a word with Renfield. When all are done, we can rest for a night, and perhaps be wiser.", next="n0"),
    "n_night": N("Dr. Seward", "I locked the library, doused the lamps, and went to the wards. I do not know why. Something in the house had changed.", end=True,
                 do=[{"set": "a5_night_attack"}, {"card": "Night of 3 October. Purfleet.\n\nA scream in the dark. A pool of blood. The Count has come.", "goto": "a5_renfield_cell"}]),
})

# ---- grounds, Carfax --------------------------------------------------------
DIALOGUE["a5_gardener_talk"] = dict(start="n0", nodes={
    "n0": N("Old gardener", "Evenin', sir. That wall's older than the house. Folks say Carfax was a monastery, once, and the chapel's older still. Nobody goes in. Nobody comes out.", choices=[
        C("Has anyone been over the wall lately?", "n_wall"),
        C("The chapel door. Is there a key?", "n_key"),
        C("I need oil, wood and cloth for torches.", "n_supply"),
        LEAVE]),
    "n_wall": N("Old gardener", "I've seen lights, sir, at night. And I've seen a great dog sitting on the wall, with eyes like coals. I don't go that end any more.", next="n0"),
    "n_key": N("Old gardener", "The old caretaker, God rest him, was afeard of thieves. Hid the chapel key somewhere in the grounds where a dog could not dig and a child could not climb. Under a stone, or in a well, or maybe in a gatepost. Look about, sir.", next="n0"),
    "n_supply": N("Old gardener", "Oil's in the barrel by the shed. Ash-wood stacked by the stove. And Mrs. Billing's washing, I daresay, has a spare strip or two.", next="n0"),
})

DIALOGUE["a5_cabman_talk"] = dict(start="n0", nodes={
    "n0": N("Cabman", "Cab, sir? Town in the hour. Anywhere you like, sir, and no questions, save the fare.", choices=[
        C("Have you carried a foreign gentleman lately?", "n_foreign"),
        C("Not just yet.", end=True)]),
    "n_foreign": N("Cabman", "Aye, a tall thin gent, ancient, with a white moustache and a fine black coat. Carried a box under his arm like a child's coffin. Paid me in gold, he did, and never so much as blinked. Bit of a cold fish. The horse near bolted.", end=True),
})

DIALOGUE["a5_harker_cg"] = dict(start="n0", nodes={
    "n0": N("Jonathan Harker", "I sold him this place. Or helped to. I drew up the deed and sealed the packet that put the Count in the very house he dreamed of. Now I come as his enemy.", choices=[
        C("Mr. Harker, the chapel key?", "n_key"),
        C("Shall we go in?", "n_go"),
        LEAVE]),
    "n_key": N("Jonathan Harker", "The deeds mention that the old caretaker hid it in the park, near a stone feature of some kind: a post, a cross, a well. I have looked at the house; I should not like to go further without the chapel key in hand.", next="n0"),
    "n_go": N("Jonathan Harker", "Not before we have the key. And the Professor says rats may be abroad. Hold your lamps high, Doctor.", next="n0"),
})

DIALOGUE["a5_vh_chapel"] = dict(start="n0", nodes={
    "n0": N("Professor Van Helsing", "Here it is, friend John. Here is where he sleeps. The Count's house of dead earth. If we do this right, he will have no bed in England tonight.", choices=[
        C("What of the rats?", "n_rats"),
        C("How shall we cleanse the boxes?", "n_how"),
        C("I am out of the Host, Professor.", "n_refill", cond="!has:host"),
        LEAVE]),
    "n_rats": N("Professor Van Helsing", "The Count commands them. They will come when we move toward the earth. Hold your lamps, hold your ground, and keep the dogs close. They are only rats, friend John. Rats are afraid of men with lamps and resolve.", next="n0"),
    "n_how": N("Professor Van Helsing", "Five stacks, by my count. Six boxes in four of them, five in the last: twenty-nine in all. A crumb of the Host upon each stack, with the intent of the heart. It is enough. It will not be pleasant, and it will not be quick, but it is the work we came for.", next="n0"),
    "n_refill": N("Professor Van Helsing", "There is one more in the pyx. Take it, and God forgive me if I have miscounted.", next="n0", do=[{"give": "host"}]),
})

DIALOGUE["a5_harker_chapel"] = dict(start="n0", nodes={
    "n0": N("Jonathan Harker", "The count is easy, if we are patient. I have kept the tally from the castle in my head: fifty boxes, I counted them sleeping and wakeful, and I will never be wrong.", choices=[
        C("How many do we see here?", "n_info"),
        C("[Add up the stacks]", "n_count", cond="a5_ster_1&a5_ster_2&a5_ster_3&a5_ster_4&a5_ster_5&!a5_missing_21"),
        LEAVE]),
    "n_info": N("Jonathan Harker", "Five stacks. By the chalk on the wall, twenty-nine boxes. But there were fifty in the castle chapel, and fifty on the Demeter. So twenty-one are elsewhere.", next="n0"),
    "n_count": N("Jonathan Harker", "Twenty-nine boxes, and all are clean. The Count can no more lie here. But where are the other twenty-one? He has scattered them across London, I am sure of it. The carriers, Doctor. There is a ledger somewhere in London that remembers every box.", end=True,
                 do=[{"set": "a5_missing_21"}, {"journal": "a5_j_boxes29"}, {"protagonist": "harker"}]),
})

# ---- the London trail -------------------------------------------------------
DIALOGUE["a5_harker_street"] = dict(start="n0", nodes={
    "n0": N("Jonathan Harker", "A trail is a chain: one link leads to the next. Carriers, then the man who carried, then the man who sold the house. Where shall we begin?", choices=[
        C("Where do I start?", "n_start"),
        C("What have we learned?", "n_status"),
        C("What am I missing?", "n_missing"),
        LEAVE]),
    "n_start": N("Jonathan Harker", "Carter, Paterson & Co. They are the carriers, and the Hawkins letter will open the office door even if it will not open the ledger. Then, whoever carried the boxes. And lastly the house-agents. A man who buys a house in cash leaves a name somewhere.", next="n0"),
    "n_status": N("Jonathan Harker", "That depends what we have done. Smollet's ledger shows six boxes to Mile End and six to Bermondsey. Bloxam knows where the nine went, I suspect. And the house-agents must know whose house it is.", next="n0"),
    "n_missing": N("Jonathan Harker", "Keys, mostly. And patience. The Count paid cash for everything. A man who pays cash is a man who hates a written record, and I have never known one to leave none.", next="n0"),
})

DIALOGUE["a5_urchin_talk"] = dict(start="n0", nodes={
    "n0": N("Street boy", "Penny for a poor lad, sir? I know every court and alley between here and the river.", choices=[
        C("[Show Mr. Smollet's scrap of paper]", "n_scrap", cond="a5_scrap&!a5_decoded"),
        C("Do you know a white-moustached old gentleman?", "n_old"),
        LEAVE]),
    "n_scrap": N("Street boy", "Coo, sir. 'Sam Bloxam, Korkrans, 4, Poters Cort, Bartel Street, Walworth.' Who writes like that? It don't make sense. What's it supposed to say?", choices=[
        C("Poter's Cort, off Bartel Street.", "n_wrong"),
        C("Potter's Court, off Bartel Street, Walworth: Corcoran's, number four.", "n_right"),
        C("Sam Bloxam is a made-up name.", "n_wrong2")]),
    "n_wrong": N("Street boy", "Never heard of no Poter. Try again, guv.", next="n_scrap"),
    "n_wrong2": N("Street boy", "Sam Bloxam's real enough. Drinks at the 'Are and 'Ounds. It's the writing that's daft.", next="n_scrap"),
    "n_right": N("Street boy", "That's it! Potter's Court, Corcoran's, down the alley by the barrel, sir. Sam Bloxam lodges there. Good luck, and a penny would not go amiss.", end=True, do=[{"set": "a5_decoded"}]),
    "n_old": N("Street boy", "A gent with a white moustache and a hat pulled low? Walked up to the big stone house with the bow window in Piccadilly, he did. Carried a box up the steps himself. One hand. Gave me a shiver.", next="n0"),
})

DIALOGUE["a5_smollet_talk"] = dict(start="n0", nodes={
    "n0": N("Mr. Smollet", "Business hours, sir. State your errand. I can't show our book to every gentleman who walks in off the street.", choices=[
        C("I am inquiring after fifty boxes of earth, consigned to Carfax.", "n_inq", cond="!a5_ledger_seen"),
        C("About that ledger entry...", "n_after", cond="a5_ledger_seen"),
        LEAVE]),
    "n_inq": N("Mr. Smollet", "Boxes of earth, is it? Aye, we carried the like. But it's a confidential book, sir. I'd need good reason.", choices=[
        C("[Slip him a sovereign]", "n_pay", cond="has:a5_sovereign"),
        C("[Show him the letter of authority]", "n_letter", cond="has:a5_hawkins_letter"),
        C("[Threaten to fetch a constable]", "n_police")]),
    "n_letter": N("Mr. Smollet", "A letter's a handsome thing, sir. But a letter's not a ledger. My memory has been poor of late. A bit of grease might clear it.", next="n_inq"),
    "n_police": N("Mr. Smollet", "Constable? On what charge? Hauling boxes? Be off with you, sir, or I'll fetch him myself.", next="n_inq"),
    "n_pay": N("Mr. Smollet", "Ah, well. Sovereign talks, sir. Here: I'll copy the entry for you. Six boxes to 197 Chicksand Street, Mile End New Town. Six more to Jamaica Lane, Bermondsey. And the nine that went to a gentleman in Piccadilly, that's Sam Bloxam's work. Here's his direction. My own spelling is a little on the poor side, mind.", next="n0",
               do=[{"give": "a5_ledger_copy"}, {"set": "a5_ledger_seen"}, {"set": "a5_scrap"}, {"journal": "a5_j_ledger"}]),
    "n_after": N("Mr. Smollet", "I have told you all I know, sir. And I'd thank you not to mention my name outside.", next="n0"),
})

DIALOGUE["a5_snelling_talk"] = dict(start="n0", nodes={
    "n0": N("Thomas Snelling", "Zzz... Eh? Who? Boxes? Aye, boxes. Dirty. Heavy. Smelt like a churchyard. The old gent that bought 'em lifted one hisself. One-handed. I'm tellin' ye, sir, I'm a sober man.", choices=[
        C("Where did he take them?", "n_where"),
        LEAVE]),
    "n_where": N("Thomas Snelling", "Chicksand Street, Mile End... and a place in Bermondsey... and that big stone house in Piccadilly. Ask Sam Bloxam. He had the cart. Zzz...", end=True),
})

DIALOGUE["a5_bloxam_talk"] = dict(start="n0", nodes={
    "n0": N("Sam Bloxam", "Who wants Sam Bloxam? If it's about that Hackney debt...", choices=[
        C("[Offer a sovereign]", "n_tell", cond="has:a5_sovereign&!a5_bloxam_done"),
        C("Tell me about the nine boxes.", "n_cold", cond="!a5_bloxam_done"),
        C("The house in Piccadilly...", "n_again", cond="a5_bloxam_done"),
        LEAVE]),
    "n_cold": N("Sam Bloxam", "Nine boxes? Don't know what you mean, guv. Memory's gone a bit foggy. Might come back with a bit of coin.", next="n0"),
    "n_tell": N("Sam Bloxam", "Well, now. Nine boxes of earth, heavy as sin. An old gent with a white moustache, strong as a horse, took us to a stone house with a bow window and high steps. Near a big white church, beyond the Junior Constitutional Club. A torn 'To Let' board. I forget the number, guv, but a groom in the mews will know it. Number 347, I'd say, but don't swear to it.", next="n0",
               do=[{"set": "a5_bloxam_done"}, {"journal": "a5_j_bloxam"}]),
    "n_again": N("Sam Bloxam", "I've told you all. Go careful. That old gent was no ordinary old gent.", next="n0"),
})

DIALOGUE["a5_agent_talk"] = dict(start="n0", nodes={
    "n0": N("Mr. Candy's clerk", "Good day, sir. How may we serve you?", choices=[
        C("I am enquiring after 347 Piccadilly.", "n_picc", cond="!a5_agent_done"),
        C("About the Piccadilly keys...", "n_after", cond="a5_agent_done"),
        LEAVE]),
    "n_picc": N("Mr. Candy's clerk", "I am afraid our clients' affairs are strictly confidential, sir.", choices=[
        C("[Show Lord Godalming's letter of authority]", "n_letter", cond="has:a5_hawkins_letter"),
        C("[Offer a sovereign]", "n_bribe", cond="has:a5_sovereign"),
        C("[Bluster]", "n_bluster")]),
    "n_bribe": N("Mr. Candy's clerk", "Sir! This is a respectable house. Please put that away.", next="n_picc"),
    "n_bluster": N("Mr. Candy's clerk", "I must ask you to leave, sir, or I shall call Mr. Candy.", next="n_picc"),
    "n_letter": N("Mr. Candy's clerk", "Lord Godalming? Of Ring? Oh, I beg your pardon, sir. The buyer was a Count de Ville, who paid in cash and wished the house kept quiet. A foreigner, very old, very strong. I would not have liked to cross him. Here are the keys, sir. And I would say, sir: if you do mean to enter, take company.", next="n0",
                 do=[{"give": "a5_agent_keys"}, {"set": "a5_agent_done"}, {"journal": "a5_j_agent"}]),
    "n_after": N("Mr. Candy's clerk", "You have the keys, sir. I hope you find what you seek.", next="n0"),
})

# ---- the night --------------------------------------------------------------
DIALOGUE["a5_bed_harker"] = dict(start="n0", nodes={
    "n0": N("Dr. Seward", "Jonathan lies on his back, face flushed, breathing heavily like one in a drugged sleep. I shake him. Nothing.", end=True),
})

DIALOGUE["a5_attack_scene"] = dict(start="n0", nodes={
    "n0": N("Dr. Seward", "In the moonlight through the yellow blind: a tall, thin man in black, his face waxen, his eyes red. His left hand grips both of Mina's wrists. His right holds her head against his open breast, where a bleeding wound drips. Her mouth is at it. On the bed, Jonathan lies in a stupor.", choices=[
        C("[Raise the crucifix and advance]", "n_cruc", cond="has:crucifix"),
        C("[Notice the garlic wreath]", "n_wreath", cond="a5_window_warded"),
        C("[Rush the Count]", "n_rush")]),
    "n_wreath": N("Dr. Seward", "The wreath lies trampled on the floor. It did not keep him out. Only an invitation could, and he had that already.", next="n0"),
    "n_rush": N("Count Dracula", "Fools. Do you think you can strike me? I who have commanded armies when your fathers were babes?", next="n0"),
    "n_cruc": N("Count Dracula", "You think yourselves so wise, all of you. Your girls are mine, and through them you, and others, shall be mine. The sheep are in my hands. Yet before I go, I shall have her again; and again.", next="n_host"),
    "n_host": N("Professor Van Helsing", "The Count drops the girl and turns on us. He is a hawk, a stoat, a wolf. Van Helsing steps forward with an envelope. 'Back!'", choices=[
        C("[Hold out the Sacred Host]", "n_cower", cond="has:host", )]),
    "n_cower": N("Dr. Seward", "He cowers. Further and further we advance with crucifixes lifted. A bar of moonlight crosses his face and he grows grey, then thin, then a pale mist under the door. We hear the whining of the wind. He is gone.", next="n_mina"),
    "n_mina": N("Mina Harker", "Unclean! Unclean! Even the Almighty shuns my polluted flesh! I must bear this shame upon my forehead until the Judgment Day!", next="n_brand"),
    "n_brand": N("Professor Van Helsing", "Madam Mina. This is the Sacred Host. Forgive me.", end=True,
                 do=[{"set": "a5_attack_done"}, {"journal": "a5_j_attack"}, {"journal": "a5_j_unclean"}, {"protagonist": "mina"},
                     {"say": "The Wafer touched her forehead and burned like a hot iron. A red scar, where it touched. The Count has marked her; the Host has marked her too, and she bears both."}]),
})

# ---- after the attack, boxes, trance ---------------------------------------
DIALOGUE["a5_mina_talk3"] = dict(start="n0", nodes={
    "n0": N("Mina Harker", "Doctor Seward. I am awake, and I am whole, and I am afraid to look in a glass.", choices=[
        C("How do you feel, Mrs. Harker?", "n_bond", cond="!a5_bond_talk"),
        C("May I see the mark?", "n_mark"),
        C("Is there anything I can do?", "n_help"),
        LEAVE]),
    "n_bond": N("Mina Harker", "I feel him. Like a cold wind with a taste. When the sun rises or sets I seem able to follow him a little way, wherever he is. The Professor says it may be our only road to him. I pray God it is not also his to me.", next="n0",
                do=[{"set": "a5_bond_talk"}, {"journal": "a5_j_bond"}]),
    "n_mark": N("Mina Harker", "I would rather you did not. It is the size of a florin, red as a coal. Jonathan weeps when he looks at it. The Professor says it will fade when the Count dies, and not before.", next="n0"),
    "n_help": N("Mina Harker", "Finish the boxes. Every one you destroy is a day gained. And promise me that you will not keep me in the dark, whatever the Professor thinks best.", next="n0"),
})

DIALOGUE["a5_vh_talk4"] = dict(start="n0", nodes={
    "n0": N("Professor Van Helsing", "Friend John, he has tasted her, and she him. That is a link we cannot cut. But it may serve us. He is not omnipotent. He fears us, you have seen it.", choices=[
        C("What now, Professor?", "n_next"),
        C("We need more of the Host.", "n_host", cond="!a5_host_refill_given"),
        C("I am out of the Host, Professor.", "n_refill", cond="!has:host"),
        C("How is Madam Mina?", "n_mina"),
        LEAVE]),
    "n_next": N("Professor Van Helsing", "Piccadilly, with the keys that Harker got from the agents. Nine boxes, or eight, if he has taken one. Then, if the Count's keys come into our hands, the houses in Mile End and Bermondsey. We shall find him leaving, or arriving. Either way, we strike.", next="n0"),
    "n_host": N("Professor Van Helsing", "I wrote to Amsterdam as soon as I arrived. This morning my priest sent four more. Piccadilly will need two, Mile End one, Bermondsey one. Take them, friend John.", next="n0",
                do=[{"set": "a5_host_refill_given"}, {"give": "host"}, {"give": "host"}, {"give": "host"}, {"give": "host"}]),
    "n_refill": N("Professor Van Helsing", "Then take another. There is one more in the pyx.", next="n0", do=[{"give": "host"}]),
    "n_mina": N("Professor Van Helsing", "She is stronger than she knows. She asked me to keep nothing from her, and I shall obey, God help me. But she must rest, friend John. She must rest.", next="n0"),
})

DIALOGUE["a5_harker_pic"] = dict(start="n0", nodes={
    "n0": N("Jonathan Harker", "Eight boxes, Professor says. The ninth the Count has taken, or perhaps he sleeps in it. We sanctify the two stacks, and we wait. If he comes, he must come through us.", choices=[
        C("How do you feel, Jonathan?", "n_feel"),
        LEAVE]),
    "n_feel": N("Jonathan Harker", "I have not slept since the night he took her. I do not mean to sleep until he is dead.", next="n0"),
})

DIALOGUE["a5_vh_pic"] = dict(start="n0", nodes={
    "n0": N("Professor Van Helsing", "Two stacks, friend. A crumb on each. Then we wait at the door. He comes here to see to his property, and we shall be waiting.", choices=[
        C("[Hang the garlic wreath on the front door]", "n_wreath", cond="has:garlic_wreath&!a5_picc_warded"),
        C("I am out of the Host.", "n_refill", cond="!has:host"),
        LEAVE]),
    "n_wreath": N("Professor Van Helsing", "Good. He will think twice at the threshold. Perhaps once is enough for us.", next="n0", do=[{"set": "a5_picc_warded"}]),
    "n_refill": N("Professor Van Helsing", "Take another. We cannot be short of it.", next="n0", do=[{"give": "host"}]),
})

DIALOGUE["a5_count_ambush"] = dict(start="n0", nodes={
    "n0": N("Count Dracula", "So. The sheep have found the wolf's lair. You are clever, you English, with your keys and your agents. But you came too late, and you leave too soon.", choices=[
        C("[Stand in the doorway with the crucifix]", "n_stand", cond="has:crucifix"),
        C("[Rush him with the knife]", "n_rush")]),
    "n_stand": N("Count Dracula", "Do you think a bauble stops me? I have lived when your fathers' fathers were dust. Stand aside!", end=True, do=[{"fight": "a5_picc_ambush"}]),
    "n_rush": N("Count Dracula", "Ha! Hold him, men! I'll not fight in a doorway.", end=True, do=[{"fight": "a5_picc_ambush"}]),
})

DIALOGUE["a5_arthur_me"] = dict(start="n0", nodes={
    "n0": N("Arthur Holmwood", "The Count's key opened the Mile End lock like butter. Six boxes, in a coal-cellar. I thought I should feel triumphant. I only feel tired.", choices=[
        C("A crumb on the stack, then?", "n_how"),
        LEAVE]),
    "n_how": N("Arthur Holmwood", "One wafer, one stack. Do it with the right heart, the Professor says. I shall try to think of Lucy.", next="n0"),
})

DIALOGUE["a5_quincey_b"] = dict(start="n0", nodes={
    "n0": N("Quincey Morris", "Last of the lot, Doc. Last house, last stack. Then there's only the one with the Count.", choices=[
        C("[Report: the houses are clean and the Count has fled]", "n_done", cond="a5_me_done&a5_b_done&a5_count_fled&!a5_boxes_done"),
        C("How many boxes remain?", "n_count"),
        LEAVE]),
    "n_count": N("Quincey Morris", "Twenty-nine at Carfax, eight at Piccadilly, six at Mile End, six here: forty-nine. One left. The Count's got it somewhere, and himself in it.", next="n0"),
    "n_done": N("Quincey Morris", "Forty-nine down, one to go. The sun is setting. Let's get back to Purfleet; Mrs. Harker will be waiting.", end=True,
                do=[{"set": "a5_boxes_done"}, {"protagonist": "mina"},
                    {"card": "Evening of 4 October. Purfleet.\n\nForty-nine boxes cleansed. One remains.", "goto": "a5_asylum_library"}]),
})

DIALOGUE["a5_vh_trance"] = dict(start="n0", nodes={
    "n0": N("Professor Van Helsing", "Madam Mina, you said the link may serve us. Let us try it. At sunrise and at sunset the Count is at his weakest and his closest. Will you let me?", choices=[
        C("[Begin the sunrise trance]", "n_t1", cond="!a5_trance1"),
        C("[Wait for sunset]", "n_t2", cond="a5_trance1&!a5_trance2"),
        C("What does she mean, Professor?", "n_decode", cond="a5_trance2"),
        LEAVE]),
    "n_t1": N("Mina Harker", "Darkness. Everything is dark... lapping water... a creaking of wood... a rope drawn taut... above me, feet. Cold. So cold.", next="n0",
              do=[{"card": "Sunrise, 5 October. Purfleet."}, {"set": "a5_trance1"}, {"journal": "a5_j_trance1"}]),
    "n_t2": N("Mina Harker", "A bell, dull and distant. Hawsers. Men calling, and a cry from the deck. 'We are going, we are going.' He is awake, Professor. He knows I am listening. He is so very near, and so very far.", next="n0",
              do=[{"card": "Sunset, 5 October. Purfleet."}, {"set": "a5_trance2"}, {"journal": "a5_j_trance2"}]),
    "n_decode": N("Professor Van Helsing", "Think, friend. Water lapping. Wood creaking. A rope pulled taut. Feet above. A bell. 'We are going.' What is the Count's box? Where is he?", choices=[
        C("He lies in the Bermondsey cellar still.", "n_wrong1"),
        C("He is aboard a ship. We must learn her name: wire Lloyd's.", "n_name", cond="journal:a5_j_trance1&journal:a5_j_trance2"),
        C("The Czarina Catherine, bound for Varna.", "n_ship", cond="journal:a5_j_trance2&has:a5_lloyds_telegram")]),
    "n_wrong1": N("Professor Van Helsing", "No. Bermondsey has no lapping water, and the box there is clean. Think of the sounds again.", next="n_decode"),
    "n_name": N("Professor Van Helsing", "Good. Lord Godalming has the ear of Lloyd's. A telegram will come. When it does, tell me.", next="n0", do=[{"set": "a5_wired_lloyds"}]),
    "n_ship": N("Professor Van Helsing", "Yes. The telegram says the Czarina Catherine cleared the Thames this morning for Varna. Water, wood, rope, the bell: a ship, and one eastbound. He is running home with his last box. Lord God, what a woman you are, Madam Mina.", end=True,
                do=[{"set": "a5_ship_known"}, {"journal": "a5_j_ship"}, {"give": "a5_ship_notes"}]),
})

DIALOGUE["a5_mina_trance"] = dict(start="n0", nodes={
    "n0": N("Mina Harker", "The Professor wants me to try the link. I am afraid, but I would rather be afraid and useful than safe and idle.", choices=[
        C("You are braver than any of us, Mrs. Harker.", "n_brave"),
        C("What does it feel like?", "n_feel"),
        LEAVE]),
    "n_brave": N("Mina Harker", "I do not feel brave. But it helps to be told.", next="n0"),
    "n_feel": N("Mina Harker", "Like standing at the edge of a dark river, with the other bank hidden. I can hear it, but I cannot see.", next="n0"),
})

# ---- chapter 24: the plan and the parting -----------------------------------
DIALOGUE["a5_vh_plan"] = dict(start="n0", nodes={
    "n0": N("Professor Van Helsing", "The Czarina Catherine: a slow ship to Varna. We go by rail to Paris, thence the Orient Express to Varna, and wait on the quay for the ship to come in. We shall be there before her.", choices=[
        C("Who goes?", "n_who"),
        C("And Madam Mina?", "n_mina"),
        C("[Agree to the plan]", "n_agree", cond="!a5_plan_made"),
        C("[Check the kit]", "n_kit", cond="a5_plan_made&!a5_packed"),
        C("I am out of the Host, Professor.", "n_refill", cond="!has:host"),
        LEAVE]),
    "n_who": N("Professor Van Helsing", "Lord Godalming, Mr. Morris, Dr. Seward, Mr. Harker, and myself. Five good men, and a ship's passage of rope, wood, and faith.", next="n0"),
    "n_mina": N("Professor Van Helsing", "She is not to come. Not this time. She has done more than any of us, and the Count has her link. If she is near him, he has her. If she is far, she is free. We shall tell her this at the last, for her own peace.", choices=[
        C("She will not agree to be left out.", "n_dissent"),
        C("It is a hard thing, but for her safety.", "n0")]),
    "n_dissent": N("Professor Van Helsing", "She has taken one wound for us. I will not let her take another. We say nothing of the plan, friend John. Nothing.", next="n0"),
    "n_agree": N("Professor Van Helsing", "Good. Then it is settled. I will make out the passage. Let each man gather what he needs.", next="n0",
                 do=[{"set": "a5_plan_made"}, {"journal": "a5_j_plan"}, {"give": "host"}, {"give": "host"}, {"give": "host"}]),
    "n_kit": N("Professor Van Helsing", "Crucifix, stake, hammer, Host. Without these we go to our graves. Do you have them all?", choices=[
        C("Crucifix, Host, stake, hammer: all here.", "n_packed", cond="has:crucifix&has:host&has:stake&has:hammer"),
        C("Not yet.", "n0")]),
    "n_packed": N("Professor Van Helsing", "Then we are ready. Go and speak with Madam Mina. She is waiting. And friend John, be kind.", next="n0", do=[{"set": "a5_packed"}]),
    "n_refill": N("Professor Van Helsing", "Take another. We must not be short of it where we go.", next="n0", do=[{"give": "host"}]),
})

DIALOGUE["a5_mina_farewell"] = dict(start="n0", nodes={
    "n0": N("Mina Harker", "They have decided. I overheard the Professor with Lord Godalming. They mean to go without me. It is for my safety, they say, and I have not the heart to refuse. And I do not mean to stay behind.", choices=[
        C("Let them go. I shall wait, and watch the link.", "n_go", cond="a5_plan_made&a5_packed"),
        C("[Argue with the Professor]", "n_arg"),
        C("Not yet. Let me think.", end=True)]),
    "n_arg": N("Professor Van Helsing", "Madam Mina, I beg you. It is for your sake. The Count has the claim on your blood. We go to cut it. Stay safe here.", next="n0"),
    "n_go": N("Mina Harker", "They stand in the hall with their kits, the five of them: Jonathan, Arthur, Quincey, Dr. Seward, and the Professor in his shabby coat. I kiss Jonathan. I press the Professor's hand. They go. I watch the cab out of sight, and feel the line in my blood quiver, as though the Count himself were looking back.", end=True,
              do=[{"journal": "a5_j_left_out"},
                  {"card": "5 October, evening.\n\nThe party leaves Charing Cross for Paris, the Orient Express, and Varna, to wait for the Czarina Catherine. Mina remains behind.",
                   "goto": "a6_varna_quay"}]),
})

# ----------------------------------------------------------------------------- combat
ENEMIES_EXTRA = {
    "a5_thrall": dict(name="Hired thrall", model="human_peasant_m", hp=14, spd=5, dmg=[2, 4], acc=62, eva=5, tags=["human"], flee_at=0.4,
                      book="The Count's hired men, ch.22"),
}

ENCOUNTERS_EXTRA = {
    "a5_picc_ambush": dict(name="The Count at the door", time="dusk", enemies=["a5_thrall", "a5_thrall", "bat"], flee_ok=True,
                           intro="The door bursts. The Count is there, a hired ruffian at each shoulder and a bat at his collar. 'Stand aside!'",
                           win="The hirelings fall. The Count has leapt through the gap like a cat through rats.", location=""),
}

_RATS_AFTER = [{"journal": "a5_j_rats"}]
ENCOUNTER_HOOKS = {
    "carfax_rats": dict(
        on_win=[{"journal": "a5_j_rats"}, {"say": "The terriers go in like furies. The last rat is a blur and a yelp, and the chapel is still. The boxes of earth lie bare in the lamplight."}],
        on_lose=[{"say": "We are driven back, bitten and bruised, past the door. Arthur's dogs hold the swarm at bay. The lamps are re-lit; we may try again."}],
        on_flee=[{"say": "We fall back to the door and shut it. The rats mass inside, a rustling tide. We will go in again with lamps held higher."}]),
    "renfield_frenzy": dict(
        on_win=[{"set": "a5_renfield_warned"}, {"journal": "a5_j_renfield_plea"},
                {"say": "Renfield lies quiet at last, panting. 'Doctor, I am sorry. He is near. He will come for me, and for her. Keep him from the windows.'"}],
        on_lose=[{"set": "a5_renfield_warned"}, {"journal": "a5_j_renfield_plea"},
                 {"say": "He flings me against the wall and then, as suddenly, sobs. Simmons restrains him. 'Doctor... He is near. Keep him from the windows.'"}],
        on_flee=[{"set": "a5_renfield_warned"}, {"journal": "a5_j_renfield_plea"},
                 {"say": "I retreat to the door as he cries after me, 'He is near! Keep him from the windows!' It is the sanest thing he has said."}]),
    "a5_picc_ambush": dict(
        on_win=[{"give": "a5_counts_keys"}, {"give": "a5_counts_money"}, {"set": "a5_count_fled"}, {"journal": "a5_j_piccadilly"}, {"journal": "a5_j_keys_money"},
                {"say": "The Count is gone. In the scuffle Jonathan's knife slit his coat from shoulder to waist, and a rain of gold and notes poured onto the hall floor, with a heavy bunch of keys. He leapt through us like a cat through rats, and through the open door."}],
        on_lose=[{"give": "a5_counts_keys"}, {"give": "a5_counts_money"}, {"set": "a5_count_fled"}, {"journal": "a5_j_piccadilly"}, {"journal": "a5_j_keys_money"},
                 {"say": "We are flung aside, but Jonathan's knife has found the Count's coat. Gold and a bunch of keys tumble on the floor as the Count leaps over us and out of the door."}],
        on_flee=[{"give": "a5_counts_keys"}, {"give": "a5_counts_money"}, {"set": "a5_count_fled"}, {"journal": "a5_j_piccadilly"}, {"journal": "a5_j_keys_money"},
                 {"say": "We give ground, and in the confusion the Count slashes through us and is gone. In the hall: a bunch of keys and a purse of gold and notes, torn loose by Jonathan's knife."}]),
}

PALETTES = {
    "a5_asylum_library": [dict(wall="plaster", floor="planks", wood="dark", cloth="blue"),
                          dict(wall="plaster_dirty", floor="planks", wood="ebony", cloth="green"),
                          dict(wall="plaster", floor="planks", wood="oak", cloth="red")],
    "a5_typing_room": [dict(wall="plaster", floor="planks", wood="pale", cloth="green"), dict(wall="plaster", floor="planks", wood="oak", cloth="cream")],
    "a5_carfax_grounds": [dict(floor="dirt", tree="grey"), dict(floor="grass", tree="grey")],
    "a5_carfax_chapel": [dict(wall="stone_mossy", floor="stone_dark"), dict(wall="stone_dark", floor="cobble")],
    "a5_carters_office": [dict(wall="plaster_dirty", floor="planks", wood="dark", cloth="black"), dict(wall="plaster", floor="planks", wood="oak", cloth="red")],
}

