''' "inflate" a region by moving each edge out one pixel at a time, stopping when a
nonzero image gradient is detected'''

# Find top edge
def find_top(dim, img_canny) :
    if dim[0] == 0: return dim[0]
    else: new_top = dim[0] - 1
    while img_canny.shape[0] > new_top > 0 :
        # if row contains white pixel
        if 255 in img_canny[new_top, dim[2]:dim[3]] :
            return new_top
        else :
            new_top -= 1
    return new_top

# Find bottom edge
def find_bottom(dim, img_canny) :
    if dim[1] == img_canny.shape[0] - 1: return dim[1]
    else: new_bottom = dim[1] + 1
    while new_bottom < img_canny.shape[0] :
        if 255 in img_canny[new_bottom, dim[2]:dim[3]] :  # if row contains white pixel
            return new_bottom
        else :
            new_bottom += 1
    return new_bottom

def find_left(dim, img_canny) :
    if dim[2] == 0: return dim[2]
    else: new_left = dim[2] - 1
    while img_canny.shape[1] > new_left > 0 :
        if 255 in img_canny[dim[0]:dim[1], new_left] :  # if column contains white pixel
            return new_left
        else :
            new_left -= 1
    return new_left

def find_right(dim, img_canny) :
    if dim[3] == img_canny.shape[1] - 1: return dim[3]
    else: new_right = dim[3] + 1
    while new_right < img_canny.shape[1] - 1 :
        if 255 in img_canny[dim[0]:dim[1], new_right] :  # if column contains white pixel
            return new_right
        else :
            new_right += 1
    return new_right

# Inflate the region
def inflate(dim, img_canny) :
    dim = [int(x) for x in dim]
    return [find_top(dim, img_canny), find_bottom(dim, img_canny), find_left(dim, img_canny), find_right(dim, img_canny)]
