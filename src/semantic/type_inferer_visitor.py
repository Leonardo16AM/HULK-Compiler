from typing import List
import itertools as itt
from collections import OrderedDict
import src.cmp.visitor as visitor
from src.utils.errors import error
from src.cmp.semantic import Context, Scope, Type, ErrorType, VoidType, IntType, SemanticError,VectorType, AutoType
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
        self.current_function = None
        self.errors = errors
        self.warnings = warnings
        self.it=0
        self.max_iters=5

    @visitor.on('node')
    def visit(self, node):
        pass

    #region program
    @visitor.when(program_node)
    def visit(self, node):
        scope=node.scope
        for declaration in node.dec_list:
            self.visit(declaration)
        self.visit(node.global_expr)
        
        if self.it<self.max_iters:
            self.it+=1
            self.visit(node)

        return self.context,self.errors,self.warnings
    


    #region type_declaration
    @visitor.when(type_declaration_node)
    def visit(self, node):        
        scope=node.scope
        if node.id.startswith('<error>'):return

        self.current_type = self.context.get_type(node.id)
        
        if self.it==0:
            if len(node.params)==0 and node.parent!=None:
                try:
                    params=self.context.get_type(node.parent).attributes
                except SemanticError as e:
                    self.errors.append(error("SEMANTIC ERROR", str(e),
                                          line=node.line, verbose=False))
                    return 
                for param in params:
                    node.params.append(variable_declaration_node(param.name,param.type.name if param.type!=AutoType() else None,None))
                    node.args.append(variable_node(param.name))
                    try:
                        self.current_type.define_attribute('IN'+param.name+'ESP', node.scope.find_variable(param).type)
                    except SemanticError as e:
                        self.current_type.define_attribute('IN'+param.name+'ESP', AutoType())
            else:
                for param in node.params:
                    add=True
                    if param.id in [at.name for at in self.current_type.attributes]:add=False
                    try:
                        self.current_type.define_attribute('IN'+param.id+'ESP',node.scope.find_variable(param.id).type)
                    except SemanticError as e:
                        if add:self.current_type.define_attribute('IN'+param.id+'ESP', AutoType())
                    

        if self.current_type.parent:
            if type(self.current_type.parent) == ErrorType():
                self.errors.append(error("SEMANTIC ERROR", f'Invalid parent type for "{node.id}"',
                                          line=node.line, verbose=False))
            
        for feature in node.features:
            self.visit(feature)
        self.current_type = None

    #region protocol_declaration
    @visitor.when(protocol_declaration_node)
    def visit(self, node):
        scope=node.scope
        if node.id.startswith('<error>'):return

        self.current_type = self.context.get_type(node.id)

        if self.current_type.parent:
            parent_type = self.current_type.parent
            if type(parent_type) == ErrorType():
                self.errors.append(error("SEMANTIC ERROR", f'Invalid parent type for protocol "{node.id}"',
                                          line=node.line, verbose=False))
            
        for fun in node.functions:
            self.visit(fun)
        self.current_type = None

    # region function_declaration
    @visitor.when(function_declaration_node)
    def visit(self, node):
        scope=node.scope
        self.current_function=node.id
        if node.id.startswith('<error>'):
            return node.return_type
        if self.current_type!=None:
            method = self.current_type.get_method(node.id)
        else:
            method = self.context.get_type("Function").get_method(node.id)

        body_type=self.visit(node.body)
        if node.return_type!=None and node.return_type!=AutoType().name:
            node.scope.return_type=self.context.get_type(node.return_type)
        else:
            node.scope.return_type=body_type
            method.return_type=body_type
        
        self.current_function=None
            
            
    def prototipes(self,clas,prot):
        if not  all(method.name in [me.name for me in clas.methods] for method in prot.methods): return False
        return True
    
    #region variable_declaration
    @visitor.when(variable_declaration_node)
    def visit(self, node):
        scope=node.scope
        if node.id.startswith('<error>'):return

        if node.id=="self":
            return self.current_type

        if node.type_id!=None:
            try:
                var_type = self.context.get_type(node.type_id)
            except SemanticError as e:
                var_type=ErrorType()
        else: 
            var_type=AutoType()
        expr_type = self.visit(node.value)
        if var_type.name==AutoType().name:
            var_type=expr_type
            scope.modify_variable(node.id,expr_type)

    #region expression_block
    @visitor.when(expression_block_node)
    def visit(self, node):
        expr_type = ErrorType()
        for expr in node.expressions:
            expr_type = self.visit(expr)
        return expr_type



    #region function_call
    @visitor.when(function_call_node)
    def visit(self, node):
        args_types = [self.visit(arg) for arg in node.args]
        
        fun_name=node.id
        curr='Function'
        # if self.current_type!=None:
        #     curr=self.current_type.name
        if  node.id=="base":
            curr=self.current_type.parent.name
            fun_name=self.current_function

        try:
            function = self.context.get_type(curr).get_method(fun_name)
        except SemanticError as e:
            self.errors.append(error("SEMANTIC ERROR", str(e), line=node.line, verbose=False))
            for arg in node.args:
                self.visit(arg)
            return ErrorType()

        if len(args_types) != len(function.param_types) :
            self.errors.append(error("SEMANTIC ERROR", f'Function: Expected {len(function.param_types)} arguments but got {len(args_types)}',
                                      line=node.line, verbose=False))
            return ErrorType()
        
        return function.return_type

    #region attribute_call
    @visitor.when(attribute_call_node)
    def visit(self, node):
        obj_type = self.visit(node.expr)

        if obj_type == ErrorType():
            return ErrorType()

        try:
            attr = obj_type.get_attribute(node.id)
            return attr.type
        except SemanticError as e:
            self.errors.append(error("SEMANTIC ERROR", str(e), line=node.line, verbose=False))
            return ErrorType()

    #region if
    @visitor.when(if_node)
    def visit(self, node):
        types = []
        for condition, body in node.conditions_bodies:
            cond_type = self.visit(condition)
            if self.visit(body)!=ErrorType():
                types.append(self.visit(body))
        if len(types)==0:return AutoType()
        return types[0] if len(types) == 1 else self.context.lowest_common_ancestor(types)

    #region while
    @visitor.when(while_node)
    def visit(self, node):
        cond_type = self.visit(node.condition)
        return self.visit(node.body)

    #region for
    @visitor.when(for_node)
    def visit(self, node):
        scope=node.scope
        iterable_type = self.visit(node.expr)
        iterable_protocol = self.context.get_type('Iterable')
        try: 
            vtype=self.context.get_type(node.variable.id)
        except Exception as e:
            vtype=AutoType()
            
        return self.visit(node.body)

    #region let
    @visitor.when(let_node)
    def visit(self, node):
        scope=node.scope
        for declaration in node.declarations:
            self.visit(declaration)
        return self.visit(node.body)

    #region new
    @visitor.when(new_node)
    def visit(self, node):
        try:
            ttype = self.context.get_type(node.type_id)
            args_types = [self.visit(arg) for arg in node.args]
        except SemanticError as e:
            return ErrorType()
            
        alats=ttype.attributes
        ttype_attr=[attr for attr in alats if (attr.name.startswith('IN') and attr.name.endswith('ESP'))]
        if len(args_types) != len(ttype_attr) and len(args_types)!=0:
            self.errors.append(error("SEMANTIC ERROR", f'New: Expected {len(ttype_attr)} arguments but got {len(args_types)} calling "{node.type_id}"', line=node.line, verbose=False))
            return ErrorType()
            
        return ttype

    #region variable
    @visitor.when(variable_node)
    def visit(self, node):
        scope=node.scope
        if node.id=="self":
            return self.current_type
        try:
            var = scope.find_variable(node.id)
        except SemanticError as e:
            self.errors.append(error("SEMANTIC ERROR", str(e), 
                                     line=node.line, verbose=False))
            return ErrorType()
        
        return var.type

    #region base_types
    @visitor.when(number_node)
    def visit(self, node):
        return self.context.get_type('Number')

    @visitor.when(bool_node)
    def visit(self, node):
        return self.context.get_type('Boolean')

    @visitor.when(string_node)
    def visit(self, node):
        return self.context.get_type('String')

    

    #region aritm_ops
    @visitor.when(plus_node)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        return self.context.get_type('Number')

    @visitor.when(minus_node)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        return self.context.get_type('Number')

    @visitor.when(multiply_node)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        return self.context.get_type('Number')

    @visitor.when(divide_node)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        return self.context.get_type('Number')

    @visitor.when(modulo_node)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        return self.context.get_type('Number')

    @visitor.when(power_node)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        return self.context.get_type('Number')

    #region comparison
    @visitor.when(less_node)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        return self.context.get_type('Boolean')
    
    @visitor.when(less_equal_node)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        return self.context.get_type('Boolean')
    
    @visitor.when(greater_node)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        return self.context.get_type('Boolean')

    @visitor.when(greater_equal_node)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        return self.context.get_type('Boolean')

    @visitor.when(equals_node)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        return self.context.get_type('Boolean')

    @visitor.when(not_equals_node)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        return self.context.get_type('Boolean')


    #region boolean_ops
    @visitor.when(and_node)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        return self.context.get_type('Boolean')

    @visitor.when(or_node)
    def visit(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        return self.context.get_type('Boolean')


    @visitor.when(not_node)
    def visit(self, node):
        expr_type = self.visit(node.expr)
        return self.context.get_type('Boolean')

    #region as
    @visitor.when(as_node)
    def visit(self, node):
        expr_type = self.visit(node.expr)
        cast_type = self.context.get_type(node.type_id)
        return cast_type

    #region is
    @visitor.when(is_node)
    def visit(self, node):
        self.visit(node.expr)
        return self.context.get_type('Boolean')
    

    #region index
    @visitor.when(index_node)
    def visit(self, node):
        index_type = self.visit(node.index)
        obj_type = self.visit(node.expr)
        if not isinstance(obj_type, VectorType):
            return ErrorType()

        return obj_type.get_element_type()

    #region vector
    @visitor.when(vector_node)
    def visit(self, node):
        elements_types = [self.visit(element) for element in node.elements]
        lca = self.context.lowest_common_ancestor(elements_types)
        if type(lca) == ErrorType():
            return ErrorType()
        vtype=VectorType(lca)
        vtype.set_parent(self.context.get_type('Iterable'))
        return vtype

    #region vector_comprehension
    @visitor.when(vector_comprehension_node)
    def visit(self, node):
        iterable_type = self.visit(node.vector)
        iterable_protocol = self.context.get_type('Iterable')
        if not iterable_type.conforms_to(iterable_protocol):
            self.errors.append(error("SEMANTIC ERROR", f'"{iterable_type.name}" does not conform to Iterable protocol',
                                      line=node.line, verbose=False))
            return ErrorType()

        scope=node.scope

        return_type = self.visit(node.expr)
        if return_type == ErrorType():
            return ErrorType()

        return VectorType(return_type)

    #region concatenation_node
    @visitor.when(concatenation_node)
    def visit(self, node):
        left_type = self.visit(node.left)
        middle_type = self.visit(node.middle)
        right_type = self.visit(node.right)
        return self.context.get_type('String')

    #region property_call
    @visitor.when(property_call_node)
    def visit(self, node):
        obj_type = self.visit(node.expr)

        if obj_type == ErrorType():
            return ErrorType()

        try:
            method = obj_type.get_method(node.func.id)
            return method.return_type
        except SemanticError as e:
            if obj_type!=AutoType():
                self.errors.append(error("SEMANTIC ERROR", str(e), line=node.line, verbose=False))
            return AutoType()

    #region assignment_node
    @visitor.when(assignment_node)
    def visit(self, node):
        scope=node.scope
        
        if node.var.id=="self":
            self.errors.append(error("SEMANTIC ERROR", f'You cannot modify self inside the class',
                                      line=node.line, verbose=False))
            return self.current_type
        
        var_info = scope.find_variable(node.var.id)
        
        if var_info is None:
            self.errors.append(error("SEMANTIC ERROR", f'Variable "{node.var.id}" not defined on scope',
                                      line=node.line, verbose=False))
            return ErrorType()
        
        expr_type = self.visit(node.expr)
        if var_info.type.name!=AutoType().name:
            return var_info.type
        

        node.scope.modify_variable(var_info.name,expr_type)
        return expr_type

    #region attribute_call
    @visitor.when(attribute_call_node)
    def visit(self, node):
        obj_type = self.visit(node.expr)

        try:
            attr = obj_type.get_attribute(node.id)
            return attr.type
        except SemanticError as e:
            self.errors.append(error("SEMANTIC ERROR", str(e), line=node.line, verbose=False))
            return ErrorType()