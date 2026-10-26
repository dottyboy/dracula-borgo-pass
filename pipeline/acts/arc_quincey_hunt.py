"""Personal arc: The Texan's Hunt (Quincey P. Morris). A frontier horse-hunt in Texas, then the night on the Pampas when a bat bled his mare Santa Fe."""
from dsl import *


# ------------------------------------------------------------------ helpers
def deco(id, asset, variant, x, z, rot=0, scale=1.0, y=0.0):
    return prop(id, asset, variant, x, z, rot=rot, scale=scale, y=y, radius=0.01)


def N(speaker, text, **kw):
    return dict(speaker=speaker, text=text, **kw)


def C(text, next=None, **kw):
    d = dict(text=text)
    if next:
        d["next"] = next
    d.update(kw)
    return d


def hv(**over):
    return human_colors(**over)


def outdoor(cells, mood, floor="grass", wall="dirt", fire=None, **kw):
    if mood == "day":
        amb, lights, extra = AMBIENT["day_exterior"], lights_day(), {}
    elif mood == "dusk":
        amb, lights, extra = AMBIENT["dusk_exterior"], lights_warm(cells, n=1, energy=2.0) + lights_moon(1.6), {}
    else:
        amb, lights, extra = AMBIENT["night_exterior"], lights_moon(), dict(night=True, moon=dict(pos=[14, 17, -22]))
    if fire:
        lights = lights + [dict(pos=[fire[0], 1.2, fire[1]], color="#ff8a40", energy=3.2, range=9)]
    d = dict(cells=cells, interior=False, wall=wall, floor=floor, ambient=amb, camera=cam(cells), lights=lights)
    d.update(extra)
    d.update(kw)
    return d


Q = "Quincey"
P = "quincey_hunt_"

# ------------------------------------------------------------------ ARC
ARC = dict(
    id="quincey_hunt", title="The Texan's Hunt", member="quincey", portrait="quincey",
    blurb="Horse-thieves on the Brazos, a mare called Santa Fe, and a night on the Pampas when something drank where no bat should. "
          "Quincey Morris's own story, of the years before he ever met a vampire.",
    unlock="roster:quincey", unlock_text="Meet Quincey Morris (Act II).", after_credits=False,
    start=dict(location="quincey_hunt_ranch", protagonist="quincey", party=["quincey"],
               items={"knife": 1, "winchester": 1}, flags=[]),
    exit_to="ARC_END",
    rewards=[dict(give="buffalo_coat"), dict(give="winchester")] + [dict(give="bullet")] * 10 + [
        dict(give="quincey_hunt_sheath"), dict(stat=dict(member="quincey", acc=3, hp=2, eva=1))],
    rewards_text="A second Winchester, ten cartridges, Quincey's tooled bowie sheath; +3 Accuracy, +2 HP, +1 Evasion for Quincey Gear: a buffalo coat.",
)

LOCATIONS = [
    dict(id="quincey_hunt_ranch", name="The Morris ranch, Brazos country, Texas", date="Spring, 1884",
         desc="Dawn on the home corral. The rail is cut clean through, the remuda is gone, and an old hand sits on an upturned bucket holding his head."),
    dict(id="quincey_hunt_stable", name="The stable", date="Spring, 1884",
         desc="Warm, dim and smelling of hay and saddle-soap. One stall stands empty, with a name painted on a board above it."),
    dict(id="quincey_hunt_prairie", name="The open range", date="Spring, 1884",
         desc="Grass to the sky in every direction, a water-hole, and a trail that wants reading before it rains."),
    dict(id="quincey_hunt_creek", name="The cottonwood bottoms", date="Spring, 1884, dusk",
         desc="Slow brown water under leaning trees. Somewhere in the reeds, something is breathing."),
    dict(id="quincey_hunt_thief_camp", name="Dunning's camp", date="Spring, 1884, night",
         desc="A fire in a hollow, horses on a picket-line, and one white-socked paint mare pulling at her rope."),
    dict(id="quincey_hunt_pampas_camp", name="Camp on the Pampas", date="The winter of 1885, Argentina",
         desc="Grass to the horizon, one supply-wagon, and a fire of dung and thistle-stalk. Arthur is cleaning his gun, Seward is writing, and the gaucho is looking at the sky."),
    dict(id="quincey_hunt_pampas_night", name="The horse lines", date="The same night",
         desc="A moon without a cloud, tall silent grass, and the picketed horses stamping uneasily at nothing."),
    dict(id="quincey_hunt_pampas_dawn", name="The grass at dawn", date="The next morning",
         desc="The wind has dropped. The grass is bright, and everything wrong lies in it."),
]

# ------------------------------------------------------------------ appearance variants
VARIANTS = {
    "quincey_hunt_horse": {
        "default": "paint",
        "paint": {"fur": T("fur", "#a8764a"), "dark": T("fur", "#2a1c14"), "leather": T("leather", "#4a3020")},
        "bay": {"fur": T("fur", "#5a3622"), "dark": T("fur", "#140c08"), "leather": T("leather", "#2a1c14")},
    },
    "human_peasant_m": {
        "quincey_hunt_wash": hv(top=T("cloth", "#8a8a7a"), bottom=T("wool", "#3a3a40"), hair=T("hair", "#c8c4b8"), accent=T("cloth", "#6a1a1a")),
        "quincey_hunt_trapper": hv(top=T("fur", "#5a4a38"), bottom=T("wool", "#4a3a2a"), hair=T("hair", "#8a8070"), skin=T("skin", "#b88d68")),
        "quincey_hunt_drover": hv(top=T("cloth", "#9a4a28"), bottom=T("wool", "#2a2a3a"), hair=T("hair", "#1a1210"), skin=T("skin", "#b8825a")),
        "quincey_hunt_rustler": hv(top=T("cloth", "#3a3a30"), bottom=T("wool", "#2a2620"), hair=T("hair", "#4a3a2a"), accent=T("cloth", "#8a2020")),
        "quincey_hunt_dunning": hv(top=T("cloth", "#1a1a1a"), bottom=T("wool", "#26221e"), hair=T("hair", "#0e0a0a"), accent=T("cloth", "#c9a248")),
        "quincey_hunt_gaucho": hv(skin=T("skin", "#a8794f"), top=T("cloth", "#e0d8c8"), bottom=T("wool", "#3a2a22"), accent=T("cloth", "#8a2418"), hair=T("hair", "#0e0a0a")),
    },
    "human_peasant_f": {
        "quincey_hunt_cook": hv(skin=T("skin", "#c89a70"), top=T("cloth", "#3a5a8a"), accent=T("cloth", "#e0d8c8"), hair=T("hair", "#1a1210")),
    },
}
ASSETS = [dict(id="quincey_hunt_horse", builder="quincey_hunt_horse", params={})]

# ------------------------------------------------------------------ LOCATION DATA
LOC_DATA = {
    # ---------------------------------------------------------------- the ranch
    "quincey_hunt_ranch": outdoor(
        [3, 3], "day", floor="dirt", wall="planks",
        walls=dict(north=["wall_4", "wall_door_4", "wall_4"]),
        scatter=dict(asset="rock", variant="grey", count=8, seed=5, avoid=[[-6, -6, 6, 6]]),
        spawn=[0, 3.5], spawns={"quincey_hunt_stable": [0, -4.2], "quincey_hunt_prairie": [4.6, 0.5]},
        on_enter=[dict(once=True, do=[dict(card="Brazos country, Texas. Spring, 1884.")])],
        props=[
            prop("quincey_hunt_d_barn", "door_big", "oak", 0, -5.8, name="Barn door", look="The big double door of the stable, propped open on a bar.",
                 go="quincey_hunt_stable", radius=0.9),
            prop("quincey_hunt_corral_rail", "fence", "default", -5.2, -1.0, rot=90, name="Cut corral rail",
                 look="The top rail has been sawn through, not broken. Whoever did it came with a file and patience, and the dogs never barked.",
                 set="quincey_hunt_saw_rail", set_text="Sawn, and sawn quietly. Wash's dogs were fed first: there are bits of meat in the dust. This was planned.", radius=0.7),
            deco("quincey_hunt_fence2", "fence", "default", -5.2, -3.0, rot=90),
            deco("quincey_hunt_fence3", "fence", "default", -5.2, 1.0, rot=90),
            deco("quincey_hunt_fence4", "fence", "default", -5.2, 3.0, rot=90),
            prop("quincey_hunt_chest_tack", "chest", "dark", -4.4, -3.8, name="Tack chest", look="Bridles, girths and a coil of good manila rope.",
                 take="rope", take_text="A fifty-foot lariat, Wash's best. I coil it over my shoulder.", give_once=True, radius=0.6),
            prop("quincey_hunt_trough", "barrel", "oak", 3.6, -3.8, name="Water trough", look="A half-barrel of rainwater. The horses were watered here last night. Now there are no horses.", radius=0.6),
            prop("quincey_hunt_bench", "bench", "oak", 3.0, 3.2, name="Saddle bench", look="Where Santa Fe's saddle usually rests. It is bare. I feel it in my chest.", radius=0.7),
            prop("quincey_hunt_cooktable", "table", "pale", -3.4, 3.4, name="Cook's table", look="A pan of corn bread under a cloth, and a note: 'Eat something before you go, Mr. Quincey. Maria.'", radius=0.8),
            npc("quincey_hunt_wash", "human_peasant_m", "quincey_hunt_wash", -2.4, -1.2, rot=30, name="Wash Tolliver",
                look="The ranch foreman, sixty if a day, with a bloody rag tied to his scalp.", talk="quincey_hunt_wash"),
            npc("quincey_hunt_cook", "human_peasant_f", "quincey_hunt_cook", -4.2, 2.0, rot=90, name="Maria the cook",
                look="She wrings her apron and crosses herself every time she looks at the empty corral.", talk="quincey_hunt_cook"),
            prop("quincey_hunt_gate_range", "signpost", "oak", 5.0, 0.5, rot=-90, name="Gate to the open range",
                 look="The east gate, and beyond it nothing but grass and a long day's riding.", go="quincey_hunt_prairie", radius=0.7,
                 go_cond="has:bullet&flag:quincey_hunt_powder_ready", go_fail="Wash is right. I will not ride out against Dunning's gang with an empty rifle. Powder and lead, and the loading bench in the stable."),
            prop("quincey_hunt_lantern_post", "lantern", "default", 4.4, -4.6, name="Yard lantern", look="Burnt down to the wick. It was dark when the thieves came."),
            deco("quincey_hunt_dead1", "deadtree", "grey", -5.6, 5.0, scale=0.9),
            deco("quincey_hunt_rockA", "rock_big", "grey", 5.4, 4.6),
        ],
    ),
    # ---------------------------------------------------------------- the stable (interior)
    "quincey_hunt_stable": dict(
        cells=[2, 2], interior=True, wall="planks", floor="dirt", ambient=AMBIENT["candle_interior"], camera=cam([2, 2]),
        lights=lights_warm([2, 2]),
        walls=dict(north=["wall_4", "wall_door_4"], west=["wall_4", "wall_window_4"], east=["wall_4", "wall_4"]),
        spawn=[1.5, 2.0], spawns={"quincey_hunt_ranch": [2, -2.4]},
        props=[
            prop("quincey_hunt_d_stable", "door", "oak", 2, -3.8, name="Door to the yard", look="Daylight and a cold draught.", go="quincey_hunt_ranch", radius=0.8),
            prop("quincey_hunt_bench_load", "table", "dark", -1.0, -2.6, name="Loading bench",
                 look="A vise, a powder-measure and a bullet-mould. Lead is cast here into slugs, and slugs are charged with powder to make cartridges.",
                 use_item={"quincey_hunt_lead": [dict(take="quincey_hunt_lead"), dict(give="quincey_hunt_slugs"), dict(journal="quincey_hunt_j_load"),
                                                 dict(say="I melt the lead over the lamp and pour it into the mould. Ten neat slugs lie cooling on the bench.")],
                           "quincey_hunt_powder": [dict(take="quincey_hunt_powder"), dict(set="quincey_hunt_powder_ready"),
                                                   dict(say="I measure the black powder into the brass cases, grain by grain, as my father taught me.")],
                           "quincey_hunt_slugs": [dict(take="quincey_hunt_slugs")] + [dict(give="bullet")] * 10 + [dict(set="quincey_hunt_cartridges"),
                                                  dict(say="I seat the slugs in the cases and crimp them with the vise. Ten cartridges for the Winchester.")]},
                 use_fail="That does not belong on the loading bench.", radius=0.9),
            prop("quincey_hunt_target", "signpost", "oak", 2.6, 1.4, rot=90, name="Target post",
                 look="Wash's old shooting post. Years of misses lie buried in the wood.",
                 take="quincey_hunt_lead", take_text="I dig the spent slugs out with the bowie and tap them into a lump. Enough lead for a few good cartridges.", give_once=True, radius=0.6),
            prop("quincey_hunt_shelf", "bookshelf", "dark", -3.4, -1.2, rot=90, name="Tack shelf", look="Saddle-soap, hoof-oil, harness buckles.", radius=0.7),
            prop("quincey_hunt_feed", "barrel", "oak", -3.2, 1.6, name="Feed barrel", look="Oats. The lid has been put back askew.", radius=0.5),
            prop("quincey_hunt_harness_chest", "chest", "dark", 0.2, -3.2, name="Harness chest", look="Collars and breeching, smelling of leather and old sweat.", radius=0.6),
            prop("quincey_hunt_stall", "bench", "pale", -3.0, 3.0, rot=90, name="Santa Fe's stall",
                 look="Her name, painted on a board by a boy of fifteen. The straw is still pressed in the shape of her.",
                 take="quincey_hunt_blanket", take_text="Her saddle-blanket, worn soft, still smelling of her. I fold it under my arm.", give_once=True, radius=0.7),
            prop("quincey_hunt_letter_table", "table", "pale", 1.2, 2.4, name="Wash's table",
                 look="A tin cup, a pipe, and a letter with a Buenos Aires stamp.",
                 take="quincey_hunt_letter", take_text="Arthur's hand. I pocket it. It can be read later.", give_once=True, radius=0.7),
            prop("quincey_hunt_stable_lamp", "lantern", "default", 3.4, -2.8, name="Hanging lamp", look="A hurricane lamp swinging from a nail."),
            deco("quincey_hunt_hay", "barrel", "dark", 3.2, 3.0),
        ],
    ),
    # ---------------------------------------------------------------- the open range
    "quincey_hunt_prairie": outdoor(
        [4, 3], "day", floor="grass", wall="dirt",
        scatter=dict(asset="rock", variant="mossy", count=10, seed=21, avoid=[[-8, -6, 8, 6]]),
        scatter2=dict(asset="deadtree", variant="grey", count=5, seed=22, avoid=[[-8, -6, 8, 6]]),
        spawn=[-6.0, 0.5], spawns={"quincey_hunt_creek": [6.2, 0.0]},
        props=[
            prop("quincey_hunt_back_ranch", "signpost", "oak", -7.0, 0.5, rot=90, name="Back to the ranch", look="A day's ride home, or a quarter of one when you are in a hurry.",
                 go="quincey_hunt_ranch", radius=0.6),
            prop("quincey_hunt_sign_shoes", "rock", "grey", -3.5, -2.5, scale=0.5, name="Hoofprints in the mud",
                 look="A string of horses crossed here, walking close, loose-herd pace. Santa Fe's own print is among them: unshod behind. Where the tracks leave the water-hole they bend east, toward low ground.",
                 set="quincey_hunt_read_shoes", set_text="East, then. They did not hurry, which means they feel safe: low ground, soft going, no sky-line.", radius=0.6),
            prop("quincey_hunt_sign_fire", "fireplace", "soot", -1.0, -4.0, scale=0.6, name="Dead camp-fire",
                 look="A ring of stones and cold white ash. Cottonwood: light, fast-burning, no coal. There is no cottonwood within fifteen miles of here except one place.",
                 set="quincey_hunt_read_fire", set_text="Cottonwood ash. They burn what they find in the creek bottoms, and they were there a night ago.", radius=0.7),
            prop("quincey_hunt_sign_cloth", "fence", "default", 4.0, -3.0, rot=40, name="Thorn bush with red cloth",
                 look="A scrap of red flannel snagged on a thorn, burrs of canebrake clinging to it. Canebrake grows only in wet ground.",
                 set="quincey_hunt_read_cloth", set_text="Red flannel with canebrake burrs: a man who has ridden through the bottoms and lately.", radius=0.7),
            prop("quincey_hunt_trails", "signpost", "dark", 1.5, 1.8, name="The three trails",
                 look="Where the water-hole's paths diverge: north to the Cap Rock, east to the cottonwood bottoms, south across the mesquite flat.",
                 talk="quincey_hunt_trails", radius=0.7),
            prop("quincey_hunt_waterhole", "rug", "blue", 0.0, -0.8, scale=1.2, name="The water-hole", look="Muddy water, tracked all round by cattle and, lately, by horses."),
            prop("quincey_hunt_creek_post", "signpost", "oak", 7.0, 0.0, rot=-90, name="East, toward the bottoms",
                 look="The trail runs downhill into a green line on the horizon: cottonwood.", go="quincey_hunt_creek", radius=0.6,
                 go_cond="flag:quincey_hunt_trail_known", go_fail="I do not know which way they went. Three trails, and I have only one chance to be right. Read the signs first."),
            npc("quincey_hunt_hobbs", "human_peasant_m", "quincey_hunt_trapper", -2.6, 3.4, rot=-30, name="Old Hobbs", look="A trapper in a buckskin coat, whittling at nothing.",
                talk="quincey_hunt_hobbs"),
            npc("quincey_hunt_tomas", "human_peasant_m", "quincey_hunt_drover", 5.0, 3.6, rot=200, name="Tomas the drover", look="A Tejano drover sitting his horse, watching the horizon with the patience of his people.",
                talk="quincey_hunt_tomas"),
            deco("quincey_hunt_skull", "rock", "grey", 3.0, 4.6, scale=0.35),
        ],
    ),
    # ---------------------------------------------------------------- the cottonwood bottoms
    "quincey_hunt_creek": outdoor(
        [3, 3], "dusk", floor="dirt", wall="dirt",
        scatter=dict(asset="deadtree", variant="grey", count=12, seed=31, avoid=[[-6, -6, 6, 6]]),
        scatter2=dict(asset="rock", variant="mossy", count=8, seed=32, avoid=[[-6, -6, 6, 6]]),
        spawn=[-4.6, 3.0], spawns={"quincey_hunt_thief_camp": [0, -4.6]},
        props=[
            prop("quincey_hunt_snag", "deadtree", "grey", -0.5, -1.5, scale=1.2, name="Leaning cottonwood snag",
                 look="A dead cottonwood leaning far out over the deep channel, with a stub like a hook on its limb. The ford is a swimming-hole; the far bank is firm.",
                 use_item={"rope": [dict(take="rope"), dict(set="quincey_hunt_crossed"), dict(journal="quincey_hunt_j_creek"),
                                    dict(say="I send the loop over the stub on the second throw, make fast, and swing across hand over hand, the way we did as boys. The far bank is firm and my boots are dry.")]},
                 use_fail="The channel is too deep and cold to swim with a rifle. Something to throw over that snag, perhaps?", radius=0.9),
            npc("quincey_hunt_wolf1", "wolf", "grey", 2.4, -2.4, rot=-40, name="Wolf pack",
                look="Two gaunt grey wolves, hunger-mad after a dry season. They have noticed me.", fight="quincey_hunt_wolves"),
            deco("quincey_hunt_wolf2", "wolf", "grey", 3.4, -1.4, rot=-70),
            prop("quincey_hunt_saddlebag", "chest", "dark", -4.4, -2.8, name="Drowned saddlebag",
                 look="Half sunk in the mud, with the buckles still done up. Whoever lost it was in a hurry.",
                 take="quincey_hunt_spur", take_text="A big silver Mexican spur, engraved with a P. Someone from Dunning's gang, called Pike, lost it at the ford.", give_once=True, radius=0.6),
            prop("quincey_hunt_cattail", "bench", "dark", 4.4, 3.4, name="Rotten log", look="Frogs are loud under it.", radius=0.6),
            prop("quincey_hunt_carcass", "rock_big", "dark", -3.6, 0.8, name="Dead calf", look="A calf with Wash's brand, killed for meat and left to the buzzards. They are not even trying to hide it any more.", radius=0.8),
            prop("quincey_hunt_ford", "signpost", "dark", 0.0, -5.2, name="The east bank trail",
                 look="Fresh horse-dung and the smell of woodsmoke. Dunning's camp is close.", go="quincey_hunt_thief_camp",
                 go_cond="flag:quincey_hunt_crossed&flag:quincey_hunt_wolves_down",
                 go_fail="The wolves are between me and the water, and the channel is too deep to swim. First deal with the wolves, then find a way across.", radius=0.7),
            prop("quincey_hunt_creek_back", "signpost", "oak", -5.2, 3.8, rot=90, name="Back to the range", look="The way I came.", go="quincey_hunt_prairie", radius=0.6),
            deco("quincey_hunt_creek_rock", "rock_big", "mossy", 4.6, 0.8),
        ],
    ),
    # ---------------------------------------------------------------- the thieves' camp
    "quincey_hunt_thief_camp": outdoor(
        [3, 3], "night", floor="dirt", wall="dirt", fire=[0, 0],
        scatter=dict(asset="deadtree", variant="grey", count=8, seed=41, avoid=[[-6, -6, 6, 6]]),
        spawn=[0, 4.6], spawns={},
        props=[
            prop("quincey_hunt_thief_fire", "fireplace", "soot", 0.0, 0.0, scale=0.8, name="Camp fire", look="Cottonwood embers. A coffee-pot and a bottle of mescal beside it.", radius=0.7),
            npc("quincey_hunt_dunning", "human_peasant_m", "quincey_hunt_dunning", 1.2, -1.8, rot=180, name="Black Jack Dunning",
                look="The leader. A black coat, a hat set square, and hands that never leave his belt.", talk="quincey_hunt_dunning", cond="!flag:quincey_hunt_rustlers_down"),
            npc("quincey_hunt_sentry", "human_peasant_m", "quincey_hunt_rustler", -2.8, 1.0, rot=130, name="Dozing rustler",
                look="He leans on a saddle, snoring through a three-day beard.", talk="quincey_hunt_sentry", cond="!flag:quincey_hunt_rustlers_down"),
            npc("quincey_hunt_santafe_camp", "quincey_hunt_horse", "paint", -3.6, -3.0, rot=60, name="Santa Fe",
                look="My mare, dancing on her picket, ears flat, sweat on her flanks. She has seen me.", talk="quincey_hunt_santafe_camp",
                use_item={"quincey_hunt_sugar": [dict(take="quincey_hunt_sugar"), dict(set="quincey_hunt_mare_calm"),
                                                 dict(say="She takes the lump with her soft lips, and the shaking stops. 'Hey, little girl. Easy. I'm here.'")]}),
            prop("quincey_hunt_picket", "fence", "default", -4.4, -3.0, rot=0, name="Picket line",
                 look="A rawhide line staked between two posts. Santa Fe has pulled it taut and left the skin raw.",
                 use_item={"knife": [dict(set="quincey_hunt_mare_loose"), dict(say="One stroke of the bowie and the line falls slack. She tosses her head once, and stays where she stands, which is how I know she trusts me.")]},
                 use_fail="The knot is wet rawhide, hard as iron. A blade would be better than my fingers.", radius=0.7),
            deco("quincey_hunt_bay1", "quincey_hunt_horse", "bay", -4.2, -1.0, rot=70),
            deco("quincey_hunt_bay2", "quincey_hunt_horse", "bay", -4.6, 0.6, rot=100),
            prop("quincey_hunt_loot", "chest", "ebony", 4.2, -2.4, name="Stolen goods",
                 look="Saddles with other men's brands, a ship's chronometer, a dozen watches.",
                 take="quincey_hunt_running_iron", take_text="A running-iron: the thieves' tool for turning one brand into another. Evidence enough for any sheriff.", give_once=True, radius=0.6),
            prop("quincey_hunt_thief_wagon", "carriage", "dark", 3.8, 2.2, rot=-40, name="Thieves' wagon", look="A chuck-wagon full of other people's cattle ropes.", radius=1.2),
            deco("quincey_hunt_thief_rock", "rock_big", "dark", -5.0, 4.4),
        ],
    ),
    # ---------------------------------------------------------------- the Pampas camp
    "quincey_hunt_pampas_camp": outdoor(
        [3, 3], "dusk", floor="grass", wall="dirt", fire=[0, -0.5],
        scatter=dict(asset="rock", variant="grey", count=6, seed=51, avoid=[[-6, -6, 6, 6]]),
        spawn=[0, 4.6], spawns={"quincey_hunt_pampas_night": [-4.6, 0]},
        props=[
            prop("quincey_hunt_campfire", "fireplace", "soot", 0.0, -0.5, scale=0.8, name="Camp fire",
                 look="A dung fire in a ring of stones, a kettle, and a place for a man to talk.", talk="quincey_hunt_tale", radius=0.8),
            npc("quincey_hunt_arthur", "human_arthur", "lord", -2.4, -2.4, rot=20, name="Arthur Holmwood", look="Young, fair, cleaning his rifle with a tenderness he should keep for people.",
                talk="quincey_hunt_arthur"),
            npc("quincey_hunt_seward", "human_seward", "doctor", 2.4, -2.6, rot=-20, name="Jack Seward", look="Notebook on his knee, spectacles in his hand, and no sleep in his eyes.",
                talk="quincey_hunt_seward"),
            npc("quincey_hunt_anselmo", "human_peasant_m", "quincey_hunt_gaucho", 4.2, 0.8, rot=-90, name="Anselmo the gaucho",
                look="Our guide, bow-legged, smoking a corn-husk cigarette. He has not looked at the fire once; he looks at the sky.", talk="quincey_hunt_anselmo"),
            npc("quincey_hunt_santafe_pampas", "quincey_hunt_horse", "paint", -4.4, 1.6, rot=80, name="Santa Fe", look="She came all the way from Texas on a steamer. She has never once complained.",
                talk="quincey_hunt_santafe_camp2"),
            prop("quincey_hunt_woodpile", "barrel", "dark", -4.8, -3.8, name="Thistle and dung stack", look="Dry thistle-stalk and cattle-dung: the only fuel for a hundred miles.",
                 take="wood", take_text="A bundle of thick, dry thistle-stalks. They burn long and smoke thickly.", give_once=True, radius=0.6),
            prop("quincey_hunt_supply", "chest", "oak", 4.6, -4.0, name="Supply chest", look="Biscuit, jerked beef, a flask of lamp oil.",
                 take="oil", take_text="A tin of lamp oil, a little more than a pint.", give_once=True, radius=0.6),
            prop("quincey_hunt_wagon", "carriage", "oak", 3.2, -4.8, rot=180, name="Supply wagon", look="Canvas hood, iron tyres, and a seat worn smooth.", radius=1.2),
            prop("quincey_hunt_tent", "bed_simple", "green", -3.0, -4.6, name="Canvas tent", look="Three men to a tent, in theory.", radius=0.9),
            prop("quincey_hunt_roll", "bench", "pale", 1.6, 3.2, name="Saddle-roll", look="My saddle, my blankets and, for tonight, a rifle at hand.", radius=0.7),
            prop("quincey_hunt_horse_lines", "signpost", "oak", -6.8, 0.0, rot=90, name="Horse lines",
                 look="Where the horses are picketed for the night, out in the tall grass.", go="quincey_hunt_pampas_night",
                 go_cond="flag:quincey_hunt_tale_told&flag:quincey_hunt_anselmo_warned",
                 go_fail="Not yet. I want to hear what the gaucho has to say first, and to sit by the fire a while with the others.", radius=0.7),
            deco("quincey_hunt_pcamp_rock", "rock_big", "grey", 5.4, 4.6),
        ],
    ),
    # ---------------------------------------------------------------- the horse lines (night)
    "quincey_hunt_pampas_night": outdoor(
        [3, 3], "night", floor="grass", wall="dirt",
        scatter=dict(asset="rock", variant="grey", count=5, seed=61, avoid=[[-6, -6, 6, 6]]),
        spawn=[4.6, 0], spawns={},
        props=[
            prop("quincey_hunt_firepit", "fireplace", "soot", 0.0, 0.0, scale=0.7, name="Fire-pit at the lines",
                 look="A shallow pit between the picket-posts. Dry grass would burn out in minutes, but something thick and smoky would burn till dawn.",
                 use_item={"wood": [dict(take="wood"), dict(set="quincey_hunt_smoke_lit"),
                                    dict(say="I pile the thistle-stalks in the pit and light it. A thick white smoke rolls across the lines. Bats do not like smoke, Anselmo says; it stings their noses.")]},
                 use_fail="It needs fuel that burns slow and smokes thick.", radius=0.7),
            prop("quincey_hunt_lamp_post", "signpost", "oak", -3.2, -1.4, name="Picket-post",
                 look="A stout post. A lantern hung high on it would light the whole of the lines.",
                 use_item={"quincey_hunt_lantern": [dict(take="quincey_hunt_lantern"), dict(set="quincey_hunt_lamp_hung"),
                                                    dict(say="I hook the lantern on the nail at the top of the post, where its light will fall on every horse.")],
                           "oil": [dict(take="oil"), dict(set="quincey_hunt_lamp_oiled"),
                                   dict(say="I fill the font, trim the wick and strike a match. A white steady flame fills the glass.")]},
                 use_fail="A lantern hung high would keep a wide ring of light, with oil in the font. The post is waiting.", radius=0.6),
            npc("quincey_hunt_santafe_night", "quincey_hunt_horse", "paint", -2.0, -2.8, rot=40, name="Santa Fe",
                look="She stands head-down, nostrils wide, shifting from hoof to hoof as if the ground itself were uneasy.", talk="quincey_hunt_santafe_camp2",
                use_item={"quincey_hunt_blanket": [dict(take="quincey_hunt_blanket"), dict(set="quincey_hunt_mare_covered"),
                                                   dict(say="I throw her own saddle-blanket over her neck and withers, knot it under her throat, and tuck in the corners. 'There, girl. Nothing gets in under that.'")]},
                use_fail="She needs something over her neck: a blanket she knows."),
            deco("quincey_hunt_other_horse1", "quincey_hunt_horse", "bay", 2.4, -3.0, rot=-60),
            deco("quincey_hunt_other_horse2", "quincey_hunt_horse", "bay", 3.6, 1.6, rot=-110),
            prop("quincey_hunt_bedroll", "bench", "pale", 2.0, 2.4, name="My bedroll", look="Where I will not be sleeping tonight. My Winchester lies across it.", talk="quincey_hunt_watch", radius=0.7),
            prop("quincey_hunt_back_camp", "signpost", "oak", 6.8, 0.0, rot=-90, name="Back to the fire", look="The glow of the camp, two hundred yards off through the grass.",
                 go="quincey_hunt_pampas_camp", radius=0.6),
            deco("quincey_hunt_night_rock", "rock", "grey", -5.0, 4.0),
        ],
    ),
    # ---------------------------------------------------------------- dawn
    "quincey_hunt_pampas_dawn": outdoor(
        [3, 3], "day", floor="grass", wall="dirt",
        scatter=dict(asset="rock", variant="grey", count=5, seed=71, avoid=[[-6, -6, 6, 6]]),
        spawn=[0, 4.6], spawns={},
        props=[
            npc("quincey_hunt_santafe_dawn", "quincey_hunt_horse", "paint", -1.0, 0.0, rot=90, name="Santa Fe",
                look="She stands, but only just, trembling, grey about the lips. There is a small neat wound at her neck, and her blanket is stained.",
                talk="quincey_hunt_santafe_dawn", cond="!flag:quincey_hunt_mare_gone"),
            npc("quincey_hunt_seward_dawn", "human_seward", "doctor", 2.0, -1.8, rot=-30, name="Jack Seward", look="Kneeling in the grass with his bag open.",
                talk="quincey_hunt_seward_dawn"),
            npc("quincey_hunt_arthur_dawn", "human_arthur", "lord", -3.8, -2.4, rot=30, name="Arthur Holmwood", look="Pale, silent, holding the mare's halter-rope out of habit.",
                talk="quincey_hunt_arthur_dawn"),
            prop("quincey_hunt_ring", "rug", "green", 3.6, 1.8, scale=1.2, name="Flattened ring in the grass",
                 look="A circle of grass pressed flat, about the size of a cartwheel, with every blade lying one way as though some great creature had wheeled and risen from it. The grass in the middle is dead, grey and brittle.",
                 set="quincey_hunt_read_ring", set_text="No beast sleeps in a circle. A bat would hang, not trample. Something stood here, and then rose.", radius=0.9),
            prop("quincey_hunt_earth", "rug", "black", -3.4, 2.6, scale=0.7, name="Scatter of dark earth",
                 look="A handful of black, dry soil, dropped on the green. There is no black soil within a hundred miles of the Pampas; the ground here is red clay.",
                 set="quincey_hunt_read_earth", set_text="Alien earth: someone carried it here. Something that cannot rest without it?", radius=0.7),
            prop("quincey_hunt_print", "rug", "cream", 0.6, 3.6, scale=0.5, name="A line of bare prints",
                 look="Long bare footprints, human in shape, that cross the grass and stop between the picket-posts. They do not return. They begin again at the ring.",
                 set="quincey_hunt_read_print", set_text="It walked in, and it did not walk out. The prints stop and the bat begins.", radius=0.7),
            prop("quincey_hunt_dead_bat", "bat", "black", 1.6, 2.2, scale=1.3, name="Dead bat",
                 look="A bat the size of a hen. One wing is broken. It is the only part of last night I understand.",
                 take="quincey_hunt_bat_wing", take_text="I cut off the wing, as a proof for Seward, who will say it needs a better word than 'bat'.", give_once=True, radius=0.6),
            prop("quincey_hunt_grave", "grave_cross", "stone_grey", 4.4, -2.4, name="Santa Fe's grave",
                 look="A mound of red clay under a cross of picket-posts. A last blanket of grass will cover it by spring.", talk="quincey_hunt_final",
                 cond="flag:quincey_hunt_mare_gone", radius=0.8),
        ],
    ),
}

# ------------------------------------------------------------------ DIALOGUE
DIALOGUE = {
    # ---- the ranch
    "quincey_hunt_wash": dict(start="n0", nodes={
        "n0": N("Wash", "Mornin', Mr. Quincey. Dunning's crowd come in the night. Sawed the rail, took the whole remuda, eleven head, and your Santa Fe along with 'em. I got this for sayin' no.",
                choices=[C("Who would dare?", "n_who", cond="!flag:quincey_hunt_wash_told"),
                         C("Where do I start?", "n_start"),
                         C("Any sugar? She'll want something sweet.", "n_sugar", cond="!flag:quincey_hunt_got_sugar"),
                         C("Rest, Wash. I'll bring them home.", end=True)]),
        "n_who": N("Wash", "Black Jack Dunning, who else? He's been running the brakes of the Brazos since the drought, cattle first, now horses. The rail was filed so quiet the dogs never barked. He fed them first.",
                   do=[dict(set="quincey_hunt_wash_told"), dict(journal="quincey_hunt_j_stolen")], next="n0"),
        "n_start": N("Wash", "Tracks leave by the east gate onto the range. But don't you ride out with an empty cylinder. Powder's up in the stable somewhere. I hid it out of the damp, so look sharp. Lead you can dig out of the old target post. Cast the lead and charge the cases at the loading bench and you'll have your rounds, and the rope you'll want is in my tack chest.",
                     do=[dict(set="quincey_hunt_wash_hint"), dict(journal="quincey_hunt_j_load")], next="n0"),
        "n_sugar": N("Wash", "Santa Fe'd follow you to Mexico for a lump. Cook keeps it in the tin. Here.",
                     do=[dict(give="quincey_hunt_sugar"), dict(set="quincey_hunt_got_sugar")], next="n0"),
    }),
    "quincey_hunt_cook": dict(start="n0", nodes={
        "n0": N("Maria", "I heard them, Señor Quincey. A horse blew twice near the barn and I thought it was the wind. I should have gone out. I should have gone out with the lamp.",
                choices=[C("Maria, it was not your doing.", "n1"), C("Which way did you hear them go?", "n2"), C("[Leave]", end=True)]),
        "n1": N("Maria", "You are kind. Eat the corn bread. A man who tracks hungry makes foolish choices.", next="n0"),
        "n2": N("Maria", "East, toward the creek bottoms. That is all I know. And a man laughing. A laugh like a saw.", next="n0"),
    }),
    # ---- the open range
    "quincey_hunt_hobbs": dict(start="n0", nodes={
        "n0": N("Hobbs", "Morning. You look like a man who lost a horse.",
                choices=[C("Eleven, and my mare. Seen any riders?", "n_r"), C("What about the creek?", "n_w"), C("[Leave]", end=True)]),
        "n_r": N("Hobbs", "Three riders came through at dusk yesterday, driving a string of loose horses. They had a pretty paint mare at the tail, fighting her rope. They headed for the low country. There is only one low country around here.",
                 do=[dict(set="quincey_hunt_hobbs_told")], next="n0"),
        "n_w": N("Hobbs", "Wolves are thick down there since the dry year. If you find the channel too deep to cross, there is an old cottonwood snag that leans halfway over it, with a stub on the limb. A good lariat will do the rest. I crossed that way in '71.",
                 do=[dict(set="quincey_hunt_hobbs_creek"), dict(journal="quincey_hunt_j_hobbs")], next="n0"),
    }),
    "quincey_hunt_tomas": dict(start="n0", nodes={
        "n0": N("Tomas", "My grandfather read the grass like a book. 'A man who is hunted leaves marks that are not on the ground,' he said. 'Look at ash, at cloth, at hooves, and wait.'",
                choices=[C("Good advice. Thank you.", end=True), C("Where did he learn that?", "n1")]),
        "n1": N("Tomas", "From the Comanches, who stole his horses. Everyone learns from whoever is stealing their horses.", next="n0"),
    }),
    "quincey_hunt_trails": dict(start="n0", nodes={
        "n0": N(Q, "Three trails leave the water-hole: north to the Cap Rock, east to the cottonwood bottoms, south across the mesquite flat. Dunning's men and my mare took one of them. I can't afford to guess.",
                choices=[C("North, over the Cap Rock.", "n_n"),
                         C("South, across the mesquite flat.", "n_s"),
                         C("East, down to the cottonwood bottoms.", "n_right",
                           cond="flag:quincey_hunt_read_shoes&flag:quincey_hunt_read_fire&flag:quincey_hunt_read_cloth"),
                         C("East? I would like some proof from the hoofprints first.", "n_need", cond="!flag:quincey_hunt_read_shoes"),
                         C("East? I would like some proof from the ashes first.", "n_need", cond="!flag:quincey_hunt_read_fire"),
                         C("East? I would like some proof from the thorn bush first.", "n_need", cond="!flag:quincey_hunt_read_cloth"),
                         C("[Not yet]", end=True)]),
        "n_n": N(Q, "Nothing up there but bare stone. A rustler doesn't drive eleven horses where there is no water and no cover.", next="n0"),
        "n_s": N(Q, "Mesquite would flay the horses' hides. Not a single hair on those thorns. Whoever went through here didn't drive horses through it.", next="n0"),
        "n_need": N(Q, "A hunch is a poor thing to ride on. There are three signs on this ground: the hoofprints at the water-hole, the dead camp-fire, and a bush with something snagged on it. Read all three, then choose.", next="n0"),
        "n_right": N(Q, "Hoofprints turning east to low ground, cottonwood ash, canebrake burrs on red flannel. All three agree: the bottoms. They think they are safe in the reeds. I'll show them different.",
                     do=[dict(set="quincey_hunt_trail_known"), dict(journal="quincey_hunt_j_signs")], end=True),
    }),
    # ---- the creek
    # ---- the camp
    "quincey_hunt_sentry": dict(start="n0", nodes={
        "n0": N("Rustler", "(snores) ... Jack says the paint is worth four hundred in Fort Worth. Four hundred dollars... (snores)",
                choices=[C("Tip his hat over his eyes and go on.", end=True), C("Listen a while longer.", "n1")]),
        "n1": N("Rustler", "... don't tell Pike I lost his spur ... damn river ... (snores)", do=[dict(set="quincey_hunt_sentry_heard")], end=True),
    }),
    "quincey_hunt_dunning": dict(start="n0", nodes={
        "n0": N("Dunning", "Well, if it ain't the Morris boy, come all the way down to the bottoms for a pony. Sit. Have a drink. The mare's a fine one. I may keep her.",
                choices=[C("Give her up, Dunning. Ride away and I'll let you.", "n_ask"),
                         C("[Show him Pike's spur]", "n_spur", cond="has:quincey_hunt_spur"),
                         C("[Show him the running-iron]", "n_iron", cond="has:quincey_hunt_running_iron"),
                         C("Then I'll take her myself.", "n_fight")]),
        "n_ask": N("Dunning", "Ride away? We are three to your one, and you are in my camp. You come mighty bold for a rancher's son.", next="n0"),
        "n_spur": N("Dunning", "(his eyes narrow) Pike's spur. You've been down at the ford, then. Well. That settles it. Nobody leaves who's seen the bottoms.", do=[dict(set="quincey_hunt_dunning_shaken")], next="n0"),
        "n_iron": N("Dunning", "My iron! You went through my... (his hand slides toward his belt) That is a hanging matter, Morris. Once I put you under the cottonwoods, there's no one to say it.", do=[dict(set="quincey_hunt_dunning_shaken")], next="n0"),
        "n_fight": N(Q, "I came for my mare, and for the others. You can hand them over, or I'll take them out of your hands.", do=[dict(fight="quincey_hunt_rustlers")], end=True),
    }),
    "quincey_hunt_santafe_camp": dict(start="n0", nodes={
        "n0": N(Q, "Easy, girl. It's me. It's Quincey.",
                choices=[C("Whistle the three notes she knows.", "n_whistle"),
                         C("Ride her out of here, now.", "n_ride", cond="flag:quincey_hunt_rustlers_down&flag:quincey_hunt_mare_loose&flag:quincey_hunt_mare_calm"),
                         C("What stops me from riding her out?", "n_hint"),
                         C("[Step back]", end=True)]),
        "n_whistle": N(Q, "Her ears swing round. She knows. She has known me since she was a wet-legged foal and I was a boy of fifteen with a bucket of oats. But there is a raw wild look in her eye. The picket has galled her, and the fire has frightened her.",
                       do=[dict(set="quincey_hunt_mare_known")], next="n0"),
        "n_hint": N(Q, "Dunning and his men still hold the camp. Her picket-line has to be cut, and she's too wild with fright to carry a man. A lump of sugar would settle her faster than any words of mine.", next="n0"),
        "n_ride": N(Q, "Up she comes under me. We go out of the hollow at a gallop, with the wind in our faces, and the horses of the remuda running behind us, as if there'd never been any other life.",
                    do=[dict(journal="quincey_hunt_j_reunion"),
                        dict(card="One year later. The Pampas of Argentina, winter 1885. Arthur Holmwood and Jack Seward, my friends, had asked me to hunt with them in the south. Santa Fe came too."),
                        dict(goto="quincey_hunt_pampas_camp")], end=True),
    }),
    # ---- the Pampas camp
    "quincey_hunt_arthur": dict(start="n0", nodes={
        "n0": N("Arthur", "Quincey! Come and sit. Seward says the fire will do us good. Anselmo says it will bring the bats. They cannot both be right.",
                choices=[C("What are you cleaning that for?", "n1"), C("Do you hear the horses?", "n2"), C("How is the hunt?", "n3"), C("[Leave]", end=True)]),
        "n1": N("Arthur", "My father says a gentleman should never let a gun go unattended for a night. My father has never been within a thousand miles of the Pampas.", next="n0"),
        "n2": N("Arthur", "They have been restless since sunset. Anselmo says it is nothing. Anselmo says it is nothing the way a man says 'it is nothing' while looking at the sky.", next="n0"),
        "n3": N("Arthur", "We have seen rhea, guanaco and a puma at a distance. We have not seen what Anselmo keeps warning me about, which I suspect is the only sensible policy.", next="n0"),
    }),
    "quincey_hunt_seward": dict(start="n0", nodes={
        "n0": N("Seward", "I am writing up the day's notes. Tell me, Quincey, did you know that Darwin recorded bats biting horses on this very continent? A small incision, and the animal bleeds a little at the neck.",
                choices=[C("A little? That doesn't sound serious.", "n1"),
                         C("Have you any bandage to spare?", "n2", cond="!flag:quincey_hunt_got_bandage"),
                         C("[Leave]", end=True)]),
        "n1": N("Seward", "No. Darwin says the horse is only inconvenienced. But Darwin did not say how many nights it might continue. I would not leave a horse uncovered.", do=[dict(set="quincey_hunt_seward_warned")], next="n0"),
        "n2": N("Seward", "A roll, from my own bag. I'd keep the rest for Arthur, who thinks pain is a form of bad manners.", do=[dict(give="bandage"), dict(set="quincey_hunt_got_bandage")], next="n0"),
    }),
    "quincey_hunt_anselmo": dict(start="n0", nodes={
        "n0": N("Anselmo", "Señor. The horses are afraid. They smell the thing that comes. You see how the stars are clear? It is a clear night. A night for the vampiro.",
                choices=[C("What can a man do against a bat?", "n1"), C("The bats here are only bats.", "n2"), C("[Leave]", end=True)]),
        "n1": N("Anselmo", "Three things, Señor. First, smoke: the vampiro hates it. A fire of something that smokes thick, thistle, not dung. Second, light: a lantern hung high, so he will not come out of the dark. Third, a cloth over the neck of the animal, a cloth it knows, because the bat goes for the bare skin, always the neck.",
                do=[dict(set="quincey_hunt_anselmo_warned"), dict(journal="quincey_hunt_j_anselmo")], next="n0"),
        "n2": N("Anselmo", "Bats, Señor, are small. The thing that comes here, when it comes, has no size at all. I have seen a steer drained white by morning, without a mark you could put a finger in. (He crosses himself.) Smoke, light, cloth.",
                do=[dict(set="quincey_hunt_anselmo_warned"), dict(journal="quincey_hunt_j_anselmo")], next="n0"),
    }),
    "quincey_hunt_tale": dict(start="n0", nodes={
        "n0": N("Arthur", "A story, Quincey. We have an hour before bed and nothing to look at but stars. Tell us one of yours.",
                choices=[C("The night I bought Santa Fe.", "n_sf"),
                         C("The Marquesas, and the shark that ate my hat.", "n_marq"),
                         C("Titicaca, and the boat that sank in a calm.", "n_tit"),
                         C("[Not now]", end=True)]),
        "n_sf": N(Q, "She was a three-day foal in a Comanche pony-herd, and I was fifteen, with six dollars and a tin of sardines. The old chief said the foal was marked for a short life, born under a falling star. I said I would take the risk. I've had her ever since. The one horse in the world who knows what I am thinking before I do.",
                  do=[dict(set="quincey_hunt_tale_told"), dict(journal="quincey_hunt_j_tale")], next="n_after"),
        "n_marq": N(Q, "We were becalmed off the Marquesas for eleven days. I'd lost my hat to a shark by Tuesday and my temper to a missionary by Friday. But the pearls... boys, you never saw such pearls. And not one of them mine.",
                    do=[dict(set="quincey_hunt_tale_told"), dict(journal="quincey_hunt_j_tale")], next="n_after"),
        "n_tit": N(Q, "The boat sank in a flat calm, boys, at four thousand feet above the sea. I never learned why, and the Indians never told. But I learned that you can swim in cold water as long as you like, if the alternative is Bolivia.",
                   do=[dict(set="quincey_hunt_tale_told"), dict(journal="quincey_hunt_j_tale")], next="n_after"),
        "n_after": N("Seward", "Excellent, Quincey. Though if you ever write it down, I will insist on correcting the medical details.", next="n_after2"),
        "n_after2": N("Arthur", "To Quincey! And to the friends one makes when one has no business being friends.", end=True),
    }),
    "quincey_hunt_santafe_camp2": dict(start="n0", nodes={
        "n0": N(Q, "(Santa Fe lays her head on my shoulder, nostrils wide.) You feel it too, girl. Something's wrong in the air.",
                choices=[C("Stroke her neck.", "n1"), C("[Leave her]", end=True)]),
        "n1": N(Q, "Her skin shivers under my hand. She has never been like this, not at the pass, not in the storm off Cape Horn. If I were a praying man I would start now.", end=True),
    }),
    # ---- the night
    "quincey_hunt_watch": dict(start="n0", nodes={
        "n0": N(Q, "The moon is as bright as a coin. The grass is tall enough to hide a man. I've sat watch over cattle in a norther, over a sick friend in Panama. Tonight I'll sit over a horse.",
                choices=[C("Begin the vigil.", "n_go", cond="flag:quincey_hunt_smoke_lit&flag:quincey_hunt_lamp_hung&flag:quincey_hunt_lamp_oiled&flag:quincey_hunt_mare_covered"),
                         C("What have I forgotten?", "n_check"),
                         C("[Not yet]", end=True)]),
        "n_check": N(Q, "Anselmo's three things: smoke at the lines (the pit and thistle), a lantern hung high on the post and filled with oil, and a cloth over Santa Fe's neck. I carry no lantern or oil with me: both are back at the fire.", next="n0"),
        "n_go": N(Q, "Smoke across the lines, light on the post, the blanket over her withers. I sit with my back to a picket-post and the Winchester across my knees. An hour goes by. Then another. The horses go still all at once, the way a room goes still when someone enters. Something moves against the moon.",
                  do=[dict(fight="quincey_hunt_bats")], end=True),
    }),
    # ---- dawn
    "quincey_hunt_santafe_dawn": dict(start="n0", nodes={
        "n0": N(Q, "She doesn't shy when I come. Her head drops against my chest. The wound at her neck is two small punctures, clean, almost tidy. The blanket was soaked through.",
                choices=[C("Sit with her.", "n1"), C("[Not yet]", end=True)]),
        "n1": N(Q, "Seward says she's lost too much and there is nothing to be done. Arthur turns away. I stay on my knees in the grass beside her, my hand on her neck, and I talk to her about nothing. The ranch. The Brazos. The sugar-tin.", next="n2"),
        "n2": N(Q, "At sunrise she gives one long breath, like a horse settling for the night, and lays her head down in the grass. They say a horse goes to grass when it dies. She does not move again.",
                do=[dict(set="quincey_hunt_mare_gone"), dict(journal="quincey_hunt_j_grass")], end=True),
    }),
    "quincey_hunt_seward_dawn": dict(start="n0", nodes={
        "n0": N("Seward", "Two punctures, three-eighths of an inch apart, and no tearing. Bat teeth, I'd say, though I've never seen a bat bleed a horse white in a single night. Quincey, what do you make of the grass?",
                choices=[C("A bat did this, Jack, plain and simple.", "n_bat"),
                         C("Snake. A big one.", "n_snake"),
                         C("This was no ordinary bat. I've read the ground.", "n_solved",
                           cond="flag:quincey_hunt_read_ring&flag:quincey_hunt_read_earth&flag:quincey_hunt_read_print"),
                         C("I haven't read the ground yet.", "n_wait", cond="!flag:quincey_hunt_read_ring"),
                         C("I haven't read the ground yet.", "n_wait", cond="!flag:quincey_hunt_read_earth"),
                         C("I haven't read the ground yet.", "n_wait", cond="!flag:quincey_hunt_read_print"),
                         C("[Leave him to his work]", end=True)]),
        "n_bat": N("Seward", "Perhaps. But a bat takes a thimbleful, not a mare. And a bat doesn't leave a ring in the grass. Look about you.", next="n0"),
        "n_snake": N("Seward", "A snake, with two fangs so exactly paired, in a horse that was watched all night? No. Nothing slithered across the grass.", next="n0"),
        "n_wait": N("Seward", "Then do. There are marks in the grass and I am no tracker. Look at the ring, the earth, and the prints near the posts.", next="n0"),
        "n_solved": N(Q, "A ring where something stood and rose. Black earth carried across a continent. A line of bare human prints that begin at the ring and end at the picket-posts. The bat was only the shape it chose for the last part of the trip.",
                      do=[dict(set="quincey_hunt_mark_solved"), dict(journal="quincey_hunt_j_mark")], next="n_solved2"),
        "n_solved2": N("Seward", "You are suggesting a thing that is not a bat, that comes and goes in the shape of one. I am a man of science, Quincey. And I find, to my surprise, that I do not wish to argue.", end=True),
    }),
    "quincey_hunt_arthur_dawn": dict(start="n0", nodes={
        "n0": N("Arthur", "I held her rope, Quincey. All night, not twenty feet away, and I saw nothing. I heard nothing. I'm sorry.",
                choices=[C("It was not your fault, Art.", "n1"), C("It was there and none of us saw it. That's what I mean to remember.", "n2"), C("[Leave him]", end=True)]),
        "n1": N("Arthur", "You are kinder than I deserve. If you ever want a man at your back... I will be there. Wherever it is.", next="n0"),
        "n2": N("Arthur", "Then we remember it together. Whatever it was, we'll know it if it comes again.", next="n0"),
    }),
    "quincey_hunt_final": dict(start="n0", nodes={
        "n0": N(Q, "A mound of red clay under a cross of picket-posts. I stand with my hat in my hand. I think of a foal in the Comanche herd under a falling star, and a boy with a tin of sardines.",
                choices=[C("Lay the sheath on the grave, then take it up again.", "n_end", cond="flag:quincey_hunt_mark_solved"),
                         C("I haven't understood what took her yet.", "n_wait", cond="!flag:quincey_hunt_mark_solved"),
                         C("[Stay a moment longer]", end=True)]),
        "n_wait": N(Q, "I'll not leave this place until I know what to call the thing that did it. Seward is by the posts, and the ground is still readable.", next="n0"),
        "n_end": N(Q, "Santa Fe's bridle and my bowie's sheath: I laid one on the other, as a kind of promise. The sheath she once bit through, on the Brazos, in a fit of spite. I take it up again. 'Whatever you were,' I say to the empty grass, 'I'll know you the next time.'",
                   do=[dict(card="Years later, in London, a Dutch doctor with a pointed beard spoke of bats at a window and a girl who grew pale. I did not need him to say the word. I said it myself. I had already seen it on the Pampas, and I had not forgotten."),
                       dict(journal="quincey_hunt_j_end"), dict(arc_end=1)], end=True),
    }),
}

# ------------------------------------------------------------------ ITEMS
ITEMS = {
    "quincey_hunt_sugar": dict(name="Sugar lump", asset="goblet", variant="default", desc="A lump of sugar from Maria's tin. Santa Fe would follow me to Mexico for one."),
    "quincey_hunt_powder": dict(name="Powder horn", asset="barrel", variant="oak", desc="A horn of black powder, kept dry."),
    "quincey_hunt_lead": dict(name="Lump of lead", asset="hammer", variant="default", desc="Spent slugs dug out of Wash's target post and tapped into a lump. Good for ten cartridges."),
    "quincey_hunt_spur": dict(name="Silver spur", asset="key", variant="gold", desc="A big Mexican spur engraved with a P, lost at the ford by one of Dunning's men."),
    "quincey_hunt_running_iron": dict(name="Running-iron", asset="hammer", variant="default", desc="A rustler's brand-changing iron, taken from Dunning's loot chest."),
    "quincey_hunt_blanket": dict(name="Santa Fe's blanket", asset="rug", variant="cream", desc="Her worn saddle-blanket, soft with years, smelling of her."),
    "quincey_hunt_letter": dict(name="Arthur's letter", asset="book", variant="diary",
                                desc="'Dear Quincey, Seward and I are sailing for Buenos Aires in the spring to hunt on the Pampas. We shall want a man who can shoot. Come, and bring the mare. Your friend, Art.'"),
    "quincey_hunt_lantern": dict(name="Hurricane lantern", asset="lantern", variant="default", desc="A stout lantern, dry as a bone. It needs oil."),
    "quincey_hunt_slugs": dict(name="Cast slugs", asset="hammer", variant="default", desc="Ten bullet-slugs, freshly cast, still smelling of hot lead."),
        "quincey_hunt_bat_wing": dict(name="Bat's wing", asset="bat", variant="black", desc="A broad leathery wing, cut from the creature at the lines. Proof for Seward."),
    "quincey_hunt_sheath": dict(name="Quincey's bowie sheath", asset="book", variant="leather", desc="Tooled Texas leather, bitten once by a spiteful mare on the Brazos. It has carried the great bowie knife through the whole of this story."),
}
for _k in ITEMS.values():
    _k.setdefault("variant", "default")

# ------------------------------------------------------------------ JOURNAL
JOURNAL = {
    "quincey_hunt_j_stolen": dict(title="The remuda is gone", source="Quincey Morris, Texas",
                                  text="Dunning's gang filed through the corral rail while the dogs were fed. Eleven head gone, and Santa Fe among them. Wash has a gash on his skull. I mean to bring every horse home, and Santa Fe first of all."),
    "quincey_hunt_j_load": dict(title="Powder and lead", source="Quincey Morris",
                                text="Wash says powder is hidden in the stable, out of the damp, and lead can be dug from the target post. With both in hand the loading bench will make ten cartridges. I mean to ride out loaded, not hopeful."),
    "quincey_hunt_j_hobbs": dict(title="The old trapper's advice", source="Quincey Morris",
                                 text="Old Hobbs says the creek bottoms are thick with wolves and that the channel is too deep to ford. But there is a cottonwood snag leaning over it with a stub on the limb, and a good lariat will swing a man across."),
    "quincey_hunt_j_signs": dict(title="Reading the signs", source="Quincey Morris",
                                 text="Hoofprints bent east to low ground. Cottonwood ash at the dead fire. Red flannel with canebrake burrs on a thorn. Three signs, one answer: Dunning and my mare are in the bottoms."),
    "quincey_hunt_j_creek": dict(title="Across the channel", source="Quincey Morris",
                                 text="A throw and a half to catch the stub, then hand over hand across black water. It is a boy's trick and I still know it. The wolves have not forgiven me for being on their side of the river."),
    "quincey_hunt_j_wolves": dict(title="Wolves at the ford", source="Quincey Morris",
                                  text="Two grey wolves, thin as rails and twice as mean. The Winchester settled one and the bowie the other. I take no pride in it. They only wanted the same supper I wanted."),
    "quincey_hunt_j_fight": dict(title="Dunning's camp", source="Quincey Morris",
                                 text="One against two, in the open, by firelight, and the odds do not improve as one gets older. The bowie settled Dunning's man and the Winchester settled Dunning. His running-iron I mean to take to the sheriff."),
    "quincey_hunt_j_reunion": dict(title="Santa Fe comes home", source="Quincey Morris",
                                   text="She took sugar from my hand and stood still for the saddle. We rode out of the hollow with eleven horses running behind. A man can lose almost everything and keep his life, but not this mare."),
    "quincey_hunt_j_anselmo": dict(title="What the gaucho knew", source="Quincey Morris, the Pampas",
                                   text="Anselmo says the vampire bat goes for the bare neck. Against it: smoke across the lines, a high lantern, and a cloth the horse knows laid over the neck. He says it as though it were common sense. It is, if you have lost enough steers."),
    "quincey_hunt_j_tale": dict(title="A story by the fire", source="Quincey Morris",
                                text="I told a tale by the fire, and Art laughed in the right places, and Seward corrected the facts. It was the best hour of the whole trip. Odd how often the best hour comes just before the worst."),
    "quincey_hunt_j_bats": dict(title="The vigil", source="Quincey Morris",
                                text="They came out of the moon, three of them, with a sound like wet leather. The smoke thickened and the lantern swung and the Winchester spoke. One went down. Two flew off. The third did not run: it circled twice, looked at me, and then it was gone."),
    "quincey_hunt_j_grass": dict(title="Gone to grass", source="Quincey Morris",
                                 text="She was bled in the small hours, through the blanket, through everything we did right. By sunrise she was gone. I buried her under a cross of picket-posts, and Art helped dig. I do not remember the rest."),
    "quincey_hunt_j_mark": dict(title="The mark in the grass", source="Quincey Morris",
                                text="A flattened ring, black earth foreign to the plain, and bare prints that begin at the ring and end at the posts. No bat made these. Something came on its own feet and left on wings. I wrote it all down, and told no one but Seward."),
    "quincey_hunt_j_end": dict(title="What I carried home", source="Quincey Morris",
                               text="I have the bowie, the Winchester, and a sheath that a mare once chewed. And a name for a thing nobody believes in. Some day I may need to use it."),
}

# ------------------------------------------------------------------ COMBAT
ENEMIES_EXTRA = {
    "quincey_hunt_rustler": dict(name="Horse thief", model="human_peasant_m", hp=13, spd=6, dmg=[2, 4], acc=66, eva=8, tags=["human"], flee_at=0.3,
                                 book="Dunning's gang (arc)"),
    "quincey_hunt_dunning": dict(name="Black Jack Dunning", model="human_peasant_m", hp=20, spd=6, dmg=[3, 5], acc=70, eva=8, tags=["human"], flee_at=0.2,
                                 book="Dunning's gang (arc)"),
}
ENCOUNTERS_EXTRA = {
    "quincey_hunt_wolves": dict(name="Wolves at the ford", time="dusk", enemies=["wolf", "wolf"], flee_ok=True,
                                intro="Two grey wolves slide out of the reeds, lips drawn back. They are thin and desperate.",
                                win="The last wolf drops. The reeds go quiet.", location="quincey_hunt_creek"),
    "quincey_hunt_rustlers": dict(name="Dunning's gang", time="dusk", enemies=["quincey_hunt_rustler", "quincey_hunt_dunning"], flee_ok=True,
                                  intro="Dunning's hand slides from his belt. 'Take him!' Boots scrape behind me; the camp is on its feet.",
                                  win="Dunning goes down on his knees. The camp is quiet. Only the horses snort.", location="quincey_hunt_thief_camp"),
    "quincey_hunt_bats": dict(name="Bats at the lines", time="night", enemies=["bat", "bat", "bat"], flee_ok=False,
                              intro="Three dark shapes, wings like torn umbrellas, drop out of the moon. I fire from the hip.",
                              win="The last of them veers out of the lantern-light and is gone. The silence afterward is worse than the noise.",
                              location="quincey_hunt_pampas_night"),
}
ENCOUNTER_HOOKS = {
    "quincey_hunt_wolves": dict(
        on_win=[dict(set="quincey_hunt_wolves_down"), dict(journal="quincey_hunt_j_wolves"), dict(say="The pack lies quiet in the reeds. The channel is still to be crossed.")],
        on_lose=[dict(set="quincey_hunt_wolves_down"), dict(journal="quincey_hunt_j_wolves"), dict(say="I come to on my back with torn sleeves and the wolves nowhere. A flung brand from the last of my matches drove them off. I am whole, and sorer than I'd care to admit.")],
        on_flee=[dict(say="I scramble up the bank, wolves snapping at my boots. They'll wait. They have all night.")]),
    "quincey_hunt_rustlers": dict(
        on_win=[dict(set="quincey_hunt_rustlers_down"), dict(journal="quincey_hunt_j_fight"), dict(say="Dunning's gang is on the ground or in the dark. The camp is mine.")],
        on_lose=[dict(set="quincey_hunt_rustlers_down"), dict(journal="quincey_hunt_j_fight"),
                 dict(say="I wake in the dust with a swollen jaw. Dunning's men have run off into the night, afraid, I reckon, of the hanging that I've threatened. The camp is empty but for the horses.")],
        on_flee=[dict(say="I back out of the firelight before they can close in. They'll be waiting.")]),
    "quincey_hunt_bats": dict(
        on_win=[dict(set="quincey_hunt_bats_down"), dict(journal="quincey_hunt_j_bats"),
                dict(card="Morning. The grass at dawn."), dict(goto="quincey_hunt_pampas_dawn")],
        on_lose=[dict(set="quincey_hunt_bats_down"), dict(journal="quincey_hunt_j_bats"),
                 dict(card="I woke at sunrise with my head against a picket-post, and no memory of the end of the night."), dict(goto="quincey_hunt_pampas_dawn")],
        on_flee=[dict(set="quincey_hunt_bats_down"), dict(journal="quincey_hunt_j_bats"), dict(goto="quincey_hunt_pampas_dawn")]),
}

# ------------------------------------------------------------------ seed variation
PALETTES = {
    "quincey_hunt_ranch": [dict(floor="dirt"), dict(floor="grass")],
    "quincey_hunt_stable": [dict(wall="planks", floor="dirt", wood="oak", cloth="green"), dict(wall="planks", floor="planks", wood="dark", cloth="blue"),
                            dict(wall="plaster_dirty", floor="dirt", wood="pale", cloth="red")],
    "quincey_hunt_prairie": [dict(floor="grass"), dict(floor="dirt")],
    "quincey_hunt_creek": [dict(floor="dirt"), dict(floor="grass")],
    "quincey_hunt_thief_camp": [dict(floor="dirt"), dict(floor="grass")],
    "quincey_hunt_pampas_camp": [dict(floor="grass"), dict(floor="dirt")],
}
PLACEMENTS = {
    "quincey_hunt_powder": [
        dict(prop="quincey_hunt_shelf", text="Behind a row of saddle-soap tins, wrapped in oilcloth: Wash's horn of black powder, dry as a bone.", hint="One tin on the shelf sits proud of the others."),
        dict(prop="quincey_hunt_feed", text="Buried in the oats, in a waxed pouch: a powder horn. Wash hides everything in the feed.", hint="The lid of the feed barrel has been put back crooked, and dust has not settled on one side."),
        dict(prop="quincey_hunt_harness_chest", text="Under the breeching, wrapped in an old shirt: a full powder horn.", hint="The harness chest is heavier than a chest of leather ought to be."),
    ],
    "quincey_hunt_lantern": [
        dict(prop="quincey_hunt_wagon", text="Under the wagon-seat, on its side, wrapped in a sack: a stout hurricane lantern.", hint="Something glass-and-iron glints under the wagon seat."),
        dict(prop="quincey_hunt_tent", text="On the tent floor, between Arthur's valise and Seward's notebooks: a hurricane lantern, unlit.", hint="Something round and metal pokes out of the tent flap."),
        dict(prop="quincey_hunt_roll", text="Wrapped in my own spare shirt inside the saddle-roll: the hurricane lantern I had forgotten I carried.", hint="My saddle-roll is lumpier than I left it."),
    ],
}
GATES = {
    "quincey_hunt_gate_range": [
        dict(cond="has:bullet&flag:quincey_hunt_powder_ready", fail="Wash is right. I will not ride out against Dunning's gang with an empty rifle. Powder and lead, then the loading bench.", needs="bullet"),
        dict(cond="has:bullet&flag:quincey_hunt_powder_ready&has:rope", fail="A full cylinder, and I will want a lariat from the tack chest before I leave the yard.", needs="bullet"),
    ],
}
