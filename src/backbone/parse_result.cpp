#include "parse_result.h"
#include <algorithm>


parse_result::parse_result(const std::vector<grammar_production> &derivations, int error)
    : ok(error == -1), error(error), tree(ok ? build_tree(derivations) : nullptr) {}

std::shared_ptr<derivation_tree> parse_result::build_tree(const std::vector<grammar_production> &derivations) {
    auto root = std::make_shared<derivation_tree>(derivations[0].head);
    build_tree_node(root, derivations, 0);
    return root;
}

int parse_result::build_tree_node(std::shared_ptr<derivation_tree> node, const std::vector<grammar_production> &derivations, int index) {
    node->production_ind = derivations[index].ind;

    auto tokens = derivations[index].body;
    std::reverse(tokens.begin(), tokens.end());

    for (const auto &token : tokens) {
        if (token.is_terminal) {
            node->add_child(std::make_shared<derivation_tree>(token, node));
        } else {
            auto child = std::make_shared<derivation_tree>(token, node);
            node->add_child(child);
            index = build_tree_node(child, derivations, index + 1);
        }
    }

    std::reverse(node->children.begin(), node->children.end());

    return index;
}
