#include "regex_ast.h"

regex_or::regex_or(std::shared_ptr<regex_ast> left, std::shared_ptr<regex_ast> right) 
    : left(left), right(right) {}

std::shared_ptr<automaton> regex_or::get_automaton() const {
    return left->get_automaton()->join(right->get_automaton());
}

regex_concat::regex_concat(std::shared_ptr<regex_ast> left, std::shared_ptr<regex_ast> right) 
    : left(left), right(right) {}

std::shared_ptr<automaton> regex_concat::get_automaton() const {
    return left->get_automaton()->concat(right->get_automaton());
}

regex_question::regex_question(std::shared_ptr<regex_ast> body) 
    : body(body) {}

std::shared_ptr<automaton> regex_question::get_automaton() const {
    return pattern_to_automaton("")->join(body->get_automaton());
}

regex_many::regex_many(std::shared_ptr<regex_ast> body) 
    : body(body) {}

std::shared_ptr<automaton> regex_many::get_automaton() const {
    return body->get_automaton()->many();
}

regex_oneandmany::regex_oneandmany(std::shared_ptr<regex_ast> body) 
    : body(body) {}

std::shared_ptr<automaton> regex_oneandmany::get_automaton() const {
    return body->get_automaton()->concat(body->get_automaton()->many());
}

regex_char::regex_char(char character) 
    : character(character) {}

std::shared_ptr<automaton> regex_char::get_automaton() const {
    return pattern_to_automaton(std::string(1, character));
}

std::shared_ptr<automaton> regex_anychar::get_automaton() const {
    auto a = std::make_shared<automaton>();
    auto new_state = a->get_new_state();
    a->add_complement(a->initial_state, new_state);
    a->add_final_state(new_state);
    return a;
}

regex_rank::regex_rank(char left, char right) 
    : left(left), right(right) {}

std::shared_ptr<automaton> regex_rank::get_automaton() const {
    int ind = static_cast<int>(left);
    auto r = std::make_shared<automaton>();

    while (ind <= static_cast<int>(right)) {
        r = r->join(pattern_to_automaton(std::string(1, static_cast<char>(ind))));
        ind++;
    }

    return r;
}

regex_not::regex_not(std::shared_ptr<regex_ast> body) 
    : body(body) {}

std::shared_ptr<automaton> regex_not::get_automaton() const {
    auto dfa = body->get_automaton()->to_dfa();
    auto new_state = dfa->get_new_state();
    dfa->add_final_state(new_state);
    dfa->add_complement(dfa->initial_state, new_state);

    for (auto& s : dfa->states) {
        if (s == new_state) {
            continue;
        }
        if (s->is_final) {
            s->is_final = false;
        }
    }
    return dfa;
}
