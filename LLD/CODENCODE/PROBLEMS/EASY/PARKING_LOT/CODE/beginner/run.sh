#!/bin/bash

# Parking Lot System - Build and Run Script
# This script compiles and runs the beginner-friendly parking lot system

echo "=================================="
echo "Parking Lot System - Compile & Run"
echo "=================================="
echo ""

# Compile
echo "📦 Compiling..."
g++ -std=c++11 -o parking_lot_demo ParkingLotDemo.cpp

# Check if compilation was successful
if [ $? -eq 0 ]; then
    echo "✅ Compilation successful!"
    echo ""
    echo "🚀 Running demo..."
    echo ""
    ./parking_lot_demo
else
    echo "❌ Compilation failed!"
    exit 1
fi
