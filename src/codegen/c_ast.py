from abc import ABC, abstractmethod
import src.cmp.visitor as visitor

class c_node:
    pass

class c_declaration_node(c_node):
    pass

class c_expression_node(c_node):
    pass


class c_program_node(c_node):
    def __init__(self,include_list,dec_list):
        self.include_list=include_list
        self.dec_list=dec_list


class c_include_statement_node(c_node):
    def __init__(self,lib_name):
        self.lib_name=lib_name

class c_statement_node(c_node):
    def __init__(self,expr):
        self.expr=expr

class c_struct_declaration_node(c_declaration_node):
    def __init__(self,struct_name,body):
        self.struct_name=struct_name
        self.body=body


class c_constant_declaration_node(c_declaration_node):
    def __init__(self,const_name,expr,type):
        self.const_name=const_name
        self.expr=expr


class c_function_declaration_node(c_declaration_node):
    def __init__(self,fun_name,args,body,type):
        self.fun_name=fun_name
        self.args=args
        self.body=body
        self.type=type


class c_variable_declaration_node(c_declaration_node):
    def __init__(self,type, var_name):
        self.var_name=var_name
        self.type=type


class c_expression_block_node(c_node):
    def __init__(self,expr_list):
        self.expr_list=expr_list

class c_and_node(c_expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class c_or_node(c_expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class c_not_node(c_expression_node):
    def __init__(self, expr):
        self.expr = expr

class c_less_node(c_expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class c_less_equal_node(c_expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class c_greater_node(c_expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class c_greater_equal_node(c_expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class c_equals_node(c_expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class c_not_equals_node(c_expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class c_plus_node(c_expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class c_minus_node(c_expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class c_multiply_node(c_expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class c_divide_node(c_expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class c_modulo_node(c_expression_node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class c_negative_node(c_expression_node):
    def __init__(self, expr):
        self.expr = expr

class c_variable_node(c_expression_node):
    def __init__(self, id):
        self.id = id

class c_function_call_node(c_expression_node):
    def __init__(self, id, args):
        self.id = id
        self.args = args

class c_int_node(c_expression_node):
    def __init__(self, value):
        self.value = value

class c_float_node(c_expression_node):
    def __init__(self, value):
        self.value = value

class c_string_node(c_expression_node):
    def __init__(self, value):
        self.value = value

class c_index_node(c_expression_node):
    def __init__(self,array,id):
        self.array =array
        self.id =id

class c_attribute_call_node(c_expression_node):
    def __init__(self, id, atrib):
        self.id = id
        self.atrib = atrib

class c_if_node(c_expression_node):
    def __init__(self, condition, body):
        self.condition= condition
        self.body=body

class c_if_else_node(c_expression_node):
    def __init__(self,condition,body1,body2):
        self.condition= condition
        self.body1=body1
        self.body2=body2

class c_for_node(c_expression_node):
    def __init__(self, var_declaration,condition,iteration,body):
        self.var_declaration=var_declaration
        self.condtion=condition
        self.iteration=iteration
        self.body=body

class c_assignment_node(c_expression_node):
    def __init__(self, variable, expr):
        self.variable = variable
        self.expr = expr

class c_while_node(c_expression_node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class c_return_node(c_expression_node):
    def __init__(self, expr):
        self.expr = expr

class c_scope_node(c_expression_node):
    def __init__(self,expr):
        self.expr = expr