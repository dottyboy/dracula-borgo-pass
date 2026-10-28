class_name PolyDungeon
extends RefCounted
## Dungeons made entirely in Godot (no Blender): rooms are regular polygons (pentagon ... decagon) joined by straight corridors.
## A new room is attached to a free edge of an existing one: it is rotated so that one of its edges faces the parent's door exactly,
## and its centre is put where that edge's midpoint meets the end of the corridor, so a door always meets a door in a straight line.
## The result is a "gla-export/1"-shaped definition (walk rectangles on a 0.5 m grid, rooms, props, lights) that Dungeon and Location
## already know how to play, plus the polygon data used to build the meshes (build_scene). Same seed = same level.

const TS := 0.5                  # walk grid, like a castle package
const WALL_T := 0.3
const WALL_H := 3.6
const DOOR_W := 2.0
const DOOR_H := 2.5
const CORR_W := 2.6              # corridor, wall to wall
const MIN_EDGE := 3.0            # an edge needs this length to carry a door
const SHAPES := {5: "PENTAGON", 6: "HEXAGON", 7: "HEPTAGON", 8: "OCTAGON", 9: "NONAGON", 10: "DECAGON"}

static var _cache: Dictionary = {}


# ---------------------------------------------------------------- polygon helpers
static func _apothem(r: Dictionary) -> float:
	return float(r.r) * cos(PI / int(r.n))


static func _normal(r: Dictionary, e: int) -> Vector2:
	return Vector2.from_angle(float(r.rot) + (e + 0.5) * TAU / int(r.n))


static func _vert(r: Dictionary, i: int) -> Vector2:
	return (r.c as Vector2) + Vector2.from_angle(float(r.rot) + (i % int(r.n)) * TAU / int(r.n)) * float(r.r)


static func _mid(r: Dictionary, e: int) -> Vector2:
	return (r.c as Vector2) + _normal(r, e) * _apothem(r)


static func _edge_len(r: Dictionary) -> float:
	return 2.0 * float(r.r) * sin(PI / int(r.n))


static func _poly(r: Dictionary, grow: float = 0.0) -> PackedVector2Array:
	var pts := PackedVector2Array()
	var rr := float(r.r) + grow / cos(PI / int(r.n))
	for i in int(r.n):
		pts.append((r.c as Vector2) + Vector2.from_angle(float(r.rot) + i * TAU / int(r.n)) * rr)
	return pts


static func _rect_poly(p0: Vector2, p1: Vector2, width: float, shorten: float = 0.0) -> PackedVector2Array:
	var d := (p1 - p0).normalized()
	var a := p0 + d * shorten
	var b := p1 - d * shorten
	var o := Vector2(-d.y, d.x) * (width / 2.0)
	return PackedVector2Array([a + o, b + o, b - o, a - o])


## Separating axis test for two convex polygons: true when they overlap.
static func _overlap(a: PackedVector2Array, b: PackedVector2Array) -> bool:
	for poly in [a, b]:
		var pts: PackedVector2Array = poly
		for i in pts.size():
			var e: Vector2 = pts[(i + 1) % pts.size()] - pts[i]
			var ax := Vector2(-e.y, e.x).normalized()
			var a0 := 1e18
			var a1 := -1e18
			for p in a:
				var d := (p as Vector2).dot(ax)
				a0 = minf(a0, d)
				a1 = maxf(a1, d)
			var b0 := 1e18
			var b1 := -1e18
			for p in b:
				var d2 := (p as Vector2).dot(ax)
				b0 = minf(b0, d2)
				b1 = maxf(b1, d2)
			if a1 <= b0 or b1 <= a0:
				return false
	return true


# ---------------------------------------------------------------- layout
static func generate(def_in: Dictionary, seed_value: int) -> Dictionary:
	var id := str(def_in.get("id", "poly"))
	var salt := str((def_in.get("recipe", {}) as Dictionary).get("salt", ""))
	var key := "%s:%d:%s" % [id, seed_value, salt]
	if _cache.has(key):
		return _cache[key]
	var rec: Dictionary = def_in.get("recipe", {})
	var sides: Array = rec.get("sides", [6, 8, 5, 7, 10])
	var rr: Array = rec.get("radius", [4.6, 6.4])
	var rn: Array = rec.get("rooms", [5, 7])
	var rng := RandomNumberGenerator.new()
	rng.seed = hash("poly:%s:%d:%s" % [id, seed_value, salt])
	var want := rng.randi_range(int(rn[0]), int(rn[1]))
	var rooms: Array = []
	var cors: Array = []
	var first := _new_room(rng, sides, rr, Vector2.ZERO, rng.randf() * TAU)
	while _edge_len(first) < MIN_EDGE:                  # the first room needs edges that can carry a door
		first = _new_room(rng, sides, rr, Vector2.ZERO, rng.randf() * TAU)
	rooms.append(first)
	var guard := 0
	var restarts := 0
	while rooms.size() < want and restarts < 8:
		if guard >= 400:                                 # boxed in: start the layout again
			restarts += 1
			guard = 0
			rooms = [first.duplicate(true)]
			(rooms[0] as Dictionary).doors = {}
			cors = []
			continue
		guard += 1
		var pi_ := rooms.size() - 1 if rng.randf() < 0.45 else rng.randi_range(0, rooms.size() - 1)
		var p: Dictionary = rooms[pi_]
		var free: Array = []
		var doors: Dictionary = p.doors
		for e in int(p.n):
			if doors.has(e) or doors.has((e + 1) % int(p.n)) or doors.has((e + int(p.n) - 1) % int(p.n)):
				continue                                     # never on or beside an existing door
			if _edge_len(p) >= MIN_EDGE:
				free.append(e)
		if free.is_empty():
			continue
		var e: int = free[rng.randi() % free.size()]
		var dir := _normal(p, e)
		var lc := rng.randf_range(3.0, 6.5)
		var pa := _mid(p, e)
		var pb := pa + dir * lc
		var nb: int = sides[rng.randi() % sides.size()]
		var rad := rng.randf_range(float(rr[0]), float(rr[1]))
		var nr := {"n": nb, "r": rad, "rot": 0.0, "c": Vector2.ZERO, "doors": {}}
		if _edge_len(nr) < MIN_EDGE:
			continue
		var j := rng.randi_range(0, nb - 1)
		nr.rot = (-dir).angle() - (j + 0.5) * TAU / nb          # edge j faces back along the corridor
		nr.c = pb + dir * _apothem(nr)
		var bad := false
		var shape := _poly(nr, 1.2)
		for k in rooms.size():
			if _overlap(shape, _poly(rooms[k], 1.2)):
				bad = true
				break
		var crect := _rect_poly(pa, pb, CORR_W + 0.6, 0.3)
		if not bad:
			for k in rooms.size():
				if k != pi_ and _overlap(crect, _poly(rooms[k], 0.4)):
					bad = true
					break
		if not bad:
			for c in cors:
				if _overlap(crect, _rect_poly(c.p0, c.p1, CORR_W + 0.6, 0.3)) or _overlap(shape, _rect_poly(c.p0, c.p1, CORR_W + 0.6)):
					bad = true
					break
		if bad:
			continue
		doors[e] = cors.size()
		(nr.doors as Dictionary)[j] = cors.size()
		cors.append({"a": pi_, "ea": e, "b": rooms.size(), "eb": j, "p0": pa, "p1": pb, "dir": dir})
		rooms.append(nr)
	# entrance in room 0, exit in the room farthest from it along the corridors
	var dist: Array = []
	dist.resize(rooms.size())
	dist.fill(-1)
	dist[0] = 0
	var todo: Array = [0]
	while not todo.is_empty():
		var cur: int = todo.pop_front()
		for c in cors:
			var o := -1
			if int(c.a) == cur:
				o = int(c.b)
			elif int(c.b) == cur:
				o = int(c.a)
			if o >= 0 and dist[o] < 0:
				dist[o] = dist[cur] + 1
				todo.append(o)
	var far := 0
	for k in rooms.size():
		if dist[k] > dist[far]:
			far = k
	var d := def_in.duplicate(true)
	d["format"] = "gla-export/1"
	d["id"] = id
	d["tile_size"] = TS
	d["wall_height"] = WALL_H
	d["level_height"] = 4.5
	d["interior"] = true
	d["stairs"] = []
	d["stair_links"] = []
	d["poly"] = {"rooms": rooms, "cors": cors}
	_fill_walk(d, rooms, cors)
	var out_rooms: Array = []
	for k in rooms.size():
		var r: Dictionary = rooms[k]
		var c: Vector2 = r.c
		var ap := _apothem(r)
		out_rooms.append({"id": k, "shape": SHAPES.get(int(r.n), "POLY"), "floor": 0, "rect": [c.x - ap, c.y - ap, c.x + ap, c.y + ap], "center": [c.x, c.y]})
	d["rooms"] = out_rooms
	var e0: Vector2 = (rooms[0] as Dictionary).c
	var e1: Vector2 = (rooms[far] as Dictionary).c
	d["entrance"] = {"floor": 0, "cell": [roundi(e0.x / TS), roundi(e0.y / TS)], "pos": [e0.x, 0.0, e0.y]}
	d["exit"] = {"floor": 0, "cell": [roundi(e1.x / TS), roundi(e1.y / TS)], "pos": [e1.x, 0.0, e1.y]}
	_dress(d, rooms, cors, rng, far)
	_cache[key] = d
	return d


static func _new_room(rng: RandomNumberGenerator, sides: Array, rr: Array, c: Vector2, rot: float) -> Dictionary:
	var n: int = sides[rng.randi() % sides.size()]
	var r := {"n": n, "r": rng.randf_range(float(rr[0]), float(rr[1])), "rot": rot, "c": c, "doors": {}}
	return r


## Walkable tiles: inside a room with 0.55 m of clearance from every wall, or in a corridor (and through the doors into the rooms).
static func _fill_walk(d: Dictionary, rooms: Array, cors: Array) -> void:
	var lo := Vector2(1e9, 1e9)
	var hi := Vector2(-1e9, -1e9)
	for r in rooms:
		var rad := float(r.r) + 1.0
		lo = lo.min((r.c as Vector2) - Vector2(rad, rad))
		hi = hi.max((r.c as Vector2) + Vector2(rad, rad))
	var ix0 := floori(lo.x / TS)
	var ix1 := ceili(hi.x / TS)
	var iz0 := floori(lo.y / TS)
	var iz1 := ceili(hi.y / TS)
	var normals: Array = []
	for r in rooms:
		var ns: Array = []
		for e in int(r.n):
			ns.append(_normal(r, e))
		normals.append(ns)
	var open := {}
	for iz in range(iz0, iz1 + 1):
		for ix in range(ix0, ix1 + 1):
			var p := Vector2(ix * TS, iz * TS)
			var ok := false
			for k in rooms.size():
				var r: Dictionary = rooms[k]
				var rel: Vector2 = p - (r.c as Vector2)
				if rel.length() > float(r.r):
					continue
				var inside := true
				var ap := _apothem(r)
				for nrm in normals[k]:
					if ap - rel.dot(nrm as Vector2) < 0.55:
						inside = false
						break
				if inside:
					ok = true
					break
			if not ok:
				for c in cors:
					var dir: Vector2 = c.dir
					var rel2: Vector2 = p - (c.p0 as Vector2)
					var along := rel2.dot(dir)
					var lat := absf(rel2.dot(Vector2(-dir.y, dir.x)))
					var len := (c.p1 as Vector2).distance_to(c.p0)
					if along >= -0.7 and along <= len + 0.7 and lat <= 0.8:
						ok = true
						break
			if ok:
				open[Vector2i(ix, iz)] = true
	# merge into rectangles: horizontal runs, then runs of identical span in consecutive rows
	var rects: Array = []
	var active := {}
	for iz in range(iz0, iz1 + 2):
		var runs := {}
		var ix := ix0
		while ix <= ix1:
			if open.has(Vector2i(ix, iz)):
				var s := ix
				while open.has(Vector2i(ix + 1, iz)):
					ix += 1
				runs["%d:%d" % [s, ix]] = [s, ix]
			ix += 1
		for k in active.keys():
			if not runs.has(k):
				var a: Array = active[k]
				rects.append([(a[0] - 0.5) * TS, (a[2] - 0.5) * TS, (a[1] + 0.5) * TS, (iz - 1 + 0.5) * TS])
				active.erase(k)
		for k in runs:
			if not active.has(k):
				active[k] = [runs[k][0], runs[k][1], iz]
	d["floors"] = [{"z": 0, "y": 0.0, "cells": open.size(), "walk_rects": rects}]


## Columns on every other corner of the bigger rooms, candelabra on the rest (with a light each), crates and barrels at a wall.
static func _dress(d: Dictionary, rooms: Array, cors: Array, rng: RandomNumberGenerator, far: int) -> void:
	var props: Array = []
	var lights: Array = []
	for k in rooms.size():
		var r: Dictionary = rooms[k]
		var c: Vector2 = r.c
		var rad := float(r.r)
		var n := int(r.n)
		var doors: Dictionary = r.doors
		for i in n:
			if doors.has(i) or doors.has((i + n - 1) % n):
				continue                                     # nothing standing beside a doorway
			var v := _vert(r, i)
			var inset := c + (v - c).normalized() * (rad - 0.95)
			if i % 2 == 0 and n >= 6:
				props.append({"kind": "COLUMN", "pos": [inset.x, 0.0, inset.y], "yaw": 0.0})
			else:
				props.append({"kind": "CANDLESTAND", "pos": [inset.x, 0.0, inset.y], "yaw": 0.0})
				lights.append({"pos": [inset.x, 1.6, inset.y], "color": [1.0, 0.55, 0.2], "energy_w": 60.0, "radius": 0.25})
		var cands: Array = []
		for e in n:
			if not doors.has(e) and not doors.has((e + 1) % n) and not doors.has((e + n - 1) % n):
				cands.append(e)
		if not cands.is_empty():
			var e: int = cands[rng.randi() % cands.size()]
			var m := _mid(r, e) - _normal(r, e) * 1.0
			var t := Vector2(-_normal(r, e).y, _normal(r, e).x)
			props.append({"kind": "CRATE" if rng.randf() < 0.5 else "BARREL", "pos": [m.x, 0.0, m.y], "yaw": rng.randf() * TAU})
			var m2 := m + t * rng.randf_range(0.9, 1.4)
			props.append({"kind": "BARREL" if rng.randf() < 0.6 else "CRATE", "pos": [m2.x, 0.0, m2.y], "yaw": rng.randf() * TAU})
		if k == far or (k == rooms.size() - 2 and rooms.size() > 3):
			var best_a := float(r.rot)                      # the direction farthest from every doorway
			var best_d := -1.0
			for i in n:
				var a := float(r.rot) + i * TAU / n
				var dmin := 10.0
				for e in doors.keys():
					dmin = minf(dmin, absf(angle_difference(a, _normal(r, int(e)).angle())))
				if dmin > best_d:
					best_d = dmin
					best_a = a
			var tb := c + Vector2.from_angle(best_a) * minf(rad * 0.45, 2.4)
			props.append({"kind": "TOMB" if k == far else "COFFIN", "pos": [tb.x, 0.0, tb.y], "yaw": float(r.rot)})
	d["props"] = props
	d["lights"] = lights


# ---------------------------------------------------------------- meshes
class Builder extends RefCounted:
	var st := SurfaceTool.new()

	func _init() -> void:
		st.begin(Mesh.PRIMITIVE_TRIANGLES)

	## One triangle, wound so that its front side faces `n` whatever the order of a, b, c.
	func tri(a: Vector3, b: Vector3, c: Vector3, n: Vector3) -> void:
		var cross := (b - a).cross(c - a)
		var v := [a, b, c] if cross.dot(n) < 0.0 else [a, c, b]
		for p in v:
			st.set_normal(n)
			st.set_uv(Vector2((p as Vector3).x * 0.5 + (p as Vector3).z * 0.5, (p as Vector3).y * 0.5))
			st.add_vertex(p)

	func quad(a: Vector3, b: Vector3, c: Vector3, d: Vector3, n: Vector3) -> void:
		tri(a, b, c, n)
		tri(a, c, d, n)

	## A wall slab along p0 -> p1 (xz), from height z0 to z1, WALL_T thick, ends overshooting by half a thickness so corners close.
	func slab(p0: Vector2, p1: Vector2, z0: float, z1: float, over: float = 0.15, thick: float = 0.3) -> void:
		var dv := (p1 - p0)
		if dv.length() < 0.05:
			return
		var d := dv.normalized()
		var o := Vector2(-d.y, d.x) * (thick / 2.0)
		var a := p0 - d * over
		var b := p1 + d * over
		var c0 := [a + o, b + o, b - o, a - o]
		var up := Vector3.UP
		var lo := []
		var hi := []
		for q in c0:
			lo.append(Vector3((q as Vector2).x, z0, (q as Vector2).y))
			hi.append(Vector3((q as Vector2).x, z1, (q as Vector2).y))
		quad(hi[0], hi[1], hi[2], hi[3], up)
		for i in 4:
			var j := (i + 1) % 4
			var side := (c0[j] as Vector2) - (c0[i] as Vector2)
			var nrm := Vector3(side.y, 0, -side.x).normalized()
			quad(lo[i], lo[j], hi[j], hi[i], nrm)


static func build_scene(def: Dictionary) -> Node3D:
	var root := Node3D.new()
	root.name = "PolyDungeon"
	var poly: Dictionary = def.poly
	var rooms: Array = poly.rooms
	var cors: Array = poly.cors
	var walls := Builder.new()
	var floors := Builder.new()
	for k in rooms.size():
		var r: Dictionary = rooms[k]
		var c: Vector2 = r.c
		var n := int(r.n)
		var doors: Dictionary = r.doors
		for i in n:
			var v0 := _vert(r, i)
			var v1 := _vert(r, i + 1)
			var f0 := v0 + (v0 - c).normalized() * 0.4         # the floor runs on under the wall
			var f1 := v1 + (v1 - c).normalized() * 0.4
			floors.tri(Vector3(c.x, 0, c.y), Vector3(f0.x, 0, f0.y), Vector3(f1.x, 0, f1.y), Vector3.UP)
			if not doors.has(i):
				walls.slab(v0, v1, 0.0, WALL_H)
			else:
				var m := _mid(r, i)
				var t := (v1 - v0).normalized()
				var j0 := m - t * (DOOR_W / 2.0)
				var j1 := m + t * (DOOR_W / 2.0)
				walls.slab(v0, j0, 0.0, WALL_H, 0.15)
				walls.slab(j1, v1, 0.0, WALL_H, 0.15)
				walls.slab(j0, j1, DOOR_H, WALL_H, 0.0)        # lintel
	for cr in cors:
		var p0: Vector2 = cr.p0
		var p1: Vector2 = cr.p1
		var dir: Vector2 = cr.dir
		var o := Vector2(-dir.y, dir.x) * (CORR_W / 2.0)
		walls.slab(p0 + o, p1 + o, 0.0, WALL_H, 0.0)
		walls.slab(p0 - o, p1 - o, 0.0, WALL_H, 0.0)
		var a := p0 - dir * 0.2
		var b := p1 + dir * 0.2
		var oo := o * 0.98
		floors.quad(Vector3(a.x + oo.x, 0, a.y + oo.y), Vector3(b.x + oo.x, 0, b.y + oo.y), Vector3(b.x - oo.x, 0, b.y - oo.y), Vector3(a.x - oo.x, 0, a.y - oo.y), Vector3.UP)
	# a door leaf in every corridor's first doorway: origin = hinge, swings open when the player comes close (Dungeon._swing_doors)
	var dmat := StandardMaterial3D.new()
	dmat.resource_name = "LA_Door"
	dmat.albedo_color = Color(0.4, 0.28, 0.16)
	var leaf_w := DOOR_W - 0.1
	for k in cors.size():
		var cr: Dictionary = cors[k]
		var dir: Vector2 = cr.dir
		var tan_ := Vector2(-dir.y, dir.x)
		var hinge: Vector2 = (cr.p0 as Vector2) - tan_ * (DOOR_W / 2.0 - 0.05)
		var lb := Builder.new()
		lb.slab(Vector2.ZERO, Vector2(leaf_w, 0), 0.0, DOOR_H - 0.05, 0.0, 0.09)
		var leaf := MeshInstance3D.new()
		leaf.name = "Door_Panel_%d" % k
		leaf.mesh = lb.st.commit()
		leaf.mesh.surface_set_material(0, dmat)
		leaf.position = Vector3(hinge.x, 0, hinge.y)
		leaf.rotation.y = atan2(-tan_.y, tan_.x)
		root.add_child(leaf)
	var wmat := StandardMaterial3D.new()
	wmat.resource_name = "LA_Simple_Wall"
	wmat.albedo_color = Color(0.5, 0.48, 0.45)
	var fmat := StandardMaterial3D.new()
	fmat.resource_name = "LA_Floor_poly"
	fmat.albedo_color = Color(0.45, 0.42, 0.4)
	var wm := MeshInstance3D.new()
	wm.name = "Procedural_Level_Walls_poly"
	wm.mesh = walls.st.commit()
	wm.mesh.surface_set_material(0, wmat)
	root.add_child(wm)
	var fm := MeshInstance3D.new()
	fm.name = "Procedural_Level_Floor_poly"
	fm.mesh = floors.st.commit()
	fm.mesh.surface_set_material(0, fmat)
	root.add_child(fm)
	return root
