def get_squares(word):
    squares = []
    for cursor in range(len(word)):
        end = min(cursor, len(word) - cursor)
        for start in range(end):
            first = word[cursor - start - 1 : cursor]
            second = word[cursor : cursor + start + 1]
            if first == second and first not in squares:
                squares.append(first)
    return sorted(squares, key=len)

def is_square_free(word):
    for cursor in range(0, len(word)):
        end = min(cursor, len(word) - cursor)
        for start in range(0, end):
            first = word[cursor - start - 1 : cursor]
            second = word[cursor : cursor + start + 1]
            if first == second:
                return False
    return True

def is_language_square_free(language):
    for w in language:
        if not is_square_free(w):
            return False
    return True

def has_square_suffix(w):
    for length in range(1, len(w) // 2 + 1):
        if w[-2 * length : -length] == w[-length:]:
            return True
    return False

def generate_square_free_words(n, k, prefix=""):
    words = [prefix]
    new_words = []
    
    for _ in range(n):
        for i in range(len(words)):
            for a in range(k):
                candidate = words[i] + str(a)
                if not has_square_suffix(candidate):
                    new_words.append(candidate)
        words = new_words
        new_words = []
    return words

def is_extremal_square_free(word, alphabet=None):
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

def is_nearly_extremal_square_free(word, alphabet=None):
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