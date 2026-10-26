class_name Combat
extends RefCounted
## Turn-based party combat (Might & Magic style rounds). Pure logic, no scene
## dependencies, so it can be tested headless. Rules come from data/systems.json
## (rules, weapons, items, skills, enemies); the book-derived vampire rules are:
## crucifix/Host/garlic/wild rose repel, mundane weapons halve damage, power by
## time of day, stake + beheading finish, helpless in the box by day.
##
## Flow: setup() -> loop { r = advance(); if r.state == "over": break;
##       act(r.actor, {type, target, item/skill}) }  (enemy turns run inside advance()).

var sys: Dictionary
var counts: Dictionary          # shared inventory counts (Game.counts)
var rng := RandomNumberGenerator.new()
var party: Array = []           # combatant dicts
var enemies: Array = []
var time := "night"
var enc: Dictionary = {}
var order: Array = []
var idx := -1
var round_no := 0
var log: Array = []
var buffs := {"insight": 0, "rally": 0, "circle": 0, "circle_cd": 0}
var result := ""                # "", "win", "lose", "fled"
var flee_ok := true
var events: Array = []         # animation cues for the UI: {t: hit|miss|die|flee|cast, from: id, to: id}


func setup(systems: Dictionary, party_ids: Array, states: Dictionary, encounter_id: String, inv_counts: Dictionary, seed_value: int) -> void:
	sys = systems
	counts = inv_counts
	rng.seed = seed_value
	enc = sys.encounters[encounter_id]
	time = enc.time
	flee_ok = enc.get("flee_ok", true)
	for id in party_ids:
		var m: Dictionary = sys.party[id]
		var st: Dictionary = states[id]
		var bn: Dictionary = st.get("bonus", {})
		var eff: Dictionary = st.get("eff", {})
		if eff.is_empty():
			eff = {"max_hp": int(m.hp) + int(bn.get("hp", 0)), "max_nerve": int(m.nerve) + int(bn.get("nerve", 0)), "acc": int(m.acc) + int(bn.get("acc", 0)),
				"eva": int(m.eva) + int(bn.get("eva", 0)), "faith": int(m.faith) + int(bn.get("faith", 0)), "dmg": int(bn.get("dmg", 0)), "armor": 0, "weapon": ""}
		party.append({"id": id, "name": m.name, "side": "party", "hp": mini(int(st.hp), int(eff.max_hp)), "max_hp": eff.max_hp, "nerve": mini(int(st.nerve), int(eff.max_nerve)),
			"max_nerve": eff.max_nerve, "spd": m.spd, "acc": eff.acc, "eva": eff.eva, "faith": eff.faith, "dmg_bonus": eff.dmg, "armor": eff.armor,
			"equip_weapon": eff.weapon, "skills": m.skills, "tags": ["human"], "st": {}, "base_weapon": m.weapon, "portrait": m.portrait})
	var n := 0
	var hp_scale := 1.0 + 0.22 * float(party_ids.size() - 1)
	for eid in enc.enemies:
		var e: Dictionary = sys.enemies[eid]
		n += 1
		var ehp := int(round(float(e.hp) * hp_scale))
		enemies.append({"id": "%s_%d" % [eid, n], "kind": eid, "name": e.name, "side": "enemy", "hp": ehp, "max_hp": ehp, "nerve": 99, "max_nerve": 99,
			"spd": e.spd, "acc": e.acc, "eva": e.eva, "dmg": e.dmg, "tags": e.tags, "abilities": e.get("abilities", []), "st": {},
			"flee_at": e.get("flee_at", 0.0), "nerve_hit": e.get("nerve_hit", 0), "model": e.model, "retreat_at": e.get("retreat_at", 0.0),
			"subdue": e.get("subdue", false), "faith": 0,
			"xp": int(e.get("xp", int(float(e.hp) / 2.0 + float(e.dmg[1]) * 1.5)))})
	if enc.get("in_boxes", false):
		for e in enemies:
			if e.tags.has("vampire"):
				e.st["box"] = 99
	_say(str(enc.intro))
	_new_round()


func _say(t: String) -> void:
	log.append(t)


## XP for the whole party: defeated/subdued/helpless enemies count fully, fled ones half.
func xp_reward() -> int:
	var total := 0.0
	for e in enemies:
		if e.hp <= 0 or e.st.has("subdued") or e.st.has("helpless") or e.st.has("destroyed"):
			total += float(e.get("xp", 5))
		elif e.st.has("fled"):
			total += float(e.get("xp", 5)) * 0.5
	return int(total)


func take_events() -> Array:
	var e := events
	events = []
	return e


func _ev(t: String, from_c: Dictionary, to_c: Dictionary = {}) -> void:
	events.append({"t": t, "from": from_c.get("id", ""), "to": to_c.get("id", "")})


func take_log() -> Array:
	var l := log
	log = []
	return l


func alive(side: Array) -> Array:
	return side.filter(func(c: Dictionary) -> bool: return c.hp > 0 and not c.st.has("fled"))


func _new_round() -> void:
	round_no += 1
	order = alive(party) + alive(enemies)
	for c in order:
		c["init"] = float(c.spd) + rng.randf() * 3.0
	order.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return a.init > b.init)
	idx = -1
	for k in buffs:
		buffs[k] = maxi(0, buffs[k] - 1) if round_no > 1 else buffs[k]


func _over() -> bool:
	if enc.has("survive") and round_no > int(enc.survive) and not alive(party).is_empty():
		result = "win"
		_say(str(enc.get("dawn_text", "Dawn breaks and the night's power ends.")))
		return true
	if round_no > 80:
		result = "lose"
		return true
	var left := alive(enemies).filter(func(e: Dictionary) -> bool: return not e.st.has("subdued") and not e.st.has("helpless"))
	left = left.filter(func(e: Dictionary) -> bool: return true)
	if left.is_empty():
		result = "win"
		_say(str(enc.win))
		if not alive(enemies).filter(func(e: Dictionary) -> bool: return e.st.has("helpless")).is_empty():
			_say("But the Un-Dead is not destroyed - without the stake it will rise again.")
		return true
	if alive(party).is_empty():
		result = "lose"
		_say("The party is overcome.")
		return true
	return false


## Runs enemy turns; returns {"state":"input","actor":..} or {"state":"over","result":..}.
func advance() -> Dictionary:
	var guard := 0
	while guard < 500:
		guard += 1
		if result != "" or _over():
			return {"state": "over", "result": result}
		idx += 1
		if idx >= order.size():
			_new_round()
			continue
		var a: Dictionary = order[idx]
		if a.hp <= 0 or a.st.has("fled") or a.st.has("subdued") or a.st.has("helpless") or a.st.has("box"):
			continue
		if _tick(a):
			continue
		if a.side == "enemy":
			_enemy_turn(a)
		else:
			return {"state": "input", "actor": a}
	return {"state": "over", "result": "lose"}


## Start-of-turn status handling. Returns true if the actor loses the turn.
func _tick(a: Dictionary) -> bool:
	a.erase("defending")
	var skip := false
	for k in a.st.keys():
		if k in ["fled", "subdued", "helpless", "destroyed", "box"]:
			continue
		a.st[k] -= 1
		if a.st[k] < 0:
			a.st.erase(k)
			continue
		if k == "helpless" or k == "box":
			skip = true
		if k == "asleep" or k == "frozen" or k == "charmed":
			skip = true
			_say("%s is %s." % [a.name, {"asleep": "asleep", "frozen": "frozen with terror", "charmed": "held in the Count's gaze"}[k]])
	return skip


# ------------------------------------------------------------------ helpers
func _is_vamp(c: Dictionary) -> bool:
	return c.tags.has("vampire")


func power(c: Dictionary) -> float:
	return float(sys.rules.time_power[time]) if _is_vamp(c) else 1.0


func weapon_for(a: Dictionary, prefer_vs: Dictionary = {}) -> Dictionary:
	var ew: String = str(a.get("equip_weapon", ""))
	if ew != "" and sys.weapons.has(ew):
		var w0: Dictionary = sys.weapons[ew]
		var ok_w := true
		if w0.has("uses_item") and int(counts.get(w0.uses_item, 0)) <= 0:
			ok_w = false
		if w0.has("ammo") and _ammo(w0) == "":
			ok_w = false
		if ok_w:
			var out0: Dictionary = w0.duplicate()
			out0["key"] = ew
			return out0
	var best_key: String = a.base_weapon
	var best_score := -1.0
	for wid in sys.weapons:
		var w: Dictionary = sys.weapons[wid]
		var users: Array = w.get("users", ["any"])
		if not (users.has("any") or users.has(a.id)):
			continue
		if wid != a.base_weapon:
			if not w.has("uses_item") or int(counts.get(w.uses_item, 0)) <= 0:
				continue
		if w.has("ammo") and _ammo(w) == "":
			continue
		var score := _avg(w) + float(w.get("acc", 0)) * 0.05
		if not prefer_vs.is_empty() and _is_vamp(prefer_vs) and (w.get("holy", false) or w.get("fire", false)):
			score *= 1.6
		if score > best_score:
			best_key = wid
			best_score = score
	var out: Dictionary = sys.weapons[best_key].duplicate()
	out["key"] = best_key
	return out


func _ammo(w: Dictionary) -> String:
	if not w.has("ammo"):
		return "x"
	if int(counts.get("sacred_bullet", 0)) > 0:
		return "sacred_bullet"
	if int(counts.get("bullet", 0)) > 0:
		return "bullet"
	return ""


func _avg(w: Dictionary) -> float:
	return (float(w.dmg[0]) + float(w.dmg[1])) / 2.0


func _roll_hit(att: Dictionary, tgt: Dictionary, bonus: int = 0) -> bool:
	var chance: float = float(att.acc) + bonus - float(tgt.eva)
	if att.side == "party":
		chance += 20.0 if buffs.insight > 0 else 0.0
		chance += 10.0 if buffs.rally > 0 else 0.0
	if att.st.has("repelled"):
		chance -= 100.0
	chance *= power(att)
	if tgt.has("defending"):
		chance -= 10.0
	if tgt.st.has("mist"):
		chance -= 40.0
	return rng.randf() * 100.0 < clampf(chance, 8.0, 95.0)


func _damage(tgt: Dictionary, amount: float, holy: bool = false) -> int:
	var d := amount
	if _is_vamp(tgt) and not holy and time != "day":
		d *= float(sys.rules.mundane_factor)
	if tgt.has("defending"):
		d *= 0.5
	var n := maxi(1, int(round(d)))
	tgt.hp = maxi(0, tgt.hp - n)
	return n


func _hurt_nerve(tgt: Dictionary, n: int) -> void:
	if tgt.side != "party" or n <= 0:
		return
	tgt.nerve = maxi(0, tgt.nerve - n)
	if tgt.nerve == 0 and not tgt.st.has("frozen"):
		tgt.st["frozen"] = int(sys.rules.nerve_zero_frozen_turns)
		_say("%s freezes with terror!" % tgt.name)
		tgt.nerve = int(tgt.max_nerve * 0.3)


# ------------------------------------------------------------------ player actions
func actions_for(a: Dictionary) -> Array:
	var out: Array = []
	var w := weapon_for(a, enemies[0] if enemies.size() > 0 else {})
	out.append({"id": "attack", "label": "Attack (%s)" % w.name, "target": "enemy", "enabled": true})
	for sk in a.skills:
		var s: Dictionary = sys.skills[sk]
		var ok := true
		var why := ""
		for it in s.get("cost", {}):
			if int(counts.get(it, 0)) < int(s.cost[it]):
				ok = false
				why = "needs %s" % it
		for it in s.get("needs", []):
			if int(counts.get(it, 0)) <= 0:
				ok = false
				why = "needs %s" % it
		if s.get("ranged_only", false) and not w.get("ranged", false):
			ok = false
			why = "needs a ranged weapon"
		out.append({"id": "skill:" + sk, "label": s.name, "target": s.target, "enabled": ok, "hint": s.text if ok else why})
	for it in ["crucifix", "host", "garlic_wreath", "wild_rose"]:
		if int(counts.get(it, 0)) > 0:
			out.append({"id": "ward:" + it, "label": "Ward: " + str(sys.items[it].name), "target": "enemy", "enabled": true})
	for it in ["brandy", "bandage"]:
		if int(counts.get(it, 0)) > 0:
			out.append({"id": "heal:" + it, "label": "%s (x%d)" % [sys.items[it].name, counts[it]], "target": "ally", "enabled": true})
	if int(counts.get("chloral", 0)) > 0 and not a.skills.has("sedate"):
		pass
	if int(counts.get("stake", 0)) > 0 and int(counts.get("hammer", 0)) > 0 and enemies.any(func(e: Dictionary) -> bool: return e.hp > 0 and (e.st.has("box") or e.st.has("helpless"))):
		out.append({"id": "finish", "label": "Stake the Un-Dead", "target": "enemy", "enabled": true, "hint": "Only on one that lies helpless"})
	out.append({"id": "defend", "label": "Defend", "target": "none", "enabled": true})
	if flee_ok:
		out.append({"id": "flee", "label": "Flee", "target": "none", "enabled": true})
	return out


func act(a: Dictionary, action: Dictionary) -> void:
	var t: String = action.id
	var tgt: Dictionary = action.get("target", {})
	if t == "attack":
		_attack(a, tgt)
	elif t == "finish":
		if tgt.st.has("box") or tgt.st.has("helpless") or time == "day":
			tgt.hp = 0
			tgt.st["destroyed"] = 1
			_say("%s drives the stake through the heart. %s crumbles to dust." % [a.name, tgt.name])
		else:
			_say("%s cannot reach the heart while %s stands." % [a.name, tgt.name])
	elif t == "defend":
		a["defending"] = true
		a.nerve = mini(a.max_nerve, a.nerve + 2)
		_say("%s takes cover." % a.name)
	elif t == "flee":
		var chance := 0.45 + 0.05 * float(a.spd) - 0.1 * alive(enemies).size()
		if rng.randf() < chance:
			result = "fled"
			_say("The party escapes!")
		else:
			_say("%s cannot get away!" % a.name)
	elif t.begins_with("skill:"):
		_skill(a, t.substr(6), tgt)
	elif t.begins_with("ward:"):
		_ward(a, t.substr(5), tgt)
	elif t.begins_with("heal:"):
		var it: Dictionary = sys.items[t.substr(5)]
		counts[t.substr(5)] = counts[t.substr(5)] - 1
		tgt.hp = mini(tgt.max_hp, tgt.hp + int(it.hp))
		tgt.nerve = mini(tgt.max_nerve, tgt.nerve + int(it.nerve))
		_say("%s uses %s on %s (+%d HP)." % [a.name, it.name, tgt.name, it.hp])


func _attack(a: Dictionary, tgt: Dictionary, mult: float = 1.0, acc_bonus: int = 0) -> void:
	if a.side == "enemy":
		_enemy_strike(a, tgt)
		return
	var w := weapon_for(a, tgt)
	var holy: bool = w.get("holy", false) or w.get("fire", false)
	if w.has("ammo"):
		var am := _ammo(w)
		if am == "":
			w = sys.weapons[a.base_weapon].duplicate()
			w["key"] = a.base_weapon
		else:
			counts[am] -= 1
			if am == "sacred_bullet":
				holy = true
	if w.get("uses_item", "") != "" and w.get("consume", false) and w.key == "torch":
		if rng.randf() < 0.34:
			counts["torch"] = maxi(0, counts.get("torch", 0) - 1)
	if _roll_hit(a, tgt, int(w.get("acc", 0)) + acc_bonus):
		var base := (float(rng.randi_range(int(w.dmg[0]), int(w.dmg[1]))) + float(a.get("dmg_bonus", 0))) * mult
		var n := _damage(tgt, base, holy)
		_say("%s hits %s with %s for %d." % [a.name, tgt.name, w.name, n])
		_ev("hit", a, tgt)
		_after_hit(tgt)
	else:
		_say("%s misses %s." % [a.name, tgt.name])
		_ev("miss", a, tgt)


func _after_hit(tgt: Dictionary) -> void:
	if tgt.hp <= 0:
		if tgt.side == "enemy" and _is_vamp(tgt):
			tgt.hp = 1
			tgt.st["helpless"] = 99
			_say("%s sinks down, but is not yet destroyed - the stake and the knife must finish it." % tgt.name)
		else:
			_say("%s is down." % tgt.name)
		_ev("die", tgt, tgt)
		return
	if tgt.side == "enemy":
		var frac := float(tgt.hp) / float(tgt.max_hp)
		if float(tgt.flee_at) > 0.0 and frac <= float(tgt.flee_at) and not tgt.tags.has("boss"):
			tgt.st["fled"] = 1
			_say("%s flees!" % tgt.name)
			_ev("flee", tgt, tgt)
		elif tgt.subdue and frac <= 0.35:
			tgt.st["subdued"] = 1
			_say("%s collapses, spent and quiet." % tgt.name)
		elif float(tgt.retreat_at) > 0.0 and frac <= float(tgt.retreat_at):
			tgt.st["fled"] = 1
			_say("%s turns to mist and is gone toward his box..." % tgt.name)


func _skill(a: Dictionary, sk: String, tgt: Dictionary) -> void:
	var s: Dictionary = sys.skills[sk]
	_ev("cast", a, tgt)
	for it in s.get("cost", {}):
		counts[it] = counts[it] - int(s.cost[it])
	match sk:
		"insight":
			buffs.insight = int(s.turns) + 1
			_say("%s studies the enemy. The party sees its openings." % a.name)
		"brace":
			a["defending"] = true
			a.nerve = mini(a.max_nerve, a.nerve + int(s.nerve))
			_say("%s braces and steadies." % a.name)
		"steady":
			tgt.nerve = mini(tgt.max_nerve, tgt.nerve + int(s.nerve))
			if tgt.st.has("frozen"):
				tgt.st.erase("frozen")
			_say("%s calms %s." % [a.name, tgt.name])
		"holy_circle":
			buffs.circle = int(s.turns) + 1
			buffs["circle_cd"] = 4
			_say("%s sets a ring of Host crumbs. No vampire may strike across it." % a.name)
		"sedate":
			if tgt.tags.has("vampire"):
				_say("%s: the draught means nothing to the Un-Dead." % a.name)
			else:
				tgt.st["asleep"] = 3
				_say("%s puts %s to sleep." % [a.name, tgt.name])
		"transfuse":
			tgt.hp = mini(tgt.max_hp, tgt.hp + int(s.hp))
			a.hp = maxi(1, a.hp - int(s.self_hp))
			_say("%s gives blood: %s +%d HP." % [a.name, tgt.name, s.hp])
		"steady_shot":
			_attack(a, tgt, 2.0, 25)
		"rally":
			buffs.rally = int(s.turns) + 1
			for p in alive(party):
				p.nerve = mini(p.max_nerve, p.nerve + int(s.nerve))
			_say("%s rallies the party." % a.name)
		"stake_strike":
			if _is_vamp(tgt) and (tgt.st.has("helpless") or tgt.st.has("box") or float(tgt.hp) / float(tgt.max_hp) <= 0.35 or (time == "day")):
				tgt.hp = 0
				tgt.st["destroyed"] = 1
				_say("%s drives the stake home. %s crumbles." % [a.name, tgt.name])
				_check_dead(tgt)
			else:
				_say("%s cannot get a clean strike yet - %s is too strong." % [a.name, tgt.name])


func _check_dead(tgt: Dictionary) -> void:
	tgt.hp = 0


func _ward(a: Dictionary, it: String, tgt: Dictionary) -> void:
	var ward: String = sys.items[it].ward
	if not sys.items[it].get("reusable", false):
		counts[it] -= 1
	if not _is_vamp(tgt):
		_say("%s holds up the %s, but %s is not a creature of the night." % [a.name, sys.items[it].name, tgt.name])
		return
	var chance := 0.5 + 0.05 * float(a.faith) + (0.15 if ward == "host" else 0.0)
	if rng.randf() < chance:
		tgt.st["repelled"] = int(sys.rules.repel[ward]) + 1
		_say("%s shrinks back from the %s!" % [tgt.name, sys.items[it].name])
	else:
		_say("%s's %s does not hold %s this time." % [a.name, sys.items[it].name, tgt.name])


# ------------------------------------------------------------------ enemies
func _enemy_turn(e: Dictionary) -> void:
	var targets := alive(party)
	if targets.is_empty():
		return
	if e.st.has("repelled"):
		_say("%s is held back." % e.name)
		return
	var vamp := _is_vamp(e)
	var abil: Array = e.abilities
	# boss specials
	if abil.has("wolves") and e.kind == "dracula" and alive(enemies).size() < 4 and rng.randf() < 0.18 and time != "day":
		var n := {"id": "wolf_s%d" % round_no, "kind": "wolf", "name": "Wolf", "side": "enemy", "hp": 10, "max_hp": 10, "nerve": 99, "max_nerve": 99,
			"spd": 6, "acc": 68, "eva": 12, "dmg": [3, 5], "tags": ["beast"], "abilities": [], "st": {}, "flee_at": 0.4, "nerve_hit": 1, "model": "wolf",
			"retreat_at": 0.0, "subdue": false, "faith": 0}
		enemies.append(n)
		order.append(n)
		_say("%s calls the wolves out of the night!" % e.name)
		return
	if abil.has("mist") and rng.randf() < 0.15 and time != "day":
		e.st["mist"] = 1
		_say("%s thins to mist." % e.name)
	if abil.has("charm") and rng.randf() < 0.3 * power(e):
		var t: Dictionary = targets[rng.randi() % targets.size()]
		var resist := 0.2 + 0.02 * float(t.nerve) + 0.03 * float(t.faith)
		if buffs.circle > 0:
			_say("%s's gaze breaks on the holy circle." % e.name)
		elif rng.randf() > resist:
			t.st["charmed"] = 2
			_say("%s catches %s's eyes. %s cannot move." % [e.name, t.name, t.name])
			return
		else:
			_say("%s resists %s's gaze." % [t.name, e.name])
	var pick: Dictionary = targets[rng.randi() % targets.size()]
	# prefer charmed/asleep victims for the bite
	for t in targets:
		if t.st.has("charmed") or t.st.has("asleep") or t.st.has("frozen"):
			pick = t
			break
	_enemy_strike(e, pick)


func _enemy_strike(e: Dictionary, tgt: Dictionary) -> void:
	if e.st.has("repelled"):
		return
	var hit := _roll_hit(e, tgt)
	if hit:
		var base := float(rng.randi_range(int(e.dmg[0]), int(e.dmg[1]))) * power(e)
		if _is_vamp(e) and buffs.circle > 0:
			base *= 0.3
			_say("The holy circle blunts %s's blow." % e.name)
		if tgt.has("defending"):
			base *= 0.5
		var n := maxi(1, int(round(base)) - int(tgt.get("armor", 0)))
		tgt.hp = maxi(0, tgt.hp - n)
		var bite := ""
		if e.abilities.has("bite") and (tgt.st.has("charmed") or tgt.st.has("asleep") or tgt.st.has("frozen")):
			bite = " drinking deep"
			e.hp = mini(e.max_hp, e.hp + n)
			tgt["drained"] = true
		_say("%s strikes %s%s for %d." % [e.name, tgt.name, bite, n])
		_ev("hit", e, tgt)
		_hurt_nerve(tgt, int(e.nerve_hit))
		if tgt.hp <= 0:
			_say("%s falls." % tgt.name)
	else:
		_say("%s misses %s." % [e.name, tgt.name])
		_ev("miss", e, tgt)
		_hurt_nerve(tgt, maxi(0, int(e.nerve_hit) - 1))


## Simple automatic policy used by balance tests and as a fallback for AI-controlled allies.
func auto_act(a: Dictionary) -> void:
	var targets := alive(enemies).filter(func(x: Dictionary) -> bool: return not x.st.has("subdued"))
	var foe: Dictionary = targets[0]
	for t in targets:
		if float(t.hp) < float(foe.hp):
			foe = t
	var acts := actions_for(a)
	var has := func(id: String) -> bool:
		for x in acts:
			if x.id == id and x.enabled:
				return true
		return false
	for t in targets:
		if (t.st.has("box") or t.st.has("helpless")) and has.call("finish"):
			act(a, {"id": "finish", "target": t})
			return
	var vamp_present := targets.any(func(x: Dictionary) -> bool: return _is_vamp(x))
	if a.skills.has("stake_strike") and vamp_present and has.call("skill:stake_strike"):
		for t in targets:
			if t.st.has("helpless") or t.st.has("box") or (_is_vamp(t) and float(t.hp) / float(t.max_hp) <= 0.35):
				act(a, {"id": "skill:stake_strike", "target": t})
				return
	if vamp_present and a.skills.has("holy_circle") and buffs.circle == 0 and buffs.circle_cd == 0 and has.call("skill:holy_circle"):
		act(a, {"id": "skill:holy_circle"})
		return
	if vamp_present:
		for t in targets:
			if _is_vamp(t) and not t.st.has("repelled") and has.call("ward:crucifix") and a.faith >= 5:
				act(a, {"id": "ward:crucifix", "target": t})
				return
	for al in alive(party):
		if float(al.hp) / float(al.max_hp) < 0.4:
			if a.skills.has("transfuse") and al != a:
				act(a, {"id": "skill:transfuse", "target": al})
				return
			if has.call("heal:brandy"):
				act(a, {"id": "heal:brandy", "target": al})
				return
	if a.skills.has("steady_shot") and has.call("skill:steady_shot"):
		act(a, {"id": "skill:steady_shot", "target": foe})
		return
	if a.skills.has("sedate") and has.call("skill:sedate") and not _is_vamp(foe) and not foe.st.has("asleep") and targets.size() > 1:
		act(a, {"id": "skill:sedate", "target": foe})
		return
	if a.skills.has("insight") and buffs.insight == 0 and round_no <= 2:
		act(a, {"id": "skill:insight"})
		return
	act(a, {"id": "attack", "target": foe})
