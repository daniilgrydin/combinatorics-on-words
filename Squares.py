import Words

# Returns true if the end of the word w has a square.
def hasSquareSuffix(w):
    n = len(w)
    for p in range(1,n//2+1):
        if w[-2*p:-p] == w[-p:]:
            return True
    return False

# Returns true if the word has a square.
def hasSquare(w):
    n = len(w)
    for i in range(n):
        if hasSquareSuffix(w[:i+1]):
            return True
    return False

# Generates all square free works of length n over an alphabet of k characters.
def squareFreeWords(n,k):
    SF=[]

    def dfs(w):

        if len(w) == n:
            SF.append(w)
            return

        for a in range(k):
            if not hasSquareSuffix(w+str(a)):
                dfs(w+str(a))

    dfs('')

    return SF

# Returns true with word w is extremal square free.
def isExtremalSquareFree(w):
    if hasSquare(w):
        return False

    for e in Words.getExtensions(w):
        if not hasSquare(e):
            return False
    return True

# Returns true if w has at most 2 square-free extensions where those 2 extensions
# are a left and a right extension (or just one left, just one right).
def isNearlyExtremalSquareFree(w):
    if len(getSquareFreeExtensions(w)) > 2:
        return False
    
    sfLeft, sfRight = 0, 0
    for a in Words.getAlphabet(w):
        sfLeft += 1 if not hasSquare(a + w) else 0
        sfRight += 1 if not hasSquare(w + a) else 0

    return sfLeft <= 1 and sfRight <= 1

# Returns the amount of extensions of a word which are square free.
def getSquareFreeExtensions(w):
    squareFreeExtensions = []
    for e in Words.getExtensions(w):
        if not hasSquare(e):
            squareFreeExtensions.append(e)
    return squareFreeExtensions

# Generates square-free words called nonchalant words in a greedy way. 
def nonchalantWords(n,A):
    result = ['1']

    def greedyAdd(w):
        for i in range(len(w),-1,-1):
            for a in A:
                if not hasSquare(w[:i] + a + w[i:]):
                    return w[:i] + a + w[i:]
        return None

    for i in range(1,n+1):
        result.append(greedyAdd(result[-1]))
    
    return result

# print(nonchalantWords(10,['1','2','3']))

# Finds the shortest extremal square free word
# H = 0120102120121012010212012 # Verify that this is the smallest square-free word.
#
# for i in range(0,26):
#     sfw = squareFreeWords(i,3)
#     esfw = []
#     nesfw = []
#     for w in sfw:
#         if isNearlyExtremalSquareFree(w):
#             nesfw.append(w)
#             if isExtremalSquareFree(w):
#                 esfw.append(w)

# print("Nearly extremal square-free words:", len(nesfw))
# for w in nesfw:
#     print(w)
# print("\n")
# print("Extremal square-free words:", len(esfw))
# for w in esfw:
#     print(w)


# Verify that N and the permutations of its alphabet and the reversals are nearly extremal square-free. 
# N = "abacbabcabacbcacbabcabacabcbabcabacbcabcb"
# NPermutations = [N,
#     Words.cycleCharacters(N, {'a':'b', 'b':'a'}),
#     Words.cycleCharacters(N, {'a':'c', 'c':'a'}),
#     Words.cycleCharacters(N, {'b':'c', 'c':'b'}),
#     Words.cycleCharacters(N, {'a':'b', 'b':'c', 'c':'a'}),
#     Words.cycleCharacters(N, {'a':'c', 'c':'b', 'b':'a'})]
# for i in NPermutations:
#     print(i + ":", isNearlyExtremalSquareFree(i), getSquareFreeExtensions(i))
#     print(i[::-1] + ":", isNearlyExtremalSquareFree(i[::-1]), getSquareFreeExtensions(i[::-1]))

# We see that square free words are the same as beta 2-free words.
# for i in squareFreeWords(10,3):
#     print(Words.betaFree(i,2))
