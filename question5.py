from __future__ import print_function
__author__="Juliana Louback <jl4354@.columbia.edu>"

from utils import init_suffix_weights
from subprocess import call
from utils import weighted_history
from utils import update_suffix_weights
from utils import set_tags
from utils import tagmodel_weights
from os import remove

"""
Usage:
python question5.py

Question 5: Create suffix-based features, set weight vector to 0 then train model with
5 iterations of the perceptron algorithm. Save model to suffix_tagger.model

Combine suffix features with tag and bigram features from question4.py.
Run new model on development data.

Must be in the same directory as tag_dev.dat, tag.model, tagger_decoder.py
and tagger_history_generator.py.

"""

def perceptron(weights, data_name, histories_name, gold_name, k):
    for i in range(0,k):
        # 1. Use model [weights] to assign a weight to each history.
        weighted_history(data_name,histories_name,weights,"q5_weighted",False,True)
        # 2. Find the histories of the highest-scoring tagging using tagger_decoder.py.
        tags = open("q5_best", "w")
        weighted = open("q5_weighted", "r")
        call(["python", "tagger_decoder.py", "HISTORY"], stdout=tags, stdin=weighted)
        # 3. Compare highest-scoring tagging with gold standard, update weights;
        # Update rule; increase accurate features +1, inaccurate -1.
        data = open(data_name,"r")
        gold = open(gold_name,"r")
        tags = open("q5_best","r")
        for word in data.readlines():
            if word != '\n':
                word = word.strip().split()[0]
                tag = tags.readline().strip().split()[2]
                gold_tag = gold.readline().strip().split()[2]
                increase = (tag == gold_tag)
                update_suffix_weights(word, tag, weights, increase)
            else:
                tag = tags.readline()
                tag = tags.readline()
                gold_tag = gold.readline()
        data.close()
        gold.close()
        tags.close()

def main():
    # Step 1: Read in training data, initialize dictionary of features with weight 0.
    weights = init_suffix_weights("tag_train.dat")
    # Step 2: Get the gold tag histories using tagger history generator.py
    gold = open("q5_gold", "w")
    train_data = open("tag_train.dat", "r")
    call(["python", "tagger_history_generator.py", "GOLD"], stdout=gold, stdin=train_data)
    # Step 3: Enumerate all possible histories
    train_data = open("tag_train.dat", "r")
    histories = open("q5_histories", "w")
    call(["python", "tagger_history_generator.py", "ENUM"], stdout=histories, stdin=train_data)
    # Step 4: Run Perceptron k=4 times.
    perceptron(weights, "tag_train.dat", "q5_histories", "q5_gold", 5)
    # Step 5: Write the final model out to suffix_tagger.model.
    final_model = file("suffix_tagger.model", "w")
    for key in weights:
        line = key + " " + str(weights[key])
        print(line, file=final_model)

    # Run model with suffix, tag and bigram features on development data
    tag_weights = tagmodel_weights()
    weights.update(tag_weights)
    weighted_history("tag_dev.dat","q4_histories",weights,"q5_weighted",True,True)
    best_tag = open("q5_best", "w")
    weighted = open("q5_weighted", "r")
    call(["python", "tagger_decoder.py", "HISTORY"], stdout=best_tag, stdin=weighted)
    # 4. Save file with word-tag combos
    set_tags("tag_dev.dat","q5_best","q5_output")
    remove("q5_best")
    remove("q5_histories")
    remove("q5_weighted")
    remove("q5_gold")


if __name__ == '__main__':
    main()