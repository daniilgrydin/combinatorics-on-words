characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
                  'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
                  'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 
                  'u', 'v', 'w', 'x', 'y', 'z']

# Get an alphabet based on the characters used in a word.
def getAlphabet(w):
    A = []
    for i in range(0, len(w)):
        if not w[i] in A:
            A.append(w[i])
    return A

# Given a word and a dictionary describing a cycle of characters, cycle the characters of the word.
def cycleCharacters(w, cycle: dict):
    result = ""
    for a in w:
        if a in cycle:
            result += cycle[a]
        else:
            result += a
    return result

# Returns a list of all extensions given a word w.
def getExtensions(w, A = None, R = None):
    if A == None:
        A = getAlphabet(w)
    if R == None:
        R = range(0,len(w)+1)

    extensions = []
    for i in R:
        for e in extendAtPosition(w, A, i):
            if not e in extensions:
                extensions.append(e)
    return extensions

def extendAtPosition(w, A, i):
    extensions = []
    for a in A:
        extensions.append(w[:i] + a + w[i:])
    return extensions

# Returns all possible words of length k with alphabet A.
def allWords(A, k):
    if k == 1:
        return A
    
    result = set()
    for w in allWords(A, k-1):
        for i in range(0,k):
            for a in A:
                result.add(w[:i] + a + w[i:])
    return result

# Returns the number of unique factors of length n in w using a brute force method. 
def complexity(w,n):
    factors = {}
    for i in range(0,len(w)-n+1):
        factors[w[i:i+n]] = None
    return len(factors.keys())

# Returns all factors of w.
def factors(w):
    result = set()
    for n in range(1,len(w)+1):
        for i in range(0, len(w)-n+1):
            result.add(w[i:n+i])
    return result   

# Returns the period of the word, that is the minimal period of w.
def period(w):
    n = len(w)
    for p in range(1, n):
        returnFlag = True
        for i in range(0, n-p):
            if w[i] != w[i+p]:
                returnFlag = False
                break
        if returnFlag:
            return p
    return 0

# Exponent of a word
def exponent(w):
    p = period(w)
    if p == 0:
        return 0
    return len(w) / p

# Returns true if there is no factor of w with exponent strictly greater than b.
def isBPlusFree(w, bPlus):
    for s in factors(w):
        if exponent(s) > bPlus:
            return False
    return True

# Returns true if there is no factor of w that has exponent greater than or equal to beta. 
def isBetaFree(w, beta):
    for s in factors(w):
        if exponent(s) >= beta:
            return False
    return True

# Returns true if for any extension of w is not beta-free. 
def isExtremalBetaFree(w, beta):
    if not isBetaFree(w, beta):
        return False

    for e in getExtensions(w):
        if isBetaFree(e, beta):
            return False
    return True

# Returns true if for any extension of w is not bPlus-free. 
def isExtremalBPlusFree(w, bPlus):
    if not isBPlusFree(w, bPlus):
        return False

    for e in getExtensions(w):
        if isBPlusFree(e, bPlus):
            return False
    return True

def isOverlapFree(w):
    return isBPlusFree(w,2)

# Generates all bplus-free words.
def bPlusFreeWords(length, A, top, bottom):
    result = set()

    def dfs(w):

        if len(w) == length:
            result.add(w)
            return

        for a in A:
            if not containsBPlusSuffix(w+str(a), top, bottom):
                dfs(w+str(a))

    dfs('')

    return result

def containsBPlusSuffix(w, top, bottom):
    n = len(w)

    # for p in range(1, k):
    #     if not isBPlusFree(w[-(p*top)-1:],top/bottom):
    #         return True
    # return False

    for p in range(0,n+1):
        s = w[p:]
        
    return False