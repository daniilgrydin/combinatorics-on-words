from combinatorics.word import generate_greedy_words
from combinatorics.exponent import is_suffix_exponent_free, ExtendedReal, is_exponent_free
from combinatorics.extremal import is_extremal, is_nearly_extremal
from combinatorics.square import is_square_free
from combinatorics.word import color_word, encode_short, get_permutations

alphabet = "012"
alpha = ExtendedReal(2, 1, False)

for length in range(1, 15):
    unique = generate_greedy_words(
        alphabet,
        length,
        lambda word: is_suffix_exponent_free(word, alpha)
    )
    with open("ternary_words.txt", "a") as f:
        for word in unique:
            f.write(word + "\n")