from tools.decomposition import TernaryConstructionDecomposition
from typing import List

def load_words(file_path):
    result = []
    for line in open(file_path, 'r').readlines():
        result.append(line.strip())
    return result

def save_words(words, file_path):
    with open(file_path, 'w') as f:
        f.write('\n'.join(words))

def load_words_by_length(file_path):
    result = [['']]
    n = 0
    for line in open(file_path, 'r').readlines():
        index = len(line.strip())
        if index > n:
            for _ in range(n+1, index+1):
                result.append([])
            n = index
        result[index].append(line.strip())
    return result

def load_images_of_morphisms(file_path):
    morphisms = []
    current = []
    for line in open(file_path, "r").readlines():
        if line[0] == '-' or len(line) == 0:
            morphisms.append(current.copy()) if len(current) > 0 else None
            current.clear()
        else:
            current.append(line.strip())
    return morphisms

def save_images_of_morphisms(morphisms, file_path):
    with open(file_path, 'w') as f:
        for m in morphisms:
            for img in m:
                f.write(img + '\n')
            f.write('-\n')

def load_constructions(file_path) -> List[TernaryConstructionDecomposition]:
    def read_construction(lines):
        for i in range(0,len(lines)):
            if lines[i][0] == 'r':
                r = lines[i][2:]
                images = lines[:i]
                return TernaryConstructionDecomposition(images, r = r)

    result = []
    current_lines = []
    for line in open(file_path, 'r').readlines():
        if line[0] == '-':
            result.append(read_construction(current_lines))
            current_lines.clear()
        else:
            current_lines.append(line.strip())
    
    return result


def save_constructions(constructions : List[TernaryConstructionDecomposition], file_path):
    with open(file_path, 'w') as f:
        for c in constructions:
            for img in c.get_morphism_images():
                f.write(img + '\n')
            f.write('r:' + c.r + '\n')
            f.write('s:' + c.s + '\n')
            f.write("r':" + c.r_prime + '\n')
            f.write("s':" + c.s_prime + '\n')
            if c.alpha != None:
                f.write("alpha:" + c.get_alpha().__str__() + '\n')
            if c.beta != None:
                f.write("beta:" + c.get_beta().__str__() + '\n')
            f.write('-\n')

def save_images_of_morphisms_from_terminal(terminal_text : str, file_path):
    morphisms = []
    current = []
    for line in terminal_text.split('\n'):
        if len(line) > 0 and line[0] in ['0', '1', '2', '3']:
            current.append(line[2:].strip())
        elif line[:5] == 'Found':
            morphisms.append(current.copy())
            current.clear()
    save_images_of_morphisms(morphisms, file_path)