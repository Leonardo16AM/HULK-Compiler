#include "grammar.h"
#include <stdexcept>

grammar::grammar(){
    terminals.insert(EOF_token());
}

grammar_production grammar::get_production(int ind) const {
    return productions[ind];
}

std::set<grammar_token>::iterator grammar::get_tokens() {
    return non_terminals.begin();
}

grammar_token grammar::get_token(const std::string &value) const {
    for (const auto &t : non_terminals) {
        if (t.value == value) {
            return t;
        }
    }
    for (const auto &t : terminals) {
        if (t.value == value) {
            return t;
        }
    }
    throw std::runtime_error("Token not found");
}

void grammar::add_main(const std::string &non_terminal) {
    main = grammar_token(non_terminal);
    main.is_main = true;
    non_terminals.insert(main);
}

void grammar::add_production(const std::string &non_terminal, const std::vector<std::string> &sentences) {
    auto get = [this](const std::string &t) {
        grammar_token token(t, islower(t[0]));
        if (token.is_terminal) {
            terminals.insert(token);
        } else {
            non_terminals.insert(token);
        }
        if (token == main) {
            token = main;
        }
        return token;
    };

    if (!isupper(non_terminal[0])) {
        throw std::invalid_argument("Non terminal must be in upper case");
    }

    grammar_token head = get(non_terminal);

    for (const auto &sentence : sentences) {
        std::vector<grammar_token> body;
        size_t start = 0;
        size_t end = sentence.find(' ');

        while (end != std::string::npos) {
            std::string token = sentence.substr(start, end - start);
            if (!token.empty() && token != "EOF") {
                body.push_back(get(token));
            }
            start = end + 1;
            end = sentence.find(' ', start);
        }

        productions.emplace_back(productions.size(), head, body);
    }
}

void grammar::calculate_first() {
    for (const auto &terminal : terminals) {
        firsts[terminal] = {terminal};
    }
    for (const auto &non_terminal : non_terminals) {
        firsts[non_terminal] = {};
    }

    bool changed = true;
    while (changed) {
        changed = false;
        for (const auto &production : productions) {
            grammar_token head = production.head;
            const auto &body = production.body;

            bool all_epsilon = true;
            for (const auto &token : body) {
                for (const auto &first : firsts[token]) {
                    if (firsts[head].insert(first).second) {
                        changed = true;
                    }
                }
                if (firsts[token].find(EOF_token()) == firsts[token].end()) {
                    all_epsilon = false;
                    break;
                }
            }
            if (all_epsilon) {
                if (firsts[head].insert(EOF_token()).second) {
                    changed = true;
                }
            }
        }
    }
}

std::set<grammar_token> grammar::calculate_sentence_first(const std::vector<grammar_token> &tokens) const {
    std::set<grammar_token> result;
    bool all_epsilon = true;

    for (const auto &token : tokens) {
        for (const auto &first : firsts.at(token)) {
            result.insert(first);
        }
        if (firsts.at(token).find(EOF_token()) == firsts.at(token).end()) {
            all_epsilon = false;
            break;
        }
    }

    if (all_epsilon) {
        result.insert(EOF_token());
    }

    return result;
}

void grammar::calculate_follow() {
    calculate_first();

    for (const auto &non_terminal : non_terminals) {
        follows[non_terminal] = {};
    }

    follows[*non_terminals.begin()].insert(EOF_token());

    bool changed = true;
    while (changed) {
        changed = false;
        for (const auto &production : productions) {
            grammar_token head = production.head;
            const auto &body = production.body;

            for (size_t i = 0; i < body.size(); ++i) {
                const auto &token = body[i];
                if (token.is_terminal) {
                    continue;
                }

                auto firsts = calculate_sentence_first({body.begin() + i + 1, body.end()});
                for (const auto &first : firsts) {
                    if (first != EOF_token() && follows[token].insert(first).second) {
                        changed = true;
                    }
                }

                if (firsts.find(EOF_token()) != firsts.end() || i == body.size() - 1) {
                    for (const auto &follow : follows[head]) {
                        if (follows[token].insert(follow).second) {
                            changed = true;
                        }
                    }
                }
            }
        }
    }
}
