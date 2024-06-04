#ifndef REGEX_OUT_H
#define REGEX_OUT_H


#include <string>
#include <vector>
#include "../backbone/error.h"
#include "regex_token.h"


template<class T>
class regex_out{
public:
    T value;
    bool ok;
    error err;

    regex_out(T val, error e=error("")) : value(val), ok(e.message().size()==0?true:false), err(e) {}
};

#endif