#!/usr/bin/env python3
"""Hand-picked objectives for Acts II-VI (Act I is written directly in data/objectives.json, the arcs come from gen_objectives.py).

    python3 pipeline/objectives_curated.py

For each act: the key story beats, in play order, as (journal id the beat writes, objective text, first hint). The second and third
hints (where it is, what to do) are taken from the generated entry of the same journal id, which is derived from world.json and so
always true. `done` is that journal entry. The act replays check that every objective here is done by the end of the act.
Run gen_objectives.py first (it fills data/objectives.json from the replays), then this file replaces the entries of Acts II-VI.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CURATED = {
 "2": [
  ("a2_j_proposals", "Hear Lucy's news", "Lucy is bursting to tell you something."),
  ("a2_j_seward_diary", "Listen to Dr. Seward's phonograph diary", "Dr. Seward keeps his case notes on wax cylinders."),
  ("a2_j_swales", "Meet old Mr. Swales on the East Cliff", "An old man on the churchyard benches has strong views about the dead."),
  ("a2_j_hut_clue", "Read the notices in the coastguard's hut", "The harbour men pin their notices up in the coastguard's hut."),
  ("a2_j_storm", "Watch the Demeter run ashore in the storm", "A great storm is coming. The cliff is the place to watch it from."),
  ("a2_j_captain", "Go aboard the wreck and find her captain", "The harbour officers can tell you how to get aboard the wreck."),
  ("a2_j_log", "Read the log of the Demeter", "Whatever was written aboard has been taken ashore."),
  ("a2_j_gone", "Find out why Lucy's bed is empty", "Something is wrong with Lucy's room."),
  ("a2_j_pin", "Find Lucy on the churchyard seat at night", "Where did Lucy walk in her sleep before?"),
  ("a3_j_seward_diary", "Go on to Dr. Seward's asylum at Purfleet", "There is nothing more to do in Whitby."),
 ],
 "3": [
  ("a3_j_dose", "Learn the chloral rule", "Dr. Seward writes down everything he gives his patients."),
  ("a3_j_fence", "Find the loose slat in the asylum wall", "Somebody must be slipping out of the asylum grounds."),
  ("a3_j_zoo", "Visit the Zoological Gardens", "A keeper of the wolves has a strange story about a night of storm."),
  ("a3_j_hillingham", "Go to Hillingham, where Lucy lies ill", "Lucy is being nursed at her mother's house."),
  ("a3_j_lucy_exam", "Examine Lucy's throat", "Look at Lucy herself."),
  ("a3_j_mina_hospital", "Find Jonathan at the hospital in Buda-Pesth", "Sister Agatha has sent word from abroad."),
  ("a3_j_wedding", "Marry Jonathan in the hospital chapel", "Sister Agatha will stand as witness."),
  ("a3_j_vh_exam", "Have Van Helsing examine Lucy", "Seward has sent for a specialist."),
  ("a3_j_tx1", "Give Lucy the first transfusion", "The Professor says Lucy needs blood."),
  ("a3_j_servants", "Find the drugged maids", "Someone made sure the household slept."),
  ("a3_j_burial", "Go to Lucy's burial at Kingstead", "There is one more sad duty."),
  ("a4_j_heath", "Go out to Hampstead Heath", "The next trouble is out on the Heath."),
 ],
 "4": [
  ("a4_j_gazette", "Read the Westminster Gazette", "The papers are full of a strange story."),
  ("a4_j_child_wound", "See the wound on the child at the hospital", "A child was hurt, and the doctors are puzzled."),
  ("a4_j_doubt", "Face the Professor's doubts in Seward's study", "Van Helsing does not yet say what he thinks."),
  ("a4_j_jonathan", "Visit Jonathan in Paddington", "Mina and Jonathan have news of their own."),
  ("a4_j_papers", "Go through Lucy's papers at Hillingham", "Lucy left things behind at her mother's house."),
  ("a4_j_lock", "Cut a key for the tomb lock", "The undertaker described the lock."),
  ("a4_j_night1", "Open the Westenra tomb and look in the coffin", "Lucy's tomb at Kingstead is the place to look."),
  ("a4_j_child_found", "Find the child in the churchyard at night", "Something white moves among the graves at night."),
  ("a4_j_arthur", "Gain Arthur's consent", "Arthur must agree before anything is done."),
  ("a4_j_stake", "Set the stake in the tomb", "The Professor knows what must be done."),
  ("a4_j_peace", "Seal the tomb", "The last task at the tomb."),
  ("a5_j_arrival", "Go back to Purfleet", "The hunt goes on at the asylum."),
 ],
 "5": [
  ("a5_j_harker_meet", "Meet Jonathan Harker in Seward's library", "Jonathan has something to show."),
  ("a5_j_link_renfield", "Learn that Renfield is the door", "Mina is putting the records in order."),
  ("a5_j_rules", "Hear from Van Helsing what the Un-Dead are", "The Professor has rules to teach."),
  ("a5_j_carfax_enter", "Search Carfax by lantern light", "The Count's English house must be searched."),
  ("a5_j_ledger", "Read the carriers' ledger", "The boxes had to be carried somewhere."),
  ("a5_j_bloxam", "Find Sam Bloxam of Walworth", "One of the carters may remember more."),
  ("a5_j_agent", "Question the house agents", "Someone sold the Count his houses."),
  ("a5_j_attack", "Survive the Count's visit to the Harkers' bedroom", "The Count is not done with Mina."),
  ("a5_j_bond", "Learn of the bond with Mina", "Mina feels something she cannot explain."),
  ("a5_j_bermondsey", "Search the boxes in Bermondsey", "The boxes were sent to more than one house."),
  ("a5_j_mile_end", "Search the boxes in Mile End", "There is another house to search."),
  ("a6_j_oath", "Go to Varna", "The hunt now goes abroad."),
 ],
 "6": [
  ("a6_j_lloyds", "Read Lloyd's report", "Shipping reports are kept at Lloyd's agency."),
  ("a6_j_telegram", "Follow the telegram to Galatz", "A telegram from Lloyd's has changed the plan."),
  ("a6_j_donelson", "Hear Captain Donelson's tale", "The captain of the Czarina Catherine has a tale to tell."),
  ("a6_j_hildesheim", "Call on Hildesheim's office", "A receipt may show who handled the box."),
  ("a6_j_skinsky", "Find out about Petrof Skinsky", "A death in a churchyard has left a clue."),
  ("a6_j_memorandum", "Read Mina's memorandum", "Mina has been setting down everything they know."),
  ("a6_j_launch", "Pursue the boxes by steam launch", "The river is the quickest way."),
  ("a6_j_veresti", "Reach the inn at Veresti", "The road leads on through the mountains."),
  ("a6_j_circle", "Make the holy circle below the castle", "Mina must be kept safe."),
  ("a6_j_castle", "Enter Castle Dracula", "The castle itself waits at the end of the road."),
  ("a6_j_tomb", "Find the Count's tomb in the old chapel", "He sleeps by day in the old chapel."),
  ("a6_j_final", "Stop the wagon on the plain below the castle", "The Szgany are bringing the box to the castle before sunset."),
  ("a6_j_quincey", "Stand with Quincey in the snow at sunset", "It ends in the snow, with the sun going down."),
 ],
}

# personal arcs: (journal id without the "<arc>_j_" prefix, text, first hint)
CURATED_ARCS = {
 "arthur_burden": [
  ("blessing", "Receive your father's blessing", "Your father has something to say before you go."),
  ("steward", "Hear the steward Wilkes confess", "Something is wrong in the estate office."),
  ("proposal", "Give Lucy the ring and the rose", "Lucy is waiting in the garden at Hillingham."),
  ("telegram_back", "Receive the telegram at the summer-house", "News is coming for you from home."),
  ("death", "Return to the Ring: your father is dead", "You are needed at home."),
  ("terms", "Hear Mr. Crowle's terms", "The banker has come to see you."),
  ("vault_open", "Open the door of the family vault", "The family chapel holds the way to the vault."),
  ("tenants", "Hear the tenants' petition", "The tenants have a request."),
  ("muniment", "Search the muniment room", "The family papers are kept in the muniment room."),
  ("sickroom", "Return to your father's chamber", "Where did it all begin?"),
 ],
 "demeter_voyage": [
  ("cargo", "Check the bill of lading", "The ship's papers must be put in order first."),
  ("cleared", "Clear customs", "The customs officer must pass the cargo."),
  ("blessed", "Receive the priest's blessing", "A sailor does not leave without a blessing."),
  ("sail", "Give the order to sail", "The mate is waiting for your word."),
  ("cabin", "Look into your cabin", "Walk the ship from end to end."),
  ("hold", "Go down into the hold", "The cargo lies below."),
  ("weather", "Read the weather at the wheel", "The sky and the glass will tell you."),
  ("olgaren", "Question Olgaren about the tall thin man", "One of the crew keeps his eyes down."),
  ("box", "Open box thirteen", "One box in the hold is not like the rest."),
  ("end", "Lash yourself to the wheel", "The last duty of a captain."),
  ("varna", "Return to the quay at Varna", "The voyage began on a quay."),
 ],
 "dracula_voivode": [
  ("council_closed", "Hear the counsellor and close the gates", "The counsellor is waiting in the great hall."),
  ("chest", "Open the Order chest in your father's chamber", "Your father's chamber keeps a secret."),
  ("radu_chained", "See Radu in the cells", "Your brother is held in the castle."),
  ("sealed", "Seal the order", "An order is waiting to be sealed."),
  ("beacon", "Light the beacon on the watch-tower", "The ridge must be warned."),
  ("refugee", "Meet the grandmother on the mountain road", "The road is full of refugees."),
  ("prisoner_broken", "Question the captured Akinji", "The camp holds a prisoner."),
  ("ford", "Raid the Reed Ford by night", "The army must cross the river."),
  ("school", "Enter the Scholomance", "A school stands by the lake."),
  ("rite", "Take part in the rite of three", "The students gather at the altar."),
  ("forged", "Find the tenth name in the forbidden library", "The School's roll is kept in the library."),
  ("tithe_vasile", "Face the Master of the tithe", "The school exacts a price."),
  ("end_vigil", "Keep Ileana's vigil in the castle chapel", "The night ends in the chapel."),
 ],
 "harker_road": [
  ("trunk", "Open your father's trunk", "Something of your father's is among your things."),
  ("engaged", "Meet Mina at the school", "Mina is at the school."),
  ("task", "Hear Mr. Hawkins about the Count's wishes", "Mr. Hawkins has a commission for you."),
  ("letters", "Read the Count's letters", "The Count's letters are kept in the office."),
  ("museum", "Read up on Transylvania", "The Reading Room has books on the country."),
  ("climb", "Climb down the castle wall", "The window is the only way out."),
  ("search", "Search the earth-box in the vault", "There is a box in the old chapel."),
  ("szgany", "Meet the Szgany at their fire", "Someone is camped on the mountain path."),
  ("woke", "Wake in the hospital with Sister Agatha", "You are among kind strangers."),
  ("letter", "Write to Mina", "There is someone you must tell."),
  ("proposal", "Make your proposal", "There is something you have to ask Mina."),
  ("morning", "Walk out on a May morning in Exeter", "The road ends where it began."),
 ],
 "lucy_summer": [
  ("flowers", "Please Mamma with the flowers", "Mamma is in the parlour."),
  ("mina_letter", "Read Mina's letters", "Mina has written."),
  ("seward", "Meet Dr. Seward in the garden", "A visitor is waiting in the garden."),
  ("quincey", "Meet Mr. Morris", "Another visitor has come."),
  ("arthur", "Meet Arthur", "A third visitor has come."),
  ("mina_walk", "Walk with Mina on the East Cliff", "Mina is on the cliff."),
  ("swales", "Hear Mr. Swales about the steps", "The old man on the cliff has a story."),
  ("anchor_p", "Meet the tall dark figure on the East Cliff at night", "The cliff is not empty at night."),
  ("counted", "Count the Abbey steps", "The steps are worth counting."),
  ("a_remember", "Write your last note to Arthur", "There is someone you must remember."),
 ],
 "mina_records": [
  ("edith", "Hear Edith's gossip", "A friend has news from the school."),
  ("task", "Accept Miss Hallam's bargain", "Miss Hallam has a task for you."),
  ("blotter", "Read the blotter in the mirror", "Something has been blotted."),
  ("cupboard", "Examine the prize cupboard", "A cupboard in the schoolroom holds a clue."),
  ("typed", "Make the typewriter speak", "The Remington can tell you something."),
  ("bradshaw", "Check Bradshaw for the Bristol line", "The trains must be checked."),
  ("letter_found", "Find Jonathan's letter at last", "The telegraph clerk may have it."),
  ("whitby", "Go to Whitby", "The seaside is next."),
  ("dreamorder", "Put your dream in order: water, wood, swing", "Your notes hold a pattern."),
  ("tomb3", "Read the third gravestone at dusk", "The old stones must be read in order."),
  ("trance", "Make the first deliberate trance", "The rocking-chair in your room."),
  ("end", "Follow the thread in the dark hold", "The end of the dream is below."),
 ],
 "quincey_hunt": [
  ("load", "Load the powder and lead", "Get ready first."),
  ("stolen", "Find out who took the horses", "The remuda is gone."),
  ("hobbs", "Take the old trapper's advice", "Old Hobbs knows the range."),
  ("signs", "Read the signs of the three trails", "The trails will show which way they went."),
  ("creek", "Cross the creek at the snag", "The cottonwood bottoms hide a crossing."),
  ("reunion", "Be reunited with Santa Fe", "Your horse is somewhere ahead."),
  ("anselmo", "Hear what Anselmo the gaucho knew", "A gaucho sits at a camp fire."),
  ("tale", "Listen to the tale by the fire", "The camp fire has a story."),
  ("mark", "Find the mark in the grass", "Dawn shows what the night left."),
  ("end", "Bring Santa Fe home", "The hunt ends where it began."),
 ],
 "renfield_mercy": [
  ("frenzy", "Find out what upset Room 12", "The attendant has something to say."),
  ("ledger", "Find the notebook of lives under the floorboard", "Something is hidden in the room."),
  ("sugar", "Look into the sugar ration", "The day-room keeps the stores."),
  ("count", "Learn what seven, three, nine mean", "The numbers mean something."),
  ("plea", "Make your plea to Dr. Seward", "The doctor must be asked."),
  ("cook", "Hear Cook and the rhyme", "The cook knows an old rhyme."),
  ("key", "Find the spider's key", "A key is hidden where nobody looks."),
  ("hodge", "Put the night attendant to sleep", "Someone must not be watching."),
  ("garden", "Slip out through the garden wicket", "The garden has a way out."),
  ("warning", "Leave your note for the doctor", "Someone must be warned."),
  ("wake", "Wake again in Room 12", "The night is over."),
 ],
 "seward_asylum": [
  ("hillingham", "Read Lucy's note", "A note has arrived."),
  ("debt", "Read the letters from Amsterdam", "Someone is owed a great debt."),
  ("grief", "Dictate your grief to the phonograph", "The phonograph is in your study."),
  ("vane", "Hear Miss Vane about her visitor", "A patient has had a visitor."),
  ("cell", "Visit Renfield in Room 12", "The most curious patient is in Room 12."),
  ("theory", "Hear Renfield's theory", "Renfield has a theory."),
  ("draught", "Weigh out the twenty-grain draught", "The dispensary keeps the scales."),
  ("slip", "Examine the forged prescription", "Somebody has forged a slip."),
  ("fire", "Put out the fire in the dispensary", "Something is burning."),
  ("sleepless", "Go back to your study, sleepless", "Three nights without sleep."),
 ],
 "vanhelsing_lore": [
  ("latin", "Read the Latin note", "A note lies in the study."),
  ("letters", "Read Arminius's letters", "The reading chair holds letters."),
  ("cross", "Receive the silver cross from your wife", "Someone at home has a gift."),
  ("debate", "Answer the Dean in the lecture-room", "The Dean has doubts."),
  ("rite", "Have the Host consecrated", "The chapel of St. Nicholas."),
  ("village", "Go to Kirchdorf in Styria", "A village far away needs help."),
  ("pastor", "Speak with Pfarrer Albrecht", "The pastor knows the village."),
  ("grave", "Ask the sexton about Katharina Lindner", "The sexton keeps the graves."),
  ("end", "Read what Arminius learned", "The last letter."),
 ],
}


def main():
    path = os.path.join(ROOT, "data", "objectives.json")
    data = json.load(open(path))
    world = json.load(open(os.path.join(ROOT, "data", "world.json")))
    for act, beats in CURATED.items():
        gen = {}
        for o in data.get(act, []):
            for part in o["done"].split("&"):
                gen[part.split(":", 1)[1]] = o
        out = []
        for jid, text, nudge in beats:
            assert jid in world["journal"], jid
            g = gen.get(jid)
            if g is None or g["hints"][2].startswith("Look for what"):
                raise SystemExit(f"{jid}: no generated 'where/what' hints for it (run gen_objectives.py first, or write them here)")
            out.append({"id": "o_" + jid, "text": text, "done": "journal:" + jid, "hints": [nudge, g["hints"][1], g["hints"][2]]})
        data[act] = out
        print(act, len(out), "objectives")
    for arc, beats in CURATED_ARCS.items():
        gen = {}
        for o in data.get(arc, []):
            for part in o["done"].split("&"):
                gen[part.split(":", 1)[1]] = o
        out = []
        for suffix, text, nudge in beats:
            jid = f"{arc}_j_{suffix}"
            assert jid in world["journal"], jid
            g = gen.get(jid)
            if g is None or g["hints"][2].startswith("Look for what"):
                raise SystemExit(f"{jid}: no generated 'where/what' hints for it")
            out.append({"id": "o_" + jid, "text": text, "done": "journal:" + jid, "hints": [nudge, g["hints"][1], g["hints"][2]]})
        data[arc] = out
        print(arc, len(out), "objectives")
    json.dump(data, open(path, "w"), indent=1)


if __name__ == "__main__":
    main()
