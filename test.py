from libraries.word import generate_greedy_words_unique, generate_greedy_words
from libraries.exponent import is_suffix_exponent_free, ExtendedReal
from libraries.word import color_word
alphabet = "0124"
length = 14
beta = ExtendedReal(4, 3, True)

print(f"Generating ({beta})-free words of length {length} over the alphabet {alphabet}")

unique = generate_greedy_words_unique(
    alphabet,
    length,
    lambda word: is_suffix_exponent_free(word, beta)
)

print(f"Total words found: {len(unique)}")
print()
if(len(unique) < 6):
    for word in unique:
        print(color_word(word, alphabet))
else:
    print(color_word(unique[0], alphabet))
    print(color_word(unique[1], alphabet))
    print(" " * (length*3//2-2) + "· · ·")
    print(color_word(unique[len(unique)//2], alphabet))
    print(" " * (length*3//2-2) + "· · ·")
    print(color_word(unique[-2], alphabet))
    print(color_word(unique[-1], alphabet))
# all = generate_greedy_words(
#     alphabet,
#     length,
#     lambda word: is_suffix_exponent_free(word, ExtendedReal(7, 4, True))
# )

# print(len(all))