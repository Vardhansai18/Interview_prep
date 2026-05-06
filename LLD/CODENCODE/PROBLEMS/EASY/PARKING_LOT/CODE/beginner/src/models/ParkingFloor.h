#ifndef PARKING_FLOOR_H
#define PARKING_FLOOR_H

#include "ParkingSpot.h"
#include <vector>
#include <memory>

/**
 * ParkingFloor Class
 * 
 * Purpose: Represents one floor of the parking lot with multiple spots
 * 
 * SOLID Principles Applied:
 * 
 * 1. Single Responsibility:
 *    - Manages collection of parking spots on one floor
 *    - Provides methods to find available spots
 *    - Doesn't handle pricing or ticketing
 * 
 * 2. Open/Closed:
 *    - Can extend to add floor-specific features
 *    - Example: VIP section, reserved spots, floor capacity
 * 
 * Design Decisions:
 * 
 * 1. Why use vector<ParkingSpot*>?
 *    - Dynamic array for flexible spot management
 *    - Easy iteration to find available spots
 *    - Alternative: map<int, ParkingSpot*> for O(1) lookup by spot number
 * 
 * 2. Why separate findAvailableSpot()?
 *    - Reusable logic for different vehicle types
 *    - Can be optimized later (e.g., maintain available spot lists)
 *    - Clear single purpose
 * 
 * Future Enhancements:
 * - Cache available spots for faster lookup
 * - Priority zones (closer spots cost more)
 * - Reserved spots for specific users
 */

class ParkingFloor {
private:
    int floorNumber;                       // Floor identifier (0, 1, 2, ...)
    std::vector<ParkingSpot*> spots;       // All parking spots on this floor

public:
    // Constructor
    ParkingFloor(int number) : floorNumber(number) {}
    
    // Destructor: Clean up allocated spots
    ~ParkingFloor() {
        for (auto spot : spots) {
            delete spot;
        }
    }
    
    // Getters
    int getFloorNumber() const { return floorNumber; }
    const std::vector<ParkingSpot*>& getSpots() const { return spots; }
    
    // Add a parking spot to this floor
    void addSpot(ParkingSpot* spot) {
        spots.push_back(spot);
    }
    
    /**
     * Find an available spot for given vehicle type
     * 
     * Algorithm: Linear search (simple for beginners)
     * Time Complexity: O(n) where n = number of spots
     * 
     * Returns: Pointer to available spot, or nullptr if none found
     * 
     * Optimization Ideas:
     * - Maintain separate lists for each vehicle type
     * - Use priority queue for nearest spot
     * - Bitmap for quick availability check
     */
    ParkingSpot* findAvailableSpot(VehicleType vehicleType) {
        for (ParkingSpot* spot : spots) {
            if (spot->canParkVehicle(vehicleType)) {
                return spot;  // Return first available spot
            }
        }
        return nullptr;  // No spots available
    }
    
    /**
     * Get total spot count on this floor
     * Useful for capacity tracking
     */
    int getTotalSpots() const {
        return spots.size();
    }
    
    /**
     * Get available spot count for specific vehicle type
     * Useful for display to users
     */
    int getAvailableSpots(VehicleType vehicleType) const {
        int count = 0;
        for (const auto& spot : spots) {
            if (spot->canParkVehicle(vehicleType)) {
                count++;
            }
        }
        return count;
    }
};

#endif // PARKING_FLOOR_H
