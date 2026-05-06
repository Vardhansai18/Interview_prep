# Beginner-Friendly Parking Lot System (C++)

## 🎯 Overview
This is a simplified parking lot system designed for beginners who understand SOLID principles. The system demonstrates:
- **Single Responsibility Principle (SRP)**: Each class has one clear purpose
- **Open/Closed Principle (OCP)**: System is open for extension (new vehicle types, pricing strategies)
- **Liskov Substitution Principle (LSP)**: Derived vehicle classes can replace base class
- **Interface Segregation Principle (ISP)**: Focused interfaces without unnecessary methods
- **Dependency Inversion Principle (DIP)**: Depends on abstractions (PricingStrategy interface)

## 📁 Project Structure
```
beginner/
├── src/
│   ├── models/          # Domain models (Vehicle, ParkingSpot, Ticket, etc.)
│   ├── services/        # Business logic (ParkingLotService)
│   └── strategies/      # Pricing strategies (Strategy Pattern)
├── ParkingLotDemo.cpp   # Main demo application
└── README.md           # This file
```

## 🚗 Core Components

### 1. **Models** (Domain Objects)
- `VehicleType`: Enum for vehicle types (BIKE, CAR, TRUCK)
- `Vehicle`: Base class for all vehicles
- `Car`, `Bike`, `Truck`: Specific vehicle implementations
- `ParkingSpot`: Represents a parking space
- `ParkingFloor`: Represents a floor with multiple spots
- `Ticket`: Parking ticket with entry time and spot info

### 2. **Services** (Business Logic)
- `ParkingLotService`: Main service to park/unpark vehicles and calculate fees

### 3. **Strategies** (Pricing)
- `PricingStrategy`: Interface for different pricing algorithms
- `SimplePricingStrategy`: Basic hourly pricing implementation

## 🔄 Core Flows

### Flow 1: Park a Vehicle
```
User → ParkingLotService.parkVehicle(vehicle)
  → Find available spot for vehicle type
  → Mark spot as occupied
  → Create ticket with entry time
  → Return ticket to user
```

### Flow 2: Unpark a Vehicle
```
User → ParkingLotService.unparkVehicle(ticket)
  → Find the parking spot from ticket
  → Calculate duration (exit time - entry time)
  → Use PricingStrategy to calculate fee
  → Mark spot as available
  → Return fee to user
```

## ✅ SOLID Principles Applied

### Single Responsibility
- `Vehicle`: Only represents vehicle data
- `ParkingSpot`: Only manages spot availability
- `ParkingLotService`: Only handles parking operations
- `PricingStrategy`: Only calculates pricing

### Open/Closed
- Add new vehicle types by extending `Vehicle` class
- Add new pricing strategies by implementing `PricingStrategy` interface
- No need to modify existing code

### Liskov Substitution
- Any `Vehicle` subclass (Car, Bike, Truck) can be used wherever `Vehicle` is expected

### Interface Segregation
- `PricingStrategy` interface has only one method: `calculatePrice()`
- Clients only depend on what they need

### Dependency Inversion
- `ParkingLotService` depends on `PricingStrategy` interface, not concrete implementations
- Can switch pricing strategies without changing service code

## 🚀 How to Run

```bash
# Make the script executable
chmod +x run.sh

# Compile and run
./run.sh
```

## 🎓 Next Steps
Once comfortable with this basic implementation, you can:
1. Add thread safety for multithreading (mutex, locks)
2. Add multiple entry/exit gates
3. Implement different parking strategies (nearest spot, level-wise)
4. Add support for reserved parking
5. Implement payment processing

## 📚 Key Concepts for Interviews
- **Encapsulation**: Data hiding in classes
- **Polymorphism**: Vehicle hierarchy, PricingStrategy interface
- **Abstraction**: Hiding complex implementation details
- **Design Patterns**: Strategy Pattern for pricing
