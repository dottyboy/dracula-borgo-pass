class_name TravelMap
extends Control
## Overworld map (Monkey Island style): the open-air places connected to the current one, laid out from where
## their exits actually lie. Opened by walking off the open edge of a scene or with the T key.

signal travel(to: String)
signal closed

const R := 22.0
const STEP := 190.0

var _pos: Dictionary = {}          # id -> Vector2 (screen)
var _edges: Array = []             # [a, b]
var _from_here: Dictionary = {}    # id -> {cond, fail} for exits usable from the current place
var _names: Dictionary = {}
var _cur := ""
var _hover := ""
var _interior: Dictionary = {}
var _sep := 120.0
var _city := false                 # London: street plan instead of countryside
var _blocks: Array = []            # Rect2 building blocks (city style)
var _land: Array = []              # PackedVector2Array blobs
var _roads: Array = []             # PackedVector2Array curves
var _decor: Array = []             # [kind, pos, scale, variant]
var _t := 0.0


## Exterior neighbours of `id` through go-props, with the direction of each exit inside the scene.
static func exits_of(id: String, with_interior := false) -> Dictionary:
	var out := {}
	var ld: Dictionary = Game.resolved.locations.get(id, {})
	for p in ld.get("props", []):
		var it: Dictionary = p.get("interact", {})
		var to := str(it.get("go", ""))
		if to == "" or not Game.resolved.locations.has(to) or (Game.resolved.locations[to].get("interior", true) and not with_interior):
			continue
		if not out.has(to):
			out[to] = {"dir": Vector2(float(p.pos[0]), float(p.pos[2])), "cond": str(it.get("go_cond", "")), "fail": str(it.get("go_fail", ""))}
	return out


static func has_map(id: String) -> bool:
	var ld: Dictionary = Game.resolved.locations.get(id, {})
	return not ld.get("interior", true) and not exits_of(id).is_empty()


func open(cur: String) -> void:
	_cur = cur
	_sep = 200.0 if (cur.contains("london") or cur.contains("bloxam")) else 120.0
	_interior.clear()
	_names.clear()
	for l in Game.world.locations:
		_names[str(l.id)] = str(l.name)
	var adj := {}          # undirected, with a direction per directed edge
	var dirs := {}
	var queue := [cur]
	var seen := {cur: 0}
	while not queue.is_empty():
		var a: String = queue.pop_front()
		var ex := exits_of(a, true)
		for b in ex:
			if Game.resolved.locations[b].get("interior", true):
				_interior[b] = true
				if not adj.has(a): adj[a] = []
				if not adj.has(b): adj[b] = []
				adj[a].append(b)
				adj[b].append(a)
				dirs["%s>%s" % [a, b]] = (ex[b].dir as Vector2)
				seen[b] = seen[a] + 1
				continue
			dirs["%s>%s" % [a, b]] = (ex[b].dir as Vector2)
			if not adj.has(a): adj[a] = []
			if not adj.has(b): adj[b] = []
			if not adj[a].has(b): adj[a].append(b)
			if not adj[b].has(a): adj[b].append(a)
			if not seen.has(b) and seen[a] < 4:
				seen[b] = seen[a] + 1
				queue.append(b)
	_from_here = exits_of(cur, true)
	# initial placement from exit directions
	var ids: Array = seen.keys()
	_pos = {cur: Vector2.ZERO}
	var order := [cur]
	var i := 0
	while i < order.size():
		var a: String = order[i]
		i += 1
		for b in adj.get(a, []):
			if _pos.has(b) or not seen.has(b):
				continue
			var d: Vector2 = dirs.get("%s>%s" % [a, b], Vector2.ZERO)
			if d == Vector2.ZERO:
				d = -(dirs.get("%s>%s" % [b, a], Vector2(0, 1)) as Vector2)
			if d.length() < 0.1:
				d = Vector2(1, 0)
			var jitter := Vector2(((hash(b) % 100) - 50) * 0.4, ((hash(b + "z") % 100) - 50) * 0.4)
			_pos[b] = _pos[a] + d.normalized() * STEP + jitter
			order.append(b)
	_edges.clear()
	for a in adj:
		for b in adj[a]:
			if seen.has(a) and seen.has(b) and str(a) < str(b):
				_edges.append([a, b])
	for it in 80:                               # relax: keep apart, keep edges near STEP
		for a in ids:
			for b in ids:
				if a == b or not _pos.has(a) or not _pos.has(b):
					continue
				var dv: Vector2 = _pos[a] - _pos[b]
				var dl := maxf(dv.length(), 1.0)
				if dl < _sep:
					_pos[a] += dv / dl * (_sep - dl) * 0.15
		for e in _edges:
			var dv2: Vector2 = _pos[e[1]] - _pos[e[0]]
			var dl2 := maxf(dv2.length(), 1.0)
			var f := (dl2 - STEP) * 0.05
			_pos[e[0]] += dv2 / dl2 * f
			_pos[e[1]] -= dv2 / dl2 * f
		_pos[cur] = _pos[cur].lerp(Vector2.ZERO, 0.0)
	# fit to the screen
	var mn := Vector2(1e9, 1e9)
	var mx := Vector2(-1e9, -1e9)
	for k in _pos:
		mn = mn.min(_pos[k])
		mx = mx.max(_pos[k])
	var size_v := get_viewport_rect().size
	var avail := size_v - Vector2(420, 340)
	var span := (mx - mn).max(Vector2(1, 1))
	var sc := minf(1.6, minf(avail.x / span.x, avail.y / span.y))
	for k in _pos:
		_pos[k] = size_v / 2.0 + ((_pos[k] - (mn + mx) / 2.0) * sc)
	_city = cur.contains("london") or cur.contains("bloxam")
	_build_scenery()
	visible = true
	mouse_filter = Control.MOUSE_FILTER_STOP
	queue_redraw()


func _rng_of(s: String) -> RandomNumberGenerator:
	var r := RandomNumberGenerator.new()
	r.seed = hash(s)
	return r


func _blob(c: Vector2, rad: float, key: String) -> PackedVector2Array:
	var r := _rng_of(key)
	var ph := [r.randf() * 6.28, r.randf() * 6.28, r.randf() * 6.28]
	var pts := PackedVector2Array()
	for i in 56:
		var a := TAU * i / 56.0
		var k := 1.0 + 0.16 * sin(a * 3.0 + ph[0]) + 0.09 * sin(a * 5.0 + ph[1]) + 0.05 * sin(a * 9.0 + ph[2])
		pts.append(c + Vector2(cos(a), sin(a)) * rad * k)
	return pts


func _curve(a: Vector2, b: Vector2, key: String) -> PackedVector2Array:
	var r := _rng_of(key)
	var n := (b - a).orthogonal().normalized()
	var mid := (a + b) / 2.0 + n * r.randf_range(-0.18, 0.18) * a.distance_to(b)
	var pts := PackedVector2Array()
	for i in 21:
		var u := i / 20.0
		pts.append(a.lerp(mid, u).lerp(mid.lerp(b, u), u))
	return pts


func _near_road(p: Vector2, margin: float) -> bool:
	for rd in _roads:
		for q in rd:
			if q.distance_to(p) < margin:
				return true
	return false


func _build_city() -> void:
	_blocks.clear()
	var s := get_viewport_rect().size
	var m := Rect2(90, 70, s.x - 180, s.y - 150)
	var r := _rng_of("city")
	var y := m.position.y + 16
	while y < m.end.y - 60:
		var h := r.randf_range(46, 78)
		var x := m.position.x + 16
		while x < m.end.x - 40:
			var w := r.randf_range(50, 120)
			var rc := Rect2(x, y, minf(w, m.end.x - 20 - x), h)
			var clear := true
			for k in _pos:
				if rc.grow(26).has_point(_pos[k]):
					clear = false
			for rd in _roads:
				for q in rd:
					if rc.grow(16).has_point(q):
						clear = false
						break
				if not clear:
					break
			if clear and rc.position.y + rc.size.y < m.end.y - 50:
				_blocks.append(rc)
			x += w + 22
		y += h + 22


func _build_scenery() -> void:
	_land.clear()
	_roads.clear()
	_decor.clear()
	if _city:
		for e in _edges:
			_roads.append(_curve(_pos[e[0]], _pos[e[1]], e[0] + e[1]))
		_build_city()
		return
	for k in _pos:
		_land.append(_blob(_pos[k], 118.0 if not _interior.has(k) else 70.0, k))
	for e in _edges:
		_roads.append(_curve(_pos[e[0]], _pos[e[1]], e[0] + e[1]))
	for k in _pos:
		var c: Vector2 = _pos[k]
		var theme: String = Dressing.theme_of(k, bool(Game.resolved.locations[k].get("interior", true)))
		if _interior.has(k):
			continue
		var r := _rng_of("d" + k)
		var count := 10
		for i in count:
			var p := c + Vector2.from_angle(r.randf() * TAU) * r.randf_range(38.0, 105.0)
			if _near_road(p, 16.0):
				continue
			var kind := "tree"
			if theme in ["dock", "street"]:
				kind = "house" if r.randf() < 0.65 else "tree"
			elif theme == "graveyard":
				kind = "cross" if r.randf() < 0.6 else "tree"
			elif theme == "wild" and r.randf() < 0.3:
				kind = "rock"
			_decor.append([kind, p, r.randf_range(0.8, 1.2), r.randi() % 3])
		if str(k).contains("abbey"):
			_decor.append(["ruin", c + Vector2(0, -52), 1.4, 0])
		if str(k).contains("harbour") or str(k).contains("quay") or str(k).contains("pier"):
			_decor.append(["boat", c + Vector2(-95, 40), 1.0, 0])
			_decor.append(["boat", c + Vector2(-70, 80), 0.8, 1])


func _process(delta: float) -> void:
	if visible:
		_t += delta
		queue_redraw()


func _known(id: String) -> bool:
	return id == _cur or Game.visited.has(id)


func _at(p: Vector2) -> String:
	for k in _pos:
		if (_pos[k] as Vector2).distance_to(p) < R + 8.0:
			return k
	return ""


func _gui_input(ev: InputEvent) -> void:
	if ev is InputEventMouseMotion:
		_hover = _at(ev.position)
	elif ev is InputEventMouseButton and ev.pressed and ev.button_index == MOUSE_BUTTON_LEFT:
		var k := _at(ev.position)
		if k == "" or k == _cur:
			if k == "" and ev.position.y > size.y - 70:
				close()
			return
		if not _from_here.has(k):
			Game.message.emit("There is no direct way from here.")
			return
		var ex: Dictionary = _from_here[k]
		if not Game.check(str(ex.cond)):
			Game.message.emit(str(ex.fail) if str(ex.fail) != "" else "The way is blocked.")
			return
		close()
		travel.emit(k)


func close() -> void:
	visible = false
	closed.emit()


func _draw_decor(d: Array) -> void:
	var p: Vector2 = d[1]
	var s: float = d[2]
	match d[0]:
		"tree":
			draw_circle(p + Vector2(2, 3) * s, 9 * s, Color(0.12, 0.2, 0.1, 0.45))
			draw_circle(p, 8.5 * s, Color(0.2, 0.38, 0.16))
			draw_circle(p + Vector2(-2, -2) * s, 5 * s, Color(0.3, 0.5, 0.22))
		"house":
			var roof: Color = [Color(0.62, 0.28, 0.2), Color(0.38, 0.38, 0.42), Color(0.5, 0.3, 0.22)][d[3]]
			draw_rect(Rect2(p + Vector2(-9, -6) * s + Vector2(2, 3), Vector2(18, 14) * s), Color(0.1, 0.1, 0.05, 0.4))
			draw_rect(Rect2(p + Vector2(-9, -6) * s, Vector2(18, 14) * s), Color(0.9, 0.84, 0.66))
			draw_colored_polygon(PackedVector2Array([p + Vector2(-11, -6) * s, p + Vector2(0, -15) * s, p + Vector2(11, -6) * s]), roof)
		"cross":
			draw_rect(Rect2(p + Vector2(-1.5, -8) * s, Vector2(3, 14) * s), Color(0.55, 0.55, 0.55))
			draw_rect(Rect2(p + Vector2(-5, -5) * s, Vector2(10, 3) * s), Color(0.55, 0.55, 0.55))
		"rock":
			draw_circle(p, 6 * s, Color(0.45, 0.45, 0.43))
			draw_circle(p + Vector2(-1.5, -1.5) * s, 3.5 * s, Color(0.6, 0.6, 0.58))
		"ruin":
			var c := Color(0.72, 0.7, 0.64)
			draw_rect(Rect2(p + Vector2(-26, -4) * s, Vector2(8, 26) * s), c)
			draw_rect(Rect2(p + Vector2(18, -4) * s, Vector2(8, 26) * s), c)
			draw_rect(Rect2(p + Vector2(-18, -14) * s, Vector2(36, 7) * s), c)
			draw_rect(Rect2(p + Vector2(-4, 2) * s, Vector2(8, 20) * s), Color(0.72, 0.7, 0.64, 0.0))
		"boat":
			draw_colored_polygon(PackedVector2Array([p + Vector2(-12, 0) * s, p + Vector2(12, 0) * s, p + Vector2(8, 6) * s, p + Vector2(-8, 6) * s]), Color(0.4, 0.26, 0.15))
			draw_line(p + Vector2(0, 0), p + Vector2(0, -14) * s, Color(0.3, 0.2, 0.1), 2.0)
			draw_colored_polygon(PackedVector2Array([p + Vector2(1, -13) * s, p + Vector2(9, -3) * s, p + Vector2(1, -3) * s]), Color(0.95, 0.93, 0.85))


func _draw_city(m: Rect2) -> void:
	var font := ThemeDB.fallback_font
	draw_rect(m, Color(0.86, 0.82, 0.72))
	# the Thames along the bottom
	var river := PackedVector2Array()
	for i in 41:
		var u := i / 40.0
		river.append(Vector2(m.position.x + u * m.size.x, m.end.y - 34 + sin(u * 7.0) * 14.0))
	draw_polyline(river, Color(0.45, 0.6, 0.68), 46.0, true)
	for b in _blocks:
		draw_rect(Rect2(b.position + Vector2(3, 4), b.size), Color(0.35, 0.3, 0.25, 0.35))
		draw_rect(b, Color(0.7, 0.62, 0.52))
		draw_rect(b.grow(-5), Color(0.62, 0.52, 0.44))
		draw_rect(b, Color(0.4, 0.32, 0.25), false, 2.0)
	for e in _roads:
		draw_polyline(e, Color(0.4, 0.4, 0.42), 24.0, true)
		draw_polyline(e, Color(0.62, 0.62, 0.64), 18.0, true)
	draw_rect(m, Color(0.32, 0.2, 0.1), false, 5.0)
	draw_string(font, Vector2(m.position.x + 24, m.position.y + 40), "London", HORIZONTAL_ALIGNMENT_LEFT, -1, 28, Color(0.15, 0.1, 0.06))
	_draw_nodes(m, font)


func _draw() -> void:
	var s := get_viewport_rect().size
	draw_rect(Rect2(Vector2.ZERO, s), Color(0.05, 0.04, 0.03, 0.88))
	var m := Rect2(90, 70, s.x - 180, s.y - 150)
	if _city:
		_draw_city(m)
		return
	# sea
	draw_rect(m, Color(0.42, 0.6, 0.66))
	var wr := _rng_of("waves")
	for i in 60:
		var q := m.position + Vector2(wr.randf() * m.size.x, wr.randf() * m.size.y)
		draw_line(q, q + Vector2(14, 0), Color(0.62, 0.78, 0.82), 2.0)
		draw_line(q + Vector2(14, 0), q + Vector2(20, -3), Color(0.62, 0.78, 0.82), 2.0)
	# land: shore, then grass; roads widen the land between places
	for e in _roads:
		draw_polyline(e, Color(0.78, 0.74, 0.5), 112.0, true)
	for b in _land:
		draw_colored_polygon(b, Color(0.78, 0.74, 0.5))
	for e in _roads:
		draw_polyline(e, Color(0.5, 0.64, 0.34), 96.0, true)
	for b in _land:
		var inner := PackedVector2Array()
		var c := Vector2.ZERO
		for p in b:
			c += p
		c /= b.size()
		for p in b:
			inner.append(c + (p - c) * 0.93)
		draw_colored_polygon(inner, Color(0.5, 0.64, 0.34))
	for e in _roads:
		draw_polyline(e, Color(0.4, 0.28, 0.16), 9.0, true)
		draw_polyline(e, Color(0.8, 0.68, 0.46), 5.5, true)
	_decor.sort_custom(func(a: Array, b: Array) -> bool: return a[1].y < b[1].y)
	for d in _decor:
		_draw_decor(d)
	draw_rect(m, Color(0.32, 0.2, 0.1), false, 5.0)
	var font := ThemeDB.fallback_font
	draw_string(font, Vector2(m.position.x + 24, m.position.y + 40), "The Neighbourhood", HORIZONTAL_ALIGNMENT_LEFT, -1, 28, Color(0.15, 0.1, 0.06), -1)
	_draw_nodes(m, font)


func _draw_nodes(m: Rect2, font: Font) -> void:
	for k in _pos:
		var p: Vector2 = _pos[k]
		var known := _known(k)
		var rr := R + (3.0 * sin(_t * 4.0) if k == _cur else 0.0) + (4.0 if k == _hover else 0.0)
		if _interior.has(k):
			var rf := Color(0.62, 0.28, 0.2) if known else Color(0.5, 0.45, 0.4)
			draw_rect(Rect2(p + Vector2(-14, -8), Vector2(28, 22)), Color(0.92, 0.86, 0.68))
			draw_colored_polygon(PackedVector2Array([p + Vector2(-18, -8), p + Vector2(0, -24), p + Vector2(18, -8)]), rf)
			draw_rect(Rect2(p + Vector2(-4, 2), Vector2(8, 12)), Color(0.3, 0.2, 0.12))
			if k == _hover:
				draw_arc(p, 30.0, 0, TAU, 24, Color(1, 1, 1, 0.9), 2.5)
		else:
			var col := Color(0.7, 0.12, 0.1) if k == _cur else (Color(0.95, 0.85, 0.35) if known else Color(0.7, 0.68, 0.62))
			draw_circle(p, rr + 3, Color(0.2, 0.1, 0.05))
			draw_circle(p, rr, col)
			draw_circle(p, rr * 0.35, Color(0.2, 0.1, 0.05))
		var label: String = str(_names.get(k, k)) if known else "?"
		var w := font.get_string_size(label, HORIZONTAL_ALIGNMENT_LEFT, -1, 18).x
		var lp := p + Vector2(-w / 2.0, R + 26)
		draw_rect(Rect2(lp + Vector2(-5, -17), Vector2(w + 10, 24)), Color(0.93, 0.87, 0.7, 0.85))
		draw_string(font, lp, label, HORIZONTAL_ALIGNMENT_LEFT, -1, 18, Color(0.2, 0.1, 0.05))
		if k == _cur:
			draw_string(font, p + Vector2(-13, -rr - 8), "You", HORIZONTAL_ALIGNMENT_LEFT, -1, 14, Color(0.15, 0.05, 0.03))
	draw_string(font, Vector2(m.position.x + 24, m.end.y - 16), "Click a place to walk there.   T / Esc / click here to close.", HORIZONTAL_ALIGNMENT_LEFT, -1, 16, Color(0.15, 0.1, 0.06))
