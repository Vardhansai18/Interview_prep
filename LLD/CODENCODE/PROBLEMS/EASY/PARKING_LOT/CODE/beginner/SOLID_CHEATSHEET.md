# 📐 SOLID Principles Cheatsheet

## Quick Reference for Low-Level Design Interviews

This cheatsheet shows how SOLID principles are applied in the Parking Lot System.

---

## S - Single Responsibility Principle (SRP)

**Definition**: A class should have only ONE reason to change.

**Why**: Makes code easier to understand, test, and maintain.

### Examples in Our System:

#### ✅ Good - Following SRP

```cpp
// Vehicle class: Only handles vehicle data
class Vehicle {
    std::string licensePlate;
    VehicleType type;
    // That's it! No parking logic, no pricing logic
};

// ParkingSpot class: Only manages one parking spot
class ParkingSpot {
    bool occupied;
    Vehicle* parkedVehicle;
    void parkVehicle() { }    // Manages spot state
    void unparkVehicle() { }
    // Doesn't calculate fees or manage floors
};

// PricingStrategy: Only calculates pricing
class SimplePricingStrategy {
    double calculatePrice() { }  // One job: pricing
    // Doesn't park vehicles or manage spots
};
```

#### ❌ Bad - Violating SRP

```cpp
// God class doing everything (BAD!)
class ParkingLot {
    void parkVehicle() { }
    void unparkVehicle() { }
    double calculatePrice() { }      // Should be separate!
    void sendEmail() { }             // Should be separate!
    void generateReport() { }        // Should be separate!
    void processPayment() { }        // Should be separate!
};
```

### Interview Tip:
Ask yourself: "If I change [X feature], which classes need to change?" 
If answer is many classes, you're violating SRP.

---

## O - Open/Closed Principle (OCP)

**Definition**: Classes should be OPEN for extension, CLOSED for modification.

**Why**: Add new features without breaking existing code.

### Examples in Our System:

#### ✅ Good - Following OCP

```cpp
// Can add new vehicle types WITHOUT modifying Vehicle.h
class Vehicle { };              // Base class (closed for modification)

class Car : public Vehicle { }; // Extension
class Bike : public Vehicle { };
class Truck : public Vehicle { };
// Want to add Bus? Just extend, don't modify Vehicle!
class Bus : public Vehicle { };  // No changes to existing code!

// Can add new pricing strategies WITHOUT modifying service
class PricingStrategy { };      // Interface (closed for modification)

class SimplePricingStrategy : public PricingStrategy { };
class HourlyPricingStrategy : public PricingStrategy { };
class WeekendPricingStrategy : public PricingStrategy { };  // NEW!
// Service code doesn't change!
```

#### ❌ Bad - Violating OCP

```cpp
// Need to modify this method for every new vehicle type (BAD!)
double calculatePrice(Vehicle* v) {
    if (v->type == CAR) {
        return 5.0;
    } else if (v->type == BIKE) {
        return 2.0;
    }
    // Adding truck? Must modify this function! ❌
    // else if (v->type == TRUCK) { ... }
}
```

### Interview Tip:
Use inheritance + polymorphism or Strategy Pattern to add features without changing existing code.

---

## L - Liskov Substitution Principle (LSP)

**Definition**: Derived classes must be substitutable for their base classes.

**Why**: Ensures inheritance is used correctly.

### Examples in Our System:

#### ✅ Good - Following LSP

```cpp
// Can use Car/Bike/Truck anywhere Vehicle is expected
void processVehicle(Vehicle* v) {
    std::string plate = v->getLicensePlate();  // Works for all!
    VehicleType type = v->getType();           // Works for all!
}

// All these work perfectly:
processVehicle(new Car("ABC123"));     ✓
processVehicle(new Bike("BIKE001"));   ✓
processVehicle(new Truck("TRK999"));   ✓
```

#### ❌ Bad - Violating LSP

```cpp
// Penguin is a bird but can't fly! Violates LSP
class Bird {
    virtual void fly() = 0;
};

class Sparrow : public Bird {
    void fly() { /* flies normally */ }  ✓
};

class Penguin : public Bird {
    void fly() {
        throw Exception("Penguins can't fly!");  ❌ Breaks substitution
    }
};

// Better: Separate into FlyingBird and NonFlyingBird
```

### Interview Tip:
"If it looks like a duck, quacks like a duck, but needs batteries, you probably have the wrong abstraction."

---

## I - Interface Segregation Principle (ISP)

**Definition**: Don't force clients to depend on interfaces they don't use.

**Why**: Keep interfaces small and focused.

### Examples in Our System:

#### ✅ Good - Following ISP

```cpp
// Small, focused interface
class PricingStrategy {
    virtual double calculatePrice(VehicleType type, double hours) = 0;
    // That's it! Only what clients need.
};

// Clients only implement what they need
class SimplePricingStrategy : public PricingStrategy {
    double calculatePrice(VehicleType type, double hours) { }
    // Not forced to implement unnecessary methods
};
```

#### ❌ Bad - Violating ISP

```cpp
// Fat interface forcing unnecessary implementations (BAD!)
class AllParkingOperations {
    virtual void parkVehicle() = 0;
    virtual void unparkVehicle() = 0;
    virtual void calculatePrice() = 0;
    virtual void handleVIPParking() = 0;      // Not all need this!
    virtual void handleReservation() = 0;     // Not all need this!
    virtual void sendNotification() = 0;      // Not all need this!
};

// Simple parking must implement everything (wasteful!)
class SimpleParkingService : public AllParkingOperations {
    void parkVehicle() { }
    void unparkVehicle() { }
    void calculatePrice() { }
    void handleVIPParking() { throw NotSupported(); }  // Forced to implement!
    void handleReservation() { throw NotSupported(); } // Forced to implement!
    void sendNotification() { throw NotSupported(); }  // Forced to implement!
};
```

### Interview Tip:
"Many client-specific interfaces are better than one general-purpose interface."

---

## D - Dependency Inversion Principle (DIP)

**Definition**: 
1. High-level modules should not depend on low-level modules. Both should depend on abstractions.
2. Abstractions should not depend on details. Details should depend on abstractions.

**Why**: Loose coupling, easier testing, flexibility.

### Examples in Our System:

#### ✅ Good - Following DIP

```cpp
// Service depends on ABSTRACTION (interface)
class ParkingLotService {
    PricingStrategy* pricingStrategy;  // Depends on interface, not concrete class
    
    ParkingLotService(PricingStrategy* strategy)  // Dependency injection
        : pricingStrategy(strategy) { }
};

// Can inject ANY pricing strategy:
ParkingLotService service1(new SimplePricingStrategy());   ✓
ParkingLotService service2(new HourlyPricingStrategy());   ✓
ParkingLotService service3(new WeekendPricingStrategy());  ✓
ParkingLotService serviceTest(new MockPricingStrategy());  ✓ Easy testing!
```

#### ❌ Bad - Violating DIP

```cpp
// Service depends on CONCRETE implementation (BAD!)
class ParkingLotService {
    SimplePricingStrategy pricingStrategy;  // Hard-coded dependency!
    
    ParkingLotService() {
        pricingStrategy = SimplePricingStrategy();  // Can't change it!
    }
    
    double calculateFee() {
        return pricingStrategy.calculatePrice();  // Tightly coupled!
    }
};

// Problems:
// - Can't switch pricing strategies
// - Hard to test (can't mock)
// - High-level depends on low-level
```

### Interview Tip:
Think of DIP as "programming to interfaces, not implementations." Use dependency injection.

---

## 🎯 How to Apply SOLID in Interviews

### Step 1: Listen to Requirements
Understand what features might be added later.

### Step 2: Identify Classes (SRP)
Each class = one clear responsibility.

### Step 3: Design for Extension (OCP)
Use inheritance, interfaces, strategy pattern.

### Step 4: Verify Relationships (LSP)
Ensure inheritance makes sense.

### Step 5: Keep Interfaces Focused (ISP)
Small, client-specific interfaces.

### Step 6: Depend on Abstractions (DIP)
Use interfaces, dependency injection.

---

## 📝 Quick Checklist

When designing a system, ask:

- [ ] Does each class have ONE clear purpose? (SRP)
- [ ] Can I add features without modifying existing code? (OCP)
- [ ] Can derived classes replace base classes safely? (LSP)
- [ ] Are my interfaces minimal and focused? (ISP)
- [ ] Do I depend on abstractions, not concrete classes? (DIP)

---

## 🎓 Interview Phrases to Use

**SRP**: "I'm separating concerns to ensure each class has a single responsibility."

**OCP**: "I'm using polymorphism so we can extend without modification."

**LSP**: "All derived classes maintain the contract of the base class."

**ISP**: "I'm keeping interfaces focused on specific client needs."

**DIP**: "I'm using dependency injection to depend on abstractions."

---

## 🚀 Common Interview Scenarios

### Scenario: "Add a new vehicle type"
- **Without SOLID**: Modify Vehicle class, modify pricing logic, modify parking logic ❌
- **With SOLID**: Create new class extending Vehicle, done! ✅ (OCP)

### Scenario: "Change pricing algorithm"
- **Without SOLID**: Modify ParkingLotService, risk breaking existing code ❌
- **With SOLID**: Create new PricingStrategy implementation, inject it ✅ (DIP, OCP)

### Scenario: "Add VIP parking"
- **Without SOLID**: Stuff everything into existing classes ❌
- **With SOLID**: New VIPParkingStrategy, new VIPSpot class ✅ (SRP, OCP)

### Scenario: "Need to test in isolation"
- **Without SOLID**: Can't test service without real pricing, database ❌
- **With SOLID**: Inject mock interfaces, easy unit testing ✅ (DIP)

---

## 🎯 Remember

SOLID is not about perfect code, it's about:
- ✅ **Maintainability**: Easy to understand and modify
- ✅ **Flexibility**: Easy to extend
- ✅ **Testability**: Easy to test in isolation
- ✅ **Reusability**: Components can be reused

Don't over-engineer! Apply SOLID pragmatically based on requirements.

---

## 📚 Further Reading

- Clean Code by Robert C. Martin
- Design Patterns: Elements of Reusable Object-Oriented Software
- Head First Design Patterns

Good luck with your interviews! 🍀
