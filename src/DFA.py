from .NFA import NFA
from cmp.utils import ContainerSet

#region DFA
class DFA(NFA):
    
    def __init__(self, states, finals, transitions, start=0):
        assert all(isinstance(value, int) for value in transitions.values())
        assert all(len(symbol) > 0 for origin, symbol in transitions)
        
        transitions = { key: [value] for key, value in transitions.items() }
        NFA.__init__(self, states, finals, transitions, start)
        self.current = start
        
    def _move(self, symbol):
        try:
            self.current = self.transitions[self.current][symbol][0]
        except KeyError:
            self.current = None
        

    
    def _reset(self):
        self.current = self.start
        
    def recognize(self, string):
        self._reset()
        for symbol in string:
            self._move(symbol)
            if self.current is None:
                return False
        return self.current in self.finals
    

#region move
def move(automaton, states, symbol):
    moves = set()
    for state in states:
        try:
            moves.update(automaton.transitions[state][symbol])
        except KeyError:
            pass

    return moves

#region epsilon_closure
def epsilon_closure(automaton, states):
    pending = [ s for s in states ] # equivalente a list(states) pero me gusta así :p
    closure = { s for s in states } # equivalente a  set(states) pero me gusta así :p
    
    while pending:
        state = pending.pop()
        for dest in automaton.epsilon_transitions(state):
            if dest not in closure:
                closure.add(dest)
                pending.append(dest)
                
                
    return ContainerSet(*closure)

#region nfa_to_dfa
def nfa_to_dfa(automaton):
    transitions = {}
    
    start = epsilon_closure(automaton, [automaton.start])
    start.id = 0
    start.is_final = any(s in automaton.finals for s in start)
    states = [ start ]

    pending = [ start ]
    while pending:
        state = pending.pop()

        for symbol in automaton.vocabulary:
            dest = epsilon_closure(automaton, move(automaton, state, symbol))
            if not dest:
                continue
            try:
                new = states[states.index(dest)]
            except ValueError:
                new = dest
                new.id = len(states)
                new.is_final = any(s in automaton.finals for s in new)
                states.append(new)
                pending.append(new)
                
            transitions[state.id, symbol] = new.id



                
    finals = [ state.id for state in states if state.is_final ]
    dfa = DFA(len(states), finals, transitions)
    return dfa

