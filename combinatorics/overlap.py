def get_overlaps(word):
    overlaps = []
    for x_length in range((len(word) - 3) // 2 + 1):
        max_start = len(word) - 2 * x_length - 3
        for start in range(max_start + 1):
            a1 = word[start]
            a2 = word[start + x_length + 1]
            a3 = word[start + 2 * x_length + 2]

            x1 = word[start + 1 : start + x_length + 1]
            x2 = word[start + x_length + 2 : start + 2 * x_length + 2]

            # check if the chunk is of form: axaxa
            if a1 == a2 and a1 == a3 and x1 == x2:
                combo = word[start : start + 2 * x_length + 3]
                if combo not in overlaps:
                    overlaps.append(combo)
    return sorted(overlaps, key=len)

def is_overlap_free(word):
    for x_length in range((len(word) - 3) // 2 + 1):
        max_start = len(word) - 2 * x_length - 3
        for start in range(max_start + 1):
            a1 = word[start]
            a2 = word[start + x_length + 1]
            a3 = word[start + 2 * x_length + 2]

            x1 = word[start + 1 : start + x_length + 1]
            x2 = word[start + x_length + 2 : start + 2 * x_length + 2]
            # check if a's are correct in place: axaxa
            if a1 == a2 and a1 == a3 and x1 == x2:
                return False
    return True
