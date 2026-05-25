from combinatorics.word import generate_greedy_words
from combinatorics.square import has_square_suffix, is_square_free
from combinatorics.extremal import is_extremal

words = generate_greedy_words("012", 25, lambda w: not has_square_suffix(w))

for word in words:
    if is_extremal(word, "012", is_square_free):
        print("found an extremal square-free ternary word of length 25:")
        print(word)
        break

print("Done!")