from combinatorics.word import generate_greedy_words_unique, backtrack
from combinatorics.exponent import ExtendedReal, is_suffix_exponent_free, is_exponent_free
from combinatorics.extremal import is_nearly_extremal

beta = ExtendedReal(7,4,True)

unique = generate_greedy_words_unique(
    "012",
    1,
    lambda word: is_suffix_exponent_free(word, beta)
)

nearly_extremal = []

for length in range(2,51):
    unique = generate_greedy_words_unique(
        "012",
        1,
        lambda word: is_suffix_exponent_free(word, beta),
        seed = unique
    )


    new_nearly_extremal = [
        word
        for word in unique
        if is_nearly_extremal(
            word,
            "012",
            lambda w: is_exponent_free(w, beta))]
    
    nearly_extremal.extend(new_nearly_extremal)
    
    print(f"Length: {length} 7/4+-free words: {len(unique)} Nearly extremal: {len(new_nearly_extremal)}")

with open("data/nearly_extremal_74p_ternary.txt", "w") as f:
    f.write("\n".join(nearly_extremal))

print("done")