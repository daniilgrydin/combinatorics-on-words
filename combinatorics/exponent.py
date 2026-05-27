class ExtendedReal:
    def __init__(self, numerator, denominator, plus):
        self.rational = Rational(numerator, denominator)
        self.plus = plus
    
    def __float__(self):
        return float(self.rational)
    
    def __str__(self):
        return f"{self.rational}{"+" if self.plus else ""}"
    
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
    
    # def is_less_than(self, other):
    #     return self.numerator * other.denominator < other.numerator * self.denominator
    
    def __float__(self):
        return self.numerator / self.denominator
    
    def __str__(self):
        return f"{self.numerator}/{self.denominator}"
    
    def is_less_than(self, other):
        print("This method is depricated, you can now use inequalities with ExtendedReals and Rationals")
        if isinstance(other, ExtendedReal):
            if other.plus:
                return self.numerator * other.rational.denominator <= other.rational.numerator * self.denominator
            else:
                return self.numerator * other.rational.denominator < other.rational.numerator * self.denominator
        elif isinstance(other, Rational):
            return self.numerator * other.denominator < other.numerator * self.denominator
        else: raise ValueError(f"{type(other)} type is not supported.")
    
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
    
    def __truediv__(self, other):
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

    # for start in range(len(word)):
    #     repetition = 0
    #     for cursor in range(start+1, len(word)):
    #         if word[start+repetition] == word[cursor]:
    #             repetition += 1
    #             power_length = cursor-start+1
    #             exponent = ExtendedReal(power_length, (power_length - repetition), False)
    #             if isinstance(target_exponent, ExtendedReal):
    #                 if target_exponent.is_less_than(exponent):
    #                     return False
    #             else:
    #                 if target_exponent < exponent:
    #                     return False
    #         else:
    #             repetition = 0
    # return True
