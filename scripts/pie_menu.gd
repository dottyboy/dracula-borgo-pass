class_name PieMenu
extends Control
## Full Throttle style verb menu: click something and a ring of icons (eye, hand, mouth, ...) pops up around the cursor.

signal chosen(verb: String)
signal cancelled

const RING := 74.0
const BTN := 36.0
const PAGE := 6                  # more entries than this are split into pages (a "more" button cycles them)

var _verbs: Array = []
var _all: Array = []             # every entry when paged
var _page := 0
var _paged := false
var _ring := RING
var _title_lift := 0.0          # paged item rings put the names above the top button, so the title moves up
var _center := Vector2.ZERO
var _title := ""
var _hover := -1
var _t := 0.0


func open(pos: Vector2, title: String, verbs: Array) -> void:
	_all = verbs
	_page = 0
	_title = title
	var vs := get_viewport_rect().size
	_paged = verbs.size() > PAGE + 1 and str(verbs[0].id).begins_with("item:")      # only item lists are paged, never the verbs
	_ring = 100.0 if _paged else RING
	_title_lift = 26.0 if (not verbs.is_empty() and str(verbs[0].id).begins_with("item:")) else 0.0
	_center = Vector2(clampf(pos.x, _ring + BTN + 120, vs.x - _ring - BTN - 120), clampf(pos.y, _ring + BTN + 70, vs.y - _ring - BTN - 70))
	_apply_page()
	_hover = -1
	_t = 0.0
	visible = true
	mouse_filter = Control.MOUSE_FILTER_STOP
	queue_redraw()


## Shows one page of entries; with more than a page's worth the last button is "more" (next page, wrapping around).
func _apply_page() -> void:
	if not _paged:
		_verbs = _all
		return
	var pages := int(ceil(float(_all.size()) / float(PAGE)))
	_page = _page % pages
	_verbs = _all.slice(_page * PAGE, mini((_page + 1) * PAGE, _all.size()))
	_verbs = _verbs + [{"id": "__more", "label": "More (%d/%d)" % [_page + 1, pages]}]


func _pos_of(i: int) -> Vector2:
	var n := _verbs.size()
	var ang := PI + PI * i if n == 2 else -PI / 2.0 + TAU * i / float(n)
	return _center + Vector2.from_angle(ang) * _ring * minf(_t / 0.12, 1.0)


func _process(delta: float) -> void:
	if visible:
		_t += delta
		queue_redraw()


func _gui_input(ev: InputEvent) -> void:
	if ev is InputEventMouseMotion:
		_hover = -1
		for i in _verbs.size():
			if _pos_of(i).distance_to(ev.position) < BTN + 4.0:
				_hover = i
	elif ev is InputEventMouseButton and ev.pressed:
		if ev.button_index == MOUSE_BUTTON_LEFT:
			for i in _verbs.size():
				if _pos_of(i).distance_to(ev.position) < BTN + 4.0:
					if str(_verbs[i].id) == "__more":
						_page += 1
						_apply_page()
						_t = 0.12
						accept_event()
						return
					close()
					chosen.emit(str(_verbs[i].id))
					return
		close()
		cancelled.emit()
		accept_event()


func close() -> void:
	visible = false


func _draw() -> void:
	if not visible:
		return
	var font := ThemeDB.fallback_font
	var k := minf(_t / 0.12, 1.0)
	draw_circle(_center, 9.0, Color(0.95, 0.8, 0.35, 0.9))
	var tw := font.get_string_size(_title, HORIZONTAL_ALIGNMENT_LEFT, -1, 20).x
	draw_rect(Rect2(_center + Vector2(-tw / 2.0 - 8, -_ring - BTN - _title_lift - 34), Vector2(tw + 16, 28)), Color(0.07, 0.05, 0.04, 0.85))
	draw_string(font, _center + Vector2(-tw / 2.0, -_ring - BTN - _title_lift - 13), _title, HORIZONTAL_ALIGNMENT_LEFT, -1, 20, Color(0.96, 0.84, 0.5))
	for i in _verbs.size():
		var p := _pos_of(i)
		var hot := i == _hover
		var r := BTN * (1.12 if hot else 1.0) * k
		draw_line(_center, p, Color(0.95, 0.8, 0.35, 0.35), 2.0)
		draw_circle(p + Vector2(2, 3), r, Color(0, 0, 0, 0.45))
		draw_circle(p, r, Color(0.14, 0.1, 0.07, 0.95))
		var ring_col := Color(1.0, 0.85, 0.4) if hot else Color(0.7, 0.55, 0.28)
		if _verbs[i].has("color"):
			ring_col = (_verbs[i].color as Color).lightened(0.25 if hot else 0.0)
		draw_arc(p, r, 0, TAU, 32, ring_col, 4.0 if _verbs[i].has("color") else 3.0, true)
		var vid := str(_verbs[i].id)
		var gc := Color(1.0, 0.92, 0.6) if hot else Color(0.9, 0.78, 0.5)
		if vid.begins_with("item:"):                      # items have no icons: their initial, and the name beside the button
			var lab := str(_verbs[i].label)
			var ini := lab.substr(0, 1).to_upper()
			var iw := font.get_string_size(ini, HORIZONTAL_ALIGNMENT_LEFT, -1, 30).x
			draw_string(font, p + Vector2(-iw / 2.0, 10.0), ini, HORIZONTAL_ALIGNMENT_LEFT, -1, 30, gc)
			var dir := (p - _center).normalized() if p.distance_to(_center) > 1.0 else Vector2.DOWN
			var lw2 := font.get_string_size(lab, HORIZONTAL_ALIGNMENT_LEFT, -1, 17).x
			var lp := p + dir * (r + 8.0)
			var tx := lp.x - (lw2 if dir.x < -0.25 else (lw2 / 2.0 if absf(dir.x) <= 0.25 else 0.0))
			var ty := lp.y + (14.0 if dir.y > 0.5 else (0.0 if dir.y < -0.5 else 6.0))
			draw_rect(Rect2(Vector2(tx - 4, ty - 17), Vector2(lw2 + 8, 24)), Color(0.07, 0.05, 0.04, 0.88))
			draw_string(font, Vector2(tx, ty), lab, HORIZONTAL_ALIGNMENT_LEFT, -1, 17, Color(0.96, 0.84, 0.5) if hot else Color(0.85, 0.74, 0.5))
		elif vid == "__more":
			_glyph("go", p, r * 0.62, gc)
		else:
			_glyph(vid, p, r * 0.62, gc)
		if hot and not vid.begins_with("item:"):
			var lbl := str(_verbs[i].label)
			var lw := font.get_string_size(lbl, HORIZONTAL_ALIGNMENT_LEFT, -1, 18).x
			draw_rect(Rect2(p + Vector2(-lw / 2.0 - 6, r + 6), Vector2(lw + 12, 24)), Color(0.07, 0.05, 0.04, 0.9))
			draw_string(font, p + Vector2(-lw / 2.0, r + 24), lbl, HORIZONTAL_ALIGNMENT_LEFT, -1, 18, Color(0.96, 0.84, 0.5))


func _glyph(id: String, p: Vector2, s: float, c: Color) -> void:
	if id.begins_with("item"):
		id = "item"
	match id:
		"use":                                           # cog
			draw_circle(p, s * 0.62, c)
			draw_circle(p, s * 0.25, Color(0.14, 0.1, 0.07))
			for i in 8:
				var a := TAU * i / 8.0
				draw_line(p + Vector2.from_angle(a) * s * 0.6, p + Vector2.from_angle(a) * s * 0.95, c, 5.0)
		"item":                                          # satchel
			draw_rect(Rect2(p + Vector2(-s * 0.8, -s * 0.35), Vector2(s * 1.6, s * 1.1)), c)
			draw_arc(p + Vector2(0, -s * 0.35), s * 0.45, PI, TAU, 12, c, 3.0, true)
			draw_rect(Rect2(p + Vector2(-s * 0.15, -s * 0.1), Vector2(s * 0.3, s * 0.3)), Color(0.14, 0.1, 0.07))
		"map":                                           # folded map
			draw_colored_polygon(PackedVector2Array([p + Vector2(-s, -s * 0.7), p + Vector2(-s * 0.35, -s * 0.5), p + Vector2(s * 0.35, -s * 0.7), p + Vector2(s, -s * 0.5), p + Vector2(s, s * 0.7), p + Vector2(s * 0.35, s * 0.5), p + Vector2(-s * 0.35, s * 0.7), p + Vector2(-s, s * 0.5)]), c)
			draw_line(p + Vector2(-s * 0.35, -s * 0.5), p + Vector2(-s * 0.35, s * 0.7), Color(0.14, 0.1, 0.07), 2.0)
			draw_line(p + Vector2(s * 0.35, -s * 0.7), p + Vector2(s * 0.35, s * 0.5), Color(0.14, 0.1, 0.07), 2.0)
			draw_circle(p + Vector2(s * 0.55, s * 0.1), s * 0.12, Color(0.7, 0.15, 0.1))
		"look":                                          # eye
			var pts := PackedVector2Array()
			for i in 13:
				var u := float(i) / 12.0
				pts.append(p + Vector2(lerpf(-s, s, u), -sin(u * PI) * s * 0.55))
			for i in 13:
				var u := 1.0 - float(i) / 12.0
				pts.append(p + Vector2(lerpf(-s, s, u), sin(u * PI) * s * 0.55))
			draw_polyline(pts, c, 2.5, true)
			draw_circle(p, s * 0.36, c)
			draw_circle(p + Vector2(-s * 0.1, -s * 0.1), s * 0.12, Color(0.14, 0.1, 0.07))
		"take", "use":                                   # hand
			draw_rect(Rect2(p + Vector2(-s * 0.55, -s * 0.05), Vector2(s * 1.1, s * 0.85)), c)
			for i in 4:
				var fx := -s * 0.55 + i * s * 0.3
				draw_rect(Rect2(p + Vector2(fx, -s * (0.9 - (0.15 if i in [1, 2] else 0.0))), Vector2(s * 0.22, s * 0.95)), c)
			draw_colored_polygon(PackedVector2Array([p + Vector2(-s * 0.55, s * 0.25), p + Vector2(-s * 0.95, -s * 0.15), p + Vector2(-s * 0.8, -s * 0.3), p + Vector2(-s * 0.4, 0.0)]), c)
		"talk":                                          # mouth
			var top := PackedVector2Array()
			for i in 11:
				var u := float(i) / 10.0
				top.append(p + Vector2(lerpf(-s, s, u), -sin(u * PI) * s * 0.5 + s * 0.1))
			var bottom := PackedVector2Array()
			for i in 11:
				var u := 1.0 - float(i) / 10.0
				bottom.append(p + Vector2(lerpf(-s, s, u), sin(u * PI) * s * 0.6 + s * 0.1))
			draw_colored_polygon(top + bottom, Color(0.75, 0.2, 0.2))
			draw_polyline(top + bottom, c, 2.5, true)
			draw_line(p + Vector2(-s, s * 0.1), p + Vector2(s, s * 0.1), c, 2.0)
		"go":                                            # arrow
			draw_colored_polygon(PackedVector2Array([p + Vector2(s, 0), p + Vector2(0, -s * 0.8), p + Vector2(0, -s * 0.3), p + Vector2(-s, -s * 0.3), p + Vector2(-s, s * 0.3), p + Vector2(0, s * 0.3), p + Vector2(0, s * 0.8)]), c)
		"attack":                                        # crossed blades
			draw_line(p + Vector2(-s, -s), p + Vector2(s, s), c, 4.0)
			draw_line(p + Vector2(s, -s), p + Vector2(-s, s), c, 4.0)
			draw_circle(p, s * 0.2, c)
		_:
			draw_circle(p, s * 0.5, c)
