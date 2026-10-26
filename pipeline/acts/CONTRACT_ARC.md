# Personal arc authoring contract (addendum to CONTRACT.md)

You write ONE personal arc: an optional, self-contained side story the player plays as one character, launched from the Chronicle menu
(key M or title screen). READ `pipeline/acts/CONTRACT.md` FIRST - everything there (rooms, props, dialogue, conditions, do-verbs, combat,
validator mindset, quality bar, new assets) applies - then this file for the differences, then `pipeline/acts/example_arc.py` (working example).
The main game is already complete (Acts I-VI: `pipeline/bible_src.py` Act I and `pipeline/acts/act_2..6.py`); skim the act that introduces your
character so your arc fits the canon, tone and rooms style, but your arc must not depend on main-game state.

## Differences
* File: `pipeline/acts/arc_<id>.py` (+ optional `arc_<id>_builders.py`). Prefix ALL your ids (locations, props, npcs, dialogues, items, journal,
  flags, encounters, assets) with `<id>_` (e.g. `harker_road_`). Variables: `ARC` (not ACT) + the same LOCATIONS/LOC_DATA/DIALOGUE/ITEMS/JOURNAL/
  PLACEMENTS/GATES/PALETTES/ENCOUNTERS_EXTRA/ENEMIES_EXTRA/ENCOUNTER_HOOKS/RECIPES_EXTRA/ASSETS/VARIANTS as acts.
* ARC = dict(id, title, member (the playable character id), portrait (portrait file id in assets/portraits, default = member), blurb (1-2 sentences),
  unlock (condition on the MAIN game: `roster:<id>`, `has:`, `flag:`, `journal:`, `party:`, `meta:game_complete` ... joined by &),
  unlock_text (what the player is told while locked), after_credits (True = additionally needs the main story finished once),
  start=dict(location, protagonist, party, items, flags), exit_to="ARC_END", rewards=[do-list applied to the MAIN game when the arc ends],
  rewards_text (what the player earns, shown on the end card and as tooltip)).
* The arc runs in an ISOLATED game state built from ARC["start"] (fresh flags, inventory, party). Nothing from the main game is visible and nothing
  you give/set inside the arc survives, except: arc journal entries are merged into the main journal, and the `rewards` list is executed on the main game.
* Rewards: use `{"give": item, ...}` (new items you define in ITEMS, or system items: host, brandy, bullet, winchester, kukri, stake, garlic, silver, chloral,
  holy_water ...), `{"stat": {"member": id, "hp": n, "nerve": n, "acc": n, "eva": n, "faith": n, "dmg": n}}` (permanent bonuses; keep modest: hp 1-4,
  nerve 1-5, acc/eva 1-4, faith 1-2, dmg 1; one or two stat entries), `{"set": flag}` (main flag; the known ones that unlock content: `rites` unlocks the
  holy-water / sacred-bullet / consecrated-knife recipes, `medicine` unlocks the chloral recipe), `{"meet": id}`. Make the reward feel earned and themed.
* The arc ENDS with a dialogue/interaction whose do-list contains `{"arc_end": 1}` (before it you may show `{"card": "..."}` epilogue text; card and arc_end
  may be in the same do list: cards show first). Use `ARC["exit_to"] = "ARC_END"`; the validator succeeds when `arc_end` is reachable.
* Playable-only characters exist as protagonists: `lucy`, `renfield`, `dracula` (the young Voivode), `captain` (Captain of the Demeter), plus
  harker mina vanhelsing seward quincey arthur. `ARC.start.party` decides who fights (a single character is fine; combat stats in data/systems.json).
* Validate: `python3 pipeline/validate_story.py --arc <id> --seed-options`; real-engine replay: `./run_arc_replays.sh <id>` (must print PASS).
  New models: `pipeline/build_arc_assets.sh <id>` (not build_act_assets.sh). Never run the other acts' scripts or edit other files.
* Scale (minimum): 5+ locations, 12+ dialogues, 5+ real puzzles/chains, 8+ items, 10+ journal entries (diary voice, <= 70 words),
  an optional or central fight where fitting (use existing encounters/enemies or ENCOUNTERS_EXTRA with hooks), a real emotional/story payoff.
  Richer is welcome. Beyond-the-book material is encouraged for backstory, but stay in the novel's world, era and tone (Victorian, gothic, 1890s).
* Include seed variation (PALETTES / PLACEMENTS / GATES) where natural; `--seed-options` must pass.
* Hand-back: files, counts, last validator line, last replay line, the unlock condition and the rewards.
