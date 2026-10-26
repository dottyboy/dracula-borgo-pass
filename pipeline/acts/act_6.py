"""ACT VI - The Hunt (novel chapters XXV-XXVII and the closing Note): Varna, Galatz, the rivers, the Borgo Pass, the castle, the sunset."""
from dsl import *


# ------------------------------------------------------------------ helpers
def deco(id, asset, variant, x, z, rot=0, scale=1.0, y=0.0):
    """Pure decoration (not clickable)."""
    return prop(id, asset, variant, x, z, rot=rot, scale=scale, y=y, radius=0.01)


def N(speaker, text, **kw):
    return dict(speaker=speaker, text=text, **kw)


def C(text, next=None, **kw):
    d = dict(text=text)
    if next:
        d["next"] = next
    d.update(kw)
    return d


def indoor(cells, wall, floor, walls, mood="candle", **kw):
    amb = {"candle": AMBIENT["candle_interior"], "day": AMBIENT["warm_day_interior"], "cold": AMBIENT["cold_interior"],
           "crypt": AMBIENT["crypt"]}[mood]
    lights = lights_warm(cells, n=3 if mood != "crypt" else 2, energy=2.4 if mood in ("candle", "day") else 1.8)
    d = dict(cells=cells, interior=True, wall=wall, floor=floor, ambient=amb, camera=cam(cells), lights=lights, walls=walls)
    d.update(kw)
    return d


SUNSET_LIGHTS = [dict(pos=[10, 3.0, -4], color="#ff7a3a", energy=3.6, range=34), dict(pos=[-5, 5, 3], color="#9a8ad0", energy=1.3, range=22)]


def outdoor(cells, mood, floor="cobble", wall="dirt", **kw):
    if mood == "day":
        amb, lights, extra = AMBIENT["day_exterior"], lights_day(), {}
    elif mood == "fog":
        amb, lights, extra = AMBIENT["sea_fog"], lights_day(2.4), {}
    elif mood == "dusk":
        amb, lights, extra = AMBIENT["dusk_exterior"], lights_warm(cells, n=1, energy=2.0) + lights_moon(1.6), {}
    elif mood == "sunset":
        amb, lights, extra = dict(color="#7a5058", energy=1.15, fog="#4a2a30"), SUNSET_LIGHTS, {}
    elif mood == "storm":
        amb, lights, extra = AMBIENT["storm_exterior"], lights_day(1.8), {}
    else:   # night
        amb, lights, extra = AMBIENT["night_exterior"], lights_moon(), dict(night=True, moon=dict(pos=[14, 17, -22]))
    d = dict(cells=cells, interior=False, wall=wall, floor=floor, ambient=amb, camera=cam(cells), lights=lights)
    d.update(extra)
    d.update(kw)
    return d


def hv(**over):
    return human_colors(**over)


# ------------------------------------------------------------------ ACT
ACT = dict(
    id=6, title="The Hunt",
    start=dict(
        location="a6_varna_quay", protagonist="seward",
        party=["harker", "mina", "vanhelsing", "seward", "quincey", "arthur"],
        items={"crucifix": 3, "host": 8, "garlic_wreath": 2, "garlic": 2, "stake": 4, "hammer": 1, "kukri": 1,
               "winchester": 4, "bullet": 24, "sacred_bullet": 4, "brandy": 2, "bandage": 3, "knife": 1,
               "a6_purse": 1, "a6_field_glasses": 1},
        flags=[],
    ),
    exit_to="END",
)

LOCATIONS = [
    dict(id="a6_varna_quay", name="The quay, Varna", date="15 October",
         desc="Grey water, tarred hulls and a forest of masts. Somewhere out on the Black Sea a ship called the Czarina Catherine is long overdue."),
    dict(id="a6_hotel_odessa", name="Hotel Odessus, Varna", date="15-28 October",
         desc="A stuffy private sitting room with a sofa for Mina, a table of telegrams, and a window on the harbour."),
    dict(id="a6_lloyds_office", name="Lloyd's agency, Varna", date="17 October",
         desc="Ledgers, brass rails and a clerk who has not yet been told why four Englishmen are so anxious about one ship."),
    dict(id="a6_galatz_quay", name="The harbour, Galatz", date="30 October",
         desc="A river harbour in the early mist. The Czarina Catherine lies at her moorings, unaccountably arrived."),
    dict(id="a6_czarina_deck", name="Aboard the Czarina Catherine", date="30 October, 9 a.m.",
         desc="A wet deck, a silent crew and a hold that smells of old earth."),
    dict(id="a6_hildesheim_office", name="Hildesheim's office, Burgen-strasse", date="30 October",
         desc="A cramped back office, all ledgers and locked boxes. Its owner counts coins with his eyes before his hands."),
    dict(id="a6_peters_churchyard", name="St. Peter's churchyard, Galatz", date="30 October",
         desc="A walled yard in the grey morning. By the wall lies the man who carried the box."),
    dict(id="a6_galatz_hotel", name="Hotel at Galatz", date="30 October, evening",
         desc="The men are asleep. In the sitting room Mina's typewriter clicks softly in the lamplight."),
    dict(id="a6_launch_deck", name="The steam launch Mina, the Sereth", date="30 October - 1 November",
         desc="Night on the river. The little launch throbs against the current, her electric lamp throwing a white road on the water."),
    dict(id="a6_rapids", name="The rapids on the Bistritza", date="2-3 November",
         desc="Brown water, white spray and a broken keel. The river will carry us no further."),
    dict(id="a6_bistritz_trail", name="The bank road to Fundu", date="2-4 November",
         desc="A mud road along the right bank, a sky of low snow-cloud, and a long way still to the mountains."),
    dict(id="a6_veresti_inn", name="Inn at Veresti", date="31 October",
         desc="A village inn with a fat landlady, a stove, and a great basket being packed with provisions."),
    dict(id="a6_mountain_road", name="The road to the Borgo Pass", date="1-3 November",
         desc="The road climbs into the pine and the snow. Peasants make the sign against the evil eye as we pass."),
    dict(id="a6_holy_circle", name="Below Castle Dracula", date="4 November, night",
         desc="A fire in the snow, a ring of crumbled Host, and a ruined castle black against the stars."),
    dict(id="a6_castle_gate", name="Castle Dracula, the courtyard", date="5 November",
         desc="By daylight the castle is only a ruin. The great chapel door has rusted shut."),
    dict(id="a6_castle_chapel", name="The old chapel", date="5 November, afternoon",
         desc="Cold, dusty, and silent. Fifty boxes once stood here. Now only the tombs remain."),
    dict(id="a6_brides_crypt", name="The sisters' vault", date="5 November",
         desc="Three tombs. In one lies a woman more radiant than any living, and the room is thick with her will."),
    dict(id="a6_hollow", name="A hollow among the rocks", date="6 November",
         desc="Two great boulders and a pocket of shelter. From here the whole plain can be seen through the glasses."),
    dict(id="a6_snow_plain", name="The plain below the castle", date="6 November, sunset",
         desc="A white plain, a low red sun, and the leiter-wagon racing the dusk toward the castle."),
    dict(id="a6_sunset_snow", name="The snowfield at sunset", date="6 November, sunset",
         desc="The wind has dropped. Where the Count stood, there is nothing but dust."),
    dict(id="a6_epilogue_study", name="Exeter, a study", date="Seven years after",
         desc="A book-lined room, a boy at play, and a thick bundle of typescript tied with ribbon."),
]

# ------------------------------------------------------------------ appearance variants
_WATER = {"stone": T("glass", "#2a4458")}
_DARK_WATER = {"stone": T("glass", "#1a2c3c")}
VARIANTS = {
    "floor_4x4": {"a6_water": _WATER, "a6_night_water": _DARK_WATER, "a6_snow": {"stone": T("snow")}},
    "wall_4": {"a6_water": _WATER, "a6_night_water": _DARK_WATER, "a6_snow": {"stone": T("snow")}},
    "human_peasant_m": {
        "a6_hildesheim": hv(top=T("wool", "#2a2622"), bottom=T("wool", "#26221e"), hair=T("hair", "#9a9486"), accent=T("cloth", "#3a3028")),
        "a6_harbour": hv(top=T("wool", "#1e2a44"), bottom=T("wool", "#1e2230"), hair=T("hair", "#6a6258"), accent=T("cloth", "#c9a248")),
        "a6_donelson": hv(top=T("wool", "#18243c"), bottom=T("wool", "#18243c"), hair=T("hair", "#a8603a"), accent=T("cloth", "#c9a248")),
        "a6_sailor": hv(top=T("cloth", "#6a6a58"), bottom=T("wool", "#3a3a32"), hair=T("hair", "#2a2018")),
        "a6_clerk": hv(top=T("wool", "#3a3a40"), bottom=T("wool", "#2a2a30"), hair=T("hair", "#4a3a2a")),
        "a6_priest": hv(top=T("cloth", "#141414"), bottom=T("cloth", "#141414"), hair=T("hair", "#c8c4b8"), accent=T("cloth", "#e8e2d0")),
        "a6_boatman": hv(top=T("cloth", "#5a4a38"), bottom=T("wool", "#3a3228"), accent=T("fur", "#4a3a2a"), hair=T("hair", "#7a6a50")),
        "a6_szgany_chief": hv(skin=T("skin", "#a8794f"), top=T("cloth", "#8a2418"), bottom=T("wool", "#222222"), accent=T("fur", "#2a2018"), hair=T("hair", "#0e0a0a")),
    },
    "human_peasant_f": {
        "a6_landlady": hv(skin=T("skin", "#e8bd98"), top=T("cloth", "#8a3a3a"), accent=T("cloth", "#e0d8c8"), hair=T("hair", "#7a6a5a")),
    },
    "a6_launch": {"default": {}},
    "a6_brig": {"default": {}, "a6_black": {"wood": T("wood_planks", "#3a2a22")}},
    "a6_leiter_wagon": {"default": {}},
    "a6_earth_box": {"default": {}},
}

ASSETS = [
    dict(id="a6_launch", builder="a6_launch", params={}),
    dict(id="a6_leiter_wagon", builder="a6_leiter_wagon", params={}),
    dict(id="a6_earth_box", builder="a6_earth_box", params={}),
    dict(id="a6_brig", builder="a6_brig", params={}),
]

# ------------------------------------------------------------------ items
ITEMS = {
    "a6_purse": dict(name="Lord Godalming's purse", asset="key", variant="gold", desc="Arthur's purse. Money, he says, is the only language every port understands."),
    "a6_field_glasses": dict(name="Field glasses", asset="lantern", variant="default", desc="Van Helsing's field glasses, brass and leather, good for a mile of open ground."),
    "a6_whetstone": dict(name="Whetstone", asset="hammer", variant="default", desc="A flat grey whetstone from a chandler's stall. Jonathan's kukri has not seen one in a week."),
    "a6_sharp_kukri": dict(name="Whetted kukri", asset="stake", variant="default", desc="Jonathan's Ghoorka knife, edged till it takes a hair from the air."),
    "a6_telegram": dict(name="Lloyd's telegram", asset="book", variant="red", desc="'Czarina Catherine reported entering Galatz at one o'clock to-day.'"),
    "a6_bradshaw": dict(name="Continental timetable", asset="book", variant="leather", desc="A thumbed railway guide. Mina has marked the Varna line in pencil."),
    "a6_permit": dict(name="Shippers' letter", asset="book", variant="diary", desc="A paper from the Varna shippers to the Captain and the Galatz agent: they may look in the box."),
    "a6_bill_of_lading": dict(name="Bill of lading", asset="book", variant="diary", desc="Fifty pounds' worth of earth, consigned to one Immanuel Hildesheim, Burgen-strasse 16, Galatz."),
    "a6_ms_letter": dict(name="Letter of introduction", asset="book", variant="red", desc="A note from Messrs. Mackenzie & Steinkoff asking Hildesheim to be helpful. It carries weight."),
    "a6_receipt": dict(name="Hildesheim's receipt", asset="book", variant="leather", desc="The box was handed over to one Petrof Skinsky, a Slovak. Signed, with a thumbprint."),
    "a6_skinsky_slip": dict(name="Boat-hire slip", asset="book", variant="red", desc="A slip of rough paper found by Skinsky's wall: a boat, a crew of Slovaks, 'up the river by night'."),
    "a6_map": dict(name="Map of the Sereth and Bistritza", asset="book", variant="red", desc="Mina's map, pencilled with the Count's likely road through Fundu to the Borgo Pass."),
    "a6_typescript": dict(name="Typescript of the journals", asset="book", variant="diary", desc="Mina's fair copy of every diary and letter. A thick bundle, still smelling of ink."),
    "a6_roumanian_flag": dict(name="Roumanian flag", asset="key", variant="default", desc="A small flag. Fly it at Fundu and the villagers will take us for officials."),
    "a6_lamp": dict(name="Electric lamp", asset="lantern", variant="default", desc="A bright electric lamp for the launch. The boatmen fall to their knees when it shines on them."),
    "a6_provisions": dict(name="Provision basket", asset="barrel", variant="oak", desc="A basket of bread, cold meat and a flask of soup, packed by a landlady who says nothing about why."),
    "a6_furs": dict(name="Furs and rugs", asset="rug", variant="black", desc="Heavy furs. It is a long way to the pass and the snow is coming."),
}

# ------------------------------------------------------------------ journal
JOURNAL = {
    "a6_j_ward": dict(title="The outer ward", source="Professor Van Helsing's notes",
                      text="By day the Count's stronghold is only a ruin: fallen merlons, a gate that no longer closes, and a keep rotted open to the snow. But a fire was lit here not two days past, and the cold ashes lead toward the gate. He has not left his house empty. He has left it waiting."),
    "a6_j_oath": dict(title="11 October. The promise", source="Dr. Seward's diary",
                      text="Before we left London Mina asked each of us to swear that, if she turned, we would do for her what we did for Lucy. Quincey swore first. Jonathan was to read the Burial Service. We are in God's hands, and we must be steady."),
    "a6_j_varna": dict(title="15 October. Varna", source="Dr. Seward's diary",
                       text="Three days by the Orient Express. Mina slept almost the whole way. Now we are at Varna, and the Czarina Catherine has not arrived. Lord Godalming wires Lloyd's daily. We have nothing to do but wait."),
    "a6_j_trance1": dict(title="Mina at sunset", source="Mina Harker's journal",
                         text="The Professor put me in trance. I heard lapping water, rushing by. I heard creaking, as of masts and cordage, and the tramp of feet overhead. I felt a motion under me. The ship is moving, and the ship is not here."),
    "a6_j_lloyds": dict(title="Lloyd's report", source="Lord Godalming, by telegram",
                        text="The Czarina Catherine was reported passing the Dardanelles on 4 October. Nothing since. A fast steamer would be here already; she is not. Either the sea has her, or she is making for some other port."),
    "a6_j_deduce": dict(title="The ship is elsewhere", source="Dr. Seward's diary",
                        text="Van Helsing says the Count knows we are at Varna: he learned it through Mina's mind, and has cut her off. The ship will not come where we wait. We must watch the wires and be ready to run."),
    "a6_j_telegram": dict(title="28 October. Galatz!", source="Dr. Seward's diary",
                          text="A telegram from Lloyd's: the Czarina Catherine has entered Galatz at one o'clock. We have been tricked, and by a margin of a day. Mina, the 'train fiend,' says the only train leaves at 6.30 in the morning."),
    "a6_j_timetable": dict(title="The 6.30", source="Mina Harker's journal",
                           text="The Continental Bradshaw gives one train a day from Varna to Galatz: leaving at half-past six, arriving in the afternoon. Jonathan laughs at me for my 'train fiend' ways, but he is glad of them now."),
    "a6_j_galatz": dict(title="30 October. The Czarina Catherine", source="Dr. Seward's diary",
                        text="The ship lies in the river harbour, and the box is gone. Captain Donelson says the box was taken ashore at dawn by men acting for a Hildesheim. Our one hope now is to follow the trail before it is cold."),
    "a6_j_donelson": dict(title="Captain Donelson's tale", source="Dr. Seward's diary",
                          text="A fog went with the ship from the Bay of Biscay to Galatz, and the crew would not touch the long box. The Captain swung a handspike at the mutiny. 'If the Deil did have any luggage aboord the ship, it was nane ither than that.'"),
    "a6_j_hildesheim": dict(title="Hildesheim", source="Jonathan Harker's journal",
                            text="Immanuel Hildesheim was bought at a fair price and delivered a receipt. The box was handed to a Slovak named Petrof Skinsky. The price was paid by an English note cashed at the bank. Hildesheim hopes we shall not trouble him again."),
    "a6_j_skinsky": dict(title="Petrof Skinsky", source="Dr. Seward's diary",
                         text="Skinsky was found in St. Peter's churchyard, his throat torn. The priest says wolves; the neighbours say a very tall man. But in his coat was a slip for a boat and a crew of Slovaks, to go up the river by night."),
    "a6_j_memorandum": dict(title="Mina's memorandum", source="Mina Harker's journal",
                            text="By exclusion: not by road, since horses fear him; not by rail, since he must be seen at stations; therefore by water, on the Sereth, then the Bistritza, which is the water that runs by the Borgo Pass. It must be so."),
    "a6_j_council": dict(title="The council of war", source="Dr. Seward's diary",
                         text="Lord Godalming and Jonathan go by steam launch. Quincey and I ride the bank. Van Helsing takes Mina by train and carriage to the Borgo Pass and the castle. Jonathan protested; Mina quieted him. Money brought us a launch, horses and maps in three hours."),
    "a6_j_launch": dict(title="Night on the river", source="Jonathan Harker's journal",
                        text="We steam day and night, overhauling every boat. The Slovaks fall on their knees when our electric lamp strikes them. They say a boat with a great box passed before us, bound up the Bistritza with Szgany at the oars."),
    "a6_j_rapids": dict(title="The rapids", source="Jonathan Harker's journal",
                        text="The launch struck a rock below the rapids and lost her keel plank. We mended her with a spar, a coil of rope and canvas, and lost half a day. Lord Godalming bought horses at a farm above the falls."),
    "a6_j_trail": dict(title="The bank road", source="Dr. Seward's diary",
                       text="Quincey and I have ridden three days along the right bank. At Fundu we heard that the launch went up the Bistritza. Snow threatens; if the road closes we shall take a sledge and go on, Russian fashion. Wolves howl behind us."),
    "a6_j_veresti": dict(title="31 October. Veresti", source="Mina Harker's journal",
                         text="The Professor bought a carriage, horses and furs. The landlady packed a great basket and wept. We are truly in the hands of God. I write this to Jonathan, who may never see it."),
    "a6_j_road": dict(title="The Borgo road", source="Mina Harker's journal",
                      text="I knew the road at the Pass. Have not my Jonathan travelled it, and written of his travel? I am strangely sleepy all day and wakeful at dusk. The peasants cross themselves at my scar. The Professor watches me and says nothing."),
    "a6_j_circle": dict(title="4 November. The holy circle", source="Mina Harker's journal",
                        text="The Professor crumbled the Host into a ring around me and the fire. I cannot step out of it, though I long to. The horses scream and cower in the snow. Mist forms in the dark, and three white women are calling me sister."),
    "a6_j_sisters": dict(title="The three sisters", source="Mina Harker's journal",
                         text="They begged, and laughed, and wept, and held out their arms. 'Come, sister. Come to us.' The Professor held the Host toward them and they could not cross. At dawn they thinned into the snow, and we found the horses dead."),
    "a6_j_castle": dict(title="5 November. The castle", source="Van Helsing's memorandum",
                        text="By day the castle is only stone. I broke the rusted chapel door with a blacksmith's hammer, and my heart was a stone also. I must not look at the faces in the tombs too long."),
    "a6_j_brides": dict(title="The three tombs", source="Van Helsing's memorandum",
                        text="In the first tomb lay a woman so lovely that I felt the madness of her call. I heard Mina's wail, and the spell broke. Stake, then knife; the dust fell and she was at peace. So with the others. Three souls made free."),
    "a6_j_tomb": dict(title="The Count's tomb", source="Van Helsing's memorandum",
                      text="I laid a piece of Host in the Count's own tomb, which was empty, and made it unclean for him forever. The doors I sealed with the Wafer also. He cannot come home to rest, whatever else he may do."),
    "a6_j_hollow": dict(title="6 November. The hollow", source="Mina Harker's journal",
                        text="We rested in a hollow between two great stones. The Professor drew a circle around the rock and looked out through the glasses. 'They are racing for the sunset. We may be too late. God's will be done!'"),
    "a6_j_final": dict(title="The sunset", source="Jonathan Harker's journal",
                       text="We rode to death of some one. The Szgany closed around the wagon. I cut through to the box; Quincey beside me. I swung the kukri at the Count's throat while Quincey's knife went to his heart. Before our eyes he crumbled into dust."),
    "a6_j_quincey": dict(title="Quincey Morris", source="Mina Harker's journal",
                         text="Quincey was stabbed in the side and bleeding fast. The setting sun fell on my forehead, and he cried, 'See! The snow is not more stainless than her forehead! The curse has passed away!' He died with a smile. A gallant gentleman."),
}

# ================================================================== LOCATIONS
LOC_DATA = {}

# ------------------------------------------------------------------ CHAPTER XXV: VARNA
LOC_DATA["a6_varna_quay"] = outdoor(
    [3, 2], "fog", floor="cobble", wall="plaster_dirty",
    walls=dict(north=["wall_4", "wall_door_4", "wall_door_4"]),
    spawn=[0.0, 2.6], spawns={"a6_hotel_odessa": [0.0, -2.6], "a6_lloyds_office": [4.0, -2.6]},
    props=[
        prop("a6_hotel_door", "door", "dark", 0.0, -3.8, name="Hotel Odessus", radius=0.7,
             look="The hotel where we wait, day after day, for a ship that does not come. Mina is within.", go="a6_hotel_odessa"),
        prop("a6_lloyds_door", "door", "oak", 4.0, -3.8, name="Lloyd's agency", radius=0.7,
             look="A brass plate: 'Agency. Shipping intelligence.' Lord Godalming has been in and out of it all week.", go="a6_lloyds_office"),
        prop("a6_station_cab", "carriage", "ebony", -4.6, 1.2, rot=90, name="Cab to the station", radius=1.6,
             look="A closed cab waits to take us to the railway station. It will not go until every detail of our plan is settled.",
             go="a6_galatz_quay", go_cond="has:a6_telegram&has:a6_permit&has:a6_sharp_kukri&flag:a6_train_time&flag:a6_oath_renewed",
             go_fail="We cannot go yet. We need Lloyd's telegram, the shippers' paper, the train time from Mina, Jonathan's knife sharpened, and Mina's promise renewed."),
        prop("a6_grindstone", "barrel", "dark", -3.0, -2.3, name="Chandler's grindstone", radius=0.5,
             look="A grindstone at a ship-chandler's stall, with a flat whetstone left on the rim. The chandler has wandered off to his dinner.",
             take="a6_whetstone", take_text="I pocketed the whetstone. I shall leave a coin on the barrel for the chandler.", give_once=True),
        prop("a6_rope_chest", "chest", "pale", 2.2, 2.6, name="Chest of ropes", radius=0.6,
             look="A seaman's chest. A good coil of rope is on top, tarred and strong.",
             take="rope", take_text="I took a coil of rope. It may prove a mercy.", give_once=True),
        prop("a6_slat_crate", "chest", "dark", -0.6, -2.4, name="Broken crate", radius=0.6,
             look="A crate burst by a dropped hook. One slat is a good length of seasoned ash.",
             take="wood", take_text="I pulled out a length of ash. It will make a stake or a fire.", give_once=True),
        prop("a6_quay_lamp", "lantern", "default", 3.4, 0.4, name="Quay lamp", radius=0.4,
             look="A ship's lamp on a post, burning oil against the fog. The reservoir is full.",
             take="oil", take_text="I drew off a little lamp oil into a flask.", give_once=True),
        prop("a6_signpost", "signpost", "oak", -2.2, 2.4, name="Signpost", radius=0.3,
             look="HOTEL ODESSUS. LLOYD'S AGENCY. RAILWAY STATION. And in Greek beneath: 'Sailors, mind the fog.'"),
        deco("a6_bench", "bench", "dark", -0.5, 0.9, rot=0),
        deco("a6_barrel_a", "barrel", "oak", 4.9, -1.4), deco("a6_barrel_b", "barrel", "dark", 5.3, -0.4, rot=20),
        deco("a6_barrel_c", "barrel", "oak", 5.2, 1.6, rot=40),
        deco("a6_hull", "a6_brig", "a6_black", -9.5, -2.0, rot=90),
        deco("a6_fence", "fence", "default", 6.5, 2.0, rot=90),
        deco("a6_rock", "rock", "dark", -5.5, -3.2, scale=0.8),
    ],
    npcs=[
        npc("a6_harbourmaster_v", "human_peasant_m", "a6_harbour", -1.8, 0.4, rot=20, name="Harbour master", radius=0.5,
            look="A stout Bulgarian harbour master in a salt-stained cap. He has been asked about one ship too often.", talk="a6_harbourmaster_varna"),
        npc("a6_sailor_v", "human_peasant_m", "a6_sailor", 2.4, 1.0, rot=-30, name="Greek sailor", radius=0.5,
            look="A weathered Greek sailor mending a net. He crosses himself whenever someone mentions the dead of the sea.", talk="a6_sailor_varna"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="a6_j_oath"), dict(journal="a6_j_varna")])],
)

LOC_DATA["a6_hotel_odessa"] = indoor(
    [2, 2], "plaster", "planks", mood="day",
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[2.6, 0.0], spawns={"a6_varna_quay": [3.0, -1.4]},
    props=[
        prop("a6_hotel_exit", "door", "dark", 3.8, -2.0, rot=-90, name="Door to the quay", radius=0.7,
             look="The door to the quay and the grey harbour.", go="a6_varna_quay"),
        prop("a6_sofa", "bed_simple", "blue", -2.8, -1.0, rot=90, name="Mina's sofa", radius=1.0,
             look="A faded sofa where Mina rests. At every sunrise and sunset the Professor puts her in trance here, and she tells us what she hears."),
        prop("a6_tele_table", "table_long", "dark", 0.4, -1.4, name="Table of telegrams", radius=1.2,
             look="Lloyd's slips, the shippers' cards, a map of the Black Sea held down with a coffee-cup. Mina's typewriter sits at one end."),
        prop("a6_bradshaw", "book", "leather", 0.4, -1.4, y=0.8, name="Continental Bradshaw", radius=0.2,
             look="A thumbed railway guide, open at the Varna line. Mina has underlined a time in pencil.",
             take="a6_bradshaw", take_text="I took the Bradshaw. Mina will want to consult it.", give_once=True),
        prop("a6_typewriter", "book", "red", 1.2, -1.4, y=0.8, name="Mina's typescripts", radius=0.2,
             look="A neat stack of typescript: every diary, every letter, every telegram. 'The facts, in order, are half the battle,' Mina says."),
        prop("a6_hotel_fire", "fireplace", "stone_dark", 2.0, -3.4, name="Fireplace", radius=0.9,
             look="A tiled stove-fireplace, hot as a bakery. The Roumanian chambermaid keeps it at roaring."),
        prop("a6_garlic_pile", "barrel", "pale", -3.2, 2.4, name="Basket of garlic", radius=0.5,
             look="The hotel cook is mystified by Van Helsing's demand for garlic, and has provided it by the basketful.",
             take="garlic", take_text="I took two more heads of garlic. They smell worse than any soup.", give_once=True),
        prop("a6_shelf", "bookshelf", "oak", -3.5, 1.2, rot=90, name="Hotel shelf", radius=0.6,
             look="Roumanian novels, a German guide to the Black Sea, and a Greek psalter nobody has opened."),
        prop("a6_hotel_lamp", "candelabra", "default", -0.8, -1.4, y=0.8, name="Lamp", radius=0.2,
             look="A paraffin lamp with a green shade. It burns long into the night while Jonathan sits up."),
        deco("a6_rug", "rug", "blue", 0.3, 1.6, scale=1.0), deco("a6_chair1", "chair", "blue", -0.8, -0.2, rot=30),
        deco("a6_chair2", "chair", "blue", 1.7, 0.4, rot=-120), deco("a6_chair3", "chair", "green", 2.8, 2.6, rot=-90),
    ],
    npcs=[
        npc("a6_vh_hotel", "human_vanhelsing", "vh", -1.8, -0.2, rot=60, name="Prof. Van Helsing", radius=0.5,
            look="The Professor sits by Mina's sofa with his watch open, waiting for the sun to touch the horizon.", talk="a6_vh_varna"),
        npc("a6_mina_hotel", "human_mina", "mina", -2.2, 0.4, rot=90, name="Mina", radius=0.5,
            look="Mina, very pale, her red scar showing under her hair. She smiles to reassure us and it breaks my heart.",
            talk="a6_mina_hotel", cond="!prot:mina"),
        npc("a6_harker_hotel", "human_harker", "harker", 1.0, 1.4, rot=-100, name="Jonathan", radius=0.5,
            look="Jonathan sits by the window with the Ghoorka knife and a rag, doing what he can with a dull edge.",
            talk="a6_harker_kukri", cond="!prot:harker",
            use_item={"a6_whetstone": [dict(take="a6_whetstone"), dict(give="a6_sharp_kukri"), dict(set="a6_kukri_whetted"),
                                       dict(say="Jonathan bent over the stone, and the edge sang. In a few minutes the Ghoorka knife would take a hair from the air. 'Thank you, Doctor. It is a good tool now. It will be needed.'")]},
            use_fail="Jonathan shakes his head. 'That will not put an edge on it.'"),
        npc("a6_quincey_hotel", "human_quincey", "texan", 2.6, 1.0, rot=-80, name="Quincey Morris", radius=0.5,
            look="Quincey lounges against the wall, as at ease in a hotel as on the prairie, with the Winchester within reach.",
            talk="a6_quincey_hotel", cond="!prot:quincey"),
        npc("a6_arthur_hotel", "human_arthur", "lord", -0.2, 2.5, rot=170, name="Lord Godalming", radius=0.5,
            look="Arthur stands over the table with his hands clasped behind him, lines of sleeplessness at his eyes.",
            talk="a6_arthur_hotel", cond="!prot:arthur"),
        npc("a6_porter", "human_peasant_m", "a6_clerk", 3.0, -0.2, rot=-90, name="Hotel porter", radius=0.5,
            look="The porter loiters with a salver, hoping for a telegram to deliver and a coin to follow.", talk="a6_porter_talk"),
    ],
    on_enter=[dict(once=True, do=[dict(protagonist="mina")])],
)

LOC_DATA["a6_lloyds_office"] = indoor(
    [2, 2], "plaster_dirty", "planks", mood="candle",
    walls=dict(north=["wall_4", "wall_window_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[2.8, -1.2], spawns={"a6_varna_quay": [3.0, -1.4]},
    props=[
        prop("a6_lloyds_exit", "door", "oak", 3.8, -2.0, rot=-90, name="Door to the quay", radius=0.7,
             look="Back to the quay and the fog.", go="a6_varna_quay"),
        prop("a6_desk", "table", "dark", 0.2, -1.8, name="Clerk's desk", radius=0.9,
             look="A tall desk with a blotter, a letter-press and a pigeonhole cabinet of telegraph forms."),
        prop("a6_register", "book", "red", 0.2, -1.8, y=0.8, name="Shipping register", radius=0.2,
             look="Lloyd's register of arrivals and sailings. Under 'C': Czarina Catherine, Roumanian-flagged, last reported off the Dardanelles on the fourth. No later entry.",
             set="a6_read_register", set_text="I traced the ship's entries with a finger. The last is in the Dardanelles on 4 October; since then, a blank."),
        prop("a6_pigeonholes", "bookshelf", "dark", -3.4, -1.0, rot=90, name="Pigeonholes", radius=0.6,
             look="Slips from every port from Odessa to Alexandria, all ordered, none about our ship."),
        prop("a6_lloyds_fire", "fireplace", "plaster_dirty", -1.6, -3.4, name="Stove", radius=0.8,
             look="A small iron stove with a kettle forever on the boil."),
        prop("a6_barometer_lamp", "lantern", "default", 2.8, 2.6, name="Brass lamp", radius=0.3,
             look="A brass lamp, polished to a mirror, on a hook by the door."),
        deco("a6_lloyds_chair1", "chair", "black", -0.8, 0.6, rot=-30), deco("a6_lloyds_chair2", "chair", "black", 2.0, 0.6, rot=210),
        deco("a6_lloyds_rug", "rug", "red", 0.0, 2.0), deco("a6_lloyds_candle", "candelabra", "default", -2.6, 2.3),
        deco("a6_lloyds_chest", "chest", "ebony", 3.3, 2.4, rot=-90),
    ],
    npcs=[
        npc("a6_lloyds_clerk", "human_peasant_m", "a6_clerk", 1.6, -0.5, rot=170, name="Lloyd's clerk", radius=0.5,
            look="A neat young clerk with ink on his cuffs. He takes Lord Godalming's money for telegrams with great composure.", talk="a6_lloyds_clerk"),
        npc("a6_shipper_agent", "human_peasant_m", "a6_hildesheim", -1.6, 0.9, rot=120, name="Shippers' agent", radius=0.5,
            look="A heavy man who speaks four languages, all of them politely, and gives away nothing in any of them.", talk="a6_shipper_agent"),
    ],
    on_enter=[dict(once=True, do=[dict(protagonist="arthur")])],
)

# ------------------------------------------------------------------ CHAPTER XXVI: GALATZ
LOC_DATA["a6_galatz_quay"] = outdoor(
    [3, 2], "fog", floor="cobble", wall="plaster_dirty",
    walls=dict(north=["wall_4", "wall_door_4", "wall_4"], west=["wall_4", "wall_door_4"]),
    spawn=[0.0, 2.6], spawns={"a6_czarina_deck": [3.0, 0.0], "a6_hildesheim_office": [0.0, -2.6],
                              "a6_peters_churchyard": [4.6, 2.2], "a6_galatz_hotel": [-4.4, 2.0], "a6_varna_quay": [-1.0, 2.8]},
    props=[
        prop("a6_czarina", "a6_brig", "default", 3.6, 0.2, rot=90, name="The Czarina Catherine", radius=2.6,
             look="A battered brig with salt-white rigging, her sails furled tight. She came in on the night tide, and no one saw her pilot.",
             go="a6_czarina_deck", go_cond="has:a6_permit", go_fail="The mate at the foot of the gangway will let no stranger aboard. We need the shippers' paper."),
        prop("a6_hildesheim_door", "door", "dark", 0.0, -3.8, name="Burgen-strasse passage", radius=0.7,
             look="A narrow passage to Burgen-strasse, where the Jew Hildesheim keeps his office.",
             go="a6_hildesheim_office", go_cond="has:a6_bill_of_lading", go_fail="I do not yet know where the box was taken. The ship's papers should tell me the consignee."),
        prop("a6_hotel_g_door", "door", "dark", -5.8, 2.0, rot=90, name="Hotel door", radius=0.7,
             look="The way back to the hotel where the others sleep.",
             go="a6_galatz_hotel", go_cond="flag:a6_skinsky_done", go_fail="Not yet. We have barely begun to trace the box."),
        prop("a6_churchyard_gate", "fence", "default", 5.4, 2.6, rot=90, name="Gate to St. Peter's", radius=0.8,
             look="A path leads up to the churchyard on the hill, where something has been found.",
             go="a6_peters_churchyard", go_cond="flag:a6_hildesheim_done", go_fail="I have no reason to go to the churchyard yet."),
        prop("a6_g_cloth", "chest", "oak", -2.4, -2.6, name="Sailcloth bundle", radius=0.6,
             look="A sail-maker's bale of canvas, lying by his shop door.",
             take="cloth", take_text="I took a length of spare canvas. It may be needed to patch a boat.", give_once=True),
        prop("a6_g_crate", "chest", "dark", 1.8, -2.2, name="Stevedore's crate", radius=0.6,
             look="Shipping marks: 'Mackenzie & Steinkoff, Galatz. Via Varna, per Czarina Catherine.' The office clerk stands next to it."),
        prop("a6_g_lamp", "lantern", "default", -3.4, 0.2, name="Dockside lamp", radius=0.3,
             look="A smoky oil-lamp in the fog. The fog clings to the river like a living thing."),
        prop("a6_g_oil", "barrel", "dark", -1.2, 2.5, name="Oil barrel", radius=0.5,
             look="A barrel of lamp oil, bung loose. A tin cup hangs on a nail.",
             take="oil", take_text="I filled a flask with lamp oil.", give_once=True),
        deco("a6_g_bollard1", "column_short", "stone_dark", 5.0, 0.2, scale=0.5), deco("a6_g_bollard2", "column_short", "stone_dark", 2.0, 1.4, scale=0.5),
        deco("a6_g_barrel1", "barrel", "oak", 0.6, 2.6), deco("a6_g_barrel2", "barrel", "dark", 1.0, 2.9, rot=50),
        deco("a6_g_signpost", "signpost", "dark", -4.4, -0.8),
        deco("a6_g_docker", "human_peasant_m", "villager", -0.4, 0.4, rot=100),
    ],
    npcs=[
        npc("a6_harbourmaster_g", "human_peasant_m", "a6_harbour", -2.2, 0.8, rot=-20, name="Harbour master", radius=0.5,
            look="The Galatz harbour master, weighing us up as we ask about the Czarina Catherine. He has seen stranger cargoes, but not many.",
            talk="a6_harbourmaster_galatz"),
        npc("a6_ms_clerk", "human_peasant_m", "a6_clerk", 1.2, -1.2, rot=170, name="Mackenzie & Steinkoff clerk", radius=0.5,
            look="A clerk from Messrs. Mackenzie & Steinkoff, shipping agents, with a ledger under his arm and a nervous cough.",
            talk="a6_ms_clerk"),
    ],
    on_enter=[dict(once=True, do=[dict(protagonist="seward"), dict(journal="a6_j_telegram")])],
)

LOC_DATA["a6_czarina_deck"] = outdoor(
    [2, 2], "fog", floor="planks", wall="planks",
    spawn=[3.0, 0.0], spawns={"a6_galatz_quay": [3.0, 0.0]},
    props=[
        prop("a6_gangway", "bench", "oak", 3.6, 1.0, rot=90, name="Gangway", radius=0.9,
             look="A plank gangway down to the quay.", go="a6_galatz_quay"),
        prop("a6_hatch", "chest", "ebony", -0.4, -0.8, name="Cargo hatch", radius=0.8,
             look="The hatch where the long box lay. The boards still smell of old earth, and a few dry crumbs of soil cling to the iron of the clasp.",
             set="a6_hold_seen", set_text="I stooped to the hatch. Earth, dry and foreign, and the faint mould of a vault."),
        prop("a6_logbook", "book", "diary", -0.4, -0.8, y=0.5, name="Captain's log", radius=0.2,
             look="Donelson's log, open at the last pages. The entries speak of fog, a silent man, and a long box. The last line is blotted."),
        prop("a6_deck_cloth", "chest", "oak", 2.4, -2.4, name="Sail locker", radius=0.6,
             look="A locker of mended canvas. The mate will not miss a yard.",
             take="cloth", take_text="I took a yard of sail canvas.", give_once=True),
        prop("a6_deck_rope", "barrel", "dark", -3.0, 1.8, name="Rope tub", radius=0.5,
             look="A tub of coiled hemp, wet but sound.",
             take="rope", take_text="I took a second coil of rope.", give_once=True),
        prop("a6_wheel", "column_short", "stone_dark", -1.6, 2.6, name="Ship's wheel", radius=0.4,
             look="The helm. The wheel spokes are dark with sweat. The Captain says no hand but his own turned it for nine days of fog."),
        deco("a6_mast", "column", "stone_dark", 0.8, 0.2), deco("a6_deck_barrel", "barrel", "oak", 3.0, -1.2),
        deco("a6_deck_lantern", "lantern", "default", 1.6, 2.4), deco("a6_deck_rock", "rock", "grey", -4.6, -2.6, scale=0.6),
        deco("a6_deck_chest2", "chest", "dark", -2.6, -2.8),
    ],
    npcs=[
        npc("a6_donelson", "human_peasant_m", "a6_donelson", 0.8, -1.8, rot=170, name="Captain Donelson", radius=0.5,
            look="A square Scot with a grey-flecked ginger beard. He grips a handspike as if the argument were still going.", talk="a6_donelson"),
        npc("a6_crew_a", "human_peasant_m", "a6_sailor", -2.2, 0.4, rot=60, name="Roumanian sailor", radius=0.5,
            look="A sailor who will not look at the hatch. He makes the sign against the evil eye when we pass.", talk="a6_roumanian_crew"),
        npc("a6_crew_b", "human_peasant_m", "villager", 2.0, 1.6, rot=-110, name="Deckhand", radius=0.5,
            look="A young deckhand scrubbing planking that is already clean. He mutters about a tall man at the dead of night.", talk="a6_deckhand"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="a6_j_donelson")])],
)

LOC_DATA["a6_hildesheim_office"] = indoor(
    [2, 2], "plaster_dirty", "planks", mood="candle",
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[2.8, -1.2], spawns={"a6_galatz_quay": [3.0, -1.4]},
    props=[
        prop("a6_hildesheim_exit", "door", "dark", 3.8, -2.0, rot=-90, name="Door to the passage", radius=0.7,
             look="Out to Burgen-strasse and the quay.", go="a6_galatz_quay"),
        prop("a6_h_desk", "table", "ebony", -0.2, -1.6, name="Hildesheim's desk", radius=0.9,
             look="A desk fitted with a hundred little drawers, each with its own lock. A set of brass scales stands on the corner."),
        prop("a6_h_ledger", "book", "leather", -0.2, -1.6, y=0.8, name="Ledger", radius=0.2,
             look="'De Ville, Carpathian earth: 12 boxes, consigned per rail from Bucharest.' The Count used a different alias for each leg of his journey."),
        prop("a6_h_strongbox", "chest", "ebony", -3.2, -1.8, name="Strongbox", radius=0.6,
             look="An iron-bound box with a triple lock. Hildesheim glances at it every time we move."),
        prop("a6_h_shelf", "bookshelf", "dark", -3.5, 1.4, rot=90, name="Account books", radius=0.6,
             look="Row on row of leather account books, spines marked in German and Hebrew."),
        prop("a6_h_coin_dish", "goblet", "default", 0.6, -1.6, y=0.8, name="Dish of coins", radius=0.15,
             look="A shallow dish of Roumanian silver. A small coin lies next to it, apparently forgotten.",
             take="silver", take_text="I took the forgotten coin. It might serve for a Slovak's hand later.", give_once=True),
        prop("a6_h_fire", "fireplace", "soot", 2.0, -3.4, name="Little stove", radius=0.8,
             look="A stove that has not been properly warm for years. Hildesheim does not like to spend."),
        deco("a6_h_chair1", "chair", "black", 0.4, -0.2, rot=180), deco("a6_h_chair2", "chair", "black", 1.4, 0.6, rot=-150),
        deco("a6_h_lamp", "candelabra", "default", -2.0, -0.6), deco("a6_h_rug", "rug", "black", 0.0, 1.8),
    ],
    npcs=[
        npc("a6_hildesheim", "human_peasant_m", "a6_hildesheim", 0.6, -0.8, rot=200, name="Immanuel Hildesheim", radius=0.5,
            look="A dark, narrow man in a rusty black coat, who looks at everything first as a price, and then as a risk.", talk="a6_hildesheim"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="a6_j_hildesheim")])],
)

LOC_DATA["a6_peters_churchyard"] = outdoor(
    [3, 2], "dusk", floor="grass", wall="dirt",
    scatter=dict(asset="deadtree", variant="grey", count=10, seed=7, avoid=[[-6, -4, 6, 4]]),
    scatter2=dict(asset="rock", variant="mossy", count=6, seed=3, avoid=[[-6, -4, 6, 4]]),
    spawn=[4.6, 2.2], spawns={"a6_galatz_quay": [4.6, 2.2]},
    props=[
        prop("a6_churchyard_exit", "fence", "default", 5.6, 2.4, rot=90, name="Gate to the quay", radius=0.8,
             look="The way back down to the harbour.", go="a6_galatz_quay"),
        prop("a6_skinsky_body", "coffin", "oak", -1.2, -0.6, rot=90, name="Petrof Skinsky", radius=1.0,
             look="A Slovak lies under a sheet by the wall. His throat is torn open, clean as by one bite, and nothing else is disturbed. It is not the work of wolves.",
             set="a6_saw_body", set_text="I lifted the sheet. One wound, at the throat, as sharp and exact as a surgeon's. Wolves tear; they do not choose."),
        prop("a6_g1", "gravestone", "stone_mossy", 2.0, -2.6, name="Gravestone", radius=0.4,
             look="Roumanian and Greek script, a name worn away. Fresh flowers lie before it."),
        prop("a6_g2", "gravestone_point", "stone_grey", 3.6, -1.0, name="Gravestone", radius=0.4,
             look="'Maria, wife of a Danubian pilot.' She has been dead seven years."),
        prop("a6_g3", "grave_cross", "stone_dark", -4.2, -2.4, name="Iron cross", radius=0.3,
             look="An iron cross with a sprig of garlic wired to the arm. The folk here know of the Un-Dead too."),
        prop("a6_c_lantern", "lantern", "default", 1.2, 1.6, name="Churchyard lantern", radius=0.3,
             look="A tin lantern left by the sexton, still lit."),
        prop("a6_graveyard_rose", "garlic", "default", -2.8, 2.4, name="Wild rose bush", radius=0.4,
             look="A late wild rose, hips red among the thorns. Van Helsing swears by it.",
             take="wild_rose", take_text="I cut a sprig of wild rose.", give_once=True),
        deco("a6_g4", "gravestone", "stone_dark", -3.0, -0.4, rot=15), deco("a6_g5", "grave_cross", "stone_grey", 0.2, -2.8),
        deco("a6_g6", "tomb", "stone_mossy", -4.8, 0.8, rot=90), deco("a6_wall1", "fence", "default", 0.0, -3.8),
    ],
    npcs=[
        npc("a6_priest", "human_peasant_m", "a6_priest", -2.6, 0.8, rot=100, name="Parish priest", radius=0.5,
            look="A tired old priest in a black soutane, who says his office over the dead man in a low voice and will not speak ill of wolves.",
            talk="a6_priest"),
        npc("a6_neighbour", "human_peasant_f", "village_woman", 2.8, 1.0, rot=-130, name="Skinsky's neighbour", radius=0.5,
            look="A woman in a black headscarf, wringing her apron. She says she saw a very tall man in the lane.", talk="a6_neighbour"),
    ],
    on_enter=[dict(once=True, do=[dict(say="The yard is quiet. A sheet covers what lies by the wall.")])],
)

LOC_DATA["a6_galatz_hotel"] = indoor(
    [2, 2], "plaster", "planks", mood="candle",
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[2.8, -1.2], spawns={"a6_galatz_quay": [3.0, -1.4]},
    props=[
        prop("a6_g_hotel_exit", "door", "dark", 3.8, -2.0, rot=-90, name="Door to the quay", radius=0.7,
             look="The way down to the quay and the river.", go="a6_galatz_quay"),
        prop("a6_memo_desk", "table_long", "dark", -0.4, -1.6, name="Mina's work table", radius=1.2,
             look="Mina's typewriter, a lamp, a spread of maps and the whole case in order. She works quietly while the men sleep.",
             talk="a6_mina_memorandum"),
        prop("a6_g_typescript", "book", "diary", -1.2, -1.6, y=0.8, name="Typescript bundle", radius=0.2,
             look="Mina's typescripts, tied with a ribbon.",
             take="a6_typescript", take_text="I took the typescript; every fact we hold is in it.", give_once=True),
        prop("a6_g_map", "book", "red", 0.6, -1.6, y=0.8, name="Map of the rivers", radius=0.2,
             look="A large-scale map of the Sereth and the Bistritza. Mina has pencilled a thin line from Galatz to the Borgo Pass.",
             take="a6_map", take_text="I folded the map into my coat.", give_once=True, cond="a6_memorandum"),
        prop("a6_g_stove", "fireplace", "stone_grey", 2.0, -3.4, name="Stove", radius=0.8,
             look="A stove with a copper kettle, still warm."),
        prop("a6_g_bed", "bed", "blue", -3.0, 1.6, rot=90, name="Hotel bed", radius=1.0,
             look="Jonathan lies on the bed in his boots, asleep at last."),
        deco("a6_g_chair", "chair", "green", 0.2, 0.2, rot=200), deco("a6_g_rug", "rug", "green", 1.0, 1.6),
        deco("a6_g_candle", "candelabra", "default", -2.4, -0.6), deco("a6_g_shelf", "bookshelf", "pale", -3.5, -0.8, rot=90),
    ],
    npcs=[
        npc("a6_vh_council", "human_vanhelsing", "vh", 1.4, 0.4, rot=-120, name="Prof. Van Helsing", radius=0.5,
            look="The Professor, awake and alert, wearing the face he put on at the grave of Lucy.", talk="a6_council", cond="!prot:vanhelsing"),
        npc("a6_dealer", "human_peasant_m", "a6_boatman", 2.4, 1.8, rot=-100, name="Roumanian dealer", radius=0.5,
            look="A fat river-trader summoned by Lord Godalming. Money has already begun to speak.", talk="a6_dealer"),
    ],
    on_enter=[dict(once=True, do=[dict(protagonist="mina")])],
)

# ------------------------------------------------------------------ CHAPTER XXVI: THE PURSUIT UP THE RIVERS
LOC_DATA["a6_launch_deck"] = outdoor(
    [3, 2], "night", floor="a6_night_water", wall="a6_night_water",
    scatter=dict(asset="pine", variant="dark", count=14, seed=21, avoid=[[-7, -5, 7, 5]]),
    spawn=[-3.8, 2.4], spawns={},
    props=[
        prop("a6_launch_model", "a6_launch", "default", 0.0, 0.0, rot=90, name="Steam launch 'Mina'", radius=1.6,
             look="Lord Godalming's launch, named for Mina. She is small, lean and fast, with a boiler that eats wood like a furnace."),
        prop("a6_boiler", "barrel", "dark", -0.6, -0.9, name="Boiler", radius=0.6,
             look="The little boiler, cold at the grate. It wants wood, and plenty of it, before the gauge will rise.",
             use_item={"wood": [dict(take="wood"), dict(set="a6_stoked"), dict(say="I stoked the grate. The gauge needle crept up, then began to shiver.")]},
             use_fail="The boiler needs wood for fuel."),
        prop("a6_engine", "chest", "ebony", 1.6, -0.9, name="Engine", radius=0.6,
             look="A compact little engine, its bearings dry as bone. A touch of oil will keep it from seizing.",
             use_item={"oil": [dict(take="oil"), dict(set="a6_engine_oiled"), dict(say="A few drops of oil on each bearing. The engine purred.")]},
             use_fail="The engine needs oil."),
        prop("a6_woodpile", "chest", "oak", -4.2, -0.4, name="Woodpile", radius=0.7,
             look="A neat stack of split logs on the quay. We shall need all of it before Fundu.",
             take="wood", take_text="I carried an armful of logs aboard.", give_once=True),
        prop("a6_flagstaff", "signpost", "oak", 2.8, 1.2, name="Flagstaff", radius=0.3,
             look="A bare flagstaff at the stern. A flag will give us the look of officials, and fewer questions on the river.",
             use_item={"a6_roumanian_flag": [dict(take="a6_roumanian_flag"), dict(set="a6_flag_up"), dict(say="The little Roumanian flag snapped in the wind. Villagers on the bank will take us for officials.")]},
             use_fail="A flag of the country would serve here."),
        prop("a6_lamp_mount", "lantern", "default", 3.6, -0.6, name="Lamp bracket", radius=0.4,
             look="An iron bracket at the bow, built for a searchlight.",
             use_item={"a6_lamp": [dict(take="a6_lamp"), dict(set="a6_lamp_fitted"), dict(say="The electric lamp threw its road of white across the water. Every boat ahead of us is now to be found.")]},
             use_fail="A strong lamp would serve in this bracket."),
        prop("a6_chart_table", "table", "pale", -2.4, 2.6, name="Chart table", radius=0.8,
             look="A chart table under a tarpaulin. The sheet is blank, waiting for a map.",
             use_item={"a6_map": [dict(set="a6_course_plotted"), dict(say="Mina's map told its story. The Count's boat must leave the Sereth at the junction by Fundu and enter the Bistritza. We pencilled the turn.")]},
             use_fail="Without Mina's map there is nothing to plot."),
        prop("a6_helm", "column_short", "stone_dark", 4.0, 2.2, name="Helm", radius=0.5,
             look="The wheel. Once all is ready, Lord Godalming will take us upstream at full steam.",
             go="a6_rapids",
             go_cond="flag:a6_stoked&flag:a6_engine_oiled&flag:a6_flag_up&flag:a6_lamp_fitted&flag:a6_course_plotted&flag:a6_fork_known",
             go_fail="We are not ready. Fuel, oil, lamp, flag and chart must all be in order, and we must know which river the boat took."),
        deco("a6_l_barrel", "barrel", "dark", 3.6, -2.4), deco("a6_l_rock", "rock", "dark", -5.5, -2.8),
        deco("a6_l_bench", "bench", "dark", -2.8, 1.2, rot=0),
    ],
    npcs=[
        npc("a6_harker_launch", "human_harker", "travel", -1.4, 1.6, rot=20, name="Jonathan", radius=0.5,
            look="Jonathan keeps watch at the bow, one hand on the kukri hilt. His eyes never leave the water.", talk="a6_harker_launch", cond="!prot:harker"),
        npc("a6_boatman_a", "human_peasant_m", "a6_boatman", 5.0, -2.4, rot=-100, name="Slovak boatman", radius=0.5,
            look="A Slovak on a drifting skiff, his lantern held low and his face turned from the light. He looks at us as at a ghost.", talk="a6_boatmen"),
        npc("a6_boatman_b", "human_peasant_m", "szgany", -5.0, -2.8, rot=100, name="Raftsman", radius=0.5,
            look="A raftsman crouched over his poles. He crossed himself twice when the lamp struck him.", talk="a6_raftsman"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="a6_j_launch")])],
)

LOC_DATA["a6_rapids"] = outdoor(
    [3, 2], "day", floor="a6_water", wall="dirt",
    scatter=dict(asset="rock", variant="dark", count=16, seed=9, avoid=[[-6, -4, 6, 4]]),
    scatter2=dict(asset="pine", variant="green", count=14, seed=15, avoid=[[-7, -5, 7, 5]]),
    spawn=[-4.4, 2.0], spawns={"a6_launch_deck": [-4.4, 2.0]},
    props=[
        prop("a6_wreck_launch", "a6_launch", "default", -0.8, 0.0, rot=70, name="Damaged launch", radius=1.6,
             look="The Mina lies on a shingle spit with a plank sprung amidships. A seam has opened below the waterline."),
        prop("a6_keel", "chest", "ebony", -0.8, 1.6, name="Sprung keel plank", radius=0.6,
             look="The broken plank. It wants a timber splint, rope to lash it and canvas to stop the water. Three things, all of which we carry.",
             use_item={
                 "wood": [dict(take="wood"), dict(set="a6_keel_wood"), dict(say="A length of ash across the break. It is a splint.")],
                 "rope": [dict(take="rope"), dict(set="a6_keel_rope"), dict(say="Rope lashed tight, turn upon turn.")],
                 "cloth": [dict(take="cloth"), dict(set="a6_keel_cloth"), dict(say="Canvas drawn under the seam. The leak slowed to a drip.")],
             }, use_fail="That will not mend the keel."),
        prop("a6_spar", "chest", "oak", 3.8, -2.2, name="Driftwood spar", radius=0.6,
             look="A good straight spar, washed up by the rapids.",
             take="wood", take_text="I dragged the spar up the bank. It will serve as a splint.", give_once=True),
        prop("a6_rapid_sign", "signpost", "dark", -3.2, -2.0, name="Warning post", radius=0.3,
             look="A pole with a red rag, planted by raftsmen. Beyond it the river drops three feet at a time."),
        prop("a6_fire", "fireplace", "soot", 3.0, 2.4, name="Bank fire", radius=0.8,
             look="A farmer's cooking-fire, ringed with stones. His wife offers us tea in a tin cup."),
        deco("a6_r_barrel", "barrel", "dark", 5.0, 0.4), deco("a6_r_cross", "grave_cross", "stone_mossy", -5.2, 2.6),
        deco("a6_r_bench", "bench", "dark", 4.2, 1.4, rot=-90),
    ],
    npcs=[
        npc("a6_farmer", "human_peasant_m", "villager", 4.0, -0.2, rot=-100, name="Farmer", radius=0.5,
            look="A farmer with an acre of sheep above the falls, who has watched our launch grind itself on his rocks with something like sympathy.",
            talk="a6_farmer"),
        npc("a6_harker_rapids", "human_harker", "travel", -2.8, 2.0, rot=30, name="Jonathan", radius=0.5,
            look="Jonathan stands in the shallows with a sodden coat and a stubborn jaw, working the launch off the rocks.",
            talk="a6_harker_rapids", cond="!prot:harker"),
        npc("a6_arthur_rapids", "human_arthur", "lord", 1.8, 2.4, rot=-150, name="Lord Godalming", radius=0.5,
            look="Arthur rolls his sleeves, wet to the elbow, with the look of a man who would sooner fix the boat than think.",
            talk="a6_arthur_rapids", cond="!prot:arthur"),
    ],
    on_enter=[dict(once=True, do=[dict(protagonist="harker"), dict(journal="a6_j_rapids")])],
)

LOC_DATA["a6_bistritz_trail"] = outdoor(
    [3, 2], "dusk", floor="dirt", wall="dirt",
    scatter=dict(asset="pine", variant="snow", count=24, seed=33, avoid=[[-7, -5, 7, 5]]),
    scatter2=dict(asset="rock", variant="grey", count=6, seed=4, avoid=[[-7, -5, 7, 5]]),
    spawn=[-4.4, 2.2], spawns={},
    props=[
        prop("a6_fundu_inn", "inn_sign", "dark", 5.4, -2.6, rot=-90, y=2.4, name="Sign of the Fundu inn", radius=0.2,
             look="A roadside sign swinging in the wind: a crowned eagle, over the legend 'Fundu'. Behind it, the lights of the little inn."),
        prop("a6_trail_post", "signpost", "dark", -1.0, 0.8, name="Fork signpost", radius=0.3,
             look="FUNDU. The Sereth bridge. Bistritza. Someone has scored a fresh knife-mark under the last arm: the Szgany boat turned this way.",
             set="a6_trail_signs", set_text="Fresh cuts in the post and a heap of straw packed under the arm: the Szgany boat put in here at dawn."),
        prop("a6_sledge", "carriage", "dark", 3.6, 1.6, rot=-120, name="Peasant sledge", radius=1.4,
             look="A low sledge on runners, for the road when the snow closes it. 'Russian fashion,' says Quincey."),
        prop("a6_trail_fire", "fireplace", "soot", -3.4, -2.4, name="Wayside fire", radius=0.8,
             look="A smoking fire at the roadside. The horses steam beside it."),
        prop("a6_trail_hay", "barrel", "pale", 1.8, -2.4, name="Hay bale", radius=0.5,
             look="A hay bale, with dry grass for the horses."),
        deco("a6_trail_barrel", "barrel", "dark", 4.2, -1.4), deco("a6_trail_cross", "grave_cross", "stone_dark", -5.3, 1.2),
        deco("a6_trail_lamp", "lantern", "default", 5.0, 0.0),
    ],
    npcs=[
        npc("a6_fundu_keeper", "human_peasant_m", "innkeeper", 3.0, -1.0, rot=-110, name="Fundu innkeeper", radius=0.5,
            look="A woolly-bearded innkeeper at his doorstep, wrapped in sheepskin. He has news for those who sit down and pay.", talk="a6_fundu_keeper"),
        npc("a6_quincey_trail", "human_quincey", "texan", -1.8, 2.0, rot=60, name="Quincey Morris", radius=0.5,
            look="Quincey, mud to his thighs, whittling a stick and watching the clouds. 'Snow by dark, Doc.'", talk="a6_quincey_trail", cond="!prot:quincey"),
        npc("a6_wolf_a", "wolf", "grey", -5.2, -2.6, rot=130, name="Wolf", radius=0.6,
            look="A grey wolf at the edge of the pines, watching us with yellow eyes. There are more behind it.",
            fight="a6_wolf_pack", cond="flag:a6_fundu_news&flag:a6_sledge_hired&flag:a6_trail_signs"),
    ],
    on_enter=[dict(once=True, do=[dict(protagonist="seward"), dict(journal="a6_j_trail")])],
)

# ------------------------------------------------------------------ CHAPTER XXVII: VAN HELSING AND MINA
LOC_DATA["a6_veresti_inn"] = indoor(
    [2, 2], "plaster_dirty", "planks", mood="candle",
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[0.0, 2.8], spawns={},
    props=[
        prop("a6_veresti_door", "door", "dark", 3.8, -2.0, rot=-90, name="Door to the yard", radius=0.7,
             look="The inn yard, where our carriage waits.", go="a6_mountain_road",
             go_cond="has:a6_provisions&has:a6_furs&flag:a6_carriage_bought&flag:a6_wrote_letter",
             go_fail="We are not ready. The Professor must buy the carriage, we need provisions and furs, and I owe Jonathan a letter."),
        prop("a6_veresti_stove", "fireplace", "stone_grey", -2.0, -3.4, name="Tiled stove", radius=0.9,
             look="A great green-tiled stove that warms the whole room. The landlady's cat lives on top of it."),
        prop("a6_provisions_basket", "barrel", "pale", 2.8, 2.4, name="Provision basket", radius=0.5,
             look="A huge covered basket: black bread, smoked sausage, cheese, a flask of plum brandy and a pot of paprika stew in a cloth.",
             take="a6_provisions", take_text="I took the basket. It weighs a stone.", give_once=True),
        prop("a6_furs_hook", "rug", "black", -3.4, 1.4, rot=90, name="Furs on the wall", radius=0.6,
             look="Sheepskin coats, a bear rug and two travelling-furs, hanging on pegs.",
             take="a6_furs", take_text="I took two heavy furs and a rug. We shall be glad of them.", give_once=True),
        prop("a6_garlic_string", "garlic", "default", -3.4, -1.2, name="String of garlic", radius=0.4,
             look="A long plait of garlic on the wall. The landlady says it keeps off 'things'.",
             take="garlic", take_text="I took a plait of garlic; the Professor will be pleased.", give_once=True),
        prop("a6_letter_table", "table", "dark", 0.0, -1.2, name="Writing table", radius=0.8,
             look="A table with a cracked inkwell, and paper. I have a letter to write to Jonathan, which he may never read.",
             set="a6_wrote_letter", set_text="I wrote to Jonathan: 'We are truly in the hands of God.' I put it with the Professor's own dispatch for Lord Godalming."),
        deco("a6_v_bench", "bench", "dark", 1.4, 0.8, rot=90), deco("a6_v_lamp", "candelabra", "default", 0.0, -1.2, y=0.8),
        deco("a6_v_rug", "rug", "red", -0.4, 1.6), deco("a6_v_barrel", "barrel", "dark", 3.2, -2.6),
    ],
    npcs=[
        npc("a6_landlady", "human_peasant_f", "a6_landlady", 1.2, -2.2, rot=170, name="Landlady", radius=0.5,
            look="A large, kind woman who will not look at my forehead and will not stop packing food into my arms.", talk="a6_landlady"),
        npc("a6_vh_veresti", "human_vanhelsing", "vh", -1.0, 0.0, rot=60, name="Prof. Van Helsing", radius=0.5,
            look="The Professor, counting money onto the table, checking horses through the window.", talk="a6_vh_veresti", cond="!prot:vanhelsing"),
    ],
    on_enter=[dict(once=True, do=[dict(protagonist="mina"), dict(journal="a6_j_veresti")])],
)

LOC_DATA["a6_mountain_road"] = outdoor(
    [3, 2], "dusk", floor="a6_snow", wall="a6_snow",
    scatter=dict(asset="pine", variant="snow", count=26, seed=51, avoid=[[-7, -5, 7, 5]]),
    scatter2=dict(asset="rock", variant="grey", count=8, seed=8, avoid=[[-7, -5, 7, 5]]),
    spawn=[-4.4, 2.4], spawns={},
    props=[
        prop("a6_road_carriage", "carriage", "ebony", -2.2, 0.8, rot=70, name="Our carriage", radius=1.7,
             look="The four-in-hand the Professor assembled from the farmers' horses and a farm cart's body. Not elegant, but it has brought us across half the Carpathians."),
        prop("a6_fork_left", "signpost", "dark", 0.6, -2.0, rot=90, name="Left fork", radius=0.3,
             look="Left, a wide cart-road dropping to a valley. Not the way Jonathan described."),
        prop("a6_fork_right", "signpost", "dark", 2.4, -2.4, rot=-60, name="Right fork", radius=0.3,
             look="Right, a narrow track, climbing between rocks. It looks like a sheep-walk."),
        prop("a6_old_road", "signpost", "oak", 4.4, 0.4, rot=-90, name="Old by-road", radius=0.5,
             look="A grass-grown road under the pines, rising towards a black notch in the mountains: the Borgo Pass, and beyond, the castle.",
             go="a6_holy_circle", go_cond="flag:a6_road_known&flag:won:borgo_wolves&has:wild_rose",
             go_fail="Not yet. I must name the road from Jonathan's journal, the wolves must be driven off, and the Professor wants a wild rose for the lid of every grave."),
        prop("a6_dog_rose", "garlic", "default", -4.8, -2.4, name="Wild rose bush", radius=0.5,
             look="A dog-rose, scarlet with hips against the snow. The Professor says it keeps the Un-Dead in their coffins.",
             take="wild_rose", take_text="I cut a sprig of wild rose.", give_once=True),
        prop("a6_road_wood", "chest", "oak", 3.4, 2.6, name="Wayside woodpile", radius=0.6,
             look="A woodpile at a shrine to the Virgin, left for travellers.",
             take="wood", take_text="I took an armful of dry logs for the night's fire.", give_once=True),
        prop("a6_shrine", "crucifix_big", "silver", -5.0, 0.6, name="Wayside crucifix", radius=0.3,
             look="A wooden crucifix under a small tin roof, hung with ribbons and fresh garlic."),
        deco("a6_rd_rock", "rock_big", "grey", 5.4, -2.2, scale=0.8),
    ],
    npcs=[
        npc("a6_road_villager", "human_peasant_f", "village_woman", 0.2, 2.2, rot=170, name="Peasant woman", radius=0.5,
            look="A woman with a basket of eggs. She makes the sign of the horns at my forehead and presses garlic into my palm.", talk="a6_road_villager"),
        npc("a6_vh_road", "human_vanhelsing", "vh", -0.8, 0.2, rot=110, name="Prof. Van Helsing", radius=0.5,
            look="The Professor, with a hand always near his satchel, watching me out of the corner of his eye.", talk="a6_vh_road", cond="!prot:vanhelsing"),
        npc("a6_road_wolf", "wolf_big", "grey", 5.0, -2.8, rot=170, name="Wolf", radius=0.7,
            look="A large grey wolf on the ridge, motionless. Its pack waits behind the rocks.", fight="borgo_wolves"),
    ],
)

LOC_DATA["a6_holy_circle"] = outdoor(
    [3, 2], "night", floor="a6_snow", wall="a6_snow",
    scatter=dict(asset="pine", variant="snow", count=26, seed=61, avoid=[[-7, -5, 7, 5]]),
    scatter2=dict(asset="rock", variant="grey", count=8, seed=17, avoid=[[-7, -5, 7, 5]]),
    spawn=[-4.4, 2.2], spawns={},
    props=[
        prop("a6_castle_far", "castle_keep", "stone_dark", 2.0, -8.5, name="Castle Dracula", radius=0.1,
             look="A black bulk against the stars. Somewhere inside it, three women sleep and wait for dark."),
        prop("a6_ring_site", "rug", "cream", 0.0, 0.4, scale=1.1, name="Ring of trodden snow", radius=1.4,
             look="A circle of trampled snow, wide enough for a woman to sit in with a fire. Here the Professor will make the holy circle.",
             use_item={"host": [dict(set="a6_circle_drawn"), dict(journal="a6_j_circle"),
                                dict(say="Van Helsing crumbled the Host into dust and strewed it round the ring. 'In this circle you are safe, Madam Mina.'")]},
             use_fail="The circle must be drawn with the Sacred Wafer."),
        prop("a6_fire_site", "fireplace", "soot", -2.6, -0.4, name="Fire-site", radius=0.8,
             look="A hollow in the snow ringed by stones, ready for a fire. It must burn all night.",
             use_item={"wood": [dict(take="wood"), dict(set="a6_fire_lit"), dict(say="The fire caught. Sparks rose into the dark, and the snow around us glowed red.")]},
             use_fail="The fire needs wood."),
        prop("a6_branch_a", "deadtree", "grey", -5.0, -2.2, name="Fallen branch", radius=0.5,
             look="A great bough of pine, dry as paper under the snow.",
             take="wood", take_text="I broke a length of wood from the bough.", give_once=True),
        prop("a6_branch_b", "deadtree", "grey", 4.8, 2.4, name="Dead pine", radius=0.5,
             look="A dead pine, snapped by the wind. Its resin will burn for hours.",
             take="wood", take_text="I split off more wood. The fire must last till dawn.", give_once=True),
        prop("a6_circle_cross", "crucifix_big", "silver", 1.9, -0.6, name="Crucifix in the snow", radius=0.3,
             look="A crucifix propped in the snow at the edge of the ring. It is not strictly needed, but the Professor says it does no harm.",
             use_item={"crucifix": [dict(set="a6_circle_blessed"), dict(say="I planted the crucifix at the ring's edge, facing the castle.")]}),
        prop("a6_c_carriage", "carriage", "ebony", -4.6, 0.8, rot=30, name="Our carriage", radius=1.6,
             look="The carriage stands with its horses tethered in the lee. The animals scream if I go near; they have smelt something."),
        deco("a6_c_rock", "rock_big", "grey", 5.4, -1.0, scale=0.9),
        deco("a6_c_lantern", "lantern", "default", 2.8, 2.2),
    ],
    npcs=[
        npc("a6_mina_circle", "human_mina", "mina", 0.0, 0.4, rot=0, name="Mina", radius=0.5,
            look="Mina sits on a fur at the heart of the ring, her shawl drawn tight, her eyes on the black castle and her hands twisting in her lap.",
            talk="a6_mina_circle", cond="!prot:mina"),
        npc("a6_sister_a", "human_bride", "bride1", -3.2, -2.4, rot=30, name="The fair sister", radius=0.5,
            look="A lovely, pale woman in white, her black hair streaming in the wind. She has no footprints in the snow.",
            talk="a6_sisters_tempt", cond="flag:a6_night_fell&!won:brides_wing"),
        npc("a6_sister_b", "human_bride", "bride2", 3.4, -2.6, rot=-30, name="The dark sister", radius=0.5,
            look="A dark sister with red lips and a hungry smile.", talk="a6_sisters_tempt", cond="flag:a6_night_fell&!won:brides_wing"),
        npc("a6_sister_c", "human_bride", "bride3", 0.4, -3.0, rot=0, name="The third sister", radius=0.5,
            look="The third sister, the fairest, reaches towards me. I know that face from Jonathan's journal.",
            talk="a6_sisters_tempt", cond="flag:a6_night_fell&!won:brides_wing"),
        npc("a6_snow_wolf", "wolf", "white", 5.0, 1.0, rot=-100, name="White wolf", radius=0.6,
            look="A white wolf circles the ring at a distance, baring its teeth, but it will not cross the line.", cond="flag:a6_night_fell"),
    ],
    on_enter=[dict(once=True, do=[dict(protagonist="vanhelsing")])],
)

LOC_DATA["a6_castle_gate"] = outdoor(
    [3, 2], "day", floor="cobble", wall="stone_grey",
    walls=dict(north=["wall_4", "wall_door_4", "wall_4"]),
    scatter=dict(asset="pine", variant="snow", count=20, seed=71, avoid=[[-7, -5, 7, 5]]),
    spawn=[0.0, 2.8], spawns={"a6_castle_chapel": [0.0, -2.6]},
    props=[
        prop("a6_chapel_door", "door_big", "ebony", 0.0, -3.8, name="Rusted chapel door", radius=0.9,
             look="A double door, eaten red with rust, the hinges frozen into the stone. It will not move for any hand.",
             go="a6_castle_chapel", go_cond="flag:a6_door_forced", go_fail="The door is rusted shut. It will need a blacksmith's blows.",
             use_item={"hammer": [dict(set="a6_door_forced"), dict(journal="a6_j_castle"),
                                  dict(say="I struck the hinges and the rust flew like blood. At the fifth blow the door groaned and gave.")]},
             use_fail="That will not move the door."),
        prop("a6_main_gate", "arch", "stone_dark", 4.2, -2.6, name="Great gate", radius=0.9,
             look="The castle's main gate, a gaping arch of black stone. A little of the wafer on its sill will keep him from using it.",
             use_item={"host": [dict(set="a6_castle_sealed"), dict(say="I laid a portion of the Host in the gateway. Whatever returns here will find the door shut.")]},
             cond="a6_tomb_sanctified", use_fail="The gate can be sealed with the Wafer."),
        prop("a6_path_down", "signpost", "dark", -4.8, 2.4, rot=90, name="Path to the circle", radius=0.5,
             look="The track down the hill to the circle, where Mina waits. I must bring her away before the afternoon dies.",
             go="a6_hollow", go_cond="flag:a6_castle_sealed", go_fail="Not yet. The castle must be sealed first, so that nothing is left behind me."),
        prop("a6_broken_cross", "crucifix_big", "silver", -3.0, -1.6, name="Broken crucifix", radius=0.3,
             look="A wayside crucifix with its arm sheared off. Someone has pushed it over, and long ago."),
        prop("a6_g_well", "column_short", "stone_mossy", 2.4, 1.0, name="Old well", radius=0.5,
             look="A dry well, choked with snow. I will not look in."),
        prop("a6_g_wreck", "carriage", "dark", 5.0, 2.0, rot=-70, name="Wrecked cart", radius=1.4,
             look="The cart's axle is broken; it has lain here for years. A little straw is still damp underneath."),
        deco("a6_keep_back", "castle_keep", "stone_dark", -1.0, -8.0), deco("a6_g_skull_rock", "rock", "dark", -5.2, -2.4),
        deco("a6_g_fence", "fence", "default", 5.8, -0.4, rot=90), deco("a6_g_column", "column", "stone_dark", -4.0, -3.3),
    ],
    npcs=[],
    on_enter=[dict(once=True, do=[dict(protagonist="vanhelsing")])],
)

LOC_DATA["a6_castle_chapel"] = indoor(
    [3, 2], "stone_dark", "stone_grey", mood="crypt",
    walls=dict(north=["wall_4", "wall_door_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[4.4, 2.0], spawns={"a6_brides_crypt": [0.0, -2.4]},
    props=[
        prop("a6_chapel_exit", "door_big", "ebony", 5.8, 2.0, rot=-90, name="Door to the courtyard", radius=0.9,
             look="The broken door and the pale winter light beyond.", go="a6_castle_gate"),
        prop("a6_crypt_door", "door_big", "dark", 0.0, -3.8, name="Iron door to the vault", radius=0.9,
             look="An iron door, dark and cold, with a small grating. The air that comes through it is sweet and wrong, and tugs at my mind. I must be warded before I go in.",
             go="a6_brides_crypt", go_cond="flag:a6_vh_warded", go_fail="The sweetness of that air is a charm. I must ward myself against it first: garlic or the crucifix.",
             use_item={"garlic_wreath": [dict(set="a6_vh_warded"), dict(say="I hung the garlic wreath on my neck and the sweetness curdled. Only the stone cold remained.")],
                       "crucifix": [dict(set="a6_vh_warded"), dict(say="I held the crucifix before me and the charm shrank to a whisper.")]},
             use_fail="That will not ward against the charm."),
        prop("a6_counts_tomb", "tomb", "stone_tomb", -3.8, -1.2, rot=90, name="The Count's tomb", radius=1.2,
             look="A great tomb, higher than the rest, with the name 'DRACULA' cut in the stone. The lid is off; inside, only a long hollow and a few crumbs of earth. Empty, by day.",
             use_item={"host": [dict(set="a6_tomb_sanctified"), dict(journal="a6_j_tomb"),
                                dict(say="I laid a piece of the Sacred Wafer in the tomb. He will find no rest here, ever again.")]},
             use_fail="Only the Wafer will sterilise this earth.", cond="won:brides_tombs"),
        prop("a6_altar", "chest", "ebony", 1.6, -1.4, name="Altar slab", radius=0.9,
             look="A bare stone-and-wood altar. Years of dust, a rat's nest, and one tarnished candlestick."),
        prop("a6_altar_wood", "bench", "dark", -1.4, 1.2, rot=90, name="Splintered pew", radius=0.7,
             look="A broken pew. One leg is a fine length of oak that might make a stake.",
             take="wood", take_text="I broke off the pew's leg, a stout length of oak.", give_once=True),
        prop("a6_chapel_cross", "crucifix_big", "silver", 3.4, -2.6, name="Old altar cross", radius=0.3,
             look="A battered silver cross at the altar's rear. The stone beneath is clean, as though regularly scrubbed."),
        deco("a6_t1", "tomb", "stone_tomb", -3.8, 1.4, rot=90), deco("a6_t2", "tomb", "stone_tomb", 3.6, 0.4, rot=90),
        deco("a6_col1", "column", "stone_dark", -1.8, -1.0), deco("a6_col2", "column", "stone_dark", 2.6, 1.8),
        deco("a6_sconce", "sconce", "default", 5.6, -1.4, y=1.8), deco("a6_cand", "candelabra", "default", 1.6, -1.4, y=0.8),
        deco("a6_chapel_bench", "bench", "dark", 0.4, 2.4),
    ],
    npcs=[],
    on_enter=[dict(once=True, do=[dict(say="The chapel is silent as a held breath. I must remember: do not look too long at any face in this house.")])],
)

LOC_DATA["a6_brides_crypt"] = indoor(
    [2, 2], "stone_tomb", "stone_dark", mood="crypt",
    walls=dict(north=["wall_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[2.8, -1.4], spawns={"a6_castle_chapel": [3.0, -1.4]},
    props=[
        prop("a6_crypt_exit", "door_big", "dark", 3.8, -2.0, rot=-90, name="Door to the chapel", radius=0.9,
             look="Back to the chapel and the daylight.", go="a6_castle_chapel"),
        prop("a6_tomb_1", "tomb", "stone_tomb", -2.2, -1.8, rot=90, name="First tomb", radius=1.0,
             look="A tomb of white stone, its lid pushed aside. In it, a woman lies in white, her lips red and parted, her breast rising a little. Utterly beautiful, utterly still.",
             talk="a6_vh_fascination"),
        prop("a6_tomb_2", "tomb", "stone_tomb", 0.0, 0.4, rot=0, name="Second tomb", radius=1.0,
             look="A second tomb, lidless. A dark woman sleeps within it, her hair wound over her shoulders like black rope."),
        prop("a6_tomb_3", "tomb", "stone_tomb", -2.2, 1.8, rot=90, name="Third tomb", radius=1.0,
             look="A third tomb. The third woman is fair and flushed, her cheek resting on her hand like a girl asleep."),
        prop("a6_crypt_stake", "chest", "dark", 2.8, 2.4, name="Mason's chest", radius=0.5,
             look="A mason's chest left in the vault. One stout wooden mallet-head remains, and a lump of ash for a stake.",
             take="wood", take_text="I picked up the ash. It will make one more stake if I need it.", give_once=True),
        deco("a6_c_col", "column", "stone_dark", 1.8, -2.4), deco("a6_c_cand", "candelabra", "default", -0.2, 2.6),
        deco("a6_c_rock", "rock", "dark", 3.2, 0.4, scale=0.5),
    ],
    npcs=[
        npc("a6_vault_sister_a", "human_bride", "bride1", -2.2, -1.2, rot=90, name="The fair sister (asleep)", radius=0.5,
            look="The fair sister, eyes shut. Day has made her helpless, and I must not hesitate.",
            fight="brides_tombs", cond="flag:a6_resisted&!won:brides_tombs"),
        npc("a6_vault_sister_b", "human_bride", "bride2", 0.0, 1.0, rot=0, name="The dark sister (asleep)", radius=0.5,
            look="The dark sister, eyes shut, lips curled in her sleep.",
            fight="brides_tombs", cond="flag:a6_resisted&!won:brides_tombs"),
        npc("a6_vault_sister_c", "human_bride", "bride3", -2.2, 2.4, rot=90, name="The third sister (asleep)", radius=0.5,
            look="The third sister, as young-seeming as a girl, one hand under her cheek.",
            fight="brides_tombs", cond="flag:a6_resisted&!won:brides_tombs"),
    ],
)

# ------------------------------------------------------------------ THE FINAL DAY
LOC_DATA["a6_hollow"] = outdoor(
    [3, 2], "day", floor="a6_snow", wall="a6_snow",
    scatter=dict(asset="pine", variant="snow", count=18, seed=81, avoid=[[-7, -5, 7, 5]]),
    spawn=[-4.4, 2.4], spawns={},
    props=[
        prop("a6_boulder_a", "rock_big", "grey", -1.6, -1.8, scale=1.4, name="Great boulder", radius=1.4,
             look="A boulder the size of a haystack. Together with its twin it makes a pocket out of the wind."),
        prop("a6_boulder_b", "rock_big", "grey", 1.8, -1.8, scale=1.3, name="Second boulder", radius=1.3,
             look="A second boulder, lichen-coated. Between the two, a hollow where a woman might shelter."),
        prop("a6_hollow_ring", "rug", "cream", 0.1, -0.4, scale=1.1, name="Floor of the hollow", radius=1.3,
             look="Level ground between the stones. The Professor will draw a ring of Host around it before we rest.",
             use_item={"host": [dict(set="a6_hollow_circle"), dict(say="The Professor drew a new ring, crumb by crumb, around the hollow. 'The wolves will come, Madam Mina. Here they cannot touch you.'")]},
             use_fail="The ring must be drawn with the Wafer."),
        prop("a6_lookout", "rock_big", "mossy", 4.6, 1.4, name="Lookout rock", radius=1.0,
             look="A flat-topped rock with a long view over the plain and the road below. A man with a glass could see every wagon in the valley.",
             use_item={"a6_field_glasses": [dict(set="a6_sighted"), dict(journal="a6_j_hollow"),
                                            dict(say="Through the glasses: a dust-cloud, and in it a leiter-wagon, whipped horses, a ring of horsemen. And, wide on both flanks, four riders closing fast. 'They are racing for the sunset!'")]},
             use_fail="I need a glass to see anything on that plain."),
        prop("a6_h_fire", "fireplace", "soot", -3.6, 1.6, name="Embers", radius=0.7,
             look="The ashes of our morning fire. A few coals still glow."),
        prop("a6_h_chest", "chest", "oak", 3.0, 2.4, name="Food chest", radius=0.5,
             look="A chest of bread and cold meat. We have eaten and drunk a little.",
             take="brandy", take_text="I took a flask of brandy for the cold.", give_once=True),
        deco("a6_h_rock1", "rock", "grey", -5.0, -2.8), deco("a6_h_rock2", "rock", "grey", 5.2, -2.6, scale=0.8),
        deco("a6_h_cross", "grave_cross", "stone_grey", -4.6, -0.4),
    ],
    npcs=[
        npc("a6_mina_hollow", "human_mina", "mina", 0.4, -0.2, rot=-20, name="Mina", radius=0.5,
            look="Mina sits wrapped in furs in the hollow, her face white, her eyes clear. Her scar is still red.",
            talk="a6_mina_hollow", cond="!prot:mina"),
        npc("a6_hollow_horse", "wolf", "black", 5.4, -1.2, rot=-60, name="Wolf", radius=0.6,
            look="A black wolf on the skyline. It will come no closer than the ring.", cond="a6_hollow_circle"),
    ],
    on_enter=[dict(once=True, do=[dict(protagonist="vanhelsing")])],
)

LOC_DATA["a6_snow_plain"] = outdoor(
    [4, 3], "sunset", floor="a6_snow", wall="a6_snow",
    scatter=dict(asset="pine", variant="snow", count=14, seed=91, avoid=[[-9, -7, 9, 7]]),
    scatter2=dict(asset="rock", variant="grey", count=8, seed=12, avoid=[[-9, -7, 9, 7]]),
    spawn=[-6.0, 4.0], spawns={},
    props=[
        prop("a6_wagon", "a6_leiter_wagon", "default", 3.0, -1.0, rot=-90, name="The leiter-wagon", radius=1.8,
             look="A long ladder-wagon, drawn by four lathered horses. On its bed, bound with chains, rides the long box."),
        prop("a6_box_closed", "a6_earth_box", "default", 3.0, -1.0, y=0.75, rot=-90, name="The box", radius=1.0,
             look="A long, iron-bound box. The Szgany ring it with knives. We cannot reach it yet.", cond="!won:szgany_cart"),
        prop("a6_box_open", "a6_earth_box", "default", 3.0, -1.0, y=0.75, rot=-90, name="The box (lid loose)", radius=1.0,
             look="The lid is loose. Under it, in the red light, a man's white face with open red eyes. The sun is a hand's breadth from the mountain.",
             fight="dracula_chase", cond="won:szgany_cart&flag:a6_pos_arthur&flag:a6_pos_seward&flag:a6_pos_quincey&has:a6_sharp_kukri"),
        prop("a6_sun_marker", "grave_cross", "stone_dark", -3.2, -3.2, name="Wayside cross", radius=0.3,
             look="A leaning wayside cross. The sun's last rays strike its arm and throw a long red shadow across the snow."),
        prop("a6_ammo_crate", "chest", "dark", -5.4, 2.4, name="Ammunition satchel", radius=0.5,
             look="A satchel of Winchester cartridges. Arthur keeps handing them round.",
             take="bullet", take_text="I took another handful of cartridges.", give_once=True),
        deco("a6_plain_rock", "rock_big", "grey", -2.8, -4.8, scale=1.2), deco("a6_plain_rock2", "rock_big", "mossy", 7.2, 3.6, scale=0.9),
        deco("a6_far_castle", "castle_keep", "stone_dark", 4.0, -13.0), deco("a6_plain_cross", "grave_cross", "stone_grey", 5.8, 4.2),
        deco("a6_plain_wolf1", "wolf", "grey", 7.0, -3.8, rot=120), deco("a6_plain_wolf2", "wolf", "black", -7.2, -2.6, rot=-70),
    ],
    npcs=[
        npc("a6_arthur_plain", "human_arthur", "lord", -4.6, 1.0, rot=-60, name="Lord Godalming", radius=0.5,
            look="Arthur, hair wild, rifle in hand, eyes fixed on the wagon. He has not slept for six days.", talk="a6_arthur_plain", cond="!prot:arthur"),
        npc("a6_seward_plain", "human_seward", "doctor", -3.2, 3.0, rot=-30, name="Dr. Seward", radius=0.5,
            look="Seward steadies his horse with a hand on its neck and looks for the best angle for a shot.", talk="a6_seward_plain", cond="!prot:seward"),
        npc("a6_quincey_plain", "human_quincey", "texan", -5.2, -1.6, rot=-80, name="Quincey Morris", radius=0.5,
            look="Quincey grips the bowie knife in one hand and his Winchester in the other, grinning like a boy.", talk="a6_quincey_plain", cond="!prot:quincey"),
        npc("a6_szgany_chief", "human_peasant_m", "a6_szgany_chief", 1.0, -3.2, rot=-170, name="Szgany captain", radius=0.5,
            look="A hawk-faced Szgany in a red coat, knife in his fist, who has been paid in gold and fear to bring a box to a castle.", talk="a6_szgany_chief"),
        npc("a6_szgany_a", "human_peasant_m", "szgany", 2.0, 1.6, rot=-170, name="Szgany rider", radius=0.5,
            look="A Szgany rider with a long knife. His lips are white.", fight="szgany_cart"),
        npc("a6_szgany_b", "human_peasant_m", "szgany", 5.0, 1.4, rot=-170, name="Szgany rider", radius=0.5,
            look="Another rider, with a rifle on his back and a bandage round his arm.", fight="szgany_cart"),
        npc("a6_szgany_c", "human_peasant_m", "szgany", 4.6, -3.6, rot=-130, name="Slovak carrier", radius=0.5,
            look="A Slovak carrier in sheepskin, standing at the wagon's tail.", fight="szgany_cart"),
    ],
    on_enter=[dict(once=True, do=[dict(protagonist="harker"), dict(journal="a6_j_final")])],
)

LOC_DATA["a6_sunset_snow"] = outdoor(
    [3, 2], "sunset", floor="a6_snow", wall="a6_snow",
    scatter=dict(asset="pine", variant="snow", count=12, seed=97, avoid=[[-7, -5, 7, 5]]),
    spawn=[-4.0, 2.4], spawns={},
    props=[
        prop("a6_dust_heap", "rock", "grey", 1.8, -1.0, scale=0.5, name="Dust", radius=0.5,
             look="A heap of dry grey dust where the Count fell, already lifting in the wind. His face, as it went, had a look of peace such as I never could have imagined there.",
             set="a6_saw_dust", set_text="I looked at the dust until it was gone. It blew away over the snow, and nothing remained."),
        prop("a6_dropped_bowie", "hammer", "default", 0.2, 0.8, name="Quincey's bowie", radius=0.3,
             look="Quincey's bowie knife, lying where it fell in the snow. The blade is clean."),
        prop("a6_road_home", "signpost", "oak", 4.6, 2.2, name="Road down the valley", radius=0.4,
             look="The road home. A wind has begun to blow from the mountains, as if the whole range had drawn a breath.",
             go="a6_epilogue_study", go_cond="flag:a6_quincey_dead", go_fail="I cannot leave him. Not yet."),
        deco("a6_s_rock", "rock_big", "grey", -4.8, -2.8), deco("a6_s_cross", "grave_cross", "stone_grey", 5.4, -1.6),
        deco("a6_s_wagon", "a6_leiter_wagon", "default", 4.8, -2.8, rot=-100),
    ],
    npcs=[
        npc("a6_quincey_dying", "human_quincey", "texan", -0.8, 0.4, rot=90, name="Quincey Morris", radius=0.5,
            look="Quincey sits against Jonathan's shoulder, one hand pressed to his side. The blood runs through his fingers. He smiles at me.",
            talk="a6_quincey_last"),
        npc("a6_harker_sunset", "human_harker", "harker", -1.8, 0.8, rot=60, name="Jonathan", radius=0.5,
            look="Jonathan kneels in the snow behind Quincey, supporting his head and weeping.", talk="a6_harker_sunset", cond="!prot:harker"),
        npc("a6_arthur_sunset", "human_arthur", "lord", -2.8, -0.6, rot=60, name="Lord Godalming", radius=0.5,
            look="Arthur stands bareheaded, the Winchester lowered, the tears frozen on his face.", cond="!prot:arthur"),
        npc("a6_vh_sunset", "human_vanhelsing", "vh", 0.6, 2.0, rot=180, name="Prof. Van Helsing", radius=0.5,
            look="Van Helsing, on his knees, praying aloud. For once he has no word of learning.", cond="!prot:vanhelsing"),
        npc("a6_seward_sunset", "human_seward", "doctor", -3.0, 1.8, rot=40, name="Dr. Seward", radius=0.5,
            look="Seward's hands move over Quincey's wound by habit. He knows how little it can do.", cond="!prot:seward"),
    ],
    on_enter=[dict(once=True, do=[dict(journal="a6_j_quincey")])],
)

LOC_DATA["a6_epilogue_study"] = indoor(
    [2, 2], "plaster", "planks", mood="day",
    walls=dict(north=["wall_window_4", "wall_window_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_4"]),
    spawn=[0.0, 2.6], spawns={},
    props=[
        prop("a6_bundle", "book", "diary", 0.0, -1.4, y=0.8, name="Bundle of typescript", radius=0.3,
             look="A thick bundle of typed pages, tied with ribbon: every diary, every letter, every telegram. No single authentic document in all of it, only copies. Yet the whole truth.",
             end_text="Seven years ago we all went through the flames; and the happiness of some of us since then is, we think, well worth the pain we endured. Our boy's birthday is the day on which Quincey Morris died, and his mother holds the secret belief that some of our brave friend's spirit has passed into him. We call him Quincey.\n\n'This boy will some day know what a brave and gallant woman his mother is,' said Van Helsing, with the child upon his knee. 'Later on he will understand how some men so loved her, that they did dare much for her sake.'\n\nJONATHAN HARKER.\n\nTHE END.",
             ),
        prop("a6_study_desk", "table_long", "dark", 0.0, -1.4, name="Study desk", radius=1.2,
             look="Jonathan's desk, with a blotter, a Ghoorka knife in a case, and a framed photograph of five men and a woman."),
        prop("a6_study_shelf", "bookshelf", "oak", -3.4, -1.0, rot=90, name="Bookshelf", radius=0.6,
             look="Law books, and on the bottom shelf a boy's picture-books, thumbed to pieces."),
        prop("a6_study_fire", "fireplace", "stone_grey", 2.0, -3.4, name="Hearth", radius=0.8,
             look="A fire burns in the grate. On the mantel stands a small, plain bowie knife, kept clean."),
        prop("a6_bowie_case", "hammer", "default", 2.0, -3.0, y=1.0, name="The bowie", radius=0.2,
             look="Quincey's bowie, in its case, on the mantel. A card reads: 'To Quincey, who is not forgotten.'"),
        deco("a6_study_rug", "rug", "red", 0.0, 1.2), deco("a6_study_chair", "chair", "green", -1.4, 0.4, rot=140),
        deco("a6_study_chair2", "chair", "green", 1.6, 0.6, rot=-140), deco("a6_study_lamp", "candelabra", "default", -2.4, 2.4),
    ],
    npcs=[
        npc("a6_mina_study", "human_mina", "mina", 2.4, 1.6, rot=-110, name="Mina", radius=0.5,
            look="Mina stands by the window, her forehead smooth and clear in the evening light. She watches a little boy chase a ball on the lawn.",
            talk="a6_mina_epilogue", cond="!prot:mina"),
    ],
    on_enter=[dict(once=True, do=[dict(protagonist="harker"), dict(card="Seven years ago we all went through the flames...\n\nAnd the happiness of some of us since then is, we think, well worth the pain we endured.")])],
)

# ================================================================== DIALOGUE
DIALOGUE = {}

# ------------------------------------------------------------------ Varna
DIALOGUE["a6_harbourmaster_varna"] = dict(start="n0", nodes={
    "n0": N("Harbour master", "Another Englishman, and another question about the Czarina Catherine. She is not in my book, sir, and no berth is kept for her.",
            choices=[C("When was she last heard of?", "n1"), C("What ships go astray between the Straits and Varna?", "n2"),
                     C("Thank you. [Leave]", end=True)]),
    "n1": N("Harbour master", "The Dardanelles, the fourth of October, by the telegraph. A slow brig, Roumanian flag, owners in Galatz. Eleven days is long, even for a slow brig.",
            do=[dict(set="a6_harbour_checked")], next="n0"),
    "n2": N("Harbour master", "Ships from the Straits make Varna by the cape, or, if the weather is foul and the captain a Roumanian, they run north for the Danube mouth and Galatz. Nobody tells a Roumanian where to go. If I wanted a ship that would not arrive, I should look at the Danube.",
            do=[dict(set="a6_clue_danube"), dict(set="a6_harbour_checked")], next="n0"),
})

DIALOGUE["a6_sailor_varna"] = dict(start="n0", nodes={
    "n0": N("Greek sailor", "You look for the Czarina? Ach, I would not wish to find her. A fog stood off Kaliakra three nights back, and it moved against the wind.",
            choices=[C("What do you mean, against the wind?", "n1"), C("Have a drop of brandy.", "n2", cond="has:brandy"), C("[Leave]", end=True)]),
    "n1": N("Greek sailor", "I mean a fog does not sail upstream, sir. This one did. My mate saw a ship go into it, and it closed behind her like a door. We made the sign and rowed for shore.",
            next="n0"),
    "n2": N("Greek sailor", "God bless you. A man who offers brandy is a man who knows a bad sea. I tell you, sir: keep a wreath of garlic at the hatch and a candle in the cabin.",
            do=[dict(set="a6_sailor_fog")], next="n0"),
})

DIALOGUE["a6_vh_varna"] = dict(start="n0", nodes={
    "n0": N("Van Helsing", "Madam Mina, the sun is near the horizon; this is the hour. Friend John has the watch, Jonathan the pencil. Are you willing?",
            choices=[C("I am ready, Professor.", "t0"),
                     C("What do the trances tell us, Professor?", "d0", cond="flag:a6_trance1"),
                     C("[Leave]", end=True)]),
    "t0": N("Van Helsing", "Look into my hand. Sleep, Madam Mina. Where are you?",
            choices=[C("What do you hear, Madam Mina?", "t1")]),
    "t1": N("Mina", "I hear water. It is lapping, and rushing, and lapping again. Cool and dark.",
            do=[dict(set="a6_trance_hear")], choices=[C("What else do you hear?", "t2")]),
    "t2": N("Mina", "Wood creaks. Rope strains. There are feet above me, going to and fro, and a bell. Everything is straining as if it wished to be free.",
            do=[dict(set="a6_trance_creak")], choices=[C("Do you feel anything beneath you?", "t3")]),
    "t3": N("Mina", "I am rising and falling. We are moving. The ship is moving, and I am not in her. I am somewhere dry and still, and I feel the motion of her as one feels a heart beat in another's chest.",
            do=[dict(set="a6_trance_move")], next="t4"),
    "t4": N("Van Helsing", "Enough, enough. Wake, Madam Mina. [Her eyes open. She remembers nothing, and I write everything down.]",
            do=[dict(set="a6_trance1"), dict(journal="a6_j_trance1")], next="n0"),
    "d0": N("Van Helsing", "Consider it as the lawyer, the doctor, the metaphysician, all three. Water laps and rushes. A ship creaks and moves. Where is she, friend, and what must we do?",
            choices=[
                C("She is in the harbour. We should wait on the quay.", "d1"),
                C("She is out on the open sea and will reach Varna any day now.", "d2"),
                C("He knows we are at Varna. He will not come where we wait; she may make for the Danube and Galatz, and we must watch the wires.", "d3",
                  cond="journal:a6_j_lloyds&flag:a6_clue_danube&flag:a6_trance1"),
                C("I cannot say. [Leave]", end=True)]),
    "d1": N("Van Helsing", "No. In port a ship does not move. Madam Mina feels motion, hears rushing water. And the harbour master has no berth marked for her. Think again.", next="d0"),
    "d2": N("Van Helsing", "Perhaps, perhaps. But Lloyd's had her at the Straits eleven days ago. A ship of that kind would be here already. Something else holds her. Read the Lloyd's report again and ask the harbour master where a ship may go besides Varna.", next="d0"),
    "d3": N("Van Helsing", "Ah, friend John, that is thinking. He learned through her trance that we are here, and then he cut that thread. Any port but this will do him. We watch every wire, and when the news comes we move.",
            do=[dict(set="a6_ship_missing"), dict(journal="a6_j_deduce"),
                dict(card="We waited. The days of October dragged by, a trance at every sunrise and sunset, and every day a telegram from Lloyd's: 'Czarina Catherine, not reported.' At last, on the twenty-eighth...")],
            end=True),
})

DIALOGUE["a6_mina_hotel"] = dict(start="n0", nodes={
    "n0": N("Mina", "I am quite well. Do not look at me so. I have rested and eaten and I am sorry to be a burden.",
            choices=[C("You asked us for a promise, Mina.", "o1", cond="!a6_oath_renewed"),
                     C("Mina, you know the railways. How do we reach Galatz?", "r0", cond="has:a6_telegram"),
                     C("[Leave]", end=True)]),
    "o1": N("Mina", "I did, and I ask it again, with the sun high and my head clear. If I turn, Arthur, John, all of you: let me not live as that thing. Kill me. Jonathan shall read the Burial Service.",
            choices=[C("I swear it, Mina.", "o3"), C("I... cannot say it.", "o2")]),
    "o2": N("Mina", "You must, dear friend, and soon. It is the one favour I ask. I will ask it every day of this journey until you say it.", next="o1"),
    "o3": N("Mina", "Thank you. Now I am no longer afraid; or no more than I can bear. God keep you all.",
            do=[dict(set="a6_oath_renewed")], end=True),
    "r0": N("Mina", "You forget that I am the train fiend. I always keep the Bradshaw. At what hour does the one train for Galatz leave, do you think?",
            choices=[C("In the afternoon, I suppose.", "r1"),
                     C("Let me consult the Bradshaw. [Open it]", "r2", cond="has:a6_bradshaw"),
                     C("I do not know. [Leave]", end=True)]),
    "r1": N("Mina", "No, dear friend. Look it up before you guess. It is on the table.", next="n0"),
    "r2": N("Mina", "Half-past six in the morning, there is only one train. It arrives in the afternoon. Tell the Professor, and tell Jonathan to sleep.",
            do=[dict(set="a6_train_time"), dict(journal="a6_j_timetable")], end=True),
})

DIALOGUE["a6_harker_kukri"] = dict(start="n0", nodes={
    "n0": N("Jonathan", "I have been at this knife an hour. It was good in Ghoorka hands; it is not good in mine. A dull blade is an insult to what it must do.",
            choices=[C("What does it have to do, Jonathan?", "n1"), C("Is there a whetstone about?", "n2"), C("[Leave]", end=True)]),
    "n1": N("Jonathan", "Cut through the throat of a man who is not a man, and do it clean. I shall be nearest. I mean to be the one.", next="n0"),
    "n2": N("Jonathan", "A fine stone would do wonders. There are chandlers on the quay. If you find one, put it in my hand. I cannot rest until this thing is right.",
            do=[dict(set="a6_wants_whetstone")], next="n0"),
})

DIALOGUE["a6_quincey_hotel"] = dict(start="n0", nodes={
    "n0": N("Quincey", "Well, Doc. We're a long way from the Staked Plains, and the buffalo here wears horns and trousers. Anything on your mind?",
            choices=[C("You swore first, Quincey. Why?", "n1"), C("Have you cartridges to spare?", "n2", cond="!a6_quincey_bullets"), C("[Leave]", end=True)]),
    "n1": N("Quincey", "Because a Texan don't ask a lady twice. Because I loved Lucy, and have lost her, and here's a woman I'd lose my right arm for. Sit down, Doc; this country gets under the skin.", next="n0"),
    "n2": N("Quincey", "Always. Here, take a handful. The Winchester wants feeding, and so do you.",
            do=[dict(give="bullet"), dict(set="a6_quincey_bullets")], next="n0"),
})

DIALOGUE["a6_arthur_hotel"] = dict(start="n0", nodes={
    "n0": N("Arthur", "Lloyd's wires every morning: 'Czarina Catherine, not reported.' It makes me want to take a boat and meet her in the Bosphorus. Is there anything you need from me?",
            choices=[C("What of the ship's owners? We cannot open the box without their consent.", "n1"),
                     C("Is there money for a long chase?", "n2"), C("[Leave]", end=True)]),
    "n1": N("Arthur", "The shippers' agent is at Lloyd's. Courteous, closed, a hard man to move. He'll not consent to open a case on the strength of a good face. You'll want a reason, not a truth. And, I suspect, a compensation.", next="n0"),
    "n2": N("Arthur", "Whatever it takes. I have the purse. I'll not spare a sovereign for my own comfort, but anything that gets us to him faster, I'll buy.", next="n0"),
})

DIALOGUE["a6_porter_talk"] = dict(start="n0", nodes={
    "n0": N("Porter", "Good day, sir. No post, sir. I only wait in case.",
            choices=[C("Any telegram for Lord Godalming?", "n1", cond="flag:a6_ship_missing&!a6_got_telegram"),
                     C("[Leave]", end=True)]),
    "n1": N("Porter", "Yes, sir! Just this minute, from Lloyd's. 'Czarina Catherine reported entering Galatz at one o'clock to-day.'",
            do=[dict(give="a6_telegram"), dict(set="a6_got_telegram"), dict(journal="a6_j_telegram")], end=True),
})

# ------------------------------------------------------------------ Lloyd's
DIALOGUE["a6_lloyds_clerk"] = dict(start="n0", nodes={
    "n0": N("Lloyd's clerk", "Lord Godalming. The usual, sir? 'No news.' I am sorry. It is the same for every ship in the Black Sea. You may consult the register if you wish.",
            choices=[C("What is the last entry for the Czarina Catherine?", "n1"), C("[Leave]", end=True)]),
    "n1": N("Lloyd's clerk", "Passing the Dardanelles, the fourth of October. Roumanian-flagged brig, hull and rigging sound. Since then, nothing; not a signal, not a sighting. If the sea had her we should have a report of wreckage by now.",
            do=[dict(journal="a6_j_lloyds"), dict(set="a6_clerk_asked")], next="n0"),
})

DIALOGUE["a6_shipper_agent"] = dict(start="n0", nodes={
    "n0": N("Shippers' agent", "Lord Godalming, is it? You have asked after a consignment aboard the Czarina Catherine. What, precisely, would you have of me?",
            choices=[
                C("Open the box. It contains a dead man that is not dead.", "n_truth"),
                C("A friend of mine has had a thing stolen, and I think it is in that ship.", "n_story"),
                C("Allow me to show my appreciation for the owners' trouble.", "n_early", cond="has:a6_purse&!a6_story_told"),
                C("The owners will surely forgive some delay for the sake of a friend. Here is something for their trouble.", "n_permit",
                  cond="has:a6_purse&flag:a6_story_told&!a6_permit_got"),
                C("[Leave]", end=True)]),
    "n_truth": N("Shippers' agent", "You will forgive me if I have the door held open. I have heard many reasons for opening cargo. That was the first to make me afraid for your health.", next="n0"),
    "n_story": N("Shippers' agent", "Stolen? That is a serious matter. If the thing is yours, a friend's, I should be glad to see it restored. But the owners will want assurance, and some consideration for delay. Return when you can promise both.",
                 do=[dict(set="a6_story_told")], next="n0"),
    "n_early": N("Shippers' agent", "You mistake me, my lord. I do not take money for nothing. Give me a reason and then we shall discuss recompense.", next="n0"),
    "n_permit": N("Shippers' agent", "Ah. Now we understand each other. I will give you a paper to the Captain and another to our man at Galatz. They will open the box in your presence, and any claim the owners have will be settled between gentlemen.",
                  do=[dict(give="a6_permit"), dict(set="a6_permit_got")], end=True),
})

# ------------------------------------------------------------------ Galatz
DIALOGUE["a6_harbourmaster_galatz"] = dict(start="n0", nodes={
    "n0": N("Harbour master", "The Czarina Catherine? In last night on the tide without a pilot. Moored in the fog, and not a soul on deck till dawn. I have never seen a ship come up the Danube so still. What is your interest, gentlemen?",
            choices=[C("Did anything leave the ship?", "n1"), C("Who handles her cargo?", "n2"), C("[Leave]", end=True)]),
    "n1": N("Harbour master", "A long box, by the first light. Men from Hildesheim's lighter took it ashore. And a very tall thin man in a big coat watched from the wharf-head; I thought he was a foreigner. When I looked again he was gone.",
            do=[dict(set="a6_harbour_g")], next="n0"),
    "n2": N("Harbour master", "Messrs. Mackenzie & Steinkoff, the agents. Their clerk is on the quay by the crates. But the Captain, Donelson, he has the papers. A Scot, and a rough one. You would do well to carry a letter from his owners.", next="n0"),
})

DIALOGUE["a6_ms_clerk"] = dict(start="n0", nodes={
    "n0": N("Clerk", "Messrs. Mackenzie & Steinkoff, gentlemen. What can I do for you? The Captain is aboard; I cannot say more than he allows.",
            choices=[C("I have the Captain's bill of lading. Who is the consignee?", "n1", cond="has:a6_bill_of_lading"),
                     C("What can you tell me about the cargo?", "n2"), C("[Leave]", end=True)]),
    "n1": N("Clerk", "A bill, signed. Yes, I see; Hildesheim, Burgen-strasse 16. He is cautious, sir, and fond of coin. Take this note from my masters; he will see the name of Mackenzie & Steinkoff and perhaps be less difficult.",
            do=[dict(give="a6_ms_letter"), dict(set="a6_ms_asked")], next="n0"),
    "n2": N("Clerk", "A single long box, sir, consigned from Varna. Fifty pounds' worth of earth, they said. I thought it a joke. Hildesheim paid the carriage with an English note and signed for it in his own hand.", next="n0"),
})

DIALOGUE["a6_donelson"] = dict(start="n0", nodes={
    "n0": N("Captain Donelson", "Ye'll be the gentlemen from Varna. I have the shippers' letter. Aye, I can see it. Well, ye may ask what ye like, but dinna expect me to tell ye a pretty story.",
            choices=[C("Tell me about the voyage, Captain.", "n1", cond="has:a6_permit"),
                     C("Show me the bill of lading.", "n3", cond="flag:a6_voyage_told&!a6_bill_got"),
                     C("[Leave]", end=True)]),
    "n1": N("Captain Donelson", "From the day we cleared the Bosphorus the fog came on, and it stayed. Nine days, nae a breath of wind, but we made a sea-mile an hour more than any ship I've seen. The men would na touch the wheel; I stood it myself.",
            choices=[C("What of the box?", "n2")]),
    "n2": N("Captain Donelson", "A long box brought aboard at Varna, by an old man in a great coat. The men crossed themselves at the sight of him. When we sailed they asked to throw it overboard, and I laid a handspike to the loudest. If the Deil did have any luggage aboord the ship, I'm thinkin' it was nane ither than that same!",
            do=[dict(set="a6_voyage_told"), dict(journal="a6_j_donelson")], next="n0"),
    "n3": N("Captain Donelson", "Here it is. Hildesheim's the name, Burgen-strasse 16. And ye'll find a Slovak called Skinsky has the box now. Go canny, gentlemen. That old man was no man.",
            do=[dict(give="a6_bill_of_lading"), dict(set="a6_bill_got")], end=True),
})

DIALOGUE["a6_roumanian_crew"] = dict(start="n0", nodes={
    "n0": N("Sailor", "[He makes the sign of the horns, and mutters in Roumanian.] Strigoi. We carried a strigoi. I would not have sailed if I had known.",
            choices=[C("What did you see on the voyage?", "n1"), C("[Leave]", end=True)]),
    "n1": N("Sailor", "A man who was not there. A tall pale man at the rail at night. We found a mate gone one morning, with a neck like a torn flower. The Captain said he fell. I know what fell.", next="n0"),
})

DIALOGUE["a6_deckhand"] = dict(start="n0", nodes={
    "n0": N("Deckhand", "I scrub, sir, I scrub. It does not take out the smell. Not blood: earth. Earth from a grave. You smell it in the hold.",
            choices=[C("Where did the man go when you docked?", "n1"), C("[Leave]", end=True)]),
    "n1": N("Deckhand", "He went into the box, sir. I was at the rail at dawn and I swear he went in like water in the sand. Then the lid shut. Then Hildesheim's men came.", next="n0"),
})

DIALOGUE["a6_hildesheim"] = dict(start="n0", nodes={
    "n0": N("Hildesheim", "You are English gentlemen. I like English gentlemen; they are always in a hurry, and a hurry is a thing that has a price. What is it that you want?",
            choices=[
                C("I come from Messrs. Mackenzie & Steinkoff, with their letter.", "n1", cond="has:a6_ms_letter"),
                C("The box taken ashore this morning. Where is it?", "n2"),
                C("A Slovak called Skinsky has the box. Can you confirm it, in writing?", "n3", cond="flag:a6_hildesheim_asked"),
                C("[Leave]", end=True)]),
    "n1": N("Hildesheim", "Ah. They are good clients. That makes it easier, although not free. What information do you want?",
            do=[dict(set="a6_hildesheim_asked")], next="n0"),
    "n2": N("Hildesheim", "I had it of a gentleman who signed 'de Ville.' A letter, a fee, and delivery. If I tell, the gentleman is no longer a client. And for a man in my line, a client lost is a thing to be paid for.", next="n0"),
    "n3": N("Hildesheim", "Skinsky is a Slovak, his men take cargo up the river by boat. I gave him the box. For a signature and thumbprint I would put it in writing, but the paper costs.",
            choices=[C("Pay him from the purse.", "n4", cond="has:a6_purse"), C("I have no money. [Leave]", end=True)]),
    "n4": N("Hildesheim", "Excellent. Here is my receipt, with the Slovak's mark. You will find him at the churchyard if he lives. I would not trouble to look in the taverns. Good day, sir. It was a pleasure doing business.",
            do=[dict(give="a6_receipt"), dict(set="a6_hildesheim_done"), dict(journal="a6_j_hildesheim")], end=True),
})

DIALOGUE["a6_priest"] = dict(start="n0", nodes={
    "n0": N("Priest", "A poor Slovak, Petrof Skinsky. They found him at dawn at the churchyard wall. The people say wolves, but we have no wolves in the town. God have mercy on his soul.",
            choices=[C("The wound is too clean for a wolf, Father.", "n1", cond="flag:a6_saw_body"),
                     C("Did he have anything on him?", "n2"),
                     C("May I see the coat, Father?", "n3", cond="flag:a6_priest_hint&!a6_skinsky_done"),
                     C("[Leave]", end=True)]),
    "n1": N("Priest", "You have seen it, then, and you are not afraid to say it. A wolf tears. This was cut, as if by a single great tooth. I have said nothing to the police. They would think me mad. I laid the dead man's coat on the wall; no one has asked for it.",
            do=[dict(set="a6_priest_hint")], next="n0"),
    "n2": N("Priest", "Only a coat. His widow came for it, but she has not the heart to wear it. I laid it by the wall until someone should ask.", next="n0"),
    "n3": N("Priest", "Take it, my son. Something is sewn in the lining. A slip of paper. A boat, and Slovaks, and the river by night. I cannot read what it means. You may. God go with you.",
            do=[dict(give="a6_skinsky_slip"), dict(set="a6_skinsky_done"), dict(journal="a6_j_skinsky")], end=True),
})

DIALOGUE["a6_neighbour"] = dict(start="n0", nodes={
    "n0": N("Neighbour", "He was a good man, Petrof, though he drank. He took money from a foreigner and a big box on a boat. Then in the night he came home white and he said: 'Do not open the door.' In the morning he was in the lane.",
            choices=[C("What did the foreigner look like?", "n1"), C("Where did the boat go?", "n2"), C("[Leave]", end=True)]),
    "n1": N("Neighbour", "Tall. Thin. A long white moustache. A voice like honey. He lifted the great box alone, and Petrof, who could carry a barrel, could not help but stare.", next="n0"),
    "n2": N("Neighbour", "Up the river, by night, with Slovaks at the oars. Petrof said they would not stop till the mountains.", next="n0"),
})

DIALOGUE["a6_mina_memorandum"] = dict(start="n0", nodes={
    "n0": N("Mina", "Jonathan sleeps and the others rest, so I am putting all of it in order. Hildesheim, Skinsky, the Captain's tale; the facts want only a clear head. Help me think it through.",
            choices=[C("Begin the memorandum.", "m0", cond="has:a6_receipt&has:a6_skinsky_slip&flag:a6_voyage_told&!a6_memorandum"),
                     C("Read it back to me.", "m_done", cond="flag:a6_memorandum"),
                     C("We have not yet gathered everything. [Leave]", end=True)]),
    "m0": N("Mina", "He cannot go by sea again; the ship is here, and watched. How would he carry his box from Galatz to the Borgo Pass? By road?",
            choices=[C("By road, in a cart.", "m_road"), C("By rail.", "m_rail"), C("By water.", "m_water")]),
    "m_road": N("Mina", "A cart takes days, and the horses will not abide him; I remember Jonathan's driver. And the receipt names a boat, Skinsky's slip says 'by night'. No, not the road.", next="m0"),
    "m_rail": N("Mina", "Every station is a risk: clerks, officials, customs. The Count must be seen. The slip says a boat. It is not rail.", next="m0"),
    "m_water": N("Mina", "By water. Skinsky's slip, Hildesheim's receipt, the neighbour's account: all speak of a boat, a Slovak crew, and the river by night. It remains: which river?",
            choices=[C("The Pruth, to the north.", "m_pruth"), C("The Sereth, then a tributary to the mountains.", "m_sereth")]),
    "m_pruth": N("Mina", "The Pruth leads away from the Pass. No, the Sereth has the Bistritza, and the Bistritza runs from the Borgo Pass itself, by Jonathan's journal. It must be that.", next="m_water"),
    "m_sereth": N("Mina", "Yes. Up the Sereth, then into the Bistritza, near Fundu. It is the only river that ends at the Count's door. I shall pencil the route on a map.",
            do=[dict(set="a6_memorandum"), dict(journal="a6_j_memorandum")], next="n0"),
    "m_done": N("Mina", "The memorandum: Galatz, the Sereth, the Bistritza, the Borgo Pass. The map is on the table. Now Professor Van Helsing must hear it.", end=True),
})

DIALOGUE["a6_council"] = dict(start="n0", nodes={
    "n0": N("Van Helsing", "Friends, Madam Mina has given us the road. I think we must divide. A launch on the water, riders on the bank, and Madam Mina and myself by rail and carriage to the Pass. Let us make arrangements.",
            choices=[C("Who goes where?", "n1"),
                     C("Jonathan will not agree to his wife's going.", "n2"),
                     C("We are ready. Let us set out.", "n3",
                       cond="flag:a6_memorandum&flag:a6_launch_bought&has:a6_map&has:a6_typescript"),
                     C("Not yet. [Leave]", end=True)]),
    "n1": N("Van Helsing", "Lord Godalming and Jonathan take the steam launch up the Sereth. Dr. Seward and Mr. Morris ride the bank. We go by the 6.30 and the carriage. At the Pass we meet. Each must have what he needs: the dealer in the hall has the launch, the horses, the flag, the lamp.", next="n0"),
    "n2": N("Mina", "Jonathan, I am safest with the Professor. The Count's will no longer holds me, and it is I who can lead the Professor through the castle. You know it. Trust me.", next="n0"),
    "n3": N("Van Helsing", "Then go, God keep you. Madam Mina will write. And, friends: remember that it is the sun that is our friend. He is helpless between sunrise and sunset. Let us not miss it.",
            do=[dict(journal="a6_j_council"), dict(protagonist="arthur"),
                dict(card="30 October, night. The party divides. Lord Godalming and Jonathan board the steam launch 'Mina' and head upstream into the dark. Dr. Seward and Quincey Morris ride the bank. Van Helsing and Mina take the morning train."),
                dict(goto="a6_launch_deck")], end=True),
})

DIALOGUE["a6_dealer"] = dict(start="n0", nodes={
    "n0": N("Dealer", "Lord Godalming has told me you require a steam launch and good horses within three hours. It is possible. For a consideration.",
            choices=[C("Buy the launch, a lamp and a flag.", "n1", cond="has:a6_purse&!a6_launch_bought"),
                     C("Is there a map or chart I might have?", "n2"), C("[Leave]", end=True)]),
    "n1": N("Dealer", "A small steam launch with a boiler of English make, and an electric lamp such as the English navy uses. And here is a Roumanian flag. Fly it at Fundu and the village will think you officials. She is called, I believe, the Mina.",
            do=[dict(give="a6_roumanian_flag"), dict(give="a6_lamp"), dict(set="a6_launch_bought"), dict(set="a6_horses_bought")], next="n0"),
    "n2": N("Dealer", "The lady at the table has a map. She is the only one who has drawn the river as it is, not as the Roumanian government pretends.", next="n0"),
})

# ------------------------------------------------------------------ the rivers
DIALOGUE["a6_harker_launch"] = dict(start="n0", nodes={
    "n0": N("Jonathan", "I will not take my eyes off the water. We must overtake him before the mountains. Every boat on this river is a suspect.",
            choices=[C("You are worried for Mina.", "n1"), C("Do you feel steady?", "n2"), C("[Leave]", end=True)]),
    "n1": N("Jonathan", "She is with the Professor, and the Professor is a good man. And she has asked me to go. But I would give ten years to be in that carriage with her.", next="n0"),
    "n2": N("Jonathan", "When I am working, yes. When I think of that castle, no. I escaped it once. I swore I would never see it again. Now I am running to it. Strange, is it not?", next="n0"),
})

DIALOGUE["a6_boatmen"] = dict(start="n0", nodes={
    "n0": N("Slovak boatman", "[He fell to his knees in the light of the lamp, and prayed.] Do not harm us, gentlemen. We have done nothing. We are poor men.",
            choices=[C("Have you seen a boat with a great box and Szgany at the oars?", "n1", cond="flag:a6_lamp_fitted"),
                     C("Stand up, man. Where is your boat bound?", "n2"),
                     C("[Leave]", end=True)]),
    "n1": N("Slovak boatman", "Yes, gracious sir! Before dusk, a boat with eight men at the oars, a great box in the middle, and in the stern a tall dark man in a cloak. He did not look at us but I felt his eyes. They turned in at the river mouth on the left, up the Bistritza. They did not stop.",
            do=[dict(set="a6_fork_known")], next="n0"),
    "n2": N("Slovak boatman", "Downriver to Galatz with timber, sir. We saw lights and heard a shot and we hid. Please do not tell the Count's men we spoke.", next="n0"),
})

DIALOGUE["a6_raftsman"] = dict(start="n0", nodes={
    "n0": N("Raftsman", "[He crossed himself twice.] If you hunt what I think you hunt, you have courage. I have seen the lights of his boat at the fork, with wolves howling on the bank. They did not harm him.",
            choices=[C("Which fork?", "n1"), C("[Leave]", end=True)]),
    "n1": N("Raftsman", "Where the Bistritza comes into the Sereth, past Fundu. A man who knew the river would go there. And a man with wolves for guards would not need to ask.", next="n0"),
})

DIALOGUE["a6_farmer"] = dict(start="n0", nodes={
    "n0": N("Farmer", "She struck the rock, your boat. I saw it from the field. Sit by the fire. You will need a night and a plank to mend that seam, and horses for the road.",
            choices=[C("Can you spare two horses and a saddle?", "n1", cond="flag:a6_keel_wood&flag:a6_keel_rope&flag:a6_keel_cloth&has:a6_purse"),
                     C("How bad is the river ahead?", "n2"), C("[Leave]", end=True)]),
    "n1": N("Farmer", "For this gold, six. Take the grey and the bay. The road follows the river. Go with God, and do not stop when the wolves howl.",
            do=[dict(set="a6_horses_ready"), dict(protagonist="seward"),
                dict(card="2-3 November. The launch is mended, but the river will carry us no further. Lord Godalming buys horses; he and Jonathan will ride for the mountains. And on the bank, Dr. Seward and Quincey Morris have been in the saddle three days."),
                dict(goto="a6_bistritz_trail")], end=True),
    "n2": N("Farmer", "Rapids for three versts. A rock in each, and the water black. A launch with a sound keel may pass. A launch with a broken one may not.", next="n0"),
})

DIALOGUE["a6_harker_rapids"] = dict(start="n0", nodes={
    "n0": N("Jonathan", "A plank sprung; no more. We need a splint, rope to bind it and canvas to stop the water. We must be on the river by nightfall.", end=True),
})

DIALOGUE["a6_arthur_rapids"] = dict(start="n0", nodes={
    "n0": N("Arthur", "If we cannot mend her we shall ride. But the river is faster, and I'll not give up the Mina while she floats. A spar for the splint, a rope, some canvas; I know what to do.", end=True),
})

DIALOGUE["a6_fundu_keeper"] = dict(start="n0", nodes={
    "n0": N("Innkeeper", "Gentlemen, you are not from here. News is a thing I sell. Bread and brandy first, and then we talk.",
            choices=[C("What news from the river?", "n1"), C("Have you a sledge?", "n2", cond="has:a6_purse&!a6_sledge_hired"), C("[Leave]", end=True)]),
    "n1": N("Innkeeper", "Last night a launch passed, with an English lamp. And the day before, a boat with Szgany, a box, and wolves following on the bank. Both turned up the Bistritza.",
            do=[dict(set="a6_fundu_news")], next="n0"),
    "n2": N("Innkeeper", "A sledge? There will be snow by dark. Take mine. Two horses, a bearskin and sleigh-bells I won't take back. For gold.",
            do=[dict(set="a6_sledge_hired")], next="n0"),
})

DIALOGUE["a6_quincey_trail"] = dict(start="n0", nodes={
    "n0": N("Quincey", "Doc, I've followed a trail in sleet for three days and I never felt so tired or so awake. Mina is ahead, God willing. What's the good word?",
            choices=[C("We must hurry. The sun sets at five.", "n1"), C("I fear for Arthur and Jonathan on the river.", "n2"), C("[Leave]", end=True)]),
    "n1": N("Quincey", "Then we hurry, and Mina does what she has to. I told her once that I'd see the thing through, and I will. Tell the horses.", next="n0"),
    "n2": N("Quincey", "The launch has a lamp and a flag; Arthur's no fool. Let's keep our heads and we'll all meet at the Pass.", next="n0"),
})

# ------------------------------------------------------------------ Veresti and the road
DIALOGUE["a6_landlady"] = dict(start="n0", nodes={
    "n0": N("Landlady", "[She makes the sign of the horns at my forehead, then flushes and pats my hand.] Forgive an old fool, little lady. Here, a bite for the road. Garlic in the soup, and garlic at the door.",
            choices=[C("Why the garlic?", "n1"), C("Is the road to the Pass safe?", "n2"), C("[Leave]", end=True)]),
    "n1": N("Landlady", "Because of what lives up there, lady. In the old castle. You are young, and your husband's journal is no answer. Wear it. Carry it.", next="n0"),
    "n2": N("Landlady", "The road to the Pass is safe by day. By night it belongs to wolves, and to him who calls them. Be across the Pass before dark, or camp in a ring.", next="n0"),
})

DIALOGUE["a6_vh_veresti"] = dict(start="n0", nodes={
    "n0": N("Van Helsing", "Madam Mina, we must have a carriage, horses, and furs. The road above Veresti is rough and the nights are cold. I have gold; let me use it.",
            choices=[C("Buy the carriage and horses.", "n1", cond="has:a6_purse&!a6_carriage_bought"),
                     C("What do you fear most on this road?", "n2"), C("[Leave]", end=True)]),
    "n1": N("Van Helsing", "Done, and well done. Four horses, a stout carriage, and a driver who will take us to the last village and not a yard further. Now furs and provisions, and your letter to Jonathan.",
            do=[dict(set="a6_carriage_bought")], next="n0"),
    "n2": N("Van Helsing", "Not the wolves, Madam Mina, nor even the Un-Dead. I fear that you will be tired, and the Count will find the thread he has lost in you. We must be careful of your sleep.", next="n0"),
})

DIALOGUE["a6_road_villager"] = dict(start="n0", nodes={
    "n0": N("Peasant woman", "[She crosses herself and thrusts garlic into my hand.] Go home, lady. Not past the cross. Dracula's wolves do not eat; they only wait.",
            choices=[C("Which road leads to the castle?", "n1"), C("Thank you for the garlic.", "n2"), C("[Leave]", end=True)]),
    "n1": N("Peasant woman", "None you want. The wide road goes to the valley; the narrow road to the shepherd's hut; the old by-road goes to the Pass, and from there to the devil's house. Your man's book knows it better than I.", next="n0"),
    "n2": N("Peasant woman", "Wear it at your throat, and when you sleep, keep your hands crossed. God keep you.",
            do=[dict(set="a6_garlic_gift")], next="n0"),
})

DIALOGUE["a6_vh_road"] = dict(start="n0", nodes={
    "n0": N("Van Helsing", "Madam Mina, we come to three roads. I know that you have read Jonathan's journal many times. Which of these is the one he took?",
            choices=[C("The wide cart-road, to the left.", "n1"), C("The narrow track, to the right.", "n2"),
                     C("Let me consult Jonathan's typescript.", "n3", cond="has:a6_typescript"),
                     C("[Leave]", end=True)]),
    "n1": N("Van Helsing", "That one goes down into the valley, Madam Mina. Jonathan's coach went up. Read again.", next="n0"),
    "n2": N("Van Helsing", "That goes to a shepherd's hut. Jonathan did not meet a shepherd. Think of the cross and the bend.", next="n0"),
    "n3": N("Mina", "Here: 'the road went up, then down, then up again under tall pines, past a cross at the bend.' It is the old by-road, the grass-grown one beyond the shrine. I know it. Have not my Jonathan travelled it, and wrote of his travel?",
            do=[dict(set="a6_road_known"), dict(journal="a6_j_road")], next="n4"),
    "n4": N("Van Helsing", "Then it is that road. Madam Mina, I must ask you to stay close and to take sleep when you can. Something is changing in you, and I do not want it to take you unawares. First, the wolves; they are waiting.", end=True),
})

# ------------------------------------------------------------------ the holy circle
DIALOGUE["a6_mina_circle"] = dict(start="n0", nodes={
    "n0": N("Mina", "Professor, I feel the snow under me but I do not feel the cold. I only feel that I am drawn to that castle, as a bird to a snake. I am so tired.",
            choices=[
                C("Step into the ring, Mina.", "n1", cond="flag:a6_circle_drawn&!a6_mina_in"),
                C("The night is coming. Let us wait.", "n2", cond="flag:a6_circle_drawn&flag:a6_fire_lit&flag:a6_mina_in"),
                C("What do you feel, Mina?", "n3"),
                C("[Leave]", end=True)]),
    "n1": N("Mina", "I am in. I did not think I could be so glad of a few handfuls of dust. Keep the fire high, Professor. Keep it high.",
            do=[dict(set="a6_mina_in")], next="n0"),
    "n2": N("Mina", "Then we wait. Whatever comes, I shall not leave this circle; I give you my word, and I give it with all the strength I have left.",
            do=[dict(set="a6_night_fell"), dict(card="The sun went down behind the mountain. The cold deepened. The horses began to scream, and from the mist beyond the firelight came a whisper of women's laughter...")],
            end=True),
    "n3": N("Mina", "I feel him in the distance, as one feels a draught under a door. He is not far, and he is not alone. Do not leave me, Professor.", next="n0"),
})

DIALOGUE["a6_sisters_tempt"] = dict(start="n0", nodes={
    "n0": N("The sisters", "Come, sister. Come to us. Come! Come! Why will you not come? We are so cold and the snow is so soft. He sent us, as he sends all his lovelies. Come!",
            choices=[C("[Mina] I will not leave this circle.", "n1"), C("[Mina] Who sent you?", "n2"), C("[Mina] I... can hear you.", "n3")]),
    "n1": N("The sisters", "Brave sister! You are not afraid of us? We are not afraid of you. Give us your hand, only your hand, through the line. One kiss. One only.",
            choices=[C("[Mina] No. Professor, they are here.", "n4"), C("[Mina] Wait... one hand...", "n3")]),
    "n2": N("The sisters", "The Master, our dear Master. He is close. He is racing the sun. Come, and be one with us, and he will be so glad.", next="n1"),
    "n3": N("Van Helsing", "[He raised the Host between her hand and the line.] Madam Mina! You cannot. The circle will hold, but not if you will it open. Look at me, look at the Host.", next="n4"),
    "n4": N("Mina", "[I draw my hand back. The sisters laugh, and wolves begin to howl all around the ring. They cannot enter; but they will try until dawn.]",
            do=[dict(fight="brides_wing")], end=True),
})

# ------------------------------------------------------------------ the vault
DIALOGUE["a6_vh_fascination"] = dict(start="n0", nodes={
    "n0": N("Van Helsing", "[She is lovely beyond description. She seems to breathe, and the colour of her lips is the colour of life. A thing in me longs to kneel and kiss her, and I know what that is: not love, but a trap.]",
            choices=[C("Look away. Use the crucifix.", "n1", cond="has:crucifix"),
                     C("Think of Mina, waiting in the circle.", "n2"),
                     C("Bend to her lips.", "n3")]),
    "n1": N("Van Helsing", "[I hold the crucifix before my eyes. The spell shrinks. She is a thing, not a woman; a beautiful corpse that has fed on the living.]",
            do=[dict(set="a6_resisted")], end=True),
    "n2": N("Van Helsing", "[Somewhere across the snow, Mina cries out my name, and I know the cry is real, or I have imagined it. It cuts the charm like a knife. My hand steadies, my eyes clear.]",
            do=[dict(set="a6_resisted")], end=True),
    "n3": N("Van Helsing", "[I am a hair's breadth from her lips when something in my mind screams: 'You are drowning!' I wrench myself back, shaking, drenched in sweat. I must not look so long.]", next="n0"),
})

# ------------------------------------------------------------------ the hollow and the plain
DIALOGUE["a6_mina_hollow"] = dict(start="n0", nodes={
    "n0": N("Mina", "Professor, the castle is behind us, the three are at peace, and I am myself again, or nearly. But I feel the Count draw near, as the tide draws in. Can you see anything?",
            choices=[C("Stay in the ring. I shall look from the rock.", "n1", cond="!a6_hollow_done"),
                     C("They come. We shall see the end of it, Madam Mina.", "n2", cond="flag:a6_hollow_circle&flag:a6_sighted"),
                     C("[Leave]", end=True)]),
    "n1": N("Mina", "Yes. I shall be quiet. But be careful not to fall; the sun is almost down, and I would not have you late.", next="n0"),
    "n2": N("Van Helsing", "[The glass shakes in my hand.] They are racing for the sunset. We may be too late. God's will be done!",
            do=[dict(set="a6_hollow_done"), dict(protagonist="harker"),
                dict(card="6 November, an hour before sunset. Four men ride on the plain: Jonathan, Lord Godalming, Dr. Seward and Quincey Morris. Before them, a wagon flogged by Szgany whips, and the dying sun."),
                dict(goto="a6_snow_plain")], end=True),
})

DIALOGUE["a6_arthur_plain"] = dict(start="n0", nodes={
    "n0": N("Arthur", "Jonathan, we have them. I will take the right flank with Seward and rifles at the ready. We pick the first man who raises a knife.",
            choices=[C("Hold the right, Arthur. Cover the escort with the rifle.", "n1", cond="!a6_pos_arthur"),
                     C("Steady, man.", "n2"), C("[Leave]", end=True)]),
    "n1": N("Arthur", "Right flank, rifle on the escort. For Lucy, and for Mina. Go.", do=[dict(set="a6_pos_arthur")], next="n0"),
    "n2": N("Arthur", "I am steady. I have never been steadier. God forgive me if I miss.", next="n0"),
})

DIALOGUE["a6_seward_plain"] = dict(start="n0", nodes={
    "n0": N("Seward", "Jonathan, I take the left, wide of the wagon, to keep their horsemen from circling. If I fire at the wolves, they are the lesser danger.",
            choices=[C("Hold the left, Jack. Break the circle if you must.", "n1", cond="!a6_pos_seward"),
                     C("How much ammunition do you have?", "n2"), C("[Leave]", end=True)]),
    "n1": N("Seward", "Left flank, understood. I shall fire over their heads if I can, and between their eyes if I cannot.", do=[dict(set="a6_pos_seward")], next="n0"),
    "n2": N("Seward", "Plenty, and a prayer for each cartridge. We do not need many.", next="n0"),
})

DIALOGUE["a6_quincey_plain"] = dict(start="n0", nodes={
    "n0": N("Quincey", "Jonathan, we two go for the box. You get the throat, I'll get the heart. If either's down, the other does the job. Shake on it.",
            choices=[C("We go together, Quincey. The kukri first, the bowie after.", "n1", cond="!a6_pos_quincey&has:a6_sharp_kukri"),
                     C("Is your side hurting you?", "n2"), C("[Leave]", end=True)]),
    "n1": N("Quincey", "That's a deal, Jonathan. For Lucy, and for the little lady up there. Let's go.", do=[dict(set="a6_pos_quincey")], next="n0"),
    "n2": N("Quincey", "Only a scratch. Don't fuss, Jonathan.", next="n0"),
})

DIALOGUE["a6_szgany_chief"] = dict(start="n0", nodes={
    "n0": N("Szgany captain", "[He looks at us, at the sun, and back at the box.] Gentlemen, the road is closed. This is a poor man's load and a poor man's journey. I am paid by the day.",
            choices=[C("Stand aside. We have no quarrel with you.", "n1"), C("Who is the master you serve?", "n2"), C("[Leave]", end=True)]),
    "n1": N("Szgany captain", "[He spits.] A man who pays in gold and watches me with eyes I do not like. I do not stand aside, English. He made us swear. He will make us die before he lets his box be touched.", next="n0"),
    "n2": N("Szgany captain", "I do not know his name. The Count of the castle, they say. If you come between the Count and his house, you will not see another day.", next="n0"),
})

DIALOGUE["a6_quincey_last"] = dict(start="n0", nodes={
    "n0": N("Quincey", "I am only too happy to have been of any service. Don't cry, little lady. It was a fair fight.",
            choices=[C("Quincey, you are hurt.", "n1"), C("[Mina] Take my hand.", "n1")]),
    "n1": N("Quincey", "[He took my hand in his feeble one, and smiled.] Oh, God! It was worth for this to die! Look! look!",
            next="n2"),
    "n2": N("Mina", "[The sun was now right down upon the mountain top, and the red gleams fell upon my face so that it was bathed in rosy light. The men sank on their knees; a deep and earnest 'Amen' broke from all.]", next="n3"),
    "n3": N("Quincey", "Now God be thanked that all has not been in vain! See! The snow is not more stainless than her forehead! The curse has passed away!",
            do=[dict(set="a6_quincey_dead")], next="n4"),
    "n4": N("Mina", "[And to our bitter grief, with a smile and in silence, he died, a gallant gentleman. I touched my forehead: there was no mark.]",
            do=[dict(journal="a6_j_quincey")], end=True),
})

DIALOGUE["a6_harker_sunset"] = dict(start="n0", nodes={
    "n0": N("Jonathan", "He was braver than any of us, Mina. He was our friend. And I never said so.",
            choices=[C("He knew, Jonathan.", "n1"), C("[Leave]", end=True)]),
    "n1": N("Jonathan", "Let us carry him down together. Wherever we go, whatever we call our children, he will be remembered.", end=True),
})

DIALOGUE["a6_mina_epilogue"] = dict(start="n0", nodes={
    "n0": N("Mina", "He is a lovely boy, Jonathan. He has Quincey's name and, I think, Quincey's laugh. The scar is gone, and so is the fear. Come and read what you have written.", end=True),
})


# ================================================================== COMBAT
ENCOUNTERS_EXTRA = {
    "a6_wolf_pack": dict(name="Wolves on the bank road", time="dusk", enemies=["wolf", "wolf", "wolf_alpha"], flee_ok=True,
                         intro="The howling swells behind us. Yellow eyes show between the pines as the snow begins to fall.",
                         win="The great wolf breaks off, and the pack melts into the dark. The horses stop trembling.",
                         location="a6_bistritz_trail"),
}

ENCOUNTER_HOOKS = {
    "a6_wolf_pack": dict(
        on_win=[dict(set="a6_wolves_beaten"),
                dict(card="Back on 31 October, a day and a half before the launch left Galatz, Van Helsing and Mina Harker had reached Veresti on their way to the Borgo Pass."),
                dict(goto="a6_veresti_inn")],
        on_lose=[dict(say="The pack drove us back into the lee of the sledge. By the grace of God and a flung brand the wolves drew off before dawn. We must hold the road and try again.")],
        on_flee=[dict(say="We wheeled the horses and ran for the inn fire. The wolves lost heart at the lamplight. We must go again.")]),
    "borgo_wolves": dict(
        on_win=[dict(set="a6_road_wolves_gone"), dict(say="The wolves slunk back into the trees. The Professor held his crucifix aloft until the last of them was gone. 'They will not come again before dark,' he said.")],
        on_lose=[dict(say="The wolves drew back at the Professor's crucifix before they could harm us. We are shaken, but whole.")],
        on_flee=[dict(say="We drew in behind the carriage and the wolves lost interest in the horses. For now.")]),
    "brides_wing": dict(
        on_win=[dict(journal="a6_j_sisters"), dict(protagonist="vanhelsing"),
                dict(card="Dawn, 5 November. A cock crowed somewhere far off, and the three white shapes thinned into the snow. The horses were dead in their traces. The Professor lifted Mina out of the ring and set her down, whispering 'Rest. It is over for tonight.' By day he must go up to the castle alone."),
                dict(goto="a6_castle_gate")],
        on_lose=[dict(say="I woke at dawn in the circle. The Professor had held the Host between us and them through the whole night. The fire was embers and the sisters were gone. We must hold the ring until morning.")],
        on_flee=[dict(say="There is no leaving the ring. We stay.")]),
    "brides_tombs": dict(
        on_win=[dict(journal="a6_j_brides"), dict(set="a6_brides_done"),
                dict(say="Stake, then knife. At the last each of them sighed and crumbled to dust, and on each face as it went was a look of peace. I swept the dust from the tombs and prayed.")],
        on_lose=[dict(say="The charm broke me for a moment. I staggered back through the iron door, gasping, and rested against the pew. I must go in again with a steadier heart.")],
        on_flee=[dict(say="I withdrew into the chapel. The sleepers did not stir. I must finish what I came for.")]),
    "szgany_cart": dict(
        on_win=[dict(set="a6_szgany_beaten"), dict(say="The ring of horsemen broke. A rifle bullet took the leader's hat; the others turned and flung themselves on their horses. The box on the wagon is bare to us.")],
        on_lose=[dict(say="The Szgany pressed us back. Arthur's rifle held them at the rim, and we drew breath. We must try again before the sun is down.")],
        on_flee=[dict(say="We fell back behind the rocks. The sun was shaving the mountain-top. There was no time to waste.")]),
    "dracula_chase": dict(
        on_win=[dict(protagonist="mina"),
                dict(card="The lid fell. Jonathan's kukri swept across the throat, and Quincey's bowie plunged into the heart. Before our eyes, and almost in the drawing of a breath, the whole body crumbled into dust and passed from sight. Even in that moment of dissolution there was in the face a look of peace such as I never could have imagined might have rested there. The sun was setting; and Quincey Morris was bleeding to death."),
                dict(goto="a6_sunset_snow")],
        on_lose=[dict(say="We fell back. The sun hung on the mountain's edge like a coin on a table. Jonathan was bleeding but on his feet. Whatever it cost, we would have to go in again.")],
        on_flee=[dict(say="There is no flight. The sun is going. We must end it now.")]),
}

PLACEMENTS = {
    "a6_whetstone": [
        dict(prop="a6_grindstone", text="I pocketed the whetstone. I shall leave a coin on the barrel for the chandler.", hint="A chandler's whetstone lies on its rim."),
        dict(prop="a6_rope_chest", text="Under the rope in the chest lay a flat grey whetstone. I took it.", hint="Something flat and heavy is wedged under the coil."),
        dict(prop="a6_slat_crate", text="Behind the broken slats was a flat grey whetstone, hidden by a careless carter.", hint="A hard grey shape shows between the slats."),
    ],
}

GATES = {}

PALETTES = {
    "a6_hotel_odessa": [dict(wall="plaster", floor="planks"), dict(wall="plaster_dirty", floor="planks")],
    "a6_hildesheim_office": [dict(wall="plaster_dirty", floor="planks"), dict(wall="stone_grey", floor="planks")],
    "a6_castle_chapel": [dict(wall="stone_dark", floor="stone_grey"), dict(wall="stone_mossy", floor="stone_dark")],
}
