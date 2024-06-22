from src.cmp.pycompiler import Symbol
from src.cmp.pycompiler import NonTerminal
from src.cmp.pycompiler import Terminal
from src.cmp.pycompiler import EOF
from src.cmp.pycompiler import Sentence, SentenceList
from src.cmp.pycompiler import Epsilon
from src.cmp.pycompiler import Production
from src.cmp.pycompiler import Grammar
from src.cmp.utils import pprint, inspect

G = Grammar()

# region Non Terminals
program = G.NonTerminal('program', startSymbol=True)
dec_list, declaration, function_dec, type_dec, protocol_dec, global_expr = G.NonTerminals('dec_list declaration function_dec type_dec protocol_dec global_expr')
statement, expr_block, single_expr, statement_list, parameters = G.NonTerminals('statement expr_block single_expr statement_list parameters')
parameter, parameter_list, struct_dec_list, struct_dec = G.NonTerminals('parameter parameter_list struct_dec_list struct_dec')
function_post, function_post_list, parameter_post, parameters_post, parameter_post_list = G.NonTerminals('function_post function_post_list parameter_post parameters_post parameter_post_list')
single_expr, arithmetic_expr, boolean_expr, string_expr = G.NonTerminals('single_expr arithmetic_expr boolean_expr string_expr')
boolean_expr_lv2, boolean_expr_lv3, comparation = G.NonTerminals('boolean_expr_lv2 boolean_expr_lv3 comparation')
arithmetic_expr_lv2, arithmetic_expr_lv3, arithmetic_expr_lv4 = G.NonTerminals('arithmetic_expr_lv2, arithmetic_expr_lv3, arithmetic_expr_lv4')
elif_branch, else_branch, var_list, var_list_element, func_call_list = G.NonTerminals('elif_branch else_branch var_list var_list_element func_call_list')
concat_list, single_expr_list, func_call, type_instance, args, general_atom = G.NonTerminals('concat_list single_expr_list func_call type_instance args general_atom')
# endregion

#region Terminals
dot, colon, semicolon, comma, opar, cpar, arrow, lcurly, rcurly, at, double_at, assignment_op, obracket, cbracket, bar_bar = G.Terminals('. : ; , ( ) -> { } @ @@ := [ ] ||')
and_t, or_t = G.Terminals('& |')
equal, plus, minus, star, div, mod, power, not_t, less, greater, less_eq, greater_eq, eq_eq, dif = G.Terminals('= + - * / % ^ ! < > <= >= == !=')
if_t, elif_t, else_t, let, in_t, while_t, for_t, is_t, type_t, function, inherits, protocol, extends, new, as_t = G.Terminals('if elif else let in while for is type function inherits protocol extends new as')
id, num, type_id, string, bool = G.Terminals('id num type_id string bool')
# endregion

# region Productions
program %= dec_list + global_expr

dec_list %= G.Epsilon
dec_list %= declaration + dec_list

declaration %= function_dec
declaration %= type_dec
declaration %= protocol_dec

function_dec %= function + id + opar + parameters + cpar + arrow + statement
function_dec %= function + id + opar + parameters + cpar + expr_block

parameters %= G.Epsilon
parameters %= parameter + parameter_list

parameter_list %= G.Epsilon
parameter_list %= comma + parameter + parameter_list

parameter %= id 
parameter %= id + colon + type_id

type_dec %= type_t + id + lcurly + struct_dec + struct_dec_list + rcurly
type_dec %= type_t + id + inherits + id + lcurly + struct_dec + struct_dec_list + rcurly

struct_dec_list %= G.Epsilon
struct_dec_list %= struct_dec + struct_dec_list

struct_dec %= id + equal + statement
struct_dec %= id + colon + type_id + equal + statement
struct_dec %= function_dec

protocol_dec %= protocol + id + lcurly + function_post + function_post_list + rcurly

function_post_list %= G.Epsilon
function_post_list %= function_post + function_post_list

function_post %= id + opar + parameters_post + cpar + colon + type_id

parameters_post %= G.Epsilon
parameters_post %= parameter_post + parameter_post_list

parameter_post_list %= G.Epsilon
parameter_post_list %= comma + parameter_post + parameter_post_list
 
parameter_post %= id + colon + type_id

global_expr %= statement
global_expr %= expr_block

statement %= single_expr + semicolon

expr_block %= lcurly + statement + statement_list + rcurly
expr_block %= lcurly + expr_block + statement_list + rcurly

statement_list %= G.Epsilon
statement_list %= statement + statement_list
statement_list %= expr_block + statement_list

single_expr %= string_expr
single_expr %= if_t + opar + boolean_expr + cpar + single_expr + elif_branch + else_branch
single_expr %= while_t + opar + boolean_expr + cpar + single_expr
single_expr %= let + var_list_element + var_list + in_t + single_expr
single_expr %= for_t + opar + id + in_t + single_expr + cpar + single_expr
single_expr %= id + assignment_op + single_expr
single_expr %= new + type_instance
single_expr %= single_expr + as_t + type_id
single_expr %= obracket + args + cbracket
single_expr %= obracket + single_expr + bar_bar + id + in_t + single_expr + cbracket

elif_branch %= G.Epsilon
elif_branch %= elif_t + opar + boolean_expr + cpar + single_expr + elif_branch

else_branch %= else_t + single_expr

var_list %= G.Epsilon
var_list %= comma + var_list_element + var_list 

var_list_element %= id + colon + type_id + equal + single_expr
var_list_element %= id + equal + single_expr

string_expr %= boolean_expr
string_expr %= string_expr + at + boolean_expr
string_expr %= string_expr + double_at + boolean_expr

boolean_expr %= boolean_expr_lv2
boolean_expr %= boolean_expr + and_t + boolean_expr_lv2

boolean_expr_lv2 %= boolean_expr_lv3
boolean_expr_lv2 %= boolean_expr_lv2 + or_t + boolean_expr_lv3

boolean_expr_lv3 %= comparation
boolean_expr_lv3 %= not_t + comparation

comparation %= comparation + is_t + type_id
comparation %= arithmetic_expr + less + arithmetic_expr
comparation %= arithmetic_expr + greater + arithmetic_expr
comparation %= arithmetic_expr + less_eq + arithmetic_expr
comparation %= arithmetic_expr + greater_eq + arithmetic_expr
comparation %= arithmetic_expr + eq_eq + arithmetic_expr
comparation %= arithmetic_expr + dif + arithmetic_expr
comparation %= arithmetic_expr

arithmetic_expr %= arithmetic_expr_lv2
arithmetic_expr %= arithmetic_expr + plus + arithmetic_expr_lv2
arithmetic_expr %= arithmetic_expr + minus + arithmetic_expr_lv2

arithmetic_expr_lv2 %= arithmetic_expr_lv3
arithmetic_expr_lv2 %= arithmetic_expr_lv2 + star + arithmetic_expr_lv3
arithmetic_expr_lv2 %= arithmetic_expr_lv2 + div + arithmetic_expr_lv3
arithmetic_expr_lv2 %= arithmetic_expr_lv2 + mod + arithmetic_expr_lv3

arithmetic_expr_lv3 %= arithmetic_expr_lv4
arithmetic_expr_lv3 %= arithmetic_expr_lv4 + power + arithmetic_expr_lv3

arithmetic_expr_lv4 %= general_atom
arithmetic_expr_lv4 %= minus + general_atom

general_atom %= id
general_atom %= func_call
general_atom %= num
general_atom %= bool
general_atom %= string
general_atom %= opar + single_expr + cpar
general_atom %= expr_block
general_atom %= id + obracket + single_expr + cbracket
general_atom %= id + dot + func_call + func_call_list

type_instance %= type_id + opar + args + cpar

func_call_list %= G.Epsilon
func_call_list %= dot + func_call + func_call_list

func_call %= id + opar + args + cpar

args %= G.Epsilon
args %= single_expr + single_expr_list

single_expr_list %= G.Epsilon
single_expr_list %= comma + single_expr + single_expr_list
# endregion

print(G)

