#!/usr/bin/env python3
"""Source of truth for game systems: vampire rules, party, weapons, combat items, enemies, encounters, recipes.
Writes data/systems.json (read by scripts/combat.gd, crafting, party UI).

Every rule/enemy/recipe carries `book` (what in the novel it comes from: chapter hint / quote summary, see
book/book_db.json) or `extra: true` where we added thematic material the book does not spell out.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- rules ----
RULES = {
    # how strong vampires are by time of day (book: powerless by day, noon-to-sunset is the time to strike,
    # sunset frees the Count, dawn/cock-crow ends the night)
    "time_power": {"day": 0.35, "dusk": 0.8, "night": 1.0, "dawn": 0.6},
    # man-made weapons do little to a vampire unless holy/fire/stake (Harker's belief; sacred bullet, wafer, fire in the book)
    "mundane_factor": 0.5,
    "repel": {"crucifix": 3, "host": 4, "garlic": 3, "wild_rose": 3},   # turns a vampire is held back
    "kill": ["stake", "beheading"],       # book: stake + head cut off (+ garlic in mouth)
    "box_helpless_by_day": True,           # helpless in the box between sunrise and sunset
    "needs_invitation": True,              # puzzle rule: first entry needs invitation of free will
    "running_water": "cannot cross unaided except at slack or full tide (puzzle/timing rule)",
    "forms": ["wolf", "bat", "mist"],      # transformation, only at the right hours
    "nerve_zero_frozen_turns": 2,
    "list": [
        dict(id="crucifix", text="A crucifix halts a vampire's attack.", book="ch.1-4,15-16,19 crucifix repels"),
        dict(id="garlic", text="Garlic repels the Un-Dead; garlic in the mouth when staked.", book="ch.10,16,18 garlic flowers"),
        dict(id="host", text="The Sacred Wafer (Host) holds a vampire back and sterilises its earth.", book="ch.18-23 Van Helsing's wafer"),
        dict(id="wild_rose", text="Wild rose on a coffin keeps the Un-Dead from leaving it.", book="ch.18 wild rose"),
        dict(id="invite", text="A vampire cannot enter a home unless invited, of free will.", book="ch.1-4,12,16"),
        dict(id="daylight", text="Powers wane by day; helpless in the box between sunrise and sunset.", book="ch.18,23,25"),
        dict(id="water", text="Cannot cross running water unaided except at slack or full tide.", book="ch.24-25"),
        dict(id="no_reflection", text="Casts no reflection (mirror, shaving glass).", book="ch.2"),
        dict(id="earth", text="Must rest in boxes of his native earth; needs the earth to be unsterilised.", book="ch.3,18,22-23"),
        dict(id="stake", text="Staking through the heart and beheading destroys a vampire.", book="ch.16,18"),
        dict(id="command", text="Commands wolves, rats, bats and moths; mist form.", book="ch.1,3,7-8,21"),
        dict(id="strength", text="Strength of many men; hypnotic gaze; blood-bond with victims.", book="ch.2-3,21,23"),
        dict(id="bullet", text="Sacred bullet and kukri/bowie blade can wound him (final chase).", book="ch.27"),
    ],
}

# ---------------------------------------------------------------- weapons ----
WEAPONS = {
    "fists": dict(name="Fists", dmg=[1, 2], acc=0, ranged=False, users=["any"]),
    "pocket_knife": dict(name="Pocket knife", dmg=[2, 4], acc=5, users=["any"]),
    "kukri": dict(name="Kukri", dmg=[5, 7], acc=5, users=["harker"], uses_item="kukri", book="Harker's kukri, ch.27"),
    "bowie": dict(name="Bowie knife", dmg=[4, 6], acc=8, users=["quincey"], book="Quincey's bowie knife, ch.27"),
    "winchester": dict(name="Winchester rifle", dmg=[6, 9], acc=5, ranged=True, ammo="bullet", uses_item="winchester", users=["quincey", "arthur", "seward", "harker"],
                       book="Winchester, ch.27"),
    "revolver": dict(name="Revolver", dmg=[4, 6], acc=0, ranged=True, ammo="bullet", users=["seward", "quincey", "arthur", "harker"]),
    "talon": dict(name="Bare hands (inhuman strength)", dmg=[6, 10], acc=5, users=["dracula"], extra=True),
    "club": dict(name="Hammer", dmg=[2, 4], acc=0, users=["any"]),
    "torch": dict(name="Torch", dmg=[3, 5], acc=0, fire=True, users=["any"], extra=True, uses_item="torch", consume=True,
                  book="Fire and wood as defence, ch.18"),
    "holy_knife": dict(name="Consecrated knife", dmg=[4, 6], acc=8, holy=True, users=["any"], extra=True, uses_item="holy_knife"),
}

# ---------------------------------------------------------------- consumables / combat items ----
ITEMS = {
    "crucifix": dict(name="Crucifix", kind="ward", ward="crucifix", reusable=True),
    "host": dict(name="Sacred Wafer", kind="ward", ward="host", book="Van Helsing, ch.18-23"),
    "garlic_wreath": dict(name="Garlic wreath", kind="ward", ward="garlic", crafted=True),
    "wild_rose": dict(name="Wild rose sprig", kind="ward", ward="wild_rose"),
    "garlic": dict(name="Garlic flowers", kind="ingredient"),
    "brandy": dict(name="Brandy", kind="heal", hp=6, nerve=4, book="brandy revives, throughout"),
    "bandage": dict(name="Bandage", kind="heal", hp=8, nerve=0),
    "chloral": dict(name="Chloral draught", kind="sedative", turns=3, book="Seward's chloral/morphia, ch.10-12"),
    "holy_water": dict(name="Holy water", kind="holy_water", extra=True),
    "stake": dict(name="Stake", kind="finisher", book="ch.16"),
    "hammer": dict(name="Hammer", kind="tool"),
    "bullet": dict(name="Bullets", kind="ammo"),
    "sacred_bullet": dict(name="Sacred bullet", kind="ammo", holy=True, book="Van Helsing's sacred bullet, ch.18"),
    "torch": dict(name="Torch", kind="weapon_item", extra=True),
    "holy_knife": dict(name="Consecrated knife", kind="weapon_item", extra=True),
    "kukri": dict(name="Kukri", kind="weapon_item"), "winchester": dict(name="Winchester rifle", kind="weapon_item"),
    "cloth": dict(name="Cloth", kind="ingredient"), "rope": dict(name="Rope", kind="ingredient"),
    "wood": dict(name="Ash wood", kind="ingredient"), "oil": dict(name="Lamp oil", kind="ingredient"),
    "water": dict(name="Water", kind="ingredient"), "knife": dict(name="Knife", kind="ingredient"),
    "silver": dict(name="Silver coin", kind="ingredient"),
}

# ---------------------------------------------------------------- party ----
PARTY = {
    "harker": dict(model="human_harker", variant="harker", name="Jonathan Harker", portrait="harker", hp=27, nerve=20, spd=5, acc=72, eva=8, faith=2, weapon="pocket_knife",
                   skills=["insight", "brace"], blurb="Solicitor. Notes everything in shorthand; survived the castle."),
    "mina": dict(model="human_mina", variant="mina", name="Mina Harker", portrait="mina", hp=18, nerve=28, spd=6, acc=65, eva=10, faith=5, weapon="fists",
                 skills=["steady", "insight"], blurb="Schoolmistress. Typewriter, timetables, and the bond that sees through the Count's eyes."),
    "vanhelsing": dict(model="human_vanhelsing", variant="vh", name="Prof. Van Helsing", portrait="vanhelsing", hp=22, nerve=32, spd=4, acc=70, eva=6, faith=9, weapon="club",
                       skills=["holy_circle", "insight", "brace"], blurb="Doctor, lawyer, metaphysician. Knows the rites."),
    "seward": dict(model="human_seward", variant="doctor", name="Dr. John Seward", portrait="seward", hp=24, nerve=22, spd=5, acc=70, eva=6, faith=4, weapon="revolver",
                   skills=["sedate", "transfuse"], blurb="Asylum physician; chloral, morphia and the transfusion needle."),
    "quincey": dict(model="human_quincey", variant="texan", name="Quincey Morris", portrait="quincey", hp=30, nerve=24, spd=7, acc=80, eva=10, faith=3, weapon="bowie",
                    skills=["steady_shot", "brace"], blurb="Texan. Winchester and bowie knife."),
    "arthur": dict(model="human_arthur", variant="lord", name="Arthur Holmwood", portrait="arthur", hp=30, nerve=22, spd=5, acc=72, eva=7, faith=4, weapon="club",
                   skills=["rally", "stake_strike"], blurb="Lord Godalming. Drove the stake home for Lucy."),
}

PARTY.update({
    "lucy": dict(model="human_lucy", variant="lucy", name="Lucy Westenra", portrait="lucy", hp=16, nerve=22, spd=6, acc=62, eva=12, faith=5, weapon="fists",
                 skills=["steady", "brace"], playable_only=True, blurb="A bright girl with three suitors and a sleeping habit."),
    "renfield": dict(model="human_renfield", variant="asylum", name="R. M. Renfield", portrait="renfield", hp=24, nerve=14, spd=6, acc=66, eva=10, faith=0,
                     weapon="fists", skills=["brace"], playable_only=True, blurb="Zoophagous patient. Sees much that others do not."),
    "dracula": dict(model="human_dracula", variant="young", name="The Voivode", portrait="dracula_young", hp=60, nerve=40, spd=8, acc=85, eva=15, faith=0,
                    weapon="talon", skills=["brace", "insight"], playable_only=True, blurb="Before the legend: a prince of the Carpathians."),
    "captain": dict(model="human_captain", variant="captain", name="Captain of the Demeter", portrait="captain", hp=28, nerve=24, spd=5, acc=70, eva=8, faith=3,
                    weapon="club", skills=["brace", "steady"], playable_only=True, blurb="A Russian master who lashed himself to the wheel."),
})

SKILLS = {
    "insight": dict(name="Insight", target="none", text="Study the enemy: party hits more often for 3 turns, weaknesses shown.", turns=3),
    "brace": dict(name="Brace", target="none", text="Take a defensive stance and steady your nerve (+4).", nerve=4),
    "steady": dict(name="Steady", target="ally", text="Restore an ally's nerve (+10).", nerve=10),
    "holy_circle": dict(name="Holy circle", target="none", text="Ring of Host crumbs: vampire blows are blunted by 70% and their gaze fails for 3 turns. Costs 1 Host.",
                        cost={"host": 1}, turns=3),
    "sedate": dict(name="Sedate", target="enemy", text="Chloral: a living enemy falls asleep for 3 turns. Costs 1 chloral.", cost={"chloral": 1}),
    "transfuse": dict(name="Transfuse", target="ally", text="Give blood: ally +12 HP, you lose 4 HP.", hp=12, self_hp=4),
    "steady_shot": dict(name="Steady shot", target="enemy", text="Aimed rifle shot, +25% accuracy, double damage. Needs a ranged weapon & ammo.", ranged_only=True),
    "rally": dict(name="Rally", target="none", text="All allies +3 nerve and +10% accuracy for 3 turns.", nerve=3, turns=3),
    "stake_strike": dict(name="Stake & hammer", target="enemy", text="Drive the stake: destroys an undead below 35% HP, or one that is helpless.",
                         needs=["stake", "hammer"]),
}

# ---------------------------------------------------------------- enemies ----
ENEMIES = {
    "wolf": dict(name="Wolf", model="wolf", hp=9, spd=6, dmg=[3, 5], acc=68, eva=12, tags=["beast"], flee_at=0.4, nerve_hit=1,
                 book="Wolves of the Borgo pass, ch.1,3,27"),
    "wolf_alpha": dict(name="Great wolf", model="wolf_big", hp=18, spd=6, dmg=[4, 7], acc=72, eva=10, tags=["beast"], flee_at=0.25, nerve_hit=2),
    "rat": dict(name="Rat", model="bat", hp=3, spd=7, dmg=[1, 2], acc=65, eva=15, tags=["beast", "swarm"], flee_at=0.0, nerve_hit=1,
                book="Rats of Carfax, ch.18-19"),
    "bat": dict(name="Bat", model="bat", hp=5, spd=8, dmg=[1, 3], acc=62, eva=35, tags=["beast"], flee_at=0.5, nerve_hit=2,
                book="Bat at the window, ch.8,21"),
    "szgany": dict(name="Szgany rider", model="human_peasant_m", hp=16, spd=6, dmg=[3, 6], acc=70, eva=8, tags=["human"], flee_at=0.3,
                   book="Szgany escort of the box, ch.27"),
    "carrier": dict(name="Slovak carrier", model="human_peasant_m", hp=14, spd=4, dmg=[2, 4], acc=62, eva=5, tags=["human"], flee_at=0.5,
                    book="Slovaks carrying the boxes, ch.4,26"),
    "bride": dict(name="Weird sister", model="human_bride", hp=28, spd=6, dmg=[4, 6], acc=75, eva=12, tags=["vampire", "undead"], nerve_hit=3,
                  abilities=["charm", "bite"], book="The three women, ch.3,27"),
    "lucy": dict(name="Lucy (the Bloofer Lady)", model="human_lucy", hp=46, spd=6, dmg=[5, 7], acc=76, eva=12, tags=["vampire", "undead"],
                 nerve_hit=3, abilities=["charm", "bite"], book="Lucy in the tomb, ch.16"),
    "renfield": dict(name="Renfield (frenzied)", model="human_renfield", hp=22, spd=6, dmg=[4, 7], acc=70, eva=10, tags=["human", "mad"],
                     subdue=True, book="Renfield's strength, ch.21"),
    "dracula": dict(name="Count Dracula", model="human_dracula", hp=170, spd=7, dmg=[7, 11], acc=82, eva=15, tags=["vampire", "undead", "boss"],
                    nerve_hit=4, abilities=["charm", "bite", "wolves", "mist"], retreat_at=0.3, book="Dracula; ch.3,21,23,27"),
}

ENCOUNTERS = {
    "borgo_wolves": dict(name="Wolves at the pass", time="night", enemies=["wolf", "wolf"], flee_ok=True, loot={"cloth": 1},
                         intro="The howling is close. Yellow eyes in the dark.", win="The wolves slink back into the trees.", location="borgo_pass"),
    "szgany_cart": dict(name="The Szgany cart", time="dusk", enemies=["szgany", "szgany", "carrier"], flee_ok=True, loot={"bullet": 4},
                        intro="The Szgany close round the leiter-wagon with the box.", win="The Szgany scatter.", location=""),
    "brides_wing": dict(name="The three sisters", time="night", enemies=["bride", "bride", "bride"], flee_ok=False, survive=6,
                        intro="'He is young and strong; there are kisses for us all.'", win="They fall back, hissing, into the shadows.",
                        dawn_text="A cock crows somewhere far off. The three shapes thin and vanish.", location="old_wing"),
    "brides_tombs": dict(name="The sisters' tombs", time="day", enemies=["bride", "bride", "bride"], flee_ok=True, in_boxes=True,
                         intro="By day they lie in their tombs, lovely and still. Now is the time.", win="The three sisters are at peace.", location=""),
    "lucy_tomb": dict(name="Lucy in the tomb", time="dusk", enemies=["lucy"], flee_ok=False, loot={"holy_water": 1},
                      intro="She comes toward us with a wanton smile.", win="At last the poor soul is at rest.", location=""),
    "carfax_rats": dict(name="Rats of Carfax", time="dusk", enemies=["rat", "rat", "rat", "rat", "rat"], flee_ok=True,
                        intro="Thousands of rats, with eyes like coals.", win="The rats scatter before the lamps.", location=""),
    "renfield_frenzy": dict(name="Renfield", time="night", enemies=["renfield"], flee_ok=True,
                            intro="He springs, with the strength of a madman.", win="He lies quiet at last.", location=""),
    "dracula_chase": dict(name="The Count at sunset", time="dusk", enemies=["dracula", "szgany", "szgany"], flee_ok=False,
                          intro="The sun is nearly down. The lid of the box is lifted.", win="The Count crumbles to dust.", location=""),
}

# ---------------------------------------------------------------- crafting ----
# Ingredients are world items; recipes unlock via flags (reading, teachers). `crafter` skills give bonuses.
RECIPES = {
    "garlic_wreath": dict(name="Garlic wreath", needs={"garlic": 2, "rope": 1}, makes={"garlic_wreath": 1}, unlock="",
                          text="Garlic flowers bound in a ring: a ward for a room, a window, or a throat.", book="Van Helsing's garlic wreaths, ch.10"),
    "torch": dict(name="Torch", needs={"wood": 1, "cloth": 1, "oil": 1}, makes={"torch": 1}, unlock="", extra=True,
                  text="A brand for the dark and for fire, which the Un-Dead fear.", book="fire and wood, ch.18"),
    "stake": dict(name="Sharpened stake", needs={"wood": 1}, tools=["knife"], makes={"stake": 1}, unlock="", text="Ash wood, a good point.", book="ch.16"),
    "holy_water": dict(name="Holy water", needs={"water": 1, "host": 1}, makes={"holy_water": 1}, unlock="flag:rites", extra=True,
                       text="A crumb of the Host in clean water. Van Helsing will have it blessed."),
    "sacred_bullet": dict(name="Sacred bullets", needs={"bullet": 2, "host": 1}, makes={"sacred_bullet": 2}, unlock="flag:rites",
                          text="Bullets touched with the Host.", book="Van Helsing's sacred bullet, ch.18", crafter_bonus={"quincey": 1}),
    "holy_knife": dict(name="Consecrated knife", needs={"knife": 1, "host": 1}, makes={"holy_knife": 1}, unlock="flag:rites", extra=True,
                       text="A blade the Un-Dead cannot shrug off."),
    "chloral": dict(name="Chloral draught", needs={"water": 1}, makes={"chloral": 1}, unlock="flag:medicine", extra=True,
                    text="Seward measures chloral into a glass.", book="chloral, ch.10-12", crafter_bonus={"seward": 1}),
    "wild_rose_wreath": dict(name="Wild-rose wreath", needs={"wild_rose": 2, "rope": 1}, makes={"wild_rose": 2}, unlock="flag:rites", extra=True,
                             text="Wild rose, woven for a lid.", book="wild rose on the box, ch.18"),
}

# ---------------------------------------------------------------- levels & equipment
LEVELS = dict(xp=[0, 30, 80, 150, 240, 350, 480, 630, 800, 1000], max=10,
              growth="per level above 1: hp +3, nerve +2, acc +1 every 2nd, eva +1 every 3rd, faith +1 every 4th, dmg +1 every 4th")
# slot: armor (flat damage reduction + extras) | charm (stat bonuses) | weapon (key into WEAPONS)
EQUIP = {
    "tweed_travelling_coat": dict(slot="armor", armor=1, name="Tweed travelling coat", desc="Good English wool; it turns a glancing blow."),
    "buffalo_coat": dict(slot="armor", armor=2, name="Buffalo coat", desc="Prairie leather, thick as a door."),
    "captains_oilskin": dict(slot="armor", armor=2, nerve=1, name="Captain's oilskin", desc="Stiff with salt; it has seen the Bay of Biscay."),
    "doctors_greatcoat": dict(slot="armor", armor=1, hp=2, name="Doctor's greatcoat", desc="Pockets for everything a physician needs."),
    "lords_riding_coat": dict(slot="armor", armor=2, name="Lord's riding coat", desc="Cut by a good tailor, lined against the cold."),
    "black_frock_coat": dict(slot="armor", armor=1, faith=1, name="Black frock coat", desc="A scholar's coat, much-washed, much-worn."),
    "travel_shawl": dict(slot="armor", armor=1, nerve=2, name="Travelling shawl", desc="Warm and pinned with care."),
    "sword_cane": dict(slot="weapon", weapon="sword_cane", name="Sword-cane", desc="An elegant stick with eighteen inches of steel inside."),
    "kukri": dict(slot="weapon", weapon="kukri", name="Kukri", desc="A heavy curved knife from the East."),
    "winchester": dict(slot="weapon", weapon="winchester", name="Winchester rifle", desc="Lever action, sixteen shots, American."),
    "torch": dict(slot="weapon", weapon="torch", name="Torch", desc="Fire, which the Un-Dead fear."),
    "holy_knife": dict(slot="weapon", weapon="holy_knife", name="Consecrated knife", desc="Blessed steel."),
    "crucifix": dict(slot="charm", faith=2, nerve=2, name="Crucifix", desc="A simple cross to hold on to."),
    "garlic_wreath": dict(slot="charm", eva=1, nerve=1, name="Garlic wreath", desc="Worn about the neck: pungent and comforting."),
    "arthur_burden_signet": dict(slot="charm", nerve=2, hp=2, name="Godalming's signet", desc="The weight of a name."),
    "demeter_voyage_keepsake": dict(slot="charm", faith=2, nerve=2, name="Captain's crucifix and rosary", desc="Bound in a dead man's hands."),
    "dracula_voivode_signet": dict(slot="charm", dmg=1, nerve=1, name="Voivode's dragon signet", desc="Old, cold, heavy."),
    "dracula_voivode_medal": dict(slot="charm", acc=2, nerve=1, name="Order of the Dragon medal", desc="A dragon coiled upon itself."),
    "dracula_voivode_charm": dict(slot="charm", eva=2, hp=2, name="Wolf-tooth charm", desc="Wolves do not like it."),
    "harker_road_sealed_journal": dict(slot="charm", nerve=2, acc=1, name="Sealed journal", desc="Jonathan's shorthand, under Sister Agatha's seal."),
    "lucy_summer_pressed_letter": dict(slot="charm", nerve=3, name="Pressed-flower letter", desc="Lucy's last gift."),
    "mina_records_keepsake": dict(slot="charm", nerve=2, faith=1, name="Typewriter ribbon & notebook", desc="Mina's patient work."),
    "renfield_mercy_keepsake": dict(slot="charm", nerve=3, name="Notebook of lives", desc="Renfield's tallies, forgiven."),
    "seward_asylum_cylinder": dict(slot="charm", nerve=2, hp=1, name="Phonograph cylinder", desc="A doctor's own voice, steady."),
    "vanhelsing_lore_bag": dict(slot="charm", faith=2, hp=1, name="Professor's black bag", desc="Wafers, wire and wisdom."),
    "quincey_hunt_sheath": dict(slot="charm", acc=2, dmg=1, name="Bowie sheath", desc="Santa Fe's saddle leather."),
}
for _k, _v in EQUIP.items():
    if _k not in ITEMS:
        ITEMS[_k] = dict(name=_v["name"], kind="equip")
WEAPONS["sword_cane"] = dict(name="Sword-cane", dmg=[5, 7], acc=6, users=["arthur", "quincey", "harker", "seward", "vanhelsing"], uses_item="sword_cane")

SYSTEMS = dict(levels=LEVELS, equip=EQUIP, rules=RULES, weapons=WEAPONS, items=ITEMS, party=PARTY, skills=SKILLS, enemies=ENEMIES,
               encounters=ENCOUNTERS, recipes=RECIPES, start_party=["harker"])

def merge_extras(systems):
    """Acts may add enemies, encounters and recipes (bible_src.merge_acts exposes them)."""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import bible_src
    b = bible_src.BIBLE
    for k, dst in (("enemies_extra", "enemies"), ("encounters_extra", "encounters"), ("recipes_extra", "recipes")):
        for kk, vv in b.get(k, {}).items():
            assert kk not in systems[dst], f"duplicate {dst} id {kk}"
            systems[dst][kk] = vv
    return systems


merge_extras(SYSTEMS)

if __name__ == "__main__":
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "systems.json").write_text(json.dumps(SYSTEMS, indent=1, ensure_ascii=False))
    print(f"systems.json: {len(PARTY)} party, {len(ENEMIES)} enemies, {len(ENCOUNTERS)} encounters, "
          f"{len(RECIPES)} recipes, {len(SKILLS)} skills, {len(WEAPONS)} weapons")
