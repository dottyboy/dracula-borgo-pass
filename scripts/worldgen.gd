class_name WorldGen
extends RefCounted
## Seeded world generation. Runs ONCE when a new game starts: takes the authored
## location templates (data/world.json) + a seed and resolves every random choice
## (palette, door/window cells, prop jitter, where quest items are hidden, which
## requirement opens a gate). The result is a plain Dictionary, saved to
## user://worlds/<seed>.json, and the game afterwards only reads it.
## Same seed -> identical world. Every choice keeps the game solvable.

const CELL := 4.0
const VERSION := 2   # bump when generation logic changes (invalidates cached worlds)
const WOODS := ["oak", "dark", "pale", "ebony"]
const CLOTHS := ["red", "blue", "green", "black"]
const ANCHORED := ["fireplace", "mirror", "bookshelf", "sconce", "inn_sign", "castle_keep", "bust"]


static func seed_from_text(t: String) -> int:
	var s := t.strip_edges()
	if s.is_valid_int():
		return int(s)
	return absi(s.hash()) % 1000000000


static func generate(world: Dictionary, seed_value: int, defaults: bool = false) -> Dictionary:
	var out := {"seed": seed_value, "locations": {}, "placed": {}, "gates": {}}
	var g := RandomNumberGenerator.new()
	g.seed = hash("world:%d" % seed_value)
	var loc_data: Dictionary = world.loc_data.duplicate(true)

	# 1. gates: pick one requirement per gate
	var needed_items: Array = []
	for gid in world.gates:
		var opts: Array = world.gates[gid]
		var pick: Dictionary = opts[0] if defaults else opts[g.randi() % opts.size()]
		out.gates[gid] = pick
		needed_items.append(pick.needs)
		for lid in loc_data:
			for p in loc_data[lid].props:
				if p.id == gid:
					p.interact.go_cond = pick.cond
					p.interact.go_fail = pick.fail
	# items that only exist as one alternative of some gate are placed only when that alternative was chosen
	var gate_items: Array = []
	for gid in world.gates:
		for o in world.gates[gid]:
			gate_items.append(o.needs)

	# 2. quest item placement: strip static takes on all holders, then place
	for item in world.placements:
		for h in world.placements[item]:
			for lid in loc_data:
				for p in loc_data[lid].props:
					if p.id == h.prop and p.get("interact", {}).has("take") and p.interact.take == item:
						p.interact.erase("take")
						p.interact.erase("take_text")
						p.interact.erase("give_once")
	for item in world.placements:
		if gate_items.has(item) and not needed_items.has(item):
			continue
		var holders: Array = world.placements[item]
		var h: Dictionary = holders[0] if defaults else holders[g.randi() % holders.size()]
		out.placed[item] = h.prop
		for lid in loc_data:
			for p in loc_data[lid].props:
				if p.id == h.prop:
					if not p.has("interact"):
						p.interact = {"look": "Weathered stone."}
					if str(p.get("name", "")) == "":
						p.name = "Stone column"
					p.interact.take = item
					p.interact.take_text = h.text
					p.interact.give_once = true
					p.interact.look = str(p.interact.get("look", "")) + " " + str(h.hint)

	# 3. per-location layout and look
	for lid in loc_data:
		if defaults:
			break
		var rng := RandomNumberGenerator.new()
		rng.seed = hash("loc:%d:%s" % [seed_value, lid])
		_style(loc_data[lid], world.palettes.get(lid, []), rng)
		_layout(loc_data[lid], rng)
	out.locations = loc_data
	return out


static func _style(ld: Dictionary, palettes: Array, rng: RandomNumberGenerator) -> void:
	ld.light_scale = rng.randf_range(0.9, 1.15)
	if palettes.is_empty():
		return
	var pal: Dictionary = palettes[rng.randi() % palettes.size()]
	ld.palette = pal
	if pal.has("wall"):
		ld.wall = pal.wall
	if pal.has("floor"):
		ld.floor = pal.floor
	for p in ld.props:
		if pal.has("wood") and WOODS.has(str(p.variant)) and not str(p.asset).begins_with("door_big"):
			p.variant = pal.wood
		if pal.has("cloth") and CLOTHS.has(str(p.variant)) and ["chair", "bed", "bed_simple", "throne", "rug"].has(str(p.asset)):
			p.variant = pal.cloth
	if pal.has("tree"):
		for k in ["scatter", "scatter2", "scatter3"]:
			if ld.has(k) and ld[k].asset.begins_with("pine"):
				ld[k].variant = pal.tree
		if ld.has("scatter"):
			ld.scatter.seed = rng.randi() % 100000


static func _side_of(p: Dictionary, w: float, d: float) -> String:
	var x: float = p.pos[0]
	var z: float = p.pos[2]
	if x < -w / 2 + 1.2:
		return "west"
	if x > w / 2 - 1.2:
		return "east"
	if z < -d / 2 + 1.2:
		return "north"
	return ""


static func _cell_index(side: String, p: Dictionary, w: float, d: float) -> int:
	if side == "north":
		return clampi(int((float(p.pos[0]) + w / 2) / CELL), 0, int(w / CELL) - 1)
	return clampi(int((float(p.pos[2]) + d / 2) / CELL), 0, int(d / CELL) - 1)


static func _layout(ld: Dictionary, rng: RandomNumberGenerator) -> void:
	var cells: Array = ld.cells
	var w: float = cells[0] * CELL
	var d: float = cells[1] * CELL
	var interior: bool = ld.get("interior", true)
	var margin := 1.0

	# --- jitter free props/NPCs (items lying on a table move with it)
	var hosts: Array = []
	for p in ld.props:
		if str(p.asset).begins_with("table"):
			hosts.append(p)
	for p in ld.props:
		if float(p.pos[1]) > 0.2 and not ANCHORED.has(str(p.asset)) and str(p.asset) != "mirror":
			for h in hosts:
				if Vector2(float(h.pos[0]) - float(p.pos[0]), float(h.pos[2]) - float(p.pos[2])).length() < 2.4:
					p.host = h.id
					break
	var deltas: Dictionary = {}
	for p in ld.props:
		if float(p.pos[1]) > 0.2 or float(p.get("radius", 0.5)) < 0.15:
			continue
		var side := _side_of(p, w, d)
		if side != "" or ANCHORED.has(str(p.asset)) or str(p.asset).begins_with("door") or str(p.asset).begins_with("column"):
			continue
		var nx := clampf(float(p.pos[0]) + rng.randf_range(-0.45, 0.45), -w / 2 + margin, w / 2 - margin)
		var nz := clampf(float(p.pos[2]) + rng.randf_range(-0.45, 0.45), -d / 2 + margin, d / 2 - margin)
		deltas[p.id] = Vector2(nx - float(p.pos[0]), nz - float(p.pos[2]))
		p.pos[0] = nx
		p.pos[2] = nz
	for p in ld.props:
		if p.has("host") and deltas.has(p.host):
			var dv: Vector2 = deltas[p.host]
			p.pos[0] += dv.x
			p.pos[2] += dv.y
	for n in ld.get("npcs", []):
		if not interior:
			continue
		n.pos[0] = clampf(float(n.pos[0]) + rng.randf_range(-0.6, 0.6), -w / 2 + margin, w / 2 - margin)
		n.pos[2] = clampf(float(n.pos[2]) + rng.randf_range(-0.6, 0.6), -d / 2 + margin, d / 2 - margin)

	# --- wall pieces: shuffle door / window cells
	var walls: Dictionary = ld.get("walls", {})
	if walls.is_empty():
		return
	for side in walls:
		var arr: Array = walls[side]
		var n := arr.size()
		var blocked: Array = []
		var doors: Array = []
		var windows := 0
		for piece in arr:
			if piece == "wall_window_4":
				windows += 1
		for p in ld.props:
			var s: String = _side_of(p, w, d)
			if s != side:
				continue
			var is_door: bool = str(p.asset).begins_with("door") and p.get("interact", {}).has("go")
			if is_door:
				doors.append(p)
			elif float(p.get("radius", 0.0)) > 0.15 or ANCHORED.has(str(p.asset)):
				blocked.append(_cell_index(side, p, w, d))
		for i in n:
			arr[i] = "wall_4"
		var free: Array = []
		for i in n:
			if not blocked.has(i):
				free.append(i)
		_shuffle(free, rng)
		for dp in doors:
			var idx := -1
			if free.size() > 0:
				idx = free.pop_back()
			else:
				idx = _cell_index(side, dp, w, d)
			arr[idx] = "wall_door_4"
			var c := -w / 2 + CELL / 2 + idx * CELL if side == "north" else -d / 2 + CELL / 2 + idx * CELL
			if side == "north":
				dp.pos[0] = c
			else:
				dp.pos[2] = c
		for i in windows:
			if free.size() == 0:
				break
			arr[free.pop_back()] = "wall_window_4"
		# arrival spawns follow the door the player came through
		for dp in doors:
			var sp := [float(dp.pos[0]), float(dp.pos[2])]
			match side:
				"north":
					sp[1] += 1.4
				"west":
					sp[0] += 1.4
				"east":
					sp[0] -= 1.4
			ld.spawns[dp.interact.go] = sp


static func _shuffle(a: Array, rng: RandomNumberGenerator) -> void:
	for i in range(a.size() - 1, 0, -1):
		var j := rng.randi() % (i + 1)
		var t: Variant = a[i]
		a[i] = a[j]
		a[j] = t
