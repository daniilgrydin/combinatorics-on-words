from combinatorics.word import generate_greedy_words_unique, save_words, get_words, get_permutations, append_words, backtrack
from combinatorics.exponent import is_suffix_exponent_free, ExtendedReal, is_exponent_free
from combinatorics.extremal import is_nearly_extremal, is_right_extremal, is_left_extremal
from combinatorics.alphabet import STANDARD_ALPHABET

# b=7/4, n=3, m=4, a=7/5, checked up to length 43 and nothing. 
def RT_plus(m):
    if m == 2: return ExtendedReal(2,1,True)
    if m == 3: return ExtendedReal(7,4,True)
    if m == 4: return ExtendedReal(7,5,True)
    return ExtendedReal(m, m-1, True)

def get_right_bookend(word, alphabet, exponent, MAX_ITERATIONS=-1):
    if MAX_ITERATIONS == -1:
        MAX_ITERATIONS = len(word)
    candidates = [""]
    for _ in range(MAX_ITERATIONS):
        candidates = generate_greedy_words_unique(
            alphabet,
            1,
            lambda w: is_suffix_exponent_free(w, exponent),
            seed = candidates
        )
        for c in candidates:
            if is_right_extremal(word + c, alphabet, lambda w: is_exponent_free(w, exponent)):
                return c
    raise RuntimeError("Could not find bookend")

def get_left_bookend(word, alphabet, exponent, MAX_ITERATIONS=-1):
    return get_right_bookend(word[::-1], alphabet, exponent, MAX_ITERATIONS)[::-1]

def get_all_right_bookends(word, alphabet, exponent, MAX_ITERATIONS=-1):
    if MAX_ITERATIONS == -1:
        MAX_ITERATIONS = len(word)
    candidates = [""]
    result = []
    for _ in range(MAX_ITERATIONS):
        candidates = generate_greedy_words_unique(
            alphabet,
            1,
            lambda w: is_suffix_exponent_free(w, exponent),
            seed = candidates
        )
        for c in candidates:
            if is_right_extremal(word + c, alphabet, lambda w: is_exponent_free(w, exponent)):
                result.append(c)
    return result

def get_all_left_bookends(word, alphabet, exponent, MAX_ITERATIONS=-1):
    if MAX_ITERATIONS == -1:
        MAX_ITERATIONS = len(word)
    candidates = [""]
    result = []
    for _ in range(MAX_ITERATIONS):
        candidates = generate_greedy_words_unique(
            alphabet,
            1,
            lambda w: is_suffix_exponent_free(w, exponent),
            seed = candidates
        )
        for c in candidates:
            if is_left_extremal(c + word, alphabet, lambda w: is_exponent_free(w, exponent)):
                result.append(c)
    return result

def iterate_exponent_free_words(*, words=[""], alphabet="01", exponent=ExtendedReal(2,1,True)):
    r"""
    Performs one iteration of `generate_greedy_words_unique`
    with filter set to lambda expression of `is_suffix_exponent_free`.
    """
    
    return generate_greedy_words_unique(
        alphabet,
        1,
        lambda w: is_suffix_exponent_free(w, exponent),
        seed = words
    )

def get_length_of_preimages(foreign_bound, upper_bound):
    r"""
    According to Lemma 23 in 
    """
    # print(foreign_bound, upper_bound)
    if not (1 < foreign_bound < upper_bound):
        raise ValueError("a must be greater than 1 and less than b")
    length_1 = 2 * upper_bound / (upper_bound - foreign_bound)
    length_2 = 2 * (2 * upper_bound - 1) / ( upper_bound - 1 )
    return int(max(length_1, length_2))   

def generate_exponent_free_words(exponent: ExtendedReal, alphabet_size: int, max_length:int):
    exponent = RT_plus(alphabet_size)
    alphabet = STANDARD_ALPHABET[:alphabet_size]
    metadata = {
        "exponent_free": exponent,
        "base": alphabet_size
    }
    all_unique = []
    all_words = []
    unique = []
    
    success, recorded_words, recorded_length = get_words(**metadata)
    if success:
        if recorded_length >= max_length:
            return [word for word in recorded_words if len(word) <= max_length]    
        else:
            all_words = recorded_words.copy()
            

    success, recorded_words, recorded_length = get_words("canonical",**metadata)
    if success:
        if recorded_length >= max_length:
            words = []
            for word in recorded_words:
                if len(word) > max_length:
                    return words
                words.extend(get_permutations(word, alphabet))
        else:
            all_unique = recorded_words.copy()
            unique = [word for word in recorded_words if len(word) == max_length]
    else:
        unique = [""]
    
    for length in range(recorded_length, max_length):
        unique = generate_greedy_words_unique(
            alphabet,
            1,
            lambda w: is_suffix_exponent_free(w, exponent),
            seed=unique
        )
        all_unique.extend(unique)
        for word in unique:
            for perm in get_permutations(word, alphabet):
                all_words.append(perm)
            
    
    save_words(all_words, **metadata)
    save_words(all_unique, "canonical", **metadata)
    return all_words
    
      
def extendERT(alphabet, known_lower_bound: ExtendedReal, MAX_ITERATIONS=1000, START_LENGTH=1):
    
    print(f"Starting extension of ERT({len(alphabet)}) with a known lower bound of {known_lower_bound}")
    print()
    
    
    
    preimage_alphabet_size = len(alphabet)+1
    preimage_exponent = RT_plus(preimage_alphabet_size)
    preimage_max_length = get_length_of_preimages(preimage_exponent, known_lower_bound)
    
    print(f"Generating ({preimage_exponent})-free pre-images over Sigma{preimage_alphabet_size} of size atmost {preimage_max_length}")
    preimages = generate_exponent_free_words(
        preimage_exponent,
        preimage_alphabet_size,
        get_length_of_preimages(preimage_exponent, known_lower_bound)
    )
    print(f"\tFound a total of {len(preimages)} preimages.")
    print()
    
    
    
    print("Generating images")
    images_meta = {
        "canonical": True,
        "base": len(alphabet),
        "exponent_free": known_lower_bound
    }
    success, recorded_words, recorded_length = get_words(**images_meta)
    
    if success and START_LENGTH > 0:
        unique_words = [word for word in recorded_words if len(word) == min(START_LENGTH, recorded_length)]
    else:
        unique_words = [""]
    
    for length in range(min(START_LENGTH, recorded_length), MAX_ITERATIONS):
        print(f"Checking length {length}")
        unique_words = iterate_exponent_free_words(
            words = unique_words,
            alphabet = alphabet,
            exponent = known_lower_bound
        )
        append_words(unique_words, **images_meta)
        print(f"\tFound {len(unique_words)} ({known_lower_bound})-free words.")
        nearly_extremal = [
            word for word in unique_words
            if is_nearly_extremal(
                word,
                alphabet,
                lambda w: is_exponent_free(
                    w,
                    known_lower_bound
                ))]
        append_words(unique_words, nearly_extremal=True, **images_meta)
        print(f"\tOut of them {len(nearly_extremal)} are nearly-extremal.")
        print(f"\t\tThere are {len(nearly_extremal)**preimage_alphabet_size} possible morphisms")
        
 
# print(save_words(
#     ["01", "10", "100000"],
#     "morphic",
#     length=(2,6),
#     nearly_extremal=True,
#     overlap_free = True,
#     exponent_free=ExtendedReal(2,1,True)
# ))

#extendERT("012", ExtendedReal(7,4,True))