import os, cv2, pickle, InflateDim, DeflateDim, DOMReader, ChildReader, HorizontalChildren, VerticalChildren

# Generate new parent and bounding box dict for DOM including white space
def generate_white_space() :
    for file in os.listdir("new_data") :
        if file.endswith(".jpg") :
            print(file)
            img = cv2.imread("new_data\%s" % file)
            save_dict("%s.txt" % file[:-4], img)

# Save new parent and bounding box dict to separate pickle files
def save_dict(file, img) :
    img_canny = cv2.Canny(img, 255, 255/5)
    dictP, dictBB = DOMReader.read_DOM(file)
    dictP_new, dictBB_new = dictP.copy(), dictBB.copy()
    for key in dictP.keys() :
        kids = ChildReader.get_children(key, dictP_new)
        # if num child nodes > 1 and child nodes are fully contained by parent
        if len(kids) > 1 and contain_children(key, kids, dictBB) :
            hor_or_vert(key, kids, dictBB_new, dictP_new, img_canny, img)
    with open("white_space\%s_BB.pickle" %file[:-4], 'wb') as handle :
        pickle.dump(dictBB_new, handle, protocol = pickle.HIGHEST_PROTOCOL)
    with open("white_space\%s_P.pickle" %file[:-4], 'wb') as handle :
        pickle.dump(dictP_new, handle, protocol = pickle.HIGHEST_PROTOCOL)

# Returns true if all child nodes are contained within parent node
def contain_children(parent, children, dictBB):
    [top,bottom,left,right] = dictBB[parent]
    for child in children:
        [c_top, c_bottom, c_left, c_right]= dictBB[child]
        if c_top < top or c_bottom >  bottom \
                or c_left < left or c_right > right :
            return False
    return True

# Generate white space nodes (based on whether child nodes are arranged horizontally or vertically)
def hor_or_vert(key, kids, dictBB, dictP, img_canny, img) :
    if VerticalChildren.is_vert(kids, dictBB) :
        arr = get_dim_arr(dictBB, key, kids)
        vert_segmentation(key, arr, img_canny, dictBB, dictP)
    elif HorizontalChildren.is_horiz(kids, dictBB) :
        arr = get_dim_arr(dictBB, key, kids)
        hor_segmentation(key, arr, img_canny, dictBB, dictP)

# Compile list containing bounding box of parent node (index 0) and child nodes
def get_dim_arr(dictBB, key, kids) :
    arr = [dictBB[key]]
    for k in kids :
        arr.append(dictBB[k])
    return arr

# Find white space nodes to new dictionaries (when child nodes are arranged vertically)
def vert_segmentation(key, arr, img_canny, dictBB, dictP) :
    outer_box = InflateDim.inflate(arr[0], img_canny)
    inner_box = DeflateDim.deflate(arr[0], img_canny)
    # white space nodes around child nodes, segmenting horizontally and then vertically
    add_node(dictBB, dictP, [outer_box[0], outer_box[1], outer_box[2], inner_box[2]], key)
    add_node(dictBB, dictP, [outer_box[0], outer_box[1], inner_box[3], outer_box[3]], key)
    add_node(dictBB, dictP, [outer_box[0], inner_box[0], inner_box[2], inner_box[3]], key)
    add_node(dictBB, dictP, [inner_box[1], outer_box[1], inner_box[2], inner_box[3]], key)
    # deflate each child node
    for child in arr[1 :] :
        def_child = DeflateDim.deflate(child, img_canny)
        # if theres white space above the deflated child node
        if def_child[0] > inner_box[0]:
            new_top = InflateDim.find_top([def_child[0], def_child[1], def_child[2], def_child[3]], img_canny) # find top of white space
            expand_top = InflateDim.inflate([new_top, def_child[0], def_child[2], def_child[3]], img_canny) # expand white space node
            if expand_top[2] < inner_box[2]: expand_top[2] = inner_box[2]
            if expand_top[3] > inner_box[3]: expand_top[3] = inner_box[3]
            if expand_top[0] < inner_box[0]: expand_top[0] = inner_box[0]
            add_node(dictBB, dictP, [expand_top[0], expand_top[1], expand_top[2], expand_top[3]], key)
        # if theres white space to the left of the deflated child node
        if def_child[2] > inner_box[2] :
            new_left = InflateDim.find_left([def_child[0], def_child[1], def_child[2], def_child[3]], img_canny)
            if new_left < inner_box[2] : new_left = inner_box[2]
            add_node(dictBB, dictP, [def_child[0], def_child[1], new_left, def_child[2]], key)
        # if theres white space to the right of the deflated child node
        if def_child[3] < inner_box[3] :
            new_right = InflateDim.find_right([def_child[0], def_child[1], def_child[2], def_child[3]], img_canny)
            if new_right > inner_box[3] : new_right = inner_box[3]
            add_node(dictBB, dictP, [def_child[0], def_child[1], def_child[3], new_right], key)  # right ws
        # if theres white space below bottom deflated child node
        if child == arr[len(arr)-1] and def_child[1] < inner_box[1]:
            new_bottom = InflateDim.find_bottom([def_child[0], def_child[1], def_child[2], def_child[3]], img_canny)  # find bottom of white space
            expand_bottom = InflateDim.inflate([def_child[1], new_bottom, def_child[2], def_child[3]], img_canny)  # expand white space node
            if expand_bottom[2] < inner_box[2] : expand_bottom[2] = inner_box[2]
            if expand_bottom[3] > inner_box[3] : expand_bottom[3] = inner_box[3]
            if expand_bottom[1] > inner_box[1] : expand_bottom[1] = inner_box[1]
            add_node(dictBB, dictP, [expand_bottom[0], expand_bottom[1], expand_bottom[2], expand_bottom[3]], key)

# Find white space nodes (when child nodes are arranged horizontally)
def hor_segmentation(key, arr, img_canny, dictBB, dictP) :
    outer_box = InflateDim.inflate(arr[0], img_canny)
    inner_box = DeflateDim.deflate(arr[0], img_canny)
    # add white space nodes around child nodes, segmenting vertically and then horizontally
    add_node(dictBB, dictP, [outer_box[0], inner_box[0], outer_box[2], outer_box[3]], key)
    add_node(dictBB, dictP, [inner_box[1], outer_box[1], outer_box[2], outer_box[3]], key)
    add_node(dictBB, dictP, [inner_box[0], inner_box[1], outer_box[2], inner_box[2]], key)
    add_node(dictBB, dictP, [inner_box[0], inner_box[1], inner_box[3], outer_box[3]], key)
    # deflate each child node
    for child in arr[1 :] :
        def_child = DeflateDim.deflate(child, img_canny)
        # if theres white space to the left of the deflated child node
        if def_child[2] > inner_box[2] :
            new_left = InflateDim.find_left([def_child[0], def_child[1], def_child[2], def_child[3]], img_canny)
            expand_left = InflateDim.inflate([def_child[0], def_child[1], new_left, def_child[2]], img_canny)
            if expand_left[0] < inner_box[0] : expand_left[0] = inner_box[0]
            if expand_left[1] > inner_box[1] : expand_left[1] = inner_box[1]
            if expand_left[2] < inner_box[2] : expand_left[2] = inner_box[2]
            add_node(dictBB, dictP, [expand_left[0], expand_left[1], expand_left[2], expand_left[3]], key)
        # if theres white space above the deflated child node
        if def_child[0] > inner_box[0] :
            new_top = InflateDim.find_top([def_child[0], def_child[1], def_child[2], def_child[3]], img_canny)
            if new_top < inner_box[0] : new_top = inner_box[0]
            add_node(dictBB, dictP, [new_top, def_child[0], def_child[2], def_child[3]], key)
        # if theres white space below the deflated child node
        if def_child[1] < inner_box[1] :
            new_bottom = InflateDim.find_bottom([def_child[0], def_child[1], def_child[2], def_child[3]], img_canny)
            if new_bottom > inner_box[1] : new_bottom = inner_box[1]
            add_node(dictBB, dictP, [def_child[0], new_bottom, def_child[2], def_child[3]], key)  # right ws
        # if theres white space to the right of rightmost deflated child node
        if child == arr[len(arr)-1] and def_child[3] < inner_box[3]:
            new_right = InflateDim.find_right([def_child[0], def_child[1], def_child[2], def_child[3]], img_canny)  # find right of white space
            expand_right = InflateDim.inflate([def_child[0], def_child[1], def_child[3], new_right], img_canny)  # expand white space node
            if expand_right[0] < inner_box[0] : expand_right[0] = inner_box[0]
            if expand_right[1] > inner_box[1] : expand_right[1] = inner_box[1]
            if expand_right[3] > inner_box[3] : expand_right[3] = inner_box[3]
            add_node(dictBB, dictP, [expand_right[0], expand_right[1], expand_right[2], expand_right[3]], key)

# Add white space node to parent and bounding box dictionary
def add_node(dictBB, dictP, dimBB, key) :
    # if height and width of white space node  are > 1
    if abs(dimBB[0] - dimBB[1]) > 1 and abs(dimBB[2] - dimBB[3]) > 1 :
        newID = max(dictP.keys()) + 1
        dictP[newID] = key
        dictBB[newID] = dimBB

generate_white_space()

