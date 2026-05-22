def dict_to_morphism(dictionary):
    return lambda w: "".join([dictionary[a] for a in w])

def is_uniform(morphism, alphabet):
    length = -1
    
    for a in alphabet:
        new_length = morphism(a)
        
        if length == -1:
            length = new_length
            continue
        
        if length != new_length:
            return False

    return True

THUE_MORPHISM = dict_to_morphism({ "0": "01", "1": "10" })

def is_synchronizing(morphism):
    pass