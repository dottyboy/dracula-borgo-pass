# Dracula - design draft v0.1 (systems built on the book database)

Source of truth: `book/extract/chapter_NN.json` (28 files, AI-extracted from the novel, schema in
`book/EXTRACT_SCHEMA.md`) merged into `book/book_db.json`. Every system below is fed from it; nothing is invented
if the book has an equivalent.

## 1. Structure: point&click story + Might&Magic-style party combat
* **Exploration/story**: current fixed-camera point&click (3rd person), one location per scene.
* **Party** (up to 6, recruited as the novel brings them together): Harker, Mina, Van Helsing, Seward, Quincey, Arthur
  (+ Lucy/Renfield as story-only). Party screen with portraits, equipment, conditions.
* **Combat** (M&M 6-8 style, turn-based): party in front/back rows vs enemy groups; initiative from Speed; actions:
  Attack, Ward (use sacred item), Spell/Rite, Item, Defend, Flee. Fights are rare, deliberate set pieces taken from
  the book's combat entries (wolves at Borgo, Szgany cart, the brides, Lucy in the tomb, Carfax boxes, Piccadilly
  house, final chase) - plus roaming encounters in a few dungeon-style areas (castle depths, Carfax, crypt).
* **Optional first-person grid dungeons** (M&M walk-mode) for castle vault / Carfax cellar / Lucy's tomb; same
  assets, different camera. Later phase, not needed for the core loop.

## 2. Stats and conditions (book-derived, not D&D clones)
* Attributes: **Body** (hp, melee), **Wits** (puzzles, initiative), **Faith** (wards/rites power), **Nerve**
  (resist fear/charm), **Blood** (transfusion/recovery). Characters get signature strengths from the text
  (Van Helsing: lore+rites, Quincey: firearms/bowie knife, Seward: medicine, Mina: shorthand/typewriter/deduction
  = clue combining, Harker: legal/travel, Arthur: leadership).
* Conditions straight from the book: **Charmed** (hypnotic influence), **Drained** (anaemia, needs transfusion),
  **Fear**, **Sleep** (vampire sleep), **Wounded**. Dracula-bond: Mina's bond is a mechanic (clairvoyance via
  hypnosis reveals boxes' location/time of day).

## 3. Vampire rules as game rules (from `vampire_lore`)
Turned into a data table `rules.json` the combat/puzzle code reads: no reflection, no entry unless invited,
sunlight/noon powerlessness, running water crossing, garlic, crucifix, Host (sanctified wafer), wild rose, sleeps
in native earth, stake + decapitation + garlic for the undead, transformation (wolf/bat/mist) at limited hours,
command over wolves/rats/bats, strength of twenty men, etc. Each rule is both an enemy trait AND a puzzle hook.

## 4. Puzzles (from `puzzles`)
Types: *inventory* (key/lantern/hammer chains), *deduction* (Mina's clue board: combine diary/telegram/ledger
entries -> reveal location/time), *ritual* (correct ward order), *timing* (sun position, tides, train/ship timetable),
*social* (dialogue trees with Nerve checks), *logistics* (track Dracula's 50 boxes: find/sanitise each). Each chapter's
`game_idea` field becomes one puzzle definition (`puzzles.json`: preconditions, steps, rewards, flags).

## 5. Crafting (from `crafting`)
Bench-less, recipe-based, discovered through the book's own instructions: garlic wreaths/flowers, sanctified wafer
crumbs, stakes, hammer+stake kits, blessed bullets/knives, transfusion kit, sealed-tomb putty, sedative/chloral
mix, wolfsbane-style wards... Ingredients are world items (`objects` with category). Recipe unlock = reading the
right document or talking to Van Helsing. Quality depends on character skill + ingredient variant.

## 6. Enemies (from `creatures`, `characters`)
Wolves (packs), bats, rats, Szgany guards, the three Sisters, Lucy (undead), Renfield (frenzy), possessed servants,
Dracula (boss with phases tied to time of day, forms, and bound to the rules table). Stat blocks generated from
book descriptions + a balance pass.

## 7. AI use
* **Done / free**: Claude subagents read chapters and fill the JSON schema (no API key, no billing).
* **Assets**: `asset_candidates` (concrete visual descriptions) -> Claude writes Blender builder functions into
  `blender_gen.py` (same pipeline as now: code -> .glb, texture roles/variants). Reviewed via the Gallery scene.
* **Textures/portraits**: procedural textures stay local; character portraits/concept art would need an
  image-generation service the machine does not have - optional later (needs API key + user's OK on cost).
* **Dialogue**: generated per scene from `scenes`, `dialogue_samples`, `speech_style`, kept in the book's
  register; human-readable JSON, edited by hand.

## 8. Build order
1. Merge extraction -> `book_db.json` + coverage report (what the book offers per system).  <- in progress
2. `rules.json`, `recipes.json`, `puzzles.json`, `enemies.json` generated from the db, then curated.
3. Engine: party/inventory/stat model, turn-based combat scene, crafting UI, clue board.
4. Asset sweep: priority-1 `asset_candidates` -> new builders; new locations per act (Whitby, Hillingham, Seward's
   asylum, Carfax, London houses, ship Demeter, Transylvania return chase).
5. Playthrough tests per act (extend `--selftest`).

## 9. Seeded worlds (implemented v1)
Seed is chosen on the title screen (text or number; `-- --seed=abc` in debug). `WorldGen.generate(world, seed)` runs once
at new game, resolves everything random into a plain dictionary and writes `user://worlds/<seed>.json`; the game
afterwards only reads that file (same seed -> identical world, reloaded from disk if present).
Varied per seed: wall/floor/wood/cloth palette per location, door and window cells on each wall (arrival spawns follow
the door), prop and NPC jitter (table items move with the table), light strength, tree style outdoors, **where each
quest item is hidden** (list of holders per item in `PLACEMENTS`, each with a find text and a hint added to the
holder's look text) and **which requirement opens a gate** (`GATES`: lantern or brass key for the forbidden wing).
Solvability is by construction (holders only in areas reachable without that item) and checked by
`godot --headless --path . -- --selftest --seeds=1,2,3...` which solves each seed via BFS over the door graph.
Next: more gate/puzzle templates per location (sequence locks, clue-board deduction), room size variants, enemy
placement per seed.

## 10. Sources
Novel: epub (ch.1-27) + PDF (also has the closing Note = chapter 28). Film material (2nd draft text; shooting
script/storyboards are scans) is kept separate in `book/pdf/` and may only inspire visuals, not canon.

## 11. Implemented: systems v1 (2026-10-19)
* `pipeline/systems_src.py` -> `data/systems.json`: vampire rules (time-of-day power, mundane weapons halved, repel by
  crucifix/Host/garlic/rose, stake+beheading, helpless in box by day), 6 party members (stats from the book),
  9 skills, 9 weapons, combat items, 10 enemies, 8 encounters, 8 crafting recipes (book-based + `extra: true`).
* `scripts/combat.gd` pure-logic turn-based engine (initiative, statuses, nerve/fear, charm, circle, flee, dawn
  survival, vampires drop to "helpless" and need the stake). `scripts/combat_ui.gd` battle screen (3D enemy stage,
  portrait cards, targeting, log). Fights start from props/NPCs with `interact.fight` (wolves at Borgo Pass).
* Crafting panel (key **C**) with recipes unlocked by flags (`rites`, `medicine`); party strip with portraits (top right).
* Tests: `-- --combattest --runs=100` (balance table), `-- --selftest --seeds=...` (full playthrough incl. a UI-driven
  fight and crafting). Balance is tuned for autopilot with perfect kits; early solo Harker is deliberately fragile.
* Cached seeded worlds are invalidated automatically when data/world.json changes (world_hash).
Not yet: recruiting the rest of the party in the story, levelling/XP, equipment screen, first-person dungeon mode,
Whitby/London acts, enemy variety per seed, sound.

## 12. Story complete (2026-10-20)
Six acts, ~76 locations, ~170 dialogues, ~200 journal entries, ~100 items, 14 encounters. Engine verbs: if-conditions, on_enter,
card/journal/recruit/protagonist/heal/fight/end; protagonist switching, journal (J), crafting (C), save/continue.
Validator = exact simulation (negation, protagonist, per-conversation state, item counts) producing replay plans; the replay
found real bugs (placements never spawned, compound conditions, card+fight chains) which are fixed.
Next (user decision 2026-10-20): recruitment - each party member gets a personal story the player must play as that
character (non-book material welcome), then levelling/equipment and the first-person dungeon option.

## 13. Personal arcs (2026-10-20)
Roster (`meet`/`recruit`) is separate from the fighting party. Arcs: isolated state (push/pop snapshot), rewards on `arc_end`, persistent
`meta.game_complete` for after-credits arcs. Playable-only characters: lucy, renfield, dracula (young Voivode), captain.
Rewards: `stat` bonuses (hp/nerve/acc/eva/faith/dmg per member, applied in combat), items, recipe-unlock flags (`rites`, `medicine`).

## 14. Scene growth, cliffs, travel map (2026-10-21)
Open-air scenes grow at runtime (`Location._grow`, `room_w/room_d`): +5x/+4z m per side, cliffs +7/+5, towns with a north building row sideways only. Extra ground gets
deterministic loot props (`Dressing.add_loot`) and themed vegetation (graveyard/wild/dock/street). Cliff scenes use a ragged-edge terrain with the sea at -14 m.
Travel map (`scripts/travel_map.gd`, key **T**, or walk into an open scene edge): shows the outdoor places linked by go-props (interiors as squares), laid out from the
direction of each exit; only direct neighbours are clickable and `go_cond` is honoured. Edge trigger is disabled in tests (`Game.autosave` false).
Map v2: aerial painted map (sea, wobbly land blobs, curved roads, houses/trees/crosses/ruin/boats per theme). Harbour got a west side street + small square (`Dressing._west_street`); smoke puffs use a soft radial sprite.

## 15. Regions / mega scene (2026-10-21)
`scripts/regions.gd` (`Regions.DEF`): several outdoor scenes merged into one continuous landscape. Members keep their own data and are built as islands
(`Location.build_island`: props, NPCs, buildings, lights, loot) on one shared terrain (`Location._terrain` region mode: land rects + connecting strips, ragged coast, sea,
sand shore in the shader), one sea, one follow camera and one player (`Actor.clamp_fn` = irregular walkable area, plus sidestep steering). Walking into another member
fires `member_changed` -> `Main._member_entered` (title, journal on_enter, music, `Game.current`, save). `go` props between members become short in-region teleports.
Active when `Regions.enabled()` (normal play, or `--region` in debug); replays/selftests keep the classic one-scene-per-location path. First region: **whitby** (act II:
harbour - East Cliff - abbey). `--region --loc=<id> --regiontest` walks the whole chain. Members are per act, so chapters without a region just don't have one.
Planned: more regions (Hillingham/Kingstead/Hampstead, asylum+Carfax), London as a city-map region, night variants, then an optional Diablo-style mode.
Regions now: whitby (act II), hillingham (act III: Hillingham garden, asylum garden, zoo, Kingstead churchyard), kingstead_night (act IV), purfleet (act V: asylum grounds + Carfax).
Mood crossfade per member (`Location.apply_member_mood`), region routing through strips (`Location.go_to`, `Actor.walk_path`), irregular cobble patches.
London stays classic scenes + city-style map (`TravelMap._city`: street plan, Thames, house icons).
Action mode (`scripts/action_mode.gd`, Esc menu toggle `Game.meta.action_mode`): real-time roaming creatures in regions, click to fight (stats from systems.json,
protagonist weapon/acc/dmg), XP + drops, respawn on defeat. Tests: `--region --loc=<id> --regiontest`, `--actiontest --loc=<id>`, `REGION=1 ./run_replays.sh 2 3 4 5`.

## 16. Pie menu (2026-10-22)
Full Throttle-style verb ring (`scripts/pie_menu.gd`, `Location._open_pie`, toggle in Esc menu `Game.meta.pie_menu`). Left-click on an object opens it when no inventory item is selected.
Verbs (only those that apply): Look (eye), Take (hand), Use (cog, set-type objects), Use item (satchel -> second ring of inventory items), Talk, Go, Attack, Map (outdoors only -> `Game.map_requested`).
Right-click on empty ground outdoors opens a map-only pie. Esc/right-click/outside closes. Test: `--pietest --loc=a2_harbour`; screenshots `--pie=<eid> --items=brandy:1`.

## 17. Mixamo characters + shared animation library (2026-10-26)
Source FBX (not in git, ~630 MB) live in `pipeline/mixamo/` (characters, `poses/`, `clean/` = de-duplicated clips, `clips.json` = game name -> clip, `anim_manifest.json`).
`export_mixamo.py char|lib` (Blender) builds `assets/models/chars/<id>.glb` (skinned, textures <=1024) and `assets/anims/mixamo_lib.glb` (116 clips on the shared Mixamo skeleton).
`MixamoRig` (scripts/mixamo_rig.gd) loads the library once, strips hips root motion, sets loop modes, builds a character with an AnimationPlayer ("anim") and scales it to a target height.
`MixamoRig.CHARS` maps procedural human models (optionally `model:variant`) to Mixamo characters; `Actor.setup` then uses kind `skinned`: idle/walk/talk/die by state, one-shots via `_SHOT_ANIMS`
(attack->slash, hurt, cast, reach, victory, bow, die, howl->yell), female characters use the female idle/walk/talk clips. Set `MixamoRig.enabled=false` to fall back to the procedural models.
Dedupe is by motion hash (`fingerprint.py`), not by name: "(2)" variants and same-named male/female/mutant clips are different clips (only 31 of 483 were true duplicates).
Mapped so far: human_dracula (Vampire), human_peasant_f (Peasant Girl), human_vanhelsing (Paladin), human_mina (Maria), human_lucy (Eve). All replays PASS.

**Dressed mannequins + cloth (2026-10-26, replaces the per-character Mixamo outfits):** `pipeline/mixamo/dress.py` dresses the bare X Bot / Y Bot as each procedural human
(`humans.json` = HUMANS from bible_src: height, sex, hair, beard, garment coat|frock|dress|gown, hat, cloak, fangs). Torso = inflated shell of the body; sleeves, trousers and boot shafts are smooth
lofted tubes along the bone chains (weights blended at elbow/knee); hands/head stay skin; face, hair, beard, hats, belt, waistcoat built from primitives. Materials are named after the variant colour roles
(skin, eyes, sclera, mouth, hair, top, bottom, shoes, accent, cloak) so `Assets.apply_variant` recolours the skinned humans exactly like the procedural ones (every NPC variant works).
Skirt / coat tails / cloak = hanging grids on chain bones `cloth_<name>_c<col>_b<i>`; `MixamoRig.add_cloth_physics` puts a SpringBoneSimulator3D on them (skeleton space is cm, down = -Y; skirts stiffness 2 gravity .25, capes freer).
`build_costumes.sh [model ...]` rebuilds `assets/models/chars/sk_<model>.glb`; `Actor.setup` uses them automatically when the file exists (`MixamoRig.config_for`), otherwise the procedural model.
The shared animation library is retargeted per skeleton (`MixamoRig.library_for`): only the hips keep a position track (height scaled, no travel), all other bones are rotation-only so other proportions do not stretch.
Mixamo files are git-ignored (licence); release builds embed them.

## 18. Opening titles (2026-10-26)
`scripts/intro.gd` (`Intro`): 44 s sequence in its own SubViewport world - night sky, moonlit mist, castle keep on its crag, pines, bats, the skinned Count with swaying cape - under quotes from the novel
(`BRAM STOKER`, "Listen to them...", "I am Dracula...", "For the dead travel fast."), then DRACULA / THE BORGO PASS and credits. Shown on a normal launch (no debug args); `--intro` forces, `--nointro` skips,
`--introshots=<dir>` saves frames for docs and quits. Any click / Space / Enter / Esc skips.
