extends Node
## Asset gallery: browse every generated model and cycle its texture variants.
## Run:  godot --path . scenes/Gallery.tscn      Keys: <-/-> model, Up/Down variant, Space spin.

var ids: Array = []
var idx := 0
var vidx := 0
var holder: Node3D
var label: Label
var cam: Camera3D
var spin := true
var walk_on := false
var talk_on := false
var _actor: Actor


func _ready() -> void:
	ids = Assets.model_ids()
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color("#1a1a22")
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color("#8890a0")
	env.ambient_light_energy = 0.7
	env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	var we := WorldEnvironment.new()
	we.environment = env
	add_child(we)
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-40, 35, 0)
	sun.shadow_enabled = true
	add_child(sun)
	cam = Camera3D.new()
	add_child(cam)
	holder = Node3D.new()
	add_child(holder)
	var cl := CanvasLayer.new()
	add_child(cl)
	label = Label.new()
	label.position = Vector2(16, 12)
	label.add_theme_font_size_override("font_size", 22)
	cl.add_child(label)
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--model="):
			idx = max(0, ids.find(a.trim_prefix("--model=")))
		if a.begins_with("--var="):
			vidx = int(a.trim_prefix("--var="))
		if a == "--walk":
			walk_on = true
		if a == "--talk":
			talk_on = true
		if a.begins_with("--strip="):
			_strip(a.trim_prefix("--strip="))
		if a.begins_with("--shot="):
			_shot(a.trim_prefix("--shot="))
	_show()


func _strip(prefix: String) -> void:
	spin = false
	await get_tree().create_timer(0.6).timeout
	for i in 6:
		get_viewport().get_texture().get_image().save_png("%s_%d.png" % [prefix, i])
		await get_tree().create_timer(0.11).timeout
	get_tree().quit()


func _shot(path: String) -> void:
	spin = false
	await get_tree().create_timer(1.0).timeout
	get_viewport().get_texture().get_image().save_png(path)
	get_tree().quit()


func _show() -> void:
	for c in holder.get_children():
		c.queue_free()
	var id: String = ids[idx]
	var vs: Array = Assets.variants_of(id)
	vidx = posmod(vidx, vs.size())
	var m: Node3D
	var act := Actor.new()
	holder.add_child(act)
	act.setup(id, str(vs[vidx]))
	m = act
	if act.kind != "static":
		act.demo_walk = walk_on
		act.talking = talk_on
		_actor = act
	var bb := AABB()
	var first := true
	for n in Assets._meshes(m):
		var t := (n as MeshInstance3D).global_transform * (n as MeshInstance3D).get_aabb()
		bb = t if first else bb.merge(t)
		first = false
	var r := maxf(bb.size.length(), 0.5)
	var c := bb.get_center()
	cam.position = c + Vector3(0.6, 0.35, 1.0).normalized() * r * 1.05
	cam.look_at(c)
	holder.position = Vector3.ZERO
	label.text = "%s  [%d/%d]   variant: %s (%d/%d)\nslots: %s" % [id, idx + 1, ids.size(), vs[vidx], vidx + 1, vs.size(),
		", ".join(PackedStringArray(Assets.manifest.models[id].slots))]


func _process(d: float) -> void:
	if spin:
		holder.rotation.y += d * 0.6


func _unhandled_key_input(e: InputEvent) -> void:
	if not e.pressed:
		return
	match e.keycode:
		KEY_RIGHT:
			idx = posmod(idx + 1, ids.size()); vidx = 0; _show()
		KEY_LEFT:
			idx = posmod(idx - 1, ids.size()); vidx = 0; _show()
		KEY_UP:
			vidx += 1; _show()
		KEY_DOWN:
			vidx -= 1; _show()
		KEY_SPACE:
			spin = not spin
		KEY_W:
			walk_on = not walk_on
			_show()
		KEY_T:
			talk_on = not talk_on
			_show()
		KEY_1:
			if _actor != null:
				_actor.play_once("attack", 0.6)
		KEY_2:
			if _actor != null:
				_actor.play_once("hurt", 0.5)
		KEY_3:
			if _actor != null:
				_actor.play_once("reach", 0.7)
		KEY_4:
			if _actor != null:
				_actor.play_once("cast", 0.8)
		KEY_5:
			if _actor != null:
				_actor.play_once("victory", 1.0)
		KEY_6:
			if _actor != null:
				_actor.play_once("die", 1.0)
