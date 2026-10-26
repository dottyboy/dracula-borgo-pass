# Voice-over plan: narrator + a voice per character

Goal: every spoken line of the game gets audio (narrator, one distinct voice per character, emotions: normal, whisper,
inner monologue, shouting/calling, ...), made with free or cheap tools, assembled automatically, played in sync with the
existing subtitles and talk animations. This file is written so that sections can be pasted into other tools (LLM,
TTS web UIs, ffmpeg).

## 1. What there is to voice (generated: `python3 pipeline/voice/extract_script.py` -> `voice/script.jsonl`)

| kind | lines | characters | audio at ~15 chars/s |
|---|---|---|---|
| dialogue (NPC and protagonist nodes) | 1 524 | 234 k | 4.3 h |
| player choices (spoken replies, not `[stage directions]`) | 1 037 | 38 k | 0.7 h |
| narration (look texts, pickup texts, place descriptions) | 2 151 | 174 k | 3.2 h |
| journal entries | 428 | 88 k | 1.6 h |
| story cards | 52 | 9 k | 0.2 h |
| item descriptions | 228 | 17 k | 0.3 h |
| **total** | **5 420** | **560 k** | **about 10 h** |

By speaker (characters, after merging aliases such as Mina / Mina Harker / Mina Murray): narrator 288 k, Mina 26 k,
Van Helsing 23 k, Seward 20 k, Lucy 11 k, Harker 10 k, Quincey 9 k, Renfield 8 k, Arthur 7 k, Dracula 3 k, plus
**192 minor speakers (155 k chars)** that map onto the voice pools below (by the NPC model that starts the dialogue).

Ten hours is a lot. Do it in tiers; each tier is shippable on its own:

1. **Tier 1 - dialogue + cards** (4.5 h): the main cast and minor speakers. This is what players notice most.
2. **Tier 2 - narrator for place descriptions and first-time look texts** (about 1.5 h, filter by `source` starting `locdesc:`).
3. **Tier 3 - journal entries** (1.6 h, read when the journal entry is added) and player replies (0.7 h).
4. **Tier 4 - everything else** (items, repeat look texts): optional, or leave as text.

## 2. Line data model

Every line in `voice/script.jsonl` (one JSON object per line):

```json
{"id": "b31f2fccf9", "source": "dialogue:a1_vault_stairs:n0", "kind": "dialogue", "speaker": "Jonathan Harker",
 "character": "harker", "text": "...", "emotion": "", "delivery": "", "dialogue": "a1_vault_stairs",
 "npc_model": "human_peasant_m", "npc_variant": "innkeeper"}
```

* `id` = sha1 of the source path, stable across rebuilds; the audio file is named after it.
* `character` = canonical id (`mina`, `vanhelsing`, `seward`, `lucy`, `harker`, `quincey`, `renfield`, `arthur`, `dracula`,
  `narrator`) or `npc:<name>` for minor speakers.
* `emotion` and `delivery` are filled by the tagging pass (section 4). Everything else is extracted.

Important: many "dialogue" nodes whose speaker is the protagonist are **inner monologue / narration** ("A narrow stair
goes down beneath the chapel ... in my hand"). The tagger decides: `delivery = inner` (monologue, voiced by the protagonist
with the inner-voice effect) or `narration` (narrator).

## 3. Cast: voice per character

Voice descriptions (paste into a voice-design field, or use them to pick a stock voice). British / period accents unless noted.

| id | role | voice brief |
|---|---|---|
| narrator | storyteller, journals | warm male baritone, 50s, measured and literary British, slight huskiness, good at hushed dread; never theatrical |
| harker | Jonathan Harker | young English man, 20s, educated, earnest, nervous under stress; the protagonist - inner monologue is also his voice |
| dracula | Count Dracula | old, tall, aristocratic Eastern European accent, low and courteous, slow, cold; whispers are very quiet and close, no growling |
| mina | Mina Murray / Harker | young English woman, 20s, clear, intelligent, gentle but firm |
| lucy | Lucy Westenra | young English woman, 20s, bright and playful; later (undead) breathy, sweet and cruel |
| vanhelsing | Professor Van Helsing | older Dutch man, 60s, kind, formal, odd English syntax, emphatic, occasional "Ach" |
| seward | Dr. John Seward | English man, 30s, calm clinical, tired, reflective |
| quincey | Quincey Morris | American (Texan) man, 30s, easy drawl, humorous, brave |
| arthur | Arthur Holmwood, Lord Godalming | young English aristocrat, 20s-30s, warm, upper-class, emotional |
| renfield | R. M. Renfield | man in 50s, switches between servile, cunning and manic; sing-song, erratic pacing |
| brides | the three sisters | three light, silvery, seductive women's voices, laughing, slightly reverberant |

Minor-speaker pools (assign each of the 192 minor speakers to one pool by `npc_model`, rotate within the pool so neighbours
differ; keep a speaker always on the same pool voice):

| pool | models | lines (chars) | brief |
|---|---|---|---|
| peasant_m (3 voices) | human_peasant_m | 60 k | weathered men, rural English/dialect-flavoured; Transylvanian ones lightly accented; Whitby locals northern English |
| peasant_f (2 voices) | human_peasant_f | 29 k | older and younger women, warm or sharp |
| captain / sailor (1) | human_captain | 3 k | gruff, commanding |
| coachman (1) | human_coachman | 2.5 k | hollow, whispery (he is Dracula in disguise) |
| gentry (use the matching main voice) | human_seward / arthur / quincey / vanhelsing / harker / mina / lucy | about 28 k | same voice as the main character with that model |
| unknown (30 k) | speakers whose NPC could not be found | | decide by hand from the name / sex; the file `voice/cast.csv` (section 7) lists them |

## 4. Emotion and delivery tagging (before TTS)

Two fields per line:

* `delivery`: `normal`, `whisper`, `inner` (inner monologue), `shout` (calling out, distant, raised voice), `narration`, `letter` (journal/diary read aloud).
* `emotion`: free tag from a fixed list: `neutral, calm, warm, cheerful, amused, curious, worried, afraid, terrified, angry,
  contempt, sad, grieving, pleading, urgent, tender, menacing, seductive, manic, determined, weary`.

### 4.1 Cheap automatic first pass (rules)

`!` and ALL CAPS -> shout; `...` / trailing dash -> hesitant; text wholly in `*asterisks*` or `(parentheses)` -> inner;
`kind in (journal, card)` -> letter/narration; words like whisper, murmur, softly in the preceding node -> whisper.
(The tagger below overrides these.)

### 4.2 LLM tagging prompt (copy-paste, run in batches of 40 lines)

```
You are the voice director for an audio drama of Bram Stoker's Dracula (1897). For each line below choose:
  delivery: one of normal | whisper | inner | shout | narration | letter
  emotion: one of neutral calm warm cheerful amused curious worried afraid terrified angry contempt sad grieving pleading
           urgent tender menacing seductive manic determined weary
  pace: slow | normal | fast        energy: 0..3 (0 = barely audible, 3 = loud)
Rules: lines spoken by the protagonist that describe what he sees or thinks (first person narration of surroundings) are
"inner". Journal and diary text is "letter". Place descriptions are "narration". Shouting only when the situation clearly
calls for it (calling across distance, panic, command). Be sparing: most lines are normal/neutral or calm.
Return ONLY a JSON array: [{"id": "...", "delivery": "...", "emotion": "...", "pace": "...", "energy": 1}, ...]
Lines (JSON): <paste a slice of voice/script.jsonl here, keep id, character, kind, text and the previous 2 lines for context>
```

Merge the answers back by `id` (a short script, section 7). Spot-check 5 % by ear.

## 5. Generating the audio (tool options)

This machine has no useful GPU, so prefer CPU-friendly or hosted tools. Licences matter for a public release: check
that the voice/model terms allow commercial use and redistribution of output.

| tool | where | emotion control | cost / notes |
|---|---|---|---|
| **Kokoro-82M** | local CPU (fast), many voices (British and American) | style by voice choice + speed, no explicit emotion | free, Apache-2.0; best free baseline for 10 h of text |
| **Piper** | local CPU, hundreds of voices incl. British | none (post-process only) | free, MIT; fast, flat |
| **Azure Neural TTS** | hosted | SSML `style`: whispering, shouting, terrified, sad, angry, cheerful ... plus rate/pitch/volume | free tier 0.5 M chars/month (560 k fits in about two months or one paid month) |
| **ElevenLabs** | hosted | best natural emotion, voice design from a text brief | paid; use for the hero voices only (Dracula, narrator, Van Helsing) |
| **Google Cloud TTS (Chirp3 / Neural2)** | hosted | limited SSML | free tier 1 M chars/month for standard voices |
| XTTS / F5-TTS / Parler-TTS | local, needs a GPU | prompt-based emotion | not realistic here; usable on a rented GPU or Colab |

Recommended: **Kokoro (or Piper) for everything first**, one voice per character from the briefs, then upgrade selected
characters with Azure or ElevenLabs. Because audio is generated **per line** with a character preset, upgrading a voice
later means re-running one character only.

### 5.1 Free vs hosted workflow in one glance

1. `voice/script.jsonl` + tags -> `voice/jobs/<character>.jsonl` (one file per character, section 7).
2. For each job file run the chosen TTS, one request per line, output `voice/raw/<character>/<id>.wav`.
3. Post-process (section 6), encode to Ogg Vorbis mono, write `assets/voice/<character>/<id>.ogg` and `data/voice_index.json`.

## 6. Making delivery and emotion audible (post-processing recipes, ffmpeg)

TTS rarely whispers or shouts convincingly, so do it in the mix. Input `in.wav` (mono, 24 kHz). Starting values, tune by ear:

```
# whisper: quiet, breathy, no low end, a touch of noise
ffmpeg -i in.wav -af "highpass=f=250,lowpass=f=7000,volume=-9dB,acompressor=threshold=-30dB:ratio=3" whisper.wav
# add breath noise: mix very low pink noise under it
ffmpeg -i whisper.wav -f lavfi -i "anoisesrc=color=pink:amplitude=0.02" -filter_complex "[0][1]amix=inputs=2:duration=first:weights=1 0.25" whisper_breath.wav

# inner monologue: close, dull, slightly wet
ffmpeg -i in.wav -af "lowpass=f=4500,highpass=f=120,aecho=0.8:0.6:40|70:0.25|0.15,volume=-4dB" inner.wav

# shout / calling from a distance: louder, compressed, band-limited, room echo
ffmpeg -i in.wav -af "highpass=f=200,acompressor=threshold=-18dB:ratio=6,volume=4dB,aecho=0.8:0.8:120|250:0.35|0.2" shout.wav

# letter / journal: narrator with a tiny bit of room
ffmpeg -i in.wav -af "aecho=0.8:0.9:30:0.12" letter.wav

# loudness-normalise every final file (dialogue -18 LUFS, whisper -24, shout -14)
ffmpeg -i x.wav -af loudnorm=I=-18:TP=-1.5:LRA=7 x_norm.wav

# encode for the game: mono Ogg Vorbis, small
ffmpeg -i x_norm.wav -ac 1 -ar 22050 -c:a libvorbis -q:a 2 x.ogg
```

Also per emotion, change TTS `speed`/`rate`: afraid/urgent 1.1x, sad/weary 0.9x, menacing 0.9x. Dracula uses a global low-pass
and lower pitch (`asetrate`) rather than a different voice for the vampire forms.

Size check: 10 h at about 24 kbps mono is roughly 110 MB; Tier 1 alone is about 50 MB.

## 7. Files, scripts and layout

```
voice/script.jsonl            all lines (extract_script.py)            tracked
voice/tags.jsonl              id -> delivery, emotion, pace, energy     tracked (output of section 4)
voice/cast.csv                character -> engine, voice id, speed, pitch, effects chain   tracked (you edit)
voice/jobs/<character>.jsonl  lines for one character, ready for TTS   generated
voice/raw/<character>/<id>.wav  TTS output                              not tracked
assets/voice/<character>/<id>.ogg  final game audio                     tracked or release asset
data/voice_index.json         id -> {file, seconds, character, delivery, energy}
```

Scripts still to write (small, each one self-contained): `merge_tags.py` (tags -> script), `make_jobs.py` (one job
file per character, minor speakers mapped to pools via `cast.csv`), `render_tts.py` (reads a job file, calls Kokoro / Piper /
Azure / ElevenLabs depending on `cast.csv`, resumable, skips existing files), `post.py` (ffmpeg chains by delivery, loudnorm,
encode, writes `voice_index.json`).

### One file per character, or one file per line?

**One short file per line** (as above) is the simpler and more robust choice:

* dialogue branches and is replayed in any order, so a timeline per character would still need a cut point per line;
* the game needs the exact length of a line (talk animation, auto-advance) and can then just `play(id)`;
* a failed or changed line is regenerated alone; a character's whole file would have to be rebuilt.

If a tool forces long takes (for example a web UI that only accepts a long script and returns one file per speaker), do this:
join one character's lines with 1.5 s of silence between them, keep `voice/jobs/<character>.txt` with the ids in order, then split
the result back with `ffmpeg silencedetect` (or a forced aligner such as Whisper) and check that the number of pieces equals the number of ids.
Never place players on a timeline in the engine: use `voice_index.json` and one `AudioStreamPlayer` per speaking actor.

## 8. In the game (Godot)

* `Voice` autoload: `Voice.say(line_id, actor)` loads `res://assets/voice/<char>/<id>.ogg`, plays it on an
  `AudioStreamPlayer3D` at the actor (or a 2D player for the narrator, inner monologue and letters), returns the length.
* Dialogue box: show the text as now, start the audio, wait for audio end (or click to skip = stop audio); `auto-advance`
  optional. If a file is missing the line falls back to text only, so partial coverage is fine.
* Lip/gesture sync: read the clip's loudness envelope once (precomputed in `voice_index.json`: 20 samples per second) and drive
  `Actor.talking` intensity: head nods and arm gestures scale with `energy`; shouts raise the arms, whispers lean in.
* Mixer: add a `Voice` bus (narrator and inner monologue slightly dry, characters with the scene's reverb); duck music by -8 dB
  while a line plays; separate volume slider in the Esc menu.
* Settings: voice on/off, subtitles always on, narrator on/off (some players only want character voices).

## 9. Work plan

1. Run `extract_script.py` (done) and review the speaker aliases / pools (`voice/summary.json`).
2. Write `cast.csv`; audition 3 sample lines per character with Kokoro/Piper (and one hero voice on ElevenLabs/Azure); freeze voices.
3. LLM tagging for Tier 1 (about 1 800 lines = 45 batches of 40); merge; review 5 %.
4. `make_jobs.py`, `render_tts.py`, `post.py`; render Tier 1 (a few hours of CPU with Kokoro/Piper); listen to a sample per character.
5. `Voice` autoload + dialogue integration + lip/gesture sync; test with the replays (voice disabled in tests).
6. Tier 2 and 3; polish (breaths, line-end tails, accent fixes for names: Szgany, Bistritz, Borgo, Whitby, Renfield).
7. Ship the audio as a separate release asset if it grows past what is comfortable in the repository.

## 10. Checklist for external tools (copy-paste)

* Keep the line `id` in every file name; never rename it.
* Mono, 24 kHz or higher, no music, no reverb in the raw TTS output (effects are added in post).
* One character = one voice id; record the engine, voice id, speed and pitch in `voice/cast.csv`.
* Pronunciation fixes go in one shared list (`voice/pronounce.json`: written form -> phonetic text) applied before TTS.
* Do not voice `[stage directions]`, UI text or item names; strip `\n` and markdown before sending.
