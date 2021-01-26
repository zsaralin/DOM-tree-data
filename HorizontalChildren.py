import os, pickle, ChildReader, DOMReader

# horizontal = 51.07551487414188 %
# with WS = 25.831632653061227 %

'''Determines percentage of child nodes arranged horizontally'''

horiz, not_horiz = 0, 0  # initialize global variables


# For each node arranged horizontally, increment horiz (otherwise, increment not_horiz)
def increment_horiz(dictP, dictBB) :
    for key in dictP.keys() :
        children = ChildReader.get_children(key, dictP)  # get child nodes
        if len(children) > 1 :
            if is_horiz(children, dictBB) :
                global horiz
                horiz += 1
            else :
                global not_horiz
                not_horiz += 1


# Returns percentage of child nodes arranged horizontally
def perc_horiz() :
    for file in os.listdir("new_data") :
        if file.endswith(".txt") :
            dictP, dictBB = DOMReader.read_DOM(file)
            increment_horiz(dictP, dictBB)
    return (horiz / (not_horiz + horiz)) * 100


# Including White Space
def perc_horiz_WS() :
    for file in os.listdir("white_space") :
        if file.endswith("BB.pickle") :
            with open("white_space\%s" % file, 'rb') as handle :
                dictBB = pickle.load(handle)
            with open("white_space\%s_P.pickle" % file[:-10], 'rb') as handle :
                dictP = pickle.load(handle)
            increment_horiz(dictP, dictBB)
    return (horiz / (not_horiz + horiz)) * 100


# Determines if child nodes are arranged horizontally
def is_horiz(children, dictBB) :
    for child in children :
        # create a copy of the child nodes, without the node under consideration
        child_copy = children.copy()
        child_copy.remove(child)
        if not_below_above(child, child_copy, dictBB) and hor_pairs(child, child_copy, dictBB) :
            return True
        else :
            return False


# no child node's top edge is below of any child node's bottom edge, and vice-versa
def not_below_above(child, children, dictBB) :
    top_node = dictBB[child][0]
    bottom_node = dictBB[child][1]
    for other_child in children :
        top_other = dictBB[other_child][0]
        bottom_other = dictBB[other_child][1]
        if top_node > bottom_other or bottom_node < top_other : return False
    return True


# For every pair of child nodes i and j (i != j), either the left edge of i is to the right of the right edge of j, or vice-versa
def hor_pairs(child, children, dictBB) :
    l_node = dictBB[child][2]
    r_node = dictBB[child][3]
    for other_child in children :
        l_other = dictBB[other_child][2]
        r_other = dictBB[other_child][3]
        if l_node <= r_other or r_node >= l_other : continue
        return False
    return True

# print(perc_horiz_WS())
