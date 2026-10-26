class_name MixamoRig
extends RefCounted
## Skinned Mixamo characters + the shared animation library (assets/anims/mixamo_lib.glb, built by
## pipeline/mixamo/export_mixamo.py). All characters share the Mixamo skeleton, so one library drives them all.

const LIB_PATH := "res://assets/anims/mixamo_lib.glb"
const LOOPING := ["idle", "walk", "run", "sneak", "sit", "talk", "hang", "ladder", "climb", "convulse", "fallen", "zombie_idle", "look_far", "victory_idle", "block", "pose"]

## Procedural human models that have a dressed Bot (assets/models/chars/sk_<model>.glb from pipeline/mixamo/dress.py).
## Params (height, sex, build) come from data/humans.json; colours come from the model's variants like any other model.
static var _humans: Dictionary = {}

static var _raw: Dictionary = {}       # name -> Animation as exported
static var _lib_hips_rest := Vector3.ZERO
static var _libs: Dictionary = {}      # per skeleton proportion: AnimationLibrary
static var enabled := true


static func config_for(model_id: String, variant: String) -> Dictionary:
	if not enabled:
		return {}
	if _humans.is_empty():
		var f := FileAccess.open("res://data/humans.json", FileAccess.READ)
		if f != null:
			_humans = JSON.parse_string(f.get_as_text())
	if not _humans.has(model_id):
		return {}
	var glb := "res://assets/models/chars/sk_%s.glb" % model_id
	if not ResourceLoader.exists(glb):
		return {}
	var h: Dictionary = _humans[model_id]
	return {"glb": glb, "model": model_id, "height": float(h.get("height", 1.75)), "build": float(h.get("build", 1.0)),
		"female": str(h.get("sex", "m")) == "f"}


static func _load_raw() -> void:
	if not _raw.is_empty():
		return
	var scene: Node = (load(LIB_PATH) as PackedScene).instantiate()
	var ap: AnimationPlayer = scene.find_children("*", "AnimationPlayer", true, false)[0]
	var sk: Skeleton3D = scene.find_children("*", "Skeleton3D", true, false)[0]
	_lib_hips_rest = sk.get_bone_rest(sk.find_bone("mixamorig_Hips")).origin
	for n in ap.get_animation_list():
		_raw[n] = ap.get_animation(n).duplicate()
	scene.free()


## Shared library retargeted to one skeleton's proportions: only the hips keep a position track (height scaled to this
## skeleton, no forward travel), every other bone is rotation-only so differently sized rigs do not stretch.
static func library_for(sk: Skeleton3D) -> AnimationLibrary:
	_load_raw()
	var hips := sk.find_bone("mixamorig_Hips")
	var rc: Vector3 = sk.get_bone_rest(hips).origin
	var key := str(snappedf(rc.length(), 0.5))
	if _libs.has(key):
		return _libs[key]
	var lib := AnimationLibrary.new()
	var ratio := rc.length() / maxf(_lib_hips_rest.length(), 0.001)
	for n in _raw:
		var a: Animation = (_raw[n] as Animation).duplicate()
		_retarget(a, rc, ratio)
		a.loop_mode = Animation.LOOP_LINEAR if _is_loop(str(n)) else Animation.LOOP_NONE
		lib.add_animation(n, a)
	_libs[key] = lib
	return lib


static func _retarget(a: Animation, rc: Vector3, ratio: float) -> void:
	var i := a.get_track_count() - 1
	while i >= 0:
		var t := a.track_get_type(i)
		var is_hips := str(a.track_get_path(i)).ends_with("mixamorig_Hips")
		if t == Animation.TYPE_SCALE_3D:
			a.remove_track(i)
		elif t == Animation.TYPE_POSITION_3D:
			if not is_hips:
				a.remove_track(i)
			else:
				var up := 0                              # vertical axis of skeleton space = largest component of the hips rest
				for ax in 3:
					if absf(_lib_hips_rest[ax]) > absf(_lib_hips_rest[up]):
						up = ax
				for k in a.track_get_key_count(i):
					var v: Vector3 = a.track_get_key_value(i, k)
					var o := rc
					o[up] = rc[up] + (v[up] - _lib_hips_rest[up]) * ratio
					a.track_set_key_value(i, k, o)
		i -= 1


static func _is_loop(n: String) -> bool:
	for l in LOOPING:
		if n == l or n.begins_with(l):
			return true
	return false


## Instantiate a character GLB with an AnimationPlayer ("anim") that has the shared library as default.
static func build(char_glb: String) -> Node3D:
	var root: Node3D = (load(char_glb) as PackedScene).instantiate()
	for n in root.get_children():
		if n is MeshInstance3D and n.name == "Cube":
			n.queue_free()
	var ap := AnimationPlayer.new()
	ap.name = "anim"
	root.add_child(ap)
	ap.root_node = ap.get_path_to(root)
	var sks := root.find_children("*", "Skeleton3D", true, false)
	ap.add_animation_library("", library_for(sks[0]))
	add_cloth_physics(root)
	return root


## Real-time cloth: every chain of "cloth_<name>_c<col>_b<i>" bones (costume.py) is driven by a spring bone setting,
## with capsules on the legs and spine so skirts and capes slide over the body.
static func add_cloth_physics(root: Node3D, stiffness: float = 0.9, drag: float = 0.45, gravity: float = 1.0) -> void:
	var found := root.find_children("*", "Skeleton3D", true, false)
	if found.is_empty():
		return
	var sk: Skeleton3D = found[0]
	var chains := {}
	for b in sk.get_bone_count():
		var n := sk.get_bone_name(b)
		if n.begins_with("cloth_") and n.ends_with("_b0"):
			chains[n] = true
	if chains.is_empty():
		return
	var hips := sk.find_bone("mixamorig_Hips")
	var u := 100.0 if hips >= 0 and sk.get_bone_global_rest(hips).origin.length() > 10.0 else 1.0   # glTF skeleton is in cm
	var down := Vector3(0, -1, 0)                    # in the glTF skeleton space of these rigs "down" is -Y (verified by render)
	var sim := SpringBoneSimulator3D.new()
	sim.name = "spring"
	sk.add_child(sim)
	var cols: Array[SpringBoneCollision3D] = []   # children of the simulator -> used by every setting
	for def in [["mixamorig_LeftUpLeg", 0.12, 0.4], ["mixamorig_RightUpLeg", 0.12, 0.4], ["mixamorig_LeftLeg", 0.085, 0.42],
			["mixamorig_RightLeg", 0.085, 0.42], ["mixamorig_Spine1", 0.17, 0.3]]:
		if sk.find_bone(def[0]) < 0:
			continue
		var c := SpringBoneCollisionCapsule3D.new()
		c.bone_name = def[0]
		c.radius = def[1] * u
		c.height = def[2] * u
		sim.add_child(c)
		cols.append(c)
	sim.setting_count = chains.size()
	var i := 0
	for root_name in chains:
		var base := str(root_name).trim_suffix("_b0")
		sim.set_root_bone(i, sk.find_bone(root_name))
		sim.set_end_bone(i, sk.find_bone(base + "_b2"))
		sim.set_gravity_direction(i, down)
		sim.set_extend_end_bone(i, true)
		sim.set_end_bone_length(i, 0.12 * u)
		sim.set_end_bone_direction(i, SkeletonModifier3D.BONE_DIRECTION_FROM_PARENT)
		sim.set_radius(i, 0.035 * u)
		var is_cape := str(root_name).begins_with("cloth_cape")
		sim.set_stiffness(i, stiffness if is_cape else 2.0)       # skirts keep their flare, capes hang freer
		sim.set_drag(i, drag)
		sim.set_gravity(i, (gravity if is_cape else 0.25) * u)
		i += 1


## Scale a freshly built character to its target height (from the skinned mesh bounds).
static func fit_height(root: Node3D, height: float) -> void:
	var top := 0.0
	var bottom := 0.0
	var first := true
	for m in root.find_children("*", "MeshInstance3D", true, false):
		var mi := m as MeshInstance3D
		var bb := mi.global_transform * mi.get_aabb()
		if first:
			top = bb.end.y
			bottom = bb.position.y
			first = false
		else:
			top = maxf(top, bb.end.y)
			bottom = minf(bottom, bb.position.y)
	if top - bottom > 0.1:
		root.scale = Vector3.ONE * (height / (top - bottom))
