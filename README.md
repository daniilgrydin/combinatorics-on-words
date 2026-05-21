# Combinatorics on Words

Table of Contents:

1. [[##Resources]]
2. [[##Usage]]
3. [[Documentation]]

## Resources

This repository contains implementations of definitions and proofs from multiple sources regarding combinatorics on words. Following material was looked into:

1) Combinatorics on Words: Christoffel Words and Repetitions in Words
    - Found in [BLRS2008](BLRS2008)
2) [Extremal overlap-free and extremal beta-free words](https://arxiv.org/abs/2006.10152)
    - Found in [MRS2020](MRS2020)
    - Proof of the Proposition 22: `python -m MRS2020.proposition22`
3) [Extremal Square-free Words](https://arxiv.org/abs/1910.06226)
    - Found in [GKN2020](GKN2020)
    - See all computational proofs: `python -m GKN2020.proofs`
4) [Lengths of extremal square-free ternary words](https://arxiv.org/pdf/2001.11763)
    - Found in [MR2020](MR2020)

## Usage

In the [libraries](libraries) folder you will find python files each filled with supplementary functions related to that files topic.

In the root there is a file `example.py` with following contents:

```py
from combinatorics.word import generate_greedy_words
from combinatorics.square import has_square_suffix, is_square_free
from combinatorics.extremal import is_extremal

words = generate_greedy_words("012", 25, lambda w: not has_square_suffix(w))

for word in words:
    if is_extremal(word, "012", is_square_free):
        print("found an extremal square-free ternary word of length 25:")
        print(word)
        break

print("Done!")
```

To test this file simply run:

```bash
python -m example
```

## Documentation

### `combinatorics` module
