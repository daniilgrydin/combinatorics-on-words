from combinatorics.morphism import dict_to_morphism
from combinatorics.exponent import ExtendedReal, is_exponent_free, get_critical_exponent, Rational
from combinatorics.extremal import is_nearly_extremal
from combinatorics.word import get_extensions

alpha = ExtendedReal(7,5,False)
beta = ExtendedReal(7,4,True)

morphism = {'0':'01020120210121020120212010201210120102120210201210212',
            '1':'01020120210121020120212010210121020102120210201210212',
            '2':'01020120210201210120212012102010210120210201210120212',
            '3':'01021012021020102120121020120210201021012010201210212'}

morphism_function = dict_to_morphism(morphism)

for w in morphism.values():
    print(f"{w} is {beta}-free: {is_exponent_free(w, beta)}")
    print(f"{w} is nearly extremal: {is_nearly_extremal(w, "012", lambda w: is_exponent_free(w, beta))}")

smallest_crit = Rational(100,1)
for w in morphism.values():
    for e in get_extensions(w, positions=range(1,len(w))):
        if get_critical_exponent(e).is_less_than(smallest_crit):
            smallest_crit = get_critical_exponent(e)
print("\nc:",smallest_crit)

print("")

for w in morphism.values():
    extensions = get_extensions(w, "012", positions=range(1,len(w)))
    for e in extensions:
        if is_exponent_free(e, beta):
            print(f"----- Internal extension {e} of {w} is {beta}-free -----")

print("")
quaternary = []
for line in open("data/75_free_quaternary_words.txt").readlines():
    quaternary.append(line.strip())

for q in quaternary:
    if not is_exponent_free(morphism_function(q), beta): 
        print(f"----- Morphism maps {q} to {morphism_function(q)} which is not {beta}-free -----")

print("Done")