import src.cmp.visitor as visitor
from src.cmp.semantic import  SemanticError, ErrorType
from src.grammar.hulk_ast import *
from src.utils.errors import *


class type_filler:
    def __init__(self, context, errors):
        if errors is None:
            errors = []
        self.context = context
        self.current_type = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(program_node)
    def visit(self, node: program_node):
        for declaration in node.dec_list:
            self.visit(declaration)
        self.visit(node.global_expr)
        return self.context, self.errors

    @visitor.when(function_declaration_node)
    def visit(self, node: function_declaration_node):
        params_names, params_types = self.get_params_names_and_types(node)
        if node.return_type is None:
            return_type = self.context.get_type('Object')
        else:
            try:
                return_type = self.context.get_type(node.return_type)
            except SemanticError as e:
                self.errors.append(error("SEMANTIC ERROR",str(e),line=node.line,verbose=False))
                return_type = ErrorType()

        
        if self.current_type==None:
            try:
                function_type = self.context.get_type('Function')
                function_type.define_method(node.id, params_names, params_types, return_type)
            except SemanticError as e:
                self.errors.append(error("SEMANTIC ERROR",str(e),line=node.line,verbose=False))
        else:
            try:
                self.current_type.define_method(node.id, params_names, params_types, return_type)
            except SemanticError as e:
                self.errors.append(error("SEMANTIC ERROR",str(e),line=node.line,verbose=False))

    def get_params_names_and_types(self, node):
        if not hasattr(node, 'params') or node.params is None:
            return [], []

        params_names = []
        params_types = []

        for param in node.params:
            param_name = param.id
            param_type_name = param.type_id
            if param_name in params_names:
                self.errors.append(error("SEMANTIC ERROR",f'Parameter "{param_name}" previously declared on function "{node.id}"',line=node.line,verbose=False))
                index = params_names.index(param_name)
                params_types[index] = ErrorType()
            else:
                try:
                    param_type = self.context.get_type(param_type_name)
                except SemanticError as e:
                    if param_type_name!=None:
                        self.errors.append(error("SEMANTIC ERROR",str(e),line=node.line,verbose=False))
                    param_type = self.context.get_type('Object')
                params_types.append(param_type)
                params_names.append(param_name)

        return params_names, params_types

    @visitor.when(type_declaration_node)
    def visit(self, node: type_declaration_node):
        if node.id.startswith('<error>'):
            return
        
        try:
            self.current_type = self.context.get_type(node.id)
        except SemanticError as e:
            self.errors.append(error("SEMANTIC ERROR",str(e),line=node.line,verbose=False))
            self.current_type = ErrorType()
            return
        
        if node.parent in ['Number', 'Boolean', 'String']:
            self.errors.append(error("SEMANTIC ERROR",f'Type "{node.id}" is inheriting from a forbidden type',line=node.line,verbose=False))
        elif node.parent is not None:
            try:
                parent = self.context.get_type(node.parent)
                current = parent
                while current is not None:
                    if current.name == self.current_type.name:
                        self.errors.append(error("SEMANTIC ERROR",'Circular inheritance',line=node.line,verbose=False))
                        parent = ErrorType()
                        break
                    current = current.parent
            except SemanticError as e:
                self.errors.append(error("SEMANTIC ERROR",str(e),line=node.line,verbose=False))
                parent = ErrorType()
            try:
                self.current_type.set_parent(parent)
            except SemanticError as e:
                self.errors.append(error("SEMANTIC ERROR",str(e),line=node.line,verbose=False))
        else:
            object_type = self.context.get_type('Object')
            self.current_type.set_parent(object_type)

        for feature in node.features:
            self.visit(feature)
        self.current_type=None

    @visitor.when(protocol_declaration_node)
    def visit(self, node: protocol_declaration_node):
        if node.id.startswith('<error>'):
            return
        

        try:
            self.current_type = self.context.get_type(node.id)
        except SemanticError as e:
            self.errors.append(error("SEMANTIC ERROR",str(e),line=node.line,verbose=False))
            self.current_type = ErrorType()
            return

        if node.parent is not None:
            try:
                parent = self.context.get_type(node.parent)
                current = parent
                while current is not None:
                    if current.name == self.current_type.name:
                        self.errors.append(error("SEMANTIC ERROR",'Circular inheritance',line=node.line,verbose=False))
                        parent = ErrorType()
                        break
                    current = current.parent
            except SemanticError as e:
                self.errors.append(error("SEMANTIC ERROR",str(e),line=node.line,verbose=False))
                parent = ErrorType()

            try:
                self.current_type.set_parent(parent)
                for method in parent.all_methods():
                    self.current_type.define_method(method[0].name,method[0].param_names,method[0].param_types,
                                                    method[0].return_type)
            except SemanticError as e:
                self.errors.append(error("SEMANTIC ERROR",str(e),line=node.line,verbose=False))


        for method in node.functions:
            try:
                self.visit(method)
            except SemanticError as e:
                self.errors.append(error("SEMANTIC ERROR", str(e), line=node.line, verbose=False))
        self.current_type=None
            
    @visitor.when(variable_declaration_node)
    def visit(self, node: variable_declaration_node):
        if node.id.startswith('<error>'):
            return
        
        try:
            var_type = self.context.get_type(node.type_id)
        except SemanticError as e:
            if node.type_id!=None:
                self.errors.append(error("SEMANTIC ERROR",str(e),line=node.line,verbose=False))
            var_type = self.context.get_type('Object')

        try:
            self.current_type.define_attribute(node.id, var_type)
        except SemanticError as e:
            if var_type!=ErrorType():
                self.errors.append(error("SEMANTIC ERROR",str(e),line=node.line,verbose=False))