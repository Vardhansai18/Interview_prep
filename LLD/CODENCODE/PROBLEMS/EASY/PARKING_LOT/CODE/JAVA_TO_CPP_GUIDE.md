# Java to C++ Conversion Guide

## Overview
This document highlights the key differences between the original Java implementation and the C++ conversion of the Parking Lot System.

## Language Feature Mappings

### 1. Package/Namespace System

**Java:**
```java
package parkinglot.domain.vehicle;
```

**C++:**
```cpp
namespace parkinglot {
namespace domain {
namespace vehicle {
    // code
}}}
```

### 2. Memory Management

**Java:**
```java
// Java uses automatic garbage collection
Vehicle car = new Car("ABC123");
```

**C++:**
```cpp
// C++ uses smart pointers for automatic memory management
auto car = std::make_shared<Car>("ABC123");
std::shared_ptr<Car> car = std::make_shared<Car>("ABC123");
```

### 3. Inheritance

**Java:**
```java
public abstract class Vehicle {
    private final String vehicleNumber;
}
```

**C++:**
```cpp
class Vehicle {
protected:
    std::string vehicleNumber;
public:
    virtual ~Vehicle() = default;  // Virtual destructor
};
```

### 4. Thread Safety

**Java:**
```java
public synchronized boolean parkVehicle(Vehicle vehicle) {
    // Method is synchronized
}
```

**C++:**
```cpp
bool parkVehicle(std::shared_ptr<Vehicle> vehicle) {
    std::lock_guard<std::mutex> lock(spotMutex);
    // Code is protected by mutex
}
```

### 5. Collections

**Java:**
```java
Map<String, Ticket> activeTickets = new ConcurrentHashMap<>();
List<ParkingFloor> parkingFloors = List.of(floor1, floor2);
```

**C++:**
```cpp
std::unordered_map<std::string, std::shared_ptr<Ticket>> activeTickets;
std::vector<std::shared_ptr<ParkingFloor>> parkingFloors = {floor1, floor2};
```

### 6. Date/Time Handling

**Java:**
```java
import java.time.LocalDateTime;
import java.time.Duration;

LocalDateTime entryTime = LocalDateTime.now();
long hours = Duration.between(entryTime, exitTime).toHours();
```

**C++:**
```cpp
#include <chrono>

using TimePoint = std::chrono::system_clock::time_point;
TimePoint entryTime = std::chrono::system_clock::now();
auto duration = std::chrono::duration_cast<std::chrono::hours>(exitTime - entryTime);
```

### 7. Interfaces

**Java:**
```java
public interface PricingStrategy {
    Double calculatePrice(Ticket ticket);
}
```

**C++:**
```cpp
class PricingStrategy {
public:
    virtual ~PricingStrategy() = default;
    virtual double calculatePrice(std::shared_ptr<Ticket> ticket) = 0;
};
```

### 8. Exceptions

**Java:**
```java
public class ParkingException extends RuntimeException {
    public ParkingException(String message) {
        super(message);
    }
}
```

**C++:**
```cpp
class ParkingException : public std::exception {
private:
    std::string message;
public:
    explicit ParkingException(const std::string& message);
    const char* what() const noexcept override;
};
```

### 9. Enums

**Java:**
```java
public enum VehicleType {
    BIKE, CAR, TRUCK
}
```

**C++:**
```cpp
enum class VehicleType {
    BIKE,
    CAR,
    TRUCK
};
```

### 10. UUID Generation

**Java:**
```java
import java.util.UUID;
String ticketId = UUID.randomUUID().toString();
```

**C++:**
```cpp
// Custom implementation using random generators
#include <random>
std::string generateUUID() {
    // Implementation using std::random_device and std::mt19937
}
```

## Build System Comparison

### Java
```bash
# Using Maven
mvn clean compile
mvn exec:java

# Using Gradle
gradle build
gradle run
```

### C++
```bash
# Using CMake
mkdir build && cd build
cmake ..
make
./parking_lot_demo

# Using g++ directly
./build.sh run
```

## Key Architectural Decisions

### 1. Smart Pointers Over Raw Pointers
- Used `std::shared_ptr` for automatic memory management
- Prevents memory leaks
- Closer to Java's garbage collection behavior

### 2. RAII (Resource Acquisition Is Initialization)
- `std::lock_guard` for automatic lock release
- Smart pointers for automatic memory deallocation
- File handles, connections follow RAII pattern

### 3. Const Correctness
- Getter methods marked as `const`
- Pass-by-const-reference where appropriate
- Better compile-time safety

### 4. Explicit Constructors
- Used `explicit` keyword to prevent implicit conversions
- Safer than Java's constructor behavior

## Performance Considerations

### C++ Advantages
1. **No Garbage Collection Overhead**: Deterministic destruction
2. **Stack Allocation Option**: Objects can be created on stack
3. **Better Cache Locality**: More control over memory layout
4. **Zero-cost Abstractions**: Virtual calls can be optimized away

### Java Advantages
1. **Simpler Memory Management**: No manual pointer management
2. **Built-in Thread Safety**: synchronized keyword
3. **Easier Reflection**: Runtime type information
4. **Cross-platform**: JVM handles platform differences

## Code Size Comparison

| Component | Java Lines | C++ Lines (h+cpp) | Ratio |
|-----------|------------|-------------------|-------|
| Vehicle Classes | ~30 | ~80 | 2.7x |
| Parking Classes | ~40 | ~90 | 2.25x |
| Service Layer | ~65 | ~110 | 1.7x |
| **Total** | ~200 | ~400 | 2.0x |

*Note: C++ requires separate header and implementation files, contributing to higher line count.*

## Testing Strategies

### Java
```java
@Test
public void testParkVehicle() {
    Vehicle car = new Car("ABC123");
    Ticket ticket = service.parkVehicle(car);
    assertNotNull(ticket);
}
```

### C++ (with GoogleTest)
```cpp
TEST(ParkingLotTest, ParkVehicle) {
    auto car = std::make_shared<Car>("ABC123");
    auto ticket = service->parkVehicle(car);
    ASSERT_NE(ticket, nullptr);
}
```

## Common Pitfalls When Converting

1. **Forgetting Virtual Destructors**: Always add virtual destructors to base classes
2. **Memory Leaks**: Use smart pointers instead of raw pointers
3. **Header Guards**: Always use include guards or `#pragma once`
4. **Mutex Deadlocks**: Be careful with nested locks
5. **Undefined Behavior**: Initialize all variables, check array bounds

## Best Practices Applied

### C++ Specific
- ✅ Smart pointers for memory management
- ✅ RAII for resource management
- ✅ Const correctness throughout
- ✅ Rule of Zero/Five for classes
- ✅ Move semantics where appropriate
- ✅ Namespace organization
- ✅ Header guards in all headers

### Common to Both
- ✅ SOLID principles
- ✅ Design patterns (Strategy, Factory)
- ✅ Single Responsibility Principle
- ✅ Open-Closed Principle
- ✅ Clean code practices

## Conclusion

The C++ implementation maintains the same design principles and architecture as the Java version while leveraging C++-specific features for better performance and control. The code is production-ready and follows modern C++17 standards.

## Further Reading

- **Effective Modern C++** by Scott Meyers
- **C++ Core Guidelines** by Bjarne Stroustrup
- **Design Patterns in C++** by GoF
- **Java to C++ Migration Guide** by Oracle
