# Definition 1.3.1. of the Thue-Morse Word with n characters.
def thue_morse_definition(length):
    from libraries.word import sum_of_digits
    thue_morse = ""
    for i in range(length):
        binary = bin(i)[2:]
        s = sum_of_digits(binary)
        digit = s % 2
        thue_morse += str(digit)
    return thue_morse

# Theorem 1.8. Prouhet's solution to the Tarry-Escott problem. 
def teProuhet(m):
    a = []
    b = []
    t = thue_morse_definition(2**(m+1))
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

