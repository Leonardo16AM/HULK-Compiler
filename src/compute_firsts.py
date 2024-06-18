from cmp.pycompiler import *
from cmp.utils import pprint, inspect
from .container_set import ContainerSet

#region compute_local_first
def compute_local_first(firsts, alpha):
    first_alpha = ContainerSet()
    
    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False

    if alpha_is_epsilon:
        first_alpha.set_epsilon(True)
        return first_alpha

    if alpha[0].IsTerminal:
        first_alpha.add(alpha[0])
    else:
        Y = alpha[0]
        
        if len(alpha) > 1:
            first_alpha.update(firsts[Y])
        else:
            first_alpha.hard_update(firsts[Y])
        
        if len(alpha) > 1:
            Z = alpha[1:]
            if firsts[Y].contains_epsilon:
                first_alpha.hard_update(compute_local_first(firsts,Z))
    
    return first_alpha

#region compute_firsts
def compute_firsts(G):
    firsts = {}
    change = True
    
    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)
        
    for nonterminal in G.nonTerminals:
        firsts[nonterminal] = ContainerSet()
    
    while change:
        change = False
        
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            first_X = firsts[X]
                
            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()
            
            local_first = compute_local_first(firsts, alpha)
            
            updated_alpha = first_alpha.hard_update(local_first)
            updated_X = first_X.hard_update(local_first)

            change |= updated_alpha
            change |= updated_X
                    
    return firsts
