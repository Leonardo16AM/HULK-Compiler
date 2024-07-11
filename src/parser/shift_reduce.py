from src.utils.errors import *
from termcolor import colored


class ShiftReduceParser():
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'

    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.table = {}
        self._build_parsing_table()

    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w,get_shift_reduce=False):
        stack = [0]
        cursor = 0
        output_parse = []
        operations = []

        while cursor < len(w):
            state = stack[-1]
            lookahead = w[cursor].token_type.Name
            if self.verbose:
                if self.verbose:print(stack,colored('<---||--->','yellow'),w[cursor:])


            if (state, lookahead) in self.table.keys():
                action, tag = self.table[state, lookahead]

                operations.append(action)

                if action == self.OK:
                    stack.pop()
                    return output_parse if not get_shift_reduce else(output_parse,operations)

                if action == self.SHIFT:
                    stack.append(tag)
                    cursor += 1

                if action == self.REDUCE:
                    output_parse.append(tag)
                    Left, Right = tag

                    for symbol in Right:
                        if not symbol.IsEpsilon:
                            stack.pop()

                    if (stack[-1], Left.Name) in self.table and self.table[(stack[-1], Left.Name)][
                        0] == self.SHIFT:
                        stack.append(self.table[(stack[-1], Left.Name)][1])
                    else:
                        error("PARSER ERROR","Not parseable",cursor)
            else:
                on_state=[value[1] for value in self.table if value[0] == state ]
                print(colored("Probably one of those tokens is missing: "+str(on_state),'red'))
                nxt=''
                for i in range(cursor,len(w)):
                    nxt+=w[i].lex+" "
                error("PARSER ERROR",f'Invalid action: Previous to "{nxt}"',"ShiftReduceParser",line=str(w[cursor].row))
        error("PARSER ERROR","Not parseable",cursor)