# Parking Lot System - C++ Implementation

A complete Low-Level Design implementation of a Parking Lot System in C++17, converted from the original Java implementation.

## 📋 Features

- **Multi-floor Support**: Handles multiple parking floors
- **Multiple Vehicle Types**: Supports Car, Bike, and Truck
- **Thread-Safe Operations**: Uses mutex locks for concurrent access
- **Flexible Pricing Strategy**: Implements Strategy pattern for pricing
- **Clean Architecture**: Follows SOLID principles and OOP best practices
- **Smart Pointers**: Uses modern C++ with shared_ptr for memory management

## 🏗️ Architecture

The system follows the **CERID** design approach:
- **C**larify - Requirements gathering
- **E**ntities - Core domain objects
- **R**esponsibilities - Single Responsibility Principle
- **I**nteractions - Component relationships
- **D**urability - Extensibility

### Project Structure

```
CODE/
├── domain/
│   ├── vehicle/
│   │   ├── VehicleType.h
│   │   ├── Vehicle.h/cpp
│   │   ├── Car.h/cpp
│   │   ├── Bike.h/cpp
│   │   └── Truck.h/cpp
│   ├── parking/
│   │   ├── ParkingSpot.h/cpp
│   │   └── ParkingFloor.h/cpp
│   └── ticket/
│       └── Ticket.h/cpp
├── strategy/
│   ├── PricingStrategy.h
│   └── HourlyPricingStrategy.h/cpp
├── services/
│   └── ParkingLotService.h/cpp
├── exception/
│   └── ParkingException.h/cpp
├── ParkingLotApplication.h/cpp
├── main.cpp
├── CMakeLists.txt
└── README.md
```

## 🔧 Requirements

- **C++ Compiler**: GCC 7+ or Clang 5+ (C++17 support required)
- **CMake**: Version 3.10 or higher
- **pthread**: POSIX threads library (usually pre-installed on Linux)

## 🚀 Building the Project

### Using CMake (Recommended)

```bash
# Navigate to the CODE directory
cd CODE

# Create build directory
mkdir build && cd build

# Generate build files
cmake ..

# Build the project
make

# Run the demo application
./parking_lot_demo
```

### Manual Compilation (Alternative)

```bash
# Compile all source files
g++ -std=c++17 -pthread -Wall -Wextra \
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

# Run the executable
./parking_lot_demo
```

## 💻 Usage Example

```cpp
// Create parking spots
auto carSpot = std::make_shared<ParkingSpot>("G-01", VehicleType::CAR);
auto bikeSpot = std::make_shared<ParkingSpot>("G-02", VehicleType::BIKE);

// Create parking floors
auto floor = std::make_shared<ParkingFloor>("Ground", 
    std::vector<std::shared_ptr<ParkingSpot>>{carSpot, bikeSpot});

// Create pricing strategy
auto strategy = std::make_shared<HourlyPricingStrategy>(20.0);

// Create service and application
auto service = std::make_shared<ParkingLotService>(
    std::vector<std::shared_ptr<ParkingFloor>>{floor}, strategy);
ParkingLotApplication app(service);

// Park a vehicle
auto car = std::make_shared<Car>("ABC123");
auto ticket = app.parkVehicle(car);

// Unpark and get charges
double charges = app.unparkVehicle(ticket);
```

## 🎯 Design Patterns Used

1. **Strategy Pattern**: For flexible pricing strategies
2. **Factory Pattern**: Vehicle creation
3. **Singleton-like Service**: Centralized parking lot service
4. **Repository Pattern**: Ticket and spot management

## 🔒 Thread Safety

The implementation ensures thread safety through:
- `std::mutex` in `ParkingSpot` for concurrent parking attempts
- `std::mutex` in `ParkingLotService` for ticket management
- `std::lock_guard` for RAII-based lock management

## 🧪 Testing the Application

Run the demo application to see the system in action:

```bash
./parking_lot_demo
```

Expected output:
```
=== Parking Lot System Demo ===

Parking bike with number: ABC01
Bike parked at spot: 01-S2
Ticket ID: <generated-uuid>

Parking car with number: ABC02
Car parked at spot: 00-S1
Ticket ID: <generated-uuid>

--- Vehicles are parked ---

Unparking bike...
Bike fare: $20

Unparking car...
Car fare: $20

=== Demo completed successfully ===
```

## 📝 Key Differences from Java Implementation

1. **Memory Management**: Uses smart pointers (`shared_ptr`) instead of Java's garbage collection
2. **Threading**: Uses `std::mutex` instead of Java's `synchronized` keyword
3. **Time Handling**: Uses `std::chrono` instead of `LocalDateTime`
4. **Collections**: Uses STL containers (`vector`, `unordered_map`) instead of Java collections
5. **UUID Generation**: Custom implementation instead of Java's `UUID.randomUUID()`
6. **Namespaces**: Uses C++ namespaces instead of Java packages

## 🔄 Extending the System

### Adding New Vehicle Type

1. Create new vehicle class inheriting from `Vehicle`
2. Add new type to `VehicleType` enum
3. No changes needed in core logic (Open-Closed Principle)

### Adding New Pricing Strategy

1. Create new class implementing `PricingStrategy` interface
2. Override `calculatePrice()` method
3. Pass to `ParkingLotService` constructor

## 📚 Learning Resources

For detailed design documentation, see:
- [parking_lot.md](../parking_lot.md) - Complete LLD documentation
- Images in [images/](../images/) folder - UML diagrams and flow charts

## 🤝 Contributing

This is an educational project demonstrating Low-Level Design concepts. Feel free to:
- Add new features
- Improve thread safety
- Add unit tests
- Optimize algorithms

## 📄 License

This is a learning project based on CodeNCode LLD Masterclass.

## 👨‍💻 Author

Converted from Java to C++ as part of interview preparation materials.

---

**Note**: This implementation prioritizes clarity and design patterns over performance optimization, making it ideal for learning and interview preparation.
