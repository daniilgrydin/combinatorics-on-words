from package.word import generate_greedy_words_unique
from package.exponent import is_suffix_exponent_free, ExtendedReal, is_exponent_free
from package.extremal import is_extremal, is_nearly_extremal
from package.square import is_square_free
from package.word import color_word

N = "abacbabcabacbcacbabcabacabcbabcabacbcabcb"
P = "abacbcabcbacabacbcabcbabcacbcabcbacabacbcabcbacbc"
Q = "abacbabcacbacabacbcacbacabcbabcabacbcabcb"
R = "abacabcacbacabcbabcacbacabacbcacbacabcbabcabacbcabcb"
S = "acabacbabcacbacabcbacbcabacbabcacbacabcbabcacbaca"

print("N", is_nearly_extremal(N, "abc", is_square_free))
print("P", is_nearly_extremal(P, "abc", is_square_free))
print("Q", is_nearly_extremal(Q, "abc", is_square_free))
print("R", is_nearly_extremal(R, "abc", is_square_free))
print("S", is_nearly_extremal(S, "abc", is_square_free))
