#ifndef ATTRIBUTED_GRAMMAR_H
#define ATTRIBUTED_GRAMMAR_H

#include "attributed_rule.h"
#include "grammar.h"
#include "derivation_tree.h"
#include <vector>
#include <memory>

template <typename T1, typename T2>
class attributed_grammar : public grammar {
public:
    attributed_grammar();
    void add_attributed_production(const std::string& non_terminal, const std::vector<std::string>& sentences, const std::vector<attributed_rule<T1, T2>>& rules);
    T1 evaluate(std::shared_ptr<derivation_tree> derivation_tree, std::vector<T2> tokens);

private:
    T1 evaluate_node(std::shared_ptr<derivation_tree> node, std::vector<T2>& tokens, std::optional<T1> inherit = std::nullopt);

    std::vector<attributed_rule<T1, T2>> rules;
};

#endif // ATTRIBUTED_GRAMMAR_H
