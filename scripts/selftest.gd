class_name SelfTest
extends RefCounted
## Plays the whole slice through the real game objects (headless-friendly):
##   godot --path . -- --selftest

var m: Node
var fails := 0


func ok(cond: bool, what: String) -> void:
	print(("  ok   " if cond else "  FAIL ") + what)
	if not cond:
		fails += 1


func settle() -> void:
	for _i in 4:
		await m.get_tree().process_frame
	while m._busy:
		await m.get_tree().process_frame


func act(eid: String, verb := "primary") -> void:
	var l: Location = m.loc
	if not l.entities.has(eid):
		ok(false, "entity %s missing in %s" % [eid, l.id])
		return
	var e: Dictionary = l.entities[eid]
	l.player.position = e.node.global_position + Vector3(0, 0, float(e.data.get("radius", 0.5)) + 0.8)
	l._approach(eid, verb)
	await settle()


func choose(fragment: String) -> void:
	for b in m.hud._dlg_choices.get_children():
		if (b as Button).text.contains(fragment):
			(b as Button).pressed.emit()
			await settle()
			return
	ok(false, "choice '%s' not found" % fragment)


func find_ui() -> CombatUI:
	for c in m.get_children():
		if c is CombatUI:
			return c
	return null


## Plays a fight through the real CombatUI methods (menu choice + target pick).
func fight_via_ui(eid: String) -> void:
	var l: Location = m.loc
	var e: Dictionary = l.entities[eid]
	l.player.position = e.node.global_position + Vector3(0, 0, 1.6)
	l._approach(eid, "primary")
	var ui: CombatUI = null
	var guard := 0
	while ui == null and guard < 100:
		await m.get_tree().create_timer(0.05).timeout
		ui = find_ui()
		guard += 1
	ok(ui != null, "combat screen opened")
	if ui == null:
		return
	var res := [""]
	ui.finished.connect(func(r: String, _c: Combat) -> void: res[0] = r)
	var turns := 0
	while is_instance_valid(ui) and turns < 1500:
		turns += 1
		await m.get_tree().create_timer(0.05).timeout
		if not is_instance_valid(ui):
			break
		if ui.combat == null or ui._actor.is_empty() or ui.combat.result != "":
			if ui.combat != null and ui.combat.result != "" and ui._menu.get_child_count() > 0:
				(ui._menu.get_child(0) as Button).pressed.emit()   # Continue
			continue
		if not ui._pending.is_empty() or ui._menu.get_child_count() == 0:
			continue
		var acts := ui.combat.actions_for(ui._actor)
		var foes := ui.combat.alive(ui.combat.enemies)
		var actor_id: String = ui._actor.id
		var before: String = ui._actor.name
		ui._actor = ui._actor
		ui._choose(acts[0])
		if not ui._pending.is_empty() and foes.size() > 0:
			ui._target_picked(foes[0])
	await settle()
	ok(not is_instance_valid(ui) and res[0] != "", "combat finished via UI: %s" % res[0])
	if res[0] == "win":
		ok(not m.loc.entities.has(eid), "defeated wolf removed from the scene")


func find_prop_loc(pid: String) -> String:
	for lid in Game.resolved.locations:
		for p in Game.resolved.locations[lid].props:
			if p.id == pid:
				return lid
	return ""


func door_to(from_loc: String, target: String) -> String:
	for p in Game.resolved.locations[from_loc].props:
		if p.get("interact", {}).get("go", "") == target:
			return p.id
	return ""


func path(from_loc: String, to_loc: String) -> Array:
	var prev := {from_loc: ""}
	var q := [from_loc]
	while q.size() > 0:
		var cur: String = q.pop_front()
		if cur == to_loc:
			break
		for p in Game.resolved.locations[cur].props:
			var g: String = p.get("interact", {}).get("go", "")
			if g != "" and not prev.has(g):
				prev[g] = cur
				q.append(g)
	var out: Array = []
	var c := to_loc
	while c != from_loc and prev.has(c):
		out.push_front(c)
		c = prev[c]
	return out


func _in_region_with(target: String) -> bool:
	return m.loc != null and m.loc.region != "" and m.loc.members.has(target)


func travel(target: String) -> void:
	for step in path(Game.current, target):
		if _in_region_with(step):
			m._goto(step, Game.current, true)       # inside a merged region the way over is simply a walk
			await settle_all()
			ok(Game.current == step, "-> %s (region)" % step)
			continue
		var pid := door_to(Game.current, step)
		await act(pid)
		if Game.current != step:
			await act(pid)       # first click on the courtyard gate only knocks
		ok(Game.current == step, "-> %s" % step)


func gather(item: String) -> void:
	var holder: String = Game.resolved.placed[item]
	await travel(find_prop_loc(holder))
	await act(holder)
	ok(Game.has_item(item), "found %s in %s" % [item, holder])


func run(main: Node, seed_value: int = 1) -> int:
	m = main
	Game.new_game(seed_value)
	print("seed %d: gate=%s key@%s" % [seed_value, Game.resolved.gates.door_old.needs, Game.resolved.placed.key])
	main._goto("golden_krone", "", true)
	await settle()
	ok(Game.current == "golden_krone", "start in inn")
	await act("door_out")
	ok(Game.current == "golden_krone", "door locked before crucifix")
	await act("hostess")
	await choose("I must")
	await choose("Continue")
	ok(Game.has_item("crucifix"), "got crucifix from hostess")
	await travel("borgo_pass")
	await fight_via_ui("wolf1")
	await travel("great_hall")
	await act("count")
	ok(m.hud._dlg.visible, "count dialogue opens")
	await choose("I am pleased")
	await choose("Continue")
	await choose("Leave")
	var need: String = Game.resolved.gates.door_old.needs
	await gather(need)
	await travel("old_wing")
	await act("garlic_o")
	ok(Game.has_item("garlic"), "old wing reachable, took garlic")
	await gather("key")
	await travel("harker_room")
	Game.selected_item = "key"
	await act("chest_r", "use")
	ok(Game.has_item("hammer"), "chest opened with key -> hammer")
	await travel("chapel_crypt")
	await act("coffin2")
	ok(Game.has_item("vault_key"), "took vault key")
	await act("goal")
	ok(m.hud._dlg.visible, "vault stairs dialogue opens")
	await choose("Descend")
	await settle_all()
	ok(Game.current == "a2_whitby_lodging", "Act I ends with a card and the move to Whitby (Act II)")
	ok(Game.protagonist == "mina" or Game.roster.has("mina"), "Mina introduced at Whitby")
	# crafting
	Game.give("wood")
	Game.give("cloth")
	Game.give("oil")
	ok(Game.can_craft("torch") == "", "torch craftable from wood+cloth+oil")
	ok(Game.craft("torch") and Game.has_item("torch") and not Game.has_item("oil"), "torch crafted, ingredients consumed")
	ok(Game.can_craft("holy_water") != "", "holy water locked until rites are known")
	Game.flags["rites"] = true
	Game.give("water")
	Game.give("host")
	ok(Game.craft("holy_water") and Game.has_item("holy_water"), "holy water crafted after unlocking rites")
	print("SELFTEST seed %d: %s (%d failures)" % [seed_value, "PASS" if fails == 0 else "FAIL", fails])
	return fails


# ------------------------------------------------------------------ plan replay
## Executes a plan written by pipeline/validate_story.py in the real engine.
func settle_all() -> void:
	var idle := 0
	var guard := 0
	while idle < 6 and guard < 4000:
		guard += 1
		await m.get_tree().process_frame
		if m._busy and find_ui() == null:
			idle = 0
			continue
		if m.hud._card.visible:
			var ev := InputEventMouseButton.new()
			ev.pressed = true
			ev.button_index = MOUSE_BUTTON_LEFT
			m.hud._card.gui_input.emit(ev)
			idle = 0
			continue
		var ui := find_ui()
		if ui != null:
			await auto_fight(ui)
			idle = 0
			continue
		if m.hud._dlg.visible:
			await close_dialogue()
			idle = 0
			continue
		idle += 1


func auto_fight(ui: CombatUI) -> void:
	var c: Combat = ui.combat
	var guard := 0
	while c.result == "" and guard < 500:
		guard += 1
		var st := c.advance()
		if st.state == "over":
			break
		c.auto_act(st.actor)
	if c.result != "win":
		forced.append(str(c.enc.name))
		c.result = "win"
	ui._apply_results()
	var res := c.result
	ui.finished.emit(res, c)
	ui.queue_free()
	await m.get_tree().process_frame


func close_dialogue() -> void:
	var guard := 0
	while m.hud._dlg.visible and guard < 40:
		guard += 1
		var btns: Array = m.hud._dlg_choices.get_children()
		var pick: Button = null
		for b in btns:
			if (b as Button).text.contains("Continue"):
				pick = b
		if pick == null:
			for b in btns:
				var tx: String = (b as Button).text
				if tx.contains("Leave") or tx.contains("Goodbye") or tx.contains("Farewell") or tx.contains("[Not yet]"):
					pick = b
		if pick == null and btns.size() > 0:
			pick = btns[btns.size() - 1]
		if pick == null:
			break
		pick.pressed.emit()
		await m.get_tree().process_frame


func play_dialogue(path: Array) -> void:
	var idx := 0
	var guard := 0
	while m.hud._dlg.visible and guard < 60:
		guard += 1
		var btns: Array = m.hud._dlg_choices.get_children()
		var pick: Button = null
		if idx < path.size():
			for b in btns:
				if (b as Button).text.strip_edges() == str(path[idx]).strip_edges() or (b as Button).text.contains(str(path[idx])):
					pick = b
					break
			if pick != null:
				idx += 1
		if pick == null:
			for b in btns:
				if (b as Button).text.contains("Continue"):
					pick = b
		if pick == null:
			if idx >= path.size():
				break
			ok(false, "dialogue choice '%s' not available" % str(path[idx]))
			print("    buttons: ", btns.map(func(b: Node) -> String: return (b as Button).text.strip_edges().left(50)), " items: ", Game.inventory.size(), " has_ticket=", Game.has_item("a4_pawn_ticket"), " prot=", Game.protagonist)
			return
		pick.pressed.emit()
		await m.get_tree().process_frame
	await close_dialogue()


var forced: Array = []


func _explain_choice(did: String, path: Array) -> void:
	for nid in Game.world.dialogue[did].nodes:
		for c in Game.world.dialogue[did].nodes[nid].get("choices", []):
			for t in path:
				if str(c.text) == str(t) and c.has("cond"):
					for part in str(c.cond).split("&"):
						print("    cond part '%s' -> %s" % [part, Game.check(part)])


func replay(main: Node, plan_path: String, seed_value: int, defaults: bool) -> int:
	m = main
	var plan: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(plan_path))
	Game.new_game(seed_value, defaults)
	var st: Dictionary = plan.start
	var arc_id := str(plan.get("arc", ""))
	if arc_id != "":
		Game.current = "__arc_host__"
		Game.start_arc(arc_id)
	else:
		Game.protagonist = str(st.protagonist)
		Game.party = []
		Game.member_state.clear()
		for id in st.party:
			Game.recruit(str(id))
		for it in st.get("items", {}):
			Game.give(str(it), int(st.items[it]))
		for f in st.get("flags", []):
			Game.set_flag(str(f))
	main._goto(str(st.location), "", true)
	await settle_all()
	print("replay act %s seed %d (%s): %d steps" % [plan.act, seed_value, "defaults" if defaults else "resolved", plan.plan.size()])
	var granted: Array = []                          # journal entries written along the solution path (for pipeline/gen_objectives.py)
	Game.journal_added.connect(func(jid: String) -> void: granted.append(jid))
	var ended := [false]
	Game.ending.connect(func(_t: String) -> void: ended[0] = true)
	var n := 0
	for step in plan.plan:
		n += 1
		if step.kind == "enter":
			continue
		if OS.get_cmdline_user_args().has("--verbose"):
			print("  step %d %s %s %s %s" % [n, step.kind, step.loc, step.get("eid", ""), str(step.get("path", ""))])
		if Game.current != str(step.loc):
			var before := Game.current
			await travel(str(step.loc))
			if Game.current != str(step.loc):
				ok(false, "step %d: cannot reach %s from %s" % [n, step.loc, before])
				break
		match step.kind:
			"use":
				Game.selected_item = str(step.item)
				await act(str(step.eid), "use")
			"talk":
				var l: Location = m.loc
				if not l.entities.has(step.eid):
					ok(false, "step %d: %s missing in %s" % [n, step.eid, l.id])
					break
				var e: Dictionary = l.entities[step.eid]
				l.player.position = e.node.global_position + Vector3(0, 0, float(e.data.get("radius", 0.5)) + 0.8)
				l._approach(str(step.eid), "primary")
				await m.get_tree().process_frame
				if not m.hud._dlg.visible:
					ok(false, "step %d: dialogue %s did not open" % [n, step.dialogue])
					break
				var fails_before := fails
				await play_dialogue(step.path)
				if fails > fails_before:
					_explain_choice(str(step.dialogue), step.path)
				await settle_all()
			_:
				var l2: Location = m.loc
				if step.kind == "door" and step.has("to") and _in_region_with(str(step.to)):
					m._goto(str(step.to), str(step.loc), true)
					await settle_all()
					continue
				if not l2.entities.has(step.eid):
					ok(false, "step %d (%s): %s missing in %s" % [n, step.kind, step.eid, l2.id])
					break
				var e2: Dictionary = l2.entities[step.eid]
				l2.player.position = e2.node.global_position + Vector3(0, 0, float(e2.data.get("radius", 0.5)) + 0.8)
				l2._approach(str(step.eid), "primary")
				await settle_all()
				if step.kind == "door" and Game.current != str(step.to) and str(step.to) != str(plan.exit_to):
					# gates such as the courtyard gate need a second click
					l2 = m.loc
					if l2.entities.has(step.eid):
						l2._approach(str(step.eid), "primary")
						await settle_all()
					ok(Game.current == str(step.to), "step %d: door %s -> %s (now %s)" % [n, step.eid, step.to, Game.current])
	var exit_to := str(plan.exit_to)
	var reached: bool = ended[0] if exit_to == "END" else (Game.current == exit_to or Game.visited.has(exit_to))
	if exit_to == "ARC_END":
		await settle_all()
		reached = Game.arcs_done.has(arc_id)
		ok(Game.in_arc == "", "arc state popped")
		var adef := Game.arc_def(arc_id)
		for r in adef.get("rewards", []):
			if r.has("give"):
				ok(Game.has_item(str(r.give)), "reward item %s granted to the main game" % r.give)
			if r.has("stat"):
				ok(Game.member_state.has(str(r.stat.member)) and not Game.member_state[str(r.stat.member)].bonus.is_empty(), "reward stat for %s applied" % r.stat.member)
			if r.has("set"):
				ok(Game.flags.get(str(r.set), false), "reward flag %s set" % r.set)
	ok(reached, "act exit reached (%s)" % exit_to)
	print("REPLAYJOURNAL ", (arc_id if arc_id != "" else str(int(plan.act))), " ", ",".join(granted))
	Game.objective_list()                            # loads data/objectives.json
	var okey := str(int(plan.act)) if typeof(plan.act) == TYPE_FLOAT or typeof(plan.act) == TYPE_INT else str(plan.act)
	if arc_id == "" and Game.objectives.has(okey):
		var left: Array = []
		for o in Game.objectives[okey]:
			if bool(o.get("required", true)) and not Game.check(str(o.done)) and Game.check(str(o.get("if", ""))):
				left.append(str(o.id))
		ok(left.is_empty(), "all required objectives of %s done (left: %s)" % [okey, str(left)])
		print("  objectives checked for ", okey, ": ", Game.objectives[okey].size(), " listed, missing ", left)
	if not forced.is_empty():
		print("  note: fights forced to victory in replay: ", forced)
	print("REPLAY act %s: %s (%d failures)" % [plan.act, "PASS" if fails == 0 else "FAIL", fails])
	return fails


## Chronicle/arc bookkeeping without scenes: unlock rules, state isolation, rewards, persistence of the after-credits flag.
func arc_flow(main: Node) -> int:
	m = main
	Game.new_game(5, true)
	Game.meta = {}
	ok(Game.arc_status("mina_records") == "locked", "Mina's arc locked before meeting her")
	Game.meet("mina")
	ok(Game.arc_status("mina_records") == "available", "Mina's arc available once met")
	ok(Game.arc_status("harker_road") == "locked", "Harker's arc waits for Act I's end")
	Game.add_journal("a1_j7")
	ok(Game.arc_status("harker_road") == "available", "Harker's arc available after Act I journal")
	ok(Game.arc_status("lucy_summer") == "locked", "Lucy's arc needs the peaceful ending flags")
	Game.set_flag("a4_staked")
	Game.set_flag("a4_arthur_peace_done")
	ok(Game.arc_status("lucy_summer") == "available", "Lucy's arc unlocks with the conditions")
	ok(Game.arc_status("renfield_mercy") == "locked", "Renfield's arc needs the mercy flag")
	Game.set_flag("a5_renfield_revived")
	ok(Game.arc_status("renfield_mercy") == "available", "Renfield's arc unlocks")
	ok(Game.arc_status("dracula_voivode") == "locked" and Game.arc_status("demeter_voyage") == "locked", "after-credits arcs locked")
	Game.ending.emit("test end")
	ok(Game.meta.get("game_complete", false), "ending sets the persistent game_complete flag")
	ok(Game.arc_status("dracula_voivode") == "available" and Game.arc_status("demeter_voyage") == "available", "after-credits arcs unlock once credits rolled")
	# isolation + rewards
	Game.give("brandy", 2)
	Game.set_flag("main_only_flag")
	var before_hp: int = Game.member_state["harker"].hp
	Game.current = "somewhere"
	Game.start_arc("mina_records")
	ok(Game.in_arc == "mina_records" and not Game.flags.get("main_only_flag", false) and Game.count("brandy") == 0, "arc state is isolated from the main game")
	ok(Game.protagonist == "mina", "arc protagonist applied")
	Game.run([{"give": "silver"}])
	Game.run([{"arc_end": 1}])
	ok(Game.in_arc == "", "arc ended")
	ok(Game.flags.get("main_only_flag", false) and Game.count("brandy") >= 2 and not Game.has_item("mina_records_typed_page"), "main state restored after the arc (brandy kept, reward adds more)")
	ok(Game.arcs_done.has("mina_records") and Game.arc_status("mina_records") == "done", "arc marked done")
	ok(Game.member_state["harker"].hp == before_hp, "unrelated members untouched")
	ok(not Game.member_state["mina"].bonus.is_empty(), "Mina received her permanent stat bonus")
	# levels and equipment
	Game.new_game(7, true)
	Game.recruit("arthur")
	Game.recruit("quincey")
	var lv0 := Game.level_of("arthur")
	Game.grant_xp(["arthur"], 29)
	ok(Game.level_of("arthur") == lv0, "29 XP is not enough for level 2")
	Game.grant_xp(["arthur"], 1)
	ok(Game.level_of("arthur") == 2, "30 XP reaches level 2")
	var e1 := Game.effective("arthur")
	ok(int(e1.max_hp) == int(Game.systems.party["arthur"].hp) + 3, "level 2 grants +3 max HP")
	ok(not Game.equip("arthur", "armor", "lords_riding_coat"), "cannot equip an item you do not own")
	Game.give("lords_riding_coat")
	Game.give("sword_cane")
	ok(Game.equip("arthur", "armor", "lords_riding_coat") and int(Game.effective("arthur").armor) == 2, "armor equips and counts")
	ok(Game.equip("quincey", "armor", "lords_riding_coat") and Game.equipped_by("lords_riding_coat") == "quincey", "an item moves between members")
	ok(int(Game.effective("arthur").armor) == 0, "...and leaves the previous wearer")
	ok(Game.equip("arthur", "weapon", "sword_cane") and Game.effective("arthur").weapon == "sword_cane", "weapon slot works for allowed users")
	Game.give("kukri")
	ok(not Game.equip("arthur", "weapon", "kukri"), "kukri is Harker-only")
	Game.give("crucifix")
	ok(Game.equip("arthur", "charm", "crucifix") and int(Game.effective("arthur").faith) >= int(Game.systems.party["arthur"].faith) + 2, "charm adds faith")
	var cmb := Combat.new()
	var states := {}
	for pid in ["arthur"]:
		var s2: Dictionary = Game.member_state[pid].duplicate(true)
		s2["eff"] = Game.effective(pid)
		states[pid] = s2
	cmb.setup(Game.systems, ["arthur"], states, "borgo_wolves", Game.counts, 3)
	ok(cmb.party[0].equip_weapon == "sword_cane" and cmb.weapon_for(cmb.party[0]).key == "sword_cane", "combat uses the equipped weapon")
	Game.add_journal("a1_j1")
	var xp_before: int = Game.member_state["arthur"].xp
	Game.add_journal("a1_j2")
	ok(int(Game.member_state["arthur"].xp) == xp_before + 2, "journal entries grant 2 XP")
	print("ARCFLOW: %s (%d failures)" % ["PASS" if fails == 0 else "FAIL", fails])
	return fails


## Every location must map to existing ambience/music streams; prints the distribution.
func audio_check(main: Node) -> int:
	m = main
	Game.new_game(1, true)
	var amb := {}
	var mus := {}
	for lid in Game.resolved.locations:
		var mood: Dictionary = Audio.mood_for(lid, Game.resolved.locations[lid])
		if not Audio.index.has(mood.ambience) or Audio._stream(mood.ambience) == null:
			ok(false, "%s: ambience %s missing" % [lid, mood.ambience])
		if not Audio.index.has(mood.music) or Audio._stream(mood.music) == null:
			ok(false, "%s: music %s missing" % [lid, mood.music])
		amb[mood.ambience] = amb.get(mood.ambience, 0) + 1
		mus[mood.music] = mus.get(mood.music, 0) + 1
	print("ambience: ", amb)
	print("music: ", mus)
	for n in Audio.index:
		if Audio._stream(n) == null:
			ok(false, "stream %s does not load" % n)
	print("AUDIOCHECK: %s (%d failures)" % ["PASS" if fails == 0 else "FAIL", fails])
	return fails
