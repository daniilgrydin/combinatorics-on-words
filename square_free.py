from combinatorics.square import is_square_free
from combinatorics.word import generate_greedy_words


with open("data/square-free-ternary.txt", "w") as f:
    unique = generate_greedy_words("012", 1, is_square_free)
    f.write("\n".join(unique)+"\n")
    for i in range(9):
        unique = generate_greedy_words("012", 1, is_square_free, seed=unique)
        f.write("\n".join(unique)+"\n")
    
print("done")