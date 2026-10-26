# Audio prompts: animals, footsteps, ambiences, effects, music, voices

Everything is written to be pasted into a text-to-audio tool (sound-effect generators, music generators, TTS). Voices have
their own plan: `docs/VOICE_PLAN.md` (this file only adds the voice-design prompts, section 7). Creature list and ids:
`docs/ASSET_PROMPTS_CREATURES.md`.

## 0. Specs, tools, naming

| item | spec |
|---|---|
| format delivered to the game | Ogg Vorbis, `assets/audio/<id>.ogg`, entry in `data/audio.json` (`kind`: sfx / ambience / music, `loop`, `db`) |
| sfx | mono, 44.1 kHz source, 0.3 to 6 s, peak -3 dBFS, no silence at the start (trim to the first transient) |
| ambience | stereo, 45 to 90 s **seamless loop** (crossfade the ends 3 s), -23 LUFS, no single loud events that make the loop obvious |
| music | stereo, 90 to 180 s loop, -20 LUFS, no vocals, no fade-out at the end (loop point at a bar line) |
| creature vocals | mono, 3 to 5 variants per sound, pitched/trimmed by hand so no two are identical |
| voices | see the voice plan; mono, 24 kHz, -18 LUFS |
| naming | `snake_case` id exactly as in the tables; variants `_1 _2 _3`; the game picks a random variant |

Prompt style that works in most sound generators: **what + material + distance + environment + duration**, e.g.
`close microphone, single, dry, no music, no voice`. Always add: `no music, no speech, clean recording, realistic` for effects and
`no drums, no vocals, seamless loop` for ambience/music. Generate 4 candidates, pick one, trim, normalise.

Tools (check licence terms of each for commercial output before shipping): ElevenLabs Sound Effects (text to SFX, best quality, paid
credits), Stable Audio Open (open weights, music and effects up to 47 s, runs on a rented GPU or Colab, licence permits many uses
but read it), AudioGen / MusicGen (open weights, GPU), Suno / Udio (music, commercial rights depend on plan), Freesound.org
(filter **CC0**), Kenney / OpenGameArt (CC0 packs), Sonniss GDC game audio bundles (royalty-free). For the 10 hours of voice use the
voice plan. Post-processing is ffmpeg (loudnorm, trim, crossfade, encode): recipes in `docs/VOICE_PLAN.md` section 6.

## 1. Creature vocals

Each row = one sound id, number of variants to generate, and the prompt body. Paste with the suffix
`, close microphone, clean recording, no music, no background noise`. Duration in brackets.

### Wolves and dogs
| id | variants | prompt |
|---|---|---|
| wolf_howl | 4 | a single wolf howling at night, long rising and falling howl, distant forest, slight natural reverb, haunting (5 s) |
| wolf_howl_chorus | 2 | a pack of five wolves howling together at night across a valley, layered voices, long reverb (8 s) |
| wolf_growl | 3 | one wolf growling low and menacing, close, throat rumble, snarl at the end (2.5 s) |
| wolf_snarl | 3 | wolf snarling and snapping its teeth, aggressive, quick (1.5 s) |
| wolf_bark_yip | 2 | wolf short sharp bark-yip call, alert (0.8 s) |
| wolf_whimper | 2 | starving wolf whimpering softly, weak, pitiful (2 s) |
| wolf_alpha_roar | 3 | enormous wolf, very deep thunderous growl rising to a roar, chest resonance (3 s) |
| wolf_death | 2 | wolf yelp and dying whine, short (1.5 s) |
| wolf_pant_steps | 1 loop | wolf panting while trotting, close (6 s loop) |
| dog_bark_big | 3 | very large dog barking twice, deep booming bark, outdoors (2 s) |
| dog_growl_big | 2 | huge mastiff growling deep and slow, menacing (3 s) |
| dog_leap_snarl | 2 | big dog leaping and landing with a snarl (1.5 s) |
| dog_bark | 3 | medium dog barking three times, alert (2 s) |
| dog_small_bark | 2 | small terrier yapping excitedly (1.5 s) |
| dog_whine | 2 | dog whining at a door, anxious (2 s) |

### Horses and farm animals
| id | variants | prompt |
|---|---|---|
| horse_neigh | 3 | horse whinny, loud and clear, rising pitch, outdoors (2.5 s) |
| horse_neigh_panic | 3 | frightened horse screaming and rearing, shrill, panicked (2.5 s) |
| horse_snort | 3 | horse snort and blow through the nostrils, close (1 s) |
| horse_nicker | 2 | soft horse nicker, friendly (1.5 s) |
| horse_hooves_walk | 1 loop | one horse walking on cobblestones, hooves, steady rhythm (8 s loop) |
| horse_hooves_trot | 1 loop | horse trotting on a dirt road (8 s loop) |
| horse_hooves_gallop | 1 loop | horse galloping on grass, fast, powerful (8 s loop) |
| carriage_gallop | 1 loop | four horses pulling a carriage at speed on a stony mountain road, wheels rattling, harness jingling (10 s loop) |
| carriage_roll | 1 loop | horse-drawn carriage rolling slowly on cobbles, creaking wood and leather (10 s loop) |
| harness_jingle | 2 | horse harness bells and leather creak as the horse shakes its head (2 s) |
| horse_small_whinny | 2 | pony whinny, higher and lighter (1.5 s) |
| donkey_bray | 2 | donkey braying, hee-haw, loud (3 s) |
| cow_moo | 3 | cow mooing, deep, distant field (3 s) |
| ox_low | 2 | ox low bellow, very deep, heavy (3 s) |
| sheep_baa | 4 | a sheep bleating, outdoors (1.5 s) |
| flock_bleat | 1 loop | flock of sheep bleating, hills, wind (12 s loop) |
| goat_bleat | 3 | goat bleating, outdoors (1.5 s) |
| pig_grunt | 3 | pig grunting and snuffling (2 s) |
| chicken_cluck | 3 | hen clucking, farmyard (2 s) |
| rooster_crow | 2 | rooster crowing at dawn, distant (3 s) |
| goose_honk | 2 | goose honking, aggressive (2 s) |

### Small mammals
| id | variants | prompt |
|---|---|---|
| rat_squeak | 4 | one rat squeaking, sharp (0.8 s) |
| rat_chitter | 2 | rat chittering and hissing, close, dry (1.5 s) |
| rat_scuttle | 2 | rat claws scurrying on stone and wood, fast (3 s) |
| rat_swarm | 1 loop | dozens of rats squealing and scrabbling in a stone cellar, overwhelming, reverb (10 s loop) |
| mouse_squeak | 2 | mouse tiny squeaks (0.6 s) |
| cat_meow | 3 | cat meowing, indoors (1.2 s) |
| cat_hiss | 3 | cat hissing and spitting, angry (1.5 s) |
| cat_purr | 1 loop | cat purring, close (6 s loop) |
| fox_bark | 2 | red fox scream-bark at night, eerie (1.5 s) |
| deer_call | 2 | red deer stag bellow in a forest, autumn (3 s) |
| bear_growl | 2 | large bear growl, deep, chesty (3 s) |

### Birds and bats
| id | variants | prompt |
|---|---|---|
| gull_cry | 4 | seagull crying, harbour, distance 10 m (2 s) |
| gull_flock | 1 loop | many seagulls over a harbour, calls and wing noise (15 s loop) |
| raven_caw | 4 | raven croaking caw, outdoors, slightly echoing (1.5 s) |
| crow_caw | 3 | crow cawing, rural field (1.2 s) |
| crows_flock | 1 loop | rookery, many crows cawing in tall trees (15 s loop) |
| owl_hoot | 3 | tawny owl hooting, night forest, distant (2.5 s) |
| owl_screech | 2 | barn owl screech, eerie (1.5 s) |
| swallow_twitter | 2 | swallows twittering in flight (3 s) |
| songbird_nightingale | 1 loop | nightingale song in a quiet garden at dusk (20 s loop) |
| sparrow_chirp | 2 | house sparrows chirping on a roof (3 s) |
| pigeon_coo | 2 | pigeons cooing and wing clap (3 s) |
| hawk_cry | 2 | buzzard cry high above a valley (2.5 s) |
| bird_wings_flap | 3 | a large bird taking off, wing flaps, close (1.5 s) |
| bat_screech | 4 | single bat high-pitched squeak screech, slightly pitched down to be audible (1 s) |
| bat_wings | 3 | leathery wings fluttering rapidly past the listener, close (1.5 s) |
| bat_swarm | 1 loop | a cloud of many bats flapping and chittering overhead in a cave (12 s loop) |
| bat_giant_screech | 3 | huge bat shriek, low and unnatural, with a rasp, ominous (2 s) |
| bat_giant_wings | 2 | big heavy leather wingbeats, slow, powerful, flying away (3 s) |
| bat_tap_window | 2 | something tapping and scratching at a glass window pane at night, soft and insistent (3 s) |

### Insects and small things
| id | variants | prompt |
|---|---|---|
| fly_buzz | 2 | single housefly buzzing around a room, close (3 s) |
| flies_swarm | 1 loop | swarm of flies buzzing, claustrophobic (10 s loop) |
| moth_wings | 2 | large moth wings fluttering against a candle lantern glass, soft (2 s) |
| spider_skitter | 1 | tiny skittering legs on wood (1.5 s) |
| cricket_night | 1 loop | crickets at night, summer meadow (30 s loop) |

### Supernatural creature sounds
| id | variants | prompt |
|---|---|---|
| vampire_hiss | 4 | human-like vampire hissing, low throat hiss, inhuman, wet rasp (2 s) |
| vampire_growl | 3 | deep guttural growl, human and animal mixed, menacing (3 s) |
| vampire_scream | 3 | piercing inhuman shriek of rage, echoing in a stone hall (2.5 s) |
| vampire_laugh_sisters | 3 | three women laughing together, silvery, seductive and cruel, like glass bells, reverb (5 s) |
| vampire_whisper | 3 | breathy whisper in an unknown tongue, close to the ear, creepy (4 s) |
| vampire_dust | 2 | dry rustle of fine dust and ash falling and collapsing (2 s) |
| mist_whoosh | 2 | cold mist rushing in under a door, soft airy whoosh with a faint low moan (3 s) |
| count_transform_bat | 2 | a man's body cracking and fluttering into a swarm of bat wings, short, creepy (3 s) |
| count_transform_wolf | 2 | bones cracking and growling transformation into a large wolf (3 s) |
| undead_groan | 3 | undead female moaning, breathy, sorrowful and hungry (3 s) |
| ghost_wail | 2 | distant ghostly wail, woman, long reverb (5 s) |
| blue_flame_whisper | 2 | small cold blue flame flickering with a faint ghostly whisper (3 s) |

## 2. Footsteps and movement

Surfaces (for the player and NPCs; 6 variants each, 0.3 s per step, **one step per file**, a slightly different pitch each):
`step_stone`, `step_wood`, `step_grass`, `step_gravel`, `step_cobble`, `step_snow`, `step_sand`, `step_mud_wet`, `step_metal`,
`step_carpet`, `step_dirt`, `step_water_shallow`, `step_stairs_stone`, `step_stairs_wood`. Prompt body:
```
single footstep of a man in leather boots walking on <surface>, dry, close microphone, no echo, no other noise (0.3 s)
```
For women: "light leather shoes with a small heel". Gait sounds with a loop version: `walk_run_stone_loop` ("man in boots running on stone, 4 s loop").

Creature movement: `hooves_cobble`, `hooves_dirt`, `paws_snow`, `paws_leaves`, `claws_stone` (rat/wolf), `wings_gull`, `wings_raven`, `wings_bat`
(see section 1).

Clothing and gear: `cloth_rustle_coat` ("heavy wool coat rustling as someone turns, 1 s"), `cloak_flutter` ("large velvet cape flapping in the wind, 3 s"),
`cloak_sweep` ("cape swishing as a man turns sharply, 1 s"), `dress_rustle`, `gloves_leather`, `belt_buckle`, `chain_rattle`, `keys_jingle`,
`backpack_set_down`, `boots_on_ladder`.

## 3. Ambiences (seamless loops, stereo, 60 s)

Existing ids to replace or improve: `amb_asylum, amb_city, amb_crypt, amb_day, amb_fire, amb_interior, amb_sea, amb_snow, amb_storm, amb_wind`.
Prompt body: `<description>, seamless loop, no music, no voices, no sudden loud events, stereo, realistic field recording`.

| id | description |
|---|---|
| amb_day | quiet English countryside morning, light breeze, distant songbirds, a faint far-off dog, insects |
| amb_wind | cold mountain pass wind, low howling gusts, occasional faint rattle of loose stones, wide stereo, desolate |
| amb_snow | deep winter silence, soft snow wind, tiny ice ticks, distant muffled wolf howl once in a while |
| amb_storm | heavy thunderstorm over the sea, rain on cobbles, rolling thunder, wind gusts, shutters banging |
| amb_sea | harbour waves lapping against stone, creaking rope and wood, distant gulls, bell buoy clang far away |
| amb_city | Victorian London street, horse hooves on cobbles, distant voices, wheels, a hawker's cry far away, factory hum |
| amb_interior | quiet old room, clock ticking slowly, wood creaks, faint wind outside, a log settling |
| amb_fire | crackling fireplace with warm room tone, occasional pop, soft draught |
| amb_crypt | stone crypt, slow water drips with long reverb, distant low drone, tiny scuttles |
| amb_asylum | Victorian asylum corridor at night, distant muffled screams and weeping far away, keys, pipes ticking, a door slam far off |
| amb_forest_night | Carpathian pine forest at night, owls, branches creaking, wind in needles, far wolf howl, crickets near |
| amb_forest_day | woodland in daytime, many birds, leaves, a woodpecker, stream trickle |
| amb_village_day | village square, hens, a cart rolling, distant hammering, children far away, wind |
| amb_village_night | village at night, dogs barking far away, creaking shutters, quiet, wind in the eaves |
| amb_inn | busy inn evening, low murmur of voices, clinking tankards, fire, a fiddle tuning far away (no readable speech) |
| amb_church | stone church interior, huge reverb, a distant organ note, wood creak, pigeons in the rafters |
| amb_graveyard_night | graveyard at night, light wind, an owl, rustling yew branches, a distant church bell once |
| amb_harbour_day | Whitby harbour, gulls, boats knocking, ropes, water, voices very far |
| amb_harbour_night | harbour at night, waves, rigging clink, a foghorn far away, no gulls |
| amb_cliff_wind | clifftop with sea wind, waves far below, grass hiss, a gull now and then |
| amb_heath_night | Hampstead heath at night, cold wind, owls, a fox scream far away, grass |
| amb_garden_dusk | Hillingham garden at dusk, nightingale, crickets starting, a breeze in trees, a distant church bell |
| amb_castle_hall | huge empty stone hall, wind through high windows, distant echoing drip, torch flutter |
| amb_castle_wind | wind howling through broken battlements, a loose shutter, ravens far away |
| amb_dungeon | dungeon, slow drips, distant chain clink, rats scuttling, low rumble |
| amb_cellar_rats | cellar full of rats, constant scratching and squeaking, drips |
| amb_library | quiet library, clock tick, paper rustle, faint wind, leather chair creak |
| amb_bedroom_night | bedroom at night, soft wind at the window, a clock far away, a floorboard, a faint bat flutter outside |
| amb_ship_hold | ship's hold in a storm, heavy timber creaking, water sloshing, rope strain, muffled waves |
| amb_ship_deck | sailing ship at sea, wind in sails, creaking rigging, waves, flapping canvas |
| amb_river_rapids | roaring river rapids, constant water, birds none |
| amb_carriage_road | rattling carriage and horses at a steady trot (use `carriage_roll` plus wind) |
| amb_zoo | London zoo evening, distant animal calls (lion, monkey, wolf howl), footsteps on gravel, murmur |
| amb_train_station | steam train station, hiss, whistle far off, murmur, iron clatter |
| amb_hotel_lobby | quiet Victorian hotel lobby, clock, soft steps on carpet, murmurs, a bell |
| amb_snow_night | snowy night, light wind, silence, sparse far howl |
| amb_rain_roof | rain on a slate roof and window, close, steady |
| amb_fog_still | thick fog, near silence, a very faint far foghorn, drips |
| amb_dawn | dawn chorus, many birds, a fresh breeze, a rooster far away |

## 4. Sound effects

Existing ids to improve: `sfx_bat, sfx_bell, sfx_bite, sfx_card, sfx_click, sfx_craft, sfx_defeat, sfx_door, sfx_door_locked, sfx_flame, sfx_heartbeat, sfx_hit, sfx_holy, sfx_howl, sfx_hurt, sfx_levelup, sfx_miss, sfx_page, sfx_pickup, sfx_repel, sfx_step, sfx_victory`.
Prompt body: `<description>, clean recording, no music, no voice`.

| id | description (duration) |
|---|---|
| sfx_click | soft wooden UI tap, subtle (0.15 s) |
| sfx_page | old paper page turn, dry rustle (0.7 s) |
| sfx_card | heavy parchment slap onto a table with a low thud (0.6 s) |
| sfx_pickup | small metal and cloth item picked up, short bright clink (0.4 s) |
| sfx_craft | hands crafting at a table, wood and metal tools, short sequence (2 s) |
| sfx_door | heavy oak door opening with a slow creak and latch (1.8 s) |
| sfx_door_close | heavy oak door closing with a thud and latch click (1 s) |
| sfx_door_locked | locked door rattling, handle tried twice, iron latch (1.2 s) |
| sfx_door_iron | rusty iron gate opening, long screech, chain (2.5 s) |
| sfx_door_crypt | heavy stone slab door sliding, grinding, dust, echo (3 s) |
| sfx_key_turn | large iron key turning in an old lock, heavy clunk (1 s) |
| sfx_lock_picklock | small metal pick scratching in a lock (1.5 s) |
| sfx_latch_window | wooden window shutter opened and latched (1 s) |
| sfx_stairs_creak | old wooden stairs creaking under weight (1 s) |
| sfx_drawer | old wooden drawer sliding open (0.8 s) |
| sfx_chest_open | heavy wooden chest lid with iron hinge creak and thump (1.5 s) |
| sfx_coffin_lid | heavy wooden coffin lid sliding open on stone, scrape and thud (2.5 s) |
| sfx_earth_shovel | shovel digging into soil, gravel scrape (1.5 s) |
| sfx_stone_move | heavy stone being dragged, rumble (3 s) |
| sfx_glass_break | window glass shattering, shards falling (1.5 s) |
| sfx_mirror_crack | mirror cracking with a sharp tinkle (1.2 s) |
| sfx_bell | single tolling church bell, deep, long decay (6 s) |
| sfx_bell_midnight | church clock striking twelve times, slow, far (30 s) |
| sfx_clock_chime | grandfather clock chime and tick (4 s) |
| sfx_phonograph | wax-cylinder phonograph crackle and a thin scratchy hum, no melody (4 s) |
| sfx_piano_note | a single distant piano note in an empty room (3 s) |
| sfx_organ_chord | slow church organ chord, minor, long reverb (6 s) |
| sfx_candle_light | match strike and candle flame ignite (1.2 s) |
| sfx_candle_out | candle snuffed out, breath puff (0.8 s) |
| sfx_flame | torch flame whoosh and flutter (2 s) |
| sfx_fire_burst | sudden burst of flame, roaring (1.5 s) |
| sfx_lantern_swing | iron lantern swinging, chain squeak (1.5 s) |
| sfx_water_pour | pouring water into a basin (2 s) |
| sfx_drink | gulping a drink from a goblet (1.5 s) |
| sfx_wine_bottle | cork pulled and wine poured into a glass (2.5 s) |
| sfx_eat | someone eating bread, chewing, close (2 s) |
| sfx_writing | quill scratching on paper (3 s) |
| sfx_letter_seal | wax seal pressed on a letter (1 s) |
| sfx_typewriter | Victorian typewriter, short clatter and bell (2 s) |
| sfx_boat_oars | rowing boat oars creaking and splashing (4 s loop) |
| sfx_ship_creak | big wooden ship hull creaking under strain (4 s) |
| sfx_ship_bell | ship's bell, two strikes (3 s) |
| sfx_foghorn | far low foghorn, long (5 s) |
| sfx_wave_crash | wave crashing against harbour stone with spray (3 s) |
| sfx_thunder | rolling thunder, very long, sub bass (8 s) |
| sfx_thunder_close | sudden close thunderclap crack with boom (4 s) |
| sfx_rain_start | rain starting on stones, 5 s fade in (6 s) |
| sfx_wind_gust | single wind gust through trees, whoosh (3 s) |
| sfx_howl | one wolf howl, far (5 s) |
| sfx_bat | bat flutter and squeak passing close (2 s) |
| sfx_bite | vampire bite: skin puncture, wet, quiet, intimate, a sharp breath (1.5 s) |
| sfx_drink_blood | wet drinking, low swallowing, unsettling (3 s) |
| sfx_heartbeat | slow deep heartbeat, loopable, 60 bpm (6 s loop) |
| sfx_heartbeat_fast | fast heartbeat with breathing, panic (6 s loop) |
| sfx_breath_cold | long cold breath in a crypt (2 s) |
| sfx_holy | holy light: bright shimmering chime with a choir swell, short (2.5 s) |
| sfx_repel | an unseen force repelling a creature: hiss, pressure wave, low thump (1.8 s) |
| sfx_crucifix_glow | warm shimmering tone as a crucifix is raised (2 s) |
| sfx_host_crumble | communion wafer crushed to dust in the hand, soft crumbling (1 s) |
| sfx_garlic | garlic bulbs rustle in a bundle (1 s) |
| sfx_stake_drive | wooden stake driven into a chest with a mallet, dull crunch and thud (1.5 s) |
| sfx_hammer | iron hammer on wood, one heavy hit (0.8 s) |
| sfx_hit | fist or club hit on body, dull thump (0.5 s) |
| sfx_hit_blade | knife slash through cloth and flesh, short whoosh (0.6 s) |
| sfx_hit_heavy | heavy blow, crunch (0.7 s) |
| sfx_miss | whoosh of a swing missing (0.5 s) |
| sfx_block | forearm blocking a blow, dull thud (0.4 s) |
| sfx_gun_revolver | Victorian revolver shot outdoors, echo (2 s) |
| sfx_rifle | lever-action rifle shot, outdoors, echo (2.5 s) |
| sfx_reload | revolver reload, clicks (2.5 s) |
| sfx_knife_draw | Bowie knife drawn from a sheath (0.8 s) |
| sfx_sword_clash | two blades clashing (1 s) |
| sfx_hurt | short male pain grunt (0.6 s) x3 variants |
| sfx_hurt_f | short female pain gasp (0.6 s) x3 |
| sfx_defeat | low descending drone and a heavy thud, defeat sting (3 s) |
| sfx_victory | short triumphant minor-to-major string sting (3 s) |
| sfx_levelup | rising bright chime arpeggio, short (1.5 s) |
| sfx_journal_add | quill and page rustle with a soft chime (1.5 s) |
| sfx_unlock | satisfying heavy mechanical unlock (1.5 s) |
| sfx_secret | subtle low rumble and mystery chime when a secret opens (2.5 s) |
| sfx_jumpscare | very short sharp orchestral stab with a crash, loud (1.2 s), use rarely |
| sfx_whisper_bed | continuous layered whispers behind the listener, unintelligible, loop (10 s loop) |
| sfx_ritual | low chanting drone with bells (8 s) |
| sfx_cart_wheel | cart wheel creaking and rolling on stone (4 s loop) |
| sfx_gate_wood | wooden garden gate opening, hinge squeak (1.5 s) |
| sfx_splash | man falling into harbour water (2 s) |
| sfx_climb_wall | hands and boots scrabbling up a stone wall, gravel falling (3 s) |
| sfx_fall_thud | body falling onto stone (1 s) |

## 5. Music

Prompt body for music generators: **genre/mood + instruments + tempo + key/mode + structure + "no vocals" + "seamless loop"**.
Existing ids: `mus_title, mus_explore, mus_dread, mus_combat, mus_sad`.

| id | length | prompt |
|---|---|---|
| mus_title | 120 s | gothic horror main theme, solo cello and low string pad, sparse harp, a distant church bell, slow 50 bpm, D minor, builds slowly to a full dark string chord, cinematic, no vocals, loopable |
| mus_menu_credits | 120 s | quiet melancholy piano and string quartet, slow 60 bpm, reflective, bittersweet, no vocals |
| mus_explore | 150 s | atmospheric ambient underscore, low drones, soft tremolo strings, occasional glass harmonics, slow, uneasy but calm, A minor, loopable |
| mus_explore_countryside | 150 s | gentle English pastoral underscore, solo violin and acoustic guitar, hopeful but with a shadow, 70 bpm |
| mus_explore_castle | 150 s | oppressive Gothic castle ambience, deep organ drone, distant bells, dissonant string swells, 40 bpm |
| mus_explore_harbour | 150 s | windswept harbour theme, accordion and low strings, sea shanty feeling, minor key, slow |
| mus_explore_london | 150 s | Victorian London night, muted brass, pizzicato strings, harpsichord, fog and gaslight, 80 bpm |
| mus_explore_forest | 150 s | dark Carpathian forest, sparse cimbalom (hammered dulcimer), low drones, wind-like strings, 50 bpm |
| mus_explore_asylum | 150 s | unsettling asylum, detuned music-box, whispers of strings, sparse piano clusters, no rhythm |
| mus_szgany_dance | 90 s | Romani fiddle and cimbalom, fast wild 140 bpm minor dance, vigorous, a little menacing |
| mus_dread | 120 s | rising horror tension underscore, low string tremolo, sub bass pulse, distant metallic scrapes, no melody, loopable |
| mus_stalk | 90 s | slow stalking tension, double bass notes and heartbeat-like timpani, dissonant violin sul ponticello |
| mus_combat | 120 s | driving gothic action: low pounding drums, staccato strings, brass stabs, 130 bpm, D minor, loopable, no vocals |
| mus_combat_boss | 150 s | epic dark boss battle, choir-less orchestral, heavy brass, organ, timpani, 140 bpm, relentless |
| mus_chase | 90 s | frantic chase, galloping strings, snare, brass hits, 160 bpm |
| mus_sad | 120 s | grief theme, solo violin with piano, slow 55 bpm, A minor, heartfelt, no vocals |
| mus_lucy | 120 s | tender doomed beauty, celesta and strings, waltz in 3/4, fading, fragile |
| mus_hope_dawn | 120 s | hopeful dawn, warm strings and horns, rising major theme, 70 bpm |
| mus_victory | 30 s | short triumphant yet weary resolution, strings and horn, ends cleanly (not a loop) |
| mus_defeat | 30 s | grim descending brass and strings, ends on a low chord (not a loop) |
| mus_dracula_theme | 120 s | the Count's theme, slow minor organ and low cellos with a seductive solo violin, 45 bpm, elegant and cold |
| mus_brides | 90 s | three sopranos humming a seductive lullaby with glass harmonica, high and eerie, no words, 60 bpm |
| mus_church | 120 s | solemn organ and choir pads, sacred but uneasy, slow |
| mus_stinger_reveal | 6 s | short dramatic orchestral sting for a revelation, ending on a held low note |
| mus_stinger_death | 6 s | short sombre sting for a death |
| mus_stinger_discovery | 5 s | short mysterious rising sting for a discovery |
| mus_end | 120 s | ending theme, the main theme resolved to a gentle major, strings and piano, fading out |

## 6. Mixing notes for the game

* Buses: `Music` (-14 dB), `Ambience` (-18 dB), `SFX` (-10 dB), `Voice` (-8 dB). Music ducks -8 dB under voice; ambience ducks -4 dB.
* Distance: animals and footsteps play as 3D sounds (`AudioStreamPlayer3D`, attenuation inverse, max distance 25 m); narrator, inner monologue and letters are 2D.
* Variation: pick randomly among `_1.._n`; pitch random 0.95 to 1.05; never repeat the last variant.
* Weather layers: ambience loops can be stacked (`amb_forest_night` + `amb_wind`); keep two layers at most.
* Footstep surface is chosen from the floor texture role (stone_blocks -> `step_stone`, wood_planks -> `step_wood`, grass, cobble, dirt, snow, gravel).

## 7. Voice-design prompts (for ElevenLabs Voice Design, Parler-TTS, or to choose a stock voice)

The full plan, tagging and post-processing: `docs/VOICE_PLAN.md`. Each prompt describes the voice only; send the sample lines to audition.

| id | voice design prompt | audition lines |
|---|---|---|
| narrator | A warm, authoritative male British narrator in his fifties, rich baritone with a slight huskiness, calm literary delivery, unhurried, lowered intimate tone for dread, like a Victorian ghost-story reader | "3 May. Bistritz. Left Munich at 8:35 P.M. on the 1st of May, arriving at Vienna early next morning." / "The sun had set, and the valley below was already drowned in shadow." |
| harker | A young English man in his twenties, educated middle-class accent, earnest, slightly nervous, clear tenor, breaks a little under fear | "I did not sleep well, though my bed was comfortable." / "There is something wrong with this place. I must be careful." |
| dracula | An old aristocratic man with a refined Eastern European accent, low and soft, slow and precise, courteous and chilling, very little breath, never shouts, every word weighed | "I am Dracula; and I bid you welcome, Mr. Harker, to my house." / "Listen to them, the children of the night. What music they make!" |
| mina | A young English woman in her twenties, clear gentle alto, intelligent, warm, steady under stress | "I have been thinking, Jonathan, that we must write everything down." |
| lucy | A bright young English woman of nineteen, light playful soprano, laughs easily; for the undead version breathy, sweet and cruel | "Oh, Mina, I am so happy I could cry!" / (undead) "Come to me, Arthur, my husband. Leave these others, and come to me." |
| vanhelsing | An older Dutch man in his sixties, warm deep voice, formal English with a Dutch accent, emphatic and kind, a little theatrical | "Ach, my friend, you must not doubt what you cannot yet understand." |
| seward | A tired English doctor in his thirties, calm measured baritone, quiet clinical, sorrow underneath | "I have never seen a case like it. The patient is perfectly lucid, and perfectly mad." |
| quincey | A friendly American Texan man in his thirties, easy drawl, humorous, relaxed warm baritone | "Well, I reckon we have a job of work ahead of us, gentlemen." |
| arthur | A young English aristocrat in his late twenties, warm light baritone, upper-class accent, emotional and sincere | "Whatever it costs, Seward, I will do it for her." |
| renfield | A man in his fifties, thin voice that swings between servile whining, cunning whisper and manic excitement, sing-song cadence, erratic pace | "Master, I am here to do your bidding! I shall be good, I shall be very good." |
| brides (3) | Three young women's voices, silvery and breathy, seductive and cruel, one giggling, one low, one sweet; reverb as in a stone hall | "He is young and strong; there are kisses for us all." |
| coachman | A hollow, quiet male voice, tall man, no emotion, a faint rasp, polite, sinister | "The night is cold, sir, and the road is long." |
| captain | A rough British sea captain, fifties, gravelly, commanding, weather-beaten | "Hold her steady, lads! We ride out the storm or we die!" |
| innkeeper / peasant men | Weathered rural men, 40 to 70, warm or gruff, regional accents (Transylvanian-accented English; northern English for Whitby) | "Do not go, sir. It is the eve of St George's Day, when the evil things have full sway." |
| peasant women | Women 30 to 70, warm, anxious or sharp, regional accents | "Must you go? Do you know what day it is?" |
| child | A small child's voice, 7 years old, frightened | "The bad lady took the little boy." |

## 8. Priority order

1. Creature vocals for the existing encounters: `wolf_howl, wolf_growl, wolf_snarl, bat_screech, rat_squeak, horse_neigh, dog_bark_big` and the footsteps `step_stone/wood/grass/cobble`.
2. Ambiences for every location type (`amb_forest_night, amb_castle_hall, amb_harbour_day/night, amb_village_*, amb_church, amb_graveyard_night`), then the rest.
3. SFX not yet in the game: door variants, coffin lid, key, thunder, boat, gunshots, blades, crucifix/host/garlic.
4. Music: one explore theme per region plus combat boss, chase, Dracula theme, stingers.
5. Remaining creature vocals (farm animals, birds, insects), footsteps for the remaining surfaces, extra stingers.
6. Voices follow `docs/VOICE_PLAN.md`.

Checklist per file: trimmed, no clipping, loudness matches its kind, loops without a click (check by repeating twice), id as file name, entry in `data/audio.json`, licence recorded in `ai/SOURCES.md`.
