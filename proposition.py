# Proposition: There are arbitrarily long (7/4+, 23/13)-extremal ternary words.
from combinatorics.morphism import dict_to_morphism, is_synchronizing
from combinatorics.word import get_extensions, backtrack, period, index_all_occurrences
from combinatorics.exponent import get_critical_exponent, ExtendedReal, Rational, is_suffix_exponent_free, is_exponent_free

def check_proposition(morphism_dict, r, s, to_alphabet, from_alphabet, alpha, beta, gamma):
    q = len(list(morphism_dict.values())[0])
    morphism = dict_to_morphism(morphism_dict)

    internal_extensions_check(morphism, from_alphabet, gamma, q)
    left_and_internal_extensions_check(morphism, from_alphabet, gamma, q, r)
    right_and_internal_extensions_check(morphism, from_alphabet, gamma, q, s)
    is_synchronizing_check(morphism, from_alphabet)
    #lemma_23_check(morphism, alpha, beta, q, from_alphabet)

    r_prime = get_r_prime(morphism_dict, r)
    s_prime = get_s_prime(morphism_dict, s)
    tr = r[-len(r_prime)-1] + r_prime
    ts = s_prime + s[len(s_prime)]

    print(f"r' = {r_prime} tr = {tr}")
    print(f"s' = {s_prime} ts = {ts}")

    check_tr_occurrences(morphism, from_alphabet, tr, alpha)
    check_for_all_preimages(morphism, 3, from_alphabet, alpha, beta, r, s)

    #z_check(morphism, from_alphabet, r, s, beta, max_z_size)

    print("Done!")


# Every internal extension of f(c) has a factor of exponent >= 17/7
def internal_extensions_check(f, from_alphabet, gamma, q):
    for c in from_alphabet:
        for e in get_extensions(f(c), positions=range(1,q)):
            if is_exponent_free(e, gamma):
                print(f"f({c}) has an extension with no exponent greater than {gamma}.")
                return False
    print(f"Every internal extension of f(c) has a factor of exponent >= {gamma}.")
    return True

# Every left and internal extension of rf(c) has a factor of exponent >= 17/7
def left_and_internal_extensions_check(f, from_alphabet, gamma, q, r):
    for c in from_alphabet:
        for e in get_extensions(r + f(c), positions=range(0,q+len(r))):
            if is_exponent_free(e, gamma):
                print(f"rf({c}) has an extension with no exponent greater than {gamma}.")
                print(e)
                return False
    print(f"Every left and internal extension of rf(c) has a factor of exponent >= {gamma}.")
    return True

# Every right and internal extension of f(c)s has a factor of exponent >= 17/7
def right_and_internal_extensions_check(f, from_alphabet, gamma, q, s):
    for c in from_alphabet:
        for e in get_extensions(f(c) + s, positions=range(1,q+len(s)+1)):
            if is_exponent_free(e, gamma):
                print(f"f({c})s has an extension with no exponent greater than {gamma}.")
                return False
    print(f"Every right and internal extension of f(c)s has a factor of exponent >= {gamma}.")
    return True

# f should be synchronizing.
def is_synchronizing_check(f, from_alphabet):
    if is_synchronizing(f, from_alphabet):
        print("f is synchronizing.")
        return True
    else:
        print("f is not synchronizing.")
        return False
    
# Checks lemma 23.
def lemma_23_check(f, alpha, beta, q, from_alphabet):
    a = alpha.rational.numerator / alpha.rational.denominator
    b = beta.rational.numerator / beta.rational.denominator
    max_size = round(max(
        (2 * b) / (b - a),
        (2 * (q - 1) * (2 * b - 1)) / (q * (b - 1))
        ))
    
    X = []
    for i in range(0, max_size + 1):
        X = backtrack(from_alphabet, i, lambda w: is_suffix_exponent_free(w, alpha))
        for x in X:
            if not is_exponent_free(f(x), beta):
                print(f"f({x}) is not {beta}-free.")
                return False
            
    print(f"For all {alpha}-free words in {from_alphabet}, f(x) is {beta}-free.")
    return True

def get_r_prime(morphism_dict, r):
    result = ""
    for i in range(1, len(r)+1):
        for image in list(morphism_dict.values()):
            if image[-i] != r[-i]:
                return result[::-1]
        result += r[-i]
     
def get_s_prime(morphism_dict, s):
    result = ""
    for i in range(0, len(s)):
        for image in list(morphism_dict.values()):
            if image[i] != s[i]:
                return result
        result += s[i]

def check_tr_occurrences(f, from_alphabet, tr, alpha):
    preimages = backtrack(from_alphabet, 2, lambda w: is_suffix_exponent_free(w, alpha))
    q = len(f(from_alphabet[0]))
    for p in preimages:
        indices = index_all_occurrences(f(p), tr)
        for i in indices:
            if i % q != q - len(tr):
                print(f"tr found at {i} in f({p}).")
                return False
    
    print("tr occurs as it should for preimages of length 2.")
    return True

def check_for_all_preimages(f, size_to_check_to, from_alphabet, alpha, beta, r, s):
    for i in range(1,size_to_check_to + 1):
        to_check = backtrack(from_alphabet, i, lambda w: is_suffix_exponent_free(w, alpha))
        for w in to_check:
            if not is_exponent_free(r + f(w), beta):
                print(f"rf({w}) is not {beta}-free.")
                return False
            if not is_exponent_free(f(w) + s, beta):
                print(f"rf({w}) is not {beta}-free.")
                return False
    print(f"f maps all {alpha}-free words to {beta}-free words up to size {size_to_check_to}.")
    return True

    # for c in "0123":
    #     to_check.append(r+morphism(c))
    #     to_check.append(morphism(c)+s)

    # rp = '0120210201210212'

    # for i in to_check:
    #     print("\nChecking",i)
    #     found = []
    #     check = 0
    #     while i.find(rp, check) != -1:
    #         found.append(i.find(rp, check))
    #         check += i.find(rp, check) + len(rp)

    #     print("Found rp at",found)

# # For every c in "0123", tr occurs exactly once in rf(c) and does not occur in f(c)s and analogously for tl.
# def check_tr_occurrences(f, from_alphabet, r, tr, s):
#     for c in from_alphabet:
#         rfc = r + f(c)
#         fcs = f(c) + s
#         if str(rfc).find(tr) != str(rfc).rfind(tr) or str(rfc) == -1:
#             print(f"tr does not occur exactly once in rf({c}).")
#             return False
#         if str(fcs).find(tr) != -1:
#             print(f"tr occurs in f({c})s.")
#             return False

#     print("tr occurs exactly as it should.")
#     return True

# def check_ts_occurrences(f, from_alphabet, s, ts, r):
#     for c in from_alphabet:
#         rfc = r + f(c)
#         fcs = f(c) + s
#         # ts
#         if str(fcs).find(ts) != str(fcs).rfind(ts) or str(fcs) == -1:
#             print(f"ts does not occur exactly once in f({c})s.")
#             return False
#         if str(rfc).find(ts) != -1:
#             print(f"ts occurs in rf({c}).")
#             return False
        
#     print("ts occurs exactly as it should.")
#     return True

# def check_tr_ts_occurrences_fy(f, from_alphabet, alpha, tr, ts):
#     Y = backtrack(from_alphabet, 2, lambda w: is_suffix_exponent_free(w, alpha))
#     for y in Y:
#         if f(y).find(tr) != -1:
#             print(f"tr occurs in f({y})")
#             return False
#         if f(y).find(ts) != -1:
#             print(f"ts occurs in f({y})")
#             return False
#     print(f"tr and ts occur exactly as they should in {alpha}-free words over {from_alphabet} of length 2.")
#     return True

def z_check(f, from_alphabet, r, s, beta, z_size):
    for i in range(1,z_size+1):
        for j in range(0,len(r)):
            for c in from_alphabet:
                if not is_exponent_free((r+f(c))[j:j+i], beta):
                    print("w contains z.")
                    return False
                
    for i in range(1,z_size+1):
        for j in range(1,len(s)+1):
            for c in from_alphabet:
                if not is_exponent_free((f(c)+s)[-j:-(j+i)], beta):
                    print("w contains z.")
                    return False
    
    print("w does not contain z.")
    return True



# check_proposition({
#     '0':'01021012021020102101210212010201210120102120210201210212',
#     '1':'01021012021020102120121012021201021012102120210201210212',
#     '2':'01021012021020102120121020120212010201210120210201210212',
#     '3':'01021012021020102120210121020102101201020120210201210212'
#     },
#     '010210120210201210212',
#     '01210120102120121',
#     '012',
#     '0123',
#     ExtendedReal(7,5,True),
#     ExtendedReal(7,4,True),
#     ExtendedReal(37,21,False),
#     '0120210201210212',
#     '20212012')

check_proposition({
    '0':'01021012021020102101210212010210120212010201210120210201210212',
    '1':'01021012021020102120121012021201020120210120102120210201210212',
    '2':'01021012021020102120121020120212010201210120102120210201210212',
    '3':'01021012021020102120210121021201021012021201020120210201210212'
    },
    '010210120210201210212',
    '01210120102120121',
    '012',
    '0123',
    ExtendedReal(7,5,True),
    ExtendedReal(7,4,True),
    ExtendedReal(37,21,False))

# check_proposition({
#     '0':'0011011001001100101100110110010011',
#     '1':'0011011001001101100110100110010011',
#     '2':'0011011001101001100100110110010011'
#     },
#     '01101100110110011001010011',
#     '00110101100110010011001001',
#     '01',
#     '012',
#     ExtendedReal(2,1,False),
#     ExtendedReal(18,7,True),
#     ExtendedReal(8,3,False))