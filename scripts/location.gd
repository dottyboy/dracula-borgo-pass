class_name Location
extends Node3D
## Builds one scene from data/world.json (loc_data) + the asset library and
## handles point & click: hover, walk-to, look/use/talk/take/exit.

signal hover_changed(text: String)
signal member_changed(member_id: String)
signal dungeon_exit(to: String)

const CELL := 4.0

var id := ""
var data: Dictionary = {}
var cam: Camera3D
var player: Actor
var entities: Dictionary = {}
var pending: Dictionary = {}
var bounds := Rect2()
var interior := true
var modal := false
var region := ""                      # set on the host of a merged region
var host: Location = null             # set on member islands
var members: Dictionary = {}          # member id -> Rect2 (region space)
var _walk_rects: Array = []           # Rect2: every member and connecting strip
var _land_rects: Array = []
var _member := ""
var _env: Environment
var _cam_off := Vector3.ZERO
var _flickers: Array = []
var _t := 0.0
var _hover := ""
var _cam_base := Vector3.ZERO
var _cam_look := Vector3.ZERO


func build(loc_id: String, from_loc: String) -> void:
	id = loc_id
	data = Game.loc_data(loc_id).duplicate(true)
	Dungeon.inject(loc_id, data)
	interior = data.get("interior", true)
	Dressing.upgrade_buildings(data)
	var cells: Array = data.cells
	var grow := _grow()
	var w: float = cells[0] * CELL + 2.0 * grow.x
	var d: float = cells[1] * CELL + 2.0 * grow.y
	room_w = w
	room_d = d
	var margin := 0.9 if interior else 0.4
	bounds = Rect2(-w / 2 + margin, -d / 2 + margin, w - 2 * margin, d - 2 * margin)
	_environment()
	_floor(cells, w, d)
	_skirt(w, d)
	_ground_detail(w, d)
	_walls(w, d)
	_lights()
	if data.has("moon"):
		_moon()
	_scatter(w, d)
	Dressing.add_loot(self)
	_props()
	_camera()
	_player(from_loc)
	_weather()
	_flames()
	Dressing.dress(self)


## One continuous landscape out of several outdoor scenes (see Regions). Members are built as islands of content
## (props, NPCs, buildings, lights) on top of one shared terrain, sea, camera and player.
func build_region(rid: String, focus: String, from_loc: String) -> void:
	if not Game.pie_chosen.is_connected(_on_pie_chosen):
		Game.pie_chosen.connect(_on_pie_chosen)      # the region root handles verb-ring choices for all its members
	region = rid
	var R: Dictionary = Regions.DEF[rid]
	var lay := Regions.layout(rid)
	_lay = lay
	members = lay.members
	_land_rects = []
	for m in members:
		_land_rects.append(members[m])
	for s in lay.strips:
		_land_rects.append(s)
	_walk_rects = _land_rects
	var amb_src: Dictionary = Game.loc_data(str(R.focus_ambient))
	id = "region_" + rid
	var fd: Dictionary = Game.loc_data(focus)
	data = {"ambient": amb_src.ambient, "floor": "grass", "water": true, "interior": false, "sky": str(R.get("sky", "day")), "wall": "stone_grey",
		"cells": [1, 1], "props": [], "npcs": [], "lights": [], "camera": amb_src.camera, "spawn": [0, 0], "spawns": {}}
	if str(fd.get("sky", "")) != "":
		data.sky = fd.sky
	interior = false
	room_w = lay.size.x
	room_d = lay.size.y
	bounds = Rect2(-room_w / 2, -room_d / 2, room_w, room_d)
	_environment()
	# floor patches (cobbled quays etc.) per member
	for m in members:
		var md: Dictionary = Game.loc_data(m)
		var fl := str(md.floor)
		if fl in ["grass", "dirt", "snow"]:
			continue
		var rc: Rect2 = members[m]
		var hard: Array = []
		var ov: Dictionary = R.get("overrides", {}).get(m, {})
		for s in ov.get("quay_sides", []):
			hard.append(s)
		if Dressing.theme_of(m, false) in ["dock", "street"] and Game.loc_data(m).get("walls", {}).has("north"):
			hard.append("north")
		_floor_patch(rc, fl, hard, float(lay.heights.get(m, 0.0)))
	var all_blockers: Array = []
	var seg_extra: Array = []
	for m in members:
		var sub := Location.new()
		var rc2: Rect2 = members[m]
		add_child(sub)
		sub.build_island(self, m, Vector3(rc2.get_center().x, float(lay.heights.get(m, 0.0)), rc2.get_center().y), R.get("overrides", {}).get(m, {}))
		for eid in sub.entities:
			entities[eid] = sub.entities[eid]
		for b in sub._blockers:
			all_blockers.append({"pos": (b.pos as Vector2) + rc2.get_center(), "r": b.r})
	# land under every building that stands outside the scenes' own rectangles (house rows behind walls), then the ground itself
	_terrain_rects = _land_rects.duplicate()
	for sub in get_children():
		if sub is Location and sub.host == self:
			var off := Vector2(sub.position.x, sub.position.z)
			for br in sub.get_meta("bldg_rects", []):
				_terrain_rects.append(Rect2((br as Rect2).position + off, (br as Rect2).size).grow(1.2))
	_terrain(room_w, room_d, "grass")
	# keep the connecting strips passable: nothing may block inside them
	var strips: Array = _land_rects.slice(members.size())
	_blockers = all_blockers.filter(func(b: Dictionary) -> bool:
		for s in strips:
			if (s as Rect2).grow(0.5).has_point(b.pos):
				return false
		return true)
	_member = focus
	var spp := region_spawn(focus, from_loc)
	data.spawn = [spp.x, spp.z]
	_build_links()
	_region_camera()
	_player(from_loc)
	player.clamp_fn = Callable(self, "_clamp_region")
	_weather()
	Dressing.dress_region(self, str(R.get("theme", "wild")))
	apply_member_mood(focus, false)
	if Game.meta.get("action_mode", false) and Game.in_arc == "":
		add_child(ActionMode.new().setup(self))


## The land between the scenes: vegetation by kind, lamp posts, benches and a few clickable finds.
func _build_links() -> void:
	var rng := RandomNumberGenerator.new()
	rng.seed = hash("links:%s:%d" % [region, Game.seed_value])
	var loot_props: Array = []
	var extra_blockers: Array = []
	var base := 0
	for i in _lay.links.size():
		base += Dressing.dress_link(self, rng, _lay.links[i], _lay.strips[i], loot_props, extra_blockers, base)
	if not loot_props.is_empty():
		var sub := Location.new()
		add_child(sub)
		sub.build_loot_island(self, loot_props)
		for eid in sub.entities:
			entities[eid] = sub.entities[eid]
	_blockers.append_array(extra_blockers)


## Helper island that only holds clickable finds (their positions are region coordinates).
func build_loot_island(host_loc: Location, props: Array) -> void:
	id = "links"
	host = host_loc
	data = {"props": props, "npcs": [], "cells": [1, 1]}
	interior = false
	_props()


var _dungeon_cells: Dictionary = {}
var _dungeon_def: Dictionary = {}
var _dungeon_armed := false
var _stairs_armed := false
var _dungeon_age := 0.0
var _dungeon_tile := 2.0


## A generated level (see Dungeon): the glb is the look, the json's walk rectangles are the movement. It runs on the region
## machinery (rectangle pathfinding, a camera that follows the player) with one member: the whole dungeon.
const DUNGEON_FILL := 1.4
const DUNGEON_LANTERN := 4.2


func build_dungeon(did: String, from_loc: String) -> void:
	var def := Dungeon.load_def(did)
	region = did
	id = did
	interior = bool(def.get("interior", true))
	_dungeon_def = def
	var rects: Array = Dungeon.floor_rects(def)
	_dungeon_cells = Dungeon.cells_of(def)
	_dungeon_tile = float(def.tile_size)
	_land_rects = rects
	_walk_rects = rects
	members = {}
	var u := Rect2(rects[0])
	for r in rects:
		u = u.merge(r)
	var sp := Dungeon.spawn_of(def, from_loc)
	var dflt_amb := {"color": "#5a463c", "energy": 0.9, "fog": "#0b0707"} if interior else {"color": "#4a5878", "energy": 0.8, "fog": "#10131c"}
	var dflt_cam := {"pos": [0, 6.4, 7.2], "look": [0, 1.0, 0], "fov": 55} if interior else {"pos": [0, 10.0, 11.5], "look": [0, 1.0, 0], "fov": 52}
	data = {"ambient": def.get("ambient", dflt_amb), "floor": "cobble", "interior": interior,
		"sky": str(def.get("sky", "night")), "wall": "stone_dark", "cells": [1, 1], "props": [], "npcs": [], "lights": Dungeon.lights_of(def),
		"camera": def.get("camera", dflt_cam), "spawn": [sp.x, sp.y], "spawns": {}, "moon": bool(def.get("moon", not interior))}
	bounds = u
	room_w = u.size.x
	room_d = u.size.y
	_environment()
	Dungeon.reset_materials()
	var dscene := Dungeon.load_scene(def)
	add_child(dscene)
	data.props = Dungeon.story_props(def)
	data.on_enter = Dungeon.story_on_enter(def)
	_props()
	_blockers.append_array(Dungeon.spawn_props(def, dscene))
	_lights()
	_dungeon_fill(def)
	_region_camera()
	_player(from_loc)
	player.clamp_fn = Callable(self, "_clamp_region")
	_dungeon_lantern()
	_weather()
	_portal_lights(def)


## Readability without lightmaps: one soft shadowless light per room (lit by the torches in spirit, so it is warm and low) ...
func _dungeon_fill(def: Dictionary) -> void:
	if not interior:
		return
	var warm := Color(str(data.ambient.color)).lerp(Color("#ffc890"), 0.55)
	for r in def.get("rooms", []):
		var rc: Array = r.rect
		var size := maxf(absf(float(rc[2]) - float(rc[0])), absf(float(rc[3]) - float(rc[1])))
		var o := OmniLight3D.new()
		o.position = Vector3(float(r.center[0]), 2.4, float(r.center[1]))
		o.light_color = warm
		o.light_energy = DUNGEON_FILL
		o.omni_range = size * 0.75 + 3.0
		o.shadow_enabled = false
		add_child(o)


## ... and a faint lantern that goes with the player, so a corridor is never black around them.
func _dungeon_lantern() -> void:
	if not interior or player == null:
		return
	var o := OmniLight3D.new()
	o.position = Vector3(0, 3.8, 1.4)
	o.light_color = Color("#ffd9a8")
	o.light_energy = DUNGEON_LANTERN
	o.omni_range = 11.0
	o.light_specular = 0.3
	o.shadow_enabled = false
	player.add_child(o)


## Warm light on the tile that leads back up, cold light on the one that leads on.
func _portal_lights(def: Dictionary) -> void:
	var lk: Dictionary = def.get("links", {})
	for key in ["entrance", "exit"]:
		var m: Variant = def.get(key)
		if not (m is Dictionary) or (key == "exit" and not lk.has("exit_to")) or (key == "entrance" and not def.has("entrance_from")):
			continue
		var o := OmniLight3D.new()
		o.position = Vector3(float(m.pos[0]), 0.9, float(m.pos[2]))
		o.light_color = Color("#8fb4ff") if key == "exit" else Color("#ffd49a")
		o.light_energy = 1.6
		o.omni_range = 4.5
		add_child(o)


## Walking onto the entrance tile again (after having walked away from it) leads back; the level's exit tile leads on.
func _dungeon_links(delta: float) -> void:
	if _dungeon_def.is_empty() or player == null:
		return
	_dungeon_age += delta
	var lk: Dictionary = _dungeon_def.get("links", {})
	var ef: Variant = _dungeon_def.get("entrance_from")
	var p := Vector2(player.position.x, player.position.z)
	var ent: Variant = _dungeon_def.get("entrance")
	if ent is Dictionary and ef is Dictionary:
		var e := Vector2(float(ent.pos[0]), float(ent.pos[2]))
		if p.distance_to(e) > 4.0:
			_dungeon_armed = true
		elif _dungeon_armed and p.distance_to(e) < 1.2 and _dungeon_age > 3.0:
			_dungeon_armed = false
			dungeon_exit.emit(str(ef.loc))
			return
	# stairs to the neighbouring floors (each floor is its own location): armed once the player has stepped away from every trigger
	var near_any := false
	for st in _dungeon_def.get("stairs_out", []):
		var tp := Vector2(float(st.trigger[0]), float(st.trigger[1]))
		if p.distance_to(tp) < 2.0:
			near_any = true
		if _stairs_armed and _dungeon_age > 1.5 and p.distance_to(tp) < 1.1:
			_stairs_armed = false
			dungeon_exit.emit(str(st.to))
			return
	if not near_any:
		_stairs_armed = true
	var ex: Variant = _dungeon_def.get("exit")
	if lk.has("exit_to") and ex is Dictionary and _dungeon_age > 3.0 and p.distance_to(Vector2(float(ex.pos[0]), float(ex.pos[2]))) < 1.2:
		dungeon_exit.emit(str(lk.exit_to))


func region_spawn(mid: String, from_loc: String) -> Vector3:
	var md: Dictionary = Game.loc_data(mid)
	var sp: Array = md.spawns.get(from_loc, md.spawn)
	var c: Vector2 = (members[mid] as Rect2).get_center()
	return Vector3(c.x + float(sp[0]), height_at(Vector2(c.x + float(sp[0]), c.y + float(sp[1]))), c.y + float(sp[1]))


## Route inside a merged region: through the connecting strips, never across the sea.
func go_to(p: Vector3) -> void:
	if region == "":
		var pts := _route(Vector2(player.position.x, player.position.z), Vector2(p.x, p.z))
		if pts.size() > 1:
			player.walk_path(pts)
		else:
			player.walk_to(p)
		return
	if not _dungeon_cells.is_empty():
		var route: Array = Dungeon.find_path(_dungeon_cells, _dungeon_tile, Vector2(player.position.x, player.position.z), Vector2(p.x, p.z))
		if route.is_empty():
			player.walk_to(_clamp_region(Vector3(p.x, 0, p.z)))
		else:
			var pts: Array = []
			for q in route:
				pts.append(Vector3((q as Vector2).x, 0, (q as Vector2).y))
			player.walk_path(pts)
		return
	var goal := _clamp_region(Vector3(p.x, 0, p.z))
	var here := Vector2(player.position.x, player.position.z)
	var to := Vector2(goal.x, goal.z)
	var n := _walk_rects.size()
	var r_from := -1
	var r_to := -1
	for i in n:
		var rc: Rect2 = _walk_rects[i]
		if r_from < 0 and rc.grow(0.5).has_point(here):
			r_from = i
		if r_to < 0 and rc.grow(0.5).has_point(to):
			r_to = i
	if r_from < 0 or r_to < 0 or r_from == r_to:
		player.walk_to(goal)
		return
	# Dijkstra over rectangles that touch each other
	var dist := {r_from: 0.0}
	var prev := {}
	var open := [r_from]
	while not open.is_empty():
		var best: int = open[0]
		for o in open:
			if dist[o] < dist[best]:
				best = o
		open.erase(best)
		if best == r_to:
			break
		for j in n:
			if j == best:
				continue
			var ra: Rect2 = _walk_rects[best]
			var rb: Rect2 = _walk_rects[j]
			var ov := ra.intersection(rb)
			if ov.size.x < 0.8 or ov.size.y < 0.8:
				continue
			var nd: float = dist[best] + ra.get_center().distance_to(rb.get_center())
			if not dist.has(j) or nd < dist[j]:
				dist[j] = nd
				prev[j] = best
				if not open.has(j):
					open.append(j)
	if not prev.has(r_to):
		player.walk_to(goal)
		return
	var chain := [r_to]
	while chain[0] != r_from:
		chain.push_front(prev[chain[0]])
	var pts: Array = []
	for k in chain.size() - 1:
		var inter: Rect2 = (_walk_rects[chain[k]] as Rect2).intersection(_walk_rects[chain[k + 1]])
		pts.append(Vector3(inter.get_center().x, 0, inter.get_center().y))
	pts.append(goal)
	player.walk_path(pts)


func _clamp_region(p: Vector3) -> Vector3:
	var best := Vector3(p.x, 0, p.z)
	var bd := 1e18
	for r in _walk_rects:
		var rc: Rect2 = r
		var q := Vector3(clampf(p.x, rc.position.x + 0.4, rc.end.x - 0.4), 0, clampf(p.z, rc.position.y + 0.4, rc.end.y - 0.4))
		var dd := (q.x - p.x) * (q.x - p.x) + (q.z - p.z) * (q.z - p.z)
		if dd < bd:
			bd = dd
			best = q
	return best


func _floor_patch(rc: Rect2, variant: String, hard: Array = ["north", "south", "west", "east"], y0 := 0.0) -> void:
	var spec: Dictionary = Assets.manifest.models["floor_4x4"].variants[variant]
	var mat: StandardMaterial3D = Assets.material_for(spec.stone).duplicate()
	mat.uv1_triplanar = true
	mat.uv1_world_triplanar = true
	mat.uv1_scale = Vector3.ONE * mat.uv1_scale.x
	mat.cull_mode = BaseMaterial3D.CULL_DISABLED
	var noise := FastNoiseLite.new()
	noise.seed = hash(variant + str(rc.position)) % 9999
	noise.frequency = 0.12
	# outline: straight along hard sides (sea wall, buildings), wobbling and chamfered along soft ones
	var pts := PackedVector2Array()
	var x0 := rc.position.x
	var x1 := rc.end.x
	var z0 := rc.position.y
	var z1 := rc.end.y
	var ch := 3.5
	var n := 14
	var inset := func(side: String, t: float, along: float) -> float:
		return 0.0 if side in hard else 0.9 + noise.get_noise_2d(along * 3.0, t * 40.0) * 1.1 + 0.3
	var ch_n := 0.0 if "north" in hard else ch
	var ch_s := 0.0 if "south" in hard else ch
	var ch_e := 0.0 if "east" in hard else ch
	var ch_w := 0.0 if "west" in hard else ch
	# north edge, west -> east
	for i in n + 1:
		var u := float(i) / n
		var x := lerpf(x0, x1, u)
		pts.append(Vector2(x, z0 + inset.call("north", u, x)))
	# east edge, north -> south
	for i in 1 + n:
		var u2 := float(i) / n
		var z := lerpf(z0, z1, u2)
		pts.append(Vector2(x1 - inset.call("east", u2, z), z))
	for i in n + 1:
		var u3 := float(i) / n
		var x2 := lerpf(x1, x0, u3)
		pts.append(Vector2(x2, z1 - inset.call("south", u3, x2)))
	for i in n + 1:
		var u4 := float(i) / n
		var z2 := lerpf(z1, z0, u4)
		pts.append(Vector2(x0 + inset.call("west", u4, z2), z2))
	# round the corners where both neighbouring sides are soft
	var cx := rc.get_center()
	var out := PackedVector2Array()
	for p in pts:
		var q := p
		var dxn := minf(absf(p.x - x1), absf(p.x - x0))
		var dzn := minf(absf(p.y - z1), absf(p.y - z0))
		var cr := 0.0
		if p.x > cx.x and p.y < cx.y:
			cr = minf(ch_e, ch_n)
		elif p.x > cx.x and p.y > cx.y:
			cr = minf(ch_e, ch_s)
		elif p.x < cx.x and p.y < cx.y:
			cr = minf(ch_w, ch_n)
		else:
			cr = minf(ch_w, ch_s)
		if cr > 0.0 and dxn < cr * 1.6 and dzn < cr * 1.6:
			var corner := Vector2(x1 if p.x > cx.x else x0, z1 if p.y > cx.y else z0)
			var to_c := (corner - p)
			var k := clampf((cr * 1.6 - maxf(dxn, dzn)) / (cr * 1.6), 0.0, 1.0)
			q = p + (cx - corner).normalized() * cr * 0.9 * k * k
		out.append(q)
	var tri := Geometry2D.triangulate_polygon(out)
	if tri.is_empty():
		tri = PackedInt32Array()
		var fan := Geometry2D.triangulate_polygon(PackedVector2Array([Vector2(x0, z0), Vector2(x1, z0), Vector2(x1, z1), Vector2(x0, z1)]))
		out = PackedVector2Array([Vector2(x0, z0), Vector2(x1, z0), Vector2(x1, z1), Vector2(x0, z1)])
		tri = fan
	var verts := PackedVector3Array()
	var norms := PackedVector3Array()
	for p in out:
		verts.append(Vector3(p.x, 0.005 + y0, p.y))
		norms.append(Vector3.UP)
	var arr := []
	arr.resize(Mesh.ARRAY_MAX)
	arr[Mesh.ARRAY_VERTEX] = verts
	arr[Mesh.ARRAY_NORMAL] = norms
	arr[Mesh.ARRAY_INDEX] = tri
	var mesh := ArrayMesh.new()
	mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)
	var mi := MeshInstance3D.new()
	mi.mesh = mesh
	mi.material_override = mat
	add_child(mi)


func _region_camera() -> void:
	var c: Dictionary = data.camera
	cam = Camera3D.new()
	cam.fov = float(c.fov)
	add_child(cam)
	var look := _v3(c.look)
	_cam_off = (_v3(c.pos) - look) * 0.9
	_zones = []
	cam.current = true
	var sp: Array = data.spawn
	_cam_look = Vector3(float(sp[0]), 1.0, float(sp[1]) - 1.4)
	_cam_base = _cam_look + _cam_off
	cam.position = _cam_base
	cam.look_at(_cam_look)


## A member of a merged region: its own props, people, buildings and lights, placed at `off`.
func build_island(host_loc: Location, mid: String, off: Vector3, overrides: Dictionary) -> void:
	id = mid
	host = host_loc
	data = Game.loc_data(mid).duplicate(true)
	for k in overrides:
		if k == "remove_props":
			data.props = data.props.filter(func(p: Dictionary) -> bool: return not (overrides.remove_props as Array).has(p.id))
		else:
			data[k] = overrides[k]
	data["no_backdrop"] = true
	interior = false
	Dressing.upgrade_buildings(data)
	var grow := _grow()
	room_w = float(data.cells[0]) * CELL + 2.0 * grow.x
	room_d = float(data.cells[1]) * CELL + 2.0 * grow.y
	position = off
	_ground_detail(room_w, room_d)
	_walls(room_w, room_d)
	_lights()
	_scatter(room_w, room_d)
	Dressing.add_loot(self)
	_props()
	_flames()
	Dressing.dress(self)


## Crossfades ambient light and fog to the mood of the place the player stands in (a region can mix times of day).
func apply_member_mood(mid: String, animate := true) -> void:
	if _env == null:
		return
	var a: Dictionary = Game.loc_data(mid).ambient
	var col := Color(str(a.color))
	var fog := Color(str(a.fog))
	var energy := float(a.energy) * 1.25
	if not animate:
		_env.ambient_light_color = col
		_env.ambient_light_energy = energy
		_env.fog_light_color = fog
		return
	var tw := create_tween().set_parallel(true)
	tw.tween_property(_env, "ambient_light_color", col, 1.5)
	tw.tween_property(_env, "ambient_light_energy", energy, 1.5)
	tw.tween_property(_env, "fog_light_color", fog, 1.5)


func _track_member() -> void:
	if player == null:
		return
	var p := Vector2(player.position.x, player.position.z)
	var here := ""
	for m in members:
		if (members[m] as Rect2).grow(1.0).has_point(p):
			here = m
			break
	if here != "" and here != _member:
		_member = here
		apply_member_mood(here)
		member_changed.emit(here)


## Open-air scenes are widened at runtime (props keep their authored positions; the extra ground is for exploring and loot).
## Scenes with walls are left alone; towns (buildings along the north edge) grow sideways only.
func _grow() -> Vector2:
	return Location.grow_for(id, data)


static func grow_for(loc_id: String, d: Dictionary) -> Vector2:
	if d.get("interior", true) or d.get("no_expand", false):
		return Vector2.ZERO
	var walls: Dictionary = d.get("walls", {})
	var cliff := loc_id.contains("cliff")
	if walls.is_empty():
		return Vector2(7.0, 5.0) if cliff else Vector2(5.0, 4.0)
	if walls.size() == 1 and walls.has("north") and Dressing.theme_of(loc_id, false) in ["dock", "street"]:
		return Vector2(5.0, 0.0)
	return Vector2.ZERO


func _quality() -> int:
	return {"low": 0, "medium": 1, "high": 2}.get(str(Game.meta.get("quality", "medium")), 1)


func _sky_name() -> String:
	if data.has("sky"):
		return str(data.sky)
	var fog := Color(str(data.ambient.fog))
	if id.contains("storm"):
		return "storm"
	if id.contains("snow") or id.contains("plain") or id.contains("mountain") or id.contains("hollow"):
		return "snow"
	if id.contains("sunset") or id.contains("dusk"):
		return "dusk"
	if data.has("moon"):
		return "night"
	return "day" if fog.v > 0.5 else "night"


func _environment() -> void:
	var a: Dictionary = data.ambient
	var env := Environment.new()
	var q := _quality()
	if interior:
		env.background_mode = Environment.BG_COLOR
		env.background_color = Color(str(a.fog))
	else:
		var path := "res://assets/sky/%s.png" % _sky_name()
		if ResourceLoader.exists(path):
			var sky := Sky.new()
			var mat := PanoramaSkyMaterial.new()
			mat.panorama = load(path)
			sky.sky_material = mat
			env.sky = sky
			env.background_mode = Environment.BG_SKY
			env.sky_rotation = Vector3(0, deg_to_rad(float(hash(id) % 360)), 0)
		else:
			env.background_mode = Environment.BG_COLOR
			env.background_color = Color(str(a.fog))
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(str(a.color))
	env.ambient_light_energy = float(a.energy) * ((2.7 if not _dungeon_def.is_empty() else 2.0) if interior else 1.25)
	env.fog_enabled = true
	env.fog_light_color = Color(str(a.fog))
	var sky_n := _sky_name()
	env.fog_density = 0.006 if interior else ({"day": 0.0065, "dusk": 0.012, "storm": 0.02, "snow": 0.014, "night": 0.016}.get(sky_n, 0.014))
	env.fog_sky_affect = 0.35
	env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	env.glow_enabled = q >= 1
	env.glow_intensity = 0.6
	env.glow_bloom = 0.08
	env.ssao_enabled = q >= 2
	env.adjustment_enabled = true
	env.adjustment_contrast = 1.07
	env.adjustment_saturation = 1.08
	var we := WorldEnvironment.new()
	we.environment = env
	_env = env
	add_child(we)
	get_viewport().msaa_3d = Viewport.MSAA_2X if q >= 2 else Viewport.MSAA_DISABLED
	if not interior:
		if not _is_watery():
			_far_ground(Color(str(a.fog)))
		_sun(sky_n, q)
		if _is_watery():
			_water(Color(str(a.fog)), sky_n)


## A huge plane under open-air scenes so the tile grid never ends in a visible edge.
func _far_ground(fog: Color) -> void:
	var pm := PlaneMesh.new()
	pm.size = Vector2(400, 400)
	var mi := MeshInstance3D.new()
	mi.mesh = pm
	var mat := StandardMaterial3D.new()
	var floor_name := str(data.floor)
	var spec: Dictionary = Assets.manifest.models["floor_4x4"].variants.get(floor_name, {})
	if spec.has("stone"):
		var tex: Dictionary = Assets.manifest.textures[spec.stone.tex]
		mat.albedo_texture = load("res://assets/" + str(tex.albedo))
		mat.uv1_scale = Vector3(100, 100, 1)
		mat.albedo_color = Color(str(spec.stone.tint)).darkened(0.35)
	else:
		mat.albedo_color = fog.darkened(0.4)
	if str(data.floor) in ["grass", "dirt", "snow"]:
		mat.albedo_texture = null
		var bf: Color = {"grass": Color("#3c5a2a"), "dirt": Color("#5a4a38"), "snow": Color("#d8dce8")}.get(str(data.floor), Color("#3c5a2a"))
		mat.albedo_color = Color(bf).lerp(fog, 0.25)
	mat.roughness = 1.0
	mi.material_override = mat
	mi.position = Vector3(0, -0.03, 0)
	add_child(mi)


func _floor(cells: Array, w: float, d: float) -> void:
	var variant: String = data.floor
	if not interior and (not _is_watery() or id.contains("cliff")) and variant in ["grass", "dirt", "snow"]:
		_terrain(w, d, variant)
		return
	## One seamless slab with a world-space triplanar material (no tile seams), extended past the room outdoors.
	var ext := 0.0
	if not interior:
		ext = 4.0 if _is_watery() and id.contains("cliff") else (0.0 if _is_watery() else 8.0)
	var spec: Dictionary = Assets.manifest.models["floor_4x4"].variants[variant]
	var mat: StandardMaterial3D = Assets.material_for(spec.stone).duplicate()
	mat.uv1_triplanar = true
	mat.uv1_world_triplanar = true
	mat.uv1_scale = Vector3.ONE * mat.uv1_scale.x
	var mi := MeshInstance3D.new()
	var bm := BoxMesh.new()
	bm.size = Vector3(w + 2.0 * ext, 0.2, d + 2.0 * ext)
	mi.mesh = bm
	mi.material_override = mat
	mi.position = Vector3(0, -0.1, 0)
	add_child(mi)


## Organic open-air ground: a rolling mesh (flat where the player walks) with a splat shader (meadow / bare earth / worn paths).
func _terrain(w: float, d: float, variant: String) -> void:
	var margin := 28.0 if region != "" else 15.0
	var step := 0.9
	var x0 := -w / 2.0 - margin
	var z0 := -d / 2.0 - margin
	var nx := int((w + 2.0 * margin) / step)
	var nz := int((d + 2.0 * margin) / step)
	var noise := FastNoiseLite.new()
	noise.seed = hash(id) % 10000
	noise.frequency = 0.045
	var verts := PackedVector3Array()
	var uvs := PackedVector2Array()
	var normals := PackedVector3Array()
	var idx := PackedInt32Array()
	var half := Vector2(w / 2.0, d / 2.0)
	var cliff_mode := id.contains("cliff")
	var heights := []
	for iz in nz + 1:
		var row := []
		for ix in nx + 1:
			var x := x0 + ix * step
			var z := z0 + iz * step
			var out := Vector2(maxf(absf(x) - half.x, 0.0), maxf(absf(z) - half.y, 0.0)).length()
			var amp := smoothstep(1.5, 9.0, out) * 1.6
			var h := noise.get_noise_2d(x, z) * amp
			if region != "":
				# land around the members and the strips between them, ragged coast, then sea
				var od := 1e9
				for r in _terrain_rects:
					var rc: Rect2 = r
					od = minf(od, Vector2(maxf(maxf(rc.position.x - x, x - rc.end.x), 0.0), maxf(maxf(rc.position.y - z, z - rc.end.y), 0.0)).length())
				var edge := 2.0 + noise.get_noise_2d(x * 2.1, z * 2.1) * 2.2
				h = height_at(Vector2(x, z)) + noise.get_noise_2d(x, z) * 0.18 * smoothstep(0.0, 4.0, od)
				h = lerpf(h, -4.6, smoothstep(edge, edge + 3.0, od))
			elif cliff_mode:
				# plateau that ends in a ragged cliff edge, then a sheer drop to the sea
				var edge := 3.5 + noise.get_noise_2d(x * 2.3, z * 2.3) * 3.0 + 1.5
				h = noise.get_noise_2d(x, z) * 0.25 * smoothstep(0.0, 3.0, out)
				h -= smoothstep(edge, edge + 2.2, out) * 14.5 + smoothstep(edge + 2.2, edge + 14.0, out) * 2.0
			row.append(h)
		heights.append(row)
	for iz in nz + 1:
		for ix in nx + 1:
			verts.append(Vector3(x0 + ix * step, heights[iz][ix], z0 + iz * step))
			uvs.append(Vector2(ix, iz))
			var hl: float = heights[iz][maxi(ix - 1, 0)]
			var hr: float = heights[iz][mini(ix + 1, nx)]
			var hu: float = heights[maxi(iz - 1, 0)][ix]
			var hd: float = heights[mini(iz + 1, nz)][ix]
			normals.append(Vector3(hl - hr, 2.0 * step, hu - hd).normalized())
	for iz in nz:
		for ix in nx:
			var i0 := iz * (nx + 1) + ix
			idx.append_array([i0, i0 + 1, i0 + nx + 1, i0 + 1, i0 + nx + 2, i0 + nx + 1])
	var arr := []
	arr.resize(Mesh.ARRAY_MAX)
	arr[Mesh.ARRAY_VERTEX] = verts
	arr[Mesh.ARRAY_NORMAL] = normals
	arr[Mesh.ARRAY_TEX_UV] = uvs
	arr[Mesh.ARRAY_INDEX] = idx
	var mesh := ArrayMesh.new()
	mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arr)
	var mat := ShaderMaterial.new()
	mat.shader = load("res://shaders/terrain.gdshader")
	var tex_g: Dictionary = Assets.manifest.textures["grass" if variant != "snow" else "snow"]
	var tex_d: Dictionary = Assets.manifest.textures["dirt"]
	mat.set_shader_parameter("grass_tex", load("res://assets/" + str(tex_g.albedo)))
	mat.set_shader_parameter("grass_nrm", load("res://assets/" + str(tex_g.normal)))
	mat.set_shader_parameter("dirt_tex", load("res://assets/" + str(tex_d.albedo)))
	var gtint := Color.WHITE
	var spec: Dictionary = Assets.manifest.models["floor_4x4"].variants.get(variant, {})
	if spec.has("stone"):
		gtint = Color(str(spec.stone.tint))
	var night := _sky_name() in ["night", "snow"] and data.has("moon")
	mat.set_shader_parameter("grass_tint", gtint)
	mat.set_shader_parameter("dirt_tint", Color(1, 1, 1) if variant != "dirt" else Color(1.1, 1.0, 0.9))
	mat.set_shader_parameter("grass_scale", 1.0 / float(tex_g.get("world", 4.0)))
	mat.set_shader_parameter("dirt_scale", 1.0 / float(tex_d.get("world", 3.0)))
	var base_far: Color = {"grass": Color("#3c5a2a"), "dirt": Color("#5a4a38"), "snow": Color("#d8dce8")}.get(variant, Color("#3c5a2a"))
	mat.set_shader_parameter("far_color", Color(base_far).lerp(Color(str(data.ambient.fog)), 0.25))
	mat.set_shader_parameter("rect", Vector4(-half.x, -half.y, half.x, half.y))
	mat.set_shader_parameter("bare", 0.75 if variant == "dirt" else (0.15 if variant == "grass" else 0.0))
	var segs := _path_segments()
	mat.set_shader_parameter("path_count", segs.size())
	mat.set_shader_parameter("shore", 1.0 if region != "" else 0.0)
	var packed := PackedVector4Array()
	for s in segs:
		packed.append(s)
	while packed.size() < 16:
		packed.append(Vector4.ZERO)
	mat.set_shader_parameter("path_a", packed)
	var mi := MeshInstance3D.new()
	mi.mesh = mesh
	mi.material_override = mat
	mi.position = Vector3(0, -0.01, 0)
	add_child(mi)


## Worn paths: from the arrival point to every exit / door in the scene, as segments (x1, z1, x2, z2).
func _path_segments() -> Array:
	if region != "":
		var rs: Array = []
		for m in members:
			var rc: Rect2 = members[m]
			var md: Dictionary = Game.loc_data(m)
			var sp: Array = md.spawn
			var c := rc.get_center()
			for p in md.get("props", []) + md.get("npcs", []):
				var it: Dictionary = p.get("interact", {})
				if (it.has("go") or it.has("talk")) and rs.size() < 43:
					rs.append(Vector4(c.x + float(sp[0]), c.y + float(sp[1]), c.x + float(p.pos[0]), c.y + float(p.pos[2])))
		for s in _land_rects.slice(members.size()):
			var sr: Rect2 = s
			rs.append(Vector4(sr.position.x, sr.get_center().y, sr.end.x, sr.get_center().y) if sr.size.x > sr.size.y else Vector4(sr.get_center().x, sr.position.y, sr.get_center().x, sr.end.y))
		return rs
	var pts: Array = []
	var sp: Array = data.spawn
	var start := Vector2(float(sp[0]), float(sp[1]))
	for p in data.get("props", []) + data.get("npcs", []):
		var it: Dictionary = p.get("interact", {})
		if it.has("go") or it.has("talk"):
			pts.append(Vector2(float(p.pos[0]), float(p.pos[2])))
	var segs: Array = []
	var hub := Vector2(0, 1.0)
	segs.append(Vector4(start.x, start.y, hub.x, hub.y))
	for p in pts:
		if segs.size() >= 15:
			break
		segs.append(Vector4(hub.x, hub.y, p.x, p.y))
	return segs


func _walls(w: float, d: float) -> void:
	var walls: Dictionary = data.get("walls", {})
	var variant: String = data.wall
	var t := 0.2
	if not interior and Dressing.is_ship(id):         # the ship's own hull and bulwarks replace the walls
		return
	var town := not interior and Dressing.theme_of(id, false) in ["dock", "street"]
	for side in walls:
		if town and side == "north":
			continue
		var arr: Array = walls[side]
		for i in arr.size():
			var m := Assets.instantiate(str(arr[i]), variant)
			match side:
				"north":
					m.position = Vector3(-w / 2 + CELL / 2 + i * CELL, 0, -d / 2 - t)
				"west":
					m.position = Vector3(-w / 2 - t, 0, -d / 2 + CELL / 2 + i * CELL)
					m.rotation_degrees.y = 90
				"east":
					m.position = Vector3(w / 2 + t, 0, -d / 2 + CELL / 2 + i * CELL)
					m.rotation_degrees.y = -90
				"south":
					m.position = Vector3(-w / 2 + CELL / 2 + i * CELL, 0, d / 2 + t)
					m.rotation_degrees.y = 180
			m.set_meta("wall_side", side)
			add_child(m)


func _lights() -> void:
	var first := true
	for l in data.get("lights", []):
		var o := OmniLight3D.new()
		o.position = _v3(l.pos)
		o.light_color = Color(str(l.color))
		o.light_energy = float(l.energy) * float(data.get("light_scale", 1.0))
		o.omni_range = float(l.range)
		o.shadow_enabled = first
		first = false
		add_child(o)
		if Color(str(l.color)).r > 0.9 and Color(str(l.color)).b < 0.6:
			_flickers.append([o, o.light_energy, randf() * 10.0])


func _moon() -> void:
	var m := Assets.instantiate("moon", "default")
	m.position = _v3(data.moon.pos)
	m.scale = Vector3.ONE * 1.6
	add_child(m)
	var sun := DirectionalLight3D.new()
	sun.light_color = Color("#9fb4ff")
	sun.light_energy = 0.7
	sun.shadow_enabled = true
	add_child(sun)
	sun.look_at_from_position(m.position, Vector3.ZERO)


func _scatter(w: float, d: float) -> void:
	for key in ["scatter", "scatter2", "scatter3"]:
		if not data.has(key):
			continue
		var s: Dictionary = data[key]
		var rng := RandomNumberGenerator.new()
		rng.seed = int(s.get("seed", 1))
		var placed := 0
		var tries := 0
		while placed < int(s.count) and tries < 2000:
			tries += 1
			var p := Vector3(rng.randf_range(-w / 2 - 12, w / 2 + 12), 0, rng.randf_range(-d / 2 - 12, d / 2 - 0.5))
			if Rect2(-w / 2 - 1.0, -d / 2 - 1.0, w + 2.0, d + 2.0).has_point(Vector2(p.x, p.z)):
				continue
			var skip := false
			if host != null:
				for lr in host._land_rects:
					if (lr as Rect2).grow(2.5).has_point(Vector2(p.x + position.x, p.z + position.z)):
						skip = true
						break
			for r in s.get("avoid", []):
				if p.x > r[0] and p.x < r[2] and p.z > r[1] and p.z < r[3]:
					skip = true
			if skip:
				continue
			var m := Assets.instantiate(str(s.asset), str(s.variant))
			m.position = p
			m.rotation.y = rng.randf() * TAU
			m.scale = Vector3.ONE * rng.randf_range(0.75, 1.35)
			add_child(m)
			placed += 1


func _props() -> void:
	var blockers: Array = []
	for p in data.get("props", []):
		var eid: String = p.id
		var it: Dictionary = p.get("interact", {})
		if Game.flags.get("taken:" + eid, false) and not it.get("give_once", false):
			continue
		var node := Actor.new()
		node.set_meta("cond", str(p.get("if", "")))
		node.position = _v3(p.pos)
		node.rotation_degrees.y = float(p.get("rot", 0))
		add_child(node)
		node.setup(str(p.asset), str(p.variant), float(p.get("scale", 1.0)))
		node.set_process(false)
		node.rotation_degrees.y = float(p.get("rot", 0))
		if p.has("interact") and p.get("name", "") != "":
			_make_body(node, eid, false, 2.2 if str(p.asset).contains("schooner") else 0.0)
			entities[eid] = {"node": node, "data": p, "npc": false}
		if p.get("pos", [0, 0, 0])[1] < 0.2 and float(p.get("radius", 0)) > 0.25:
			blockers.append({"pos": Vector2(p.pos[0], p.pos[2]), "r": float(p.radius) * 0.8})
	for n in data.get("npcs", []):
		var a := Actor.new()
		a.set_meta("cond", str(n.get("if", "")))
		a.position = _v3(n.pos)
		add_child(a)
		a.setup(str(n.asset), str(n.variant), float(n.get("scale", 1.0)))
		a.face_yaw_deg(float(n.get("rot", 0)))
		_make_body(a, str(n.id), true)
		entities[n.id] = {"node": a, "data": n, "npc": true}
		blockers.append({"pos": Vector2(n.pos[0], n.pos[2]), "r": 0.4})
	_blockers = blockers
	_cond_nodes = get_children().filter(func(n: Node) -> bool: return n.has_meta("cond"))
	Game.state_changed.connect(_apply_conditions)
	Game.speaking.connect(_on_speaking)
	if host == null and not Game.pie_chosen.is_connected(_on_pie_chosen):
		Game.pie_chosen.connect(_on_pie_chosen)

	_apply_conditions()


var _blockers: Array = []
var _cond_nodes: Array = []
var _fliers: Array = []
var _zones: Array = []
var room_w := 0.0            # playable size including the automatic expansion of open scenes
var room_d := 0.0
var _zone := ""
var _manual_view := ""      # set by the V key: stay on a chosen camera until cycled back to "auto"


## The NPC whose name matches the dialogue speaker gestures and faces the player.
func _on_speaking(who: String) -> void:
	var w := who.to_lower()
	for eid in entities:
		var e: Dictionary = entities[eid]
		if not e.npc:
			continue
		var nm := str(e.data.get("name", "")).to_lower()
		var on := w != "" and nm != "" and (nm == w or nm.contains(w) or w.contains(nm))
		(e.node as Actor).talking = on
		if on and player != null:
			(e.node as Actor).face_point(player.position)


## Shows/hides props and NPCs whose "if" condition changed (and switches off their click colliders).
func _apply_conditions() -> void:
	for n in _cond_nodes:
		if not is_instance_valid(n):
			continue
		var on := Game.check(str(n.get_meta("cond")))
		n.visible = on
		for b in n.get_children():
			if b is StaticBody3D:
				(b as StaticBody3D).collision_layer = 1 if on else 0


## `max_height` > 0 cuts a big model's click box down to its base (a ship: the hull is clickable, its rigging is not, so it does not hide people behind it).
func _make_body(node: Node3D, eid: String, tall: bool = false, max_height: float = 0.0) -> void:
	var box := AABB()
	var first := true
	if node is Actor and (node as Actor).kind == "skinned":
		# skinned meshes report a useless AABB: use a standing-person box
		var h := (node as Actor).skin_height
		box = AABB(Vector3(-0.38, 0.0, -0.32), Vector3(0.76, h, 0.64))
		first = false
	for m in Assets._meshes(node) if not (node is Actor and (node as Actor).kind == "skinned") else []:
		var mi: MeshInstance3D = m
		var bb := mi.get_aabb()
		var t := node.global_transform.affine_inverse() * mi.global_transform
		var tb := t * bb
		box = tb if first else box.merge(tb)
		first = false
	if first:
		return
	if max_height > 0.0 and box.size.y > max_height:
		box.size.y = max_height
	var body := StaticBody3D.new()
	var shape := CollisionShape3D.new()
	var bs := BoxShape3D.new()
	bs.size = box.size + Vector3(0.1, 0.1, 0.1)
	shape.shape = bs
	shape.position = box.get_center()
	body.add_child(shape)
	body.set_meta("eid", eid)
	if max_height > 0.0:
		body.set_meta("weak", true)
	node.add_child(body)


func _camera() -> void:
	var c: Dictionary = data.camera
	cam = Camera3D.new()
	cam.fov = float(c.fov)
	add_child(cam)
	var look := _v3(c.look)
	var pos0 := look + (_v3(c.pos) - look) * 0.88            # a little closer than authored: characters read better
	_zones = [{"id": "main", "rect": Rect2(-1000, -1000, 2000, 2000), "pos": pos0, "look": look, "fov": float(c.fov)}]
	var w: float = room_w
	var authored: Array = data.get("cameras", [])
	for z in authored:
		var r: Array = z.rect
		_zones.push_front({"id": str(z.id), "rect": Rect2(r[0], r[1], r[2] - r[0], r[3] - r[1]), "pos": _v3(z.pos), "look": _v3(z.look), "fov": float(z.get("fov", c.fov))})
	if authored.is_empty() and w >= 11.0 and data.get("auto_cameras", true):
		# automatic side views: when the character walks to the left/right part of a wide scene the camera cuts to a diagonal angle
		var ex := w * 0.5 + 40.0
		_zones.push_front({"id": "left", "rect": Rect2(-ex, -1000, ex - w * 0.17, 2000), "pos": Vector3(w * 0.27, pos0.y * 0.96, pos0.z * 0.93),
			"look": Vector3(-w * 0.29, look.y, look.z), "fov": float(c.fov)})
		_zones.push_front({"id": "right", "rect": Rect2(w * 0.17, -1000, ex - w * 0.17, 2000), "pos": Vector3(-w * 0.27, pos0.y * 0.96, pos0.z * 0.93),
			"look": Vector3(w * 0.29, look.y, look.z), "fov": float(c.fov)})
	cam.current = true
	_zone = ""
	_cut_to("main", false)


func _cut_to(zone_id: String, flash: bool = true) -> void:
	for z in _zones:
		if z.id == zone_id:
			cam.fov = float(z.fov)
			cam.position = z.pos
			cam.look_at(z.look)
			_cam_base = z.pos
			_cam_look = z.look
			_zone = zone_id
			_update_walls()
			if flash:
				Game.camera_cut.emit()
			return


func _update_zone() -> void:
	if player == null or _zones.size() < 2 or _manual_view != "":
		return
	var p := Vector2(player.position.x, player.position.z)
	var target := "main"
	for z in _zones:
		if z.id != "main" and (z.rect as Rect2).has_point(p):
			target = str(z.id)
			break
	if _zone != "main" and target == "main":
		# hysteresis: stay in the current side view until clearly out of it
		for z in _zones:
			if z.id == _zone and (z.rect as Rect2).grow(1.2).has_point(p):
				target = _zone
	if target != _zone:
		_cut_to(target)


## Hide walls that stand between the camera and the room (authored cameras may sit outside a wall).
func _update_walls() -> void:
	var w: float = room_w
	var d: float = room_d
	for n in get_children():
		if n.has_meta("wall_side"):
			var side := str(n.get_meta("wall_side"))
			var hide: bool = (side == "south" and cam.position.z > d / 2.0) or (side == "north" and cam.position.z < -d / 2.0) \
				or (side == "west" and cam.position.x < -w / 2.0) or (side == "east" and cam.position.x > w / 2.0)
			n.visible = not hide


func _player(from_loc: String) -> void:
	player = Actor.new()
	var sp: Array = data.spawns.get(from_loc, data.spawn)
	player.position = Vector3(sp[0], height_at(Vector2(sp[0], sp[1])), sp[1])
	if region != "":
		player.height_fn = Callable(self, "height_at")
	player.bounds = bounds
	player.blockers = _blockers
	add_child(player)
	var pm: Dictionary = Game.systems.party[Game.protagonist]
	player.setup(str(pm.get("model", "human_harker")), str(pm.get("variant", "harker")))
	player.face_yaw_deg(0)
	player.arrived.connect(_on_arrived)
	player.step.connect(func() -> void: Audio.sfx("step", 1.0, -2.0))


func _v3(a: Array) -> Vector3:
	return Vector3(a[0], a[1], a[2])


# ------------------------------------------------------------------ input --
func _unhandled_input(ev: InputEvent) -> void:
	if modal or host != null:
		return
	if ev is InputEventKey and ev.pressed and ev.keycode == KEY_V and _zones.size() > 1:
		var ids: Array = [""]
		for z in _zones:
			ids.append(str(z.id))
		var next: String = ids[(ids.find(_manual_view) + 1) % ids.size()]
		_manual_view = next
		if next == "":
			Game.message.emit("Camera: automatic (V to change)")
			_zone = ""
			_update_zone()
		else:
			Game.message.emit("Camera: %s view (V to change)" % next)
			_cut_to(next)
		return
	if ev is InputEventMouseMotion:
		_update_hover(ev.position)
	elif ev is InputEventMouseButton and ev.pressed:
		var eid := _pick(ev.position)
		if ev.button_index == MOUSE_BUTTON_LEFT:
			if eid != "":
				if Game.selected_item == "" and Game.meta.get("pie_menu", true) and host == null and entities.has(eid):
					_open_pie(eid, ev.position)
				else:
					_approach(eid, "use" if Game.selected_item != "" else "primary")
			else:
				var fp := _floor_point(ev.position)
				if fp != Vector3.INF:
					pending = {}
					go_to(fp)
		elif ev.button_index == MOUSE_BUTTON_RIGHT:
			if Game.selected_item != "":
				Game.selected_item = ""
				Game.inventory_changed.emit()
			elif eid != "":
				_approach(eid, "look")
			elif Game.meta.get("pie_menu", true) and host == null:
				open_ground_pie(ev.position)


var _pie_pos := Vector2.ZERO


func _open_pie(eid: String, pos: Vector2) -> void:
	_pie_pos = pos
	var it: Dictionary = entities[eid].data.get("interact", {})
	var verbs: Array = [{"id": "look", "label": "Look"}]
	if it.has("fight") and not Game.flags.get("won:" + str(it.fight), false):
		verbs.append({"id": "attack", "label": "Attack"})
	if it.has("talk"):
		verbs.append({"id": "talk", "label": "Talk"})
	if it.has("go") or it.has("end_text"):
		verbs.append({"id": "go", "label": "Go"})
	if it.has("take"):
		verbs.append({"id": "take", "label": "Take"})
	if it.has("set"):
		verbs.append({"id": "use", "label": "Use"})
	if not Game.inventory.is_empty():
		verbs.append({"id": "item", "label": "Use item on it"})
	if _can_map():
		verbs.append({"id": "map", "label": "Map"})
	if verbs.size() == 1:
		_approach(eid, "look")                     # nothing to do with it but look: skip the menu
		return
	Game.pie_requested.emit(eid, pos, str(entities[eid].data.get("name", "")), verbs)


func _can_map() -> bool:
	return not interior and TravelMap.has_map(Game.current)


## Right click on empty ground outdoors: a small menu with just the map.
func open_ground_pie(pos: Vector2) -> void:
	if _can_map():
		_pie_pos = pos
		Game.pie_requested.emit("", pos, "Where to?", [{"id": "map", "label": "Map"}])


func _on_pie_chosen(eid: String, verb: String) -> void:
	if verb == "map":
		Game.map_requested.emit()
		return
	if not entities.has(eid):
		return
	if verb == "look":
		_approach(eid, "look")
	elif verb == "item":
		var items: Array = []
		for iid in Game.sorted_inventory():
			if Game.item_filter == "" or Game.item_category(str(iid)) == Game.item_filter:
				items.append({"id": "item:" + str(iid), "label": Game.item_name(str(iid)), "color": Game.CAT_COLOR[Game.item_category(str(iid))]})
		var ttl := "Use on " + str(entities[eid].data.get("name", ""))
		if Game.item_filter != "":
			ttl += "  [%s]" % Game.CAT_SHORT[Game.item_filter]
		Game.pie_requested.emit(eid, _pie_pos, ttl, items)
	elif verb.begins_with("item:"):
		Game.selected_item = verb.substr(5)
		Game.inventory_changed.emit()
		_approach(eid, "use")
	else:
		_approach(eid, "primary")


func _ray(pos: Vector2) -> Dictionary:
	var from := cam.project_ray_origin(pos)
	var to := from + cam.project_ray_normal(pos) * 200.0
	var q := PhysicsRayQueryParameters3D.create(from, to)
	return get_world_3d().direct_space_state.intersect_ray(q)


func _pick(pos: Vector2) -> String:
	var r := _ray(pos)
	if r.is_empty():
		return ""
	var c: Object = r.collider
	var first := str(c.get_meta("eid")) if c.has_meta("eid") else ""
	if not c.has_meta("weak"):
		return first
	# a "weak" click box (a ship's hull) gives way to anything clickable behind it: people and props standing beyond the ship
	var from := cam.project_ray_origin(pos)
	var to := from + cam.project_ray_normal(pos) * 200.0
	var skip: Array[RID] = []
	for _i in 4:
		skip.append((c as CollisionObject3D).get_rid())
		var q := PhysicsRayQueryParameters3D.create(from, to)
		q.exclude = skip
		var r2 := get_world_3d().direct_space_state.intersect_ray(q)
		if r2.is_empty():
			return first
		c = r2.collider
		if not c.has_meta("weak"):
			return str(c.get_meta("eid")) if c.has_meta("eid") else first
	return first


func _floor_point(pos: Vector2) -> Vector3:
	var o := cam.project_ray_origin(pos)
	var n := cam.project_ray_normal(pos)
	var hit: Variant = Plane(Vector3.UP, 0).intersects_ray(o, n)
	if hit != null and region != "" and not _lay.is_empty():
		for _i in 3:                                  # ground is not flat in a region: re-aim at the height under the hit
			var h2: Variant = Plane(Vector3.UP, height_at(Vector2(hit.x, hit.z))).intersects_ray(o, n)
			if h2 == null:
				break
			hit = h2
	return hit if hit != null else Vector3.INF


func _update_hover(pos: Vector2) -> void:
	var eid := _pick(pos)
	var label := ""
	if eid != "":
		var nm: String = entities[eid].data.get("name", "")
		if Game.selected_item != "":
			label = "Use %s with %s" % [Game.item_def(Game.selected_item).name, nm]
		else:
			label = nm
	elif Game.selected_item != "":
		label = "Use %s with ..." % Game.item_def(Game.selected_item).name
	if label != _hover:
		_hover = label
		hover_changed.emit(label)


## Classic scenes: route around the blockers (tables, barrels, trees) by a visibility graph over points on circles around them,
## so a click behind a table walks around it instead of pushing against it. Returns waypoints (last one = goal).
func _route(a: Vector2, b: Vector2) -> Array:
	const PAD := 0.3
	var near: Array = []
	for bl in _blockers:
		var c: Vector2 = bl.pos
		var r: float = float(bl.r)
		if r < 0.15:
			continue
		var cl := Geometry2D.get_closest_point_to_segment(c, a, b)
		if cl.distance_to(c) < r + 4.0:
			near.append({"c": c, "r": r + PAD})
	var direct_ok := func(u: Vector2, v: Vector2) -> bool:
		for n in near:
			if (n.c as Vector2).distance_to(u) < float(n.r) - 0.02:
				continue                                  # starting inside an inflated circle (just pushed out): ignore it
			if Geometry2D.get_closest_point_to_segment(n.c, u, v).distance_to(n.c) < float(n.r) - 0.02:
				return false
		return true
	if near.is_empty() or direct_ok.call(a, b):
		return [Vector3(b.x, 0, b.y)]
	var nodes: Array = [a, b]
	for n in near:
		for k in 10:
			var q: Vector2 = n.c + Vector2.from_angle(TAU * k / 10.0) * (float(n.r) + 0.12)
			if not bounds.grow(-0.3).has_point(q):
				continue
			var inside := false
			for m in near:
				if (m.c as Vector2).distance_to(q) < float(m.r) - 0.05:
					inside = true
					break
			if not inside:
				nodes.append(q)
	var dist: Array = []
	var prev: Array = []
	var done: Array = []
	for i in nodes.size():
		dist.append(INF)
		prev.append(-1)
		done.append(false)
	dist[0] = 0.0
	for _i in nodes.size():
		var u := -1
		var best := INF
		for i in nodes.size():
			if not done[i] and dist[i] < best:
				best = dist[i]
				u = i
		if u < 0 or u == 1:
			break
		done[u] = true
		for v in nodes.size():
			if done[v]:
				continue
			var d: float = (nodes[u] as Vector2).distance_to(nodes[v])
			if dist[u] + d < dist[v] and direct_ok.call(nodes[u], nodes[v]):
				dist[v] = dist[u] + d
				prev[v] = u
	if prev[1] < 0:
		return [Vector3(b.x, 0, b.y)]
	var path: Array = []
	var cur := 1
	while cur != 0 and cur >= 0:
		path.push_front(Vector3((nodes[cur] as Vector2).x, 0, (nodes[cur] as Vector2).y))
		cur = prev[cur]
	return path


## Ground level of a region at a point of region space (flat everywhere else).
func height_at(p: Vector2) -> float:
	return Regions.height_at(_lay, p) if region != "" and not _lay.is_empty() and _lay.has("links") else 0.0


func _flat_dist(a: Vector3, b: Vector3) -> float:
	return Vector2(a.x - b.x, a.z - b.z).length()


## Where to stand and how close counts as "there" for an entity. Things that sit on another blocker (a bottle on a table) can
## only be reached from outside that blocker, so the stand-off distance grows with it.
func reach_info(eid: String) -> Dictionary:
	var e: Dictionary = entities[eid]
	var c: Vector3 = (e.node as Node3D).global_position
	var r := float(e.data.get("radius", 0.5))
	var stand := r + 0.9
	var reach := r + 1.25
	var cp := Vector2(c.x, c.z)
	for b in _blockers:
		if (b.pos as Vector2).distance_to(cp) < float(b.r) + 0.05:
			stand = maxf(stand, float(b.r) + 0.6)
			reach = maxf(reach, float(b.r) + 0.9)
	return {"stand": stand, "reach": reach}


func _approach(eid: String, verb: String) -> void:
	var e: Dictionary = entities[eid]
	var node: Node3D = e.node
	if verb == "look":
		player.face_point(node.global_position)
		_look(eid)
		return
	var ri := reach_info(eid)
	var dir := player.position - node.global_position
	dir.y = 0
	dir = dir.normalized() if dir.length() > 0.01 else Vector3(0, 0, 1)
	pending = {"eid": eid, "verb": verb}
	if _flat_dist(player.position, node.global_position) < float(ri.reach) + 0.05:
		_on_arrived()
	else:
		go_to(node.global_position + dir * float(ri.stand))


func _process(delta: float) -> void:
	_t += delta
	for f in _fliers:
		var fa: Actor = f.actor
		var ft: float = _t * float(f.speed) + float(f.phase)
		var c: Vector3 = f.center
		fa.position = c + Vector3(cos(ft) * float(f.r), float(f.h) + sin(ft * 1.7) * 0.4, sin(ft) * float(f.r) * 0.7)
		var vel := Vector3(-sin(ft), 0, cos(ft) * 0.7) * signf(float(f.speed))
		fa._yaw = atan2(vel.x, vel.z)
		fa.rotation.z = -0.25 * signf(float(f.speed))
	if host != null:
		return
	_update_zone()
	_edge_exit(delta)
	if region != "" and player != null and cam != null and not debug_free_cam:
		_track_member()
		if id.begins_with("dungeon_"):
			Dungeon.track(player.position, cam.position, delta)
			_dungeon_links(delta)
		var tgt := player.position + Vector3(0, 1.0, -1.4)
		_cam_look = _cam_look.lerp(tgt, 1.0 - exp(-delta * 4.0))
		_cam_base = _cam_look + _cam_off
		cam.position = _cam_base
		cam.look_at(_cam_look)
	elif cam != null and _quality() >= 1 and not debug_free_cam:
		cam.position = _cam_base + Vector3(sin(_t * 0.17) * 0.16, sin(_t * 0.11) * 0.06, sin(_t * 0.13) * 0.1)
		cam.look_at(_cam_look)
	for f in _flickers:
		var o: OmniLight3D = f[0]
		o.light_energy = f[1] * (0.88 + 0.12 * sin(_t * 9.0 + f[2]) + 0.06 * sin(_t * 23.0 + f[2] * 2.0))
	if not pending.is_empty() and player != null:
		var e: Dictionary = entities[pending.eid]
		var ri := reach_info(pending.eid)
		var fd := _flat_dist(player.position, e.node.global_position)
		if fd < float(ri.reach):
			player.stop()
			_stuck_t = 0.0
			_on_arrived()
		elif player.moving:
			# hemmed in (a crowd of NPCs, a cluttered corner): give up walking after a moment and act from where we stand
			if player.position.distance_to(_stuck_pos) > 0.25:
				_stuck_pos = player.position
				_stuck_t = 0.0
			_stuck_t += delta
			if _stuck_t > 1.6:
				_stuck_t = 0.0
				player.stop()
				if fd < float(ri.reach) + 1.8:
					_on_arrived()
				else:
					pending = {}
					Game.message.emit("I cannot get there from here.")
		else:
			_stuck_t = 0.0


var _edge_wait := 1.0
var _lay: Dictionary = {}
var _terrain_rects: Array = []     # land rects plus building footprints (terrain only; walking uses _land_rects)
var debug_free_cam := false    # tests / screenshots: leave the camera where it was put
var _stuck_t := 0.0
var _stuck_pos := Vector3.ZERO
var dry_run := false         # tests: arriving does not trigger the entity's action


## Walking into an open edge of an outdoor scene opens the overworld map.
func _edge_exit(delta: float) -> void:
	_edge_wait -= delta
	if interior or region != "" or host != null or not Game.autosave or player == null or player.moving or _edge_wait > 0.0 or not pending.is_empty():
		return
	var walls: Dictionary = data.get("walls", {})
	var p := player.position
	var side := ""
	if p.x <= bounds.position.x + 0.2: side = "west"
	elif p.x >= bounds.end.x - 0.2: side = "east"
	elif p.z <= bounds.position.y + 0.2: side = "north"
	elif p.z >= bounds.end.y - 0.2: side = "south"
	if side == "" or walls.has(side):
		return
	_edge_wait = 3.0
	Game.map_requested.emit()


func _on_arrived() -> void:
	if pending.is_empty():
		return
	var p := pending
	pending = {}
	if dry_run:
		return
	var e: Dictionary = entities[p.eid]
	player.face_point(e.node.global_position)
	if p.verb == "use":
		_use(p.eid)
	else:
		_primary(p.eid)


## Removes every entity whose interact.fight matches (they were beaten or fled).
func clear_fight(enc_id: String) -> void:
	for eid in entities.keys():
		var e: Dictionary = entities[eid]
		if e.data.get("interact", {}).get("fight", "") == enc_id:
			e.node.queue_free()
			entities.erase(eid)


func _look(eid: String) -> void:
	var it: Dictionary = entities[eid].data.get("interact", {})
	Game.message.emit(str(it.get("look", "Nothing special.")))


func _primary(eid: String) -> void:
	var e: Dictionary = entities[eid]
	var it: Dictionary = e.data.get("interact", {})
	if it.has("fight") and not Game.flags.get("won:" + str(it.fight), false):
		e.node.face_point(player.position)
		Game.fight_requested.emit(str(it.fight), eid)
	elif it.has("talk"):
		e.node.face_point(player.position)
		Game.dialogue_requested.emit(str(it.talk))
	elif it.has("end_text"):
		if Game.check(str(it.get("go_cond", ""))):
			Game.ending.emit(str(it.end_text))
		else:
			Game.message.emit(str(it.get("go_fail", "")))
	elif it.has("go"):
		if Game.check(str(it.get("go_cond", ""))):
			Game.goto_requested.emit(str(it.go), id)
		elif it.has("set") and not Game.flags.get(str(it.set), false):
			Game.set_flag(str(it.set))
			Game.message.emit(str(it.get("set_text", "")))
		else:
			Audio.sfx("door_locked")
			Game.message.emit(str(it.get("go_fail", "It will not open.")))
	elif it.has("do"):
		# a one-time scripted reaction (journal, reward, a few lines); afterwards the prop just describes itself
		var did_key := "did:" + eid
		if not Game.flags.get(did_key, false):
			Game.set_flag(did_key)
			Game.run(it.do)
		else:
			_look(eid)
	elif it.has("take"):
		_take(eid)
	elif it.has("set"):
		if not Game.flags.get(str(it.set), false):
			Game.set_flag(str(it.set))
			Game.message.emit(str(it.get("set_text", "")))
		else:
			_look(eid)
	else:
		_look(eid)


func _take(eid: String) -> void:
	var e: Dictionary = entities[eid]
	var it: Dictionary = e.data.interact
	var key := "taken:" + eid
	if Game.flags.get(key, false):
		Game.message.emit("There is nothing more to find here.")
		return
	Game.set_flag(key)
	player.play_once("reach", 0.7)
	Game.give(str(it.take))
	Audio.sfx("pickup")
	Game.message.emit(str(it.get("take_text", "Taken.")))
	if not it.get("give_once", false):
		e.node.queue_free()
		entities.erase(eid)


func _use(eid: String) -> void:
	var it: Dictionary = entities[eid].data.get("interact", {})
	var item := Game.selected_item
	var uses: Dictionary = it.get("use_item", {})
	if uses.has(item):
		player.play_once("reach", 0.7)
		Game.run(uses[item])
		Game.selected_item = ""
		Game.inventory_changed.emit()
	else:
		Game.message.emit(str(it.get("use_fail", "That will not work here.")))


# ------------------------------------------------------------------ atmosphere
func _weather() -> void:
	var q := _quality()
	if q == 0:
		return
	var kind := str(data.get("weather", ""))
	if kind == "":
		if id.contains("storm") or id.contains("deck") and str(data.ambient.fog) == "#20262c":
			kind = "rain"
		elif _sky_name() == "snow":
			kind = "snow"
		elif interior:
			kind = "dust"
		elif str(data.ambient.fog).begins_with("#0") and not id.contains("street"):
			kind = "mist"
	if kind == "":
		return
	var p := CPUParticles3D.new()
	p.emitting = true
	p.local_coords = false
	p.visibility_aabb = AABB(Vector3(-20, -2, -20), Vector3(40, 20, 40))
	var mesh := QuadMesh.new()
	var mat := StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
	mat.vertex_color_use_as_albedo = true
	var w: float = room_w
	var d: float = room_d
	match kind:
		"rain":
			mesh.size = Vector2(0.02, 0.5)
			mat.albedo_color = Color(0.7, 0.75, 0.85, 0.35)
			p.amount = 600 if q >= 2 else 300
			p.lifetime = 0.8
			p.direction = Vector3(0.25, -1, 0)
			p.initial_velocity_min = 14.0
			p.initial_velocity_max = 17.0
			p.gravity = Vector3(0, -6, 0)
			p.emission_shape = CPUParticles3D.EMISSION_SHAPE_BOX
			p.emission_box_extents = Vector3(w * 0.9, 0.2, d * 0.9)
			p.position = Vector3(0, 9, 0)
		"snow":
			mesh.size = Vector2(0.06, 0.06)
			mat.albedo_color = Color(1, 1, 1, 0.8)
			p.amount = 500 if q >= 2 else 250
			p.lifetime = 6.0
			p.direction = Vector3(0.2, -1, 0.1)
			p.initial_velocity_min = 0.8
			p.initial_velocity_max = 1.6
			p.gravity = Vector3(0.3, -0.4, 0)
			p.emission_shape = CPUParticles3D.EMISSION_SHAPE_BOX
			p.emission_box_extents = Vector3(w * 0.9, 0.2, d * 0.9)
			p.position = Vector3(0, 8, 0)
		"dust":
			mesh.size = Vector2(0.025, 0.025)
			mat.albedo_color = Color(1.0, 0.85, 0.6, 0.35)
			p.amount = 60
			p.lifetime = 9.0
			p.direction = Vector3(0, 1, 0)
			p.spread = 180.0
			p.initial_velocity_min = 0.03
			p.initial_velocity_max = 0.12
			p.gravity = Vector3.ZERO
			p.emission_shape = CPUParticles3D.EMISSION_SHAPE_BOX
			p.emission_box_extents = Vector3(w * 0.4, 1.5, d * 0.4)
			p.position = Vector3(0, 1.6, 0)
		"mist":
			mesh.size = Vector2(5.0, 2.2)
			mat.albedo_color = Color(0.6, 0.68, 0.8, 0.07)
			mat.albedo_texture = _flame_texture()
			p.amount = 18
			p.lifetime = 16.0
			p.direction = Vector3(1, 0, 0)
			p.spread = 20.0
			p.initial_velocity_min = 0.15
			p.initial_velocity_max = 0.4
			p.gravity = Vector3.ZERO
			p.emission_shape = CPUParticles3D.EMISSION_SHAPE_BOX
			p.emission_box_extents = Vector3(w * 0.8, 0.3, d * 0.8)
			p.position = Vector3(0, 0.6, 0)
	mesh.material = mat
	p.mesh = mesh
	add_child(p)


## Where flames burn on light-source models (local offset from the prop origin) and how big.
const FLAME_SPOTS := {
	"candle": [Vector3(0, 0.2, 0), 0.5], "candelabra": [Vector3(0, 1.45, 0), 1.0], "lantern": [Vector3(0, 0.2, 0), 0.9],
	"sconce": [Vector3(0, 0.2, -0.18), 0.6], "lamp_post": [Vector3(0, 3.1, 0), 0.8], "fireplace": [Vector3(0, 0.3, -0.05), 3.2], "torch": [Vector3(0, 0.3, 0), 1.0],
}


func _flames() -> void:
	var q := _quality()
	if q == 0:
		return
	var tex := _flame_texture()
	for eid in entities:
		var e: Dictionary = entities[eid]
		var asset: String = str(e.data.get("asset", ""))
		if FLAME_SPOTS.has(asset):
			_add_flame(e.node, FLAME_SPOTS[asset][0], float(FLAME_SPOTS[asset][1]), tex)
	for n in get_children():
		if n is Actor and n.has_meta("flame_asset"):
			pass


func _add_flame(parent: Node3D, off: Vector3, size: float, tex: Texture2D) -> void:
	var p := CPUParticles3D.new()
	p.position = off
	p.amount = int(10 + size * 6)
	p.lifetime = 0.7
	p.local_coords = true
	p.direction = Vector3(0, 1, 0)
	p.spread = 12.0
	p.initial_velocity_min = 0.15 * size
	p.initial_velocity_max = 0.4 * size
	p.gravity = Vector3(0, 0.3, 0)
	p.scale_amount_min = 0.7
	p.scale_amount_max = 1.2
	var mesh := QuadMesh.new()
	mesh.size = Vector2(0.09, 0.14) * size
	var mat := StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
	mat.billboard_mode = BaseMaterial3D.BILLBOARD_PARTICLES
	mat.albedo_texture = tex
	mat.vertex_color_use_as_albedo = true
	mesh.material = mat
	p.mesh = mesh
	var ramp := Gradient.new()
	ramp.set_color(0, Color(1.0, 0.85, 0.4, 0.9))
	ramp.set_color(1, Color(1.0, 0.25, 0.05, 0.0))
	p.color_ramp = ramp
	var sc := Curve.new()
	sc.add_point(Vector2(0, 0.6))
	sc.add_point(Vector2(0.3, 1.0))
	sc.add_point(Vector2(1, 0.1))
	p.scale_amount_curve = sc
	parent.add_child(p)


var _flame_tex: Texture2D


func _flame_texture() -> Texture2D:
	if _flame_tex == null:
		var g := Gradient.new()
		g.set_color(0, Color(1, 1, 1, 1))
		g.set_color(1, Color(1, 1, 1, 0))
		var gt := GradientTexture2D.new()
		gt.gradient = g
		gt.fill = GradientTexture2D.FILL_RADIAL
		gt.fill_from = Vector2(0.5, 0.5)
		gt.fill_to = Vector2(0.5, 0.0)
		gt.width = 64
		gt.height = 64
		_flame_tex = gt
	return _flame_tex


func _sun(sky_n: String, q: int) -> void:
	if sky_n == "night" or sky_n == "snow" and data.has("moon"):
		return
	var s := DirectionalLight3D.new()
	match sky_n:
		"day":
			s.light_color = Color("#fff0d4")
			s.light_energy = 1.0
			s.rotation_degrees = Vector3(-52, -35, 0)
		"dusk":
			s.light_color = Color("#ff9a5a")
			s.light_energy = 1.4
			s.rotation_degrees = Vector3(-14, -60, 0)
		"storm":
			s.light_color = Color("#9fb0c4")
			s.light_energy = 0.5
			s.rotation_degrees = Vector3(-60, -20, 0)
		_:
			s.light_color = Color("#d8dcff")
			s.light_energy = 0.9
			s.rotation_degrees = Vector3(-40, 30, 0)
	s.shadow_enabled = q >= 1
	s.directional_shadow_max_distance = 40.0
	add_child(s)


func _is_watery() -> bool:
	if data.has("water"):
		return bool(data.water)
	for k in ["harbour", "pier", "quay", "demeter", "deck", "launch", "bows", "brig", "schooner", "rapids", "river", "wheel", "cliff", "wreck"]:
		if id.contains(k):
			return true
	return false


## Animated sea/river plane around the scene (ship decks and quays float on it; cliffs look down on it).
func _water(fog: Color, sky_n: String) -> void:
	var pm := PlaneMesh.new()
	pm.size = Vector2(500, 500)
	pm.subdivide_width = 1
	pm.subdivide_depth = 1
	var mi := MeshInstance3D.new()
	mi.mesh = pm
	var mat := ShaderMaterial.new()
	mat.shader = load("res://shaders/water.gdshader")
	var deep: Color = {"day": Color("#2b5a78"), "dusk": Color("#3a3a58"), "storm": Color("#1f2a30"), "night": Color("#0d1a2c"), "snow": Color("#1b2a3c")}.get(sky_n, Color("#1f3a50"))
	var shallow: Color = {"day": Color("#5aa0b0"), "dusk": Color("#d0805a"), "storm": Color("#46565c"), "night": Color("#223a55"), "snow": Color("#4a6070")}.get(sky_n, Color("#3a6a80"))
	mat.set_shader_parameter("deep_color", deep)
	mat.set_shader_parameter("shallow_color", shallow)
	mat.set_shader_parameter("sky_color", fog.lightened(0.15))
	mat.set_shader_parameter("wave_strength", 0.55 if sky_n == "storm" else 0.22)
	mi.material_override = mat
	mi.position = Vector3(0, -14.0 if id.contains("cliff") else -0.75, 0)
	add_child(mi)


## Hull / quay wall / cliff face under water-side rooms so the floor does not float in the void.
func _skirt(w: float, d: float) -> void:
	if interior or not _is_watery() or id.contains("cliff"):
		return
	var cliff := id.contains("cliff")
	var depth := 14.0 if cliff else 1.6
	var ext := 4.0 if cliff else 0.0
	var mi := MeshInstance3D.new()
	var bm := BoxMesh.new()
	bm.size = Vector3(w + 2.0 * ext, depth, d + 2.0 * ext)
	mi.mesh = bm
	var mat := StandardMaterial3D.new()
	var wooden := str(data.floor) == "planks"
	var tex_id := "wood_planks" if wooden else "stone_rough"
	var t: Dictionary = Assets.manifest.textures[tex_id]
	mat.albedo_texture = load("res://assets/" + str(t.albedo))
	mat.albedo_color = Color("#5a4636") if wooden else Color("#6a645e")
	mat.uv1_triplanar = true
	mat.uv1_scale = Vector3(0.5, 0.5, 0.5)
	mat.roughness = 1.0
	mi.material_override = mat
	mi.position = Vector3(0, -depth / 2.0 - 0.2, 0)
	add_child(mi)


var _tuft_tex: Texture2D


func _tuft_texture() -> Texture2D:
	if _tuft_tex == null:
		var img := Image.create(64, 64, true, Image.FORMAT_RGBA8)
		img.fill(Color(0, 0, 0, 0))
		var rng := RandomNumberGenerator.new()
		rng.seed = 7
		for b in 7:
			var cx := rng.randf_range(8.0, 56.0)
			var lean := rng.randf_range(-10.0, 10.0)
			var hgt := rng.randf_range(34.0, 62.0)
			for y in int(hgt):
				var u := float(y) / hgt
				var half := (1.0 - u) * 3.2
				var xc := cx + lean * u * u
				var shade := 0.55 + 0.45 * u
				for x in range(int(xc - half), int(xc + half) + 1):
					if x >= 0 and x < 64:
						img.set_pixel(x, 63 - y, Color(0.30 * shade, 0.55 * shade + 0.1, 0.18 * shade, 1.0))
		img.generate_mipmaps()
		_tuft_tex = ImageTexture.create_from_image(img)
	return _tuft_tex


## Distance from (x, z) to the worn paths (matches the terrain shader).
func _path_distance(x: float, z: float, segs: Array) -> float:
	var best := 99.0
	var p := Vector2(x, z)
	for s in segs:
		var a := Vector2(s.x, s.y)
		var b := Vector2(s.z, s.w)
		var ab := b - a
		var t := clampf((p - a).dot(ab) / maxf(ab.dot(ab), 0.0001), 0.0, 1.0)
		best = minf(best, p.distance_to(a + ab * t))
	return best


## Scatter grass tufts / flower clusters / pebbles organically: noise-driven clumps, none on paths (one draw call per kind).
func _ground_detail(w: float, d: float) -> void:
	if interior or _quality() == 0 or (_is_watery() and not id.contains("cliff")):
		return
	var floor_name := str(data.floor)
	var rng := RandomNumberGenerator.new()
	rng.seed = hash("detail:" + id)
	var noise := FastNoiseLite.new()
	noise.seed = hash(id) % 5000 + 11
	noise.frequency = 0.16
	var segs := _path_segments()
	var tufts := floor_name in ["grass", "dirt"]
	var ext := 1.0 if host != null else (2.5 if id.contains("cliff") else 7.0)
	var tuft_pts: Array = []
	var tries := 0
	var want := (900 if floor_name == "grass" else 260) if tufts else 0
	while tuft_pts.size() < want and tries < want * 6:
		tries += 1
		var x := rng.randf_range(-w / 2.0 - ext, w / 2.0 + ext)
		var z := rng.randf_range(-d / 2.0 - ext, d / 2.0 + ext * 0.6)
		var dens := (noise.get_noise_2d(x, z) + 1.0) * 0.5
		if rng.randf() > pow(dens, 2.2) * 2.4:
			continue
		if _path_distance(x, z, segs) < 0.75:
			continue
		tuft_pts.append(Vector2(x, z))
	if tuft_pts.size() > 0:
		_multimesh_tufts(tuft_pts, rng, floor_name)
	if tufts and floor_name == "grass":
		_flower_clusters(w, d, rng, segs)
	if not tufts:
		_multimesh_pebbles(w, d, rng)


func _multimesh_tufts(pts: Array, rng: RandomNumberGenerator, floor_name: String) -> void:
	var mm := MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	mm.use_colors = true
	var am := ArrayMesh.new()
	var verts := PackedVector3Array()
	var uvs := PackedVector2Array()
	var idx := PackedInt32Array()
	for q in 3:
		var ang := q * PI / 3.0
		var dx := cos(ang) * 0.17
		var dz := sin(ang) * 0.17
		var base := verts.size()
		verts.append_array([Vector3(-dx, 0, -dz), Vector3(dx, 0, dz), Vector3(dx, 0.34, dz), Vector3(-dx, 0.34, -dz)])
		uvs.append_array([Vector2(0, 1), Vector2(1, 1), Vector2(1, 0), Vector2(0, 0)])
		idx.append_array([base, base + 1, base + 2, base, base + 2, base + 3])
	var arrays := []
	arrays.resize(Mesh.ARRAY_MAX)
	arrays[Mesh.ARRAY_VERTEX] = verts
	arrays[Mesh.ARRAY_TEX_UV] = uvs
	arrays[Mesh.ARRAY_INDEX] = idx
	am.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arrays)
	var mat := StandardMaterial3D.new()
	mat.albedo_texture = _tuft_texture()
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA_SCISSOR
	mat.alpha_scissor_threshold = 0.5
	mat.cull_mode = BaseMaterial3D.CULL_DISABLED
	mat.vertex_color_use_as_albedo = true
	mat.roughness = 1.0
	am.surface_set_material(0, mat)
	mm.mesh = am
	mm.instance_count = pts.size()
	for i in pts.size():
		var p: Vector2 = pts[i]
		var s := rng.randf_range(0.55, 1.6)
		mm.set_instance_transform(i, Transform3D(Basis(Vector3.UP, rng.randf() * TAU).scaled(Vector3(s, s * rng.randf_range(0.8, 1.6), s)), Vector3(p.x, 0.0, p.y)))
		var g := rng.randf_range(0.7, 1.15)
		mm.set_instance_color(i, Color(g * 0.9, g, g * 0.85) if floor_name == "grass" else Color(0.6, 0.55, 0.38) * g)
	var mmi := MultiMeshInstance3D.new()
	mmi.multimesh = mm
	add_child(mmi)


## Small clusters of wild flowers (tiny coloured blobs on short stems) scattered in clumps.
func _flower_clusters(w: float, d: float, rng: RandomNumberGenerator, segs: Array) -> void:
	var heads: Array = []
	for c in rng.randi_range(7, 12):
		var cx := rng.randf_range(-w / 2.0 - 3.0, w / 2.0 + 3.0)
		var cz := rng.randf_range(-d / 2.0 - 3.0, d / 2.0 + 2.0)
		var col: Color = [Color("#f4f2e6"), Color("#ecc83a"), Color("#9a62c8"), Color("#d84a4a"), Color("#f0a0c0")][rng.randi() % 5]
		for k in rng.randi_range(10, 24):
			var ang := rng.randf() * TAU
			var r := sqrt(rng.randf()) * rng.randf_range(0.7, 1.7)
			var x := cx + cos(ang) * r
			var z := cz + sin(ang) * r
			if _path_distance(x, z, segs) < 0.7:
				continue
			heads.append([Vector3(x, rng.randf_range(0.14, 0.3), z), col.lightened(rng.randf_range(-0.1, 0.12))])
	if heads.is_empty():
		return
	var mm := MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	mm.use_colors = true
	var sm := SphereMesh.new()
	sm.radius = 0.045
	sm.height = 0.07
	sm.radial_segments = 6
	sm.rings = 3
	var mat := StandardMaterial3D.new()
	mat.vertex_color_use_as_albedo = true
	mat.roughness = 0.8
	sm.surface_set_material(0, mat)
	mm.mesh = sm
	mm.instance_count = heads.size()
	for i in heads.size():
		mm.set_instance_transform(i, Transform3D(Basis(), heads[i][0]))
		mm.set_instance_color(i, heads[i][1])
	var mmi := MultiMeshInstance3D.new()
	mmi.multimesh = mm
	add_child(mmi)


func _multimesh_pebbles(w: float, d: float, rng: RandomNumberGenerator) -> void:
	var mm := MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	mm.use_colors = true
	var sm := SphereMesh.new()
	sm.radius = 0.09
	sm.height = 0.07
	sm.radial_segments = 6
	sm.rings = 3
	var mat := StandardMaterial3D.new()
	mat.vertex_color_use_as_albedo = true
	mat.roughness = 1.0
	sm.surface_set_material(0, mat)
	mm.mesh = sm
	var count := 160
	mm.instance_count = count
	for i in count:
		var s := rng.randf_range(0.6, 1.5)
		var t := Transform3D(Basis(Vector3.UP, rng.randf() * TAU).scaled(Vector3(s, s, s)), Vector3(rng.randf_range(-w / 2.0 - 4.0, w / 2.0 + 4.0), 0.0, rng.randf_range(-d / 2.0 - 4.0, d / 2.0 + 4.0)))
		mm.set_instance_transform(i, t)
		var v := rng.randf_range(0.35, 0.7)
		mm.set_instance_color(i, Color(v, v * 0.97, v * 0.92))
	var mmi := MultiMeshInstance3D.new()
	mmi.multimesh = mm
	add_child(mmi)
