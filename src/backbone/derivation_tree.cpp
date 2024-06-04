#include "derivation_tree.h"

derivation_tree::derivation_tree(const grammar_token &token, std::shared_ptr<derivation_tree> father)
    : token(token), father(father), production_ind(-1) {}

void derivation_tree::add_child(std::shared_ptr<derivation_tree> child) {
    children.push_back(child);
}

void derivation_tree::set_father(std::shared_ptr<derivation_tree> father) {
    this->father = father;
}
