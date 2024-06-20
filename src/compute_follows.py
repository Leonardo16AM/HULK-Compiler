from src.cmp.pycompiler import *
from src.cmp.utils import pprint, inspect
from src.container_set import ContainerSet
from itertools import islice
from src.compute_firsts import compute_local_first

#region compute_follows
def compute_follows(G, firsts):
    follows = { }
    change = True
    
    local_firsts = {}
    
    for nonterminal in G.nonTerminals:
        follows[nonterminal] = ContainerSet()
    follows[G.startSymbol] = ContainerSet(G.EOF)
    
    while change:
        change = False
        
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            follow_X = follows[X]
            
            
            for i, Y in enumerate(alpha):
                beta = alpha[i+1:]
                
                if Y.IsTerminal:
                    continue
                
                try:
                    follow_Y = follows[Y]
                except KeyError:
                    follow_Y = follows[Y] = ContainerSet()
                

                if beta:
                    local_firsts[Y] = compute_local_first(firsts, beta)
                    change |= follow_Y.update(local_firsts[Y])
                
                if not beta or local_firsts[Y].contains_epsilon:
                    change |= follow_Y.update(follow_X)

                
    return follows