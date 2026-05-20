class Automata:
    def __init__(self):
        self.handlers = {}
        self.start_state = None
        self.endStates = []

    def add_state(self, name, handler, end_state=False):
        name = name.lower()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name):
        self.start_state = name.lower()

    def run(self, cargo):
        try:
            handler = self.handlers[self.start_state]
        except:
            raise ValueError("must call .set_start() before .run()")
        """ Assumption that if start state is an end state - then it should not halt right away """
        newState, cargo = handler(cargo)
        while True:
            newState, cargo = handler(cargo)
            if newState.lower() in self.endStates:
                return f"halted at {newState}"
            if len(cargo) == 0:
                if len(self.endStates) == 0:
                    return f"reached end of sequence at {newState}"
                else:
                    return f"did not halt, finished at {newState}"
            handler = self.handlers[newState.lower()]
