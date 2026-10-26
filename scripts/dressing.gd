class_name Dressing
extends RefCounted
## Automatic set dressing so every location looks composed, not just furnished:
##   walls: paintings / banners, curtains beside windows, wall sconces that really light the room;
##   light: moon or sun spot through windows with a faint light shaft;
##   floor: rugs under tables and beds, stains, soft contact shadows under props and characters;
##   corners: cobwebs; themed clutter around the edges (barrels, benches, candelabra, rocks...).
## Purely cosmetic (no collisions, nothing clickable), deterministic per location + world seed.

const CELL := 4.0

const DECOR := {
	"tavern": {"wall": [["barrel", "dark", 2, 3], ["chest", "dark", 0, 1], ["bench", "dark", 1, 2]]},
	"study": {"wall": [["bookshelf", "dark", 1, 2], ["chest", "dark", 0, 1], ["candelabra", "default", 1, 1]]},
	"bedroom": {"wall": [["chest", "dark", 1, 1], ["candelabra", "default", 0, 1]]},
	"church": {"wall": [["candelabra", "default", 2, 3], ["gravestone", "stone_tomb", 0, 1], ["crucifix_big", "silver", 0, 1]]},
	"asylum": {"wall": [["bench", "oak", 1, 2], ["barrel", "dark", 0, 1], ["bed_simple", "black", 0, 1]]},
	"hall": {"wall": [["candelabra", "default", 2, 3], ["column_short", "stone_dark", 0, 2], ["barrel", "dark", 0, 1]]},
	"dock": {"wall": [["bollard", "default", 3, 5], ["crate_stack", "oak", 1, 3], ["barrel", "dark", 2, 3], ["rope_coil", "default", 1, 2], ["lamp_post", "default", 2, 3],
		["anchor", "iron", 0, 1], ["net_rack", "oak", 0, 1]]},
	"street": {"wall": [["lamp_post", "default", 2, 3], ["crate_stack", "oak", 1, 2], ["barrel", "dark", 2, 3], ["bench", "dark", 0, 1], ["market_stall", "red", 0, 1],
		["hay_bale", "straw", 0, 2], ["cart", "oak", 0, 1]]},
	"wild": {"scatter": [["rock", "grey", 3, 5], ["boulders", "mossy", 1, 3], ["bush", "green", 4, 8], ["fern", "green", 5, 9], ["flower_patch", "yellow", 2, 4],
		["flower_patch", "white", 2, 4], ["log", "bark", 1, 2], ["stump", "bark", 1, 3], ["oak", "green", 2, 4], ["deadtree", "grey", 0, 2]]},
	"graveyard": {"scatter": [["gravestone", "stone_tomb", 5, 9], ["gravestone_point", "stone_tomb", 3, 5], ["grave_cross", "stone_tomb", 2, 4], ["yew", "dark", 3, 5],
		["bush", "dark", 3, 5], ["flower_patch", "white", 2, 4], ["stump", "bark", 0, 2], ["low_wall", "stone_mossy", 2, 4], ["boulders", "mossy", 1, 2]]},
}


static func theme_of(id: String, interior: bool) -> String:
	if not interior:
		for k in ["churchyard", "cliff", "abbey", "grave", "cemetery", "church"]:
			if id.contains(k):
				return "graveyard"
	var checks := [["church", ["chapel", "crypt", "tomb", "vault", "church", "catacomb", "brides"]],
		["asylum", ["asylum", "ward", "dispensary", "cell", "scullery", "renfield"]],
		["dock", ["harbour", "quay", "pier", "deck", "hold", "galley", "launch", "schooner", "bows", "wheel", "forecastle", "rapids"]],
		["tavern", ["krone", "inn", "tavern", "veresti", "hotel", "odess"]],
		["study", ["study", "library", "office", "typing", "records", "archive", "muniment", "schoolroom", "desk"]],
		["bedroom", ["bedroom", "lodging", "sickroom", "chamber", "room"]],
		["hall", ["hall", "castle", "keep", "gate", "courtyard", "great"]],
		["street", ["street", "yard", "station", "london", "mile_end", "bermondsey", "piccadilly", "close", "green"]]]
	for c in checks:
		for k in c[1]:
			if id.contains(k):
				return str(c[0])
	return "hall" if interior else "wild"


static func dress(loc: Location) -> void:
	if loc.data.get("dress", true) == false:
		return
	var q: int = loc._quality()
	var rng := RandomNumberGenerator.new()
	rng.seed = hash("dress:%s:%d" % [loc.id, Game.seed_value])
	var w: float = loc.room_w
	var d: float = loc.room_d
	var theme := theme_of(loc.id, loc.interior)
	var occ: Array = _occupancy(loc)
	# contact shadows first (cheap, helps every scene)
	_blobs(loc, q)
	if loc.interior:
		var used := _walls(loc, rng, w, d, theme, occ, q)
		_rugs(loc, occ)
		_stains(loc, rng, w, d, theme)
		_cobwebs(loc, rng, w, d, theme)
		_clutter(loc, rng, w, d, theme, occ, used)
	else:
		var sky_n: String = loc._sky_name()
		if theme in ["dock", "street"]:
			_buildings(loc, rng, w, d, q)
		_wall_buildings(loc, rng, w, d, theme)
		_door_buildings(loc, rng, w, d)
		if theme in ["dock", "street"] and loc.room_w > float(loc.data.cells[0]) * CELL + 1.0 and not loc.data.get("no_west_street", false):
			_west_street(loc, rng, w, d)
		if theme == "dock" and loc._is_watery():
			_quay_edges(loc, w, d)
		_clutter(loc, rng, w, d, theme, occ, {})
		if not loc.data.get("no_backdrop", false):
			_backdrop(loc, rng, w, d, theme, sky_n, q)
			_fliers(loc, rng, w, d, theme, sky_n, q)


# ------------------------------------------------------------------ helpers
static func _occupancy(loc: Location) -> Array:
	var occ: Array = []
	for p in loc.data.get("props", []) + loc.data.get("npcs", []):
		occ.append([float(p.pos[0]), float(p.pos[2]), maxf(float(p.get("radius", 0.4)), 0.3) + 0.3, p.get("interact", {}).has("go")])
	return occ


static func _free(occ: Array, x: float, z: float, r: float) -> bool:
	for o in occ:
		var rr: float = float(o[2]) + r + (1.0 if o[3] else 0.0)
		if Vector2(x - float(o[0]), z - float(o[1])).length() < rr:
			return false
	return true


static func _tex(path: String) -> Texture2D:
	if ResourceLoader.exists(path):
		return load(path)
	return null


static func _quad(loc: Node3D, tex: Texture2D, size: Vector2, pos: Vector3, yaw_deg: float, tint: Color = Color.WHITE, mode: String = "scissor", flat: bool = false) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	var qm := QuadMesh.new()
	qm.size = size
	mi.mesh = qm
	var mat := StandardMaterial3D.new()
	mat.albedo_texture = tex
	mat.albedo_color = tint
	mat.roughness = 1.0
	mat.cull_mode = BaseMaterial3D.CULL_DISABLED
	match mode:
		"scissor":
			mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA_SCISSOR
			mat.alpha_scissor_threshold = 0.4
		"blend":
			mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		"add":
			mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
			mat.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
			mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mi.material_override = mat
	mi.position = pos
	mi.rotation_degrees.y = yaw_deg
	if flat:
		mi.rotation_degrees.x = -90.0
	loc.add_child(mi)
	return mi


## Wall cells that are plain wall pieces: [{side, i, pos(Vector3 on the inner face), yaw, kind}]
static func _wall_cells(loc: Location, w: float, d: float) -> Array:
	var out: Array = []
	var walls: Dictionary = loc.data.get("walls", {})
	for side in walls:
		var arr: Array = walls[side]
		for i in arr.size():
			var c := -w / 2.0 + CELL / 2.0 + i * CELL if side == "north" else -d / 2.0 + CELL / 2.0 + i * CELL
			var pos := Vector3.ZERO
			var yaw := 0.0
			match side:
				"north":
					pos = Vector3(c, 0, -d / 2.0 + 0.04)
					yaw = 0.0
				"west":
					pos = Vector3(-w / 2.0 + 0.04, 0, c)
					yaw = 90.0
				"east":
					pos = Vector3(w / 2.0 - 0.04, 0, c)
					yaw = -90.0
			out.append({"side": side, "i": i, "pos": pos, "yaw": yaw, "kind": str(arr[i])})
	return out


static func _wall_blocked(occ: Array, pos: Vector3, side: String) -> bool:
	for o in occ:
		var near_wall := false
		var along := 0.0
		if side == "north":
			near_wall = absf(float(o[1]) - pos.z) < 1.6
			along = absf(float(o[0]) - pos.x)
		else:
			near_wall = absf(float(o[0]) - pos.x) < 1.6
			along = absf(float(o[1]) - pos.z)
		if near_wall and along < 1.7 + (0.6 if o[3] else 0.0):
			return true
	return false


# ------------------------------------------------------------------ walls: art, curtains, sconces, window light
static func _walls(loc: Location, rng: RandomNumberGenerator, w: float, d: float, theme: String, occ: Array, q: int) -> Dictionary:
	var cells := _wall_cells(loc, w, d)
	var plain: Array = cells.filter(func(c: Dictionary) -> bool: return c.kind == "wall_4" and not _wall_blocked(occ, c.pos, c.side))
	var used := {}
	var warm_theme := theme in ["hall", "church", "tavern", "study", "bedroom", "asylum"]
	# window treatments
	var window_n := 0
	for c in cells:
		if c.kind != "wall_window_4":
			continue
		var inward := Vector3(sin(deg_to_rad(c.yaw)), 0, cos(deg_to_rad(c.yaw)))
		var side_dir := Vector3(cos(deg_to_rad(c.yaw)), 0, -sin(deg_to_rad(c.yaw)))
		if theme in ["bedroom", "study", "hall", "tavern"]:
			for s in [-1.0, 1.0]:
				_quad(loc, _tex("res://assets/textures/velvet_albedo.png"), Vector2(0.4, 1.9), c.pos + side_dir * s * 0.72 + Vector3(0, 1.75, 0) + inward * 0.04, c.yaw, Color("#5a1c24") if theme != "study" else Color("#2e4a30"), "opaque")
		if window_n < 2 and q >= 1:
			_window_light(loc, c, inward, q, window_n == 0)
		window_n += 1
	# decide art / sconce cells
	plain.shuffle()
	var sconces := 4 if theme in ["hall", "church"] else (3 if theme in ["tavern", "asylum"] else 2)
	var made_lights := 0
	for c in plain:
		var key := "%s%d" % [c.side, c.i]
		if made_lights < sconces and warm_theme:
			_sconce(loc, c, rng, q >= 1 and made_lights < (3 if q == 1 else 4))
			made_lights += 1
			used[key] = true
			continue
	var art := 0
	for c in plain:
		var key := "%s%d" % [c.side, c.i]
		if used.has(key) or art >= 4:
			continue
		if theme in ["hall", "church"] and art < 3 and rng.randf() < 0.7:
			var banner := "banner_red" if rng.randf() < 0.6 else "banner_black"
			_quad(loc, _tex("res://assets/decals/%s.png" % banner), Vector2(0.9, 2.2), c.pos + Vector3(0, 1.9, 0), c.yaw)
			art += 1
			used[key] = true
		elif theme not in ["dock", "street"] and rng.randf() < 0.55:
			var pn := "painting_%d" % (1 + rng.randi() % 3)
			_quad(loc, _tex("res://assets/decals/%s.png" % pn), Vector2(0.85, 1.13), c.pos + Vector3(0, 1.95, 0), c.yaw)
			art += 1
			used[key] = true
	return used


static func _sconce(loc: Location, c: Dictionary, rng: RandomNumberGenerator, with_light: bool = true) -> void:
	if not Assets.has_model("sconce"):
		return
	var inward := Vector3(sin(deg_to_rad(c.yaw)), 0, cos(deg_to_rad(c.yaw)))
	var pos: Vector3 = c.pos + Vector3(0, 2.15, 0) + (Vector3(1, 0, 0) if c.side != "north" else Vector3.ZERO) * 0.0
	var m := Assets.instantiate("sconce", "default")
	m.position = pos
	m.rotation_degrees.y = c.yaw
	loc.add_child(m)
	loc._add_flame(m, Vector3(0, 0.2, -0.18), 0.6, loc._flame_texture())
	if not with_light:
		return
	var l := OmniLight3D.new()
	l.position = pos + inward * 0.45 + Vector3(0, 0.15, 0)
	l.light_color = Color("#ffa24a")
	l.light_energy = 0.9
	l.omni_range = 5.0
	l.omni_attenuation = 1.4
	loc.add_child(l)
	loc._flickers.append([l, 0.9, rng.randf() * 10.0])


static func _window_light(loc: Location, c: Dictionary, inward: Vector3, q: int, shadows: bool) -> void:
	var fog := Color(str(loc.data.ambient.fog))
	var day := fog.v > 0.3
	var spot := SpotLight3D.new()
	var out_pos: Vector3 = c.pos + Vector3(0, 2.1, 0) - inward * 1.6
	spot.position = out_pos
	spot.light_color = Color("#ffe9c4") if day else Color("#8aa6ff")
	spot.light_energy = 3.2 if day else 2.4
	spot.spot_range = 16.0
	spot.spot_angle = 26.0
	spot.spot_angle_attenuation = 0.8
	spot.shadow_enabled = shadows and q >= 2
	loc.add_child(spot)
	var target: Vector3 = c.pos + inward * 5.0
	target.y = 0.0
	spot.look_at_from_position(out_pos, target, Vector3.UP)
	# faint shaft of light (additive quad slanting from the window to the floor)
	var tex := _tex("res://assets/decals/shaft.png")
	if tex != null:
		var mid: Vector3 = c.pos + inward * 1.6 + Vector3(0, 1.15, 0)
		var shaft := _quad(loc, tex, Vector2(1.7, 3.6), mid, c.yaw, Color(1.0, 0.92, 0.75, 0.9) if day else Color(0.6, 0.7, 1.0, 0.8), "add")
		shaft.rotation_degrees.x = 38.0
		shaft.rotation_degrees.z = 0.0


# ------------------------------------------------------------------ floor
static func _rugs(loc: Location, occ: Array) -> void:
	if not Assets.has_model("rug"):
		return
	var has_rug: Array = []
	for p in loc.data.get("props", []):
		if str(p.asset) == "rug":
			has_rug.append(Vector2(float(p.pos[0]), float(p.pos[2])))
	var palette: Dictionary = loc.data.get("palette", {})
	var variant: String = str(palette.get("cloth", "red"))
	var count := 0
	for p in loc.data.get("props", []):
		var a := str(p.asset)
		if (a == "table_long" or a == "table" or a == "bed" or a == "bed_simple") and float(p.pos[1]) < 0.2 and count < 2:
			var pos := Vector2(float(p.pos[0]), float(p.pos[2]))
			var covered := false
			for r in has_rug:
				if r.distance_to(pos) < 1.8:
					covered = true
			if covered:
				continue
			var m := Assets.instantiate("rug", variant if Assets.variants_of("rug").has(variant) else "red")
			m.position = Vector3(pos.x, 0.012, pos.y + (0.5 if a.begins_with("table") else 0.0))
			var s := Vector3(1.0, 1.0, 1.0)
			if a == "table_long":
				m.rotation_degrees.y = 90.0
				s = Vector3(1.5, 1.0, 1.7)
			elif a == "table":
				s = Vector3(1.1, 1.0, 0.95)
			else:
				s = Vector3(0.9, 1.0, 0.8)
			m.scale = s
			loc.add_child(m)
			count += 1


static func _stains(loc: Location, rng: RandomNumberGenerator, w: float, d: float, theme: String) -> void:
	var n := 5 if theme in ["church", "asylum", "hall"] else 3
	for i in n:
		var tex := _tex("res://assets/decals/stain_%d.png" % (1 + rng.randi() % 2))
		var s := rng.randf_range(1.3, 3.0)
		_quad(loc, tex, Vector2(s, s), Vector3(rng.randf_range(-w / 2 + 1, w / 2 - 1), 0.011, rng.randf_range(-d / 2 + 1, d / 2 - 1)),
			rng.randf() * 360.0, Color(1, 1, 1, 0.8), "blend", true)


static func _cobwebs(loc: Location, rng: RandomNumberGenerator, w: float, d: float, theme: String) -> void:
	if not theme in ["church", "asylum", "hall", "study"] and not str(loc.data.get("wall", "")).contains("mossy"):
		return
	var tex := _tex("res://assets/decals/cobweb.png")
	var h := 3.0
	for c in [[-1.0, -1.0], [1.0, -1.0]]:
		if rng.randf() < 0.75:
			var m := _quad(loc, tex, Vector2(1.1, 1.1), Vector3(c[0] * (w / 2.0 - 0.52), h, -d / 2.0 + 0.52), c[0] * 45.0, Color(1, 1, 1, 0.55), "blend")
			m.scale.x = -c[0]


static func _blobs(loc: Location, q: int) -> void:
	if q == 0:
		return
	var g := Gradient.new()
	g.set_color(0, Color(0, 0, 0, 0.5))
	g.set_color(1, Color(0, 0, 0, 0))
	var gt := GradientTexture2D.new()
	gt.gradient = g
	gt.fill = GradientTexture2D.FILL_RADIAL
	gt.fill_from = Vector2(0.5, 0.5)
	gt.fill_to = Vector2(0.5, 0.0)
	gt.width = 64
	gt.height = 64
	for eid in loc.entities:
		var e: Dictionary = loc.entities[eid]
		var node: Node3D = e.node
		var r := float(e.data.get("radius", 0.4))
		if float(e.data.pos[1]) > 0.2 or r < 0.2:
			continue
		var scale := clampf(r * 2.2, 0.8, 4.0) if not e.npc else 1.1
		_quad(node, gt, Vector2(scale, scale), Vector3(0, 0.014, 0), 0.0, Color.WHITE, "blend", true)
	if loc.player != null:
		_quad(loc.player, gt, Vector2(1.1, 1.1), Vector3(0, 0.014, 0), 0.0, Color.WHITE, "blend", true)


# ------------------------------------------------------------------ themed clutter along walls / scattered outdoors
static func _clutter(loc: Location, rng: RandomNumberGenerator, w: float, d: float, theme: String, occ: Array, used: Dictionary) -> void:
	var spec: Dictionary = DECOR.get(theme, {})
	var placed: Array = []
	if spec.has("wall") and loc.interior:
		var cells := _wall_cells(loc, w, d)
		for entry in spec.wall:
			var asset := str(entry[0])
			if not Assets.has_model(asset):
				continue
			var variant := str(entry[1])
			if not Assets.variants_of(asset).has(variant):
				variant = Assets.default_variant(asset)
			var n := rng.randi_range(int(entry[2]), int(entry[3]))
			for k in n:
				for attempt in 12:
					var c: Dictionary = cells[rng.randi() % cells.size()]
					var along := rng.randf_range(-1.6, 1.6)
					var inward := Vector3(sin(deg_to_rad(c.yaw)), 0, cos(deg_to_rad(c.yaw)))
					var side_dir := Vector3(cos(deg_to_rad(c.yaw)), 0, -sin(deg_to_rad(c.yaw)))
					var off := 0.55 if asset != "bookshelf" and asset != "column_short" else 0.35
					var p: Vector3 = c.pos + side_dir * along + inward * off
					if not _free(occ, p.x, p.z, 0.45) or not _free(placed, p.x, p.z, 0.4) or c.kind != "wall_4":
						continue
					if absf(p.x) > w / 2.0 - 0.3 or absf(p.z) > d / 2.0 - 0.3:
						continue
					_place(loc, asset, variant, p, c.yaw + rng.randf_range(-12, 12) if asset in ["barrel", "chest"] else c.yaw, rng, placed)
					break
	elif spec.has("scatter"):
		var half_w := w / 2.0 + 7.0
		var half_d := d / 2.0 + 6.0
		for entry in spec.scatter:
			var asset := str(entry[0])
			if not Assets.has_model(asset):
				continue
			var variant := str(entry[1])
			if variant == "green" and loc._sky_name() in ["night", "snow", "storm"]:
				variant = "dark"
			if not Assets.variants_of(asset).has(variant):
				variant = Assets.default_variant(asset)
			var n := rng.randi_range(int(entry[2]), int(entry[3]))
			for k in n:
				for attempt in 14:
					var p := Vector3(rng.randf_range(-half_w, half_w), 0, rng.randf_range(-half_d, d / 2.0 + 1.0))
					if not _free(occ, p.x, p.z, 1.0) or not _free(placed, p.x, p.z, 1.2):
						continue
					_place(loc, asset, variant, p, rng.randf() * 360.0, rng, placed, rng.randf_range(0.7, 1.3))
					break
	elif spec.has("wall") and not loc.interior:
		# street / dock: crates and barrels around the edge of the playable area
		var half_w := w / 2.0
		var half_d := d / 2.0
		for entry in spec.wall:
			var asset := str(entry[0])
			if not Assets.has_model(asset):
				continue
			var variant := str(entry[1])
			if not Assets.variants_of(asset).has(variant):
				variant = Assets.default_variant(asset)
			var n := rng.randi_range(int(entry[2]), int(entry[3]))
			for k in n:
				for attempt in 14:
					var edge := rng.randi() % 3
					var p := Vector3(rng.randf_range(-half_w + 0.5, half_w - 0.5), 0, -half_d + 0.6)
					if edge == 1:
						p = Vector3(-half_w + 0.6, 0, rng.randf_range(-half_d + 0.5, half_d - 0.5))
					elif edge == 2:
						p = Vector3(half_w - 0.6, 0, rng.randf_range(-half_d + 0.5, half_d - 0.5))
					if not _free(occ, p.x, p.z, 0.5) or not _free(placed, p.x, p.z, 0.5):
						continue
					_place(loc, asset, variant, p, rng.randf() * 360.0, rng, placed)
					break


static func _place(loc: Location, asset: String, variant: String, p: Vector3, yaw: float, rng: RandomNumberGenerator, placed: Array, scale_f: float = 1.0) -> void:
	var m := Assets.instantiate(asset, variant)
	m.position = p
	m.rotation_degrees.y = yaw
	m.scale = Vector3.ONE * scale_f
	loc.add_child(m)
	placed.append([p.x, p.z, 0.4, false])
	if Location.FLAME_SPOTS.has(asset):
		var f: Array = Location.FLAME_SPOTS[asset]
		loc._add_flame(m, f[0], float(f[1]), loc._flame_texture())
		if asset == "lamp_post" and loc._quality() >= 1:
			var ll := OmniLight3D.new()
			ll.position = p + Vector3(0, 3.1, 0)
			ll.light_color = Color("#ffc070")
			ll.light_energy = 1.2
			ll.omni_range = 7.0
			loc.add_child(ll)
			loc._flickers.append([ll, 1.2, rng.randf() * 10.0])
		if asset == "candelabra" and loc._flickers.size() < 12 and loc._quality() >= 2:
			var l := OmniLight3D.new()
			l.position = p + Vector3(0, 1.7, 0)
			l.light_color = Color("#ffb060")
			l.light_energy = 0.6
			l.omni_range = 3.4
			loc.add_child(l)
			loc._flickers.append([l, 0.6, rng.randf() * 10.0])


# ------------------------------------------------------------------ exterior: buildings, backdrop, fliers
static func _roof_variant(rng: RandomNumberGenerator) -> String:
	return ["slate", "slate", "tile"][rng.randi() % 3]


## Real buildings along the north edge (instead of a bare wall): front facing the camera, windows, dormers, chimneys.
static func _buildings(loc: Location, rng: RandomNumberGenerator, w: float, d: float, q: int) -> void:
	if not loc.data.get("walls", {}).has("north") and loc.data.get("buildings", true) == false:
		return
	var wall_v := str(loc.data.get("wall", "plaster_dirty"))
	if not wall_v in ["plaster", "plaster_dirty", "stone_grey", "stone_dark", "stone_mossy"]:
		wall_v = "plaster_dirty"
	var specs := [["house_front_a", 9.0, 5.5], ["house_front_b", 6.0, 5.0], ["house_front_c", 4.4, 4.0]]
	var x := -w / 2.0
	var guard := 0
	while x < w / 2.0 - 3.0 and guard < 8:
		guard += 1
		var remaining := w / 2.0 - x
		var pick: Array = specs[rng.randi() % specs.size()]
		if float(pick[1]) > remaining:
			pick = specs[2] if remaining < 6.0 else specs[1]
		var wd: float = float(pick[1])
		var sx := 1.0
		if remaining - wd < 3.0:
			sx = remaining / wd                   # stretch the last building to close the row
			wd = remaining
		var key := "%s_%s" % [wall_v, _roof_variant(rng)]
		var m := Assets.instantiate(str(pick[0]), key if Assets.variants_of(str(pick[0])).has(key) else Assets.default_variant(str(pick[0])))
		m.position = Vector3(x + wd / 2.0, 0, -d / 2.0 - float(pick[2]) / 2.0 - 0.05)
		m.scale = Vector3(sx, 1.0, 1.0)
		loc.add_child(m)
		x += wd + 0.2
		if q >= 1 and rng.randf() < 0.7:
			_smoke(loc, Vector3(m.position.x + wd * 0.28, 7.6, m.position.z + 0.5))


static func _smoke(loc: Location, pos: Vector3) -> void:
	if OS.get_cmdline_user_args().has("--nosmoke"):
		return
	var p := CPUParticles3D.new()
	p.position = pos
	p.amount = 14
	p.lifetime = 4.5
	p.local_coords = false
	p.direction = Vector3(0.3, 1, 0)
	p.spread = 14.0
	p.initial_velocity_min = 0.5
	p.initial_velocity_max = 0.9
	p.gravity = Vector3(0.15, 0.05, 0)
	p.scale_amount_min = 0.8
	p.scale_amount_max = 1.8
	var mesh := QuadMesh.new()
	mesh.size = Vector2(0.9, 0.9)
	var mat := StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.billboard_mode = BaseMaterial3D.BILLBOARD_PARTICLES
	var img := Image.create(64, 64, false, Image.FORMAT_RGBA8)
	for yy in 64:
		for xx in 64:
			var rr := Vector2(xx - 31.5, yy - 31.5).length() / 31.5
			var al := clampf(1.0 - rr, 0.0, 1.0)
			img.set_pixel(xx, yy, Color(1, 1, 1, al * al))
	var soft := ImageTexture.create_from_image(img)
	mat.albedo_texture = soft
	mat.albedo_color = Color(0.78, 0.78, 0.82)
	mat.vertex_color_use_as_albedo = true
	mesh.material = mat
	p.mesh = mesh
	var ramp := Gradient.new()
	ramp.set_color(0, Color(1, 1, 1, 0.45))
	ramp.set_color(1, Color(1, 1, 1, 0.0))
	p.color_ramp = ramp
	loc.add_child(p)


## Distant scenery: hills (land), skyline (towns), masts and a lighthouse (harbours).
static func _backdrop(loc: Location, rng: RandomNumberGenerator, w: float, d: float, theme: String, sky_n: String, q: int) -> void:
	if q == 0:
		return
	var fog := Color(str(loc.data.ambient.fog))
	var watery: bool = loc._is_watery()
	# hills ring
	var mm := MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	mm.use_colors = true
	var sm := SphereMesh.new()
	sm.radius = 1.0
	sm.height = 2.0
	sm.radial_segments = 10
	sm.rings = 5
	var mat := StandardMaterial3D.new()
	mat.vertex_color_use_as_albedo = true
	mat.roughness = 1.0
	sm.surface_set_material(0, mat)
	mm.mesh = sm
	var n := 16 if not watery else 9
	mm.instance_count = n
	for i in n:
		var ang := (float(i) / float(n)) * TAU + rng.randf_range(-0.12, 0.12)
		if watery and sin(ang) > -0.2:
			ang += PI * 0.9                   # keep the sea side (towards the camera) open
		var r := rng.randf_range(95.0, 135.0)
		var s := rng.randf_range(22.0, 46.0)
		var t := Transform3D(Basis().scaled(Vector3(s * 1.3, s * rng.randf_range(0.22, 0.42), s)), Vector3(cos(ang) * r, -s * 0.12, sin(ang) * r - 20.0))
		mm.set_instance_transform(i, t)
		var tint := fog.lerp(Color(0.18, 0.28, 0.2) if sky_n in ["day", "dusk"] else Color(0.08, 0.1, 0.16), 0.55)
		mm.set_instance_color(i, tint.darkened(rng.randf_range(0.0, 0.25)))
	var mmi := MultiMeshInstance3D.new()
	mmi.multimesh = mm
	loc.add_child(mmi)
	# town skyline behind the north edge
	if theme in ["dock", "street", "tavern"]:
		var count := 6
		for i in count:
			var asset := "house_wide" if rng.randf() < 0.5 else "house_row"
			var x := -w / 2.0 - 10.0 + float(i) * ((w + 20.0) / float(count)) + rng.randf_range(-2.0, 2.0)
			var sc := rng.randf_range(1.2, 1.9)
			var m := Assets.instantiate(asset, "plaster_dirty_slate" if rng.randf() < 0.6 else "stone_grey_slate")
			m.position = Vector3(x, 0.0, -d / 2.0 - 16.0 - rng.randf_range(0.0, 10.0))
			m.scale = Vector3.ONE * sc
			m.rotation_degrees.y = rng.randf_range(-6.0, 6.0)
			loc.add_child(m)
	if watery:
		for i in 2:
			var ship := Assets.instantiate("mast_cluster", "brown")
			ship.position = Vector3(-34.0 + i * 62.0 + rng.randf_range(-4, 4), -0.75, -42.0 - i * 14.0)
			ship.rotation_degrees.y = rng.randf_range(-25.0, 25.0)
			ship.scale = Vector3.ONE * rng.randf_range(0.9, 1.3)
			loc.add_child(ship)
		if loc.id.contains("harbour") or loc.id.contains("pier") or loc.id.contains("cliff") or loc.id.contains("quay"):
			var lh := Assets.instantiate("lighthouse", "white")
			lh.position = Vector3(-46.0, -0.8, -70.0)
			lh.scale = Vector3.ONE * 1.5
			loc.add_child(lh)


## Gulls over water by day, bats over open ground at night. Moved each frame by Location._process.
static func _fliers(loc: Location, rng: RandomNumberGenerator, w: float, d: float, theme: String, sky_n: String, q: int) -> void:
	if q == 0:
		return
	var model := ""
	var variant := ""
	var n := 0
	if loc._is_watery() and sky_n != "night":
		model = "gull"
		variant = "white"
		n = 5
	elif sky_n in ["night", "snow"] and theme in ["wild", "church", "street"] and not loc.id.contains("snow"):
		model = "bat"
		variant = "black"
		n = 3
	if n == 0 or not Assets.has_model(model):
		return
	for i in n:
		var a := Actor.new()
		loc.add_child(a)
		a.setup(model, variant, 1.1 if model == "gull" else 1.0)
		a.set_process(true)
		loc._fliers.append({"actor": a, "center": Vector3(rng.randf_range(-w * 0.3, w * 0.3), 0, rng.randf_range(-d * 0.4, d * 0.3)),
			"r": rng.randf_range(5.0, 11.0), "h": rng.randf_range(4.5, 8.5), "speed": rng.randf_range(0.25, 0.5) * (1.0 if i % 2 == 0 else -1.0),
			"phase": rng.randf() * TAU})


## Kerb stones around the open sides of a quay.
static func _quay_edges(loc: Location, w: float, d: float) -> void:
	if not Assets.has_model("quay_edge"):
		return
	var sides: Array = loc.data.get("quay_sides", ["south", "west", "east"])
	var n := int(w / 4.0)
	for i in n:
		if not "south" in sides:
			break
		var x := -w / 2.0 + 2.0 + i * 4.0
		var m := Assets.instantiate("quay_edge", "stone_grey")
		m.position = Vector3(x, 0, d / 2.0 + 0.1)
		loc.add_child(m)
	var nz := int(d / 4.0)
	for i in nz:
		var z := -d / 2.0 + 2.0 + i * 4.0
		for sx in [-1.0, 1.0]:
			if (sx < 0.0 and not "west" in sides) or (sx > 0.0 and not "east" in sides):
				continue
			var m2 := Assets.instantiate("quay_edge", "stone_grey")
			m2.position = Vector3(sx * (w / 2.0 + 0.1), 0, z)
			m2.rotation_degrees.y = 90.0 * sx
			loc.add_child(m2)


# ------------------------------------------------------------------ hidden loot in the extra ground
const LOOT := {
	"wild": [["stump", "bark", "Hollow stump", "Something is wedged in the hollow of the stump."], ["boulders", "mossy", "Small cairn", "Someone piled these stones on purpose."],
		["log", "bark", "Rotten log", "A fallen log, hollow at one end."]],
	"graveyard": [["gravestone", "stone_tomb", "Fallen headstone", "A headstone that slipped on the soft ground."], ["grave_cross", "stone_tomb", "Leaning cross", "Wreaths and ribbons, some of them recent."],
		["stump", "bark", "Old stump", "A stump grown over with ivy."]],
	"dock": [["crate_stack", "oak", "Broken crates", "Stove in and left, like most of the harbour's rubbish."], ["rope_coil", "default", "Abandoned tackle", "A tangle of line and a rusted hook."],
		["barrel", "dark", "Leaking barrel", "It has been rolled out of the way and forgotten."]],
	"street": [["crate_stack", "oak", "Abandoned crates", "Straw and nails."], ["barrel", "dark", "Rain barrel", "Black water and a few leaves."]],
	"interior": [["chest", "dark", "Dusty trunk", "Nobody has opened this in a long time."], ["barrel", "dark", "Old barrel", "It sounds empty - but not entirely."]],
}
const LOOT_ITEMS := {
	"wild": ["wood", "garlic", "silver", "bandage", "brandy", "rope"], "graveyard": ["silver", "wood", "garlic", "cloth"],
	"dock": ["rope", "oil", "silver", "bandage", "cloth"], "street": ["silver", "bandage", "cloth", "bullet"], "interior": ["silver", "brandy", "cloth", "bandage", "water"],
}


## Adds a few clickable finds to the part of the scene beyond the authored props (outer ring outdoors, corners indoors).
static func add_loot(loc: Location) -> void:
	if loc.data.get("loot", true) == false:
		return
	var theme := theme_of(loc.id, loc.interior)
	var key: String = "interior" if loc.interior else (theme if LOOT.has(theme) else "wild")
	if loc.interior and loc.room_w * loc.room_d < 60.0:
		return
	var rng := RandomNumberGenerator.new()
	rng.seed = hash("loot:%s:%d" % [loc.id, Game.seed_value])
	var occ := _occupancy(loc)
	var cells: Array = loc.data.cells
	var ohw: float = float(cells[0]) * CELL / 2.0
	var ohd: float = float(cells[1]) * CELL / 2.0
	var count := 2 if loc.interior else clampi(int(loc.room_w * loc.room_d / 110.0), 2, 5)
	var sp: Array = loc.data.spawn
	var made := 0
	var tries := 0
	while made < count and tries < 300:
		tries += 1
		var x := rng.randf_range(-loc.room_w / 2.0 + 1.0, loc.room_w / 2.0 - 1.0)
		var z := rng.randf_range(-loc.room_d / 2.0 + 1.0, loc.room_d / 2.0 - 1.0)
		if not loc.interior and absf(x) < ohw - 1.0 and absf(z) < ohd - 1.0:
			continue          # outdoors: only in the extra ring
		if loc.interior and absf(x) < loc.room_w / 2.0 - 2.2 and absf(z) < loc.room_d / 2.0 - 2.2:
			continue          # indoors: only near the walls
		if Vector2(x - float(sp[0]), z - float(sp[1])).length() < 3.0 or not _free(occ, x, z, 0.9):
			continue
		var spec: Array = LOOT[key][rng.randi() % LOOT[key].size()]
		var item: String = LOOT_ITEMS[key][rng.randi() % LOOT_ITEMS[key].size()]
		var amount := 2 if item in ["bullet", "wood", "rope"] else 1
		var eid := "loot_%s_%d" % [loc.id, made]
		var variant := str(spec[1])
		if not Assets.has_model(str(spec[0])):
			continue
		if not Assets.variants_of(str(spec[0])).has(variant):
			variant = Assets.default_variant(str(spec[0]))
		loc.data.props.append({"id": eid, "asset": str(spec[0]), "variant": variant, "pos": [x, 0.0, z], "rot": rng.randi() % 360, "scale": 1.0, "radius": 0.6, "name": str(spec[2]),
			"interact": {"look": str(spec[3]), "take": item, "give_once": true, "take_amount": amount,
				"take_text": "Wedged in among the rubbish I find %s." % Game.item_name(item).to_lower()}})
		occ.append([x, z, 1.1, false])
		made += 1


## A side street leaving the open west edge of a town scene: houses facing it, lamps, a cobbled road fading out, and a small square at its mouth.
static func _west_street(loc: Location, rng: RandomNumberGenerator, w: float, d: float) -> void:
	var x0 := -w / 2.0
	var wall_v := str(loc.data.get("wall", "plaster_dirty"))
	if not wall_v in ["plaster", "plaster_dirty", "stone_grey", "stone_dark", "stone_mossy"]:
		wall_v = "plaster_dirty"
	var row_z: Array = []
	var z := -d / 2.0 + 2.0
	while z < d / 2.0:
		if absf(z) > 2.6:
			row_z.append(z)
		z += 6.2
	for zz in row_z:
		var spec: String = ["house_front_a", "house_front_b", "house_front_c"][rng.randi() % 3]
		var key := "%s_%s" % [wall_v, _roof_variant(rng)]
		var m := Assets.instantiate(spec, key if Assets.variants_of(spec).has(key) else Assets.default_variant(spec))
		m.position = Vector3(x0 - 3.2, 0, zz)
		m.rotation_degrees.y = 90.0
		m.scale = Vector3(0.7, 1.0, 1.0)
		loc.add_child(m)
	# the road itself
	var road := MeshInstance3D.new()
	var pm := PlaneMesh.new()
	pm.size = Vector2(22.0, 5.0)
	road.mesh = pm
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color(0.34, 0.31, 0.27)
	mat.roughness = 1.0
	road.material_override = mat
	road.position = Vector3(x0 - 8.0, 0.03, 0)
	loc.add_child(road)
	for sx in [-4.0, -11.0]:
		for sz in [-2.6, 2.6]:
			if Assets.has_model("lamp_post"):
				var lp := Assets.instantiate("lamp_post", Assets.default_variant("lamp_post"))
				lp.position = Vector3(x0 + sx, 0, sz)
				loc.add_child(lp)
	# small square at the mouth of the street
	for spec in [["well", 2.4, 4.0], ["market_stall", 3.2, -3.6], ["cart", 1.6, -5.0]]:
		if Assets.has_model(str(spec[0])):
			var m2 := Assets.instantiate(str(spec[0]), Assets.default_variant(str(spec[0])))
			m2.position = Vector3(x0 + float(spec[1]) + 1.0, 0, float(spec[2]))
			m2.rotation_degrees.y = rng.randf_range(-30, 30)
			loc.add_child(m2)


## Distant scenery and flying birds for a merged region, built once for the whole landscape.
static func dress_region(loc: Location, theme: String) -> void:
	var rng := RandomNumberGenerator.new()
	rng.seed = hash("region:%s:%d" % [loc.id, Game.seed_value])
	var q: int = loc._quality()
	var sky_n: String = loc._sky_name()
	_backdrop(loc, rng, loc.room_w, loc.room_d, theme, sky_n, q)
	_fliers(loc, rng, loc.room_w, loc.room_d, theme, sky_n, q)


# ------------------------------------------------------------------ whole buildings instead of lone walls
const HOUSE_SPECS := [["house_front_a", 9.0, 5.5], ["house_front_b", 6.0, 5.0], ["house_front_c", 4.4, 4.0]]


static func _house_variant(loc: Location, rng: RandomNumberGenerator, spec: String) -> String:
	var wall_v := str(loc.data.get("wall", "plaster_dirty"))
	if not wall_v in ["plaster", "plaster_dirty", "stone_grey", "stone_dark", "stone_mossy"]:
		wall_v = "plaster_dirty"
	var key := "%s_%s" % [wall_v, _roof_variant(rng)]
	return key if Assets.variants_of(spec).has(key) else Assets.default_variant(spec)


## A run of houses behind a wall line: `origin` is where the run starts, `along` its direction, `front` the way the facades face.
static func _house_run(loc: Location, rng: RandomNumberGenerator, origin: Vector3, along: Vector3, front: Vector3, length: float, rot_y: float) -> void:
	var u := 0.0
	var guard := 0
	while u < length - 1.5 and guard < 8:
		guard += 1
		var remaining := length - u
		var pick: Array = HOUSE_SPECS[rng.randi() % HOUSE_SPECS.size()]
		if float(pick[1]) > remaining:
			pick = HOUSE_SPECS[2] if remaining < 6.0 else HOUSE_SPECS[1]
		var wd: float = float(pick[1])
		var sx := 1.0
		if remaining - wd < 3.0:
			sx = remaining / wd
			wd = remaining
		var m := Assets.instantiate(str(pick[0]), _house_variant(loc, rng, str(pick[0])))
		m.position = origin + along * (u + wd / 2.0) - front * (float(pick[2]) / 2.0)
		m.rotation_degrees.y = rot_y
		m.scale = Vector3(sx, 1.0, 1.0)
		loc.add_child(m)
		_note_building(loc, m.position, wd, float(pick[2]), rot_y)
		u += wd + 0.2


static func _note_building(loc: Location, pos: Vector3, wd: float, dp: float, rot_y: float) -> void:
	var rects: Array = loc.get_meta("bldg_rects", [])
	var swap := absf(sin(deg_to_rad(rot_y))) > 0.5
	var sz := Vector2(dp, wd) if swap else Vector2(wd, dp)
	rects.append(Rect2(Vector2(pos.x, pos.z) - sz / 2.0, sz))
	loc.set_meta("bldg_rects", rects)


## Every wall run of an open-air scene (house fronts with doors, garden walls...) gets a whole building behind it.
static func _wall_buildings(loc: Location, rng: RandomNumberGenerator, w: float, d: float, theme: String) -> void:
	if loc.data.get("buildings", true) == false or loc.id.contains("deck") or loc.id.contains("demeter") or loc.id.contains("castle"):
		return
	var walls: Dictionary = loc.data.get("walls", {})
	for side in walls:
		if side == "north" and theme in ["dock", "street"]:
			continue                                   # the town row already stands there
		var n: int = (walls[side] as Array).size()
		var len := float(n) * CELL
		match side:
			"north":
				_house_run(loc, rng, Vector3(-w / 2.0, 0, -d / 2.0 - 0.3), Vector3(1, 0, 0), Vector3(0, 0, -1) * -1.0, len, 0.0)
			"south":
				_house_run(loc, rng, Vector3(-w / 2.0, 0, d / 2.0 + 0.3), Vector3(1, 0, 0), Vector3(0, 0, 1) * -1.0, len, 180.0)
			"west":
				_house_run(loc, rng, Vector3(-w / 2.0 - 0.3, 0, -d / 2.0), Vector3(0, 0, 1), Vector3(-1, 0, 0) * -1.0, len, 90.0)
			"east":
				_house_run(loc, rng, Vector3(w / 2.0 + 0.3, 0, -d / 2.0), Vector3(0, 0, 1), Vector3(1, 0, 0) * -1.0, len, -90.0)


## A door that stands alone in the open gets a whole house built around it (facade = the door plane).
static func _door_buildings(loc: Location, rng: RandomNumberGenerator, w: float, d: float) -> void:
	if loc.data.get("buildings", true) == false or loc.id.contains("deck") or loc.id.contains("demeter"):
		return
	var rects: Array = loc.get_meta("bldg_rects", [])
	for p in loc.data.get("props", []):
		var a := str(p.asset)
		if a != "door" and a != "door_big":
			continue
		var go := str(p.get("interact", {}).get("go", ""))
		if go == "" or not Game.resolved.locations.has(go) or not Game.resolved.locations[go].get("interior", true):
			continue
		var pos := Vector3(float(p.pos[0]), 0, float(p.pos[2]))
		var covered := false
		for r in rects:
			if (r as Rect2).grow(1.6).has_point(Vector2(pos.x, pos.z)):
				covered = true
				break
		if covered:
			continue
		var rot := float(p.get("rot", 0))
		var fwd := Vector3(sin(deg_to_rad(rot)), 0, cos(deg_to_rad(rot)))
		var pick: Array = HOUSE_SPECS[0] if a == "door_big" else HOUSE_SPECS[1]
		var wd: float = float(pick[1])
		var dp: float = float(pick[2])
		var center := pos - fwd * (dp / 2.0 + 0.05)
		var foot := Rect2(Vector2(center.x, center.z) - (Vector2(dp, wd) if absf(fwd.x) > 0.5 else Vector2(wd, dp)) / 2.0, (Vector2(dp, wd) if absf(fwd.x) > 0.5 else Vector2(wd, dp)))
		var clash := false
		for o in loc.data.get("props", []) + loc.data.get("npcs", []):
			if str(o.id) == str(p.id):
				continue
			if foot.grow(-0.2).has_point(Vector2(float(o.pos[0]), float(o.pos[2]))) and (float(o.get("radius", 0.0)) > 0.3 or str(o.asset).begins_with("human")):
				clash = true
				break
		if clash:
			continue
		var m := Assets.instantiate(str(pick[0]), _house_variant(loc, rng, str(pick[0])))
		m.position = center
		m.rotation_degrees.y = rot
		loc.add_child(m)
		_note_building(loc, center, wd, dp, rot)


## Lone "tower" props that stand for a church or a manor become real buildings (data is a per-scene copy, so this is safe).
static func upgrade_buildings(data: Dictionary) -> void:
	if data.get("interior", true):
		return
	for p in data.get("props", []):
		if str(p.asset) != "tower":
			continue
		var pid := str(p.id)
		if pid.contains("church") or pid.contains("chapel") or pid.contains("abbey"):
			p.asset = "church"
			p.variant = "stone_grey_slate" if str(data.get("wall", "")) != "stone_mossy" else "stone_mossy_slate"
			p.scale = 1.0
			p.radius = 3.0
		elif pid.contains("house"):
			p.asset = "manor"
			p.variant = "plaster_dirty_slate" if str(data.get("wall", "")) in ["plaster", "plaster_dirty"] else "stone_grey_slate"
			p.scale = 1.0
			p.radius = 3.5
