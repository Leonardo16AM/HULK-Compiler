#include "regex_test.h"
#include <iostream>
#include <string>

#include "regex/regex_token.h"
#include "regex/regex_grammar.h"
#include "regex/regex_out.h"
#include "regex/regex_parser.h"
#include "regex/regex_lexer.h"
#include "regex/regex_ast.h"

#include "../backbone/error.h"


bool regex_test(){
    std::cout << "Testing regex" << std::endl;

    std::string regex="( |\n|\t)+|//[^\n]*\n|/\*([^\*]|\*[^/])*(\*/|\*\*/)";

    regex_out out = regex_lexer(regex);

    if(!out.ok){
        std::cout << "Lexer failed" << std::endl;
        return false;
    }

    for(auto t: out.value){
        std::cout << t.value <<" ";
    }
    std::cout << std::endl;



    return true;
}