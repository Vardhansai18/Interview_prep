#include "Vehicle.h"

namespace parkinglot {
namespace domain {
namespace vehicle {

Vehicle::Vehicle(const std::string& vehicleNumber, VehicleType vehicleType)
    : vehicleNumber(vehicleNumber), vehicleType(vehicleType) {}

std::string Vehicle::getVehicleNumber() const {
    return vehicleNumber;
}

VehicleType Vehicle::getVehicleType() const {
    return vehicleType;
}

} // namespace vehicle
} // namespace domain
} // namespace parkinglot
