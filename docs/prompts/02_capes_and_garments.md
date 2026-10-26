# Capes, cloaks and all other garments that move

Use the blocks from `README.md` section 1 for the character prompts; capes are generated alone.

## Capes, cloaks and all other garments that move (separate models, never part of the character)

A cape is generated alone, hanging on an invisible body, so image-to-3D gives a clean cloth shape; in the game it is attached
to the shoulders as cloth (chain bones). Generate a back view and a front view, one prompt each.

```
A long black Victorian opera cape with a high standing collar and a deep crimson silk lining, hanging straight down from the
shoulders as if worn by an invisible tall man (no body, no head, no arms visible), seen from the FRONT, full length to the
ankles, whole cape inside the frame, in front of a flat light-green background, photoshoot lighting from all angles,
photorealistic, heavy velvet folds, intricate details.
```
Same text with "seen from the BACK" for the second image.

| id | description (replace the cape part) |
|---|---|
| cape_dracula | long black velvet opera cape, high collar, crimson silk lining, silver clasp at the neck (the count) |
| cape_dracula_tattered | the same cape, torn and ragged at the hem, dissolving into black fog at the bottom (vampire form) |
| cloak_coachman | long hooded black wool travelling cloak, hood down, plain, dust on the hem |
| cloak_traveller | dark green wool travelling cloak with a short shoulder cape, brass clasp |
| cloak_sea | oilskin sailor's coat-cloak, glossy dark yellow-brown, hood down |
| cloak_nun / shawl | black wool shawl draped over the shoulders, fringe at the edge |
| cloak_lady | plum Victorian lady's mantle with fur collar, hip length |
| cloak_peasant | coarse brown wool Carpathian cloak with a rope tie |

Textures for capes: black velvet (nap, soft folds), crimson silk (sheen), oilskin (glossy coated canvas), coarse brown wool - see
section 7.


## Garments generated separately (skirts, dresses, gowns, coats, aprons)

Women's bodies are generated in tight trousers (see `README.md` WOMEN_OUTFIT). Everything that hangs or flows is a **separate model**
that the game attaches as cloth (chain bones + spring bones, like the cape). Each garment: front and back image, shown on an invisible
body, flat green background, same lighting; the garment is fitted for an average woman 1.65 m tall with the waist at the hips.

**GARMENT_PREFIX**
```
A single Victorian garment shown as if worn by an invisible slender woman of average height (no body, no head, no arms, no legs
visible, only the cloth holding its shape), seen from the FRONT, whole garment inside the frame, in front of a flat light-green
background, photoshoot lighting from all angles, photorealistic fabric detail, heavy realistic folds. The garment:
```
(second image: same text with "seen from the BACK".)

| id | the garment |
|---|---|
| skirt_plain | a plain ankle-length wool skirt, narrow waistband, gathered gently, dark colour |
| skirt_bell | a wide bell-shaped crinoline skirt to the ankles, smooth, with a hem band |
| skirt_bustle | a Victorian bustle skirt with a draped overskirt and a pleated train behind |
| skirt_short_peasant | a knee-length gathered peasant skirt with an apron tie |
| dress_day | a long-sleeved high-collar Victorian day dress with a fitted bodice and a full skirt (use as one piece over the trousers body) |
| dress_nightgown | a plain white long nightgown, long sleeves, ruffled collar, to the ankles |
| gown_evening | a floor-length gown with a fitted bodice, bare lace sleeves, a gathered skirt and a short train |
| gown_vampire | a flowing translucent gauze gown with long trailing sleeves, torn at the hem |
| coat_long_lady | a fitted knee-length ladies' coat with a fur collar and cuffs, double row of buttons |
| coat_travel_lady | a long hooded travelling coat in dark wool, belted |
| jacket_short | a short fitted jacket with a peplum at the hips |
| apron_white | a long white cotton apron with a bib and waist ties |
| apron_work | a coarse brown work apron |
| shawl_wool | a big wool shawl draped over the shoulders, fringed edge |
| shawl_lace | a black lace shawl worn over the shoulders |
| habit_nun | a long black nun's habit skirt with a white wimple and short black veil |
| nurse_dress | a plain grey nurse's dress with a white apron and cap |
| mantle_fur | a short plum velvet mantle with a fur collar |

Colour variants are made in the game (tint), so generate each garment once in a neutral mid-dark colour, plus the special ones above.
Men's matching items (long frock coats beyond the knee, ulsters, aprons, oilskins) use the same prefix with "invisible tall man".
