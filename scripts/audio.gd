extends Node
## Music / ambience / sound effects. Streams come from data/audio.json (assets/audio/*.ogg, made by pipeline/audio_gen.py).
## Channels have their own bus and volume (saved in Game.meta.audio). Mood (ambience + music) is derived from the location.

const CHANNELS := ["Music", "Ambience", "SFX"]

var index: Dictionary = {}
var volume := {"master": 0.8, "music": 0.7, "ambience": 0.8, "sfx": 0.9}
var _players := {"Music": [], "Ambience": []}
var _active := {"Music": 0, "Ambience": 0}
var _current := {"Music": "", "Ambience": ""}
var _sfx_pool: Array = []
var _howl_timer := 0.0
var _howling := false
var _streams: Dictionary = {}
var enabled := true


func _ready() -> void:
	var f := FileAccess.open("res://data/audio.json", FileAccess.READ)
	if f != null:
		index = JSON.parse_string(f.get_as_text())
	for ch in CHANNELS:
		if AudioServer.get_bus_index(ch) < 0:
			AudioServer.add_bus()
			AudioServer.set_bus_name(AudioServer.bus_count - 1, ch)
			AudioServer.set_bus_send(AudioServer.bus_count - 1, "Master")
	for ch in ["Music", "Ambience"]:
		for i in 2:
			var p := AudioStreamPlayer.new()
			p.bus = ch
			p.volume_db = -80.0
			add_child(p)
			_players[ch].append(p)
	for i in 8:
		var p := AudioStreamPlayer.new()
		p.bus = "SFX"
		add_child(p)
		_sfx_pool.append(p)
	var saved: Variant = Game.meta.get("audio", null)
	if saved is Dictionary:
		for k in saved:
			volume[k] = float(saved[k])
	apply_volumes()
	_howl_timer = randf_range(20.0, 45.0)
	Game.journal_added.connect(func(_id: String) -> void: sfx("page"))
	Game.card_requested.connect(func(_t: String, _g: String) -> void: sfx("card"))
	Game.ending.connect(func(_t: String) -> void:
		sfx("bell")
		music("mus_sad", 3.0))
	Game.goto_requested.connect(func(_to: String, _from: String) -> void: sfx("door"))


func apply_volumes() -> void:
	AudioServer.set_bus_volume_db(0, linear_to_db(maxf(volume.master, 0.0001)))
	AudioServer.set_bus_volume_db(AudioServer.get_bus_index("Music"), linear_to_db(maxf(volume.music, 0.0001)))
	AudioServer.set_bus_volume_db(AudioServer.get_bus_index("Ambience"), linear_to_db(maxf(volume.ambience, 0.0001)))
	AudioServer.set_bus_volume_db(AudioServer.get_bus_index("SFX"), linear_to_db(maxf(volume.sfx, 0.0001)))


func set_volume(channel: String, v: float) -> void:
	volume[channel] = v
	apply_volumes()
	Game.meta["audio"] = volume.duplicate()
	Game.save_meta()


func _stream(name: String) -> AudioStream:
	if _streams.has(name):
		return _streams[name]
	var e: Dictionary = index.get(name, {})
	if e.is_empty() or not ResourceLoader.exists("res://" + str(e.file)):
		return null
	var s: AudioStream = load("res://" + str(e.file))
	if s is AudioStreamOggVorbis:
		s = s.duplicate()
		(s as AudioStreamOggVorbis).loop = bool(e.get("loop", false))
	_streams[name] = s
	return s


func _crossfade(channel: String, name: String, fade: float) -> void:
	if not enabled or _current[channel] == name:
		return
	_current[channel] = name
	var old: AudioStreamPlayer = _players[channel][_active[channel]]
	_active[channel] = 1 - _active[channel]
	var nw: AudioStreamPlayer = _players[channel][_active[channel]]
	var tw := create_tween().set_parallel(true)
	tw.tween_property(old, "volume_db", -80.0, fade)
	var s := _stream(name) if name != "" else null
	if s != null:
		nw.stream = s
		nw.volume_db = -80.0
		nw.play()
		tw.tween_property(nw, "volume_db", float(index[name].get("db", -8)), fade)
	tw.chain().tween_callback(func() -> void:
		if old != nw:
			old.stop())


func music(name: String, fade: float = 2.0) -> void:
	_crossfade("Music", name, fade)


func ambience(name: String, fade: float = 2.0) -> void:
	_crossfade("Ambience", name, fade)
	_howling = name in ["amb_wind", "amb_snow"]


func sfx(name: String, pitch: float = 1.0, db: float = 0.0) -> void:
	if not enabled:
		return
	var s := _stream("sfx_" + name if not name.begins_with("sfx_") else name)
	if s == null:
		return
	for p in _sfx_pool:
		if not (p as AudioStreamPlayer).playing:
			p.stream = s
			p.pitch_scale = pitch * randf_range(0.96, 1.04)
			p.volume_db = float(index.get(name if name.begins_with("sfx_") else "sfx_" + name, {}).get("db", -6)) + db
			p.play()
			return


func _process(delta: float) -> void:
	if _howling:
		_howl_timer -= delta
		if _howl_timer <= 0.0:
			_howl_timer = randf_range(25.0, 55.0)
			sfx("howl", randf_range(0.85, 1.1), -6.0)


## Pick ambience + music for a location from its id and data.
func mood_for(loc_id: String, ld: Dictionary) -> Dictionary:
	var amb: String = str(ld.get("ambience", ""))
	var mus: String = str(ld.get("music", ""))
	var id := loc_id
	var interior: bool = ld.get("interior", true)
	var fog := Color(str(ld.get("ambient", {}).get("fog", "#000000")))
	var day := fog.v > 0.55
	if amb == "":
		if _has(id, ["storm"]):
			amb = "amb_storm"
		elif _has(id, ["harbour", "quay", "sea", "demeter", "deck", "launch", "brig", "bows", "wheel", "cabin", "hold", "galley", "forecastle", "river", "rapids", "schooner", "pier", "wreck"]):
			amb = "amb_sea"
		elif _has(id, ["crypt", "tomb", "vault", "chapel", "coffin", "cellar", "catacomb"]):
			amb = "amb_crypt"
		elif _has(id, ["asylum", "ward", "dispensary", "renfield", "cell", "scullery"]):
			amb = "amb_asylum"
		elif _has(id, ["snow", "plain", "mountain", "sunset"]):
			amb = "amb_snow"
		elif _has(id, ["street", "piccadilly", "london", "mile_end", "bermondsey", "bloxam", "yard", "station", "paddington", "carter", "exeter", "close"]) and not interior:
			amb = "amb_city"
		elif not interior:
			amb = "amb_day" if day else "amb_wind"
		else:
			amb = "amb_fire" if _warm(ld) else "amb_interior"
	if mus == "":
		if _has(id, ["epilogue", "funeral", "sickroom", "deathbed", "grief"]):
			mus = "mus_sad"
		elif _has(id, ["crypt", "tomb", "vault", "brides", "old_wing", "hold", "dark", "castle_chapel", "carfax_chapel", "scholomance", "tithe"]):
			mus = "mus_dread"
		else:
			mus = "mus_explore"
	return {"ambience": amb, "music": mus}


func _has(id: String, keys: Array) -> bool:
	for k in keys:
		if id.contains(k):
			return true
	return false


func _warm(ld: Dictionary) -> bool:
	for l in ld.get("lights", []):
		var c := Color(str(l.color))
		if c.r > 0.9 and c.b < 0.6:
			return true
	return false


func set_mood(loc_id: String, ld: Dictionary) -> void:
	var m := mood_for(loc_id, ld)
	ambience(m.ambience)
	music(m.music)
