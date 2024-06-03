#include "lexer_out.h"

lexer_out::lexer_out(){
    this->ok = true;
    this->lexer_tokens = {};
    this->err = nullptr;
}

lexer_out::lexer_out(std::vector<lexer_token> lexer_tokens){
    this->ok = true;
    this->lexer_tokens = lexer_tokens;
    this->err = nullptr;
}

lexer_out::lexer_out(error* e){
    this->ok = false;
    this->lexer_tokens = {};
    this->err = e;
}

lexer_out::~lexer_out(){
    if(this->err != nullptr){
        delete this->err;
    }
}

lexer_token lexer_out::operator[](int index){
    return this->lexer_tokens[index];
}

int lexer_out::size(){
    return this->lexer_tokens.size();
}
