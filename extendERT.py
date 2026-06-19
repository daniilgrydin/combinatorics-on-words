import tools.file_rw as rw

BETA_FREE_FILE_NAME             = "beta-free_words.txt" 
CRITICAL_WORDS_FILE_NAME        = "critical_words.txt"
NEARLY_EXTREMAL_FILE_NAME       = "nearly_extremal.txt"
MORPHISMS_DIRECTORY_NAME        = "morphisms"
CONSTRUCTIONS_DIRECTORY_NAME    = "constructions"
Q_MORPHISM_FILE_NAME            = lambda morph_dir, q: morph_dir + '/' + str(q) + "-uniform_morphism.txt"
IDEAL_CONSTRUCTION_FILE_NAME    = lambda const_dir, q:const_dir + '/' + str(q) + "-uniform_ideal_constructions.txt"


def setup_extension_folder(full_path, name):
    import os

    extension_directory = full_path + "/" + name + "/"
    beta_free_path          = extension_directory + BETA_FREE_FILE_NAME
    critical_words_path     = extension_directory + CRITICAL_WORDS_FILE_NAME
    nearly_extremal_path    = extension_directory + NEARLY_EXTREMAL_FILE_NAME
    morphisms_directory     = extension_directory + MORPHISMS_DIRECTORY_NAME
    constructions_directory = extension_directory + CONSTRUCTIONS_DIRECTORY_NAME

    os.mkdir(extension_directory)
    open(beta_free_path, 'x')
    open(critical_words_path, 'x')
    open(nearly_extremal_path, 'x')
    os.mkdir(morphisms_directory)
    os.mkdir(constructions_directory)

    return extension_directory

def get_input(prompt, pass_filter):
    recieved = input(prompt + '\n')
    while not pass_filter(recieved):
        received = input(prompt + "\n")
    return received


def extendERT(alphabet, alpha, beta, gamma, alpha_free_words_file, extension_directory):
    from combinatorics.word import generate_greedy_words, bucket_words_by_length
    from combinatorics.exponent import is_suffix_exponent_free, get_words_with_critical_exponent, Rational
    from tools.construction_search_tools import generate_critical_nearly_extremal, find_morphisms, find_ideal_constructions
    import os

    beta_free_file = extension_directory + BETA_FREE_FILE_NAME
    beta_free_words = rw.load_words(beta_free_file)

    critical_words_file = extension_directory + CRITICAL_WORDS_FILE_NAME
    critical_words = rw.load_words(critical_words_file)

    nearly_extremal_file = extension_directory + NEARLY_EXTREMAL_FILE_NAME
    nearly_extremal = rw.load_words(nearly_extremal_file)

    preimages = rw.load_words(alpha_free_words_file)

    morphism_directory = extension_directory + MORPHISMS_DIRECTORY_NAME
    constructions_direction = extension_directory + CONSTRUCTIONS_DIRECTORY_NAME

    largest_prefix = '010210120210201202'
    largest_suffix = '020120210201210212'
    size_prefix_suffix = 12

    print("\n------------------------------------------------------------")
    print(f"1. Generating {beta}-free words.")
    print("------------------------------------------------------------")

    if len(beta_free_words) == 0:
        beta_free_words = generate_greedy_words(alphabet, 1, lambda w: is_suffix_exponent_free(w, beta))
        existing_length = 1
    else:
        existing_length = len(max(beta_free_words, key=len))

    print(f"{len(beta_free_words)} {beta}-free words loaded up to length {existing_length}.")
    to_generate = get_input("Up to what length should be generated? (Enter -1 to generate none.)",
        lambda recieved: recieved.isnumeric() and int(recieved) >= -1)

    for i in range(existing_length + 1, to_generate + 1):
        print("Generating length", i)
        beta_free_words = generate_greedy_words(alphabet, 1, lambda w: is_suffix_exponent_free(w, beta), beta_free_words)
        rw.append_words(beta_free_words, beta_free_file)

    print("\n------------------------------------------------------------")
    print(f"2. Generating critical words.")
    print("------------------------------------------------------------")

    existing_length = len(max(critical_words, key=len))
    crit = Rational(beta.rational.numerator, beta.rational.denominator)

    print(f"{len(critical_words)} critical words loaded up to length {existing_length}.")
    print(f"Generating multiples of {crit.numerator}.")
    to_generate = get_input("How many multiples to generate? (-1 to generate none.)",
        lambda recieved: recieved.isnumeric() and int(recieved) >= -1)

    if to_generate >= 1:
        critical_words = get_words_with_critical_exponent(crit, 
                                        max_multiple=to_generate,
                                        beta_free_words=beta_free_words, 
                                        output_file=critical_words_file, 
                                        do_print=True)

    print("\n------------------------------------------------------------")
    print(f"3. Generating nearly extremal words.")
    print("------------------------------------------------------------")

    existing_length = len(max(nearly_extremal, key=len))

    print(f"{len(nearly_extremal)} critical words loaded up to length {existing_length}.")
    to_generate = get_input("Up to what inside length should be generated? (-1 to generate none.)",
        lambda recieved: recieved.isnumeric() and int(recieved) >= -1)
    prefix = get_input("What prefix should be used?",
        lambda recieved: recieved.isnumeric())
    suffix = get_input("What suffix should be used?",
        lambda recieved: recieved.isnumeric())
    
    for q in range(existing_length, to_generate + 1):
        nearly_extremal = generate_critical_nearly_extremal(alphabet, q, beta, 
                                beta_free_file, critical_words=critical_words,
                                prefixes=[prefix], 
                                suffixes=[prefix],
                                output_path=nearly_extremal_file)


    print("\n------------------------------------------------------------")
    print(f"4. Finding morphisms.")
    print("------------------------------------------------------------")

    find_morphisms_stop = get_input("How many morphisms to sample? (-1 to sample none.)",
        lambda recieved: recieved.isnumeric() and int(recieved) >= -1) + 1
    morphisms_to_check = get_input("Max morphisms to check?",
        lambda recieved: recieved.isnumeric() and int(recieved) >= 0)

    for i in range(1, rw.max_word_length_in_file(nearly_extremal_file) + 1):
        find_morphisms(alphabet, beta, i, preimages=preimages,
                    nearly_extremal_words=bucket_words_by_length(nearly_extremal)[i], 
                    output_file=MORPHISMS_DIRECTORY_NAME(extension_directory, i), 
                    to_check=morphisms_to_check, STOP=find_morphisms_stop)

    print("\n------------------------------------------------------------")
    print(f"5. Finding ideal constructions.")
    print("------------------------------------------------------------")

    morphism_files = os.listdir(morphism_directory)
    lengths_to_check = []
    for m in morphism_files:
        lengths_to_check.append(m[m.rfind('/')+1:m.rfind('-')])

    # The algorithm for finding bookends needs to be improved. It should be time based and
    # look through the smallest lengths of bookends first.

    # for q in lengths_to_check:
    #     ideal = find_ideal_constructions(morphism_images_file=Q_MORPHISM_FILE_NAME(morphism_directory, q), 
    #                                 max_bookend_size=q, min_A_size=8, 
    #                                 beta_free_words_file = beta_free_file,
    #                                 get_exponents=True, 
    #                                 output_file=ideal_construction_file_name(q))

    # 6

    # check_proposition({'0':'0102101202102012021012010210120210201021202102012101202120121020120210201210212',
    #     '1':'0102101202102012021012010201210120210201021202102012102120121020120210201210212',
    #     '2':'0102101202102012021012010201210212021012102120102012102120121020120210201210212',
    #     '3':'0102101202102012021012010212012102120102101202102012102120121020120210201210212'},
    #     '01021012021020120210120102101202102012021201020120210201210212',
    #     '01021012021020120212010201202102012102120121020120210201210212',
    #     "012",
    #     "0123",
    #     ExtendedReal(7,5,True),
    #     ExtendedReal(15,8,True),
    #     ExtendedReal(21,11,False),
    #     '01020120210201210212010',
    #     '21201021012021020120212')