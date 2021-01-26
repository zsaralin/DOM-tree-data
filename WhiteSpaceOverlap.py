import os, DOMReader, pickle, statistics
# 99.8819153483961 %

'''Determines percentage of white space nodes that overlap'''

overlap_WS = [] # one entry per webpage

# Return average percentage of white space nodes that overlap
def list_overlap_WS() :
    for file in os.listdir("new_data") :
        if file.endswith(".txt") :
            dictBB = DOMReader.read_DOM(file)[1]
            maxID = max(dictBB.keys())
            with open("white_space\%s_BB.pickle" % file[:-4], 'rb') as handle :
                dictBB = pickle.load(handle)
                dictBB_WS = {k : v for k, v in dictBB.items() if
                             k > maxID}  # bounding box dictionary for only white space nodes
                num_overlap = get_num_overlap(dictBB_WS)
                overlap_WS.append(num_overlap / len(dictBB_WS.keys()) * 100) # add percentage to overlap_WS list
    return statistics.mean(overlap_WS)

# Returns number of white space nodes that overlap in a single DOM tree
def get_num_overlap(dictBB_WS) :
    num_overlap = 0
    for key in dictBB_WS.keys() :
        copy_dict = dictBB_WS.copy()
        del copy_dict[key]
        if is_overlap(dictBB_WS[key], copy_dict) :
            num_overlap += 1
    return num_overlap


# Return true if a given node is overlapping another white space node in the DOM tree
def is_overlap(target_node, copy_dict) :
    for o_key in copy_dict :  # for nodes other than the target node
        if target_node[0] < copy_dict[o_key][1] and target_node[3] > copy_dict[o_key][2] or \
                copy_dict[o_key][0] < target_node[1] and copy_dict[o_key][3] > target_node[2] or \
                target_node[1] > copy_dict[o_key][0] and target_node[3] > copy_dict[o_key][2] or \
                copy_dict[o_key][1] < target_node[0] and copy_dict[o_key][3] > target_node[2] :
            return True
    return False

# list_overlap_WS()
