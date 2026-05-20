from libraries.methods import THUE_MORSE_WORD, WORD

# for c in range(2, 9):
#     wrd = THUE_MORSE_WORD.ternary_thue_morse_word(2**c)
#     # wrd = wrd.replace("2", "")
#     # wrd = WORD.word_to_chunks_of_n(wrd, 4)
#     wrd = WORD.word_to_chunks_of_n(wrd, len(wrd) // 4)
#     print("length:", f"2^{c}")
#     print(WORD.color_word(wrd.replace(" ", "\n"), ["0", "1", "2"]))
#     print()

wrd = THUE_MORSE_WORD.thue_morse_definition(2**8)
# wrd = wrd.replace("2", "")
# wrd = WORD.word_to_chunks_of_n(wrd, 4)
wrd = WORD.word_to_chunks_of_n(wrd, len(wrd) // 16)
print(WORD.color_word(wrd.replace(" ", "\n"), ["0", "1", "2"]))
print()