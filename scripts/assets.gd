extends Node
## Model + texture library. Reads data/manifest.json (written by the asset
## pipeline) and builds models with a chosen texture variant. The same .glb is
## reused by swapping the texture of each material role.

var manifest: Dictionary = {}
var _mats: Dictionary = {}
var _scenes: Dictionary = {}


func _ready() -> void:
	var f := FileAccess.open("res://data/manifest.json", FileAccess.READ)
	if f == null:
		push_error("data/manifest.json missing - run pipeline/build_assets.py")
		return
	manifest = JSON.parse_string(f.get_as_text())


func has_model(id: String) -> bool:
	return manifest.get("models", {}).has(id)


func model_ids() -> Array:
	var ids: Array = manifest.models.keys()
	ids.sort()
	return ids


func variants_of(id: String) -> Array:
	return manifest.models[id].variants.keys()


func default_variant(id: String) -> String:
	return manifest.models[id].default


func instantiate(id: String, variant: String = "") -> Node3D:
	var m: Dictionary = manifest.models[id]
	var ps: PackedScene = _scenes.get(id)
	if ps == null:
		ps = load("res://" + str(m.file))
		_scenes[id] = ps
	var root: Node3D = ps.instantiate()
	root.set_meta("model_id", id)
	apply_variant(root, id, variant if variant != "" else str(m.default))
	return root


func apply_variant(root: Node, id: String, variant: String) -> void:
	var v: Dictionary = manifest.models[id].variants.get(variant, {})
	root.set_meta("variant", variant)
	for n in _meshes(root):
		var mi: MeshInstance3D = n
		if mi.mesh == null:
			continue
		for s in mi.mesh.get_surface_count():
			var src: Material = mi.mesh.surface_get_material(s)
			var role: String = src.resource_name if src != null else ""
			if v.has(role):
				mi.set_surface_override_material(s, material_for(v[role]))


func _meshes(n: Node) -> Array:
	var out: Array = []
	if n is MeshInstance3D:
		out.append(n)
	for c in n.get_children():
		out.append_array(_meshes(c))
	return out


func material_for(spec: Dictionary) -> StandardMaterial3D:
	var key: String = "%s|%s" % [spec.tex, spec.tint]
	if _mats.has(key):
		return _mats[key]
	var t: Dictionary = manifest.textures[spec.tex]
	var mat := StandardMaterial3D.new()
	mat.resource_name = key
	mat.albedo_texture = load("res://assets/" + str(t.albedo))
	mat.albedo_color = Color(str(spec.tint))
	mat.normal_enabled = true
	mat.normal_texture = load("res://assets/" + str(t.normal))
	var wsz := float(t.get("world", 1.0))
	mat.uv1_scale = Vector3(1.0 / wsz, 1.0 / wsz, 1.0)
	mat.roughness = float(t.get("roughness", 0.8))
	mat.metallic = float(t.get("metallic", 0.0))
	mat.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC
	if t.has("emission"):
		mat.emission_enabled = true
		mat.emission = Color(str(spec.tint))
		mat.emission_energy_multiplier = float(t.emission)
	if t.has("alpha"):
		mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		mat.albedo_color.a = float(t.alpha)
	_mats[key] = mat
	return mat
