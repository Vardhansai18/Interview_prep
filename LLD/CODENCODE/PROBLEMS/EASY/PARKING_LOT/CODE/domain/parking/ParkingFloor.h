#ifndef PARKING_FLOOR_H
#define PARKING_FLOOR_H

#include <string>
#include <vector>
#include <memory>
#include "ParkingSpot.h"

namespace parkinglot {
namespace domain {
namespace parking {

class ParkingFloor {
private:
    std::string floorId;
    std::vector<std::shared_ptr<ParkingSpot>> parkingSpots;

public:
    ParkingFloor(const std::string& floorId, 
                 const std::vector<std::shared_ptr<ParkingSpot>>& parkingSpots);
    
    // Return copy of parking spots to prevent external modification
    std::vector<std::shared_ptr<ParkingSpot>> getParkingSpots() const;
    std::string getFloorId() const;
};

} // namespace parking
} // namespace domain
} // namespace parkinglot

#endif // PARKING_FLOOR_H
