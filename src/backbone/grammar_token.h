#ifndef GRAMMAR_TOKEN_H
#define GRAMMAR_TOKEN_H

#include <string>
#include <functional>
#include <variant>
#include <optional>

class grammar_token {
public:
    grammar_token();
    grammar_token(const std::string& value, bool is_terminal = false, bool is_main = false);
    bool operator==(const grammar_token& other) const;
    std::size_t hash() const;
    std::string to_string() const;

    std::string value;
    bool is_terminal;
    bool is_main;
};

namespace std {
    template <>
    struct hash<grammar_token> {
        std::size_t operator()(const grammar_token& token) const {
            return token.hash();
        }
    };
}

class EOF_token : public grammar_token {
public:
    EOF_token();
};

#endif // GRAMMAR_TOKEN_H
