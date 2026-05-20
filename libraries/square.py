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