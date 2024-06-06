# Define el compilador
CXX := g++

# Define los flags de compilación
CXXFLAGS := -Wall -g -std=c++17 -Iinclude -Isrc -Isrc/backbone -Isrc/tests

# Directorio fuente
SRC_DIR := src/backbone

# Archivos fuente adicionales y encontrados recursivamente
SOURCES = src/main.cpp src/regex/regex_ast.cpp src/backbone/automaton.cpp src/tests/automaton_test.cpp src/tests/backbone_test.cpp src/backbone/lexer_token.cpp src/backbone/lexer_out.cpp src/backbone/grammar_token.cpp src/backbone/grammar.cpp src/backbone/grammar_production.cpp src/backbone/derivation_tree.cpp src/backbone/attributed_grammar.cpp src/backbone/parser_out.cpp src/tests/regex_test.cpp

# Archivos objeto
OBJECTS = $(SOURCES:.cpp=.o)

# Nombre del ejecutable
EXECUTABLE = hulk

# Regla principal
all: $(EXECUTABLE)

# Regla para construir el ejecutable
$(EXECUTABLE): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $@ $^

# Regla para compilar los archivos objeto
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Limpiar archivos generados
clean:
	rm -f $(OBJECTS) $(EXECUTABLE)

.PHONY: all clean
