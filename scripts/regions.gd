class_name Regions
extends RefCounted
## Open-world regions: several outdoor scenes merged into one continuous landscape. Every member keeps its own data
## (props, NPCs, lights, journal entries) and is placed at a fixed centre; the ground, sea, camera and player are shared.
## Members are chosen per act (they are different location ids per chapter), so a chapter that needs no region simply has none.
## Cities (London) will use their own region with city-map style members.

const GAP := 6.0

const DEF := {
	"whitby": {
		"name": "Whitby", "sky": "day", "theme": "dock",
		"focus_ambient": "a2_east_cliff",
		"members": {"a2_harbour": Vector2(0, 0), "a2_east_cliff": Vector2(34, 0), "a2_abbey_ruins": Vector2(68, 0)},
		"links": [["a2_harbour", "a2_east_cliff"], ["a2_east_cliff", "a2_abbey_ruins"]],
		"overrides": {
			"a2_harbour": {"remove_props": ["a2_h_cliff1", "a2_h_cliff3", "a2_h_stairs"], "no_west_street": true, "quay_sides": ["south", "west"]},
		},
	},
	"hillingham": {
		"name": "Hillingham and the asylum", "sky": "dusk", "theme": "wild",
		"focus_ambient": "a3_hillingham_garden",
		"members": {"a3_hillingham_garden": Vector2(0, 0), "a3_asylum_garden": Vector2(18, -3), "a3_zoo_gardens": Vector2(41, 0), "a3_kingstead_churchyard": Vector2(0, 20)},
		"links": [["a3_hillingham_garden", "a3_asylum_garden"], ["a3_asylum_garden", "a3_zoo_gardens"], ["a3_hillingham_garden", "a3_kingstead_churchyard"]],
		"overrides": {},
	},
	"kingstead_night": {
		"name": "Hampstead by night", "sky": "night", "theme": "wild",
		"focus_ambient": "a4_kingstead_gate",
		"members": {"a4_hampstead_heath": Vector2(0, 0), "a4_heath_lane": Vector2(0, -24), "a4_kingstead_gate": Vector2(30, -24), "a4_kingstead_churchyard": Vector2(30, -52)},
		"links": [["a4_hampstead_heath", "a4_heath_lane"], ["a4_heath_lane", "a4_kingstead_gate"], ["a4_kingstead_gate", "a4_kingstead_churchyard"]],
		"overrides": {},
	},
	"purfleet": {
		"name": "The asylum and Carfax", "sky": "day", "theme": "wild",
		"focus_ambient": "a5_asylum_grounds",
		"members": {"a5_asylum_grounds": Vector2(0, 0), "a5_carfax_grounds": Vector2(0, -22)},
		"links": [["a5_asylum_grounds", "a5_carfax_grounds"]],
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


## Rects in region space (origin = centre of everything), members first, then the connecting strips.
static func layout(rid: String) -> Dictionary:
	var r: Dictionary = DEF[rid]
	var mn := Vector2(1e9, 1e9)
	var mx := Vector2(-1e9, -1e9)
	var rects := {}
	for m in r.members:
		var sz := size_of(m)
		var c: Vector2 = r.members[m]
		var rc := Rect2(c - sz / 2.0, sz)
		rects[m] = rc
		mn = mn.min(rc.position)
		mx = mx.max(rc.end)
	var origin := (mn + mx) / 2.0
	var out := {}
	for m in rects:
		var rc: Rect2 = rects[m]
		out[m] = Rect2(rc.position - origin, rc.size)
	var strips: Array = []
	for l in r.links:
		var a: Rect2 = out[l[0]]
		var b: Rect2 = out[l[1]]
		var ca := a.get_center()
		var cb := b.get_center()
		if absf(cb.x - ca.x) >= absf(cb.y - ca.y):
			var left := a if ca.x < cb.x else b
			var right := b if ca.x < cb.x else a
			var zc := (ca.y + cb.y) / 2.0
			strips.append(Rect2(left.end.x - 2.0, zc - 4.0, right.position.x - left.end.x + 4.0, 8.0))
		else:
			var top := a if ca.y < cb.y else b
			var bot := b if ca.y < cb.y else a
			var xc := (ca.x + cb.x) / 2.0
			strips.append(Rect2(xc - 4.0, top.end.y - 2.0, 8.0, bot.position.y - top.end.y + 4.0))
	return {"members": out, "strips": strips, "size": mx - mn, "origin": origin}
