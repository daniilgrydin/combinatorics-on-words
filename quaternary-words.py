from combinatorics.word import generate_greedy_words_unique
from combinatorics.exponent import is_suffix_exponent_free, ExtendedReal, is_exponent_free
from combinatorics.extremal import is_extremal, is_nearly_extremal
from combinatorics.square import is_square_free
from combinatorics.word import color_word, encode_short, get_permutations

alphabet = "0123"
alpha = ExtendedReal(7, 5, True)
beta = ExtendedReal(7, 4, True)

for length in range(1, 11):
    unique = generate_greedy_words_unique(
        alphabet,
        length,
        lambda word: is_suffix_exponent_free(word, alpha)
    )
    with open("quaternary_words.txt", "a") as f:
        for word in unique:
            perms = get_permutations(word, alphabet)
            print(perms)
            for perm in perms:
                f.write(perm + "\n")