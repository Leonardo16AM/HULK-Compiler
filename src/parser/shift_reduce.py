from src.utils.errors import *
from termcolor import colored
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

    def __call__(self, w, get_shift_reduce=False):
        stack = [ 0 ]
        cursor = 0
        output = []
        operations=[]
        
        while True:
            state = stack[-1]
            lookahead = w[cursor]
            if self.verbose: 
                print(stack, '<---||--->', w[cursor:])
                print("ACTION::: ",self.action)
                
            if (state, lookahead) not in self.action:
                error("PARSER ERROR","(state, lookahead) not in self.action:",f"({state}, {lookahead})")
                return None
            
            
            action, tag = self.action[state, lookahead]
            
            if action == ShiftReduceParser.SHIFT:
                operations.append(self.SHIFT)
                stack.append(lookahead)
                stack.append(tag)
                cursor += 1
            
            elif action == ShiftReduceParser.REDUCE:
                head,body=tag
                for symbol in reversed(body):
                    stack.pop()
                state=stack[-1]
                goto=self.goto[state,head]
                stack.append(head)
                stack.append(goto)
                
                operations.append(self.REDUCE)
                output.append(tag)
            

            elif action == ShiftReduceParser.OK:
                stack.pop()
                if not get_shift_reduce:
                    return output
                else:
                    return (output, operations)
            
            
            else:
                error("PARSER ERROR","Invalid action","ShiftReduceParser")

