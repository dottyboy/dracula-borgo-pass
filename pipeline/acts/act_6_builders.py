"""Extra 3D builders for Act VI (steam launch, leiter-wagon, earth box). `math` is injected by blender_gen."""


def b_a6_launch(a):
    """A small steam launch, bow toward -Y (= +z, the camera, in game)."""
    a.part("launch")
    a.box((1.5, 4.6, 0.6), (0, 0.2, 0.35), "wood")                       # hull
    a.box((1.1, 1.2, 0.5), (0, -2.6, 0.38), "wood")                      # bow block
    a.box((0.5, 0.8, 0.45), (0, -3.3, 0.36), "wood")                     # stem
    a.box((1.2, 4.4, 0.06), (0, 0.2, 0.68), "wood")                      # deck
    a.box((1.2, 1.6, 0.9), (0, 0.9, 1.15), "wood")                       # cabin
    a.box((1.3, 1.8, 0.07), (0, 0.9, 1.63), "wood")                      # cabin roof
    for sx in (-1, 1):
        a.box((0.04, 0.5, 0.35), (sx * 0.61, 0.9, 1.25), "glass")
    a.cyl(0.22, 1.3, (0, -0.55, 1.35), "iron", r2=0.17, seg=10)           # funnel
    a.cyl(0.25, 0.1, (0, -0.55, 2.02), "iron", seg=10)
    a.cyl(0.35, 0.5, (0, -0.35, 0.95), "iron", seg=10)                   # boiler
    a.box((0.5, 0.5, 0.35), (0, 2.5, 0.88), "iron")                      # engine
    a.cyl(0.04, 1.0, (0.3, -3.2, 1.2), "wood", seg=6)                     # flag staff
    a.box((0.02, 0.45, 0.28), (0.3, -3.45, 1.6), "cloth")
    a.sphere(0.1, (0, -2.8, 1.05), "flame", seg=6)                        # electric lamp at the bow


def b_a6_leiter_wagon(a):
    """Peasant ladder-wagon (leiter-wagon), flat bed for a long box. Front toward -Y."""
    a.part("wagon")
    a.box((1.3, 3.0, 0.1), (0, 0, 0.7), "wood")
    for sx in (-1, 1):
        a.box((0.06, 3.0, 0.5), (sx * 0.62, 0, 1.0), "wood")           # side rails
        for y in (-1.2, -0.6, 0.0, 0.6, 1.2):
            a.box((0.05, 0.05, 0.5), (sx * 0.62, y, 1.0), "wood")
        for y in (-1.0, 1.0):
            a.cyl(0.55, 0.09, (sx * 0.78, y, 0.55), "wood", seg=12, rot=(0, math.pi / 2, 0))
            a.cyl(0.09, 0.14, (sx * 0.78, y, 0.55), "iron", seg=8, rot=(0, math.pi / 2, 0))
    a.beam((0, -1.4, 0.7), (0, -3.0, 0.62), 0.09, "wood")                # shaft



def b_a6_earth_box(a):
    """A long wooden box of native earth with iron bands (the Count's resting place)."""
    a.part("box")
    a.box((0.8, 1.8, 0.6), (0, 0, 0.3), "wood")
    a.box((0.84, 1.84, 0.06), (0, 0, 0.62), "wood")
    for y in (-0.6, 0.0, 0.6):
        a.box((0.86, 0.07, 0.64), (0, y, 0.31), "iron")
    a.box((0.7, 1.6, 0.04), (0, 0, 0.66), "earth")


def b_a6_brig(a):
    """A small sea-going brig/schooner (the Czarina Catherine), bow toward -Y."""
    a.part("brig")
    a.box((2.2, 7.0, 0.9), (0, 0.3, 0.55), "wood")
    a.box((1.6, 1.8, 0.8), (0, -3.9, 0.7), "wood")
    a.box((0.8, 1.2, 0.7), (0, -5.0, 0.8), "wood")
    a.box((2.0, 6.8, 0.07), (0, 0.3, 1.02), "wood")
    a.box((2.3, 1.8, 0.7), (0, 3.2, 1.4), "wood")                          # poop deck
    for y, h in ((-1.4, 6.0), (1.2, 6.5)):
        a.cyl(0.11, h, (0, y, 1.0 + h / 2), "wood", seg=8)
        a.box((2.4, 0.06, 0.1), (0, y, 1.0 + h * 0.8), "wood")           # yard
        a.box((2.2, 0.04, h * 0.5), (0, y + 0.05, 1.0 + h * 0.5), "cloth")  # furled sail
    a.beam((0, -5.4, 1.2), (0, -1.4, 5.4), 0.04, "iron")                  # bowsprit stay
    a.box((0.9, 0.06, 0.5), (0, -4.3, 1.4), "wood")
