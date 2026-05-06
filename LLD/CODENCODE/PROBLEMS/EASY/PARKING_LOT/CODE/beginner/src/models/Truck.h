#ifndef TRUCK_H
#define TRUCK_H

#include "Vehicle.h"

/**
 * Truck Class (Derived from Vehicle)
 * 
 * Purpose: Represents a truck/large vehicle
 * 
 * SOLID Principles Applied:
 * 
 * 1. Single Responsibility:
 *    - Encapsulates truck-specific data
 * 
 * 2. Open/Closed:
 *    - Can extend for truck-specific features
 *    - Example: weightCapacity, numAxles, isRefrigerated
 * 
 * Future Considerations:
 * - Trucks might need multiple parking spots
 * - Higher parking fees
 * - Special parking zones for trucks
 * 
 * Interview Tip:
 * - Discuss how you'd handle multi-spot parking
 * - Could add: int getSpotsRequired() method
 * - Service layer would handle spot allocation logic
 */

class Truck : public Vehicle {
public:
    // Constructor: Initialize truck with license plate
    explicit Truck(const std::string& plate)
        : Vehicle(plate, VehicleType::TRUCK) {}
};

#endif // TRUCK_H
