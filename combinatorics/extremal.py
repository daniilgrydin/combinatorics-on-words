# a word is extremal with respect to some criteria if it satisfies that criteria,
# but no extension does
def is_extremal(word, alphabet, filter):
    from .word import get_extensions

    # if not filter(word):
    #     return False

    extensions = get_extensions(word, alphabet)
    for extension in extensions:
        if filter(extension):
            return False

    return True

# a word is nearly extremal with respect to some criteria if it satisfies that criteria,
# and only two extensions (one left extension and one right) also satisfy that criteria
def is_nearly_extremal(word, alphabet, filter):
    from .word import get_extensions

    if not filter(word):
        return False

    # checking the inside extensions
    extensions = get_extensions(word, alphabet, range(1, len(word)-1))
    for extension in extensions:
        if filter(extension):
            return False
    
    # checking the left extensions
    found_left_extension = False
    left_extensions = get_extensions(word, alphabet, [1])
    for extension in left_extensions:
        if filter(extension):
            if found_left_extension:
                return False
            found_left_extension = True
    
    # checking the right extensions
    found_right_extension = False
    right_extensions = get_extensions(word, alphabet, [len(word)-1])
    for extension in right_extensions:
        if filter(extension):
            if found_right_extension:
                return False
            found_right_extension = True

    return True