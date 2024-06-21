
from enum import Enum, auto

#region TokenType
class TokenType(Enum):
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    OPEN_BRACKET = auto()
    CLOSE_BRACKET = auto()
    OPEN_SQUARE_BRACKET = auto()
    CLOSE_SQUARE_BRACKET = auto()
    COMMA = auto()
    DOT = auto()
    COLON = auto()
    SEMICOLON = auto()
    ARROW = auto()
    DOUBLE_BAR = auto()
    ASSIGMENT = auto()
    DEST_ASSIGMENT = auto()

    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()
    PI = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    DIV = auto()
    MOD = auto()
    POWER = auto()
    POWER2 = auto()

    AND = auto()
    OR = auto()
    NOT = auto()

    ARR = auto()
    DOUBLE_ARR = auto()

    EQ = auto()
    NEQ = auto()
    LEQ = auto()
    GEQ = auto()
    LT = auto()
    GT = auto()

    FUNCTION = auto()
    LET = auto()
    IN = auto()
    IF = auto()
    ELSE = auto()
    ELIF = auto()
    WHILE = auto()
    FOR = auto()
    NEW = auto()
    IS = auto()
    AS = auto()
    PROTOCOL = auto()
    EXTENDS = auto()
    TYPE = auto()
    INHERITS = auto()
    BASE = auto()

    UNTERMINATED_STRING = auto()
    ESCAPED_CHAR = auto()
    SPACES = auto()

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
        (TokenType.TYPE, "type"), (TokenType.INHERITS, "inherits"), (TokenType.BASE, "base"),
        (TokenType.BOOLEAN, "true|false"), (TokenType.PI, "PI")]

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

    hulk_lexer_synchronizing_tokens = [
        (TokenType.SPACES, "  *"), (TokenType.ESCAPED_CHAR, "\n|\t")
    ] + operators

    return hulk_tokens