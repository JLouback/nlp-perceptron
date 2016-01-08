from __future__ import print_function
__author__="Juliana Louback <jl4354@.columbia.edu>"

from os import remove
from subprocess import call
from utils import weighted_history
from utils import set_tags
from utils import tagmodel_weights

"""
Usage:
python question4.py

Question 4: Decode training data with model given in the file tag.model
Reads in tag_dev.dat as development data. Outputs q4_histories containing
all possible histories for the data (used in question5.py); q4_output with the POS
tagging results.

Must be in the same directory as tag_dev.dat, tag.model, tagger_decoder.py
and tagger_history_generator.py.

"""

def decode():
    # read tag.model into a map from feature strings to weights.
    weights = tagmodel_weights()
    # For each sentence in development data (Steps 1-4):
    # 1. Enumerate all possible histories
    histories = open("q4_histories", "w")
    data = open("tag_dev.dat", "r")
    call(["python", "tagger_history_generator.py", "ENUM"], stdout=histories, stdin=data)
    # 2. Compute the features for each history and use tag.model to assign a weight to each history
    weighted_history("tag_dev.dat","q4_histories",weights,"q4_weighted",True,False)
    # 3. Call tagger_decoder.py HISTORY and pipe in the weighted histories to compute the highest scoring tagging.
    best_tag = open("q4_best", "w")
    weighted = open("q4_weighted", "r")
    call(["python", "tagger_decoder.py", "HISTORY"], stdout=best_tag, stdin=weighted)
    # 4. Save file with word-tag combos
    set_tags("tag_dev.dat","q4_best","q4_output")
    remove("q4_best")
    remove("q4_weighted")

if __name__ == '__main__':
    decode()
