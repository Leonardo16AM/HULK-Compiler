from src.semantic.type_finder_visitor import type_finder
from src.semantic.type_filler_visitor import type_filler
from src.semantic.var_finder_visitor import var_finder
from termcolor import colored

def semantic_check(ast):
    errors=[]
    type_collector = type_finder(errors)
    context,errors=type_collector.visit(ast)

    var_collector=var_finder(context,errors)
    scope=var_collector.visit(ast)
    print(colored(scope,'yellow'))

    type_fill = type_filler(context, errors)
    context,errors=type_fill.visit(ast)


    print(context)

    if errors:
        for error in errors:
            print(error)
        return False
    
    print("NO SEMANTIC ERRORS FOUND")
    return True

