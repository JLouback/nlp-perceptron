from __future__ import print_function
__author__="Juliana Louback <jl4354@.columbia.edu>"

from collections import defaultdict
from subprocess import call
from itertools import izip

"""

utils functions used in question4.py

"""

# Returns weighted history according to [weights] dictionary for each history in [histories].
# Saves weighted history to [output]
# If [original] == True, looks for tag and bigram features
# If [suffix_feature] == True, looks for suffix features
# Used in both question4.py and question5.py
def weighted_history(data, histories, weights, output, original, suffix_feature):
    histories = open(histories, "r")
    data = open(data, "r")
    weighted = open(output, "w")
    count = 1
    history = histories.readline().strip()
    for word in data.readlines():
        if word == '\n':
            print("", file=weighted)
            count = 0
        else:
            if history == "":
                history = histories.readline().strip()
            word = word.strip().split()[0]
            while history is not '' and int(history.split()[0]) is count:
                weight = 0
                pos = history.split()[2]
                if original:
                    tag_key = "TAG:" + word + ":" + pos
                    bigram_key = "BIGRAM:" + history.split()[1] + ":" + pos
                    try:
                        weight += float(weights[tag_key])
                    except KeyError:
                        pass
                    try:
                        weight += float(weights[bigram_key])
                    except KeyError:
                        pass
                if suffix_feature:
                    suffix = word[-1:]
                    key = "SUFFIX:" + suffix + ":" + pos
                    try:
                        weight += float(weights[key])
                    except KeyError:
                        pass
                    try:
                        suffix = word[-2:]
                        key = "SUFFIX:" + suffix + ":" + pos
                        weight += float(weights[key])
                    except:
                        pass
                    try:
                        suffix = word[-3:]
                        key = "SUFFIX:" + suffix + ":" + pos
                        weight += float(weights[key])
                    except:
                        pass
                history_weight = history + " " + str(weight)
                print(history_weight,file=weighted)
                history = histories.readline().strip()
        count += 1

# Returns weighted history as in weighted history, but also includes new features
# from Combo 3 in question 6
def weighted_history2(data, histories, weights, output, original, suffix_feature):
    histories = open(histories, "r")
    data = open(data, "r")
    weighted = open(output, "w")
    count = 1
    history = histories.readline().strip()
    for word in data.readlines():
        if word == '\n':
            print("", file=weighted)
            count = 0
        else:
            if history == "":
                history = histories.readline().strip()
            word = word.strip().split()[0]
            while history is not '' and int(history.split()[0]) is count:
                weight = 0
                pos = history.split()[2]
                if original:
                    tag_key = "TAG:" + word + ":" + pos
                    bigram_key = "BIGRAM:" + history.split()[1] + ":" + pos
                    try:
                        weight += float(weights[tag_key])
                    except KeyError:
                        pass
                    try:
                        weight += float(weights[bigram_key])
                    except KeyError:
                        pass
                if suffix_feature:
                    suffix = word[-1:]
                    key = "SUFFIX:" + suffix + ":" + pos
                    try:
                        weight += float(weights[key])
                    except KeyError:
                        pass
                    try:
                        suffix = word[-2:]
                        key = "SUFFIX:" + suffix + ":" + pos
                        weight += float(weights[key])
                    except:
                        pass
                    try:
                        suffix = word[-3:]
                        key = "SUFFIX:" + suffix + ":" + pos
                        weight += float(weights[key])
                    except:
                        pass
                if "-" in word and pos == "ADJ":
                    weight += float(weights["CONTAINS:HYPHEN:ADJ"])
                if any(i.isdigit() for i in word) and pos == "NUM":
                    weight += float(weights["CONTAINS:DIGIT:NUM"])
                history_weight = history + " " + str(weight)
                print(history_weight,file=weighted)
                history = histories.readline().strip()
        count += 1

# Writes to [output] with words in [data], tag in [tags]
# used in question4.py
def set_tags(data, tags, output):
    tags = open(tags, "r")
    data = open(data, "r")
    result = open(output, "w")
    for word in data.readlines():
        tag = tags.readline().strip()
        if word != '\n':
            word = word.strip()
            line = word + " " + tag.split()[2]
            print(line, file=result)
        else:
            print("",file=result)
            tag = tags.readline()

# read tag.model into a map from feature strings to weights. used in question4.py
def tagmodel_weights():
    weights = defaultdict()
    tag_model = open("tag.model", "r").readlines()
    for line in tag_model:
        key = line.strip().split(" ")[0]
        value = line.strip().split(" ")[1]
        weights[key] = value
    return weights

def suffix_weights(model_file):
    weights = defaultdict()
    model = open(model_file, "r").readlines()
    for line in model:
        key = line.strip().split(" ")[0]
        value = line.strip().split(" ")[1]
        weights[key] = value
    return weights


# Read in training data, initialize dictionary of features with weight 0.
# Used in question5.py
def init_suffix_weights(data):
    train = open(data, "r")
    line = train.readline()
    weights = defaultdict()
    while line:
        if line != '\n':
            line = line.strip()
            word = line.split()[0]
            tag = line.split()[1]
            suffix = word[-1:]
            key = "SUFFIX:" + suffix + ":" + tag
            weights[key] = 0
            try:
                suffix = word[-2:]
                key = "SUFFIX:" + suffix + ":" + tag
                weights[key] = 0
            except IndexError:
                pass
            try:
                suffix = word[-3:]
                key = "SUFFIX:" + suffix + ":" + tag
                weights[key] = 0
            except IndexError:
                pass
        line = train.readline()
    return weights

# Updates suffix weights, [increase] is bool function indicating whether to
# promote or demote weights; the keys of the features to be updated are
# derived from [word] and [tag]
def update_suffix_weights(word, tag, weights, increase):
    update = -0.0001
    if increase:
        update = 0.0001
    suffix = word[-1:]
    key = "SUFFIX:" + suffix + ":" + tag
    weight = 0
    try:
        weight = weights[key]
    except KeyError:
        pass
    weights[key] = weight + update
    try:
        suffix = word[-2:]
        key = "SUFFIX:" + suffix + ":" + tag
        weight = 0
        try:
            weight = weights[key]
        except KeyError:
            pass
        weights[key] = weight + update
    except IndexError:
        pass
    try:
        suffix = word[-3:]
        key = "SUFFIX:" + suffix + ":" + tag
        weight = 0
        try:
            weight = weights[key]
        except KeyError:
            pass
        weights[key] = weight + update
    except IndexError:
        pass

