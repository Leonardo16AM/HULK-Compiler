import os
from termcolor import colored
from src.utils.preprocess import *
from src.lexer.hulk_lexer import hulk_lexer
from src.grammar.hulk_grammar import G
from src.parser.LR1_parser import LR1Parser
# from src.cmp.tools.parsing import LR1Parser
from src.cmp.evaluation import evaluate_reverse_parse
from src.semantic.ast_printer_visitor import *
from src.semantic.semantic_check import semantic_check

    
def pipeline(file_path):
    
    print(colored("========================================LOADING FILE===============================================",'blue'))
    with open(file_path, 'rb') as file:
        code = file.read().decode('utf-8')
    code = code.replace('\r\n', '\n').replace('\r', '\n')
    print(f"LOADED: {file_path}")

    print(colored("========================================TOKENIZING=================================================",'blue'))

    if os.path.isfile("src/lang/hulk_lexer.pkl"):
        print("LOADING LEXER")
        lexer=load_object("src/lang/hulk_lexer.pkl")
    else:
        lexer=hulk_lexer()
        save_object(lexer,"src/lang/hulk_lexer.pkl") 

    tokens=lexer(code)
    print("TOKENS:" , tokens)

    print(colored("=========================================PARSING===================================================",'blue'))

    if os.path.isfile("src/lang/hulk_parser.pkl"):
        print("LOADING PARSER")
        parser=load_object("src/lang/hulk_parser.pkl")
    else:
        print("LOADING GRAMMAR")
        print("CREATING LR1 PARSER")
        parser=LR1Parser(G,True)    
        save_object(parser,"src/lang/hulk_parser.pkl") 

    print("PARSING TOKENS")
    types=[ token.token_type for token in tokens]

    parse,operations=parser(types,get_shift_reduce=True)

    print("PARSE:",colored(parse,"magenta"))

    ast=evaluate_reverse_parse(parse,operations,tokens)

    formatter = FormatVisitor()
    print(formatter.visit(ast))

    print(colored("========================================CHECKING_SEMATICS========================================",'blue'))
    semantic_check(ast)
    print(colored("========================================GERNERATING_CODE=========================================",'blue'))
    print(colored("============================================FINISHED=============================================",'blue'))


if __name__ == '__main__':
    pipeline("examples/print.hulk")
