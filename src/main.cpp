#include <iostream>
#include "tests/backbone_test.h"

int main(){
    std::cout<<"Compilation started"<<std::endl;

    if(!testbackbone()){
        std::cout<<"Test failed"<<std::endl;
        return 1;
    }

    std::cout<<"Compilation ended"<<std::endl;
    return 0;
}