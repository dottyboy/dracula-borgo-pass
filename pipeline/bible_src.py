#!/usr/bin/env python3
"""Source of truth for the world: assets, texture variants, characters,
locations, items and dialogue. Run it to (re)write pipeline/world_bible.json,
which every other pipeline step and the game read.

Coordinates in locations: metres, x right, z toward the camera, y up.
Model front is +Z, rotation is degrees around Y.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "world_bible.json"

# --------------------------------------------------------------------------- #
# assets (geometry). Each id -> blender_gen builder + params
# --------------------------------------------------------------------------- #
ASSETS = []


def asset(id, builder, **params):
    ASSETS.append({"id": id, "builder": builder, "params": params})


asset("floor_4x4", "floor", w=4, d=4)
asset("wall_4", "wall", w=4, h=3.4)
asset("wall_door_4", "wall", w=4, h=3.4, door=1.4)
asset("wall_window_4", "wall", w=4, h=3.4, window=1.0)
asset("arch", "arch")
asset("column", "column")
asset("column_short", "column", h=1.8, r=0.25)
asset("stairs", "stairs")
asset("tower", "tower")
asset("castle_keep", "castle_keep")
asset("door", "door")
asset("door_big", "door", w=1.8, h=2.8)
asset("table", "table")
asset("table_long", "table", w=4.2, d=1.1)
asset("chair", "chair")
asset("throne", "throne")
asset("bed", "bed")
asset("bed_simple", "bed", posts=False)
asset("chest", "chest")
asset("barrel", "barrel")
asset("candle", "candle")
asset("candelabra", "candelabra")
asset("lantern", "lantern")
asset("sconce", "sconce")
asset("crucifix", "crucifix")
asset("crucifix_big", "crucifix", h=1.1)
asset("coffin", "coffin")
asset("tomb", "tomb")
asset("gravestone", "gravestone")
asset("gravestone_point", "gravestone", style="point")
asset("grave_cross", "grave_cross")
asset("book", "book")
asset("bookshelf", "bookshelf")
asset("fireplace", "fireplace")
asset("mirror", "mirror")
asset("goblet", "goblet")
asset("bottle", "bottle")
asset("garlic", "garlic")
asset("stake", "stake")
asset("hammer", "hammer")
asset("key", "key")
asset("rug", "rug")
asset("bench", "bench")
asset("bust", "figure_bust")
asset("pine", "pine")
asset("pine_small", "pine", h=4.0)
asset("deadtree", "deadtree")
asset("rock", "rock")
asset("rock_big", "rock", s=2.2)
asset("fence", "fence")
asset("carriage", "carriage")
asset("signpost", "signpost")
asset("inn_sign", "inn_sign")
asset("moon", "moon")
asset("house_row", "house_row")
asset("house_wide", "house_row", w=9.0, d=5.5, h=4.8, floors=2)
asset("cottage", "cottage")
asset("house_front_a", "house_row", w=9.0, d=5.5, h=4.8, floors=2, door=False)
asset("house_front_b", "house_row", w=6.0, d=5.0, h=4.6, floors=2, door=False)
asset("house_front_c", "cottage_nd")
asset("manor", "house_row", w=11.0, d=6.5, h=5.8, rise=3.0, floors=2)
asset("church", "church")
asset("lighthouse", "lighthouse")
asset("mast_cluster", "mast_cluster")
asset("pier", "pier")
asset("boat", "boat")
asset("lamp_post", "lamp_post")
asset("crate_stack", "crate_stack")
asset("bollard", "bollard")
asset("rope_coil", "rope_coil")
asset("gull", "bat", span=0.9)
asset("bush", "bush")
asset("shrub", "bush", r=0.5)
asset("fern", "fern")
asset("flower_patch", "flower_patch")
asset("reeds", "reeds")
asset("log", "log")
asset("stump", "stump")
asset("hedge", "hedge")
asset("low_wall", "low_wall")
asset("well", "well")
asset("market_stall", "market_stall")
asset("hay_bale", "hay_bale")
asset("cart", "cart")
asset("anchor", "anchor")
asset("net_rack", "net_rack")
asset("cliff_face", "cliff_face")
asset("cliff_stairs", "cliff_stairs")
asset("quay_edge", "quay_edge")
asset("oak", "oak")
asset("yew", "yew")
asset("boulders", "boulders")
asset("picket_fence", "picket_fence")
asset("bat", "bat")
asset("wolf", "wolf")
asset("wolf_big", "wolf", scale=1.25)

HUMANS = [
    ("human_harker", dict(height=1.78, sex="m", hair="short", garment="coat")),
    ("human_dracula", dict(height=1.9, sex="m", hair="slick", beard="moustache", garment="coat", cloak=True, fangs=True)),
    ("human_mina", dict(height=1.65, sex="f", hair="bun", garment="dress")),
    ("human_lucy", dict(height=1.68, sex="f", hair="long", garment="gown")),
    ("human_vanhelsing", dict(height=1.7, build=1.05, sex="m", hair="short", beard="pointed", garment="coat")),
    ("human_seward", dict(height=1.8, sex="m", hair="short", beard="moustache", garment="coat")),
    ("human_renfield", dict(height=1.7, build=0.85, sex="m", hair="short", garment="frock")),
    ("human_quincey", dict(height=1.85, build=1.1, sex="m", hair="short", beard="pointed", garment="coat", hat="top")),
    ("human_arthur", dict(height=1.82, build=1.05, sex="m", hair="short", garment="coat")),
    ("human_bride", dict(height=1.72, build=0.95, sex="f", hair="long", garment="gown", fangs=True)),
    ("human_peasant_m", dict(height=1.68, sex="m", hair="short", beard="full", garment="frock", hat="fur")),
    ("human_peasant_f", dict(height=1.58, sex="f", hair="short", garment="dress", hat="shawl")),
    ("human_captain", dict(height=1.78, build=1.1, sex="m", hair="short", beard="full", garment="coat", hat="fur")),
    ("human_coachman", dict(height=1.85, build=1.1, sex="m", hair="short", garment="coat", cloak=True, hat="top")),
]
for _id, _p in HUMANS:
    asset(_id, "human", **_p)

# --------------------------------------------------------------------------- #
# texture variants:  variants[asset][variant_name] = {role: {tex, tint}}
# `tex` is a procedural texture id (texture_gen.py); tint multiplies it.
# Swapping the dict entry re-skins the very same mesh.
# --------------------------------------------------------------------------- #


def T(tex, tint="#ffffff"):
    return {"tex": tex, "tint": tint}


VARIANTS = {}


def variants(id, first, **named):
    """First key is the default variant."""
    VARIANTS[id] = {"default": first, **named}


STONE = {
    "stone_grey": {"stone": T("stone_blocks")},
    "stone_mossy": {"stone": T("stone_moss")},
    "stone_dark": {"stone": T("stone_blocks", "#6a6a74")},
    "stone_tomb": {"stone": T("stone_rough", "#d2cdc0")},
    "plaster": {"stone": T("plaster", "#e8dfcc")},
    "plaster_dirty": {"stone": T("plaster", "#9a8f78")},
    "cobble": {"stone": T("cobble")},
    "planks": {"stone": T("wood_planks", "#cdb89a")},
    "dirt": {"stone": T("dirt")},
    "grass": {"stone": T("grass")},
}
WOOD = {
    "oak": {"wood": T("wood_planks")},
    "dark": {"wood": T("wood_planks", "#6a5040")},
    "pale": {"wood": T("wood_planks", "#e6d3aa")},
    "ebony": {"wood": T("wood_planks", "#3a2a22")},
}
FABRIC = {
    "red": T("velvet", "#7a1a1f"), "blue": T("cloth", "#2a3e6a"), "green": T("cloth", "#2e4a30"),
    "black": T("cloth", "#1a1a1a"), "cream": T("cloth", "#d8ccb0"),
}

for _id in ("floor_4x4", "wall_4", "wall_door_4", "wall_window_4", "arch", "column", "column_short", "stairs",
            "tower", "castle_keep", "tomb", "bust", "fireplace", "gravestone", "gravestone_point", "grave_cross"):
    variants(_id, "stone_grey", **STONE)
for _id in ("door", "door_big", "table", "table_long", "bench", "barrel", "bookshelf", "chest", "signpost",
            "inn_sign", "carriage", "coffin"):
    variants(_id, "oak", **WOOD)
for _id in ("chair", "bed", "bed_simple", "throne"):
    variants(_id, "red",
             red={"wood": T("wood_planks", "#6a5040"), "cloth": FABRIC["red"]},
             blue={"wood": T("wood_planks"), "cloth": FABRIC["blue"]},
             green={"wood": T("wood_planks", "#e6d3aa"), "cloth": FABRIC["green"]},
             black={"wood": T("wood_planks", "#3a2a22"), "cloth": FABRIC["black"]})
variants("rug", "red", **{k: {"cloth": v} for k, v in FABRIC.items()})
ROOF = {"slate": {"roof": T("stone_blocks", "#3c3a44")}, "tile": {"roof": T("stone_blocks", "#7a3a2a")}, "thatch": {"roof": T("dirt", "#b09a5a")}}
for _id in ("house_row", "house_wide", "cottage", "house_front_a", "house_front_b", "house_front_c", "manor", "church"):
    VARIANTS[_id] = {"default": "plaster_slate", **{f"{sn}_{rn}": {**sv, **rv} for sn, sv in STONE.items() if sn in ("plaster", "plaster_dirty", "stone_grey", "stone_dark", "stone_mossy") for rn, rv in ROOF.items()}}
VARIANTS["lighthouse"] = {"default": "white", "white": {"stone": T("plaster", "#f0ece4"), "roof": T("plaster", "#9a2a28"), "wood": T("wood_planks", "#5a4636")},
                          "grey": {"stone": T("stone_blocks", "#b8b4ac"), "roof": T("stone_blocks", "#3a3a40")}}
VARIANTS["mast_cluster"] = {"default": "brown", "brown": {"wood": T("wood_planks", "#3a2a22"), "cloth": T("cloth", "#bdb29a")}, "dark": {"wood": T("wood_planks", "#2a2018"), "cloth": T("cloth", "#6a6258")}}
for _id in ("pier", "crate_stack"):
    variants(_id, "oak", **WOOD)
VARIANTS["boat"] = {"default": "tarred", "tarred": {"wood": T("wood_planks", "#2e2620"), "earth": T("wood_planks", "#6a5040")}, "white": {"wood": T("wood_planks", "#d8d2c6"), "earth": T("wood_planks", "#8a7a68")}}
variants("lamp_post", "default", default={})
variants("bollard", "default", default={})
variants("rope_coil", "default", default={})
VARIANTS["gull"] = {"default": "white", "white": {"fur": T("fur", "#f2f2f0"), "wing": T("cloth", "#e8e8e6"), "eyes": T("flat", "#202020")}}
for _id in ("pine", "pine_small"):
    variants(_id, "green", green={}, snow={"foliage": T("snow", "#f0f4f8")}, dark={"foliage": T("foliage", "#16261e")})
variants("deadtree", "grey", grey={})
for _id in ("rock", "rock_big"):
    variants(_id, "grey", grey={}, mossy={"rock": T("stone_moss")}, dark={"rock": T("stone_rough", "#555555")})
for _id in ("wolf", "wolf_big"):
    variants(_id, "grey", grey={"fur": T("fur", "#6a6760")}, black={"fur": T("fur", "#1c1a1a")},
             white={"fur": T("fur", "#d8d8d4")})
variants("bat", "black", black={"fur": T("fur", "#141414")}, brown={"fur": T("fur", "#3a2c24")})
variants("book", "leather", leather={"leather": T("leather", "#6a4630")}, diary={"leather": T("leather", "#26262c")},
         red={"leather": T("leather", "#6a1a1a")})
variants("candle", "white", white={}, red={"wax": T("wax", "#8a1a1a")})
variants("bottle", "glass", glass={}, green={"glass": T("glass", "#2f6a40")}, amber={"glass": T("glass", "#b87a30")})
for _id in ("candelabra", "lantern", "sconce", "crucifix", "crucifix_big", "mirror", "goblet", "garlic", "stake",
            "hammer", "key", "fence", "moon"):
    variants(_id, "default", default={})
VARIANTS["crucifix"]["silver"] = {"gold": T("iron", "#e8e8f0")}
VARIANTS["crucifix_big"]["silver"] = {"gold": T("iron", "#e8e8f0")}
VARIANTS["key"]["gold"] = {"iron": T("gold")}
VARIANTS["fireplace"]["soot"] = {"stone": T("stone_blocks", "#3a3a3a")}


def human(**over):
    d = {"skin": T("skin", "#e8c3a0"), "eyes": T("flat", "#201510"), "mouth": T("flat", "#8a3a3a"),
         "hair": T("hair", "#4a3322"), "top": T("wool", "#5a4632"), "bottom": T("wool", "#3a3128"),
         "shoes": T("leather", "#2a1d14"), "accent": T("cloth", "#2a2a2a"), "cloak": T("cloth", "#111111")}
    d.update(over)
    return d


RED_EYES = T("flat", "#c01818")
PALE = T("skin", "#d9d2c6")
VAMP = dict(skin=T("skin", "#e0d4cc"), eyes=T("flat", "#901818"), mouth=T("flat", "#b01818"), accent=T("cloth", "#9a1c1c"))
variants("human_harker", "harker",
         harker=human(top=T("wool", "#6b5a45"), bottom=T("wool", "#4a4034"), hair=T("hair", "#5b3b22")),
         travel=human(top=T("wool", "#3f4a3a"), bottom=T("wool", "#2e2a24")))
variants("human_dracula", "count",
         count=human(skin=PALE, eyes=RED_EYES, mouth=T("flat", "#9c1c1c"), hair=T("hair", "#d8d8d8"),
                     top=T("cloth", "#0d0d0d"), bottom=T("cloth", "#0d0d0d"), cloak=T("cloth", "#0a0a0a"),
                     accent=T("cloth", "#aa1111"), shoes=T("leather", "#0a0a0a")),
         young=human(skin=T("skin", "#d9c2a8"), eyes=RED_EYES, hair=T("hair", "#1a1a1a"), top=T("cloth", "#1a1a22"),
                     bottom=T("cloth", "#1a1a22"), cloak=T("cloth", "#16161c")),
         london=human(skin=T("skin", "#d9c8b0"), eyes=RED_EYES, hair=T("hair", "#9a9a9a"), top=T("wool", "#2a2a30"),
                      bottom=T("wool", "#2a2a30"), cloak=T("cloth", "#222222")))
variants("human_mina", "mina",
         mina=human(skin=T("skin", "#f0cfb0"), hair=T("hair", "#3a2518"), top=T("cloth", "#5a6f8a"),
                    accent=T("cloth", "#e8e0d0")),
         nurse=human(skin=T("skin", "#f0cfb0"), hair=T("hair", "#3a2518"), top=T("cloth", "#dcdcdc"),
                     accent=T("cloth", "#7a7a7a")))
variants("human_lucy", "lucy",
         lucy=human(skin=T("skin", "#f2d4b8"), hair=T("hair", "#d9a84a"), top=T("cloth", "#e9dfe2"),
                    accent=T("cloth", "#d9a0a8")),
         nightgown=human(skin=T("skin", "#f4ddc8"), hair=T("hair", "#d9a84a"), top=T("cloth", "#f4f4f4"),
                         accent=T("cloth", "#cfcfcf")),
         undead=human(skin=T("skin", "#d6d6d6"), eyes=RED_EYES, hair=T("hair", "#c9a040"),
                      top=T("cloth", "#eeeeee"), accent=T("cloth", "#9a1c1c")))
variants("human_vanhelsing", "vh",
         vh=human(skin=T("skin", "#e0b896"), hair=T("hair", "#cfcfcf"), top=T("wool", "#2e2e36"),
                  bottom=T("wool", "#2a2a30")))
variants("human_seward", "doctor",
         doctor=human(top=T("wool", "#2a3a4a"), bottom=T("wool", "#2a2a2a"), hair=T("hair", "#4a3a2a"),
                      accent=T("cloth", "#e0e0e0")))
variants("human_renfield", "asylum",
         asylum=human(skin=T("skin", "#d5b896"), hair=T("hair", "#6a5a40"), top=T("cloth", "#d4cdbd"),
                      bottom=T("cloth", "#c8c0ae"), shoes=T("cloth", "#555555"), accent=T("cloth", "#b0a890")))
variants("human_quincey", "texan",
         texan=human(skin=T("skin", "#cfa078"), hair=T("hair", "#3a2a18"), top=T("wool", "#5a3e2a"),
                     bottom=T("wool", "#3a3a40"), accent=T("leather", "#2a1a10")))
variants("human_arthur", "lord",
         lord=human(hair=T("hair", "#b89a60"), top=T("wool", "#2a3a5a"), bottom=T("wool", "#3a3a3a")))
variants("human_bride", "bride1",
         bride1=human(**VAMP, hair=T("hair", "#d9a84a"), top=T("cloth", "#e8e0d8")),
         bride2=human(**VAMP, hair=T("hair", "#1a1210"), top=T("cloth", "#d8d4dc")),
         bride3=human(**VAMP, hair=T("hair", "#8a2a18"), top=T("cloth", "#e0d8cc")))
variants("human_peasant_m", "innkeeper",
         innkeeper=human(top=T("cloth", "#6a5a3a"), bottom=T("wool", "#4a3a2a"), accent=T("fur", "#5a4a3a"),
                         hair=T("hair", "#6a5a4a")),
         szgany=human(skin=T("skin", "#b88a62"), top=T("cloth", "#7a2a1a"), bottom=T("wool", "#2a2a2a"),
                      accent=T("fur", "#2a2018"), hair=T("hair", "#141010")),
         villager=human(top=T("cloth", "#4a5a40"), bottom=T("wool", "#4a3a2a"), accent=T("fur", "#3a3028"),
                        hair=T("hair", "#8a7a5a")))
variants("human_peasant_f", "innkeeper_wife",
         innkeeper_wife=human(top=T("cloth", "#7a3a3a"), accent=T("cloth", "#d8d0c0"), hair=T("hair", "#6a5a4a")),
         village_woman=human(top=T("cloth", "#3a4a5a"), accent=T("cloth", "#a89a7a"), hair=T("hair", "#4a3a2a")))
variants("human_captain", "captain",
         captain=human(skin=T("skin", "#c8a080"), hair=T("hair", "#6a5a4a"), top=T("wool", "#1f2a3a"), bottom=T("wool", "#1a1f28"),
                       accent=T("fur", "#3a3a3a"), shoes=T("leather", "#2a1d14")))
variants("human_coachman", "driver",
         driver=human(skin=T("skin", "#c8b8a8"), eyes=RED_EYES, top=T("cloth", "#1a1a1a"), bottom=T("cloth", "#1a1a1a"),
                      cloak=T("cloth", "#141414"), accent=T("cloth", "#0a0a0a")))


for _id in ("bush", "shrub", "hedge", "fern", "oak", "yew"):
    variants(_id, "green", green={}, dark={"foliage": T("foliage", "#1b2e1c")}, autumn={"foliage": T("foliage", "#8a5a22")}, dry={"foliage": T("foliage", "#7a7a3a")})
variants("flower_patch", "white", white={"petal": T("flat", "#f2f0e8")}, yellow={"petal": T("flat", "#e8c83a")}, purple={"petal": T("flat", "#8a58b8")}, red={"petal": T("flat", "#b83030")})
variants("reeds", "green", green={}, dry={"plant": T("foliage", "#9a8a4a")})
for _id in ("log", "stump"):
    variants(_id, "bark", bark={}, pale={"bark": T("bark", "#cdbfa8")})
variants("low_wall", "stone_grey", **STONE)
variants("well", "stone_grey", stone_grey={}, mossy={"stone": T("stone_moss")}, dark={"stone": T("stone_blocks", "#6a6a74")})
variants("market_stall", "red", red={"cloth": T("cloth", "#8a2a2a")}, blue={"cloth": T("cloth", "#2a4a8a")}, green={"cloth": T("cloth", "#3a6a3a")}, cream={"cloth": T("cloth", "#d8ccb0")})
variants("hay_bale", "straw", straw={}, old={"straw": T("parchment", "#a89a60")})
for _id in ("cart", "net_rack", "picket_fence"):
    variants(_id, "oak", **WOOD)
variants("anchor", "iron", iron={}, rusty={"iron": T("iron", "#8a5a3a")})
variants("cliff_face", "grey", grey={}, mossy={"rock": T("stone_moss")}, dark={"rock": T("stone_rough", "#555560")})
variants("cliff_stairs", "stone_grey", **STONE)
variants("quay_edge", "stone_grey", **STONE)
variants("boulders", "grey", grey={}, mossy={"rock": T("stone_moss")}, dark={"rock": T("stone_rough", "#555555")})

# generic fallbacks per role, used when a variant does not override a role
ROLE_DEFAULTS = {
    "stone": T("stone_blocks"), "wood": T("wood_planks"), "iron": T("iron"), "glass": T("glass", "#9fb5c4"),
    "gold": T("gold"), "leather": T("leather", "#6a4630"), "cloth": T("velvet", "#7a1a1f"),
    "linen": T("cloth", "#e8e2d0"), "trim": T("cloth", "#c9a248"), "wax": T("wax", "#efe4c8"),
    "flame": T("flame", "#ffc860"), "paper": T("parchment"), "earth": T("dirt"), "roof": T("stone_blocks", "#4a3a3a"),
    "bark": T("bark"), "foliage": T("foliage", "#2a4030"), "rock": T("stone_rough"), "plant": T("foliage", "#8a9a50"),
    "garlic": T("cloth", "#f2efe2"), "wine": T("flat", "#5a0c10"), "fur": T("fur", "#5a5750"),
    "dark": T("flat", "#111111"), "eyes": T("flat", "#e0c040"), "wing": T("leather", "#2a2024"),
    "petal": T("flat", "#e8d878"), "straw": T("parchment", "#d8c070"),
    "glow": T("flame", "#fff2c8"), "sclera": T("flat", "#f4f0ea"),
}

# --------------------------------------------------------------------------- #
# book grounding: keywords scanned in the novel (extract_book.py)
# --------------------------------------------------------------------------- #
LOCATIONS = [
    dict(id="golden_krone", name="Golden Krone Hotel, Bistritz", keywords=["Golden Krone"],
         desc="Harker's last stop of civilisation. The landlord's wife presses a crucifix on him.",
         chapter="I"),
    dict(id="borgo_pass", name="Borgo Pass", keywords=["Borgo Pass"],
         desc="A moonlit mountain road. Wolves howl; blue flames flicker where treasure lies.", chapter="I"),
    dict(id="castle_courtyard", name="Castle Dracula, courtyard", keywords=["courtyard", "great door"],
         desc="A vast ruined courtyard under the moon. One great door, no light.", chapter="II"),
    dict(id="great_hall", name="Castle Dracula, the hall", keywords=["great hall", "hall"],
         desc="A lamp-lit hall where the Count bids him welcome.", chapter="II"),
    dict(id="harker_room", name="Harker's bedroom", keywords=["bedroom", "shaving", "looking-glass", "mirror"],
         desc="A comfortable room with a mirror. There is no reflection of the Count in it.", chapter="II"),
    dict(id="library", name="The library", keywords=["library", "Bradshaw"],
         desc="Books in English on every subject; the Count has studied England thoroughly.", chapter="II"),
    dict(id="old_wing", name="The forbidden wing", keywords=["other part of the castle", "sleep in any other"],
         desc="A dim chamber on the unexplored side of the castle, where he is forbidden to sleep.", chapter="III"),
    dict(id="chapel_crypt", name="The ruined chapel and crypt", keywords=["chapel", "crypt", "boxes of earth"],
         desc="Fifty boxes of earth lie in the old chapel. In one, the Count lies as if dead.", chapter="IV"),
    dict(id="whitby_churchyard", name="Whitby churchyard", keywords=["churchyard", "Whitby"],
         desc="Windswept graves above the harbour. Mina's seat overlooks the sea.", chapter="VI"),
]
CHARACTERS = [
    dict(id="harker", name="Jonathan Harker", keywords=["Jonathan", "Harker"]),
    dict(id="dracula", name="Count Dracula", keywords=["Count", "Dracula"]),
    dict(id="mina", name="Mina Murray", keywords=["Mina"]),
    dict(id="lucy", name="Lucy Westenra", keywords=["Lucy"]),
    dict(id="vanhelsing", name="Professor Van Helsing", keywords=["Van Helsing"]),
    dict(id="seward", name="Dr. John Seward", keywords=["Seward"]),
    dict(id="renfield", name="R. M. Renfield", keywords=["Renfield"]),
    dict(id="quincey", name="Quincey Morris", keywords=["Quincey", "Morris"]),
    dict(id="arthur", name="Arthur Holmwood", keywords=["Arthur", "Holmwood"]),
    dict(id="brides", name="The Three Sisters", keywords=["three young women", "sisters", "voluptuous"]),
    dict(id="innkeeper", name="Landlord of the Golden Krone", keywords=["landlord", "hostess"]),
    dict(id="szgany", name="Szgany", keywords=["Szgany", "gipsies", "Slovak"]),
    dict(id="coachman", name="The coachman", keywords=["driver", "caleche", "calèche"]),
    dict(id="wolves", name="The wolves", keywords=["wolves", "wolf"]),
    dict(id="bats", name="The bats", keywords=["bat"]),
]
PROPS = [
    dict(id="crucifix", name="Crucifix", keywords=["crucifix", "rosary"]),
    dict(id="garlic", name="Garlic", keywords=["garlic"]),
    dict(id="stake", name="Stake", keywords=["stake"]),
    dict(id="key", name="Key", keywords=[r"\bkeys?\b"]),
    dict(id="candles", name="Candles", keywords=["candle"]),
    dict(id="coffin", name="Coffin / earth box", keywords=["coffin", "boxes of earth"]),
    dict(id="mirror", name="Mirror", keywords=["looking-glass", "mirror"]),
    dict(id="diary", name="Diary", keywords=["diary", "journal"]),
    dict(id="lantern", name="Lamp", keywords=["lamp", "lantern"]),
    dict(id="blue_flame", name="Blue flame", keywords=["blue flame"]),
    dict(id="carriage", name="Calèche", keywords=["caleche", "calèche", "carriage"]),
    dict(id="bookshelf", name="Library books", keywords=["books"]),
    dict(id="fireplace", name="Fireplace", keywords=["fire", "hearth"]),
    dict(id="wine", name="Tokay wine", keywords=["Tokay", "wine"]),
    dict(id="razor", name="Shaving razor", keywords=["razor"]),
    dict(id="gravestone", name="Gravestone", keywords=["gravestone", "tombstone"]),
]

# --------------------------------------------------------------------------- #
# the playable vertical slice: Jonathan Harker, chapters I-IV
# --------------------------------------------------------------------------- #
# interaction `do` verbs: say:<text> give:<item> take:<item> set:<flag>
#   goto:<location>[@x,z] talk:<dialogue> remove:<prop_id> end:<text>
# conditions: "flag" / "!flag" / "has:item" / "!has:item"


def prop(id, asset, variant, x, z, rot=0, scale=1.0, y=0.0, name=None, look=None, radius=0.5, **interact):
    p = dict(id=id, asset=asset, variant=variant, pos=[x, y, z], rot=rot, scale=scale, radius=radius)
    if name:
        p["name"] = name
    if look:
        interact["look"] = look
    if interact:
        p["interact"] = interact
    return p


def npc(id, asset, variant, x, z, rot=0, name="", look="", talk=None, radius=0.5, **extra):
    d = dict(id=id, asset=asset, variant=variant, pos=[x, 0, z], rot=rot, name=name, radius=radius,
             interact={"look": look, **({"talk": talk} if talk else {}), **extra})
    return d


ITEMS = {
    "crucifix": dict(name="Crucifix", asset="crucifix", variant="silver",
                     desc="The old woman's gift. 'For your mother's sake.' I did not like it, but I took it."),
    "garlic": dict(name="Garlic flowers", asset="garlic", variant="default",
                   desc="Garlic. The peasants ward off evil with it. They must know something."),
    "diary": dict(name="Journal", asset="book", variant="diary",
                  desc="My shorthand journal. The only thing in this place I can still call my own."),
    "razor": dict(name="Shaving glass", asset="mirror", variant="default",
                  desc="A small shaving mirror. I saw no reflection of the Count behind me."),
    "key": dict(name="Iron key", asset="key", variant="gold",
                desc="A key from the Count's own coat. It is heavier than it looks."),
    "lantern": dict(name="Lantern", asset="lantern", variant="default",
                    desc="A good lamp. The castle is dark in places even by day."),
    "stake": dict(name="Wooden stake", asset="stake", variant="default",
                  desc="Sharpened oak. A thing I should not know the use of."),
    "hammer": dict(name="Hammer", asset="hammer", variant="default", desc="A mason's hammer from the chapel."),
    "vault_key": dict(name="Count's keys", asset="key", variant="gold",
                      desc="Taken from the Count's own belt. I can hardly believe he did not wake."),
    "wine": dict(name="Tokay", asset="bottle", variant="amber", desc="Golden Tokay. 'Excellent wine', I wrote in my journal."),
}

LOC_DATA = {}

LOC_DATA["golden_krone"] = dict(
    cells=[2, 2], wall="plaster_dirty", floor="planks", interior=True,
    ambient=dict(color="#3a2c20", energy=0.5, fog="#140e08"),
    camera=dict(pos=[0, 4.4, 8.6], look=[0, 1.1, -0.5], fov=52),
    lights=[dict(pos=[0, 2.4, -3], color="#ff9a40", energy=2.6, range=9), dict(pos=[-2.5, 1.8, 1], color="#ffb060", energy=1.4, range=6)],
    walls=dict(north=["wall_4", "wall_window_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[0, 3.2], spawns={"borgo_pass": [2.8, 2.0]},
    props=[
        prop("fire", "fireplace", "soot", 0, -3.4, name="Fireplace", look="A smoky fire. The landlord's family keep it burning all night. A half-burnt stick of ash wood lies in the hearth.", radius=0.9,
             take="wood", take_text="I pulled out a half-burnt stick of ash wood.", give_once=True),
        prop("table1", "table_long", "dark", -1.2, -0.6, name="Long table", look="The remains of my paprika hendl. Excellent, if thirsty work.", radius=1.2),
        prop("chair1", "chair", "red", -1.4, 0.4, rot=180, name="Chair", look="A rough chair with a scrap of homespun cloth over the back.", radius=0.35,
             take="cloth", take_text="I took the scrap of homespun cloth. It may bind or wrap something."),
        prop("chair2", "chair", "red", 0.2, -1.5, rot=0, name="Chair", look="A coil of rope hangs over the back.", radius=0.35,
             take="rope", take_text="I took the coil of rope."),
        prop("barrel1", "barrel", "dark", -3.1, -2.6, name="Barrel", look="Plum brandy, by the smell.", radius=0.4,
             take="brandy", take_text="I filled a flask from the barrel. Slivovitz: it will steady the nerves.", give_once=True),
        prop("bottle1", "bottle", "amber", -1.2, -0.6, y=0.8, name="Tokay", radius=0.1, look="Golden Tokay, left by the hostess.",
             take="wine", take_text="I pocketed the bottle. It gives courage for the road ahead."),
        prop("door_out", "door", "dark", 3.8, 2.0, rot=-90, name="Door to the inn yard", radius=0.6,
             look="The door to the yard, where the coach waits.",
             go="borgo_pass", go_cond="has:crucifix", go_fail="The hostess has not yet finished with me. I should hear what she has to say first."),
        prop("sign", "inn_sign", "oak", 3.9, -2.4, rot=-90, y=2.6, name="Sign: the Golden Krone", look="The Golden Krone Hotel. 'Mittel Land' - the Middle Land, as Bistritz calls itself.", radius=0.1),
        prop("lamp_i", "lantern", "default", -2.4, 2.6, name="Oil lamp", look="An oil lamp, nearly full.", radius=0.3,
             take="oil", take_text="I decanted a little lamp oil into a flask.", give_once=True),
        prop("knife_i", "bottle", "glass", 0.9, -0.6, y=0.8, name="Table knife", look="A plain table knife lies by the plates.", radius=0.1,
             take="knife", take_text="I slipped the table knife into my pocket."),
        prop("rug", "rug", "red", 0.5, 1.8, name=None, radius=0.01, look=None),
    ],
    npcs=[
        npc("hostess", "human_peasant_f", "innkeeper_wife", 2.0, -0.8, rot=-30, name="Hostess",
            look="The landlord's wife. She wrings her hands, and weeps for me.", talk="hostess"),
        npc("landlord", "human_peasant_m", "innkeeper", -2.8, -1.6, rot=30, name="Landlord",
            look="A broad man, anxious to speak and unable to.", talk="landlord"),
    ],
)

LOC_DATA["borgo_pass"] = dict(
    cells=[3, 2], wall="dirt", floor="grass", interior=False, night=True,
    ambient=dict(color="#2a3a5c", energy=0.9, fog="#0e1522"),
    camera=dict(pos=[0, 5.2, 10.5], look=[0, 1.0, -1.0], fov=55),
    lights=[dict(pos=[-4, 6, 2], color="#8aa6ff", energy=3.2, range=24), dict(pos=[4, 4, 4], color="#aab8ff", energy=1.6, range=16)],
    moon=dict(pos=[14, 17, -22]),
    scatter=dict(asset="pine", variant="dark", count=26, seed=11, avoid=[[-3, -2, 3, 5]]),
    scatter2=dict(asset="rock", variant="mossy", count=8, seed=5, avoid=[[-3, -2, 3, 5]]),
    spawn=[-4.2, 3.0], spawns={"golden_krone": [-4.2, 3.0], "castle_courtyard": [-4.2, 3.0]},
    props=[
        prop("coach", "carriage", "ebony", 1.2, 0.5, rot=-25, name="Calèche", radius=1.7,
             look="A black calèche with four black horses' worth of harness and no horses. The driver waits, tall and silent.",
             go="castle_courtyard", go_cond="has:crucifix", go_fail="Not yet. The hostess's warning still rings in my ears."),
        prop("sign2", "signpost", "dark", -5.6, 2.4, rot=20, name="Signpost", radius=0.3,
             look="The Borgo Pass. A track climbing toward the Carpathian night."),
        prop("flame", "candle", "red", -2.4, -2.8, name="Blue flame", radius=0.4,
             look="A faint blue flame flickers over the grass. They say gold is buried where it burns.",
             take="stake", take_text="I mark the spot, and pull up a sharpened stake that someone left nearby. It may serve.", give_once=True),
        prop("tree_d", "deadtree", "grey", 4.4, -3.6, name="Dead tree", radius=0.5, look="Bare against the clouds."),
    ],
    npcs=[
        npc("driver", "human_coachman", "driver", 3.0, 1.2, rot=-60, name="Driver",
            look="A tall driver with a long brown beard, a black hat, and eyes that shine red in the lamp.",
            talk="driver", radius=0.6),
        npc("wolf1", "wolf", "grey", -5.2, -2.6, rot=140, name="Wolf", look="Yellow eyes in the dark. The howling is close.", radius=0.6, roam=True,
            fight="borgo_wolves"),
        npc("wolf2", "wolf_big", "black", -6.4, -1.0, rot=120, name="Wolf", look="The pack grows bold. Near the driver, they cower.", radius=0.7, roam=True,
            fight="borgo_wolves"),
    ],
)

LOC_DATA["castle_courtyard"] = dict(
    cells=[3, 3], wall="stone_mossy", floor="cobble", interior=False, night=True,
    ambient=dict(color="#2a3350", energy=0.85, fog="#0c0f18"),
    camera=dict(pos=[0, 5.8, 11], look=[0, 1.2, -1.5], fov=55),
    lights=[dict(pos=[0, 5, 0], color="#a0b4ff", energy=1.4, range=18), dict(pos=[0, 1.8, -5.4], color="#ff9040", energy=1.2, range=6)],
    moon=dict(pos=[-14, 17, -22]),
    walls=dict(west=["wall_4", "wall_4", "wall_4"], east=["wall_4", "wall_door_4", "wall_4"]),
    spawn=[0, 4.2], spawns={"great_hall": [0, -3.4], "borgo_pass": [0, 4.2], "chapel_crypt": [4.6, 0.0]},
    props=[
        prop("keep", "castle_keep", "stone_dark", 0, -9.6, scale=1.0, name=None, radius=0.01),
        prop("gate_door", "door_big", "ebony", 0, -5.2, name="Great door", radius=1.0,
             look="A great door, old and studded with large iron nails. No light, no sound.",
             go="great_hall", go_cond="flag:knocked", set="knocked",
             set_text="I knocked. After a moment, the sound of a heavy step behind the door. A key turns, chains rattle. I wait."),
        prop("well", "barrel", "dark", -3.4, 1.0, name="Rain barrel", radius=0.4, look="Stagnant water. A bat flits across the surface."),
        prop("lantern_c", "lantern", "default", -4.6, -3.6, y=0.0, name="Old lantern", radius=0.3,
             look="A rusted lantern, long burned dry."),
        prop("chapel_gate", "door", "dark", 5.8, 0.0, rot=-90, name="Chapel path", radius=0.5,
             look="A path leads toward the ruined chapel at the edge of the castle.",
             go="chapel_crypt", go_cond="has:hammer", go_fail="A rusted iron lock bars the way. Something heavy might break it."),
        prop("column1", "column", "stone_mossy", -3.0, -4.6, name=None, radius=0.35),
        prop("column2", "column", "stone_mossy", 3.0, -4.6, name=None, radius=0.35),
    ],
    npcs=[],
)

LOC_DATA["great_hall"] = dict(
    cells=[3, 3], wall="stone_dark", floor="cobble", interior=True,
    ambient=dict(color="#2a1c18", energy=0.55, fog="#0e0806"),
    camera=dict(pos=[0, 4.8, 9.2], look=[0, 1.0, -1.6], fov=55),
    lights=[dict(pos=[3, 2.8, -4], color="#ff8030", energy=3.0, range=11), dict(pos=[0, 3.0, 2], color="#ffa860", energy=1.8, range=10)],
    walls=dict(north=["wall_4", "wall_door_4", "wall_4"], west=["wall_4", "wall_door_4", "wall_4"], east=["wall_4", "wall_door_4", "wall_4"]),
    spawn=[0, -4.0], spawns={"castle_courtyard": [0, -4.0], "harker_room": [-4.4, 0.0], "library": [4.4, 0.0]},
    props=[
        prop("fire_h", "fireplace", "stone_grey", 4.0, -5.4, name="Great fireplace", radius=1.0, look="A fire the size of a man burns in the grate. It is the only warmth in the castle."),
        prop("table_h", "table_long", "ebony", 0, 0.5, name="Dining table", radius=2.2,
             look="Laid for one. The Count says he has already dined, and does not drink... wine."),
        prop("chair_h", "chair", "black", 0, 1.9, rot=180, name="My chair", radius=0.4, look="Set for me."),
        prop("throne_h", "throne", "black", -2.6, -2.8, name="The Count's chair", radius=0.6, look="Empty. He does not eat in my presence."),
        prop("wine_h", "bottle", "amber", 1.3, 0.5, y=0.8, name="Tokay", radius=0.1, look="Golden Tokay, old and rich.", take="wine", take_text="I took the bottle."),
        prop("garlic_h", "garlic", "default", -1.2, 0.5, y=0.8, name="Garlic flowers", radius=0.1,
             look="A bowl of garlic flowers, set out unaccountably on the Count's table.",
             take="garlic", take_text="I took a handful of garlic flowers.", give_once=True),
        prop("candelabra_h", "candelabra", "default", 1.5, -1.8, name="Candelabra", radius=0.3, look="Golden candlesticks, long past polishing."),
        prop("door_room", "door", "ebony", -5.8, 0.0, rot=90, name="Door to my bedroom", radius=0.6,
             look="My bedroom. The Count showed me there himself.", go="harker_room"),
        prop("door_lib", "door", "ebony", 5.8, 0.0, rot=-90, name="Door to the library", radius=0.6, look="The library.", go="library"),
        prop("door_out_h", "door_big", "ebony", 0, -5.8, name="Great door", radius=0.8, look="The door to the courtyard.", go="castle_courtyard"),
        prop("bust_h", "bust", "stone_tomb", -4.6, -4.2, name="Stone bust", radius=0.4, look="A carved face of some forgotten ancestor, scarred with age."),
        prop("col_h1", "column", "stone_dark", -3.4, -3.0, name=None, radius=0.35),
        prop("col_h2", "column", "stone_dark", 3.4, -3.0, name=None, radius=0.35),
        prop("rug_h", "rug", "red", 0, 0.5, radius=0.01),
    ],
    npcs=[
        npc("count", "human_dracula", "count", 1.6, -2.0, rot=0, name="Count Dracula",
            look="A tall old man, clean shaven save for a long white moustache, clad in black from head to foot. His hand is cold as ice.",
            talk="count", radius=0.6),
    ],
)

LOC_DATA["harker_room"] = dict(
    cells=[2, 2], wall="plaster", floor="planks", interior=True,
    ambient=dict(color="#241c18", energy=0.6, fog="#0e0a08"),
    camera=dict(pos=[0, 4.2, 8.5], look=[0, 1.1, -0.5], fov=52),
    lights=[dict(pos=[0, 2.6, -1], color="#ffb060", energy=2.2, range=9)],
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[3.0, 2.0], spawns={"great_hall": [3.0, 2.0]},
    props=[
        prop("bed_r", "bed", "red", -2.2, -2.3, name="Bed", radius=1.0, look="A four-poster. I sleep here, though not easily.", rot=0),
        prop("mirror_r", "mirror", "default", 1.5, -3.7, y=0.8, name="Shaving mirror", radius=0.4,
             look="Cutting myself shaving, the Count's hand seized my throat... and in the glass there was no reflection of him at all.",
             take="razor", take_text="I unhooked the little glass. Whatever he is, he cannot be seen in it.", set="a1_mirror_seen"),
        prop("table_r", "table", "dark", 1.8, 0.6, name="Writing desk", radius=0.9, look="Paper, ink, and no one to write to."),
        prop("diary_r", "book", "diary", 1.8, 0.6, y=0.8, name="My journal", radius=0.2,
             look="My journal, kept in shorthand.", take="diary", take_text="I will not be parted from my journal."),
        prop("chest_r", "chest", "dark", -3.0, 1.2, name="Locked chest", radius=0.6,
             look="A locked chest. Forced from within? Or from without?", use_item={"key": [{"say": "The iron key turns. Inside, a mason's hammer and a fistful of garlic bulbs."}, {"give": "hammer"}, {"give": "garlic"}, {"set": "chest_open"}]},
             use_fail="It will not open."),
        prop("candle_r", "candelabra", "default", 3.4, -2.6, name="Candelabra", radius=0.3, look="Four candles. A fifth would not hurt."),
        prop("door_r", "door", "ebony", 3.8, 2.0, rot=-90, name="Door to the hall", radius=0.6, look="The hall.", go="great_hall"),
        prop("rug_r", "rug", "green", 0, 0.5, radius=0.01),
    ],
    npcs=[],
)

LOC_DATA["library"] = dict(
    cells=[2, 2], wall="stone_dark", floor="planks", interior=True,
    ambient=dict(color="#201a14", energy=0.55, fog="#0e0a06"),
    camera=dict(pos=[0, 4.2, 8.5], look=[0, 1.1, -0.5], fov=52),
    lights=[dict(pos=[0, 2.6, -1], color="#ffc070", energy=2.2, range=9)],
    walls=dict(north=["wall_4", "wall_4"], west=["wall_door_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[-3.0, -1.0], spawns={"great_hall": [-3.0, -1.0], "old_wing": [3.0, -1.0]},
    props=[
        prop("shelf1", "bookshelf", "dark", -1.6, -3.55, name="Bookshelves", radius=0.8,
             look="English books on every subject - law, history, geography... and 'Bradshaw's Guide'. The Count has studied England thoroughly.", ),
        prop("shelf2", "bookshelf", "dark", 1.8, -3.55, name="Bookshelves", radius=0.8,
             look="More English books, thick and well-thumbed."),
        prop("table_l", "table", "dark", 0.8, 0.5, name="Reading table", radius=0.9, look="Magazines, newspapers, and a London directory."),
        prop("chair_l", "chair", "green", 0.8, 1.8, rot=180, name="Chair", radius=0.4, look="The Count's favourite chair, I think."),
        prop("candle_l", "candelabra", "default", 3.2, 2.0, name="Candelabra", radius=0.3, look="It burns day and night."),
        prop("door_l", "door", "ebony", -3.8, -2.0, rot=90, name="Door to the hall", radius=0.6, look="The hall.", go="great_hall"),
        prop("door_old", "door", "dark", 3.8, -2.0, rot=-90, name="Locked door", radius=0.6,
             look="'Whatever you do, do not sleep in any other part of the castle.' This door leads there.",
             go="old_wing", go_cond="has:lantern", go_fail="Too dark. I need a light before I go beyond that door."),
    ],
    npcs=[],
)

LOC_DATA["old_wing"] = dict(
    cells=[2, 2], wall="stone_mossy", floor="cobble", interior=True,
    ambient=dict(color="#101018", energy=0.35, fog="#04040a"),
    camera=dict(pos=[0, 4.2, 8.5], look=[0, 1.1, -0.5], fov=52),
    lights=[dict(pos=[0, 2.4, 0], color="#6080ff", energy=1.4, range=8)],
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_door_4", "wall_4"], east=["wall_4", "wall_4"]),
    spawn=[-3.0, -1.0], spawns={"library": [-3.0, -1.0]},
    props=[
        prop("couch", "bed_simple", "black", 1.4, -2.0, name="Dusty couch", radius=1.0,
             look="Here, in the moonlight, I let myself fall asleep. I should not have.", rot=0),
        prop("table_o", "table", "ebony", -2.0, -2.5, name="Old table", radius=0.9, look="A lady's embroidery frame, dusty with years."),
        prop("garlic_o", "garlic", "default", -2.0, -2.5, y=0.8, name="Garlic flowers", radius=0.1, look="Dried garlic flowers, left on the table. They are old.",
             take="garlic", take_text="I took the garlic flowers. A superstition? Maybe not.", give_once=True),
        prop("door_o", "door", "dark", -3.8, -2.0, rot=90, name="Door to the library", radius=0.6, look="Back to the library.", go="library"),
        prop("window_o", "mirror", "default", 3.3, -3.7, y=0.8, name="Tarnished mirror", radius=0.3, look="Black with age. Nothing stares back."),
    ],
    npcs=[
        npc("bride_a", "human_bride", "bride1", -1.2, -0.4, rot=20, name="Fair woman",
            look="One was dark, and had great aquiline nose, like the Count; the other fair, with great masses of golden hair and eyes like pale sapphires.",
            talk="brides", radius=0.5),
        npc("bride_b", "human_bride", "bride2", 0.2, -1.0, rot=0, name="Dark woman", look="They whispered together and laughed - a silvery, musical laugh, as hard as glass.", talk="brides", radius=0.5),
        npc("bride_c", "human_bride", "bride3", 1.2, 0.0, rot=-20, name="Third sister", look="'He is young and strong; there are kisses for us all.'", talk="brides", radius=0.5),
    ],
)

LOC_DATA["chapel_crypt"] = dict(
    cells=[3, 2], wall="stone_tomb", floor="dirt", interior=True,
    ambient=dict(color="#141420", energy=0.4, fog="#050509"),
    camera=dict(pos=[0, 4.6, 9.5], look=[0, 1.1, -1], fov=54),
    lights=[dict(pos=[0, 2.4, 0], color="#8090ff", energy=2.0, range=10), dict(pos=[-3, 1.8, -2], color="#ff7030", energy=1.2, range=6)],
    walls=dict(north=["wall_4", "wall_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[5.0, -1.0], spawns={"castle_courtyard": [5.0, -1.0]},
    props=[
        prop("coffin1", "coffin", "dark", -1.6, -1.5, rot=90, name="Earth box", radius=1.0, look="One of fifty boxes of earth, newly dug, I think."),
        prop("coffin2", "coffin", "ebony", 1.6, -1.5, rot=90, name="Earth box", radius=1.0,
             look="The lid is open. The Count lies within, eyes open, stony and without colour. Not breathing. A key hangs at his belt.",
             take="vault_key", take_text="With shaking hands I take the keys from his belt. He does not stir.", give_once=True,
             use_item={"stake": [{"say": "I raise the stake... and my arm will not obey me. Alone, with only this, I am no match for him. Not yet."}]}),
        prop("tomb_c", "tomb", "stone_tomb", -0.2, -3.3, name="Stone tomb", radius=1.0, look="Worn letters. 'Dracula'. The rest is lost."),
        prop("cross_c", "crucifix_big", "silver", 3.6, -3.2, name="Crucifix", radius=0.3, look="Even here, the cross endures. The Count would flinch from it."),
        prop("candle_c", "candelabra", "default", -3.6, -3.0, name="Candelabra", radius=0.3, look="Its flames lean toward the coffin."),
        prop("door_c", "door", "dark", 5.8, -2.0, rot=-90, name="Door to the courtyard", radius=0.6, look="Back to the night air.", go="castle_courtyard"),
        prop("goal", "stairs", "stone_tomb", -4.6, 1.0, rot=90, name="Stair to the old vault", radius=0.8,
             look="A narrow stair beneath the chapel. Perhaps the road to freedom - perhaps worse.",
             talk="a1_vault_stairs"),
    ],
    npcs=[],
)

LOC_DATA["chapel_crypt"]["on_enter"] = [dict(do=[{"journal": "a1_j6"}])]
LOC_DATA["old_wing"]["on_enter"] = [dict(do=[{"journal": "a1_j5"}])]
LOC_DATA["harker_room"]["on_enter"] = [dict(**{"if": "flag:a1_mirror_seen"}, do=[{"journal": "a1_j4"}])]

# --------------------------------------------------------------------------- #
# dialogue
# --------------------------------------------------------------------------- #
DIALOGUE = {
    "a1_vault_stairs": dict(start="n0", nodes={
        "n0": dict(speaker="Jonathan Harker", text="A narrow stair goes down beneath the chapel. A heavy door bars the foot of it; the Count's keys hang in my hand. Below, I can hear the Szgany loading boxes of earth.",
                   choices=[dict(text="[Descend with the Count's keys]", cond="has:vault_key", next="n1"),
                            dict(text="[The door is locked. Go back]", cond="!has:vault_key", end=True),
                            dict(text="[Not yet]", end=True)]),
        "n1": dict(speaker="Jonathan Harker", text="The key turns. This is my last throw. Whatever lies below - better to die like a man than to wait for those women.",
                   do=[{"journal": "a1_j7"},
                       {"card": "30 June. Castle Dracula.\n\n\"I shall try to scale the castle wall once more, and get away. It is the last chance I have. Good-bye, all! Mina!\"\n\nBut that night, far away on the English coast, another story had already begun..."},
                       {"goto": "a2_whitby_lodging"}]),
    }),
    "hostess": dict(start="n0", nodes={
        "n0": dict(speaker="Hostess", text="Must you go, Herr Harker? It is the eve of St. George's Day. Do you not know that at midnight all the evil things in the world will have full sway?",
                   choices=[dict(text="I must. A client waits at the castle.", next="n1"),
                            dict(text="What evil things?", next="n2")]),
        "n1": dict(speaker="Hostess", text="Then take this for your mother's sake. Wear it round your neck.",
                   do=[{"give": "crucifix"}, {"journal": "a1_j1"}, {"say": "She hung the crucifix round my neck. I did not like it - a stern Englishman's creed - but I took it."}], end=True),
        "n2": dict(speaker="Hostess", text="Ah, the Count's land is not as ours. At night the dead ride fast. Please, take this.", next="n1"),
    }),
    "landlord": dict(start="n0", nodes={
        "n0": dict(speaker="Landlord", text="Herr Engländer... the Count's castle is no place... *he stumbles, shakes his head*. Eat. Rest. The coach comes at midnight.", end=True),
    }),
    "driver": dict(start="n0", nodes={
        "n0": dict(speaker="Driver", text="*In a deep, hollow voice* We are early tonight, sir. The wolves have been bold. Get in.", do=[{"journal": "a1_j2"}],
                   choices=[dict(text="Do you know the Count?", next="n1"),
                            dict(text="[Board the calèche]", cond="has:crucifix", do=[{"goto": "castle_courtyard"}]),
                            dict(text="[Not yet]", end=True)]),
        "n1": dict(speaker="Driver", text="*His eyes glint red.* Everyone in this land knows the Count, sir. Few have seen him.", next="n0"),
    }),
    "count": dict(start="n0", nodes={
        "n0": dict(speaker="Count Dracula", text="Welcome to my house! Enter freely and of your own will! The night is cold, and you need to eat and rest.",
                   choices=[dict(text="Your English is flawless, Count.", next="n1"),
                            dict(text="I am pleased to be here. I have the papers for Carfax.", next="n2"),
                            dict(text="[Leave]", end=True)]),
        "n1": dict(speaker="Count Dracula", text="I am anxious to speak as the English do. Here I am noble; I am a Count. But in London no one would know me. I should be as the others - a stranger.", next="n0"),
        "n2": dict(speaker="Count Dracula", text="Good. Whenever you want anything, ring. Only - you will remember? - do not sleep anywhere in my house save in your own room.", do=[{"set": "warned"}, {"journal": "a1_j3"}], next="n0"),
    }),
    "brides": dict(start="n0", nodes={
        "n0": dict(speaker="Fair woman", text="'Go on! You are first, and we shall follow. Yours is the right to begin.' *They giggle, silvery and cold.*",
                   choices=[dict(text="[Hold up the crucifix]", cond="has:crucifix", next="n1"),
                            dict(text="[Back away]", end=True)]),
        "n1": dict(speaker="Fair woman", text="*She hisses, falls back.* 'Take that away! He will not let us feed on you tonight. Not yet.'",
                   do=[{"say": "A great flurry of wind - the Count was there, furious. 'How dare you touch him? This man belongs to me!'"}], end=True),
    }),
}


# --------------------------------------------------------------------------- #
# seed variation data (consumed by scripts/worldgen.gd at new-game time)
# palettes: look of a location; placements: where a quest item can be hidden;
# gates: alternative requirements for the same door. All options keep the game solvable.
# --------------------------------------------------------------------------- #
PALETTES = {
    "golden_krone": [dict(wall="plaster_dirty", floor="planks", wood="dark", cloth="red"),
                     dict(wall="plaster", floor="planks", wood="oak", cloth="green"),
                     dict(wall="stone_grey", floor="cobble", wood="ebony", cloth="blue")],
    "borgo_pass": [dict(floor="grass", tree="dark"), dict(floor="dirt", tree="green"), dict(floor="grass", tree="snow")],
    "castle_courtyard": [dict(wall="stone_mossy", floor="cobble"), dict(wall="stone_dark", floor="cobble"),
                         dict(wall="stone_grey", floor="stone_dark")],
    "great_hall": [dict(wall="stone_dark", floor="cobble", wood="ebony", cloth="red"),
                   dict(wall="stone_grey", floor="cobble", wood="dark", cloth="black"),
                   dict(wall="stone_mossy", floor="stone_dark", wood="ebony", cloth="blue")],
    "harker_room": [dict(wall="plaster", floor="planks", wood="dark", cloth="red"),
                    dict(wall="plaster_dirty", floor="planks", wood="pale", cloth="green"),
                    dict(wall="stone_grey", floor="planks", wood="oak", cloth="blue")],
    "library": [dict(wall="stone_dark", floor="planks", wood="dark", cloth="green"),
                dict(wall="plaster_dirty", floor="planks", wood="ebony", cloth="red"),
                dict(wall="stone_grey", floor="planks", wood="oak", cloth="blue")],
    "old_wing": [dict(wall="stone_mossy", floor="cobble", wood="ebony", cloth="black"),
                 dict(wall="stone_dark", floor="stone_dark", wood="dark", cloth="blue")],
    "chapel_crypt": [dict(wall="stone_tomb", floor="dirt"), dict(wall="stone_mossy", floor="dirt"),
                     dict(wall="stone_dark", floor="cobble")],
}

PLACEMENTS = {
    "lantern": [
        dict(prop="lantern_c", text="I took the lantern. It will serve in the dark places.", hint="Someone left a working lantern against the wall."),
        dict(prop="well", text="Behind the barrel, a lantern, still warm. Someone was here just now.", hint="The barrel stands a little away from the wall, as if moved."),
        dict(prop="column1", text="A lantern sits in the shadow at the foot of the column. I take it.", hint="A faint glint at the column's foot."),
    ],
    "key": [
        dict(prop="shelf2", text="Hidden in the hollowed pages of a book: an iron key. Why would the Count hide it here?", hint="One thick volume stands out on this shelf. It feels hollow."),
        dict(prop="shelf1", text="Behind the row of law books, an iron key on a nail.", hint="The dust is wiped away behind one row of books."),
        dict(prop="table_l", text="Under the London directory lay an iron key.", hint="The directory is lying a little crooked, as if lifted."),
        dict(prop="candle_l", text="Under the candelabra's base, a flat iron key.", hint="The candelabra stands on something that is not quite flat."),
        dict(prop="throne_h", text="In the cushion of the Count's chair - an iron key sewn into the lining.", hint="One seam of the cushion is freshly stitched."),
        dict(prop="bed_r", text="Under the pillow of my own bed lay an iron key. Left for me, or for someone else?", hint="The pillow is lumpy."),
    ],
    "brass_key": [
        dict(prop="throne_h", text="A brass key lies in the folds of the cushion.", hint="Something small glints in the cushion."),
        dict(prop="well", text="In the rain barrel, under the water: a brass key.", hint="Something yellow glimmers beneath the water."),
        dict(prop="table_h", text="Under the table cloth, taped to the underside: a brass key.", hint="One corner of the table-cloth hangs oddly."),
        dict(prop="column1", text="Wedged in a crack of the column: a brass key.", hint="There is a crack in the column's base."),
    ],
}

GATES = {
    "door_old": [
        dict(cond="has:lantern", fail="Too dark. I need a light before I go beyond that door.", needs="lantern"),
        dict(cond="has:brass_key", fail="It is locked. The keyhole is small and brass-bright.", needs="brass_key"),
    ],
}
ITEMS["brass_key"] = dict(name="Brass key", asset="key", variant="default", desc="A small brass key. It belongs to some inner door.")

JOURNAL = {
    "a1_j1": dict(title="3 May. Bistritz", source="Jonathan Harker's journal", text="Left Munich at 8:35 P.M. The impression I had was that we were leaving the West and entering the East. At the Golden Krone the landlord's wife begged me not to go: it is the eve of St. George's Day. She gave me a crucifix."),
    "a1_j2": dict(title="The driver", source="Jonathan Harker's journal", text="Four black horses stood where there had been none. A tall driver with a long brown beard and eyes that seemed red in the lamplight. Wolves howled all about us."),
    "a1_j3": dict(title="The Count", source="Jonathan Harker's journal", text="A tall old man, clean shaven save for a long white moustache, clad in black from head to foot. His hand was as cold as ice. 'Welcome to my house! Enter freely and of your own will!' I am not to sleep in any other part of the castle."),
    "a1_j4": dict(title="The shaving glass", source="Jonathan Harker's journal", text="I was shaving when I felt a hand on my shoulder. I had seen no one come in, and in the glass there was no reflection of him at all. I cut myself. The Count seized my throat - then drew back at the crucifix."),
    "a1_j5": dict(title="The three women", source="Jonathan Harker's journal", text="In the forbidden part of the castle, in the moonlight, three young women whispered by my couch: 'He is young and strong; there are kisses for us all.' The Count's fury dispersed them. I am a prisoner."),
    "a1_j6": dict(title="Fifty boxes of earth", source="Jonathan Harker's journal", text="In the old chapel I found fifty great boxes of earth. In one of them lay the Count - eyes open, stony, without colour. Not dead and not alive. I took the keys from his belt."),
    "a1_j_cat": dict(title="Beneath the chapel", source="Jonathan Harker's journal", text="With the Count's keys I tried the low iron door beside his box. A stair, worn hollow by feet long turned to dust, led down into the earth. The air was cold and stale, and somewhere far below water dripped. If this castle has a heart, it lies under here."),
    "a1_j_cliff": dict(title="The iron door", source="Jonathan Harker's journal", text="The iron door gave at last under the hammer. Beyond lay a ledge of rock, the wind, and a drop into the black gorge. Across the gap rose the castle's south wall, and in it one window. I knew that window. It was mine. There is no road out this way - only the road I already know."),
    "a1_j_gold": dict(title="The heaped gold", source="Jonathan Harker's journal", text="In a vaulted chamber lay a great heap of gold - Roman, British, Austrian, Hungarian, Greek and Turkish coin - under a film of dust. None of it, I noticed, was less than three hundred years old. A man with such a hoard has no need to keep a guest, unless he wants something more."),
    "a1_j7": dict(title="30 June. The last chance", source="Jonathan Harker's journal", text="The Szgany are loading the boxes onto wagons. The Count means to go to England. If I can escape, I may warn them. Good-bye, all! Mina!"),
}

BIBLE = dict(title="Dracula: The Borgo Pass", assets=ASSETS, variants=VARIANTS, role_defaults=ROLE_DEFAULTS,
             locations=LOCATIONS, characters=CHARACTERS, props=PROPS,
             items=ITEMS, loc_data=LOC_DATA, dialogue=DIALOGUE, palettes=PALETTES, placements=PLACEMENTS, gates=GATES, start_location="golden_krone")

def merge_acts(bible):
    """Merge pipeline/acts/act_*.py (one module per story act) into the bible. Duplicate ids are errors."""
    import importlib
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    bible["journal"] = dict(JOURNAL)
    bible["encounter_hooks"] = {}
    bible["acts"] = [dict(id=1, title="Transylvania", module="bible_src",
                          start=dict(location="golden_krone", protagonist="harker", party=["harker"], items={}, flags=[]),
                          exit_to="a2_whitby_lodging")]
    bible["encounters_extra"] = {}
    bible["enemies_extra"] = {}
    bible["recipes_extra"] = {}
    import os
    only = os.environ.get("ONLY_ACT")      # validate/build a single act without touching the others
    only_arc = os.environ.get("ONLY_ARC")  # same for a personal arc
    bible["arcs_list"] = []
    acts_dir = Path(__file__).resolve().parent / "acts"
    files = [(f, "act") for f in sorted(acts_dir.glob("act_[0-9]*.py"))] + [(f, "arc") for f in sorted(acts_dir.glob("arc_*.py"))]
    for f, kind in files:
        if f.stem.endswith("_builders"):
            continue
        if kind == "act" and (only and f.stem != f"act_{only}" or only_arc):
            continue
        if kind == "arc" and (only_arc and f.stem != f"arc_{only_arc}" or (only and not only_arc)):
            continue
        m = importlib.import_module("acts." + f.stem)
        if kind == "arc":
            bible["arcs_list"].append(dict(m.ARC, module=f.stem))
        else:
            bible["acts"].append(dict(m.ACT, module=f.stem))
        ids = {a["id"] for a in bible["assets"]}
        for a in getattr(m, "ASSETS", []):
            assert a["id"] not in ids, f"{f.stem}: duplicate asset {a['id']}"
            bible["assets"].append(a)
            ids.add(a["id"])
        for k, v in getattr(m, "VARIANTS", {}).items():
            if k in bible["variants"]:
                bible["variants"][k].update({kk: vv for kk, vv in v.items() if kk != "default"})
            else:
                bible["variants"][k] = v
        bible["role_defaults"].update(getattr(m, "ROLE_DEFAULTS", {}))
        for meta in getattr(m, "LOCATIONS", []):
            assert not any(l["id"] == meta["id"] for l in bible["locations"]), f"{f.stem}: duplicate location meta {meta['id']}"
            bible["locations"].append(meta)
        for k, v in getattr(m, "LOC_DATA", {}).items():
            assert k not in bible["loc_data"], f"{f.stem}: duplicate location {k}"
            bible["loc_data"][k] = v
        for key, dst in (("DIALOGUE", "dialogue"), ("ITEMS", "items"), ("PLACEMENTS", "placements"), ("GATES", "gates"),
                         ("PALETTES", "palettes"), ("JOURNAL", "journal"), ("ENCOUNTER_HOOKS", "encounter_hooks"),
                         ("ENCOUNTERS_EXTRA", "encounters_extra"), ("ENEMIES_EXTRA", "enemies_extra"),
                         ("RECIPES_EXTRA", "recipes_extra")):
            for k, v in getattr(m, key, {}).items():
                assert k not in bible[dst], f"{f.stem}: duplicate {dst} id {k}"
                bible[dst][k] = v
    return bible


merge_acts(BIBLE)

if __name__ == "__main__":
    import sys
    if "--out" in sys.argv:
        OUT = Path(sys.argv[sys.argv.index("--out") + 1])
    OUT.write_text(json.dumps(BIBLE, indent=1, ensure_ascii=False))
    print(f"wrote {OUT.name}: {len(ASSETS)} assets, {len(VARIANTS)} variant sets, {len(LOC_DATA)} locations")
