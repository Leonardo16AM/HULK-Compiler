#include "automaton.h"
#include <memory>
#include <vector>

state::state(int ind, bool is_final) 
    : ind(ind), is_final(is_final), complement_state(nullptr) {}


void state::add_transition(char symbol, std::shared_ptr<state> state) {
    transitions[symbol] = state;
}

void state::add_eof_transition(std::shared_ptr<state> state) {
    eof_transitions.insert(state);
}

std::shared_ptr<state> state::goto_symbol(char symbol) {
    if (transitions.find(symbol) != transitions.end()) {
        return transitions[symbol];
    }
    return complement_state;
}

std::vector<std::shared_ptr<state>> state::goto_eof() {
    return std::vector<std::shared_ptr<state>>(eof_transitions.begin(), eof_transitions.end());
}

nlohmann::json state::to_json() const {
    nlohmann::json result;
    for (const auto& transition : transitions) {
        result[std::string(1, transition.first)].push_back(transition.second->ind);
    }
    for (const auto& eof_state : eof_transitions) {
        result["eof"].push_back(eof_state->ind);
    }
    if (complement_state) {
        result["default"] = complement_state->ind;
    }
    result["is_final"] = is_final;
    return result;
}

bool state::operator==(const state& other) const {
    return ind == other.ind;
}

bool state::operator!=(const state& other) const {
    return !(*this == other);
}

bool state::operator<(const state& other) const {
    return ind < other.ind;
}

automaton::automaton(bool copy) {
    if (!copy) {
        initial_state = std::make_shared<state>(0);
        states.push_back(initial_state);
    }
}

void automaton::add_transition(std::shared_ptr<state> from_state, char symbol, std::shared_ptr<state> to_state) {
    from_state->add_transition(symbol, to_state);
}

void automaton::add_eof_transition(std::shared_ptr<state> from_state, std::shared_ptr<state> to_state) {
    from_state->add_eof_transition(to_state);
}

void automaton::add_final_state(std::shared_ptr<state> state) {
    state->is_final = true;
}

void automaton::add_complement(std::shared_ptr<state> from_state, std::shared_ptr<state> to_state) {
    from_state->complement_state = to_state;
}

std::shared_ptr<state> automaton::get_new_state(std::shared_ptr<state> st) {
    auto new_state = st ? st : std::make_shared<state>(states.size());
    new_state->ind = states.size();
    states.push_back(new_state);
    return new_state;
}

std::vector<std::shared_ptr<state>> automaton::final_states() const {
    std::vector<std::shared_ptr<state>> final_states;
    for (const auto& state : states) {
        if (state->is_final) {
            final_states.push_back(state);
        }
    }
    return final_states;
}

bool automaton::match(const std::string& str) const {
    std::unordered_set<std::pair<int, int>> visited;
    return match(initial_state, str, 0, visited);
}

bool automaton::match(const std::shared_ptr<state>& state, const std::string& str, int index, std::unordered_set<std::pair<int, int>>& visited) const {
    if (visited.find({state->ind, index}) != visited.end()) {
        return false;
    }
    visited.insert({state->ind, index});
    if (index == (int)str.size()) {
        return state->is_final;
    }
    for (const auto& eof_state : state->eof_transitions) {
        if (match(eof_state, str, index, visited)) {
            return true;
        }
    }
    auto goto_state = state->goto_symbol(str[index]);
    if (goto_state) {
        return match(goto_state, str, index + 1, visited);
    }
    return false;
}

std::shared_ptr<automaton> automaton::join(const std::shared_ptr<automaton>& automaton) {
    auto copy_automaton = automaton->copy();
    add_eof_transition(initial_state, copy_automaton->initial_state);
    for (const auto& state : copy_automaton->states) {
        get_new_state(state);
    }
    return shared_from_this();
}

std::shared_ptr<automaton> automaton::concat(const std::shared_ptr<automaton>& automaton) {
    auto copy_automaton = automaton->copy();
    for (const auto& state : final_states()) {
        add_eof_transition(state, copy_automaton->initial_state);
        state->is_final = false;
    }
    for (const auto& state : copy_automaton->states) {
        get_new_state(state);
    }
    return shared_from_this();
}

std::shared_ptr<automaton> automaton::many() {
    for (const auto& state : final_states()) {
        add_eof_transition(state, initial_state);
    }
    initial_state->is_final = true;
    return shared_from_this();
}

std::shared_ptr<automaton> automaton::copy() const {
    auto new_automaton = std::make_shared<automaton>(true);
    for (size_t i = 0; i < states.size(); ++i) {
        new_automaton->get_new_state();
    }
    new_automaton->initial_state = new_automaton->states[initial_state->ind];
    for (const auto& state : states) {
        for (const auto& eof_state : state->eof_transitions) {
            new_automaton->add_eof_transition(new_automaton->states[state->ind], new_automaton->states[eof_state->ind]);
        }
        for (const auto& transition : state->transitions) {
            new_automaton->add_transition(new_automaton->states[state->ind], transition.first, new_automaton->states[transition.second->ind]);
        }
        new_automaton->states[state->ind]->is_final = state->is_final;
        new_automaton->states[state->ind]->complement_state = state->complement_state ? new_automaton->states[state->complement_state->ind] : nullptr;
    }
    return new_automaton;
}

std::shared_ptr<automaton> automaton::to_dfa() {
    auto new_automaton = std::make_shared<automaton>();
    std::vector<std::pair<std::shared_ptr<state>, std::unordered_set<std::shared_ptr<state>>>> new_nodes;
    auto initial_set = std::unordered_set<std::shared_ptr<state>>{initial_state};
    goto_eof(initial_set);
    new_nodes.emplace_back(new_automaton->initial_state, initial_set);
    new_automaton->initial_state->is_final = std::any_of(initial_set.begin(), initial_set.end(), [](const auto& state) { return state->is_final; });
    std::queue<std::pair<std::shared_ptr<state>, std::unordered_set<std::shared_ptr<state>>>> q;
    q.push(new_nodes[0]);
    while (!q.empty()) {
        auto [node, states] = q.front();
        q.pop();
        std::unordered_set<char> symbols;
        for (const auto& state : states) {
            for (const auto& transition : state->transitions) {
                symbols.insert(transition.first);
            }
        }
        for (char symbol : symbols) {
            auto goto_set = goto_symbol(states, symbol);
            next_goto(goto_set, new_automaton, node, new_nodes, q, symbol);
        }
        auto goto_set = goto_complement(states);
        next_goto(goto_set, new_automaton, node, new_nodes, q);
    }
    return new_automaton;
}

void automaton::load(const std::string& name) {
    std::ifstream ifs("cache/" + name + "_automaton.json");
    nlohmann::json cache;
    ifs >> cache;
    from_json(cache);
}

void automaton::build(const std::string& name) {
    nlohmann::json cache = to_json();
    std::ofstream ofs("cache/" + name + "_automaton.json");
    ofs << cache;
}

nlohmann::json automaton::to_json() const {
    nlohmann::json result;
    for (const auto& state : states) {
        result.push_back(state->to_json());
    }
    return result;
}

void automaton::from_json(const nlohmann::json& json_dict) {
    states.clear();
    for (size_t i = 0; i < json_dict.size(); ++i) {
        get_new_state();
    }
    for (size_t i = 0; i < json_dict.size(); ++i) {
        const auto& state_json = json_dict[i];
        for (const auto& [key, value] : state_json.items()) {
            if (key == "eof") {
                for (int ind : value) {
                    states[i]->add_eof_transition(states[ind]);
                }
            } else if (key == "default") {
                states[i]->complement_state = states[value.get<int>()];
            } else if (key == "is_final") {
                states[i]->is_final = value.get<bool>();
            } else {
                for (int ind : value) {
                    states[i]->add_transition(key[0], states[ind]);
                }
            }
        }
    }
    initial_state = states[0];
}

std::shared_ptr<automaton> pattern_to_automaton(const std::string& pattern) {
    auto autom = std::make_shared<automaton>();
    auto state = autom->initial_state;
    for (char symbol : pattern) {
        auto new_state = autom->get_new_state();
        autom->add_transition(state, symbol, new_state);
        state = new_state;
    }
    autom->add_final_state(state);
    return autom;
}

std::unordered_set<std::shared_ptr<state>> automaton::goto_complement(const std::unordered_set<std::shared_ptr<state>>& states) const {
    std::unordered_set<std::shared_ptr<state>> goto_set;
    for (const auto& state : states) {
        if (state->complement_state) {
            goto_set.insert(state->complement_state);
        }
    }
    goto_eof(goto_set);
    return goto_set;
}

void automaton::goto_eof(std::unordered_set<std::shared_ptr<state>>& states) const {
    bool change = true;
    while (change) {
        change = false;
        std::unordered_set<std::shared_ptr<state>> aux;
        for (const auto& state : states) {
            for (const auto& eof_state : state->goto_eof()) {
                if (states.find(eof_state) == states.end()) {
                    aux.insert(eof_state);
                }
            }
        }
        for (const auto& state : aux) {
            change = true;
            states.insert(state);
        }
    }
}

std::unordered_set<std::shared_ptr<state>> automaton::goto_symbol(const std::unordered_set<std::shared_ptr<state>>& states, char symbol) const {
    std::unordered_set<std::shared_ptr<state>> goto_set;
    for (const auto& state : states) {
        auto symbol_state = state->goto_symbol(symbol);
        if (symbol_state) {
            goto_set.insert(symbol_state);
        }
    }
    goto_eof(goto_set);
    return goto_set;
}

void automaton::next_goto(std::unordered_set<std::shared_ptr<state>>& goto_set, std::shared_ptr<automaton>& new_automaton, const std::shared_ptr<state>& node, std::vector<std::pair<std::shared_ptr<state>, std::unordered_set<std::shared_ptr<state>>>>& new_nodes, std::queue<std::pair<std::shared_ptr<state>, std::unordered_set<std::shared_ptr<state>>>>& q, char symbol) const {
    if (goto_set.empty()) return;

    auto new_node = get_node(new_nodes, goto_set);
    if (!new_node) {
        new_node = new_automaton->get_new_state();
        if (std::any_of(goto_set.begin(), goto_set.end(), [](const auto& state) { return state->is_final; })) {
            new_automaton->add_final_state(new_node);
        }
        new_nodes.emplace_back(new_node, goto_set);
        q.emplace(new_node, goto_set);
    }

    if (symbol != '\0') {
        new_automaton->add_transition(node, symbol, new_node);
    } else {
        new_automaton->add_complement(node, new_node);
    }
}

std::shared_ptr<state> automaton::get_node(const std::vector<std::pair<std::shared_ptr<state>, std::unordered_set<std::shared_ptr<state>>>>& nodes, const std::unordered_set<std::shared_ptr<state>>& states) const {
    for (const auto& [node, node_states] : nodes) {
        if (states == node_states) {
            return node;
        }
    }
    return nullptr;
}
