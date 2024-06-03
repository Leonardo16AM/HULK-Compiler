#ifndef DERIVATION_TREE_H
#define DERIVATION_TREE_H

#include "grammar_token.h"
#include <vector>
#include <memory>

class derivation_tree {
public:
    derivation_tree(const grammar_token &token, std::shared_ptr<derivation_tree> father = nullptr);

    void add_child(std::shared_ptr<derivation_tree> child);
    void set_father(std::shared_ptr<derivation_tree> father);

    grammar_token token;
    std::vector<std::shared_ptr<derivation_tree>> children;
    std::shared_ptr<derivation_tree> father;
    int production_ind;
};

#endif // DERIVATION_TREE_H
