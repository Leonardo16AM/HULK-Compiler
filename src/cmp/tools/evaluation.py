from src.cmp.pycompiler import EOF
G=iter
b=next
n=isinstance
D=None
K=len
F=enumerate
def evaluate_parse(f,J):
 if not f or not J:
  return
 f=G(f)
 J=G(J)
 x=evaluate(b(f),f,J)
 assert n(b(J).token_type,EOF)
 return x
def evaluate(production,f,J,inherited_value=D):
 N,l=production
 y=production.attributes
 t=[D]*(K(l)+1)
 k=[D]*(K(l)+1)
 k[0]=inherited_value
 for i,R in F(l,1):
  if R.IsTerminal:
   assert k[i]is D
   t[i]=b(J).lex
  else:
   H=b(f)
   assert R==H.Left
   P=y[i]
   if P is not D:
    k[i]=P(k,t)
   t[i]=evaluate(H,f,J,k[i])
 P=y[0]
 return P(k,t)if P is not D else D
