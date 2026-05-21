from libraries.word import get_extensions, get_factors, exponent, generate_greedy_words
from libraries.square import generate_square_free_words
from libraries.exponent import ExtendedReal, get_critical_exponent

class Prop22Verifier:
    f0 : str
    f1 : str 
    f2 : str
    r : str
    s : str
    alpha : float 
    beta : float
    tr : str 
    ts : str

    def __init__(self, f0, f1, f2, r, s, alpha, beta):
        self.f0 = f0
        self.f1 = f1 
        self.f2 = f2
        self.r = r
        self.s = s
        self.alpha = alpha
        self.beta = beta
        if len(f0) != len(f1) or len(f0) != len(f2) or len(f1) != len(f2):
            print("f is not uniform.") 

    def f(self, w):
        result = ""
        for a in w:
            if a == '0':
                result += self.f0
            if a == '1':
                result += self.f1
            if a == '2':
                result += self.f2
        return result

    def verify(self):
        routines = [self.i,self.ii,self.iii,self.iv]
        words = [self.f0,self.f1,self.f2]
        for r in routines:
            for w in words:
                r(w)
            print(r.__name__,"done")

        print("Tr:",self.tr)
        print("Ts:",self.ts)

        self.v()
        print("v done")

        self.checkSynchronizing()
        print("Synchronizing check done")
        self.lemma23Check()
        print("Lemma 23 check done")
        
        print("Done")

    # "Every internal extension of the word f(c) contains a factor of exponent at least beta"
    def i(self, fc):
        for ext in get_extensions(fc, positions = range(1, len(fc)) ):
            passFlag = False
            for fact in get_factors(ext):
                if exponent(fact) >= self.beta:
                    passFlag = True
                    break
            if not passFlag:
                print("(i) Fails: No factor of the extension",ext,"has exponent at least",self.beta)
                return
    
    # "Every left extension and every internal extension of the word rf(c) contains a factor
    # of exponent at least beta"
    def ii(self, fc):
        for ext in get_extensions(self.r + fc, positions = range(0, len(fc)) ):
            passFlag = False
            for fact in get_factors(ext):
                if exponent(fact) >= self.beta:
                    passFlag = True
                    break
            if not passFlag:
                print("(ii) Fails: No factor of the extension",ext,"has exponent at least",self.beta)
                return
            
    # "Every right extension and every internal extension of the word f(c)s contains a factor
    # of exponent at least beta"
    def iii(self, fc):
        for ext in get_extensions(fc + self.s, positions = range(1, len(fc)+1) ):
            passFlag = False
            for fact in get_factors(ext):
                if exponent(fact) >= self.beta:
                    passFlag = True
                    break
            if not passFlag:
                print("(iii) Fails: No factor of the extension",ext,"has exponent at least",self.beta)
                return
            
    def checkSynchronizing(self):
        A = ['0','1','2']
        for a in A:
            for b in A:
                for c in A:
                    fab = self.f(a+b)
                    fcIndex = fab.find(self.f(c))
                    if fcIndex > 0 and fcIndex != len(fab) - len(self.f0):
                        print("Not synchronizing.")
                        return

    def lemma23Check(self):
        a = 2
        b = self.alpha
        for i in range(1,self.maxSizeW()+1):
            for w in generate_square_free_words(3,i):
                if get_critical_exponent(self.f(w)) > b:
                    print("Lemma 23 Fails: Word of length <=",self.maxSizeW(),"has a word",w,"that is square-free" \
                    " but that image f(w) is not",b,"free.")
                    return

    def maxSizeW(self):
        a = 2
        b = self.alpha
        q = len(self.f0)
        sizeW = max((2*b) / (b - a), 
                    (2*(q-1)*(2*b-1)) / (q*(b-1)))
        return round(sizeW)

    def getSPrime(self):
        sPrime = ""
        for i in range(0,len(self.f0)):
            if self.s[i] == self.f0[i]:
                sPrime += self.f0[i]
            else:
                return sPrime
        return []

    def getRPrime(self):
        rPrime = ""
        for i in range(1,len(self.f0)):
            if self.r[-i] == self.f0[-i]:
                rPrime += self.f0[-i]
            else:
                return rPrime[::-1]
        return []
            
    def getTr(self,k):
        return (self.r + self.s)[len(self.r)-len(self.getRPrime())-1: k-1]
    
    def getTs(self,k):
        return (self.r + self.s)[-(len(self.s)-len(self.getSPrime())): -k: -1]

    def iv(self, fc):
        tr = ""
        ts = ""

        rfc = self.r + fc
        fcs = fc + self.s

        maxSize = len(self.r) + len(self.s)

        tr = self.getTr(1)
        count = 1
        while rfc.count(tr) != 1 or fcs.count(tr) != 0:
            count += 1
            tr = self.getTr(count)

            if count > maxSize:
                print("(iv) Fails: Could not find Tr")
                break
        
        ts = self.getTs(1)
        count = 1
        while fcs.count(ts) != 1 or rfc.count(ts) != 0:
            count += 1
            ts = self.getTs(count)

            if count > maxSize:
                print("(iv) Fails: Could not find Ts")
                break

        self.tr = tr
        self.ts = ts
        

    def v(self):
        sf = ['01', '02', '10', '12', '20', '21']
        tr = self.tr
        ts = self.ts
        for w in sf:
            if self.f(w).count(tr) > 0 or self.f(w).count(tr) > 0:
                print("(v) Fails:",tr,"or",ts,"occurs in",w)
                return

print("(b)")
propb = Prop22Verifier('001011001101100100110100110110010011',
                       '001011001101100100110110010110010011',
                       '001011001101100101100100110110010011',
                       '1100110010011',
                       '001001',
                       7/3, 17/7)
propb.verify()

print("\n(c)")
propc = Prop22Verifier('001001100101100100110010110100110010110011011',
                       '001001100101100110100101100110110010110011011',
                       '001001100101100110100110110011010010110011011',
                       '00110110011011',
                       '00100110010011',
                       17/7, 5/2)
propc.verify()

print("\n(d)")
propd = Prop22Verifier('0011011001001100101100110110010011',
                       '0011011001001101001101100110010011',
                       '0011011001001101100110100110010011',
                       '00110110011011001010011',
                       '00110101100100110010011',
                       5/2, 18/7)
propd.verify()

print("\n(e)")
prope = Prop22Verifier('0011011001001100101100110110010011',
                       '0011011001001101100110100110010011',
                       '0011011001101001100100110110010011',
                       '01101100110110011001010011',
                       '00110101100110010011001001',
                       18/7, 8/3)
prope.verify()

input()


# def i(w):
#     for ext in get_extensions(w, R = range(1, len(w)) ):
#         passFlag = False
#         for fact in factors(ext):
#             if exponent(fact) >= (17/7):
#                 passFlag = True
#                 break
#         if not passFlag:
#             print("(i) No factor of",ext,"has exponent at least 17/7")
#             return False
#     return True

# def ii(w):
#     for ext in get_extensions(r + w, R = range(0, len(w)) ):
#         passFlag = False
#         for fact in factors(ext):
#             if exponent(fact) >= (17/7):
#                 passFlag = True
#                 break
#         if not passFlag:
#             print("(ii) No factor of",ext,"has exponent at least 17/7")
#             return False
#     return True

# def iii(w):
#     for ext in get_extensions(w + s, R = range(1, len(w)+1) ):
#         passFlag = False
#         for fact in factors(ext):
#             if exponent(fact) >= (17/7):
#                 passFlag = True
#                 break
#         if not passFlag:
#             print("(iii) No factor of",ext,"has exponent at least 17/7")
#             return False
#     return True

# def iv(w):
#     tr = '00110010011'
#     rw = r + w
#     ws = w + s
#     n = len(tr)
#     rwCount = 0
#     wsCount = 0
#     for i in range(0,len(rw) - n + 1):
#         if rw[i:i+n] == tr:
#             rwCount += 1
#     for i in range(0,len(ws) - n + 1):
#         if ws[i:i+n] == tr:
#             wsCount += 1
#     print("tr occurred",rwCount,"time(s) in rw and",wsCount,"time(s) in ws")

# def v(w):
#     tr = '00110010011'
#     n = len(tr)
#     count = 0
#     for i in range(0,len(w) - n + 1):
#         if w[i:i+n] == tr:
#             count += 1
#     print("tr occured in w",count,"time(s)")

# Demonstrates that these functions fail
# i('0110010') 
# ii('0110010')
# iii('1011')

# A = ['0','1','2']
# for a in A:
    # i(f(a))
    # ii(f(a))
    # iii(f(a))
#     iv(f(a))
# v(f('01'))
# v(f('02'))
# v(f('10'))
# v(f('12'))
# v(f('20'))
# v(f('21'))
# v(f('00'))
# v(f('11'))
# v(f('22'))


# show that w is 7/3+-free
# for i in range(7, 14 + 1):
#     for w in Squares.squareFreeWords(i,3):
#         if not Words.isBPlusFree(f(w),7/3):
#             print(w, 'is not 7/3+-free')
#     print(i, "complete")

# show that z has period at most 13.
# for a in A:
#     for fact in factors(r + f(a) + s):
#         if Words.period(fact) <= 13:
#             #print(fact,"has period",Words.period(fact),"and exponent",exponent(fact))
#             if exponent(fact) > 7/3:
#                 print(fact,"has period",Words.period(fact),"<= 13 and exponent ",exponent(fact),"> 7/3")

# print("Done")
