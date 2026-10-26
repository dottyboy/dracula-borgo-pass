# Roadmap: what we work through, in order

Each tier ends with something playable or releasable. Do them top to bottom; tracks B and C can be interleaved
between voice tiers when a long render is running. Audio hours = characters / 15 per second (`voice/summary.json`).

## Track A - Voice (details: `docs/VOICE_PLAN.md`)

| tier | content | lines | audio | done when |
|---|---|---|---|---|
| **V0 foundation** | cast list + voice auditions, tag tool, TTS scripts, `Voice` autoload with 3 demo lines | - | - | a sample line per character plays in the game in the right voice, subtitles and talk animation in sync |
| **V1 main cast dialogue** | Mina, Van Helsing, Seward, Lucy, Harker, Quincey, Renfield, Arthur, Dracula (dialogue nodes only) | 740 | 2.2 h | every story conversation with a main character is voiced |
| **V2 minor speakers + story cards** | 192 minor speakers on the pools (peasants, captain, coachman, brides ...) + 52 cards read by the narrator | 835 | 2.4 h | all dialogue in the game has a voice; cards narrated |
| **V3 narrator: places** | place descriptions read on arrival (168), nothing else from the narrator yet | 168 | 0.3 h | entering a location is announced; narrator on/off in Esc menu |
| **V4 journal + player replies** | journal entries read when added (428), player's spoken choices (1 037) | 1 465 | 2.3 h | journal and replies voiced; protagonist inner-monologue effect in place |
| **V5 look texts + items** | examine texts (1 983) and item descriptions (228), voiced on first examine only | 2 211 | 3.2 h | optional; skip anything that sounds repetitive |
| **V6 polish** | pronunciation list, breaths and tails, loudness pass, mix/ducking, release asset packaging | - | - | audio shipped as a release asset |

Inside each tier the order is the story order (acts I to VI), so the opening is always finished first.
Per tier: tag (LLM) -> review 5 % -> render -> post -> index -> listen to 10 random lines per character -> commit index.

## Track B - Characters (models)

| tier | work | done when |
|---|---|---|
| **C0** | old Dracula is **regenerated without a cape** (prompt `DraculaOld_nocape`), then rigged with `pipeline/mixamo/rig_ai.py` (drop the slow weight smoothing step; the previous cape model is retired); cape comes from the separate cape model/cloth | new old Dracula walks and talks in game; replays pass |
| **C1** | same pipeline for young Dracula, vampire form and fog form from `ai portraits/` (one script call each); variant mapping `sk_<model>_<variant>.glb` in `MixamoRig.config_for` | all Dracula variants skinned |
| **C2** | more AI portraits for the other main cast (Van Helsing, Mina, Lucy, Harker ...) through the same path; fall back to the dressed bots where missing | every main character has a face that matches the portraits |
| **C3** | dressed-bot polish: faces, hair shapes, softer skirts, shoulders, sleeves; remaining generic NPC looks | no visible mannequin joints or floating limbs |
| **C5** | quadruped, bird and rat rigs for AI animals (generic quad rig in Blender, `rig_quad.py`), replace the rat enemy that currently uses the bat model | wolves, horses, rats, ravens animated from AI models |
| **C4** | animation extras: sitting/ladder/climb/lying poses wired to props, shout/whisper gestures driven by voice energy | voice-driven gestures in dialogue |

Licence check before any AI-made model enters the public repository or a release (tool terms for output).

## Track C - Game and release polish

| tier | work |
|---|---|
| **G0** | known art issues: harbour water edge colour, night variants inside regions, London map label overlap, manor stone too bright |
| **G1** | real play-through (mouse): pie menu, map, regions, action mode; fix whatever feels wrong |
| **G2** | Esc menu: voice volume, narrator on/off, Mixamo characters on/off, intro skip |
| **G3** | release v0.3.0 after V1 (first voiced build), v0.4.0 after V2, then one release per later tier; README gallery refreshed each time |
| **G4** | accessibility and languages: subtitles size, text speed; Croatian text pass if wanted |

## Suggested start

1. C0 (finish old Dracula, short and unblocks C1).
2. V0 (cast and tooling) - the longest preparation, everything else is mechanical after it.
3. V1 with the first act, then continue act by act.
4. After each tier: G3 release.

## Track D - Sound (details: `docs/AUDIO_PROMPTS.md`, creatures `docs/ASSET_PROMPTS_CREATURES.md`)

| tier | content | done when |
|---|---|---|
| **S1** | creature vocals for existing encounters (wolf, bat, rat, horse, dog) + footsteps for stone, wood, grass, cobble | encounters and walking sound right |
| **S2** | ambiences for every location type (about 40 loops) | no silent location |
| **S3** | missing SFX: doors, coffin, key, thunder, boats, weapons, holy items | every interaction has a sound |
| **S4** | music: one explore theme per region, boss, chase, Dracula theme, stingers | each act has its own score |
| **S5** | remaining animal sounds (farm, birds, insects), extra surfaces and stingers | polish |

## Track E - AI asset production (details: `docs/ASSET_PROMPTS.md`, `docs/ASSET_PROMPTS_CAST.md`, `docs/ASSET_PROMPTS_CREATURES.md`)

Order: Dracula (no cape) + capes, main cast, generic roles, creatures, props by frequency, textures (stone, cobble, planks, plaster first), skies, decals, NPC variants.
