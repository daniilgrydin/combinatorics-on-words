from combinatorics.word import generate_greedy_words_unique_parallel
from combinatorics.square import has_square_suffix, is_square_free
from combinatorics.extremal import is_extremal

def has_no_square_suffix(w):
    return not has_square_suffix(w)

if __name__ == '__main__':
    words = generate_greedy_words_unique_parallel("012", 25, has_no_square_suffix)

    for word in words:
        if is_extremal(word, "012", is_square_free):
            print("found an extremal square-free ternary word of length 25:")
            print(word)
            break

    print("Done!")