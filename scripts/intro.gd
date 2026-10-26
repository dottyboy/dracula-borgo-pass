class_name Intro
extends Control
## Opening titles: a slow night dolly towards the castle (moonlit sky, mist, pines, bats, the Count with his cape) over a
## few lines from the novel, then the title card and credits. Click / Space / Enter / Esc skips. Emits `finished`.

signal finished

const LENGTH := 44.0

var _t := 0.0
var _cam: Camera3D
var _count: Actor
var _bats: Array = []
var _text: Label
var _small: Label
var _sub: Label
var _title: Label
var _credits: Label
var _black: ColorRect
var _done := false
var _shot_dir := ""      # debug: `--introshots=<dir>` saves frames at fixed times and quits
var _shot_times := [5.5, 13.0, 21.0, 29.0, 35.5, 39.0]
var _shot_i := 0


func _ready() -> void:
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--introshots="):
			_shot_dir = a.get_slice("=", 1)
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	var svc := SubViewportContainer.new()
	svc.stretch = true
	svc.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	svc.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(svc)
	var vp := SubViewport.new()
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_2X
	svc.add_child(vp)
	_build_world(vp)
	_build_text()
	_black = ColorRect.new()
	_black.color = Color.BLACK
	_black.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_black.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_black)
	_schedule()


func _build_world(vp: SubViewport) -> void:
	var env := Environment.new()
	env.background_mode = Environment.BG_SKY
	var sky := Sky.new()
	var mat := PanoramaSkyMaterial.new()
	mat.panorama = load("res://assets/sky/night.png")
	sky.sky_material = mat
	env.sky = sky
	env.sky_rotation = Vector3(0, deg_to_rad(40), 0)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.20, 0.24, 0.36)
	env.ambient_light_energy = 0.9
	env.fog_enabled = true
	env.fog_light_color = Color(0.17, 0.2, 0.28)
	env.fog_density = 0.028
	env.volumetric_fog_enabled = false
	env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	env.glow_enabled = true
	var we := WorldEnvironment.new()
	we.environment = env
	vp.add_child(we)
	var moon := DirectionalLight3D.new()
	moon.rotation_degrees = Vector3(-28, 200, 0)
	moon.light_color = Color(0.62, 0.72, 1.0)
	moon.light_energy = 1.5
	moon.shadow_enabled = true
	vp.add_child(moon)
	# ground
	var ground := MeshInstance3D.new()
	var pm := PlaneMesh.new()
	pm.size = Vector2(300, 300)
	ground.mesh = pm
	var gm := StandardMaterial3D.new()
	gm.albedo_color = Color(0.07, 0.09, 0.08)
	gm.roughness = 1.0
	ground.material_override = gm
	vp.add_child(ground)
	# the castle on its crag, far ahead
	var rng := RandomNumberGenerator.new()
	rng.seed = 1897
	var keep := Assets.instantiate("castle_keep")
	keep.position = Vector3(2, 0.0, -46)
	keep.scale = Vector3.ONE * 2.2
	vp.add_child(keep)
	for i in 9:
		var r := Assets.instantiate("rock_big")
		r.position = Vector3(rng.randf_range(-12, 14), 0, -46 + rng.randf_range(-6, 6))
		r.scale = Vector3.ONE * rng.randf_range(2.0, 4.5)
		r.rotation.y = rng.randf() * TAU
		vp.add_child(r)
	var tw := Assets.instantiate("tower")
	tw.position = Vector3(-9, 0, -44)
	tw.scale = Vector3.ONE * 1.8
	vp.add_child(tw)
	# pines flanking the road
	for i in 46:
		var side := -1.0 if i % 2 == 0 else 1.0
		var z := 12.0 - float(i / 2) * 3.0 + rng.randf_range(-1.0, 1.0)
		var p := Assets.instantiate("pine" if rng.randf() < 0.7 else "deadtree")
		p.position = Vector3(side * rng.randf_range(3.5, 16.0), 0, z)
		p.scale = Vector3.ONE * rng.randf_range(1.0, 2.0)
		p.rotation.y = rng.randf() * TAU
		vp.add_child(p)
	# the moon
	var mo := Assets.instantiate("moon")
	mo.position = Vector3(-18, 26, -80)
	mo.scale = Vector3.ONE * 6.0
	vp.add_child(mo)
	# the Count at the roadside, cape stirring
	_count = Actor.new()
	vp.add_child(_count)
	_count.setup("human_dracula", "count", 1.0)
	_count.position = Vector3(1.6, 0, -6.0)
	_count.face_yaw_deg(14.0)
	_count.rotation.y = deg_to_rad(14.0)
	# bats
	for i in 7:
		var b := Actor.new()
		vp.add_child(b)
		b.setup("bat", "", 1.6)
		b.position = Vector3(-30, 6, -10)
		_bats.append(b)
	_cam = Camera3D.new()
	_cam.fov = 48
	_cam.far = 400.0
	vp.add_child(_cam)
	_cam.current = true
	_cam.position = Vector3(-2.5, 1.5, 9)
	_cam.look_at(Vector3(1.5, 3.0, -30))


func _label(size: int, color: Color) -> Label:
	var l := Label.new()
	var f := SystemFont.new()
	f.font_names = PackedStringArray(["Palatino Linotype", "Palatino", "Book Antiqua", "Georgia", "Cormorant Garamond", "DejaVu Serif", "Liberation Serif", "serif"])
	l.add_theme_font_override("font", f)
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", color)
	l.add_theme_color_override("font_outline_color", Color(0, 0, 0, 0.85))
	l.add_theme_constant_override("outline_size", 6)
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	l.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	l.offset_left = 120
	l.offset_right = -120
	l.modulate.a = 0.0
	l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(l)
	return l


func _build_text() -> void:
	_small = _label(22, Color("#c8c0b0"))
	_small.offset_top = -80
	_text = _label(30, Color("#e8e0d0"))
	_text.offset_top = 150
	_sub = _label(26, Color("#b8b0a0"))
	_sub.offset_top = 150
	_title = _label(110, Color("#d8d2c4"))
	_title.offset_top = -150
	_credits = _label(21, Color("#a8a090"))
	_credits.offset_top = 300


func _show(l: Label, txt: String, fade_in: float, hold: float, fade_out: float, at: float) -> void:
	var tw := create_tween()
	tw.tween_interval(at)
	tw.tween_callback(func() -> void: l.text = txt)
	tw.tween_property(l, "modulate:a", 1.0, fade_in)
	tw.tween_interval(hold)
	tw.tween_property(l, "modulate:a", 0.0, fade_out)


func _schedule() -> void:
	var tw := create_tween()
	tw.tween_property(_black, "color:a", 0.0, 3.0).from(1.0)
	_show(_small, "a game after the novel by", 1.5, 2.0, 1.2, 3.0)
	_show(_text, "BRAM STOKER", 1.8, 2.2, 1.4, 4.2)
	_show(_text, "\"Listen to them - the children of the night.\nWhat music they make!\"", 1.6, 4.0, 1.6, 10.5)
	_show(_text, "\"I am Dracula; and I bid you welcome, Mr. Harker,\nto my house.\"", 1.6, 4.0, 1.6, 18.5)
	_show(_text, "\"For the dead travel fast.\"", 1.6, 3.4, 1.6, 26.0)
	var t2 := create_tween()
	t2.tween_interval(32.0)
	t2.tween_property(_title, "modulate:a", 1.0, 2.4)
	t2.tween_callback(func() -> void: _title.text = "DRACULA")
	_show(_sub, "THE BORGO PASS", 2.0, 8.0, 1.5, 34.0)
	_show(_credits, "Story  Bram Stoker, 1897     Game  Dottyboy, with Claude\nEngine  Godot     Modelling  Blender     Animation  Adobe Mixamo", 1.5, 4.0, 1.5, 37.5)
	var t3 := create_tween()
	t3.tween_interval(LENGTH - 2.0)
	t3.tween_property(_black, "color:a", 1.0, 1.8)
	t3.tween_callback(_finish)


func _process(delta: float) -> void:
	_t += delta
	var u := clampf(_t / (LENGTH - 6.0), 0.0, 1.0)
	var e := u * u * (3.0 - 2.0 * u)
	_cam.position = Vector3(lerpf(-2.5, 0.2, e) + sin(_t * 0.31) * 0.12, 1.55 + sin(_t * 0.23) * 0.05, lerpf(9.0, -2.4, e))
	_cam.look_at(Vector3(lerpf(1.5, 1.4, e), lerpf(3.0, 1.55, e), lerpf(-30.0, -6.0, e)))
	for i in _bats.size():
		var b: Actor = _bats[i]
		var ph := fmod(_t * 0.09 + float(i) * 0.137, 1.0)
		var x := lerpf(-26.0, 26.0, ph)
		b.position = Vector3(x, 4.5 + sin(_t * 1.3 + float(i)) * 1.2 + float(i % 3), -14.0 + sin(_t * 0.5 + float(i) * 2.0) * 7.0 - float(i) * 2.5)
		b.rotation.y = deg_to_rad(90.0)
	if _shot_dir != "" and _shot_i < _shot_times.size() and _t >= _shot_times[_shot_i]:
		get_viewport().get_texture().get_image().save_png("%s/intro_%d.png" % [_shot_dir, _shot_i])
		_shot_i += 1
		if _shot_i >= _shot_times.size():
			get_tree().quit()


func _input(ev: InputEvent) -> void:
	var skip := false
	if ev is InputEventMouseButton and ev.pressed:
		skip = true
	elif ev is InputEventKey and ev.pressed and ev.keycode in [KEY_ESCAPE, KEY_SPACE, KEY_ENTER, KEY_KP_ENTER]:
		skip = true
	if skip:
		get_viewport().set_input_as_handled()
		_finish()


func _finish() -> void:
	if _done:
		return
	_done = true
	finished.emit()
	queue_free()
