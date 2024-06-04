#ifndef REGEX_OUT_H
#define REGEX_OUT_H


#include <string>
#include <vector>
#include "../backbone/error.h"
#include "regex_token.h"

class regex_out{
public:
    std::vector<regex_token> value;
    bool ok;
    error err;

    regex_out(std::vector<regex_token> value = {}, error e=error("")) : value(value), ok(value.size()!=0), err(e) {}
};

#endif