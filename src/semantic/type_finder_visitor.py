import src.cmp.visitor as visitor
from src.cmp.semantic import Context, SemanticError
from src.grammar.hulk_ast import *
from src.utils.errors import *


class type_finder:
    def __init__(self, errors) -> None:
        self.context = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(program_node)
    def visit(self, node: program_node):
        self.context = Context()

        

        self.context.create_type('<void>')
        self.context.create_type('None')
        object_type = self.context.create_type('Object')
        number_type = self.context.create_type('Number')
        number_type.set_parent(object_type)

        bool_type = self.context.create_type('Boolean')
        bool_type.set_parent(object_type)


        
        string_type = self.context.create_type('String')
        string_type.set_parent(object_type)
        string_type.define_method('size', [], [], number_type)
        string_type.define_method('next', [], [], bool_type)
        string_type.define_method('current', [], [], string_type)
        
        object_type.define_method('equals', ['other'], [object_type], bool_type)
        object_type.define_method('toString', [], [], string_type)

        self.context.create_type('Function')
        print_function = self.context.get_type('Function')
        print_function.define_method('print', ['value'], [object_type], string_type)

        sqrt_function = self.context.get_type('Function')
        sqrt_function.define_method('sqrt', ['value'], [number_type], number_type)
        
        sin_function = self.context.get_type('Function')
        sin_function.define_method('sin', ['angle'], [number_type], number_type)

        cos_function = self.context.get_type('Function')
        cos_function.define_method('cos', ['angle'], [number_type], number_type)

        exp_function = self.context.get_type('Function')
        exp_function.define_method('exp', ['value'], [number_type], number_type)
        
        log_function = self.context.get_type('Function')
        log_function.define_method('log', ['value'], [number_type], number_type)
        
        rand_function = self.context.get_type('Function')
        rand_function.define_method('rand', [], [], number_type)

        base_function = self.context.get_type('Function')
        base_function.define_method('base', [], [], object_type)


        parse_function = self.context.get_type('Function')
        parse_function.define_method('parse', ['value'], [string_type], number_type)

        iterable_protocol = self.context.create_type('Iterable')
        iterable_protocol.define_method('next', [], [], bool_type)
        iterable_protocol.define_method('current', [], [], object_type)

        range_type = self.context.create_type('Range')
        range_type.set_parent(iterable_protocol)
        range_type.params_names, range_type.params_types = ['min', 'max'], [number_type, number_type]
        range_type.define_attribute('min', number_type)
        range_type.define_attribute('max', number_type)
        range_type.define_attribute('current', number_type)
        range_type.define_method('next', [], [], bool_type)
        range_type.define_method('current', [], [], number_type)

        range_function = self.context.get_type('Function')
        range_function.define_method('range', ['min', 'max'], [number_type, number_type], range_type)

        for decl in node.dec_list:
            self.visit(decl)
        self.visit(node.global_expr)
        return self.context, self.errors

    @visitor.when(type_declaration_node)
    def visit(self, node: type_declaration_node):
        try:
            self.context.create_type(node.id)
        except SemanticError as e:
            self.errors.append(error("SEMANTIC ERROR",str(e),line=node.line,verbose=False))
            self.context.create_type(f'<error> {node.id}')
            node.id=f'<error> {node.id}'

    @visitor.when(protocol_declaration_node)
    def visit(self, node: protocol_declaration_node):
        try:
            self.context.create_type(node.id)
        except SemanticError as e:
            self.errors.append(error("SEMANTIC ERROR",str(e),line=node.line,verbose=False))
            self.context.create_type(f'<error> {node.id}')
            node.id=f'<error> {node.id}'