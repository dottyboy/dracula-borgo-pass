class_name HUD
extends CanvasLayer
## All 2D UI built in code: hover label, message line, inventory bar,
## dialogue box, fade, title and ending screens.

signal start_pressed
signal continue_pressed
signal arc_requested(id: String)
signal dialogue_finished

const PARCH := Color("#e9dcc0")
const GOLD := Color("#c9a24a")

var modal := false
var root: Control
var fast_fade := false
var _hover: Label
var _msg: Label
var _msg_timer := 0.0
var _inv: HBoxContainer
var _dlg: PanelContainer
var _dlg_speaker: Label
var _dlg_text: Label
var _dlg_choices: VBoxContainer
var _fade: ColorRect
var _title: Control
var _title_sub: Label
var _end: Control
var _end_text: Label
var _dialogue: Dictionary = {}
var _loc_title: Label
var _cut_flash: ColorRect
var _seed_edit: LineEdit
var _party_box: HBoxContainer
var _card: Control
var _card_text: Label
var _card_goto := ""
var _journal: PanelContainer
var _jlist: ItemList
var _jtext: RichTextLabel
var _chron: PanelContainer
var _chron_list: VBoxContainer
var _chron_info: Label
var _pp: PanelContainer
var _pp_list: VBoxContainer
var _pp_detail: VBoxContainer
var _pp_sel := ""
var _menu: PanelContainer
var _craft: PanelContainer
var _craft_list: VBoxContainer


static func make_theme() -> Theme:
	var th := Theme.new()
	var f := SystemFont.new()
	f.font_names = PackedStringArray(["Palatino Linotype", "Palatino", "Book Antiqua", "Georgia", "Cormorant Garamond", "DejaVu Serif", "Liberation Serif", "serif"])
	f.antialiasing = TextServer.FONT_ANTIALIASING_LCD
	th.default_font = f
	th.default_font_size = 18
	return th


func _ready() -> void:
	layer = 10
	var vig := ColorRect.new()
	vig.set_anchors_preset(Control.PRESET_FULL_RECT)
	vig.mouse_filter = Control.MOUSE_FILTER_IGNORE
	vig.material = ShaderMaterial.new()
	(vig.material as ShaderMaterial).shader = load("res://shaders/vignette.gdshader")
	add_child(vig)
	_cut_flash = ColorRect.new()
	_cut_flash.set_anchors_preset(Control.PRESET_FULL_RECT)
	_cut_flash.color = Color(0.02, 0.0, 0.03, 1.0)
	_cut_flash.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_cut_flash.modulate.a = 0.0
	add_child(_cut_flash)
	Game.camera_cut.connect(func() -> void:
		_cut_flash.modulate.a = 0.55
		create_tween().tween_property(_cut_flash, "modulate:a", 0.0, 0.28))
	root = Control.new()
	root.theme = make_theme()
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(root)

	_hover = _label(root, 22, GOLD)
	_hover.set_anchors_preset(Control.PRESET_CENTER_TOP)
	_hover.offset_left = -400.0
	_hover.offset_right = 400.0
	_hover.offset_top = 14.0
	_hover.offset_bottom = 44.0
	_hover.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER

	_loc_title = _label(root, 15, Color("#ffffff80"))
	_loc_title.position = Vector2(16, 10)

	_msg = _label(root, 20, PARCH)
	_msg.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_msg.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_msg.offset_left = 120
	_msg.offset_right = -120
	_msg.offset_top = -190
	_msg.offset_bottom = -78
	_msg.vertical_alignment = VERTICAL_ALIGNMENT_BOTTOM
	_msg.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER

	var bar := PanelContainer.new()
	bar.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	bar.offset_top = -64
	bar.add_theme_stylebox_override("panel", _box(Color(0.05, 0.02, 0.03, 0.85), GOLD * Color(1, 1, 1, 0.6)))
	root.add_child(bar)
	_inv = HBoxContainer.new()
	_inv.add_theme_constant_override("separation", 8)
	bar.add_child(_inv)

	_dlg = PanelContainer.new()
	_dlg.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_dlg.offset_left = 80
	_dlg.offset_right = -80
	_dlg.offset_top = -330
	_dlg.offset_bottom = -76
	_dlg.add_theme_stylebox_override("panel", _box(Color(0.06, 0.02, 0.03, 0.94), GOLD))
	_dlg.visible = false
	root.add_child(_dlg)
	var vb := VBoxContainer.new()
	vb.add_theme_constant_override("separation", 8)
	_dlg.add_child(vb)
	_dlg_speaker = _label(vb, 24, GOLD)
	_dlg_text = _label(vb, 20, PARCH)
	_dlg_text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_dlg_text.custom_minimum_size = Vector2(0, 70)
	_dlg_choices = VBoxContainer.new()
	vb.add_child(_dlg_choices)

	_fade = ColorRect.new()
	_fade.color = Color.BLACK
	_fade.set_anchors_preset(Control.PRESET_FULL_RECT)
	_fade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_fade.modulate.a = 0.0
	root.add_child(_fade)

	_title = _overlay(root, "DRACULA", "The Borgo Pass\n\n\"3 May. Bistritz. - Left Munich at 8:35 P.M., on 1st May, arriving at Vienna early next morning...\"\n\nChoose a seed - the same seed always builds the same world.")
	_end = _overlay(root, "", "")
	_end.visible = false
	_title_sub = _title.get_meta("sub")
	_end_text = _end.get_meta("sub")
	_end.gui_input.connect(func(ev: InputEvent) -> void:
		if ev is InputEventMouseButton and ev.pressed:
			_end.visible = false
			_title.visible = true)
	var tv: VBoxContainer = _title.get_child(0)
	var row := HBoxContainer.new()
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	row.add_theme_constant_override("separation", 10)
	tv.add_child(row)
	var sl := Label.new()
	sl.text = "Seed:"
	row.add_child(sl)
	_seed_edit = LineEdit.new()
	_seed_edit.custom_minimum_size = Vector2(260, 0)
	_seed_edit.text = str(randi() % 1000000)
	row.add_child(_seed_edit)
	var rnd := Button.new()
	rnd.text = "Random"
	rnd.pressed.connect(func() -> void: _seed_edit.text = str(randi() % 1000000))
	row.add_child(rnd)
	var go := Button.new()
	go.text = "  Begin  "
	go.pressed.connect(func() -> void:
		_title.visible = false
		start_pressed.emit())
	row.add_child(go)
	var chb := Button.new()
	chb.text = "  Chronicle  "
	chb.pressed.connect(toggle_chronicle)
	row.add_child(chb)
	if Game.has_save():
		var cont := Button.new()
		cont.text = "  Continue  "
		cont.pressed.connect(func() -> void:
			_title.visible = false
			continue_pressed.emit())
		row.add_child(cont)
	_party_box = HBoxContainer.new()
	_party_box.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	_party_box.grow_horizontal = Control.GROW_DIRECTION_BEGIN
	_party_box.position = Vector2(-16, 8)
	_party_box.add_theme_constant_override("separation", 6)
	_party_box.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(_party_box)
	_craft = PanelContainer.new()
	_craft.set_anchors_preset(Control.PRESET_CENTER)
	_craft.grow_horizontal = Control.GROW_DIRECTION_BOTH
	_craft.grow_vertical = Control.GROW_DIRECTION_BOTH
	_craft.custom_minimum_size = Vector2(620, 0)
	_craft.add_theme_stylebox_override("panel", _box(Color(0.06, 0.02, 0.03, 0.96), GOLD))
	_craft.visible = false
	root.add_child(_craft)
	var cv := VBoxContainer.new()
	_craft.add_child(cv)
	var ct := _label(cv, 24, GOLD)
	ct.text = "Crafting  (C to close)"
	_craft_list = VBoxContainer.new()
	cv.add_child(_craft_list)
	_card = _overlay(root, "", "")
	_card.visible = false
	_card_text = _card.get_meta("sub")
	_card_text.add_theme_font_size_override("font_size", 26)
	_card.gui_input.connect(func(ev: InputEvent) -> void:
		if ev is InputEventMouseButton and ev.pressed:
			_card.visible = false
			modal = false
			if _card_goto == "__title__":
				_card_goto = ""
				_title.visible = true
			elif _card_goto != "":
				var to := _card_goto
				_card_goto = ""
				Game.queued_after = {}
				Game.goto_requested.emit(to, Game.current)
			else:
				Game.card_done())
	Game.card_requested.connect(func(text: String, then_goto: String) -> void:
		_card_text.text = text + "\n\n[click to continue]"
		_card_goto = then_goto
		_card.visible = true
		modal = true)
	_journal = PanelContainer.new()
	_journal.set_anchors_preset(Control.PRESET_CENTER)
	_journal.grow_horizontal = Control.GROW_DIRECTION_BOTH
	_journal.grow_vertical = Control.GROW_DIRECTION_BOTH
	_journal.custom_minimum_size = Vector2(1000, 520)
	_journal.add_theme_stylebox_override("panel", _box(Color(0.1, 0.07, 0.04, 0.97), GOLD))
	_journal.visible = false
	root.add_child(_journal)
	var jh := HBoxContainer.new()
	_journal.add_child(jh)
	_jlist = ItemList.new()
	_jlist.custom_minimum_size = Vector2(300, 0)
	jh.add_child(_jlist)
	_jtext = RichTextLabel.new()
	_jtext.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_jtext.add_theme_font_size_override("normal_font_size", 19)
	_jtext.bbcode_enabled = true
	jh.add_child(_jtext)
	_jlist.item_selected.connect(func(i: int) -> void:
		var e: Dictionary = Game.world.journal[str(Game.journal[i])]
		_jtext.text = "[b]%s[/b]\n[i]%s[/i]\n\n%s" % [e.title, e.get("source", ""), e.text])
	_pp = PanelContainer.new()
	_pp.set_anchors_preset(Control.PRESET_CENTER)
	_pp.grow_horizontal = Control.GROW_DIRECTION_BOTH
	_pp.grow_vertical = Control.GROW_DIRECTION_BOTH
	_pp.custom_minimum_size = Vector2(1040, 560)
	_pp.add_theme_stylebox_override("panel", _box(Color(0.05, 0.04, 0.07, 0.97), GOLD))
	_pp.visible = false
	root.add_child(_pp)
	var pph := HBoxContainer.new()
	pph.add_theme_constant_override("separation", 14)
	_pp.add_child(pph)
	_pp_list = VBoxContainer.new()
	_pp_list.custom_minimum_size = Vector2(250, 0)
	pph.add_child(_pp_list)
	_pp_detail = VBoxContainer.new()
	_pp_detail.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	pph.add_child(_pp_detail)
	Game.level_up.connect(func(id: String, lv: int) -> void:
		say("%s reaches level %d!" % [str(Game.systems.party[id].name), lv])
		Audio.sfx("levelup"))
	_menu = PanelContainer.new()
	_menu.set_anchors_preset(Control.PRESET_CENTER)
	_menu.grow_horizontal = Control.GROW_DIRECTION_BOTH
	_menu.grow_vertical = Control.GROW_DIRECTION_BOTH
	_menu.custom_minimum_size = Vector2(460, 0)
	_menu.add_theme_stylebox_override("panel", _box(Color(0.05, 0.03, 0.05, 0.97), GOLD))
	_menu.visible = false
	root.add_child(_menu)
	var mv := VBoxContainer.new()
	mv.add_theme_constant_override("separation", 8)
	_menu.add_child(mv)
	var mt := _label(mv, 28, GOLD)
	mt.text = "Menu"
	for ch in [["master", "Master"], ["music", "Music"], ["ambience", "Ambience"], ["sfx", "Effects"]]:
		var mrow := HBoxContainer.new()
		var mlb := Label.new()
		mlb.text = str(ch[1])
		mlb.custom_minimum_size = Vector2(110, 0)
		mrow.add_child(mlb)
		var msl := HSlider.new()
		msl.min_value = 0.0
		msl.max_value = 1.0
		msl.step = 0.05
		msl.value = float(Audio.volume[ch[0]])
		msl.custom_minimum_size = Vector2(280, 24)
		msl.value_changed.connect(func(v: float) -> void: Audio.set_volume(str(ch[0]), v))
		mrow.add_child(msl)
		mv.add_child(mrow)
	var qrow := HBoxContainer.new()
	var qlb := Label.new()
	qlb.text = "Quality"
	qlb.custom_minimum_size = Vector2(110, 0)
	qrow.add_child(qlb)
	var qopt := OptionButton.new()
	for qn in ["Low (no particles/glow/shadows)", "Medium", "High (SSAO, antialiasing)"]:
		qopt.add_item(qn)
	qopt.select({"low": 0, "medium": 1, "high": 2}.get(str(Game.meta.get("quality", "medium")), 1))
	qopt.item_selected.connect(func(i: int) -> void:
		Game.meta["quality"] = ["low", "medium", "high"][i]
		Game.save_meta()
		say("Quality changes when you enter the next scene."))
	qrow.add_child(qopt)
	mv.add_child(qrow)
	var pm := CheckButton.new()
	pm.text = "Pie menu: click an object to choose Look / Use / Talk (Full Throttle style)"
	pm.button_pressed = bool(Game.meta.get("pie_menu", true))
	pm.focus_mode = Control.FOCUS_NONE
	pm.toggled.connect(func(on: bool) -> void:
		Game.meta["pie_menu"] = on
		Game.save_meta())
	mv.add_child(pm)
	var am := CheckButton.new()
	am.text = "Action mode: wild creatures roam the open world, click to fight (applies when entering a region)"
	am.button_pressed = bool(Game.meta.get("action_mode", false))
	am.focus_mode = Control.FOCUS_NONE
	am.toggled.connect(func(on: bool) -> void:
		Game.meta["action_mode"] = on
		Game.save_meta()
		say("Action mode %s - takes effect when you next enter an open region." % ("on" if on else "off")))
	mv.add_child(am)
	for entry in [["Party and equipment (P)", "party"], ["Chronicle (M)", "chronicle"], ["Journal (J)", "journal"], ["Crafting (C)", "craft"]]:
		var mb := Button.new()
		mb.text = str(entry[0])
		mb.focus_mode = Control.FOCUS_NONE
		mb.pressed.connect(func() -> void:
			_close_menu()
			_open_panel(str(entry[1])))
		mv.add_child(mb)
	var resume := Button.new()
	resume.text = "Resume"
	resume.focus_mode = Control.FOCUS_NONE
	resume.pressed.connect(_close_menu)
	mv.add_child(resume)
	var quit := Button.new()
	quit.text = "Quit game"
	quit.focus_mode = Control.FOCUS_NONE
	quit.pressed.connect(func() -> void:
		Game.save_game()
		get_tree().quit())
	mv.add_child(quit)
	_chron = PanelContainer.new()
	_chron.set_anchors_preset(Control.PRESET_CENTER)
	_chron.grow_horizontal = Control.GROW_DIRECTION_BOTH
	_chron.grow_vertical = Control.GROW_DIRECTION_BOTH
	_chron.custom_minimum_size = Vector2(980, 0)
	_chron.add_theme_stylebox_override("panel", _box(Color(0.06, 0.04, 0.08, 0.97), GOLD))
	_chron.visible = false
	root.add_child(_chron)
	var chv := VBoxContainer.new()
	_chron.add_child(chv)
	var cht := _label(chv, 26, GOLD)
	cht.text = "Chronicle - personal stories  (M to close)"
	var chscroll := ScrollContainer.new()
	chscroll.custom_minimum_size = Vector2(0, 470)
	chv.add_child(chscroll)
	_chron_list = VBoxContainer.new()
	_chron_list.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	chscroll.add_child(_chron_list)
	_chron_info = _label(chv, 16, PARCH)
	_chron_info.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	Game.journal_added.connect(func(id: String) -> void: say("Journal updated: %s  (J)" % Game.world.journal[id].title))
	Game.party_changed.connect(_rebuild_party)
	Game.message.connect(say)
	Game.inventory_changed.connect(_rebuild_inventory)
	Game.dialogue_requested.connect(start_dialogue)
	_rebuild_inventory()
	_rebuild_party()
	modal = true


func _process(delta: float) -> void:
	if _msg_timer > 0.0:
		_msg_timer -= delta
		if _msg_timer <= 0.0:
			_msg.text = ""


func _label(parent: Node, size: int, color: Color) -> Label:
	var l := Label.new()
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", color)
	l.add_theme_color_override("font_outline_color", Color(0, 0, 0, 0.95))
	l.add_theme_constant_override("outline_size", 6)
	l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(l)
	return l


func _box(bg: Color, border: Color) -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = bg
	s.border_color = border
	s.set_border_width_all(2)
	s.set_corner_radius_all(4)
	s.set_content_margin_all(12)
	return s


func _overlay(root: Control, title: String, sub: String) -> Control:
	var c := ColorRect.new()
	c.color = Color(0.02, 0.0, 0.02, 0.96)
	c.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.add_child(c)
	var vb := VBoxContainer.new()
	vb.set_anchors_preset(Control.PRESET_CENTER)
	vb.grow_horizontal = Control.GROW_DIRECTION_BOTH
	vb.grow_vertical = Control.GROW_DIRECTION_BOTH
	vb.custom_minimum_size = Vector2(900, 0)
	vb.mouse_filter = Control.MOUSE_FILTER_IGNORE
	c.add_child(vb)
	var t := _label(vb, 96, Color("#a31520"))
	t.text = title
	t.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	var s := _label(vb, 22, PARCH)
	s.text = sub
	s.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	s.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	c.set_meta("sub", s)
	return c


# ------------------------------------------------------------------ api ----
func seed_text() -> String:
	return _seed_edit.text


func set_hover(t: String) -> void:
	_hover.text = t


func set_location_title(t: String) -> void:
	_loc_title.text = t


func say(text: String) -> void:
	_msg.text = text
	_msg_timer = 4.0 + text.length() * 0.045


func fade_to(a: float, t: float = 0.5) -> void:
	if fast_fade:
		_fade.modulate.a = a
		return
	var tw := create_tween()
	tw.tween_property(_fade, "modulate:a", a, t)
	await tw.finished


func show_ending(text: String) -> void:
	_end_text.text = text
	_end.visible = true
	modal = true



func _close_menu() -> void:
	_menu.visible = false
	modal = false


func _open_panel(which: String) -> void:
	match which:
		"party":
			toggle_party()
		"chronicle":
			toggle_chronicle()
		"journal":
			_journal.visible = true
			modal = true
			_jlist.clear()
			for id in Game.journal:
				_jlist.add_item(str(Game.world.journal[id].title))
			if _jlist.item_count > 0:
				_jlist.select(_jlist.item_count - 1)
				_jlist.item_selected.emit(_jlist.item_count - 1)
		"craft":
			_craft.visible = true
			modal = true
			_rebuild_craft()


func toggle_party() -> void:
	_pp.visible = not _pp.visible
	modal = _pp.visible
	if _pp.visible:
		_pp_rebuild()


func _pp_rebuild() -> void:
	for c in _pp_list.get_children():
		c.queue_free()
	var t := Label.new()
	t.text = "Party  (P to close)"
	t.add_theme_font_size_override("font_size", 22)
	t.add_theme_color_override("font_color", GOLD)
	_pp_list.add_child(t)
	if _pp_sel == "" or not Game.party.has(_pp_sel):
		_pp_sel = str(Game.party[0]) if Game.party.size() > 0 else ""
	for id in Game.party:
		var m: Dictionary = Game.systems.party[id]
		var b := Button.new()
		b.text = " %s  Lv %d" % [str(m.name), Game.level_of(str(id))]
		b.alignment = HORIZONTAL_ALIGNMENT_LEFT
		b.focus_mode = Control.FOCUS_NONE
		var path := "res://assets/portraits/%s.png" % str(m.portrait)
		if ResourceLoader.exists(path):
			b.icon = load(path)
			b.expand_icon = true
			b.add_theme_constant_override("icon_max_width", 52)
		b.custom_minimum_size = Vector2(0, 58)
		b.toggle_mode = true
		b.button_pressed = (str(id) == _pp_sel)
		b.pressed.connect(func() -> void:
			_pp_sel = str(id)
			_pp_rebuild())
		_pp_list.add_child(b)
	_pp_show()


func _pp_show() -> void:
	for c in _pp_detail.get_children():
		c.queue_free()
	if _pp_sel == "":
		return
	var id := _pp_sel
	var m: Dictionary = Game.systems.party[id]
	var st: Dictionary = Game.member_state[id]
	var eff := Game.effective(id)
	var title := _label(_pp_detail, 28, GOLD)
	title.text = "%s   Level %d" % [str(m.name), Game.level_of(id)]
	var nxt := Game.xp_to_next(id)
	var xpl := _label(_pp_detail, 16, PARCH)
	xpl.text = "XP %d / %s" % [int(st.get("xp", 0)), str(nxt) if nxt > 0 else "max"]
	var blurb := _label(_pp_detail, 15, Color("#bfae8a"))
	blurb.text = str(m.get("blurb", ""))
	blurb.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	var grid := GridContainer.new()
	grid.columns = 4
	grid.add_theme_constant_override("h_separation", 26)
	_pp_detail.add_child(grid)
	var rows := [["HP", "%d / %d" % [int(st.hp), int(eff.max_hp)]], ["Nerve", "%d / %d" % [int(st.nerve), int(eff.max_nerve)]], ["Accuracy", str(eff.acc)],
		["Evasion", str(eff.eva)], ["Faith", str(eff.faith)], ["Damage +", str(eff.dmg)], ["Armor", str(eff.armor)], ["Speed", str(m.spd)]]
	for r in rows:
		var a := Label.new()
		a.text = str(r[0])
		a.add_theme_color_override("font_color", GOLD)
		grid.add_child(a)
		var v := Label.new()
		v.text = str(r[1])
		grid.add_child(v)
	var eh := _label(_pp_detail, 20, GOLD)
	eh.text = "Equipment"
	for slot in ["weapon", "armor", "charm"]:
		var row := HBoxContainer.new()
		var lb := Label.new()
		lb.text = slot.capitalize()
		lb.custom_minimum_size = Vector2(90, 0)
		row.add_child(lb)
		var ob := OptionButton.new()
		ob.custom_minimum_size = Vector2(420, 0)
		ob.add_item("(auto: best weapon)" if slot == "weapon" else "(none)")
		ob.set_item_metadata(0, "")
		var cur := str(st.get("equip", {}).get(slot, ""))
		var sel := 0
		for it in Game.inventory:
			if not Game.systems.equip.has(it) or str(Game.systems.equip[it].slot) != slot:
				continue
			if slot == "weapon":
				var w: Dictionary = Game.systems.weapons[str(Game.systems.equip[it].weapon)]
				var users: Array = w.get("users", ["any"])
				if not (users.has("any") or users.has(id)):
					continue
			var other := Game.equipped_by(str(it))
			var label := str(Game.systems.equip[it].name) + (" (worn by %s)" % str(Game.systems.party[other].name) if other != "" and other != id else "")
			ob.add_item(label)
			ob.set_item_metadata(ob.item_count - 1, str(it))
			if str(it) == cur:
				sel = ob.item_count - 1
		ob.select(sel)
		ob.item_selected.connect(func(i: int) -> void:
			Game.equip(id, slot, str(ob.get_item_metadata(i)))
			_pp_show())
		row.add_child(ob)
		_pp_detail.add_child(row)
		if cur != "" and Game.systems.equip.has(cur):
			var d := Label.new()
			d.text = "      " + str(Game.systems.equip[cur].desc)
			d.add_theme_font_size_override("font_size", 13)
			d.add_theme_color_override("font_color", Color("#bfae8a"))
			_pp_detail.add_child(d)
	var sh := _label(_pp_detail, 20, GOLD)
	sh.text = "Skills"
	for sk in m.skills:
		var s: Dictionary = Game.systems.skills[sk]
		var sl := Label.new()
		sl.text = "  %s - %s" % [str(s.name), str(s.text)]
		sl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		sl.add_theme_font_size_override("font_size", 14)
		_pp_detail.add_child(sl)


func toggle_chronicle() -> void:
	_chron.visible = not _chron.visible
	modal = _chron.visible
	if _chron.visible:
		_rebuild_chronicle()


func _rebuild_chronicle() -> void:
	for c in _chron_list.get_children():
		c.queue_free()
	var arcs: Array = Game.world.get("arcs_list", [])
	if arcs.is_empty():
		_chron_info.text = "No personal stories installed."
		return
	_chron_info.text = "Optional stories played as one character. Finishing them grants permanent rewards. Some unlock through your choices; some only after the credits."
	for a in arcs:
		var st := Game.arc_status(str(a.id))
		var row := HBoxContainer.new()
		var tr := TextureRect.new()
		var path := "res://assets/portraits/%s.png" % str(a.get("portrait", a.get("member", "")))
		if ResourceLoader.exists(path):
			tr.texture = load(path)
		tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		tr.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
		tr.custom_minimum_size = Vector2(56, 56)
		row.add_child(tr)
		var l := Label.new()
		l.custom_minimum_size = Vector2(560, 0)
		l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		var status: String = {"done": "[completed]", "available": "[available]", "locked": "[locked]", "active": "[in progress]"}[st]
		var extra := ""
		if st == "locked":
			extra = "\n   " + str(a.get("unlock_text", "Complete the main story." if a.get("after_credits", false) else "Not yet unlocked."))
		elif st != "done":
			extra = "\n   " + str(a.get("blurb", ""))
		l.text = "%s %s%s" % [str(a.title), status, extra]
		row.add_child(l)
		var b := Button.new()
		b.text = "Play" if st != "done" else "Replay"
		b.disabled = st == "locked" or st == "active"
		b.focus_mode = Control.FOCUS_NONE
		b.tooltip_text = str(a.get("rewards_text", ""))
		b.pressed.connect(func() -> void:
			_chron.visible = false
			modal = false
			arc_requested.emit(str(a.id)))
		row.add_child(b)
		_chron_list.add_child(row)


var _travel: TravelMap
var _pie: PieMenu
var _pie_eid := ""


func show_pie(eid: String, pos: Vector2, title: String, verbs: Array) -> void:
	if _pie == null:
		_pie = PieMenu.new()
		_pie.set_anchors_preset(Control.PRESET_FULL_RECT)
		_pie.visible = false
		_pie.chosen.connect(func(v: String) -> void:
			modal = false
			Game.pie_chosen.emit(_pie_eid, v))
		_pie.cancelled.connect(func() -> void: modal = false)
		root.add_child(_pie)
	if modal:
		return
	_pie_eid = eid
	modal = true
	_pie.open(pos, title, verbs)


func open_map() -> void:
	if _travel == null:
		_travel = TravelMap.new()
		_travel.set_anchors_preset(Control.PRESET_FULL_RECT)
		_travel.visible = false
		_travel.travel.connect(func(to: String) -> void:
			modal = false
			Game.goto_requested.emit(to, Game.current))
		_travel.closed.connect(func() -> void: modal = false)
		root.add_child(_travel)
	if _travel.visible or modal or not TravelMap.has_map(Game.current):
		return
	modal = true
	_travel.open(Game.current)


func _unhandled_key_input(ev: InputEvent) -> void:
	var free_state: bool = not _title.visible and not _end.visible and not _card.visible
	if ev.pressed and ev.keycode == KEY_T and free_state:
		if _travel != null and _travel.visible:
			_travel.close()
		else:
			open_map()
	if ev.pressed and ev.keycode == KEY_P and free_state and (not modal or _pp.visible):
		toggle_party()
	if ev.pressed and ev.keycode == KEY_ESCAPE and free_state:
		if _pie != null and _pie.visible:
			_pie.close()
			modal = false
		elif _travel != null and _travel.visible:
			_travel.close()
		elif _menu.visible:
			_close_menu()
		elif _pp.visible or _chron.visible or _journal.visible or _craft.visible:
			_pp.visible = false
			_chron.visible = false
			_journal.visible = false
			_craft.visible = false
			modal = false
		elif not modal:
			_menu.visible = true
			modal = true
	if ev.pressed and ev.keycode == KEY_M and not _title.visible and not _end.visible and not _card.visible and (not modal or _chron.visible):
		toggle_chronicle()
	if ev.pressed and ev.keycode == KEY_J and not _title.visible and not _end.visible and not _card.visible and (not modal or _journal.visible):
		_journal.visible = not _journal.visible
		modal = _journal.visible
		if _journal.visible:
			_jlist.clear()
			for id in Game.journal:
				_jlist.add_item(str(Game.world.journal[id].title))
			if _jlist.item_count > 0:
				_jlist.select(_jlist.item_count - 1)
				_jlist.item_selected.emit(_jlist.item_count - 1)
			else:
				_jtext.text = "Nothing written yet."
	if ev.pressed and ev.keycode == KEY_C and not _title.visible and not _end.visible and (not modal or _craft.visible):
		_craft.visible = not _craft.visible
		modal = _craft.visible
		if _craft.visible:
			_rebuild_craft()


func _rebuild_party() -> void:
	if _pp != null and _pp.visible:
		_pp_rebuild()
	for c in _party_box.get_children():
		c.queue_free()
	for id in Game.party:
		var m: Dictionary = Game.systems.party[id]
		var st: Dictionary = Game.member_state.get(id, {"hp": m.hp})
		var maxhp := int(Game.effective(str(id)).max_hp) if Game.member_state.has(id) else int(m.hp)
		var vb := VBoxContainer.new()
		var tr := TextureRect.new()
		var path := "res://assets/portraits/%s.png" % m.portrait
		if ResourceLoader.exists(path):
			tr.texture = load(path)
		tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		tr.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
		tr.custom_minimum_size = Vector2(64, 64)
		vb.add_child(tr)
		var l := _label(vb, 13, PARCH)
		l.text = "L%d  %d/%d%s" % [Game.level_of(str(id)), int(st.hp), maxhp, " *" if st.get("drained", false) else ""]
		l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		_party_box.add_child(vb)


func _rebuild_craft() -> void:
	for c in _craft_list.get_children():
		c.queue_free()
	var any := false
	for rid in Game.systems.recipes:
		var r: Dictionary = Game.systems.recipes[rid]
		if not Game.check(str(r.get("unlock", ""))):
			continue
		any = true
		var need: Array = []
		for it in r.needs:
			need.append("%s %d/%d" % [Game.item_name(it), Game.count(it), int(r.needs[it])])
		for t in r.get("tools", []):
			need.append("tool: %s %s" % [Game.item_name(t), "ok" if Game.has_item(t) else "missing"])
		var b := Button.new()
		b.text = "%s   (%s)" % [r.name, ", ".join(PackedStringArray(need))]
		b.tooltip_text = str(r.text)
		b.alignment = HORIZONTAL_ALIGNMENT_LEFT
		b.focus_mode = Control.FOCUS_NONE
		b.disabled = Game.can_craft(rid) != ""
		b.pressed.connect(func() -> void:
			Game.craft(rid)
			_rebuild_craft())
		_craft_list.add_child(b)
	if not any:
		var l := Label.new()
		l.text = "No recipes known yet."
		_craft_list.add_child(l)


func _rebuild_inventory() -> void:
	for c in _inv.get_children():
		c.queue_free()
	var hint := Label.new()
	hint.text = "Items:" if Game.inventory.size() > 0 else "(no items)"
	hint.add_theme_color_override("font_color", GOLD)
	_inv.add_child(hint)
	for id in Game.inventory:
		var b := Button.new()
		b.text = Game.item_name(id) + (" x%d" % Game.count(id) if Game.count(id) > 1 else "")
		b.toggle_mode = true
		b.button_pressed = (Game.selected_item == id)
		b.focus_mode = Control.FOCUS_NONE
		b.gui_input.connect(func(ev: InputEvent) -> void:
			if ev is InputEventMouseButton and ev.pressed:
				if ev.button_index == MOUSE_BUTTON_LEFT:
					Game.selected_item = "" if Game.selected_item == id else id
					Game.inventory_changed.emit()
				elif ev.button_index == MOUSE_BUTTON_RIGHT:
					say(str(Game.item_def(id).desc)))
		_inv.add_child(b)


# -------------------------------------------------------------- dialogue ----
func start_dialogue(id: String) -> void:
	_dialogue = Game.world.dialogue[id]
	modal = true
	_dlg.visible = true
	_node(str(_dialogue.start))


func _node(nid: String) -> void:
	var n: Dictionary = _dialogue.nodes[nid]
	_dlg_speaker.text = str(n.speaker)
	Game.speaking.emit(str(n.speaker))
	_dlg_text.text = str(n.text)
	for c in _dlg_choices.get_children():
		c.queue_free()
	if n.has("do"):
		Game.run(n.do)
	var choices: Array = n.get("choices", [])
	var shown := 0
	for ch in choices:
		var d: Dictionary = ch
		if not Game.check(str(d.get("cond", ""))):
			continue
		_choice_button(str(d.text), func() -> void: _pick_choice(d))
		shown += 1
	if shown == 0:
		_choice_button("Continue", func() -> void:
			if n.has("next"):
				_node(str(n.next))
			else:
				_close_dialogue())


func _choice_button(text: String, cb: Callable) -> void:
	var b := Button.new()
	b.text = "  " + text
	b.alignment = HORIZONTAL_ALIGNMENT_LEFT
	b.focus_mode = Control.FOCUS_NONE
	b.pressed.connect(cb)
	_dlg_choices.add_child(b)


func _pick_choice(d: Dictionary) -> void:
	var closing: bool = d.get("end", false) or not d.has("next")
	if d.has("do"):
		if closing:
			_close_dialogue()
		Game.run(d.do)
		if not closing:
			_node(str(d.next))
		return
	if closing:
		_close_dialogue()
	else:
		_node(str(d.next))


func _close_dialogue() -> void:
	Game.speaking.emit("")
	_dlg.visible = false
	modal = false
	dialogue_finished.emit()
