class_name ActionMode
extends Node
## Optional real-time "hack and slash" layer for merged regions (Esc menu: Action mode). Wild creatures roam the open world,
## click one to fight it, loot and XP drop. The story's own turn-based fights are unchanged. Stats come from systems.json.

const AGGRO := 7.5
const LEASH := 16.0
const REACH := 1.9

const SPAWNS := {
	"dock": ["rat", "rat", "bat"],
	"wild": ["wolf", "bat", "wolf"],
}
const NIGHT_SPAWNS := ["wolf", "wolf", "bat", "wolf_alpha"]
const DROPS := ["silver", "bandage", "garlic", "cloth", "brandy"]

var loc: Location
var enemies: Array = []
var target := -1
var _atk_cd := 0.0
var _regen := 0.0
var _rng := RandomNumberGenerator.new()
var _since_hurt := 99.0
var _respawn_to := ""


func setup(l: Location) -> ActionMode:
	loc = l
	_rng.seed = hash("action:%s:%d" % [l.id, Game.seed_value])
	var R: Dictionary = Regions.DEF[l.region]
	var night: bool = str(R.get("sky", "day")) == "night"
	var kinds: Array = NIGHT_SPAWNS if night else SPAWNS.get(str(R.get("theme", "wild")), SPAWNS.wild)
	var sp: Vector3 = l.player.position
	var idx := 0
	for m in l.members:
		var rc: Rect2 = l.members[m]
		var n := 3 if rc.get_area() > 400.0 else 2
		for i in n:
			for attempt in 30:
				var p := Vector3(_rng.randf_range(rc.position.x + 2.0, rc.end.x - 2.0), 0, _rng.randf_range(rc.position.y + 2.0, rc.end.y - 2.0))
				if Vector2(p.x - sp.x, p.z - sp.z).length() < 9.0:
					continue
				var blocked := false
				for b in l._blockers:
					if (b.pos as Vector2).distance_to(Vector2(p.x, p.z)) < float(b.r) + 1.0:
						blocked = true
						break
				if blocked:
					continue
				_spawn(str(kinds[idx % kinds.size()]), p)
				idx += 1
				break
	return self


func _spawn(kind: String, p: Vector3) -> void:
	var def: Dictionary = Game.systems.enemies[kind]
	var a := Actor.new()
	a.position = p
	loc.add_child(a)
	a.setup(str(def.model), Assets.default_variant(str(def.model)))
	a.clamp_fn = Callable(loc, "_clamp_region")
	a.blockers = loc._blockers
	a.speed = 3.0 if kind.begins_with("wolf") else 2.4
	loc._make_body(a, "", false)
	for c in a.get_children():
		if c is StaticBody3D and c.has_meta("eid"):
			c.set_meta("enemy", enemies.size())
	var lb := Label3D.new()
	lb.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	lb.no_depth_test = true
	lb.font_size = 40
	lb.outline_size = 10
	lb.pixel_size = 0.0045
	lb.position = Vector3(0, 1.9 if not kind.begins_with("bat") and kind != "rat" else 1.2, 0)
	a.add_child(lb)
	var e := {"node": a, "def": def, "kind": kind, "hp": int(def.hp), "max": int(def.hp), "home": p, "cd": _rng.randf() * 1.0, "wander": _rng.randf() * 3.0, "dead": false, "label": lb}
	enemies.append(e)
	_label(e)


func _label(e: Dictionary) -> void:
	var lb: Label3D = e.label
	lb.text = "%s  %d/%d" % [str(e.def.name), int(e.hp), int(e.max)]
	lb.modulate = Color(1, 0.55, 0.45) if bool(e.get("aggro", false)) else Color(0.95, 0.9, 0.8)


func _paused() -> bool:
	if loc == null or not is_instance_valid(loc) or loc.modal or loc.player == null:
		return true
	return false


func _unhandled_input(ev: InputEvent) -> void:
	if _paused():
		return
	if ev is InputEventMouseButton and ev.pressed and ev.button_index == MOUSE_BUTTON_LEFT:
		var i := _pick(ev.position)
		if i >= 0:
			target = i
			loc.pending = {}
			get_viewport().set_input_as_handled()
		elif Game.selected_item == "" and loc._pick(ev.position) == "":
			target = -1        # clicking the ground cancels the attack, the location walks there
	elif ev is InputEventMouseMotion:
		var j := _pick(ev.position)
		if j >= 0:
			loc.hover_changed.emit("Attack %s" % str(enemies[j].def.name))


func _pick(pos: Vector2) -> int:
	var r := loc._ray(pos)
	if r.is_empty():
		return -1
	var c: Object = r.collider
	if c.has_meta("enemy"):
		var i := int(c.get_meta("enemy"))
		if i < enemies.size() and not enemies[i].dead:
			return i
	return -1


func _process(delta: float) -> void:
	if _paused():
		return
	var pid := Game.protagonist
	var st: Dictionary = Game.member_state[pid]
	var eff := Game.effective(pid)
	var pp := loc.player.position
	_since_hurt += delta
	_atk_cd -= delta
	# player attacks the clicked enemy
	if target >= 0:
		var t: Dictionary = enemies[target]
		if t.dead:
			target = -1
		else:
			var tp: Vector3 = t.node.position
			var dist := Vector2(tp.x - pp.x, tp.z - pp.z).length()
			if dist > REACH:
				if int(Engine.get_process_frames()) % 10 == 0:
					loc.go_to(tp)
			else:
				loc.player.stop()
				loc.player.face_point(tp)
				if _atk_cd <= 0.0:
					_player_attack(t, eff)
	for e in enemies:
		if not e.dead:
			_enemy_ai(e, delta, pp, eff, st)
	# slow recovery away from danger
	if _since_hurt > 8.0 and int(st.hp) < int(eff.max_hp):
		_regen += delta
		if _regen > 3.0:
			_regen = 0.0
			st.hp = mini(int(st.hp) + 1, int(eff.max_hp))
			Game.party_changed.emit()


func _player_attack(t: Dictionary, eff: Dictionary) -> void:
	var w: Dictionary = Game.systems.weapons.get(str(eff.weapon) if str(eff.weapon) != "" else str(Game.systems.party[Game.protagonist].weapon), Game.systems.weapons.fists)
	_atk_cd = 0.85
	loc.player.play_once("attack", 0.45)
	var chance := clampi(int(eff.acc) + int(w.get("acc", 0)) + 25 - int(t.def.eva), 25, 97)
	if _rng.randi() % 100 >= chance:
		_float(t.node.position + Vector3(0, 1.4, 0), "miss", Color(0.8, 0.8, 0.8))
		Audio.sfx("miss")
		return
	var dm: Array = w.dmg
	var dmg := _rng.randi_range(int(dm[0]), int(dm[1])) + int(eff.dmg)
	t.hp = int(t.hp) - dmg
	t["aggro"] = true
	Audio.sfx("hit")
	_float(t.node.position + Vector3(0, 1.4, 0), str(dmg), Color(1, 0.85, 0.3))
	t.node.play_once("hurt", 0.3)
	if int(t.hp) <= 0:
		_kill(t)
	else:
		_label(t)


func _kill(t: Dictionary) -> void:
	t.dead = true
	t.label.visible = false
	t.node.play_once("die", 0.8)
	Audio.sfx("defeat", 1.4, -8.0)
	target = -1
	var xp := maxi(1, int(t.max) / 3)
	Game.grant_xp(Game.party, xp)
	var txt := "%s defeated (+%d xp)" % [str(t.def.name), xp]
	if _rng.randf() < 0.55:
		var item: String = DROPS[_rng.randi() % DROPS.size()]
		Game.give(item)
		txt += " - found %s" % Game.item_name(item).to_lower()
	Game.message.emit(txt)
	get_tree().create_timer(2.5).timeout.connect(func() -> void:
		if is_instance_valid(t.node):
			t.node.visible = false)


func _enemy_ai(e: Dictionary, delta: float, pp: Vector3, eff: Dictionary, st: Dictionary) -> void:
	var a: Actor = e.node
	var ep := a.position
	var d := Vector2(pp.x - ep.x, pp.z - ep.z).length()
	e.cd = float(e.cd) - delta
	var was: bool = bool(e.get("aggro", false))
	if d < AGGRO or (was and d < LEASH):
		e["aggro"] = true
	else:
		e["aggro"] = false
	if bool(e.aggro) != was:
		_label(e)
	if bool(e.aggro):
		if d > 1.3:
			if int(Engine.get_process_frames() + int(e.cd * 100)) % 12 == 0 or not a.moving:
				a.walk_to(pp)
		else:
			a.stop()
			a.face_point(pp)
			if float(e.cd) <= 0.0:
				e.cd = 1.5
				a.play_once("attack", 0.4)
				var chance := clampi(int(e.def.acc) - int(eff.eva) - int(eff.armor) * 3, 20, 95)
				if _rng.randi() % 100 < chance:
					var dm: Array = e.def.dmg
					var dmg := maxi(1, _rng.randi_range(int(dm[0]), int(dm[1])) - int(eff.armor))
					st.hp = int(st.hp) - dmg
					_since_hurt = 0.0
					Audio.sfx("hurt")
					_float(pp + Vector3(0, 1.8, 0), "-%d" % dmg, Color(1, 0.35, 0.3))
					Game.party_changed.emit()
					if int(st.hp) <= 0:
						_defeat()
				else:
					_float(pp + Vector3(0, 1.8, 0), "dodged", Color(0.8, 0.9, 1))
	else:
		e.wander = float(e.wander) - delta
		if float(e.wander) <= 0.0:
			e.wander = _rng.randf_range(2.5, 6.0)
			var h: Vector3 = e.home
			a.walk_to(h + Vector3(_rng.randf_range(-4, 4), 0, _rng.randf_range(-4, 4)))


func _defeat() -> void:
	var st: Dictionary = Game.member_state[Game.protagonist]
	var eff := Game.effective(Game.protagonist)
	Game.message.emit("Everything goes dark ... you come to, bruised, a little way off.")
	for e in enemies:
		e["aggro"] = false
		if not e.dead:
			(e.node as Actor).stop()
			_label(e)
	target = -1
	st.hp = maxi(1, int(eff.max_hp) / 2)
	var np: Vector3 = loc.region_spawn(Game.current, "")
	loc.player.position = np
	loc.player.stop()
	loc._cam_look = Vector3(np.x, 1.0, np.z - 1.4)
	Game.party_changed.emit()


func _float(pos: Vector3, text: String, col: Color) -> void:
	var lb := Label3D.new()
	lb.text = text
	lb.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	lb.no_depth_test = true
	lb.font_size = 56
	lb.outline_size = 14
	lb.pixel_size = 0.006
	lb.modulate = col
	lb.position = pos
	loc.add_child(lb)
	var tw := create_tween().set_parallel(true)
	tw.tween_property(lb, "position:y", pos.y + 1.0, 0.9)
	tw.tween_property(lb, "modulate:a", 0.0, 0.9).set_delay(0.3)
	tw.chain().tween_callback(lb.queue_free)
