#ifndef BIKE_H
#define BIKE_H

#include "Vehicle.h"

/**
 * Bike Class (Derived from Vehicle)
 * 
 * Purpose: Represents a motorcycle/bike
 * 
 * SOLID Principles Applied:
 * 
 * 1. Single Responsibility:
 *    - Only represents bike data
 *    - Separation of concerns maintained
 * 
 * 2. Open/Closed:
 *    - Can extend to add bike-specific features (e.g., hasHelmet)
 *    - Without modifying base Vehicle class
 * 
 * Future Extensions:
 * - Add engine capacity field
 * - Add electric vs gasoline type
 * - Different pricing for different bike types
 */

class Bike : public Vehicle {
public:
    // Constructor: Initialize bike with license plate
    explicit Bike(const std::string& plate)
        : Vehicle(plate, VehicleType::BIKE) {}
};

#endif // BIKE_H
