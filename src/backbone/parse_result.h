#ifndef PARSE_RESULT_H
#define PARSE_RESULT_H

#include "grammar_production.h"
#include "derivation_tree.h"
#include <vector>
#include <memory>

class parse_result {
public:
    parse_result(const std::vector<grammar_production> &derivations = {}, int error = -1);

    bool ok;
    int error;
    std::shared_ptr<derivation_tree> tree;

private:
    static std::shared_ptr<derivation_tree> build_tree(const std::vector<grammar_production> &derivations);
    static int build_tree_node(std::shared_ptr<derivation_tree> node, const std::vector<grammar_production> &derivations, int index);
};

#endif // PARSE_RESULT_H
