from libraries.word import generate_greedy_words_unique
from libraries.exponent import is_suffix_exponent_free, ExtendedReal, is_exponent_free
from libraries.extremal import is_extremal, is_nearly_extremal
from libraries.square import is_square_free
from libraries.word import color_word

alphabet = "01"
length = 4
alpha = ExtendedReal(7, 3, True)
beta = ExtendedReal(17, 7, False)

print(f"Generating ({alpha})-free words of length {54+length} over the alphabet {alphabet}")

unique = generate_greedy_words_unique(
    alphabet,
    1,
    lambda word: is_suffix_exponent_free(word, alpha)
)

print(f"Starting with {len(unique)} words")

for l in range(length):
    
    unique = generate_greedy_words_unique(
        alphabet,
        1,
        lambda word: is_suffix_exponent_free(word, alpha),
        seed = unique
    )
    
    extremal = [
        word for word in unique
        if is_nearly_extremal(
            word,
            alphabet,
            lambda word: is_exponent_free(word, beta)
        )
    ]

    print(f"l={l}, extremal found: {len(extremal)}")
    print()
    if len(extremal) > 0:
        if(len(extremal) < 6):
            for word in extremal:
                print(color_word(word, alphabet))
        else:
            print(color_word(extremal[0], alphabet))
            print(color_word(extremal[1], alphabet))
            print(" " * (l*3//2-2) + "· · ·")
            print(color_word(extremal[len(extremal)//2], alphabet))
            print(" " * (l*3//2-2) + "· · ·")
            print(color_word(extremal[-2], alphabet))
            print(color_word(extremal[-1], alphabet))
        break