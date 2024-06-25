from src.cmp.pycompiler import Grammar
from src.grammar.hulk_ast import*
 
G = Grammar()

# region Non Terminals
program = G.NonTerminal('program', startSymbol=True)
dec_list, declaration, function_dec, type_dec, protocol_dec, global_expr = G.NonTerminals(
    'dec_list declaration function_dec type_dec protocol_dec global_expr')

statement, expr_block, single_expr, statement_list, parameters = G.NonTerminals(
    'statement expr_block single_expr statement_list parameters')

parameter_list, feature_list, feature, method_dec = G.NonTerminals(
    'parameter_list feature_list feature method_dec')

function_post, function_post_list, parameters_post, parameter_post_list = G.NonTerminals(
    'function_post function_post_list parameters_post parameter_post_list')

single_expr, single_expr_lv2, arithmetic_expr, boolean_expr, string_expr = G.NonTerminals(
    'single_expr single_expr_lv2 arithmetic_expr boolean_expr string_expr')

boolean_expr_lv2, boolean_expr_lv3, comparation, molecule = G.NonTerminals(
    'boolean_expr_lv2 boolean_expr_lv3 comparation molecule')

arithmetic_expr_lv2, arithmetic_expr_lv3, arithmetic_expr_lv4 = G.NonTerminals(
    'arithmetic_expr_lv2 arithmetic_expr_lv3 arithmetic_expr_lv4')

elif_branch, var_list = G.NonTerminals('elif_branch var_list')

arg_list, func_call, args, general_atom = G.NonTerminals(
    'arg_list func_call args general_atom')
# endregion

# region Terminals
dot, colon, semicolon, comma, opar, cpar, arrow, lcurly, rcurly = G.Terminals(
    '. : ; , ( ) => { }')

at, double_at, assignment_op, obracket, cbracket, bar_bar = G.Terminals(
    '@ @@ := [ ] ||')

and_t, or_t = G.Terminals('& |')

equal, plus, minus, star, star_star, div, mod, caret, not_t = G.Terminals(
    '= + - * ** / % ^ !')

less, greater, less_eq, greater_eq, eq_eq, dif = G.Terminals(
    '< > <= >= == !=')

if_t, elif_t, else_t, let, in_t, while_t, for_t, is_t = G.Terminals(
    'if elif else let in while for is')

type_t, function, inherits, protocol, extends, new, as_t = G.Terminals(
    'type function inherits protocol extends new as')

id, num, string, bool = G.Terminals('id num string bool')
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
function_dec %= function + id + opar + parameters + cpar + colon + id + arrow + statement, lambda h, s: function_declaration_node(s[2], s[4], s[7], s[9])
function_dec %= function + id + opar + parameters + cpar + colon + id + expr_block, lambda h, s: function_declaration_node(s[2], s[4], s[7], s[8])

method_dec %= id + opar + parameters + cpar + arrow + statement, lambda h, s: function_declaration_node(s[1], s[3], None, s[6])
method_dec %= id + opar + parameters + cpar + expr_block, lambda h, s: function_declaration_node(s[1], s[3], None, s[5])
method_dec %= id + opar + parameters + cpar + colon + id + arrow + statement, lambda h, s: function_declaration_node(s[1], s[3], s[6], s[8])
method_dec %= id + opar + parameters + cpar + colon + id + expr_block, lambda h, s: function_declaration_node(s[1], s[3], s[6], s[7])

parameters %= G.Epsilon, lambda h, s: []
parameters %= parameter_list, lambda h, s: s[1]

parameter_list %= id, lambda h, s: [variable_declaration_node(s[1], None, None)]
parameter_list %= id + colon + id, lambda h, s: [variable_declaration_node(s[1], s[3], None)]
parameter_list %= id + comma + parameter_list, lambda h, s: [variable_declaration_node(s[1], None, None)] + s[3]
parameter_list %= id + colon + id + comma + parameter_list, lambda h, s: [variable_declaration_node(s[1], s[3], None)] + s[5]

type_dec %= type_t + id + lcurly + feature_list + rcurly, lambda h, s: type_declaration_node(s[2], [], None, [], s[4])
type_dec %= type_t + id + opar + parameters + cpar + lcurly + feature_list + rcurly, lambda h, s: type_declaration_node(s[2], s[4], None, [], s[7])
type_dec %= type_t + id + inherits + id + lcurly + feature_list + rcurly, lambda h, s: type_declaration_node(s[2], [], s[4], [], s[6])
type_dec %= type_t + id + inherits + id  + opar + args + cpar + lcurly + feature_list + rcurly, lambda h, s: type_declaration_node(s[2], [], s[4], s[6], s[9])
type_dec %= type_t + id + opar + parameters + cpar + inherits + id + lcurly + feature_list + rcurly, lambda h, s: type_declaration_node(s[2], s[4], s[7], [], s[9])
type_dec %= type_t + id + opar + parameters + cpar + inherits + id + opar + args + cpar + lcurly + feature_list + rcurly, lambda h, s: type_declaration_node(s[2], s[4], s[7], s[9], s[12])

feature_list %= G.Epsilon, lambda h, s: []
feature_list %= feature + feature_list, lambda h, s: [s[1]] + s[2]

feature %= id + equal + statement, lambda h, s: variable_declaration_node(s[1], None, s[3])
feature %= id + colon + id + equal + statement, lambda h, s: variable_declaration_node(s[1], s[3], s[5])
feature %= method_dec, lambda h, s: s[1]

protocol_dec %= protocol + id + lcurly + function_post + function_post_list + rcurly, lambda h, s: protocol_declaration_node(s[2], [s[4]]+s[5], None)
protocol_dec %= protocol + id + extends + id + lcurly + function_post + function_post_list + rcurly, lambda h, s: protocol_declaration_node(s[2], [s[6]]+s[7], s[4])

function_post_list %= G.Epsilon, lambda h, s: []
function_post_list %= function_post + function_post_list, lambda h, s: [s[1]] + s[2]

function_post %= id + opar + parameters_post + cpar + colon + id + semicolon, lambda h, s: function_declaration_node(s[1], s[3], s[6], None)

parameters_post %= G.Epsilon, lambda h, s: []
parameters_post %= parameter_post_list, lambda h, s: s[1]

parameter_post_list %= id + colon + id, lambda h, s: [variable_declaration_node(s[1], s[3], None)]
parameter_post_list %= id + colon + id + comma + parameter_post_list, lambda h, s: [variable_declaration_node(s[1], s[3], None)] + s[5]

global_expr %= statement, lambda h, s: s[1]
global_expr %= expr_block, lambda h, s: s[1]

statement %= single_expr + semicolon, lambda h, s: s[1]

expr_block %= lcurly + statement_list + rcurly, lambda h, s: expression_block_node(s[2])

statement_list %= statement, lambda h, s: [s[1]]
statement_list %= statement + statement_list, lambda h, s: [s[1]] + s[2]

single_expr %= single_expr_lv2, lambda h, s: s[1]
single_expr %= new + id + opar + args + cpar, lambda h, s: new_node(s[2], s[4])
single_expr %= molecule + assignment_op + single_expr, lambda h, s: assignment_node(s[1], s[3])
single_expr %= let + var_list + in_t + single_expr, lambda h, s: let_node(s[2], s[4])
single_expr %= while_t + opar + boolean_expr + cpar + single_expr, lambda h, s: while_node(s[3], s[5])
single_expr %= for_t + opar + id + in_t + single_expr + cpar + single_expr, lambda h, s: for_node(variable_declaration_node(s[3], None, None), s[5], s[7])
single_expr %= if_t + opar + boolean_expr + cpar + single_expr + elif_branch + else_t + single_expr, lambda h, s: if_node([(s[3], s[5])] + s[6] + [(bool_node(True), s[8])])

single_expr_lv2 %= string_expr, lambda h, s: s[1]
single_expr_lv2 %= string_expr + as_t + id, lambda h, s: as_node(s[1], s[3])

elif_branch %= G.Epsilon, lambda h, s: []
elif_branch %= elif_t + opar + boolean_expr + cpar + single_expr + elif_branch, lambda h, s: [(s[3], s[5])] + s[6]

var_list %= id + equal + single_expr, lambda h, s: [variable_declaration_node(s[1], None, s[3])]
var_list %= id + colon + id + equal + single_expr, lambda h, s: [variable_declaration_node(s[1], s[3], s[5])]
var_list %= id + equal + single_expr + comma + var_list, lambda h, s: [variable_declaration_node(s[1], None, s[3])] + s[5]
var_list %= id + colon + id + equal + single_expr + comma + var_list, lambda h, s: [variable_declaration_node(s[1], s[3], s[5])] + s[7]

string_expr %= boolean_expr, lambda h, s: s[1]
string_expr %= string_expr + at + boolean_expr, lambda h, s: concatenation_node(s[1], '', s[3]) #add the space in the middle
string_expr %= string_expr + double_at + boolean_expr, lambda h, s: concatenation_node(s[1], ' ', s[3])

# boolean_expr %= molecule, lambda h, s: s[1]
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
comparation %= arithmetic_expr + is_t + id, lambda h, s: is_node(s[1], s[3])

arithmetic_expr %= arithmetic_expr_lv2, lambda h, s: s[1]
arithmetic_expr %= arithmetic_expr + plus + arithmetic_expr_lv2, lambda h, s: plus_node(s[1], s[3])
arithmetic_expr %= arithmetic_expr + minus + arithmetic_expr_lv2, lambda h, s: minus_node(s[1], s[3])

arithmetic_expr_lv2 %= arithmetic_expr_lv3, lambda h, s: s[1]
arithmetic_expr_lv2 %= arithmetic_expr_lv2 + div + arithmetic_expr_lv3, lambda h, s: divide_node(s[1], s[3])
arithmetic_expr_lv2 %= arithmetic_expr_lv2 + mod + arithmetic_expr_lv3, lambda h, s: modulo_node(s[1], s[3])
arithmetic_expr_lv2 %= arithmetic_expr_lv2 + star + arithmetic_expr_lv3, lambda h, s: multiply_node(s[1], s[3])

arithmetic_expr_lv3 %= arithmetic_expr_lv4, lambda h, s: s[1]
arithmetic_expr_lv3 %= minus + arithmetic_expr_lv3, lambda h, s: negative_node(s[2])

arithmetic_expr_lv4 %= molecule, lambda h, s: s[1]
arithmetic_expr_lv4 %= molecule + caret + arithmetic_expr_lv4, lambda h, s: power_node(s[1], s[3])
arithmetic_expr_lv4 %= molecule + star_star + arithmetic_expr_lv4, lambda h, s: power_node(s[1], s[3])

molecule %= general_atom, lambda h, s: s[1]
molecule %= molecule + dot + func_call, lambda h, s: property_call_node(s[1], s[3])
molecule %= molecule + dot + id, lambda h, s: attribute_call_node(s[1], s[3])
molecule %= molecule + obracket + single_expr + cbracket, lambda h, s: index_node(s[1], s[3])

general_atom %= id, lambda h, s: variable_node(s[1])
general_atom %= num, lambda h, s: number_node(s[1])
general_atom %= bool, lambda h, s: bool_node(s[1])
general_atom %= string, lambda h, s: string_node(s[1])
general_atom %= func_call, lambda h, s: s[1]
general_atom %= expr_block, lambda h, s: s[1]
general_atom %= opar + single_expr + cpar, lambda h, s: s[2]
general_atom %= obracket + args + cbracket, lambda h, s: vector_node(s[2])
general_atom %= obracket + single_expr + bar_bar + id + in_t + single_expr + cbracket, lambda h, s: vector_comprehension_node(variable_declaration_node(s[4], None, None), s[2], s[6])

func_call %= id + opar + args + cpar, lambda h, s: function_call_node(s[1], s[3])

args %= G.Epsilon, lambda h, s: []
args %= single_expr + arg_list, lambda h, s: [s[1]] + s[2]

arg_list %= G.Epsilon, lambda h, s: []
arg_list %= comma + single_expr + arg_list, lambda h, s: [s[2]] + s[3]


# endregion






















'''
                                            ⠄⠄⠄⢰⣧⣼⣯⠄⣸⣠⣶⣶⣦⣾⠄⠄⠄⠄⡀⠄⢀⣿⣿⠄⠄⠄⢸⡇⠄⠄
                                            ⠄⠄⠄⣾⣿⠿⠿⠶⠿⢿⣿⣿⣿⣿⣦⣤⣄⢀⡅⢠⣾⣛⡉⠄⠄⠄⠸⢀⣿⠄
                                            ⠄⠄⢀⡋⣡⣴⣶⣶⡀⠄⠄⠙⢿⣿⣿⣿⣿⣿⣴⣿⣿⣿⢃⣤⣄⣀⣥⣿⣿⠄
                                            ⠄⠄⢸⣇⠻⣿⣿⣿⣧⣀⢀⣠⡌⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⣿⣿⣿⠄
                                            ⠄⢀⢸⣿⣷⣤⣤⣤⣬⣙⣛⢿⣿⣿⣿⣿⣿⣿⡿⣿⣿⡍⠄⠄⢀⣤⣄⠉⠋⣰
                                            ⠄⣼⣖⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⢇⣿⣿⡷⠶⠶⢿⣿⣿⠇⢀⣤
                                            ⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣷⣶⣥⣴⣿⡗
                                            ⢀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠄
                                            ⢸⣿⣦⣌⣛⣻⣿⣿⣧⠙⠛⠛⡭⠅⠒⠦⠭⣭⡻⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠄
                                            ⠘⣿⣿⣿⣿⣿⣿⣿⣿⡆⠄⠄⠄⠄⠄⠄⠄⠄⠹⠈⢋⣽⣿⣿⣿⣿⣵⣾⠃⠄
                                            ⠄⠘⣿⣿⣿⣿⣿⣿⣿⣿⠄⣴⣿⣶⣄⠄⣴⣶⠄⢀⣾⣿⣿⣿⣿⣿⣿⠃⠄⠄
                                            ⠄⠄⠈⠻⣿⣿⣿⣿⣿⣿⡄⢻⣿⣿⣿⠄⣿⣿⡀⣾⣿⣿⣿⣿⣛⠛⠁⠄⠄⠄
                                            ⠄⠄⠄⠄⠈⠛⢿⣿⣿⣿⠁⠞⢿⣿⣿⡄⢿⣿⡇⣸⣿⣿⠿⠛⠁⠄⠄⠄⠄⠄
                                            ⠄⠄⠄⠄⠄⠄⠄⠉⠻⣿⣿⣾⣦⡙⠻⣷⣾⣿⠃⠿⠋⠁⠄⠄⠄⠄⠄⢀⣠⣴
                                            ⣿⣿⣿⣶⣶⣮⣥⣒⠲⢮⣝⡿⣿⣿⡆⣿⡿⠃⠄⠄⠄⠄⠄⠄⠄⣠⣴⣿⣿⣿
'''