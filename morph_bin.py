from combinatorics.word import generate_greedy_words_unique
from combinatorics.exponent import is_suffix_exponent_free, ExtendedReal, is_exponent_free
from combinatorics.extremal import is_nearly_extremal
from combinatorics.morphism import dict_to_morphism, is_synchronizing

from itertools import combinations
from concurrent.futures import ProcessPoolExecutor
from functools import partial
import time

def check_valid_morphism(tuple, quaternary_images, alpha):
        H0, H1, H2 = tuple
        morphism = dict_to_morphism({
            "0": H0,
            "1": H1,
            "2": H2
        })
        if not is_synchronizing(morphism, "012"): return False

        for q in quaternary_images:
            if not is_exponent_free(morphism(q), alpha): return False

        return True

if __name__ == "__main__":
    start = time.time()

    from_alphabet = "012"
    to_alphabet = "01"

    from_exponent = ExtendedReal(2, 1, False) # ternary
    to_exponent = ExtendedReal(17, 7, True) # binary

    quaternary_images = []

    with open("data/square-free-ternary-words.txt", "r") as f:
        for q in f.readlines():
            if len(q) > 1:
                quaternary_images.append(q.strip())

    unique = [""]
    print("len\tcount\tgen_t\tchk_t\tmorph")
    for length in range(len(unique[0])+1, 100):
        unique = generate_greedy_words_unique(
            to_alphabet,
            1,
            partial(is_suffix_exponent_free, target_exponent=to_exponent),
            seed=unique
        )

        nearly_extremal = [
            word
            for word in unique
            if
            # word[-1] != "0"
            is_nearly_extremal(
                word,
                to_alphabet,
                lambda w: is_exponent_free(w, to_exponent))]
        
        print(nearly_extremal)
    
        print(f"  {length}\t  {len(nearly_extremal)}\t{round(time.time()-start,1)}s", end="\t")
        start = time.time()
        # print(f"There are {(len(nearly_extremal))*(len(nearly_extremal)-1)*(len(nearly_extremal)-2)*(len(nearly_extremal)-3)} permutations of them.")
        # for i in range(0, len(nearly_extremal), max(1, len(nearly_extremal)//5)):
        #     print(color_word(nearly_extremal[i], alphabet))
        
        combos = list(combinations(nearly_extremal, 3))
        with ProcessPoolExecutor(16) as pool:
            results = list(pool.map(partial(check_valid_morphism, quaternary_images=quaternary_images, alpha=from_exponent), combos, chunksize=10000))
            if any(results):
                print("Found morphism!")
            morphisms_count = results.count(True)
        print(f"{round(time.time()-start,1)}s\t  {morphisms_count}")