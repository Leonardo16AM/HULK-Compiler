from src.codegen.c_ast import *
from src.codegen.c_ast_gen import *
from src.codegen.c_gen_code import *
import subprocess
import os
from termcolor import colored

class C_code:
    def __init__(self, code):
        self.code = code
    
    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.path=path
        with open(path, 'w') as file:
            file.write(self.code)
    
    def compile_and_run(self, path=None):
        if path==None:
            path=self.path

        filename = os.path.splitext(path)[0]
        
        compile_command = f"gcc {path} -o {filename}.exe"
        compile_process = subprocess.run(compile_command, shell=True, capture_output=True, text=True)
        
        if compile_process.returncode != 0:
            print(colored(f"Compilation failed:\n{compile_process.stderr}","red"))
            return
        
        dir_name = os.path.dirname(filename)
        exe_name = os.path.basename(filename) + ".exe"
        
        os.chdir(dir_name)
        
        run_command = exe_name
        run_process = subprocess.run(run_command, shell=True, capture_output=True, text=True)
        
        if run_process.returncode != 0:
            print(colored(f"Execution failed:\n{run_process.stderr}","red" ))
        else:
            print(f"Execution output:\n{run_process.stdout}")
def codegen(ast):
    ast_gen=ast_generator()
    c_ast=ast_gen.visit(ast)
    code_gen=code_generator()
    code=code_gen.visit(c_ast)

    code=C_code(code)
    return code