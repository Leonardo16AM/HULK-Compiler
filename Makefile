# Nombre del compilador
CXX = g++

# Opciones de compilación
CXXFLAGS = -Wall -std=c++11 -Iinclude

# Archivos fuente
SOURCES = src/main.cpp src/backbone/token.cpp src/backbone/lexer_out.cpp src/tests/backbone_test.cpp

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
