import math

# Gets the complexity of factors of length m in the Thue-Morse word using 
# the recursive method (Proposition 2.10.)
def complexityTMRec(m):
    if m <= 0:
        return 1
    if m == 1:
        return 2
    if m == 2:
        return 4
    if m == 3:
        return 6 
    
    if m % 2 == 1:
        n = (m - 1) / 2
        return 2 * complexityTMRec(n + 1)
    else:
        n = m / 2
        return complexityTMRec(n + 1) + complexityTMRec(n)
    
# Gets the complexity of factors of length m in the Thue-Morse word using 
# the explciit formula (Proposition 2.14.)
def complexityTM(m):
    if m <= 0:
        return 1
    if m == 1:
        return 2
    if m == 2:
        return 4
    
    k = math.floor(math.log2(m))
    r = m - 2**k

    if r <= 2**(k-1):
        return 3*2**k + 4*(r-1)
    else:
        return 4*2**k + 2*(r-1)
    
# print(Words.complexity(tMorphism(1000),15))
# print(complexityTMRec(15))
# print(complexityTM(15))
 
#print(tDef(21))
# print(tAutomaton(14))
# print(tRecursive(14))
# print(tMorphism(14))

# m = 4 Tarry-Escott solution using Thue-Morse word
#
# a,b = teProuhet(4)
# print("List a", a)
# print("List b", b)
# print("Verify", teVerifier(a,b,4))

# Generalization of a decomposition into 3 sets
#
# a = [0,5,7,11,13,15,19,21,26]
# b = [1,3,8,9,14,16,20,22,24]
# c = [2,4,6,10,12,17,18,23,25]
# print("Verify a and b", teVerifier(a,b,2))
# print("Verify
#  a and c", teVerifier(a,c,2))
# print("Verify b and c", teVerifier(b,c,2))


