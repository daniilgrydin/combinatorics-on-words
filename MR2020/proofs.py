from ..package.square import is_language_square_free, has_square_suffix, is_square_free
from ..package.word import generate_greedy_words, get_factors
import itertools as iter

def generate_square_free_words(length, alphabet_size):
    return generate_greedy_words(
        "".join([str(i) for i in range(alphabet_size)]),
        length,
        lambda w: not has_square_suffix(w)
    )

def verify_theorem_1_1():
    A_finite = [25,41,48,50,63,71,72,77,79,81,83,84,85]
    for i in range(1,87):
        if i not in A_finite:
            print("Looking for square-free ")
            is_language_square_free(generate_square_free_words(i,3))
    print("Done")

def verify_theorem_2_3(A, substitution):
    # (I)
    V = generate_square_free_words(3, len(A))
    for v in V:
        if not is_square_free(substitution(v)):
            print("(I) Fails: The image of v=",v,"is not square-free.")
            return False
    #return True

    # (II)
    letter_3_permutations = []
    for p in iter.permutations(A,3):
        letter_3_permutations.append(p)
    # (i)
    for p in letter_3_permutations:
        if p[0] in get_factors(p[1]): 
            print("(I)(i) Fails:", p[0], "is a factor of", p[1])
            return False
        
    return True