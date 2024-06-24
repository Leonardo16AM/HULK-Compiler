from src.lexer.lexer import lexer
from src.lexer.hulk_tokens import hulk_tokens
from src.cmp.pycompiler import EOF
from src.grammar.hulk_grammar import G

#region hulk_lexer
class hulk_lexer(lexer):
    def __init__(self):
        super().__init__(hulk_tokens(),EOF(G))
