# Makefile for Notification System

CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -pthread
TARGET = notification_system
SRC = Main.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET)

run: $(TARGET)
	./$(TARGET)

.PHONY: all clean run
