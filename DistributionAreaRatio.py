import matplotlib.pyplot as plt, os, numpy as np, pickle, ChildReader, DOMReader

'''Displays distribution of Area Ratio graph'''

ratio_list = []  # initialize list of area ratios

# Return area ratio for a single child (area of parent/area of child)
def get_area_ratio(dictBB, key, child_key) :
    parent_area = abs(dictBB[key][0] - dictBB[key][1]) * abs(dictBB[key][2] - dictBB[key][3])
    child_area = abs(dictBB[child_key][0] - dictBB[child_key][1]) * abs(dictBB[child_key][2] - dictBB[child_key][3])
    return parent_area/child_area

# Add aspect ratio for all nodes in DOM tree to ratio_list
def add_area_ratio(dictP, dictBB):
    for key in dictP :
        children = ChildReader.get_children(key, dictP)
        for c in children :
            ratio_list.append(get_area_ratio(dictBB, key, c))

# Calculate area ratio for each node, save list to a pickle file
def get_ratio_list() :
    for file in os.listdir("new_data") :
        if file.endswith(".txt") :
            dictP, dictBB = DOMReader.read_DOM(file)
            add_area_ratio(dictP, dictBB)
    pickle.dump(ratio_list, open("pickle_files\\areaRatio.p", "wb"))

# Including white space nodes
def get_ratio_list_WS():
    for file in os.listdir("white_space") :
        if file.endswith("BB.pickle") :
            with open("white_space\%s" %file, 'rb') as handle :
                dictBB = pickle.load(handle)
            with open("white_space\%s_P.pickle" %file[:-10], 'rb') as handle :
                dictP = pickle.load(handle)
            add_area_ratio(dictP, dictBB)
    pickle.dump(ratio_list, open("pickle_files\\areaRatio_WS.p", "wb"))

# Display Area Ratio Histogram
def plot_histo() :
    with open("pickle_files\\areaRatio_WS.p", "rb") as input_file :
        data = list(pickle.load(input_file))
    plt.title('Distribution Area Ratio (with WS)')
    plt.xlabel('Area Ratio')
    plt.ylabel('Number of Nodes')
    plt.hist(data , np.arange(0, 20, 0.1))
    plt.show()

get_ratio_list_WS()
plot_histo()

