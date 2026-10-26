"""Quincey's arc: a horse model for Santa Fe, the mare."""
# `math` is injected by blender_gen's loader; builders receive the Asset `a` (z up, front -y, origin at base centre).


def b_quincey_hunt_horse(a):
    a.part("horse")
    a.box((0.50, 1.00, 0.55), (0, 0.0, 1.02), "fur")                      # barrel
    a.box((0.46, 0.34, 0.50), (0, -0.55, 1.08), "fur")                    # chest
    a.box((0.48, 0.34, 0.52), (0, 0.55, 1.05), "fur")                     # hindquarters
    for sx in (-1, 1):
        for sy in (-1, 1):
            a.box((0.13, 0.13, 0.78), (sx * 0.17, sy * 0.52, 0.42), "fur")   # legs
            a.box((0.15, 0.15, 0.10), (sx * 0.17, sy * 0.52, 0.05), "dark")  # hooves
    a.beam((0, -0.58, 1.20), (0, -0.86, 1.72), 0.24, "fur")               # neck
    a.beam((0, -0.86, 1.72), (0, -1.12, 1.46), 0.20, "fur")               # head
    a.box((0.14, 0.16, 0.14), (0, -1.16, 1.40), "dark")                   # muzzle
    a.box((0.05, 0.06, 0.14), (-0.07, -0.84, 1.88), "fur")                # ears
    a.box((0.05, 0.06, 0.14), (0.07, -0.84, 1.88), "fur")
    a.beam((0, -0.60, 1.32), (0, -0.88, 1.84), 0.07, "dark")              # mane
    a.beam((0, 0.62, 1.22), (0, 0.78, 0.62), 0.09, "dark")                # tail
    a.box((0.42, 0.46, 0.07), (0, 0.0, 1.33), "leather")                  # saddle
    a.box((0.10, 0.12, 0.12), (0, -0.20, 1.42), "leather")                # pommel
