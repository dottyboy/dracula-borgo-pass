# Creatures and animals: complete prompt sheet

Companion to `docs/ASSET_PROMPTS.md` (read its sections 0, 1 and 8 first: pipeline, reusable blocks, quality checklist).
Everything below is copy-paste ready. Sounds for each creature are in `docs/AUDIO_PROMPTS.md` (ids in the "sound" column).

## 0. How creatures differ from people

* One subject per image, **side view (profile), whole animal in frame including all feet, tail and ears**, standing on all
  four legs in a neutral stance, mouth closed, flat light-green background, no ground shadow. For image-to-3D also make a
  **front view of the head** if the tool accepts a second image.
* Birds and bats: wings **half open and symmetric**, seen from the side; a second image with wings **fully spread, seen from above**.
* Insects: top-down, wings spread, whole animal.
* Rig class (how the animal will be animated): `quad` (four-legged walk/trot), `bird` (hop/walk + wing flap), `bat` (wing flap only),
  `swarm` (many small animated copies), `static` (no skeleton), `fx` (particles/shader, no model). Today the game animates quads and
  bats procedurally; skinned AI animals will need a generic quadruped rig first (roadmap C5), so keep legs clearly separated and the body
  in a plain standing pose.
* Scale is given in metres (shoulder height for quadrupeds, wingspan for flyers) so the game can fit the model.
* Keep one wording per species across colour variants: only change the colour/state phrase.

**ANIMAL_PREFIX**
```
A full-body side view, shot from the nose to the tail, standing on all four legs in a neutral relaxed pose, all four feet
visible with a little spacing below them, whole animal inside the frame, A photorealistic
```
**ANIMAL_SUFFIX**
```
, mouth closed, calm neutral expression, in front of a flat light-green background, photoshoot lighting from all angles, even
shadowless lighting, intricate fur/feather detail, no ground, no shadow, no other objects, no text.
```
**ANIMAL_NEGATIVE:** `cropped, cut off paws, motion blur, running, jumping, mouth open, several animals, human, rider, saddle (unless asked), collar, leash, text, watermark, cartoon, illustration, deformed legs, extra legs`

## 1. Canids (wolves and dogs)

| id | in the game | rig | scale | sound |
|---|---|---|---|---|
| wolf_grey (wolf:grey) | Borgo Pass packs, many encounters (8 placements) | quad | 0.75 m | wolf_* |
| wolf_black (wolf:black) | night packs, the Szgany road | quad | 0.75 m | wolf_* |
| wolf_white (wolf:white) | snow scenes, Act VI | quad | 0.75 m | wolf_* |
| wolf_lean (arthur_burden_lean_wolf) | the starved wolf of the Arthur arc | quad | 0.7 m | wolf_whimper, wolf_growl |
| wolf_alpha (wolf_big:grey/black) | "Great wolf" boss, 4 placements | quad | 0.95 m | wolf_alpha_* |
| dog_huge (a2_dog, wolf_big) | "The huge dog" that leaps from the Demeter onto Whitby pier | quad | 0.9 m | dog_* |
| berserker (a3_berserker) | Bersicker, the escaped zoo wolf in London | quad | 0.85 m | wolf_alpha_*, wolf_howl |
| dog_hound | Seward's household / gamekeepers, hunt arcs | quad | 0.65 m | dog_* |
| dog_sheep | Carpathian sheepdog guarding flocks, shaggy white | quad | 0.7 m | dog_* |
| dog_terrier | Whitby / Purfleet small ratting terrier | quad | 0.4 m | dog_small_* |

```
<ANIMAL_PREFIX> large grey Carpathian wolf, thick winter coat, grey-brown fur with pale underside, heavy ruff around the neck,
yellow amber eyes, long legs, bushy tail hanging low, lean muscular build <ANIMAL_SUFFIX>
```
Variants (replace only the colour/state words): **black** "jet-black wolf, faint brown on the muzzle"; **white** "pure white arctic-type
wolf with pale blue-grey shadows"; **lean** "starved grey wolf, ribs visible, matted dull fur, sunken flanks, hungry eyes";
**alpha** "very large powerful alpha wolf, scarred muzzle, one torn ear, thick mane, dark grey with a black saddle, heavy chest".

```
<ANIMAL_PREFIX> enormous black mastiff-like dog, size of a calf, short dense black coat, massive head, broad muzzle, pendulous
jowls, dark brown eyes with a faint red glint, thick neck, powerful chest, long thin tail <ANIMAL_SUFFIX>
```
```
<ANIMAL_PREFIX> Victorian foxhound, white with brown and black patches, floppy ears, deep chest, alert friendly expression <ANIMAL_SUFFIX>
<ANIMAL_PREFIX> shaggy white Carpathian sheepdog, thick long coat, dark nose, heavy build, calm eyes <ANIMAL_SUFFIX>
<ANIMAL_PREFIX> small rough-coated Victorian terrier, brown and white, cropped ears, alert posture <ANIMAL_SUFFIX>
```

## 2. Horses and other livestock

| id | in the game | rig | scale | sound |
|---|---|---|---|---|
| horse_bay (quincey_hunt_horse:bay) | Quincey hunt arc, riding | quad | 1.5 m | horse_* |
| horse_paint (quincey_hunt_horse:paint) | the same arc, Texan pinto | quad | 1.45 m | horse_* |
| horse_black_pair | the coachman's four black horses at Borgo Pass | quad x2 | 1.6 m | horse_* , harness |
| horse_grey_carriage | London / Whitby cabs and carriages | quad | 1.6 m | horse_* , harness |
| horse_draft | carts, Szgany wagons (heavy, feathered feet) | quad | 1.7 m | horse_* |
| horse_white_ghost | optional dream / vision horse | quad | 1.5 m | horse_snort |
| pony | Whitby beach, children's cart | quad | 1.1 m | horse_small_* |
| donkey | carriers, Slovak carriers' carts | quad | 1.2 m | donkey_bray |
| cow | Whitby fields, Hillingham dairy | quad | 1.4 m | cow_moo |
| ox | Szgany / Slovak wagons | quad | 1.5 m | ox_low |
| sheep (white + black) | Whitby cliffs, Carpathian flocks | quad | 0.75 m | sheep_baa |
| goat | Carpathian farmsteads | quad | 0.8 m | goat_bleat |
| pig | farmyards (Purfleet) | quad | 0.8 m | pig_grunt |
| chicken, goose | village yards | bird | 0.35 m | chicken_cluck, goose_honk |

```
<ANIMAL_PREFIX> bay riding horse, glossy reddish-brown coat, black mane, tail and lower legs, white star on the forehead,
muscular, bridle and plain Victorian saddle with stirrups <ANIMAL_SUFFIX>
```
Variants: **paint** "brown-and-white pinto horse, large irregular patches, light mane, Western saddle"; **carriage** "black carriage horse
in full harness with blinkers and collar, shiny coat, braided mane, no carriage (harness straps cut off at the sides)";
**draft** "heavy draft horse, dapple grey, thick neck, feathered hooves, work harness"; **pony** "shaggy chestnut pony, short legs".
```
<ANIMAL_PREFIX> dairy cow, black and white, heavy udder, alert ears <ANIMAL_SUFFIX>
<ANIMAL_PREFIX> long-haired draught ox, dark brown, heavy horns, wooden yoke <ANIMAL_SUFFIX>
<ANIMAL_PREFIX> woolly white Carpathian sheep, dark face and legs <ANIMAL_SUFFIX>
<ANIMAL_PREFIX> small donkey, grey-brown, dark cross on the shoulders, long ears <ANIMAL_SUFFIX>
<ANIMAL_PREFIX> goat with curved horns, brown and white, thin beard <ANIMAL_SUFFIX>
<ANIMAL_PREFIX> farm pig, pink-brown, floppy ears <ANIMAL_SUFFIX>
```

## 3. Small mammals

| id | in the game | rig | scale | sound |
|---|---|---|---|---|
| rat_brown | Carfax chapel cellar rats (currently the bat model is used!), "Rat" enemy | quad | 0.25 m long | rat_* |
| rat_black | crypts, ship hold on the Demeter | quad | 0.25 m | rat_* |
| rat_swarm | Dracula's rat summons, many small animated copies | swarm | tile 1 m | rat_swarm |
| mouse | libraries, inns (background life) | quad | 0.1 m | mouse_squeak |
| cat_black | Seward / Hillingham, Whitby alleys | quad | 0.3 m | cat_* |
| cat_tabby | inns, harbour | quad | 0.3 m | cat_* |
| fox | Hampstead heath, Transylvanian woods | quad | 0.4 m | fox_bark |
| deer / stag | Hampstead, Kingstead, forest scenes | quad | 1.2 m | deer_call |
| hare | heath, meadow | quad | 0.25 m | - |
| bear (brown) | Carpathian forest (bears are mentioned by the book); optional encounter | quad | 1.1 m | bear_growl |
| hedgehog | gardens (ambient) | quad | 0.1 m | - |

```
<ANIMAL_PREFIX> brown sewer rat, long hairless tail, small round ears, pink nose, whiskers, hunched stance <ANIMAL_SUFFIX>
<ANIMAL_PREFIX> black ship rat, sleek, long tail, red-brown eyes <ANIMAL_SUFFIX>
<ANIMAL_PREFIX> black domestic cat, green eyes, tail up <ANIMAL_SUFFIX>
<ANIMAL_PREFIX> red fox, thick winter coat, bushy tail with white tip <ANIMAL_SUFFIX>
<ANIMAL_PREFIX> red deer stag, antlers, brown coat, standing alert <ANIMAL_SUFFIX>
<ANIMAL_PREFIX> European brown bear, heavy shoulders, thick dark coat <ANIMAL_SUFFIX>
```
Rat swarm: "A top-down tile 1 m by 1 m of about twenty small brown rats crowded together on a flat grey stone floor, seamless
edges, overhead orthographic view" (use it as a decal/particle source).

## 4. Birds

| id | in the game | rig | scale | sound |
|---|---|---|---|---|
| gull (gull:white) | harbour, Whitby cliffs (exists, procedural) | bird | 0.6 m wingspan 1.4 m | gull_* |
| raven | castle ruins, graveyards, omen scenes (needed) | bird | 0.6 m, span 1.2 m | raven_caw |
| crow | fields, Kingstead churchyard | bird | 0.45 m | crow_caw |
| owl_barn | church tower, Carfax, night | bird | 0.35 m, span 0.9 m | owl_hoot |
| owl_tawny | woods, Hillingham garden night | bird | 0.4 m | owl_hoot |
| swallow | Whitby cliffs, summer day | bird | 0.17 m | swallow_twitter |
| nightingale / blackbird | Hillingham garden, dusk | bird | 0.2 m | songbird_* |
| sparrow | street, inn yards (ambient) | bird | 0.15 m | sparrow_chirp |
| pigeon | London, Hillingham | bird | 0.35 m | pigeon_coo |
| vulture / buzzard | Borgo Pass, Act I and VI | bird | span 1.6 m | hawk_cry |
| chicken, goose | village | bird | 0.35 m | see section 2 |

```
<ANIMAL_PREFIX> common raven standing, glossy black plumage with a blue sheen, heavy black beak, wings folded, strong legs <ANIMAL_SUFFIX>
<ANIMAL_PREFIX> carrion crow standing, matte black, slim beak <ANIMAL_SUFFIX>
<ANIMAL_PREFIX> barn owl standing upright, heart-shaped white face, golden-buff back, dark eyes <ANIMAL_SUFFIX>
<ANIMAL_PREFIX> tawny owl standing upright, mottled brown, round face, large dark eyes <ANIMAL_SUFFIX>
<ANIMAL_PREFIX> swallow perched, steel-blue back, red throat, long forked tail <ANIMAL_SUFFIX>
<ANIMAL_PREFIX> pigeon standing, grey with an iridescent neck <ANIMAL_SUFFIX>
<ANIMAL_PREFIX> buzzard perched, brown mottled, hooked beak <ANIMAL_SUFFIX>
```
Second image for flyers: "The same bird with wings fully spread, seen from directly above, symmetrical, flat green background."

## 5. Bats, insects and other small things

| id | in the game | rig | scale | sound |
|---|---|---|---|---|
| bat_black (bat:black) | the bat swarms, Renfield's window, Dracula's scouts | bat | span 0.5 m | bat_* |
| bat_brown (bat:brown) | caves, crypts | bat | span 0.4 m | bat_* |
| bat_giant | Dracula's bat form (from the book: large bat at the window) | bat | span 1.3 m | bat_giant_* |
| bat_swarm | clouds of bats, silhouette sheets | swarm | - | bat_swarm |
| moth_deaths_head | the death's-head hawkmoth at Renfield's cell (a scene in the book) | bird | span 0.12 m | moth_wings |
| fly (bluebottle) | Renfield feeds on flies; asylum rooms | swarm | 0.02 m | fly_buzz |
| spider | cobweb corners, Renfield | swarm | 0.03 m | - |
| beetle | cellars, graveyards | static | 0.03 m | - |
| crab (shore) | Whitby beach | static | 0.1 m | - |
| fish / eel | harbour water (decoration) | static | 0.3 m | - |

**FLYER_SUFFIX** (use instead of ANIMAL_SUFFIX for bats, moths and flies)
```
, wings fully spread and symmetric, seen from directly above, flat light-green background, photoshoot lighting from all angles, even lighting, no shadow, no text
```
```
A photorealistic black vampire bat (large flying fox type), dark fur, leathery wing membranes with visible finger bones, small glinting dark eyes <FLYER_SUFFIX>
A photorealistic huge bat, wingspan of a large crow, black-grey fur, dull glowing red eyes, clawed wing thumbs <FLYER_SUFFIX>
A photorealistic death's-head hawkmoth, brown and yellow wings, a pale skull pattern on the thorax <FLYER_SUFFIX>
A photorealistic bluebottle blowfly, metallic blue-green body, transparent wings <FLYER_SUFFIX>
```

## 6. Supernatural and effects (no model unless noted)

| id | what | how to make |
|---|---|---|
| mist_form | Dracula's fog/mist form, wolf or human-shaped mist | particle/shader effect in Godot; prompt a reference: "a tall human silhouette made of thick swirling white-grey mist with two faint red eyes, black background" for the look |
| dust_motes | moonlit dust, Dracula's dust in the coffin | particle system; reference texture: "soft white round dust particle, black background" |
| blue_flames | the treasure flames at Borgo Pass | particle effect; reference "small cold blue flame floating above the ground, black background, photoreal" |
| rat_wave / bat_cloud | summoned swarms | `swarm` rigs from sections 3 and 5 |
| coffin_earth | earth boxes: "a long black oak box filled with dark soil, lid open" (static prop in ASSET_PROMPTS section 6) |
| ghost_lucy / shade | the tall thin figure on the Demeter | human model with translucent shader (use a normal human model, no prompt needed) |
| eye_glint | red eyes in the dark | emissive small sprites; no prompt |
| wolf_pack_silhouette | background silhouettes on the horizon | "five wolves in a line silhouetted against a pale moonlit horizon, flat black, side view" (decal) |

## 7. Creature variants and numbers to generate (suggested order)

1. wolf_grey, wolf_alpha, rat_brown, bat_black, horse_bay (the encounters and story scenes you meet first).
2. raven, owl_barn, gull (exists), dog_huge, horse_black_pair, bat_giant.
3. wolf_black, wolf_white, wolf_lean, horse_paint, horse_grey_carriage, horse_draft, cat_black.
4. sheep, cow, donkey, goat, pig, chicken, goose (village life).
5. insects, small birds, fox, deer, bear (ambient and optional).
Keep `ai/creatures/<id>.png` and `.glb` named after the id; record tool and seed in `ai/SOURCES.md`.
