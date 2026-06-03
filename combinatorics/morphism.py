def dict_to_morphism(dictionary):
    return lambda w: "".join([dictionary[a] for a in w])

def is_uniform(morphism, alphabet):
    length = -1
    
    for a in alphabet:
        new_length = len(morphism(a))
        
        if length == -1:
            length = new_length
            continue
        
        if length != new_length:
            return False

    return True

THUE_MORPHISM = dict_to_morphism({ "0": "01", "1": "10" })

def is_synchronizing(morphism, from_alphabet):
    for a in from_alphabet:
        for b in from_alphabet:
            for c in from_alphabet:
                word = morphism(a+b)
                find_index = word.find(morphism(c))
                if find_index != -1: ## if f(ab) = uf(c)v for some u,v
                    u = word[:find_index]
                    v = word[find_index+len(morphism(c)):]
                    if (len(u) == 0 and a == c) or (len(v) == 0 and b == c):
                        pass # Good
                    else:
                        return False
    return True

def get_morphism_images_from_file(file, image_count):
    morphisms = []
    current = []
    count = 0
    to_read = open(file, "r").readlines()
    for line in to_read:
        if line[0] != '-':
            current.append(line.strip())
            count += 1
            if count == image_count:
                count = 0
                morphisms.append(list(current))
                current = []
    return morphisms