#ifndef LEXER_OUT_H
#define LEXER_OUT_H

#include <vector>
#include "token.h"
#include "error.h"

class lexer_out{
    public:
    bool ok;
    std::vector<token> tokens;
    error* err;

    lexer_out();
    lexer_out(std::vector<token> tokens);
    lexer_out(error* e);
    ~lexer_out();

    token operator[](int index);
    int size();
};

#endif
