from src.cmp.pycompiler import Item
from src.cmp.utils import ContainerSet
from src.grammar.compute_firsts import compute_local_first
from src.grammar.compute_firsts import compute_firsts
from src.cmp.automata import State, multiline_formatter
from src.parser.shift_reduce import ShiftReduceParser

#region expand
def expand(item, firsts):
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []
    
    lookaheads = ContainerSet()
    
    for preview in item.Preview():
        for x in compute_local_first(firsts,preview):
            lookaheads.add(x)

    assert not lookaheads.contains_epsilon


    return [Item(p, 0, lookaheads) for p in next_symbol.productions]     

#region compress
def compress(items):
    centers = {}

    for item in items:
        center = item.Center()
        try:
            lookaheads = centers[center]
        except KeyError:
            centers[center] = lookaheads = set()
        lookaheads.update(item.lookaheads)
    
    return { Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items() }


#region closure_lr1
def closure_lr1(items, firsts):
    closure = ContainerSet(*items)
    
    changed = True
    while changed:
        changed = False
        
        new_items = ContainerSet()
        for item in closure:
            new_items.extend(expand(item, firsts))


        changed = closure.update(new_items)
        
    return compress(closure)

#region goto_lr1
def goto_lr1(items, symbol, firsts=None, just_kernel=False):
    assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(items, firsts)




#region build_LR1_automaton
def build_LR1_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'
    
    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)
    
    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.EOF,))
    start = frozenset([start_item])
    
    closure = closure_lr1(start, firsts)
    automaton = State(frozenset(closure), True)
    
    pending = [ start ]
    visited = { start: automaton }
    
    while pending:
        current = pending.pop()
        current_state = visited[current]
        
        for symbol in G.terminals + G.nonTerminals:
            next_state = goto_lr1(current_state.state, symbol, firsts)
            
            if not next_state:
                continue
            
            closure= frozenset(next_state)
            try:
                next_state = visited[closure]
            except KeyError:
                pending.append(closure)
                next_state = visited[closure] = State(closure, True)

            
            current_state.add_transition(symbol.Name, next_state)
    
    automaton.set_formatter(multiline_formatter)
    return automaton

#region LR1Parser
class LR1Parser(ShiftReduceParser):


    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        
        automaton = build_LR1_automaton(G)
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for item in node.state:           
                if item.NextSymbol is not None:
                    if item.NextSymbol.IsTerminal:
                        next_state = node.get(item.NextSymbol.Name)
                        self._register(self.action, (idx, item.NextSymbol), (ShiftReduceParser.SHIFT,next_state.idx))
                    else:
                        next_state = node.get(item.NextSymbol.Name)
                        self._register(self.goto, (idx, item.NextSymbol), next_state.idx)
                else:
                    if item.production.Left == G.startSymbol:
                        self._register(self.action, (idx, G.EOF), (ShiftReduceParser.OK, None))
                    else:
                        for lookahead in item.lookaheads:
                            self._register(self.action, (idx, lookahead), (ShiftReduceParser.REDUCE, item.production))
                        
        
    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value