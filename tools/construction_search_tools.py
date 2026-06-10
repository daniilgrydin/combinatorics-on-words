import tools.file_rw as rw

# q is the last q-uniform morphism to be built.
# nearly_extremal_file is a file of nearly extremal words. If it already exists and contains words, new ones will be appended.
# morphism_seed_files is a list of uniform morphism image files that we already have. If this is not provided, building
# will begin at 1.
def build_morphisms(q_to_build, preimage_words_file, preimage_alphabet, image_alphabet, beta, 
                    nearly_extremal_file, morphism_out_folder, morphism_seed_files = [],
                    seed_prefix = '', seed_suffix = '' ,
                    do_print = True, do_deep_print = False):
    
    # Initial loading
    morphisms = {0:[['']]}
    for file in morphism_seed_files:
        if do_print: print(f"Loading morphisms from {file}.")
        current = rw.load_images_of_morphisms(file) # [ [images], [images] ]
        morphisms[len(current[0][0])] = current.copy()
        current.clear()
    existing_q = max(morphisms.keys())

    nearly_extremal = []
    try:
        nearly_extremal = rw.load_words(nearly_extremal_file)
        if do_print: print(f"{len(nearly_extremal)} words loaded from {nearly_extremal_file}")
    except FileNotFoundError:
        nearly_extremal = [""]

    def get_prescribed_prefix_suffix(nearly_extremal, last_morphism):
        from combinatorics.word import get_common_prefix, get_common_suffix

        morphism_words = []
        for m in last_morphism:
            for img in m:
                morphism_words.append(img)

        common_prefix = get_common_prefix(morphism_words)
        common_suffix = get_common_suffix(morphism_words)

        prefixes = best_common_prefixes(len(common_prefix) + 1, words=nearly_extremal)
        suffixes = best_common_suffixes(len(common_suffix) + 1, words=nearly_extremal)

        return common_prefix if len(prefixes) == 0 else prefixes[0][0], common_suffix if len(suffixes) == 0 else suffixes[0][0]

    # Building
    for q in range(existing_q + 1, q_to_build + 1):
        if do_print: print(f"Currently building q = {q}...")
        last_morphism_key = max(morphisms.keys())
        prefix, suffix = get_prescribed_prefix_suffix(nearly_extremal, morphisms[last_morphism_key])
        if len(prefix) < len(seed_prefix):
            prefix = seed_prefix
        if len(suffix) < len(seed_suffix):
            suffix = seed_suffix
        if do_print: print(f"Prescribed prefix/suffix: {prefix}, {suffix}")

        nearly_extremal = generate_nearly_extremal(image_alphabet, q, beta, nearly_extremal_file,
                                prefix=prefix, suffix=suffix, do_print=do_deep_print)
        morphisms_dicts = find_morphisms(preimage_alphabet, preimage_words_file, nearly_extremal_file, beta, q, 
                      output=morphism_out_folder + f"/{q}-uniform_morphism.txt", STOP=10, do_print=do_deep_print,
                      filter=lambda w: w[:len(prefix)] == prefix and w[-len(suffix)] == suffix)
        
        q_morphisms = []
        for m in morphisms_dicts:
            q_morphisms.append(list(m.values()))
        if len(q_morphisms) > 0:
            morphisms[q] = q_morphisms

    if do_print: print("Done")
        

# alpha_a is the alphabet of words in words_file_a
# words_file_a should be the path to a file with alpha-free words over an n+1 size alphabet (eg. 7/5-free quaternary words)
# nearly_extremal_words_file_b should be the path to a file with nearly extremal beta-free words over an n size alphabet (eg. nearly extremal 7/4+ ternary words)
# beta is power of the desired words obtained from the morphism
# filter is a function of a word that can narrow down the number of combinations to check (eg. words beginning with 0102 and ending with 0212)
# output is a file to write the morphisms to
def find_morphisms(preimage_alphabet, preimage_words_file, nearly_extremal_words_file, beta, q,
                    output, filter = lambda w: True, STOP=-1, do_print = True):
    from math import comb
    from random import randrange
    from itertools import combinations

    words_a = []
    with open(preimage_words_file, "r") as f:
        for w in f.readlines():
            if len(w) > 1:
                words_a.append(w.strip())

    if do_print: print(f"Loaded {preimage_words_file}")

    nearly_extremal = []
    try:
        for w in rw.load_words(nearly_extremal_words_file):
            if len(w) == q:
                nearly_extremal.append(w)
        if do_print: print(f"Loaded {len(nearly_extremal)} from {nearly_extremal_words_file}")
    except FileNotFoundError:
        return []

    # # Create nearly_extremal_lengths. Each index holds words of the index's length.
    # nearly_extremal_lengths = []
    # for i in range(0, max_q+1):
    #     nearly_extremal_lengths.append([])
    # # Populate nearly_extremal_lengths
    # for n in nearly_extremal:
    #     nearly_extremal_lengths[len(n)].append(n)

    # Count the number of combinations
    if do_print: print(f"Total combinations to check: {comb(len(nearly_extremal), len(preimage_alphabet))}")

    def check_valid_morphism(tuple):
        from combinatorics.morphism import dict_to_morphism, is_synchronizing
        from combinatorics.exponent import is_exponent_free

        morphism_dict = {}
        for i in range(0, len(preimage_alphabet)):
            morphism_dict[preimage_alphabet[i]] = tuple[i]

        morphism = dict_to_morphism(morphism_dict)

        if not is_synchronizing(morphism, preimage_alphabet): 
            return False

        for w in words_a:
            if not is_exponent_free(morphism(w), beta): 
                return False

        return True
    
    morphisms = []
    candidate_combinations = [c for c in combinations(nearly_extremal, len(preimage_alphabet))]
    n = len(candidate_combinations)
    found = 0
    combo_count = 0
    for i in range(n):
        combo = candidate_combinations.pop(randrange(0, n - i))

        if combo_count % 25 == 0 and do_print:
            print("Checked",combo_count,"morphisms.")
        combo_count += 1

        if not check_valid_morphism(combo): continue
        if do_print: print("Found morphism!\a")
        result_morphism_dict = {}
        for i in range(0, len(preimage_alphabet)):
            if do_print: print(preimage_alphabet[i], combo[i])
            result_morphism_dict[preimage_alphabet[i]] = combo[i]
        morphisms.append(result_morphism_dict)
        if do_print: print()
        found += 1
        if found == STOP:
            break

    if len(morphisms) >= len(preimage_alphabet):
        rw.save_images_of_morphisms([m.values() for m in morphisms], output)
    
    return morphisms
    
# alphabet is what nearly extremal words will be made over
# max_length is the size [1,max_length] of nearly_extremal words to make
# file_path is the file that the nearly extremal words will be written to 
def generate_nearly_extremal(alphabet, max_length, beta, file_path = "",  prefix="", suffix="", do_print = True):
    from combinatorics.word import generate_greedy_words
    from combinatorics.exponent import is_suffix_exponent_free, is_exponent_free
    from combinatorics.extremal import is_nearly_extremal

    nearly_extremal = []

    try:
        nearly_extremal = rw.load_words(file_path)
        if do_print: print(f"{len(nearly_extremal)} words loaded from file.")
        if len(nearly_extremal) > 0:
            existing_length = len(nearly_extremal[-1])
        else:
            existing_length = 1
    except FileNotFoundError:
        existing_length = 1


    existing_length = max(existing_length - len(prefix) - len(suffix), 1)
    if do_print: print(f"Generating nearly extremal {beta}-free words over {alphabet}")

    words = generate_greedy_words(
        alphabet,
        existing_length,
        lambda word: is_suffix_exponent_free(word, beta)
    )


    for length in range(existing_length+1, max_length - len(prefix) - len(suffix) + 1):
        if do_print: print(f"Currently generating length: {length + len(prefix) + len(suffix)}...")

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
                    if do_print: print(f"{count} found...")
                    rw.save_words(nearly_extremal, file_path)
        
        rw.save_words(nearly_extremal, file_path)
    
    return nearly_extremal
            

# Finds morphisms with ideal bookends and returns the constructions of those morphisms and bookends.
# morphism_images_file is a string path to a file in standard morphism image structure.
# max_bookend_size is the largest bookends to looked for.
# min_A_size is the smallest A will be.
# B_seed_file is a file of all beta-free words. This is not necessary but greatly speeds up time searching for a suitable B. 
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
def best_common_prefixes(length, words = [], words_file = "", n = 1):
    from combinatorics.word import get_common_prefix

    words_to_search = []

    if len(words) > 0:
        words_to_search = words
    else: 
        try:
            words_to_search = rw.load_words(words_file)
        except FileNotFoundError:
            return [("", 0)]

    prefixes = {}

    # start = max(minimum_length, len(get_common_prefix(words_to_search)))
    # stop = len(max(words_to_search, key=len))
    # for i in range(start+1, stop+2):
    #     for w in words_to_search:
    #         prefixes[w[:i]] = prefixes.get(w[:i], 0) + 1

    for w in words_to_search:
        if len(w) >= length:
            prefixes[w[:length]] = prefixes.get(w[:length], 0) + 1
    
    best = []
    for _ in range(min(n, len(prefixes))):
        prefix = max(prefixes, key=prefixes.get)
        best.append((prefix, prefixes[prefix]))
        prefixes.pop(prefix)
    
    return best

def best_common_suffixes(length, words = [], words_file = "", n = 1):
    from combinatorics.word import get_common_suffix

    words_to_search = []

    if len(words) > 0:
        words_to_search = words
    else: 
        try:
            words_to_search = rw.load_words(words_file)
        except FileNotFoundError:
            return [("", 0)]
    
    suffixes = {}

    # start = max(minimum_length, len(get_common_suffix(words_to_search)))
    # stop = len(max(words_to_search, key=len))
    # for i in range(start, stop+1):
    #     for w in words_to_search:
    #         suffixes[w[-i:]] = suffixes.get(w[-i:], 0) + 1

    for w in words_to_search:
        if len(w) >= length:
            suffixes[w[-length:]] = suffixes.get(w[-length:], 0) + 1

    best = []
    for _ in range(min(n, len(suffixes))):
        suffix = max(suffixes, key=suffixes.get)
        best.append((suffix, suffixes[suffix]))
        suffixes.pop(suffix)
    
    return best

# Takes ideal constructions and takes the n best ones.
# Deep check prints more details about each construction. 
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
    for _ in range(min(n, len(exponent_differences))):
        construction = max(exponent_differences, key=exponent_differences.get)
        best.append(construction)
        exponent_differences.pop(construction)
    
    return best