import os, DOMReader, pickle, numpy as np, matplotlib.pyplot as plt
'''Displays distribution of area graph for white space nodes'''

# Generates a list containing the area of each white space node
def list_size_WS(): # Histogram showing size of White Space Nodes
    size_WS = []
    for file in os.listdir("new_data") :
        if file.endswith(".txt") :
            print(file)
            dictBB = DOMReader.read_DOM(file)[1]
            maxID = max(dictBB.keys())
            with open("white_space\%s_BB.pickle" % file[:-4], 'rb') as handle :
                    dictBB = pickle.load(handle)
                    for i in range(maxID+1,max(dictBB.keys())+1):
                        size_WS.append(abs(dictBB[i][0] - dictBB[i][1]) * abs(dictBB[i][2] - dictBB[i][3]))
    pickle.dump(np.array(size_WS), open("pickle_files\\ws_dim.p", "wb"))

# Display histogram showing distribution for area of white space nodes
def plot_histo():
    plt.title('Distribution for Area of White Space Nodes')
    plt.xlabel('Log(Area)')
    plt.ylabel('Number of White Space Nodes')
    with open("pickle_files\ws_dim.p", "rb") as input_file :
        data = pickle.load(input_file)
    plt.hist(np.log(data), 50)
    plt.show()

# list_size_WS()
# plot_histo()