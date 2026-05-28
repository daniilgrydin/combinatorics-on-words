# Proposition: There are arbitrarily long (7/4+, 23/13)-extremal ternary words.
from combinatorics.morphism import dict_to_morphism, is_synchronizing
from combinatorics.word import get_extensions, backtrack
from combinatorics.exponent import get_critical_exponent, ExtendedReal, is_suffix_exponent_free, is_exponent_free

def check_proposition(morphism_dict, r, s, to_alphabet, from_alphabet, alpha, beta, gamma):
    r_prime = get_r_prime(morphism_dict, r)
    s_prime = get_s_prime(morphism_dict, s)
    tr = get_tr()
    ts = get_ts()
    q = len(morphism_dict[0])
    morphism = dict_to_morphism(morphism_dict)

    internal_extensions_check(morphism, from_alphabet, gamma, q)
    left_and_internal_extensions_check(morphism, from_alphabet, gamma, q, r)
    right_and_internal_extensions_check(morphism, from_alphabet, gamma, q, s)
    is_synchronizing_check(morphism, from_alphabet)
    lemma_23_check(morphism, alpha, beta, q, from_alphabet)
    check_tr_ts_occurrences(morphism, from_alphabet, tr, ts)
    check_tr_ts_occurrences_fy(morphism, alpha, ts, tr)


# Every internal extension of f(c) has a factor of exponent >= 17/7
def internal_extensions_check(f, from_alphabet, gamma, q):
    for c in from_alphabet:
        for e in get_extensions(f(c), positions=range(1,q)):
            if get_critical_exponent(e) < gamma:
                print(f"f({c}) has an exponent less than {gamma}.")
                return False
    print(f"Every internal extension of f(c) has a factor of exponent >= {gamma}.")
    return True

# Every left and internal extension of rf(c) has a factor of exponent >= 17/7
def left_and_internal_extensions_check(f, from_alphabet, gamma, q, r):
    for c in from_alphabet:
        for e in get_extensions(r + f(c), positions=range(0,q+len(r))):
            if get_critical_exponent(e) < gamma:
                print(f"rf({c}) has an exponent less than {gamma}.")
                return False
    print(f"Every left and internal extension of rf(c) has a factor of exponent >= {gamma}.")
    return True

# Every right and internal extension of f(c)s has a factor of exponent >= 17/7
def right_and_internal_extensions_check(f, from_alphabet, gamma, q, s):
    for c in from_alphabet:
        for e in get_extensions(f(c) + s, positions=range(1,q+len(s)+1)):
            if get_critical_exponent(e) < gamma:
                print(f"f({c})s has an exponent less than {gamma}.")
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

def get_r_prime():
    r_prime = ""
     

def get_s_prime():
    pass

def get_tr():
    pass

def get_ts():
    pass

# For every c in "0123", tr occurs exactly once in rf(c) and does not occur in f(c)s and analogously for tl.
def check_tr_ts_occurrences(f, from_alphabet, tr, ts):
    for c in from_alphabet:
        rfc = r[c] + f(c)
        fcs = f(c) + s[c]
        # tr first
        if str(rfc).find(tr) != str(rfc).rfind(tr) or str(rfc) != -1:
            print(f"tr does not occur exactly once in rf({c}).")
            return False
        if str(fcs).find(tr) != -1:
            print(f"tr occurs in f({c})s.")
            return False
        # ts
        if str(fcs).find(ts) != str(fcs).rfind(ts) or str(fcs) != -1:
            print(f"ts does not occur exactly once in f({c})s.")
            return False
        if str(rfc).find(ts) != -1:
            print(f"ts occurs in rf({c}).")
            return False
    print("tr and ts occur exactly as they should.")
    return True

def check_tr_ts_occurrences_fy(from_alphabet, alpha, tr, ts):
    Y = backtrack(from_alphabet, 2, lambda w: is_suffix_exponent_free(w, alpha))
    for y in Y:
        if str(f(y)).find(tr) == -1:
            print(f"tr occurs in f({y})")
            return False
        if str(f(y)).find(ts) == -1:
            print(f"ts occurs in f({y})")
            return False
    print(f"tr and ts occur exactly as they should in {alpha}-free words over {from_alphabet} of length 2.")
    return True

check_proposition({
    '0':'01020120210121020120212010201210120102120210201210212',
    '1':'01020120210121020120212010210121020102120210201210212',
    '2':'01020120210201210120212012102010210120210201210120212',
    '3':'01021012021020102120121020120210201021012010201210212'
    },
    '',
    '',
    '012',
    '0123',
    ExtendedReal(7,5,True),
    ExtendedReal(7,4,True),
    ExtendedReal(23,13,False))