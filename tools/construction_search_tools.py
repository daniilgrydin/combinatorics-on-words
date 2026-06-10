import tools.file_rw as rw

# alpha_a is the alphabet of words in words_file_a
# words_file_a should be the path to a file with alpha-free words over an n+1 size alphabet (eg. 7/5-free quaternary words)
# nearly_extremal_words_file_b should be the path to a file with nearly extremal beta-free words over an n size alphabet (eg. nearly extremal 7/4+ ternary words)
# beta is power of the desired words obtained from the morphism
# filter is a function of a word that can narrow down the number of combinations to check (eg. words beginning with 0102 and ending with 0212)
# output is a file to write the morphisms to
def find_morphism(alpha_a, words_file_a, nearly_extremal_words_file_b, beta, q, filter, output, STOP=-1):
    from math import comb
    from random import randrange
    from itertools import combinations

    words_a = []
    with open(words_file_a, "r") as f:
        for w in f.readlines():
            if len(w) > 1:
                words_a.append(w.strip())

    print(f"Loaded {words_file_a}")

    nearly_extremal = []
    for line in open(nearly_extremal_words_file_b, 'r').readlines():
        candidate = line.strip()
        if filter(candidate) and len(candidate) == q:
            nearly_extremal.append(line.strip())
    print(f"Loaded {len(nearly_extremal)} from {nearly_extremal_words_file_b}")

    # # Create nearly_extremal_lengths. Each index holds words of the index's length.
    # nearly_extremal_lengths = []
    # for i in range(0, max_q+1):
    #     nearly_extremal_lengths.append([])
    # # Populate nearly_extremal_lengths
    # for n in nearly_extremal:
    #     nearly_extremal_lengths[len(n)].append(n)

    # Count the number of combinations
    print(f"Total combinations to check: {comb(len(nearly_extremal), len(alpha_a))}")

    def check_valid_morphism(tuple):
        from combinatorics.morphism import dict_to_morphism, is_synchronizing
        from combinatorics.exponent import is_exponent_free

        morphism_dict = {}
        for i in range(0, len(alpha_a)):
            morphism_dict[alpha_a[i]] = tuple[i]

        morphism = dict_to_morphism(morphism_dict)

        if not is_synchronizing(morphism, alpha_a): 
            return False

        for w in words_a:
            if not is_exponent_free(morphism(w), beta): 
                return False

        return True
    
    print("checking q =", i)

    morphisms = []
    candidate_combinations = list(combinations(nearly_extremal, len(alpha_a)))
    n = len(candidate_combinations)
    found = 0
    combo_count = 0
    for i in range(n):
        combo = candidate_combinations.pop(n - i)

        if combo_count % 25 == 0:
            print("Checked",combo_count,"morphisms.")
        combo_count += 1

        if not check_valid_morphism(combo): continue
        print("Found morphism!\a")
        result_morphism_dict = {}
        for i in range(0, len(alpha_a)):
            print(alpha_a[i], combo[i])
            result_morphism_dict[alpha_a[i]] = combo[i]
        morphisms.append(result_morphism_dict)
        print()
        found += 1
        if found == STOP:
            break

    if len(morphisms) >= len(alpha_a):
        rw.save_images_of_morphisms([m.values() for m in morphisms], output)
    
    print("Done")

# alphabet is what nearly extremal words will be made over
# max_length is the size [1,max_length] of nearly_extremal words to make
# file_path is the file that the nearly extremal words will be written to 
def generate_nearly_extremal(alphabet, max_length, beta, file_path,  prefix="", suffix=""):
    from ..combinatorics.word import generate_greedy_words
    from ..combinatorics.exponent import is_suffix_exponent_free, is_exponent_free
    from ..combinatorics.extremal import is_nearly_extremal

    nearly_extremal = []
    
    try:
        print("Reading from file.")
        for l in open(file_path, 'r').readlines():
            nearly_extremal.append(l.strip())
        print(f"{len(nearly_extremal)} words loaded from file.")
        if len(nearly_extremal) > 0:
            existing_length = len(nearly_extremal[-1])
        else:
            existing_length = 1
    except FileNotFoundError:
        existing_length = 1


    existing_length = max(existing_length - len(prefix) - len(suffix), 1)
    print(f"Generating nearly extremal {beta}-free words over {alphabet}")

    words = generate_greedy_words(
        alphabet,
        existing_length,
        lambda word: is_suffix_exponent_free(word, beta)
    )


    for length in range(existing_length+1, max_length - len(prefix) - len(suffix) + 1):
        print(f"Currently generating length: {length + len(prefix) + len(suffix)}...")

        words = generate_greedy_words(
            alphabet,
            1,
            lambda word: is_suffix_exponent_free(word, beta),
            seed = words
        )

        count = 0

        for w in words:
            if is_nearly_extremal(
            prefix + w + suffix,
            alphabet,
            lambda w: is_exponent_free(w, beta) 
            ): 
                nearly_extremal.append(prefix + w + suffix)
                count += 1
                if count % 10 == 0:
                    print(f"{count} found...")
                    with open(file_path, 'w') as f:
                        f.write("\n".join(nearly_extremal))
        
        with open(file_path, 'w') as f:
            f.write("\n".join(nearly_extremal))
            

    print("Done")

# Finds morphisms with ideal bookends and returns the constructions of those morphisms and bookends.
def find_ideal_constructions(morphism_images_file, image_count, 
                         max_bookend_size = -1, min_A_size = 0, 
                         B_seed_file = None, do_print = True, output_file = None):
    from tools.decomposition import get_bookends_from_morphism, TernaryConstructionDecomposition
    from bookends import is_left_bookend_ideal, is_right_bookend_ideal
    from tools.file_rw import load_words_by_length
    from typing import List

    morphisms = []
    current = []
    for line in open(morphism_images_file, 'r').readlines():
        if line[0] == '-': continue
        current.append(line.strip())
        if len(current) == image_count:
            morphisms.append(current.copy())
            current.clear()

    if do_print:
        print(len(morphisms), "morphisms loaded.")

    if B_seed_file != None:
        B_seed = load_words_by_length(B_seed_file)
        if do_print: 
            print("Words loaded from B seed file.")
    else:
        B_seed = None
        if do_print: 
            print("No B seed file.")

    count = 0
    result_constructions : List[TernaryConstructionDecomposition] = []

    for m in morphisms:
        if count % 5 == 0:
            if do_print:
                print(count, "morphisms processed...")

        count += 1
        try:
            r,s = get_bookends_from_morphism(m, max_bookend_size, min_A_size, B_seed)
            if do_print:
                print("Bookends found for", m)
        except:
            continue

        if is_left_bookend_ideal(m, r) and is_right_bookend_ideal(m, s):
            if do_print:
                print("Found ideal bookends for", m)
                print("r:",r)
                print("s:",s)
            result_constructions.append(TernaryConstructionDecomposition(m, r = r, s = s))

    if output_file != None:
        rw.save_constructions(result_constructions, output_file)

    return result_constructions

# Returns the n prefixes that occur most in the file of words with a minimum length.
def best_common_prefixes(words_file, n, minimum_length = 0):
    from combinatorics.word import get_common_prefix

    words = []
    for line in open(words_file, 'r').readlines():
        words.append(line.strip())
    
    prefixes = {}

    start = max(minimum_length, len(get_common_prefix(words)))
    stop = len(min(words, key=len))
    for i in range(start+1, stop+2):
        for w in words:
            prefixes[w[:i]] = prefixes.get(w[:i], 0) + 1
    
    best = []
    for _ in range(n):
        prefix = max(prefixes, key=prefixes.get)
        best.append((prefix, prefixes[prefix]))
        prefixes.pop(prefix)
    
    return best

def find_best_constructions(constructions_file, n=1, deep_check = True, do_print = True):
    from combinatorics.exponent import get_min_critical_exponent_of_extensions_of_words, get_critical_exponent_of_words

    constructions = rw.load_constructions(constructions_file)
    
    exponent_differences = {}
    for c in constructions:
        if do_print:
            print(f"Checking construction with morphism images: \n{c.get_morphism_images()}.")

        if deep_check:

            image_critical = get_critical_exponent_of_words(c.get_morphism_images())
            left_critical  = get_critical_exponent_of_words([c.r + w for w in c.get_morphism_images()])
            right_critical = get_critical_exponent_of_words([w + c.s for w in c.get_morphism_images()])

            if do_print:
                print(f"f(c) has critical exponent {image_critical}.")
                print(f"rf(c) has critical exponent {left_critical}.")
                print(f"f(c)s has critical exponent {right_critical}.")
        
        alpha = c.get_alpha()
        beta  = c.get_beta()

        if do_print:
            print(f"rf(c)s has critical exponent alpha = {alpha}.")
            print(f"All extensions of rf(c)s have critical exponent beta = {beta}.")
            print(f"This construction has a exponent difference of {beta - alpha}.")

        exponent_differences[c] = beta - alpha
    
    best = []
    for _ in range(n):
        construction = max(exponent_differences, key=exponent_differences.get)
        best.append(construction)
        exponent_differences.pop(construction)
    
    return best