# Chapter extraction schema (book/extract/chapter_NN.json)

One JSON object per chapter. Be exhaustive: every named place, object, person, creature, rule, obstacle, fight and
recipe in the text, even minor. Use ONLY what the text says or directly implies; mark inference with "inferred": true.
Quotes: verbatim from the text, max 30 words each.

{
 "chapter": 1, "narrator": "...", "dates": "3 May - 5 May", "summary": "5-8 sentences",
 "scenes": [{"id":"c01_s01","title":"","location":"","time":"","characters":[""],"summary":"","mood":"","key_quote":""}],
 "locations": [{"name":"","kind":"indoor|outdoor|vehicle","description":"what it looks like, from text","features":["physical objects/architecture present"],"atmosphere":"","lighting_time":"","quote":""}],
 "characters": [{"name":"","role":"","appearance":"physical description from text","clothing":"","personality":"","speech_style":"","notable_lines":[""],"abilities":[""]}],
 "objects": [{"name":"","category":"weapon|ward|tool|document|clothing|food_drink|medicine|occult|vehicle|furniture|container|key|other","description":"","function_in_story":"","location_or_owner":"","quote":""}],
 "creatures": [{"name":"","description":"","behaviour":"","weaknesses":[""],"quote":""}],
 "vampire_lore": [{"rule":"short statement","kind":"power|weakness|ritual|limitation|transformation|detection","detail":"","quote":""}],
 "puzzles": [{"name":"","setup":"","obstacle":"","book_solution":"how characters actually solved it","items_used":[""],"game_idea":"a playable puzzle derived from it","quote":""}],
 "combat": [{"name":"","participants":[""],"enemy_types":[""],"weapons_used":[""],"tactics":"","outcome":"","game_idea":"how to turn into a turn-based/party encounter","quote":""}],
 "crafting": [{"result":"","ingredients":[""],"method":"","purpose":"","quote":""}],
 "dialogue_samples": [{"speaker":"","line":"","context":""}],
 "asset_candidates": [{"name":"","type":"prop|architecture|character|creature|vehicle|effect|document","visual_description":"concrete geometry/material/colour detail usable for a 3D modeller","priority":1}],
 "quest_hooks": ["short ideas for quests / objectives / choices that this chapter supports"]
}
Empty lists are fine; do not invent. Output must be valid JSON only in the file.
