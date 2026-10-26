# Main characters
https://huggingface.co/spaces/black-forest-labs/flux-3-image-klein  

https://huggingface.co/spaces/Aura1in/Krea-2-Turbo_v2 

https://perchance.org/ai-text-to-image-generator


Use the blocks from `README.md` section 1.

## 2. Dracula (all forms)

Your four prompts stay as they are (they worked). Use them with the CHARACTER_SUFFIX instead of the walking stick / flowing
cape details when the model is to be rigged. Extra variants to generate:

**DraculaOld_nocape** (replaces the old DraculaOld model: rig this one; the first DraculaOld GLB is retired)
```
<CHARACTER_PREFIX> Count Dracula in human form as an elderly, ancient man, completely clean-shaven, no beard, no mustache.
Pale gaunt deeply wrinkled face, sharp cheekbones, aquiline nose, piercing red eyes, long slicked-back stark white hair.
Elegant faded black Victorian 3-piece suit with a long black frock coat to the knees, high-collar shirt with a dark cravat,
black leather boots, no cape. <CHARACTER_SUFFIX>
```

**DraculaYoung_nocape**: same as above but "a handsome, pale, aristocratic man in his late 30s, dark slicked-back hair and a
neat dark moustache, piercing red eyes, black Victorian 3-piece suit with double-breasted vest, white high collar and dark
cravat, no cape".

**DraculaLondon**: "a vigorous man of about 50, iron-grey hair, small white moustache, dark grey tweed Victorian town suit,
top hat in hand NOT held (hat on head), pale skin, red-tinged eyes". (Variant `london`.)

## 3. Main cast

Use CHARACTER_PREFIX + text + CHARACTER_SUFFIX. File name = id.

| id (model:variant) | description |
|---|---|
| harker (human_harker:harker) | Jonathan Harker, English solicitor, 27, clean-faced with short brown hair, earnest and slightly tired, brown wool Victorian travelling coat, waistcoat, white shirt, cravat, brown trousers, dark leather boots |
| harker_travel (human_harker:travel) | the same man in a dark green wool travelling coat, scarf, sturdy boots |
| mina (human_mina:mina) | Mina Murray, English schoolmistress, 23, dark brown hair in a bun, intelligent kind face, fitted blue-grey long-sleeved high-collar top with a plain cream round collar and cuffs, buttons down the front, narrow brown leather belt at the waist, tight fitted trousers tucked into tall boots, NO skirt, NO dress, NO coat (those are made separately, see 02_capes_and_garments.md) |
| mina_nurse (human_mina:nurse) | Mina as a nurse: fitted white and grey long-sleeved top with a small white collar, hair covered by a small white cap, tight pale grey trousers into black boots, NO apron, NO dress (apron and dress made separately) |
| lucy (human_lucy:lucy) | Lucy Westenra, 19, golden-blond hair worn loose and long, bright face, fitted cream long-sleeved blouse with pink trim at the collar and cuffs, tight fitted trousers tucked into tall boots, NO skirt, NO dress, NO coat (those are made separately, see 02_capes_and_garments.md) (tight cream trousers) |
| lucy_nightgown (human_lucy:nightgown) | Lucy in a fitted plain white long-sleeved nightshirt top and tight white trousers, loose hair, bare feet, ghostly pale, NO nightgown skirt (made separately) |
| lucy_undead (human_lucy:undead) | Lucy as a vampire: very pale grey skin, red eyes, voluptuous cruel smile with small fangs, fitted white long-sleeved top stained dark and tight white trousers, bare feet, long golden hair, NO gown (made separately) |
| vanhelsing (human_vanhelsing:vh) | Professor Abraham Van Helsing, Dutch, about 65, stocky, bald-ish with short white hair, white pointed beard, kind sharp eyes, black Victorian frock coat, dark waistcoat, white shirt, black cravat, black trousers and boots |
| seward (human_seward:doctor) | Dr John Seward, English psychiatrist, 29, short brown hair, neat moustache, tired thoughtful face, dark blue-grey frock coat, grey waistcoat, white collar, grey trousers, black shoes |
| quincey (human_quincey:texan) | Quincey Morris, Texan, 30, tanned, short dark hair, pointed beard, friendly grin, dark brown frontier coat over a red shirt, grey trousers, tall boots, wide-brimmed hat on head (hat allowed) |
| arthur (human_arthur:lord) | Arthur Holmwood, Lord Godalming, 27, fair swept hair, handsome open face, dark navy tailcoat, dark grey trousers, polished boots |
| renfield (human_renfield:asylum) | R. M. Renfield, lunatic, about 55, thin, dishevelled sandy-grey hair, wild eyes, bare dirty cream asylum shirt and trousers, grey slippers, restraining jacket NOT worn |
| bride1 (human_bride:bride1) | one of the three vampire sisters: very pale, long wavy golden hair, red lips with fangs, fitted off-white long-sleeved gauze top and tight off-white trousers, bare feet; seductive and cruel, eyes dark with red glints, NO gown, NO skirt (made separately) |
| bride2 | the same but long straight black hair, silvery-lilac top and trousers |
| bride3 | the same but long red-auburn hair, pale ivory top and trousers |

**Renfield, two types (plus an optional third).**
| id | description |
|---|---|
| renfield_patient | Renfield as an asylum patient: thin, sandy-grey dishevelled hair, wild bright eyes, cracked lips, creased off-white asylum shirt and trousers, bare feet or slippers, restless crooked posture relaxed into T-pose |
| renfield_lucid | Renfield on a good day: combed grey-sandy hair, shaved, calm intelligent eyes, a tidy dark grey Victorian suit with waistcoat and white collar, polished black shoes |
| renfield_restrained (optional) | Renfield in a white canvas restraining jacket with the sleeves loose at the sides (so the T-pose is possible), bare feet |

**Van Helsing, younger.**
| id | description |
|---|---|
| vanhelsing_young | Abraham Van Helsing at about 38, dark brown hair swept back, dark short beard trimmed to a point, intense bright eyes, lean, black Victorian frock coat, dark waistcoat, white shirt, black cravat, black trousers and boots, no spectacles |
| vanhelsing_middle | Van Helsing at about 50, hair salt-and-pepper, short grey pointed beard, same clothes as the old version |

**More main-cast looks for the arcs** (use the same prompt style; one line each; women always in fitted top and tight trousers, skirts/dresses/coats are separate): Lucy in a fitted white summer blouse with a straw hat on the head; Mina in a fitted dark travelling top with a small hat on the head; Arthur in mourning black; Quincey in a fringed frontier jacket; Seward in a white doctor's coat over his suit; Harker, weary after the castle, thin, in a torn travelling coat; Harker, white-haired as in London (Mina's diary: his hair turned white), same clothes as the travelling coat but neat.

