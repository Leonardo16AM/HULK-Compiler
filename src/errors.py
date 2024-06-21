
class ParserError(Exception):
    def __init__(self, text, token_index):
        super().__init__(text)

class LexerError(Exception):
    def __init__(self, text):
        super().__init__(text)

class SemanticError(Exception):
    def __init__(self, text):
        super().__init__(text)

class InternalError(Exception):
    def __init__(self, text):
        super().__init__(text)