import time
from libraries.methods import *
import random

def extremal_wrapped(word):
    global alphabet
    return SQUARE.is_extremal(word, alphabet)

def benchmark(function, input_generator, rng, trials_per_value):
    times = {}
    for val in rng:
        local_time = 0
        for _ in range(trials_per_value):
            input = input_generator(val)
            start = time.time()
            function(input)
            end = time.time()
            local_time += end-start
        terminated = str(round(local_time/trials_per_value, 5)) + "s"
        times[val] = terminated
        print(val, ":", terminated)
    return times


alphabet = "abc"
# inputs = [("".join(random.choices(alphabet, k=3**i)), alphabet) for i in range(5,20)]
# inputs = [(alphabet*(3**i//len(alphabet)), alphabet) for i in range(5,20)]
# print(inputs)

generator = lambda length : "".join(random.choices(alphabet, k=length))

print("Benchmarking...")
bench = benchmark(extremal_wrapped, generator, [3**i for i in range(5, 18)], 15)

for val in bench:
    print(val, ":", bench[val])
