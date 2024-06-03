#include "grammar_token.h"


grammar_token::grammar_token()
    : value("_"), is_terminal(false), is_main(false) {}

grammar_token::grammar_token(const std::string& value, bool is_terminal, bool is_main)
    : value(value), is_terminal(is_terminal && !is_main), is_main(is_main) {}

bool grammar_token::operator==(const grammar_token& other) const {
    return value == other.value;
}

bool grammar_token::operator<(const grammar_token& other) const {
    return value < other.value;
}

bool grammar_token::operator!=(const grammar_token& other) const {
    return value != other.value;
}

std::size_t grammar_token::hash() const {
    return std::hash<std::string>()(value);
}

std::string grammar_token::to_string() const {
    return value;
}

EOF_token::EOF_token() : grammar_token("EOF", true) {}
