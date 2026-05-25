class ExtendedReal:
    def __init__(self, numerator, denominator, plus):
        self.numerator = numerator
        self.denominator = denominator
        self.plus = plus
        
    def is_less_than(self, other):
        if isinstance(other, float) or isinstance(other, int):
            if self.plus:
                return self.numerator < self.denominator * other
            else:
                return self.numerator <= self.denominator * other
        if isinstance(other, ExtendedReal):
            if self.plus == other.plus:
                return self.numerator * other.denominator < other.numerator * self.denominator
            else:
                if self.plus:
                    return self.numerator * other.denominator < other.numerator * self.denominator
                else:
                    return self.numerator * other.denominator <= other.numerator * self.denominator
        else: raise ValueError(f"{type(other)} type is not supported.")
    
    def __float__(self):
        return self.numerator / self.denominator
    
    def __str__(self):
        return f"{self.numerator}/{self.denominator}{"+" if self.plus else ""}"

def get_critical_exponent(word):
    max_power = ExtendedReal(1, 1, False)
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
                power = ExtendedReal(power_length, (power_length - repetition), False)
                if max_power.is_less_than(power):
                    max_power = power
                    # max_power_start = start
            else:
                repetition = 0
    return max_power

def is_suffix_exponent_free(word, target_exponent: ExtendedReal):
    length = len(word)
    period = length-1
    cursor = period
    for factor in range(length-2, -1, -1):
        if word[factor] == word[cursor]:
            cursor -= 1
            exponent = ExtendedReal((length-factor), (length - period), False)
            print(exponent)
            if not exponent.is_less_than(target_exponent):
                print(f"has factor {word[factor:]} with exponent {exponent} >= {target_exponent}")
                return False
        else:
            period = factor
            cursor = length-1
    print("Done")
    return True

def is_exponent_free(word, target_exponent: ExtendedReal):
    # for end in range(len(word)):
    #     if not is_suffix_exponent_free(word[:end], target_exponent):
    #         return False
    # return True
    return get_critical_exponent(word).is_less_than(target_exponent)