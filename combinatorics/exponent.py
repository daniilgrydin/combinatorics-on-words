class ExtendedReal:
    def __init__(self, numerator, denominator, plus):
        self.rational = Rational(numerator, denominator)
        self.plus = plus
    
    def __float__(self):
        return float(self.rational)
    
    def __str__(self):
        return str(self.rational) + ("+" if self.plus else "")
    
    def __eq__(self, other):
        if isinstance(other, ExtendedReal):
            return (
                self.plus == other.plus
                and self.rational == self.rational
            )
        return self.rational == other and not self.plus

    def __add__(self,other):
        if isinstance(other, ExtendedReal):
            rational_part = self.rational + other.rational
            return ExtendedReal(rational_part.numerator, rational_part.denominator, self.plus or other.plus)
        rational_part = self.rational + other
        return ExtendedReal(
            rational_part.numerator,
            rational_part.denominator,
            self.plus
        )
    
    def __sub__ (self,other):
        if isinstance(other, ExtendedReal):
            rational_part = self.rational - other.rational
            return ExtendedReal(rational_part.numerator, rational_part.denominator, self.plus or other.plus)
        rational_part = self.rational - other
        return ExtendedReal(
            rational_part.numerator,
            rational_part.denominator,
            self.plus
        )
        
    def __mul__(self, other):
        if isinstance(other, ExtendedReal):
            rational_part = self.rational * other.rational
            return ExtendedReal(rational_part.numerator, rational_part.denominator, self.plus or other.plus)
        rational_part = self.rational * other
        return ExtendedReal(
            rational_part.numerator,
            rational_part.denominator,
            self.plus
        )

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __neg__(self):
        rational_part = -self.rational
        return ExtendedReal(rational_part.numerator, rational_part.denominator, self.plus)
    
    def __truediv__(self, other):
        if isinstance(other, ExtendedReal):
            rational_part = self.rational / other.rational
            return ExtendedReal(rational_part.numerator, rational_part.denominator, self.plus or other.plus)
        rational_part = self.rational / other
        return ExtendedReal(
            rational_part.numerator,
            rational_part.denominator,
            self.plus
        )

    def __lt__(self, other):
        if isinstance(other, ExtendedReal):
            if self.plus == other.plus or self.plus:
                return self.rational < other.rational
            else:
                return self.rational <= other.rational
        if  self.plus:
            return self.rational < other
        else:
            return self.rational <= other

    def __gt__(self, other):
        if isinstance(other, ExtendedReal):
            if self.plus == other.plus or self.plus:
                return self.rational > other.rational
            else:
                return self.rational >= other.rational
        if self.plus:
            return self.rational > other
        else:
            return self.rational >= other
    
    def __le__(self, other):
        if isinstance(other, ExtendedReal):
            if self.plus == other.plus or other.plus:
                return self.rational <= other.rational
            else:
                return self.rational < other.rational
        if  self.plus:
            return self.rational < other
        else:
            return self.rational <= other

    def __ge__(self, other):
        if isinstance(other, ExtendedReal):
            if self.plus == other.plus or other.plus:
                return self.rational >= other.rational
            else:
                return self.rational > other.rational
        if self.plus:
            return self.rational > other
        else:
            return self.rational >= other
    
    def __int__(self):
        return int(self.rational)
    
class Rational:
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator
        self.reduce()
    
    # def is_less_than(self, other):
    #     return self.numerator * other.denominator < other.numerator * self.denominator
    
    def __float__(self):
        return self.numerator / self.denominator
    
    def __str__(self):
        return str(self.numerator) + "/" + str(self.denominator)
    
    def is_less_than(self, other):
        print("This method is depricated, you can now use inequalities with ExtendedReals and Rationals")
        if isinstance(other, ExtendedReal):
            if other.plus:
                return self.numerator * other.rational.denominator <= other.rational.numerator * self.denominator
            else:
                return self.numerator * other.rational.denominator < other.rational.numerator * self.denominator
        elif isinstance(other, Rational):
            return self.numerator * other.denominator < other.numerator * self.denominator
        else: raise ValueError(str(type(other)) + "type is not supported.")
    
    def __eq__(self, other):
        if isinstance(other, int):
            return self.numerator == self.denominator * other
        if isinstance(other, Rational):
            return self.numerator * other.denominator == self.denominator * other.numerator
        return NotImplemented
    
    def __add__(self, other):
        if isinstance(other, int):
            return Rational(
                self.numerator + other * self.denominator,
                self.denominator
            )
        if isinstance(other, Rational):
            return Rational(
                (self.numerator * other.denominator) + (other.numerator * self.denominator),
                self.denominator * other.denominator
            )
        return NotImplemented
    
    def __sub__(self, other):
        if isinstance(other, int):
            return Rational(
                self.numerator - other * self.denominator,
                self.denominator
            )
        if isinstance(other, Rational):
            return Rational(
                (self.numerator * other.denominator) - (other.numerator * self.denominator),
                self.denominator * other.denominator
            )
        return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, int):
            return Rational(
                self.numerator * other,
                self.denominator
            )
        if isinstance(other, Rational):
            return Rational(
                self.numerator * other.numerator,
                self.denominator * other.denominator
            )
        return NotImplemented
    
    def __truediv__(self, other): # self / other
        if isinstance(other, int):
            return Rational(
                self.numerator,
                self.denominator * other
            )
        if isinstance(other, Rational):
            return Rational(
                self.numerator * other.denominator,
                self.denominator * other.numerator
            )
        return NotImplemented
    
    def __rtruediv__(self, other): # other / self
        if isinstance(other, int):
            return Rational(
                self.denominator * other,
                self.numerator
            )
        if isinstance(other, Rational):
            return Rational(
                other.numerator * self.denominator,
                other.denominator * self.numerator
            )
        return NotImplemented
    
    def __lt__(self, other):
        if isinstance(other, int):
            return self.numerator < self.denominator * other
        if isinstance(other, Rational):
            return self.numerator * other.denominator < self.denominator * other.numerator
        if isinstance(other, ExtendedReal):
            if other.plus:
                return self.numerator * other.rational.denominator <= other.rational.numerator * self.denominator
            else:
                return self.numerator * other.rational.denominator < other.rational.numerator * self.denominator
        return NotImplemented
        
    def __le__(self, other):
        if isinstance(other, int):
            return self.numerator <= self.denominator * other
        if isinstance(other, Rational):
            return self.numerator * other.denominator <= self.denominator * other.numerator
        return NotImplemented
    
    def __gt__(self, other):
        if isinstance(other, int):
            return self.numerator > self.denominator * other
        if isinstance(other, Rational):
            return self.numerator * other.denominator > self.denominator * other.numerator
        return NotImplemented
    
    def __ge__(self, other):
        if isinstance(other, int):
            return self.numerator >= self.denominator * other
        if isinstance(other, Rational):
            return self.numerator * other.denominator >= self.denominator * other.numerator
        return NotImplemented
    
    def __neg__(self):
        return Rational(-self.numerator, self.denominator)

    def __int__(self):
        return self.numerator // self.denominator
    
    def reduce(self):
        def gcd(a,b):
            if b == 0:
                return a
            q = a % b
            if q != 0:
                return gcd(b,q)
            else: 
                return b
            
        div = gcd(max(self.numerator, self.denominator), min(self.numerator, self.denominator))
        self.numerator = self.numerator // div
        self.denominator = self.denominator // div

def get_critical_exponent(word):
    max_power = Rational(1,1)
    # max_power_start = 0
    for start in range(len(word)):
        repeated = 0
        end = start + 1
        while end < len(word):
            # rep = "" if repeated == 0 else " " * (repeated-1) + "."
            # print(" "* start + "v" + rep)
            # print(word, repeated)
            # print(" "* end + "^")
            if word[start+repeated] == word[end]:
                repeated += 1
                power_length = end-start+1
                power = Rational(power_length, (power_length - repeated))
                # print(power)
                if max_power < power:
                    max_power = power
            else:
                if repeated > 0:
                    end -= 1
                repeated = 0
            end += 1
            # print()
            # print()
    return max_power

def get_critical_factors(word):
    result = set()
    target = get_critical_exponent(word)

    for start in range(len(word)):
        for multiple in range(1, len(word[start:]) // target.numerator + 1):
            end = start + multiple * target.numerator
            current_factor = word[start:end]
            period = multiple * target.denominator
            repeat = 0
            while repeat+period < len(current_factor) and \
            current_factor[repeat] == current_factor[repeat+period]:
                repeat += 1
            if repeat+period == len(current_factor):
                result.add(current_factor)

    return result

def get_critical_exponent_of_words(words):
    criticals = []
    for w in words:
        criticals.append(get_critical_exponent(w))
    return max(criticals)

def is_suffix_exponent_free(word, target_exponent: ExtendedReal):
    word = word[::-1]
    repeated = 0
    end = 1
    max_power = Rational(1,1)
    while end < len(word):
        # rep = "" if repeated == 0 else " " * (repeated-1) + "."
        # print(" "* start + "v" + rep)
        # print(word, repeated)
        # print(" "* end + "^")
        if word[repeated] == word[end]:
            repeated += 1
            power_length = end+1
            power = Rational(power_length, (power_length - repeated))
            # print(word[:end],power)
            if power >= target_exponent:
                # print(power)
                return False
            if max_power < power:
                max_power = power
                # max_power_start = start
        else:
            if repeated > 0:
                end -= 1
            repeated = 0
        end += 1
        # print()
        # print()
    # print(max_power)
    return True

def is_exponent_free(word, target_exponent: ExtendedReal):
    for i in range(len(word)):
        if not is_suffix_exponent_free(word[:i+1], target_exponent):
            return False
    return True

def get_min_critical_exponent_of_extensions(word):
    from .word import get_extensions

    critical_exponents = []
    for e in get_extensions(word):
        critical_exponents.append(get_critical_exponent(e))
    
    return min(critical_exponents)

def get_min_critical_exponent_of_extensions_of_words(words):
    criticals = []
    for w in words:
        criticals.append(get_min_critical_exponent_of_extensions(w))
    return min(criticals)

def get_words_with_critical_exponent(target_exponent, max_multiple, min_multiple = 1, words = [], words_file = "", output_file = "", do_print = False):
    import tools.file_rw as rw

    result = []
    beta = ExtendedReal(target_exponent.numerator, target_exponent.denominator, True)

    if len(words_file) > 0:
        words = rw.load_words_by_length(words_file)

    for m in range(min_multiple, max_multiple + 1):
        initial_part_length = m * target_exponent.denominator
        if do_print: print("Looking at words of length", m * target_exponent.numerator)
        for w in words[initial_part_length]:
            current = w
            to_repeat = (target_exponent - 1) * initial_part_length
            while to_repeat >= initial_part_length:
                current += w
                to_repeat -= initial_part_length
            if to_repeat != 0:
                current += w[:int(to_repeat)]
            if is_exponent_free(current, beta):
                result.append(current)
        rw.save_words(result, output_file)
    
    return result