from src.cmp.utils import Token
from src.utils.errors import *

#region regex_tokenizer
def regex_tokenizer(text, G, skip_whitespaces=True):
    tokens = []
    fixed_tokens = {char: Token(char, G[char]) for char in ['|', '*', '(', ')', 'ε']}

    i = 0
    while i < len(text):
        char = text[i]

        if skip_whitespaces and char.isspace():
            i += 1
            continue

        if char == '\\':
            if i + 1 < len(text):
                next_char = text[i + 1]
                token = Token(next_char, G['symbol'])
                i += 2 
            else:
                error("LEXER ERROR", "Carácter de escape '\\' al final del texto no es válido",char)
        else:
            try:
                token = fixed_tokens[char]
            except KeyError:
                token = Token(char, G['symbol'])
            i += 1

        tokens.append(token)

    tokens.append(Token('<EOF>', G.EOF))
    return tokens
