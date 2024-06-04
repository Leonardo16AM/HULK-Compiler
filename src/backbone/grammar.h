#ifndef GRAMMAR_H
#define GRAMMAR_H

#include "grammar_production.h"
#include <vector>
#include <set>
#include <unordered_map>
#include <string>

class grammar {
public:
    grammar();
    grammar_production get_production(int ind) const;
    std::set<grammar_token>::iterator get_tokens();
    grammar_token get_token(const std::string &value) const;
    void add_main(const std::string &non_terminal);
    void add_production(const std::string &non_terminal, const std::vector<std::string> &sentences);
    void calculate_first();
    std::set<grammar_token> calculate_sentence_first(const std::vector<grammar_token> &tokens) const;
    void calculate_follow();

private:
    std::vector<grammar_production> productions;
    std::set<grammar_token> terminals;
    std::set<grammar_token> non_terminals;
    std::unordered_map<grammar_token, std::set<grammar_token>> firsts;
    std::unordered_map<grammar_token, std::set<grammar_token>> follows;
    grammar_token main;
};

#endif // GRAMMAR_H
