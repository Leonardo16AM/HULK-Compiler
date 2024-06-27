from itertools import islice
from src.cmp.utils import ContainerSet
from src.utils.errors import *



#region compute_local_first
def compute_local_first(firsts,alpha):
 f=firsts
 p=alpha
 D=ContainerSet()
 try:
  P=p.IsEpsilon
 except:
  P=False
 if P:
  D.set_epsilon()
 else:
  for G in p:
   M=f[G]
   D.update(M)
   if not M.contains_epsilon:
    break
  else:
   D.set_epsilon()
 return D
def compute_firsts(G):
 f={}
 E=True
 for b in G.terminals:
  f[b]=ContainerSet(b)
 for t in G.nonTerminals:
  f[t]=ContainerSet()
 while E:
  E=False
  for O in G.Productions:
   X=O.Left
   p=O.Right
   A=f[X]
   try:
    D=f[p]
   except:
    D=f[p]=ContainerSet()
   J=compute_local_first(f,p)
   E|=D.hard_update(J)
   E|=A.hard_update(J)
 return f

#region compute_follows
def compute_follows(G,firsts):
 f=firsts
 q={}
 E=True
 e={}
 for t in G.nonTerminals:
  q[t]=ContainerSet()
 q[G.startSymbol]=ContainerSet(G.EOF)
 while E:
  E=False
  for O in G.Productions:
   X=O.Left
   p=O.Right
   R=q[X]
   for i,sy in enumerate(p):
    if sy.IsNonTerminal:
     Q=q[sy]
     try:
      fb=e[p,i]
     except:
      fb=e[p,i]=compute_local_first(f,islice(p,i+1,None))
     E|=Q.update(fb)
     if fb.contains_epsilon:
      E|=Q.update(R)
 return q

#region build_parsing_table
def build_parsing_table(G,firsts,follows):
 f=firsts
 ff=follows
 M={}
 for a in G.Productions:
  X=a.Left
  P=a.Right
  for e in f[P]:
   try:
    M[X,e].append(a)
   except:
    M[X,e]=[a]
  if f[P].contains_epsilon:
   for e in ff[X]:
    try:
     M[X,e].append(a)
    except:
     M[X,e]=[a]
 return M

#region metodo_predictivo_no_recursivo
def metodo_predictivo_no_recursivo(G,M=None,firsts=None,follows=None):
 fi=firsts
 fo=follows
 if M is None:
  if fi is None:
   fi=compute_firsts(G)
  if fo is None:
   fo=compute_follows(G,fi)
  M=build_parsing_table(G,fi,fo)
 def m(w):
  V=[G.EOF,G.startSymbol]
  mm=0
  z=[]
  while True:
   g=V.pop()
   a=w[mm]
   if g.IsTerminal:
    if g==a:
     if g==G.EOF:
      break
     else:
      mm+=1
    else:
     print("Error. Aborting...")
     return None
   else:
    try:
     P=M[g,a][0]
     for i in range(len(P.Right)-1,-1,-1):
      V.append(P.Right[i])
     z.append(P)
    except:
     print("Error. Aborting...")
     return None
  return z
 return m

deprecated_metodo_predictivo_no_recursivo = metodo_predictivo_no_recursivo
def metodo_predictivo_no_recursivo(G, M=None, firsts=None, follows=None):
    parser = deprecated_metodo_predictivo_no_recursivo(G, M, firsts, follows)
    def updated(tokens):
        return parser([t.token_type for t in tokens])
    return updated


#region SHIFT REDUCE PARSER
class ShiftReduceParser:
 SHIFT='SHIFT'
 REDUCE='REDUCE'
 OK='OK'
 def __init__(self,G,verbose=False):
  self.G=G
  self.verbose=verbose
  self.action={}
  self.goto={}
  self._build_parsing_table()
 def _build_parsing_table(self):
  raise NotImplementedError()
 def __call__(self,w,get_shift_reduce=False):
  stack=[0]
  cursor=0
  output=[]
  operations=[]
  while True:
   state=stack[-1]
   lookahead=w[cursor]
   if self.verbose:print(stack,colored('<---||--->','yellow'),w[cursor:])

   on_state = [ action for action in self.action if action[0]==state]
   
  #  if type(lookahead)==str:
  #   print(on_state[0][0])
  #   print(self.OK)

  #  print(type(self.action))


  #  for action in on_state:
  #   print(action,self.action[action])
  
   if type(lookahead)!=str:
    for action in on_state:
      if action[1].Name==lookahead.Name:
       lookahead=action[1]

  

   if(state,lookahead)not in self.action:
    print(colored(f"ACTION:::  {[action for action in self.action if action[0]==state]}",'red'))
    error("PARSING ERROR","Couldn't find (state,lookahead in self.action)",f" (state,lookahead):({state},{lookahead})")
    return None
   
   action,tag=self.action[state,lookahead]
   if action==self.SHIFT:
    operations.append(self.SHIFT)
    stack+=[lookahead,tag]
    cursor+=1
   elif action==self.REDUCE:
    operations.append(self.REDUCE)
    output.append(tag)
    head,body=tag
    for symbol in reversed(body):
     stack.pop()
     assert stack.pop()==symbol
    state=stack[-1]
    goto=self.goto[state,head]
    stack+=[head,goto]
   elif action==self.OK:
    stack.pop()
    assert stack.pop()==self.G.startSymbol
    assert len(stack)==1
    return output if not get_shift_reduce else(output,operations)
   else:
    raise Exception('Invalid action!!!')
   

from src.cmp.utils import ContainerSet
from src.cmp.pycompiler import Item


# region expand
def expand(d,n):
 y=d.NextSymbol
 if y is None or not y.IsNonTerminal:
  return[]
 V=ContainerSet()
 for E in d.Preview():
  k=compute_local_first(n,E)
  V.update(k)
 assert not V.contains_epsilon
 return[Item(prod,0,V)for prod in y.productions]

# region compress
def compress(A):
 l={}
 for d in A:
  f=d.Center()
  try:
   V=l[f]
  except KeyError:
   l[f]=V=set()
  V.update(d.lookaheads)
 return{Item(x.production,x.pos,set(k))for x,k in l.items()}


# region closure_lr1
def closure_lr1(A,n):
 H=ContainerSet(*A)
 O=True
 while O:
  O=False
  a=ContainerSet()
  for d in H:
   a.extend(expand(d,n))
  O=H.update(a)
 return compress(H)

# region goto_lr1
def goto_lr1(A,P,firsts=None,just_kernel=False):
 assert just_kernel or firsts is not None,'`firsts` must be provided if `just_kernel=False`'
 A=frozenset(d.NextItem()for d in A if d.NextSymbol==P)
 return A if just_kernel else closure_lr1(A,firsts)

from src.cmp.automata import State,multiline_formatter

# region build_LR1_automaton
def build_LR1_automaton(G):
 assert len(G.startSymbol.productions)==1,'Grammar must be augmented'
 n=compute_firsts(G)
 n[G.EOF]=ContainerSet(G.EOF)
 I=G.startSymbol.productions[0]
 o=Item(I,0,lookaheads=(G.EOF,))
 t=frozenset([o])
 H=closure_lr1(t,n)
 r=State(frozenset(H),True)
 v=[t]
 h={t:r}
 from termcolor import colored
 while v:
  print(colored(len(v),'magenta'))
  print("===================")
  L=v.pop()
  U=h[L]
  for P in G.terminals+G.nonTerminals:
   H=closure_lr1(L,n)
   g=goto_lr1(H,P,just_kernel=True)
   if not g:
    continue
   try:
    w=h[g]
   except KeyError:
    H=closure_lr1(g,n)
    w=h[g]=State(frozenset(H),True)
    v.append(g)
   U.add_transition(P.Name,w)
 r.set_formatter(multiline_formatter)
 return r

def build_LR1_automaton(grammar):
    assert len(grammar.startSymbol.productions) == 1, 'La gramática debe estar aumentada'
    firsts_sets = compute_firsts(grammar)
    firsts_sets[grammar.EOF] = ContainerSet(grammar.EOF)
    
    initial_production = grammar.startSymbol.productions[0]
    initial_item = Item(initial_production, 0, lookaheads=(grammar.EOF,))
    initial_set = frozenset([initial_item])
    
    initial_closure = closure_lr1(initial_set, firsts_sets)
    initial_state = State(frozenset(initial_closure), True)
    
    unmarked_states = [initial_set]
    state_map = {initial_set: initial_state}
    
    from termcolor import colored
    while unmarked_states:
        print(colored(len(unmarked_states), 'magenta'))
        print("===================")
        
        current_set = unmarked_states.pop()
        current_state = state_map[current_set]
        
        for symbol in grammar.terminals + grammar.nonTerminals:
            current_closure = closure_lr1(current_set, firsts_sets)
            goto_set = goto_lr1(current_closure, symbol, just_kernel=True)
            if not goto_set:
                continue
            
            try:
                next_state = state_map[goto_set]
            except KeyError:
                next_closure = closure_lr1(goto_set, firsts_sets)
                next_state = state_map[goto_set] = State(frozenset(next_closure), True)
                unmarked_states.append(goto_set)
            
            current_state.add_transition(symbol.Name, next_state)
    
    initial_state.set_formatter(multiline_formatter)
    return initial_state

# region LR1Parser
class LR1Parser(ShiftReduceParser):
 def _build_parsing_table(W):
  G=W.G.AugmentedGrammar(True)
  
  from termcolor import colored
  if W.verbose:
   print(colored(f'Grammar :{G}','cyan'))
  r=build_LR1_automaton(G)
  if W.verbose:
   print(colored(f'States :{r}','yellow'))
  #  r.plot()

  for i,D in enumerate(r):
   if W.verbose:print(i,'\t','\n\t '.join(str(x)for x in D.state),'\n')
   D.idx=i
  for D in r:
   
   if W.verbose:
    print(colored(f'{D}','cyan'))
    print('========================')
   e=D.idx
   for d in D.state:
    if d.IsReduceItem:
     p=d.production
     if p.Left==G.startSymbol:
      W._register(W.action,(e,G.EOF),(W.OK,None))
     else:
      for P in d.lookaheads:
       W._register(W.action,(e,P),(W.REDUCE,p))
    else:
     P=d.NextSymbol
     g=D.get(P.Name).idx
     if P.IsTerminal:
      W._register(W.action,(e,P),(W.SHIFT,g))
     else:
      W._register(W.goto,(e,P),g)
 @staticmethod
 def _register(F,K,N):
  assert K not in F or F[K]==N,'Shift-Reduce or Reduce-Reduce conflict!!!'
  F[K]=N


# class LR1Parser(ShiftReduceParser):
#     def _build_parsing_table(parser_instance):
#         augmented_grammar = parser_instance.G.AugmentedGrammar(True)

#         from termcolor import colored
#         if parser_instance.verbose:
#             print(colored(f'Grammar: {augmented_grammar}', 'cyan'))
        
#         automaton = build_LR1_automaton(augmented_grammar)
        
#         if parser_instance.verbose:
#             print(colored(f'States: {automaton}', 'yellow'))
#         # automaton.plot()

#         for state_index, state in enumerate(automaton):
#             if parser_instance.verbose:
#                 print(state_index, '\t', '\n\t '.join(str(item) for item in state.state), '\n')
#             state.idx = state_index
        
#         for state in automaton:
#             if parser_instance.verbose:
#                 print(colored(f'{state}', 'cyan'))
#                 print('========================')
            
#             state_id = state.idx
#             for item in state.state:
#                 if item.IsReduceItem:
#                     production = item.production
#                     if production.Left == augmented_grammar.startSymbol:
#                         parser_instance._register(parser_instance.action, (state_id, augmented_grammar.EOF), (parser_instance.OK, None))
#                     else:
#                         for lookahead in item.lookaheads:
#                             parser_instance._register(parser_instance.action, (state_id, lookahead), (parser_instance.REDUCE, production))
#                 else:
#                     next_symbol = item.NextSymbol
#                     next_state_id = state.get(next_symbol.Name).idx
#                     if next_symbol.IsTerminal:
#                         parser_instance._register(parser_instance.action, (state_id, next_symbol), (parser_instance.SHIFT, next_state_id))
#                     else:
#                         parser_instance._register(parser_instance.goto, (state_id, next_symbol), next_state_id)
