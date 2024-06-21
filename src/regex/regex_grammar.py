from src.cmp.pycompiler import Grammar
from src.regex.regex_nodes import *

#region regex_grammar
def regex_grammar():
    G=Grammar()

    base=G.NonTerminal('<base>',True)

    bext,kleene,batch,union,concat,kext = G.NonTerminals('<bext> <kleene> <batch> <union> <concat> <kext>')
    pipe,star,oppar,clpar,symb,eps = G.Terminals('| * ( ) symbol ε')

    base %= bext+union,lambda h,s:s[2],None,lambda h,s:s[1]

    union %= pipe+base,lambda h,s:OrNode(h[0],s[2])
    union %= G.Epsilon,lambda h,s:h[0]

    bext %= kleene+concat,lambda h,s:s[2],None,lambda h,s:s[1]

    concat %= bext,lambda h,s:ConcatNode(h[0],s[1])
    concat %= G.Epsilon,lambda h,s:h[0]

    kleene %= batch+kext,lambda h,s:s[2],None,lambda h,s:s[1]
    
    kext %= star,lambda h,s:ClosureNode(h[0])
    kext %= G.Epsilon,lambda h,s:h[0]
    
    batch %= symb,lambda h,s:SymbolNode(s[1])
    batch %= eps,lambda h,s:EpsilonNode(s[1])
    batch %= oppar+base+clpar,lambda h,s:s[2]

    return G
