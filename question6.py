from __future__ import print_function
__author__="Juliana Louback <jl4354@.columbia.edu>"

from utils import init_suffix_weights
from subprocess import call
from utils import weighted_history
from utils import set_tags
from utils import tagmodel_weights
from utils import suffix_weights
from utils import weighted_history2
from os import remove

"""
Usage:
python question6.py

Question 6: Create new features, build on model created in question5.py.

"""

def main():
    # Get suffix, tag and bigram feature vectors generated in quesiton4.py and question5.py
    weights = tagmodel_weights()
    weights.update(suffix_weights("suffix_tagger.model"))

    # Combo 1: Modify certain suffix rules: ============================================
    weights_1 = weights
    # suffix "ly" is usually ADV; increase weight
    weights_1["SUFFIX:ly:ADV"] = float(weights["SUFFIX:ly:ADV"]) + 3
    # suffix "ed" is usually VERB; increase weight
    weights_1["SUFFIX:ed:VERB"] = float(weights["SUFFIX:ed:VERB"]) + 3
    # suffix "ing" is usually VERB; increase weight
    weights_1["SUFFIX:ing:VERB"] = float(weights["SUFFIX:ing:VERB"]) + 0.05
    # Run model with suffix, tag and bigram features on development data
    weighted_history("tag_dev.dat","q4_histories",weights_1,"q6_weighted",True,True)
    best_tag = open("q6_best", "w")
    weighted = open("q6_weighted", "r")
    call(["python", "tagger_decoder.py", "HISTORY"], stdout=best_tag, stdin=weighted)
    # 4. Save file with word-tag combos
    set_tags("tag_dev.dat","q6_best","q6_output_combo1")

    # Combo 2: Modify one bigram rule ==================================================
    weights_2 = weights
    # bigram "VERB VERB" is often wrong; decrease weight
    weights_2["BIGRAM:VERB:VERB"] = -0.5
    # Run model with suffix, tag and bigram features on development data
    weighted_history("tag_dev.dat","q4_histories",weights_2,"q6_weighted",True,True)
    best_tag = open("q6_best", "w")
    weighted = open("q6_weighted", "r")
    call(["python", "tagger_decoder.py", "HISTORY"], stdout=best_tag, stdin=weighted)
    # 4. Save file with word-tag combos
    set_tags("tag_dev.dat","q6_best","q6_output_combo2")


    # Combo 3: Add content rules: =====================================================
    weights_3 = weights
    # If a word has a hyphen, tag as ADJ
    weights_3["CONTAINS:HYPHEN:ADJ"] = 5
    # If word has digits, tag as NUM
    weights_3["CONTAINS:DIGIT:NUM"] = 5
    weighted_history2("tag_dev.dat","q4_histories",weights_3,"q6_weighted",True,True)
    best_tag = open("q6_best", "w")
    weighted = open("q6_weighted", "r")
    call(["python", "tagger_decoder.py", "HISTORY"], stdout=best_tag, stdin=weighted)
    # 4. Save file with word-tag combos
    set_tags("tag_dev.dat","q6_best","q6_output_combo3")
    remove("q6_best")

    # Combo 4: All together now: =====================================================
    # suffix "ly" is usually ADV; increase weight
    weights["SUFFIX:ly:ADV"] = float(weights["SUFFIX:ly:ADV"]) + 3
    # suffix "ed" is usually VERB; increase weight
    weights["SUFFIX:ed:VERB"] = float(weights["SUFFIX:ed:VERB"]) + 3
    # No use to add to ["SUFFIX:ing:VERB"] feature
    # bigram "VERB VERB" is often wrong; decrease weight
    # weights["BIGRAM:VERB:VERB"] = -0.5
    # If a word has a hyphen, tag as ADJ
    weights["CONTAINS:HYPHEN:ADJ"] = 5
    # If word has digits, tag as NUM
    weights["CONTAINS:DIGIT:NUM"] = 5
    weighted_history2("tag_dev.dat","q4_histories",weights,"q6_weighted",True,True)
    best_tag = open("q6_best", "w")
    weighted = open("q6_weighted", "r")
    call(["python", "tagger_decoder.py", "HISTORY"], stdout=best_tag, stdin=weighted)
    # 4. Save file with word-tag combos
    set_tags("tag_dev.dat","q6_best","q6_output_combo4")

    remove("q6_best")
    remove("q6_weighted")
    remove("q4_histories")

if __name__ == '__main__':
    main()