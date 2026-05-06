#ifndef PARKING_SPOT_H
#define PARKING_SPOT_H

#include "VehicleType.h"
#include "Vehicle.h"
#include <memory>

/**
 * ParkingSpot Class
 * 
 * Purpose: Represents a single parking space
 * 
 * SOLID Principles Applied:
 * 
 * 1. Single Responsibility Principle (SRP):
 *    - Only manages: spot number, type, availability, current vehicle
 *    - Doesn't handle pricing or parking lot logic
 * 
 * 2. Open/Closed Principle (OCP):
 *    - Can extend to add: handicap spots, EV charging spots
 *    - Without breaking existing code
 * 
 * Key Design Decisions:
 * 
 * 1. Why store spotType?
 *    - Different vehicles need different spots
 *    - Bike spots smaller than truck spots
 *    - Ensures type safety (can't park truck in bike spot)
 * 
 * 2. Why use raw pointer for Vehicle*?
 *    - ParkingSpot doesn't own the vehicle (just references it)
 *    - Vehicle lifetime managed elsewhere
 *    - Simpler for beginners than shared_ptr
 * 
 * 3. Why track occupied status separately?
 *    - Quick availability check without null check
 *    - Clear intent in code
 *    - Could derive from parkedVehicle != nullptr, but explicit is clearer
 */

class ParkingSpot {
private:
    int spotNumber;              // Unique identifier for this spot
    VehicleType spotType;        // Type of vehicle this spot accepts
    bool occupied;               // Is spot currently occupied?
    Vehicle* parkedVehicle;      // Current vehicle (nullptr if empty)

public:
    // Constructor: Initialize empty parking spot
    ParkingSpot(int number, VehicleType type)
        : spotNumber(number), spotType(type), occupied(false), parkedVehicle(nullptr) {}
    
    // Getters
    int getSpotNumber() const { return spotNumber; }
    VehicleType getSpotType() const { return spotType; }
    bool isOccupied() const { return occupied; }
    Vehicle* getParkedVehicle() const { return parkedVehicle; }
    
    // Check if this spot can park given vehicle type
    bool canParkVehicle(VehicleType vehicleType) const {
        // Spot must be empty AND type must match
        return !occupied && spotType == vehicleType;
    }
    
    // Park a vehicle in this spot
    void parkVehicle(Vehicle* vehicle) {
        parkedVehicle = vehicle;
        occupied = true;
    }
    
    // Remove vehicle from this spot
    void unparkVehicle() {
        parkedVehicle = nullptr;
        occupied = false;
    }
};

#endif // PARKING_SPOT_H
