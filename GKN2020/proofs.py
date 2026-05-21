from ..package.square import is_square_free, is_nearly_extremal_square_free
from ..package.graph import get_variations, construct_thue_digraph, is_thue_digraph, lemma_7_all_pairs_have_walks
import networkx as nx
import matplotlib.pyplot as plt

def proof_lemma_3():
    print("\t\t-=-=-\033[43m\033[30m Lemma 3 \033[0m-=-=-")
    print("\tThe word N is nearly extremal and the only \n\tsquare free extensions are cN and Na.\n")
    
    N = "abacbabcabacbcacbabcabacabcbabcabacbcabcb"
    nearly_extremal = is_nearly_extremal_square_free(N)
    left_extension = 'c' + N
    right_extension = N + 'a'
    print(f"N = {N}")
    print(f"is N nearly-extremal?\t{nearly_extremal}")
    print(f"is cN square free?\t{is_square_free(left_extension)}")
    print(f"is Na square free?\t{is_square_free(right_extension)}")

def proof_lemma_4():
    print("\t\t-=-=-\033[43m\033[30m Lemma 4 \033[0m-=-=-")
    print("\tThe digraph D_N is a Thue digraph.\n")
    
    N = "abacbabcabacbcacbabcabacabcbabcabacbcabcb"
    print(f"N = {N}")
    permutations_of_N = get_variations(N)
    G = construct_thue_digraph(permutations_of_N)
    if input("show the D_N digraph (y/n):").lower() == "y":
        nx.draw_kamada_kawai(
            G,
            with_labels=True,
            node_color="lightblue",
            font_weight="bold",
            labels=permutations_of_N,
        )
        plt.show()
    print(f"is D_N a Thue Digraph: {is_thue_digraph(G)}")
        
def proof_corollary_5():
    print("\t\t-=-=-\033[101m\033[30m Corollary 5 \033[0m-=-=-")
    print("\tAll words in S(D_N) are nearly extremal.\n")
    N = "abacbabcabacbcacbabcabacabcbabcabacbcabcb"
    print(f"N = {N}")
    permutations_of_N = get_variations(N)
    G = construct_thue_digraph(permutations_of_N)
    print("Part of the proof is to show that for any two\nconsecutive blocks B1 and B2 in D_N, B1+B2 is nearly extremal.")
    print("Every pair B1+B2:")
    for edge in G.edges():
        print(f"{permutations_of_N[edge[0]]}\t+\t{permutations_of_N[edge[1]]}\tis {"nearly extremal" if is_nearly_extremal_square_free(edge[0]+edge[1]) else "not nearly extremal"}")
    
def proof_lemma_8():
    print("\t\t-=-=-\033[43m\033[30m Lemma 8 \033[0m-=-=-")
    print("\tShow that the following partition\n\tof V(D_N) satisfies (*) of Lemma 7:")
    print("\t\tV_1 = {N, N_bc, ~N, ~N_bc}")
    print("\t\tV_2 = {N_ab, N_abc, ~N_ab, ~N_abc}")
    print("\t\tV_3 = {N_ac, N_acb, ~N_ac, ~N_acb}\n")
    N = "abacbabcabacbcacbabcabacabcbabcabacbcabcb"
    print(f"N = {N}\n")
    permutations_of_N = get_variations(N)
    G = construct_thue_digraph(permutations_of_N)
    name_to_permutation = {permutations_of_N[key]: key for key in permutations_of_N.keys()}
    partition = {
        name_to_permutation["N"]: "V_1",
        name_to_permutation["N_bc"]: "V_1",
        name_to_permutation["~N"]: "V_1",
        name_to_permutation["~N_bc"]: "V_1",
        
        name_to_permutation["N_ab"]: "V_2",
        name_to_permutation["N_abc"]: "V_2",
        name_to_permutation["~N_ab"]: "V_2",
        name_to_permutation["~N_abc"]: "V_2",
        
        name_to_permutation["N_ac"]: "V_3",
        name_to_permutation["N_acb"]: "V_3",
        name_to_permutation["~N_ac"]: "V_3",
        name_to_permutation["~N_acb"]: "V_3"
    }
    print(f"\nSatisfies Lemma 7?\t{lemma_7_all_pairs_have_walks(G, partition, True, "", permutations_of_N)}")
    

def proof_lemma_10():
    print("\t\t-=-=-\033[43m\033[30m Lemma 10 \033[0m-=-=-")
    print("\tThe words QN and NR are square free,\n\tand their only extensions are QNa and cNR.\n")
    
    N = "abacbabcabacbcacbabcabacabcbabcabacbcabcb"
    Q = "cbacbcabacbabcabacbcabcbacbc"
    R = "acabcacbabcabacbcabcbacabacbcabcb"
    print(f"N = {N}")
    print(f"Q = {Q}")
    print(f"R = {R}")
    print("QN:")
    print(f"\tis QNa square free?\t{is_square_free(Q+N+"a")}")
    print(f"\tis QNb square free?\t{is_square_free(Q+N+"b")}")
    print(f"\tis QNc square free?\t{is_square_free(Q+N+"c")}")
    print(f"\tis aQN square free?\t{is_square_free("a"+Q+N)}")
    print(f"\tis bQN square free?\t{is_square_free("b"+Q+N)}")
    print(f"\tis cQN square free?\t{is_square_free("c"+Q+N)}")
    print("NR:")
    print(f"\tis NRa square free?\t{is_square_free(N+R+"a")}")
    print(f"\tis NRb square free?\t{is_square_free(N+R+"b")}")
    print(f"\tis NRc square free?\t{is_square_free(N+R+"c")}")
    print(f"\tis aNR square free?\t{is_square_free("a"+N+R)}")
    print(f"\tis bNR square free?\t{is_square_free("b"+N+R)}")
    print(f"\tis cNR square free?\t{is_square_free("c"+N+R)}")

def proof_lemma_11():
    print("\t\t-=-=-\033[43m\033[30m Lemma 11 \033[0m-=-=-")
    print("\tThe digraph D*_N is a Thue digraph.\n")
    N = "abacbabcabacbcacbabcabacabcbabcabacbcabcb"
    Q = "cbacbcabacbabcabacbcabcbacbc"
    R = "acabcacbabcabacbcabcbacabacbcabcb"
    print(f"N = {N}")
    print(f"Q = {Q}")
    print(f"R = {R}")
    permutations_of_N = get_variations(N)
    G = construct_thue_digraph(permutations_of_N)
    G.add_edge(Q, N)
    G.add_edge(N, R)
    permutations_of_N[Q] = "Q"
    permutations_of_N[R] = "R"
    if input("show the D*_N digraph (y/n):").lower() == "y":
        nx.draw_kamada_kawai(
            G,
            with_labels=True,
            node_color="lightblue",
            font_weight="bold",
            labels=permutations_of_N,
        )
        plt.show()
    print(f"is D*_N a Thue Digraph: {is_thue_digraph(G)}")

def proof_conjecture_14():
    print("\t\t-=-=-\033[46m\033[30m Conjecture 13 \033[0m-=-=-")
    print("\tGenerate a nonchalant word of arbitrary length.")
    
def proof_conjecture_15():
    print("\t\t-=-=-\033[46m\033[30m Conjecture 13 \033[0m-=-=-")
    print("\tThe sequence of nonchalant words\n\tover an alpabet of size k converges to\n\tan infinite words for every k>2.")

if __name__ == "__main__":
    print("Starting proofs...\n")
    proof_lemma_3()
    print("\t"*6, "\033[42m\033[30m □ \033[0m\n\n")
    proof_lemma_4()
    print("\t"*6, "\033[42m\033[30m □ \033[0m\n\n")
    proof_corollary_5()
    print("\t"*6, "\033[42m\033[30m □ \033[0m\n\n")
    proof_lemma_8()
    print("\t"*6, "\033[42m\033[30m □ \033[0m\n\n")
    proof_lemma_10()
    print("\t"*6, "\033[42m\033[30m □ \033[0m\n\n")
    proof_lemma_11()
    print("\t"*6, "\033[42m\033[30m □ \033[0m\n\n")
    proof_conjecture_14()
    print("\n\n")
    proof_conjecture_15()
    print("\n\n")
