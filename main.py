# from src.cmp.tools.regex import Regex as regex
from src.regex.regex import  regex

#region RE-Test

# Test 1: Single character
r = regex('a')
assert r('a') == True
assert r('b') == False

# Test 2: Kleene star
r = regex('a*')
assert r('') == True
assert r('a') == True
assert r('aa') == True    
assert r('b') == False

# Test 3: Union
r = regex('a|b')
assert r('a') == True
assert r('b') == True
assert r('c') == False

# Test 4: Union with Kleene star
r = regex('a*|b')
assert r('') == True
assert r('a') == True
assert r('aa') == True
assert r('b') == True
assert r('c') == False

# Test 5: Union of Kleene stars
r = regex('a*|b*')
assert r('') == True
assert r('a') == True
assert r('aa') == True
assert r('b') == True
assert r('bb') == True
assert r('c') == False

# Test 6: Concatenation
r = regex('ab')
assert r('ab') == True
assert r('a') == False
assert r('b') == False
assert r('abc') == False

# Test 7: Complex expression with concatenation and union
r = regex('(a|b)c')
assert r('ac') == True
assert r('bc') == True
assert r('cc') == False
assert r('a') == False

# Test 8: Nested Kleene stars
r = regex('(a|b)*c')
assert r('c') == True
assert r('ac') == True
assert r('bc') == True
assert r('aabc') == True
assert r('aabbc') == True
assert r('cc') == False

# Test 9: Union and concatenation with nested Kleene star
r = regex('a*(bc|d)*e')
assert r('e') == True
assert r('ae') == True
assert r('abce') == True
assert r('abcdbce') == True
assert r('aabcbcde') == True
assert r('f') == False

print("All tests passed!")
