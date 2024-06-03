#include "attributed_grammar.h"
#include <algorithm>

template <typename T1, typename T2>
attributed_grammar<T1, T2>::attributed_grammar() : grammar() {}

template <typename T1, typename T2>
void attributed_grammar<T1, T2>::add_attributed_production(const std::string& non_terminal, const std::vector<std::string>& sentences, const std::vector<attributed_rule<T1, T2>>& rules) {
    add_production(non_terminal, sentences);
    this->rules.insert(this->rules.end(), rules.begin(), rules.end());
}

template <typename T1, typename T2>
T1 attributed_grammar<T1, T2>::evaluate(std::shared_ptr<derivation_tree> derivation_tree, std::vector<T2> tokens) {
    std::reverse(tokens.begin(), tokens.end());
    return evaluate_node(derivation_tree, tokens);
}

template <typename T1, typename T2>
T1 attributed_grammar<T1, T2>::evaluate_node(std::shared_ptr<derivation_tree> node, std::vector<T2>& tokens, std::optional<T1> inherit) {
    auto get_terminal = [&tokens]() -> grammar_token {
        auto t = tokens.back();
        tokens.pop_back();
        return t;
    };

    std::vector<std::optional<T1>> h(1 + node->children.size(), std::nullopt);
    h[0] = inherit;
    std::vector<std::optional<std::variant<T1, T2>>> s(1 + node->children.size(), std::nullopt);

    auto rule = rules[node->production_ind];

    for (size_t i = 0; i < node->children.size(); ++i) {
        auto& n = node->children[i];
        if (n->token.is_terminal) {
            s[i + 1] = get_terminal();
        } else {
            if (rule.actions.find(i) != rule.actions.end()) {
                h[i + 1] = rule.actions[i](h, s);
            }
            s[i + 1] = evaluate_node(n, tokens, h[i + 1]);
        }
    }

    return rule.header_action(h, s);
}
