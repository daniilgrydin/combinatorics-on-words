def word_in_alphabet(word, alphabet):
    for char in word:
        if char not in alphabet:
            return False
    return True