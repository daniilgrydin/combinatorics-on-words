from extendERT import get_all_right_bookends, get_all_left_bookends
from combinatorics.exponent import ExtendedReal, is_exponent_free
from itertools import combinations
from combinatorics.extremal import is_left_extremal, is_right_extremal

def get_morphism_images_from_file(file, image_count):
    morphisms = []
    current = []
    count = 0
    to_read = open(file, "r").readlines()
    for line in to_read:
        if line[0] != '-':
            current.append(line.strip())
            count += 1
            if count == image_count:
                count = 0
                morphisms.append(list(current))
                current = []
    return morphisms

def has_common_bookends(morphisms, alphabet, beta, max_bookend_size):
    for m in morphisms:
        print("Morphism:",m)

        left = get_all_left_bookends(m[0], alphabet, beta, max_bookend_size)
        right = get_all_right_bookends(m[0], alphabet, beta, max_bookend_size)
        found_bookends = True

        for i in range(1,len(m)):
            left_pass = False
            right_pass = False
            for l in left:
                if is_left_extremal(l + m[i], alphabet, lambda w: is_exponent_free(w, beta)):
                    left_pass = True
            for r in right:
                if is_right_extremal(m[i] + r, alphabet, lambda w: is_exponent_free(w, beta)):
                    right_pass = True
            if not left_pass or not right_pass:
                found_bookends = False
                break

        if found_bookends:
            print("Found common bookends.")
            print("Left:", left)
            print("Right:", right)
        print()

def determine_common_right_bookends(morphism, alphabet, beta, candidate_bookends):
    result = []
    for c in candidate_bookends:
        for i in morphism:
            if not is_right_extremal(i + c, alphabet, lambda w: is_exponent_free(w, beta)):
                break
        result.append(c)
    return result


def determine_common_left_bookends(morphism, alphabet, beta, candidate_bookends):
    result = []
    for c in candidate_bookends:
        for i in morphism:
            if not is_left_extremal(c + i, alphabet, lambda w: is_exponent_free(w, beta)):
                break
        result.append(c)
    return result

def is_bookend_ideal