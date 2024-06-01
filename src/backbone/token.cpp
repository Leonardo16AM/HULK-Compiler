#include "token.h"

token::token(){
    this->value = "";
    this->row = 0;
    this->col = 0;
    this->type = "";
}

token::token(std::string val, int r, int c, std::string typ){
    this->value = val;
    this->row = r;
    this->col = c;
    this->type = typ;
}

bool token::operator==(const token& other){
    return this->type == other.type;
}

bool token::operator!=(const token& other){
    return this->type != other.type;
}
