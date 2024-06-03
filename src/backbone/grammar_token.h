#ifndef GRAMMARTOKEN_H
#define GRAMMARTOKEN_H

#include <string>

class grammar_token {
public:
    grammar_token();
    grammar_token(const std::string &value, bool is_terminal = false, bool is_main = false);
    bool operator==(const grammar_token &other) const;
    std::size_t hash() const;
    std::string toString() const;

    std::string value;
    bool is_terminal;
    bool is_main;
};

namespace std {
    template <>
    struct hash<grammar_token> {
        std::size_t operator()(const grammar_token &token) const {
            return token.hash();
        }   
    };
}

class EOFToken : public grammar_token {
public:
    EOFToken();
};

#endif 
