"""Minimal working example of an act file (copy to act_N.py and expand). Not loaded by the pipeline (name does not match act_<digit>*.py)."""
from dsl import *

ACT = dict(
    id=9, title="Example act",
    start=dict(location="ex_room", protagonist="mina", party=["mina"], items={}, flags=[]),
    exit_to="ex_next_act_first_location",          # location id of the next act's start (or "END" for the last act)
)

LOCATIONS = [dict(id="ex_room", name="A sitting room", desc="Shown once, the first time the player enters.", date="3 August")]

LOC_DATA = {
    "ex_room": dict(
        cells=[2, 2], interior=True, wall="plaster", floor="planks",
        ambient=AMBIENT["candle_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2]),
        walls=dict(north=["wall_window_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
        spawn=[3.0, 2.0], spawns={},
        props=[
            prop("ex_table", "table", "dark", 0, -1.0, name="Table", look="A small table.", radius=0.9),
            prop("ex_letter", "book", "leather", 0, -1.0, y=0.8, name="Letter", look="A letter, unopened.", radius=0.2,
                 take="ex_letter_item", take_text="I took the letter.", give_once=True),
            # a door on the east wall (x = +3.8, centred on the wall piece: z = -2 or +2). rot -90 faces into the room.
            prop("ex_door", "door", "dark", 3.8, 2.0, rot=-90, name="Door", look="The way out.", radius=0.6,
                 go="ex_next_act_first_location", go_cond="has:ex_letter_item", go_fail="I should not leave without the letter."),
        ],
        npcs=[npc("ex_maid", "human_peasant_f", "village_woman", -2, 0, rot=90, name="Maid", look="A maid.", talk="ex_maid_talk")],
        on_enter=[dict(do=[dict(journal="ex_j1")], once=True)],
    ),
}

DIALOGUE = {
    "ex_maid_talk": dict(start="a", nodes={
        "a": dict(speaker="Maid", text="Good morning, miss. Will you want the letter?",
                  choices=[dict(text="Yes, please.", next="b", do=[dict(set="maid_ok")]), dict(text="[Leave]", end=True)]),
        "b": dict(speaker="Maid", text="It is on the table.", end=True),
    }),
}

ITEMS = {"ex_letter_item": dict(name="Letter", asset="book", variant="leather", desc="A letter addressed to me.")}
JOURNAL = {"ex_j1": dict(title="3 August", source="Mina Murray's journal", text="A short diary entry in the voice of the book.")}
