#ifndef ATTRIBUTED_RULE_H
#define ATTRIBUTED_RULE_H

#include <functional>
#include <vector>
#include <unordered_map>
#include <memory>
#include <variant>

template <typename T1, typename T2>
class attributed_rule {
public:
    attributed_rule(
        std::function<T1(const std::vector<T1>&, const std::vector<std::variant<T1, T2>>&)> header_action,
        const std::vector<std::pair<int, std::function<T1(const std::vector<std::variant<T1, T2>>&,
                                                           const std::vector<std::variant<T1, T2>>&)>>>& actions = {})
        : header_action(header_action) {
        for (const auto& [index, action] : actions) {
            this->actions[index] = action;
        }
    }

    std::unordered_map<int, std::function<T1(const std::vector<std::variant<T1, T2>>&, const std::vector<std::variant<T1, T2>>&)>>
        actions;
    std::function<T1(const std::vector<T1>&, const std::vector<std::variant<T1, T2>>&)> header_action;
};

#endif // ATTRIBUTED_RULE_H
