#ifndef REGEX_GRAMMAR_H
#define REGEX_GRAMMAR_H

#include <string>
#include <vector>
#include "../backbone/attributed_grammar.h"
#include "../backbone/attributed_rule.h"
#include "../backbone/grammar_token.h"
#include "regex_token.h"
#include "regex_ast.h"



std::vector<char> regex_special_tokens= {'?', '+', '*', '^',
                        '$', '[', ']', '(', ')', '{', '}', '.', '|', '-'};



#endif