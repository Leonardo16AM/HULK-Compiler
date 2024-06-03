#include "grammar_production.h"

grammar_production::grammar_production(int ind, const grammar_token &head, const std::vector<grammar_token> &body)
    : head(head), body(body), ind(ind) {}

bool grammar_production::operator==(const grammar_production &other) const {
    return to_string() == other.to_string();
}

std::string grammar_production::to_string() const {
    std::string value = head.to_string() + " -> ";

    for (const auto &v : body) {
        value += v.to_string() + " ";
    }

    return value;
}

std::size_t grammar_production::hash() const {
    return std::hash<int>()(ind);
}
