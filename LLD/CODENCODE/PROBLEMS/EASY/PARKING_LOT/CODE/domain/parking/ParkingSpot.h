#ifndef PARKING_SPOT_H
#define PARKING_SPOT_H

#include <string>
#include <mutex>
#include <memory>
#include "../vehicle/Vehicle.h"
#include "../vehicle/VehicleType.h"

namespace parkinglot {
namespace domain {
namespace parking {

using namespace parkinglot::domain::vehicle;

class ParkingSpot {
private:
    std::string id;
    VehicleType vehicleType;
    std::shared_ptr<Vehicle> vehicle;
    std::mutex spotMutex;

public:
    ParkingSpot(const std::string& id, VehicleType vehicleType);
    
    bool parkVehicle(std::shared_ptr<Vehicle> vehicle);
    void removeVehicle();
    bool isSpotAvailable() const;
    
    std::string getId() const;
    VehicleType getVehicleType() const;
};

} // namespace parking
} // namespace domain
} // namespace parkinglot

#endif // PARKING_SPOT_H
