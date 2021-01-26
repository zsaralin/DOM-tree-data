import pickle, os, matplotlib.pyplot as plt, numpy as np, DOMReader

'''Determine distribution of child nodes'''
child_list = []  # initialize list containing number of children per node

# Add number of children for each node in DOM tree to child_list
def add_num_children(dictP):
    for key in dictP :
        num_child = list(dictP.values()).count(key)
        child_list.append(num_child)

# Save distribution for number of child nodes to a pickle file
def get_num_children():
    for file in os.listdir("new_data") :
        if file.endswith(".txt") :
            add_num_children(DOMReader.read_DOM(file)[0])
    pickle.dump(np.array(child_list), open("pickle_files/children_list.p", "wb"))

# Including white space nodes
def get_num_children_WS():
    for file in os.listdir("white_space") :
        if file.endswith("P.pickle") :
            with open("white_space\%s" %file, 'rb') as handle :
                add_num_children(pickle.load(handle))
    pickle.dump(np.array(child_list), open("pickle_files/children_list_WS.p", "wb"))

# Returns probability for specific number of children
def getP(num_child):
    with open("pickle_files/children_list.p", "rb") as input_file : data = pickle.load(input_file)
    return np.count_nonzero(data == num_child)/len(data)

# Plots histogram displaying distribution of child nodes
def plot_histo():
    plt.title('Distribution for Number of Child Nodes')
    plt.xlabel('Number of Child Nodes')
    plt.ylabel('Number of Nodes')
    plt.gca().set_xlim([0, 15])
    with open("pickle_files/children_list_WS.p", "rb") as input_file : data = pickle.load(input_file)
    plt.hist(data, np.arange(0, 50, .5))
    plt.show()

# get_num_children_WS()
# print(distDom.getP(1))
# plot_histo()
# distDom.plotLog()

