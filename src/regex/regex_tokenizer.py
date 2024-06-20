from src.cmp.utils import Token

#region regex_tokenizer
def regex_tokenizer(text, G, skip_whitespaces=True):
    pipe, star, opar, cpar, symbol, epsilon = G.Terminals('| * ( ) symbol ε')
    tokens = []
    fixed_tokens= {
        '|': pipe,
        '*': star,
        '(': opar,
        ')': cpar,
        'ε': epsilon
    }

    for char in text:
        if skip_whitespaces and char.isspace():
            continue
        if char in fixed_tokens:
            tokens.append(Token(char, fixed_tokens[char]))
        else:
            tokens.append(Token(char, symbol))

    tokens.append(Token('$', G.EOF))
    return tokens