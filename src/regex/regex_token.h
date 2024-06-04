#ifndef REGEX_TOKEN_H
#define REGEX_TOKEN_H
#include <string>

class regex_token{
public:
    std::string value;
    bool is_special;
    int pos;

    regex_token(std::string val, int p, bool is_spec = false) : value(val), pos(p), is_special(is_spec) {}
    
    std::string to_string() const {
        return value;
    }
};

#endif
