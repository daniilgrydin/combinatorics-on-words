from extendERT import get_all_right_bookends, get_all_left_bookends
from combinatorics.exponent import ExtendedReal, is_exponent_free
from itertools import combinations
from combinatorics.extremal import is_left_extremal, is_right_extremal

def find_common_left_bookends(morphism_images, alphabet, beta, max_bookend_size):
    result_left = []

    left = get_all_left_bookends(morphism_images[0], alphabet, beta, max_bookend_size)

    for l in left:
        pass_flag = True
        for m in morphism_images:
            if not is_left_extremal(l + m, alphabet, lambda w: is_exponent_free(w, beta)):
                pass_flag = False
                break
        if pass_flag:
            result_left.append(l)

    return result_left

def find_common_right_bookends(morphism_images, alphabet, beta, max_bookend_size):
    result_right = []

    right = get_all_right_bookends(morphism_images[0], alphabet, beta, max_bookend_size)

    for r in right:
        pass_flag = True
        for m in morphism_images:
            if not is_right_extremal(m + r, alphabet, lambda w: is_exponent_free(w, beta)):
                pass_flag = False
                break
        if pass_flag:
            result_right.append(r)

    return result_right


def determine_common_right_bookends(morphism_images, alphabet, beta, candidate_bookends):
    result = []
    for c in candidate_bookends:
        for i in morphism_images:
            if not is_right_extremal(i + c, alphabet, lambda w: is_exponent_free(w, beta)):
                break
        result.append(c)
    return result


def determine_common_left_bookends(morphism_images, alphabet, beta, candidate_bookends):
    result = []
    for c in candidate_bookends:
        for i in morphism_images:
            if not is_left_extremal(c + i, alphabet, lambda w: is_exponent_free(w, beta)):
                break
        result.append(c)
    return result

# If s' shares the same common prefix with all images (ie. They stop sharing prefixes at the same index.)
def is_right_bookend_ideal(morphism_images, bookend):
    for i in range(0, len(bookend)):
        pass_count = 0
        for image in morphism_images:
            if image[i] == bookend[i]:
                pass_count += 1
        if pass_count == 0:
            return True
        elif pass_count != len(morphism_images):
            return False
        
# If r' shares the same common suffix with all images (ie. They stop sharing prefixes at the same index.)
def is_left_bookend_ideal(morphism_images, bookend):
    for i in range(1, len(bookend)+1):
        pass_count = 0
        for image in morphism_images:
            if image[-i] == bookend[-i]:
                pass_count += 1
        if pass_count == 0:
            return True
        elif pass_count != len(morphism_images):
            return False
