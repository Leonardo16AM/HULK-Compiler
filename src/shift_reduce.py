
#region ShiftReduceParser
class ShiftReduceParser:
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'
    
    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()
    
    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w):
        stack = [ 0 ]
        cursor = 0
        output = []
        
        while True:
            state = stack[-1]
            lookahead = w[cursor]
            if self.verbose: print(stack, '<---||--->', w[cursor:])
                
            if (state, lookahead) not in self.action:
                return None
            
            
            action, tag = self.action[state, lookahead]
            
            if action == ShiftReduceParser.SHIFT:
                stack.append(tag)
                cursor += 1
            
            elif action == ShiftReduceParser.REDUCE:
                production = tag
                for _ in range(len(production.Right)):
                    stack.pop()
                stack.append(self.goto[stack[-1], production.Left])
                output.append(production)
            
            elif action == ShiftReduceParser.OK:
                return output
            
            else:
                return None

