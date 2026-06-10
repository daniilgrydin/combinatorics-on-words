class TernaryConstructionDecomposition():
    def __init__(self, morphism, r : str = None, s : str = None):
        from combinatorics.word import get_common_prefix, get_common_suffix

        images = []
        if isinstance(morphism, dict):
            images = [morphism['0'], morphism['1'], morphism['2'], morphism['3']]
        # elif isinstance(morphism, function):
        #     images = [morphism('0'), morphism('1'), morphism('2'), morphism('3')]
        else:
            images = morphism
        
        if r != None:
            self.A = determine_A(images, get_A_candidates_from_bookend(r))
            self.B = get_B_from_r_and_A(r, self.A)
            self.A_rev_comp = ternary_complement(self.A)[::-1]
            self.B_rev_comp = ternary_complement(self.B)[::-1]
            self.r = r
            self.s = self.A + self.B_rev_comp + self.A_rev_comp
        elif s != None:
            self.A = determine_A(images, get_A_candidates_from_bookend(s))
            self.B = get_B_from_s_and_A(s, self.A)
            self.A_rev_comp = ternary_complement(self.A)[::-1]
            self.B_rev_comp = ternary_complement(self.B)[::-1]
            self.r = self.A + self.B + self.A_rev_comp
            self.s = s
        else:
            print("No bookends provided, so search may be slow.")
            self.r, self.s = get_bookends_from_morphism(images)
            self.A = determine_A(images, get_A_candidates_from_bookend(self.r))
            self.B = get_B_from_r_and_A(self.r, self.A)
            self.A_rev_comp = ternary_complement(self.A)[::-1]
            self.B_rev_comp = ternary_complement(self.B)[::-1]

        self.V1, self.V2 = get_V1_V2(images, self.A)
        self.g = get_g(images, self.A, self.V1, self.V2)
        self.r_prime = get_common_suffix([self.r, images[0], images[1], images[2], images[3]])
        self.s_prime = get_common_prefix([self.s, images[0], images[1], images[2], images[3]])

        self.alpha = None
        self.beta  = None

    def get_morphism_images(self):
        return [
            self.A + self.V1 + self.g['0'] + self.V2 + self.A_rev_comp,
            self.A + self.V1 + self.g['1'] + self.V2 + self.A_rev_comp,
            self.A + self.V1 + self.g['2'] + self.V2 + self.A_rev_comp,
            self.A + self.V1 + self.g['3'] + self.V2 + self.A_rev_comp
        ]
    
    def get_alpha(self):
        from combinatorics.exponent import get_critical_exponent_of_words

        if self.alpha == None:
            self.alpha = get_critical_exponent_of_words(
                [self.r + img + self.s for img in self.get_morphism_images()])
            
        return self.alpha

    def get_beta(self):
        from combinatorics.exponent import get_min_critical_exponent_of_extensions_of_words

        if self.beta == None:
            self.beta = get_min_critical_exponent_of_extensions_of_words(
                [self.r + img + self.s for img in self.get_morphism_images()])
            
        return self.beta


    def __str__(self):
        return f" \
        A: {self.A} \n \
        A~-: {self.A_rev_comp} \n \
        B: {self.B} \n \
        B~-: {self.B_rev_comp} \n \
        r: {self.r} \n \
        r': {self.r_prime} \n \
        s: {self.s} \n \
        s': {self.s_prime} \n \
        V1: {self.V1} \n \
        V2: {self.V2} \n \
        g(0): {self.g['0']} \n \
        g(1): {self.g['1']} \n \
        g(2): {self.g['2']} \n \
        g(3): {self.g['3']} \n \
        "

def decompose_ternary_construction(morphism_images, r, s):
    A = determine_A(morphism_images, get_A_candidates_from_bookend(r))
    B = get_B_from_r_and_A(r, A)
    V1, V2 = get_V1_V2(morphism_images, A)
    g = get_g(morphism_images, A, V1, V2)

    print("A:",A)
    print("B:",B)
    print("V1:",V1)
    print("V2:",V2)
    print("g:",g)
    
def get_A_candidates_from_bookend(b):
    candidates = []
    for i in range(0, len(b)):
        candidate = b[:i+1]
        if ternary_complement(b[-len(candidate):])[::-1] == candidate:
            candidates.append(candidate)
    return candidates

def get_B_from_r_and_A(r, A):
    return r[len(A):-len(A)]

def get_B_from_s_and_A(s, A):
    return ternary_complement(s[len(A):-len(A)])[::-1]

def determine_A(morphism_images, A_candidates):
    candidates = []
    for A in A_candidates:
        pass_flag = True
        for img in morphism_images:
            if not img[:len(A)] == A or not img[-len(A):] == ternary_complement(A)[::-1]:
                pass_flag = False
                break
        if pass_flag:
            candidates.append(A)
    
    if len(candidates) == 0:
        raise RuntimeError("No candidates found for A.")

    return max(candidates)

def get_V1_V2(morphism_images, A):
    from combinatorics.word import get_common_suffix, get_common_prefix

    trimmed_images = []
    for img in morphism_images:
        trimmed_images.append(img[len(A):-len(A)])
    return get_common_prefix(trimmed_images), get_common_suffix(trimmed_images)

def get_g(morphism_images, A, V1, V2):
    trimmed_images = []
    for img in morphism_images:
        trimmed_images.append(img[len(A) + len(V1):-len(A) - len(V2)])
    return {'0':trimmed_images[0],
            '1':trimmed_images[1],
            '2':trimmed_images[2],
            '3':trimmed_images[3]}

def ternary_complement(w):
    result = ""
    for c in w:
        if c == '0':
            result += '2'
        elif c == '1':
            result += '1'
        else:
            result += '0'
    return result

def get_bookends_from_morphism(images, max_bookend_size = -1, min_A_size = 0, B_seed = None):
    from combinatorics.word import get_common_prefix, get_common_suffix, generate_greedy_words
    from combinatorics.exponent import get_critical_exponent, Rational, ExtendedReal, is_suffix_exponent_free, is_exponent_free
    from combinatorics.extremal import is_left_extremal, is_right_extremal

    if max_bookend_size == -1:
        max_bookend_size = len(images[0])

    largest_A = get_common_prefix(images)
    largest_A_rev_comp = get_common_suffix(images)
    potential_A = get_common_prefix([largest_A, ternary_complement(largest_A_rev_comp)[::-1]])

    if len(potential_A) < min_A_size:
        raise RuntimeError("No bookends found.")

    beta = Rational(1,1)
    for img in images:
        exponent = get_critical_exponent(img)
        if exponent > beta:
            beta = exponent
    beta = ExtendedReal(beta.numerator, beta.denominator, True)

    if B_seed == None:
        B_candidates = []
        for i in range(0, max_bookend_size - 2*len(potential_A) + 1):
            B_candidates.append(generate_greedy_words("012", 
                                            1,
                                            lambda w: is_suffix_exponent_free(w, beta), 
                                            B_candidates[-1] if len(B_candidates) > 0 else [""]))
    else:
        B_candidates = B_seed

    for i in range(len(potential_A), min_A_size - 1, -1):
        A_candidate = potential_A[:i]

        if B_seed == None:
            B_candidates.append(generate_greedy_words("012", 
                                                1, 
                                                lambda w: is_suffix_exponent_free(w, beta), 
                                                B_candidates[-1] if len(B_candidates) > 0 else [""]))
                
        for generated_index in range(0, max_bookend_size - 2*len(A_candidate) + 1):
            for B_candidate in B_candidates[generated_index]:
                r_candidate = A_candidate + B_candidate + ternary_complement(A_candidate)[::-1]

                left_extremal_flag = True
                for img in images:
                    if not is_left_extremal(r_candidate + img, "012", lambda w: is_exponent_free(w, beta)):
                        left_extremal_flag = False
                        break
                
                if not left_extremal_flag: # r_candidate did not work.
                    continue

                # r_candidate is a left bookend. Try for right bookend
                s_candidate = A_candidate + ternary_complement(B_candidate)[::-1] + ternary_complement(A_candidate)[::-1]
                right_extremal_flag = True
                for img in images:
                    if not is_right_extremal(img + s_candidate, "012", lambda w: is_exponent_free(w, beta)):
                        right_extremal_flag = False
                        break

                if right_extremal_flag and left_extremal_flag:
                    return r_candidate, s_candidate

    raise RuntimeError("No bookends found.")


# primary = TernaryConstructionDecomposition([
#     '01021012021020102101210212010201210120102120210201210212',
#     '01021012021020102120121012021201021012102120210201210212',
#     '01021012021020102120121020120212010201210120210201210212',
#     '01021012021020102120210121020102101201020120210201210212'
#      ])

# print(TernaryConstructionDecomposition(['010210120210201021012010201210120212010210121020102120210201210212', 
# '010210120210201021012010212012101201020120210120102120210201210212', 
# '010210120210201021201210201202120121021201021012102120210201210212', 
# '010210120210201021202101210201021012021201021012102120210201210212'], 
#     r = '010212010201210212021020120212010201210212'))

# print()

# print(TernaryConstructionDecomposition(['010210120210201021012010201210120212010210121020102120210201210212', 
# '010210120210201021012010212012101201020120210120102120210201210212', 
# '010210120210201021201210201202120121021201021012102120210201210212', 
# '010210120210201021202101210201021012021201021012102120210201210212'], 
#     s = '010210120212010201202102010210120212010212'))

