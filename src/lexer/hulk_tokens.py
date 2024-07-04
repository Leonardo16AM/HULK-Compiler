
from src.grammar.hulk_grammar import *
#region TokenType
class TokenType():
    OPEN_PAREN = opar
    CLOSE_PAREN = cpar
    OPEN_BRACKET = lcurly
    CLOSE_BRACKET = rcurly
    OPEN_SQUARE_BRACKET = obracket
    CLOSE_SQUARE_BRACKET = cbracket
    COMMA = comma
    DOT = dot
    COLON = colon
    SEMICOLON = semicolon
    ARROW = arrow
    DOUBLE_BAR = bar_bar
    ASSIGMENT = equal
    DEST_ASSIGMENT = assignment_op

    IDENTIFIER = id
    STRING = string
    NUMBER = num
    BOOLEAN = bool
    PLUS = plus
    MINUS = minus
    STAR = star
    DIV = div
    MOD = mod
    POWER = caret
    POWER2 = star_star

    AND = and_t
    OR = or_t
    NOT = not_t

    ARR = at
    DOUBLE_ARR = double_at

    EQ = eq_eq
    NEQ = dif
    LEQ = less_eq
    GEQ = greater_eq
    LT = less
    GT = greater

    FUNCTION = function
    LET = let
    IN =  in_t
    IF =  if_t
    ELSE = else_t
    ELIF = elif_t
    WHILE = while_t
    FOR = for_t
    NEW = new
    IS = is_t
    AS = as_t
    PROTOCOL = protocol
    EXTENDS = extends
    TYPE = type_t
    INHERITS = inherits

    UNTERMINATED_STRING = 'UNTERMINATED_STRING'
    ESCAPED_CHAR = 'ESCAPED_CHAR'
    SPACES = 'SPACES'

#region hulk_tokens
def hulk_tokens():
    operators = [
        (TokenType.OPEN_BRACKET, "{"), (TokenType.CLOSE_BRACKET, "}"), (TokenType.SEMICOLON, ";"),
        (TokenType.OPEN_PAREN, "\\("), (TokenType.CLOSE_PAREN, "\\)"), (TokenType.ARROW, "=>"), (TokenType.COMMA, ","),
        (TokenType.ASSIGMENT, "="), (TokenType.DEST_ASSIGMENT, ":="),
        (TokenType.PLUS, "+"), (TokenType.MINUS, "-"), (TokenType.STAR, "\\*"), (TokenType.DIV, "/"),
        (TokenType.POWER, "^"), (TokenType.MOD, "%"), (TokenType.POWER2, "\\*\\*"),
        (TokenType.EQ, "=="), (TokenType.NEQ, "!="), (TokenType.LEQ, "<="), (TokenType.GEQ, ">="),
        (TokenType.LT, "<"), (TokenType.GT, ">"), (TokenType.AND, "&"), (TokenType.OR, "\\|"),
        (TokenType.NOT, "!"), (TokenType.ARR, "@"), (TokenType.DOUBLE_ARR, "@@"), (TokenType.DOT, "."),
        (TokenType.COLON, ":"), (TokenType.DOUBLE_BAR, "\\|\\|"), (TokenType.OPEN_SQUARE_BRACKET, "\\["),
        (TokenType.CLOSE_SQUARE_BRACKET, "\\]")]

    reserved_words = [
        (TokenType.LET, "let"), (TokenType.IN, "in"),
        (TokenType.IF, "if"), (TokenType.ELSE, "else"), (TokenType.ELIF, "elif"),
        (TokenType.FUNCTION, "function"),
        (TokenType.WHILE, "while"), (TokenType.FOR, "for"),
        (TokenType.NEW, "new"), (TokenType.IS, "is"), (TokenType.AS, "as"),
        (TokenType.PROTOCOL, "protocol"), (TokenType.EXTENDS, "extends"),
        (TokenType.TYPE, "type"), (TokenType.INHERITS, "inherits"), 
        (TokenType.BOOLEAN, "true|false")]

    nonzero_digits = '|'.join(str(n) for n in range(1, 10))
    digits = '|'.join(str(n) for n in range(10))
    lower_letters = '|'.join(chr(n) for n in range(ord('a'), ord('z') + 1))
    upper_letters = '|'.join(chr(n) for n in range(ord('A'), ord('Z') + 1))

    string_regex = "\"(\\\\\"|\\x00|\\x01|\\x02|\\x03|\\x04|\\x05|\\x06|\\x07|\\x08|\\t|\\n|\\x0b|\\x0c|\\r|\\x0e|\\x0f|\\x10|\\x11|\\x12|\\x13|\\x14|\\x15|\\x16|\\x17|\\x18|\\x19|\\x1a|\\x1b|\\x1c|\\x1d|\\x1e|\\x1f| |!|#|$|%|&|\'|\\(|\\)|\\*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|\\||}|~|\\x7f|\\x80|\\x81|\\x82|\\x83|\\x84|\\x85|\\x86|\\x87|\\x88|\\x89|\\x8a|\\x8b|\\x8c|\\x8d|\\x8e|\\x8f|\\x90|\\x91|\\x92|\\x93|\\x94|\\x95|\\x96|\\x97|\\x98|\\x99|\\x9a|\\x9b|\\x9c|\\x9d|\\x9e|\\x9f|\\xa0|¡|¢|£|¤|¥|¦|§|¨|©|ª|«|¬|\\xad|®|¯|°|±|²|³|´|µ|¶|·|¸|¹|º|»|¼|½|¾|¿|À|Á|Â|Ã|Ä|Å|Æ|Ç|È|É|Ê|Ë|Ì|Í|Î|Ï|Ð|Ñ|Ò|Ó|Ô|Õ|Ö|×|Ø|Ù|Ú|Û|Ü|Ý|Þ|ß|à|á|â|ã|ä|å|æ|ç|è|é|ê|ë|ì|í|î|ï|ð|ñ|ò|ó|ô|õ|ö|÷|ø|ù|ú|û|ü|ý|þ|ÿ)*\""

    unterminated_string_regex = "\"(\\x00|\\x01|\\x02|\\x03|\\x04|\\x05|\\x06|\\x07|\\x08|\\t|\\n|\\x0b|\\x0c|\\r|\\x0e|\\x0f|\\x10|\\x11|\\x12|\\x13|\\x14|\\x15|\\x16|\\x17|\\x18|\\x19|\\x1a|\\x1b|\\x1c|\\x1d|\\x1e|\\x1f| |!|#|$|%|&|\'|\\(|\\)|\\*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\\\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|\\||}|~|\\x7f|\\x80|\\x81|\\x82|\\x83|\\x84|\\x85|\\x86|\\x87|\\x88|\\x89|\\x8a|\\x8b|\\x8c|\\x8d|\\x8e|\\x8f|\\x90|\\x91|\\x92|\\x93|\\x94|\\x95|\\x96|\\x97|\\x98|\\x99|\\x9a|\\x9b|\\x9c|\\x9d|\\x9e|\\x9f|\\xa0|¡|¢|£|¤|¥|¦|§|¨|©|ª|«|¬|\\xad|®|¯|°|±|²|³|´|µ|¶|·|¸|¹|º|»|¼|½|¾|¿|À|Á|Â|Ã|Ä|Å|Æ|Ç|È|É|Ê|Ë|Ì|Í|Î|Ï|Ð|Ñ|Ò|Ó|Ô|Õ|Ö|×|Ø|Ù|Ú|Û|Ü|Ý|Þ|ß|à|á|â|ã|ä|å|æ|ç|è|é|ê|ë|ì|í|î|ï|ð|ñ|ò|ó|ô|õ|ö|÷|ø|ù|ú|û|ü|ý|þ|ÿ)*"

    number_regex = '|'.join([f"({nonzero_digits})({digits})*",
                         f"({nonzero_digits})({digits})*.({digits})({digits})*",
                         f"0.({digits})({digits})*",
                         "0"])

    identifier_regex = f"(_|{upper_letters}|{lower_letters})(_|{upper_letters}|{lower_letters}|{digits})*"

    hulk_tokens = operators + reserved_words + [
        (TokenType.NUMBER, number_regex), (TokenType.IDENTIFIER, identifier_regex),
        (TokenType.STRING, string_regex), (TokenType.UNTERMINATED_STRING, unterminated_string_regex),
        (TokenType.SPACES, "  *"), (TokenType.ESCAPED_CHAR, "\n|\t")
    ]

    return hulk_tokens