# 🔄 Detailed Flow Explanations

## Complete Step-by-Step Walkthrough of All System Flows

This document explains EVERY step that happens when you use the parking lot system. Perfect for understanding the system deeply and explaining it in interviews.

---

## 📋 Table of Contents
1. [System Initialization Flow](#1-system-initialization-flow)
2. [Park Vehicle Flow](#2-park-vehicle-flow)
3. [Unpark Vehicle Flow](#3-unpark-vehicle-flow)
4. [Display Status Flow](#4-display-status-flow)
5. [Error Handling Flows](#5-error-handling-flows)

---

## 1. System Initialization Flow

### Overview
Before parking vehicles, we need to set up the parking lot structure.

### Step-by-Step Execution

#### Step 1.1: Create Pricing Strategy
```cpp
PricingStrategy* pricingStrategy = new SimplePricingStrategy();
```

**What Happens:**
1. Memory allocated for SimplePricingStrategy object
2. Object contains pricing logic (Bike: $2/hr, Car: $5/hr, Truck: $10/hr)
3. Pointer stored in `pricingStrategy`

**Memory State:**
```
Heap:
  [SimplePricingStrategy object]
     ↑
     |
  pricingStrategy (pointer)
```

#### Step 1.2: Create Parking Lot Service
```cpp
ParkingLotService parkingLot(pricingStrategy);
```

**What Happens:**
1. ParkingLotService constructor called
2. Constructor receives pricing strategy pointer
3. Initializes member variables:
   - `floors`: Empty vector (size 0)
   - `activeTickets`: Empty map
   - `pricingStrategy`: Stores the pointer
   - `ticketCounter`: Set to 1

**Memory State:**
```
Stack:
  parkingLot object:
    - floors: [] (empty vector)
    - activeTickets: {} (empty map)
    - pricingStrategy: → [SimplePricingStrategy]
    - ticketCounter: 1
```

**SOLID Principle Applied:** 
- **Dependency Inversion (DIP)**: Service depends on PricingStrategy interface, not concrete SimplePricingStrategy
- Can swap pricing strategies without changing ParkingLotService code

#### Step 1.3: Create Parking Floor
```cpp
ParkingFloor* floor0 = new ParkingFloor(0);
```

**What Happens:**
1. Memory allocated on heap for ParkingFloor
2. Constructor called with floorNumber = 0
3. Initializes:
   - `floorNumber`: 0
   - `spots`: Empty vector

**Memory State:**
```
Heap:
  [ParkingFloor]
    - floorNumber: 0
    - spots: []
```

#### Step 1.4: Create Parking Spots
```cpp
floor0->addSpot(new ParkingSpot(1, VehicleType::BIKE));
floor0->addSpot(new ParkingSpot(2, VehicleType::BIKE));
floor0->addSpot(new ParkingSpot(3, VehicleType::CAR));
```

**What Happens for Each Spot:**
1. `new ParkingSpot(1, VehicleType::BIKE)` creates spot:
   - `spotNumber`: 1
   - `spotType`: BIKE
   - `occupied`: false
   - `parkedVehicle`: nullptr

2. `floor0->addSpot(spot)` adds to floor's vector:
   - `spots.push_back(spot)` appends pointer to vector

**Memory State After Adding 5 Spots:**
```
Heap:
  [ParkingFloor 0]
    - floorNumber: 0
    - spots: [spot1*, spot2*, spot3*, spot4*, spot5*]
                 ↓       ↓       ↓       ↓       ↓
              [Spot1] [Spot2] [Spot3] [Spot4] [Spot5]
               BIKE    BIKE    CAR     CAR     TRUCK
               empty   empty   empty   empty   empty
```

**SOLID Principle Applied:**
- **Single Responsibility (SRP)**: Each class has one job
  - ParkingSpot: Manages one spot's state
  - ParkingFloor: Manages collection of spots
  - ParkingLotService: Orchestrates operations

#### Step 1.5: Add Floor to Service
```cpp
parkingLot.addFloor(floor0);
```

**What Happens:**
1. `addFloor()` method called
2. `floors.push_back(floor0)` adds pointer to floors vector

**Complete Memory State:**
```
Stack:
  parkingLot:
    - floors: [floor0*, floor1*]
      ↓
Heap:
    [Floor 0]           [Floor 1]
      spots: [5 spots]    spots: [3 spots]
```

**Initialization Complete!** ✅

---

## 2. Park Vehicle Flow

### Overview
User arrives with vehicle and wants to park.

### Step-by-Step Execution

#### Input
```cpp
Vehicle* car1 = new Car("CAR-ABC-123");
Ticket* ticket = parkingLot.parkVehicle(car1);
```

#### Step 2.1: Create Vehicle Object
```cpp
Vehicle* car1 = new Car("CAR-ABC-123");
```

**What Happens:**
1. Memory allocated for Car object
2. Car constructor called: `Car("CAR-ABC-123")`
3. Calls parent constructor: `Vehicle("CAR-ABC-123", VehicleType::CAR)`
4. Initializes:
   - `licensePlate`: "CAR-ABC-123"
   - `type`: VehicleType::CAR

**Memory State:**
```
Heap:
  [Car object]
    - licensePlate: "CAR-ABC-123"
    - type: CAR
```

**SOLID Principle Applied:**
- **Liskov Substitution (LSP)**: Car can be used wherever Vehicle is expected
- **Open/Closed (OCP)**: New vehicle types added by extending, not modifying

#### Step 2.2: Call parkVehicle Method
```cpp
Ticket* ticket = parkingLot.parkVehicle(car1);
```

**Method Signature:**
```cpp
Ticket* ParkingLotService::parkVehicle(Vehicle* vehicle)
```

**Entry Point:** ParkingLotService receives vehicle pointer

#### Step 2.3: Get Vehicle Type
```cpp
VehicleType type = vehicle->getType();  // Returns: VehicleType::CAR
```

**What Happens:**
1. Virtual method call (polymorphism)
2. Calls `getType()` on Car object
3. Returns VehicleType::CAR

**Why This Works:**
- Polymorphism: Even though pointer is `Vehicle*`, correct method called
- Runtime determination of actual type

#### Step 2.4: Search for Available Spot
```cpp
for (ParkingFloor* floor : floors) {
    ParkingSpot* spot = floor->findAvailableSpot(type);
    if (spot != nullptr) {
        // Found spot!
    }
}
```

**Search Algorithm:**
```
FOR each floor in floors:
  1. Call floor->findAvailableSpot(CAR)
  
  2. Floor searches its spots:
     FOR each spot in spots:
       IF spot.canParkVehicle(CAR):
         RETURN spot
     
  3. If spot found, exit loop
  4. If not, continue to next floor
```

**Detailed Floor Search:**
```cpp
ParkingSpot* ParkingFloor::findAvailableSpot(VehicleType vehicleType) {
    for (ParkingSpot* spot : spots) {
        if (spot->canParkVehicle(vehicleType)) {
            return spot;  // First available spot
        }
    }
    return nullptr;
}
```

**Spot Check:**
```cpp
bool ParkingSpot::canParkVehicle(VehicleType vehicleType) const {
    return !occupied && spotType == vehicleType;
    //     ^^^^^^^^^^    ^^^^^^^^^^^^^^^^^^^^^^^
    //     Must be       Must match
    //     empty         vehicle type
}
```

**Example Execution:**

Floor 0, Spot 1 (BIKE):
- `!occupied`: true (empty)
- `spotType == CAR`: false (BIKE ≠ CAR)
- Result: false, continue

Floor 0, Spot 2 (BIKE):
- `!occupied`: true
- `spotType == CAR`: false
- Result: false, continue

Floor 0, Spot 3 (CAR):
- `!occupied`: true
- `spotType == CAR`: true ✅
- Result: **true!** Found spot!

**Time Complexity:** O(F × S) where F = floors, S = spots per floor

#### Step 2.5: Park Vehicle in Spot
```cpp
spot->parkVehicle(vehicle);
```

**What Happens:**
```cpp
void ParkingSpot::parkVehicle(Vehicle* vehicle) {
    parkedVehicle = vehicle;  // Store pointer to vehicle
    occupied = true;           // Mark as occupied
}
```

**Memory State Change:**
```
Before:
  [Spot 3]
    - spotNumber: 3
    - spotType: CAR
    - occupied: false
    - parkedVehicle: nullptr

After:
  [Spot 3]
    - spotNumber: 3
    - spotType: CAR
    - occupied: true ✓
    - parkedVehicle: → [Car "CAR-ABC-123"] ✓
```

#### Step 2.6: Generate Ticket ID
```cpp
std::string ticketId = generateTicketId();
```

**What Happens:**
```cpp
std::string ParkingLotService::generateTicketId() {
    std::stringstream ss;
    ss << "TICKET-" << std::setw(4) << std::setfill('0') << ticketCounter++;
    return ss.str();
}
```

**Step-by-Step:**
1. Create stringstream
2. Add "TICKET-" prefix
3. Format counter with leading zeros: `ticketCounter` = 1 → "0001"
4. Increment counter: `ticketCounter++` (now 2)
5. Return: "TICKET-0001"

**Sequence:**
- First call: "TICKET-0001", counter becomes 2
- Second call: "TICKET-0002", counter becomes 3
- Third call: "TICKET-0003", counter becomes 4

#### Step 2.7: Create Ticket
```cpp
Ticket* ticket = new Ticket(ticketId, vehicle, spot);
```

**Ticket Constructor:**
```cpp
Ticket::Ticket(const std::string& id, Vehicle* v, ParkingSpot* s)
    : ticketId(id), vehicle(v), spot(s) {
    entryTime = std::chrono::system_clock::now();  // Record current time
}
```

**What Happens:**
1. Allocate memory for Ticket
2. Store ticketId: "TICKET-0001"
3. Store vehicle pointer: → Car object
4. Store spot pointer: → Spot 3
5. Record entry time: Current system time

**Memory State:**
```
Heap:
  [Ticket]
    - ticketId: "TICKET-0001"
    - vehicle: → [Car "CAR-ABC-123"]
    - spot: → [Spot 3]
    - entryTime: 2026-05-06 09:16:13
```

#### Step 2.8: Store Ticket in Map
```cpp
activeTickets[ticketId] = ticket;
```

**What Happens:**
1. Map insertion: key = "TICKET-0001", value = ticket pointer
2. O(log n) insertion time (std::map is red-black tree)

**activeTickets Map:**
```
{
  "TICKET-0001" → [Ticket 1]
  "TICKET-0002" → [Ticket 2]  // If exists
  "TICKET-0003" → [Ticket 3]  // If exists
}
```

**Why Map?**
- Fast lookup by ticket ID: O(log n)
- Essential for quick exit processing
- Track all active parking sessions

#### Step 2.9: Return Ticket
```cpp
return ticket;
```

**What Happens:**
1. Return ticket pointer to caller
2. Caller now has ticket to unpark later

**Complete Park Flow Done!** ✅

### Park Flow Summary

```
User → parkVehicle(car)
  → Get vehicle type
  → Search all floors for available CAR spot
  → Find first available spot (Spot 3)
  → Mark spot as occupied
  → Store vehicle in spot
  → Generate unique ticket ID
  → Create ticket with entry time
  → Store ticket in map for lookup
  → Return ticket to user
```

**Data Structures Updated:**
1. ✅ ParkingSpot: occupied = true, parkedVehicle set
2. ✅ activeTickets map: New entry added
3. ✅ ticketCounter: Incremented

---

## 3. Unpark Vehicle Flow

### Overview
User returns with ticket and wants to exit.

### Step-by-Step Execution

#### Input
```cpp
double fee = parkingLot.unparkVehicle("TICKET-0001");
```

#### Step 3.1: Lookup Ticket
```cpp
auto it = activeTickets.find(ticketId);
```

**What Happens:**
1. Map search for key "TICKET-0001"
2. Returns iterator pointing to found element (or end() if not found)
3. Time Complexity: O(log n)

**Search Process:**
```
Map (Red-Black Tree):
       "TICKET-0002"
       /           \
"TICKET-0001"    "TICKET-0003"
     ↑
     Found!
```

#### Step 3.2: Validate Ticket
```cpp
if (it == activeTickets.end()) {
    return -1.0;  // Invalid ticket
}
```

**What Happens:**
- If iterator == end(), ticket not found
- Return error code -1.0
- If found, continue processing

#### Step 3.3: Extract Ticket Information
```cpp
Ticket* ticket = it->second;
ParkingSpot* spot = ticket->getSpot();
Vehicle* vehicle = ticket->getVehicle();
double duration = ticket->getDurationInHours();
```

**What Happens:**

1. **Get Ticket Object:**
   ```cpp
   Ticket* ticket = it->second;
   ```
   - Map iterator has pair<key, value>
   - `it->second` gives the value (Ticket pointer)

2. **Get Parking Spot:**
   ```cpp
   ParkingSpot* spot = ticket->getSpot();
   ```
   - Retrieves spot where vehicle is parked
   - Need this to mark spot as available later

3. **Get Vehicle:**
   ```cpp
   Vehicle* vehicle = ticket->getVehicle();
   ```
   - Retrieves parked vehicle
   - Need type for pricing

4. **Calculate Duration:**
   ```cpp
   double duration = ticket->getDurationInHours();
   ```
   
   **Duration Calculation Detailed:**
   ```cpp
   double Ticket::getDurationInHours() const {
       auto now = std::chrono::system_clock::now();          // Current time
       auto duration = std::chrono::duration_cast<std::chrono::minutes>(
           now - entryTime                                    // Time difference
       );
       return duration.count() / 60.0;                       // Convert to hours
   }
   ```
   
   **Example:**
   - Entry time: 10:00 AM
   - Exit time (now): 11:30 AM
   - Difference: 90 minutes
   - Duration: 90 / 60.0 = 1.5 hours

**Extracted Data:**
```
ticket: → [Ticket "TICKET-0001"]
spot: → [Spot 3, CAR, occupied, with car]
vehicle: → [Car "CAR-ABC-123"]
duration: 1.5 hours
```

#### Step 3.4: Calculate Fee
```cpp
double fee = pricingStrategy->calculatePrice(vehicle->getType(), duration);
```

**What Happens:**

1. **Get Vehicle Type:**
   ```cpp
   vehicle->getType()  // Returns: VehicleType::CAR
   ```

2. **Call Pricing Strategy:**
   ```cpp
   pricingStrategy->calculatePrice(VehicleType::CAR, 1.5)
   ```

3. **Strategy Execution** (SimplePricingStrategy):
   ```cpp
   double SimplePricingStrategy::calculatePrice(
       VehicleType vehicleType, 
       double durationInHours
   ) const {
       // Round up to nearest hour
       int hours = static_cast<int>(std::ceil(durationInHours));
       // 1.5 → 2 hours
       
       if (hours < 1) hours = 1;  // Minimum 1 hour
       
       double hourlyRate = 0.0;
       switch (vehicleType) {
           case VehicleType::CAR:
               hourlyRate = 5.0;  // $5/hour for cars
               break;
           // ... other cases
       }
       
       return hourlyRate * hours;  // $5 * 2 = $10
   }
   ```

**Calculation Flow:**
```
Duration: 1.5 hours
   ↓
Round up: 2 hours
   ↓
Vehicle type: CAR → Rate: $5/hour
   ↓
Fee: 2 * $5 = $10.00
```

**SOLID Principle Applied:**
- **Strategy Pattern (OCP + DIP)**: Pricing logic encapsulated in strategy
- Can swap strategies without changing service code
- Easy to add new pricing algorithms

#### Step 3.5: Free Parking Spot
```cpp
spot->unparkVehicle();
```

**What Happens:**
```cpp
void ParkingSpot::unparkVehicle() {
    parkedVehicle = nullptr;  // Remove vehicle reference
    occupied = false;          // Mark as available
}
```

**Memory State Change:**
```
Before:
  [Spot 3]
    - spotNumber: 3
    - spotType: CAR
    - occupied: true
    - parkedVehicle: → [Car]

After:
  [Spot 3]
    - spotNumber: 3
    - spotType: CAR
    - occupied: false ✓
    - parkedVehicle: nullptr ✓
```

**Spot Now Available for Next Vehicle!**

#### Step 3.6: Remove Ticket from Active Tickets
```cpp
activeTickets.erase(it);
```

**What Happens:**
1. Remove entry from map
2. O(log n) operation
3. Ticket no longer valid for future lookups

**Map State Change:**
```
Before:
  {
    "TICKET-0001" → [Ticket 1]
    "TICKET-0002" → [Ticket 2]
    "TICKET-0003" → [Ticket 3]
  }

After:
  {
    "TICKET-0002" → [Ticket 2]
    "TICKET-0003" → [Ticket 3]
  }
```

#### Step 3.7: Clean Up Ticket Memory
```cpp
delete ticket;
```

**What Happens:**
1. Deallocate ticket memory from heap
2. Prevents memory leak
3. Ticket object destroyed

**Memory Management:**
```
Before:
  Heap: [Ticket 1] [Ticket 2] [Ticket 3]

After:
  Heap: [Ticket 2] [Ticket 3]
        ↑ Ticket 1 memory freed
```

**Important:** 
- Vehicle object NOT deleted (user owns it)
- Only ticket deleted (parking lot owns tickets)

#### Step 3.8: Return Fee
```cpp
return fee;
```

**What Happens:**
1. Return calculated fee to caller
2. User pays this amount

**Complete Unpark Flow Done!** ✅

### Unpark Flow Summary

```
User → unparkVehicle("TICKET-0001")
  → Lookup ticket in map
  → Validate ticket exists
  → Extract spot, vehicle, duration
  → Calculate parking duration in hours
  → Use pricing strategy to calculate fee
  → Free up parking spot
  → Remove ticket from active tickets
  → Delete ticket object
  → Return fee to user
```

**Data Structures Updated:**
1. ✅ ParkingSpot: occupied = false, parkedVehicle = nullptr
2. ✅ activeTickets map: Entry removed
3. ✅ Heap: Ticket memory freed

---

## 4. Display Status Flow

### Overview
Show current state of parking lot.

### Step-by-Step Execution

#### Input
```cpp
parkingLot.displayStatus();
```

#### Step 4.1: Display Header
```cpp
std::cout << "\n=== PARKING LOT STATUS ===\n" << std::endl;
```

#### Step 4.2: Iterate Through Floors
```cpp
for (const auto& floor : floors) {
    // Display floor information
}
```

**What Happens:**
- Loop through all floors in vector
- For each floor, display its status

#### Step 4.3: Display Floor Information
```cpp
std::cout << "Floor " << floor->getFloorNumber() << ":" << std::endl;
std::cout << "  Total Spots: " << floor->getTotalSpots() << std::endl;
```

**getTotalSpots() Implementation:**
```cpp
int ParkingFloor::getTotalSpots() const {
    return spots.size();  // Vector size
}
```

#### Step 4.4: Count Available Spots by Type
```cpp
std::cout << "  Available - Bikes: " << floor->getAvailableSpots(VehicleType::BIKE)
         << " | Cars: " << floor->getAvailableSpots(VehicleType::CAR)
         << " | Trucks: " << floor->getAvailableSpots(VehicleType::TRUCK);
```

**getAvailableSpots() Implementation:**
```cpp
int ParkingFloor::getAvailableSpots(VehicleType vehicleType) const {
    int count = 0;
    for (const auto& spot : spots) {
        if (spot->canParkVehicle(vehicleType)) {
            count++;
        }
    }
    return count;
}
```

**Example Execution:**

Floor 0, checking available CAR spots:
```
Spot 1 (BIKE, empty): canParkVehicle(CAR) = false (type mismatch)
Spot 2 (BIKE, empty): canParkVehicle(CAR) = false (type mismatch)
Spot 3 (CAR, occupied): canParkVehicle(CAR) = false (occupied)
Spot 4 (CAR, empty): canParkVehicle(CAR) = true ✓ count++
Spot 5 (TRUCK, empty): canParkVehicle(CAR) = false (type mismatch)

Result: 1 available CAR spot
```

#### Step 4.5: Display Active Tickets
```cpp
std::cout << "Active Tickets: " << activeTickets.size() << "\n";
```

**What Happens:**
- Count entries in map
- Each entry = one parked vehicle

**Display Status Complete!** ✅

---

## 5. Error Handling Flows

### 5.1 Parking Lot Full Scenario

#### Flow:
```cpp
Vehicle* car = new Car("CAR-FULL-999");
Ticket* ticket = parkingLot.parkVehicle(car);

if (ticket == nullptr) {
    // No spot available!
}
```

**What Happens:**

1. **Search All Floors:**
   ```
   Floor 0: Check all spots
     - Spot 1 (BIKE): occupied
     - Spot 2 (BIKE): occupied
     - Spot 3 (CAR): occupied
     - Spot 4 (CAR): occupied ← All CAR spots full!
     - Spot 5 (TRUCK): occupied
   → findAvailableSpot() returns nullptr
   
   Floor 1: Check all spots
     - Spot 6 (BIKE): occupied
     - Spot 7 (CAR): occupied
     - Spot 8 (CAR): occupied ← All CAR spots full!
   → findAvailableSpot() returns nullptr
   ```

2. **Loop Completes Without Finding Spot:**
   ```cpp
   for (ParkingFloor* floor : floors) {
       ParkingSpot* spot = floor->findAvailableSpot(type);
       if (spot != nullptr) {
           // Never enters this block
       }
   }
   // Falls through
   return nullptr;  // No spots available
   ```

3. **Caller Handles:**
   ```cpp
   if (ticket == nullptr) {
       std::cout << "Parking lot is full!" << std::endl;
       delete car;  // Must clean up vehicle
   }
   ```

**Key Points:**
- Graceful degradation: No crash, just return nullptr
- Caller responsible for checking return value
- Must delete vehicle since it wasn't parked

### 5.2 Invalid Ticket Scenario

#### Flow:
```cpp
double fee = parkingLot.unparkVehicle("INVALID-9999");

if (fee < 0) {
    // Invalid ticket!
}
```

**What Happens:**

1. **Map Lookup:**
   ```cpp
   auto it = activeTickets.find("INVALID-9999");
   ```
   - Searches map for key "INVALID-9999"
   - Not found!

2. **Check Result:**
   ```cpp
   if (it == activeTickets.end()) {
       return -1.0;  // Error code
   }
   ```
   - Iterator equals end() (not found)
   - Return error code immediately

3. **Caller Handles:**
   ```cpp
   if (fee < 0) {
       std::cout << "Invalid ticket!" << std::endl;
   }
   ```

**Key Points:**
- No exceptions thrown (simple error handling)
- Negative fee = error indicator
- Better approach for production: use std::optional or throw exception

### 5.3 Type Mismatch Scenario

#### Scenario: Try to park Truck in Bike spot

**What Happens:**
```cpp
Spot (BIKE, empty).canParkVehicle(TRUCK):
  - !occupied: true ✓ (spot is empty)
  - spotType == vehicleType: BIKE == TRUCK → false ✗
  - Result: false (can't park)
```

**System Behavior:**
- Skips this spot
- Continues searching
- Finds appropriate TRUCK spot (if available)
- Or returns nullptr if no TRUCK spots available

**Type Safety Ensures:**
- Small vehicles don't take large spots (inefficient)
- Large vehicles don't fit in small spots (impossible)

---

## 📊 Complete System State Diagram

```
Initial State:
  Floors: [Floor 0, Floor 1]
  Spots: All empty
  activeTickets: {}
  ticketCounter: 1

After Parking Car 1:
  Floors: [Floor 0 (1 CAR spot occupied), Floor 1]
  Spots: Spot 3 has Car 1
  activeTickets: {"TICKET-0001": Ticket1}
  ticketCounter: 2

After Parking Car 2:
  Floors: [Floor 0 (2 CAR spots occupied), Floor 1]
  Spots: Spot 3 has Car 1, Spot 4 has Car 2
  activeTickets: {"TICKET-0001": Ticket1, "TICKET-0002": Ticket2}
  ticketCounter: 3

After Unparking Car 1:
  Floors: [Floor 0 (1 CAR spot occupied), Floor 1]
  Spots: Spot 3 empty, Spot 4 has Car 2
  activeTickets: {"TICKET-0002": Ticket2}
  ticketCounter: 3 (unchanged)
```

---

## 🎯 Key Takeaways

### Data Flow
1. **Park**: User → Service → Floor → Spot → Ticket → User
2. **Unpark**: User → Service → Map → Ticket → Strategy → Fee → User

### Memory Management
- Service owns: Floors, Tickets
- User owns: Vehicles
- Proper cleanup in destructors

### Time Complexities
- Park: O(F × S) - search all spots
- Unpark: O(log N) - map lookup
- Display: O(F × S) - check all spots

### SOLID in Action
- **SRP**: Each class one responsibility
- **OCP**: Extend via inheritance/interfaces
- **LSP**: Derived classes substitutable
- **ISP**: Focused interfaces
- **DIP**: Depend on abstractions

---

## 🎤 Interview Explanation Template

"Let me walk you through how parking a vehicle works:

1. First, we receive a Vehicle pointer - could be Car, Bike, or Truck due to polymorphism
2. We extract the vehicle type to know what kind of spot we need
3. We iterate through all floors, asking each to find an available spot of that type
4. Each floor checks its spots linearly - looking for empty spots matching the vehicle type
5. When we find a spot, we mark it occupied and store the vehicle pointer
6. We generate a unique ticket ID using an incrementing counter
7. We create a ticket object that captures: vehicle, spot, and current time
8. We store the ticket in a map for quick lookup during exit
9. We return the ticket to the user

For unparking, we reverse the process: look up the ticket, calculate duration, use our pricing strategy to compute the fee, free the spot, and return the amount."

---

This completes the detailed flow explanation! Every step is now documented with memory states, data structures, and SOLID principles highlighted. Perfect for interviews! 🚀
