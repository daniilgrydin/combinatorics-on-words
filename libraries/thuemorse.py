def thue_morse_definition(length):
    from libraries.word import sum_of_digits
    thue_morse = ""
    for i in range(length):
        binary = bin(i)[2:]
        s = sum_of_digits(binary)
        digit = s % 2
        thue_morse += str(digit)
    return thue_morse

def thue_morse_definition_alt_1(length):
    thue_morse = ""
    for i in range(length):
        binary = bin(i)[2:]
        digit = 0
        for b in binary:
            if b == "1":
                digit = 1 - digit
        thue_morse += str(digit)
    return thue_morse

def thue_morse_definition_alt_2(length: int):
    digits = [0] * length
    for i in range(length):
        if i % 2 == 0:  # even
            digits[i] = digits[i // 2]
        else:  # odd
            digits[i] = 1 - digits[(i - 1) // 2]
    return "".join([str(d) for d in digits])

def thue_morse_definition_alt_3(length: int):
    length_b = length.bit_length()  # rounded up log base 2

    def mu(s):
        basis = {"0": "01", "1": "10"}
        result = ""
        for c in s:
            result += basis[c]
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
