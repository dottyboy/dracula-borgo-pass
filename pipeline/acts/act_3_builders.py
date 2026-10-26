"""Act III extra models: Seward's phonograph, a long-case clock, the doctor's bag (transfusion kit)."""
# `math` is injected by blender_gen's loader; builders receive the Asset `a` (z up, front -y, origin at base centre).


def b_a3_phonograph(a):
    a.part("phonograph")
    a.box((0.34, 0.30, 0.16), (0, 0, 0.08), "wood")
    a.box((0.30, 0.26, 0.02), (0, 0, 0.17), "iron")
    a.cyl(0.07, 0.03, (0, 0, 0.20), "wax", seg=14)                       # the wax cylinder
    a.beam((0.0, 0.0, 0.22), (0.0, -0.10, 0.36), 0.02, "iron")            # tone arm
    a.cyl(0.03, 0.34, (0.0, 0.17, 0.42), "gold", r2=0.19, seg=14, rot=(-1.1, 0, 0))   # the horn
    a.cyl(0.015, 0.14, (0.12, 0.10, 0.23), "iron", seg=8)                 # crank
    a.box((0.07, 0.015, 0.015), (0.12, 0.10, 0.31), "iron")


def b_a3_clock(a):
    a.part("clock")
    a.box((0.46, 0.30, 0.20), (0, 0, 0.10), "wood")
    a.box((0.34, 0.22, 1.30), (0, 0, 0.85), "wood")
    a.box((0.46, 0.30, 0.22), (0, 0, 1.62), "wood")
    a.cyl(0.14, 0.03, (0, -0.125, 1.62), "gold", seg=16, rot=(1.5708, 0, 0))   # dial
    a.box((0.02, 0.01, 0.10), (0, -0.145, 1.66), "iron")
    a.box((0.08, 0.01, 0.015), (0.03, -0.145, 1.62), "iron")
    a.box((0.20, 0.02, 0.80), (0, -0.115, 0.95), "glass")                   # pendulum case window
    a.cyl(0.05, 0.015, (0, -0.125, 0.70), "gold", seg=12, rot=(1.5708, 0, 0))   # pendulum bob


def b_a3_bag(a):
    a.part("bag")
    a.box((0.46, 0.20, 0.22), (0, 0, 0.11), "leather")
    a.box((0.46, 0.21, 0.06), (0, 0, 0.25), "leather")
    a.box((0.06, 0.215, 0.07), (0, 0, 0.22), "iron")                        # clasp
    a.box((0.28, 0.03, 0.03), (0, 0, 0.31), "leather")                      # handle
    a.box((0.03, 0.03, 0.10), (-0.14, 0, 0.28), "leather")
    a.box((0.03, 0.03, 0.10), (0.14, 0, 0.28), "leather")
