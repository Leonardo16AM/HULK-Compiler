from src.cmp.pycompiler import Item
from src.cmp.utils import ContainerSet
from src.grammar.compute_firsts import compute_local_first
from src.grammar.compute_firsts import compute_firsts
from src.cmp.automata import State, multiline_formatter
from src.parser.shift_reduce import ShiftReduceParser
from termcolor import colored
from src.utils.errors import *



def expand(G, item: Item, firsts, items: set[Item]):
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []

    lookaheads = set()

    for preview in item.Preview():
        lookaheads.update(compute_local_first( firsts, preview))

    for production in next_symbol.productions:
        new_item = Item(production, 0, lookaheads)

        if new_item not in items:
            items.add(new_item)
            expand(G, new_item, firsts, items)

    return items


def compress(items):
    centers = {}

    for item in items:
        center = item.Center()
        try:
            lookaheads = centers[center]
        except KeyError:
            centers[center] = lookaheads = set()
        lookaheads.update(item.lookaheads)

    return {Item(x.production, x.pos, lookahead) for x, lookahead in centers.items()}


def closure_lr1(G, items, firsts):
    closure = ContainerSet(*items)

    new_items = ContainerSet()

    for item in items:
        new_items.set.update(expand(G, item, firsts, set()))

    closure.update(new_items)

    return compress(closure)


def goto_lr1(G, items, symbol, firsts=None, just_kernel=False):
    assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(G, items, firsts)


def build_LR1_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

    firsts = compute_firsts(G)
    firsts[G.EOF] = {G.EOF}

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.EOF,))
    start = frozenset([start_item])

    closure = frozenset(closure_lr1(G, start, firsts))
    automaton = State(closure, final = any(item.IsReduceItem for item in closure))

    pending = [closure]
    visited = {closure: automaton}

    while pending:
        current = pending.pop()
        current_state = visited[current]

        for symbol in G.terminals + G.nonTerminals:
            closure = frozenset(goto_lr1(G, current, symbol, firsts))

            if len(closure) > 0:
                if closure not in visited:
                    visited[closure] = State(closure, final = any(item.IsReduceItem for item in closure))
                    pending.append(closure)

                current_state.add_transition(symbol.Name, visited[closure])

    automaton.set_formatter(multiline_formatter)
    return automaton


class LR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)

        automaton = build_LR1_automaton(G)

        index = 0
        states = {automaton: index}
        index += 1

        pending = [automaton]

        while len(pending) > 0:
            current = pending.pop()

            for symbol, list_state in current.transitions.items():
                assert len(list_state) == 1
                state = list_state[0]

                if state not in states:
                    pending.append(state)
                    states[state] = index
                    index += 1

                self.table[states[current], symbol] = (ShiftReduceParser.SHIFT, states[state])

        for state in states.keys():
            if state.final:
                for item in state.state:
                    if item.production == G.startSymbol.productions[0] and item.IsReduceItem:
                        self.table[states[state], G.EOF.Name] = (ShiftReduceParser.OK, None)

        for state in states.keys():
            if state.final:
                for item in state.state:
                    if item.IsReduceItem:
                        if item.production != G.startSymbol.productions[0]:
                            for terminal in item.lookaheads:
                                if (states[state], terminal.Name) not in self.table:
                                    self.table[states[state], terminal.Name] = (
                                        ShiftReduceParser.REDUCE, item.production)
                                else:
                                    error("PARSER ERROR", "Grammar not LR(1), shit reduce or reduce reduce error",f"At {states[state], terminal.Name}: table[{states[state]},{terminal.Name}] = {self.table[states[state], terminal.Name]} and tried to set it to {ShiftReduceParser.REDUCE, item.production}")
                                 

