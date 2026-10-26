"""Helpers for writing act files (pipeline/acts/act_N.py). Import with:  from dsl import *"""


def T(tex, tint="#ffffff"):
    """A texture reference for a material role: procedural texture id + tint."""
    return {"tex": tex, "tint": tint}


def prop(id, asset, variant, x, z, rot=0, scale=1.0, y=0.0, name=None, look=None, radius=0.5, cond=None, **interact):
    """Static or interactive prop. interact keys: look, take(+take_text, give_once), set(+set_text), go(+go_cond, go_fail),
    talk, fight, end_text, use_item={item:[do..]}, use_fail. cond = visibility condition (the 'if' field)."""
    p = dict(id=id, asset=asset, variant=variant, pos=[x, y, z], rot=rot, scale=scale, radius=radius)
    if name:
        p["name"] = name
    if cond:
        p["if"] = cond
    if look:
        interact["look"] = look
    if interact:
        p["interact"] = interact
    return p


def npc(id, asset, variant, x, z, rot=0, name="", look="", talk=None, radius=0.5, cond=None, **extra):
    d = dict(id=id, asset=asset, variant=variant, pos=[x, 0, z], rot=rot, name=name, radius=radius,
             interact={"look": look, **({"talk": talk} if talk else {}), **extra})
    if cond:
        d["if"] = cond
    return d


def human_colors(**over):
    d = {"skin": T("skin", "#e8c3a0"), "eyes": T("flat", "#201510"), "mouth": T("flat", "#8a3a3a"),
         "hair": T("hair", "#4a3322"), "top": T("wool", "#5a4632"), "bottom": T("wool", "#3a3128"),
         "shoes": T("leather", "#2a1d14"), "accent": T("cloth", "#2a2a2a"), "cloak": T("cloth", "#111111")}
    d.update(over)
    return d


STONE = {
    "stone_grey": {"stone": T("stone_blocks")}, "stone_mossy": {"stone": T("stone_moss")},
    "stone_dark": {"stone": T("stone_blocks", "#6a6a74")}, "stone_tomb": {"stone": T("stone_rough", "#d2cdc0")},
    "plaster": {"stone": T("plaster", "#e8dfcc")}, "plaster_dirty": {"stone": T("plaster", "#9a8f78")},
    "cobble": {"stone": T("cobble")}, "planks": {"stone": T("wood_planks", "#cdb89a")},
    "dirt": {"stone": T("dirt")}, "grass": {"stone": T("grass")}, "snow": {"stone": T("snow")},
}
WOOD = {"oak": {"wood": T("wood_planks")}, "dark": {"wood": T("wood_planks", "#6a5040")},
        "pale": {"wood": T("wood_planks", "#e6d3aa")}, "ebony": {"wood": T("wood_planks", "#3a2a22")}}
FABRIC = {"red": T("velvet", "#7a1a1f"), "blue": T("cloth", "#2a3e6a"), "green": T("cloth", "#2e4a30"),
          "black": T("cloth", "#1a1a1a"), "cream": T("cloth", "#d8ccb0")}


def cam(cells, y_extra=0.0):
    """Default fixed camera for a room of `cells` (cx, cz) 4 m cells. Returns the `camera` dict."""
    d = cells[1] * 4.0
    return dict(pos=[0, 3.2 + 0.3 * d + y_extra, d / 2 + 4.5], look=[0, 1.0, -d * 0.12], fov=52 if d <= 8 else 55)


# ambient presets: color = ambient light, fog = background/fog colour, energy = strength
AMBIENT = {
    "candle_interior": dict(color="#3a2c20", energy=0.55, fog="#140e08"),
    "warm_day_interior": dict(color="#5a4a38", energy=0.9, fog="#2a2018"),
    "cold_interior": dict(color="#242a3a", energy=0.5, fog="#0a0c12"),
    "night_exterior": dict(color="#2a3a5c", energy=0.9, fog="#0e1522"),
    "day_exterior": dict(color="#7a8aa0", energy=1.3, fog="#a8b4c0"),
    "dusk_exterior": dict(color="#5a4a60", energy=1.0, fog="#3a2a38"),
    "storm_exterior": dict(color="#3a4048", energy=0.8, fog="#20262c"),
    "crypt": dict(color="#141420", energy=0.4, fog="#050509"),
    "sea_fog": dict(color="#6a7a88", energy=1.1, fog="#8a98a4"),
}


def lights_warm(cells, n=2, energy=2.4):
    """A couple of warm omni lights for an interior (flicker automatically)."""
    w, d = cells[0] * 4.0, cells[1] * 4.0
    pts = [[0, 2.6, -d * 0.25], [-w * 0.3, 1.9, d * 0.2], [w * 0.3, 1.9, d * 0.2]]
    return [dict(pos=p, color="#ff9a40", energy=energy * (1.0 if i == 0 else 0.55), range=max(w, d) * 1.1) for i, p in enumerate(pts[:n])]


def lights_moon(energy=3.0):
    return [dict(pos=[-4, 6, 2], color="#8aa6ff", energy=energy, range=24), dict(pos=[4, 4, 4], color="#aab8ff", energy=energy * 0.5, range=16)]


def lights_day(energy=3.2):
    return [dict(pos=[0, 8, 4], color="#fff2d8", energy=energy, range=30), dict(pos=[-5, 5, -2], color="#d8e4ff", energy=energy * 0.5, range=22)]
