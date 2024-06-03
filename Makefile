# Define el compilador
CXX := g++
# Define los flags de compilación
CXXFLAGS := -Wall -g -std=c++17

# Directorio fuente
SRC_DIR := src/backbone

# Archivos fuente adicionales y encontrados recursivamente
SOURCES = src/main.cpp src/tests/backbone_test.cpp src/backbone/lexer_token.cpp src/backbone/lexer_out.cpp src/backbone/grammar_token.cpp src/backbone/grammar.cpp src/backbone/grammar_production.cpp src/backbone/derivation_tree.cpp src/backbone/attributed_rule.cpp src/backbone/attributed_grammar.cpp src/backbone/parse_result.cpp

# Reemplaza la extensión .cpp por .o para obtener los nombres de los objetos
OBJECTS := $(SOURCES:.cpp=.o)

# Nombre del ejecutable final
TARGET := my_program

# Regla principal
all: $(TARGET)

# Regla para compilar el ejecutable
$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $@ $^

# Regla para compilar cada archivo .cpp en un archivo .o
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c -o $@ $<

# Limpiar los archivos compilados
clean:
	rm -f $(OBJECTS) $(TARGET)
