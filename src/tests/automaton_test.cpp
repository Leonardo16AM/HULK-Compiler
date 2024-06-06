#include "../backbone/automaton.h"
#include <memory>
#include <vector>
#include <iostream>

bool automaton_test(){
    std::cout << "Testing automaton" << std::endl;
    state s1(1);
    state s2(2);
    state s3(3);
    state s4(4);
    state s5(5);
    state s6(6);
    state s7(7);
    state s8(8);
    state s9(9);

    s1.add_transition('a', std::make_shared<state>(2));
    s1.add_transition('b', std::make_shared<state>(3));
    s2.add_transition('a', std::make_shared<state>(4));
    s2.add_transition('b', std::make_shared<state>(5));
    s3.add_transition('a', std::make_shared<state>(6));
    s3.add_transition('b', std::make_shared<state>(7));
    s4.add_transition('a', std::make_shared<state>(8));
    s4.add_transition('b', std::make_shared<state>(9));
    s5.add_transition('a', std::make_shared<state>(10));
    s5.add_transition('b', std::make_shared<state>(11));
    s6.add_transition('a', std::make_shared<state>(12));
    s6.add_transition('b', std::make_shared<state>(13));
    s7.add_transition('a', std::make_shared<state>(14));
    s7.add_transition('b', std::make_shared<state>(15));
    s8.add_transition('a', std::make_shared<state>(16));
    s8.add_transition('b', std::make_shared<state>(17));
    s9.add_transition('a', std::make_shared<state>(18));
    s9.add_transition('b', std::make_shared<state>(19));

    s1.add_eof_transition(std::make_shared<state>(20));
    s2.add_eof_transition(std::make_shared<state>(21));
    s3.add_eof_transition(std::make_shared<state>(22));
    s4.add_eof_transition(std::make_shared<state>(23));
    s5.add_eof_transition(std::make_shared<state>(24));
    s6.add_eof_transition(std::make_shared<state>(25));
    s7.add_eof_transition(std::make_shared<state>(26));
    s8.add_eof_transition(std::make_shared<state>(27));
    s9.add_eof_transition(std::make_shared<state>(28));

    automaton a;
    a.add_transition(std::make_shared<state>(1), 'a', std::make_shared<state>(2));
    a.add_transition(std::make_shared<state>(1), 'b', std::make_shared<state>(3));
    a.add_transition(std::make_shared<state>(2), 'a', std::make_shared<state>(4));
    a.add_transition(std::make_shared<state>(2), 'b', std::make_shared<state>(5));
    a.add_transition(std::make_shared<state>(3), 'a', std::make_shared<state>(6));
    a.add_transition(std::make_shared<state>(3), 'b', std::make_shared<state>(7));
    a.add_transition(std::make_shared<state>(4), 'a', std::make_shared<state>(8));
    a.add_transition(std::make_shared<state>(4), 'b', std::make_shared<state>(9));
    a.add_transition(std::make_shared<state>(5), 'a', std::make_shared<state>(10));

    a.add_eof_transition(std::make_shared<state>(1), std::make_shared<state>(20));
    a.add_eof_transition(std::make_shared<state>(2), std::make_shared<state>(21));
    a.add_eof_transition(std::make_shared<state>(3), std::make_shared<state>(22));
    a.add_eof_transition(std::make_shared<state>(4), std::make_shared<state>(23));
    a.add_eof_transition(std::make_shared<state>(5), std::make_shared<state>(24));

    a.add_final_state(std::make_shared<state>(20));
    a.add_final_state(std::make_shared<state>(21));
    a.add_final_state(std::make_shared<state>(22));
    a.add_final_state(std::make_shared<state>(23));
    a.add_final_state(std::make_shared<state>(24));

    a.add_complement(std::make_shared<state>(1), std::make_shared<state>(20));
    a.add_complement(std::make_shared<state>(2), std::make_shared<state>(21));
    a.add_complement(std::make_shared<state>(3), std::make_shared<state>(22));
    a.add_complement(std::make_shared<state>(4), std::make_shared<state>(23));
    a.add_complement(std::make_shared<state>(5), std::make_shared<state>(24));


    return true;
}
