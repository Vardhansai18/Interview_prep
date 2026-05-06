#ifndef CAR_H
#define CAR_H

#include "Vehicle.h"

/**
 * Car Class (Derived from Vehicle)
 * 
 * Purpose: Represents a car specifically
 * 
 * SOLID Principles Applied:
 * 
 * 1. Single Responsibility:
 *    - Only represents car-specific data
 *    - Currently simple, but could add car-specific fields (e.g., numDoors)
 * 
 * 2. Liskov Substitution:
 *    - Car can be used anywhere Vehicle is expected
 *    - Example: Vehicle* v = new Car("ABC123") ✓ Valid
 * 
 * Why Inheritance?
 * - Code reuse: Don't repeat licensePlate, type fields
 * - Polymorphism: Can treat all vehicles uniformly
 * - Extensibility: Easy to add car-specific behavior later
 * 
 * Interview Tip:
 * - Explain why you chose inheritance vs composition
 * - Here, Car "IS-A" Vehicle (inheritance makes sense)
 * - If we had "has-a" relationship, use composition instead
 */

class Car : public Vehicle {
public:
    // Constructor: Pass license plate to parent Vehicle constructor
    // VehicleType::CAR is automatically set
    explicit Car(const std::string& plate)
        : Vehicle(plate, VehicleType::CAR) {}
    
    // No additional methods needed for basic implementation
    // But could add: getNumDoors(), isConvertible(), etc.
};

#endif // CAR_H
