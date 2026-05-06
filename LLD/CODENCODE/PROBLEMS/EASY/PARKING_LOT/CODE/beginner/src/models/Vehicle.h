#ifndef VEHICLE_H
#define VEHICLE_H

#include <string>
#include "VehicleType.h"

/**
 * Vehicle Class (Base Class)
 * 
 * Purpose: Represents any vehicle that can park
 * 
 * SOLID Principles Applied:
 * 
 * 1. Single Responsibility Principle (SRP):
 *    - Only responsible for storing vehicle information
 *    - Doesn't handle parking logic (that's for ParkingLotService)
 * 
 * 2. Open/Closed Principle (OCP):
 *    - Open for extension: Can create Car, Bike, Truck subclasses
 *    - Closed for modification: No need to change Vehicle class
 * 
 * 3. Liskov Substitution Principle (LSP):
 *    - Any subclass (Car, Bike) can replace Vehicle without breaking code
 * 
 * Design Decision:
 * - Made destructor virtual for proper cleanup in inheritance
 * - Used const methods for getters (can't modify object)
 */

class Vehicle {
protected:
    std::string licensePlate;  // Unique identifier for vehicle
    VehicleType type;           // Type of vehicle (BIKE, CAR, TRUCK)

public:
    // Constructor: Initialize vehicle with license plate and type
    Vehicle(const std::string& plate, VehicleType vehicleType)
        : licensePlate(plate), type(vehicleType) {}
    
    // Virtual destructor: Important for proper cleanup in inheritance
    virtual ~Vehicle() = default;
    
    // Getters: Retrieve vehicle information
    // const: Promise not to modify the object
    std::string getLicensePlate() const { return licensePlate; }
    VehicleType getType() const { return type; }
};

#endif // VEHICLE_H
