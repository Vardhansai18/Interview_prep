#!/bin/bash

# Build script for Parking Lot System
# This script compiles the C++ parking lot system and creates the executable

echo "======================================"
echo "Building Parking Lot System..."
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if g++ is installed
if ! command -v g++ &> /dev/null; then
    echo -e "${RED}Error: g++ compiler not found!${NC}"
    echo "Please install g++ first:"
    echo "  sudo apt-get install build-essential g++"
    exit 1
fi

# Check C++ version support
g++ --version | head -1

echo ""
echo "Compiling source files..."

# Compile all source files
g++ -std=c++17 -pthread -Wall -Wextra -I. \
    main.cpp \
    ParkingLotApplication.cpp \
    domain/vehicle/Vehicle.cpp \
    domain/vehicle/Car.cpp \
    domain/vehicle/Bike.cpp \
    domain/vehicle/Truck.cpp \
    domain/parking/ParkingSpot.cpp \
    domain/parking/ParkingFloor.cpp \
    domain/ticket/Ticket.cpp \
    strategy/HourlyPricingStrategy.cpp \
    services/ParkingLotService.cpp \
    exception/ParkingException.cpp \
    -o parking_lot_demo

# Check if compilation was successful
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Build successful!${NC}"
    echo ""
    echo "Executable created: ./parking_lot_demo"
    echo ""
    echo "To run the demo, execute:"
    echo "  ./parking_lot_demo"
    echo ""
    echo "Or run with this script:"
    echo "  ./build.sh run"
    echo ""
    
    # If 'run' argument is provided, execute the demo
    if [ "$1" == "run" ]; then
        echo "======================================"
        echo "Running Demo..."
        echo "======================================"
        echo ""
        ./parking_lot_demo
    fi
else
    echo -e "${RED}✗ Build failed!${NC}"
    echo "Please check the error messages above."
    exit 1
fi
