from src.semantic.type_finder_visitor import type_finder
from src.semantic.type_filler_visitor import type_filler
from src.semantic.var_finder_visitor import var_finder
from src.semantic.type_inferer_visitor import type_inferer
from termcolor import colored

def semantic_check(ast,verbose=False):
    errors=[]
    warnings=[]
    type_collector = type_finder(errors)
    context,errors=type_collector.visit(ast)


    if verbose:errors.append("TYPE FILLING")
    type_fill = type_filler(context, errors)
    context,errors=type_fill.visit(ast)


    if verbose:errors.append("VAR COLLECTION")
    var_collector=var_finder(context,errors,warnings)
    scope=var_collector.visit(ast)
    
    
    scope.define_variable("PI",context.get_type("Number"))
    scope.define_variable("E",context.get_type("Number"))

    if verbose:print(colored(scope,'yellow'))
    
    print(colored(context,'blue'))

    if verbose:errors.append("TYPE CHECKING")
    type_inf=type_inferer(context,errors,warnings)
    context,errors,warnings=type_inf.visit(ast,scope)

    print(colored(context,'cyan'))

    
    for warning in warnings:
        print(warning)
    if errors:
        for error in errors:
            print(error)
        return False
    

    
    if verbose:print("NO SEMANTIC ERRORS FOUND")
    return True

