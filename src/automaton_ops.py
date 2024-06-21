from src.NFA import NFA
from src.DFA import DFA,nfa_to_dfa
from src.cmp.utils import DisjointSet

#region automata_union
def automata_union(a1, a2):
    transitions = {}
    
    start = 0
    d1 = 1
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[(origin + d1, symbol)] = { d + d1 for d in destinations }

    for (origin, symbol), destinations in a2.map.items():
        transitions[(origin + d2, symbol)] = { d + d2 for d in destinations }


    transitions[(start, '')] = { a1.start + d1, a2.start + d2 }
    
    

    for f in a1.finals:
        transitions[(f + d1, '')] = { final }

    for f in a2.finals:
        transitions[(f + d2, '')] = { final }


    states = a1.states + a2.states + 2
    finals = { final }
    
    return NFA(states, finals, transitions, start)

#region automata_concatenation
def automata_concatenation(a1, a2):
    transitions = {}
    
    start = 0
    d1 = 0
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[(origin + d1, symbol)] = { d + d1 for d in destinations }

    for (origin, symbol), destinations in a2.map.items():
        transitions[(origin + d2, symbol)] = { d + d2 for d in destinations }


    for f in a1.finals:
        transitions[(f + d1, '')] = { a2.start + d2 }

    for f in a2.finals:
        transitions[(f + d2, '')] = { final }
            
    states = a1.states + a2.states + 1
    finals = { final }
    
    return NFA(states, finals, transitions, start)

#region automata_closure
def automata_closure(a1):
    transitions = {}
    
    start = 0
    d1 = 1
    final = a1.states + d1

    for (origin, symbol), destinations in a1.map.items():
        transitions[(origin + d1, symbol)] = { d + d1 for d in destinations }

    transitions[(start, '')] = { a1.start + d1, final }

    for f in a1.finals:
        transitions[(f + d1, '')] = { a1.start + d1, final }

    transitions[(final, '')] = { start }

    states = a1.states + 2
    finals = { final }

    return NFA(states, finals, transitions, start)




#region automata_minimization
def distinguish_states(group, automaton, partition):
    split = {}
    vocabulary = tuple(automaton.vocabulary)

    for member in group:
        transitions = automaton.transitions[member.value]
        labels = ((transitions[symbol][0] if symbol in transitions else None) for symbol in vocabulary)
        key = tuple((partition[node].representative if node in partition.nodes else None) for node in labels)
        try:
            split[key].append(member.value)
        except KeyError:
            split[key] = [member.value]

    return [subgroup for subgroup in split.values()]

def state_minimization(automaton):
    partition = DisjointSet(*range(automaton.states))
    
    partition.merge(s for s in automaton.finals)
    partition.merge(s for s in range(automaton.states) if s not in automaton.finals)
    
    while True:
        new_partition = DisjointSet(*range(automaton.states))
        for group in partition.groups:
            distinguished = distinguish_states(group, automaton, partition)
            for subgroup in distinguished:
                new_partition.merge(subgroup)

        if len(new_partition) == len(partition):
            break

        partition = new_partition
        
    return partition

def automata_minimization(automaton):
    partition = state_minimization(automaton)
    
    states = [s for s in partition.representatives]
    
    transitions = {}
    for i, state in enumerate(states):
        origin = state.value
        for symbol, destinations in automaton.transitions[origin].items():
            representative = partition[destinations[0]].representative
            j = states.index(representative)
            try:
                transitions[i, symbol]
                assert False
            except KeyError:
                transitions[i, symbol] = j
    
    start = states.index(partition[automaton.start].representative)
    finals = [i for i, state in enumerate(states) if state.value in automaton.finals]

    return DFA(len(states), finals, transitions, start)

#region eps_nfa
def eps_nfa():
    return NFA(1, {0}, {}, 0)



#region basic_nfa
def basic_nfa(token):
    return NFA(2, {1}, {(0, token): {1}}, 0)