
from src.compute_firsts import compute_firsts
from src.compute_follows import compute_follows
from src.shift_reduce import ShiftReduceParser
from src.cmp.pycompiler import EOF
from src.errors import LexerError

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
                    raise LexerError(f"(REGEX) Unexpected token: {current_token.lex}")
            else:
                try:
                    production = self.parsing_table[top, current_token.token_type][0]
                    stack.extend(reversed(production.Right))
                    history.append(production)
                except KeyError:
                    raise LexerError(f"(REGEX) Unexpected token: {current_token.lex}")
        return history