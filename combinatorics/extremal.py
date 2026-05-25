# a word is extremal with respect to some criteria if it satisfies that criteria,
# but no extension does
def is_extremal(word, alphabet, filter):
    from .word import get_extensions

    # if not filter(word):
    #     return False

    extensions = get_extensions(word, alphabet)
    for extension in extensions:
        print(extension)
        if filter(extension):
            return False

    return True

# a word is nearly extremal with respect to some criteria if it satisfies that criteria,
# and only two extensions (one left extension and one right) also satisfy that criteria
def is_nearly_extremal(word, alphabet, filter):
    from .word import get_extensions
    from .exponent import get_critical_exponent

    print("checking self")
    if not filter(word):
        return False

    print("checking middle")
    # checking the inside extensions
    extensions = get_extensions(word, alphabet, range(1, len(word)))
    for extension in extensions:
        if filter(extension):
            print(f"The word:\t\t{word}\nhas an extextension:\t{extension}")
            print(f"with power {get_critical_exponent(extension)}")
            return False
    
    print("checking left")
    # checking the left extensions
    found_left_extension = False
    left_extensions = get_extensions(word, alphabet, [1])
    for extension in left_extensions:
        if filter(extension):
            if found_left_extension:
                return False
            found_left_extension = True
    if not found_left_extension: return False
    
    print("checking right")
    # checking the right extensions
    found_right_extension = False
    right_extensions = get_extensions(word, alphabet, [len(word)])
    for extension in right_extensions:
        if filter(extension):
            if found_right_extension:
                return False
            found_right_extension = True
    if not found_right_extension: return False

    return True

def is_extremal_alpha_free(word, alpha, alphabet):
    from .word import get_extensions
    from .exponent import is_exponent_free, get_critical_exponent

    print("checking self")
    if not is_exponent_free(word, alpha):
        return False

    print("checking middle")
    # checking the inside extensions
    extensions = get_extensions(word, alphabet, range(1, len(word)))
    for extension in extensions:
        if is_exponent_free(extension, alpha):
            print(f"extension {extension}\n\thas exponent {get_critical_exponent(extension)}<{alpha}")
            return False
    
    print("checking left")
    # checking the left extensions
    found_left_extension = False
    left_extensions = get_extensions(word, alphabet, [1])
    for extension in left_extensions:
        if is_exponent_free(extension, alpha):
            if found_left_extension:
                return False
            found_left_extension = True
    if not found_left_extension: return False
    
    print("checking right")
    # checking the right extensions
    found_right_extension = False
    right_extensions = get_extensions(word, alphabet, [len(word)])
    for extension in right_extensions:
        if is_exponent_free(extension, alpha):
            if found_right_extension:
                return False
            found_right_extension = True
    if not found_right_extension: return False

    return True