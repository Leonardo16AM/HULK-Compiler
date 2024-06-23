import src.cmp.visitor as visitor
from src.cmp.ast import *
from abc import ABC, abstractmethod

class node:
    pass



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
    def __init__(self, id, params, features, parent=None):
        self.id = id
        self.params = params
        self.features = features
        self.parent = parent

class protocol_declaration_node(declaration_node):
    def __init__(self, id, functions):
        self.id = id
        self.functions = functions

class variable_declaration_node(declaration_node):
    def __init__(self, id, type_id, value):
        self.id = id
        self.type_id = type_id
        self.value = value

class protocol_declaration_node(declaration_node):
    def __init__(self, id, functions):
        self.id = id
        self.functions = functions

class expression_block_node(expression_node):
    def __init__(self, expressions):
        self.expressions = expressions

class concatenation_node(expression_node):
    def __init__(self, left, right):
        self.left = left
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
    def __init__(self, vector, index):
        self.vector = vector
        self.index = index

class as_node(expression_node):
    def __init__(self, expr, type_id):
        self.expr = expr
        self.type_id = type_id

class property_call_node(expression_node):
    def __init__(self, id, calls):
        self.id = id
        self.calls = calls

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
    def __init__(self, id, expr):
        self.id = id
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
    def __init__(self, id, expr, body):
        self.id = id
        self.expr = expr
        self.body = body

class vector_comprehension_node(expression_node):
    def __init__(self, id, expr, iterable):
        self.id = id
        self.expr = expr
        self.vector = iterable
        