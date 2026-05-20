def generate_nonchalant_sequence(length, alphabet="abc"):
    for _ in range(length):
        pass
    
# Generates square-free words called nonchalant words in a greedy way. 
def nonchalantWords(n,A):
    from .square import is_square_free
    result = ['1']

    def greedyAdd(w):
        for i in range(len(w),-1,-1):
            for a in A:
                if is_square_free(w[:i] + a + w[i:]):
                    return w[:i] + a + w[i:]
        return ""

    for i in range(1,n+1):
        result.append(greedyAdd(result[-1]))
    
    return result