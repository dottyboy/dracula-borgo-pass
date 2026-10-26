class_name Actor
extends Node3D
## A model with procedural skeletal animation (no armature): the generated models are nested joint nodes
## (hips > torso > head, shoulder > elbow, hip > knee). This script drives them:
##   idle (breathing, weight shift, looking around), walk (hip sway, knee/elbow bend, counter-rotating torso),
##   talk (head nods + arm gestures), one-shots: reach, attack, hurt, cast, die, victory, bow.
## Quadrupeds (wolves) trot with a diagonal gait, tail wag and jaw; bats flap two-segment wings.

signal arrived
signal step

var model: Node3D
var kind := "static"          # human | quad | bat | static
var parts: Dictionary = {}
var speed := 2.6
var dest := Vector3.ZERO
var moving := false
var queue: Array = []             # further waypoints after `dest`
var blockers: Array = []      # [{pos: Vector2, r: float}]
var bounds := Rect2(-5, -5, 10, 10)
var clamp_fn: Callable            # optional: keeps the actor inside an irregular walkable area
var talking := false
var dead := false
var demo_walk := false       # gallery preview
var _t := randf() * 10.0
var _yaw := 0.0
var _last_phase := 0.0
var _gait := 0.0
var _walk_blend := 0.0
var _shot := ""
var _shot_t := 0.0
var _shot_len := 0.0
var _flash: StandardMaterial3D
var _ap: AnimationPlayer      # skinned (Mixamo) characters
var _female := false
var _idle_pick := "idle"
var _rest_y := 0.0           # rest height of the animated root joint (hips / body)


func setup(model_id: String, variant: String, scale_f: float = 1.0) -> void:
	var mx := MixamoRig.config_for(model_id, variant)
	if not mx.is_empty():
		_setup_skinned(mx, scale_f, variant)
		return
	model = Assets.instantiate(model_id, variant)
	add_child(model)
	model.scale = Vector3.ONE * scale_f
	_index(model)
	if parts.has("leg_up_l") and parts.has("arm_up_l"):
		kind = "human"
	elif parts.has("leg_up_fl"):
		kind = "quad"
	elif parts.has("wing_l"):
		kind = "bat"
	var root_joint: Node3D = parts.get("hips", parts.get("body"))
	if root_joint != null:
		_rest_y = root_joint.position.y


func _setup_skinned(cfg: Dictionary, scale_f: float, variant: String) -> void:
	kind = "skinned"
	model = MixamoRig.build(str(cfg.glb))
	add_child(model)
	Assets.apply_variant(model, str(cfg.model), variant if variant != "" else Assets.default_variant(str(cfg.model)))
	MixamoRig.fit_height(model, float(cfg.height) * scale_f)
	var bd := float(cfg.get("build", 1.0))
	model.scale = Vector3(model.scale.x * bd, model.scale.y, model.scale.z * bd)
	_female = bool(cfg.get("female", false))
	_ap = model.get_node("anim")
	_idle_pick = ["idle_f1", "idle_f2", "idle_f3"][randi() % 3] if _female else ["idle", "idle", "idle_neutral"][randi() % 3]
	_play(_idle_pick, 1.0)


func _play(anim: String, speed: float = 1.0, blend: float = 0.2) -> void:
	if _ap == null or not _ap.has_animation(anim):
		return
	if _ap.current_animation != anim:
		_ap.play(anim, blend, speed)
	else:
		_ap.speed_scale = speed


const _SHOT_ANIMS := {"attack": "slash", "hurt": "hurt", "cast": "cast", "reach": "reach", "victory": "victory",
	"bow": "bow", "die": "die", "howl": "yell"}


func _anim_skinned(walking: bool) -> void:
	if _shot != "" and _SHOT_ANIMS.has(_shot):
		var a: String = _SHOT_ANIMS[_shot]
		if _ap.has_animation(a):
			var len := _ap.get_animation(a).length
			_play(a, clampf(len / maxf(_shot_len, 0.2), 0.8, 2.6), 0.1)
		return
	if dead:
		_play("die", 1.0, 0.1)
		return
	if walking:
		_play(("walk_f" if _female else "walk"), clampf(speed / 1.6, 0.6, 2.0))
	elif talking:
		_play("talk_f" if _female else "talk", 1.0)
	else:
		_play(_idle_pick, 1.0)


func _index(n: Node) -> void:
	for c in n.get_children():
		if c is Node3D:
			parts[c.name] = c
			_index(c)


func face_point(p: Vector3) -> void:
	var d := p - position
	d.y = 0
	if d.length() > 0.01:
		_yaw = atan2(d.x, d.z)


func face_yaw_deg(deg: float) -> void:
	_yaw = deg_to_rad(deg)
	rotation.y = _yaw


func _clamped(p: Vector3) -> Vector3:
	if clamp_fn.is_valid():
		return clamp_fn.call(p)
	return Vector3(clampf(p.x, bounds.position.x, bounds.end.x), 0, clampf(p.z, bounds.position.y, bounds.end.y))


func walk_to(p: Vector3) -> void:
	queue = []
	dest = _clamped(Vector3(p.x, 0, p.z))
	moving = true


## Walk through several points in order (used by merged regions to route through the connecting strips).
func walk_path(points: Array) -> void:
	if points.is_empty():
		return
	queue = points.slice(1)
	dest = Vector3(points[0].x, 0, points[0].z)
	moving = true


func stop() -> void:
	moving = false


## One-shot gesture layered over idle/walk: reach, attack, hurt, cast, victory, bow, die.
func play_once(name: String, length: float = 0.6) -> void:
	_shot = name
	_shot_t = 0.0
	_shot_len = length
	if name == "die":
		dead = true
	if name == "hurt":
		_flash_red()


func _flash_red() -> void:
	if _flash == null:
		_flash = StandardMaterial3D.new()
		_flash.albedo_color = Color(1.0, 0.1, 0.05, 0.45)
		_flash.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		_flash.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	for m in Assets._meshes(model):
		(m as MeshInstance3D).material_overlay = _flash
	var tw := create_tween()
	tw.tween_interval(0.22)
	tw.tween_callback(func() -> void:
		for m in Assets._meshes(model):
			(m as MeshInstance3D).material_overlay = null)


func _try_step(step_v: Vector3) -> Vector3:
	var np := position + step_v
	for b in blockers:
		var c: Vector2 = b.pos
		var off := Vector2(np.x, np.z) - c
		var minr: float = float(b.r) + 0.3
		if off.length() < minr:
			var pushed := c + off.normalized() * minr if off.length() > 0.001 else c + Vector2(minr, 0)
			np.x = pushed.x
			np.z = pushed.y
	var cl := _clamped(np)
	np.x = cl.x
	np.z = cl.z
	return np


func _process(delta: float) -> void:
	_t += delta
	var walking := false
	if moving:
		var d := dest - position
		d.y = 0
		if d.length() < (0.9 if not queue.is_empty() else 0.08):
			if not queue.is_empty():
				dest = queue.pop_front()
			else:
				moving = false
				arrived.emit()
		else:
			var step_v := d.normalized() * minf(speed * delta, d.length())
			var np := _try_step(step_v)
			if (np - position).length() < 0.5 * step_v.length():
				# blocked head-on: steer around the obstacle (try both sides, wider angles)
				for ang in [0.6, -0.6, 1.2, -1.2, 1.9, -1.9]:
					var alt := _try_step(step_v.rotated(Vector3.UP, ang))
					if (alt - position).length() >= 0.5 * step_v.length():
						np = alt
						break
			if (np - position).length() < 0.2 * speed * delta:
				moving = false
				arrived.emit()
			else:
				_yaw = atan2(d.x, d.z)
				position = np
				walking = true
	if demo_walk:
		walking = true
	rotation.y = lerp_angle(rotation.y, _yaw, minf(1.0, delta * 10.0))
	_walk_blend = move_toward(_walk_blend, 1.0 if walking else 0.0, delta * 6.0)
	if walking:
		_gait += delta * (6.5 + speed * 1.6)
	if _shot != "":
		_shot_t += delta
		if _shot_t >= _shot_len:
			if _shot != "die":
				_shot = ""
	match kind:
		"human":
			_anim_human(walking)
		"quad":
			_anim_quad(walking)
		"bat":
			_anim_bat()
		"skinned":
			_anim_skinned(walking)


func _rot(n: String, x: float, y: float = 0.0, z: float = 0.0) -> void:
	var p: Node3D = parts.get(n)
	if p != null:
		p.rotation = Vector3(x, y, z)


func _bump() -> float:
	if _shot == "":
		return 0.0
	var u := clampf(_shot_t / _shot_len, 0.0, 1.0)
	return sin(u * PI)


func _anim_human(walking: bool) -> void:
	var w := _gait
	var bw := _walk_blend
	var iw := 1.0 - bw
	var sw := sin(w)
	var cw := cos(w)
	var breathe := sin(_t * 1.7)
	# phase flip -> footstep
	if walking:
		if (sw > 0.0) != (_last_phase > 0.0):
			step.emit()
		_last_phase = sw
	var b := _bump()
	# hips: bob + sway + idle weight shift
	var hips: Node3D = parts.hips
	hips.position.y = _rest_y + absf(cw) * 0.035 * bw - 0.03 * bw + breathe * 0.003
	hips.rotation = Vector3(0.0, sw * 0.12 * bw, sin(_t * 0.5) * 0.02 * iw + sw * 0.04 * bw)
	var torso_pitch := -0.06 * bw + breathe * 0.012
	var torso_yaw := -sw * 0.16 * bw
	var arm_gesture_r := 0.0
	var arm_gesture_l := 0.0
	var head_yaw := sin(_t * 0.45) * 0.3 * iw
	var head_pitch := sin(_t * 0.31) * 0.05 * iw
	if talking:
		head_yaw = sin(_t * 1.9) * 0.18
		head_pitch = sin(_t * 3.4) * 0.08 - 0.03
		arm_gesture_r = 0.5 + 0.5 * sin(_t * 2.3)
		arm_gesture_l = maxf(0.0, sin(_t * 1.3 + 1.0))
	# legs
	for side in ["l", "r"]:
		var sgn := 1.0 if side == "l" else -1.0
		var f := sw * sgn                       # forward amount of this leg (positive = forward)
		var thigh := -f * 0.62 * bw
		var knee := maxf(0.0, cw * sgn) * 0.95 * bw + 0.04
		_rot("leg_up_" + side, thigh, 0.0, sgn * -0.01)
		_rot("leg_low_" + side, knee)
		# arms swing opposite to the leg on the same side
		var af := -f
		var up := -af * 0.55 * bw
		var elbow := -(0.12 + 0.3 * maxf(0.0, af)) * bw - 0.1 * iw
		var gest := arm_gesture_r if side == "r" else arm_gesture_l
		up = lerpf(up, -0.9 - 0.2 * sin(_t * 4.0), gest * 0.8) + sin(_t * 1.1 + sgn) * 0.025 * iw
		elbow = lerpf(elbow, -1.1 + 0.3 * sin(_t * 5.1), gest * 0.8)
		var spread := sgn * (0.05 + 0.02 * breathe) * -1.0
		var ua := up
		var la := elbow
		match _shot:
			"reach":
				if side == "r":
					ua = lerpf(up, -1.35, b)
					la = lerpf(elbow, -0.35, b)
			"attack":
				if side == "r":
					var u := clampf(_shot_t / _shot_len, 0.0, 1.0)
					ua = lerpf(0.9, -1.6, smoothstep(0.0, 0.5, u)) if u < 0.55 else lerpf(-1.6, up, (u - 0.55) / 0.45)
					la = lerpf(-0.4, -0.2, u)
			"cast":
				ua = lerpf(up, -1.9, b)
				la = lerpf(elbow, -0.2, b)
			"victory":
				ua = lerpf(up, -2.7, b)
				la = lerpf(elbow, -0.15, b)
			"hurt":
				ua = lerpf(up, 0.6, b)
				la = lerpf(elbow, -0.5, b)
			"bow":
				ua = lerpf(up, 0.15, b)
				la = lerpf(elbow, -0.7, b)
		_rot("arm_up_" + side, ua, 0.0, spread)
		_rot("arm_low_" + side, la)
	# one-shot body poses
	var lunge := 0.0
	match _shot:
		"attack":
			var u2 := clampf(_shot_t / _shot_len, 0.0, 1.0)
			torso_pitch += -0.35 * sin(u2 * PI)
			torso_yaw += 0.4 * (1.0 - u2) - 0.5 * smoothstep(0.3, 0.6, u2) * (1.0 - u2)
			lunge = 0.35 * sin(u2 * PI)
		"hurt":
			torso_pitch += 0.28 * b
			head_pitch += 0.3 * b
			lunge = -0.12 * b
		"bow":
			torso_pitch += -0.5 * b
			head_pitch += -0.2 * b
		"cast":
			torso_pitch += 0.12 * b
			head_pitch += -0.25 * b
		"victory":
			torso_pitch += 0.1 * b
			head_pitch += -0.25 * b
		"reach":
			torso_pitch += -0.3 * b
			head_pitch += 0.1 * b
	var torso: Node3D = parts.torso
	torso.rotation = Vector3(torso_pitch, torso_yaw, 0.0)
	torso.scale = Vector3(1.0, 1.0 + breathe * 0.008, 1.0 + breathe * 0.012)
	_rot("head", head_pitch - torso_pitch * 0.6, head_yaw - torso_yaw * 0.7)
	model.position.z = lunge
	if _shot == "die":
		var u3 := clampf(_shot_t / 0.9, 0.0, 1.0)
		model.rotation.x = lerpf(0.0, -PI / 2.0 + 0.1, smoothstep(0.0, 1.0, u3))
		model.position.y = lerpf(0.0, 0.18, u3)
	elif dead:
		model.rotation.x = -PI / 2.0 + 0.1
		model.position.y = 0.18
	else:
		model.rotation.x = 0.0
		if _shot == "":
			model.position.y = 0.0


func _anim_quad(walking: bool) -> void:
	var w := _gait * 1.15
	var bw := _walk_blend
	var iw := 1.0 - bw
	var sw := sin(w)
	var cw := cos(w)
	var breathe := sin(_t * 2.2)
	if walking:
		if (sw > 0.0) != (_last_phase > 0.0):
			step.emit()
		_last_phase = sw
	var body: Node3D = parts.body
	body.position.y = _rest_y + absf(cw) * 0.03 * bw + breathe * 0.004
	body.rotation = Vector3(sin(w * 2.0) * 0.02 * bw, sw * 0.04 * bw, 0.0)
	body.scale = Vector3(1.0, 1.0 + breathe * 0.012, 1.0 + breathe * 0.015)
	var pairs := {"fl": 1.0, "br": 1.0, "fr": -1.0, "bl": -1.0}
	for nm in pairs:
		var f: float = sw * float(pairs[nm])
		_rot("leg_up_" + nm, -f * 0.65 * bw)
		_rot("leg_low_" + nm, maxf(0.0, cw * float(pairs[nm])) * 0.9 * bw)
	var jaw := 0.0
	var head_p := sin(_t * 1.1) * 0.1 * iw - 0.05 * bw
	var lunge := 0.0
	match _shot:
		"attack":
			var u := clampf(_shot_t / _shot_len, 0.0, 1.0)
			jaw = 0.6 * maxf(0.0, sin(u * PI * 2.0))
			head_p += -0.35 * sin(u * PI)
			lunge = -0.45 * sin(u * PI)
		"hurt":
			head_p += 0.4 * _bump()
			lunge = 0.15 * _bump()
		"howl":
			head_p += -0.9 * _bump()
			jaw = 0.5 * _bump()
	_rot("head", head_p, sin(_t * 0.5) * 0.3 * iw)
	_rot("jaw", jaw)
	_rot("tail", 0.0, sin(_t * (5.0 + 5.0 * bw)) * (0.35 + 0.25 * bw))
	model.position.z = -lunge
	if _shot == "die":
		var u3 := clampf(_shot_t / 0.8, 0.0, 1.0)
		model.rotation.z = lerpf(0.0, PI / 2.0, u3)
		model.position.y = lerpf(0.0, 0.25, u3)
	elif dead:
		model.rotation.z = PI / 2.0
		model.position.y = 0.25


func _anim_bat() -> void:
	var f := _t * 14.0
	_rot("wing_l", 0.0, 0.0, sin(f) * 0.75)
	_rot("wing_r", 0.0, 0.0, -sin(f) * 0.75)
	_rot("wing_l_tip", 0.0, 0.0, sin(f - 0.9) * 0.6)
	_rot("wing_r_tip", 0.0, 0.0, -sin(f - 0.9) * 0.6)
	var body: Node3D = parts.body
	body.position.y = _rest_y + sin(f * 0.5) * 0.04
	body.rotation.x = sin(f * 0.5) * 0.08
