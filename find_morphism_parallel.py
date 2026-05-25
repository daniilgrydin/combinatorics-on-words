from combinatorics.word import generate_greedy_words_unique
from combinatorics.exponent import is_suffix_exponent_free, ExtendedReal, is_exponent_free
from combinatorics.extremal import is_nearly_extremal
from combinatorics.morphism import dict_to_morphism, is_synchronizing

from itertools import combinations
from concurrent.futures import ProcessPoolExecutor
from functools import partial
import time

def check_valid_morphism(tuple, quaternary_images, alpha):
        H0, H1, H2, H3 = tuple
        morphism = dict_to_morphism({
            "0": H0,
            "1": H1,
            "2": H2,
            "3": H3
        })
        if not is_synchronizing(morphism, "0123"): return False

        for q in quaternary_images:
            if not is_exponent_free(morphism(q), alpha): return False

        return True

if __name__ == "__main__":

    alphabet = "012"

    alpha = ExtendedReal(7, 5, True) # quaternary
    beta = ExtendedReal(7, 4, True) # ternary

    quaternary_images = []

    with open("data/75_free_quaternary_words.txt", "r") as f:
        for q in f.readlines():
            if len(q) > 1:
                quaternary_images.append(q.strip())

    unique = generate_greedy_words_unique(
        alphabet,
        1,
        partial(is_suffix_exponent_free, target_exponent=beta)
    )
    print("len\tcount\tgen_t\tchk_t\tmorhp")

    for length in range(len(unique[0])+1, 100):
        start = time.time()
        unique = generate_greedy_words_unique(
            alphabet,
            1,
            partial(is_suffix_exponent_free, target_exponent=beta),
            seed=unique
        )

        nearly_extremal = [
            word
            for word in unique
            if
            word[-1] != "0"
            and is_nearly_extremal(
                word,
                alphabet,
                lambda w: is_exponent_free(w, beta))]

        print(f"  {length}\t  {len(nearly_extremal)}\t{round(time.time()-start,1)}s", end="\t")
        start = time.time()
        # print(f"There are {(len(nearly_extremal))*(len(nearly_extremal)-1)*(len(nearly_extremal)-2)*(len(nearly_extremal)-3)} permutations of them.")
        # for i in range(0, len(nearly_extremal), max(1, len(nearly_extremal)//5)):
        #     print(color_word(nearly_extremal[i], alphabet))
        
        combos = list(combinations(nearly_extremal, 4))
        morphisms_count = 0
        with ProcessPoolExecutor(16) as pool:
            results = list(pool.map(partial(check_valid_morphism, quaternary_images=quaternary_images, alpha=alpha), combos, chunksize=10000))
            if any(results):
                print("Found morphism!")
            morphisms_count = results.count(True)
            
        # for combo in combinations(nearly_extremal, 4):
        #     # if not is_synchronizing(morphism): continue
            
        #     if not check_valid_morphism(combo): continue
        #     print("Found morphism!\a")
        #     print("0", combo[0])
        #     print("1", combo[1])
        #     print("2", combo[2])
        #     print("3", combo[3])
        #     print()
        #     break
        print(f"{round(time.time()-start,1)}s\t  {morphisms_count}")