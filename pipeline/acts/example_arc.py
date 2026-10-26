"""Minimal working example of a personal arc (copy to arc_<id>.py). Not loaded (name is example_arc)."""
from dsl import *

ARC = dict(
    id="ex_arc", title="The Example Story", member="mina", portrait="mina",
    blurb="One sentence shown on the arc's title card and in the Chronicle.",
    unlock="roster:mina",                        # condition on the MAIN game (roster:id, has:, flag:, journal:, meta:game_complete ...)
    unlock_text="Meet Mina in Act II.",          # shown while locked
    after_credits=False,                         # True: also requires that the main story was finished once (persistent)
    start=dict(location="ex_arc_room", protagonist="mina", party=["mina"], items={}, flags=[]),
    exit_to="ARC_END",
    rewards=[dict(give="ex_arc_reward"), dict(stat=dict(member="mina", hp=2, nerve=3)), dict(set="ex_arc_done_flag")],   # applied to the MAIN game when the arc ends
    rewards_text="+2 HP, +3 Nerve for Mina; a keepsake.",
)

LOCATIONS = [dict(id="ex_arc_room", name="A quiet room", desc="Shown once on first entry.")]
LOC_DATA = {
    "ex_arc_room": dict(
        cells=[2, 2], interior=True, wall="plaster", floor="planks", ambient=AMBIENT["candle_interior"], camera=cam([2, 2]),
        lights=lights_warm([2, 2]), walls=dict(north=["wall_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_4"]),
        spawn=[0, 2.5], spawns={},
        props=[prop("ex_arc_desk", "table", "dark", 0, -1.5, name="Desk", look="A desk.", radius=0.9,
                    talk="ex_arc_finish")],
    ),
}
DIALOGUE = {"ex_arc_finish": dict(start="a", nodes={"a": dict(speaker="Mina", text="That is all, for now.",
            choices=[dict(text="[Finish this story]", do=[dict(journal="ex_arc_j"), dict(arc_end=1)]), dict(text="[Not yet]", end=True)])})}
ITEMS = {"ex_arc_reward": dict(name="Keepsake", asset="book", variant="leather", desc="A small keepsake from a story long ago.")}
JOURNAL = {"ex_arc_j": dict(title="A quiet room", source="Mina's recollection", text="A short entry that is merged into the main journal when the arc ends.")}
