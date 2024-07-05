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

        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{ans}"),c_function_call_node("object_number",[op_node]))))

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
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{ans}"),c_function_call_node("object_bool",[op_node]))))

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
        
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{ans}"),c_function_call_node("object_bool",[op_node]))))
        return c_expression_block_node(list)
    
    def object_to_bool_binaryop(self,ans:int ,l:int , r:int, op):
        list=[]
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{ans}")))
        op_node="F"
        if(op=="equals"):
            op_node=c_function_call_node("equals",[c_variable_node(f"Nod_{l}"),c_variable_node(f"Nod_{r}")])
        elif(op=="not_equals"):
            op_node=c_function_call_node("not_equals",[c_variable_node(f"Nod_{l}"),c_variable_node(f"Nod_{r}")])
    
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{ans}"),c_function_call_node("object_bool",[op_node]))))
        return c_expression_block_node(list)

    def unaryop(self, ans: int,l:int ,op):
        list=[]
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{ans}")))
        op_node
        if(op=="not"):
            op_node=c_not_node(c_function_call_node("get_bool",[c_variable_node(f"Nod_{ans}")]))
            list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{ans}"),c_function_call_node("object_bool",[op_node]))))
        elif(op=="negative"):
            op_node=c_negative_node(c_function_call_node("get_number",[c_variable_node(f"Nod_{ans}")]))
            list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{ans}"),c_function_call_node("object_number",[op_node]))))
        
        return c_expression_block_node(list)

    def Interface(self,args:int,Funcs_Objs:list):
        fun_name=f"Interface_{args}"
        argum=[]
        arglist=[]
        arglist.append(c_variable_node("obj"))
        argum.append(c_variable_declaration_node("Object *","obj"))
        argum.append(c_variable_declaration_node("Object *","class"))
        argum.append(c_variable_declaration_node("char *","fun_name"))
        for i in range(args):
            argum.append(c_variable_declaration_node("Object *",f"arg_{i}"))
            arglist.append(c_variable_node(f"arg_{i}"))
        body=[]
        for tup in Funcs_Objs:
            str="object"+f"{len(tup[1])}"+"_"+tup[1]+"_"+tup[0]
            condition1=c_not_node(c_function_call_node("strcmp",[c_string_node("\""+tup[1]+"\""),c_pointer_to_node(c_variable_node("class"),c_variable_node("real_type"))]))
            condition2=c_not_node(c_function_call_node("strcmp",[c_string_node("\""+tup[0]+"\""),c_variable_node("fun_name")]))
            condition=c_and_node(condition1,condition2)
            ifbody=c_statement_node(c_return_node(c_function_call_node(str,arglist)))
            body.append(c_if_node(condition,ifbody))
        retlist=list(arglist)
        retlist.insert(1,c_variable_node("fun_name"))
        retlist.insert(1,c_variable_node("class"))
        retlist[1]=c_function_call_node("get",[c_pointer_to_node(c_variable_node("class"),c_variable_node("attributes")),c_string_node("\"parent\"")])
        body.append(c_statement_node(c_return_node(c_function_call_node(fun_name,retlist))))
        return c_function_declaration_node(fun_name,argum,c_expression_block_node(body),"Object *")

    @visitor.on('node')
    def visit(self, node, espectial = None):
        pass
    
    @visitor.when(program_node)
    def visit(self, node, espectial = None):
        self.cont=0
        list=[]
        self.Ob_funs_dic={}
        self.Ob_funs_dic[0]=[]
        self.Ob_funs_dic[0].append(("current","Range"))
        self.Ob_funs_dic[0].append(("next","Range"))
        self.fun_def=[]
        for dec in node.dec_list:
            list.append(self.visit(dec,espectial))
        for fun in self.fun_def:
            list.insert(0,fun)
        for key in self.Ob_funs_dic:
            d=self.Interface(key,self.Ob_funs_dic[key])
            list.insert(0,c_function_declaration_node(d.fun_name,d.args,None,d.type))
            list.append(d)
        body=self.visit(node.global_expr,espectial)
        MainBody=[]
        MainBody.append(body)
        MainBody.append(c_statement_node(c_return_node(c_int_node("0"))))
        main=c_function_declaration_node("main",[],c_expression_block_node(MainBody),"int")
        list.append(main)
        return c_program_node([],list)

            
    @visitor.when(function_declaration_node)
    def visit(self, node, espectial = None):
        fun_name=""
        body=""
        
        args=[]
        if espectial != None:
            args.append(c_variable_declaration_node("Object *",f"Var_self"))
        for arg in node.params:
            args.append(c_variable_declaration_node("Object *",f"Var_{arg.id}"))
        if(espectial==None):
            fun_name=f"function_{node.id}"
            self.fun_def.append(c_function_declaration_node(fun_name,args,None,"Object*"))
            body=self.visit(node.body,espectial)
        else:
            fun_name=f"object{len(espectial)}_{espectial}_{node.id}"
            if(len(node.params) not in self.Ob_funs_dic):
                self.Ob_funs_dic[len(node.params)]=[]
            self.Ob_funs_dic[len(node.params)].append((node.id,espectial))
            body=self.visit(node.body,node.id)
        retvar=self.cont
        type="Object *"
        self.cont+=1
        ret=c_statement_node(c_return_node(c_variable_node(f"Nod_{retvar}")))
        body=c_expression_block_node([body,ret])
        return c_function_declaration_node(fun_name,args,body,type)

    @visitor.when(type_declaration_node)
    def visit(self, node, espectial = None):
        funlist=[]
        params=[]
        for arg in node.params:
            if(isinstance(arg,variable_declaration_node)):
                params.append(c_variable_declaration_node("Object *",f"Var_{arg.id}"))
            continue
        body=[]
        body.append(c_statement_node(c_variable_declaration_node("Object*","Var_self")))
        body.append(c_statement_node(c_assignment_node(c_variable_node("Var_self"),c_function_call_node("instantiate",[c_string_node("\""+node.id+"\"")]))))
        args=[]
        for arg in node.args:
            body.append(self.visit(arg))
            args.append(c_variable_node(f"Nod_{self.cont}"))
        if(node.parent== None):
            node.parent="Object"
        parent_instantiation=c_function_call_node(f"object_{node.parent}",args)
        body.append(c_statement_node(c_function_call_node("insert",[c_pointer_to_node(c_variable_node("Var_self"),c_variable_node("attributes")),c_string_node("\"parent\""),parent_instantiation])))
            
        for feat in node.features:
            d=self.visit(feat,node.id)
            if isinstance(feat,function_declaration_node):
                funlist.append(d)
            else:
                body.append(d)
        body.append(c_statement_node(c_return_node(c_variable_node("Var_self"))))
        self.fun_def.append(c_function_declaration_node(f"object_{node.id}",params,None,"Object*"))
        constructor=c_function_declaration_node(f"object_{node.id}",params,c_expression_block_node(body),"Object*")
        funlist.append(constructor)
        return c_expression_block_node(funlist)
        
        
    @visitor.when(variable_declaration_node)
    def visit(self, node, espectial = None):
        exp=self.visit(node.value,espectial)
        self.cont+=1
        list=[exp]
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_variable_node(f"Nod_{self.cont-1}"))))
        if(espectial== None):
            list.append(c_statement_node(c_variable_declaration_node("Object *",f"Var_{node.id}")))
            list.append(c_statement_node(c_assignment_node(c_variable_node(f"Var_{node.id}"),c_variable_node(f"Nod_{self.cont-1}"))))
        else:
            list.append(c_statement_node(c_function_call_node("insert",[c_pointer_to_node(c_variable_node("Var_self"),c_variable_node("attributes")),c_string_node("\"Var_"+node.id+"\""),c_variable_node(f"Nod_{self.cont}")])))
        return c_expression_block_node(list)
    
    @visitor.when(expression_block_node)
    def visit(self, node, espectial = None):
        list=[]
        for expr in node.expressions:
            list.append(self.visit(expr,espectial))
        self.cont+=1
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_variable_node(f"Nod_{self.cont-1}"))))
        
        return c_expression_block_node(list)

    @visitor.when(concatenation_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left,espectial))
        l=self.cont
        list.append(self.visit(string_node('"'+node.middle+'"')))
        m=self.cont
        list.append(self.visit(node.right,espectial))
        r=self.cont
        self.cont+=1
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_function_call_node("concatenate",[c_variable_node(f"Nod_{l}"),c_function_call_node("concatenate",[c_string_node(f"Nod_{m}"),c_variable_node(f"Nod_{r}")])]))))
        return c_expression_block_node(list)

        
    
    @visitor.when(and_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left,espectial))
        l=self.cont
        list.append(self.visit(node.right,espectial))
        r=self.cont
        self.cont+=1
        list.append(self.bool_to_bool_binaryop(self.cont,l,r,"and"))
        return c_expression_block_node(list)

    @visitor.when(or_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left,espectial))
        l=self.cont
        list.append(self.visit(node.right,espectial))
        r=self.cont
        self.cont+=1
        list.append(self.bool_to_bool_binaryop(self.cont,l,r,"or"))
        return c_expression_block_node(list)
    
    @visitor.when(not_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.expr,espectial))
        l=self.cont
        self.cont+=1
        list.append(self.unaryop(self.cont,l,"not"))
        return c_expression_block_node(list)

    @visitor.when(is_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.expr,espectial))
        exp=self.cont
        self.cont+=1
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}"))) 
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_function_call_node(f"is_child_from_class",[c_variable_node(exp),"\""+node.type_id+"\""]))))
        return c_expression_block_node(list)

    @visitor.when(less_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left,espectial))
        l=self.cont
        list.append(self.visit(node.right,espectial))
        r=self.cont
        self.cont+=1
        list.append(self.number_to_bool_binaryop(self.cont,l,r,"less"))
        return c_expression_block_node(list)

    @visitor.when(less_equal_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left,espectial))
        l=self.cont
        list.append(self.visit(node.right,espectial))
        r=self.cont
        self.cont+=1
        list.append(self.number_to_bool_binaryop(self.cont,l,r,"less_equal"))
        return c_expression_block_node(list)
    
    @visitor.when(greater_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left,espectial))
        l=self.cont
        list.append(self.visit(node.right,espectial))
        r=self.cont
        self.cont+=1
        list.append(self.number_to_bool_binaryop(self.cont,l,r,"greater"))
        return c_expression_block_node(list)

    @visitor.when(greater_equal_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left,espectial))
        l=self.cont
        list.append(self.visit(node.right,espectial))
        r=self.cont
        self.cont+=1
        list.append(self.number_to_bool_binaryop(self.cont,l,r,"greater_equal"))
        return c_expression_block_node(list)

    @visitor.when(equals_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left,espectial))
        l=self.cont
        list.append(self.visit(node.right,espectial))
        r=self.cont
        self.cont+=1
        list.append(self.object_to_bool_binaryop(self.cont,l,r,"equals"))
        return c_expression_block_node(list)

    @visitor.when(not_equals_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left,espectial))
        l=self.cont
        list.append(self.visit(node.right,espectial))
        r=self.cont
        self.cont+=1
        list.append(self.object_to_bool_binaryop(self.cont,l,r,"not_equals"))
        return c_expression_block_node(list)

    @visitor.when(plus_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left,espectial))
        l=self.cont
        list.append(self.visit(node.right,espectial))
        r=self.cont
        self.cont+=1
        list.append(self.number_to_number_binaryop(self.cont,l,r,"plus"))
        return c_expression_block_node(list)

    @visitor.when(minus_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left,espectial))
        l=self.cont
        list.append(self.visit(node.right,espectial))
        r=self.cont
        self.cont+=1
        list.append(self.number_to_number_binaryop(self.cont,l,r,"minus"))
        return c_expression_block_node(list)
    
    @visitor.when(negative_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.expr,espectial))
        l=self.cont
        self.cont+=1
        list.append(self.unaryop(self.cont,l,"negative"))
        return c_expression_block_node(list)


    @visitor.when(multiply_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left,espectial))
        l=self.cont
        list.append(self.visit(node.right,espectial))
        r=self.cont
        self.cont+=1
        list.append(self.number_to_number_binaryop(self.cont,l,r,"multiply"))
        return c_expression_block_node(list)

    @visitor.when(divide_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left,espectial))
        l=self.cont
        list.append(self.visit(node.right,espectial))
        r=self.cont
        self.cont+=1
        list.append(self.number_to_number_binaryop(self.cont,l,r,"divide"))
        return c_expression_block_node(list)

    @visitor.when(modulo_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left,espectial))
        l=self.cont
        list.append(self.visit(node.right,espectial))
        r=self.cont
        self.cont+=1
        list.append(self.number_to_number_binaryop(self.cont,l,r,"modulo"))
        return c_expression_block_node(list)

    @visitor.when(power_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.left,espectial))
        l=self.cont
        list.append(self.visit(node.right,espectial))
        r=self.cont
        self.cont+=1
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))
        l_as_number=c_function_call_node("get_number",[c_variable_node(f"Nod_{l}")])
        r_as_number=c_function_call_node("get_number",[c_variable_node(f"Nod_{r}")])
        op_node=c_function_call_node("pow",[l_as_number,r_as_number])
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_function_call_node("object_number",[op_node]))))
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
        fun_name=f"function_{node.id}"
        if espectial!=None and node.id=="base":
            nlist.append(c_function_call_node("get",[c_pointer_to_node(c_variable_node("Var_self"),c_variable_node("attributes")),c_string_node("\"parent\"")]))
            nlist.append(c_function_call_node("get",[c_pointer_to_node(c_variable_node("Var_self"),c_variable_node("attributes")),c_string_node("\"parent\"")]))
            nlist.append(c_string_node("\""+espectial+"\""))
            fun_name=f"Interface_{len(node.args)}"
        for arg in node.args:
            list.append(self.visit(arg))
            nlist.append(c_variable_node(f"Nod_{self.cont}"))
        self.cont+=1
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))

        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_function_call_node(fun_name,nlist))))
        return c_expression_block_node(list)

    @visitor.when(number_node)
    def visit(self, node, espectial = None):
        list=[]
        self.cont+=1
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_function_call_node("object_number",[c_float_node(node.value)]))))
        return c_expression_block_node(list)
    
    @visitor.when(bool_node)
    def visit(self, node, espectial = None):
        list=[]
        self.cont+=1
        val= "1" if node.value=="true" else "0"
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_function_call_node("object_bool",[c_int_node(val)]))))
        return c_expression_block_node(list)
    
    @visitor.when(string_node)
    def visit(self, node, espectial = None):
        list=[]
        self.cont+=1
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_function_call_node("object_string",[c_string_node(node.value)]))))
        return c_expression_block_node(list)
    
    @visitor.when(index_node)
    def visit(self, node, espectial = None):
        pass

    @visitor.when(as_node)
    def visit(self, node, espectial = None):
        pass

    @visitor.when(property_call_node)
    def visit(self, node, espectial = None):
        list=[self.visit(node.expr,espectial)]
        obye=self.cont
        nodef=node.func
        nlist=[]
        nlist.append(c_variable_node(f"Nod_{obye}"))
        nlist.append(c_variable_node(f"Nod_{obye}"))
        nlist.append(c_string_node("\""+nodef.id+"\""))
        fun_name=f"Interface_{len(nodef.args)}"
        for arg in nodef.args:
            list.append(self.visit(arg))
            nlist.append(c_variable_node(f"Nod_{self.cont}"))
        self.cont+=1
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_function_call_node(fun_name,nlist))))
        return c_expression_block_node(list)


    @visitor.when(attribute_call_node)
    def visit(self, node, espectial = None):
        self.cont+=1
        list=[]
        list.append(c_statement_node(c_variable_declaration_node("Object*",f"Nod_{self.cont}")))
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_function_call_node("get",[c_pointer_to_node(c_variable_node("Var_self"),c_variable_node("attributes")),c_string_node(f"\"Var_{node.id}\"")]))))
        return c_expression_block_node(list)

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
        list=[]
        arglist=[]
        for arg in node.args:
            list.append(self.visit(arg))
            arglist.append(c_variable_node(f"Nod_{self.cont}"))
        self.cont+=1
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))
        list.append(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_function_call_node(f"object_{node.type_id}",arglist))))
        return c_expression_block_node(list)

    @visitor.when(assignment_node)
    def visit(self, node, espectial = None):
        list=[]
        list.append(self.visit(node.var))
        l=self.cont
        list.append(self.visit(node.expr))
        r=self.cont
        self.cont+=1
        list.append(c_statement_node(c_assignment_node(c_pointer_node(c_variable_node(f"Nod_{l}")),c_pointer_node(c_variable_node(f"Nod_{r}")))))
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
        condition=self.visit(node.condition)
        condid=self.cont
        body=self.visit(node.body)
        bodid=self.cont
        self.cont+=1
        list=[]
        list.append(c_statement_node(c_variable_declaration_node("Object *",f"Nod_{self.cont}")))
        whilebody=[]
        whilebody.append(condition)
        ifcond=c_function_call_node("get_bool",[c_variable_node(f"Nod_{condid}")])
        body=c_expression_block_node([body,(c_statement_node(c_assignment_node(c_variable_node(f"Nod_{self.cont}"),c_variable_node(f"Nod_{bodid}"))))])
        elsebod=c_statement_node(c_break_node())
        whilebody.append(c_if_else_node(ifcond,body,elsebod))
        whilecond=c_int_node("1")
        list.append(c_while_node(whilecond,c_expression_block_node(whilebody)))
        return c_expression_block_node(list)
        

    @visitor.when(for_node)
    def visit(self, node, espectial = None):
        while_body=let_node([variable_declaration_node(node.variable.id,None,property_call_node(variable_node("let"),function_call_node("current",[])))],node.body)
        body=while_node(property_call_node(variable_node("let"),function_call_node("next",[])),while_body)
        for_nod=let_node([variable_declaration_node("let",None,node.expr)],body)
        return self.visit(for_nod)

    @visitor.when(vector_comprehension_node)
    def visit(self, node, espectial = None):
        pass