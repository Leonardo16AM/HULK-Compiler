#ifndef gRAMMAR_pRODUCTION_H
#define gRAMMAR_pRODUCTION_H

#include "grammar_token.h"
#include <vector>
#include <string>

class grammar_production {
public:
    grammar_production(int ind, const grammar_token &head, const std::vector<grammar_token> &body);
    bool operator==(const grammar_production &other) const;
    bool operator!=(const grammar_production &other) const;
    std::string to_string() const;
    std::size_t hash() const;

    grammar_token head;
    std::vector<grammar_token> body;
    int ind;
};

namespace std {
    template <>
    struct hash<grammar_production> {
        std::size_t operator()(const grammar_production &prod) const {
            return prod.hash();
        }
    };
}

#endif // gRAMMAR_pRODUCTION_H
