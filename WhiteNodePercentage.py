import os, pickle, matplotlib.pyplot as plt, numpy as np, DOMReader, statistics

# 47.4360072113212 % (White Space Nodes/Total Nodes)

# Generates a list for percentage of white space nodes per DOM tree
# Save list to pickle file
def list_perc_WS():
    perc_WS = [] # list containing percentage of white space nodes per webpage
    for file in os.listdir("white_space") :
        if file.endswith("BB.pickle") :
            with open("white_space\%s" % file, 'rb') as handle :
                with_WS = len(pickle.load(handle)) # number of nodes including white space
                without_WS = len(DOMReader.read_DOM(file[:-10]+".txt")[1]) # number of nodes in original DOM
                perc_WS.append(((with_WS-without_WS)/with_WS)*100)
    # statistics.mean(perc_WS) # Average percentage of white space nodes
    pickle.dump(np.array(perc_WS), open("pickle_files\ws_list.p", "wb"))

# Display histogram for percentage of white space nodes
def plot_histo():
    plt.title('Distribution for Percentage of White Space Nodes')
    plt.xlabel('Percentage of White Space Nodes')
    plt.ylabel('Number of Webpages')
    with open("pickle_files\ws_list.p", "rb") as input_file : data = pickle.load(input_file)
    plt.gca().set_xlim([0, 100])
    plt.hist(data)
    plt.show()

