"""ACT III - "The Asylum and the Blood" (novel chapters 9-12).
Dr. Seward's asylum and Renfield; a short interlude in Buda-Pesth (Mina); Lucy's decline at Hillingham, Van Helsing,
the garlic, four transfusions, the wolf, Mrs Westenra's death, Lucy's death and burial. Ends: goto a4_hampstead_heath."""
from dsl import *


def n(speaker, text, choices=None, next=None, do=None, end=False):
    d = dict(speaker=speaker, text=text)
    if do:
        d["do"] = do
    if choices:
        d["choices"] = choices
    elif next:
        d["next"] = next
    elif end:
        d["end"] = True
    return d


def c(text, next=None, do=None, cond=None, end=False):
    d = dict(text=text)
    if next:
        d["next"] = next
    if do:
        d["do"] = do
    if cond:
        d["cond"] = cond
    if end:
        d["end"] = True
    return d


def say(t):
    return {"say": t}


def D(start, **nodes):
    return dict(start=start, nodes=nodes)


LEAVE = c("[Leave]", end=True)

ACT = dict(
    id=3, title="The Asylum and the Blood",
    start=dict(location="a3_asylum_study", protagonist="seward", party=["seward"], items={}, flags=["a3_begun"]),
    exit_to="a4_hampstead_heath",
)

LOCATIONS = [
    dict(id="a3_asylum_study", name="Dr. Seward's study, Purfleet", date="2 September",
         desc="My own room in the asylum: the desk, the phonograph, the case-books. Somewhere below, a patient is counting flies."),
    dict(id="a3_asylum_ward", name="The asylum ward and dispensary",
         desc="A whitewashed passage of locked doors. At the end hangs the dispensary cabinet, and at the head of the passage a cell I would rather not open."),
    dict(id="a3_renfield_cell", name="Renfield's cell",
         desc="A bare room with a barred window facing the old house of Carfax. It smells of sugar, dust and something small and dead."),
    dict(id="a3_asylum_garden", name="The asylum grounds", date="3 September",
         desc="Elms, a high wall, and beyond it the ruinous chimneys of Carfax. Sparrows quarrel on the gravel."),
    dict(id="a3_zoo_gardens", name="The Zoological Gardens",
         desc="Keepers' cottages behind the elephant-house. Far off, a wolf is howling in the afternoon."),
    dict(id="a3_buda_hospital", name="Hospital of St. Joseph and Ste. Mary, Buda-Pesth", date="24 August",
         desc="A long, clean ward of white beds and quiet nuns. In the corner bed lies a thin, grey-haired man I cannot recognise, and cannot mistake."),
    dict(id="a3_buda_chapel", name="The hospital chapel",
         desc="A small chapel, candles, a plain altar. Sister Agatha has said it may be done here, at once."),
    dict(id="a3_hillingham_hall", name="Hillingham, the hall", date="6 September",
         desc="Mrs Westenra's house at Hampstead, quiet as a held breath. A clock ticks too loudly. Upstairs, Lucy sleeps."),
    dict(id="a3_lucy_bedroom", name="Lucy's bedroom, Hillingham",
         desc="A girlish room: a white bed, a deep window-seat, curtains stirring where no one has touched them."),
    dict(id="a3_hillingham_garden", name="The Hillingham garden",
         desc="Lawn, shrubbery, a tool-shed, and the night coming down. Something flaps against the lit windows above."),
    dict(id="a3_kingstead_churchyard", name="Kingstead churchyard", date="22 September",
         desc="The Westenra vault under the yews. A thin rain. Four men, a Professor, and a very small coffin of silence."),
]

ASSETS = [
    dict(id="a3_phonograph", builder="a3_phonograph", params={}),
    dict(id="a3_clock", builder="a3_clock", params={}),
    dict(id="a3_bag", builder="a3_bag", params={}),
]
VARIANTS = {
    "a3_phonograph": {"default": "oak", "oak": {}, "dark": {"wood": T("wood_planks", "#4a3a30")}},
    "a3_clock": {"default": "oak", "oak": {}, "dark": {"wood": T("wood_planks", "#4a3a30")}},
    "a3_bag": {"default": "brown", "brown": {}, "black": {"leather": T("leather", "#1c1a1a")}},
}

ITEMS = {
    "a3_dispensary_key": dict(name="Dispensary key", asset="key", variant="gold", desc="A small brass key marked D. It opens the poison cabinet in the ward. Only I, and Hennessey, carry one."),
    "a3_chloral_crystals": dict(name="Chloral crystals", asset="bottle", variant="amber", desc="Chloral hydrate, in clean white crystal. Dissolved in water it sends a man to sleep. In the wrong dose it sends him a good deal further."),
    "a3_sugar_lumps": dict(name="Hoarded sugar", asset="candle", variant="white", desc="Sugar lumps, hidden in a patient's pillow. Sugar attracts flies. Flies are his stock-in-trade."),
    "a3_fly_jar": dict(name="Jar of flies", asset="bottle", variant="glass", desc="A jam-jar with a muslin lid and forty bluebottles. He counts them aloud every evening."),
    "a3_spider_box": dict(name="Box of spiders", asset="chest", variant="oak", desc="A matchbox in which large spiders have been kept like cattle. He feeds them flies and they grow fat."),
    "a3_renfield_notebook": dict(name="Renfield's notebook", asset="book", variant="leather", desc="Columns of figures: so many flies, so many spiders, so many sparrows, in a small, neat, terrible hand."),
    "a3_orderly_key": dict(name="Orderly's key", asset="key", variant="default", desc="A ring-key on a loop of tarred string. It hung under the night orderly's saucer, where a man hides a key he is not supposed to have. It fits the old cell doors in the cellar."),
    "a3_arthur_telegram": dict(name="Arthur's telegram", asset="book", variant="red", desc="'Lucy is not well. Come to Hillingham at once. - Arthur.' It was written, I think, by someone who had not slept."),
    "a3_telegram_form": dict(name="Telegram form", asset="book", variant="leather", desc="A blank post-office telegram form. Every word costs a halfpenny, and an hour may cost a great deal more."),
    "a3_transfusion_kit": dict(name="Transfusion kit", asset="a3_bag", variant="brown", desc="My black bag: silver tubing, lancets, a small syringe, carbolic. Everything a transfusion needs but the blood."),
    "a3_door_key": dict(name="Bedroom key", asset="key", variant="default", desc="The housekeeper's key to Lucy's room. A locked door is the one ward that cannot be argued with."),
    "a3_window_pin": dict(name="Iron window-pin", asset="stake", variant="default", desc="A stout iron pin from the potting-shed. Dropped through the sash-staples it holds a window against anything but a saw."),
    "a3_harker_diary": dict(name="Jonathan's journal", asset="book", variant="diary", desc="The shorthand journal from the Castle. Jonathan will not look at it and will not part from it."),
    "a3_sealing_wax": dict(name="Sealing wax", asset="candle", variant="red", desc="A stick of red wax from Sister Agatha's desk."),
    "a3_ribbon": dict(name="Black ribbon", asset="rug", variant="black", desc="A length of black ribbon from the sisters' sewing basket."),
    "a3_wedding_ring": dict(name="Wedding ring", asset="goblet", variant="default", desc="A plain gold ring, found in Jonathan's waistcoat pocket among a few coins. I think it was meant for this."),
    "a3_sister_letter": dict(name="Sister Agatha's letter", asset="book", variant="leather", desc="'He has had a brain fever. He wishes you to know he loves you, and that he is afraid.' - Agatha, Sister of St Joseph."),
    "a3_lucy_memo": dict(name="Lucy's memorandum", asset="book", variant="red", desc="A crumpled paper found against her heart. Her handwriting is neat to the last line, and then it is not."),
    "a3_gazette_cutting": dict(name="Gazette cutting", asset="book", variant="leather", desc="'An Escaped Wolf': the keeper's tale, cut from the Pall Mall Gazette. A tall, thin man with a beaky nose was admiring the wolf before it escaped."),
    "a3_smelling_salts": dict(name="Smelling salts", asset="bottle", variant="green", desc="Mrs Westenra's own salts. They will bring round a faint, but not a drugged girl."),
}

JOURNAL = {
    "a3_j_cellar": dict(title="The old cellar", source="Dr. Seward's diary",
                        text="Under my own asylum lies the old cellar where my predecessors kept the violent cases: padded stalls, iron staples, a dripping tap. Renfield has no business knowing of it, and yet he spoke of 'the cold dark under the house' only last week. I find I do not like the coincidence."),
    "a3_j_cellar_cell": dict(title="The cell of a hundred hands", source="Dr. Seward's diary",
                             text="With the orderly's key I opened the grated door in the cellar. The plaster is scratched from floor to ceiling with one sentence in a hundred hands: HE IS COMING. On the straw lay a crucifix and a braid of garlic, left by some earlier patient who believed it. I took them. I have never believed in such things, and I did not like how glad I was of them."),
    "a3_j_cellar_grating": dict(title="How Renfield gets out", source="Dr. Seward's diary",
                                text="At the far end of the cellar the old coal grating hangs from one hinge, the bars bent outward and the mud beneath it fresh. No orderly bent those bars. It opens on the grounds, and from there it is an easy walk to Carfax. Hennessey asked how Renfield leaves his cell. I think I have found where he goes after."),
    "a3_j_casebook": dict(title="An old case-book", source="Dr. Seward's diary",
                          text="Margin notes in my predecessor's hand: 'Zoophagy - the madman eats lives to gain life. Seen once before, and he spoke of a Master then also.' I read it twice, and wish I had not. Whatever Renfield serves, it has served itself of other minds before his."),
    "a3_j_seward_diary": dict(title="Phonograph diary", source="Dr. Seward's diary", text="My patient Renfield is the interest of my days: a life-eater, a zoophagous maniac who collects flies, then spiders, then sparrows. I keep this diary on the phonograph; it records my voice and my doubts alike. Lucy's name keeps surfacing, and Arthur's letters worry me."),
    "a3_j_dose": dict(title="The chloral rule", source="Dr. Seward's case-book", text="My own pencilled rule: chloral hydrate, ten grains for a man of nine stone, fifteen for twelve, thirty for a bull. Renfield is nine stone and wasted. Ten grains, then, in water, and no more."),
    "a3_j_sedated": dict(title="Renfield sleeps", source="Dr. Seward's diary", text="Ten grains in clean water, a quiet word, and Renfield went down like a lamb. I do not like how easily he took it. A man who eats lives should resist the needle more."),
    "a3_j_zoophagy": dict(title="The ladder of lives", source="Dr. Seward's diary", text="Sugar for flies, flies for spiders, spiders for sparrows, and in time, he asked me, a kitten. Renfield believes that to swallow many lives is to gain life. He calls it 'the blood is the life'. He says 'the Master' is coming."),
    "a3_j_fence": dict(title="The loose slat", source="Dr. Seward's diary", text="A slat in the wall by the elms was hanging by one nail, and a path through the long grass leads straight to Carfax. I have nailed it fast. Pocock swears it is not the first time."),
    "a3_j_arthur_wire": dict(title="Arthur's telegram", source="Dr. Seward's diary", text="The boy came at four. Arthur's father is dying and Arthur dare not leave him; Lucy is ill, and he trusts me to see her. I go to Hillingham tonight. Renfield is quiet; for that I am grateful and, I admit, a little uneasy."),
    "a3_j_hillingham": dict(title="Hillingham", source="Dr. Seward's diary", text="Lucy is bloodless, breathing heavily, and sleeps with her window open. Mrs Westenra says she is much better. I find no disease I can name, and that frightens me more than any I can."),
    "a3_j_lucy_exam": dict(title="Lucy's throat", source="Dr. Seward's diary", text="Two small punctures on her throat, white-edged and torn, and no fever. Her gums are pale as paper. Whatever drains her is drawing it from outside the body. I cannot do this alone: I will write to the one man who might know, my old teacher Van Helsing."),
    "a3_j_bradshaw": dict(title="The timetable", source="Dr. Seward's diary", text="Bradshaw: the night boat leaves the Hook of Holland for Harwich and the boat-train reaches Liverpool Street at five minutes past six in the morning. The telegraph closes at eight tonight. A wire sent before then, and Van Helsing can be at Hillingham by breakfast."),
    "a3_j_wired": dict(title="The wire to Amsterdam", source="Dr. Seward's diary", text="Sent, before the office shut: 'Come by the night boat from the Hook; boat-train reaches Liverpool Street 6.05; urgent, a matter of life.' The boy ran off through the dusk. I cannot do more tonight."),
    "a3_j_mina_hospital": dict(title="Buda-Pesth", source="Mina Harker's journal", text="Sister Agatha's letter said he was alive, and weak, and calling for me. I found him in the corner bed, white-haired and looking through me as if I were a window. When at last he knew me, he wept. I will not leave him again."),
    "a3_j_mina_diary_sealed": dict(title="The sealed journal", source="Mina Harker's journal", text="He has given me his journal of the Castle, and begged me never to read it unless some solemn duty demands it. I sealed it with black ribbon and red wax before witnesses, so that neither of us shall be tempted. It is the first thing we have decided together."),
    "a3_j_wedding": dict(title="Mina Harker", source="Mina Harker's journal", text="We were married in the chapel of St Joseph, with Sister Agatha for a witness and an English priest for a voice. I am Mina Harker now. Jonathan does not remember his terror at the altar, but I do: he held my hand as if I were a rope over a pit."),
    "a3_j_vh_arrival": dict(title="Van Helsing", source="Dr. Seward's diary", text="He came as the clock struck seven, small, deliberate, with a leather case and a hundredweight of questions. One look at Lucy and he sent for blood. 'Let us not waste time on words, friend John. She needs blood, or she will die this night.'"),
    "a3_j_vh_exam": dict(title="The Professor's examination", source="Dr. Seward's diary", text="He examined her throat with a lens, her eyes with a candle, and her wrist with his watch. He asked what no physician asks: did she sleep with her window open, did she walk at night, did anything fly at the pane? Then he said: 'Arthur is her lover. His blood first.'"),
    "a3_j_garlic_rules": dict(title="The garlic", source="Dr. Seward's diary", text="He gave me flowers of garlic from Haarlem with the gravity of a priest giving the Host. 'The window. The door. The chimney. And a wreath for her neck, friend John. Do not laugh. It is medicine.' I did not laugh. I was, rather, afraid."),
    "a3_j_tx1": dict(title="The first transfusion", source="Dr. Seward's diary", text="Arthur's blood passed into Lucy and the colour came back to her face as dawn comes to a window. Van Helsing's hands never trembled. He told us afterward: 'Arthur must never know that any hand but his own gave her life. A husband has jealousies even for gifts.'"),
    "a3_j_night1": dict(title="The garlic has been moved", source="Dr. Seward's diary", text="At dawn the wreath lay on the floor, the garlic had been swept from the window-sill, the window itself was ajar. Lucy was white again and could say nothing. She had not rung. She had not stirred, and she does not remember."),
    "a3_j_sleepwalk": dict(title="Lucy walks in her sleep", source="Dr. Seward's diary", text="Garlic petals on the carpet from the bed to the window-seat; her slippers by the sill, wet with dew. Lucy herself undid the wards, asleep, and does not know it. Van Helsing is quite sure it is not her will but another's. We lock the door, pin the window, and watch."),
    "a3_j_tx2": dict(title="The second transfusion", source="Dr. Seward's diary", text="I gave my own blood this time. 'You are strong, friend John, and the secret is the more safe in a doctor's arm than a lover's.' The bed swam a little; brandy set it right. Arthur does not know. Lucy sleeps, and for an hour, so did I."),
    "a3_j_mother_removed": dict(title="The open window", source="Dr. Seward's diary", text="Mrs Westenra, whose kindness has done more harm than any wolf, found the flowers 'stuffy' and flung them out, and opened the windows to the dawn. We came back to a room cold as a cellar and a girl whom the night had emptied again. Van Helsing wept, and I saw him do it."),
    "a3_j_tx3": dict(title="The third transfusion", source="Dr. Seward's diary", text="Van Helsing gave his own blood, saying only: 'Devils or no devils, we fight him all the same.' He will not say who 'him' is. Lucy's cheek has a little rose in it; Mrs Westenra has promised on her honour to touch nothing in the room."),
    "a3_j_peace": dict(title="Four days of peace", source="Dr. Seward's diary", text="A box of garlic arrives each morning from Haarlem. Lucy eats a little, laughs a little, reads Arthur's letters aloud. Van Helsing sleeps in a chair with a hand on the door. Something flaps at the window each night. He says it is a bat. He does not say it with a smile."),
    "a3_j_wolf": dict(title="The wolf in the window", source="Dr. Seward's diary", text="At midnight the glass burst inwards, and a great grey wolf was on the bed. We drove it back, and it fled, howling, into the garden. Mrs Westenra rose to see, and her heart stopped at the sight. She fell across her daughter and lay still. Lucy lay under her in a swoon."),
    "a3_j_mother_dead": dict(title="Mrs Westenra", source="Dr. Seward's diary", text="She is dead. She had not slept since the shutters failed. A woman who had borne so much so lightly was killed by an animal's face at the window. The garlic that might have kept it out she herself had cleared away."),
    "a3_j_servants": dict(title="The drugged maids", source="Dr. Seward's diary", text="The maids lay insensible round the kitchen table, smelling of laudanum, and the decanter on the sideboard was left half-full. Van Helsing sniffed it and said nothing. This was not a drunkard's sleep. Someone wished to be undisturbed in that house."),
    "a3_j_tx4": dict(title="The fourth transfusion", source="Dr. Seward's diary", text="Quincey Morris came in, rumpled and weather-worn, and held out his arm before we could ask. 'A brave man's blood is the best thing on this earth when a woman is in trouble.' Four men have now given Lucy their blood. She sleeps; I do not."),
    "a3_j_lucy_death": dict(title="Lucy's last night", source="Dr. Seward's diary", text="Her breath is slow and snoring; her teeth look longer, the gums have drawn back. Arthur kissed her forehead at Van Helsing's word, and that was all. Between one breath and the next she was dead, and for a moment, lovelier than ever she had been."),
    "a3_j_teeth": dict(title="Her teeth", source="Dr. Seward's diary", text="Van Helsing drew her lip back with a finger. The canine teeth are longer and sharper than any I have seen in a living mouth. 'You have eyes, friend John. Remember this; remember it well.' He would say no more."),
    "a3_j_memo": dict(title="The paper at her breast", source="Dr. Seward's diary", text="Lucy's last memorandum was found against her heart: a scrap of a night's fear, 'Arthur, forgive me', in a hand that fails by the end of the page. Van Helsing read it twice and pocketed it. I asked him what it meant, and he answered: 'Another day.'"),
    "a3_j_zoo": dict(title="Berserker", source="Dr. Seward's diary", text="Mr. Bilder, keeper of the wolves, says Berserker is the gentlest great beast in the gardens, and that on the night of the storm he went mad, tore at the bars, and was gone by morning. A tall thin man had been watching him that evening, he says, with a hooked nose."),
    "a3_j_burial": dict(title="Rain on the yews", source="Dr. Seward's diary", text="The coffin went down an hour ago. The clergyman has gone; the mourners have gone to the carriages; and the Professor has not moved from the vault door. I have never seen a man look so little like a mourner and so much like a sentry."),
    "a3_j_funeral": dict(title="Kingstead", source="Dr. Seward's diary", text="We laid her in the Westenra vault. Arthur wept like a boy; Quincey wept like a man; I did neither, and shall, I think, hereafter. Van Helsing stood at the door and said, 'It is not finished.' I did not ask him what he meant."),
}

ENEMIES_EXTRA = {
    "a3_berserker": dict(name="Berserker", model="wolf_big", hp=24, spd=6, dmg=[4, 7], acc=72, eva=10, tags=["beast"], flee_at=0.2, nerve_hit=2,
                         book="the escaped wolf of the Zoological Gardens, ch.11"),
}
ENCOUNTERS_EXTRA = {
    "a3_berserker_night": dict(name="The wolf in Lucy's room", time="night", enemies=["a3_berserker"], flee_ok=False,
                               intro="The window bursts inward. A great grey wolf lands on the carpet, between us and the bed.",
                               win="The wolf yelps, and is gone through the glass into the dark.", location="a3_lucy_bedroom"),
    "a3_renfield_struggle": dict(name="Renfield in his cell", time="night", enemies=["renfield"], flee_ok=True,
                                 intro="Renfield flings himself at me with a madman's strength, snarling about lives and masters.",
                                 win="Hennessey and I pin him until he is quiet.", location="a3_renfield_cell"),
}
ENCOUNTER_HOOKS = {
    "a3_berserker_night": dict(
        on_win=[{"set": "a3_wolf_down"}, {"journal": "a3_j_wolf"}, {"journal": "a3_j_mother_dead"},
                say("The wolf is gone. Mrs Westenra lies across her daughter's bed, her hand at her heart. Lucy has not stirred.")],
        on_lose=[{"set": "a3_wolf_down"}, {"journal": "a3_j_wolf"}, {"journal": "a3_j_mother_dead"},
                 say("I come to on the carpet with a bruised head. The wolf is gone. Mrs Westenra lies dead across her daughter, and Van Helsing is already bending over them.")],
        on_flee=[{"set": "a3_wolf_down"}, {"journal": "a3_j_wolf"}, {"journal": "a3_j_mother_dead"},
                 say("We scatter. The wolf, having smashed what it came to smash, is gone. In the silence we find Mrs Westenra dead on the bed beside her daughter.")]),
    "a3_renfield_struggle": dict(
        on_win=[{"set": "a3_renfield_calm"}, {"set": "a3_fought_renfield"}, {"journal": "a3_j_sedated"},
                say("He lies quiet at last, panting, and I have the cut on my hand to remember it by.")],
        on_lose=[{"set": "a3_renfield_calm"}, {"set": "a3_fought_renfield"}, {"journal": "a3_j_sedated"},
                 say("Hennessey and two attendants carry me out and the attendants hold Renfield down. By evening he is quiet.")],
        on_flee=[{"set": "a3_renfield_calm"}, {"set": "a3_fought_renfield"}, {"journal": "a3_j_sedated"},
                 say("I get the door shut between us. Hennessey fetches two attendants, and Renfield is quieted in the end by sheer weariness.")]),
}

PLACEMENTS = {
    "a3_dispensary_key": [
        dict(prop="a3_study_desk", text="In the false back of my own desk drawer: the dispensary key, where I hid it from myself.", hint="The drawer is a half-inch shallower than it should be."),
        dict(prop="a3_study_shelf", text="Behind Lombroso, where I put it last Thursday: the little brass dispensary key.", hint="One volume has been pushed forward from the rest."),
        dict(prop="a3_study_mantel", text="Under the mantel clock, on a scrap of blotting-paper: the dispensary key.", hint="The mantel clock sits crooked, on something small."),
    ],
    "a3_transfusion_kit": [
        dict(prop="a3_study_chest", text="My transfusion kit, in its black bag, at the bottom of the instrument chest where it has lain since Edinburgh.", hint="The chest is lighter than a locked chest should be."),
        dict(prop="a3_ward_trunk", text="Under a pile of clean linen in the ward trunk: my black bag with the silver tubing.", hint="The trunk lid does not shut; something black is under the linen."),
        dict(prop="a3_garden_shed", text="At the back of the gardener's shed, wrapped in sacking: my black bag. Hennessey must have stowed it.", hint="There is a black corner of leather under a sack."),
    ],
    "a3_window_pin": [
        dict(prop="a3_h_shed", text="Hanging on a nail in the potting-shed: a stout iron pin with a ring head.", hint="Among the rakes, an iron rod shines like a new coin."),
        dict(prop="a3_umbrella_stand", text="Thrust in among the umbrellas: an iron pin from some old shutter.", hint="One 'umbrella' is straighter and colder than the others."),
        dict(prop="a3_h_bench", text="Under the potting-bench, an iron pin with a ring head.", hint="Something metallic glints between the bench and the wall."),
    ],
}
GATES = {
    "a3_door_cell": [
        dict(cond="flag:a3_met_hennessey", fail="I should speak to Hennessey before I go in alone to a man like that.", needs="a3_dispensary_key"),
        dict(cond="flag:a3_met_hennessey&has:a3_dispensary_key", fail="Hennessey has the other key, and the sense not to let me in without a word.", needs="a3_dispensary_key"),
    ],
}
PALETTES = {
    "a3_asylum_study": [dict(wall="plaster", floor="planks", wood="dark", cloth="green"),
                        dict(wall="plaster_dirty", floor="planks", wood="oak", cloth="blue"),
                        dict(wall="stone_grey", floor="planks", wood="ebony", cloth="red")],
    "a3_hillingham_hall": [dict(wall="plaster", floor="planks", wood="pale", cloth="red"),
                           dict(wall="plaster", floor="planks", wood="oak", cloth="blue")],
    "a3_lucy_bedroom": [dict(wall="plaster", floor="planks", wood="pale", cloth="blue"),
                        dict(wall="plaster", floor="planks", wood="pale", cloth="green")],
    "a3_buda_hospital": [dict(wall="plaster", floor="planks", wood="pale", cloth="cream"),
                         dict(wall="plaster_dirty", floor="planks", wood="oak", cloth="cream")],
}


# =============================================================================================================
# LOCATIONS
# =============================================================================================================
LOC_DATA = {}

# ---------------------------------------------------------------- 1. Seward's study (start)
LOC_DATA["a3_asylum_study"] = dict(
    cells=[2, 2], interior=True, wall="plaster", floor="planks",
    ambient=AMBIENT["warm_day_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2]),
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[2.4, 1.6], spawns={"a3_asylum_ward": [2.6, 2.0]},
    props=[
        prop("a3_study_desk", "table", "dark", -1.6, -1.8, name="My desk", radius=0.9,
             look="Case-books, a blotter, a green-shaded lamp. A drawer that has seen better locks."),
        prop("a3_phonograph", "a3_phonograph", "oak", -1.6, -1.8, y=0.8, name="Phonograph", radius=0.3,
             look="Edison's wax-cylinder phonograph. My diary speaks aloud now, and sometimes disagrees with me.", talk="a3_phonograph"),
        prop("a3_study_chair", "chair", "green", -1.6, -0.8, rot=180, name="Desk chair", radius=0.4,
             look="My chair. The leather is worn to the shape of long nights."),
        prop("a3_ledger_table", "table", "pale", 1.8, -2.4, name="Reading table", radius=0.8,
             look="A small table under the window, piled with ledgers."),
        prop("a3_ledger", "book", "red", 1.8, -2.4, y=0.8, name="Case ledger", radius=0.2,
             look="The asylum case-ledger. Dosages, weights, observations.", talk="a3_case_ledger"),
        prop("a3_notes_table", "table", "dark", -2.2, 1.6, name="Side table", radius=0.7,
             look="Where I sort what I have found, before I let myself conclude anything."),
        prop("a3_case_notes", "book", "leather", -2.2, 1.6, y=0.8, name="Renfield: working notes", radius=0.2,
             look="My working notes on Renfield. I will set down what I have gathered, and decide.", talk="a3_case_notes"),
        prop("a3_study_shelf", "bookshelf", "dark", 2.2, -3.4, name="Medical shelf", radius=0.8,
             look="Lombroso, Esquirol, Maudsley, Bucknill and Tuke. A row of sensible men who did not meet Renfield."),
        prop("a3_study_mantel", "fireplace", "stone_grey", -3.4, 0.0, rot=90, name="Fireplace", radius=0.9,
             look="A banked fire, a mantel clock, a photograph of Lucy I should not have kept so near."),
        prop("a3_study_chest", "chest", "dark", -3.2, -3.0, rot=90, name="Instrument chest", radius=0.6,
             look="An old campaign chest of instruments I rarely need."),
        prop("a3_bust", "bust", "plaster", 3.0, -1.2, rot=-90, name="Plaster bust", radius=0.3,
             look="Hippocrates, chipped on the nose. He has heard everything I have said into the phonograph, and has not judged."),
        prop("a3_study_lamp", "lantern", "default", 1.8, -2.4, y=0.8, name=None, radius=0.1),
        prop("a3_study_candle", "candelabra", "default", 0.2, -3.0, name="Candelabra", radius=0.3,
             look="Three candles, for the nights the gas gives out."),
        prop("a3_study_rug", "rug", "red", 0.2, 0.4, radius=0.01),
        prop("a3_study_window_sill", "bottle", "green", 0.4, -3.3, y=0.9, name="Green bottle", radius=0.1,
             look="Laudanum, labelled, locked up in spirit if not in fact. I keep it on the sill so I will not forget the danger."),
        prop("a3_door_ward", "door", "dark", 3.8, 2.0, rot=-90, name="Door to the ward", radius=0.6,
             look="The passage to the ward and the dispensary.", go="a3_asylum_ward"),
    ],
    npcs=[
        npc("a3_hennessey", "human_harker", "travel", 0.6, 0.8, rot=200, name="Dr. Hennessey",
            look="My assistant, brisk and tired, with a stethoscope round his neck and a rumpled Irish smile.", talk="a3_hennessey"),
    ],
    on_enter=[dict(do=[{"journal": "a3_j_seward_diary"}, say("2 September. Renfield has been loud all night, Lucy's name is in every letter, and I have not eaten. The phonograph, at least, never asks how I feel.")], once=True)],
)

# ---------------------------------------------------------------- 2. the ward
LOC_DATA["a3_asylum_ward"] = dict(
    cells=[3, 2], interior=True, wall="plaster_dirty", floor="stone_grey",
    ambient=AMBIENT["cold_interior"], camera=cam([3, 2]), lights=lights_warm([3, 2], n=3, energy=2.2),
    walls=dict(north=["wall_4", "wall_door_4", "wall_4"], west=["wall_4", "wall_door_4"], east=["wall_door_4", "wall_4"]),
    spawn=[-4.6, 2.0], spawns={"a3_asylum_study": [-4.6, 2.0], "a3_renfield_cell": [0, -2.6], "a3_asylum_garden": [4.6, -2.0]},
    props=[
        prop("a3_door_study", "door", "dark", -5.8, 2.0, rot=90, name="Door to my study", radius=0.6,
             look="My study, where the phonograph waits.", go="a3_asylum_study"),
        prop("a3_door_cell", "door", "ebony", 0.0, -3.8, name="Renfield's door", radius=0.6,
             look="A heavy oak door with a barred grille at the height of a face. Something moves behind it, and counts.",
             go="a3_renfield_cell", go_cond="flag:a3_met_hennessey", go_fail="I should speak to Hennessey before I go in alone to a man like that."),
        prop("a3_door_garden", "door", "dark", 5.8, -2.0, rot=-90, name="Door to the grounds", radius=0.6,
             look="The garden door, with a little daylight under it.", go="a3_asylum_garden"),
        prop("a3_cabinet", "bookshelf", "ebony", -3.6, -3.4, name="Dispensary cabinet", radius=0.8,
             look="The poison cabinet: chloral, morphia, laudanum, and my one decent brandy. It is locked, and I am the guard.",
             use_item={"a3_dispensary_key": [{"give": "a3_chloral_crystals"},
                                              {"give": "brandy"}, {"set": "a3_cabinet_open"},
                                              say("The key turns. I take the stock bottle of chloral crystals and a flask of brandy, leaving the morphia where it is.")]},
             use_fail="That will not open it. It wants the little brass key marked D."),
        prop("a3_scales", "table", "pale", -1.8, -1.6, name="Weighing table", radius=0.7,
             look="Hennessey weighs the patients here. A strip of chalk reads: 'R. - 9 st. 4 lb. (down 11 lb.)'. He eats nothing at table."),
        prop("a3_mix_table", "table", "oak", 2.6, -1.6, name="Dispensing bench", radius=0.8,
             look="Scales, a graduated glass and a brass measure. Here I weigh out what sends men to sleep.", talk="a3_mix_dose"),
        prop("a3_mix_bottle", "bottle", "glass", 2.6, -1.6, y=0.8, name=None, radius=0.1),
        prop("a3_basin", "barrel", "dark", 4.4, -3.2, name="Water butt", radius=0.45,
             look="Clean rainwater from the roof, with a tin dipper. Good enough for a draught.", talk="a3_basin"),
        prop("a3_ward_trunk", "chest", "oak", -4.8, 1.0, rot=90, name="Linen trunk", radius=0.6,
             look="Clean sheets for the beds. The lid does not sit quite flat."),
        prop("a3_ward_bench", "bench", "dark", 3.0, 2.4, name="Visitors' bench", radius=0.6,
             look="A bench no one sits on for long."),
        prop("a3_ward_lamp", "lantern", "default", -2.4, 2.4, name="Lamp", radius=0.3,
             look="An oil lamp, trimmed and lit, with a wire guard."),
        prop("a3_ward_cross", "crucifix_big", "default", 2.2, -3.6, y=1.2, name="Crucifix", radius=0.3,
             look="Some patients ask for it and some are quieter without it. We keep it."),
        prop("a3_ward_runner", "rug", "black", 0.0, 0.4, radius=0.01),
        prop("a3_ward_sconce", "sconce", "default", -5.5, -1.0, rot=90, y=1.6, radius=0.1),
    ],
    npcs=[
        npc("a3_dobbs", "human_peasant_m", "villager", -0.8, 1.6, rot=160, name="Dobbs the attendant",
            look="A square, patient attendant in a white coat, with keys at his belt and his hat in his hand.", talk="a3_dobbs"),
    ],
)

# ---------------------------------------------------------------- 3. Renfield's cell
LOC_DATA["a3_renfield_cell"] = dict(
    cells=[2, 2], interior=True, wall="plaster_dirty", floor="stone_dark",
    ambient=AMBIENT["cold_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2], n=2, energy=1.6),
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[2.4, 1.6], spawns={"a3_asylum_ward": [2.6, 2.0]},
    props=[
        prop("a3_cell_door", "door", "ebony", 3.8, 2.0, rot=-90, name="Door to the ward", radius=0.6,
             look="The cell door, with a grille on the corridor side only.", go="a3_asylum_ward"),
        prop("a3_cell_window", "fence", "default", -2.0, -3.6, name="Barred window", radius=0.7,
             look="Iron bars, painted so often they are fat with paint. Through them, Carfax's chimneys show black against the sky."),
        prop("a3_cot", "bed_simple", "blue", -2.6, 0.8, rot=90, name="Iron cot", radius=0.9,
             look="A cot, a blanket, a neatly folded sheet. The pillow is lumpy: it has been slit and sewn up again with fishing-twine.",
             take="a3_sugar_lumps", take_text="Inside the pillow, wrapped in a handkerchief: a dozen lumps of sugar, hoarded from his tea.", give_once=True),
        prop("a3_cell_table", "table", "dark", 1.2, -2.2, name="Little table", radius=0.7,
             look="A deal table scrubbed white. On it the evidence of an industry."),
        prop("a3_cell_jar", "bottle", "glass", 0.7, -2.2, y=0.8, scale=2.5, name="Jam-jar", radius=0.35,
             look="Forty bluebottles in a jam-jar, bumbling against the muslin.",
             take="a3_fly_jar", take_text="I lift the jar. Forty flies, and every one of them counted.", give_once=True),
        prop("a3_cell_notebook", "book", "leather", 1.7, -2.2, y=0.8, scale=2.5, name="Notebook", radius=0.35,
             look="A school exercise book filled with rows of figures and little crosses.",
             take="a3_renfield_notebook", take_text="Flies; spiders; sparrows. Each total is added with a flourish. I take the notebook.", give_once=True),
        prop("a3_spider_chest", "chest", "oak", 2.7, -0.6, rot=-90, scale=0.6, name="Wooden box", radius=0.4,
             look="A shallow deal box with a sliding lid. Something dry rustles inside.",
             take="a3_spider_box", take_text="A box of fat spiders, each in its own cardboard cell like a lodger. I take it.", give_once=True),
        prop("a3_cell_sparrow", "bat", "brown", -0.4, -1.4, y=0.1, scale=0.45, name="Tame sparrow", radius=0.3,
             look="A sparrow hops on the flagstones, quite unafraid of a man who has been feeding it spiders."),
        prop("a3_cell_stool", "chair", "blue", 0.6, 1.4, rot=180, name="Stool", radius=0.35, look="A bolted-down stool."),
        prop("a3_cell_bucket", "barrel", "dark", -3.0, -2.6, scale=0.7, name="Bucket", radius=0.3, look="A bucket. The least interesting thing in the room."),
        prop("a3_cell_lamp", "sconce", "default", 3.5, -1.2, rot=-90, y=1.6, radius=0.1),
        prop("a3_cell_rug", "rug", "black", 0.0, 0.6, scale=0.8, radius=0.01),
    ],
    npcs=[
        npc("a3_renfield_wild", "human_renfield", "asylum", 0.2, 0.2, rot=180, name="Renfield", radius=0.6, cond="!a3_renfield_calm",
            look="He crouches by the wall, muttering numbers, his eyes fixed on a point just behind my head. He is thin as a rake and awake as a lamp.",
            fight="a3_renfield_struggle",
            use_item={"chloral": [{"set": "a3_renfield_calm"}, {"set": "a3_sedated_safely"}, {"journal": "a3_j_sedated"},
                                  say("I speak quietly, hold out the glass, and he drinks it as a child drinks medicine. In ten minutes he is sitting on the cot, calm, and ready to talk.")]},
            use_fail="That will not calm him."),
        npc("a3_renfield_talk", "human_renfield", "asylum", 0.2, 0.2, rot=180, name="Renfield", radius=0.6, cond="a3_renfield_calm",
            look="Renfield, sitting quietly on the cot with his hands between his knees. He looks like a clerk, which he once was.", talk="a3_renfield_talk"),
    ],
    on_enter=[{"if": "!a3_renfield_calm", "do": [say("He has heard me in the corridor. The counting stops. Then it begins again, much faster.")]}],
)

# ---------------------------------------------------------------- 4. the asylum grounds
LOC_DATA["a3_asylum_garden"] = dict(
    cells=[3, 3], interior=False, wall="dirt", floor="grass",
    ambient=AMBIENT["day_exterior"], camera=cam([3, 3]), lights=lights_day(),
    walls=dict(west=["wall_4", "wall_door_4", "wall_4"]),
    scatter=dict(asset="pine", variant="green", count=22, seed=7, avoid=[[-7, -7, 7, 7]]),
    scatter2=dict(asset="rock", variant="mossy", count=6, seed=3, avoid=[[-7, -7, 7, 7]]),
    spawn=[-4.4, 0.0], spawns={"a3_asylum_ward": [-4.6, 0.0]},
    props=[
        prop("a3_garden_door", "door", "dark", -5.8, 0.0, rot=90, name="Door to the ward", radius=0.6,
             look="The ward door, painted the grey of institutions.", go="a3_asylum_ward"),
        prop("a3_carfax", "castle_keep", "stone_dark", 0, -12.0, name="Carfax", radius=0.01,
             look="Carfax: the old house next door, shut up, tumbledown, sold lately to a foreigner by Mr Hawkins's firm. It is nearer than I should like."),
        prop("a3_garden_shed", "chest", "dark", -3.4, -4.4, scale=1.4, name="Garden shed", radius=0.9,
             look="The gardener's shed. A row of hooks, a smell of earth and creosote."),
        prop("a3_toolbox", "chest", "oak", -1.4, -4.6, scale=0.8, name="Toolbox", radius=0.4,
             look="Pocock's toolbox, with the lid propped by a trowel.",
             take="hammer", take_text="A good claw hammer. I take it, and leave the nails.", give_once=True),
        prop("a3_loose_slat", "fence", "default", 4.2, -4.8, name="Loose slat in the wall", radius=0.7,
             look="One slat of the boundary fence swings on a single nail. Through the gap, long grass, a worn track leading to the garden of Carfax.",
             set="a3_saw_slat", set_text="A man could squeeze through here, if he were thin and determined.",
             use_item={"hammer": [{"set": "a3_fence_mended"}, {"journal": "a3_j_fence"},
                                  say("Three nails, and the slat is as firm as the wall. Whatever walked this track will have to find another door.")]},
             use_fail="A hammer would do it, if I had one."),
        prop("a3_garden_bench", "bench", "oak", 0.0, -2.4, rot=0, name="Garden bench", radius=0.7,
             look="A bench in the sun, facing the high wall. Convalescent patients sit here when they are well enough to be bored."),
        prop("a3_garden_sparrows", "bat", "brown", -1.8, -0.2, y=0.1, scale=0.4, name="Sparrows", radius=0.4,
             look="Sparrows on the gravel, plump as aldermen. One of them hops closer, as if it had been fed by a gentleman."),
        prop("a3_cab_hillingham", "carriage", "ebony", 4.0, 1.6, rot=-70, name="Hansom for Hampstead", radius=1.6,
             look="A hansom with a tired grey horse. The driver wants to know which road.",
             go="a3_hillingham_hall", go_cond="has:a3_arthur_telegram&flag:a3_diet_solved",
             go_fail="I cannot leave while Renfield is a puzzle I have not worked out, and while Arthur's message has not come."),
        prop("a3_cab_zoo", "carriage", "dark", 4.2, 4.4, rot=-70, name="Cab to the Zoological Gardens", radius=1.6,
             look="A four-wheeler hired for the afternoon. 'The Zoo, sir? Regent's Park, an hour or so.'", go="a3_zoo_gardens"),
        prop("a3_garden_fence1", "fence", "default", 0.0, 5.4, radius=0.01),
        prop("a3_garden_fence2", "fence", "default", 3.0, 5.4, radius=0.01),
        prop("a3_garden_fence3", "fence", "default", -3.0, 5.4, radius=0.01),
        prop("a3_garden_lantern", "lantern", "default", -4.2, 3.2, name="Garden lamp", radius=0.3, look="A gas lamp on an iron standard."),
    ],
    npcs=[
        npc("a3_pocock", "human_peasant_m", "villager", -2.6, -2.8, rot=40, name="Pocock the gardener",
            look="The head gardener, with hands like roots and a face that has seen weather and patients alike.", talk="a3_pocock"),
        npc("a3_boy_asylum", "human_peasant_m", "innkeeper", -2.0, 2.4, rot=20, name="Telegraph boy", cond="a3_renfield_calm", radius=0.4,
            look="A boy in a pillbox cap, red from running, with a buff envelope held out in front of him like a tray.", talk="a3_boy_asylum"),
    ],
)

# ---------------------------------------------------------------- 5. the Zoological Gardens (optional)
LOC_DATA["a3_zoo_gardens"] = dict(
    cells=[3, 3], interior=False, wall="dirt", floor="grass",
    ambient=AMBIENT["dusk_exterior"], camera=cam([3, 3]), lights=lights_day(2.6),
    scatter=dict(asset="pine", variant="dark", count=18, seed=21, avoid=[[-7, -7, 7, 7]]),
    spawn=[4.4, 3.0], spawns={"a3_asylum_garden": [4.4, 3.0]},
    props=[
        prop("a3_zoo_sign", "signpost", "dark", 3.6, 4.4, rot=-30, name="Signpost", radius=0.3,
             look="'Zoological Gardens. Carnivora: left. Pachyderms: right. Visitors are requested not to tease the animals.'"),
        prop("a3_wolf_cage_1", "fence", "default", -3.0, -4.6, radius=0.01),
        prop("a3_wolf_cage_2", "fence", "default", -0.5, -4.6, radius=0.01),
        prop("a3_wolf_cage_3", "fence", "default", 2.0, -4.6, radius=0.01),
        prop("a3_wolf_cage_side", "fence", "default", -4.6, -3.0, rot=90, radius=0.01),
        prop("a3_cage_bars", "fence", "default", -1.4, -3.4, name="Bent bars", radius=0.7,
             look="Two bars of the wolves' cage are bent outward, like grass in a flood. A wolf did not do this alone."),
        prop("a3_keeper_table", "table", "pale", 3.2, -1.4, name="Keeper's table", radius=0.7,
             look="A plain table outside Mr Bilder's cottage. Tea, a mug, and a folded newspaper."),
        prop("a3_gazette_cutting", "book", "leather", 3.2, -1.4, y=0.8, name="Pall Mall Gazette", radius=0.15,
             look="'An Escaped Wolf'. The paper is already soft from the keeper's thumb.",
             take="a3_gazette_cutting", take_text="Mr Bilder says I may have the cutting. 'Better you than the Missus, who reads it aloud.'", give_once=True),
        prop("a3_zoo_bench", "bench", "oak", -3.6, 2.4, name="Bench", radius=0.6, look="A bench with a view of the wolves and no wolves in it."),
        prop("a3_zoo_hay", "barrel", "oak", 4.6, -3.6, scale=1.1, name="Hay barrel", radius=0.4, look="Straw for the cages."),
        prop("a3_zoo_lamp", "lantern", "default", 0.8, 3.2, name="Gas lamp", radius=0.3, look="A gas lamp not yet lit."),
        prop("a3_zoo_cab", "carriage", "dark", 4.6, 5.0, rot=-80, name="Cab to Purfleet", radius=1.6,
             look="My cab, waiting for the return to the asylum.", go="a3_asylum_garden"),
        prop("a3_zoo_rock", "rock_big", "mossy", -5.4, -1.0, radius=0.01),
    ],
    npcs=[
        npc("a3_bilder", "human_peasant_m", "innkeeper", 2.2, -0.2, rot=-60, name="Mr. Bilder, keeper", radius=0.5,
            look="A stout keeper in a flat cap, smelling of straw and wintergreen. He has the manner of a man much interviewed.", talk="a3_bilder"),
        npc("a3_mrs_bilder", "human_peasant_f", "village_woman", 3.8, -2.6, rot=-110, name="Mrs. Bilder", radius=0.4,
            look="The keeper's wife on her step, with her arms folded and her opinions plain.", talk="a3_mrs_bilder"),
        npc("a3_berserker_cage", "wolf_big", "grey", -1.6, -5.4, rot=0, name="Berserker's cage", radius=0.8,
            look="A great grey wolf paces his cage, back and forth, back and forth, with his eyes on the north.", talk="a3_berserker_look"),
    ],
    on_enter=[dict(do=[{"journal": "a3_j_zoo"}, say("A great grey wolf is pacing a cage in the afternoon sun, and the keepers look like men who have not slept.")], once=True)],
)


# ---------------------------------------------------------------- 6. Buda-Pesth: the hospital (Mina)
LOC_DATA["a3_buda_hospital"] = dict(
    cells=[2, 3], interior=True, wall="plaster", floor="planks",
    ambient=AMBIENT["warm_day_interior"], camera=cam([2, 3]), lights=lights_warm([2, 3], n=3, energy=2.0),
    walls=dict(north=["wall_window_4", "wall_4"], west=["wall_4", "wall_4", "wall_4"], east=["wall_4", "wall_door_4", "wall_4"]),
    spawn=[2.4, 4.0], spawns={"a3_buda_chapel": [2.6, 0.0]},
    props=[
        prop("a3_h_door_chapel", "door", "pale", 3.8, 0.0, rot=-90, name="Door to the chapel", radius=0.6,
             look="A plain door, and beyond it the sound of someone setting out candles.", go="a3_buda_chapel"),
        prop("a3_cot_a", "bed_simple", "green", -2.6, -4.0, rot=90, name="Empty cot", radius=0.9, look="A made-up cot, white as a bandage."),
        prop("a3_cot_b", "bed_simple", "green", -2.6, -1.4, rot=90, name="Cot", radius=0.9, look="A sleeping patient, an old man with a rosary round his wrist."),
        prop("a3_jonathan_bed", "bed_simple", "blue", -2.6, 1.6, rot=90, name="Jonathan's bed", radius=0.9,
             look="The corner bed. A blanket is drawn up to the chin of the thinnest, whitest man I have ever loved."),
        prop("a3_cot_d", "bed_simple", "green", -2.6, 4.2, rot=90, name="Cot", radius=0.9, look="Empty. The sister has put a sprig of box on the pillow."),
        prop("a3_sister_desk", "table", "pale", 2.4, -4.2, name="Sister's desk", radius=0.8,
             look="A small desk with a lamp, a ledger and a rosary. The ledger records every patient's fever to the quarter-degree."),
        prop("a3_sealing_wax", "candle", "red", 2.0, -4.0, y=0.8, scale=2.5, name="Stick of wax", radius=0.35,
             look="A stick of red sealing wax and a taper beside it.",
             take="a3_sealing_wax", take_text="I take the wax. Sister Agatha nods; it is for a good cause.", give_once=True),
        prop("a3_sister_letter", "book", "leather", 2.9, -4.2, y=0.8, name="Letter", radius=0.15,
             look="The letter that brought me here, left under the lamp.",
             take="a3_sister_letter", take_text="I fold Sister Agatha's letter into my bag. I shall want it, one day, to show him how it was.", give_once=True),
        prop("a3_sewing", "chest", "pale", 3.0, -1.8, rot=-90, scale=0.7, name="Sewing-basket", radius=0.5,
             look="A sister's sewing-basket: thread, thimbles, scraps of black ribbon for shrouds.",
             take="a3_ribbon", take_text="I take a length of black ribbon from the basket.", give_once=True),
        prop("a3_seal_table", "table", "oak", 0.6, 2.4, name="Writing table", radius=0.8,
             look="A clean little table near the window, ink, paper, and room enough for a decision.", talk="a3_seal_table",
             use_item={"a3_harker_diary": [{"set": "a3_diary_on_table"}, say("I lay Jonathan's journal on the table. A little black book, held shut with an elastic band.")],
                       "a3_ribbon": [{"set": "a3_ribbon_ready"}, say("I lay the black ribbon beside the book.")],
                       "a3_sealing_wax": [{"set": "a3_wax_ready"}, say("I set the wax and taper beside the ribbon.")]},
             use_fail="That is not what I need for this table."),
        prop("a3_coat_chair", "chair", "blue", -0.4, 2.2, rot=90, name="Jonathan's coat", radius=0.4,
             look="A man's threadbare coat is over the chair-back, with a waistcoat folded beneath it. The waistcoat pocket is lumpy.",
             take="a3_wedding_ring", take_text="In the waistcoat pocket, a few coins, a ticket and a plain gold ring wrapped in a handkerchief. He bought it before the Castle. I take it.", give_once=True),
        prop("a3_mina_trunk", "chest", "dark", 1.0, 4.4, rot=0, scale=0.9, name="My trunk", radius=0.5,
             look="My travelling trunk, still strapped. I have brought one good dress, in case."),
        prop("a3_h_cross", "crucifix_big", "default", -0.2, -5.0, y=1.0, name="Crucifix", radius=0.3,
             look="A crucifix over the sister's desk. The ward is quiet beneath it."),
        prop("a3_h_candle", "candelabra", "default", 1.4, 0.8, name="Candelabra", radius=0.3, look="Three candles for the night nurse."),
        prop("a3_h_rug", "rug", "cream", 0.2, -1.2, radius=0.01),
        prop("a3_h_basin", "barrel", "pale", 3.3, 3.6, scale=0.7, name="Basin", radius=0.3, look="A basin of cool water and a folded cloth."),
    ],
    npcs=[
        npc("a3_agatha", "human_mina", "nurse", 1.2, -2.2, rot=200, name="Sister Agatha", radius=0.5,
            look="A tall, quiet Sister of St Joseph, with a calm face, an English that is better than mine is German, and a hand like a bird's.", talk="a3_agatha"),
        npc("a3_jonathan_hosp", "human_harker", "harker", -1.4, 1.6, rot=90, name="Jonathan", radius=0.5,
            look="Jonathan, in a hospital shirt, his hair gone white. He is sitting up, which is more than the doctors promised.", talk="a3_jonathan_hosp"),
        npc("a3_sister_maria", "human_peasant_f", "village_woman", 2.4, 3.0, rot=180, name="Sister Maria", radius=0.4,
            look="A young Hungarian sister folding sheets with great severity.", talk="a3_sister_maria"),
    ],
    on_enter=[dict(do=[{"journal": "a3_j_mina_hospital"},
                       say("24 August. Buda-Pesth. I am Mina Murray no longer in my own mind; I am just the girl who came across Europe after a letter.")], once=True)],
)

# ---------------------------------------------------------------- 7. the chapel (wedding)
LOC_DATA["a3_buda_chapel"] = dict(
    cells=[2, 2], interior=True, wall="stone_tomb", floor="planks",
    ambient=AMBIENT["candle_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2], n=3, energy=2.6),
    walls=dict(north=["wall_4", "wall_window_4"], west=["wall_4", "wall_door_4"], east=["wall_4", "wall_4"]),
    spawn=[-2.6, 2.0], spawns={"a3_buda_hospital": [-2.6, 2.0]},
    props=[
        prop("a3_c_door", "door", "pale", -3.8, 2.0, rot=90, name="Door to the ward", radius=0.6,
             look="Back to the ward and the corner bed.", go="a3_buda_hospital"),
        prop("a3_altar", "table", "dark", 0.0, -2.8, name="Altar", radius=0.9,
             look="A plain altar-table with a white cloth, two candles, and a missal open to the marriage service."),
        prop("a3_altar_cross", "crucifix_big", "silver", 0.0, -2.8, y=0.8, name="Silver crucifix", radius=0.2,
             look="A small silver crucifix. It is Hungarian and old and the face on it is kind."),
        prop("a3_c_candle1", "candelabra", "default", -1.8, -2.4, name="Candelabrum", radius=0.3, look="Candles for a wedding in the afternoon."),
        prop("a3_c_candle2", "candelabra", "default", 1.8, -2.4, name="Candelabrum", radius=0.3, look="Candles for a wedding in the afternoon."),
        prop("a3_c_bench1", "bench", "dark", -1.2, 0.0, rot=90, name="Bench", radius=0.8, look="A worn pew."),
        prop("a3_c_bench2", "bench", "dark", 1.2, 0.0, rot=90, name="Bench", radius=0.8, look="A worn pew."),
        prop("a3_c_bench3", "bench", "dark", -1.2, 1.8, rot=90, name="Bench", radius=0.8, look="A worn pew."),
        prop("a3_c_bench4", "bench", "dark", 1.2, 1.8, rot=90, name="Bench", radius=0.8, look="A worn pew."),
        prop("a3_c_rug", "rug", "red", 0.0, -1.2, scale=0.9, radius=0.01),
        prop("a3_c_font", "barrel", "pale", 3.0, 2.6, scale=0.55, name="Holy-water stoup", radius=0.3, look="A stone stoup of holy water."),
        prop("a3_c_sconce", "sconce", "default", 3.5, -0.4, rot=-90, y=1.6, radius=0.1),
    ],
    npcs=[
        npc("a3_priest", "human_peasant_m", "villager", 0.0, -1.2, rot=0, name="Father Hermann", radius=0.5,
            look="An English-speaking priest in a worn white surplice, with ink on his thumb. He has agreed to this at two hours' notice.", talk="a3_priest"),
        npc("a3_jonathan_chapel", "human_harker", "harker", 1.2, -0.4, rot=-30, name="Jonathan", radius=0.5, cond="a3_diary_sealed",
            look="Jonathan, steadied between two orderlies' chairs. He has combed what is left of his hair.", talk="a3_jonathan_chapel"),
        npc("a3_agatha_chapel", "human_mina", "nurse", -1.4, -0.4, rot=30, name="Sister Agatha", radius=0.5, cond="a3_diary_sealed",
            look="Sister Agatha, who has agreed to be the witness for the sake of two strangers and a miracle.", talk="a3_agatha_chapel"),
    ],
)

# ---------------------------------------------------------------- 8. Hillingham hall
LOC_DATA["a3_hillingham_hall"] = dict(
    cells=[3, 2], interior=True, wall="plaster", floor="planks",
    ambient=AMBIENT["warm_day_interior"], camera=cam([3, 2]), lights=lights_warm([3, 2], n=3, energy=2.4),
    walls=dict(north=["wall_door_4", "wall_window_4", "wall_4"], west=["wall_4", "wall_4"], east=["wall_door_4", "wall_4"]),
    spawn=[4.6, -1.4], spawns={"a3_lucy_bedroom": [-4.0, -2.6], "a3_hillingham_garden": [4.6, -1.4], "a3_buda_chapel": [4.6, -1.4]},
    props=[
        prop("a3_door_bedroom", "door", "pale", -4.0, -3.8, name="Stairs to Lucy's room", radius=0.6,
             look="The stairs up to Lucy's room. A faint smell of lavender, and of something older.",
             go="a3_lucy_bedroom", go_cond="flag:a3_met_mother", go_fail="Mrs Westenra expects me to speak to her first. It would be a rudeness to go up like a tradesman."),
        prop("a3_door_hall_garden", "door", "pale", 5.8, -2.0, rot=-90, name="Door to the garden", radius=0.6,
             look="The garden door, ajar, with the hum of evening bees behind it.", go="a3_hillingham_garden"),
        prop("a3_clock", "a3_clock", "oak", 4.2, -3.3, name="Long-case clock", radius=0.5,
             look="A tall clock that ticks like a pulse. It says a quarter to seven, and the post-office closes at eight."),
        prop("a3_hall_desk", "table", "pale", -1.8, -2.4, name="Writing desk", radius=0.8,
             look="Mrs Westenra's writing desk: crested paper, pen and ink, a bundle of Lucy's old Whitby postcards."),
        prop("a3_form", "book", "leather", -1.8, -2.4, y=0.8, name="Telegram forms", radius=0.15,
             look="A packet of post-office telegram forms, each with a printed line: 'Sender's name below, address above'.",
             take="a3_telegram_form", take_text="I take a form. I should compose the message with care; every word is a halfpenny and an hour.", give_once=True),
        prop("a3_reading_table", "table", "dark", 1.6, -2.4, name="Reading table", radius=0.8,
             look="A table for papers and magazines. A railway timetable lies open."),
        prop("a3_bradshaw", "book", "red", 1.6, -2.4, y=0.8, name="Bradshaw's Guide", radius=0.2,
             look="Bradshaw's Railway Guide, open to the Continental pages.", talk="a3_bradshaw"),
        prop("a3_sideboard", "chest", "ebony", -5.0, -2.6, rot=90, scale=1.1, name="Sideboard", radius=0.7,
             look="Mrs Westenra's sideboard: sherry, port, and one decent bottle of brandy for emergencies.",
             take="brandy", take_text="I take the brandy. I rather suspect I shall need it.", give_once=True),
        prop("a3_side_table", "table", "pale", -4.4, 2.2, rot=90, scale=0.7, name="Side table", radius=0.5, look="A small table by the wall."),
        prop("a3_decanter", "bottle", "amber", -4.4, 2.2, y=0.6, name="Decanter of port", radius=0.15, cond="a3_wolf_down",
             look="The port decanter, half empty. It does not smell like port.",
             set="a3_sniffed_decanter", set_text="Laudanum, and a great deal of it. The servants were drugged. This was not drink; it was a plan."),
        prop("a3_key_rack", "key", "default", 2.6, -3.6, y=1.3, name="Key rack", radius=0.2,
             look="The housekeeper's key-board, labelled in copperplate. 'Miss L.'s room' hangs by itself.",
             take="a3_door_key", take_text="I take the key to Lucy's room. It may be the only ward that cannot be argued with.", give_once=True),
        prop("a3_hall_fire", "fireplace", "stone_grey", -5.4, 0.4, rot=90, name="Fireplace", radius=0.9,
             look="A fire kept alight in all weathers. The room is warm and the house is cold."),
        prop("a3_armchair", "chair", "red", -2.6, 1.6, rot=90, name="Armchair by the fire", radius=0.5,
             look="An easy chair by the fire. One could wait for morning in it.", talk="a3_wait_night"),
        prop("a3_haarlem_box", "chest", "pale", 1.2, 1.8, scale=0.8, name="Box from Haarlem", radius=0.5, cond="a3_vh_arrived",
             look="A deal box with Dutch stamps, full of garlic flowers. The scent is enormous.", talk="a3_haarlem_box"),
        prop("a3_umbrella_stand", "barrel", "dark", 4.8, 2.4, scale=0.55, name="Umbrella stand", radius=0.35,
             look="Umbrellas, a cane or two, and an iron bar someone has stood among them."),
        prop("a3_hall_rug", "rug", "red", 0.4, 0.2, radius=0.01),
        prop("a3_hall_candles", "candelabra", "default", 3.0, 0.4, name="Candelabrum", radius=0.3, look="A branch of candles."),
        prop("a3_maid_chair", "chair", "blue", 3.4, 1.4, rot=90, name="Kitchen chair", radius=0.4, cond="a3_wolf_down",
             look="A kitchen chair, brought in for the insensible maid."),
        prop("a3_hall_bust", "bust", "plaster", 5.0, 0.6, rot=-90, name="Bust", radius=0.3, look="A bust of someone's grandfather, looking disapproving."),
    ],
    npcs=[
        npc("a3_mrs_westenra", "human_peasant_f", "innkeeper_wife", -0.4, 0.8, rot=160, name="Mrs. Westenra", cond="!a3_wolf_down",
            look="Lucy's mother: small, silvered, gentle, with a cardiac flush she thinks no one notices and a heart the doctors will not name.", talk="a3_mrs_westenra"),
        npc("a3_maid", "human_peasant_f", "village_woman", 2.6, 0.2, rot=200, name="Maid", cond="!a3_wolf_down", radius=0.4,
            look="A young maid with a duster in her pocket and a way of looking over her shoulder at the stairs.", talk="a3_maid"),
        npc("a3_maid_asleep", "human_peasant_f", "village_woman", 3.4, 1.4, rot=90, name="Maid (insensible)", cond="a3_wolf_down", radius=0.4,
            look="One of the maids, slumped and breathing like an engine, as if she would never wake.", talk="a3_maid_asleep",
            use_item={"a3_smelling_salts": [{"take": "a3_smelling_salts"}, {"set": "a3_servants_woken"}, {"journal": "a3_j_servants"},
                                            say("The salts take. She coughs, sits up, and begins to weep. Behind her the others stir. Quincey's cab is crunching up the drive.")]},
            use_fail="That will not wake her."),
        npc("a3_arthur", "human_arthur", "lord", -1.4, 2.0, rot=140, name="Arthur Holmwood", cond="a3_vh_examined", radius=0.5,
            look="Arthur, a big fair man who looks as if he had been struck. He holds his hat in both hands.", talk="a3_arthur_talk"),
        npc("a3_quincey", "human_quincey", "texan", 0.6, 2.2, rot=170, name="Quincey Morris", cond="a3_servants_woken", radius=0.5,
            look="Quincey Morris, mud to the knees and a wide hat, standing as if he had ridden in. His voice is the softest thing about him.", talk="a3_quincey_talk"),
    ],
    on_enter=[
        {"if": "a3_mina_done", "once": True, "do": [
            {"set": "a3_vh_arrived"}, {"recruit": "vanhelsing"}, {"journal": "a3_j_vh_arrival"},
            say("7 September, morning. The door bell. A small, solid, grey-bearded man with a leather case on the step: Van Helsing, who must have come by the night boat. 'Where is she?' he says, in place of any greeting.")]},
        dict(once=True, do=[{"journal": "a3_j_hillingham"},
                            say("6 September. Hillingham. The garden is full of flowers and the house is full of fear.")]),
    ],
)

# ---------------------------------------------------------------- 9. Lucy's bedroom
LOC_DATA["a3_lucy_bedroom"] = dict(
    cells=[2, 2], interior=True, wall="plaster", floor="planks",
    ambient=AMBIENT["candle_interior"], camera=cam([2, 2]), lights=lights_warm([2, 2], n=3, energy=2.2),
    walls=dict(north=["wall_window_4", "wall_window_4"], west=["wall_4", "wall_4"], east=["wall_4", "wall_door_4"]),
    spawn=[2.6, 2.0], spawns={"a3_hillingham_hall": [2.6, 2.0]},
    props=[
        prop("a3_door_hall", "door", "pale", 3.8, 2.0, rot=-90, name="Door to the stairs", radius=0.6,
             look="The door to the landing. A bolt on the inside, a lock outside.", go="a3_hillingham_hall",
             use_item={"garlic": [{"set": "a3_g_door"}, say("I rub a head of garlic across the jamb and the sill, the way he showed me.")],
                       "a3_door_key": [{"set": "a3_door_locked"}, say("I turn the key in the lock and pocket it. Whoever wants in must come through a door I hold.")]},
             use_fail="That will do nothing to a door."),
        prop("a3_lucy_bed", "bed", "blue", 0.0, -2.0, name="Lucy's bed", radius=1.2,
             look="A white bed with a blue counterpane. The pillow is a perfect, slightly sunken oval.", talk="a3_transfusion_bed"),
        prop("a3_window_seat", "chest", "pale", 2.0, -3.3, scale=1.2, name="Window-seat", radius=0.8,
             look="A deep window-seat under the east window. In the evenings she sits here and counts the stars. The sash is painted so it will not open. Except that it has opened.",
             use_item={"garlic": [{"set": "a3_g_window"}, say("I lay garlic flowers along the sill and the frame, and pack the crack at the sash with the stalks.")],
                       "a3_window_pin": [{"set": "a3_window_pinned"}, say("I drop the iron pin through the sash-staples. The window is now a wall.")]},
             use_fail="That is no use on a window."),
        prop("a3_bed_fire", "fireplace", "stone_grey", -3.4, 0.4, rot=90, name="Fireplace", radius=0.9,
             look="A small grate, swept and empty. A chimney is a door, if one is thin enough.",
             use_item={"garlic": [{"set": "a3_g_chimney"}, say("Garlic stuffed up the flue, and a bunch in the grate. Odd work for a physician.")]},
             use_fail="Not for a chimney."),
        prop("a3_bedside_chair", "chair", "blue", 1.6, -0.2, rot=180, name="Chair by the bed", radius=0.45,
             look="A chair set where a watcher would sit. A rug, a cushion, a book unopened.", talk="a3_vigil"),
        prop("a3_vanity", "table", "pale", -2.6, 2.2, rot=90, name="Dressing-table", radius=0.7,
             look="A girl's dressing-table: brushes, a hand-glass, a faded Whitby postcard."),
        prop("a3_vanity_mirror", "mirror", "default", -3.5, 2.2, rot=90, name="Mirror", radius=0.4,
             look="A mirror in which a pale girl, if she stood there, would still look like herself."),
        prop("a3_wardrobe", "bookshelf", "pale", 3.3, -2.4, rot=-90, name="Wardrobe", radius=0.8,
             look="Dresses of a summer that ended in Whitby."),
        prop("a3_bureau", "chest", "pale", -3.2, -2.8, rot=90, scale=0.7, name="Mrs Westenra's dressing-case", radius=0.5, cond="a3_wolf_down",
             look="Her mother's dressing-case, dropped in the night. Powder, hairpins, and a little bottle of sal volatile.",
             take="a3_smelling_salts", take_text="Smelling salts. They will not wake a drugged girl who is truly gone, but they may wake a servant who is only dosed.", give_once=True),
        prop("a3_nightstand", "table", "pale", 2.6, 0.4, scale=0.6, name="Night-table", radius=0.4,
             look="A water jug, a glass, a candle, and a medicine bottle three-quarters empty."),
        prop("a3_night_candle", "candle", "white", 2.6, 0.4, y=0.6, name=None, radius=0.1),
        prop("a3_petals", "garlic", "default", 0.8, -1.0, name="Scattered garlic", radius=0.4, cond="a3_night1",
             look="Garlic flowers scattered between the bed and the window, as though dropped by someone walking away.",
             set="a3_saw_petals", set_text="A trail of petals: from the bed-head, across the carpet, to the window-seat."),
        prop("a3_slippers", "rug", "cream", 1.7, -2.6, scale=0.18, name="Lucy's slippers", radius=0.3, cond="a3_night1",
             look="Her white slippers, beside the window-seat. The soles are wet with dew.",
             set="a3_saw_slippers", set_text="Dew on the soles. She walked on the grass. In her sleep? Or at some other bidding?"),
        prop("a3_broken_glass", "bottle", "glass", 2.0, -2.2, name="Broken window", radius=0.5, cond="a3_wolf_down",
             look="The east window is gone: a ragged hole, glass across the carpet, the curtains snapping in the night air."),
        prop("a3_mother_sheet", "rug", "cream", 0.9, -0.7, scale=0.7, name="Mrs Westenra, under a sheet", radius=0.5, cond="a3_wolf_down",
             look="We have covered her with a sheet, and with the last decency we had. Her hand has slipped out from under it, and Van Helsing has put it back."),
        prop("a3_bed_rug", "rug", "blue", -0.6, 0.6, radius=0.01),
    ],
    npcs=[
        npc("a3_lucy", "human_lucy", "nightgown", -1.4, -1.0, rot=60, name="Lucy", cond="!a3_lucy_dead", radius=0.5,
            look="Lucy, propped on pillows: a white-lipped, still beautiful girl with blue-veined eyelids and a pulse like a bird's.", talk="a3_lucy_talk",
            use_item={"garlic": [{"set": "a3_g_neck"}, say("A garland of garlic flowers around her neck, tied with white ribbon, as the Professor taught me.")]},
            use_fail="I do not think that will help her."),
        npc("a3_lucy_dead_npc", "human_lucy", "nightgown", -1.4, -1.0, rot=60, name="Lucy", cond="a3_lucy_dead", radius=0.5,
            look="Lucy, as if asleep. There is more colour in her cheeks than in life, and I am more afraid of it than of any pallor.", talk="a3_lucy_corpse"),
        npc("a3_vh_bed", "human_vanhelsing", "vh", -0.2, 0.8, rot=180, name="Van Helsing", cond="a3_vh_arrived", radius=0.5,
            look="The Professor, in his shirt-sleeves, washing his hands in the basin as he thinks.", talk="a3_vh_talk"),
    ],
)

# ---------------------------------------------------------------- 10. the Hillingham garden
LOC_DATA["a3_hillingham_garden"] = dict(
    cells=[3, 2], interior=False, wall="dirt", floor="grass",
    ambient=AMBIENT["dusk_exterior"], camera=cam([3, 2]), lights=lights_moon(2.4), moon=dict(pos=[10, 14, -18]),
    walls=dict(west=["wall_door_4", "wall_4"]),
    scatter=dict(asset="pine", variant="dark", count=22, seed=17, avoid=[[-6, -4, 6, 4]]),
    spawn=[-4.4, -1.4], spawns={"a3_hillingham_hall": [-4.6, -1.4], "a3_asylum_garden": [3.4, 1.4], "a3_kingstead_churchyard": [3.4, 1.4]},
    props=[
        prop("a3_garden_door_back", "door", "pale", -5.8, -2.0, rot=90, name="Door to the hall", radius=0.6,
             look="Back to the house.", go="a3_hillingham_hall"),
        prop("a3_h_shed", "chest", "dark", 4.4, -2.8, scale=1.3, name="Potting-shed", radius=0.9,
             look="A lean-to of tarred boards against the wall. It smells of earth, twine and old mats."),
        prop("a3_h_bench", "bench", "oak", 2.0, -2.6, name="Potting-bench", radius=0.8,
             look="A slatted work-bench strewn with pots, twine and bulbs."),
        prop("a3_h_herbs", "garlic", "default", -3.0, -2.4, name="Kitchen herbs", radius=0.5,
             look="A bed of kitchen herbs. The cook's garlic is green and rank and entirely ordinary, nothing like the white flowers the Professor wants."),
        prop("a3_h_bat", "bat", "black", -2.4, -3.4, y=2.6, name="Bat", radius=0.5,
             look="A bat circles the lit upper window again, and again. It does not fly like an English bat."),
        prop("a3_cab_asylum", "carriage", "ebony", 3.6, 2.2, rot=-70, name="Cab to Purfleet", radius=1.6,
             look="A cab waiting for a fare back to the asylum.", go="a3_asylum_garden"),
        prop("a3_hearse", "carriage", "ebony", 4.8, 0.4, rot=-90, name="Hearse", radius=1.6, cond="a3_ready_funeral",
             look="A black-plumed hearse with a black-plumed horse. The undertaker's men take their hats off, one at a time.",
             go="a3_kingstead_churchyard"),
        prop("a3_h_well", "barrel", "dark", -1.0, 3.4, scale=1.1, name="Rain-barrel", radius=0.4, look="Rainwater, and a drowned moth."),
        prop("a3_h_fence1", "fence", "default", 0.0, 3.6, radius=0.01),
        prop("a3_h_fence2", "fence", "default", 3.0, 3.6, radius=0.01),
        prop("a3_h_lamp", "lantern", "default", -4.6, 2.6, name="Lantern", radius=0.3, look="A lantern hung on the wall by the door."),
    ],
    npcs=[
        npc("a3_boy_wire", "human_peasant_m", "innkeeper", -1.6, 1.0, rot=30, name="Telegraph boy", radius=0.4,
            look="A boy from the post-office, perched on the bench with a pad and pencil. He is eating a bun and does not intend to be hurried.", talk="a3_boy_wire"),
    ],
)

# ---------------------------------------------------------------- 11. Kingstead churchyard (finale)
LOC_DATA["a3_kingstead_churchyard"] = dict(
    cells=[3, 3], interior=False, wall="dirt", floor="grass",
    ambient=AMBIENT["storm_exterior"], camera=cam([3, 3]), lights=lights_day(1.8),
    scatter=dict(asset="pine", variant="dark", count=26, seed=29, avoid=[[-7, -7, 7, 7]]),
    scatter2=dict(asset="deadtree", variant="grey", count=5, seed=31, avoid=[[-7, -7, 7, 7]]),
    spawn=[3.6, 3.6], spawns={"a3_hillingham_garden": [3.6, 3.6]},
    props=[
        prop("a3_vault", "tomb", "stone_tomb", 0.0, -4.0, scale=1.5, name="Westenra vault", radius=1.2,
             look="A marble vault at the end of the yew walk. A cross, a name, a date. The door is bronze, and not yet closed.",
             use_item={"garlic": [{"take": "garlic"}, {"set": "a3_garlic_in_tomb"}, {"journal": "a3_j_funeral"},
                                  say("Under the Professor's eye I lay garlic flowers on the coffin-lid and across the lintel. 'It is the old custom of the country where I was born,' he says, and says no more.")]},
             use_fail="Not that. Garlic flowers, as he asked."),
        prop("a3_stone1", "gravestone", "stone_grey", -3.6, -2.0, name="Old gravestone", radius=0.4, look="'Beloved wife'. The lichen has finished the rest."),
        prop("a3_stone2", "gravestone_point", "stone_mossy", -2.0, -4.6, name="Gravestone", radius=0.4, look="A weathered stone, a skull and an hour-glass."),
        prop("a3_stone3", "gravestone", "stone_dark", 3.2, -1.8, name="Gravestone", radius=0.4, look="'Thomas Holloway, of this parish.'"),
        prop("a3_stone4", "grave_cross", "stone_grey", 4.6, -3.4, name="Stone cross", radius=0.4, look="A small stone cross with a wreath of dead lilies."),
        prop("a3_stone5", "grave_cross", "stone_mossy", -4.8, 0.4, name="Leaning cross", radius=0.4, look="A cross leaning at ten degrees to the world."),
        prop("a3_churchyard_bench", "bench", "oak", 3.8, 1.2, rot=-90, name="Bench", radius=0.7, look="A wet bench. No one is sitting on it."),
        prop("a3_churchyard_lamp", "lantern", "default", -4.2, 3.4, name="Lantern", radius=0.3, look="A lantern, for the late burials."),
        prop("a3_churchyard_rock", "rock_big", "mossy", 5.2, -1.0, radius=0.01),
        prop("a3_flowers", "garlic", "default", 1.4, -2.4, name="Wreaths", radius=0.5,
             look="Wreaths of white lilies and white roses. Arthur's is the largest, and the Professor's is the only one that smells of anything."),
    ],
    npcs=[
        npc("a3_vh_final", "human_vanhelsing", "vh", -1.2, -0.6, rot=180, name="Van Helsing", radius=0.5,
            look="The Professor, bare-headed in the rain, with his hat in his hands and a bag at his feet.", talk="a3_vh_final"),
        npc("a3_arthur_funeral", "human_arthur", "lord", 1.2, 0.2, rot=200, name="Arthur", radius=0.5,
            look="Arthur, motionless as a post. Quincey has an arm round his shoulders.", talk="a3_arthur_funeral"),
        npc("a3_quincey_funeral", "human_quincey", "texan", 2.4, 0.4, rot=200, name="Quincey", radius=0.5,
            look="Quincey, his hat pulled down against the rain and, I think, against my eyes.", talk="a3_quincey_funeral"),
        npc("a3_gravedigger", "human_peasant_m", "villager", -3.4, -2.6, rot=30, name="Sexton", radius=0.4,
            look="The sexton, a leathery man, leaning on a spade and waiting, with the immense patience of his trade.", talk="a3_gravedigger"),
    ],
    on_enter=[dict(do=[{"journal": "a3_j_burial"},
                       {"set": "a3_at_funeral"},
                       say("22 September. Rain on the yews. The coffin was lowered an hour ago; the clergyman has gone, and the Professor has not.")], once=True)],
)


# =============================================================================================================
# DIALOGUE
# =============================================================================================================
G1 = "a3_g1_window&a3_g1_door&a3_g1_chimney&a3_g1_neck"      # round 1: all four garlic wards in place
G2 = "a3_g2_window&a3_g1_door&a3_g1_chimney&a3_g2_neck"      # round 2: window and neck renewed
G3 = "a3_g3_window&a3_g3_door&a3_g3_chimney&a3_g3_neck"      # round 3: everything renewed
DIALOGUE = {}

# ------------------------------------------------------------------ the asylum
DIALOGUE["a3_phonograph"] = D("n0",
    n0=n("Dr. Seward (phonograph)", "I turn the crank and the cylinder begins to speak in my own tired voice. 'Patient: R. M. Renfield, aged fifty-nine. Sanguine temperament, great physical strength, morbidly excitable, periods of gloom ending in some fixed idea. Fixed idea: that he must absorb life. I note that he has begun to make a ladder of it.'",
          do=[{"journal": "a3_j_seward_diary"}], next="n1"),
    n1=n("Dr. Seward (phonograph)", "'Also noted: two letters from Arthur Holmwood, three from Lucy, none from Quincey. Lucy writes of Whitby, of sleepwalking, of a pale and anxious friend, Mina. I do not like what I read between the lines. Practical matters: the dispensary key is mislaid again; Renfield's dose will need to be weighed correctly, for he is not what he was; and Hennessey will be wanting me.'",
          choices=[c("[Stop the machine]", end=True)]),
)

DIALOGUE["a3_case_ledger"] = D("n0",
    n0=n("Case ledger", "The asylum ledger lies open. Each patient has his column: weight, temper, treatment, notes.",
         choices=[c("Turn to the dosage page.", next="n_dose"), c("Read Renfield's entry.", next="n_file"), LEAVE]),
    n_dose=n("Case ledger", "In my own hand, in pencil in the margin: 'Chloral hydrate, ten grains for a man of nine stone; fifteen for twelve stone; thirty for a bull. Never above his weight, and never when he is already dosed.' I underline 'nine stone' and the word 'never'.",
             do=[{"journal": "a3_j_dose"}], end=True),
    n_file=n("Case ledger", "'R. M. Renfield. Wt 9 st 4 lb, wasting. Eats little at table. Hoards sugar. Keeps a jar of flies, a box of spiders, and a sparrow. Asked this week whether he might have a kitten. Refused.' Beneath, in a different ink: 'Count the sugar.'", end=True),
)

DIALOGUE["a3_case_notes"] = D("n0",
    n0=n("Dr. Seward", "I spread what I have found across the table. Sugar in his pillow, a jar of flies, a box of spiders, his notebook of figures. I need all four before I trust my own deduction. 'What', I ask the room, 'does this man do?'",
         choices=[
             c("He is a harmless naturalist who loves small things.", next="n_wrong1"),
             c("He hoards sugar because he has a sweet tooth, and keeps the rest as pets.", next="n_wrong2"),
             c("Sugar draws flies; flies feed spiders; spiders feed sparrows. He is building a ladder of lives to feed on, and he wants a cat for the next rung.",
               cond="has:a3_sugar_lumps&has:a3_fly_jar&has:a3_spider_box&has:a3_renfield_notebook", next="n_ok",
               do=[{"set": "a3_diet_solved"}, {"journal": "a3_j_zoophagy"}]),
             c("I have not gathered enough yet.", end=True)]),
    n_wrong1=n("Dr. Seward", "A naturalist keeps what he studies. He does not count them every night, and does not look at the sparrow like that. No.", next="n0"),
    n_wrong2=n("Dr. Seward", "A sweet tooth does not hide sugar under a pillow and keep a ledger of insects. No.", next="n0"),
    n_ok=n("Dr. Seward", "It is not a hobby; it is a method. He is feeding life into life, link by link, and believes the strength gathers in him. I wrote 'zoophagous mania' on his sheet this morning without understanding what I was writing. He is a maniac, and the maniac has a plan.", end=True),
)

DIALOGUE["a3_hennessey"] = D("n0",
    n0=n("Dr. Hennessey", "Morning, Doctor. Renfield was at it all night, counting out loud, sometimes in a whisper and sometimes not. I wouldn't go in without a sedative. He's been like a man listening for something.",
         do=[{"set": "a3_met_hennessey"}],
         choices=[
             c("What does he eat?", next="n_eats"),
             c("Has he tried to get out?", next="n_escape"),
             c("Where is the dispensary key?", next="n_key"),
             c("I will take a pull from that flask of yours, if you can spare it.", cond="a3_renfield_calm&!a3_got_flask", next="n_flask",
               do=[{"give": "brandy"}, {"set": "a3_got_flask"}]),
             LEAVE]),
    n_eats=n("Dr. Hennessey", "Nothing at table, hardly. But Dobbs found sugar hidden in his pillow, and he lives on bluebottles, I swear it. He swallowed a spider in front of me. He said it was 'a very fine one'.", end=True),
    n_escape=n("Dr. Hennessey", "Twice since June, once at night, and Pocock found him in the Carfax garden at dawn. How he gets from his cell to the wall I don't know; but the wall, now, is another matter. Ask Pocock about the fence.", do=[{"set": "a3_heard_escape"}], end=True),
    n_key=n("Dr. Hennessey", "You always put it somewhere clever, Doctor. Last time it was behind Lombroso. The time before, the mantel clock. If I were you, I'd look in your own study before you look anywhere else.", end=True),
    n_flask=n("Dr. Hennessey", "Take what you need. You've earned it. Between us, if the old fellow's quiet at last, I'd drink to that myself.", end=True),
)

DIALOGUE["a3_mix_dose"] = D("n0",
    n0=n("Dr. Seward", "Scales, a graduated glass, a brass measure. Chloral crystals dissolved in water: but how many grains? The ledger has the rule; the weighing table has the weight. A mistake here is a mistake in a man's body, not a ledger.",
         choices=[
             c("Five grains: a mild draught, in case he is already tired.", cond="has:a3_chloral_crystals&has:water", next="n_weak"),
             c("Ten grains: right for nine stone.", cond="has:a3_chloral_crystals&has:water", next="n_ok",
               do=[{"give": "chloral"}]),
             c("Fifteen grains, to be certain.", cond="has:a3_chloral_crystals&has:water", next="n_mid"),
             c("Thirty grains. Make a certainty of it.", cond="has:a3_chloral_crystals&has:water", next="n_strong"),
             LEAVE]),
    n_weak=n("Dr. Seward", "Five would make him drowsy and furious. A furious Renfield does not stay drowsy. No.", next="n0"),
    n_ok=n("Dr. Seward", "Ten grains in a measure of clean water: not a grain more than his nine stone can carry. I stopper it and put it in my pocket.", end=True),
    n_mid=n("Dr. Seward", "Fifteen is for a man of twelve stone, and Renfield is nine and wasting. He would sleep all night and wake raving with a bad heart. No.", next="n0"),
    n_strong=n("Dr. Seward", "Thirty is a bull's dose. It would stop his heart. I put the measure down with a shaking hand.", next="n0"),
)

DIALOGUE["a3_basin"] = D("n0",
    n0=n("Dr. Seward", "Rainwater, clean enough, and a tin dipper hanging on its chain.",
         choices=[c("Fill a measuring-glass with water.", do=[{"give": "water"}, say("I fill the glass to the mark.")], end=True), LEAVE]),
)

DIALOGUE["a3_dobbs"] = D("n0",
    n0=n("Dobbs", "Evening, Doctor. I'd not go in alone, if I were you, not unless he's had his draught. He bit Mr Hennessey's glove in half last week, and wasn't sorry.",
         choices=[
             c("How is he tonight?", next="n_a"),
             c("Anything unusual?", next="n_b"),
             LEAVE]),
    n_a=n("Dobbs", "Like a clock wound too tight, sir. He's been talking to the window. Not praying, sir, just talking, as if someone were out there answering.", end=True),
    n_b=n("Dobbs", "The sparrow, sir. He's tamed one, and it sits on his shoulder. And last night he asked me, very civil, whether the 'Master' had come. I said I didn't know any master in the building, only you. He laughed at that. Laughed for a quarter of an hour.", end=True),
)

DIALOGUE["a3_renfield_talk"] = D("n0",
    n0=n("Renfield", "Ah, Doctor Seward. How very good of you to call. I have had the strangest sort of calm. I was wondering whether we might speak as gentlemen.",
         choices=[
             c("Why do you keep flies, Renfield?", next="n_flies"),
             c("Is it true you asked for a kitten?", next="n_kitten"),
             c("Who is the Master?", cond="a3_diet_solved", next="n_master"),
             c("What do you see from the window?", next="n_window"),
             c("Do you know a lady called Lucy Westenra?", next="n_lucy"),
             LEAVE]),
    n_flies=n("Renfield", "They are lives, Doctor. Each is a little, glittering life, and it takes so many to make one great one. A spider eats a hundred flies. A sparrow eats a hundred spiders. And a cat... a cat has the lives of the whole garden in her.", end=True),
    n_kitten=n("Renfield", "A kitten. A nice little sleek playful kitten, that I can teach and feed and feed, and feed. I should not hurt it. Not until it was grown.",
               choices=[c("No, Renfield. You may not have one.", next="n_k_no", do=[{"set": "a3_refused_kitten"}]),
                        c("Perhaps. If you are good.", next="n_k_yes")]),
    n_k_no=n("Renfield", "(He is not angry; he is quiet. He says, softly:) Then you will regret it, Doctor. Not me. I shall not.", end=True),
    n_k_yes=n("Renfield", "(He brightens horribly.) You will? Oh, Doctor, then you are a friend! (I wish I had not said it. I shall not repeat it.)", end=True),
    n_master=n("Renfield", "He is coming, Doctor. Not yet, not tonight, but he is near. He promises me lives, and more lives, a world of flies... I only want to be ready. I was a poor mad creature, and he has said that I shall be honoured. (He looks at the window and weeps.)",
               do=[{"set": "a3_heard_master"}], end=True),
    n_window=n("Renfield", "Carfax. There are lights in it now, at night. Boxes. Great boxes, carried by men who sweat and swear in a foreign tongue. Mr Hawkins's clients, perhaps. Whoever it is, he has more patience than I.", end=True),
    n_lucy=n("Renfield", "Lucy? A sweet name for a sweet creature. I believe I have seen a letter. Sweet things go to waste, Doctor, in a house with an open window. Do you know, you should be very careful, very careful indeed. (He is not mocking me. He is frightened.)", end=True),
)

DIALOGUE["a3_pocock"] = D("n0",
    n0=n("Pocock", "Doctor. Fine day for the fruit trees. You're not here for the fruit trees.",
         choices=[
             c("Mr Hennessey says someone has been through the wall.", next="n_wall"),
             c("I need a hammer.", next="n_hammer"),
             c("Carfax. What do you know of it?", next="n_carfax"),
             LEAVE]),
    n_wall=n("Pocock", "Aye. Slat by the elms, hangin' by one nail. There's a track through the long grass to Carfax's garden, worn like a sheep-path, and the grass bent the wrong way, sir; towards the house. I told Mr Hennessey. Told 'im last month.", do=[{"set": "a3_heard_pocock"}], end=True),
    n_hammer=n("Pocock", "Toolbox in the shed, sir. Don't leave any nails about. They find them.", end=True),
    n_carfax=n("Pocock", "Sold in the spring. Men have been carrying boxes in at night, like coffins. I don't ask, sir. The fruit doesn't ask me.", end=True),
)

DIALOGUE["a3_boy_asylum"] = D("n0",
    n0=n("Telegraph boy", "Telegram for Dr. Seward, sir! Came at four, sir, by Hampstead. The sender looked proper upset.",
         choices=[
             c("Take the telegram.", cond="!a3_got_telegram", next="n_t",
               do=[{"give": "a3_arthur_telegram"}, {"set": "a3_got_telegram"}, {"journal": "a3_j_arthur_wire"}]),
             c("Nothing to send in return.", end=True)]),
    n_t=n("Telegraph boy", "No reply paid, sir. Thank you, sir!", end=True),
)

DIALOGUE["a3_bilder"] = D("n0",
    n0=n("Mr. Bilder", "Berserker? Lord love you, sir, the gentlest great beast in the Gardens. Dog-gentle. Would let the Missus scratch him through the bars. Yet that night, sir. That night.",
         choices=[
             c("What happened the night he went?", next="n_night"),
             c("Was anyone about?", next="n_stranger"),
             c("May I have the newspaper cutting?", next="n_cut"),
             LEAVE]),
    n_night=n("Mr. Bilder", "Storm, sir, thunder and lightning. He began to howl before it started. I was in the cottage when I heard iron bend. Went out with a lantern, and the bars were wrenched. He was gone by morning, and not a track in the mud, not a sign of him over the wall.", do=[{"set": "a3_zoo_asked"}], end=True),
    n_stranger=n("Mr. Bilder", "Aye. A tall, thin man, hooked nose, black moustache and a pointed beard with a few white hairs. A tight-lipped gent, with red in his eyes under the lamp. He'd been standing at Berserker's cage the evening before, and Berserker, who never so much as shifted for visitors, put his head on the bars and looked at him. Nothing more. They knew each other, I'd swear.", do=[{"set": "a3_zoo_stranger"}], end=True),
    n_cut=n("Mr. Bilder", "It's on the table, sir. A reporter wrote it down as I said it, and he got one thing right and nine things wrong. Take it. The Missus reads it aloud and I can't abide it.", end=True),
)
DIALOGUE["a3_mrs_bilder"] = D("n0",
    n0=n("Mrs. Bilder", "Mr. Bilder says it was a storm, sir. I say a wolf in a storm would stay in his cage and howl. This one went where he was wanted. Mark me.",
         choices=[c("What do you mean, 'wanted'?", next="n1"), LEAVE]),
    n1=n("Mrs. Bilder", "He was a pet, sir, a great soft dog of a thing, till somebody whistled. Don't ask me who. I only say there are things that go when they are called.", end=True),
)
DIALOGUE["a3_berserker_look"] = D("n0",
    n0=n("Berserker", "The wolf stops pacing and looks at you. For a moment you are sure he is about to speak, and then he drops his head, and begins again, back and forth, back and forth, with his eyes on the north.", end=True),
)

# ------------------------------------------------------------------ Buda-Pesth (Mina)
DIALOGUE["a3_agatha"] = D("n0",
    n0=n("Sister Agatha", "You are Miss Murray. I wrote to you. He has been calling for you in his sleep, and sometimes in his waking. The doctors say it was a brain fever, brought on by some great shock. What shock, he will not say.",
         choices=[
             c("How is he, Sister?", next="n_how"),
             c("Where is his journal? I have heard of it.", next="n_diary"),
             c("Sister, may we be married here, today?", next="n_wed"),
             LEAVE]),
    n_how=n("Sister Agatha", "Weak, and very quiet. He wakes sometimes in the night and asks whether the windows are barred. I tell him they are not, and he is comforted. I have watched men who fought on battlefields. He has seen something worse.", end=True),
    n_diary=n("Sister Agatha", "Under his pillow, Miss. He asked me to keep it from him, then asked for it back. He says he cannot bear to read it, but that you may, if some solemn duty ever demands it. Ask him gently. It is his to give.", end=True),
    n_wed=n("Sister Agatha", "I would be proud to witness it, child. I will arrange a priest, and the chapel. Bring a ring, bring your husband's consent, and let that journal be sealed first, so neither of you is tempted. Black ribbon is in the basket, wax on the desk. Some promises are better kept by a seal than by a vow.",
            do=[{"set": "a3_wed_asked"}], end=True),
)
DIALOGUE["a3_jonathan_hosp"] = D("n0",
    n0=n("Jonathan", "Mina? Is it really you? I had been afraid... I thought it was another dream, with a kind face on it.",
         choices=[
             c("Rest, Jonathan. I am here, and I shall not leave you.", next="n_rest"),
             c("Sister Agatha says there is a journal, Jonathan.", cond="!a3_got_diary", next="n_diary",
               do=[{"give": "a3_harker_diary"}, {"set": "a3_got_diary"}]),
             c("Jonathan, will you marry me, here, today?", cond="a3_got_diary", next="n_marry", do=[{"set": "a3_jonathan_agrees"}]),
             LEAVE]),
    n_rest=n("Jonathan", "(He takes my hand with both his. His fingers feel like twigs.) The Count... no, I shall not say it. Not now. Only that when I walked out of the Castle, I walked out of every door I had ever believed in.", end=True),
    n_diary=n("Jonathan", "Here, take it. I wrote it all, every night. Read it if you must, never if you needn't, and do not ask me to confirm one line. I want to be married before I remember what is in it. (He pushes the little black book across the blanket.)",
              end=True),
    n_marry=n("Jonathan", "Yes. Oh, yes. There is a ring in my coat, I think, in the waistcoat pocket. I bought it in London the week before I left, and could not bring myself to throw it away. Mina, if you will have a broken man...", end=True),
)
DIALOGUE["a3_sister_maria"] = D("n0",
    n0=n("Sister Maria", "He is a very good patient, Miss. He eats everything. But he sleeps with the light on, and the Sisters say he talks of wolves. We do not mention wolves.", end=True),
)
DIALOGUE["a3_seal_table"] = D("n0",
    n0=n("Mina", "A table by the window, and good light. If I could close Jonathan's journal so that it can only be opened by our decision... black ribbon, wax, and the book itself.",
         choices=[
             c("Tie the journal with the ribbon and seal it with wax.", cond="has:a3_harker_diary&has:a3_ribbon&has:a3_sealing_wax", next="n_ok",
               do=[{"take": "a3_ribbon"}, {"take": "a3_sealing_wax"}, {"set": "a3_diary_sealed"}, {"journal": "a3_j_mina_diary_sealed"}]),
             LEAVE]),
    n_ok=n("Mina", "I tie the ribbon in a bow and let the red wax fall, a drop, a seal. It is nothing, a book and a ribbon, and I feel as though I have closed a door in my own house. Whatever is in it is safe from us until we need it.", end=True),
)
DIALOGUE["a3_priest"] = D("n0",
    n0=n("Father Hermann", "My child, Sister Agatha says you wish to be married. It is not the usual hour, and not the usual reason. Tell me.",
         choices=[
             c("We are ready, Father: the ring, his consent, and the journal sealed.", cond="a3_diary_sealed&has:a3_wedding_ring&a3_jonathan_agrees", next="v1"),
             c("What must we bring, Father?", next="n_need"),
             LEAVE]),
    n_need=n("Father Hermann", "A ring, my child, and the bridegroom's consent, which he must give freely and in his right mind. Sister Agatha mentions something about a journal that must be sealed first; I confess I do not ask. And a witness, which she is.", end=True),
    v1=n("Father Hermann", "Wilhelmina Murray, wilt thou have this man to be thy wedded husband, to live together after God's ordinance? Wilt thou love him, comfort him, honour and keep him in sickness and in health?", next="v2"),
    v2=n("Mina", "'I will.' (My voice is not mine. It is smaller, and certain.) 'I will, in sickness and in health, and I think the sickness is the part that matters.'", next="v3"),
    v3=n("Jonathan", "'I will. I, Jonathan, take thee, Wilhelmina, to my wedded wife. To have and to hold, from this day forward... and I will not let go.' (His fingers are shaking. He puts the ring on, and it does not slip.)", next="v4"),
    v4=n("Father Hermann", "Those whom God hath joined together let no man put asunder. Go in peace, Mrs Harker.",
         do=[{"set": "a3_mina_done"}, {"journal": "a3_j_wedding"}, {"protagonist": "seward"},
             {"card": "Hillingham, 7 September.  The wire from Dr. Seward was answered, in the end. Van Helsing is on the step."},
             {"goto": "a3_hillingham_hall"}], end=True),
)
DIALOGUE["a3_jonathan_chapel"] = D("n0",
    n0=n("Jonathan", "I can stand if you hold my arm. If I could ask one more thing, Mina: that we never talk of the Castle unless we must. I want to remember being happy before I remember anything else.", end=True),
)
DIALOGUE["a3_agatha_chapel"] = D("n0",
    n0=n("Sister Agatha", "I have put my hand to many a bedside, child. This is the first altar I have been asked to stand at in sixteen years. Go on. The priest is waiting, and the candles do not last.", end=True),
)

# ------------------------------------------------------------------ Hillingham
DIALOGUE["a3_bradshaw"] = D("n0",
    n0=n("Bradshaw's Guide", "The Continental pages are open, and someone has underlined a line in pencil. Amsterdam: the Hook of Holland boat leaves at night for Harwich, the boat-train for Liverpool Street. The day services by Calais and Dover take half as long again, with two changes.",
         choices=[c("Note the night boat times.", next="n1"), LEAVE]),
    n1=n("Dr. Seward", "Night boat from the Hook; boat-train reaches Liverpool Street at five minutes past six. And the telegraph at Hampstead closes at eight, with a boy who must be paid before then. If I want Van Helsing here by breakfast, my wire must name the night boat.",
         do=[{"journal": "a3_j_bradshaw"}, {"set": "a3_read_bradshaw"}], end=True),
)
DIALOGUE["a3_haarlem_box"] = D("n0",
    n0=n("Dr. Seward", "A box of garlic flowers from Haarlem, with the Professor's own scrawl on the lid. 'Not for the kitchen.'",
         choices=[c("Take a handful of the flowers.", do=[{"give": "garlic"}, {"give": "garlic"}, {"give": "garlic"}, say("I take three heads of the pale, rank flowers. The whole hall smells of them.")], end=True), LEAVE]),
)
DIALOGUE["a3_wait_night"] = D("n0",
    n0=n("Dr. Seward", "The fire is low. The house is silent. The wire is gone; there is nothing to do but wait for morning, and the train.",
         choices=[
             c("Sit by the fire until morning.", cond="a3_wired_vh&!a3_mina_done", next="n1"),
             c("Not yet. There is more to do first.", end=True)]),
    n1=n("Dr. Seward", "I sit in the armchair, and the fire gutters, and Lucy's breathing comes down the stairs like a clock. Somewhere, Jonathan Harker is lying in a foreign bed, and Mina has gone to find him. I have not even had time to think of them.",
         do=[{"card": "Meanwhile, in Buda-Pesth, a fortnight earlier.  24 August.  Mina Murray crosses Europe to find a man she is not yet married to."},
             {"protagonist": "mina"}, {"goto": "a3_buda_hospital"}], end=True),
)
DIALOGUE["a3_mrs_westenra"] = D("n0",
    n0=n("Mrs. Westenra", "Dr. Seward! How good of you. Lucy is so very much better, I think. She only wants her window open and a little air. Girls will make such a fuss about the stuffiness of a sickroom.",
         choices=[
             c("How is Lucy, Mrs Westenra?", next="n_a", do=[{"set": "a3_met_mother"}]),
             c("And you, Mrs Westenra? Your own heart?", cond="a3_met_mother", next="n_heart", do=[{"set": "a3_asked_heart"}]),
             c("I should like her room kept quiet and undisturbed tonight.", cond="a3_met_mother", next="n_quiet"),
             c("About the garlic in Lucy's room, madam...", cond="a3_night2", next="n_g"),
             LEAVE]),
    n_a=n("Mrs. Westenra", "She sleeps so much. She was never so languid at Whitby, and those sea airs were supposed to have done her such good. She cries out in her sleep sometimes, poor child. I have thought of sending for Dr. Hargreaves, but Arthur says to wait for you. You may go up. She is sleeping, I think.", end=True),
    n_heart=n("Mrs. Westenra", "Oh, a little fluttering. It is nothing. I have it every evening. Dr. Hargreaves says I must not be startled. I tell him I am never startled; nothing ever happens in Hampstead.", end=True),
    n_quiet=n("Mrs. Westenra", "Of course, Doctor. I shall not so much as put my head round the door. Although I do think the poor child is too much alone at night; the house is so large, and the maids are so far.", end=True),
    n_g=n("Mrs. Westenra", "Those dreadful flowers! I confess I threw them out, and opened the window. A girl cannot get well in a room that smells like a kitchen drain. Dr. Seward, it is my house and my child.",
          choices=[
              c("They are a fashionable Dutch remedy, madam, nothing more.", next="n_g_bad1"),
              c("Professor Van Helsing has many degrees. He prescribes it.", next="n_g_bad2"),
              c("Madam, they are as real a medicine as digitalis. If they are moved again, I fear Lucy may not wake. I beg you to trust a physician who has seen this before.",
                next="n_g_ok", do=[{"set": "a3_mother_agrees"}])]),
    n_g_bad1=n("Mrs. Westenra", "A fashionable remedy! Then it will be out of fashion by Sunday. No, Doctor, I think not.", next="n_g"),
    n_g_bad2=n("Mrs. Westenra", "Degrees! Dr. Hargreaves has several, and he does not tell me to hang a vegetable round my daughter's neck.", next="n_g"),
    n_g_ok=n("Mrs. Westenra", "(Her hand has gone to her heart.) Oh, my dear Doctor. Put like that... I would never forgive myself. I promise, on my honour. Touch nothing in that room. I shall not even pass the door.", end=True),
)
DIALOGUE["a3_maid"] = D("n0",
    n0=n("Maid", "Oh, sir, begging your pardon. I've worked here nine years, and I never saw Miss Lucy like this. She isn't herself in the mornings, sir, and she never was a one to walk about.",
         choices=[
             c("Does she walk in her sleep?", next="n_a"),
             c("Where is the key to Miss Lucy's room kept?", next="n_key", do=[{"set": "a3_know_key"}]),
             LEAVE]),
    n_a=n("Maid", "At Whitby, Mrs W. says, sir. But here, I found her slippers wet one morning, standing by the window. I thought: she's been walking on the dew. Then I thought: no, I'm being silly.", end=True),
    n_key=n("Maid", "On the rack in the hall, sir, with all the other keys. Miss L.'s room, in the housekeeper's hand. We keep them all there. Mrs Westenra says it makes the house feel safe, sir.", end=True),
)
DIALOGUE["a3_maid_asleep"] = D("n0",
    n0=n("Maid", "(She mumbles, 'The port, the port... the gentleman said it was for the mistress.' Her head rolls. She is as insensible as a log.)",
         choices=[c("Try to rouse her.", next="n1"), LEAVE]),
    n1=n("Dr. Seward", "I shake her, slap her wrists, call her name. Her eyes roll open, and shut. Whatever she took has her fast. Smelling salts might do what shaking cannot; Mrs Westenra has a bottle in her dressing-case upstairs.", end=True),
)
DIALOGUE["a3_arthur_talk"] = D("n0",
    n0=n("Arthur", "Jack! Thank God. Is she... how bad is it? They would not let me stay at the Hall, with my father as he is, and I have been going out of my mind.",
         choices=[
             c("Arthur, Van Helsing says she needs a man's blood tonight. Will you give it?", cond="a3_vh_examined", next="n_help",
               do=[{"recruit": "arthur"}, {"set": "a3_arthur_ready"}]),
             c("Arthur, there is something I must tell you about the transfusions.", cond="a3_tx2", next="n_secret"),
             c("She is sleeping, Arthur. Be patient a little.", next="n_pat"),
             LEAVE]),
    n_help=n("Arthur", "Take what you want, Jack. Take all of it. I'd give my last drop and think it cheap. (He is already rolling his sleeve.)", end=True),
    n_pat=n("Arthur", "Patient. Yes. I have been told to be patient since June.", end=True),
    n_secret=n("Dr. Seward", "(The Professor has told me, bluntly, that Arthur must never know another man's blood has gone into her. A lover has jealousies even for gifts.) Arthur... I mean to tell you the truth about this.",
               choices=[c("I gave her blood too, Arthur.", next="n_s_truth", do=[{"set": "a3_told_arthur"}]),
                        c("Nothing. Only that you saved her life.", next="n_s_keep", do=[{"set": "a3_secret_kept"}])]),
    n_s_truth=n("Arthur", "You gave... then in a manner of speaking, she is... (He is white.) No. No, Jack, I'm sorry. I'm sorry. You saved her too. I am the lowest kind of fool to be jealous of a doctor's arm.", end=True),
    n_s_keep=n("Arthur", "Then I am the happiest man in London tonight, and I would not have it otherwise.", end=True),
)
DIALOGUE["a3_quincey_talk"] = D("n0",
    n0=n("Quincey Morris", "Jack. I came on the first train after your wire. Arthur said to come quick and not to ask questions, and I never do. Looks to me as if you fellows have been through a stampede.",
         choices=[
             c("Quincey, Lucy needs blood, and the Professor says yours is the best we have.", next="n_blood",
               cond="!a3_quincey_ready", do=[{"recruit": "quincey"}, {"give": "brandy"}, {"set": "a3_quincey_ready"}]),
             c("Tell me about the bat on the Pampas.", next="n_bat"),
             LEAVE]),
    n_blood=n("Quincey Morris", "A brave man's blood is the best thing on this earth when a woman's in trouble. I'm your man, Jack. And here, take my flask. Texan brandy. It will put a fire in anyone's veins.", end=True),
    n_bat=n("Quincey Morris", "Out on the Pampas, my mare, the best in the world, was found dead one morning with two little punctures in her throat and not a drop in her. One of those big bats that they call vampires had been at her. I've been thinking of her all night.", end=True),
)

# ------------------------------------------------------------------ the telegram (timing puzzle)
DIALOGUE["a3_boy_wire"] = D("n0",
    n0=n("Telegraph boy", "You want to send a wire, sir? I take 'em to the office at Hampstead. Office shuts at eight, sir, and the last Amsterdam collect goes out at half past seven. What's the message?",
         choices=[
             c("'Come tomorrow morning if convenient. Lucy unwell.'", cond="has:a3_telegram_form", next="n_late"),
             c("'Come by the day train through Calais and Dover; two changes.'", cond="has:a3_telegram_form", next="n_slow"),
             c("'Come by the night boat from the Hook; boat-train reaches Liverpool Street 6.05; urgent, a matter of life.'",
               cond="has:a3_telegram_form&journal:a3_j_bradshaw&a3_examined_lucy", next="n_ok",
               do=[{"take": "a3_telegram_form"}, {"set": "a3_wired_vh"}, {"journal": "a3_j_wired"}]),
             c("I am not ready to send it yet.", end=True)]),
    n_late=n("Dr. Seward", "'Tomorrow morning if convenient' is no message to send to a man who runs a hospital. Lucy may not have the day to spare. I tear it up.", next="n0"),
    n_slow=n("Dr. Seward", "Two changes and a long day. He would arrive tomorrow evening, if the Channel is kind. No. The night boat, surely.", next="n0"),
    n_ok=n("Telegraph boy", "'Night boat, 6.05, urgent, a matter of life.' That'll fetch him, sir. Never saw a wire to Amsterdam with so few words. I'll run.", end=True),
)

# ------------------------------------------------------------------ Lucy and the Professor
DIALOGUE["a3_lucy_talk"] = D("n0",
    n0=n("Lucy", "Dr. Seward. How kind of you to come all this way. I hope you don't think I'm ill. I'm so sleepy, that's all. And Arthur's poor father... I wish he were here.",
         choices=[
             c("How are you feeling, Lucy?", next="n_feel"),
             c("May I look at your throat, Lucy?", cond="a3_met_mother", next="n_exam",
               do=[{"set": "a3_examined_lucy"}, {"journal": "a3_j_hillingham"}, {"journal": "a3_j_lucy_exam"}]),
             c("Do you walk in your sleep?", next="n_walk", do=[{"set": "a3_asked_sleepwalk"}]),
             c("Do you remember the flowers last night?", cond="a3_night1", next="n_flowers", do=[{"set": "a3_lucy_denies"}]),
             c("Lucy, Arthur is here. He has come to see you.", cond="a3_tx4&party:arthur", next="d1"),
             LEAVE]),
    n_feel=n("Lucy", "Weak, and rather faint, and hungry for a thing I don't know the name of. I dream so vividly, Doctor. There is a flapping at the window, and a long thin shadow, and sometimes a pair of red eyes that I can't bring myself to dislike.", end=True),
    n_exam=n("Lucy", "If you must. (She lifts the lace at her collar, and I see them.) Two little punctures, white-edged, not deep, not angry. They will not heal. She says she must have pricked herself on a safety-pin.", end=True),
    n_walk=n("Lucy", "Mamma says I did at Whitby. I woke on the East Cliff once, with Mina beside me, and I was freezing. But I haven't, here. I'm sure I haven't.", end=True),
    n_flowers=n("Lucy", "Flowers? I never liked garlic before, but last night it was delightful. I slept as I have not slept in weeks. In the morning... it was all gone from my neck? I don't remember. I don't remember taking it off.", end=True),
    d1=n("Lucy", "(Her eyes open, blue and clear, and a little flush has come into her cheeks.) Arthur. Dear Arthur. Is it really you? I dreamed you'd come, and now I can't tell the dream from the room.", next="d2"),
    d2=n("Arthur", "(He kneels by the bed and takes her hand. He cannot speak for a moment.) Lucy. My Lucy. I am here, and I shall not leave you.", next="d3"),
    d3=n("Lucy", "(Very softly, to him alone.) Kiss me, Arthur.",
         choices=[
             c("[Let Arthur kiss her mouth.]", next="d_wrong"),
             c("[Say, 'Arthur, the forehead.']", next="d_forehead")]),
    d_wrong=n("Van Helsing", "(He is across the room before I can speak, and his hand is on Arthur's shoulder.) No! Not on your life! Not for your life, nor hers!  Arthur... the forehead, only the forehead, I implore you.", next="d_forehead"),
    d_forehead=n("Arthur", "(He kisses her on the forehead, and she smiles, and closes her eyes, and the smile does not change.) Lucy? Lucy?",
                 do=[{"set": "a3_lucy_dead"}, {"journal": "a3_j_lucy_death"}], next="d_end"),
    d_end=n("Dr. Seward", "She does not answer. The colour that fed her cheek stays there, and her lips are red and soft in the candle, and she looks more beautiful than I have ever seen her. I put my fingers to her wrist. Nothing. Van Helsing takes Arthur out gently; Quincey follows. I stay with her.", end=True),
)

DIALOGUE["a3_vh_talk"] = D("n0",
    n0=n("Van Helsing", "Friend John. You have the face of a man who has not slept, which is correct. You may speak.",
         choices=[
             c("Professor, what do you make of her?", cond="a3_vh_arrived&!a3_vh_examined", next="q1"),
             c("What must be done tonight?", cond="a3_vh_examined", next="n_plan", do=[{"journal": "a3_j_garlic_rules"}, {"set": "a3_know_supplies"}]),
             c("Show me again how to ward the room.", cond="a3_vh_examined", next="n_ward"),
             c("Professor, look at the petals and the slippers.", cond="a3_night1&a3_saw_petals&a3_saw_slippers", next="sw1"),
             c("Mrs Westenra threw out the garlic and opened the window.", cond="a3_night2", next="n_mw"),
             c("Professor, the wolf. What is it? Where did it come from?", cond="a3_wolf_down", next="n_wolf"),
             LEAVE]),
    q1=n("Van Helsing", "I have looked, friend John, but you have looked first. Tell me what you saw. Three questions, as a surgeon answers before a student. Where are the marks?",
         choices=[c("On her wrist, like a bad vaccination.", next="qw1"),
                  c("On her throat, two small punctures, white-edged and torn.", next="q2"),
                  c("On her ankle, where a bat might alight.", next="qw1")]),
    qw1=n("Van Helsing", "No, friend John. Think. Look again with the candle. You are a physician and you have an eye. Use it.", next="q1"),
    q2=n("Van Helsing", "Good. And what does she do, in the evenings? What happens to her, in the night, that does not happen to other sick girls?",
         choices=[c("She sleeps badly from nerves, nothing more.", next="qw2"),
                  c("She sleeps with the window open, walks in her sleep, and wakes weaker each morning.", next="q3"),
                  c("She has consumption; the pallor shows it.", next="qw2")]),
    qw2=n("Van Helsing", "No. A phthisis does not shift with the window. Think about her nights.", next="q2"),
    q3=n("Van Helsing", "Good. And now the hardest question. She has lost, I judge, a great deal of blood. We cannot do the most simple thing, give it back, with a single man. Whose blood first?",
         choices=[c("Her mother's: she is of the same blood.", next="qw3"),
                  c("Arthur's: her betrothed, who loves her.", next="q_done"),
                  c("A stranger's from the hospital.", next="qw3")]),
    qw3=n("Van Helsing", "No. Her mother's heart would stop. A stranger's... it is not wrong, but he is not the man whose blood is a gift. Think again, friend John. The man she loves.", next="q3"),
    q_done=n("Van Helsing", "Exactly. Arthur's. And then yours, and then mine, and, when God sends him, a fourth. Fetch Arthur. And you shall prepare: the black bag with the tubing, the brandy, the chloral for her sleep; I will bring the flowers.",
             do=[{"set": "a3_vh_examined"}, {"journal": "a3_j_vh_exam"}], end=True),
    n_plan=n("Van Helsing", "Four things tonight. First, the black bag, your silver tubing and lancets. Second, brandy, for the donor, afterwards, and for you when you faint. Third, a sleeping draught, chloral; she must not be awake or the sight will frighten her. Fourth, her room: garlic at the window, at the door, in the chimney, and a wreath for her neck. And then, we pray.", end=True),
    n_ward=n("Van Helsing", "Window, door, chimney, neck. A chimney is a door to what is thin enough. And the neck: a wreath tied with white ribbon, so it does not fall. Rub the flowers, press them into the cracks. Leave nothing out, friend John. A ward with one hole is no ward at all.", end=True),
    sw1=n("Van Helsing", "You have seen the petals. You have seen the slippers. They are a story. Tell me what happened in this room, in the night.",
          choices=[c("Mrs Westenra came in meaning well, and took the garlic away.", next="sw_w1"),
                   c("The maid came in and cleared the room.", next="sw_w2"),
                   c("Lucy herself rose in her sleep, took off the wreath, swept the window, and lay down again.", next="sw_ok")]),
    sw_w1=n("Van Helsing", "No. Her mother did not come near. The trail begins at the bed and ends at the window, and no hand but hers made it. Think again.", next="sw1"),
    sw_w2=n("Van Helsing", "The maid is here for the daylight, not the night. Her footprints do not wander. No.", next="sw1"),
    sw_ok=n("Van Helsing", "Yes. Asleep, walking, drawn by something that is not her, she undid what we did, and does not remember. The thing that hunts her has found a will that is weaker than the flowers. So: we lock her door and keep the key. We pin her window shut with iron. And we wake her, friend John, if we must. Find the key on the hall rack. The pin is in the garden somewhere; a cottage garden always has an iron pin.",
            do=[{"set": "a3_sleepwalk_solved"}, {"journal": "a3_j_sleepwalk"}], end=True),
    n_mw=n("Van Helsing", "(He sits down on the edge of the bed with his hands between his knees. His shoulders shake, and he laughs, and it is not laughter.) Oh, God. God forgive me; I am a fool. That good, kind woman has killed her daughter, and she believes she was kind. Friend John, there is only one thing left. You are strong, and so is Arthur; I am older, but I am here. The third transfusion shall be mine. Speak to Mrs Westenra. Persuade her.",
          do=[{"set": "a3_vh_plan"}], end=True),
    n_wolf=n("Van Helsing", "A wolf from the Gardens, friend John. Escaped, by every account in the paper. That is the plain explanation, and I have not the heart to give you the other. Go. See to the servants. Something has gone through this house tonight that wanted all its doors open.", end=True),
)

DIALOGUE["a3_transfusion_bed"] = D("n0",
    n0=n("Dr. Seward", "Lucy lies white on the pillow, her breath no louder than a moth's. The black bag, the tubing, the lancets are ready, if I am; and a donor, and brandy for afterwards, and chloral to keep her from seeing what is done.",
         choices=[
             c("First transfusion: Arthur's blood.", cond="party:arthur&has:a3_transfusion_kit&has:brandy&has:chloral&a3_vh_examined&!a3_tx1", next="t1",
               do=[{"set": "a3_tx1"}, {"journal": "a3_j_tx1"}]),
             c("Second transfusion: my own blood.", cond="a3_night1&a3_sleepwalk_solved&has:a3_transfusion_kit&has:brandy&a3_tx1&!a3_tx2", next="t2",
               do=[{"set": "a3_tx2"}, {"journal": "a3_j_tx2"}]),
             c("Third transfusion: Van Helsing's blood.", cond="a3_night2&party:vanhelsing&has:a3_transfusion_kit&has:brandy&has:chloral&a3_tx2&!a3_tx3", next="t3",
               do=[{"set": "a3_tx3"}, {"journal": "a3_j_tx3"}]),
             c("Fourth transfusion: Quincey Morris.", cond="a3_wolf_down&party:quincey&has:a3_transfusion_kit&has:brandy&has:chloral&a3_tx3&!a3_tx4", next="t4",
               do=[{"set": "a3_tx4"}, {"journal": "a3_j_tx4"}]),
             c("Use Mrs Westenra's blood. She is her mother.", next="n_mother"),
             c("Ask Arthur to give again so soon.", next="n_again"),
             LEAVE]),
    n_mother=n("Van Helsing", "No! Her heart is a thing that will stop at a loud word. The blood would do no good, and the shock would be worse than the loss. Another donor, friend John.", next="n0"),
    n_again=n("Van Helsing", "A man may give a little, once. Not twice in a day. We shall have to find other donors, and lose no time about it.", next="n0"),
    t1=n("Van Helsing", "Chloral in water, a cup, drink. Good, she sleeps. Now, Arthur, your arm. (He lays the cut vein to the silver tube; the blood goes in, and the colour comes to her cheek like dawn.) Good. Brandy for Arthur. Not a word to him of what we shall do hereafter, friend John. A lover is jealous of everything, even the gift.", end=True),
    t2=n("Van Helsing", "You, friend John. Roll the sleeve. (I lie back and he opens the vein. It does not hurt; it is merely cold. The room goes grey, then white; the brandy brings it back.) She has colour. Say nothing to Arthur. It is our secret, and a good one.", end=True),
    t3=n("Van Helsing", "Mine, then. (He is shaking, though not with fear.) I am not young. Do not stare, friend John; it is my arm, not yours, that I am wasting. (The tube is warm. His face is grey and his jaw is set. He says, quietly, 'We fight him all the same.')", end=True),
    t4=n("Quincey Morris", "(He peels off his coat, rolls his sleeve, and lies down on the sofa-bed with his boots on.) Do it quick, Doc. I never had a tooth drawn easier. (The tube hums. His colour holds. Van Helsing, white at the mouth, injects morphia under Lucy's skin to keep her still.) A brave man's blood is the best thing on earth.", end=True),
)

DIALOGUE["a3_vigil"] = D("n0",
    n0=n("Dr. Seward", "The chair by the bed. The candle. The ticking. A man can sit here and keep time against the dark. But only if everything else has been done first.",
         choices=[
             c("Keep watch through the first night.", cond=G1 + "&a3_tx1&!a3_night1", next="v1",
               do=[{"set": "a3_night1"}, {"journal": "a3_j_night1"},
                   {"card": "8 September.  Morning.  The wreath is on the floor."}]),
             c("Keep watch through the second night.", cond=G2 + "&a3_door_locked&a3_window_pinned&a3_night1&a3_tx2&!a3_night2", next="v2",
               do=[{"set": "a3_night2"}, {"journal": "a3_j_mother_removed"}, {"card": "12 September.  Morning.  The window is open, and Mrs Westenra is smiling."}]),
             c("Keep watch for the days that follow.", cond=G3 + "&a3_door_locked&a3_window_pinned&a3_night2&a3_tx3&a3_mother_agrees&!a3_night3", next="v3",
               do=[{"set": "a3_night3"}, {"journal": "a3_j_peace"}]),
             c("Keep watch through the seventeenth night.", cond="a3_night3&!a3_wolf_started", next="v4",
               do=[{"set": "a3_wolf_started"}, {"card": "17 September.  Midnight.  Something is at the glass."},
                   {"fight": "a3_berserker_night"}]),
             LEAVE]),
    v1=n("Dr. Seward", "I sit, and doze, and nod, and the candle sinks. Towards dawn something wakes me; I cannot say what. The wreath is on the floor, the garlic has been swept off the sill, and the window is ajar. Lucy has not moved. She is white as paper.", end=True),
    v2=n("Dr. Seward", "I slept at the Professor's order, in the next room, and for the first time in days I slept. When I woke, Mrs Westenra was in Lucy's room opening the shutters and singing, with a handful of garlic flowers in her apron. She had meant it kindly. The room was cold.", end=True),
    v3=n("Dr. Seward", "Four days. Every morning a box from Haarlem, and every evening the same quiet. Lucy eats a little and laughs a little, and Mrs Westenra, true to her promise, will not so much as touch the door. At night something taps, and flaps, and Van Helsing says it is a bat, and does not say it with a smile. On the fifth night the wind rises.", end=True),
    v4=n("Dr. Seward", "Outside, a long howl, and a thin one answering it, and the whole house cowers.", end=True),
)

DIALOGUE["a3_lucy_corpse"] = D("n0",
    n0=n("Dr. Seward", "She lies so quietly. The candles are lit at head and foot, and Van Helsing is standing at the window with his back to me, very straight.",
         choices=[
             c("Look closely at her mouth.", cond="!a3_teeth_seen", next="n_teeth", do=[{"set": "a3_teeth_seen"}, {"journal": "a3_j_teeth"}]),
             c("Search for the paper Van Helsing noticed at her breast.", cond="!a3_got_memo", next="n_memo",
               do=[{"give": "a3_lucy_memo"}, {"set": "a3_got_memo"}, {"journal": "a3_j_memo"}]),
             c("Ask Van Helsing what we must do now.", cond="a3_teeth_seen&has:a3_lucy_memo", next="n_do", do=[{"set": "a3_ready_funeral"}]),
             LEAVE]),
    n_teeth=n("Van Helsing", "(He draws her lip back with a finger. The canine teeth are longer and sharper than any I have seen in a living mouth.) You have eyes, friend John. You see them? Remember this, and tell no one. I shall explain later, and you will not believe me, and that is as it should be.", end=True),
    n_memo=n("Dr. Seward", "It is folded small, in the fold of her nightgown over her heart. 'Hillingham, 12 September. Arthur, if you read this, forgive me; I am not myself. There is something in the night that is not a dream. I am so frightened of what I am becoming...' The handwriting fails near the end.", end=True),
    n_do=n("Van Helsing", "The funeral, friend John. The undertaker comes in the morning. You will say nothing to Arthur of the teeth, nothing of the paper. We shall bury her as a Christian woman, in her own vault, and we shall watch, afterwards. The hearse is at the garden gate. Come.", end=True),
)

# ------------------------------------------------------------------ Kingstead (finale)
DIALOGUE["a3_vh_final"] = D("n0",
    n0=n("Van Helsing", "Friend John. The others have gone to the carriages. Stay a moment. Look at the vault, and tell me what you see.",
         choices=[
             c("What did you mean, 'it is not finished'?", next="n_unf"),
             c("Professor, the garlic.", next="n_garlic", cond="!a3_got_funeral_garlic", do=[{"give": "garlic"}, {"set": "a3_got_funeral_garlic"}]),
             c("The memorandum. 'There is something in the night.' What is it?", cond="has:a3_lucy_memo", next="n_memo"),
             c("I am ready to go back to Purfleet.", cond="a3_garlic_in_tomb&a3_teeth_seen", end=True,
               do=[{"journal": "a3_j_funeral"},
                   {"card": "Lucy lies in her marble vault at Kingstead.  Van Helsing keeps the key, and will not say why.  The death notices are all in the Westminster Gazette.  Another story is beginning, on Hampstead Heath, at night."},
                   {"goto": "a4_hampstead_heath"}]),
             LEAVE]),
    n_unf=n("Van Helsing", "I mean that you will see, friend John. In a week, in a fortnight, there will be news in the papers that you will read with a clear head. When it comes, remember that I was not mad. Remember her teeth.", end=True),
    n_garlic=n("Van Helsing", "You have some garlic still? Lay it on the coffin, and across the door. It is a custom of the country where I was born. I ask you to do it for her sake, not for mine, and not to laugh.", end=True),
    n_memo=n("Van Helsing", "It is the voice of a girl who was not alone in her room. Keep it. If Arthur ever asks, you will tell him that she wrote of him with love, which is the truth. The rest, we shall see.", end=True),
)
DIALOGUE["a3_arthur_funeral"] = D("n0",
    n0=n("Arthur", "I cannot believe it, Jack. A month ago she was laughing on the lawn. A month. And I was there at the end, and I did not know what I was seeing. You and the Professor knew, I think. I don't ask. I am not able to ask.", end=True),
)
DIALOGUE["a3_quincey_funeral"] = D("n0",
    n0=n("Quincey Morris", "Funeral. Never could abide funerals. Never could stay away from one, either. Look after Art, Jack. He'll want somebody to hold on to, and he'll pretend he doesn't.", end=True),
)
DIALOGUE["a3_gravedigger"] = D("n0",
    n0=n("Sexton", "Forty years, sir, I've been putting 'em in, and never once buried a young lady with so many gentlemen in a row. Quiet, they were. Real quiet. Four of 'em, and the foreign one.",
         choices=[c("Did you notice anything unusual?", next="n1"), LEAVE]),
    n1=n("Sexton", "No, sir. Only that the Professor made us bring the coffin up a second time to look at the lid. And he wanted the key, and wouldn't let it go. And the dog won't come near the yew. Might be nothing.", end=True),
)


# ---- garlic wards come in three rounds (the night events undo the earlier ones), so each round has its own targets
_bed = LOC_DATA["a3_lucy_bedroom"]


def _clone_wards():
    protos = {p["id"]: p for p in _bed["props"]}
    door, seat, fire = protos.pop("a3_door_hall"), protos.pop("a3_window_seat"), protos.pop("a3_bed_fire")
    lucy = next(x for x in _bed["npcs"] if x["id"] == "a3_lucy")
    _bed["props"] = [p for p in _bed["props"] if p["id"] not in ("a3_door_hall", "a3_window_seat", "a3_bed_fire")]
    _bed["npcs"] = [x for x in _bed["npcs"] if x["id"] != "a3_lucy"]
    stages = {1: "!a3_night1", 2: "a3_night1&!a3_night2", 3: "a3_night2"}
    for r, cond in stages.items():
        for proto, key, flag, extra in ((door, "door", "a3_g%d_door", {"a3_door_key": [{"set": "a3_door_locked"}, say("I turn the key in the lock and pocket it. Whoever wants in must come through a door I hold.")]}),
                                        (seat, "window", "a3_g%d_window", {"a3_window_pin": [{"set": "a3_window_pinned"}, say("I drop the iron pin through the sash-staples. The window is now a wall.")]}),
                                        (fire, "chimney", "a3_g%d_chimney", {})):
            if r == 2 and key in ("door", "chimney"):
                if key == "chimney":
                    continue
            q = copy.deepcopy(proto)
            q["id"] = proto["id"] + "_r%d" % r
            q["if"] = cond
            ui = {"garlic": [{"set": flag % r}, say("I rub garlic flowers into the %s as the Professor showed me." % key)]}
            if r >= 2 or key == "door":
                ui.update(extra) if r >= 2 else None
            q["interact"]["use_item"] = ui
            _bed["props"].append(q)
        if r != 2 or True:
            q = copy.deepcopy(lucy)
            q["id"] = "a3_lucy_r%d" % r
            q["if"] = cond + "&!a3_lucy_dead" if r != 3 else "a3_night2&!a3_lucy_dead"
            q["interact"]["use_item"] = {"garlic": [{"set": "a3_g%d_neck" % r}, say("A garland of garlic flowers around her neck, tied with white ribbon, as the Professor taught me.")]}
            _bed["npcs"].append(q)


import copy
_clone_wards()


# =============================================================================================================
# Condition normalisation.  game.gd's check() tests the has:/party:/journal:/prot:/'!' prefixes BEFORE it splits on '&',
# so a compound condition must not START with one of those.  A flag that is always true (a3_begun, set in ACT.start)
# is prepended where needed, so every compound condition in this act evaluates correctly in the engine.
# =============================================================================================================
_BAD_FIRST = ("has:", "party:", "journal:", "prot:", "!")


def _fix_cond(cond):
    if isinstance(cond, str) and "&" in cond and cond.startswith(_BAD_FIRST):
        return "a3_begun&" + cond
    return cond


def _fix_doc():
    for ld in LOC_DATA.values():
        for ent in ld.get("props", []) + ld.get("npcs", []):
            if "if" in ent:
                ent["if"] = _fix_cond(ent["if"])
            it = ent.get("interact", {})
            if "go_cond" in it:
                it["go_cond"] = _fix_cond(it["go_cond"])
        for e in ld.get("on_enter", []):
            if "if" in e:
                e["if"] = _fix_cond(e["if"])
    for dlg in DIALOGUE.values():
        for nd in dlg["nodes"].values():
            for ch in nd.get("choices", []):
                if "cond" in ch:
                    ch["cond"] = _fix_cond(ch["cond"])
    for opts in GATES.values():
        for o in opts:
            o["cond"] = _fix_cond(o["cond"])


_fix_doc()
