import src.cmp.visitor as visitor
from src.cmp.semantic import SemanticError, Context, Scope, VariableInfo
from src.grammar.hulk_ast import *
from src.utils.errors import *

class var_finder:
    def __init__(self, context, errors=None):
        if errors is None:
            errors = []
        self.context = context
        self.current_type = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(program_node)
    def visit(self, node: program_node, scope: Scope = None):
        scope = Scope()
        node.scope = scope

        for declaration in node.dec_list:
            self.visit(declaration, scope.create_child())

        self.visit(node.global_expr, scope.create_child())
        return scope

    @visitor.when(function_declaration_node)
    def visit(self, node: function_declaration_node, scope: Scope):
        node.scope = scope
        function_scope = scope.create_child()
        
        for param in node.params:
            try:
                function_scope.define_variable(param.id, self.context.get_type(param.type_id))
            except SemanticError as e:
                self.errors.append(error("SEMANTIC ERROR",str(e)+f' On function {node.id}', line=node.line, verbose=False))
        self.visit(node.body, function_scope)

    @visitor.when(type_declaration_node)
    def visit(self, node: type_declaration_node, scope: Scope):
        node.scope = scope
        type_scope = scope.create_child()

        for feature in node.features:
            self.visit(feature, type_scope)

    @visitor.when(protocol_declaration_node)
    def visit(self, node: protocol_declaration_node, scope: Scope):
        node.scope = scope
        protocol_scope = scope.create_child()

        for func in node.functions:
            self.visit(func, protocol_scope)

    @visitor.when(variable_declaration_node)
    def visit(self, node: variable_declaration_node, scope: Scope):
        node.scope = scope
        try:
            var_type = self.context.get_type(node.type_id)
        except SemanticError as e:
            self.errors.append(error("SEMANTIC ERROR", str(e)+f' On varible {node.id}', line=node.line, verbose=False))
            var_type = None

        scope.define_variable(node.id, var_type)
        self.visit(node.value, scope.create_child())

    @visitor.when(expression_block_node)
    def visit(self, node: expression_block_node, scope: Scope):
        block_scope = scope.create_child()
        node.scope = block_scope

        for expr in node.expressions:
            self.visit(expr, block_scope.create_child())

    @visitor.when(let_node)
    def visit(self, node: let_node, scope: Scope):
        let_scope = scope.create_child()
        node.scope = let_scope

        for declaration in node.declarations:
            self.visit(declaration, let_scope)

        self.visit(node.body, let_scope)

    @visitor.when(for_node)
    def visit(self, node: for_node, scope: Scope):
        for_scope = scope.create_child()
        node.scope = for_scope

        for_scope.define_variable(node.variable, None)
        self.visit(node.expr, for_scope)
        self.visit(node.body, for_scope.create_child())

    @visitor.when(while_node)
    def visit(self, node: while_node, scope: Scope):
        while_scope = scope.create_child()
        node.scope = while_scope

        self.visit(node.condition, while_scope.create_child())
        self.visit(node.body, while_scope.create_child())

    @visitor.when(if_node)
    def visit(self, node: if_node, scope: Scope):
        node.scope = scope
        for condition, body in node.conditions_bodies:
            if_scope = scope.create_child()
            self.visit(condition, if_scope)
            self.visit(body, if_scope)

    @visitor.when(assignment_node)
    def visit(self, node: assignment_node, scope: Scope):
        node.scope = scope
        self.visit(node.var, scope.create_child())
        self.visit(node.expr, scope.create_child())

    @visitor.when(variable_node)
    def visit(self, node: variable_node, scope: Scope):
        node.scope = scope

    @visitor.when(function_call_node)
    def visit(self, node: function_call_node, scope: Scope):
        node.scope = scope
        for arg in node.args:
            self.visit(arg, scope.create_child())


    @visitor.when(concatenation_node)
    def visit(self, node: concatenation_node, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.middle, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(and_node)
    def visit(self, node: and_node, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(or_node)
    def visit(self, node: or_node, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(not_node)
    def visit(self, node: not_node, scope: Scope):
        node.scope = scope
        self.visit(node.expr, scope.create_child())

    @visitor.when(is_node)
    def visit(self, node: is_node, scope: Scope):
        node.scope = scope
        self.visit(node.expr, scope.create_child())

    @visitor.when(less_node)
    def visit(self, node: less_node, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(less_equal_node)
    def visit(self, node: less_equal_node, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(greater_node)
    def visit(self, node: greater_node, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(greater_equal_node)
    def visit(self, node: greater_equal_node, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(equals_node)
    def visit(self, node: equals_node, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(not_equals_node)
    def visit(self, node: not_equals_node, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(plus_node)
    def visit(self, node: plus_node, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(minus_node)
    def visit(self, node: minus_node, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(multiply_node)
    def visit(self, node: multiply_node, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(divide_node)
    def visit(self, node: divide_node, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(modulo_node)
    def visit(self, node: modulo_node, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(negative_node)
    def visit(self, node: negative_node, scope: Scope):
        node.scope = scope
        self.visit(node.expr, scope.create_child())

    @visitor.when(power_node)
    def visit(self, node: power_node, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())

    @visitor.when(number_node)
    def visit(self, node: number_node, scope: Scope):
        node.scope = scope

    @visitor.when(bool_node)
    def visit(self, node: bool_node, scope: Scope):
        node.scope = scope

    @visitor.when(string_node)
    def visit(self, node: string_node, scope: Scope):
        node.scope = scope

    @visitor.when(index_node)
    def visit(self, node: index_node, scope: Scope):
        node.scope = scope
        self.visit(node.expr, scope.create_child())
        self.visit(node.index, scope.create_child())

    @visitor.when(as_node)
    def visit(self, node: as_node, scope: Scope):
        node.scope = scope
        self.visit(node.expr, scope.create_child())

    @visitor.when(property_call_node)
    def visit(self, node: property_call_node, scope: Scope):
        node.scope = scope
        self.visit(node.expr, scope.create_child())
        self.visit(node.func, scope.create_child())

    @visitor.when(attribute_call_node)
    def visit(self, node: attribute_call_node, scope: Scope):
        node.scope = scope
        self.visit(node.expr, scope.create_child())

    @visitor.when(vector_node)
    def visit(self, node: vector_node, scope: Scope):
        node.scope = scope
        for element in node.elements:
            self.visit(element, scope.create_child())

    @visitor.when(new_node)
    def visit(self, node: new_node, scope: Scope):
        node.scope = scope
        for arg in node.args:
            self.visit(arg, scope.create_child())

    @visitor.when(vector_comprehension_node)
    def visit(self, node: vector_comprehension_node, scope: Scope):
        node.scope = scope
        comprehension_scope = scope.create_child()
        comprehension_scope.define_variable(node.variable, None)
        self.visit(node.expr, comprehension_scope)
        self.visit(node.vector, scope.create_child())