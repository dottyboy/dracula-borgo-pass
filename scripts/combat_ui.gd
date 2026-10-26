class_name CombatUI
extends CanvasLayer
## Battle screen: enemy models on a small 3D stage (own world), party portrait
## cards with HP/Nerve, action menu, target picking and a combat log.

signal finished(result: String, combat: Combat)

var combat: Combat
var _root: Control
var _stage: SubViewport
var _enemy_row: HBoxContainer
var _party_row: HBoxContainer
var _menu: VBoxContainer
var _log: RichTextLabel
var _title: Label
var _hint: Label
var _actors: Dictionary = {}
var _cards: Dictionary = {}
var _ebuttons: Dictionary = {}
var _actor: Dictionary = {}
var _pending: Dictionary = {}
var _busy := false
var _env: Environment


func _ready() -> void:
	layer = 20
	_root = Control.new()
	_root.theme = HUD.make_theme()
	_root.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(_root)
	var bg := ColorRect.new()
	bg.color = Color(0.03, 0.01, 0.02, 0.97)
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	_root.add_child(bg)
	_title = _lbl(_root, 28, Color("#c9a24a"))
	_title.position = Vector2(24, 10)
	_hint = _lbl(_root, 18, Color("#e9dcc0"))
	_hint.position = Vector2(24, 48)
	# enemy stage
	var svc := SubViewportContainer.new()
	svc.stretch = true
	svc.position = Vector2(200, 80)
	svc.size = Vector2(880, 270)
	_root.add_child(svc)
	_stage = SubViewport.new()
	_stage.own_world_3d = true
	_stage.transparent_bg = false
	_stage.size = Vector2i(880, 270)
	svc.add_child(_stage)
	var cam := Camera3D.new()
	cam.position = Vector3(0, 1.3, 5.3)
	cam.fov = 38
	_stage.add_child(cam)
	cam.look_at(Vector3(0, 0.85, 0))
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-30, 25, 0)
	sun.light_energy = 1.3
	sun.light_color = Color("#ffcf9a")
	_stage.add_child(sun)
	var env := Environment.new()
	_env = env
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color("#0c1220")
	env.fog_enabled = true
	env.fog_density = 0.05
	env.fog_light_color = Color("#0c1220")
	env.glow_enabled = true
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color("#6a5a70")
	env.ambient_light_energy = 0.8
	var we := WorldEnvironment.new()
	we.environment = env
	_stage.add_child(we)
	var rim := DirectionalLight3D.new()
	rim.rotation_degrees = Vector3(-25, 200, 0)
	rim.light_energy = 0.9
	rim.light_color = Color("#7a90ff")
	_stage.add_child(rim)
	var floor_mi := MeshInstance3D.new()
	var cm := CylinderMesh.new()
	cm.top_radius = 6.0
	cm.bottom_radius = 6.0
	cm.height = 0.1
	floor_mi.mesh = cm
	var fm := StandardMaterial3D.new()
	fm.albedo_color = Color("#1c1a1e")
	fm.roughness = 1.0
	floor_mi.material_override = fm
	floor_mi.position = Vector3(0, -0.06, 0)
	_stage.add_child(floor_mi)
	_enemy_row = HBoxContainer.new()
	_enemy_row.position = Vector2(200, 352)
	_enemy_row.size = Vector2(880, 40)
	_enemy_row.alignment = BoxContainer.ALIGNMENT_CENTER
	_enemy_row.add_theme_constant_override("separation", 10)
	_root.add_child(_enemy_row)
	# log
	_log = RichTextLabel.new()
	_log.bbcode_enabled = true
	_log.scroll_following = true
	_log.position = Vector2(1090, 80)
	_log.size = Vector2(180, 310)
	_log.add_theme_font_size_override("normal_font_size", 14)
	_root.add_child(_log)
	# menu
	_menu = VBoxContainer.new()
	_menu.position = Vector2(20, 90)
	_menu.size = Vector2(176, 300)
	_root.add_child(_menu)
	# party cards
	_party_row = HBoxContainer.new()
	_party_row.position = Vector2(20, 410)
	_party_row.size = Vector2(1240, 290)
	_party_row.add_theme_constant_override("separation", 8)
	_root.add_child(_party_row)


func _lbl(parent: Node, size: int, color: Color) -> Label:
	var l := Label.new()
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", color)
	l.add_theme_color_override("font_outline_color", Color.BLACK)
	l.add_theme_constant_override("outline_size", 5)
	parent.add_child(l)
	return l


func start(encounter_id: String, seed_value: int) -> void:
	combat = Combat.new()
	var states := {}
	for id in Game.party:
		var st: Dictionary = Game.member_state[id].duplicate(true)
		st["eff"] = Game.effective(str(id))
		states[id] = st
	combat.setup(Game.systems, Game.party, states, encounter_id, Game.counts, seed_value)
	_title.text = str(combat.enc.name)
	var bg: String = {"night": "#0c1220", "dusk": "#33202a", "dawn": "#3a3036", "day": "#8d9aa8"}.get(str(combat.enc.time), "#0c1220")
	_env.background_color = Color(bg)
	_env.fog_light_color = Color(bg)
	_build_enemies()
	_build_party()
	_flush_log()
	_next()


func _build_enemies() -> void:
	var n := combat.enemies.size()
	for i in n:
		var e: Dictionary = combat.enemies[i]
		var a := Actor.new()
		_stage.add_child(a)
		var kind: String = "wolf" if str(e.model).begins_with("wolf") else str(e.model)
		a.setup(str(e.model), Assets.default_variant(str(e.model)))
		a.position = Vector3((i - (n - 1) / 2.0) * 1.7, 0, 0)
		a.face_yaw_deg(0)
		a.speed = 0
		_actors[e.id] = a
		var b := Button.new()
		b.custom_minimum_size = Vector2(150, 36)
		b.focus_mode = Control.FOCUS_NONE
		b.pressed.connect(func() -> void: _target_picked(e))
		_enemy_row.add_child(b)
		_ebuttons[e.id] = b
	_retint()


func _retint() -> void:
	for e in combat.enemies:
		var b: Button = _ebuttons.get(e.id)
		if b == null:
			var a0: Actor = _actors.get(e.id)
			continue
		var txt := "%s  %d/%d" % [e.name, maxi(0, e.hp), e.max_hp]
		for k in e.st:
			if k in ["asleep", "repelled", "box", "helpless", "fled", "subdued", "mist", "charmed"]:
				txt += " [%s]" % k
		b.text = txt
		var gone: bool = e.hp <= 0 or e.st.has("fled") or e.st.has("subdued")
		b.disabled = gone or _pending.is_empty()
		var a: Actor = _actors.get(e.id)
		if a != null:
			a.visible = not (e.hp <= 0 or e.st.has("fled"))
			if e.st.has("subdued") or e.st.has("helpless") or e.st.has("box"):
				a.rotation_degrees.z = 80
			else:
				a.rotation_degrees.z = 0


func _build_party() -> void:
	for p in combat.party:
		var card := PanelContainer.new()
		card.custom_minimum_size = Vector2(196, 280)
		var vb := VBoxContainer.new()
		card.add_child(vb)
		var tr := TextureRect.new()
		var path := "res://assets/portraits/%s.png" % p.portrait
		if ResourceLoader.exists(path):
			tr.texture = load(path)
		tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		tr.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
		tr.custom_minimum_size = Vector2(180, 180)
		vb.add_child(tr)
		var nm := Label.new()
		nm.text = str(p.name)
		vb.add_child(nm)
		var hp := ProgressBar.new()
		hp.max_value = p.max_hp
		hp.show_percentage = false
		hp.custom_minimum_size = Vector2(0, 14)
		hp.modulate = Color("#d04040")
		vb.add_child(hp)
		var nv := ProgressBar.new()
		nv.max_value = p.max_nerve
		nv.show_percentage = false
		nv.custom_minimum_size = Vector2(0, 10)
		nv.modulate = Color("#6a8ad0")
		vb.add_child(nv)
		var st := Label.new()
		st.add_theme_font_size_override("font_size", 12)
		vb.add_child(st)
		var click := Button.new()
		click.flat = true
		click.set_anchors_preset(Control.PRESET_FULL_RECT)
		click.focus_mode = Control.FOCUS_NONE
		click.pressed.connect(func() -> void: _target_picked(p))
		card.add_child(click)
		_party_row.add_child(card)
		_cards[p.id] = {"card": card, "hp": hp, "nv": nv, "st": st, "name": nm}
	_refresh()


func _refresh() -> void:
	for p in combat.party:
		var c: Dictionary = _cards[p.id]
		c.hp.value = p.hp
		c.nv.value = p.nerve
		var s := "HP %d/%d  Nerve %d" % [p.hp, p.max_hp, p.nerve]
		for k in p.st:
			if k in ["charmed", "frozen", "asleep"]:
				s += " [%s]" % k
		if p.get("drained", false):
			s += " [drained]"
		if combat.buffs.circle > 0:
			s += " (circle)"
		c.st.text = s
		c.card.modulate = Color(1, 1, 1) if p.hp > 0 else Color(0.4, 0.4, 0.4)
		c.name.add_theme_color_override("font_color", Color("#ffd870") if (not _actor.is_empty() and _actor.id == p.id) else Color.WHITE)
	_retint()


func _play_events() -> void:
	for ev in combat.take_events():
		var from_a: Actor = _actors.get(ev.from)
		var to_a: Actor = _actors.get(ev.to)
		match str(ev.t):
			"hit":
				if from_a != null:
					from_a.play_once("attack", 0.55)
				if to_a != null:
					to_a.play_once("hurt", 0.4)
				elif _cards.has(ev.to):
					_shake_card(str(ev.to))
			"miss":
				if from_a != null:
					from_a.play_once("attack", 0.55)
			"die":
				if to_a != null:
					to_a.play_once("die", 0.9)
			"cast":
				if from_a != null:
					from_a.play_once("howl" if str(from_a.name).begins_with("wolf") else "cast", 0.7)


func _shake_card(pid: String) -> void:
	var card: Control = _cards[pid].card
	var tw := create_tween()
	tw.tween_property(card, "modulate", Color(1.0, 0.4, 0.4), 0.08)
	tw.tween_property(card, "modulate", Color(1, 1, 1), 0.25)


func _flush_log() -> void:
	_play_events()
	for l in combat.take_log():
		_log.append_text(str(l) + "\n")
		_sfx_for(str(l))
	_refresh()


func _sfx_for(line: String) -> void:
	if line.contains("drinking"):
		Audio.sfx("bite")
	elif line.contains(" hits "):
		Audio.sfx("hit")
	elif line.contains(" misses "):
		Audio.sfx("miss")
	elif line.contains(" strikes ") or line.contains(" falls"):
		Audio.sfx("hurt")
	elif line.contains("shrinks back") or line.contains("held back") or line.contains("holy circle") or line.contains("Host crumbs"):
		Audio.sfx("repel")
	elif line.contains("crumbles") or line.contains("stake home"):
		Audio.sfx("holy")
	elif line.contains("wolves"):
		Audio.sfx("howl")
	elif line.contains("freezes"):
		Audio.sfx("heartbeat")


func _next() -> void:
	var r := combat.advance()
	_flush_log()
	if r.state == "over":
		_menu_clear()
		_hint.text = {"win": "Victory.", "lose": "Defeat.", "fled": "You escaped."}[r.result]
		var b := Button.new()
		b.text = "Continue"
		b.pressed.connect(func() -> void:
			_apply_results()
			finished.emit(combat.result, combat)
			queue_free())
		_menu.add_child(b)
		return
	_actor = r.actor
	_show_menu()


func _menu_clear() -> void:
	for c in _menu.get_children():
		c.queue_free()
	_pending = {}


func _show_menu() -> void:
	_menu_clear()
	_refresh()
	_hint.text = "%s - choose an action" % _actor.name
	for a in combat.actions_for(_actor):
		var b := Button.new()
		b.text = str(a.label)
		b.disabled = not a.enabled
		b.tooltip_text = str(a.get("hint", ""))
		b.focus_mode = Control.FOCUS_NONE
		b.pressed.connect(func() -> void: _choose(a))
		_menu.add_child(b)


func _choose(a: Dictionary) -> void:
	match a.target:
		"none":
			combat.act(_actor, {"id": a.id})
			_after()
		"enemy", "ally":
			_pending = a
			_hint.text = "%s: pick a target (%s)" % [a.label, "an enemy below" if a.target == "enemy" else "a party member"]
			for c in _menu.get_children():
				c.disabled = true
			_retint()


func _target_picked(t: Dictionary) -> void:
	if _pending.is_empty():
		return
	if (_pending.target == "enemy") != (t.side == "enemy"):
		return
	var act := {"id": _pending.id, "target": t}
	_pending = {}
	combat.act(_actor, act)
	_after()


func _after() -> void:
	_pending = {}
	_menu_clear()
	_flush_log()
	var tw := create_tween()
	tw.tween_interval(0.5)
	await tw.finished
	_next()


func _apply_results() -> void:
	for p in combat.party:
		var st: Dictionary = Game.member_state[p.id]
		st.hp = maxi(1, p.hp) if combat.result != "lose" else maxi(1, p.max_hp / 2)
		st.nerve = maxi(1, p.nerve)
		if p.get("drained", false):
			st.drained = true
