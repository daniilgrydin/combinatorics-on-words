from combinatorics.word import generate_greedy_words_unique, get_factors
from combinatorics.exponent import is_suffix_exponent_free, ExtendedReal, is_exponent_free
from combinatorics.extremal import is_nearly_extremal
from combinatorics.morphism import dict_to_morphism, is_synchronizing

from itertools import combinations
from math import comb
import time


alphabet = "012"
max_q_to_check = 50

alpha = ExtendedReal(7, 5, True) # quaternary
beta = ExtendedReal(7, 4, True) # ternary

quaternary_images = []

morphism_rejections = {"not synchronizing":0}

def check_valid_morphism(tuple):
    H0, H1, H2, H3 = tuple
    morphism = dict_to_morphism({
        "0": H0,
        "1": H1,
        "2": H2,
        "3": H3
    })

    if not is_synchronizing(morphism, "0123"): 
        morphism_rejections["not synchronizing"] += 1
        return False

    for q in quaternary_images:
        if not is_exponent_free(morphism(q), beta): 
            #print(q)
            morphism_rejections[q] = morphism_rejections.get(q,0) + 1
            return False

    return True

def priority_buckets(words):
    priority = {}
    shared_prefixes = {}
    shared_suffixes = {}
    for w in words:
        for i in range(1,len(w)):
            prefix_key = w[:i]
            shared_prefixes[prefix_key] = shared_prefixes.get(prefix_key,[]).append(w)
            
            suffix_key = w[-i:]
            shared_suffixes[suffix_key] = shared_suffixes.get(suffix_key,[]).append(w)
    


with open("data/75_free_quaternary_words.txt", "r") as f:
    for q in f.readlines():
        if len(q) > 1:
            quaternary_images.append(q.strip())

print("Loaded 7/4+-free quaternary words of length", len(quaternary_images))

# unique = generate_greedy_words_unique(
#     alphabet,
#     1,
#     lambda word: is_suffix_exponent_free(word, beta)
# )

# for length in range(len(unique[0])+1, 100):
#     start = time.time()
#     unique = generate_greedy_words_unique(
#         alphabet,
#         1,
#         lambda word: is_suffix_exponent_free(word, beta),
#         seed=unique
#     )

#     nearly_extremal = [
#         word
#         for word in unique
#         if
#         word[-1] != "0"
#         and is_nearly_extremal(
#             word,
#             alphabet,
#             lambda w: is_exponent_free(w, beta))]

nearly_extremal = []
for line in open("data/nearly_extremal_74p_ternary.txt", 'r').readlines():
    candidate = line.strip()
    if candidate[-1] == '2' and len(candidate) <= max_q_to_check:
        nearly_extremal.append(line.strip())
print("Loaded nearly_extremal with size", len(nearly_extremal))

# Create nearly_extremal_lengths. Each index holds words of the index's length.
nearly_extremal_lengths = []
for i in range(0, len(max(nearly_extremal, key=len)) + 1):
    nearly_extremal_lengths.append([])
# Populate nearly_extremal_lengths
for n in nearly_extremal:
    nearly_extremal_lengths[len(n)].append(n)

# Count the number of combinations
total_combinations_to_check = 0
for n in nearly_extremal_lengths:
    total_combinations_to_check += comb(len(n),4)
print(f"Total combinations to check: {total_combinations_to_check}")

#print(f"Found\t{len(nearly_extremal)}\twords of length\t{length}\tin\t{round(time.time()-start,1)}")
# print(f"There are {(len(nearly_extremal))*(len(nearly_extremal)-1)*(len(nearly_extremal)-2)*(len(nearly_extremal)-3)} permutations of them.")
# for i in range(0, len(nearly_extremal), max(1, len(nearly_extremal)//5)):
#     print(color_word(nearly_extremal[i], alphabet))

count = 0
for n in nearly_extremal_lengths:
    if len(n) != 0:
        print("q =",len(n[-1]))
        print(morphism_rejections)
    for combo in combinations(n, 4):
        count += 1
        # if not_synchronizing_count % 1000000 == 0:
        #     print(not_synchronizing_count,"morphisms rejected because they are not synchronizing")
        # if not_beta_free_count % 1000000 == 0:
        #     print(not_beta_free_count,"morphisms rejected because their images are not 7/4+-free")

        # if not is_synchronizing(morphism): continue
        if not check_valid_morphism(combo): continue
        print("Found morphism!\a")
        print("0", combo[0])
        print("1", combo[1])
        print("2", combo[2])
        print("3", combo[3])
        print()
        break