''' "deflate" a node by moving the edges of the bounding
box in one pixel at a time, stopping each edge when there
is a nonzero image gradient somewhere along its length'''

# Find top edge
def find_top(dim, img_canny) :
    new_top = dim[0]
    while new_top < dim[1] :
        # if top row contains white pixel
        if 255 in img_canny[new_top, dim[2] :dim[3]] :
            return new_top
        else :
            new_top += 1
    return new_top

# Find bottom edge
def find_bottom(dim, img_canny) :
    new_bottom = dim[1] - 1
    while new_bottom > dim[0] :
        # if bottom row contains white pixel
        if 255 in img_canny[new_bottom, dim[2] : dim[3]] :
            return new_bottom
        else :
            new_bottom -= 1
    return new_bottom

# Find left edge
def find_left(dim, img_canny) :
    new_left = dim[2]
    while new_left < dim[3] :
        if 255 in img_canny[dim[0] :dim[1], 9] :
            return new_left
        else :
            new_left += 1
    return new_left

# Find right edge
def find_right(dim, img_canny) :
    new_right = dim[3] - 1
    while new_right > dim[2] :
        pixels = img_canny[dim[0] :dim[1], new_right]
        # if right column contains white pixel
        if 255 in pixels :
            return new_right
        else :
            new_right -= 1
    return new_right

# Deflate the node
def deflate(dim, img_canny) :
    dim = [int(x) for x in dim]
    return [find_top(dim, img_canny), find_bottom(dim, img_canny),
            find_left(dim, img_canny), find_right(dim, img_canny)]
