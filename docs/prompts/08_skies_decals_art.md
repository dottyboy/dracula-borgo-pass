# Skies, decals, signs and story art

## 9. Skies, decals, signs and story art

**Sky panoramas** (equirectangular 2:1, 4096 x 2048, seamless left-right edge; game files `assets/sky/<id>.png`)
```
Equirectangular 360 degree panorama, 2:1 aspect ratio, seamless horizontal wrap, <sky>, no ground, no buildings, no text,
photorealistic, high dynamic range, moody Victorian gothic atmosphere.
```
| id | `<sky>` |
|---|---|
| day | pale blue English sky, scattered cumulus clouds, soft daylight haze at the horizon |
| dusk | deep orange and purple dusk sky, long thin clouds, first stars |
| night | clear dark blue Carpathian night, a bright full moon on the left, many stars, thin cloud |
| snow | pale grey-white winter overcast, faint blue light |
| storm | heavy black-grey storm clouds, lightning glow inside the clouds, rain veil, green-yellow tint |
| fog | thick white-grey fog sky, almost no contrast (new) |

**Decals** (square 1024, transparent or flat background, flat frontal view; game folder `assets/decals`)
| id | prompt idea |
|---|---|
| cobweb | a dense old spider web across a corner, grey-white threads on a black background (use as alpha) |
| painting_1/2/3 | a framed Victorian oil painting: (1) stern nobleman portrait, (2) stormy sea and ship, (3) Carpathian castle on a crag; full frame visible, flat frontal |
| banner_black / banner_red | a hanging medieval banner with a dragon emblem, black and crimson, tattered edges |
| stain_1/2 | dark old blood stain / water stain on stone, top-down, irregular edge |
| shaft | a shaft of moonlight through a window, soft beam on black background |
| more | cracked plaster, moss patch, soot mark above a candle, scratched wooden door, rust stain, handprints in dust |

**Title and story art** (16:9, 3840 x 2160, no text so the game adds the type)
* Title: "The Carpathian castle on a crag at night under a full moon, thin mist in the valley, a lone road, bats crossing the moon, gothic horror painting, photorealistic".
* Chapter cards (one per act): Bistritz inn by candlelight; Whitby harbour at night with the Demeter wrecked on the shore; Hillingham garden at dusk with a pale figure in white; Hampstead heath at night with a mist; Carfax chapel interior; snowy Borgo Pass at sunset with a wagon.
* Item icons (256 x 256, centred object, plain dark background, one image per item): see `items` in `data/world.json` (228 items; start with crucifix, host, garlic, stake, key, letters).

