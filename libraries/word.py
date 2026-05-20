def sum_of_digits(word):
    sum = 0
    for c in word:
        sum += int(c)
    return sum


def word_to_chunks_of_n(binary, n=4):
    return " ".join(
        [binary[i : min(i + n, len(binary))] for i in range(0, len(binary), n)]
    )

def report_word(word):
    from libraries.square import get_squares, is_square_free
    from libraries.overlap import get_overlaps, is_overlap_free
    from extremal import is_extremal, is_nearly_extremal
    
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
    if is_extremal(word, set(word)):
        print(f"\n\t\t{short_word} is extremal.")
    if is_nearly_extremal(word, set(word)):
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

def generate_greedy_words(alphabet, length, condition):
    words = [""]
    
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

def generate_greedy_words_unique(alphabet, length, condition):
    words = [""]
    unique_letters = [0]
    
    new_words = []
    new_unique_letters = []
    
    for iteration in range(length):
        for i in range(len(words)):
            for j in range(min(unique_letters[i]+1, len(alphabet))):
                candidate = words[i] + alphabet[j]
                if condition(candidate):
                    if j >= unique_letters[i]:
                        new_unique_letters.append(unique_letters[i]+1)
                    else:
                        new_unique_letters.append(unique_letters[i])
                    new_words.append(candidate)
        words = new_words
        unique_letters = new_unique_letters
        new_words = []
        new_unique_letters = []
    return words