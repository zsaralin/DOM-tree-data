import os, pickle, re, matplotlib.pyplot as plt, numpy as np, DOMReader

'''Determines distribution of header size'''

# Saves list of header sizes to a pickle file
def dist_header_size():
    header_list = []
    for file in os.listdir("new_data") :
        if file.endswith(".txt") :
            with open("new_data\%s" % file, encoding = "utf-8-sig") as web_data :
                header_size = get_header_size(DOMReader.get_lines(web_data.readlines()))
                if header_size is not None : header_list.append(header_size) # Add header size to list
    pickle.dump(np.array(header_list), open("pickle_files/headerSize.p", "wb"))

# Get header size for a single webpage
def get_header_size(web_data):
    for i in web_data :  # for each node
        if i[2] == 'HEADER' :
            single_line = [0] * 4
            single_line[0] = float(''.join(re.findall("[+-]?\d+\.?\d*", i[4])))
            single_line[1] = float(''.join(re.findall("[+-]?\d+\.?\d*", i[5])))
            single_line[2] = float(''.join(re.findall("[+-]?\d+\.?\d*", i[6])))
            single_line[3] = float(''.join(re.findall("[+-]?\d+\.?\d*", i[7])))
            return abs(single_line[0] - single_line[1]) * abs(single_line[2] - single_line[3])

# Plot histogram with distribution of header size
def plot_histo() :
    plt.title('Distribution of Header Sizes')
    plt.ylabel('Number of Nodes')
    plt.xlabel('Header Size')
    with open("pickle_files/headerSize.p", "rb") as data : the_data = pickle.load(data)
    plt.hist(the_data)
    plt.show()

# dist_header_size()
# plot_histo()