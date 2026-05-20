import math

# Definition 1.3.1. of the Thue-Morse Word with n characters.
def tDef(n):
    t = ""
    for i in range(0,n):
        t = t + str(d2(i) % 2)
    return t

# d2 function that adds all 1s in the binary representation of n.
def d2(n):
    result = 0
    b = format(n, 'b')
    for i in range(0, len(b)):
        if b[i] == '1':
            result += 1
    return result

# Alternate definition 1 for t using a DFAO
def tAutomaton(n):
    t = ""
    for i in range(0, n):
        b = format(i, 'b')
        state = False
        for j in range(0, len(b)):
            if b[j] == '1':
                state = not state
        t += '1' if state else '0'
    return t

# Alternative definition 2 for t using recursion
def tRecursive(n):
    tList = [None] * n
    tList[0] = '0'
    for i in range(0,n//2):
        tList[2*i] = tList[i]
        tList[2*i + 1] = '0' if tList[i] == '1' else '1' 

    if n % 2 == 1:
        tList[n-1] = tList[n//2]

    t = ""
    for i in range(0,n):
        t += tList[i]

    return t

# Alternate definition 3 useing the Thue-Morse morphism. 
def tMorphism(n):
    m = math.ceil(math.log2(n))
    t = "0"
    for i in range(0,m):
        t = muMorphism(t)
    return t[:n]

# The Thue-Morse morphism function.
def muMorphism(w):
    result = ""
    for i in range(0, len(w)):
        if w[i] == '0':
            result += '01'
        else:
            result += '10'
    return result

# Theorem 1.8. Prouhet's solution to the Tarry-Escott problem. 
def teProuhet(m):
    a = []
    b = []
    t = tDef(2**(m+1))
    for i in range(0,2**(m+1)):
        if t[i] == '0':
            a.append(i)
        else:
            b.append(i)
    return a,b

# Verifies Tarry-Escott Problems with sequences a, b, and degree m.
def teVerifier(a, b, m):
    for i in range(1,m+1):
        sumA = 0
        sumB = 0
        for j in range(0,len(a)):
            sumA = sumA + a[j]**i
        for j in range(0,len(b)):
            sumB = sumB + b[j]**i
        if sumA != sumB:
            return False
    return True

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