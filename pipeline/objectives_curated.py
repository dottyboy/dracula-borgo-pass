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
    json.dump(data, open(path, "w"), indent=1)


if __name__ == "__main__":
    main()
