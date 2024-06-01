#include "lexer_out.h"

lexer_out::lexer_out(){
    this->ok = true;
    this->tokens = {};
    this->err = nullptr;
}

lexer_out::lexer_out(std::vector<token> tokens){
    this->ok = true;
    this->tokens = tokens;
    this->err = nullptr;
}

lexer_out::lexer_out(error* e){
    this->ok = false;
    this->tokens = {};
    this->err = e;
}

lexer_out::~lexer_out(){
    if(this->err != nullptr){
        delete this->err;
    }
}

token lexer_out::operator[](int index){
    return this->tokens[index];
}

int lexer_out::size(){
    return this->tokens.size();
}
