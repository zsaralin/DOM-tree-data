import os, pickle, ChildReader, DOMReader

# vertical = 43.8698194762268 %
# with WS = 3.5408163265306123 %
'''Determines percentage of child nodes arranged vertically'''

vert, not_vert = 0, 0  # initialize global variables

def increment_vert(dictP, dictBB) :
    for key in dictP.keys() :
        kids = ChildReader.get_children(key, dictP)  # get child nodes
        if len(kids) > 1 :
            if is_vert(kids, dictBB) :
                global vert
                vert += 1
            else :
                global not_vert
                not_vert += 1


# Returns percentage of child nodes arranged vertically
def perc_vert() :
    for file in os.listdir("new_data") :
        if file.endswith(".txt") :
            dictP, dictBB = DOMReader.read_DOM(file)
            increment_vert(dictP, dictBB)
    return (vert / (not_vert + vert)) * 100


# Including white space nodes
def perc_vert_WS() :
    for file in os.listdir("white_space") :
        if file.endswith("BB.pickle") :
            with open("white_space\%s" % file, 'rb') as handle :
                dictBB = pickle.load(handle)
            with open("white_space\%s_P.pickle" % file[:-10], 'rb') as handle :
                dictP = pickle.load(handle)
            increment_vert(dictP, dictBB)
    return (vert / (not_vert + vert)) * 100


# Determines if child nodes are arranged horizontally
def is_vert(children, dictBB) :
    for child in children :
        # create a copy of the child nodes, without the node under consideration
        children_copy = children.copy()
        children_copy.remove(child)
        if not_beside(child, children_copy, dictBB) and vert_pairs(child, children_copy, dictBB) :
            return True
        else :
            return False


# no child node's left edge is to the right of any child node's right edge, and vice-versa
def not_beside(cKey, children, dictBB) :
    left_node = dictBB[cKey][2]
    right_node = dictBB[cKey][3]
    for other_child in children :
        left_other = dictBB[other_child][2]
        right_other = dictBB[other_child][3]
        if left_node > right_other or right_node < left_other :
            return False
    return True


# For every pair of child nodes i and j (i != j), either the top edge of i is below the bottom edge of j, or vice-versa
def vert_pairs(cKey, children, dictBB) :
    t_node = dictBB[cKey][0]
    b_node = dictBB[cKey][1]
    for other_child in children :
        t_other = dictBB[other_child][0]
        b_other = dictBB[other_child][1]
        if t_node >= b_other or b_node <= t_other : continue
        return False
    return True

# print(perc_vert_WS())
