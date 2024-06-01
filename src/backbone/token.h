#ifndef TOKEN_H
#define TOKEN_H

#include <iostream>
#include <string>

class token{
public:
    std::string value;
    int row;
    int col;
    std::string type;
    
    token();
    token(std::string val, int r, int c, std::string typ);
    bool operator==(const token& other);
    bool operator!=(const token& other);
};

#endif
