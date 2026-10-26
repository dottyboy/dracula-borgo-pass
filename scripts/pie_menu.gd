class_name PieMenu
extends Control
## Full Throttle style verb menu: click something and a ring of icons (eye, hand, mouth, ...) pops up around the cursor.

signal chosen(verb: String)
signal cancelled

const RING := 74.0
const BTN := 36.0

var _verbs: Array = []
var _center := Vector2.ZERO
var _title := ""
var _hover := -1
var _t := 0.0


func open(pos: Vector2, title: String, verbs: Array) -> void:
	_verbs = verbs
	_title = title
	var vs := get_viewport_rect().size
	_center = Vector2(clampf(pos.x, RING + BTN + 10, vs.x - RING - BTN - 10), clampf(pos.y, RING + BTN + 30, vs.y - RING - BTN - 60))
	_hover = -1
	_t = 0.0
	visible = true
	mouse_filter = Control.MOUSE_FILTER_STOP
	queue_redraw()


func _pos_of(i: int) -> Vector2:
	var n := _verbs.size()
	var ang := PI + PI * i if n == 2 else -PI / 2.0 + TAU * i / float(n)
	return _center + Vector2.from_angle(ang) * RING * minf(_t / 0.12, 1.0)


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
	draw_rect(Rect2(_center + Vector2(-tw / 2.0 - 8, -RING - BTN - 34), Vector2(tw + 16, 28)), Color(0.07, 0.05, 0.04, 0.85))
	draw_string(font, _center + Vector2(-tw / 2.0, -RING - BTN - 13), _title, HORIZONTAL_ALIGNMENT_LEFT, -1, 20, Color(0.96, 0.84, 0.5))
	for i in _verbs.size():
		var p := _pos_of(i)
		var hot := i == _hover
		var r := BTN * (1.12 if hot else 1.0) * k
		draw_line(_center, p, Color(0.95, 0.8, 0.35, 0.35), 2.0)
		draw_circle(p + Vector2(2, 3), r, Color(0, 0, 0, 0.45))
		draw_circle(p, r, Color(0.14, 0.1, 0.07, 0.95))
		draw_arc(p, r, 0, TAU, 32, Color(1.0, 0.85, 0.4) if hot else Color(0.7, 0.55, 0.28), 3.0, true)
		_glyph(str(_verbs[i].id), p, r * 0.62, Color(1.0, 0.92, 0.6) if hot else Color(0.9, 0.78, 0.5))
		if hot:
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
