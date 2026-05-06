# Parking Lot System - Interview Quick Reference

## 🎯 Quick Overview
A complete Low-Level Design implementation demonstrating:
- SOLID principles
- Design patterns (Strategy, Factory)
- Thread-safe operations
- Object-oriented programming

## 📋 Interview Talking Points

### 1. Design Approach (CERID)
- **Clarify**: Gathered functional and non-functional requirements
- **Entities**: Identified 7 core entities (Vehicle, ParkingSpot, Floor, Ticket, Service, Strategy, Application)
- **Responsibilities**: Applied Single Responsibility Principle
- **Interactions**: Defined clear relationships and data flow
- **Durability**: Ensured extensibility through design patterns

### 2. Key Design Decisions

#### Why Strategy Pattern for Pricing?
- **Open-Closed Principle**: Can add new pricing strategies without modifying existing code
- **Example**: Easily switch from Hourly to Daily/Monthly pricing
- **Extensibility**: Support different pricing for different vehicle types

#### Why Separate Floors and Spots?
- **Scalability**: Can add/remove floors independently
- **Organization**: Logical separation matches real-world structure
- **Future Extension**: Can add floor-specific features (VIP floors, EV charging)

#### Thread Safety Implementation
- **Mutex in ParkingSpot**: Prevents concurrent allocation of same spot
- **Mutex in Service**: Protects ticket map operations
- **Lock Guards**: RAII ensures locks are always released

### 3. SOLID Principles Applied

#### Single Responsibility Principle (SRP)
- `Vehicle`: Only represents vehicle data
- `ParkingSpot`: Only manages single spot allocation
- `Ticket`: Only tracks parking transaction
- `PricingStrategy`: Only calculates pricing
- `ParkingLotService`: Only orchestrates parking operations

#### Open-Closed Principle (OCP)
- **Open for Extension**: Add new vehicle types, pricing strategies
- **Closed for Modification**: Core logic doesn't change
- **Example**: Adding `ElectricCar` doesn't modify existing vehicle code

#### Liskov Substitution Principle (LSP)
- Any `Vehicle` subclass can be used wherever `Vehicle` is expected
- Any `PricingStrategy` implementation works with the service

#### Interface Segregation Principle (ISP)
- Small, focused interfaces (`PricingStrategy` has one method)
- Clients don't depend on unused methods

#### Dependency Inversion Principle (DIP)
- `ParkingLotService` depends on `PricingStrategy` interface, not concrete implementation
- Easy to inject different strategies

### 4. Common Interview Questions

#### Q: How would you handle different spot sizes?
**A**: Add `SpotSize` enum (COMPACT, REGULAR, LARGE), map vehicle types to required sizes.

#### Q: How to find nearest available spot?
**A**: 
- Add distance calculation in `ParkingFloor`
- Implement `findNearestSpot(entryPoint, vehicleType)`
- Could use spatial data structures for optimization

#### Q: How to handle peak hour pricing?
**A**: 
- Implement `PeakHourPricingStrategy`
- Check current time and apply multiplier
- Strategy pattern makes this easy

#### Q: How to track occupancy?
**A**:
```cpp
class ParkingFloor {
    int getOccupancy() {
        int occupied = 0;
        for (auto& spot : spots) {
            if (!spot->isAvailable()) occupied++;
        }
        return occupied;
    }
};
```

#### Q: What about payment processing?
**A**:
- Add `PaymentProcessor` interface
- Implement `CashPayment`, `CardPayment`, `DigitalWallet`
- Another Strategy pattern application

#### Q: How to scale this system?
**A**:
- **Horizontal Scaling**: Multiple service instances with shared database
- **Caching**: Cache floor/spot availability
- **Event-Driven**: Use message queues for ticket processing
- **Microservices**: Separate services for parking, payment, reporting

### 5. Time & Space Complexity

#### Park Vehicle: O(F × S)
- F = number of floors
- S = spots per floor
- Linear search through all spots
- **Optimization**: Maintain available spots in priority queue

#### Unpark Vehicle: O(1)
- Direct ticket lookup in hash map
- Constant time spot release

#### Space Complexity: O(F × S + T)
- F × S for all parking spots
- T for active tickets

### 6. Extension Points

#### Easy to Add:
- ✅ New vehicle types (Motorcycle, Truck, Bus)
- ✅ New pricing strategies (Flat, Progressive, Peak-hour)
- ✅ Discount policies (Early bird, Member)
- ✅ Multiple entrances/exits

#### Moderate Complexity:
- Reservation system (add `ReservationService`)
- Electric vehicle charging (add `ChargingSpot` subclass)
- Valet parking (add `ValetService`)

#### Complex (Architecture Change):
- Multi-location support
- Real-time availability API
- Mobile app integration
- Analytics and reporting

### 7. Production Considerations

#### What's Missing for Production?
1. **Database Integration**: Currently in-memory only
2. **Persistence**: Tickets lost on restart
3. **Logging**: No audit trail
4. **Monitoring**: No metrics/alerts
5. **Configuration**: Hardcoded values
6. **Error Recovery**: Limited error handling
7. **Testing**: No unit tests included
8. **API Layer**: No REST/gRPC endpoints

#### Quick Wins for Production:
```cpp
// Add database
#include <sqlite3.h>
class TicketRepository {
    void save(Ticket ticket);
    Ticket find(string id);
};

// Add logging
#include <spdlog/spdlog.h>
spdlog::info("Vehicle parked: {}", ticket->getId());

// Add metrics
class Metrics {
    void recordParking(VehicleType type);
    void recordRevenue(double amount);
};
```

### 8. Alternative Designs Considered

#### Option 1: Spots Find Themselves
```cpp
// Each spot knows if it's available
// Service asks spots if they can accommodate
```
❌ **Rejected**: Violates SRP, spots doing too much

#### Option 2: Central Allocation Algorithm
```cpp
class SpotAllocator {
    ParkingSpot allocate(Vehicle);
}
```
✅ **Good**: Separation of concerns, can optimize easily
📝 **Note**: Could be added as enhancement

#### Option 3: Event-Driven Architecture
```cpp
// Publish events: VehicleParked, VehicleExited
// Subscribers handle pricing, notifications
```
✅ **Good for**: Large scale systems
❌ **Overkill for**: Simple parking lot

## 🎤 Presentation Tips

1. **Start with Requirements**: Always clarify what you're building
2. **Draw Diagrams**: Sketch classes and relationships on whiteboard
3. **Discuss Trade-offs**: Mention alternatives considered
4. **Ask Questions**: "Should we handle reservation?" "Multiple entrances?"
5. **Think Aloud**: Share your thought process
6. **Start Simple**: Get basic version working, then extend
7. **Handle Edge Cases**: "What if spot taken concurrently?" "Invalid ticket?"

## 📚 Study Points Before Interview

- ✅ SOLID principles (be able to explain each)
- ✅ Common design patterns (Strategy, Factory, Singleton)
- ✅ Thread safety concepts (mutex, deadlock, race conditions)
- ✅ Time/space complexity analysis
- ✅ Database normalization (if DB questions asked)
- ✅ API design (REST/gRPC)
- ✅ Scalability patterns (caching, load balancing, sharding)

## ⚡ Quick Build Commands

```bash
# Build and run
cd CODE
./build.sh run

# Or manual compile
g++ -std=c++17 -pthread main.cpp /*.cpp -o demo
./demo
```

## 📝 Key Takeaways

1. **Design First**: Think through requirements before coding
2. **SOLID Wins**: Makes code maintainable and extensible
3. **Patterns Matter**: Strategy pattern adds huge flexibility
4. **Thread Safety**: Critical for real-world systems
5. **Keep It Simple**: Don't over-engineer initially

---

**Remember**: In interviews, clear communication matters more than perfect code!
