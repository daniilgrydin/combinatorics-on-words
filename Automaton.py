class FiniteDeterministicAutomaton:
    _alphabet : list
    _states : list
    _finalStates : list
    _dotFunction = None
    _initialState : str
    currentState : str

    def __init__(self, alphabet, states, initialState, finalStates, dotFunction):
        self._alphabet = alphabet
        self._states = states
        self._initialState = initialState
        self.currentState = initialState
        self._finalStates = finalStates
        self._dotFunction = dotFunction

    def processWord(self, w):
        q = self.currentState
        for a in w:
            q = self._dotFunction(q, a)
        self.currentState = q
        return self.currentState
    
    def isAcceptedWord(self, w):
        self.processWord(w)
        if self.currentState in self._finalStates:
            return True
        else:
            return False
    
    def reset(self):
        self.currentState = self._initialState





# The Thue-Morse automaton is a 2-automatic. 
def thueMorseDot(q,a):
    if a == '0':
        return q
    if q == 's0':
        return 's1'
    else:
        return 's0'
    
# ThueMorse using the automaton
#
# phi = {'s0' : '0', 's1' : '1'} #Just the phi function to go from states to an alphabet
# thueMorseAutomaton = FiniteDeterministicAutomaton(['0','1'], ['s0','s1'], 's0', [], thueMorseDot)

# result = ""
# for i in range(0,21):
#     thueMorseAutomaton.reset()
#     thueMorseAutomaton.processWord(format(i,'b'))
#     result += phi[thueMorseAutomaton.currentState]
# print(result)

# Next state function for Exercise 2.15
# This verifies my solution.
#
# def ex215dot(q,a):
#     transitionTable = {'1a':'2', '2a':'2',
#                    '3a':'4', '4a':'2',
#                    '1b':'1', '2b':'3',
#                    '3b':'1', '4b':'3'}
#     return transitionTable[q+a]

# ex215dotAutomaton = FiniteDeterministicAutomaton(['a','b'], ['1','2','3','4'], '1', ['4'], ex215dot)

# allWords = Words.allWords(['a','b'],8)
# for w in allWords:
#     if ex215dotAutomaton.isAcceptedWord(w):
#         if w[-3:] != 'aba':
#             print("This shouldn't exist", w)
#     ex215dotAutomaton.reset()
# print("Done")
