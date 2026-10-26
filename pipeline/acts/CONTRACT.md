# Act authoring contract

You are writing ONE act of a 3D point&click adventure of Bram Stoker's *Dracula* (Godot 4 engine already written).
Deliver one Python data file `pipeline/acts/act_N.py` (+ optionally `pipeline/acts/act_N_builders.py` for new 3D models).
Do not edit any other file. Work only inside your own act file(s). Other acts are being written in parallel by others.

## Read first
1. This file, then `pipeline/acts/example_act.py` (working example), then `pipeline/dsl.py` (helpers: `prop`, `npc`, `cam`,
   `AMBIENT`, `lights_*`, `T`, colour dicts) and the base game in `pipeline/bible_src.py` (see LOC_DATA / DIALOGUE of the
   finished Act I: how rooms, props, puzzles and dialogue look in practice).
2. The book text for your chapters: `book/chapters/chapter_NN.txt` and the structured extraction `book/extract/chapter_NN.json`
   (scenes, locations, objects, puzzles, combat, dialogue_samples, asset_candidates, quest_hooks). `book/book_db.json` has everything merged.
   `docs/DESIGN.md` explains the systems (rules/combat/crafting). Film scripts in `book/pdf/` are inspiration only.
3. `python3 pipeline/list_assets.py [filter]` lists every usable 3D model with its material roles and variants,
   and the available texture ids.

## Quality bar
* Follow the novel's story and set pieces faithfully: the player must live the key events of your chapters in order
  (as the characters of that chapter, using `protagonist` switches where the book switches narrator).
* Add richness beyond the book where it fits the theme: optional rooms, side puzzles, found objects/documents,
  extra NPC chatter, collectables, crafting ingredients (garlic, wood, cloth, rope, oil, water, knife, silver, host,
  bullets, wild rose...), hidden notes, small mysteries. Mark nothing as canon that contradicts the book.
* Writing: English, Victorian register, diary/epistolary flavour, short evocative `look` texts (1-3 sentences) on EVERY
  named prop and NPC. Dialogue: each important NPC has real conversations with choices that matter or reveal lore.
  Journal entries (text <= 70 words) summarise story beats in the narrator's voice; at least 3 per chapter covered.
* Scale (minimum): 7+ locations (some outdoor, some interior), 18+ dialogues/NPC conversations, 8+ real puzzles
  (inventory chains, deduction with journal/flag conditions, ritual order, social, timing), 2+ combat encounters
  where the book has fights, 12+ items, a real finale for the act. More is welcome if it stays coherent.
* Puzzles must be solvable by reasoning from clues the player can find. Chain them (item A opens B gives C).
* Every location needs on-screen life: 8-16 props (furniture, clutter, windows/doors, light sources) and NPCs.
  Use existing models creatively (re-textured variants). If a key model is missing, write a builder (see below).

## File layout (all names are module-level variables in act_N.py; all optional except ACT and LOC_DATA)
```
ACT = dict(id=N, title="..", start=dict(location=.., protagonist=<party id>, party=[..], items={item: count}, flags=[..]),
           exit_to="<first location id of the next act>")      # last act: exit_to="END" and an end_text/{"end":..} action
LOCATIONS = [dict(id, name, desc, date?)]       # one per location: HUD title; desc shown once on first entry
LOC_DATA = {loc_id: {...}}                       # see below
DIALOGUE = {id: dict(start="n0", nodes={...})}
ITEMS = {id: dict(name, asset, variant, desc)}   # asset must exist; existing item ids may be reused (see systems below)
JOURNAL = {id: dict(title, source, text)}
PLACEMENTS / GATES / PALETTES                    # seed variation (optional, see below)
ENCOUNTER_HOOKS = {encounter_id: dict(on_win=[do..], on_lose=[do..], on_flee=[do..])}
ENCOUNTERS_EXTRA / ENEMIES_EXTRA / RECIPES_EXTRA # new combat encounters/enemies/recipes (formats: see data/systems.json)
ASSETS = [dict(id, builder, params)]  VARIANTS = {asset_id: {"default": name, name: {role: T(tex, tint)}}}  ROLE_DEFAULTS = {}
```
IDs must be globally unique: prefix every id (locations, props, npcs, dialogues, items, journal, flags, encounters, assets)
with `aN_` (e.g. `a3_study`, `a3_renfield_talk`, flag `a3_saw_letter`) EXCEPT: existing ids you reuse deliberately
(items from `data/systems.json`: crucifix, host, garlic, garlic_wreath, wild_rose, brandy, bandage, chloral, holy_water, stake,
hammer, bullet, sacred_bullet, torch, holy_knife, kukri, winchester, cloth, rope, wood, oil, water, knife, silver; party ids:
harker mina vanhelsing seward quincey arthur; encounters: borgo_wolves szgany_cart brides_wing brides_tombs lucy_tomb
carfax_rats renfield_frenzy dracula_chase; enemies: wolf wolf_alpha rat bat szgany carrier bride lucy renfield dracula).

## LOC_DATA entry
```
cells=[cx, cz]          room is cx*4 by cz*4 metres, centred on 0; x right, z toward the camera (south), y up
interior=True|False     interiors need `walls`; exteriors extend the ground 2 cells beyond the room
wall="plaster"          wall material variant; floor="planks"   (variants of wall_4/floor_4x4: stone_grey stone_mossy stone_dark
                        stone_tomb plaster plaster_dirty cobble planks dirt grass snow)
ambient=AMBIENT[..]  camera=cam([cx,cz])  lights=[..]  (use dsl helpers; any lighting mood you like; moon=dict(pos=[x,y,z]) adds moon+sun for night)
walls=dict(north=[pieces..], west=[..], east=[..])   pieces: "wall_4" | "wall_door_4" | "wall_window_4"; north has cx entries (x left->right),
                        west/east have cz entries (z back->front). The south side is open (camera side). Exteriors: omit walls or use partial walls.
scatter=dict(asset="pine", variant="dark", count=26, seed=11, avoid=[[x0,z0,x1,z1]])  (outdoor trees/rocks outside the room; optional scatter2/3)
spawn=[x,z]  spawns={from_location_id: [x,z]}   where the player appears (WorldGen recomputes spawns for wall doors automatically)
props=[prop(..)...]  npcs=[npc(..)...]  on_enter=[dict(if=cond, once=True, do=[..])]
```
Placement rules: a door prop (asset starting `door`, with `go=`) must stand ON a wall line, centred on a `wall_door_4` piece:
north wall z = -d/2+0.2 (x = cell centre), west x = -w/2+0.2 (rot 90), east x = w/2-0.2 (rot -90); cell centres are -w/2+2+4*i.
Keep 1 m clear between free props; props within 1.6 m of a wall are treated as wall-anchored (never jittered); other props and NPCs
are jittered +-0.5 m by the seed so never rely on exact positions. Items standing on a table use y=0.8 and the same x,z as the table.
Prop orientation: model front is +z (toward camera) at rot 0; rot=90 faces +x, rot=-90 faces -x, rot=180 faces away.
Walkable area = room minus 1 m margin. Camera sees the whole room; don't hide interactive props behind tall ones.
Props without name/interact are pure decoration (not clickable). Anything with `name` AND interact is clickable.
Exits to other locations are `go=` props (doors, gates, stairs, a carriage...). Every location needs at least one way back unless the
transition is deliberately one-way (then everything the player still needs behind must be finished before: the validator checks this).

## Camera zones (optional)
The default `camera` is used while the player is in the middle of the scene. Wide scenes (>= 3 cells) automatically get left/right diagonal side views
that the camera cuts to when the character walks into that part of the scene (key V cycles views manually). You can author your own:
`cameras=[dict(id="pier", rect=[x0, z0, x1, z1], pos=[x, y, z], look=[x, y, z], fov=50), ...]` - first matching rect wins; a camera positioned outside
a walled room hides the wall in front of it (add the matching `walls` side: "south" is supported). Use zones to reach corners and "other sides"
of a location: large scenes (cells up to 6x4) with items spread over several areas are welcome. `auto_cameras=False` turns the automatic side views off.

## prop()/npc() interact keys (precedence when clicked: fight > talk > end_text > go > take > set > look)
look="text"                    right-click text (also left-click fallback)
take="item_id", take_text=.., give_once=True   pick up (once). Without give_once the prop disappears when taken.
set="flag", set_text=..        sets a flag once (also used as a first-click gate before `go`, e.g. knocking)
go="location_id", go_cond="has:x&flag:y", go_fail="text"   walk through; cond false -> go_fail text
talk="dialogue_id"             opens dialogue
fight="encounter_id"           starts a combat (winning sets flag won:<encounter>, removes the NPC, runs ENCOUNTER_HOOKS)
end_text="text", go_cond=..    finale of the whole game (last act only)
use_item={item_id: [do..]}, use_fail=..   "use item X on this" actions
cond="..."  (prop(..., cond=...)) visibility: the entity exists only while the condition holds (re-evaluated live when flags/items change).
Conditions: `flag:x` (or bare `x`), `has:item`, `journal:entry`, `party:id`, `!cond` (negation, ONLY for visibility, never for progress gating),
joined with `&`. `prot:id` also exists but is cosmetic only, do not gate progress on it.
`do` lists = scripted actions, executed in order: {"say": text} {"give": item} {"take": item} {"set": flag} {"journal": id}
{"recruit": party_id} {"protagonist": party_id} {"heal": 1} {"goto": location} {"card": text} (full-screen title card; together with goto in the
same list the card is shown first, then the move: use this for scene/act transitions and time jumps) {"talk": dialogue_id}
{"fight": encounter_id} {"end": text}.  on_enter lists may ONLY use say/card(+goto)/journal/set/give/recruit/protagonist/heal
and only the first matching entry runs per arrival.  Items that are `take`n are consumed.

## Dialogue
```
"id": dict(start="n0", nodes={"n0": dict(speaker="Name", text="...", do=[..]?, choices=[dict(text="..", next="n1", cond=?, do=?, end=?)] | next="n1" | end=True)})
```
Nodes without choices show "Continue" (goes to `next`, or closes). A choice without `next` (or with end=True) closes the dialogue after its `do`.
Dialogues are repeatable, so guard one-time rewards with flags (`cond="!a3_got_x"` on the choice that gives them, and `do=[set a3_got_x, give ..]`).

## Seed variation (optional but welcome: "the same level may differ in puzzles and look")
PALETTES = {loc_id: [dict(wall=.., floor=.., wood=.., cloth=..), ...]}   look variants (always safe)
PLACEMENTS = {item_id: [dict(prop=holder_prop_id, text="found text", hint="clue appended to the holder's look"), ...]}  where a key item is hidden
GATES = {door_prop_id: [dict(cond="has:x", fail="..", needs="x"), ...]}  alternative requirements for one door
Every option must keep the act solvable (the validator checks each with --seed-options). Holders must be reachable without the item itself.

## Combat
Party for fights = `Game.party` (recruit allies with {"recruit": id}; protagonist is just the model/portrait the player walks with).
Use existing encounters/enemies or add ENCOUNTERS_EXTRA/ENEMIES_EXTRA with the same keys as data/systems.json (encounter: name, time
(day/dusk/night/dawn), enemies=[enemy ids], flee_ok, intro, win, optional survive=<rounds until dawn>, in_boxes=True for sleeping vampires).
Hooks (`ENCOUNTER_HOOKS`) continue the story after a fight (set flags, journal, goto + card). A lost fight restores the party at half HP:
always provide an `on_lose` that lets the story go on (never a dead end).

## New 3D assets (only if needed; reuse first)
ASSETS entry `dict(id="aN_name", builder="name", params={})` with a builder function `b_name(a, **params)` in `pipeline/acts/act_N_builders.py`.
Read `pipeline/blender_gen.py` (class Asset: `part`, `box`, `cyl`, `sphere`, `beam`; model front is -Y in Blender = +z in game; origin at the base centre,
1 unit = 1 m; material ROLE names like stone/wood/iron/cloth/leather/gold/glass/wax/flame/skin/hair/top/bottom; keep models low-poly and
readable from above at 3-8 m). Add VARIANTS with texture ids from list_assets.py. Build + preview with
`pipeline/build_act_assets.sh N [asset ids]` then look at /tmp/asset_previews/<id>.png (use the Read tool on the PNG). Only run that script for your act number.

## Validate (mandatory, must end with OK before you finish)
`python3 pipeline/validate_story.py --act N --seed-options`
It checks ids/assets/dialogue/items/conditions and *plays your act*: from ACT["start"] the player must be able to reach ACT["exit_to"]
using only what is in your act. Fix all ERRORs; read WARNs. Never touch data/ or world_bible.json (the validator is read-only).
A one-way transition cannot be undone: the validator completes everything it can before crossing; keep required items before the crossing.
If the act starts with items/flags carried over from earlier acts, put them in ACT["start"].

## Hand-back
Reply with: files written, counts (locations, dialogues, puzzles, items, journal, encounters, new assets), the validator's last line,
the ids of the first and exit locations, and any open problems. Do not paste file contents.
