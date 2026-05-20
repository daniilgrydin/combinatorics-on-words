# Definition 1.3.1. of the Thue-Morse Word with n characters.
def thue_morse_definition(length):
    from libraries.word import sum_of_digits
    thue_morse = ""
    for i in range(length):
        binary = bin(i)[2:]
        s = sum_of_digits(binary)
        digit = s % 2
        thue_morse += str(digit)
    return thue_morse

# Alternate definition 1 for t using a DFAO
def thue_morse_definition_automaton(length):
    t = ""
    for i in range(0, length):
        b = format(i, 'b')
        state = False
        for j in range(0, len(b)):
            if b[j] == '1':
                state = not state
        t += '1' if state else '0'
    return t

# Alternative definition 2 for t using recursion
def thue_morse_definition_recursive(length: int):
    digits = [0] * length
    for i in range(length):
        if i % 2 == 0:  # even
            digits[i] = digits[i // 2]
        else:  # odd
            digits[i] = 1 - digits[(i - 1) // 2]
    return "".join([str(d) for d in digits])

# Alternate definition 3 using the Thue-Morse morphism. 
def thue_morse_definition_alt_3(length: int):
    length_b = length.bit_length()  # rounded up log base 2

    # The Thue-Morse morphism function.
    def mu(word):
        map = {"0": "01", "1": "10"}
        result = ""
        for digit in word:
            result += map[digit]
        return result

    result = "0"
    for _ in range(length_b):
        result = mu(result)
    return result[:length]


def ternary_thue_morse_word(length):
    length_b = length * 2  # approximation based on observation
    tm_word = thue_morse_definition(length_b)
    count = 0
    ttm_word = ""
    for b in tm_word:
        if b == "0":
            ttm_word += str(count)
            count = 0
        else:
            count += 1
    return ttm_word[:length]
