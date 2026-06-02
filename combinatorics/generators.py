# alpha_a is the alphabet of words in words_file_a
# alpha b is the alphabet of the words in words_file_b
# words_file_a should be the path to a file with alpha-free words over an n+1 size alphabet (eg. 7/5-free quaternary words)
# nearly_extremal_words_file_b should be the path to a file with nearly extremal beta-free words over an n size alphabet (eg. nearly extremal 7/4+ ternary words)
# beta is power of the desired words obtained from the morphism
# min_q is the minimum uniform of the morphism desired
# max_q is the maximum uniform of the morphism desired (should not be greater than the len of words in words_file_b)
# filter is a function of a word that can narrow down the number of combinations to check (eg. words beginning with 0102 and ending with 0212)
# output is a file to write the morphisms to
def find_morphism(alpha_a, alpha_b, words_file_a, nearly_extremal_words_file_b, beta, min_q, max_q, filter, output, STOP=-1):
    from math import comb
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
        if filter(candidate) and len(candidate) <= max_q:
            nearly_extremal.append(line.strip())
    print(f"Loaded {len(nearly_extremal)} from {nearly_extremal_words_file_b}")

    # Create nearly_extremal_lengths. Each index holds words of the index's length.
    nearly_extremal_lengths = []
    for i in range(0, max_q+1):
        nearly_extremal_lengths.append([])
    # Populate nearly_extremal_lengths
    for n in nearly_extremal:
        nearly_extremal_lengths[len(n)].append(n)

    # Count the number of combinations
    total_combinations_to_check = 0
    for n in nearly_extremal_lengths:
        total_combinations_to_check += comb(len(n), len(alpha_a))
    print(f"Total combinations to check: {total_combinations_to_check}")

    def check_valid_morphism(tuple):
        from .morphism import dict_to_morphism, is_synchronizing
        from .exponent import is_exponent_free

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
    
    morphisms = []
    found = 0

    for i in range(min_q, max_q+1):
        if found == STOP:
            break
        print("checking q =",i)
        for combo in combinations(nearly_extremal_lengths[i], len(alpha_a)):
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

    out_file = open(output, 'w')
    for m in morphisms:
        out_file.write("\n-")
        for v in m.values():
            out_file.write("\n" + str(v))
        out_file.write("\n-")
    out_file .close()
    
    print("Done")

# alphabet is what nearly extremal words will be made over
# max_length is the size [1,max_length] of nearly_extremal words to make
# file_path is the file that the nearly extremal words will be written to 
def generate_nearly_extremal(alphabet, max_length, beta, file_path):
    from .word import generate_greedy_words_unique
    from .exponent import is_suffix_exponent_free, is_exponent_free
    from .extremal import is_nearly_extremal

    print(f"Generating nearly extremal {beta}-free words over {alphabet}")

    unique = generate_greedy_words_unique(
        alphabet,
        1,
        lambda word: is_suffix_exponent_free(word, beta)
    )

    nearly_extremal = []

    for length in range(2,max_length):
        print(f"Currently generating length: {length}...")

        unique = generate_greedy_words_unique(
            alphabet,
            1,
            lambda word: is_suffix_exponent_free(word, beta),
            seed = unique
        )

        new_nearly_extremal = [
            word
            for word in unique
            if is_nearly_extremal(
                word,
                alphabet,
                lambda w: is_exponent_free(w, beta))]
        
        nearly_extremal.extend(new_nearly_extremal)
        
        with open(file_path, "w") as f:
            f.write("\n".join(nearly_extremal))

    print("Done")