import HeaderSize, BodySize, DOMReader, os, numpy as np, pickle, matplotlib.pyplot as plt

'''Distribution of header size/body size ratio for all webpages'''

# Saves distribution of header size/body size ratio
def dist_head_ratio() :
    ratio_list = [] # initialize list containing header/body ratio
    for file in os.listdir("new_data") :
        if file.endswith(".txt") :
            with open("new_data\%s" % file, encoding = "utf-8-sig") as web_data :
                web_lines = DOMReader.get_lines(web_data.readlines())
                header_size = HeaderSize.get_header_size(web_lines)
                body_size = BodySize.get_body(web_lines)
                if header_size is not None and body_size is not None:
                    ratio_list.append(header_size / body_size)
    pickle.dump(np.array(ratio_list), open("pickle_files/headerRatio.p", "wb"))

# Plot histogram with distribution of header/body ratio
def plot_histo() :
    plt.title('Distribution of Header/Body Area Ratio')
    plt.ylabel('Number of Nodes')
    plt.xlabel('Size of Header/Size of Body')
    with open("pickle_files/headerRatio.p", "rb") as data : header_dist = pickle.load(data)
    plt.hist(header_dist)
    plt.show()

# dist_head_ratio()
# plot_histo()