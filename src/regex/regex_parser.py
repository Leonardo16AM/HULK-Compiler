
from src.grammar.compute_firsts import compute_firsts
from src.grammar.compute_follows import compute_follows
from src.parser.shift_reduce import ShiftReduceParser
from src.cmp.pycompiler import EOF
from src.utils.errors import *


generate_iter = iter
get_next = next
is_instance = isinstance
NoneType = None
get_length = len
enumerate_items = enumerate

def evaluate_parse(productions, tokens):
    if not productions or not tokens:
        return
    production_iter = generate_iter(productions)
    token_iter = generate_iter(tokens)
    result = evaluate(get_next(production_iter), production_iter, token_iter)
    assert is_instance(get_next(token_iter).token_type, EOF)
    return result

def evaluate(production, production_iter, token_iter, inherited_value=NoneType):
    non_terminal, rules = production
    attributes = production.attributes
    synthesized_values = [NoneType] * (get_length(rules) + 1)
    inherited_values = [NoneType] * (get_length(rules) + 1)
    inherited_values[0] = inherited_value
    
    for index, rule in enumerate_items(rules, 1):
        if rule.IsTerminal:
            assert inherited_values[index] is NoneType
            synthesized_values[index] = get_next(token_iter).lex
        else:
            next_production = get_next(production_iter)
            assert rule == next_production.Left
            rule_attr = attributes[index]
            if rule_attr is not NoneType:
                inherited_values[index] = rule_attr(inherited_values, synthesized_values)
            synthesized_values[index] = evaluate(next_production, production_iter, token_iter, inherited_values[index])
    
    root_attr = attributes[0]
    return root_attr(inherited_values, synthesized_values) if root_attr is not NoneType else NoneType




#region RegexParser
class RegexParser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.firsts = compute_firsts(grammar)
        self.follows = compute_follows(grammar, self.firsts)
        self.parsing_table = self.build_parsing_table()

    def build_parsing_table(self):
        table = {}
        for production in self.grammar.Productions:
            head, body = production.Left, production.Right
            for terminal in self.firsts[body]:
                table.setdefault((head, terminal), []).append(production)
            if self.firsts[body].contains_epsilon:
                for terminal in self.follows[head]:
                    table.setdefault((head, terminal), []).append(production)
        return table

    def parse(self, tokens):
        stack = [self.grammar.EOF, self.grammar.startSymbol]
        position = 0
        history = []
        while True:
            top = stack.pop()
            current_token = tokens[position]
            if top.IsTerminal:
                if top == current_token.token_type:
                    if top == self.grammar.EOF:
                        break
                    position += 1
                else:
                    error("LEXER ERROR","(REGEX) Unexpected token",current_token.lex,True)
            else:
                try:
                    production = self.parsing_table[top, current_token.token_type][0]
                    stack.extend(reversed(production.Right))
                    history.append(production)
                except KeyError:
                    error("LEXER ERROR","(REGEX) Unexpected token type",current_token.token_type,True)
        return history