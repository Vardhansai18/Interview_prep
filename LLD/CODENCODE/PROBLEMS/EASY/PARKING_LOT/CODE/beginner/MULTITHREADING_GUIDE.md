# 🧵 Multithreading Guide

## Introduction

This guide explains how to extend the current single-threaded parking lot system to support multithreading. This is essential for production systems where multiple users access the system simultaneously.

## Why Multithreading?

In real-world scenarios:
- Multiple entry gates accepting vehicles simultaneously
- Multiple exit gates processing payments concurrently
- Admin viewing status while operations happen
- Race conditions can occur without proper synchronization

## Common Concurrency Issues

### Issue 1: Race Condition on Parking Spot
```cpp
// Thread 1 and Thread 2 both try to park at same time
Thread 1: Check spot available → TRUE
Thread 2: Check spot available → TRUE  // Spot still shows available!
Thread 1: Park vehicle
Thread 2: Park vehicle  // BUG: Two vehicles in one spot!
```

### Issue 2: Race Condition on Ticket Counter
```cpp
// Both threads might get same ticket ID
Thread 1: Read ticketCounter = 5
Thread 2: Read ticketCounter = 5  // Same value!
Thread 1: Increment to 6
Thread 2: Increment to 6  // Should be 7!
```

### Issue 3: Active Tickets Map Corruption
```cpp
// Concurrent modifications to map can corrupt it
Thread 1: activeTickets.insert(...)
Thread 2: activeTickets.erase(...)  // Concurrent access = crash!
```

## Solution: Add Thread Safety

### Step 1: Add Mutex to ParkingLotService

```cpp
#include <mutex>

class ParkingLotService {
private:
    std::vector<ParkingFloor*> floors;
    std::map<std::string, Ticket*> activeTickets;
    PricingStrategy* pricingStrategy;
    int ticketCounter;
    
    // ADD THIS: Mutex for thread safety
    mutable std::mutex parkingMutex;    // For general operations
    mutable std::mutex ticketMutex;     // For ticket operations
    
public:
    // ... rest of code
};
```

### Step 2: Protect parkVehicle() Method

```cpp
Ticket* parkVehicle(Vehicle* vehicle) {
    // Lock mutex at start of critical section
    std::lock_guard<std::mutex> lock(parkingMutex);
    
    VehicleType type = vehicle->getType();
    
    for (ParkingFloor* floor : floors) {
        ParkingSpot* spot = floor->findAvailableSpot(type);
        
        if (spot != nullptr) {
            spot->parkVehicle(vehicle);
            
            std::string ticketId = generateTicketId();  // Also protected
            Ticket* ticket = new Ticket(ticketId, vehicle, spot);
            
            activeTickets[ticketId] = ticket;
            return ticket;
        }
    }
    
    return nullptr;
    // Mutex automatically released when lock_guard goes out of scope
}
```

### Step 3: Protect unparkVehicle() Method

```cpp
double unparkVehicle(const std::string& ticketId) {
    std::lock_guard<std::mutex> lock(parkingMutex);
    
    auto it = activeTickets.find(ticketId);
    if (it == activeTickets.end()) {
        return -1.0;
    }
    
    Ticket* ticket = it->second;
    ParkingSpot* spot = ticket->getSpot();
    Vehicle* vehicle = ticket->getVehicle();
    double duration = ticket->getDurationInHours();
    
    double fee = pricingStrategy->calculatePrice(vehicle->getType(), duration);
    
    spot->unparkVehicle();
    activeTickets.erase(it);
    delete ticket;
    
    return fee;
}
```

### Step 4: Protect Ticket ID Generation

```cpp
std::string generateTicketId() {
    std::lock_guard<std::mutex> lock(ticketMutex);
    
    std::stringstream ss;
    ss << "TICKET-" << std::setw(4) << std::setfill('0') << ticketCounter++;
    return ss.str();
}
```

### Step 5: Spot-Level Granularity (Advanced)

For better performance, lock individual spots instead of entire parking lot:

```cpp
class ParkingSpot {
private:
    int spotNumber;
    VehicleType spotType;
    bool occupied;
    Vehicle* parkedVehicle;
    std::mutex spotMutex;  // Per-spot lock

public:
    bool tryParkVehicle(Vehicle* vehicle) {
        std::lock_guard<std::mutex> lock(spotMutex);
        
        if (occupied || spotType != vehicle->getType()) {
            return false;
        }
        
        parkedVehicle = vehicle;
        occupied = true;
        return true;
    }
    
    void unparkVehicle() {
        std::lock_guard<std::mutex> lock(spotMutex);
        parkedVehicle = nullptr;
        occupied = false;
    }
};
```

## Threading Patterns

### Pattern 1: Multiple Entry Gates

```cpp
void entryGateWorker(int gateId, ParkingLotService& parkingLot) {
    while (true) {
        // Simulate vehicle arrival
        Vehicle* vehicle = getNextVehicle();  // From queue
        
        Ticket* ticket = parkingLot.parkVehicle(vehicle);
        
        if (ticket) {
            std::cout << "Gate " << gateId << ": Parked " 
                     << vehicle->getLicensePlate() << std::endl;
        } else {
            std::cout << "Gate " << gateId << ": Lot full!" << std::endl;
        }
    }
}

// Usage:
std::thread gate1(entryGateWorker, 1, std::ref(parkingLot));
std::thread gate2(entryGateWorker, 2, std::ref(parkingLot));
```

### Pattern 2: Multiple Exit Gates

```cpp
void exitGateWorker(int gateId, ParkingLotService& parkingLot) {
    while (true) {
        std::string ticketId = getNextExitingVehicle();  // From queue
        
        double fee = parkingLot.unparkVehicle(ticketId);
        
        if (fee >= 0) {
            std::cout << "Gate " << gateId << ": Fee $" << fee << std::endl;
        } else {
            std::cout << "Gate " << gateId << ": Invalid ticket!" << std::endl;
        }
    }
}
```

## Locking Strategies

### Strategy 1: Coarse-Grained Locking (Beginners)
- **Pros**: Simple, hard to get wrong
- **Cons**: Lower concurrency, potential bottleneck
- **Use when**: Starting out, system not under heavy load

```cpp
// One mutex for entire service
std::lock_guard<std::mutex> lock(serviceMutex);
```

### Strategy 2: Fine-Grained Locking (Advanced)
- **Pros**: Better performance, higher concurrency
- **Cons**: Complex, risk of deadlocks
- **Use when**: High traffic, performance critical

```cpp
// Separate mutexes for different resources
std::lock_guard<std::mutex> floorLock(floorMutex);
std::lock_guard<std::mutex> ticketLock(ticketMutex);
```

### Strategy 3: Read-Write Locks (Expert)
- **Pros**: Multiple readers, single writer optimization
- **Cons**: Most complex
- **Use when**: Many reads, few writes

```cpp
std::shared_mutex rwMutex;

// Multiple readers can hold this simultaneously
std::shared_lock<std::shared_mutex> readLock(rwMutex);

// Only one writer at a time
std::unique_lock<std::shared_mutex> writeLock(rwMutex);
```

## Deadlock Prevention

### Rule 1: Lock Ordering
Always acquire locks in same order:
```cpp
// GOOD: Always lock in same order
void transfer() {
    std::lock_guard<std::mutex> lock1(mutex1);
    std::lock_guard<std::mutex> lock2(mutex2);
}

// BAD: Can deadlock
void transfer_bad() {
    std::lock_guard<std::mutex> lock2(mutex2);  // Reversed!
    std::lock_guard<std::mutex> lock1(mutex1);
}
```

### Rule 2: Use std::lock for Multiple Mutexes
```cpp
// Locks both atomically, prevents deadlock
std::lock(mutex1, mutex2);
std::lock_guard<std::mutex> lock1(mutex1, std::adopt_lock);
std::lock_guard<std::mutex> lock2(mutex2, std::adopt_lock);
```

## Testing Multithreaded Code

### Test 1: Concurrent Parking
```cpp
void testConcurrentPark() {
    ParkingLotService parkingLot(new SimplePricingStrategy());
    // Setup parking lot...
    
    std::vector<std::thread> threads;
    
    // Launch 10 threads parking simultaneously
    for (int i = 0; i < 10; i++) {
        threads.emplace_back([&parkingLot, i]() {
            Vehicle* car = new Car("CAR-" + std::to_string(i));
            Ticket* ticket = parkingLot.parkVehicle(car);
            // Check ticket validity...
        });
    }
    
    // Wait for all threads
    for (auto& t : threads) {
        t.join();
    }
    
    // Verify: No duplicate spots, correct ticket count
}
```

### Test 2: Race Condition Test
```cpp
// Try to expose race conditions by high contention
void stressTest() {
    const int NUM_THREADS = 100;
    const int OPERATIONS_PER_THREAD = 1000;
    
    // Have threads rapidly park/unpark
    // Check for crashes, assertion failures, corrupted data
}
```

## Performance Considerations

### Measure Before Optimizing
```cpp
auto start = std::chrono::high_resolution_clock::now();
// ... operation ...
auto end = std::chrono::high_resolution_clock::now();
auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
```

### Reduce Critical Section Size
```cpp
// BAD: Holding lock too long
{
    std::lock_guard<std::mutex> lock(mutex);
    doExpensiveComputation();  // Don't need lock for this!
    updateSharedData();
}

// GOOD: Minimal critical section
{
    auto result = doExpensiveComputation();  // Outside lock
    
    std::lock_guard<std::mutex> lock(mutex);
    updateSharedData(result);  // Only lock when needed
}
```

## Common Interview Questions

**Q: Why not use one global mutex for everything?**
A: Simple but creates bottleneck. Fine-grained locking allows better concurrency.

**Q: What's the difference between mutex and semaphore?**
A: Mutex is binary (locked/unlocked), semaphore can have count > 1 for resource pools.

**Q: How do you prevent deadlock?**
A: Lock ordering, timeout locks, deadlock detection algorithms.

**Q: What's thread-safety vs thread-aware?**
A: Thread-safe = works correctly with multiple threads. Thread-aware = knows about threads but requires external synchronization.

## Next Steps

1. **Implement Thread-Safe Version**: Apply changes above
2. **Test Thoroughly**: Use multiple threads in demo
3. **Measure Performance**: Compare single vs multi-threaded
4. **Study Alternatives**: Lock-free data structures, atomic operations
5. **Production Features**: Connection pooling, thread pools, async operations

## References for Deep Dive

- C++ Concurrency in Action (Anthony Williams)
- Java Concurrency in Practice (applicable concepts)
- std::mutex, std::lock_guard, std::unique_lock documentation
- Threading model for your target platform

## Warning ⚠️

Multithreading is complex! Start simple:
1. Master single-threaded version first
2. Add one mutex at a time
3. Test extensively
4. Document locking strategy
5. Review with experienced developers

Good luck! 🧵
