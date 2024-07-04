from src.cmp import visitor as visitor
from src.cmp.ast import *
from src.codegen.c_ast import *
from abc import ABC, abstractmethod

class code_generator:
    def get_tools(self):
        f = open("src/codegen/ctools.c", "r")
        c = f.read()
        f.close()

        return c.split("//Finish C_TOOLS")[0]
         

    @visitor.on('node')
    def visit(self,node):
        pass

    @visitor.when(c_program_node)
    def visit(self,node):
        ans=self.get_tools()+"\n"
        for inc in node.include_list:
            ans+=self.visit(inc)

        for dec in node.dec_list:
            ans+=self.visit(dec)
        return ans
    
    @visitor.when(c_include_statement_node)
    def visit(self, node):
        return f"#include<{node.lib_name}>\n"
    
    @visitor.when(c_statement_node)
    def visit(self,node):
        return f"{self.visit(node.expr)};\n"

    @visitor.when(c_struct_declaration_node)
    def visit(self, node):
        return f"typedef struct {node.struct_name} {'{'}\n {self.visit(node.body)} {'}'} {node.struct_name};\n"

    @visitor.when(c_constant_declaration_node)
    def visit(self, node):
        return f"constant {node.type} {node.const_name} = {self.visit(node.expr)};\n"
    
    @visitor.when(c_function_declaration_node)
    def visit(self, node):
        ans=f"{node.type} {node.fun_name}("
        for i in range(0,len(node.args)):
            ans+=self.visit(node.args[i])
            if(i!=len(node.args)-1):
                ans+=", "
        ans+='){\n'
        ans+=self.visit(node.body)
        ans+='}\n'
        return ans

    @visitor.when(c_variable_declaration_node)
    def visit(self, node):
        return f"{node.type} {node.var_name}"
    
    @visitor.when(c_expression_block_node)
    def visit(self, node):
        ans=""
        for exp in node.expr_list:
            ans+=self.visit(exp)
        return ans
    
    @visitor.when(c_and_node)
    def visit(self, node):
        return f"( {self.visit(node.left)} && {self.visit(node.right)} )"
    
    @visitor.when(c_or_node)
    def visit(self, node):
        return f"( {self.visit(node.left)} || {self.visit(node.right)} )"
    
    @visitor.when(c_not_node)
    def visit(self, node):
        return f"(! {self.visit(node.expr)})"
    
    @visitor.when(c_less_node)
    def visit(self, node):
        return f"( {self.visit(node.left)} < {self.visit(node.right)} )"
    
    @visitor.when(c_less_equal_node)
    def visit(self, node):
        return f"( {self.visit(node.left)} <= {self.visit(node.right)} )"
    
    @visitor.when(c_greater_node)
    def visit(self, node):
        return f"( {self.visit(node.left)} > {self.visit(node.right)} )"
    
    @visitor.when(c_greater_equal_node)
    def visit(self, node):
        return f"( {self.visit(node.left)} >= {self.visit(node.right)} )"
    
    @visitor.when(c_equals_node)
    def visit(self, node):
        return f"( {self.visit(node.left)} == {self.visit(node.right)} )"
    
    @visitor.when(c_not_equals_node)
    def visit(self, node):
        return f"( {self.visit(node.left)} != {self.visit(node.right)} )"
    
    @visitor.when(c_plus_node)
    def visit(self, node):
        return f"( {self.visit(node.left)} + {self.visit(node.right)} )"
    
    @visitor.when(c_minus_node)
    def visit(self, node):
        return f"( {self.visit(node.left)} - {self.visit(node.right)} )"
    
    @visitor.when(c_multiply_node)
    def visit(self, node):
        return f"( {self.visit(node.left)} * {self.visit(node.right)} )"
    
    @visitor.when(c_divide_node)
    def visit(self, node):
        return f"( {self.visit(node.left)} / {self.visit(node.right)} )"
    
    @visitor.when(c_modulo_node)
    def visit(self, node):
        return f"( {self.visit(node.left)} % {self.visit(node.right)} )"
    
    @visitor.when(c_negative_node)
    def visit(self, node):
        return f"( - {self.visit(node.expr)} )"
    
    @visitor.when(c_variable_node)
    def visit(self, node):
        return f"{node.id}"
    
    @visitor.when(c_function_call_node)
    def visit(self, node):
        ans=f"{node.id}("
        for i in range(len(node.args)):
            ans+=self.visit(node.args[i])
            if(i!=len(node.args)-1):
                ans+=", "
        ans+=")"
        return ans
    
    @visitor.when(c_int_node)
    def visit(self, node):
        return f"{node.value}"

    @visitor.when(c_float_node)
    def visit(self, node):
        return f"{node.value}"
            

    @visitor.when(c_string_node)
    def visit(self, node):
        return f"{node.value}"
    
    @visitor.when(c_index_node)
    def visit(self, node):
        return f"{self.visit(node.array)}[{node.id}]"
    
    @visitor.when(c_attribute_call_node)
    def visit(self, node):
        return f"{node.id}.{self.visit(node.atrib)}]"
    
    @visitor.when(c_if_node)
    def visit(self, node):
        return f"if({self.visit(node.conditon)}){'{'}\n {self.visit(node.body)} {'}'}\n"
    
    @visitor.when(c_if_else_node)
    def visit(self, node):

        return f"if({self.visit(node.condition)}){'{'}\n{self.visit(node.body1)}{'}'}else{'{'}\n {self.visit(node.body2)} {'}'}\n"
    
    @visitor.when(c_for_node)
    def visit(self, node):
        return f"for({self.visit(node.var_declaration)};{self.visit(node.condition)};{self.visit(node.iteration)}){'{'}\n {self.visit(node.body)} {'}'}\n"
    
    @visitor.when(c_assignment_node)
    def visit(self, node):
        return f"{self.visit(node.variable)} = {self.visit(node.expr)}"
    
    @visitor.when(c_while_node)
    def visit(self, node):
        return f"while({self.visit(node.condition)}){'{'}\n {self.visit(node.body)} {'}'}\n"
    
    @visitor.when(c_return_node)
    def visit(self, node):
        return f"return {self.visit(node.expr)}"
    
    @visitor.when(c_scope_node)
    def visit(self, node):
        return f"{'{'}\n {self.visit(node.expr)}{'}'}\n"
    
    @visitor.when(c_break_node)
    def visit(self, node):
        return f"break"
    
    
        
    
    

    
