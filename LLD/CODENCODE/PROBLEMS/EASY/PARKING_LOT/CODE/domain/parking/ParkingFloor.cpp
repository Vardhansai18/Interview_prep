#include "ParkingFloor.h"

namespace parkinglot {
namespace domain {
namespace parking {

ParkingFloor::ParkingFloor(const std::string& floorId,
                           const std::vector<std::shared_ptr<ParkingSpot>>& parkingSpots)
    : floorId(floorId), parkingSpots(parkingSpots) {}

std::vector<std::shared_ptr<ParkingSpot>> ParkingFloor::getParkingSpots() const {
    // Return a copy to prevent external modification
    return parkingSpots;
}

std::string ParkingFloor::getFloorId() const {
    return floorId;
}

} // namespace parking
} // namespace domain
} // namespace parkinglot
