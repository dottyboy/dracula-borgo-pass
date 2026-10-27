class_name Regions
extends RefCounted
## Open-world regions: several outdoor scenes merged into one continuous landscape. Every member keeps its own data
## (props, NPCs, lights, journal entries) and is placed at a fixed centre; the ground, sea, camera and player are shared.
## Members are chosen per act (they are different location ids per chapter), so a chapter that needs no region simply has none.
## Cities (London) will use their own region with city-map style members.

## Link info (third element of a link): kind = road | park | forest | stairs, gap = clear distance between the two scenes in
## metres, width = width of the connecting land. `heights` = ground level of each member (the connector ramps between them;
## "stairs" links climb in steps).
const DEF := {
	"whitby": {
		"name": "Whitby", "sky": "day", "theme": "dock",
		"focus_ambient": "a2_east_cliff",
		"members": {"a2_harbour": Vector2(0, 0), "a2_east_cliff": Vector2(34, 0), "a2_abbey_ruins": Vector2(68, 0)},
		"heights": {"a2_harbour": 0.0, "a2_east_cliff": 9.0, "a2_abbey_ruins": 10.5},
		"links": [["a2_harbour", "a2_east_cliff", {"kind": "stairs", "gap": 34.0, "width": 9.0}],
			["a2_east_cliff", "a2_abbey_ruins", {"kind": "park", "gap": 24.0, "width": 22.0}]],
		"overrides": {
			"a2_harbour": {"remove_props": ["a2_h_cliff1", "a2_h_cliff3", "a2_h_stairs"], "no_west_street": true, "quay_sides": ["south", "west"]},
			"a2_east_cliff": {"remove_props": ["a2_c_steps"]},
			"a2_abbey_ruins": {"remove_props": ["a2_a_steps"]},
		},
	},
	"hillingham": {
		"name": "Hillingham and the asylum", "sky": "dusk", "theme": "wild",
		"focus_ambient": "a3_hillingham_garden",
		"members": {"a3_hillingham_garden": Vector2(0, 0), "a3_asylum_garden": Vector2(18, -3), "a3_zoo_gardens": Vector2(41, 0), "a3_kingstead_churchyard": Vector2(0, 20)},
		"heights": {"a3_kingstead_churchyard": 1.5},
		"links": [["a3_hillingham_garden", "a3_asylum_garden", {"kind": "road", "gap": 20.0, "width": 14.0}],
			["a3_asylum_garden", "a3_zoo_gardens", {"kind": "park", "gap": 22.0, "width": 22.0}],
			["a3_hillingham_garden", "a3_kingstead_churchyard", {"kind": "forest", "gap": 20.0, "width": 18.0}]],
		"overrides": {},
	},
	"kingstead_night": {
		"name": "Hampstead by night", "sky": "night", "theme": "wild",
		"focus_ambient": "a4_kingstead_gate",
		"members": {"a4_hampstead_heath": Vector2(0, 0), "a4_heath_lane": Vector2(0, -24), "a4_kingstead_gate": Vector2(30, -24), "a4_kingstead_churchyard": Vector2(30, -52)},
		"heights": {"a4_heath_lane": 1.0, "a4_kingstead_gate": 2.0, "a4_kingstead_churchyard": 2.0},
		"links": [["a4_hampstead_heath", "a4_heath_lane", {"kind": "forest", "gap": 22.0, "width": 16.0}],
			["a4_heath_lane", "a4_kingstead_gate", {"kind": "road", "gap": 22.0, "width": 12.0}],
			["a4_kingstead_gate", "a4_kingstead_churchyard", {"kind": "road", "gap": 12.0, "width": 10.0}]],
		"overrides": {},
	},
	"purfleet": {
		"name": "The asylum and Carfax", "sky": "day", "theme": "wild",
		"focus_ambient": "a5_asylum_grounds",
		"members": {"a5_asylum_grounds": Vector2(0, 0), "a5_carfax_grounds": Vector2(0, -22)},
		"heights": {"a5_carfax_grounds": 1.0},
		"links": [["a5_asylum_grounds", "a5_carfax_grounds", {"kind": "road", "gap": 24.0, "width": 14.0}]],
		"overrides": {},
	},
}


static func region_of(loc_id: String) -> String:
	for rid in DEF:
		if DEF[rid].members.has(loc_id):
			return rid
	return ""


static func enabled() -> bool:
	return Game.autosave or Game.force_regions


## Member size in metres, including the automatic widening of open scenes.
static func size_of(loc_id: String) -> Vector2:
	var d: Dictionary = Game.loc_data(loc_id)
	var g := Location.grow_for(loc_id, d)
	return Vector2(float(d.cells[0]) * Location.CELL + 2.0 * g.x, float(d.cells[1]) * Location.CELL + 2.0 * g.y)


## Rects in region space (origin = centre of everything), members first, then the connecting strips. Also the link table
## (axis, edges, heights) and the member heights used by `height_at`.
static func layout(rid: String) -> Dictionary:
	var r: Dictionary = DEF[rid]
	var rects := {}
	for m in r.members:
		var sz := size_of(m)
		rects[m] = Rect2((r.members[m] as Vector2) - sz / 2.0, sz)
	# spread the scenes so that every link has its requested clear gap (the far side of the link moves, with everything behind it)
	for lk in r.links:
		var info: Dictionary = lk[2] if lk.size() > 2 else {}
		if not info.has("gap"):
			continue
		var a: Rect2 = rects[lk[0]]
		var b: Rect2 = rects[lk[1]]
		var d := b.get_center() - a.get_center()
		var shift := Vector2.ZERO
		if absf(d.x) >= absf(d.y):
			shift.x = (float(info.gap) - (b.position.x - a.end.x)) if d.x > 0 else -(float(info.gap) - (a.position.x - b.end.x))
		else:
			shift.y = (float(info.gap) - (b.position.y - a.end.y)) if d.y > 0 else -(float(info.gap) - (a.position.y - b.end.y))
		for m in _behind(r, lk[0], lk[1]):
			rects[m] = Rect2((rects[m] as Rect2).position + shift, (rects[m] as Rect2).size)
	var strips_raw: Array = []
	var links_raw: Array = []
	for lk in r.links:
		var info: Dictionary = lk[2] if lk.size() > 2 else {}
		var width := float(info.get("width", 8.0))
		var a: Rect2 = rects[lk[0]]
		var b: Rect2 = rects[lk[1]]
		var ca := a.get_center()
		var cb := b.get_center()
		var ha := float(r.get("heights", {}).get(lk[0], 0.0))
		var hb := float(r.get("heights", {}).get(lk[1], 0.0))
		var entry := {"a": lk[0], "b": lk[1], "kind": str(info.get("kind", "road")), "ha": ha, "hb": hb, "width": width}
		if absf(cb.x - ca.x) >= absf(cb.y - ca.y):
			var zc := (ca.y + cb.y) / 2.0
			var ea := a.end.x if cb.x > ca.x else a.position.x
			var eb := b.position.x if cb.x > ca.x else b.end.x
			var x0 := minf(ea, eb) - 2.0
			var x1 := maxf(ea, eb) + 2.0
			strips_raw.append(Rect2(x0, zc - width / 2.0, x1 - x0, width))
			entry.merge({"axis": 0, "ea": ea, "eb": eb, "mid": zc})
		else:
			var xc := (ca.x + cb.x) / 2.0
			var ea := a.end.y if cb.y > ca.y else a.position.y
			var eb := b.position.y if cb.y > ca.y else b.end.y
			var y0 := minf(ea, eb) - 2.0
			var y1 := maxf(ea, eb) + 2.0
			strips_raw.append(Rect2(xc - width / 2.0, y0, width, y1 - y0))
			entry.merge({"axis": 1, "ea": ea, "eb": eb, "mid": xc})
		links_raw.append(entry)
	var mn := Vector2(1e9, 1e9)
	var mx := Vector2(-1e9, -1e9)
	for rc in rects.values() + strips_raw:
		mn = mn.min((rc as Rect2).position)
		mx = mx.max((rc as Rect2).end)
	var origin := (mn + mx) / 2.0
	var out := {}
	for m in rects:
		out[m] = Rect2((rects[m] as Rect2).position - origin, (rects[m] as Rect2).size)
	var strips: Array = []
	for sr in strips_raw:
		strips.append(Rect2((sr as Rect2).position - origin, (sr as Rect2).size))
	for e in links_raw:
		e.ea = float(e.ea) - (origin.x if int(e.axis) == 0 else origin.y)
		e.eb = float(e.eb) - (origin.x if int(e.axis) == 0 else origin.y)
		e.mid = float(e.mid) - (origin.y if int(e.axis) == 0 else origin.x)
	return {"members": out, "strips": strips, "size": mx - mn, "origin": origin, "links": links_raw,
		"heights": r.get("heights", {}).duplicate()}


## Members on the far side of link a-b (b and everything reachable from b without crossing a).
static func _behind(r: Dictionary, a: String, b: String) -> Array:
	var seen := {b: true}
	var queue := [b]
	while not queue.is_empty():
		var cur: String = queue.pop_front()
		for lk in r.links:
			var other := ""
			if lk[0] == cur:
				other = lk[1]
			elif lk[1] == cur:
				other = lk[0]
			if other == "" or other == a or seen.has(other):
				continue
			seen[other] = true
			queue.append(other)
	return seen.keys()


## Ground level at a point of region space: flat inside each scene, a ramp (or flight of steps) along each connecting strip,
## blended smoothly outside.
static func height_at(lay: Dictionary, p: Vector2) -> float:
	var num := 0.0
	var den := 0.0
	var hs: Dictionary = lay.heights
	for m in lay.members:
		var rc: Rect2 = lay.members[m]
		var d := Vector2(maxf(maxf(rc.position.x - p.x, p.x - rc.end.x), 0.0), maxf(maxf(rc.position.y - p.y, p.y - rc.end.y), 0.0)).length()
		var w := 1.0 / pow(0.3 + d * d, 2.0)
		num += float(hs.get(m, 0.0)) * w
		den += w
	for i in lay.links.size():
		var e: Dictionary = lay.links[i]
		var rc: Rect2 = lay.strips[i]
		var d := Vector2(maxf(maxf(rc.position.x - p.x, p.x - rc.end.x), 0.0), maxf(maxf(rc.position.y - p.y, p.y - rc.end.y), 0.0)).length()
		var c := p.x if int(e.axis) == 0 else p.y
		var u := clampf((c - float(e.ea)) / (float(e.eb) - float(e.ea)), 0.0, 1.0)
		var hv := float(e.ha) + (float(e.hb) - float(e.ha)) * _ramp(u, str(e.kind), absf(float(e.hb) - float(e.ha)))
		var w := 1.0 / pow(0.3 + d * d, 2.0)
		num += hv * w
		den += w
	return num / den


static func _ramp(u: float, kind: String, rise: float) -> float:
	if kind == "stairs" and rise > 0.4:
		var n := ceilf(rise / 0.3)
		var f := u * n
		var tread := floorf(f)
		var riser := smoothstep(0.7, 1.0, f - tread)
		return minf((tread + riser) / n, 1.0)
	return smoothstep(0.0, 1.0, u)


