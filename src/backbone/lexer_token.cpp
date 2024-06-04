#include "lexer_token.h"

lexer_token::lexer_token(){
    this->value = "";
    this->row = 0;
    this->col = 0;
    this->type = "";
}

lexer_token::lexer_token(std::string val, int r, int c, std::string typ){
    this->value = val;
    this->row = r;
    this->col = c;
    this->type = typ;
}

bool lexer_token::operator==(const lexer_token& other){
    return this->type == other.type;
}

bool lexer_token::operator!=(const lexer_token& other){
    return this->type != other.type;
}
