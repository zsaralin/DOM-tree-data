import re

'''Reads DOM text file'''

# Return every line as a string list
def get_lines(list_str) :
    content = [x.strip() for x in list_str]  # remove white space
    each_line = [''] * len(content)  # initialize each_line array
    for q in range(len(content)) :  # for every line
        each_line[q] = content[q].split(',')
    return each_line


# Return float list with bounding box positions of a single node
def get_bb(single_line) :
    for i in range(len(single_line)) :
        if 'bbox_top' in single_line[i] :
            bbox_top = ''.join(re.findall("[+-]?\d+\.?\d*", single_line[i]))
            bbox_bottom = ''.join(re.findall("[+-]?\d+\.?\d*", single_line[i + 1]))
            bbox_left = ''.join(re.findall("[+-]?\d+\.?\d*", single_line[i + 2]))
            bbox_right = ''.join(re.findall("[+-]?\d+\.?\d*", single_line[i + 3]))
            return [float(bbox_top), float(bbox_bottom), float(bbox_left), float(bbox_right)]


# Return dictionary with parent for every node ID
def every_parent(lines) :
    parent_data = {}
    for line in lines :  # for each node
        parent_data[int(line[0])] = int(line[1])
    return parent_data


# Return dictionary with bb positions for every node ID
def every_bb(lines) :
    bb_data = {}
    for line in lines :
        bb_data[int(line[0])] = get_bb(line)
    return bb_data

# Refine each dictionary, deleting empty/negligible nodes and fixing negative borders
def refine_dict(dictBB, dictP) :
    body_dim = dictBB[1]  # bounding box of body
    for key in list(dictBB) :
        # if bounding box is None, or right/bottom edge < 1
        if dictBB[key] is None or dictBB[key][1] < 1 or dictBB[key][3] < 1 :
            del dictBB[key], dictP[key]
            continue
        # if edge of bounding box is outside of body
        if dictBB[key][0] < 0 : dictBB[key][0] = 0
        if dictBB[key][2] < 0 : dictBB[key][2] = 0
        if dictBB[key][1] > body_dim[1] : dictBB[key][1] = body_dim[1]
        if dictBB[key][3] > body_dim[2] : dictBB[key][3] = body_dim[3]
        # if height or width of bounding box is <= 1
        if abs(dictBB[key][0] - dictBB[key][1]) <= 1 or abs(dictBB[key][2] - dictBB[key][3]) <= 1 :
            del dictBB[key], dictP[key]
            continue

# Return Parent and Bounding Box dictionaries given text file
def read_DOM(file) :
    with open("new_data\%s" % file, encoding = "utf-8-sig") as data :
        web_lines = data.readlines()
    list_data = get_lines(web_lines)
    dictP, dictBB = (every_parent(list_data)), (every_bb(list_data))
    refine_dict(dictBB, dictP)
    return [dictP, dictBB]
