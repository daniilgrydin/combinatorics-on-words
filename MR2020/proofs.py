from libraries.square import *
from libraries.word import *
import itertools as iter

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
        if p[0] in factors(p[1]): 
            print("(I)(i) Fails:", p[0], "is a factor of", p[1])
            return False
        
    return True