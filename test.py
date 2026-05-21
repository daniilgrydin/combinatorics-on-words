from libraries.word import generate_greedy_words_unique, generate_greedy_words
from libraries.exponent import is_suffix_exponent_free, ExtendedReal
from libraries.word import color_word
from MR2020.proofs import *

# Verify Theorem 2.3 from "Lengths of Extremal Square-free Words"
#
# def h(w):
#     if w == '0':
#         return ['0752a3']
#     if w == '1':
#         return ['07a3b8']
#     if w == '2':
#         return ['075948', '07594148']
    
#     result = []
#     for a in w:
#         result.append(h(a))
#     return result

# print(verify_theorem_2_3(['0','1','2'], h))

# alphabet = "012"
# length = 50
# beta = ExtendedReal(7, 4, True)

# print(f"Generating ({beta})-free words of length {length} over the alphabet {alphabet}")

# unique = generate_greedy_words_unique(
#     alphabet,
#     length,
#     lambda word: is_suffix_exponent_free(word, beta)
# )

# print(f"Total words found: {len(unique)}")


# for w in unique:
#     if Words.isExtremalBPlusFree(w,7/4):
#         print(w,"is extremal 7/4+-free")

# print("done")
# print()
# if(len(unique) < 6):
#     for word in unique:
#         print(color_word(word, alphabet))
# else:
#     print(color_word(unique[0], alphabet))
#     print(color_word(unique[1], alphabet))
#     print(" " * (length*3//2-2) + "· · ·")
#     print(color_word(unique[len(unique)//2], alphabet))
#     print(" " * (length*3//2-2) + "· · ·")
#     print(color_word(unique[-2], alphabet))
#     print(color_word(unique[-1], alphabet))
# all = generate_greedy_words(
#     alphabet,
#     length,
#     lambda word: is_suffix_exponent_free(word, ExtendedReal(7, 4, True))
# )

# print(len(all))