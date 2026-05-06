# 📊 System Architecture & Diagrams

Visual representations of the Parking Lot System architecture, class relationships, and flow diagrams.

---

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER                                  │
│                   (Drives Vehicle)                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 ParkingLotService                            │
│              (Business Logic Layer)                          │
│                                                              │
│  • parkVehicle()                                            │
│  • unparkVehicle()                                          │
│  • displayStatus()                                          │
└──────┬───────────────────────┬──────────────────────────────┘
       │                       │
       │                       │ uses
       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐
│  ParkingFloor   │    │ PricingStrategy  │
│   (Collection)  │    │   (Interface)    │
│                 │    │                  │
│  • Floor 0      │    └────────┬─────────┘
│  • Floor 1      │             │
│  • Floor 2      │             │ implements
└────────┬────────┘             ▼
         │              ┌────────────────────┐
         │ contains     │SimplePricingStrategy│
         ▼              └────────────────────┘
┌─────────────────┐
│  ParkingSpot    │
│  (Individual)   │
│                 │
│  • Spot 1       │
│  • Spot 2       │
│  • Spot 3       │
└────────┬────────┘
         │ holds
         ▼
┌─────────────────┐
│    Vehicle      │
│  (Inheritance)  │
│                 │
│  ├─ Car         │
│  ├─ Bike        │
│  └─ Truck       │
└─────────────────┘
```

---

## 🔷 Class Diagram

```
┌───────────────────────────────────────────────────────────────┐
│                      Class Relationships                       │
└───────────────────────────────────────────────────────────────┘

┌──────────────────┐
│  VehicleType     │
│   <<enum>>       │
├──────────────────┤
│ + BIKE           │
│ + CAR            │
│ + TRUCK          │
└──────────────────┘
         ▲
         │ uses
         │
┌────────┴──────────┐
│     Vehicle       │ ◄────────────────┐
├───────────────────┤                  │
│ - licensePlate    │                  │
│ - type            │                  │ is-a
├───────────────────┤                  │
│ + getLicensePlate()│                 │
│ + getType()       │                  │
└───────────────────┘                  │
         ▲                             │
         │                             │
   ┌─────┴─────┬─────────┐            │
   │           │         │            │
   │           │         │            │
┌──┴────┐  ┌──┴────┐  ┌─┴─────┐      │
│  Bike │  │  Car  │  │ Truck │      │
└───────┘  └───────┘  └───────┘      │
                                      │
                                      │
┌─────────────────────────────────────┤
│        ParkingSpot                  │
├─────────────────────────────────────┤
│ - spotNumber                        │
│ - spotType: VehicleType             │
│ - occupied: bool                    │
│ - parkedVehicle: Vehicle*  ─────────┘
├─────────────────────────────────────┤
│ + parkVehicle(Vehicle*)             │
│ + unparkVehicle()                   │
│ + canParkVehicle(): bool            │
└─────────────────────────────────────┘
         ▲
         │ contains many
         │
┌────────┴────────────────────────────┐
│        ParkingFloor                 │
├─────────────────────────────────────┤
│ - floorNumber: int                  │
│ - spots: vector<ParkingSpot*>       │
├─────────────────────────────────────┤
│ + addSpot(ParkingSpot*)             │
│ + findAvailableSpot(): ParkingSpot* │
│ + getAvailableSpots(): int          │
└─────────────────────────────────────┘
         ▲
         │ has many
         │
┌────────┴───────────────────────────────┐
│      ParkingLotService                 │
├────────────────────────────────────────┤
│ - floors: vector<ParkingFloor*>        │
│ - activeTickets: map<string, Ticket*>  │
│ - pricingStrategy: PricingStrategy* ───┐
│ - ticketCounter: int                   │
├────────────────────────────────────────┤
│ + parkVehicle(Vehicle*): Ticket*       │
│ + unparkVehicle(string): double        │
│ + displayStatus()                      │
└────────────────────────────────────────┘
                                          │
                                          │ depends on
                                          │
                              ┌───────────▼────────────┐
                              │   PricingStrategy      │
                              │     <<interface>>      │
                              ├────────────────────────┤
                              │ + calculatePrice():    │
                              │     double             │
                              └───────────▲────────────┘
                                          │
                                          │ implements
                                          │
                              ┌───────────┴────────────┐
                              │ SimplePricingStrategy  │
                              ├────────────────────────┤
                              │ - BIKE_RATE: 2.0       │
                              │ - CAR_RATE: 5.0        │
                              │ - TRUCK_RATE: 10.0     │
                              ├────────────────────────┤
                              │ + calculatePrice():    │
                              │     double             │
                              └────────────────────────┘

┌─────────────────────────────────────┐
│            Ticket                   │
├─────────────────────────────────────┤
│ - ticketId: string                  │
│ - vehicle: Vehicle*  ───────────────┼──> Vehicle
│ - spot: ParkingSpot*  ──────────────┼──> ParkingSpot
│ - entryTime: time_point             │
├─────────────────────────────────────┤
│ + getDurationInHours(): double      │
│ + getFormattedEntryTime(): string   │
└─────────────────────────────────────┘
```

---

## 🔄 Sequence Diagrams

### Park Vehicle Flow

```
User            Service         Floor           Spot          Ticket
 │                │               │               │              │
 │─parkVehicle──>│               │               │              │
 │   (Car)        │               │               │              │
 │                │               │               │              │
 │                │─getType()────>│               │              │
 │                │<─CAR──────────│               │              │
 │                │               │               │              │
 │                │─findSpot────>│               │              │
 │                │  (CAR)        │               │              │
 │                │               │               │              │
 │                │               │─canPark?────>│              │
 │                │               │  (CAR)        │              │
 │                │               │<─true─────────│              │
 │                │               │               │              │
 │                │<─Spot 3───────│               │              │
 │                │               │               │              │
 │                │───────────parkVehicle()─────>│              │
 │                │               │               │              │
 │                │               │               │─occupied=T──>│
 │                │               │               │─store Car──>│
 │                │               │               │              │
 │                │──────────────createTicket──────────────────>│
 │                │               │               │              │
 │                │<─────────────Ticket────────────────────────┤
 │                │               │               │              │
 │<─Ticket────────│               │               │              │
 │   (TICKET-001) │               │               │              │
```

### Unpark Vehicle Flow

```
User            Service         Ticket       Strategy         Spot
 │                │               │              │              │
 │─unparkVehicle─>│               │              │              │
 │ (TICKET-001)   │               │              │              │
 │                │               │              │              │
 │                │─lookupTicket─>│              │              │
 │                │<─Ticket───────┤              │              │
 │                │               │              │              │
 │                │─getDuration─>│              │              │
 │                │<─1.5 hrs──────┤              │              │
 │                │               │              │              │
 │                │─calculatePrice───────────────>│              │
 │                │  (CAR, 1.5hrs)│              │              │
 │                │               │              │              │
 │                │<─$10.00──────────────────────┤              │
 │                │               │              │              │
 │                │──────────────unparkVehicle()──────────────>│
 │                │               │              │              │
 │                │               │              │─occupied=F──>│
 │                │               │              │─vehicle=null>│
 │                │               │              │              │
 │                │─deleteTicket─>│              │              │
 │                │               │              │              │
 │<─$10.00────────│               │              │              │
```

---

## 🗂️ Data Structure Visualization

### ParkingLotService Internal State

```
ParkingLotService
├─ floors: vector
│   ├─ [0] → Floor 0
│   │   └─ spots: vector
│   │       ├─ [0] → Spot 1 (BIKE, empty)
│   │       ├─ [1] → Spot 2 (BIKE, empty)
│   │       ├─ [2] → Spot 3 (CAR, occupied, Car-ABC-123)
│   │       ├─ [3] → Spot 4 (CAR, empty)
│   │       └─ [4] → Spot 5 (TRUCK, empty)
│   │
│   └─ [1] → Floor 1
│       └─ spots: vector
│           ├─ [0] → Spot 6 (BIKE, empty)
│           ├─ [1] → Spot 7 (CAR, empty)
│           └─ [2] → Spot 8 (CAR, empty)
│
├─ activeTickets: map (Red-Black Tree)
│   ├─ "TICKET-0001" → Ticket (Bike-001, Spot 1, 10:00 AM)
│   ├─ "TICKET-0003" → Ticket (Car-ABC-123, Spot 3, 10:05 AM)
│   └─ "TICKET-0005" → Ticket (Truck-XYZ, Spot 5, 10:15 AM)
│
├─ pricingStrategy → SimplePricingStrategy
│   ├─ BIKE_RATE = $2/hr
│   ├─ CAR_RATE = $5/hr
│   └─ TRUCK_RATE = $10/hr
│
└─ ticketCounter = 6
```

---

## 💾 Memory Layout

```
Stack:
┌──────────────────────────────────────┐
│  main() stack frame                  │
├──────────────────────────────────────┤
│  parkingLot (ParkingLotService)      │
│    ├─ floors: vector                 │
│    ├─ activeTickets: map             │
│    ├─ pricingStrategy: pointer ──────┼─┐
│    └─ ticketCounter: 1               │ │
└──────────────────────────────────────┘ │
                                         │
Heap:                                    │
┌────────────────────────────────────────▼
│ SimplePricingStrategy object           │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ Floor 0 object                         │
│   └─ spots vector holding:             │
│       ├─ Spot 1 object ─> nullptr      │
│       ├─ Spot 2 object ─> nullptr      │
│       ├─ Spot 3 object ─> Car object   │
│       ├─ Spot 4 object ─> nullptr      │
│       └─ Spot 5 object ─> nullptr      │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ Floor 1 object                         │
│   └─ spots vector holding:             │
│       ├─ Spot 6 object ─> nullptr      │
│       ├─ Spot 7 object ─> nullptr      │
│       └─ Spot 8 object ─> nullptr      │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ Vehicle objects:                       │
│   ├─ Car("CAR-ABC-123")                │
│   ├─ Bike("BIKE-001")                  │
│   └─ Truck("TRUCK-XYZ-789")            │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│ Ticket objects:                        │
│   ├─ Ticket 1 (for Bike)               │
│   ├─ Ticket 2 (for Car)                │
│   └─ Ticket 3 (for Truck)              │
└────────────────────────────────────────┘
```

---

## 🎯 Design Pattern Visualization

### Strategy Pattern (Pricing)

```
             Client
      (ParkingLotService)
               │
               │ depends on
               │ abstraction
               ▼
      ┌────────────────┐
      │ Strategy       │◄───────── Interface
      │ <<interface>>  │           (Abstract)
      └────────────────┘
               ▲
               │ implements
      ┌────────┴────────┐
      │                 │
┌─────┴──────┐   ┌──────┴───────┐
│  Simple    │   │   Hourly     │
│  Pricing   │   │   Pricing    │
│  Strategy  │   │   Strategy   │
└────────────┘   └──────────────┘
    Concrete        Concrete
    Strategy        Strategy

At Runtime:
              ┌───────────────┐
              │   Service     │
              │               │
              │ strategy ─────┼──> SimplePricingStrategy
              └───────────────┘
                                   (Can be swapped!)
                                        │
                                        │ Changed to:
                                        ▼
              ┌───────────────┐     HourlyPricingStrategy
              │   Service     │
              │               │     (No code changes!)
              │ strategy ─────┼──> 
              └───────────────┘
```

### Inheritance Hierarchy (Vehicle)

```
                 ┌──────────┐
                 │ Vehicle  │  ◄── Base Class
                 │          │      (Abstract concept)
                 └────┬─────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
   ┌────▼───┐    ┌───▼────┐   ┌────▼────┐
   │  Bike  │    │  Car   │   │  Truck  │  ◄── Concrete
   └────────┘    └────────┘   └─────────┘      Classes

Polymorphism in Action:

   Vehicle* v1 = new Car("ABC");    ┐
   Vehicle* v2 = new Bike("XYZ");   ├─ All valid!
   Vehicle* v3 = new Truck("123");  ┘

   // All can be treated uniformly:
   v1->getLicensePlate();  ✓
   v2->getType();          ✓
   v3->getLicensePlate();  ✓
```

---

## 🔄 State Transition Diagram

### ParkingSpot State Machine

```
    ┌─────────────────┐
    │   AVAILABLE     │ ◄── Initial State
    │  occupied=false │
    │  vehicle=nullptr│
    └────────┬────────┘
             │
             │ parkVehicle()
             │
             ▼
    ┌─────────────────┐
    │   OCCUPIED      │
    │  occupied=true  │
    │  vehicle=Car*   │
    └────────┬────────┘
             │
             │ unparkVehicle()
             │
             ▼
    ┌─────────────────┐
    │   AVAILABLE     │
    │  occupied=false │
    │  vehicle=nullptr│
    └─────────────────┘
```

### Ticket Lifecycle

```
Vehicle Arrives
       │
       ▼
   ┌────────────┐
   │  CREATED   │ ◄── new Ticket()
   │            │     Entry time recorded
   └─────┬──────┘
         │
         │ Stored in map
         │
         ▼
   ┌────────────┐
   │   ACTIVE   │ ◄── In activeTickets map
   │            │     Vehicle parked
   └─────┬──────┘
         │
         │ User exits
         │
         ▼
   ┌────────────┐
   │   USED     │ ◄── Fee calculated
   │            │     Removed from map
   └─────┬──────┘
         │
         │ delete ticket
         │
         ▼
   ┌────────────┐
   │  DELETED   │ ◄── Memory freed
   └────────────┘
```

---

## 🧩 Component Dependencies

```
┌─────────────────────────────────────────────────────────┐
│                     Dependency Graph                     │
└─────────────────────────────────────────────────────────┘

Layer 1: Enums/Basic Types
┌──────────────┐
│ VehicleType  │ (No dependencies)
└──────────────┘

Layer 2: Domain Models
┌──────────┐         ┌──────────────┐
│ Vehicle  │◄────────┤ VehicleType  │
└────┬─────┘         └──────────────┘
     │
     │ inherited by
     │
     ├─ Car
     ├─ Bike
     └─ Truck

┌──────────────┐     ┌──────────┐     ┌──────────────┐
│ ParkingSpot  │────>│ Vehicle  │────>│ VehicleType  │
└──────────────┘     └──────────┘     └──────────────┘

┌──────────────┐     ┌──────────────┐
│ ParkingFloor │────>│ ParkingSpot  │
└──────────────┘     └──────────────┘

┌──────────┐         ┌──────────────┐     ┌──────────┐
│  Ticket  │────────>│ ParkingSpot  │────>│ Vehicle  │
└──────────┘         └──────────────┘     └──────────┘

Layer 3: Strategies
┌──────────────────┐
│ PricingStrategy  │◄─────┐ (Interface)
└────────┬─────────┘      │
         │                │ implements
         └─ SimplePricingStrategy

Layer 4: Services (Top Level)
┌────────────────────┐
│ ParkingLotService  │
└──────┬─────────────┘
       │
       ├────> ParkingFloor
       ├────> Ticket
       ├────> Vehicle
       └────> PricingStrategy
```

---

## 📦 Module Organization

```
beginner/
│
├── Core Domain (models/)
│   ├── VehicleType.h     ──┐
│   ├── Vehicle.h          │
│   ├── Car.h              ├─> Vehicle Hierarchy
│   ├── Bike.h             │
│   ├── Truck.h           ──┘
│   │
│   ├── ParkingSpot.h     ──┐
│   ├── ParkingFloor.h     ├─> Parking Structure
│   └── Ticket.h          ──┘
│
├── Business Logic (services/)
│   └── ParkingLotService.h ──> Orchestrator
│
└── Algorithms (strategies/)
    ├── PricingStrategy.h    ──> Interface
    └── SimplePricingStrategy.h ──> Implementation
```

---

## 🎯 SOLID Principles Mapped

```
┌───────────────────────────────────────────────────────────┐
│                  SOLID Principles Applied                 │
└───────────────────────────────────────────────────────────┘

S - Single Responsibility
├─ Vehicle: Only vehicle data
├─ ParkingSpot: Only spot state
├─ ParkingFloor: Only floor management
├─ Ticket: Only parking session data
├─ PricingStrategy: Only pricing logic
└─ ParkingLotService: Only orchestration

O - Open/Closed
├─ Vehicle hierarchy: Extend with Car, Bike, Truck
└─ PricingStrategy: Add new strategies without modification

L - Liskov Substitution
├─ Car, Bike, Truck → Can replace Vehicle
└─ All maintain base class contract

I - Interface Segregation
└─ PricingStrategy: Single focused method

D - Dependency Inversion
└─ Service → PricingStrategy interface (not concrete)
```

---

## 🎨 Visual Summary

```
╔═══════════════════════════════════════════════════════════╗
║              PARKING LOT SYSTEM OVERVIEW                  ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  📥 INPUT: Vehicle arrives                                ║
║      ↓                                                    ║
║  🏗️  SERVICE: Find spot, create ticket                   ║
║      ↓                                                    ║
║  🎫 OUTPUT: Ticket                                        ║
║                                                           ║
║  ⏱️  TIME PASSES                                          ║
║                                                           ║
║  📥 INPUT: Return with ticket                             ║
║      ↓                                                    ║
║  🏗️  SERVICE: Lookup, calculate fee, free spot           ║
║      ↓                                                    ║
║  💰 OUTPUT: Fee amount                                    ║
║                                                           ║
║  ✅ RESULT: Spot available for next vehicle              ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

This document provides visual representations to help understand the system architecture better. Use these diagrams when:
- Explaining the system in interviews
- Understanding relationships between classes
- Tracing execution flows
- Planning extensions

Happy learning! 🎨📊
