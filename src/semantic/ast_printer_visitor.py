import src.cmp.visitor as visitor
from src.cmp.ast import *
from abc import ABC, abstractmethod
from src.grammar.hulk_ast import *

class FormatVisitor:
    @visitor.on('node')
    def visit(self, node, tabs=0):
        pass
    
    @visitor.when(program_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ProgramNode'
        dec_list = '\n'.join(self.visit(dec, tabs + 1) for dec in node.dec_list)
        global_expr = self.visit(node.global_expr, tabs + 1)
        return f'{ans}\n{dec_list}\n{global_expr}'

    @visitor.when(function_declaration_node)
    def visit(self, node, tabs=0):

        ans = '\t' * tabs + f'\\__FunctionDeclarationNode: def {node.id}(<params>) -> {node.return_type}'
        params = '\t' * (tabs+1) + 'params:\n' + '\n'.join(self.visit(param, tabs+1) for param in node.params)
        body = '\t' * (tabs+1) + f'This function has no body'
        if node.body:
            body = '\t' * (tabs+1) + 'Body:\n'+self.visit(node.body, tabs + 1)
        return f'{ans}\n{params}\n{body}'

    @visitor.when(type_declaration_node)
    def visit(self, node, tabs=0):
        parent = f" : {node.parent}" if node.parent else "None"
        ans = '\t' * tabs + f'\\__TypeDeclarationNode: class {node.id}(<params>) inherits {parent}(<args>)'
        params = '\t' * (tabs+1) + 'params:\n'+'\n'.join(self.visit(param, tabs + 1) for param in node.params)
        args = '\t' * (tabs+1) + 'args:\n'+'\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        features = '\t' * (tabs+1) + 'features:\n'+'\n'.join(self.visit(feature, tabs + 1) for feature in node.features)
        return f'{ans}\n{params}\n{args}\n{features}'

    @visitor.when(protocol_declaration_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ProtocolDeclarationNode: protocol {node.id} extends {node.parent}'
        functions = '\n'.join(self.visit(func, tabs + 1) for func in node.functions)
        return f'{ans}\n{functions}'

    @visitor.when(variable_declaration_node)
    def visit(self, node, tabs=0):
        value = '\t' * (tabs+1) + f'None'
        if node.value:
            value = self.visit(node.value, tabs + 1)
        ans = '\t' * tabs + f'\\__VariableDeclarationNode: {node.id}: {node.type_id} ='
        return f'{ans}\n{value}'

    @visitor.when(expression_block_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ExpressionBlockNode'
        expressions = '\n'.join(self.visit(expr, tabs + 1) for expr in node.expressions)
        return f'{ans}\n{expressions}'

    @visitor.when(concatenation_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ConcatenationNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(and_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AndNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(or_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__OrNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(not_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__NotNode'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(is_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__IsNode: is {node.type_id}'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(less_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__LessNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(less_equal_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__LessEqualNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(greater_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__GreaterNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(greater_equal_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__GreaterEqualNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(equals_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__EqualsNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(not_equals_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__NotEqualsNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(plus_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__PlusNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(minus_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__MinusNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(negative_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__NegativeNode'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    

    @visitor.when(multiply_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__MultiplyNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(divide_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__DivideNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(modulo_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ModuloNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(power_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__PowerNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(variable_node)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__VariableNode: {node.id}'

    @visitor.when(function_call_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__FunctionCallNode: {node.id}(<args>)'
        args = '\t' * (tabs+1) + 'args:\n'+'\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{ans}\n{args}'

    @visitor.when(number_node)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__NumberNode: {node.value}'

    @visitor.when(bool_node)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__BoolNode: {node.value}'

    @visitor.when(string_node)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__StringNode: {node.value}'

    @visitor.when(index_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__IndexNode:'
        expr = self.visit(node.expr, tabs + 1)
        index = self.visit(node.index, tabs + 1)
        return f'{ans}\n{expr}\n{index}'

    @visitor.when(as_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AsNode: as {node.type_id}'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(property_call_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__PropertyCallNode: \n{self.visit(node.expr, tabs + 1)}'
        func =  self.visit(node.func, tabs + 1)
        return f'{ans}\n{func}'
    
    @visitor.when(attribute_call_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AttributeCallNode: {node.id}\n{self.visit(node.expr, tabs + 1)}'
        return f'{ans}'

    @visitor.when(if_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__IfNode'
        conditions_bodies = '\n'.join(str(self.visit(cond_body[0], tabs + 1)) + '\n' + str(self.visit(cond_body[1], tabs + 1)) for cond_body in node.conditions_bodies)
        return f'{ans}\n{conditions_bodies}'

    @visitor.when(vector_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__VectorNode'
        elements = '\n'.join(self.visit(element, tabs + 1) for element in node.elements)
        return f'{ans}\n{elements}'

    @visitor.when(new_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__NewNode: new {node.type_id}'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{ans}\n{args}'

    @visitor.when(assignment_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AssignmentNode: \n{self.visit(node.var, tabs+1)}'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(let_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__LetNode'
        declarations = '\n'.join(self.visit(declaration, tabs + 1) for declaration in node.declarations)
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{declarations}\n{body}'

    @visitor.when(while_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__WhileNode'
        condition = self.visit(node.condition, tabs + 1)
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{condition}\n{body}'

    @visitor.when(for_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ForNode:'
        vars = self.visit(node.variable, tabs + 1)
        expr = self.visit(node.expr, tabs + 1)
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{vars}\n{expr}\n{body}'

    @visitor.when(vector_comprehension_node)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__VectorComprehensionNode'
        variable = self.visit(node.variable, tabs + 1)
        expr = self.visit(node.expr, tabs + 1)
        vector = self.visit(node.vector, tabs + 1)
        return f'{ans}\n{variable}\n{expr}\n{vector}'