
class ParserError(Exception):
    def __init__(self, text, token_index):
        super().__init__(text)
        self.token_index = token_index

class LexerError(Exception):
    def __init__(self, text, token_index):
        super().__init__(text)
        self.token_index = token_index

class SemanticError(Exception):
    def __init__(self, text):
        super().__init__(text)

class InternalError(Exception):
    def __init__(self, text):
        super().__init__(text)