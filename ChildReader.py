'''Returns information about a given node's children'''

# return ID of single child
def get_child(search_key, dictP) :
    for key, val in dictP.items() :
        if search_key == val : return key

# Return list containing ID of child nodes
def get_children(search_key, dictP) :
    child_keys = []
    for key, val in dictP.items() :
        if search_key == val :
            child_keys.append(key)
    return child_keys