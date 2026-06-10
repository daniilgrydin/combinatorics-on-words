from combinatorics.morphism import dict_to_morphism

from typing import Iterable, Any

def de_bruijn(k: Iterable[str] | int, n: int) -> str:
    """de Bruijn sequence for alphabet k
    and subsequences of length n.
    from Wikipedia
    """
    # Two kinds of alphabet input: an integer expands
    # to a list of integers as the alphabet..
    if isinstance(k, int):
        alphabet = list(map(str, range(k)))
    else:
        # While any sort of list becomes used as it is
        alphabet = k
        k = len(k)

    a = [0] * k * n
    sequence = []

    def db(t, p):
        if t > n:
            if n % p == 0:
                sequence.extend(a[1 : p + 1])
        else:
            a[t] = a[t - p]
            db(t + 1, p)
            for j in range(a[t - p] + 1, k):
                a[t] = j
                db(t + 1, t)

    db(1, 1)
    return "".join(alphabet[i] for i in sequence)

def get_left_period(images):
    for i in range(len(images[0])):
        try:
            siblings = [img[i] for img in images]
        except:
            return images[0][:i]
        if len(set(siblings)) > 1: # there are atleast two different letters in siblings
            return images[0][:i]
    return images[0]

def get_right_period(images):
    return get_left_period([img[::-1] for img in images])[::-1]

def get_tr(images, left, right, pre_alphabet):
    morphism = dict_to_morphism({
        pre_alphabet[i]: images[i] for i in range(len(images))
    })
    debru = de_bruijn(pre_alphabet, 2)
    master_word = left + morphism(debru) + right
    
    left_period = left + get_left_period(images)
    
    common_suffixes = images.copy()
    common_suffixes.append(left)
    common_suffix = get_right_period(common_suffixes)
    
    start = len(left) - len(common_suffix) - 1
    
    for end in range(start, len(left_period)):
        possible_tr = left_period[start:end]
        if (master_word.count(possible_tr) <= 1
            and all([(left + morphism(c) + right).count(possible_tr) <= 1 for c in pre_alphabet])
        ):
            return possible_tr
    return ""

def get_ts(images, left, right, pre_alphabet):
    new_images = [img[::-1] for img in images]
    left = left[::-1]
    right = right[::-1]
    return get_tr(new_images, right, left, pre_alphabet)[::-1]

def get_trts(images, left, right, pre_alphabet):
    return (
        get_tr(images, left, right, pre_alphabet),
        get_ts(images, left, right, pre_alphabet)
    )