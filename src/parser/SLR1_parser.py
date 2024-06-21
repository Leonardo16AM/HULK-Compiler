from parser.shift_reduce import ShiftReduceParser
from src.cmp.automata import State
from src.cmp.pycompiler import Item
from src.grammar.compute_firsts import compute_firsts
from src.grammar.compute_follows import compute_follows


#region build_LR0_automaton
def build_LR0_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0)

    automaton = State(start_item, True)

    pending = [ start_item ]
    visited = { start_item: automaton }

    while pending:
        current_item = pending.pop()
        if current_item.IsReduceItem:
            continue

        current_state = visited[current_item]

        new_item=current_item.NextItem()
        if  new_item not in visited:
            pending.append(new_item)
            visited[new_item]=State(new_item,True)
        new_state=visited[new_item]

    
        current_state.add_transition(current_item.NextSymbol.Name,new_state)

        if current_item.NextSymbol.IsNonTerminal:
            for prod in current_item.NextSymbol.productions:
                new_item=Item(prod,0)
                if new_item not in visited:
                    pending.append(new_item)
                    visited[new_item]=State(new_item,True)
                current_state.add_epsilon_transition(visited[new_item])

    
    return automaton

#region SLR1Parser
class SLR1Parser(ShiftReduceParser):

    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)
        
        automaton = build_LR0_automaton(G).to_deterministic()
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for state in node.state:
                item = state.state
                if item.IsReduceItem:
                    if item.production.Left == G.startSymbol:
                        self._register(self.action, (idx, G.EOF), (ShiftReduceParser.OK, None))
                    else:
                        for symbol in follows[item.production.Left]:
                            self._register(self.action, (idx, symbol), (ShiftReduceParser.REDUCE, item.production))
                else:
                    next_symbol = item.NextSymbol
                    if next_symbol.IsTerminal:
                        self._register(self.action, (idx, next_symbol), (ShiftReduceParser.SHIFT, node[next_symbol.Name][0].idx))
                    else:
                        self._register(self.goto, (idx, next_symbol), node[next_symbol.Name][0].idx)
    
    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value