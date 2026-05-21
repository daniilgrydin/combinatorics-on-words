STANDARD_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ENCODING_ALPHABET = STANDARD_ALPHABET + "!@#$%^&*"

def word_in_alphabet(word, alphabet):
    for char in word:
        if char not in alphabet:
            return False
    return True

def extract_alphabet(word):
    alphabet = []
    for i in range(0, len(word)):
        if word[i] not in alphabet:
            alphabet.append(word[i])
    return alphabet