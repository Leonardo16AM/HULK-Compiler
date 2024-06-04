#include <iostream>
#include "tests/backbone_test.h"
#include "tests/regex_test.h"
#include "backbone/attributed_rule.h"

int main(){
    std::cout<<"Compilation started"<<std::endl;

    if(!testbackbone()){
        std::cout<<"BACKBONE Test failed"<<std::endl;
    }

    
    if(!regex_test()){
        std::cout<<"REGEX Test failed"<<std::endl;
    }


    std::cout<<"Compilation ended"<<std::endl;
    return 0;
}