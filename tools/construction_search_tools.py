import tools.file_rw as rw

# q is the last q-uniform morphism to be built.
# nearly_extremal_file is a file of nearly extremal words. If it already exists and contains words, new ones will be appended.
# morphism_seed_files is a list of uniform morphism image files that we already have. If this is not provided, building
# will begin at 1.
def build_morphisms(q_to_build, preimage_words_file, preimage_alphabet, image_alphabet, beta, 
                    critical_nearly_extremal_file, morphism_out_folder, morphism_seed_files = [],
                    seed_prefix = '', seed_suffix = '' , b_seed_file = "", morphisms_to_sample = 8,
                    morphisms_to_check = 1000, prefixes_suffixes_to_sample = 5, critical_seed_file = "",
                    prefix_suffix_coverage = 0.3, do_print = True, do_deep_print = False):
    from combinatorics.word import get_common_prefix, get_common_suffix
    from combinatorics.exponent import Rational
    
    # Initial loading
    morphisms = {0:[['']]}
    for file in morphism_seed_files:
        if do_print: print(f"Loading morphisms from {file}.")
        current = rw.load_images_of_morphisms(file) # [ [images], [images] ]
        morphisms[len(current[0][0])] = current.copy()
        current.clear()

    critical_nearly_extremal = []
    try:
        critical_nearly_extremal, none_sizes = rw.load_words(critical_nearly_extremal_file, get_none_sizes=True)
        if do_print: print(f"{len(critical_nearly_extremal)} nearly extremal words loaded from {critical_nearly_extremal_file}")
    except FileNotFoundError:
        critical_nearly_extremal = [""]

    existing_q = max([max(none_sizes) if len(none_sizes) > 0 else 0, 
                      len(max(critical_nearly_extremal, key=len)) if len(critical_nearly_extremal) > 0 else 0])


    def get_prescribed_prefixes_suffixes(previous_morphisms):
        from combinatorics.word import index_prefix_occurrences, index_suffix_occurrences, keys_from_max_values

        morphism_words = []
        for m in previous_morphisms:
            for img in m:
                morphism_words.append(img)

        common_prefix = get_common_prefix(morphism_words)
        common_suffix = get_common_suffix(morphism_words)

        prefixes_indexed = index_prefix_occurrences(len(common_prefix) + 1, words=morphism_words)
        prefixes = keys_from_max_values(prefixes_indexed, prefixes_suffixes_to_sample)
        count = 2

        while len(prefixes) >= prefixes_suffixes_to_sample and \
        sum([prefixes_indexed[p] for p in prefixes]) > prefix_suffix_coverage * len(morphism_words):
            prefixes_indexed = index_prefix_occurrences(len(common_prefix) + count, words=morphism_words)
            prefixes = keys_from_max_values(prefixes_indexed, prefixes_suffixes_to_sample)
            count += 1
        prefixes_indexed = index_prefix_occurrences(len(common_prefix) + count - 2, words=morphism_words)
        prefixes = keys_from_max_values(prefixes_indexed, prefixes_suffixes_to_sample)

        suffixes_indexed = index_suffix_occurrences(len(common_suffix) + 1, words=morphism_words)
        suffixes = keys_from_max_values(suffixes_indexed, prefixes_suffixes_to_sample)
        count = 2

        while len(suffixes) >= prefixes_suffixes_to_sample and \
        sum([suffixes_indexed[s] for s in suffixes]) > prefix_suffix_coverage * len(morphism_words):
            suffixes_indexed = index_suffix_occurrences(len(common_suffix) + count, words=morphism_words)
            suffixes = keys_from_max_values(suffixes_indexed, prefixes_suffixes_to_sample)
            count += 1
        suffixes_indexed = index_suffix_occurrences(len(common_suffix) + count - 2, words=morphism_words)
        suffixes = keys_from_max_values(suffixes_indexed, prefixes_suffixes_to_sample)
        
        return common_prefix if len(prefixes) == 0 else prefixes, common_suffix if len(suffixes) == 0 else suffixes

    # Building
    for q in range(existing_q + 1, q_to_build + 1):
        if do_print: print(f"Currently building q = {q}...")

        last_morphisms = []
        for m in morphisms.values():
            last_morphisms.extend(m)
        prefixes, suffixes = get_prescribed_prefixes_suffixes(last_morphisms)
        
        if len(prefixes) == 0 or len(max(prefixes, key=len)) < len(seed_prefix):
            prefixes = [seed_prefix]
        if len(suffixes) == 0 or len(max(suffixes, key=len)) < len(seed_suffix):
            suffixes = [seed_suffix]

        if do_print: 
            print(f"Prescribed prefixes: {prefixes}")
            print(f"Prescribed suffixes: {suffixes}")

        critical_exponent = Rational(beta.rational.numerator, beta.rational.denominator)
        critical_nearly_extremal = generate_critical_nearly_extremal(image_alphabet, q, beta, 
                                critical_exponent, critical_words_file=critical_seed_file,
                                beta_free_words = b_seed_file, output_path=critical_nearly_extremal_file,
                                prefixes=prefixes, suffixes=suffixes, 
                                do_print=do_deep_print)
        
        def morphism_filter(w):
            for p in prefixes:
                if w[:len(p)] != p:
                    return False
            for s in suffixes:
                if w[-len(s)] != s:
                    return False
            return True

        morphisms_dicts = find_morphisms(preimage_alphabet, preimage_words_file, critical_nearly_extremal_file, beta, q, 
                      output_file=morphism_out_folder + f"/{q}-uniform_morphism.txt", STOP=morphisms_to_sample, do_print=do_deep_print,
                      filter=morphism_filter)
        
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
def find_morphisms(preimage_alphabet, beta, q,
                    output_file, nearly_extremal_words = [], nearly_extremal_words_file = "", 
                    preimages = [], preimage_words_file = "", 
                    to_check=-1, STOP=-1, do_print = True):
    from math import comb
    from random import randrange
    from itertools import combinations

    if do_print: print(f"Loaded preimages from {preimage_words_file}")

    if len(nearly_extremal_words_file) > 0:
        nearly_extremal_words = rw.load_words_by_length(nearly_extremal_words_file)[q]
    elif len(nearly_extremal_words) == 0:
        if do_print: print("No nearly extremal words were given.")
        return []
    
    if len(preimage_words_file) > 0:
        preimages = rw.load_words(preimage_words_file)
    elif len(preimages) == 0:
        if do_print: print("No preimages given.")
        return []

    if do_print: print(f"Loaded {len(nearly_extremal_words)} nearly extremal from {nearly_extremal_words_file}.")

    # Count the number of combinations
    if do_print: print(f"Total combinations to check: {comb(len(nearly_extremal_words), len(preimage_alphabet))}")

    def check_valid_morphism(tuple):
        from combinatorics.morphism import dict_to_morphism, is_synchronizing
        from combinatorics.exponent import is_exponent_free

        morphism_dict = {}
        for i in range(0, len(preimage_alphabet)):
            morphism_dict[preimage_alphabet[i]] = tuple[i]

        morphism = dict_to_morphism(morphism_dict)

        if not is_synchronizing(morphism, preimage_alphabet): 
            return False

        for w in preimages:
            if not is_exponent_free(morphism(w), beta): 
                return False

        return True
    
    try:
        morphisms = rw.load_images_of_morphisms(output_file)
    except FileNotFoundError:
        morphisms = []

    candidate_combinations = [c for c in combinations(nearly_extremal_words, len(preimage_alphabet))]
    n = len(candidate_combinations)
    found = 0
    combo_count = 0
    for i in range(n):
        combo = candidate_combinations.pop(randrange(0, n - i))

        if combo_count % 25 == 0 and do_print:
            print("Checked",combo_count,"morphisms.")
        combo_count += 1

        if to_check != -1 and combo_count >= to_check:
            if len(morphisms) > 0:
                rw.save_images_of_morphisms(morphisms, output_file)
            return morphisms

        if not check_valid_morphism(combo): continue
        if do_print: print("\nFound morphism!\a")
        result_morphism_dict = {}
        for i in range(0, len(preimage_alphabet)):
            if do_print: print(preimage_alphabet[i], combo[i])
            result_morphism_dict[preimage_alphabet[i]] = combo[i]
        morphisms.append(result_morphism_dict.values())
        if do_print: print()
        found += 1
        if found == STOP:
            break

    if len(morphisms) > 0:
        rw.save_images_of_morphisms(morphisms, output_file)
    return morphisms
    
# alphabet is what nearly extremal words will be made over
# max_length is the size [1,max_length] of nearly_extremal words to make
# file_path is the file that the nearly extremal words will be written to 
def generate_nearly_extremal(alphabet, max_length, beta, file_path = "",  
                             prefix="", suffix="", b_seed_file = "", do_print = True):
    from combinatorics.word import generate_greedy_words
    from combinatorics.exponent import is_suffix_exponent_free, is_exponent_free, Rational, get_critical_exponent
    from combinatorics.extremal import is_nearly_extremal

    nearly_extremal = []

    try:
        nearly_extremal, none_sizes = rw.load_words(file_path, get_none_sizes=True)
        if do_print: print(f"{len(nearly_extremal)} words loaded from file.")
        if len(nearly_extremal) > 0:
            existing_length = len(nearly_extremal[-1])
        else:
            existing_length = 1
    except FileNotFoundError:
        existing_length = 1


    existing_length = max(max(existing_length, 
                            max(none_sizes) if len(none_sizes) > 0 else 0) - len(prefix) - len(suffix),
                            1)

    if do_print: print(f"Generating nearly extremal {beta}-free words over {alphabet}")

    if len(b_seed_file) > 0:
        words_by_length = rw.load_words_by_length(b_seed_file)
        words = words_by_length[existing_length]
    else:
        words = generate_greedy_words(
            alphabet,
            existing_length,
            lambda word: is_suffix_exponent_free(word, beta)
        )

    for length in range(existing_length+1, max_length - len(prefix) - len(suffix) + 1):
        if do_print: print(f"Currently generating length: {length + len(prefix) + len(suffix)}...")

        if len(b_seed_file) > 0:
            words = words_by_length[length]
        else:
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
    
        if count == 0:
            rw.append_none_flag(file_path, length + len(prefix) + len(suffix))

    return nearly_extremal
            

# Finds morphisms with ideal bookends and returns the constructions of those morphisms and bookends.
# morphism_images_file is a string path to a file in standard morphism image structure.
# max_bookend_size is the largest bookends to looked for.
# min_A_size is the smallest A will be.
# B_seed_file is a file of all beta-free words. This is not necessary but greatly speeds up time searching for a suitable B. 
def find_ideal_constructions(morphisms = [], morphism_images_file="",
                         max_bookend_size = -1, get_exponents = False,
                         beta_free_words_file = None, do_print = True, output_file = None,
                         timeout_length = -1):
    from tools.decomposition import get_bookends_from_morphism, TernaryConstructionDecomposition
    from bookends import is_left_bookend_ideal, is_right_bookend_ideal
    from tools.file_rw import load_words_by_length
    from typing import List

    if len(morphism_images_file) > 0:
        morphisms = rw.load_images_of_morphisms(morphism_images_file)
    elif len(morphisms) == 0:
        if do_print: print("No morphisms given.")
        return []

    if do_print:
        print("Finding ideal constructions.")
        print(len(morphisms), "morphisms loaded.")

    if beta_free_words_file != None:
        B_seed = load_words_by_length(beta_free_words_file)
        if do_print: 
            print("Words loaded from B seed file.")
    else:
        B_seed = None
        if do_print: 
            print("No B seed file.")

    count = 0

    try:
        result_constructions : List[TernaryConstructionDecomposition] = rw.load_constructions(output_file)
    except FileNotFoundError:
        result_constructions : List[TernaryConstructionDecomposition] = []

    for m in morphisms:
        if do_print:
            print(f"\n{count} morphisms processed...")

        count += 1
        bookends_result = get_bookends_from_morphism(m, "012", max_bookend_size, B_seed, timeout_length)
        if bookends_result == None:
            continue

        if do_print:
            print("Bookends found for", m)

        r = bookends_result[0]
        s = bookends_result[1]

        if is_left_bookend_ideal(m, r) and is_right_bookend_ideal(m, s):
            if do_print:
                print("Found ideal bookends for", m)
                print("r:",r)
                print("s:",s)
            current_construction = TernaryConstructionDecomposition(m, r = r, s = s)
            if get_exponents:
                current_construction.get_alpha()
                current_construction.get_beta()
            result_constructions.append(current_construction)
            if len(output_file) > 0:
                rw.save_constructions(result_constructions, output_file)

    if len(output_file) > 0 and len(result_constructions) > 0:
        rw.save_constructions(result_constructions, output_file)

    return result_constructions

# Takes ideal constructions and takes the n best ones.
# Deep check prints more details about each construction. 
def find_best_constructions(constructions_file, n=1, output_file="", deep_check = True, do_print = True):
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
    
    if len(output_file) > 0:
        try:
            rw.save_constructions(best, output_file)
        except FileNotFoundError:
            print(f"{output_file} not found, so constructions were not written.")
    
    return best

# Finds nearly extremal words using words with a specified critical exponent to build them.
# Inside length is the length of words to be used from the beta free words.
# Beta is the power that the words should be nearly extremal of
# Critical exponent is the exponent of the critical words
# Critical seed file contains words with the given critical exponent
# b seed file are beta-free words for padding
# Prefixes/suffixes are lists containing desired prefixes and suffixes
def generate_critical_nearly_extremal(alphabet, inside_length, beta, beta_free_words_file,
                                    critical_words = [], critical_words_file = "", 
                                    output_path = "", prefixes=[], suffixes=[], do_print = True):
    from combinatorics.extremal import is_nearly_extremal
    from combinatorics.exponent import is_exponent_free, get_critical_exponent
        
    if len(critical_words_file) > 0:
        critical_words = rw.load_words(critical_words_file)
    elif len(critical_words) == 0:
        if do_print: print("No critical words were given.")
        return []
    
    crit = get_critical_exponent(critical_words[0])

    if do_print: print("Generating nearly extremal", beta, "-free words with inside length", inside_length, 
                    "and critical exponent", crit)

    beta_free_words_by_length = rw.load_words_by_length(beta_free_words_file)

    try:
        result = rw.load_words(output_path)
    except FileNotFoundError:
        result = []

    count = 0
    # They call this the most for loops ever seen in a program
    for seed in critical_words: 
        for prefix in prefixes:
            for suffix in suffixes:
                for inside in beta_free_words_by_length[inside_length]:
                    for insert in range(0, len(inside) + 1):
                        candidate = prefix + inside[:insert] + seed + inside[insert:] + suffix
                        if is_nearly_extremal(candidate, alphabet, lambda w: is_exponent_free(w, beta)):
                            result.append(candidate)
                            if do_print: 
                                print("\nNearly extremal:", candidate)
                                print("Prefix:", prefix)
                                print("Suffix:", suffix)
                                print("Inside:", inside)
                                print("Critical:", seed)
                            count += 1
                            if count % 10 == 0:
                                if do_print: print(count, "found...")
                                if len(output_path) > 0:
                                    rw.save_words(result, output_path)
    if len(output_path) > 0:
        rw.save_words(result, output_path)
        if len(result) == 0:
            rw.append_none_flag(output_path, inside_length)
    return result