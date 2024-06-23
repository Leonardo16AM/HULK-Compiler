from itertools import islice
from src.cmp.utils import ContainerSet



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
   if self.verbose:print(stack,'<---||--->',w[cursor:])
   if self.verbose:print("ACTION::: ",self.action)
   if(state,lookahead)not in self.action:
    print((state,lookahead))
    print("Error. Aborting...")
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