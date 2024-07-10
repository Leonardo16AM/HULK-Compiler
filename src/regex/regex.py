# Importaciones y configuración inicial
from src.automaton.automaton_ops import *
from src.regex.regex_nodes import *
from src.regex.regex_grammar import regex_grammar
from src.regex.regex_tokenizer import regex_tokenizer
from src.regex.regex_parser import RegexParser,evaluate_parse

#region regex
class regex:
    def __init__(self, regex, skip_whitespaces=False):
        self.regex = regex
        self.automaton = self.build_automaton(regex, skip_whitespaces)

    def __call__(self, text):
        return self.automaton.recognize(text)

    @staticmethod
    def build_automaton(regex, skip_whitespaces):
        grammar = regex_grammar()
        parser = RegexParser(grammar)
        tokenizer = regex_tokenizer(regex, grammar, skip_whitespaces)
        parsing_history = parser.parse(tokenizer)
        evaluation_result = evaluate_parse(parsing_history, tokenizer)
        nfa = evaluation_result.evaluate()
        dfa = nfa_to_dfa(nfa)
        minimized_dfa = automata_minimization(dfa)
        return minimized_dfa