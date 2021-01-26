import pickle, os, numpy as np, matplotlib.pyplot as plt, DOMReader

'''Displays distribution of area graph'''

area_set = [] # initialize set containing area of each node

# Add area of each node in DOM treeto aspect_list
def add_area(dictBB):
    for key in dictBB :
        area_set.append(abs(dictBB[key][0] - dictBB[key][1]) * abs(dictBB[key][2] - dictBB[key][3]))

# Generate list of areas for all webpages
# Save list to pickle file
def get_area_list():
    for file in os.listdir("new_data") :
        if file.endswith(".txt") :
            add_area(DOMReader.read_DOM(file)[1])
    pickle.dump(area_set, open("pickle_files/areas.p", "wb"))

# Include white space nodes
def get_area_list_WS():
    for file in os.listdir("white_space") :
        if file.endswith("BB.pickle") :
            with open("white_space\%s" %file, 'rb') as handle :
                add_area(pickle.load(handle))
    pickle.dump(area_set, open("pickle_files/areas_WS.p", "wb"))

# Display histogram for distribution of area
def display_histo() :
    with open("pickle_files/areas.p", "rb") as input_file:
        data =  list(pickle.load(input_file))
    plt.title('Distribution of Sizes')
    plt.xlabel('Area')
    plt.ylabel('Number of Nodes')
    plt.hist(np.log(data) , 50)
    plt.show()

# get_area_list()
# display_histo()
