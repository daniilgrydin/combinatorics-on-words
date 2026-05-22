from combinatorics.word import generate_greedy_words_unique
from combinatorics.exponent import is_suffix_exponent_free, ExtendedReal, is_exponent_free
from combinatorics.extremal import is_extremal, is_nearly_extremal
from combinatorics.square import is_square_free
from combinatorics.word import color_word, encode_short
from combinatorics.morphism import is_synchronizing, is_uniform, dict_to_morphism
import itertools

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
#    print(f"Need quaternary words of length {max_length(length, float(alpha), float(beta))}")

quaternary_words_file = open("data/75_free_quaternary_words.txt", 'r')
quaternary_words_75p_free = []
for line in quaternary_words_file.readlines():
    quaternary_words_75p_free.append(line.removesuffix('\n'))
quaternary_words_file.close()

print(f"\nThere are {len(quaternary_words_75p_free)} quaternary 7/5+-free words up to length 10.")

nearly_extremal_dummy = ['01','10','12','20','102','012','210','201']
nearly_extremal_combinations = itertools.combinations(nearly_extremal_dummy, 4)

candidate_morphism_dicts = []
for i in nearly_extremal_combinations:
    new_morphism_dict = {}
    new_morphism_dict['0'] = i[0]
    new_morphism_dict['1'] = i[1]
    new_morphism_dict['2'] = i[2]
    new_morphism_dict['3'] = i[3]
    if is_uniform(dict_to_morphism(new_morphism_dict), "0123"):
        candidate_morphism_dicts.append(new_morphism_dict)

print(f"\nThere are {len(candidate_morphism_dicts)} candidate morphisms to check.\n")

for m in candidate_morphism_dicts:
    passFlag = True
    morphism = dict_to_morphism(m)

    if not is_uniform(morphism, "0123"):
        print(f"Morphism {m} is not uniform")
        continue
    elif not is_synchronizing(morphism, "0123"):
        print(f"Morphism {m} is not synchronizing")
        continue

    for w in quaternary_words_75p_free:
        if not is_exponent_free(morphism(w), beta):
            print(f"Morphism {m} maps {w} to a ternary word {morphism(w)} which is not 7/4+-free.")
            passFlag = False
            break

    if passFlag:
        print(f"\nMorphism {m} sends every 7/5+-free quaternary word to a 7/4+-free ternary word!\n")