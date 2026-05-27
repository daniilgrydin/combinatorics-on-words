def sum_of_digits(word):
    sum = 0
    for c in word:
        sum += int(c)
    return sum

def permute(word, cycle):
    new_word = ""
    for c in word:
        if c not in cycle:
            new_word += c
            continue
        index = (cycle.find(c) + 1) % len(cycle)
        new_word += cycle[index]
    return new_word

def get_permutations(word, alphabet):
    from itertools import permutations
    perms = [''.join(p) for p in permutations(alphabet)]
    perms = list(set(perms))
    output = [""]*len(perms)
    for i in range(len(perms)):
        output[i] = (permute(word, perms[i]))
    return sorted(list(set(output)) + [word])

def substitude_alphabet(word, from_alphabet, to_alphabet):
    if word == from_alphabet[0]:
        return to_alphabet[0]
    
    output = ""
    for a in word:
        output += to_alphabet[from_alphabet.index(a)]
    return output

def convert_base(word, from_alphabet, to_alphabet):
    if word == from_alphabet[0]:
        return to_alphabet[0]
    
    if len(from_alphabet) == len(to_alphabet):
        return substitude_alphabet(word, from_alphabet, to_alphabet)

    decimal = 0
    for i in range(len(word)):
        digit = from_alphabet.index(word[i])
        if digit > 0:
            decimal += len(from_alphabet) ** (len(word)-1-i) * digit
    output = ""
    while decimal:
        output += to_alphabet[int(decimal % len(to_alphabet))]
        decimal //= len(to_alphabet)
    return output[::-1]

def encode_short(word, alphabet):
    from .alphabet import ENCODING_ALPHABET
    leading_zeros = 0
    for a in word:
        if a != alphabet[0]:
            break
        leading_zeros += 1
        
    return f"{alphabet}{f":{leading_zeros}" if leading_zeros else ""}:{convert_base(word, alphabet, ENCODING_ALPHABET)}"

def decode_short(code):
    from .alphabet import ENCODING_ALPHABET
    alphabet = ""
    encrypted = ""
    leading_zeros = 0
    if code.count(":") == 2:
        alphabet, leading_zeros, encrypted = code.split(":")
    else:
        alphabet, encrypted = code.split(":")
    leading_zeros = alphabet[0]*int(leading_zeros)
    return leading_zeros + convert_base(encrypted, ENCODING_ALPHABET, alphabet)

def word_to_chunks_of_n(binary, n=4):
    return " ".join(
        [binary[i : min(i + n, len(binary))] for i in range(0, len(binary), n)]
    )


def report_word(word):
    from combinatorics.square import get_squares, is_square_free
    from combinatorics.overlap import get_overlaps, is_overlap_free
    from square import is_extremal_square_free, is_nearly_extremal_square_free

    short_word = word[: min(len(word), 7)]
    if len(short_word) < len(word):
        short_word += "..."
    sqr = get_squares(word)
    print(f"\nIs square free? {is_square_free(word)}")
    print(f"\tSquares in {short_word} (total={len(sqr)}):")
    print(", ".join(sqr))
    ovr = get_overlaps(word)
    print(f"\nIs overlap free? {is_overlap_free(word)}")
    print(f"\tOverlaps in {short_word} (total={len(ovr)}):")
    print(", ".join(ovr))
    if is_extremal_square_free(word, set(word)):
        print(f"\n\t\t{short_word} is extremal.")
    if is_nearly_extremal_square_free(word, set(word)):
        print(f"\n\t\t{short_word} is nearly extremal.")
    print("-*-" * 12)


def color_word(word, alphabet):
    foreground = [
        "30",
        "31",
        "32",
        "33",
        "34",
        "35",
        "36",
        "91",
        "92",
        "93",
        "94",
        "95",
        "96",
    ]
    background = [
        "41",
        "42",
        "43",
        "44",
        "45",
        "46",
        "101",
        "102",
        "103",
        "104",
        "105",
        "106",
    ]

    output = ""

    for c in word:
        if c not in alphabet:
            output += c
            continue
        index = alphabet.index(c)
        fg = foreground[index // len(foreground)]
        bg = background[index % len(background)]
        output += f"\033[0;{fg};{bg}m {c} \033[0m"

    return output


def canonical_form(word):
    letters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    dic = {}
    dic_r = {}
    new_word = ""
    new_word_r = ""
    for i in range(len(word)):
        c = word[i]
        if c not in dic.keys():
            dic[c] = letters[len(dic.keys())]
        new_word += dic[c]

        c_r = word[len(word) - i - 1]
        if c_r not in dic_r.keys():
            dic_r[c_r] = letters[len(dic_r.keys())]
        new_word_r += dic_r[c_r]

    return min(new_word, new_word_r)


def cycle_letters(word, cycle: dict):
    result = ""
    for letter in word:
        if letter in cycle:
            result += cycle[letter]
        else:
            result += letter
    return result

def get_extensions(word, alphabet=None, positions=None):
    from .alphabet import extract_alphabet

    if alphabet is None:
        alphabet = extract_alphabet(word)
    if positions is None:
        positions = range(0, len(word) + 1)

    extensions = []
    for i in positions:
        for extension in extend_at_position(word, alphabet, i):
            if extension not in extensions:
                extensions.append(extension)
    return extensions


def extend_at_position(word, alphabet, position):
    extensions = []
    for a in alphabet:
        extensions.append(word[:position] + a + word[position:])
    return extensions


def complexity(word, n):
    factors = {}
    for i in range(0, len(word) - n + 1):
        factors[word[i : i + n]] = None
    return len(factors.keys())


def get_factors(w):
    result = set()
    for n in range(1, len(w) + 1):
        for i in range(0, len(w) - n + 1):
            result.add(w[i : n + i])
    return result


def p(w):
    n = len(w)
    for p in range(1, n):
        returnFlag = True
        for i in range(0, n - p):
            if w[i] != w[i + p]:
                returnFlag = False
                break
        if returnFlag:
            return p
    return 0

# def exponent(w):
#     for n in range(1, len(w) + 1):
#         for i in range(0, len(w) - n + 1):
#             f = w[i : n + i]
#             n = len(w)
#             period = 0
#             for p in range(1, n):
#                 returnFlag = True
#                 for j in range(0, n - p):
#                     if w[j] != w[j + p]:
#                         returnFlag = False
#                         break
#                 if returnFlag:
#                     period = p
#                     break
#             power = Rational(len(f), period) if period != 0 else Rational(1,1)
#             if target_exponent.is_less_than(power):
#                 #print(f"Target {target_exponent} < {power}")
#                 return False
#     return True

# def exponent(w):
#     p = period(w)
#     if p == 0:
#         return 0
#     return (len(w), p)

def backtrack(alphabet, length, condition):
    result = []

    def dfs(word):
        if len(word) == length:
            result.append(word)
            return

        for a in alphabet:
            if condition(word+a):
                dfs(word+a)

    dfs('')

    return result

def generate_greedy_words(alphabet, length, condition, seed=[""]):
    words = seed

    new_words = []

    for iteration in range(length):
        for i in range(len(words)):
            for j in range(len(alphabet)):
                candidate = words[i] + alphabet[j]
                if condition(candidate):
                    new_words.append(candidate)
        words = new_words
        new_words = []
    return words


def generate_greedy_words_unique(alphabet, iterations, condition, seed=[""]):
    words = seed
    unique_letters = [0]
    if seed != [""]:
        unique_letters = [len(set(s)) for s in seed]

    new_words = []
    new_unique_letters = []

    for iteration in range(iterations):
        # print(len(words[0]), len(words))
        for i in range(len(words)):
            for j in range(min(unique_letters[i] + 1, len(alphabet))):
                candidate = words[i] + alphabet[j]
                if condition(candidate):
                    if j >= unique_letters[i]:
                        new_unique_letters.append(unique_letters[i] + 1)
                    else:
                        new_unique_letters.append(unique_letters[i])
                    new_words.append(candidate)
        if len(new_words) == 0:
            return []
        words = new_words
        unique_letters = new_unique_letters
        new_words = []
        new_unique_letters = []
    return words

def circular(word):
    words = [word]
    for i in range(1,len(word)):
        words.append(words[-1][-1] + words[-1][:-1])
    return words

# def find_extremal_from_list(words, beta):
#     from .exponent import is_exponent_free
#     from .exponent import ExtendedReal

def all_cycles(alphabet) -> list[dict]:
    from itertools import permutations

    cycles = []
    cycles_set = {''}

    # Get permutations of the alphabet.
    cycle_permutations = []
    for i in range(2, len(alphabet)+1):
        cycle_permutations.extend(permutations(alphabet, i))
    
    # Create circular words from the permutations.
    circular_words = []
    for p in cycle_permutations:
        word = ""
        for a in p:
            word += a
        circular_words.append(circular(word))
    
    # Create the set from circular words.
    for c in circular_words:
        c.sort()
        cycles_set.add(c[0])
    
    # Turn cycle strings into dictionaries
    for c in cycles_set:
        cycle_dict = {}
        for a in alphabet:
            letter_at = c.find(a)
            if letter_at == -1:
                cycle_dict[a] = a
            else:
                cycle_dict[a] = c[(letter_at + 1) % len(c)]
        cycles.append(cycle_dict)

    return cycles
