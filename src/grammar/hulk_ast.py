from src.cmp.ast import *

class node:
    line = '0'
    scope = None

class program_node(node):
    def __init__(self, dec_list, global_expr):
        self.dec_list = dec_list
        self.global_expr = global_expr

class declaration_node(node):
    pass

class expression_node(node):
    pass


class function_declaration_node(declaration_node):
    def __init__(self, id, params, return_type, body):
        self.id = id
        self.params = params
        self.return_type = return_type
        self.body = body

class type_declaration_node(declaration_node):
    def __init__(self, id, params, parent, args, features):
        self.id = id
        self.params = params
        self.parent = parent
        self.args = args
        self.features = features

class protocol_declaration_node(declaration_node):
    def __init__(self, id, functions, parent):
        self.id = id
        self.functions = functions
        self.parent = parent

class variable_declaration_node(declaration_node):
    def __init__(self, id, type_id, value):
        self.id = id
        self.type_id = type_id
        self.value = value


class expression_block_node(expression_node):
    def __init__(self, expressions):
        self.expressions = expressions

class concatenation_node(expression_node):
    def __init__(self, left, middle ,right):
        self.left = left
        self.middle = middle
        self.right = right

class and_node(expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class or_node(expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class not_node(expression_node):
    def __init__(self, expr):
        self.expr = expr

class is_node(expression_node):
    def __init__(self, expr, type_id):
        self.expr = expr
        self.type_id = type_id

class less_node(expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class less_equal_node(expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class greater_node(expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class greater_equal_node(expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class equals_node(expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class not_equals_node(expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class plus_node(expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class minus_node(expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class multiply_node(expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class divide_node(expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class modulo_node(expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class negative_node(expression_node):
    def __init__(self, expr):
        self.expr = expr

class power_node(expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class variable_node(expression_node):
    def __init__(self, id):
        self.id = id

class function_call_node(expression_node):
    def __init__(self, id, args):
        self.id = id
        self.args = args

class number_node(expression_node):
    def __init__(self, value):
        self.value = value

class bool_node(expression_node):
    def __init__(self, value):
        self.value = value

class string_node(expression_node):
    def __init__(self, value):
        self.value = value

class index_node(expression_node):
    def __init__(self, expr, index):
        self.expr = expr
        self.index = index

class as_node(expression_node):
    def __init__(self, expr, type_id):
        self.expr = expr
        self.type_id = type_id

class property_call_node(expression_node):
    def __init__(self, expr, func):
        self.expr = expr
        self.func = func

class attribute_call_node(expression_node):
    def __init__(self, expr, id):
        self.expr = expr
        self.id = id

class if_node(expression_node):
    def __init__(self, conditions_bodies):
        self.conditions_bodies = conditions_bodies

class vector_node(expression_node):
    def __init__(self, elements):
        self.elements = elements

class new_node(expression_node):
    def __init__(self, type_id, args):
        self.type_id = type_id
        self.args = args

class assignment_node(expression_node):
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

class let_node(expression_node):
    def __init__(self, declarations, body):
        self.declarations = declarations
        self.body = body

class while_node(expression_node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class for_node(expression_node):
    def __init__(self, variable, expr, body):
        self.variable = variable
        self.expr = expr
        self.body = body

class vector_comprehension_node(expression_node):
    def __init__(self, variable, expr, iterable):
        self.variable = variable 
        self.expr = expr
        self.vector = iterable
        