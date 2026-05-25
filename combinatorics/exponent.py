class ExtendedReal:
    def __init__(self, numerator, denominator, plus):
        self.numerator = numerator
        self.denominator = denominator
        self.plus = plus
        
    def is_less_than(self, other):
        if isinstance(other, Rational):
            return self.numerator * other.denominator < other.numerator * self.denominator
        else: raise ValueError(f"{type(other)} type is not supported.")
    
    def __float__(self):
        return self.numerator / self.denominator
    
    def __str__(self):
        return f"{self.numerator}/{self.denominator}{"+" if self.plus else ""}"
    
class Rational:
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator
    
    def is_less_than(self, other):
        return self.numerator * other.denominator < other.numerator * self.denominator
    
    def __float__(self):
        return self.numerator / self.denominator
    
    def __str__(self):
        return f"{self.numerator}/{self.denominator}"

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
                if max_power.is_less_than(power):
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
            if not power.is_less_than(target_exponent):
                # print(power)
                return False
            if max_power.is_less_than(power):
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
