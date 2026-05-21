from combinatorics.word import generate_greedy_words_unique
from combinatorics.exponent import is_suffix_exponent_free, ExtendedReal, is_exponent_free
from combinatorics.extremal import is_extremal, is_nearly_extremal
from combinatorics.square import is_square_free
from combinatorics.word import color_word, encode_short

def max_length(q, a:float, b:float):
    return max(
        2 * b / (b - a),
        2 * (q - 1) * (2 * b - 1) / (q * (b - 1))
    )


alphabet = "012"
# length = 4
alpha = ExtendedReal(7, 5, True) # quaternary
beta = ExtendedReal(7, 4, True) # ternary

unique = generate_greedy_words_unique(
    alphabet,
    1, # checked up to 58 and found nothing, so continuing the search (58, ...]
    lambda word: is_suffix_exponent_free(word, beta)
)

for length in range(4,100):
    unique = generate_greedy_words_unique(
        alphabet,
        1,
        lambda word: is_suffix_exponent_free(word, beta),
        seed=unique
    )

    nearly_extremal = [
        word
        for word in unique
        if is_nearly_extremal(
            word,
            alphabet,
            lambda w: is_exponent_free(w, beta))]

    print(f"Found {len(nearly_extremal)} nearly-extremal {beta}-free words of length {length}!")
    for i in range(0, len(nearly_extremal), max(1, len(nearly_extremal)//20)):
        print(color_word(nearly_extremal[i], alphabet))
    print(f"Need quaternary words of length {max_length(length, float(alpha), float(beta))}")
    