import os, DOMReader, pickle

# without WS :  99.45824991167117 %
# with WS : 88.35105738491794 %

''' Calculates average percentage of nodes fully
contained by an ancestor for all webpages'''

num_contain, num_total = 0, 0

# Returns percentage of nodes fully contained by an ancestor
def get_contain() :
    for file in os.listdir("new_data") :
        if file.endswith(".txt") :
            dictP, dictBB = DOMReader.read_DOM(file)
            page_contain(dictP, dictBB)
    return num_contain / num_total * 100

# Including white space nodes
def get_contain_WS():
    for file in os.listdir("white_space") :
        if file.endswith("BB.pickle") :
            with open("white_space\%s" %file, 'rb') as handle :
                dictBB = pickle.load(handle)
            with open("white_space\%s_P.pickle" %file[:-10], 'rb') as handle :
                dictP = pickle.load(handle)
            page_contain(dictP, dictBB)
    num_contain / num_total * 100

# Increments number of nodes fully contained by an ancestor for all webpages
def page_contain(dictP, dictBB) :
    for key in dictP :
        key_contain(key, dictP, dictBB)

# Increments number of nodes fully contained by an ancestor for a single webpage
def key_contain(key, dictP, dictBB) :
    childNode = dictBB[key]  # Child Node
    keyP = dictP[key]  # Parent Node
    if keyP in dictBB.keys() :
        global num_total
        num_total += 1
    while keyP in dictBB.keys() :
        parentNode = dictBB[keyP]  # bounding box of Parent Node
        if childNode[0] >= parentNode[0] and childNode[1] <= parentNode[1] \
                and childNode[2] >= parentNode[2] and childNode[3] <= parentNode[3] :
            global num_contain
            num_contain += 1
            return
        else :
            keyP = dictP[keyP]  # retrieve next ancestor

# print('Percentage of Nodes fully contained by Ancestor =', get_contain(), '%')
