SHORTEST_EXTREMAL_TERNARY_WORD = "abcabacbcabcbabcabacbcabc"
NEARLY_EXTREMAL_TERNARY_WORD = "abacbabcabacbcacbabcabacabcbabcabacbcabcb"

def is_extremal(word, alphabet=None):
    from libraries.square import is_square_free
    
    if alphabet is None:
        alphabet = set(word)
    if not is_square_free(word):
        return False
    for cursor in range(len(word) + 1):
        prefix = word[:cursor]
        suffix = word[cursor:]
        for letter in alphabet:
            if is_square_free(prefix + letter + suffix):
                return False
    return True

def is_nearly_extremal(word, alphabet=None):
    from libraries.square import is_square_free
    
    if not is_square_free(word):
        return False
    if alphabet is None:
        alphabet = set(word)
    for cursor in range(1,len(word)):
        prefix = word[:cursor]
        suffix = word[cursor:]
        for letter in alphabet:
            if is_square_free(prefix + letter + suffix):
                return False
    return True

def is_nearly_extremal_details(word, alphabet=None):
    from libraries.square import is_square_free
    
    if not is_square_free(word):
        return False
    if alphabet is None:
        alphabet = set(word)
    for cursor in range(1,len(word)):
        prefix = word[:cursor]
        suffix = word[cursor:]
        for letter in alphabet:
            if is_square_free(prefix + letter + suffix):
                return False
    #* Lucas said that there should be exactly one left extension,
    #* and excatly one right extension.
    right_extensions = 0
    left_extensions = 0
    for letter in alphabet:
        if is_square_free(word + letter):
            right_extensions += 1
        if is_square_free(letter + word):
            left_extensions += 1
    if right_extensions != left_extensions or right_extensions != 1: return False
    return True