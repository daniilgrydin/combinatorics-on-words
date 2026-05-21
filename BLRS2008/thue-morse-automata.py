from ..package.automata import Automata

def read_1(cargo:str):
    bit = cargo[0]
    if len(cargo) > 1:
        cargo = cargo[1:]
    else:
        cargo = ""
    if bit == "1":
        return ("a", cargo)
    return ("b", cargo)

def read_0(cargo:str):
    bit = cargo[0]
    if len(cargo) > 1:
        cargo = cargo[1:]
    else:
        cargo = ""
    if bit == "1":
        return ("b", cargo)
    return ("a", cargo)

thue_morse = Automata()
thue_morse.add_state("a", read_0)
thue_morse.add_state("b", read_1)
thue_morse.set_start("a")

for n in range(16):
    print(thue_morse.run(bin(n)[2:]))