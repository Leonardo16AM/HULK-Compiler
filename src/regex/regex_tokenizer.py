from src.cmp.utils import Token

#region regex_tokenizer
def regex_tokenizer(text, G, skip_whitespaces=True):
    tokens = []
    fixed_tokens = {char:Token(char,G[char])for char in['|','*','(',')','ε']}

    for char in text:
        if skip_whitespaces and char.isspace():
            continue
        try:
            token = fixed_tokens[char]
        except KeyError:
            token = Token(char, G['symbol'])
        finally:
            tokens.append(token)

    tokens.append(Token('$', G.EOF))
    return tokens
