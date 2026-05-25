class ExtendedReal:
    def __init__(self, numerator, denominator, plus):
        self.numerator = numerator
        self.denominator = denominator
        self.plus = plus
        
    def is_less_than(self, other):
        if isinstance(other, Rational):
            if self.plus:
                return self.numerator * other.denominator < other.numerator * self.denominator
            else:
                return self.numerator * other.denominator <= other.numerator * self.denominator
        else: raise ValueError(f"{type(other)} type is not supported.")
    
    def __float__(self):
        return self.numerator / self.denominator
    
    def __str__(self):
        return f"{self.numerator}/{self.denominator}{"+" if self.plus else ""}"
    
class Rational:
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator
    
    def __float__(self):
        return self.numerator / self.denominator
    
    def __str__(self):
        return f"{self.numerator}/{self.denominator}"

def get_critical_exponent(word):
    max_power = 1
    # max_power_start = 0
    for start in range(len(word)):
        repetition = 0
        for cursor in range(start+1, len(word)):
            # print(word)
            # print(" "* start + "^")
            # print(" "* cursor + "*")
            if word[start+repetition] == word[cursor]:
                repetition += 1
                power_length = cursor-start+1
                power = power_length / (power_length - repetition)
                if power > max_power:
                    max_power = power
                    # max_power_start = start
            else:
                repetition = 0
    return max_power

def is_suffix_exponent_free(word, target_exponent: ExtendedReal | float | int):
    length = len(word)
    period = length-1
    cursor = period-1
    for factor in range(length-2, -1, -1):
        # print()
        # print(" " * (factor) + "v")
        # print(word)
        # print(" " * (cursor) + "*")
        # print(" " * (period) + "^")
        if word[factor] == word[cursor]:
            cursor -= 1
            power = Rational(length if period != 0 else 0, period)
            if isinstance(target_exponent, ExtendedReal):
                if target_exponent.is_less_than(power):
                    return False
            else:
                if target_exponent < power:
                    return False
        else:
            period = factor
            cursor = length
    return True

def is_exponent_free(word, target_exponent: ExtendedReal | float | int):
    from .word import get_factors, period
    for f in get_factors(word):
        p = period(f)
        power = Rational(len(f), p) if p != 0 else Rational(1,1)
        if target_exponent.is_less_than(power):
            #print(f"Target {target_exponent} < {power}")
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
