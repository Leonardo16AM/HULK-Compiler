import src.cmp.visitor as visitor
from src.cmp.ast import *
from abc import ABC, abstractmethod
from src.grammar.hulk_ast import *
from src.codegen.c_ast import *




class ast_generator:

    def number_to_number_binaryop(self,ans:int ,l:int , r:int, op):
        list=[]
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{ans}")))
        l_as_number=c_function_call_node("get_number",[c_variable_node(f"Nod_{l}")])
        r_as_number=c_function_call_node("get_number",[c_variable_node(f"Nod_{r}")])

        op_node="F"
        if(op=="plus"):
            op_node=c_plus_node(l_as_number,r_as_number)
        elif(op=="minus"):
            op_node=c_minus_node(l_as_number,r_as_number)
        elif(op=="multiply"):
            op_node=c_multiply_node(l_as_number,r_as_number)
        elif(op=="divide"):
            op_node=c_divide_node(l_as_number,r_as_number)
        elif(op=="modulo"):
            op_node=c_modulo_node(l_as_number,r_as_number)

        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{ans}"),c_function_call_node("number_object",[op_node]))))

        return c_expression_block_node(list)

    def bool_to_bool_binaryop(self,ans:int ,l:int , r:int, op):
        list=[]
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{ans}")))
        l_as_bool=c_function_call_node("get_bool",[c_variable_node(f"Nod_{l}")])
        r_as_bool=c_function_call_node("get_bool",[c_variable_node(f"Nod_{r}")])

        op_node="F"
        if(op=="and"):
            op_node=c_and_node(l_as_bool,r_as_bool)
        elif(op=="or"):
            op_node=c_or_node(l_as_bool,r_as_bool)
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{ans}"),c_function_call_node("bool_object",[op_node]))))

        return c_expression_block_node(list)

    def number_to_bool_binaryop(self,ans:int ,l:int , r:int, op):
        list=[]
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{ans}")))
        l_as_number=c_function_call_node("get_number",[c_variable_node(f"Nod_{l}")])
        r_as_number=c_function_call_node("get_number",[c_variable_node(f"Nod_{r}")])

        op_node="F"
        if(op=="less_equal"):
            op_node=c_less_equal_node(l_as_number,r_as_number)    
        elif(op=="less"):
            op_node=c_less_node(l_as_number,r_as_number)
        elif(op=="greater"):
            op_node=c_greater_node(l_as_number,r_as_number)
        elif(op=="greater_equal"):
            op_node=c_greater_equal_node(l_as_number,r_as_number)
        
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{ans}"),c_function_call_node("bool_object",[op_node]))))
        return c_expression_block_node(list)
    
    def object_to_bool_binaryop(self,ans:int ,l:int , r:int, op):
        list=[]
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{ans}")))
        op_node="F"
        if(op=="equals"):
            op_node=c_function_call_node("equals",[c_variable_node(f"Nod_{l}"),c_variable_node(f"Nod_{r}")])
        elif(op=="not_equals"):
            op_node=c_function_call_node("not_equals",[c_variable_node(f"Nod_{l}"),c_variable_node(f"Nod_{r}")])
    
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{ans}"),c_function_call_node("bool_object",[op_node]))))
        return c_expression_block_node(list)

    def unaryop(self, ans: int,l:int ,op):
        list=[]
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{ans}")))
        op_node
        if(op=="not"):
            op_node=c_not_node(c_function_call_node("get_bool",[c_variable_node(f"Nod_{ans}")]))
            list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{ans}"),c_function_call_node("bool_object",[op_node]))))
        elif(op=="negative"):
            op_node=c_negative_node(c_function_call_node("get_number",[c_variable_node(f"Nod_{ans}")]))
            list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{ans}"),c_function_call_node("number_object",[op_node]))))
        
        return c_expression_block_node(list)

    @visitor.on('node')
    def visit(self, node, espectial = None):
        pass
    
    @visitor.when(program_node)
    def visit(self, node, espectial = None):
        self.cont=0
        list=[]
        for dec in node.dec_list:
            list.append(self.visit(dec))
        body=self.visit(node.global_expr)
        MainBody=[]
        MainBody.append(body)
        MainBody.append(c_statement_node(c_return_node(c_int_node("0"))))
        main=c_function_declaration_node("main",[],c_expression_block_node(MainBody),"int")
        list.append(main)
        return c_program_node([],list)

            

        
    @visitor.when(function_declaration_node)
    def visit(self, node, espectial = None):
        fun_name=f"function_{node.id}"
        body=self.visit(node.body)
        retvar=self.cont
        args=[]
        for arg in node.params:
            args.append(c_variable_declaration_node("Object *",f"Var_{arg.id}"))
        type="Object *"
        self.cont+=1
        ret=c_statement_node(c_return_node(c_variable_node(f"Nod_{retvar}")))
        body=c_expression_block_node([body,ret])
        return c_function_declaration_node(fun_name,args,body,type)

    @visitor.when(type_declaration_node)
    def visit(self, node, espectial = None):
        pass

    @visitor.when(protocol_declaration_node)
    def visit(self, node, espectial = None):
        pass
    
    @visitor.when(variable_declaration_node)
    def visit(self, node, espectial = None):
        exp=self.visit(node.value)
        self.cont+=1
        list=[exp]
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Var_{node.id}")))
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_variable_node(f"Nod_{self.cont-1}"))))
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Var_{node.id}"),c_variable_node(f"Nod_{self.cont-1}"))))
        return c_expression_block_node(list)
    
    @visitor.when(expression_block_node)
    def visit(self, node, espectial = None):
        list=[]
        for expr in node.expressions:
            list.append(self.visit(expr))
        self.cont+=1
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_variable_node(f"Nod_{self.cont-1}"))))
        
        return c_expression_block_node(list)

    @visitor.when(concatenation_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left))
        l=self.cont
        list.append(self.visit(string_node(f"{'"'}{node.middle}{'"'}")))
        m=self.cont
        list.append(self.visit(node.right))
        r=self.cont
        self.cont+=1
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_function_call_node("concatenate",[c_variable_node(f"Nod_{l}"),c_function_call_node("concatenate",[c_string_node(f"Nod_{m}"),c_variable_node(f"Nod_{r}")])]))))
        return c_expression_block_node(list)

        
    
    @visitor.when(and_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left))
        l=self.cont
        list.append(self.visit(node.right))
        r=self.cont
        self.cont+=1
        list.append(self.bool_to_bool_binaryop(self.cont,l,r,"and"))
        return c_expression_block_node(list)

    @visitor.when(or_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left))
        l=self.cont
        list.append(self.visit(node.right))
        r=self.cont
        self.cont+=1
        list.append(self.bool_to_bool_binaryop(self.cont,l,r,"or"))
        return c_expression_block_node(list)
    
    @visitor.when(not_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.expr))
        l=self.cont
        self.cont+=1
        list.append(self.unaryop(self.cont,l,"not"))
        return c_expression_block_node(list)

    @visitor.when(is_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.expr))
        exp=self.cont
        class_pointer=c_function_call_node("get_class_object",[c_string_node(node.type_id)])
        self.cont+=1
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_function_call_node(f"is_child_from_class",[c_variable_node(exp),class_pointer]))))
        return c_expression_block_node(list)

    @visitor.when(less_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left))
        l=self.cont
        list.append(self.visit(node.right))
        r=self.cont
        self.cont+=1
        list.append(self.number_to_bool_binaryop(self.cont,l,r,"less"))
        return c_expression_block_node(list)

    @visitor.when(less_equal_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left))
        l=self.cont
        list.append(self.visit(node.right))
        r=self.cont
        self.cont+=1
        list.append(self.number_to_bool_binaryop(self.cont,l,r,"less_equal"))
        return c_expression_block_node(list)
    
    @visitor.when(greater_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left))
        l=self.cont
        list.append(self.visit(node.right))
        r=self.cont
        self.cont+=1
        list.append(self.number_to_bool_binaryop(self.cont,l,r,"greater"))
        return c_expression_block_node(list)

    @visitor.when(greater_equal_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left))
        l=self.cont
        list.append(self.visit(node.right))
        r=self.cont
        self.cont+=1
        list.append(self.number_to_bool_binaryop(self.cont,l,r,"greater_equal"))
        return c_expression_block_node(list)

    @visitor.when(equals_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left))
        l=self.cont
        list.append(self.visit(node.right))
        r=self.cont
        self.cont+=1
        list.append(self.object_to_bool_binaryop(self.cont,l,r,"equals"))
        return c_expression_block_node(list)

    @visitor.when(not_equals_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left))
        l=self.cont
        list.append(self.visit(node.right))
        r=self.cont
        self.cont+=1
        list.append(self.object_to_bool_binaryop(self.cont,l,r,"not_equals"))
        return c_expression_block_node(list)

    @visitor.when(plus_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left))
        l=self.cont
        list.append(self.visit(node.right))
        r=self.cont
        self.cont+=1
        list.append(self.number_to_number_binaryop(self.cont,l,r,"plus"))
        return c_expression_block_node(list)

    @visitor.when(minus_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left))
        l=self.cont
        list.append(self.visit(node.right))
        r=self.cont
        self.cont+=1
        list.append(self.number_to_number_binaryop(self.cont,l,r,"minus"))
        return c_expression_block_node(list)
    
    @visitor.when(negative_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.expr))
        l=self.cont
        self.cont+=1
        list.append(self.unaryop(self.cont,l,"negative"))
        return c_expression_block_node(list)


    @visitor.when(multiply_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left))
        l=self.cont
        list.append(self.visit(node.right))
        r=self.cont
        self.cont+=1
        list.append(self.number_to_number_binaryop(self.cont,l,r,"multiply"))
        return c_expression_block_node(list)

    @visitor.when(divide_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left))
        l=self.cont
        list.append(self.visit(node.right))
        r=self.cont
        self.cont+=1
        list.append(self.number_to_number_binaryop(self.cont,l,r,"divide"))
        return c_expression_block_node(list)

    @visitor.when(modulo_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left))
        l=self.cont
        list.append(self.visit(node.right))
        r=self.cont
        self.cont+=1
        list.append(self.number_to_number_binaryop(self.cont,l,r,"modulo"))
        return c_expression_block_node(list)

    @visitor.when(power_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left))
        l=self.cont
        list.append(self.visit(node.right))
        r=self.cont
        self.cont+=1
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))
        l_as_number=c_function_call_node("get_number",[c_variable_node(f"Nod_{l}")])
        r_as_number=c_function_call_node("get_number",[c_variable_node(f"Nod_{r}")])
        op_node=c_function_call_node("pow",[l_as_number,r_as_number])
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_function_call_node("number_object",[op_node]))))
        return c_expression_block_node(list)



    @visitor.when(variable_node)
    def visit(self, node, espectial = None):
        list=[]
        self.cont+=1
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_variable_node(f"Var_{node.id}"))))
        return c_expression_block_node(list)
    
    @visitor.when(function_call_node)
    def visit(self, node, espectial = None):
        list=[]
        nlist=[]
        for arg in node.args:
            list.append(self.visit(arg))
            nlist.append(c_variable_node(f"Nod_{self.cont}"))
        self.cont+=1
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_function_call_node(f"function_{node.id}",nlist))))
        return c_expression_block_node(list)

    @visitor.when(number_node)
    def visit(self, node, espectial = None):
        list=[]
        self.cont+=1
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_function_call_node("number_object",[c_float_node(node.value)]))))
        return c_expression_block_node(list)
    
    @visitor.when(bool_node)
    def visit(self, node, espectial = None):
        list=[]
        self.cont+=1
        val= "1" if node.value=="true" else "0"
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_function_call_node("bool_object",[c_int_node(val)]))))
        return c_expression_block_node(list)
    
    @visitor.when(string_node)
    def visit(self, node, espectial = None):
        list=[]
        self.cont+=1
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_function_call_node("string_object",[c_string_node(node.value)]))))
        return c_expression_block_node(list)
    
    @visitor.when(index_node)
    def visit(self, node, espectial = None):
        pass

    @visitor.when(as_node)
    def visit(self, node, espectial = None):
        pass

    @visitor.when(property_call_node)
    def visit(self, node, espectial = None):
        pass

    @visitor.when(attribute_call_node)
    def visit(self, node, espectial = None):
        pass

    @visitor.when(if_node)
    def visit(self, node, espectial = None):
        list=[]
        conditions=[]
        results=[]
       
        for blocks in node.conditions_bodies:
            c=self.visit(blocks[0])
            conditions.append((self.cont,c))
            r=self.visit(blocks[1])
            results.append((self.cont,r))
        self.cont+=1
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))
        tam=len(conditions)
        lastblock=c_expression_block_node([results[tam-1][1],c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_variable_node(f"Nod_{results[tam-1][0]}")))])
        for i in reversed(range(tam-1)):
            condition1=c_function_call_node("get_bool",[c_variable_node(f"Nod_{conditions[i][0]}")])
            body1=c_expression_block_node([results[i][1],c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_variable_node(f"Nod_{results[i][0]}")))])
            lastblock=c_expression_block_node([conditions[i][1],c_if_else_node(condition1,body1,lastblock)])
        list.append(lastblock)
        return c_expression_block_node(list)
    
    @visitor.when(vector_node)
    def visit(self, node, espectial = None):
        pass

    @visitor.when(new_node)
    def visit(self, node, espectial = None):
        pass

    @visitor.when(assignment_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.var))
        l=self.cont
        list.append(self.visit(node.expr))
        r=self.cont
        self.cont+=1
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"*Nod_{l}"),c_variable_node(f"*Nod_{r}"))))
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_variable_node(f"Nod_{l}"))))
        return c_expression_block_node(list)

    @visitor.when(let_node)
    def visit(self, node, espectial = None):
        list=[]
        declist=[]
        for dec in node.declarations:
            list.append(self.visit(dec))
            declist.append(self.cont)
        b2=self.visit(node.body)
        bod=self.cont
        self.cont+=1
        list.append(b2)
        finalans=[(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))]
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_variable_node(f"Nod_{declist[0]}"))))
        finalans.append(c_scope_node(c_expression_block_node(list)))
        return c_expression_block_node(finalans)

    @visitor.when(while_node)
    def visit(self, node, espectial = None):
        condition=self.visit

    @visitor.when(for_node)
    def visit(self, node, espectial = None):
        pass

    @visitor.when(vector_comprehension_node)
    def visit(self, node, espectial = None):
        pass