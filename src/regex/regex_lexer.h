#ifndef REGEX_LEXER_H
#define REGEX_LEXER_H

#include <string>
#include <vector>
#include <algorithm>

#include "regex_token.h"
#include "regex_out.h"
#include "regex_grammar.h"
#include "../backbone/error.h"

regex_out<std::vector<regex_token>> regex_lexer(const std::string &text) {
    std::vector<regex_token> result;
    bool scape = false;

    for (size_t i = 0; i < text.size(); i++) {
        if (scape) {
            scape = false;
            continue;
        }
        
        std::string ti=text.substr(i,1);

        if (text[i] == '\\') {
            if (i + 1 == text.size()) {
                return regex_out<std::vector<regex_token>>({},error("Invalid character \\: pos " + std::to_string(i),0, i));
            } else {
                result.push_back(regex_token( ti , (int)i+1,false));
            }

            scape = true;

            continue;
        }

        result.push_back(regex_token(ti, i, std::find(regex_special_tokens.begin(), regex_special_tokens.end(), text[i]) != regex_special_tokens.end()));
    }

    return regex_out<std::vector<regex_token>>(result,error(""));
}
#endif