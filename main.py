import os
import argparse
from termcolor import colored
from src.utils.preprocess import *
from src.utils.errors import *
from src.lexer.hulk_lexer import hulk_lexer
from src.grammar.hulk_grammar import G
from src.parser.LR1_parser import LR1Parser
from src.cmp.evaluation import evaluate_reverse_parse
from src.semantic.ast_printer_visitor import *
from src.semantic.semantic_check import semantic_check

    
def pipeline(file_path="examples/custom_test.hulk",verbose=True):
    
    if verbose:print(colored("========================================LOADING FILE===============================================",'blue'))
    try:
        with open(file_path, 'rb') as file:
            code = file.read().decode('utf-8')
        code = code.replace('\r\n', '\n').replace('\r', '\n')
    except FileNotFoundError:
        error("FILE NOT FOUND", f"File '{file_path}' not found")

    if verbose:print(f"LOADED: {file_path}")

    if verbose:print(colored("========================================TOKENIZING=================================================",'blue'))

    if os.path.isfile("src/lang/hulk_lexer.pkl"):
        if verbose:print("LOADING LEXER")
        lexer=load_object("src/lang/hulk_lexer.pkl")
    else:
        lexer=hulk_lexer()
        save_object(lexer,"src/lang/hulk_lexer.pkl") 

    tokens=lexer(code)
    if verbose:print("TOKENS:" , tokens)

    if verbose:print(colored("=========================================PARSING===================================================",'blue'))

    if os.path.isfile("src/lang/hulk_parser.pkl"):
        if verbose:print("LOADING PARSER")
        parser=load_object("src/lang/hulk_parser.pkl")
    else:
        if verbose:print("CREATING LR1 PARSER")
        parser=LR1Parser(G)    
        save_object(parser,"src/lang/hulk_parser.pkl") 

    if verbose:print("PARSING TOKENS")
    
    parse,operations=parser([token.token_type for token in tokens],get_shift_reduce=True)
    operations.pop()
    ast=evaluate_reverse_parse(parse,operations,tokens)
    if verbose:
        formatter = FormatVisitor()
        print(formatter.visit(ast))

    if verbose:print(colored("========================================CHECKING_SEMATICS========================================",'blue'))
    semantic_check(ast)
    if verbose:print(colored("========================================GERNERATING_CODE=========================================",'blue'))
    if verbose:print(colored("============================================FINISHED=============================================",'blue'))



def main():
    parser = argparse.ArgumentParser(description='Process a file path with optional verbosity.')
    parser.add_argument('file_path', nargs='?', type=str, default="examples/custom_test.hulk", help='Path to the file to be processed')
    parser.add_argument('-v', dest='verbose', action='store_true', help='Enable verbose mode')
    parser.add_argument('-nv', dest='verbose', action='store_false', help='Disable verbose mode')
    parser.set_defaults(verbose=True)
    
    args = parser.parse_args()

    pipeline(file_path=args.file_path, verbose=args.verbose)

if __name__ == '__main__':
    main()
