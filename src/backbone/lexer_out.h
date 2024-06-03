#ifndef LEXER_OUT_H
#define LEXER_OUT_H

#include <vector>
#include "lexer_token.h"
#include "error.h"

class lexer_out{
    public:
    bool ok;
    std::vector<lexer_token> lexer_tokens;
    error* err;

    lexer_out();
    lexer_out(std::vector<lexer_token> lexer_tokens);
    lexer_out(error* e);
    ~lexer_out();

    lexer_token operator[](int index);
    int size();
};

#endif
