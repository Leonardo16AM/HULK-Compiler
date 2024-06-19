from cmp.ast import AtomicNode,BinaryNode,UnaryNode
from cmp.pycompiler import Grammar
from ..automaton_ops import automata_closure,automata_concatenation,automata_minimization,automata_union,nfa_to_dfa
from ..DFA import DFA
from ..NFA import NFA
from cmp.utils import Token

#region EpsilonNode
class EpsilonNode(AtomicNode):
    def evaluate(self):
        return DFA(states=1,finals=[0],transitions={})

#region SymbolNode
class SymbolNode(AtomicNode):
    def evaluate(self):
        s=self.lex
        return DFA(states=2,finals=[1],transitions={(0,s):1})

#region ClosureNode
class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
      return automata_closure(value)  

#region UnionNode
class UnionNode(BinaryNode):
    @staticmethod
    def operate(left,right):
        return automata_union(left,right)

#region ConcatNode
class ConcatNode(BinaryNode):
    @staticmethod
    def operate(left,right):
        return automata_concatenation(left,right)
 