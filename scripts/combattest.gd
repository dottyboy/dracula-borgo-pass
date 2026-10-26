class_name CombatTest
extends RefCounted
## Balance harness: auto-plays encounters many times with fixed loadouts.
##   godot --headless --path . -- --combattest [--runs=200]

const KITS := {
	"alone": {"party": ["harker"], "items": {"crucifix": 1}},
	"alone+": {"party": ["harker"], "items": {"crucifix": 1, "kukri": 1, "brandy": 2, "stake": 1}},
	"trio": {"party": ["harker", "vanhelsing", "seward"], "items": {"crucifix": 1, "host": 3, "chloral": 2, "brandy": 2, "bandage": 2, "stake": 1, "hammer": 1}},
	"full": {"party": ["harker", "mina", "vanhelsing", "seward", "quincey", "arthur"],
			"items": {"crucifix": 1, "host": 6, "chloral": 3, "brandy": 3, "bandage": 3, "stake": 1, "hammer": 1, "bullet": 12, "winchester": 1, "kukri": 1, "sacred_bullet": 3, "garlic_wreath": 2}},
}
const PLAN := {
	"borgo_wolves": ["alone", "alone+", "trio"],
	"renfield_frenzy": ["alone+", "trio", "full"],
	"szgany_cart": ["trio", "full"],
	"carfax_rats": ["trio", "full"],
	"brides_wing": ["alone+", "trio", "full"],
	"lucy_tomb": ["trio", "full"],
	"brides_tombs": ["alone+", "trio", "full"],
	"dracula_chase": ["trio", "full"],
}


static func run(runs: int) -> void:
	print("%-17s %-7s %5s %5s %5s  avgHP%%  rounds" % ["encounter", "kit", "win", "fled", "lose"])
	for eid in PLAN:
		for kit in PLAN[eid]:
			var w := 0
			var f := 0
			var l := 0
			var hp_frac := 0.0
			var rounds := 0
			for r in runs:
				var counts: Dictionary = {}
				for it in KITS[kit].items:
					counts[it] = KITS[kit].items[it]
				var states := {}
				for id in KITS[kit].party:
					states[id] = {"hp": Game.systems.party[id].hp, "nerve": Game.systems.party[id].nerve}
				var c := Combat.new()
				c.setup(Game.systems, KITS[kit].party, states, eid, counts, 1000 + r)
				var guard := 0
				while guard < 300:
					guard += 1
					var st := c.advance()
					if st.state == "over":
						break
					c.auto_act(st.actor)
				match c.result:
					"win": w += 1
					"fled": f += 1
					_: l += 1
				var tot := 0.0
				var mx := 0.0
				for p in c.party:
					tot += p.hp
					mx += p.max_hp
				hp_frac += tot / mx
				rounds += c.round_no
			print("%-17s %-7s %4d%% %4d%% %4d%%   %4d%%   %4.1f" % [eid, kit, 100 * w / runs, 100 * f / runs, 100 * l / runs, 100.0 * hp_frac / runs, float(rounds) / runs])
