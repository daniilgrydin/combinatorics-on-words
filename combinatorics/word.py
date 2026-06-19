import tools.file_rw as rw

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
    # perms = list(set(perms))
    perms = [
        {alphabet[i]: perm[i] for i in range(len(alphabet))}
        for perm in perms
    ]
    output = [""]*len(perms)
    for i in range(len(perms)):
        for a in word:
            output[i] += perms[i][a]
    return sorted(list(set(output)))

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
        
    return str(alphabet) + ":" + (str(leading_zeros) if leading_zeros else "") + str(convert_base(word, alphabet, ENCODING_ALPHABET))

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
    print("\nIs square free?", is_square_free(word))
    print("\tSquares in", short_word, "(total=", len(sqr) + "):")
    print(", ".join(sqr))
    ovr = get_overlaps(word)
    print("\nIs overlap free?", is_overlap_free(word))
    print("\tOverlaps in", short_word, "(total=", len(ovr) + "):")
    print(", ".join(ovr))
    if is_extremal_square_free(word, set(word)):
        print("\n\t\t", short_word, "is extremal.")
    if is_nearly_extremal_square_free(word, set(word)):
        print("\n\t\t", short_word, "is nearly extremal.")
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
        output += "\033[0;" + str(fg) + ";" + str(bg) + "m" + str(c) + "\033[0m"

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


def period(w):
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
#     from .exponent import Rational
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
#             if not target_exponent < power:
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


def explain_word(
        *,
        length          : int | tuple | None            = None,
        exponent_free                           = None,
        extremal        : bool | None           = None,
        nearly_extremal : bool | None           = None,
        **kwargs
    ):
    data = []
    if extremal is not None:
        data.append("extremal")
    if nearly_extremal is not None:
        data.append("nearly extremal")
    if exponent_free is not None:
        data.append((str(exponent_free)) + "-free")
    data.append("words")
    if length is not None:
        data.append("of length" + str(length))
    if len(kwargs) > 0:
        other = [
            (str(key) + ": " + str(value) if not isinstance(value, bool) else str(key))
            for key, value in kwargs.items()]
        data.append("with additional parameters: " + ", ".join(other))
    return " ".join(data)

def construct_file_name(
        *args,
        length          : int | tuple | None            = None,
        exponent_free                           = None,
        extremal        : bool | None           = None,
        nearly_extremal : bool | None           = None,
    ):
    data = []
    if length is not None:
        if isinstance(length, tuple):
            data.append(str(length[0]) + "-" + str(length[1]))
        else:
            data.append(length)
            
    if extremal is not None:
        data.append("ex")
    if nearly_extremal is not None:
        data.append("nex")
    if exponent_free is not None:
        data.append(str(exponent_free.rational.numerator) + ("+" if exponent_free.plus else "-") + str(exponent_free.rational.denominator))
    data.extend(sorted(args))
    return "-".join(data) + ".txt"

def word_filename_description(
        *arg,
        length          : int | tuple | None            = None,
        exponent_free                           = None,
        extremal        : bool | None           = None,
        nearly_extremal : bool | None           = None,
        **kwargs
    ):
    for a in arg:
        kwargs[a] = True    
    description = explain_word(
        length=length,
        exponent_free=exponent_free,
        extremal=extremal,
        nearly_extremal=nearly_extremal,
        **kwargs
    )
    things = ()
    for key, value in kwargs.items():
        if isinstance(value, bool):
            things += (key[:min(3, len(key))],)
        else:
            val = str(value)
            things += (key[:min(3, len(key))] + val[:min(3, len(val))],)
    filename = construct_file_name(
        length=length,
        exponent_free=exponent_free,
        extremal=extremal,
        nearly_extremal=nearly_extremal,
        *things
    )
    return (filename, description)

def save_words(
    words=[],
    *arg,
    length          : int | tuple | None    = None,
    exponent_free                           = None,
    extremal        : bool | None           = None,
    nearly_extremal : bool | None           = None,
    file_name       : str | None            = None,
    **kwargs
):
    from datetime import datetime
    auto_filename, description = word_filename_description(
        *arg,
        length=length,
        exponent_free=exponent_free,
        extremal=extremal,
        nearly_extremal=nearly_extremal,
        **kwargs
    )
    if file_name is None:
        file_name = auto_filename
    
    with open("data/" + file_name, "w") as f:
        f.write("\n".join(words))
    
    with open("data/index.md", "a") as f:
        f.write("| " + str(datetime.now()) + " | " + str(len(words)) + " | `" + str(file_name) + "` | " + str(description) + " |\n")
    
    return file_name

def get_words(
    *args,
    length          : int | tuple | None    = None,
    exponent_free                           = None,
    extremal        : bool | None           = None,
    nearly_extremal : bool | None           = None,
    **kwargs
):
    path, _ = word_filename_description(
        *args,
        length = length,
        exponent_free = exponent_free,
        extremal = extremal,
        nearly_extremal = nearly_extremal,
        **kwargs
    )
    # print("Looking for", path)
    max_length = 0
    try:
        with open("data/" + path, "r") as f:
            words = []
            for line in f.readlines():
                word = line.strip()
                max_length = max(max_length, len(word))
                words.append(word)
            return (True, words, max_length)
    except FileNotFoundError:
        print("Not Found")
        return (False, [""], 0)
    
def append_words(
    words,
    *args,
    # length          : int | tuple | None    = None,
    # exponent_free                           = None,
    # extremal        : bool | None           = None,
    # nearly_extremal : bool | None           = None,
    **kwargs
):
    success, recorded_words, _ = get_words(*args, **kwargs)
    if not success:
        return save_words(words, *args, **kwargs)
    for word in words:
        if word not in recorded_words:
            recorded_words.append(word)
    return save_words(sorted(recorded_words, key=lambda w: (len(w), w)), *args, **kwargs)

def index_all_occurrences(word, subword):
    indices = []
    n = len(subword)
    for i in range(0, len(word)-n+1):
        if word[i:i+n] == subword:
            indices.append(i)
    return indices

def get_common_prefix(words):
    if len(words) == 0:
        return ""

    common_prefix = ""
    for i in range(len(min(words))):
        current_letter = words[0][i] 
        for w in words:
            if w[i] != current_letter:
                return common_prefix
        common_prefix += current_letter
    return common_prefix

def get_common_suffix(words):
    if len(words) == 0:
        return ""

    common_suffix = ""
    for i in range(1, len(min(words))+1):
        current_letter = words[0][-i] 
        for w in words:
            if w[-i] != current_letter:
                return common_suffix[::-1]
        common_suffix += current_letter
    return common_suffix[::-1]


def index_prefix_occurrences(length, words = [], words_file = ""):
    words_to_search = []

    if len(words) > 0:
        words_to_search = words
    else: 
        try:
            words_to_search = rw.load_words(words_file)
        except FileNotFoundError:
            return [("", 0)]

    prefixes = {}

    for w in words_to_search:
        if len(w) >= length:
            prefixes[w[:length]] = prefixes.get(w[:length], 0) + 1
    
    return prefixes

def index_suffix_occurrences(length, words = [], words_file = ""):
    words_to_search = []

    if len(words) > 0:
        words_to_search = words
    else: 
        try:
            words_to_search = rw.load_words(words_file)
        except FileNotFoundError:
            return [("", 0)]
    
    suffixes = {}

    for w in words_to_search:
        if len(w) >= length:
            suffixes[w[-length:]] = suffixes.get(w[-length:], 0) + 1
    
    return suffixes

def index_factor_occurrences(length, words = [], words_file = ""):
    words_to_search = []

    if len(words) > 0:
        words_to_search = words
    else: 
        try:
            words_to_search = rw.load_words(words_file)
        except FileNotFoundError:
            return [("", 0)]
    
    factors = {}

    for w in words_to_search:
        if len(w) >= length:
            for i in range(0,len(w) - length + 1):
                factors[w[i:length+i]] = factors.get(w[-length:], 0) + 1
    
    return factors

def keys_from_max_values(dict, n = 1):
    keys = []
    for _ in range(n):
        if len(dict) == 0: break
        keys.append(max(dict, key=dict.get))
    return keys

def bucket_words_by_length(words):
    result = [[""]]
    for w in words:
        index = len(w)
        if index > len(result):
            for _ in range(len(result)+1, index+1):
                    result.append([])
        result[index].append(w)
    return result