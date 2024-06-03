#include <iostream>
#include <string>

#include "../backbone/error.h"
#include "../backbone/lexer_token.h"
#include "../backbone/lexer_out.h"

#include "../backbone/grammar_token.h"
#include "../backbone/grammar.h"
#include "../backbone/grammar_production.h"
#include "../backbone/derivation_tree.h"
#include "../backbone/attributed_grammar.h"
#include "../backbone/attributed_rule.h"

#include "backbone_test.h"


bool testbackbone(){

    #pragma region grammar_token
        lexer_token t1 = lexer_token("value", 1, 1, "type");
        lexer_token t2 = lexer_token("value", 1, 1, "type");
        lexer_token t3 = lexer_token("value", 1, 1, "type2");

        if(!(t1 == t2)){
            std::cout << "lexer_Token comparison failed" << std::endl;
            return false;
        }

        if(t1 == t3){
            std::cout << "lexer_Token comparison failed" << std::endl;
            return false;
        }
    #pragma endregion


    
    #pragma region lexer_out
    lexer_out l1 = lexer_out();
    lexer_out l2 = lexer_out({t1, t2, t3});
    lexer_out l3 = lexer_out(new error("error",1,1));

    if(l1.ok != true){
        std::cout << "Lexer_out default constructor failed" << std::endl;
        return false;
    }
    
    if(l2.ok != true){
        std::cout << "Lexer_out vector constructor failed" << std::endl;
        return false;
    }

    if(l3.ok != false){
        std::cout << "Lexer_out error constructor failed" << std::endl;
        return false;
    }

    if(l2.size() != 3){
        std::cout << "Lexer_out size failed" << std::endl;
        return false;
    }

    if(!(l2[0] == t1)){
        std::cout << "Lexer_out operator[] failed" << std::endl;
        return false;
    }
    #pragma endregion

    
    #pragma region grammar_token
    grammar_token g1 = grammar_token();
    grammar_token g2 = grammar_token("value2", true, false);
    grammar_token g3 = grammar_token("value", true, true);
    grammar_token g4 = grammar_token("value", false, false);

    if(g1.value != "_"){
        std::cout << "Grammar_token default constructor failed" << std::endl;
        return false;
    }

    if(g2.value != "value2" || g2.is_terminal != true || g2.is_main != false){
        std::cout << "Grammar_token constructor failed" << std::endl;
        return false;
    }

    if(g2 == g3){
        std::cout << "Grammar_token comparison failed (==)" << std::endl;
        return false;
    }

    if(g3 != g4){
        std::cout << "Grammar_token comparison failed (!=)" << std::endl;
        return false;
    }

    if(g3.hash() != std::hash<std::string>()("value")){
        std::cout << "Grammar_token hash failed" << std::endl;
        return false;
    }

    if(g3.to_string() != "value"){
        std::cout << "Grammar_token to_string failed" << std::endl;
        return false;
    }

    EOF_token e1 = EOF_token();
    if(e1.value != "EOF" || e1.is_terminal != true){
        std::cout << "EOF_token constructor failed" << std::endl;
        return false;
    }
    #pragma endregion


    #pragma region grammar_production
    #pragma endregion

    
    #pragma region grammar
    #pragma endregion

    
    #pragma region derivation_tree
    #pragma endregion


    
    #pragma region attributed_grammar
    #pragma endregion


    #pragma region attributed_rule
    #pragma endregion

    std::cout<<"Backbone test passed"<<std::endl;
    return true;
}