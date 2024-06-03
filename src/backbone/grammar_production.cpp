#include "grammar_production.h"

grammar_production::grammar_production(int ind, const grammar_token &head, const std::vector<grammar_token> &body)
    : head(head), body(body), ind(ind) {}

bool grammar_production::operator==(const grammar_production &other) const {
    return toString() == other.toString();
}

std::string grammar_production::toString() const {
    std::string value = head.toString() + " -> ";

    for (const auto &v : body) {
        value += v.toString() + " ";
    }

    return value;
}

std::size_t grammar_production::hash() const {
    return std::hash<int>()(ind);
}
