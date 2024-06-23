from src.cmp.pycompiler import Grammar
from grammar.hulk_ast import*
 
G = Grammar()

# region Non Terminals
program = G.NonTerminal('program', startSymbol=True)
dec_list, declaration, function_dec, type_dec, protocol_dec, global_expr = G.NonTerminals('dec_list declaration function_dec type_dec protocol_dec global_expr')
statement, expr_block, single_expr, statement_list, parameters = G.NonTerminals('statement expr_block single_expr statement_list parameters')
parameter, parameter_list, feature_list, feature = G.NonTerminals('parameter parameter_list feature_list feature')
function_post, function_post_list, parameter_post, parameters_post, parameter_post_list = G.NonTerminals('function_post function_post_list parameter_post parameters_post parameter_post_list')
single_expr, arithmetic_expr, boolean_expr, string_expr = G.NonTerminals('single_expr arithmetic_expr boolean_expr string_expr')
boolean_expr_lv2, boolean_expr_lv3, comparation = G.NonTerminals('boolean_expr_lv2 boolean_expr_lv3 comparation')
arithmetic_expr_lv2, arithmetic_expr_lv3, arithmetic_expr_lv4 = G.NonTerminals('arithmetic_expr_lv2, arithmetic_expr_lv3, arithmetic_expr_lv4')
elif_branch, else_branch, var_list, var_list_element, func_call_list = G.NonTerminals('elif_branch else_branch var_list var_list_element func_call_list')
concat_list, arg_list, func_call, type_instance, args, general_atom = G.NonTerminals('concat_list arg_list func_call type_instance args general_atom')
# endregion

#region Terminals
dot, colon, semicolon, comma, opar, cpar, arrow, lcurly, rcurly, at, double_at, assignment_op, obracket, cbracket, bar_bar = G.Terminals('. : ; , ( ) -> { } @ @@ := [ ] ||')
and_t, or_t = G.Terminals('& |')
equal, plus, minus, star, div, mod, power, not_t, less, greater, less_eq, greater_eq, eq_eq, dif = G.Terminals('= + - * / % ^ ! < > <= >= == !=')
if_t, elif_t, else_t, let, in_t, while_t, for_t, is_t, type_t, function, inherits, protocol, extends, new, as_t = G.Terminals('if elif else let in while for is type function inherits protocol extends new as')
id, num, type_id, string, bool = G.Terminals('id num type_id string bool')
# endregion

# region Productions
program %= dec_list + global_expr, lambda h, s: program_node(s[1], s[2])

dec_list %= G.Epsilon, lambda h, s: []
dec_list %= declaration + dec_list, lambda h, s: [s[1]] + s[2]

declaration %= function_dec, lambda h, s: s[1]
declaration %= type_dec, lambda h, s: s[1]
declaration %= protocol_dec, lambda h, s: s[1]

function_dec %= function + id + opar + parameters + cpar + arrow + statement, lambda h, s: function_declaration_node(s[2], s[4], None, s[7])
function_dec %= function + id + opar + parameters + cpar + expr_block, lambda h, s: function_declaration_node(s[2], s[4], None, s[6])
function_dec %= function + id + opar + parameters + cpar + colon + type_id + arrow + statement, lambda h, s: function_declaration_node(s[2], s[4], s[7], s[9])
function_dec %= function + id + opar + parameters + cpar + colon + type_id + expr_block, lambda h, s: function_declaration_node(s[2], s[4], s[7], s[8])

parameters %= G.Epsilon, lambda h, s: []
parameters %= parameter_list, lambda h, s: s[2]

parameter_list %= id, lambda h, s: [(s[1], None)]
parameter_list %= id + colon + type_id, lambda h, s: [(s[1], s[3])]
parameter_list %= id + comma + parameter_list, lambda h, s: [(s[1], None)] + s[3]
parameter_list %= id + colon + type_id + comma + parameter_list, lambda h, s: [(s[1], s[3])] + s[5]

# id, params, features, parent
type_dec %= type_t + id + lcurly + feature + feature_list + rcurly, lambda h, s: type_declaration_node(s[2], [], [s[4]]+s[5], None)
type_dec %= type_t + id + inherits + id + lcurly + feature + feature_list + rcurly, lambda h, s: type_declaration_node(s[2], [], [s[6]]+s[7], s[4])
type_dec %= type_t + id + opar + parameters + cpar + lcurly + feature + feature_list + rcurly, lambda h, s: type_declaration_node(s[2], s[4], [s[7]]+s[8], None)
type_dec %= type_t + id + inherits + id + opar + parameters + cpar + lcurly + feature + feature_list + rcurly, lambda h, s: type_declaration_node(s[2], s[6], [s[9]]+s[10], s[4])

feature_list %= G.Epsilon, lambda h, s: []
feature_list %= feature + feature_list, lambda h, s: [s[1]] + s[2]

feature %= id + equal + statement, lambda h, s: variable_declaration_node(s[1], None, s[3])
feature %= id + colon + type_id + equal + statement, lambda h, s: variable_declaration_node(s[1], s[3], s[5])
feature %= function_dec, lambda h, s: s[1]

protocol_dec %= protocol + id + lcurly + function_post + function_post_list + rcurly, lambda h, s: protocol_declaration_node(s[2], [s[4]]+s[5])

function_post_list %= G.Epsilon, lambda h, s: []
function_post_list %= function_post + function_post_list, lambda h, s: [s[1]] + s[2]

function_post %= id + opar + parameters_post + cpar + colon + type_id + semicolon, lambda h, s: function_declaration_node(s[1], s[3], s[6], None)

parameters_post %= G.Epsilon, lambda h, s: []
parameters_post %= parameter_post_list, lambda h, s: s[2]

parameter_post_list %= id + colon + type_id, lambda h, s: [(s[1], s[3])]
parameter_post_list %= id + colon + type_id + comma + parameter_post_list, lambda h, s: [(s[1], s[3])] + s[5]

global_expr %= statement, lambda h, s: s[1]
global_expr %= expr_block, lambda h, s: s[1]

statement %= single_expr + semicolon, lambda h, s: s[1]

expr_block %= lcurly + statement_list + rcurly, lambda h, s: expression_block_node(s[2])
expr_block %= lcurly + statement_list + rcurly, lambda h, s: expression_block_node(s[2])

statement_list %= statement, lambda h, s: [s[1]]
statement_list %= expr_block, lambda h, s: [s[1]]
statement_list %= statement + statement_list, lambda h, s: [s[1]] + s[2]
statement_list %= expr_block + statement_list, lambda h, s: [s[1]] + s[2]

single_expr %= string_expr, lambda h, s: s[1]
single_expr %= obracket + args + cbracket, lambda h, s: vector_node(s[2])
single_expr %= single_expr + is_t + type_id, lambda h, s: is_node(s[1], s[3])
single_expr %= id + assignment_op + single_expr, lambda h, s: assignment_node(s[1], s[3])
single_expr %= new + type_id + opar + args + cpar, lambda h, s: new_node(s[2], s[4])
single_expr %= let + var_list + in_t + single_expr, lambda h, s: let_node(s[2], s[5])
single_expr %= while_t + opar + boolean_expr + cpar + single_expr, lambda h, s: while_node(s[3], s[5])
single_expr %= for_t + opar + id + in_t + single_expr + cpar + single_expr, lambda h, s: for_node(variable_declaration_node(s[3], None, None), s[5], s[7])
single_expr %= obracket + single_expr + bar_bar + id + in_t + single_expr + cbracket, lambda h, s: vector_comprehension_node(variable_declaration_node(s[4]), s[2], s[6])
single_expr %= if_t + opar + boolean_expr + cpar + single_expr + elif_branch + else_t + single_expr, lambda h, s: if_node([(s[3], s[5])] + s[6] + [(True, s[7])])

elif_branch %= G.Epsilon, lambda h, s: []
elif_branch %= elif_t + opar + boolean_expr + cpar + single_expr + elif_branch, lambda h, s: [(s[3], s[5])] + s[6]

var_list %= id + equal + single_expr, lambda h, s: [variable_declaration_node(s[1], None, s[3])]
var_list %= id + colon + type_id + equal + single_expr, lambda h, s: [variable_declaration_node(s[1], s[3], s[5])]
var_list %= id + equal + single_expr + comma + var_list, lambda h, s: [variable_declaration_node(s[1], None, s[3])] + s[5]
var_list %= id + colon + type_id + equal + single_expr + comma + var_list, lambda h, s: [variable_declaration_node(s[1], s[3], s[5])] + s[7]

string_expr %= boolean_expr, lambda h, s: s[1]
string_expr %= string_expr + at + boolean_expr, lambda h, s: concatenation_node(s[1], s[3])
string_expr %= string_expr + double_at + boolean_expr, lambda h, s: concatenation_node(s[1], s[3])

boolean_expr %= boolean_expr_lv2, lambda h, s: s[1]
boolean_expr %= boolean_expr + and_t + boolean_expr_lv2, lambda h, s: and_node(s[1], s[3])

boolean_expr_lv2 %= boolean_expr_lv3, lambda h, s: s[1]
boolean_expr_lv2 %= boolean_expr_lv2 + or_t + boolean_expr_lv3, lambda h, s: or_node(s[1], s[3])

boolean_expr_lv3 %= comparation, lambda h, s: s[1]
boolean_expr_lv3 %= not_t + comparation, lambda h, s: not_node(s[2])

comparation %= arithmetic_expr, lambda h, s: s[1]
comparation %= arithmetic_expr + dif + arithmetic_expr, lambda h, s: not_equals_node(s[1], s[3])
comparation %= arithmetic_expr + less + arithmetic_expr, lambda h, s: less_node(s[1], s[3])
comparation %= arithmetic_expr + eq_eq + arithmetic_expr, lambda h, s: equals_node(s[1], s[3])
comparation %= arithmetic_expr + greater + arithmetic_expr, lambda h, s: greater_node(s[1], s[3])
comparation %= arithmetic_expr + less_eq + arithmetic_expr, lambda h, s: less_equal_node(s[1], s[3])
comparation %= arithmetic_expr + greater_eq + arithmetic_expr, lambda h, s: greater_equal_node(s[1], s[3])

arithmetic_expr %= arithmetic_expr_lv2, lambda h, s: s[1]
arithmetic_expr %= arithmetic_expr + plus + arithmetic_expr_lv2, lambda h, s: plus_node(s[1], s[3])
arithmetic_expr %= arithmetic_expr + minus + arithmetic_expr_lv2, lambda h, s: minus_node(s[1], s[3])

arithmetic_expr_lv2 %= arithmetic_expr_lv3, lambda h, s: s[1]
arithmetic_expr_lv2 %= arithmetic_expr_lv2 + div + arithmetic_expr_lv3, lambda h, s: divide_node(s[1], s[3])
arithmetic_expr_lv2 %= arithmetic_expr_lv2 + mod + arithmetic_expr_lv3, lambda h, s: modulo_node(s[1], s[3])
arithmetic_expr_lv2 %= arithmetic_expr_lv2 + star + arithmetic_expr_lv3, lambda h, s: multiply_node(s[1], s[3])

arithmetic_expr_lv3 %= arithmetic_expr_lv4, lambda h, s: s[1]
arithmetic_expr_lv3 %= minus + arithmetic_expr_lv3, lambda h, s: minus_node(0, s[2])

arithmetic_expr_lv4 %= general_atom, lambda h, s: s[1]
arithmetic_expr_lv4 %= general_atom + power + arithmetic_expr_lv4, lambda h, s: power_node(s[1], s[3])

general_atom %= id, lambda h, s: variable_node(s[1])
general_atom %= num, lambda h, s: number_node(s[1])
general_atom %= bool, lambda h, s: bool_node(s[1])
general_atom %= string, lambda h, s: string_node(s[1])
general_atom %= func_call, lambda h, s: s[1]
general_atom %= expr_block, lambda h, s: s[1]
general_atom %= opar + single_expr + cpar, lambda h, s: s[2]
general_atom %= general_atom + as_t + type_id, lambda h, s: as_node(s[1], s[3])
general_atom %= id + dot + func_call + func_call_list, lambda h, s: property_call_node(s[1], [s[3]]+s[4])
general_atom %= id + obracket + single_expr + cbracket, lambda h, s: index_node(s[1], s[3])

func_call_list %= G.Epsilon, lambda h, s: []
func_call_list %= dot + func_call + func_call_list, lambda h, s: [s[2]] + s[3]

func_call %= id + opar + args + cpar, lambda h, s: function_call_node(s[1], s[3])

args %= G.Epsilon, lambda h, s: []
args %= single_expr + arg_list, lambda h, s: [s[1]] + s[3]

arg_list %= G.Epsilon, lambda h, s: []
arg_list %= comma + single_expr + arg_list, lambda h, s: [s[2]] + s[3]
# endregion



