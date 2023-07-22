CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++17

SRC = kill_Down_with_Trojans.cpp
EXECUTABLE = kill_Down_with_Trojans

all: $(EXECUTABLE)

$(EXECUTABLE): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(EXECUTABLE)

clean:
	rm -f $(EXECUTABLE)
