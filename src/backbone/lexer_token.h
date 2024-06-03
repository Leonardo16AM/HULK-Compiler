#ifndef LEXER_TOKEN_H
#define LEXER_TOKEN_H

#include <iostream>
#include <string>

class lexer_token{
public:
    std::string value;
    int row;
    int col;
    std::string type;
    
    lexer_token();
    lexer_token(std::string val, int r, int c, std::string typ);
    bool operator==(const lexer_token& other);
    bool operator!=(const lexer_token& other);
};

#endif
