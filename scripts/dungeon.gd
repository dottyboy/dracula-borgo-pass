class_name Dungeon
extends RefCounted
## Generated levels from Game Level Architect ("gla-export/1": a .glb plus a .json describing where one may walk,
## the entrance/exit, rooms and lights). A dungeon is a location whose id starts with "dungeon_"; its files are
## data/dungeons/<id>.json and assets/dungeons/<id>.glb (see pipeline/import_dungeon.py).
## The glb gives the look, the json the movement: Location uses the walk rectangles exactly like a merged region.

const DIR := "res://data/dungeons/"
const GLB_DIR := "res://assets/dungeons/"
const WALL_PREFIXES := ["Procedural_Level_Castle", "Procedural_Level_Walls", "Procedural_Level_RoundWalls", "Procedural_Level_Doors", "Procedural_Level_RoundDoors", "Procedural_Level_Windows"]
const LIGHT_W_TO_ENERGY := 1.0 / 25.0         # Blender watts -> this game's light energy
const RECT_GROW := 0.45                       # rectangles overlap a little so neighbouring ones connect (movement keeps 0.4 m inside)

## Architect decoration kinds -> this game's models: [model, variant, blocker radius (0 = walk through)]
const PROP_MAP := {
	"CRATE": ["crate_stack", "", 0.55], "BARREL": ["barrel", "oak", 0.4], "TABLE": ["table", "dark", 0.8], "CHAIR": ["chair", "black", 0.0],
	"CHEST": ["chest", "dark", 0.5], "BOOKSHELF": ["bookshelf", "ebony", 0.55], "COLUMN": ["column", "stone_dark", 0.45],
	"COFFIN": ["coffin", "ebony", 0.9], "TOMB": ["tomb", "stone_dark", 0.95], "BED": ["bed", "red", 1.0], "CANDLESTAND": ["candelabra", "", 0.25],
}

static var _cut_materials: Array = []
static var _doors: Array = []          # {node, closed_y, c (panel centre relative to its hinge, local), t, target, sign}
const DOOR_OPEN := 2.3                  # a panel starts to open when the player is this close to its middle
const DOOR_CLOSE := 3.4
const DOOR_SPEED := 2.6


static func path(id: String) -> String:
	return DIR + id + ".json"


static func exists(id: String) -> bool:
	return id.begins_with("dungeon_") and FileAccess.file_exists(path(id))


static func load_def(id: String) -> Dictionary:
	var f := FileAccess.open(path(id), FileAccess.READ)
	var parsed: Variant = JSON.parse_string(f.get_as_text())
	assert(parsed is Dictionary and str(parsed.get("format", "")).begins_with("gla-export/"), "not a Level Architect export: " + id)
	var def: Dictionary = parsed
	# hand-written story layer: data/dungeons/<id>.story.json (never overwritten by an import)
	var sp := DIR + id + ".story.json"
	if FileAccess.file_exists(sp):
		var st: Variant = JSON.parse_string(FileAccess.get_file_as_string(sp))
		if st is Dictionary:
			def["story"] = st
			if st.has("entrance") and def.has("entrance_from"):
				(def.entrance_from as Dictionary).merge(st.entrance, true)
	return def


## Story props, positioned by anchors so they survive re-importing a different generated level:
## "entrance", "exit", "room:K" (K-th room, wrapping), "far:K" (K-th farthest room from the entrance). dx/dz nudge the spot if it stays walkable.
static func story_props(def: Dictionary) -> Array:
	var out: Array = []
	var st: Dictionary = def.get("story", {})
	var cells := cells_of(def)
	var ts := float(def.tile_size)
	var ent := Vector2(float(def.entrance.pos[0]), float(def.entrance.pos[2])) if def.get("entrance") is Dictionary else Vector2.ZERO
	var ex := Vector2(float(def.exit.pos[0]), float(def.exit.pos[2])) if def.get("exit") is Dictionary else ent
	var rooms: Array = []
	for r in def.get("rooms", []):
		rooms.append(Vector2(float(r.center[0]), float(r.center[1])))
	var far := rooms.duplicate()
	far.sort_custom(func(a: Vector2, b: Vector2) -> bool: return a.distance_to(ent) > b.distance_to(ent))
	for p in st.get("props", []):
		var at := str(p.get("at", "entrance"))
		var pt := ent
		if at == "exit":
			pt = ex
		elif at.begins_with("room:") and not rooms.is_empty():
			pt = rooms[int(at.substr(5)) % rooms.size()]
		elif at.begins_with("far:") and not far.is_empty():
			pt = far[int(at.substr(4)) % far.size()]
		var base := _nearest_cell(cells, ts, pt)
		var c := Vector2(base.x * ts, base.y * ts) if base != Vector2i(1 << 30, 0) else pt
		var nudged := c + Vector2(float(p.get("dx", 0.0)), float(p.get("dz", 0.0)))
		if _open(cells, nudged, ts, 0.5):
			c = nudged
		var d: Dictionary = (p as Dictionary).duplicate(true)
		d["pos"] = [c.x, float(p.get("y", 0.0)), c.y]
		d["scale"] = float(p.get("scale", 1.0))
		d["variant"] = str(p.get("variant", ""))
		d["rot"] = float(p.get("rot", 0))
		d["radius"] = float(p.get("radius", 0.5))
		out.append(d)
	return out


static func story_on_enter(def: Dictionary) -> Array:
	return def.get("story", {}).get("on_enter", [])


## Walk rectangles of one floor as Rect2 in (x, z), slightly grown so adjacent ones overlap.
static func floor_rects(def: Dictionary, floor_index: int = 0) -> Array:
	var out: Array = []
	var fl: Dictionary = def.floors[mini(floor_index, def.floors.size() - 1)]
	for r in fl.walk_rects:
		out.append(Rect2(float(r[0]), float(r[1]), float(r[2]) - float(r[0]), float(r[3]) - float(r[1])).grow(RECT_GROW))
	return out


## The walkable tiles of one floor, as {Vector2i(ix, iz): true}; a tile's centre is (ix * tile, iz * tile).
## Rebuilt from the walk rectangles (they are an exact cover of the tiles).
static func cells_of(def: Dictionary, floor_index: int = 0) -> Dictionary:
	var ts := float(def.tile_size)
	var out := {}
	var fl: Dictionary = def.floors[mini(floor_index, def.floors.size() - 1)]
	for r in fl.walk_rects:
		for ix in range(roundi(float(r[0]) / ts + 0.5), roundi(float(r[2]) / ts - 0.5) + 1):
			for iz in range(roundi(float(r[1]) / ts + 0.5), roundi(float(r[3]) / ts - 0.5) + 1):
				out[Vector2i(ix, iz)] = true
	return out


static func _cell_at(cells: Dictionary, p: Vector2, ts: float) -> Vector2i:
	return Vector2i(roundi(p.x / ts), roundi(p.y / ts))


## A point is comfortable to stand on when it and the four points 0.4 m around it are on walkable tiles.
static func _open(cells: Dictionary, p: Vector2, ts: float, margin: float = 0.4) -> bool:
	for o in [Vector2.ZERO, Vector2(margin, 0), Vector2(-margin, 0), Vector2(0, margin), Vector2(0, -margin)]:
		if not cells.has(_cell_at(cells, p + o, ts)):
			return false
	return true


static func _clear(cells: Dictionary, a: Vector2, b: Vector2, ts: float) -> bool:
	var n := maxi(1, ceili(a.distance_to(b) / 0.25))
	for i in n + 1:
		if not _open(cells, a.lerp(b, float(i) / n), ts):
			return false
	return true


## Route over tile centres (A*, 8 directions without cutting corners), then straightened wherever the way is clear.
## Returns waypoints in (x, z); empty when there is no route.
static func find_path(cells: Dictionary, ts: float, from: Vector2, to: Vector2) -> Array:
	var start := _nearest_cell(cells, ts, from)
	var goal := _nearest_cell(cells, ts, to)
	if start == Vector2i(1 << 30, 0) or goal == Vector2i(1 << 30, 0):
		return []
	var came := {}
	var g := {start: 0.0}
	var open := [start]
	while not open.is_empty():
		var cur: Vector2i = open[0]
		var best_f := 1e18
		for o in open:
			var f: float = g[o] + Vector2(o - goal).length()
			if f < best_f:
				best_f = f
				cur = o
		if cur == goal:
			break
		open.erase(cur)
		for d in [Vector2i(1, 0), Vector2i(-1, 0), Vector2i(0, 1), Vector2i(0, -1), Vector2i(1, 1), Vector2i(1, -1), Vector2i(-1, 1), Vector2i(-1, -1)]:
			var nb: Vector2i = cur + d
			if not cells.has(nb):
				continue
			if d.x != 0 and d.y != 0 and not (cells.has(cur + Vector2i(d.x, 0)) and cells.has(cur + Vector2i(0, d.y))):
				continue
			var ng: float = g[cur] + Vector2(d).length()
			if not g.has(nb) or ng < g[nb]:
				g[nb] = ng
				came[nb] = cur
				if not open.has(nb):
					open.append(nb)
	if goal != start and not came.has(goal):
		return []
	var chain: Array = [goal]
	while chain[0] != start:
		chain.push_front(came[chain[0]])
	var pts: Array = []
	for c in chain:
		pts.append(Vector2(c.x * ts, c.y * ts))
	pts[0] = from if _open(cells, from, ts) else pts[0]
	# string pulling
	var out: Array = [pts[0]]
	var i := 0
	while i < pts.size() - 1:
		var j := pts.size() - 1
		while j > i + 1 and not _clear(cells, pts[i], pts[j], ts):
			j -= 1
		out.append(pts[j])
		i = j
	var last: Vector2 = to if cells.has(_cell_at(cells, to, ts)) else pts[pts.size() - 1]
	if _open(cells, last, ts) and _clear(cells, out[out.size() - 1], last, ts):
		out[out.size() - 1] = last
	return out


static func _nearest_cell(cells: Dictionary, ts: float, p: Vector2) -> Vector2i:
	var c := _cell_at(cells, p, ts)
	if cells.has(c):
		return c
	var best := Vector2i(1 << 30, 0)
	var bd := 1e18
	for k in cells:
		var d := Vector2(k.x * ts, k.y * ts).distance_squared_to(p)
		if d < bd:
			bd = d
			best = k
	return best


## Story locations can grow an entrance to a dungeon without touching world.json (so the story validator never sees it):
## a dungeon json with "entrance_from": {"loc", "pos": [x, z], "name", "look", "rot"} adds a door prop to that location when it is built.
static func inject(loc_id: String, data: Dictionary) -> void:
	for did in all_ids():
		var def := load_def(did)
		var ef: Variant = def.get("entrance_from")
		if not (ef is Dictionary) or str(ef.loc) != loc_id:
			continue
		var pos: Array = ef.pos
		data.props.append({"id": did + "_door", "asset": str(ef.get("asset", "door")), "variant": str(ef.get("variant", "dark")),
			"pos": [pos[0], 0.0, pos[1]], "rot": float(ef.get("rot", 0)), "scale": 1.0, "radius": 0.6, "name": str(ef.get("name", "A way down")),
			"interact": {"go": did, "look": str(ef.get("look", "A passage leading down into the dark.")),
				"go_cond": str(ef.get("go_cond", "")), "go_fail": str(ef.get("go_fail", "It will not open."))}})
		var back: Array = ef.get("back_pos", [float(pos[0]) - 1.2, float(pos[1])])
		data.spawns[did] = [back[0], back[1]]


static func all_ids() -> Array:
	var out: Array = []
	var d := DirAccess.open(DIR)
	if d == null:
		return out
	for f in d.get_files():
		if f.begins_with("dungeon_") and f.ends_with(".json") and not f.contains(".story"):
			out.append(f.get_basename())
	return out


static func spawn_of(def: Dictionary, from_loc: String) -> Vector2:
	var arr: Dictionary = def.get("arrivals", {})
	if arr.has(from_loc):
		return Vector2(float(arr[from_loc][0]), float(arr[from_loc][1]))
	var e: Variant = def.get("entrance")
	if e is Dictionary:
		return Vector2(float(e.pos[0]), float(e.pos[2]))
	var rects := floor_rects(def)
	return rects[0].get_center() if not rects.is_empty() else Vector2.ZERO


## Lights in the format Location._lights() reads.
static func lights_of(def: Dictionary) -> Array:
	var out: Array = []
	for l in def.get("lights", []):
		out.append({"pos": [l.pos[0], l.pos[1], l.pos[2]], "color": "#" + Color(l.color[0], l.color[1], l.color[2]).to_html(false),
			"energy": clampf(float(l.energy_w) * LIGHT_W_TO_ENERGY, 0.8, 4.0), "range": 7.5})
	return out


## The level's visuals. Works whether or not Godot has imported the .glb yet (editor import vs. runtime load).
static func load_scene(def: Dictionary) -> Node3D:
	var p: String = GLB_DIR + str(def.glb)
	var root: Node3D = null
	if ResourceLoader.exists(p):
		root = (load(p) as PackedScene).instantiate()
	else:
		var doc := GLTFDocument.new()
		var st := GLTFState.new()
		var err := doc.append_from_file(ProjectSettings.globalize_path(p), st)
		assert(err == OK, "cannot load " + p)
		root = doc.generate_scene(st)
	root.position.y = -float(def.get("floor_y", 0.0))   # an upper floor of a multi-floor level is shifted down to y = 0
	_restyle(root)
	_cutaway(root)
	_find_doors(root)
	return root


## Door panels (Architect exports each as its own node whose origin is the hinge): they swing open as the player comes close.
static func _find_doors(root: Node) -> void:
	_doors.clear()
	for mi in root.find_children("*_Panel_*", "MeshInstance3D", true, false):
		var inst: MeshInstance3D = mi
		if inst.mesh == null:
			continue
		var bb: AABB = inst.mesh.get_aabb()
		# the scene is not in the tree yet, so global_transform is not available: compose the chain by hand
		var chain := inst.transform
		var up: Node = inst.get_parent()
		while up is Node3D:
			chain = (up as Node3D).transform * chain
			up = up.get_parent()
		_doors.append({"node": inst, "closed_y": inst.rotation.y, "c": bb.get_center(), "t": 0.0, "target": 0.0, "sign": 1.0,
			"mid0": chain * bb.get_center()})


## Architect's debug-colour swatch materials (one flat colour per room...) become this game's stone, wood and cobble.
## Real masonry (the brick rings, towers) keeps its own textures. Matching is by the material names the exporter keeps.
static func _style_for(mat_name: String) -> String:
	if mat_name.begins_with("LA_Floor") or mat_name.contains("_Room") or mat_name.begins_with("LA_Corridor"):
		return "floor"
	if mat_name == "LA_Simple_Wall" or mat_name == "LA_Simple_Stair":
		return "wall"
	if mat_name == "LA_Door" or mat_name == "LA_Entrance" or mat_name == "LA_Exit" or mat_name == "LA_Prop":
		return "wood"
	return ""


static func _spec(kind: String) -> Dictionary:
	match kind:
		"floor":
			return Assets.manifest.models["floor_4x4"].variants["cobble"].stone
		"wall":
			return Assets.manifest.models["wall_4"].variants["stone_dark"].stone
		"wood":
			return Assets.manifest.models["floor_4x4"].variants["planks"].stone
	return {}


static func _restyle(node: Node) -> void:
	var cache := {}
	for mi in node.find_children("*", "MeshInstance3D", true, false):
		var inst: MeshInstance3D = mi
		if inst.mesh == null:
			continue
		for s in inst.mesh.get_surface_count():
			var src: Material = inst.get_active_material(s)
			if src == null:
				continue
			var kind := _style_for(src.resource_name)
			if kind == "" or kind == "wall":
				if kind == "wall":
					inst.set_meta("wall_style", true)
				continue
			if not cache.has(kind):
				var m: StandardMaterial3D = Assets.material_for(_spec(kind)).duplicate()
				m.uv1_triplanar = true
				m.uv1_world_triplanar = true
				m.uv1_scale = Vector3.ONE * m.uv1_scale.x
				cache[kind] = m
			inst.set_surface_override_material(s, cache[kind])


## Walls fade out above head height between the camera and the player.
static func _cutaway(node: Node) -> void:
	var sh: Shader = load("res://shaders/cutaway.gdshader")
	var cache := {}
	for mi in node.find_children("*", "MeshInstance3D", true, false):
		var inst: MeshInstance3D = mi
		var wall := false
		for pre in WALL_PREFIXES:
			if inst.name.begins_with(pre) or (inst.get_parent() != null and inst.get_parent().name.begins_with(pre)):
				wall = true
		if not wall or inst.mesh == null:
			continue
		for s in inst.mesh.get_surface_count():
			var src: Material = inst.get_active_material(s)
			if not (src is StandardMaterial3D):
				continue
			var key := src.get_instance_id()
			if not cache.has(key):
				var std: StandardMaterial3D = src
				var sm := ShaderMaterial.new()
				sm.shader = sh
				sm.set_shader_parameter("albedo_col", std.albedo_color)
				if std.albedo_texture != null:
					sm.set_shader_parameter("albedo_tex", std.albedo_texture)
					sm.set_shader_parameter("use_albedo_tex", true)
				if std.normal_enabled and std.normal_texture != null:
					sm.set_shader_parameter("normal_tex", std.normal_texture)
					sm.set_shader_parameter("use_normal_tex", true)
				sm.set_shader_parameter("roughness", std.roughness)
				if _style_for(std.resource_name) == "wall":
					var spec := _spec("wall")
					var base: StandardMaterial3D = Assets.material_for(spec)
					sm.set_shader_parameter("tri_tex", base.albedo_texture)
					sm.set_shader_parameter("tri_col", base.albedo_color)
					sm.set_shader_parameter("tri_scale", base.uv1_scale.x)
					sm.set_shader_parameter("use_tri", true)
					sm.set_shader_parameter("use_albedo_tex", false)
				_cut_materials.append(sm)
				cache[key] = sm
			inst.set_surface_override_material(s, cache[key])


## Replaces Architect's baked decoration mesh with this game's own models (the json lists kind, position and yaw).
## Returns the blockers (circles in x, z) for the big ones. Models face +Z, Architect's props face +X: yaw + 90 degrees.
static func spawn_props(def: Dictionary, root: Node3D) -> Array:
	var blockers: Array = []
	var props: Array = def.get("props", [])
	if props.is_empty():
		return blockers
	for mi in root.find_children("Procedural_Level_Decoration*", "MeshInstance3D", true, false):
		mi.queue_free()
	var holder := Node3D.new()
	holder.name = "GamePropsFromArchitect"
	root.add_child(holder)
	var wall_h := float(def.get("wall_height", 3.0))
	for p in props:
		var kind := str(p.kind)
		if not PROP_MAP.has(kind):
			continue
		var m: Array = PROP_MAP[kind]
		var node: Node3D = Assets.instantiate(str(m[0]), str(m[1]))
		if node == null:
			continue
		node.position = Vector3(float(p.pos[0]), float(p.pos[1]), float(p.pos[2]))
		node.rotation.y = float(p.yaw) + PI / 2.0
		if kind == "COLUMN":
			node.scale = Vector3.ONE * (wall_h / 3.0)
		holder.add_child(node)
		if float(m[2]) > 0.0:
			blockers.append({"pos": Vector2(node.position.x, node.position.z), "r": float(m[2])})
	return blockers


## Called every frame by Location: tells the wall shader where the player and camera are, and swings doors.
static func track(player_pos: Vector3, cam_pos: Vector3, delta: float = 0.0) -> void:
	_swing_doors(player_pos, delta)
	for m in _cut_materials:
		if is_instance_valid(m):
			(m as ShaderMaterial).set_shader_parameter("player_pos", player_pos)
			(m as ShaderMaterial).set_shader_parameter("cam_pos", cam_pos)


static func _swing_doors(player_pos: Vector3, delta: float) -> void:
	for d in _doors:
		var node: Node3D = d.node
		if not is_instance_valid(node):
			continue
		var mid: Vector3 = d.mid0          # the doorway's middle (fixed: the panel's own middle moves while it swings)
		var dist := Vector2(mid.x - player_pos.x, mid.z - player_pos.z).length()
		var was: float = d.target
		if dist < DOOR_OPEN:
			d.target = 1.0
		elif dist > DOOR_CLOSE:
			d.target = 0.0
		if d.target != was and d.t == (0.0 if d.target > 0.5 else 1.0):
			Audio.sfx("door", 1.0, -4.0)
		if d.target > 0.5 and was < 0.5:
			# swing away from the player: try both senses of rotation and keep the one that moves the panel's middle farther from them
			var hinge: Vector3 = node.global_position
			var c: Vector3 = d.c
			var rot_a := Basis(Vector3.UP, PI / 2.0) * c
			var rot_b := Basis(Vector3.UP, -PI / 2.0) * c
			var pa := Vector2(hinge.x + rot_a.x - player_pos.x, hinge.z + rot_a.z - player_pos.z).length()
			var pb := Vector2(hinge.x + rot_b.x - player_pos.x, hinge.z + rot_b.z - player_pos.z).length()
			d.sign = 1.0 if pa >= pb else -1.0
		d.t = move_toward(d.t, d.target, delta * DOOR_SPEED)
		node.rotation.y = float(d.closed_y) + float(d.sign) * (PI / 2.0) * smoothstep(0.0, 1.0, d.t)


static func reset_materials() -> void:
	_cut_materials.clear()
	_doors.clear()
