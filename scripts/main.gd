extends Node
## Orchestrates title -> locations -> dialogue -> ending. Debug args after `--`:
##   --loc=<id>  --give=a,b  --flags=x,y  --shot=<png>  --frames=<n>

var hud: HUD
var loc: Location
var _busy := false
var _args: Dictionary = {}


## Opening titles over the title screen (normal launch only; `--intro` forces, `--nointro` skips).
func _play_intro() -> void:
	var layer := CanvasLayer.new()
	layer.layer = 100
	add_child(layer)
	var intro := Intro.new()
	layer.add_child(intro)
	intro.finished.connect(layer.queue_free)


func _ready() -> void:
	for a in OS.get_cmdline_user_args():
		var kv := a.trim_prefix("--").split("=", true, 1)
		_args[kv[0]] = kv[1] if kv.size() > 1 else "1"
	hud = HUD.new()
	add_child(hud)
	for a in OS.get_cmdline_user_args():
		if a in ["--selftest", "--arcflow", "--combattest", "--genworld"] or a.begins_with("--act") or a.begins_with("--arc=") or a.begins_with("--replay"):
			Audio.enabled = false
	Audio.music("mus_title", 0.5)
	if (_args.is_empty() or _args.has("intro")) and not _args.has("nointro"):
		_play_intro()
	hud.start_pressed.connect(_start)
	hud.continue_pressed.connect(_continue)
	Game.goto_requested.connect(_goto)
	Game.map_requested.connect(hud.open_map)
	Game.pie_requested.connect(hud.show_pie)
	Game.ending.connect(func(t: String) -> void: hud.show_ending(t))
	Game.fight_requested.connect(_fight)
	Game.arc_finished.connect(_arc_finished)
	hud.arc_requested.connect(_start_arc)
	Game.force_regions = _args.has("region") or _args.has("actiontest") or _args.has("action")
	if _args.has("actiontest") or _args.has("action"):
		Game.meta["action_mode"] = true
	if _args.has("selftest") or _args.has("replay") or _args.has("act") or _args.has("arc") or _args.has("loc") or _args.has("combattest"):
		hud.fast_fade = _args.has("selftest") or _args.has("replay") or _args.has("act") or _args.has("arc")
		Game.autosave = false
	if _args.has("arc"):
		_args["replay"] = "res://data/plans/arc_%s.json" % _args.arc
	if _args.has("act") or _args.has("replay") or _args.has("arc"):
		hud._title.visible = false
		var rc: int = await SelfTest.new().replay(self, str(_args.get("replay", "res://data/plans/act_%s.json" % _args.get("act", "1"))),
				int(_args.get("seed", "1")), str(_args.get("world", "default")) == "default")
		get_tree().quit(rc)
		return
	if _args.has("genworld"):
		Game.new_game(int(_args.genworld), false)
		print("world written: ", ProjectSettings.globalize_path("user://worlds/%s.json" % _args.genworld))
		get_tree().quit()
		return
	if _args.has("mapshot"):
		Game.autosave = false
		Game.new_game(1, true)
		for k in Game.resolved.locations:
			if str(k).begins_with(str(_args.get("vis", "a2_"))):
				Game.visited[k] = true
		Game.current = str(_args.get("loc", "a2_harbour"))
		hud._title.visible = false
		print("MAP has=", TravelMap.has_map(Game.current), " modal=", hud.modal, " cur=", Game.current)
		hud.modal = false
		hud.open_map()
		await get_tree().create_timer(0.8).timeout
		get_viewport().get_texture().get_image().save_png(str(_args.mapshot))
		get_tree().quit()
		return
	if _args.has("chronicle"):
		Game.autosave = false
		Game.new_game(1, true)
		for pid in ["mina", "seward", "quincey", "arthur", "vanhelsing"]:
			Game.meet(pid)
		Game.add_journal("a1_j7")
		Game.meta["game_complete"] = true
		hud._title.visible = false
		hud.toggle_chronicle()
		await get_tree().create_timer(1.0).timeout
		get_viewport().get_texture().get_image().save_png(str(_args.get("shot", "/tmp/chron.png")))
		get_tree().quit()
		return
	if _args.has("partyscreen"):
		Game.autosave = false
		Game.new_game(1, true)
		for pid in ["mina", "vanhelsing", "seward", "quincey", "arthur"]:
			Game.recruit(pid)
		for it in ["kukri", "winchester", "sword_cane", "lords_riding_coat", "buffalo_coat", "crucifix", "arthur_burden_signet", "travel_shawl", "bullet"]:
			Game.give(it)
		Game.grant_xp(Game.party, 190)
		Game.equip("arthur", "weapon", "sword_cane")
		Game.equip("arthur", "armor", "lords_riding_coat")
		Game.equip("arthur", "charm", "arthur_burden_signet")
		Game.equip("quincey", "armor", "buffalo_coat")
		Game.equip("harker", "weapon", "kukri")
		hud._title.visible = false
		hud._pp_sel = "arthur"
		hud.toggle_party()
		await get_tree().create_timer(1.0).timeout
		get_viewport().get_texture().get_image().save_png(str(_args.get("shot", "/tmp/party.png")))
		get_tree().quit()
		return
	if _args.has("audiocheck"):
		var rc3: int = await SelfTest.new().audio_check(self)
		get_tree().quit(rc3)
		return
	if _args.has("arcflow"):
		var rc2: int = await SelfTest.new().arc_flow(self)
		get_tree().quit(rc2)
		return
	if _args.has("combattest"):
		CombatTest.run(int(_args.get("runs", "100")))
		get_tree().quit()
		return
	if _args.has("selftest"):
		hud._title.visible = false
		var code := 0
		for sd in str(_args.get("seeds", "1")).split(",", false):
			code += await SelfTest.new().run(self, int(sd))
		get_tree().quit(code)
		return
	if _args.has("loc"):
		hud._title.visible = false
		_start()
		if _args.has("fight"):
			await get_tree().create_timer(1.6).timeout
			_fight(str(_args.fight), "")
			if _args.has("shot"):
				await get_tree().create_timer(2.2).timeout
				get_viewport().get_texture().get_image().save_png(str(_args.shot))
				get_tree().quit()


func _continue() -> void:
	var loc_id := Game.load_game()
	if loc_id == "":
		_start()
		return
	_goto(loc_id, "", true)


func _start() -> void:
	Game.new_game(WorldGen.seed_from_text(str(_args.get("seed", hud.seed_text()))))
	hud.say("Seed %d" % Game.seed_value)
	for i in str(_args.get("give", "")).split(",", false):
		Game.give(i)
	for f in str(_args.get("flags", "")).split(",", false):
		Game.flags[f] = true
	for pm in str(_args.get("party", "")).split(",", false):
		Game.recruit(pm)
	for gi in str(_args.get("items", "")).split(",", false):
		var kv := gi.split(":")
		Game.give(kv[0], int(kv[1]) if kv.size() > 1 else 1)
	var first: String = str(_args.get("loc", Game.world.start_location))
	_goto(first, "", true)


var _link_test_started := false


func _goto(loc_id: String, from_loc: String, instant := false) -> void:
	if _busy:
		return
	_busy = true
	hud.modal = true
	var is_dungeon := Dungeon.exists(loc_id)
	var rid := "" if is_dungeon else (Regions.region_of(loc_id) if Regions.enabled() else "")
	if rid != "" and loc != null and loc.region == rid and is_instance_valid(loc):
		# already inside this region: just walk the player over to the other place
		await hud.fade_to(1.0, 0.3)
		var np := loc.region_spawn(loc_id, from_loc)
		loc.player.position = np
		loc.player.stop()
		loc.pending = {}
		loc._cam_look = Vector3(np.x, 1.0, np.z - 1.4)
		loc._member = loc_id
		loc.apply_member_mood(loc_id)
		_member_entered(loc_id)
		await hud.fade_to(0.0, 0.4)
		hud.modal = false
		_busy = false
		return
	if loc != null:
		loc.queue_free()
		await get_tree().process_frame
	loc = Location.new()
	add_child(loc)
	if is_dungeon:
		loc.build_dungeon(loc_id, from_loc)
		loc.dungeon_exit.connect(func(to: String) -> void: _goto(to, loc_id))
	elif rid != "":
		loc.build_region(rid, loc_id, from_loc)
		loc.member_changed.connect(_member_entered)
	else:
		loc.build(loc_id, from_loc)
	Game.current = loc_id
	Audio.set_mood(loc_id, loc.data)
	Game.apply_act_start(loc_id)
	Game.save_game()
	loc.hover_changed.connect(hud.set_hover)
	if _args.has("at"):
		var xz := str(_args.at).split(",")
		loc.player.position = Vector3(float(xz[0]), 0, float(xz[1]))
	var title := ""
	for l in Game.world.locations:
		if l.id == loc_id:
			title = str(l.name)
			if not Game.visited.has(loc_id):
				hud.say(str(l.desc))
	Game.visited[loc_id] = true
	hud.set_location_title(title)
	await hud.fade_to(0.0, 0.6)
	hud.modal = false
	_busy = false
	_on_enter(loc_id)
	if _args.has("actiontest"):
		Engine.time_scale = 6.0
		var am: ActionMode = null
		for c in loc.get_children():
			if c is ActionMode:
				am = c
		print("ACTIONTEST enemies: ", am.enemies.size() if am else -1)
		var kills := 0
		var deaths_before := 0
		for i in am.enemies.size():
			var en: Dictionary = am.enemies[i]
			loc.player.position = (en.node.position as Vector3) + Vector3(1.2, 0, 0)
			am.target = i
			var t := 0.0
			var st: Dictionary = Game.member_state[Game.protagonist]
			st.hp = Game.effective(Game.protagonist).max_hp
			while not en.dead and t < 40.0:
				await get_tree().create_timer(0.25).timeout
				t += 0.25
				if int(st.hp) <= 3:
					st.hp = Game.effective(Game.protagonist).max_hp
					deaths_before += 1
			if en.dead:
				kills += 1
			print("ACTIONTEST ", en.def.name, " dead=", en.dead, " player hp=", st.hp)
		print("ACTIONTEST kills ", kills, "/", am.enemies.size(), " xp=", Game.member_state[Game.protagonist].xp, " ", "PASS" if kills == am.enemies.size() else "FAIL")
		get_tree().quit(0 if kills == am.enemies.size() else 1)
		return
	if _args.has("pietest"):
		Engine.time_scale = 6.0
		loc._open_pie("a2_h_garlic", Vector2(640, 330))
		await get_tree().process_frame
		print("PIETEST open=", hud._pie.visible, " modal=", hud.modal)
		hud._pie.chosen.emit("take")
		var t := 0.0
		while not Game.has_item("garlic") and t < 20.0:
			await get_tree().create_timer(0.25).timeout
			t += 0.25
		print("PIETEST modal after=", hud.modal, " garlic=", Game.has_item("garlic"), " ", "PASS" if Game.has_item("garlic") and not hud.modal else "FAIL")
		get_tree().quit()
		return
	if _args.has("cellartest") and not _link_test_started:
		## Act V: the two-floor cellars below the Carfax chapel -- gated by the rats, a journal and gifts on each floor, stairs between them.
		_link_test_started = true
		Engine.time_scale = 8.0
		var ok := loc.entities.has("dungeon_carfax_cellar_f0_door")
		loc._primary("dungeon_carfax_cellar_f0_door")      # rats still about: refuses
		await get_tree().create_timer(0.8).timeout
		ok = ok and Game.current == "a5_carfax_chapel"
		print("CELLARTEST refuses while the rats live: ", Game.current == "a5_carfax_chapel")
		Game.set_flag("won:carfax_rats")
		loc._primary("dungeon_carfax_cellar_f0_door")
		var t := 0.0
		while Game.current != "dungeon_carfax_cellar_f0" and t < 20.0:
			await get_tree().create_timer(0.25).timeout
			t += 0.25
		await get_tree().create_timer(2.5).timeout
		ok = ok and Game.current == "dungeon_carfax_cellar_f0" and Game.journal.has("a5_j_cellar")
		print("CELLARTEST floor 0: ", Game.current, " journal ", Game.journal.has("a5_j_cellar"))
		loc._primary("cel_oil")
		loc._primary("cel_labels")
		await get_tree().create_timer(0.3).timeout
		ok = ok and Game.has_item("oil") and Game.journal.has("a5_j_labels")
		print("CELLARTEST oil + labels: ", Game.has_item("oil"), " ", Game.journal.has("a5_j_labels"))
		var def := Dungeon.load_def("dungeon_carfax_cellar_f0")
		var st: Dictionary = def.stairs_out[0]
		loc.go_to(Vector3(float(st.trigger[0]), 0, float(st.trigger[1])))
		t = 0.0
		while Game.current == "dungeon_carfax_cellar_f0" and t < 90.0:
			await get_tree().create_timer(0.25).timeout
			t += 0.25
		await get_tree().create_timer(2.5).timeout
		ok = ok and Game.current == "dungeon_carfax_cellar_f1" and Game.journal.has("a5_j_vault")
		print("CELLARTEST floor 1: ", Game.current, " journal ", Game.journal.has("a5_j_vault"))
		loc._primary("vlt_rope")
		loc._primary("vlt_well")
		await get_tree().create_timer(0.3).timeout
		ok = ok and Game.has_item("rope") and Game.flags.get("did:vlt_well", false)
		print("CELLARTEST rope + well: ", Game.has_item("rope"), " ", Game.flags.get("did:vlt_well", false))
		print("CELLARTEST ", "PASS" if ok else "FAIL")
		get_tree().quit(0 if ok else 1)
		return
	if _args.has("sidetest") and not _link_test_started:
		## --sidetest=<door entity>|<journal on arrival>|<prop to use>|<item expected>  (a side area entered from the current location)
		_link_test_started = true
		Engine.time_scale = 8.0
		var parts := str(_args.sidetest).split("|")
		var door_id := parts[0]
		var ok := loc.entities.has(door_id)
		var dest := str(loc.entities[door_id].data.interact.go) if ok else ""
		var origin: String = Game.current
		loc._primary(door_id)
		var t := 0.0
		while Game.current != dest and t < 20.0:
			await get_tree().create_timer(0.25).timeout
			t += 0.25
		await get_tree().create_timer(2.5).timeout
		ok = ok and Game.current == dest and Game.journal.has(parts[1])
		print("SIDETEST ", origin, " -> ", Game.current, " journal ", parts[1], ": ", Game.journal.has(parts[1]))
		ok = ok and loc.entities.has(parts[2])
		loc._primary(parts[2])
		await get_tree().create_timer(0.3).timeout
		var got: bool = Game.has_item(parts[3]) if parts[3] != "" else true
		print("SIDETEST ", parts[2], " gives ", parts[3], ": ", got)
		ok = ok and got
		var def := Dungeon.load_def(Game.current)
		var ent := Vector3(float(def.entrance.pos[0]), 0, float(def.entrance.pos[2]))
		var far := Vector3(float(def.rooms[0].center[0]), 0, float(def.rooms[0].center[1]))
		loc.go_to(far)
		t = 0.0
		while loc.player.position.distance_to(far) > 1.5 and t < 90.0:
			await get_tree().create_timer(0.25).timeout
			t += 0.25
		loc.go_to(ent)
		t = 0.0
		while Game.current == dest and t < 90.0:
			await get_tree().create_timer(0.25).timeout
			t += 0.25
		await get_tree().create_timer(1.5).timeout
		print("SIDETEST back in ", Game.current)
		ok = ok and Game.current == origin
		print("SIDETEST ", "PASS" if ok else "FAIL")
		get_tree().quit(0 if ok else 1)
		return
	if _args.has("stairtest") and not _link_test_started:
		## Two floors as two locations: walk onto the stair, arrive upstairs, walk onto the way back down, arrive on the first floor again.
		_link_test_started = true
		Engine.time_scale = 8.0
		var ok := true
		var start_id: String = Game.current
		var def := Dungeon.load_def(start_id)
		var out: Array = def.stairs_out
		print("STAIRTEST ", start_id, " has ", out.size(), " stair(s) out")
		ok = ok and out.size() > 0
		var tr := Vector3(float(out[0].trigger[0]), 0, float(out[0].trigger[1]))
		loc.go_to(tr)
		var t := 0.0
		while Game.current == start_id and t < 90.0:
			await get_tree().create_timer(0.25).timeout
			t += 0.25
		await get_tree().create_timer(2.5).timeout
		var up_id: String = Game.current
		print("STAIRTEST arrived on ", up_id, " at ", loc.player.position)
		ok = ok and up_id == str(out[0].to)
		var def2 := Dungeon.load_def(up_id)
		var back_ok := false
		for st in def2.stairs_out:
			if str(st.to) == start_id:
				var tr2 := Vector3(float(st.trigger[0]), 0, float(st.trigger[1]))
				var arrive_here := Vector3(float(out[0].arrive[0]), 0, float(out[0].arrive[1]))
				ok = ok and loc.player.position.distance_to(arrive_here) < 1.5
				loc.go_to(tr2)
				t = 0.0
				while Game.current == up_id and t < 90.0:
					await get_tree().create_timer(0.25).timeout
					t += 0.25
				await get_tree().create_timer(2.5).timeout
				back_ok = Game.current == start_id
				break
		print("STAIRTEST back down: ", back_ok, " now ", Game.current)
		ok = ok and back_ok
		print("STAIRTEST ", "PASS" if ok else "FAIL")
		get_tree().quit(0 if ok else 1)
		return
	if _args.has("dungeondoortest") and not _link_test_started:
		## Door panels swing open when the player is close, and shut again when he walks away.
		_link_test_started = true
		var doors: Array = Dungeon._doors
		print("DOORTEST panels: ", doors.size())
		var ok := doors.size() > 0
		for d in doors.slice(0, 3):
			var node: Node3D = d.node
			var mid: Vector3 = d.mid0
			var real: Vector3 = node.global_transform * (d.c as Vector3)
			print("DOORTEST   doorway middle ", mid, " vs the panel's actual middle ", real)
			ok = ok and mid.distance_to(real) < 0.05
			var closed_y: float = d.closed_y
			loc.player.position = Vector3(mid.x + 1.2, 0, mid.z + 1.2)
			await get_tree().create_timer(3.0).timeout
			var opened := absf(angle_difference(closed_y, node.rotation.y))
			loc.player.position = Vector3(mid.x + 12.0, 0, mid.z + 12.0)
			await get_tree().create_timer(3.0).timeout
			var shut := absf(angle_difference(closed_y, node.rotation.y))
			print("DOORTEST ", node.name, " opened by ", snappedf(rad_to_deg(opened), 1.0), " deg, shut again to ", snappedf(rad_to_deg(shut), 1.0), " deg")
			ok = ok and opened > 1.4 and shut < 0.1
		print("DOORTEST ", "PASS" if ok else "FAIL")
		get_tree().quit(0 if ok else 1)
		return
	if _args.has("ruinstorytest") and not _link_test_started:
		## Act VI: the ruined castle outside a6_castle_gate.
		_link_test_started = true
		Engine.time_scale = 8.0
		var ok := loc.entities.has("dungeon_castle_ruin_door")
		print("RUINTEST breach in a6_castle_gate: ", ok)
		loc._primary("dungeon_castle_ruin_door")
		var wt := 0.0
		while Game.current != "dungeon_castle_ruin" and wt < 20.0:
			await get_tree().create_timer(0.25).timeout
			wt += 0.25
		await get_tree().create_timer(2.5).timeout
		ok = ok and Game.current == "dungeon_castle_ruin" and Game.journal.has("a6_j_ward")
		print("RUINTEST inside + journal: ", Game.current, " ", Game.journal.has("a6_j_ward"))
		for eid in ["ward_merlon", "ward_beam", "ward_keep_door", "ward_caleche", "ward_pouch", "ward_glass", "ward_fire"]:
			var there: bool = loc.entities.has(eid)
			ok = ok and there
			print("RUINTEST entity ", eid, ": ", there)
		loc._primary("ward_beam")
		loc._primary("ward_pouch")
		ok = ok and Game.has_item("wood") and Game.has_item("bullet")
		print("RUINTEST wood + bullet: ", Game.has_item("wood"), " ", Game.has_item("bullet"))
		loc._primary("ward_fire")
		ok = ok and Game.flags.get("did:ward_fire", false)
		print("RUINTEST ", "PASS" if ok else "FAIL")
		get_tree().quit(0 if ok else 1)
		return
	if _args.has("dungeonstorytest") and not _link_test_started:
		## The optional catacombs below the chapel: locked without the Count's keys, then journal, reward items and xp.
		_link_test_started = true
		Engine.time_scale = 8.0
		var ok := loc.entities.has("dungeon_crypt_door")
		var door: Dictionary = loc.entities["dungeon_crypt_door"].data.interact
		ok = ok and str(door.go_cond) == "has:vault_key"
		print("STORYTEST door gated by the keys: ", ok)
		loc._primary("dungeon_crypt_door")          # no keys yet: must stay put
		await get_tree().create_timer(0.8).timeout
		ok = ok and Game.current == "chapel_crypt"
		print("STORYTEST locked without keys: ", Game.current == "chapel_crypt")
		Game.give("vault_key")
		loc._primary("dungeon_crypt_door")          # with the keys: goes down by itself
		var wt := 0.0
		while Game.current != "dungeon_crypt" and wt < 20.0:
			await get_tree().create_timer(0.25).timeout
			wt += 0.25
		await get_tree().create_timer(2.5).timeout
		ok = ok and Game.current == "dungeon_crypt"
		print("STORYTEST inside: ", Game.current)
		print("STORYTEST journal entry on entering: ", Game.journal.has("a1_j_cat"))
		ok = ok and Game.journal.has("a1_j_cat")
		for eid in ["cat_gold", "cat_cross", "cat_tomb", "cat_coffin", "cat_candles", "cat_cup", "cat_iron_door"]:
			var there: bool = loc.entities.has(eid)
			print("STORYTEST entity ", eid, ": ", there)
			ok = ok and there
		var xp_before := int(Game.member_state[Game.protagonist].get("xp", 0))
		loc._primary("cat_cross")
		print("STORYTEST silver taken: ", Game.has_item("silver"))
		ok = ok and Game.has_item("silver")
		loc._primary("cat_gold")
		await get_tree().create_timer(0.3).timeout
		print("STORYTEST gold journal: ", Game.journal.has("a1_j_gold"), " xp ", xp_before, " -> ", int(Game.member_state[Game.protagonist].get("xp", 0)))
		ok = ok and Game.journal.has("a1_j_gold")
		loc._use("cat_iron_door")                  # nothing selected: refuses
		ok = ok and not Game.journal.has("a1_j_cliff")
		Game.give("hammer")
		Game.selected_item = "hammer"
		loc._use("cat_iron_door")
		await get_tree().create_timer(0.3).timeout
		print("STORYTEST iron door opened with the hammer: ", Game.journal.has("a1_j_cliff"))
		ok = ok and Game.journal.has("a1_j_cliff")
		var xp_mid := int(Game.member_state[Game.protagonist].get("xp", 0))
		loc._primary("cat_gold")   # second time is just a description: must not repeat the reward
		await get_tree().create_timer(0.3).timeout
		ok = ok and int(Game.member_state[Game.protagonist].get("xp", 0)) == xp_mid
		print("STORYTEST no second reward: ", int(Game.member_state[Game.protagonist].get("xp", 0)) == xp_mid)
		print("STORYTEST ", "PASS" if ok else "FAIL")
		get_tree().quit(0 if ok else 1)
		return
	if _args.has("dungeonlinktest") and not _link_test_started:
		_link_test_started = true
		## chapel_crypt -> the dungeon through its injected door, walk away, walk back onto the entrance tile -> chapel_crypt again.
		Engine.time_scale = 8.0
		var ok := loc.entities.has("dungeon_crypt_door")
		print("LINKTEST door in chapel_crypt: ", ok)
		await _goto("dungeon_crypt", "chapel_crypt")
		await get_tree().create_timer(0.5).timeout
		ok = ok and Game.current == "dungeon_crypt"
		print("LINKTEST inside: ", Game.current, " at ", loc.player.position)
		var def := Dungeon.load_def("dungeon_crypt")
		var e := Vector3(float(def.entrance.pos[0]), 0, float(def.entrance.pos[2]))
		var far := Vector3(float(def.rooms[1].center[0]), 0, float(def.rooms[1].center[1]))
		loc.go_to(far)
		var t := 0.0
		while loc.player.position.distance_to(far) > 1.2 and t < 90.0:
			await get_tree().create_timer(0.25).timeout
			t += 0.25
		loc.go_to(e)
		t = 0.0
		while Game.current == "dungeon_crypt" and t < 90.0:
			await get_tree().create_timer(0.25).timeout
			t += 0.25
		await get_tree().create_timer(1.0).timeout
		print("LINKTEST back: ", Game.current, " player at ", loc.player.position)
		ok = ok and Game.current == "chapel_crypt"
		print("LINKTEST ", "PASS" if ok else "FAIL")
		get_tree().quit(0 if ok else 1)
		return
	if _args.has("bodytest"):
		## Prints the click collider of every NPC (size/centre) and whether a ray through the NPC's screen position picks it.
		await get_tree().create_timer(0.5).timeout
		for eid in loc.entities.keys():
			var en: Dictionary = loc.entities[eid]
			if not str(en.data.get("asset", "")).begins_with("human"):
				continue
			var nd: Node3D = en.node
			var bodies := nd.get_children().filter(func(c: Node) -> bool: return c is StaticBody3D)
			var info := "no body"
			var pick := ""
			if not bodies.is_empty():
				var sh: CollisionShape3D = bodies[0].get_child(0)
				var gc: Vector3 = (bodies[0] as Node3D).to_global(sh.position)
				info = "size %s centre %s (node at %s, scale %s)" % [(sh.shape as BoxShape3D).size, gc, nd.global_position, nd.scale]
				pick = loc._pick(loc.cam.unproject_position(gc))
			print("BODYTEST ", eid, " ", en.data.get("variant", ""), ": ", info, " pick=", pick)
		get_tree().quit()
		return
	if _args.has("regionview"):
		## Whole-region overview screenshot: --regionview=<x,y,z camera position>
		var cp := str(_args.regionview).split(",")
		print("REGIONVIEW members ", loc.members, " strips ", loc._land_rects.slice(loc.members.size()), " player ", loc.player.position)
		loc.debug_free_cam = true
		loc.cam.fov = float(_args.get("fov", 55))
		loc.cam.position = Vector3(float(cp[0]), float(cp[1]), float(cp[2]))
		loc.cam.look_at(Vector3(float(cp[0]) * 0.3, 0, float(cp[2]) * 0.2 - 8.0) if not _args.has("look") else Vector3(float(str(_args.look).split(",")[0]), float(str(_args.look).split(",")[1]), float(str(_args.look).split(",")[2])))
		await get_tree().create_timer(1.2).timeout
		get_viewport().get_texture().get_image().save_png(str(_args.get("vshot", "/tmp/regionview.png")))
		get_tree().quit()
		return
	if _args.has("regionpie"):
		## Verb-ring choice in the current scene: take the first takeable entity through the pie signal and report.
		Engine.time_scale = 6.0
		hud.modal = false
		print("REGIONPIE connected=", Game.pie_chosen.get_connections().size(), " region=", loc.region)
		var target := str(_args.get("eid", ""))
		for eid in loc.entities.keys():
			if target != "":
				break
			if loc.entities[eid].data.get("interact", {}).has("take"):
				target = str(eid)
				break
		var before := Game.inventory.size()
		Game.pie_chosen.emit(target, "take")
		var t := 0.0
		while Game.inventory.size() == before and t < 40.0:
			await get_tree().create_timer(0.25).timeout
			t += 0.25
		print("REGIONPIE take ", target, ": ", "OK" if Game.inventory.size() > before else "FAILED", " after ", t, " s")
		get_tree().quit()
		return
	if _args.has("maptest"):
		## Opens the travel map in the current scene and travels to the first exit (works in classic and region mode).
		Engine.time_scale = 4.0
		hud.modal = false
		if _args.has("realkeys"):
			# the real input path: key T, then Esc, with autosave on like normal play
			Game.autosave = true
			if _args.has("as"):
				Game.protagonist = str(_args.as)
				Game.apply_act_start("a2_whitby_lodging")
			hud._title.visible = false
			var ev := InputEventKey.new()
			ev.keycode = KEY_T
			ev.pressed = true
			Input.parse_input_event(ev)
			await get_tree().create_timer(0.5).timeout
			print("MAPTEST key T -> visible=", hud._travel != null and hud._travel.visible, " modal=", hud.modal, " protagonist=", Game.protagonist, " card=", hud._card.visible, " title=", hud._title.visible)
			get_tree().quit()
			return
		print("MAPTEST can_map=", loc._can_map(), " has_map=", TravelMap.has_map(Game.current), " cur=", Game.current, " region=", loc.region)
		hud.open_map()
		await get_tree().create_timer(0.6).timeout
		print("MAPTEST open: modal=", hud.modal, " visible=", hud._travel != null and hud._travel.visible)
		if _args.has("shot"):
			get_viewport().get_texture().get_image().save_png(str(_args.shot))
		var ex := TravelMap.exits_of(Game.current)
		if not ex.is_empty() and hud._travel != null:
			var to: String = str(_args.get("to", ex.keys()[0]))
			hud._travel.travel.emit(to)
			await get_tree().create_timer(2.5).timeout
			print("MAPTEST travelled to ", to, " -> current=", Game.current, " modal=", hud.modal, " busy=", _busy)
		get_tree().quit()
		return
	if _args.has("reachtest"):
		## For every location: walk the player to every interactable entity the way a click would (stand-off from reach_info).
		Engine.time_scale = 8.0
		var only := str(_args.get("only", ""))
		var ids: Array = Game.resolved.locations.keys()
		ids.sort()
		var fails := 0
		var total := 0
		for lid in ids:
			if (only != "" and not str(lid).begins_with(only)) or Dungeon.exists(str(lid)):
				continue
			loc.queue_free()
			await get_tree().process_frame
			loc = Location.new()
			add_child(loc)
			loc.build(str(lid), "")
			await get_tree().process_frame
			var start: Vector3 = loc.player.position
			for eid in loc.entities.keys():
				var en: Dictionary = loc.entities[eid]
				var it: Dictionary = en.data.get("interact", {})
				if not (it.has("take") or it.has("talk") or it.has("go") or it.has("fight") or it.has("set")):
					continue
				loc.player.position = start
				loc.player.stop()
				loc.dry_run = true
				loc._approach(eid, "primary")
				var t := 0.0
				while not loc.pending.is_empty() and t < 60.0:
					await get_tree().create_timer(0.25).timeout
					t += 0.25
				total += 1
				if not loc.pending.is_empty() or t >= 59.0:
					fails += 1
					print("REACH FAIL ", lid, " ", eid, " (", it.keys(), ") player ", loc.player.position)
				elif t > 20.0:
					print("REACH SLOW ", lid, " ", eid, " ", t)
		print("REACHTEST ", "PASS" if fails == 0 else "FAIL", " ", total, " entities, ", fails, " unreachable")
		get_tree().quit(0 if fails == 0 else 1)
		return
	if _args.has("dungeontest"):
		## Walk from the entrance to the exit and to the middle of every room of a generated dungeon.
		Engine.time_scale = 8.0
		var def := Dungeon.load_def(Game.current)
		loc._dungeon_def = {}          # walking onto the entrance/exit tiles must not leave the level during the test
		var goals: Array = []
		if def.get("exit") is Dictionary:
			goals.append(["exit", Vector2(float(def.exit.pos[0]), float(def.exit.pos[2]))])
		if def.rooms.is_empty():
			var rr: Array = Dungeon.floor_rects(def)
			for i in range(0, rr.size(), 2):
				goals.append(["area %d" % i, (rr[i] as Rect2).get_center()])
		for r in def.rooms:
			if int(r.floor) == int(def.floors[0].z):
				goals.append(["room %d (%s)" % [int(r.id), str(r.shape)], Vector2(float(r.center[0]), float(r.center[1]))])
		var ok := true
		var cells: Dictionary = Dungeon.cells_of(def)
		var ts: float = float(def.tile_size)
		for g in goals:
			# a room's middle may hold a tomb or a chest: aim for the nearest tile that is clear of every blocker
			var best: Vector2 = g[1]
			var bd := 1e18
			for k in cells:
				var c := Vector2(k.x * ts, k.y * ts)
				var clear := true
				for b in loc._blockers:
					if (b.pos as Vector2).distance_to(c) < float(b.r) + 1.0:
						clear = false
						break
				if clear and c.distance_to(g[1]) < bd:
					bd = c.distance_to(g[1])
					best = c
			g[1] = best
			var want := loc._clamp_region(Vector3((g[1] as Vector2).x, 0, (g[1] as Vector2).y))
			loc.go_to(Vector3((g[1] as Vector2).x, 0, (g[1] as Vector2).y))
			var t := 0.0
			while Vector2(loc.player.position.x - want.x, loc.player.position.z - want.z).length() > 0.9 and t < 90.0:
				await get_tree().create_timer(0.25).timeout
				t += 0.25
			var reached := Vector2(loc.player.position.x - want.x, loc.player.position.z - want.z).length() <= 0.9
			print("DUNGEONTEST walk to ", g[0], ": ", "OK" if reached else "FAILED", " at ", loc.player.position)
			ok = ok and reached
		for eid in loc.entities:
			var en: Dictionary = loc.entities[eid]
			var ep: Vector3 = (en.node as Node3D).global_position
			loc.go_to(ep)
			var t2 := 0.0
			var reach := float(en.data.get("radius", 0.5)) + 1.4
			while loc.player.position.distance_to(ep) > reach and t2 < 90.0:
				await get_tree().create_timer(0.25).timeout
				t2 += 0.25
			var near: bool = loc.player.position.distance_to(ep) <= reach
			print("DUNGEONTEST approach ", eid, ": ", "OK" if near else "FAILED", "" if near else "  player %s entity %s moving=%s" % [loc.player.position, ep, loc.player.moving])
			ok = ok and near
		print("DUNGEONTEST ", "PASS" if ok else "FAIL", " (", goals.size(), " goals)")
		get_tree().quit(0 if ok else 1)
		return
	if _args.has("regiontest"):
		Engine.time_scale = 8.0
		var ok := true
		var tour: Array = []
		var adj := {}
		for lk in Regions.DEF[loc.region].links:
			adj[lk[0]] = adj.get(lk[0], []) + [lk[1]]
			adj[lk[1]] = adj.get(lk[1], []) + [lk[0]]
		var dfs := func(self_fn: Callable, node: String, parent: String) -> void:
			for nb in adj.get(node, []):
				if nb != parent:
					tour.append(nb)
					self_fn.call(self_fn, nb, node)
					tour.append(node)
		dfs.call(dfs, Game.current, "")
		for target in tour:
			var dest: Vector3 = loc.region_spawn(target, "")
			loc.go_to(dest)
			var t := 0.0
			while Game.current != target and t < 60.0:
				await get_tree().create_timer(0.25).timeout
				t += 0.25
			print("REGIONTEST walk to ", target, ": ", "OK" if Game.current == target else "FAILED", " at ", loc.player.position)
			if Game.current != target:
				print("   moving=", loc.player.moving, " dest=", loc.player.dest, " want=", dest, " member=", loc._member)
				for b in loc.player.blockers:
					if (b.pos as Vector2).distance_to(Vector2(loc.player.position.x, loc.player.position.z)) < 3.0:
						print("   near blocker ", b)
			ok = ok and Game.current == target
		print("REGIONTEST ", "PASS" if ok else "FAIL")
		get_tree().quit(0 if ok else 1)
		return
	if _args.has("shot") and not _args.has("fight"):
		await get_tree().create_timer(float(_args.get("wait", "1.2"))).timeout
		for _i in int(_args.get("frames", "4")):
			await get_tree().process_frame
		if _args.has("invfilter"):
			Game.item_filter = str(_args.invfilter)
		if _args.has("pie"):
			loc._open_pie(str(_args.pie), Vector2(float(str(_args.get("px", "640"))), 330))
			await get_tree().create_timer(0.4).timeout
			if _args.has("piesub"):                  # the "use item on it" ring (page 1, or page 2 with --piepage=2)
				hud._pie.close()
				hud.modal = false
				loc._on_pie_chosen(str(_args.pie), "item")
				await get_tree().create_timer(0.3).timeout
				if str(_args.get("piepage", "1")) == "2":
					hud._pie._page += 1
					hud._pie._apply_page()
				await get_tree().create_timer(0.3).timeout
		if _args.has("invclick"):
			## really press the chip with that group name and count what is left on the bar
			var buttons := hud._inv.get_children().filter(func(c: Node) -> bool: return c is Button)
			var before := buttons.size()
			for bt in buttons:
				if (bt as Button).text == str(_args.invclick):
					(bt as Button).pressed.emit()
			await get_tree().process_frame
			await get_tree().process_frame
			print("INVCLICK ", _args.invclick, ": buttons ", before, " -> ", hud._inv.get_children().filter(func(c: Node) -> bool: return c is Button).size(), " filter=", Game.item_filter)
		if _args.has("invfilter"):
			Game.item_filter = str(_args.invfilter)
			hud._rebuild_inventory()
			await get_tree().process_frame
			await get_tree().process_frame
		if _args.has("invscroll"):
			hud._inv_scroll.scroll_horizontal = int(_args.invscroll)
			await get_tree().process_frame
		if _args.has("hovertext"):
			hud.set_hover(str(_args.hovertext).replace("_", " "))
			await get_tree().process_frame
		var img := get_viewport().get_texture().get_image()
		img.save_png(str(_args.shot))
		print("saved ", _args.shot)
		get_tree().quit()


func _start_arc(id: String) -> void:
	if _busy or Game.in_arc != "":
		return
	var a := Game.arc_def(id)
	if Game.current == "":
		Game.new_game(randi() % 1000000000)      # started from the title screen: a fresh world to host the arc
		Game.current = "__arc_host__"
	Game.start_arc(id)
	Game.card_requested.emit("%s\n\n%s" % [str(a.title), str(a.get("blurb", ""))], str(a.start.location))


func _arc_finished(id: String, return_to: String) -> void:
	var a := Game.arc_def(id)
	var txt := "%s - complete.\n\n%s" % [str(a.title), str(a.get("rewards_text", ""))]
	Game.card_requested.emit(txt, "__title__" if return_to == "__arc_host__" else return_to)
	if return_to == "__arc_host__":
		Game.current = ""


## The player walked (or was carried) into another member of a merged region.
func _member_entered(mid: String) -> void:
	var md: Dictionary = Game.loc_data(mid)
	Game.current = mid
	Audio.set_mood(mid, md)
	Game.apply_act_start(mid)
	for l in Game.world.locations:
		if l.id == mid:
			hud.set_location_title(str(l.name))
			if not Game.visited.has(mid):
				hud.say(str(l.desc))
	Game.visited[mid] = true
	Game.save_game()
	_on_enter(mid, md)


func _on_enter(loc_id: String, ldata: Dictionary = {}) -> void:
	var entries: Array = (ldata if not ldata.is_empty() else loc.data).get("on_enter", [])
	for i in entries.size():
		var e: Dictionary = entries[i]
		var key := "entered:%s:%d" % [loc_id, i]
		if not Game.check(str(e.get("if", ""))):
			continue
		if e.get("once", true) and Game.flags.get(key, false):
			continue
		Game.set_flag(key)
		Game.run(e.do)
		break


func _fight(enc_id: String, _source: String) -> void:
	if _busy:
		return
	_busy = true
	hud.modal = true
	await hud.fade_to(1.0, 0.3)
	loc.visible = false
	hud.visible = false
	Audio.music("mus_combat", 1.0)
	var ui := CombatUI.new()
	add_child(ui)
	ui.start(enc_id, Game.seed_value * 31 + enc_id.hash())
	await hud.fade_to(0.0, 0.3)
	var res: Array = await ui.finished
	hud.visible = true
	loc.visible = true
	Audio.sfx("victory" if res[0] == "win" else ("defeat" if res[0] == "lose" else "step"))
	Audio.set_mood(loc.id, loc.data)
	_busy = false
	hud.modal = false
	Game.party_changed.emit()
	var hooks: Dictionary = Game.world.get("encounter_hooks", {}).get(enc_id, {})
	var combat_obj: Combat = res[1]
	var gained := combat_obj.xp_reward() if res[0] != "lose" else 0
	if gained > 0:
		Game.grant_xp(Game.party, gained)
	var loot_txt := ""
	if res[0] == "win":
		var loot: Dictionary = Game.systems.encounters[enc_id].get("loot", {})
		for it in loot:
			Game.give(str(it), int(loot[it]))
			loot_txt += " +%d %s" % [int(loot[it]), Game.item_name(str(it))]
	var reward_msg := ""
	if gained > 0 or loot_txt != "":
		reward_msg = "\n+%d XP.%s" % [gained, loot_txt]
	match res[0]:
		"win", "fled":
			if res[0] == "win":
				Game.set_flag("won:" + enc_id)
				loc.clear_fight(enc_id)
			hud.say((str(Game.systems.encounters[enc_id].win) if res[0] == "win" else "We got away, shaken.") + reward_msg)
			var key := "on_win" if res[0] == "win" else "on_flee"
			if hooks.has(key):
				Game.run(hooks[key])
		"lose":
			hud.say("Darkness... and then a grey dawn. I wake battered, but alive.")
			if hooks.has("on_lose"):
				Game.run(hooks["on_lose"])


func _process(_d: float) -> void:
	if loc != null and is_instance_valid(loc):
		loc.modal = hud.modal or _busy
