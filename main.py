from src.regex.regex import regex
from src.regex.regex_grammar import *

#Testing regex functions

G=regex_grammar()

print(G)

#Test 1
# r=regex('a')
# assert r('a')==True
# assert r('b')==False

# #Test 2
# r=regex('a*')
# assert r('')==True
# assert r('a')==True
# assert r('aa')==True    
# assert r('b')==False

# #Test 3
# r=regex('a|b')
# assert r('a')==True
# assert r('b')==True
# assert r('c')==False

# #Test 4
# r=regex('a*|b')
# assert r('')==True
# assert r('a')==True
# assert r('aa')==True
# assert r('b')==True
# assert r('c')==False

#Test 5
r=regex('a*|b*')
# assert r('')==True
# assert r('a')==True
# assert r('aa')==True
# assert r('b')==True
# assert r('bb')==True
# assert r('c')==False
