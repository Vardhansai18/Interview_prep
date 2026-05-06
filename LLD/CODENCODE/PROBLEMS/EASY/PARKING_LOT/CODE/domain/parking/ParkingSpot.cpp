#include "ParkingSpot.h"

namespace parkinglot {
namespace domain {
namespace parking {

ParkingSpot::ParkingSpot(const std::string& id, VehicleType vehicleType)
    : id(id), vehicleType(vehicleType), vehicle(nullptr) {}

bool ParkingSpot::parkVehicle(std::shared_ptr<Vehicle> vehicle) {
    std::lock_guard<std::mutex> lock(spotMutex);
    
    if (this->vehicle == nullptr && vehicleType == vehicle->getVehicleType()) {
        this->vehicle = vehicle;
        return true;
    }
    
    return false;
}

void ParkingSpot::removeVehicle() {
    std::lock_guard<std::mutex> lock(spotMutex);
    this->vehicle = nullptr;
}

bool ParkingSpot::isSpotAvailable() const {
    return vehicle == nullptr;
}

std::string ParkingSpot::getId() const {
    return id;
}

VehicleType ParkingSpot::getVehicleType() const {
    return vehicleType;
}

} // namespace parking
} // namespace domain
} // namespace parkinglot
