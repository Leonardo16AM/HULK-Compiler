#ifndef REGEX_AST_H
#define REGEX_AST_H

#include "../backbone/automaton.h"

class regex_ast {
public:
    virtual std::shared_ptr<automaton> get_automaton() const = 0;
    virtual ~regex_ast() = default;
};

class regex_or : public regex_ast {
public:
    regex_or(std::shared_ptr<regex_ast> left, std::shared_ptr<regex_ast> right);
    std::shared_ptr<automaton> get_automaton() const override;

private:
    std::shared_ptr<regex_ast> left;
    std::shared_ptr<regex_ast> right;
};

class regex_concat : public regex_ast {
public:
    regex_concat(std::shared_ptr<regex_ast> left, std::shared_ptr<regex_ast> right);
    std::shared_ptr<automaton> get_automaton() const override;

private:
    std::shared_ptr<regex_ast> left;
    std::shared_ptr<regex_ast> right;
};

class regex_question : public regex_ast {
public:
    regex_question(std::shared_ptr<regex_ast> body);
    std::shared_ptr<automaton> get_automaton() const override;

private:
    std::shared_ptr<regex_ast> body;
};

class regex_many : public regex_ast {
public:
    regex_many(std::shared_ptr<regex_ast> body);
    std::shared_ptr<automaton> get_automaton() const override;

private:
    std::shared_ptr<regex_ast> body;
};

class regex_oneandmany : public regex_ast {
public:
    regex_oneandmany(std::shared_ptr<regex_ast> body);
    std::shared_ptr<automaton> get_automaton() const override;

private:
    std::shared_ptr<regex_ast> body;
};

class regex_char : public regex_ast {
public:
    regex_char(char character);
    std::shared_ptr<automaton> get_automaton() const override;

private:
    char character;
};

class regex_anychar : public regex_ast {
public:
    std::shared_ptr<automaton> get_automaton() const override;
};

class regex_rank : public regex_ast {
public:
    regex_rank(char left, char right);
    std::shared_ptr<automaton> get_automaton() const override;

private:
    char left;
    char right;
};

class regex_not : public regex_ast {
public:
    regex_not(std::shared_ptr<regex_ast> body);
    std::shared_ptr<automaton> get_automaton() const override;

private:
    std::shared_ptr<regex_ast> body;
};

#endif
