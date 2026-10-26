extends Node
## Global game state: world data, flags, inventory, scripted actions, dialogue.

signal message(text: String)
signal inventory_changed
signal goto_requested(location: String, from: String)
signal dialogue_requested(id: String)
signal ending(text: String)
signal fight_requested(encounter: String, source: String)
signal map_requested
signal pie_requested(eid: String, pos: Vector2, title: String, verbs: Array)
signal pie_chosen(eid: String, verb: String)
signal party_changed
signal state_changed
signal card_requested(text: String, then_goto: String)
signal journal_added(id: String)
signal arc_started(id: String)
signal level_up(id: String, level: int)
signal speaking(who: String)
signal camera_cut
signal arc_finished(id: String, return_to: String)

var world: Dictionary = {}
var flags: Dictionary = {}
var inventory: Array = []      # unique item ids owned (UI order)
var counts: Dictionary = {}    # item id -> quantity
var systems: Dictionary = {}
var party: Array = []
var member_state: Dictionary = {}  # id -> {hp, nerve, drained}
var selected_item: String = ""
var current: String = ""
var visited: Dictionary = {}
var protagonist := "harker"
var roster: Array = []          # characters the story has introduced (unlocks their personal arcs)
var in_arc := ""
var arc_stack: Array = []       # snapshot of the main game while an arc is played
var arcs_done: Array = []
var meta: Dictionary = {}       # persists across games: {game_complete: bool}
var journal: Array = []


func _ready() -> void:
	var f := FileAccess.open("res://data/world.json", FileAccess.READ)
	if f == null:
		push_error("data/world.json missing - run pipeline/build_assets.py")
		return
	world = JSON.parse_string(f.get_as_text())
	load_meta()
	ending.connect(func(_t: String) -> void:
		meta["game_complete"] = true
		save_meta())
	systems = JSON.parse_string(FileAccess.get_file_as_string("res://data/systems.json"))


var resolved: Dictionary = {}
var seed_value := 0
var force_regions := false      # debug: build merged regions even in test modes


## Resolve the whole seeded world once (or reload it from disk), then only read it.
func new_game(seed_in: int = -1, defaults: bool = false) -> void:
	world_defaults = defaults
	seed_value = seed_in if seed_in >= 0 else randi() % 1000000000
	var path := "user://worlds/%d%s.json" % [seed_value, "_default" if defaults else ""]
	var loaded: Variant = null
	if FileAccess.file_exists(path):
		loaded = JSON.parse_string(FileAccess.get_file_as_string(path))
	var wh := str(JSON.stringify(world).hash()) + "v" + str(WorldGen.VERSION)
	if loaded is Dictionary and loaded.has("locations") and loaded.get("world_hash", "") == wh:
		resolved = loaded
	else:
		resolved = WorldGen.generate(world, seed_value, defaults)
		resolved["world_hash"] = wh
		DirAccess.make_dir_recursive_absolute("user://worlds")
		var f := FileAccess.open(path, FileAccess.WRITE)
		f.store_string(JSON.stringify(resolved, " "))
	flags.clear()
	current = ""
	roster = []
	in_arc = ""
	arc_stack = []
	arcs_done = []
	protagonist = "harker"
	journal.clear()
	inventory.clear()
	counts.clear()
	party = systems.start_party.duplicate()
	member_state.clear()
	for id in party:
		_init_member(id)
		if not roster.has(id):
			roster.append(id)
	visited.clear()
	selected_item = ""
	inventory_changed.emit()


const SAVE_PATH := "user://savegame.json"
var autosave := true
var world_defaults := false


func has_save() -> bool:
	return FileAccess.file_exists(SAVE_PATH)


func save_game() -> void:
	if not autosave or current == "":
		return
	var d := {"seed": seed_value, "defaults": world_defaults, "flags": flags, "counts": counts, "inventory": inventory, "party": party,
		"member_state": member_state, "protagonist": protagonist, "journal": journal, "visited": visited, "current": current,
		"roster": roster, "arcs_done": arcs_done, "in_arc": in_arc, "arc_stack": arc_stack}
	var f := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	f.store_string(JSON.stringify(d))


## Restores a saved game; returns the location id to enter (or "" if none).
func load_game() -> String:
	if not has_save():
		return ""
	var d: Variant = JSON.parse_string(FileAccess.get_file_as_string(SAVE_PATH))
	if not d is Dictionary:
		return ""
	new_game(int(d.seed), bool(d.get("defaults", false)))
	flags = d.flags
	counts = {}
	for k in d.counts:
		counts[k] = int(d.counts[k])
	inventory = d.inventory
	party = d.party
	member_state = d.member_state
	protagonist = str(d.protagonist)
	journal = d.journal
	visited = d.visited
	roster = d.get("roster", party.duplicate())
	arcs_done = d.get("arcs_done", [])
	in_arc = str(d.get("in_arc", ""))
	arc_stack = d.get("arc_stack", [])
	inventory_changed.emit()
	party_changed.emit()
	return str(d.current)


var queued_after: Dictionary = {}


## Called by the HUD when a title card is dismissed: continues with a queued fight/dialogue (a goto is handled by the HUD).
func card_done() -> void:
	var q := queued_after
	queued_after = {}
	if q.get("goto", "") != "":
		return
	if q.get("fight", "") != "":
		fight_requested.emit(q.fight, "")
	elif q.get("talk", "") != "":
		dialogue_requested.emit(q.talk)


const META_PATH := "user://meta.json"


func load_meta() -> void:
	if FileAccess.file_exists(META_PATH):
		var d: Variant = JSON.parse_string(FileAccess.get_file_as_string(META_PATH))
		if d is Dictionary:
			meta = d


func save_meta() -> void:
	if not autosave:
		return
	var f := FileAccess.open(META_PATH, FileAccess.WRITE)
	f.store_string(JSON.stringify(meta))


func arc_def(id: String) -> Dictionary:
	for a in world.get("arcs_list", []):
		if a.id == id:
			return a
	return {}


## "done" | "available" | "locked" | "active". Unlock conditions are checked against the MAIN game state.
func arc_status(id: String) -> String:
	if in_arc == id:
		return "active"
	if arcs_done.has(id):
		return "done"
	var a := arc_def(id)
	if a.is_empty():
		return "locked"
	if in_arc != "":
		return "locked"
	if a.get("after_credits", false) and not meta.get("game_complete", false):
		return "locked"
	return "available" if check(str(a.get("unlock", ""))) else "locked"


func _snapshot() -> Dictionary:
	return JSON.parse_string(JSON.stringify({"flags": flags, "counts": counts, "inventory": inventory, "party": party,
		"member_state": member_state, "protagonist": protagonist, "journal": journal, "visited": visited, "current": current,
		"roster": roster}))


func _restore(s: Dictionary) -> void:
	flags = s.flags
	counts = {}
	for k in s.counts:
		counts[k] = int(s.counts[k])
	inventory = s.inventory
	party = s.party
	member_state = s.member_state
	protagonist = str(s.protagonist)
	journal = s.journal
	visited = s.visited
	roster = s.roster
	selected_item = ""
	inventory_changed.emit()
	party_changed.emit()
	state_changed.emit()


func start_arc(id: String) -> void:
	var a := arc_def(id)
	arc_stack.append(_snapshot())
	var main_states := member_state
	in_arc = id
	var st: Dictionary = a.start
	flags = {}
	for f in st.get("flags", []):
		flags[f] = true
	counts = {}
	inventory = []
	for it in st.get("items", {}):
		give(str(it), int(st.items[it]))
	party = []
	member_state = {}
	for pid in st.party:
		party.append(pid)
		if main_states.has(pid):
			member_state[pid] = main_states[pid].duplicate(true)
			member_state[pid].hp = int(systems.party[pid].hp) + int(member_state[pid].get("bonus", {}).get("hp", 0))
			member_state[pid].nerve = int(systems.party[pid].nerve) + int(member_state[pid].get("bonus", {}).get("nerve", 0))
		else:
			_init_member(pid)
	protagonist = str(st.protagonist)
	journal = []
	visited = {}
	selected_item = ""
	arc_started.emit(id)
	party_changed.emit()
	state_changed.emit()


func end_arc() -> void:
	if in_arc == "":
		return
	var id := in_arc
	var arc_journal := journal.duplicate()
	var snap: Dictionary = arc_stack.pop_back()
	_restore(snap)
	in_arc = ""
	for j in arc_journal:
		add_journal(str(j))
	if not arcs_done.has(id):
		arcs_done.append(id)
	run(arc_def(id).get("rewards", []))
	arc_finished.emit(id, str(snap.current))
	save_game()


## First arrival at an act's start location: make sure the party/roster/protagonist/items the act assumes exist.
func apply_act_start(loc_id: String) -> void:
	if in_arc != "":
		return
	for a in world.get("acts", []):
		if str(a.start.location) != loc_id or flags.get("actstart:%s" % a.id, false):
			continue
		flags["actstart:%s" % a.id] = true
		for pid in a.start.party:
			recruit(str(pid))
		protagonist = str(a.start.protagonist)
		for it in a.start.get("items", {}):
			var need := int(a.start.items[it]) - count(str(it))
			if need > 0:
				give(str(it), need)
		for f in a.start.get("flags", []):
			flags[str(f)] = true
		state_changed.emit()


func set_flag(name: String) -> void:
	if not flags.get(name, false):
		flags[name] = true
		state_changed.emit()


func add_journal(id: String) -> void:
	if world.get("journal", {}).has(id) and not journal.has(id):
		journal.append(id)
		journal_added.emit(id)
		grant_xp(party, 2)


func loc_data(id: String) -> Dictionary:
	return resolved.locations[id]


func item_def(id: String) -> Dictionary:
	return world.items.get(id, {"name": id, "asset": "key", "variant": "default", "desc": ""})


func has_item(id: String) -> bool:
	return counts.get(id, 0) > 0


func count(id: String) -> int:
	return counts.get(id, 0)


func give(id: String, n: int = 1) -> void:
	counts[id] = counts.get(id, 0) + n
	if not inventory.has(id):
		inventory.append(id)
	inventory_changed.emit()


func take_away(id: String, n: int = 1) -> void:
	counts[id] = maxi(0, counts.get(id, 0) - n)
	if counts[id] == 0:
		counts.erase(id)
		inventory.erase(id)
		if selected_item == id:
			selected_item = ""
	inventory_changed.emit()


func _init_member(id: String) -> void:
	var m: Dictionary = systems.party[id]
	member_state[id] = {"hp": m.hp, "nerve": m.nerve, "drained": false, "bonus": {}, "xp": 0, "level": 1,
		"equip": {"weapon": "", "armor": "", "charm": ""}}


# ------------------------------------------------------------------ levels, equipment, effective stats
func level_growth(level: int) -> Dictionary:
	var l := level - 1
	return {"hp": 3 * l, "nerve": 2 * l, "acc": l / 2, "eva": l / 3, "faith": l / 4, "dmg": l / 4}


func level_of(id: String) -> int:
	return int(member_state.get(id, {}).get("level", 1))


func xp_to_next(id: String) -> int:
	var lv := level_of(id)
	var thr: Array = systems.levels.xp
	return int(thr[lv]) if lv < int(systems.levels.max) else 0


func grant_xp(ids: Array, n: int) -> void:
	if n <= 0:
		return
	for id in ids:
		if not member_state.has(id):
			continue
		var st: Dictionary = member_state[id]
		st["xp"] = int(st.get("xp", 0)) + n
		var thr: Array = systems.levels.xp
		while int(st.get("level", 1)) < int(systems.levels.max) and int(st.xp) >= int(thr[int(st.get("level", 1))]):
			var before := level_growth(int(st.level))
			st["level"] = int(st.level) + 1
			var after := level_growth(int(st.level))
			st["hp"] = int(st.hp) + int(after.hp) - int(before.hp)
			st["nerve"] = int(st.nerve) + int(after.nerve) - int(before.nerve)
			level_up.emit(id, int(st.level))
	party_changed.emit()


## Base stats + level growth + permanent bonuses + equipment, ready for combat and for the party screen.
func effective(id: String) -> Dictionary:
	var m: Dictionary = systems.party[id]
	var st: Dictionary = member_state.get(id, {})
	var g := level_growth(int(st.get("level", 1)))
	var b: Dictionary = st.get("bonus", {})
	var eq: Dictionary = st.get("equip", {})
	var out := {"max_hp": int(m.hp) + int(g.hp) + int(b.get("hp", 0)), "max_nerve": int(m.nerve) + int(g.nerve) + int(b.get("nerve", 0)),
		"acc": int(m.acc) + int(g.acc) + int(b.get("acc", 0)), "eva": int(m.eva) + int(g.eva) + int(b.get("eva", 0)),
		"faith": int(m.faith) + int(g.faith) + int(b.get("faith", 0)), "dmg": int(g.dmg) + int(b.get("dmg", 0)), "armor": 0, "weapon": ""}
	for slot in ["armor", "charm"]:
		var it := str(eq.get(slot, ""))
		if it != "" and systems.equip.has(it):
			var e: Dictionary = systems.equip[it]
			out.armor += int(e.get("armor", 0))
			out.max_hp += int(e.get("hp", 0))
			out.max_nerve += int(e.get("nerve", 0))
			out.acc += int(e.get("acc", 0))
			out.eva += int(e.get("eva", 0))
			out.faith += int(e.get("faith", 0))
			out.dmg += int(e.get("dmg", 0))
	var w := str(eq.get("weapon", ""))
	if w != "" and systems.equip.has(w) and has_item(w):
		out["weapon"] = str(systems.equip[w].weapon)
	return out


func equipped_by(item: String) -> String:
	for id in member_state:
		for slot in member_state[id].get("equip", {}):
			if member_state[id].equip[slot] == item:
				return str(id)
	return ""


func equip(id: String, slot: String, item: String) -> bool:
	if not member_state.has(id):
		return false
	if item != "":
		if not systems.equip.has(item) or str(systems.equip[item].slot) != slot or not has_item(item):
			return false
		if slot == "weapon":
			var w: Dictionary = systems.weapons[str(systems.equip[item].weapon)]
			var users: Array = w.get("users", ["any"])
			if not (users.has("any") or users.has(id)):
				return false
		var other := equipped_by(item)
		if other != "":
			member_state[other].equip[slot] = ""
	if not member_state[id].has("equip"):
		member_state[id]["equip"] = {"weapon": "", "armor": "", "charm": ""}
	member_state[id].equip[slot] = item
	party_changed.emit()
	return true


func meet(id: String) -> void:
	if not roster.has(id):
		roster.append(id)
		state_changed.emit()


func add_bonus(id: String, b: Dictionary) -> void:
	if not member_state.has(id):
		if not systems.party.has(id):
			return
		_init_member(id)
	var cur: Dictionary = member_state[id].bonus
	for k in b:
		cur[k] = int(cur.get(k, 0)) + int(b[k])
	if b.has("hp"):
		member_state[id].hp += int(b.hp)
	if b.has("nerve"):
		member_state[id].nerve += int(b.nerve)
	party_changed.emit()


func recruit(id: String) -> void:
	meet(id)
	if not party.has(id):
		party.append(id)
		_init_member(id)
		party_changed.emit()


func item_name(id: String) -> String:
	if systems.items.has(id):
		return str(systems.items[id].name)
	return str(item_def(id).name)


## Crafting: returns "" on success or a reason.
func can_craft(rid: String) -> String:
	var r: Dictionary = systems.recipes[rid]
	if not check(str(r.get("unlock", ""))):
		return "Unknown recipe"
	for it in r.needs:
		if count(it) < int(r.needs[it]):
			return "Missing %s" % item_name(it)
	for t in r.get("tools", []):
		if not has_item(t):
			return "Needs %s" % item_name(t)
	return ""


func craft(rid: String) -> bool:
	if can_craft(rid) != "":
		return false
	var r: Dictionary = systems.recipes[rid]
	for it in r.needs:
		take_away(it, int(r.needs[it]))
	for it in r.makes:
		give(it, int(r.makes[it]))
	Audio.sfx("craft")
	message.emit("Crafted: %s." % str(r.name))
	return true


func check(cond: String) -> bool:
	if cond == "":
		return true
	if cond.contains("&"):
		for part in cond.split("&"):
			if not check(part.strip_edges()):
				return false
		return true
	var neg := cond.begins_with("!")
	var c := cond.substr(1) if neg else cond
	var r := false
	if c.begins_with("has:"):
		r = has_item(c.substr(4))
	elif c.begins_with("prot:"):
		r = protagonist == c.substr(5)
	elif c.begins_with("party:"):
		r = party.has(c.substr(6))
	elif c.begins_with("roster:"):
		r = roster.has(c.substr(7))
	elif c.begins_with("meta:"):
		r = meta.get(c.substr(5), false)
	elif c.begins_with("journal:"):
		r = journal.has(c.substr(8))
	elif c.begins_with("flag:"):
		r = flags.get(c.substr(5), false)
	else:
		r = flags.get(c, false)
	return r != neg


## Executes scripted actions in order; all "say" lines are joined into one message.
func run(actions: Array) -> void:
	var said: Array = []
	var jump := ""
	var talk := ""
	var card := ""
	var fight := ""
	for a in actions:
		var d: Dictionary = a
		if d.has("say"):
			said.append(str(d.say))
		if d.has("give"):
			give(str(d.give))
		if d.has("take"):
			take_away(str(d.take))
		if d.has("set"):
			set_flag(str(d.set))
		if d.has("unset"):
			flags.erase(str(d.unset))
			state_changed.emit()
		if d.has("journal"):
			add_journal(str(d.journal))
		if d.has("recruit"):
			recruit(str(d.recruit))
		if d.has("meet"):
			meet(str(d.meet))
		if d.has("xp"):
			grant_xp(party, int(d.xp))
		if d.has("stat"):
			var sd: Dictionary = d.stat
			add_bonus(str(sd.member), {"hp": int(sd.get("hp", 0)), "nerve": int(sd.get("nerve", 0)), "acc": int(sd.get("acc", 0)),
				"eva": int(sd.get("eva", 0)), "faith": int(sd.get("faith", 0)), "dmg": int(sd.get("dmg", 0))})
		if d.has("arc_end"):
			end_arc()
			return
		if d.has("protagonist"):
			protagonist = str(d.protagonist)
			state_changed.emit()
		if d.has("heal"):
			for id in party:
				member_state[id].hp = systems.party[id].hp
				member_state[id].nerve = systems.party[id].nerve
			party_changed.emit()
		if d.has("card"):
			card = str(d.card)
		if d.has("fight"):
			fight = str(d.fight)
		if d.has("end"):
			ending.emit(str(d.end))
		if d.has("goto"):
			jump = str(d.goto)
		if d.has("talk"):
			talk = str(d.talk)
	if said.size() > 0 and card == "":
		message.emit("\n".join(said))
	if card != "":
		queued_after = {"fight": fight, "talk": talk, "goto": jump}
		card_requested.emit(card + ("\n\n" + "\n".join(said) if said.size() > 0 else ""), jump)
	elif jump != "":
		goto_requested.emit(jump, current)
	elif fight != "":
		fight_requested.emit(fight, "")
	elif talk != "":
		dialogue_requested.emit(talk)
