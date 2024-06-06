#ifndef AUTOMATON_H
#define AUTOMATON_H

#include <string>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <queue>
#include <memory>
#include <fstream>
#include <../ext/json.hpp>



namespace std {
    template <>
    struct hash<std::pair<int, int>> {
        std::size_t operator()(const std::pair<int, int>& p) const {
            return std::hash<int>()(p.first) ^ std::hash<int>()(p.second);
        }
    };
}


class state {
public:
    int ind;
    bool is_final;
    std::unordered_map<char, std::shared_ptr<state>> transitions;
    std::unordered_set<std::shared_ptr<state>> eof_transitions;
    std::shared_ptr<state> complement_state;

    state(int ind, bool is_final = false);

    void add_transition(char symbol, std::shared_ptr<state> state);
    void add_eof_transition(std::shared_ptr<state> state);
    std::shared_ptr<state> goto_symbol(char symbol);
    std::vector<std::shared_ptr<state>> goto_eof();
    nlohmann::json to_json() const;

    bool operator==(const state& other) const;
    bool operator!=(const state& other) const;
    bool operator<(const state& other) const;
};

class automaton : public std::enable_shared_from_this<automaton>{
public:
    std::shared_ptr<state> initial_state;
    std::vector<std::shared_ptr<state>> states;

    automaton(bool copy = false);

    void add_transition(std::shared_ptr<state> from_state, char symbol, std::shared_ptr<state> to_state);
    void add_eof_transition(std::shared_ptr<state> from_state, std::shared_ptr<state> to_state);
    void add_final_state(std::shared_ptr<state> state);
    void add_complement(std::shared_ptr<state> from_state, std::shared_ptr<state> to_state);
    std::shared_ptr<state> get_new_state(std::shared_ptr<state> state = nullptr);

    std::vector<std::shared_ptr<state>> final_states() const;
    bool match(const std::string& str) const;

    std::shared_ptr<automaton> join(const std::shared_ptr<automaton>& automaton);
    std::shared_ptr<automaton> concat(const std::shared_ptr<automaton>& automaton);
    std::shared_ptr<automaton> many();

    std::shared_ptr<automaton> copy() const;
    std::shared_ptr<automaton> to_dfa();

    void load(const std::string& name);
    void build(const std::string& name);
    nlohmann::json to_json() const;
    void from_json(const nlohmann::json& json_dict);



    bool match(const std::shared_ptr<state>& state, const std::string& str, int index, std::unordered_set<std::pair<int, int>>& visited) const;
    void next_goto(std::unordered_set<std::shared_ptr<state>>& goto_set, std::shared_ptr<automaton>& new_automaton, const std::shared_ptr<state>& node, std::vector<std::pair<std::shared_ptr<state>, std::unordered_set<std::shared_ptr<state>>>>& new_nodes, std::queue<std::pair<std::shared_ptr<state>, std::unordered_set<std::shared_ptr<state>>>>& q, char symbol = '\0') const;
    std::shared_ptr<state> get_node(const std::vector<std::pair<std::shared_ptr<state>, std::unordered_set<std::shared_ptr<state>>>>& nodes, const std::unordered_set<std::shared_ptr<state>>& states) const;
    std::unordered_set<std::shared_ptr<state>> goto_complement(const std::unordered_set<std::shared_ptr<state>>& states) const;
    void goto_eof(std::unordered_set<std::shared_ptr<state>>& states) const;
    std::unordered_set<std::shared_ptr<state>> goto_symbol(const std::unordered_set<std::shared_ptr<state>>& states, char symbol) const;
};

std::shared_ptr<automaton> pattern_to_automaton(const std::string& pattern);

#endif