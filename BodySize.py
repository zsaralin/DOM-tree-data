import os, re, pickle, numpy as np, matplotlib.pyplot as plt, DOMReader
'''Determines distribution of body size'''

# Saves distribution of body size to pickle file
def get_dist_body() :
    body_list = [] # initialize list containing body sizes
    for file in os.listdir("new_data") :
        if file.endswith(".txt") :
            with open("new_data\%s" % file, encoding = "utf-8-sig") as web_data :
                body_size = get_body(DOMReader.get_lines(web_data.readlines()))
                body_list.append(body_size)
    pickle.dump(np.array(body_list), open("pickle_files/bodySizes.p", "wb"))

# Returns body of single webpage
def get_body(web_data) :
    for i in web_data :  # for each node
        if i[2] == 'BODY' :
            single_line = [0] * 4
            single_line[0] = float(''.join(re.findall("[+-]?\d+\.?\d*", i[4])))
            single_line[1] = float(''.join(re.findall("[+-]?\d+\.?\d*", i[5])))
            single_line[2] = float(''.join(re.findall("[+-]?\d+\.?\d*", i[6])))
            single_line[3] = float(''.join(re.findall("[+-]?\d+\.?\d*", i[7])))
            return abs(single_line[0] - single_line[1]) * abs(single_line[2] - single_line[3])

# Plot histogram with distribution of body size
def plot_histo() :
    plt.title('Distribution of Body Sizes')
    plt.ylabel('Number of Webpages')
    plt.xlabel('Size of Webpage Body')
    with open("pickle_files/bodySizes.p", "rb") as data : body_data = pickle.load(data)
    plt.hist(body_data)
    plt.show()

# get_dist_body()
# plot_histo()