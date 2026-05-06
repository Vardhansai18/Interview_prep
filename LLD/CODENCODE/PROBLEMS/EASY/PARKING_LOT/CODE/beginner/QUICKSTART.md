# 🎯 Quick Start Guide

## Prerequisites
- C++ compiler with C++11 support (g++, clang++)
- Basic understanding of SOLID principles
- Terminal/command line access

## Running the Demo

### Option 1: Using the Run Script (Easiest)
```bash
cd /root/projects/interview_prep/LLD/CODENCODE/PROBLEMS/EASY/PARKING_LOT/CODE/beginner
chmod +x run.sh
./run.sh
```

### Option 2: Manual Compilation
```bash
# Navigate to beginner folder
cd /root/projects/interview_prep/LLD/CODENCODE/PROBLEMS/EASY/PARKING_LOT/CODE/beginner

# Compile
g++ -std=c++11 -o parking_lot_demo ParkingLotDemo.cpp

# Run
./parking_lot_demo
```

## What You'll See

The demo will show you:
1. ✅ Parking lot initialization (2 floors, multiple spots)
2. ✅ Parking different vehicle types (Bike, Car, Truck)
3. ✅ Handling "parking lot full" scenario
4. ✅ Unparking and fee calculation
5. ✅ Error handling (invalid tickets)
6. ✅ Real-time status display

## Expected Output

```
╔══════════════════════════════════════════════════════════╗
║     PARKING LOT SYSTEM - BEGINNER FRIENDLY DEMO          ║
║                                                          ║
║  Demonstrating SOLID Principles in Action               ║
╚══════════════════════════════════════════════════════════╝

============================================================
  STEP 1: Initialize Parking Lot Structure
============================================================

Creating pricing strategy...
Creating parking lot service...
...
```

## Learning Path

1. **First Time**: Just run and observe the output
2. **Second Time**: Read the code comments in each file
3. **Third Time**: Modify pricing rates and see the impact
4. **Fourth Time**: Add a new vehicle type (e.g., Van)
5. **Advanced**: Move to multithreading (see MULTITHREADING_GUIDE.md)

## Common Issues & Solutions

### Issue: "Permission denied" when running run.sh
```bash
chmod +x run.sh
```

### Issue: "g++ command not found"
```bash
# Ubuntu/Debian
sudo apt-get install g++

# macOS
xcode-select --install

# Check version
g++ --version
```

### Issue: Compilation errors
- Ensure you're using C++11 or later
- Check that all header files are in correct locations
- Verify file paths match the structure

## File Structure Overview

```
beginner/
├── ParkingLotDemo.cpp          # Main demo application (START HERE)
├── run.sh                       # Quick run script
├── README.md                    # Full documentation
├── QUICKSTART.md               # This file
├── src/
│   ├── models/                  # Domain objects
│   │   ├── VehicleType.h       # Enum for vehicle types
│   │   ├── Vehicle.h           # Base vehicle class
│   │   ├── Car.h, Bike.h, Truck.h
│   │   ├── ParkingSpot.h       # Single parking space
│   │   ├── ParkingFloor.h      # Floor with multiple spots
│   │   └── Ticket.h            # Parking receipt
│   ├── strategies/              # Pricing algorithms
│   │   ├── PricingStrategy.h   # Interface (Strategy Pattern)
│   │   └── SimplePricingStrategy.h
│   └── services/                # Business logic
│       └── ParkingLotService.h # Main orchestrator
```

## Next Steps

After running the demo successfully:
1. Read [README.md](README.md) for detailed explanation
2. Study [SOLID_CHEATSHEET.md](SOLID_CHEATSHEET.md) for principles
3. Try modifying the code (start small!)
4. Read [MULTITHREADING_GUIDE.md](MULTITHREADING_GUIDE.md) for advanced topics

## Interview Tips

When discussing this system in interviews:
1. Start with high-level architecture
2. Explain SOLID principles applied
3. Discuss trade-offs (e.g., linear search vs optimized)
4. Show how to extend (new vehicle types, pricing strategies)
5. Mention thread-safety considerations for production

## Need Help?

- Check comments in source code (extensively documented)
- Review README.md for detailed flows
- See SOLID_CHEATSHEET.md for principle explanations
- Try the demo multiple times to understand flow

Happy Learning! 🚀
