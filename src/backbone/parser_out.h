#ifndef PARSER_OUT_H
#define PARSER_OUT_H

#include "grammar_production.h"
#include "derivation_tree.h"
#include <vector>
#include <memory>

class parser_out {
public:
    parser_out(const std::vector<grammar_production> &derivations = {}, int error = -1);

    bool ok;
    int error;
    std::shared_ptr<derivation_tree> tree;

private:
    static std::shared_ptr<derivation_tree> build_tree(const std::vector<grammar_production> &derivations);
    static int build_tree_node(std::shared_ptr<derivation_tree> node, const std::vector<grammar_production> &derivations, int index);
};

#endif // PARSER_OUT_H
