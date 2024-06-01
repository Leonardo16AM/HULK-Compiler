#include <iostream>
#include <string>

#include "../backbone/error.h"
#include "../backbone/token.h"
#include "../backbone/lexer_out.h"
#include "backbone_test.h"


bool testbackbone(){

    token t1 = token("value", 1, 1, "type");
    token t2 = token("value", 1, 1, "type");
    token t3 = token("value", 1, 1, "type2");

    if(!(t1 == t2)){
        std::cout << "Token comparison failed" << std::endl;
        return false;
    }

    if(t1 == t3){
        std::cout << "Token comparison failed" << std::endl;
        return false;
    }

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


    std::cout<<"Backbone test passed"<<std::endl;
    return true;
}