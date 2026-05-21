# Combinatorics on Words

## Usage

In the [libraries](libraries) folder you will find python files each filled with supplementary functions related to that files topic.

For example, if you want to find a square free ternary word of length 12 where each extension contains an overlap, it can be achieved with following code:

```py
from libraries.word import generate_greedy_words, get_factors
from libraries.square import has_square_suffix
from libraries.overlap import is_overlap_free

words = generate_greedy_words("012", 12, has_square_suffix)

for word in words:
    
    factors = get_factors(word)
    has_overlap_free_factor = False
    
    for factor in factors:
        if is_overlap_free(factor):
            has_overlap_free_factor = True
            break

    if not has_overlap_free_factor:
        print("found a square-free ternary word of length 12 where every extension creates an overlap:")
        print(word)
        break
```

## Resources

This repository contains implementations of definitions and proofs from multiple sources regarding combinatorics on words. Following material was looked into:

1) Combinatorics on Words: Christoffel Words and Repetitions in Words
    - Found in [BLRS2008](BLRS2008)
2) [Extremal overlap-free and extremal beta-free words](https://arxiv.org/abs/2006.10152)
    - Found in [MRS2020](MRS2020)
3) [Extremal Square-free Words](https://arxiv.org/abs/1910.06226)
    - Found in [GKN2020](GKN2020)
4) [Lengths of extremal square-free ternary words](https://arxiv.org/pdf/2001.11763)
    - Found in [MR2020](MR2020)
