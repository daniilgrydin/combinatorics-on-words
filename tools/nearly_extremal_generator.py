from combinatorics.word import generate_greedy_words_unique
from combinatorics.exponent import ExtendedReal, is_suffix_exponent_free, is_exponent_free
from combinatorics.extremal import is_nearly_extremal

#beta = ExtendedReal(7,4,True)

def generate_nearly_extremal(alphabet, min_length, max_length, beta, file_path, prefix="", suffix=""):

    unique = generate_greedy_words_unique(
        alphabet,
        1,
        lambda word: is_suffix_exponent_free(word, beta)
    )

    nearly_extremal = []

    for length in range(2,max_length+1):
        print(f"Current length: {length}...")

        unique = generate_greedy_words_unique(
            alphabet,
            1,
            lambda word: is_suffix_exponent_free(word, beta),
            seed = unique
        )

        if length < min_length: continue

        new_nearly_extremal = [
            word
            for word in unique
            if word[:len(prefix)] == prefix and word[-len(suffix):] == suffix
                and is_nearly_extremal(
                word,
                alphabet,
                lambda w: is_exponent_free(w, beta))]
                
        nearly_extremal.extend(new_nearly_extremal)

        with open(file_path, "w") as f:
            f.write("\n".join(nearly_extremal))

generate_nearly_extremal("012", 0, 80, ExtendedReal(7,4,True), "data/prescribed_nearly_extremal_74p_ternary.txt", "010210120210201", "120210201210212")
