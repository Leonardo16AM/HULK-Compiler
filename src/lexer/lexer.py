from src.cmp.utils import Token
from src.cmp.automata import State
from src.regex.regex import regex
from src.errors import LexerError



class lexer:
    def __init__(self, table, eof):
        self.eof = eof
        print("BUILDING LEXER")
        self.regexs = self._build_regexs(table)
        print("REGEX BUILT")
        self.automaton = self._build_automaton()
        print("AUTOMATON BUILT")
        

    def _build_regexs(self, table):
        regexs = []
        for priority, (token_type, regex_str) in enumerate(table):
            
            r=regex(regex_str)
            first_state = State.from_nfa(r.automaton)
            
            unseen = [first_state]
            visited=[]
            while unseen:
                state = unseen.pop()
                visited.append(state)
                if state.final:
                    state.tag = priority, token_type

                for symbol, next_state in state.transitions.items():
                    for next in next_state:
                        if next not in visited:
                            unseen.append(next)
                            
                for next_state in state.epsilon_transitions:
                    if next_state not in visited:
                        unseen.append(next_state)
            
            regexs.append((priority, first_state))

        return regexs

    def _build_automaton(self):
        start = State('<start>')
        for priority, automaton in self.regexs:
            start.add_epsilon_transition(automaton)
        
        # start=start.to_deterministic()
        return start



    def _walk(self, string):
        final_state = None
        lexeme = ''

        states = self.automaton.epsilon_closure

        for i,symbol in enumerate(string):
            states = { s for state in states if state.has_transition(symbol) for s in state[symbol]}
            
            eps_states = { s for state in states for s in state.epsilon_transitions}
            states=states.union(eps_states)

            if not states:
                break
            else:
                for state in states:
                    if state.final:
                        if final_state is None or (len(lexeme)<i+1)  or (len(lexeme)==i+1 and final_state.tag[0]>state.tag[0]):
                            final_state = state
                            lexeme = string[:i+1]
            
        return final_state, lexeme

    def _tokenize(self, text):
        while text:
            final_state, lexeme = self._walk(text)

            if final_state:
                (priority, token_type) = final_state.tag
                yield lexeme, token_type
                text = text[len(lexeme):]
            else:
                raise LexerError("Tokenization error at: " + text)
        yield '$', self.eof

    def __call__(self, text):
        return [Token(lex, ttype) for lex, ttype in self._tokenize(text)]
