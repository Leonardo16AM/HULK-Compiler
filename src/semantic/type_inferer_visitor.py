from typing import List
import itertools as itt
from collections import OrderedDict
import src.cmp.visitor as visitor
from src.utils.errors import error
from src.cmp.semantic import Context, Scope, Type, ErrorType, VoidType, IntType, SemanticError,VectorType
from src.grammar.hulk_ast import *
from termcolor import colored


class type_inferer:

    def __init__(self, context, errors=None, warnings=None):
        if errors is None:
            errors = []
        if warnings is None:
            warnings = []
        self.context: Context = context
        self.current_type = None
        self.errors = errors
        self.warnings = warnings
        self.object_type=self.context.get_type("Object")

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(program_node)
    def visit(self, node, scope=Scope()):
        for declaration in node.dec_list:
            self.visit(declaration, scope)
        self.visit(node.global_expr, scope)
        return self.context,self.errors,self.warnings

    @visitor.when(type_declaration_node)
    def visit(self, node, scope):
        if node.id.startswith('<error>'):return

        scope=scope.create_child()
        self.current_type = self.context.get_type(node.id)


        if len(node.params)==0 and node.parent!=None:
            node.params=self.context.get_type(node.parent).attributes
            for param in node.params:
                try:
                    self.current_type.define_attribute(param, self.context.get_type(param))
                    scope.define_variable(param, self.context.get_type(param))
                except SemanticError as e:
                    self.current_type.define_attribute(param, self.object_type)
                    scope.define_variable(param, self.object_type)
        else:
            for param in node.params:
                add=True
                if param.id in [at.name for at in self.current_type.attributes]:add=False
                try:
                    if add:self.current_type.define_attribute(param, self.context.get_type(param))
                    scope.define_variable(param.id, self.context.get_type(param.id))
                except SemanticError as e:
                    if add:self.current_type.define_attribute(param.id, self.object_type)
                    try:
                        scope.define_variable(param.id, self.object_type)
                    except Exception as e: pass
        
        if self.current_type.parent:
            parent_type = self.current_type.parent
            if type(parent_type) == ErrorType():
                self.errors.append(error("SEMANTIC ERROR", f'Invalid parent type for "{node.id}"', line=node.line, verbose=False))
            
        for feature in node.features:
            self.visit(feature, scope)

        self.current_type = None


    @visitor.when(protocol_declaration_node)
    def visit(self, node, scope):
        if node.id.startswith('<error>'):return

        scope=scope.create_child()
        self.current_type = self.context.get_type(node.id)

        if self.current_type.parent:
            parent_type = self.current_type.parent
            if type(parent_type) == ErrorType():
                self.errors.append(error("SEMANTIC ERROR", f'Invalid parent type for protocol "{node.id}"', line=node.line, verbose=False))
            
        for fun in node.functions:
            try:
                # self.current_type.define_method(fun.id,[],[],self.context.get_type(fun.return_type))
                self.visit(fun, scope)
            except SemanticError as e:
                # self.errors.append(error("SEMANTIC ERROR", str(e), line=node.line, verbose=False))
                pass

        self.current_type = None

    @visitor.when(function_declaration_node)
    def visit(self, node, scope):
        if node.id.startswith('<error>'):
            return
        
        if self.current_type!=None:
            method = self.current_type.get_method(node.id)
        else:
            method = self.context.get_type("Function").get_method(node.id)
        

        scope = scope.create_child()

        if node.params and method.param_types:
            for param, param_type in zip(node.params, method.param_types):
                scope.define_variable(param.id, param_type)

        return_type = self.visit(node.body, scope)
        if node.body and  not return_type.conforms_to(method.return_type) and method.return_type!=self.object_type:
            self.errors.append(error("SEMANTIC ERROR", 'Incompatible return type', line=node.line, verbose=False))

    def prototipes(self,clas,prot):
        if not  all(method in prot.methods for method in clas.methods): return False
        if not  all(att in prot.attributes for att in clas.attributes): return False
        return True

    @visitor.when(variable_declaration_node)
    def visit(self, node, scope):
        
        if node.id.startswith('<error>'):return

        if node.id=="self":
            return self.object_type

        if node.type_id!=None:
            try:
                var_type = self.context.get_type(node.type_id)
            except SemanticError as e:
                var_type=ErrorType()
        else: 
            var_type=self.object_type
        expr_type = self.visit(node.value, scope)
        
        if not expr_type.conforms_to(var_type) and not self.prototipes(expr_type,var_type):
            self.errors.append(error("SEMANTIC ERROR", f'Incompatible variable type, variable "{node.id}" with type "{expr_type.name}"', line=node.line, verbose=False))
        var_type=expr_type
        scope.define_variable(node.id, var_type)

    @visitor.when(expression_block_node)
    def visit(self, node, scope):
        expr_type = ErrorType()
        for expr in node.expressions:
            expr_type = self.visit(expr, scope)
        return expr_type

    @visitor.when(function_call_node)
    def visit(self, node, scope):
        args_types = [self.visit(arg, scope) for arg in node.args]
        try:
            function = self.context.get_type('Function').get_method(node.id)
        except SemanticError as e:
            self.errors.append(error("SEMANTIC ERROR", str(e), line=node.line, verbose=False))
            for arg in node.args:
                self.visit(arg, scope)
            return ErrorType()

        if len(args_types) != len(function.param_types) :
            self.errors.append(error("SEMANTIC ERROR", f'Expected {len(function.param_types)} arguments but got {len(args_types)}', line=node.line, verbose=False))
            return ErrorType()

        for arg_type, param_type in zip(args_types, function.param_types):
            if not arg_type.conforms_to(param_type):
                self.errors.append(error("SEMANTIC ERROR", f'Incompatible argument type {arg_type.name} for parameter type {param_type.name}', line=node.line, verbose=False))
                return ErrorType()

        return function.return_type

    @visitor.when(attribute_call_node)
    def visit(self, node, scope):
        obj_type = self.visit(node.expr, scope)

        if obj_type == ErrorType():
            return ErrorType()

        try:
            attr = obj_type.get_attribute(node.id)
            return attr.type
        except SemanticError as e:
            self.errors.append(error("SEMANTIC ERROR", str(e), line=node.line, verbose=False))
            return ErrorType()

    @visitor.when(if_node)
    def visit(self, node, scope):
        types = []
        for condition, body in node.conditions_bodies:
            cond_type = self.visit(condition, scope)
            if cond_type != self.context.get_type('Boolean'):
                self.errors.append(error("SEMANTIC ERROR", 'Condition must be of type bool', line=condition.line, verbose=False))
            if self.visit(body, scope)!=ErrorType():
                types.append(self.visit(body, scope))
        if len(types)==0:return self.object_type
        return types[0] if len(types) == 1 else self.context.lowest_common_ancestor(types)

    @visitor.when(while_node)
    def visit(self, node, scope):
        cond_type = self.visit(node.condition, scope)
        if cond_type != self.context.get_type('Boolean'):
            self.errors.append(error("SEMANTIC ERROR", 'Condition must be of type bool', line=node.line, verbose=False))
        self.visit(node.body, scope)
        return VoidType()

    @visitor.when(for_node)
    def visit(self, node, scope):
        iterable_type = self.visit(node.expr, scope)
        iterable_protocol = self.context.get_type('Iterable')
        if not iterable_type.conforms_to(iterable_protocol):
            self.errors.append(error("SEMANTIC ERROR", 'Expression must conform to Iterable protocol', line=node.line, verbose=False))
        try: 
            vtype=self.context.get_type(node.variable.id)
        except Exception as e:
            vtype=self.object_type
            
        scope.define_variable(node.variable.id, vtype )
        self.visit(node.body, scope)
        return VoidType()

    @visitor.when(let_node)
    def visit(self, node, scope):
        scope = scope.create_child()
        for declaration in node.declarations:
            self.visit(declaration, scope)
        return self.visit(node.body, scope)

    @visitor.when(new_node)
    def visit(self, node, scope):
        try:
            ttype = self.context.get_type(node.type_id)
            args_types = [self.visit(arg, scope) for arg in node.args]
        except SemanticError as e:
            return ErrorType()

        if len(args_types) != len(ttype.attributes) and len(args_types)!=0:
            self.errors.append(error("SEMANTIC ERROR", f'Expected {len(ttype.attributes)} arguments but got {len(args_types)} calling "{node.type_id}"', line=node.line, verbose=False))
            return ErrorType()

        for arg_type, attr in zip(args_types, ttype.attributes):
            try:
                param_type=self.context.get_type(attr.name)
                if not arg_type.conforms_to(param_type):
                    self.errors.append(error("SEMANTIC ERROR", f'Incompatible argument type {arg_type.name} for parameter type {param_type.name} while calling "{node.type_id}"', line=node.line, verbose=False))
                    return ErrorType()
            except Exception as e:
                return ErrorType()    
        return ttype

    @visitor.when(variable_node)
    def visit(self, node, scope):
        if node.id=="self":
            return self.object_type
        var = scope.find_variable(node.id)
        if var is None:
            self.errors.append(error("SEMANTIC ERROR", f'Variable {node.id} not defined', line=node.line, verbose=False))
            return ErrorType()
        
        return var.type

    #region base_types
    @visitor.when(number_node)
    def visit(self, node, scope):
        return self.context.get_type('Number')

    @visitor.when(bool_node)
    def visit(self, node, scope):
        return self.context.get_type('Boolean')

    @visitor.when(string_node)
    def visit(self, node, scope):
        return self.context.get_type('String')

    

    #region aritm_ops
    @visitor.when(plus_node)
    def visit(self, node, scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        accepted=[self.context.get_type('Number'),self.context.get_type('Object')]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(error("SEMANTIC ERROR", f'lInvalid operation between {left_type.name} and {right_type.name}', line=node.line, verbose=False))
            return ErrorType()

        return self.context.get_type('Number')

    @visitor.when(minus_node)
    def visit(self, node, scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)

        accepted=[self.context.get_type('Number'),self.context.get_type('Object')]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(error("SEMANTIC ERROR", f'miInvalid operation between {left_type.name} and {right_type.name}', line=node.line, verbose=False))
            return ErrorType()

        return self.context.get_type('Number')

    @visitor.when(multiply_node)
    def visit(self, node, scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)

        accepted=[self.context.get_type('Number'),self.context.get_type('Object')]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(error("SEMANTIC ERROR", f'mInvalid operation between {left_type.name} and {right_type.name}', line=node.line, verbose=False))
            return ErrorType()

        return self.context.get_type('Number')

    @visitor.when(divide_node)
    def visit(self, node, scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        
        accepted=[self.context.get_type('Number'),self.context.get_type('Object')]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(error("SEMANTIC ERROR", f'DInvalid operation between {left_type.name} and {right_type.name}', line=node.line, verbose=False))
            return ErrorType()

        return self.context.get_type('Number')

    @visitor.when(modulo_node)
    def visit(self, node, scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)

        accepted=[self.context.get_type('Number'),self.context.get_type('Object')]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(error("SEMANTIC ERROR", f'Invalid operation between {left_type.name} and {right_type.name}', line=node.line, verbose=False))
            return ErrorType()

        return self.context.get_type('Number')

    @visitor.when(power_node)
    def visit(self, node, scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)

        accepted=[self.context.get_type('Number'),self.context.get_type('Object')]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(error("SEMANTIC ERROR", f'Invalid operation between {left_type.name} and {right_type.name}', line=node.line, verbose=False))
            return ErrorType()

        return self.context.get_type('Number')

    #region comparison
    @visitor.when(less_node)
    def visit(self, node, scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)

        accepted=[self.context.get_type('Number'),self.context.get_type('Object')]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(error("SEMANTIC ERROR", f'Invalid comparison between {left_type.name} and {right_type.name}', line=node.line, verbose=False))
            return ErrorType()

        return self.context.get_type('Boolean')
    
    @visitor.when(less_equal_node)
    def visit(self, node, scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)

        accepted=[self.context.get_type('Number'),self.context.get_type('Object')]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(error("SEMANTIC ERROR", f'Invalid comparison between {left_type.name} and {right_type.name}', line=node.line, verbose=False))
            return ErrorType()

        return self.context.get_type('Boolean')
    
    @visitor.when(greater_node)
    def visit(self, node, scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)

        accepted=[self.context.get_type('Number'),self.context.get_type('Object')]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(error("SEMANTIC ERROR", f'Invalid comparison between {left_type.name} and {right_type.name}', line=node.line, verbose=False))
            return ErrorType()

        return self.context.get_type('Boolean')

    @visitor.when(greater_equal_node)
    def visit(self, node, scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)

        accepted=[self.context.get_type('Number'),self.context.get_type('Object')]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(error("SEMANTIC ERROR", f'Invalid comparison between {left_type.name} and {right_type.name}', line=node.line, verbose=False))
            return ErrorType()

        return self.context.get_type('Boolean')

    @visitor.when(equals_node)
    def visit(self, node, scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)

        accepted=[self.context.get_type('Number'),self.context.get_type('Object')]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(error("SEMANTIC ERROR", f'Invalid comparison between {left_type.name} and {right_type.name}', line=node.line, verbose=False))
            return ErrorType()

        return self.context.get_type('Boolean')

    @visitor.when(not_equals_node)
    def visit(self, node, scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)

        accepted=[self.context.get_type('Number'),self.context.get_type('Object')]
        if left_type not in accepted or right_type not in accepted:
            self.errors.append(error("SEMANTIC ERROR", f'Invalid comparison between {left_type.name} and {right_type.name}', line=node.line, verbose=False))
            return ErrorType()

        return self.context.get_type('Boolean')



    @visitor.when(and_node)
    def visit(self, node, scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)

        if left_type != self.context.get_type('Boolean') or right_type != self.context.get_type('Boolean'):
            self.errors.append(error("SEMANTIC ERROR", f'Invalid logical operation between {left_type.name} and {right_type.name}', line=node.line, verbose=False))
            return ErrorType()

        return self.context.get_type('Boolean')

    @visitor.when(or_node)
    def visit(self, node, scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)

        if left_type != self.context.get_type('Boolean') or right_type != self.context.get_type('Boolean'):
            self.errors.append(error("SEMANTIC ERROR", f'Invalid logical operation between {left_type.name} and {right_type.name}', line=node.line, verbose=False))
            return ErrorType()

        return self.context.get_type('Boolean')


    @visitor.when(not_node)
    def visit(self, node, scope):
        expr_type = self.visit(node.expr, scope)

        if expr_type != self.context.get_type('Boolean'):
            self.errors.append(error("SEMANTIC ERROR", f'Invalid logical operation with {expr_type.name}', line=node.line, verbose=False))
            return ErrorType()

        return self.context.get_type('Boolean')

    @visitor.when(as_node)
    def visit(self, node, scope):
        expr_type = self.visit(node.expr, scope)
        cast_type = self.context.get_type(node.type_id)

        if not expr_type.conforms_to(cast_type) and not cast_type.conforms_to(expr_type):
            self.errors.append(error("SEMANTIC ERROR", f'Cannot cast {expr_type.name} to {cast_type.name}', line=node.line, verbose=False))
            return ErrorType()

        return cast_type

    @visitor.when(is_node)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        return self.context.get_type('Boolean')

    @visitor.when(index_node)
    def visit(self, node, scope):
        index_type = self.visit(node.index, scope)
        if index_type != self.context.get_type('Number'):
            self.errors.append(error("SEMANTIC ERROR", f'Index must be of type int, not {index_type.name}', line=node.line, verbose=False))
            return ErrorType()

        obj_type = self.visit(node.expr, scope)
        if not isinstance(obj_type, VectorType):
            self.errors.append(error("SEMANTIC ERROR", f'Cannot index into non-vector type {obj_type.name}', line=node.line, verbose=False))
            return ErrorType()

        return obj_type.get_element_type()

    @visitor.when(vector_node)
    def visit(self, node, scope):
        elements_types = [self.visit(element, scope) for element in node.elements]
        lca = self.context.lowest_common_ancestor(elements_types)
        if type(lca) == ErrorType():
            return ErrorType()
        vtype=VectorType(lca)
        return vtype

    @visitor.when(vector_comprehension_node)
    def visit(self, node, scope):
        iterable_type = self.visit(node.vector, scope)
        iterable_protocol = self.context.get_type('Iterable')
        if not iterable_type.conforms_to(iterable_protocol):
            self.errors.append(error("SEMANTIC ERROR", f'{iterable_type.name} does not conform to Iterable protocol', line=node.line, verbose=False))
            return ErrorType()

        scope = scope.create_child()
        scope.define_variable(node.variable, iterable_type)

        return_type = self.visit(node.expr, scope)
        if return_type == ErrorType():
            return ErrorType()

        return VectorType(return_type)

    @visitor.when(concatenation_node)
    def visit(self, node, scope):
        left_type = self.visit(node.left, scope)
        middle_type = self.visit(node.middle, scope)
        right_type = self.visit(node.right, scope)

        concatenable=[self.context.get_type('String'),self.context.get_type('Number')]
        if left_type not in  concatenable or right_type not in concatenable:
            
            self.errors.append(error("SEMANTIC ERROR", f'Invalid concatenation between types {left_type.name} and {right_type.name}', line=node.line, verbose=False))
            return ErrorType()

        return self.context.get_type('String')


    @visitor.when(property_call_node)
    def visit(self, node, scope):
        obj_type = self.visit(node.expr, scope)

        if obj_type == ErrorType():
            return ErrorType()

        try:
            method = obj_type.get_method(node.func)
            return method.return_type
        except SemanticError as e:
            self.errors.append(error("SEMANTIC ERROR", str(e), line=node.line, verbose=False))
            return ErrorType()

    @visitor.when(assignment_node)
    def visit(self, node, scope):
        var_info = scope.find_variable(node.var.id)
        if var_info is None:
            self.errors.append(error("SEMANTIC ERROR", f'Variable "{node.var.id}" not defined', line=node.line, verbose=False))
            return ErrorType()

        expr_type = self.visit(node.expr, scope)
        if not expr_type.conforms_to(var_info.type):
            self.errors.append(error("SEMANTIC ERROR", f'Cannot assign "{expr_type.name}" to "{var_info.type.name}"', line=node.line, verbose=False))
            return ErrorType()

        return var_info.type

    @visitor.when(attribute_call_node)
    def visit(self, node, scope):
        obj_type = self.visit(node.expr, scope)

        if obj_type == ErrorType():
            return ErrorType()

        try:
            attr = obj_type.get_attribute(node.id)
            return attr.type
        except SemanticError as e:
            self.errors.append(error("SEMANTIC ERROR", str(e), line=node.line, verbose=False))
            return ErrorType()