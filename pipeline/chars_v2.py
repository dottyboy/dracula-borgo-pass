"""Improved characters and creatures. Replaces b_human / b_wolf / b_bat of blender_gen (loaded as an override).

Humans are jointed: nested nodes hips > torso > head, arm_up_* > arm_low_*, leg_up_* > leg_low_* with pivots on the real joints
(shoulder, elbow, hip, knee, neck). The game animates them procedurally (scripts/actor.gd): walk cycle with knee/elbow bend,
idle breathing, talking gestures, attack/hurt/death poses. Model front = -Y in Blender (= +z in game); left = -X.
"""


def _hat(a, kind, hz, k, r):
    if kind == "top":
        a.cyl(r * 1.75, 0.018 * k, (0, 0, hz + 0.1 * k), "accent", seg=14)
        a.cyl(r * 1.02, 0.2 * k, (0, 0.0, hz + 0.2 * k), "accent", r2=r * 0.95, seg=14)
        a.cyl(r * 1.06, 0.035 * k, (0, 0, hz + 0.135 * k), "cloak", seg=14)
    elif kind == "bowler":
        a.cyl(r * 1.6, 0.015 * k, (0, 0, hz + 0.1 * k), "accent", seg=14)
        a.sphere(r * 1.05, (0, 0, hz + 0.115 * k), "accent", scale=(1, 1, 0.85), seg=12)
    elif kind == "wide":
        a.cyl(r * 2.5, 0.012 * k, (0, 0, hz + 0.095 * k), "accent", r2=r * 2.3, seg=16)
        a.cyl(r * 1.1, 0.12 * k, (0, 0, hz + 0.16 * k), "accent", r2=r * 0.95, seg=12)
        a.cyl(r * 1.13, 0.025 * k, (0, 0, hz + 0.125 * k), "cloak", seg=12)
    elif kind == "fur":
        a.cyl(r * 1.15, 0.13 * k, (0, 0, hz + 0.11 * k), "accent", r2=r * 1.0, seg=10)
        a.sphere(r * 1.1, (0, 0, hz + 0.17 * k), "accent", scale=(1, 1, 0.5), seg=10)
    elif kind == "cap":
        a.sphere(r * 1.08, (0, 0.005, hz + 0.075 * k), "accent", scale=(1, 1, 0.6), seg=12)
        a.box((r * 1.5, r * 0.9, 0.012 * k), (0, -r * 1.05, hz + 0.075 * k), "accent")
    elif kind == "shawl":
        a.sphere(r * 1.12, (0, 0.02 * k, hz + 0.02 * k), "accent", scale=(1.0, 1.05, 1.0), seg=12)
        a.sphere(r * 1.7, (0, 0.06 * k, hz - 0.14 * k), "accent", scale=(1.1, 0.8, 0.55), seg=12)
    elif kind == "bonnet":
        a.sphere(r * 1.12, (0, 0.03 * k, hz + 0.03 * k), "accent", scale=(1, 1.1, 1.05), seg=12)
        a.cyl(r * 1.15, 0.01 * k, (0, -r * 0.4, hz + 0.075 * k), "accent", seg=12, rot=(1.1, 0, 0))


def b_human(a, height=1.75, build=1.0, sex="m", hair="short", beard="none", garment="coat", hat="none",
            cloak=False, hunch=0.0, age=0, fangs=False):
    k = height / 1.75
    fem = sex == "f"
    b = build
    hip_z = 0.93 * k
    waist_z = 1.07 * k
    chest_z = 1.27 * k
    sh_z = 1.43 * k
    neck_z = 1.50 * k
    head_z = 1.65 * k
    sw = (0.205 if not fem else 0.175) * b            # half shoulder width
    hipw = (0.145 if not fem else 0.165) * b
    lean = 0.04 * hunch * k                           # stoop: head and chest forward (-Y)
    dress = garment in ("dress", "gown")

    # ---------------- hips (root of the body)
    a.part("hips", (0, 0, hip_z))
    a.cyl(hipw * 1.05, 0.2 * k, (0, 0, hip_z + 0.02 * k), "bottom" if not dress else "top", r2=hipw * 0.95, seg=12)
    a.sphere(hipw * 1.0, (0, 0.01, hip_z - 0.02 * k), "bottom" if not dress else "top", scale=(1, 0.85, 0.7), seg=10)
    a.cyl(hipw * 1.12, 0.035 * k, (0, 0, hip_z + 0.1 * k), "accent", seg=12)                              # belt / waistband
    if garment in ("coat", "frock"):
        hem = 0.52 if garment == "coat" else 0.36
        # coat skirts: front panels and long tails behind
        a.limb((0, hipw * 0.1, hip_z + 0.1 * k), (0, hipw * 0.1, hip_z - hem * k), hipw * 1.18, hipw * 1.4, "top", seg=12)
        a.box((hipw * 1.1, 0.03, hem * 0.95 * k), (-hipw * 0.5, hipw * 1.0, hip_z - hem * 0.42 * k), "top", rot=(0, 0, 0.1))
        a.box((hipw * 1.1, 0.03, hem * 0.95 * k), (hipw * 0.5, hipw * 1.0, hip_z - hem * 0.42 * k), "top", rot=(0, 0, -0.1))
    if dress:
        hem_r = hipw * (2.6 if garment == "gown" else 2.0)
        a.limb((0, 0, hip_z + 0.08 * k), (0, 0, 0.06 * k), hipw * 1.12, hem_r, "top", seg=16)
        a.cyl(hem_r * 1.01, 0.045 * k, (0, 0, 0.07 * k), "accent", seg=16)
        if garment == "gown":
            a.limb((0, hipw * 0.6, hip_z - 0.1 * k), (0, hem_r * 1.5, 0.04 * k), hipw * 0.7, hem_r * 0.85, "top", seg=10)   # train
    if cloak:
        a.box((sw * 2.5, 0.035, 1.25 * k), (0, hipw * 1.35, hip_z - 0.18 * k), "cloak", rot=(0.05, 0, 0))

    # ---------------- torso
    a.part("torso", (0, 0, waist_z), parent="hips")
    chest_r = sw * (0.95 if not fem else 0.85)
    a.limb((0, 0, waist_z - 0.05 * k), (0, -lean, chest_z), hipw * 0.92 if fem else hipw * 0.98, chest_r, "top", seg=12)
    a.limb((0, -lean, chest_z), (0, -lean * 1.4, sh_z), chest_r, sw * 0.9, "top", seg=12)
    a.sphere(sw * 0.95, (0, -lean * 1.4, sh_z - 0.02 * k), "top", scale=(1.05, 0.55, 0.42), seg=12)           # shoulder yoke
    if fem:
        for sx in (-1, 1):
            a.sphere(0.05 * k * b, (sx * 0.065 * b, -0.085 * b - lean, chest_z - 0.025 * k), "top", scale=(1, 0.9, 0.9), seg=8)
    a.cyl(0.05 * k, 0.1 * k, (0, -lean * 1.4, neck_z - 0.02 * k), "skin", r2=0.045 * k, seg=10)               # neck
    if garment in ("coat", "frock"):
        fy = -chest_r * 0.96 - lean
        a.box((0.075 * b, 0.014, 0.22 * k), (0, fy, chest_z + 0.0 * k), "accent")                                # waistcoat / shirt front
        for i in range(3):
            a.sphere(0.011 * k, (0.0, fy - 0.004, chest_z - 0.12 * k + i * 0.07 * k), "accent", seg=6)
        a.box((0.1 * b, 0.05, 0.03 * k), (0, -0.08 * b - lean * 1.3, neck_z - 0.03 * k), "accent")             # collar / cravat
    elif dress:
        pass
    if cloak:
        a.box((sw * 2.7, 0.2 * b, 0.1 * k), (0, 0.03, sh_z - 0.02 * k), "cloak")
        a.box((0.07, 0.04, 0.17 * k), (-sw * 0.78, 0.09 * b, sh_z + 0.07 * k), "cloak", rot=(0.0, -0.2, 0))       # standing collar
        a.box((0.07, 0.04, 0.17 * k), (sw * 0.78, 0.09 * b, sh_z + 0.07 * k), "cloak", rot=(0.0, 0.2, 0))
        a.box((sw * 2.5, 0.04, 0.95 * k), (0, 0.15 * b, chest_z - 0.4 * k), "cloak", rot=(0.12, 0, 0))
        a.box((0.1 * k, 0.03, 0.045 * k), (0, -0.1 * b - lean, sh_z - 0.04 * k), "accent")                     # clasp

    # ---------------- head
    a.part("head", (0, -lean * 1.4, neck_z), parent="torso")
    hz = head_z
    hr = 0.112 * k
    hy = -lean * 1.6
    a.sphere(hr, (0, hy, hz), "skin", scale=(0.88, 1.0, 1.13), seg=14)                                           # skull
    a.sphere(hr * 0.78, (0, hy - 0.03 * k, hz - 0.06 * k), "skin", scale=(0.86, 0.95, 1.0), seg=10)              # jaw / chin
    a.box((0.034 * k, 0.05 * k, 0.07 * k), (0, hy - hr * 0.95, hz - 0.01 * k), "skin", rot=(-0.25, 0, 0))        # nose
    for sx in (-1, 1):
        a.sphere(0.022 * k, (sx * hr * 0.9, hy + 0.01 * k, hz - 0.005 * k), "skin", scale=(0.4, 0.8, 1.2), seg=6)   # ears
        a.sphere(0.0165 * k, (sx * 0.04 * k, hy - hr * 0.83, hz + 0.028 * k), "sclera", scale=(1.0, 0.6, 0.8), seg=6)   # eye whites
        a.sphere(0.0095 * k, (sx * 0.04 * k, hy - hr * 0.9, hz + 0.028 * k), "eyes", seg=6)                      # pupils / irises
        a.box((0.04 * k, 0.012 * k, 0.012 * k), (sx * 0.041 * k, hy - hr * 0.88, hz + 0.052 * k), "hair" if hair != "bald" else "skin", rot=(0, sx * 0.16, 0))  # brows
    a.box((0.06 * k, 0.012 * k, 0.012 * k), (0, hy - hr * 0.88, hz - 0.058 * k), "mouth")
    if fangs:
        for sx in (-1, 1):
            a.limb((sx * 0.018 * k, hy - hr * 0.9, hz - 0.052 * k), (sx * 0.018 * k, hy - hr * 0.92, hz - 0.085 * k), 0.007 * k, 0.0, "sclera", seg=4)
    if hair == "short":
        a.sphere(hr * 1.07, (0, hy + 0.018 * k, hz + 0.028 * k), "hair", scale=(0.9, 1.0, 1.02), seg=12)
        a.box((0.012, 0.03 * k, 0.07 * k), (-hr * 0.9, hy - 0.02 * k, hz - 0.01 * k), "hair")
        a.box((0.012, 0.03 * k, 0.07 * k), (hr * 0.9, hy - 0.02 * k, hz - 0.01 * k), "hair")
    elif hair == "long":
        a.sphere(hr * 1.1, (0, hy + 0.02 * k, hz + 0.025 * k), "hair", scale=(0.92, 1.02, 1.04), seg=12)
        a.limb((0, hy + hr * 0.7, hz + 0.02 * k), (0, hy + hr * 0.85, hz - 0.36 * k), hr * 0.85, hr * 0.55, "hair", seg=8)
        for sx in (-1, 1):
            a.limb((sx * hr * 0.85, hy - 0.01 * k, hz + 0.0), (sx * hr * 0.9, hy + 0.01 * k, hz - 0.2 * k), 0.026 * k, 0.018 * k, "hair", seg=6)
    elif hair == "bun":
        a.sphere(hr * 1.07, (0, hy + 0.018 * k, hz + 0.028 * k), "hair", scale=(0.9, 1.0, 1.02), seg=12)
        a.sphere(0.058 * k, (0, hy + hr * 0.95, hz + 0.075 * k), "hair", seg=8)
    elif hair == "slick":
        a.sphere(hr * 1.06, (0, hy + 0.028 * k, hz + 0.018 * k), "hair", scale=(0.9, 1.03, 0.98), seg=12)
        a.limb((0, hy + hr * 0.8, hz + 0.05 * k), (0, hy + hr * 1.05, hz - 0.1 * k), hr * 0.7, hr * 0.45, "hair", seg=8)
    elif hair == "bald":
        a.sphere(hr * 0.98, (0, hy + 0.03 * k, hz - 0.02 * k), "hair", scale=(0.92, 0.8, 0.5), seg=10)          # fringe only
    if beard in ("moustache", "full", "pointed"):
        for sx in (-1, 1):
            a.limb((sx * 0.006, hy - hr * 0.9, hz - 0.045 * k), (sx * 0.055 * k, hy - hr * 0.8, hz - 0.052 * k), 0.012 * k, 0.006 * k, "hair", seg=6)
    if beard == "full":
        a.sphere(hr * 0.82, (0, hy - 0.045 * k, hz - 0.1 * k), "hair", scale=(0.95, 0.9, 1.1), seg=10)
    elif beard == "pointed":
        a.limb((0, hy - hr * 0.7, hz - 0.1 * k), (0, hy - hr * 0.78, hz - 0.2 * k), 0.04 * k, 0.005 * k, "hair", seg=8)
    if hat != "none":
        _hat(a, hat, hz, k, hr)

    # ---------------- arms
    for sx, side in ((-1, "l"), (1, "r")):
        shx = sx * (sw + 0.015)
        sy = -lean * 1.4
        a.part("arm_up_" + side, (shx, sy, sh_z - 0.03 * k), parent="torso")
        a.sphere(0.052 * k * b, (shx, sy, sh_z - 0.035 * k), "top", seg=8)
        a.limb((shx, sy, sh_z - 0.04 * k), (shx * 1.04, sy, sh_z - 0.30 * k), 0.052 * k * b, 0.044 * k * b, "top", seg=10)
        a.part("arm_low_" + side, (shx * 1.04, sy, sh_z - 0.30 * k), parent="arm_up_" + side)
        a.limb((shx * 1.04, sy, sh_z - 0.30 * k), (shx * 1.06, sy, sh_z - 0.56 * k), 0.043 * k * b, 0.034 * k * b, "top" if not dress else "top", seg=10)
        a.cyl(0.037 * k, 0.03 * k, (shx * 1.06, sy, sh_z - 0.545 * k), "accent", seg=10)                         # cuff
        a.sphere(0.038 * k, (shx * 1.07, sy, sh_z - 0.61 * k), "skin", scale=(0.8, 1.0, 1.25), seg=8)           # hand
        a.box((0.012 * k, 0.03 * k, 0.045 * k), (shx * 1.07 - sx * 0.026 * k, sy - 0.015 * k, sh_z - 0.6 * k), "skin")   # thumb

    # ---------------- legs
    for sx, side in ((-1, "l"), (1, "r")):
        lx = sx * hipw * 0.5
        a.part("leg_up_" + side, (lx, 0, hip_z - 0.03 * k), parent="hips")
        low = "skin" if dress else "bottom"
        a.limb((lx, 0, hip_z - 0.02 * k), (lx, 0, 0.5 * k), 0.085 * k * b, 0.058 * k * b, low, seg=10)
        a.part("leg_low_" + side, (lx, 0, 0.5 * k), parent="leg_up_" + side)
        a.limb((lx, 0, 0.5 * k), (lx, 0, 0.085 * k), 0.057 * k * b, 0.04 * k, low, seg=10)
        # boot / shoe
        a.limb((lx, 0, 0.16 * k), (lx, 0, 0.05 * k), 0.048 * k, 0.05 * k, "shoes", seg=10)
        a.box((0.092 * k, 0.2 * k, 0.07 * k), (lx, -0.045 * k, 0.04 * k), "shoes")
        a.sphere(0.047 * k, (lx, -0.125 * k, 0.045 * k), "shoes", scale=(1, 1.1, 0.75), seg=8)


def b_wolf(a, scale=1.0):
    s = scale
    # body (root) with chest and haunch
    a.part("body", (0, 0, 0.62 * s))
    a.sphere(0.27 * s, (0, -0.28 * s, 0.7 * s), "fur", scale=(0.95, 1.35, 1.0), seg=10)       # chest
    a.sphere(0.25 * s, (0, 0.34 * s, 0.68 * s), "fur", scale=(0.9, 1.3, 0.95), seg=10)        # haunch
    a.limb((0, -0.25 * s, 0.7 * s), (0, 0.4 * s, 0.68 * s), 0.25 * s, 0.22 * s, "fur", seg=10)
    a.sphere(0.2 * s, (0, -0.52 * s, 0.82 * s), "fur", scale=(0.9, 1.1, 1.1), seg=8)          # neck mass / mane
    a.part("tail", (0, 0.62 * s, 0.7 * s), parent="body")
    a.limb((0, 0.62 * s, 0.7 * s), (0, 0.98 * s, 0.52 * s), 0.065 * s, 0.03 * s, "fur", seg=8)
    a.part("head", (0, -0.7 * s, 0.9 * s), parent="body")
    a.sphere(0.16 * s, (0, -0.8 * s, 0.9 * s), "fur", scale=(0.95, 1.05, 0.95), seg=10)
    a.limb((0, -0.85 * s, 0.88 * s), (0, -1.06 * s, 0.85 * s), 0.1 * s, 0.06 * s, "fur", seg=8)  # snout
    a.sphere(0.03 * s, (0, -1.08 * s, 0.86 * s), "dark", seg=6)                                  # nose
    for sx in (-1, 1):
        a.limb((sx * 0.08 * s, -0.78 * s, 1.0 * s), (sx * 0.1 * s, -0.76 * s, 1.14 * s), 0.055 * s, 0.0, "fur", seg=4)   # ears
        a.sphere(0.018 * s, (sx * 0.075 * s, -0.93 * s, 0.93 * s), "eyes", seg=6)
    a.part("jaw", (0, -0.86 * s, 0.82 * s), parent="head")
    a.limb((0, -0.86 * s, 0.82 * s), (0, -1.03 * s, 0.8 * s), 0.07 * s, 0.045 * s, "fur", seg=8)
    legs = {"fl": (-1, -0.36), "fr": (1, -0.36), "bl": (-1, 0.4), "br": (1, 0.4)}
    for nm, (sx, y) in legs.items():
        x = sx * 0.14 * s
        a.part("leg_up_" + nm, (x, y * s, 0.6 * s), parent="body")
        a.limb((x, y * s, 0.6 * s), (x, (y + (0.04 if y > 0 else -0.02)) * s, 0.33 * s), 0.085 * s, 0.05 * s, "fur", seg=8)
        a.part("leg_low_" + nm, (x, (y + (0.04 if y > 0 else -0.02)) * s, 0.33 * s), parent="leg_up_" + nm)
        a.limb((x, (y + (0.04 if y > 0 else -0.02)) * s, 0.33 * s), (x, (y + 0.0) * s, 0.04 * s), 0.045 * s, 0.032 * s, "fur", seg=8)
        a.box((0.06 * s, 0.11 * s, 0.035 * s), (x, (y - 0.03) * s, 0.02 * s), "dark")


def b_bat(a, span=1.0):
    a.part("body", (0, 0, 0))
    a.sphere(0.09, (0, 0, 0), "fur", scale=(0.9, 1.5, 0.95), seg=8)
    a.sphere(0.065, (0, -0.16, 0.025), "fur", seg=8)
    a.limb((0, -0.2, 0.02), (0, -0.26, 0.0), 0.035, 0.02, "fur", seg=6)
    for sx in (-1, 1):
        a.limb((sx * 0.025, -0.19, 0.08), (sx * 0.035, -0.2, 0.17), 0.03, 0.0, "fur", seg=4)
        a.sphere(0.012, (sx * 0.03, -0.215, 0.04), "eyes", seg=5)
    for sx, nm in ((-1, "wing_l"), (1, "wing_r")):
        a.part(nm, (sx * 0.06, 0, 0.03), parent="body")
        a.limb((sx * 0.06, 0, 0.03), (sx * span * 0.26, -0.04, 0.06), 0.022, 0.016, "fur", seg=6)
        a.box((span * 0.24, 0.3, 0.006), (sx * span * 0.17, 0.05, 0.04), "wing", rot=(0, 0, sx * 0.1))
        a.part(nm + "_tip", (sx * span * 0.26, -0.04, 0.06), parent=nm)
        a.limb((sx * span * 0.26, -0.04, 0.06), (sx * span * 0.5, -0.12, 0.05), 0.016, 0.006, "fur", seg=5)
        a.box((span * 0.22, 0.26, 0.005), (sx * span * 0.38, 0.0, 0.05), "wing", rot=(0, 0, -sx * 0.15))
