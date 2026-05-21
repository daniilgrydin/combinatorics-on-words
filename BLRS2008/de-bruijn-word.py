from ..package.automata import Automata

def state_aa(cargo):
    bit = cargo[0]
    if len(cargo) > 1:
        cargo = cargo[1:]
    else:
        cargo = ""
    if bit == "1":
        return ("ab", cargo)
    return ("aa", cargo)

def state_ab(cargo):
    bit = cargo[0]
    if len(cargo) > 1:
        cargo = cargo[1:]
    else:
        cargo = ""
    if bit == "1":
        return ("bb", cargo)
    return ("ba", cargo)

def state_ba(cargo):
    bit = cargo[0]
    if len(cargo) > 1:
        cargo = cargo[1:]
    else:
        cargo = ""
    if bit == "1":
        return ("ab", cargo)
    return ("aa", cargo)

def state_bb(cargo):
    bit = cargo[0]
    if len(cargo) > 1:
        cargo = cargo[1:]
    else:
        cargo = ""
    if bit == "1":
        return ("bb", cargo)
    return ("ba", cargo)


automaton = Automata()
automaton.add_state("aa", state_aa)
automaton.add_state("ab", state_ab, True)
automaton.add_state("ba", state_ba)
automaton.add_state("bb", state_bb)

automaton.set_start("ab")
print(automaton.run(""))