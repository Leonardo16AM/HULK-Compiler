import os
from termcolor import colored
from src.utils.preprocess import *
from src.lexer.hulk_lexer import hulk_lexer


def pipeline(file_path):
    print(colored("=================LOADING FILE===================",'blue'))

    with open(file_path, 'rb') as file:
        code = file.read().decode('utf-8')

    code = code.replace('\r\n', '\n').replace('\r', '\n')

    print(f"LOADED: {file_path}")
    
    # LEXER
    
    print(colored("=================TOKENIZING=====================",'blue'))

    if os.path.isfile("src/lang/hulk_lexer.pkl"):
        print("LOADING LEXER")
        lexer=load_object("src/lang/hulk_lexer.pkl")
    else:
        lexer=hulk_lexer()
        save_object(lexer,"src/lang/hulk_lexer.pkl") 

    tokens=lexer(code)
    print("TOKENS:" , tokens)


    print(colored("===================PARSING======================",'blue'))
    print(colored("================CHECKING_SEMATICS===============",'blue'))
    print(colored("================GERNERATING_CODE================",'blue'))


if __name__ == '__main__':
    pipeline("examples/print.hulk")


    