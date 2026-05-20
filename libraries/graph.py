import networkx as nx
import matplotlib.pyplot as plt

def permute(word, cycle):
    new_word = ""
    for c in word:
        if c not in cycle:
            new_word += c
            continue
        index = (cycle.find(c) + 1) % len(cycle)
        new_word += cycle[index]
    return new_word

def get_variations(word):
    per_ab = permute(word, "ab")
    per_ac = permute(word, "ac")
    per_bc = permute(word, "bc")
    per_abc = permute(word, "abc")
    per_acb = permute(word, "acb")
    return {
        word: "N",
        per_ab: "N_ab",
        per_ac: "N_ac",
        per_bc: "N_bc",
        per_abc: "N_abc",
        per_acb: "N_acb",
        word[::-1]: "~N",
        per_ab[::-1]: "~N_ab",
        per_ac[::-1]: "~N_ac",
        per_bc[::-1]: "~N_bc",
        per_abc[::-1]: "~N_abc",
        per_acb[::-1]: "~N_acb",
    }


def construct_thue_digraph(words):
    from .square import is_nearly_extremal_square_free
    digraph = nx.DiGraph()
    digraph.add_nodes_from(words.keys())
    for B1 in words:
        for B2 in words:
            if B1 == B2:
                continue
            if is_nearly_extremal_square_free(B1 + B2):
                digraph.add_edge(B1, B2)
    return digraph

def get_square_free_paths(digraph: nx.DiGraph, length):
    paths = [[node] for node in digraph.nodes(data=False)]
    new_paths = []
    
    for _ in range(length-1):
        for path in paths:
            for suc in digraph.successors(path[-1]):
                if (
                    (len(path) > 0 and suc == path[0])
                    or
                    (len(path) > 1 and suc == path[1])
                ): continue
                new_paths.append(path.copy())
                new_paths[-1].append(suc)
        paths = new_paths
        new_paths = []
    return paths

def is_thue_digraph(digraph: nx.DiGraph):
    from .square import is_square_free
    nodes = digraph.nodes()
    for B1 in nodes:
        for B2 in nodes:
            if B1 == B2: continue
            
            #? (2) check that no block is a factor of another block
            if B1 in B2:
                print(f"Block\n{B1}\nIs contained in\n{B2}")
                return False
            
            # if length of B1 is 1 and each block is unique (by above)
            # than there is no reason to check for splicing
            if len(B1) > 1:continue
            
            #? (1) check that B1 and B2 cannot be spliced to create another block
                # assuming that B1 and B2 have same length
            for start in range(1, len(B1)-1):
                for end in range(len(B1)):
                    if B1[:start] + B2[end:] in nodes:
                        print(f"Block\n{B1}\nAnd\n{B2}\nCan be spliced into\n{B1[:start] + B2[end:]}\nWhich is in the graph")
                        return False
    
    #? (3) check that no 
    for path in get_square_free_paths(digraph, 3):
        if not is_square_free("".join(path)):
            print(f"Path\n{"\t".join(path)}\nIs not square free")
            return False

    return True
    
# def lemma_7_walk_satisfies_parittion(walk, partition):
#     starting_part = -1
#     for i, node in enumerate(walk):
#         if i == 0:
#             starting_part = partition[node]
#             continue

#         if partition[node] != starting_part and i != len(walk)-1:
#             return False
#     return True

def lemma_7_find_walk(G:nx.DiGraph, start, end, partition):
    if start == end:
        return [start]
    walks = [[start]]
    new_walks = []
    for _ in range(G.number_of_nodes()):
        for walk in walks:
            last = walk[-1]
            for next in G.successors(last):
                if next in walk:
                    continue
                if next == end:
                    walk.append(end)
                    return walk
                if partition[next] != partition[start]:
                    continue
                new_walk = walk.copy()
                new_walk.append(next)
                new_walks.append(new_walk)
        walks = new_walks
        new_walks = []
    raise RuntimeError("There is no path.")

def lemma_7_all_pairs_have_walks(G, partition, printing=False, prefix="", permutations={}):
    achievability = {}
    for start in G.nodes():
        for end in G.nodes():
            try:
                if start == end: continue
                walk = lemma_7_find_walk(G, start, end, partition)
            except:
                continue
            nav = f"{partition[start]}>{partition[end]}"
            if nav not in achievability.keys():
                achievability[nav] = walk
                if printing:
                    print(
                        prefix + f"({nav})\t" +
                        "\t->\t".join([permutations[node] for node in walk])    
                    )
    groups = set(partition.values())
    for from_group in groups:
        for to_group in groups:
            if f"{from_group}>{to_group}" not in achievability.keys():
                return False
    return True

def main():
    from .square import is_nearly_extremal_square_free
    # Digraph from the paper "Extremal Square-free Words", Lemma 4 page 5
    N = "abacbabcabacbcacbabcabacabcbabcabacbcabcb"
    Q = "cbacbcabacbabcabacbcabcbacbc"
    R = "acabcacbabcabacbcabcbacabacbcabcb"
    permutations_of_N = get_variations(N)
    G = construct_thue_digraph(permutations_of_N)
    # print(is_thue_digraph(G))
    # G.add_node("")
    print(
        "\n".join([
            "\t".join([
                permutations_of_N[node] for node in path
            ])
            + f"\tis{" " if is_nearly_extremal_square_free("".join(path)) else " not "}square-free"
            # + f"\t{"".join(path)}"
            for path in get_square_free_paths(G, 3)
        ])
    )

    # print(get_all_paths(G, 3))
    # nx.draw_kamada_kawai(
    #     G,
    #     with_labels=True,
    #     node_color="lightblue",
    #     font_weight="bold",
    #     labels=permutations_of_N,
    # )
    # plt.show()


if __name__ == "__main__":
    main()