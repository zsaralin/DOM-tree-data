import matplotlib.pyplot as plt, os, numpy as np, pickle, DOMReader

'''Determines distribution of aspect ratio (width/height)'''

aspect_list = [] #initialize list of aspect ratio

# Add log of aspect ratio for all nodes to aspect_list
def add_asp_ratio(dictBB):
    for key in dictBB :
        aspect_list.append(np.log(abs(dictBB[key][2] - dictBB[key][3]) / abs(dictBB[key][0] - dictBB[key][1])))

# Calculate log of aspect ratio for each node
# Save distribution of aspect ratio to a pickle file
def get_ratio_list():
    for file in os.listdir("new_data") :
        if file.endswith(".txt") :
            add_asp_ratio(DOMReader.read_DOM(file)[1])
    pickle.dump(aspect_list, open("pickle_files/aspectRatio.p", "wb"))

# Including white space nodes
def get_ratio_list_WS() :
    for file in os.listdir("white_space") :
        if file.endswith("BB.pickle") :
            with open("white_space\%s" %file, 'rb') as handle :
                add_asp_ratio(pickle.load(handle))
    pickle.dump(aspect_list, open("pickle_files/aspectRatio_WS.p", "wb"))

# Display log graph for aspect ratio
def plot_log() :
    plt.title('Distribution of Aspect Ratio (with WS)') # set labels
    plt.xlabel('Aspect Ratio')
    plt.ylabel('Number of Nodes')
    with open("pickle_files/aspectRatio_WS.p", "rb") as input_file : data = pickle.load(input_file)
    plt.hist(data, 50)
    plt.show()

# Find probability of given aspect ratio
def prob_aspect(asp_ratio) :
    with open("pickle_files/aspectRatio.p", "rb") as input_file : data = pickle.load(input_file)
    n, bins, _ = plt.hist(data, 50)
    for i in range(len(bins)-1) :
        curr = bins[i]
        next = bins[i + 1]
        if curr <= asp_ratio < next :
            return n[i]/sum(n)
    return 0

# get_ratio_list_WS()
# plot_log()
# print(prob_aspect(12.2))